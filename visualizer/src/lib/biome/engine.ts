import {
	AmbientLight,
	BoxGeometry,
	Color,
	DataTexture,
	DirectionalLight,
	DoubleSide,
	Fog,
	Group,
	MathUtils,
	Mesh,
	PerspectiveCamera,
	PlaneGeometry,
	RepeatWrapping,
	RGBAFormat,
	Scene,
	ShaderMaterial,
	SRGBColorSpace,
	type Texture,
	TextureLoader,
	Vector3,
	Timer,
	WebGLRenderer
} from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { Sky } from 'three/addons/objects/Sky.js';
import { Water } from 'three/addons/objects/Water.js';
import type {
	BiomeEngineLike,
	BiomeViewState,
	LatticeBeing,
	RainDebugTelemetry,
	SeabedPreset
} from './types';
import { CausticsPipeline, applyCausticsToMaterial } from './caustics';
import { BiomeEngineWebGPU } from './engine-webgpu';
import {
	SEABED_PRESETS,
	buildFallbackNormalTexture,
	computeRippleBoost,
	BIOME_FOV,
	BIOME_NEAR,
	BIOME_FAR,
	BIOME_CLEAR_COLOR,
	BIOME_BG_COLOR,
	BIOME_FOG_COLOR,
	BIOME_FOG_NEAR,
	BIOME_FOG_FAR,
	BIOME_SKY_SCALE,
	BIOME_ORBIT_DAMPING,
	BIOME_MAX_POLAR
} from './engine-shared';
import { buildTerrainPlaneGeometry, createPopulationMesh, updatePopulationMesh } from './terrain';
import { BiomeRainSystem } from './rain-system';
import { biomeStore } from './store';
import { terrainVert, terrainFrag, dioramaVert, dioramaBaseFrag, dioramaFrameFrag } from './shaders';

export type { BiomeEngineLike } from './types';

function whitePixelTexture(): DataTexture {
	const t = new DataTexture(new Uint8Array([255, 255, 255, 255]), 1, 1, RGBAFormat);
	t.needsUpdate = true;
	return t;
}

function createTerrainMesh(
	size: number,
	segments: number,
	preset: SeabedPreset
): Mesh<PlaneGeometry, ShaderMaterial> {
	const geometry = buildTerrainPlaneGeometry(size, segments);
	const cols = SEABED_PRESETS[preset];
	const material = new ShaderMaterial({
		uniforms: {
			baseColor: { value: new Color(cols.base) },
			shallowColor: { value: new Color(cols.shallow) },
			seabedMap: { value: whitePixelTexture() },
			useSeabedMap: { value: 0.0 }
		},
		vertexShader: terrainVert,
		fragmentShader: terrainFrag,
		side: DoubleSide
	});
	return new Mesh(geometry, material);
}

export class BiomeEngine implements BiomeEngineLike {
	private renderer: WebGLRenderer;
	private scene = new Scene();
	private camera: PerspectiveCamera;
	private timer = new Timer();
	private mounted = false;

	private sun = new DirectionalLight('#ffffff', 2.1);
	private ambient = new AmbientLight('#7ba6f7', 0.22);
	private waterGroup = new Group();
	private terrain: Mesh<PlaneGeometry, ShaderMaterial>;
	private water: Water | null = null;
	private dioramaBase: Mesh;
	private dioramaFrame = new Group();
	private normalMap: Texture | null = null;
	private caustics: CausticsPipeline;
	private beings: ReturnType<typeof createPopulationMesh>;
	private underwaterObjects: Mesh[] = [];

	private controls: OrbitControls;
	private rippleBoost = 0;
	private sky: Sky | null = null;

	private seabedUrlLoaded: string | null = null;
	private seabedLoader: TextureLoader | null = null;

	private state: BiomeViewState;
	private waterTime = 0;
	private raf = 0;
	private onTick: ((delta: number) => void) | null = null;
	private onPointerRipple = (e: PointerEvent) => {
		const boost = computeRippleBoost(e, this.canvas, this.camera, this.water);
		if (boost > 0) this.rippleBoost = Math.min(this.rippleBoost + boost, 5.5);
	};
	private onWheel = (e: WheelEvent) => e.preventDefault();
	private _scratchVec3 = new Vector3();
	private _fog: Fog | null = null;
	private basePixelRatio = Math.min(window.devicePixelRatio, 2);
	private dynamicPixelRatio = this.basePixelRatio;
	private frameMsEma = 16.7;
	private slowFrameTicks = 0;
	private fastFrameTicks = 0;
	private rainPerfScale = 1;

	private rain: BiomeRainSystem;

	constructor(private canvas: HTMLCanvasElement, state: BiomeViewState) {
		this.state = state;
		this.beings = createPopulationMesh(state.terrain);
		this.renderer = new WebGLRenderer({
			canvas,
			antialias: true,
			alpha: false
		});
		this.renderer.setPixelRatio(this.dynamicPixelRatio);
		this.renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
		this.renderer.setClearColor(BIOME_CLEAR_COLOR);
		this.renderer.toneMappingExposure = 0.78;

		this.camera = new PerspectiveCamera(BIOME_FOV, canvas.clientWidth / canvas.clientHeight, BIOME_NEAR, BIOME_FAR);
		this.camera.position.set(168, 132, 168);

		this.controls = new OrbitControls(this.camera, this.canvas);
		this.controls.target.set(0, -12, 0);
		this.controls.enableDamping = true;
		this.controls.dampingFactor = BIOME_ORBIT_DAMPING;
		this.controls.minDistance = 46;
		this.controls.maxDistance = 620;
		this.controls.maxPolarAngle = BIOME_MAX_POLAR;
		this.controls.update();

		this.scene.add(this.sun);
		this.scene.add(this.ambient);
		this.sun.intensity = 2.4;
		this.ambient.intensity = 0.34;
		this.sun.position.set(170, 230, 150);
		if (state.water.fog) {
			this._fog = new Fog(BIOME_FOG_COLOR, BIOME_FOG_NEAR, BIOME_FOG_FAR);
			this.scene.fog = this._fog;
		}

		this.terrain = createTerrainMesh(state.terrain.size, state.terrain.segments, state.terrain.seabedPreset);
		this.terrain.receiveShadow = true;
		this.terrain.castShadow = false;
		this.scene.add(this.terrain);

		const baseSize = state.terrain.size * 1.06;
		this.dioramaBase = new Mesh(
			new BoxGeometry(baseSize, 18, baseSize),
			new ShaderMaterial({
				uniforms: {
					baseColor: { value: new Color('#16253a') },
					shallowColor: { value: new Color('#24415f') },
					seabedMap: { value: whitePixelTexture() },
					useSeabedMap: { value: 0.0 }
				},
				vertexShader: dioramaVert,
				fragmentShader: dioramaBaseFrag,
				side: DoubleSide
			})
		);
		this.dioramaBase.position.y = -34;
		this.scene.add(this.dioramaBase);

		const frameMat = new ShaderMaterial({
			uniforms: {
				baseColor: { value: new Color('#0b1624') },
				shallowColor: { value: new Color('#1f2f45') },
				seabedMap: { value: whitePixelTexture() },
				useSeabedMap: { value: 0.0 }
			},
			vertexShader: dioramaVert,
			fragmentShader: dioramaFrameFrag,
			side: DoubleSide
		});
		const railLength = state.terrain.size + 14;
		const railThickness = 4;
		const railHeight = 3.2;
		const north = new Mesh(new BoxGeometry(railLength, railHeight, railThickness), frameMat);
		const south = new Mesh(new BoxGeometry(railLength, railHeight, railThickness), frameMat);
		const east = new Mesh(new BoxGeometry(railThickness, railHeight, railLength), frameMat);
		const west = new Mesh(new BoxGeometry(railThickness, railHeight, railLength), frameMat);
		const edge = state.terrain.size / 2 + railThickness / 2;
		north.position.set(0, state.water.surfaceY + 1.3, -edge);
		south.position.set(0, state.water.surfaceY + 1.3, edge);
		east.position.set(edge, state.water.surfaceY + 1.3, 0);
		west.position.set(-edge, state.water.surfaceY + 1.3, 0);
		this.dioramaFrame.add(north, south, east, west);
		this.scene.add(this.dioramaFrame);

		this.scene.add(this.beings);
		this.underwaterObjects.push(this.terrain, this.beings as unknown as Mesh);

		this.caustics = new CausticsPipeline(state.caustics);
		this.initializeWater();
		this.syncSky();
		this.applySeabedTextureUrl(state.terrain.seabedTextureDataUrl);
		this.bindPointerRipples();

		this.rain = new BiomeRainSystem(state.rain);
		this.scene.add(this.rain.instancedRain);
		this.scene.add(this.rain.splashMesh);
	}

	private bindPointerRipples(): void {
		this.canvas.addEventListener('pointerdown', this.onPointerRipple);
		this.canvas.addEventListener('pointermove', this.onPointerRipple);
		this.canvas.addEventListener('wheel', this.onWheel, { passive: false });
	}

	private initializeWater(): void {
		const geometry = new PlaneGeometry(this.state.terrain.size, this.state.terrain.size, 1, 1);
		const normalMap = buildFallbackNormalTexture();
		this.normalMap = normalMap;

		if (this.water) {
			this.water.geometry.dispose();
			this.water.material.dispose();
			this.waterGroup.remove(this.water);
		}

		this.water = new Water(geometry, {
			textureWidth: this.state.water.textureWidth,
			textureHeight: this.state.water.textureHeight,
			waterNormals: normalMap,
			sunDirection: this.sun.position.clone().normalize(),
			sunColor: this.state.water.sunColor,
			waterColor: this.state.water.waterColor,
			distortionScale: this.state.water.distortionScale,
			fog: this.state.water.fog,
			alpha: this.state.water.alpha
		});

		this.water.rotation.x = -Math.PI / 2;
		this.water.position.y = this.state.water.surfaceY;
		this.waterGroup.add(this.water);
		this.scene.add(this.waterGroup);
	}

	private syncSky(): void {
		const wantSky =
			this.state.sky.enabled &&
			(!this.state.sky.respectPerformanceGate || window.devicePixelRatio <= 2);
		if (!wantSky) {
			if (this.sky) {
				this.scene.remove(this.sky);
				this.sky.geometry.dispose();
				(this.sky.material as ShaderMaterial).dispose();
				this.sky = null;
			}
			this.scene.background = new Color(BIOME_BG_COLOR);
			return;
		}
		if (!this.sky) {
			this.sky = new Sky();
			this.sky.scale.setScalar(BIOME_SKY_SCALE);
			this.scene.add(this.sky);
		}
		const mat = this.sky.material as ShaderMaterial;
		mat.uniforms.turbidity.value = this.state.sky.turbidity;
		mat.uniforms.rayleigh.value = this.state.sky.rayleigh;
		this._scratchVec3.copy(this.sun.position).normalize().multiplyScalar(400000);
		mat.uniforms.sunPosition.value.copy(this._scratchVec3);
		this.scene.background = null;
	}

	private applySeabedPreset(preset: SeabedPreset): void {
		const cols = SEABED_PRESETS[preset];
		this.terrain.material.uniforms.baseColor.value = new Color(cols.base);
		this.terrain.material.uniforms.shallowColor.value = new Color(cols.shallow);
	}

	private applySeabedTextureUrl(url: string | null): void {
		const mat = this.terrain.material;
		if (!url) {
			this.seabedUrlLoaded = null;
			mat.uniforms.useSeabedMap.value = 0.0;
			return;
		}
		if (url === this.seabedUrlLoaded) return;
		this.seabedUrlLoaded = url;
		if (!this.seabedLoader) this.seabedLoader = new TextureLoader();
		this.seabedLoader.load(
			url,
			(tex) => {
				tex.wrapS = RepeatWrapping;
				tex.wrapT = RepeatWrapping;
				tex.colorSpace = SRGBColorSpace;
				const prev = mat.uniforms.seabedMap.value as Texture;
				if (prev?.image && (prev.image as HTMLImageElement).width > 1) prev.dispose();
				mat.uniforms.seabedMap.value = tex;
				mat.uniforms.useSeabedMap.value = 1.0;
				mat.needsUpdate = true;
			},
			undefined,
			() => {
				mat.uniforms.useSeabedMap.value = 0.0;
			}
		);
	}

	private shouldRunCaustics(): boolean {
		if (!this.state.caustics.enabled || this.state.caustics.path !== 'env_march') return false;
		if (this.state.caustics.respectPerformanceGate && window.devicePixelRatio > 2) return false;
		return true;
	}

	async mount(onTick?: (delta: number) => void): Promise<void> {
		if (this.mounted) return;
		this.mounted = true;
		this.onTick = onTick ?? null;
		this.rain.setOverlayResolution(this.canvas.clientWidth, this.canvas.clientHeight);
		await this.rain.rebuild(
			this.terrain,
			this.state.water.surfaceY,
			this.state.terrain.size,
			this.state.rain
		);
		this.loop();
	}

	private loop = () => {
		if (!this.mounted) return;
		this.timer.update();
		const delta = this.timer.getDelta();
		const frameMs = delta * 1000;
		this.frameMsEma = this.frameMsEma * 0.9 + frameMs * 0.1;

		// Lightweight adaptive scaling for steadier frame pacing.
		if (this.frameMsEma > 24) {
			this.slowFrameTicks += 1;
			this.fastFrameTicks = 0;
		} else if (this.frameMsEma < 17) {
			this.fastFrameTicks += 1;
			this.slowFrameTicks = 0;
		} else {
			this.slowFrameTicks = 0;
			this.fastFrameTicks = 0;
		}
		if (this.slowFrameTicks > 10) {
			const nextRatio = Math.max(1, this.dynamicPixelRatio - 0.1);
			const nextRainScale = Math.max(0.55, this.rainPerfScale - 0.08);
			if (nextRatio !== this.dynamicPixelRatio) {
				this.dynamicPixelRatio = nextRatio;
				this.renderer.setPixelRatio(this.dynamicPixelRatio);
				this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight, false);
			}
			if (Math.abs(nextRainScale - this.rainPerfScale) > 0.01) {
				this.rainPerfScale = nextRainScale;
				this.rain.setPerformanceScale(this.rainPerfScale);
			}
			this.slowFrameTicks = 0;
		} else if (this.fastFrameTicks > 40) {
			const nextRatio = Math.min(this.basePixelRatio, this.dynamicPixelRatio + 0.1);
			const nextRainScale = Math.min(1, this.rainPerfScale + 0.05);
			if (nextRatio !== this.dynamicPixelRatio) {
				this.dynamicPixelRatio = nextRatio;
				this.renderer.setPixelRatio(this.dynamicPixelRatio);
				this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight, false);
			}
			if (Math.abs(nextRainScale - this.rainPerfScale) > 0.01) {
				this.rainPerfScale = nextRainScale;
				this.rain.setPerformanceScale(this.rainPerfScale);
			}
			this.fastFrameTicks = 0;
		}

		this.rippleBoost = Math.max(0, this.rippleBoost - delta * 2.2);
		const ripple = 1 + this.rippleBoost;

		if (!this.state.paused) {
			this.waterTime += delta * this.state.water.timeScale;
		}

		if (this.water?.material && 'uniforms' in this.water.material) {
			this.water.material.uniforms.time.value = this.waterTime;
			this.water.material.uniforms.sunDirection.value.copy(this.sun.position).normalize();
			const base = this.state.water.distortionScale;
			this.water.material.uniforms.distortionScale.value = base * ripple;
		}

		if (this.shouldRunCaustics()) {
			this.caustics.updateSettings(this.state.caustics);
			this._scratchVec3.copy(this.sun.position).normalize();
			this.caustics.update(
				this.renderer,
				this.scene,
				this.underwaterObjects,
				this.normalMap,
				this._scratchVec3
			);
			applyCausticsToMaterial(
				this.terrain.material,
				this.caustics.texture,
				this.state.caustics.intensity
			);
		}

		this.controls.update();
		this.rain.step(delta, this.state.paused);
		this.renderer.render(this.scene, this.camera);
		this.rain.renderOverlay(this.renderer);
		if (!this.state.paused) this.onTick?.(delta);
		this.raf = window.requestAnimationFrame(this.loop);
	};

	resize(width: number, height: number): void {
		if (width < 2 || height < 2) return;
		this.camera.aspect = width / height;
		this.camera.updateProjectionMatrix();
		this.renderer.setSize(width, height, false);
		this.rain.setOverlayResolution(width, height);
		this.controls.update();
	}

	updateState(state: BiomeViewState): void {
		const prev = this.state;
		const presetChanged = state.terrain.seabedPreset !== prev.terrain.seabedPreset;
		const sizeChanged =
			state.terrain.size !== prev.terrain.size ||
			state.terrain.segments !== prev.terrain.segments;
		const waterTexChanged =
			state.water.textureWidth !== prev.water.textureWidth ||
			state.water.textureHeight !== prev.water.textureHeight;

		this.state = state;

		const rainRebuild =
			state.rain.enabled !== prev.rain.enabled ||
			state.rain.mode !== prev.rain.mode ||
			state.rain.collisionDropCount !== prev.rain.collisionDropCount ||
			state.terrain.size !== prev.terrain.size ||
			state.terrain.segments !== prev.terrain.segments ||
			Math.abs(state.water.surfaceY - prev.water.surfaceY) > 0.01;
		this.rain.updateSettings(state.rain);
		if (rainRebuild) {
			void this.rain.rebuild(this.terrain, state.water.surfaceY, state.terrain.size, state.rain);
		}

		this.sun.color.set(state.water.sunColor);
		this.sun.position.set(
			state.water.sunDirection[0] * 160,
			Math.max(40, state.water.sunDirection[1] * 180),
			state.water.sunDirection[2] * 160
		);
		if (state.water.fog) {
			if (!this._fog) this._fog = new Fog(BIOME_FOG_COLOR, BIOME_FOG_NEAR, BIOME_FOG_FAR);
			this.scene.fog = this._fog;
		} else {
			this.scene.fog = null;
		}

		if (sizeChanged) {
			this.terrain.geometry.dispose();
			this.terrain.geometry = buildTerrainPlaneGeometry(state.terrain.size, state.terrain.segments);
			this.dioramaBase.geometry.dispose();
			this.dioramaBase.geometry = new BoxGeometry(state.terrain.size * 1.06, 18, state.terrain.size * 1.06);
			const edge = state.terrain.size / 2 + 2;
			const rails = this.dioramaFrame.children as Mesh[];
			if (rails[0]) {
				rails[0].geometry.dispose();
				rails[0].geometry = new BoxGeometry(state.terrain.size + 14, 3.2, 4);
				rails[0].position.set(0, state.water.surfaceY + 1.3, -edge);
			}
			if (rails[1]) {
				rails[1].geometry.dispose();
				rails[1].geometry = new BoxGeometry(state.terrain.size + 14, 3.2, 4);
				rails[1].position.set(0, state.water.surfaceY + 1.3, edge);
			}
			if (rails[2]) {
				rails[2].geometry.dispose();
				rails[2].geometry = new BoxGeometry(4, 3.2, state.terrain.size + 14);
				rails[2].position.set(edge, state.water.surfaceY + 1.3, 0);
			}
			if (rails[3]) {
				rails[3].geometry.dispose();
				rails[3].geometry = new BoxGeometry(4, 3.2, state.terrain.size + 14);
				rails[3].position.set(-edge, state.water.surfaceY + 1.3, 0);
			}
		}
		if (presetChanged || sizeChanged) {
			this.applySeabedPreset(state.terrain.seabedPreset);
		}

		this.applySeabedTextureUrl(state.terrain.seabedTextureDataUrl);

		if (this.water && waterTexChanged) {
			this.initializeWater();
		}

		if (this.water?.material && 'uniforms' in this.water.material) {
			this.water.material.uniforms.distortionScale.value = state.water.distortionScale;
			this.water.material.uniforms.alpha.value = state.water.alpha;
			(this.water.material.uniforms.waterColor.value as Color).set(state.water.waterColor);
			(this.water.material.uniforms.sunColor.value as Color).set(state.water.sunColor);
		}
		if (this.water) {
			this.water.position.y = state.water.surfaceY;
		}
		for (const rail of this.dioramaFrame.children as Mesh[]) rail.position.y = state.water.surfaceY + 1.3;

		this.syncSky();

		if (!this.shouldRunCaustics()) {
			applyCausticsToMaterial(this.terrain.material, null, 0);
		}
	}

	updateBeings(beings: LatticeBeing[]): void {
		updatePopulationMesh(this.beings, beings, this.state.terrain);
	}

	getRainDebugTelemetry(): RainDebugTelemetry | null {
		return this.rain.getRainDebugTelemetry();
	}

	nudgeCamera(dx: number, dy: number): void {
		this.controls.rotateLeft(dx * 0.012);
		this.controls.rotateUp(dy * 0.012);
		this.controls.update();
	}

	dispose(): void {
		this.mounted = false;
		if (this.raf) window.cancelAnimationFrame(this.raf);
		this.canvas.removeEventListener('pointerdown', this.onPointerRipple);
		this.canvas.removeEventListener('pointermove', this.onPointerRipple);
		this.canvas.removeEventListener('wheel', this.onWheel);
		this.controls.dispose();
		this.caustics.dispose();
		this.water?.geometry.dispose();
		this.water?.material.dispose();
		this.dioramaBase.geometry.dispose();
		(this.dioramaBase.material as ShaderMaterial).dispose();
		for (const rail of this.dioramaFrame.children as Mesh[]) {
			rail.geometry.dispose();
			(rail.material as ShaderMaterial).dispose();
		}
		this.terrain.geometry.dispose();
		this.terrain.material.dispose();
		const seabedTex = this.terrain.material.uniforms.seabedMap.value as Texture;
		const img = seabedTex?.image as { width?: number } | undefined;
		if (img && typeof img.width === 'number' && img.width > 1) seabedTex.dispose();
		this.beings.geometry.dispose();
		(this.beings.material as import('three').MeshStandardMaterial).dispose();
		if (this.sky) {
			this.sky.geometry.dispose();
			(this.sky.material as ShaderMaterial).dispose();
		}
		this.scene.remove(this.rain.instancedRain);
		this.scene.remove(this.rain.splashMesh);
		this.rain.dispose();
		this.renderer.dispose();
	}
}

export function createBiomeEngine(canvas: HTMLCanvasElement, state: BiomeViewState): BiomeEngineLike {
	// Keep renderer type stable on a single canvas to avoid context-type conflicts in hot-reload/dev.
	const hasWebGPU = typeof navigator !== 'undefined' && typeof navigator.gpu !== 'undefined';
	if (state.rendering.useWebGPU && hasWebGPU) {
		return new BiomeEngineWebGPU(canvas, state);
	}
	return new BiomeEngine(canvas, state);
}

export function spawnLocalBeings(count: number): LatticeBeing[] {
	const beings: LatticeBeing[] = [];
	const edge = Math.max(4, Math.ceil(Math.sqrt(count)));
	for (let i = 0; i < count; i++) {
		beings.push({
			id: `being-${i + 1}`,
			x: i % edge,
			y: Math.floor(i / edge),
			fitness: MathUtils.clamp(0.2 + Math.random() * 0.8, 0, 1),
			alive: Math.random() > 0.03
		});
	}
	return beings;
}

export function bindLocalClock(): void {
	biomeStore.patch({ clockMode: 'local', status: 'running' });
}
