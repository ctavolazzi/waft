import {
	AdditiveBlending,
	AmbientLight,
	Color,
	DataTexture,
	DirectionalLight,
	DoubleSide,
	Fog,
	Group,
	Mesh,
	MeshBasicMaterial,
	MeshStandardMaterial,
	PerspectiveCamera,
	PlaneGeometry,
	Raycaster,
	RGBAFormat,
	RepeatWrapping,
	Scene,
	SRGBColorSpace,
	LinearFilter,
	Vector3,
	Timer,
	UnsignedByteType,
	WebGPURenderer,
	Texture,
	TextureLoader
} from 'three/webgpu';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { SkyMesh } from 'three/addons/objects/SkyMesh.js';
import { WaterMesh } from 'three/addons/objects/WaterMesh.js';
import type { BiomeEngineLike, BiomeViewState, LatticeBeing } from './types';
import { buildTerrainPlaneGeometry, createPopulationMesh, updatePopulationMesh } from './terrain';
import {
	SEABED_PRESETS,
	computeRippleBoost,
	debugBiome,
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

// WebGPU uses three/webgpu DataTexture; re-import buildFallbackNormalTexture logic inline
// since it must use the webgpu-specific DataTexture constructor.
function buildFallbackNormals(): Texture {
	const width = 128;
	const height = 128;
	const data = new Uint8Array(width * height * 4);
	for (let y = 0; y < height; y++) {
		for (let x = 0; x < width; x++) {
			const i = (y * width + x) * 4;
			const wave =
				Math.sin((x / width) * Math.PI * 10) * 0.5 + Math.cos((y / height) * Math.PI * 12) * 0.5;
			data[i] = 127 + Math.floor(wave * 18);
			data[i + 1] = 127 + Math.floor(wave * 18);
			data[i + 2] = 255;
			data[i + 3] = 255;
		}
	}
	const texture = new DataTexture(data, width, height);
	texture.needsUpdate = true;
	texture.wrapS = RepeatWrapping;
	texture.wrapT = RepeatWrapping;
	texture.colorSpace = SRGBColorSpace;
	return texture;
}

/**
 * WebGPU spike: `WaterMesh` + `WebGPURenderer`. Caustics and the legacy `Water` shader are not ported here.
 */
export class BiomeEngineWebGPU implements BiomeEngineLike {
	private renderer: WebGPURenderer;
	private scene = new Scene();
	private camera: PerspectiveCamera;
	private timer = new Timer();
	private mounted = false;

	private sun = new DirectionalLight('#ffffff', 2.1);
	private ambient = new AmbientLight('#7ba6f7', 0.22);
	private waterGroup = new Group();
	private terrain: Mesh;
	private water: WaterMesh | null = null;
	private normalMap: Texture | null = null;
	private beings: ReturnType<typeof createPopulationMesh>;
	private controls: OrbitControls;
	private rippleBoost = 0;
	private onPointerRipple = (e: PointerEvent) => {
		const boost = computeRippleBoost(e, this.canvas, this.camera, this.water);
		if (boost > 0) this.rippleBoost = Math.min(this.rippleBoost + boost, 5.5);
	};
	private onWheel = (e: WheelEvent) => e.preventDefault();
	private _scratchVec3 = new Vector3();
	private _fog: Fog | null = null;
	private _bgColor = new Color(BIOME_BG_COLOR);

	private sky: SkyMesh | null = null;
	private seabedUrlLoaded: string | null = null;
	private seabedLoader: TextureLoader | null = null;
	private volumetricOverlay: Mesh | null = null;
	private volumetricTexture: DataTexture | null = null;
	private volumetricBytes = new Uint8Array(0);
	private volumetricRay = new Raycaster();
	private lastVolumetricUpdateMs = 0;
	private lastDebugLogMs = 0;

	private state: BiomeViewState;
	private onTick: ((delta: number) => void) | null = null;

	constructor(private canvas: HTMLCanvasElement, state: BiomeViewState) {
		this.state = state;
		this.renderer = new WebGPURenderer({ canvas, antialias: true, alpha: false });
		this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
		this.renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
		this.renderer.setClearColor(BIOME_CLEAR_COLOR, 1);
		debugBiome('[BiomeRuntime] webgpu-engine-constructed');

		this.camera = new PerspectiveCamera(BIOME_FOV, canvas.clientWidth / canvas.clientHeight, BIOME_NEAR, BIOME_FAR);
		this.camera.position.set(95, 80, 130);

		this.controls = new OrbitControls(this.camera, this.canvas);
		this.controls.target.set(0, 0, 0);
		this.controls.enableDamping = true;
		this.controls.dampingFactor = BIOME_ORBIT_DAMPING;
		this.controls.minDistance = 28;
		this.controls.maxDistance = 520;
		this.controls.maxPolarAngle = BIOME_MAX_POLAR;
		this.controls.update();

		this.scene.add(this.sun);
		this.scene.add(this.ambient);
		this.sun.position.set(130, 210, 110);
		this.scene.background = this._bgColor;
		if (state.water.fog && !state.volumetrics.enabled) {
			this._fog = new Fog(BIOME_FOG_COLOR, BIOME_FOG_NEAR, BIOME_FOG_FAR);
			this.scene.fog = this._fog;
		}

		this.beings = createPopulationMesh(state.terrain);
		this.terrain = this.buildTerrainMesh(state);
		this.terrain.receiveShadow = true;
		this.scene.add(this.terrain);
		this.scene.add(this.beings);

		this.initializeWater();
		this.syncSky();
		this.syncVolumetrics();
		this.applySeabedTextureUrl(state.terrain.seabedTextureDataUrl);

		this.canvas.addEventListener('pointerdown', this.onPointerRipple);
		this.canvas.addEventListener('pointermove', this.onPointerRipple);
		this.canvas.addEventListener('wheel', this.onWheel, { passive: false });
	}

	private shouldRunVolumetrics(): boolean {
		if (!this.state.rendering.useWebGPU) return false;
		if (!this.state.volumetrics.enabled) return false;
		if (this.state.volumetrics.respectPerformanceGate && window.devicePixelRatio > 2) return false;
		return true;
	}

	private disposeVolumetrics(): void {
		if (this.volumetricOverlay) {
			this.camera.remove(this.volumetricOverlay);
			this.volumetricOverlay.geometry.dispose();
			(this.volumetricOverlay.material as MeshBasicMaterial).dispose();
			this.volumetricOverlay = null;
		}
		this.volumetricTexture?.dispose();
		this.volumetricTexture = null;
		this.volumetricBytes = new Uint8Array(0);
	}

	private ensureVolumetrics(): void {
		const width = Math.max(48, Math.floor(this.state.volumetrics.froxelWidth));
		const height = Math.max(32, Math.floor(this.state.volumetrics.froxelHeight));
		const bytesNeeded = width * height * 4;
		if (this.volumetricBytes.length !== bytesNeeded) {
			this.volumetricBytes = new Uint8Array(bytesNeeded);
		}
		if (!this.volumetricTexture || this.volumetricTexture.image.width !== width || this.volumetricTexture.image.height !== height) {
			this.volumetricTexture?.dispose();
			this.volumetricTexture = new DataTexture(this.volumetricBytes, width, height, RGBAFormat, UnsignedByteType);
			this.volumetricTexture.minFilter = LinearFilter;
			this.volumetricTexture.magFilter = LinearFilter;
			this.volumetricTexture.needsUpdate = true;
		}
		if (!this.volumetricOverlay) {
			const near = this.camera.near + 0.02;
			const h = 2 * Math.tan((this.camera.fov * Math.PI) / 360) * near;
			const w = h * this.camera.aspect;
			const geometry = new PlaneGeometry(w, h, 1, 1);
			const material = new MeshBasicMaterial({
				map: this.volumetricTexture,
				transparent: true,
				blending: AdditiveBlending,
				depthWrite: false,
				depthTest: false,
				fog: false
			});
			material.toneMapped = false;
			this.volumetricOverlay = new Mesh(geometry, material);
			this.volumetricOverlay.position.z = -near;
			this.volumetricOverlay.renderOrder = 1000;
			this.camera.add(this.volumetricOverlay);
			this.scene.add(this.camera);
		}
	}

	private estimateSunVisibility(): number {
		const toSun = this._scratchVec3.copy(this.sun.position).sub(this.camera.position).normalize();
		this.volumetricRay.set(this.camera.position, toSun);
		const hits = this.volumetricRay.intersectObject(this.terrain, false);
		if (!hits.length) return 1;
		const distHit = hits[0]?.distance ?? Infinity;
		const sunDist = this.sun.position.distanceTo(this.camera.position);
		return distHit < sunDist ? 0.22 : 1;
	}

	private updateVolumetricTexture(): void {
		if (!this.volumetricTexture) return;
		const now = performance.now();
		if (now - this.lastVolumetricUpdateMs < 33) return;
		this.lastVolumetricUpdateMs = now;

		const w = this.volumetricTexture.image.width;
		const h = this.volumetricTexture.image.height;
		const density = Math.max(0, this.state.volumetrics.density);
		const anisotropy = Math.max(0, Math.min(0.95, this.state.volumetrics.anisotropy));
		const heightFalloff = Math.max(0.01, this.state.volumetrics.heightFalloff);
		const sunVis = this.estimateSunVisibility();
		// _scratchVec3 was set by estimateSunVisibility; recompute for local use
		const toSun = this._scratchVec3.copy(this.sun.position).sub(this.camera.position).normalize();
		const sunDx = toSun.x * 0.5 + 0.5;
		const sunDy = toSun.y * 0.5 + 0.5;

		let i = 0;
		for (let y = 0; y < h; y++) {
			const v = y / Math.max(1, h - 1);
			const fogHeight = Math.exp(-v * 4 * heightFalloff);
			const depthT = 1 - v;
			for (let x = 0; x < w; x++) {
				const u = x / Math.max(1, w - 1);
				const dx = u - sunDx;
				const dy = v - sunDy;
				const d2 = dx * dx + dy * dy;
				const shaft = Math.exp(-d2 * (35 - anisotropy * 18));
				const band = Math.sin((u * 54 + depthT * 90) + now * 0.0018) * 0.5 + 0.5;
				const scatter = Math.min(1, density * (0.2 + fogHeight * 0.8) * (0.25 + shaft * 0.75) * (0.7 + band * 0.3));
				const transmittance = Math.exp(-density * depthT * 2.2);
				const light = scatter * transmittance * sunVis;
				const r = Math.min(1, light * 0.85);
				const g = Math.min(1, light * 0.93);
				const b = Math.min(1, light * 1.1);
				const a = Math.min(1, scatter * 0.9);
				this.volumetricBytes[i++] = Math.floor(r * 255);
				this.volumetricBytes[i++] = Math.floor(g * 255);
				this.volumetricBytes[i++] = Math.floor(b * 255);
				this.volumetricBytes[i++] = Math.floor(a * 255);
			}
		}
		this.volumetricTexture.needsUpdate = true;
	}

	private syncVolumetrics(): void {
		const want = this.shouldRunVolumetrics();
		if (!want) {
			this.disposeVolumetrics();
			return;
		}
		this.ensureVolumetrics();
		this.updateVolumetricTexture();
		// Keep per-frame volumetric logging disabled to avoid console noise.
	}

	private buildTerrainMesh(state: BiomeViewState): Mesh {
		const geometry = buildTerrainPlaneGeometry(state.terrain.size, state.terrain.segments);
		const material = new MeshStandardMaterial({
			color: new Color(SEABED_PRESETS[state.terrain.seabedPreset].base),
			metalness: 0.05,
			roughness: 0.92,
			side: DoubleSide
		});
		return new Mesh(geometry, material);
	}

	private initializeWater(): void {
		const geometry = new PlaneGeometry(this.state.terrain.size, this.state.terrain.size, 1, 1);
		const normalMap = buildFallbackNormals();
		this.normalMap?.dispose();
		this.normalMap = normalMap;

		if (this.water) {
			this.water.geometry.dispose();
			this.waterGroup.remove(this.water);
		}

		this.water = new WaterMesh(geometry, {
			waterNormals: normalMap,
			sunColor: this.state.water.sunColor,
			sunDirection: this.sun.position.clone().normalize(),
			waterColor: this.state.water.waterColor,
			distortionScale: this.state.water.distortionScale,
			alpha: this.state.water.alpha,
			size: 1,
			resolutionScale: 0.45
		});

		this.water.rotation.x = -Math.PI / 2;
		this.water.position.y = this.state.water.surfaceY;
		this.waterGroup.add(this.water);
		this.scene.add(this.waterGroup);
	}

	private syncSky(): void {
		const wantSky =
			this.state.sky.enabled &&
			!this.state.volumetrics.enabled &&
			(!this.state.sky.respectPerformanceGate || window.devicePixelRatio <= 2);
		if (!wantSky) {
			if (this.sky) {
				this.scene.remove(this.sky);
				this.sky.geometry.dispose();
				this.sky = null;
			}
			return;
		}
		if (!this.sky) {
			this.sky = new SkyMesh();
			this.sky.scale.setScalar(BIOME_SKY_SCALE);
			this.scene.add(this.sky);
		}
		this.sky.turbidity.value = this.state.sky.turbidity;
		this.sky.rayleigh.value = this.state.sky.rayleigh;
		this._scratchVec3.copy(this.sun.position).normalize().multiplyScalar(400000);
		this.sky.sunPosition.value.copy(this._scratchVec3);
		this.scene.background = this._bgColor;
	}

	private applySeabedTextureUrl(url: string | null): void {
		const mat = this.terrain.material as MeshStandardMaterial;
		if (!url) {
			this.seabedUrlLoaded = null;
			mat.map?.dispose();
			mat.map = null;
			mat.needsUpdate = true;
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
				mat.map?.dispose();
				mat.map = tex;
				mat.needsUpdate = true;
			},
			undefined,
			() => {
				mat.map = null;
				mat.needsUpdate = true;
			}
		);
	}

	async mount(onTick?: (delta: number) => void): Promise<void> {
		if (this.mounted) return;
		this.mounted = true;
		this.onTick = onTick ?? null;
		await this.renderer.init();
		await this.renderer.setAnimationLoop(() => {
			if (!this.mounted) return;
			this.timer.update();
			const delta = this.timer.getDelta();
			this.rippleBoost = Math.max(0, this.rippleBoost - delta * 2.2);
			const ripple = 1 + this.rippleBoost;

			if (this.water) {
				this.water.sunDirection.value.copy(this.sun.position).normalize();
				this.water.distortionScale.value = this.state.water.distortionScale * ripple;
				this.water.alpha.value = this.state.water.alpha;
				this.water.waterColor.value.set(this.state.water.waterColor);
				this.water.sunColor.value.set(this.state.water.sunColor);
				this.water.position.y = this.state.water.surfaceY;
			}

			this.controls.update();
			this.syncVolumetrics();
			const beingsMaterial = this.beings.material as MeshStandardMaterial;
			const glowPulse = 1.2 + Math.sin(performance.now() * 0.004) * 0.55;
			beingsMaterial.emissive.set('#8fe7ff');
			beingsMaterial.emissiveIntensity = glowPulse;
			// Keep per-frame runtime logging disabled to avoid console noise.
			try {
				this.renderer.render(this.scene, this.camera);
			} catch (error) {
				this.mounted = false;
				void this.renderer.setAnimationLoop(null);
				console.error('[BiomeEngineWebGPU] render failed, stopping WebGPU loop', error);
				return;
			}
			if (!this.state.paused) this.onTick?.(delta);
		});
	}

	resize(width: number, height: number): void {
		if (width < 2 || height < 2) return;
		this.camera.aspect = width / height;
		this.camera.updateProjectionMatrix();
		this.renderer.setSize(width, height, false);
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
		this.sun.color.set(state.water.sunColor);
		this.sun.position.set(
			state.water.sunDirection[0] * 160,
			Math.max(40, state.water.sunDirection[1] * 180),
			state.water.sunDirection[2] * 160
		);
		if (state.water.fog && !state.volumetrics.enabled) {
			if (!this._fog) this._fog = new Fog(BIOME_FOG_COLOR, BIOME_FOG_NEAR, BIOME_FOG_FAR);
			this.scene.fog = this._fog;
		} else {
			this.scene.fog = null;
		}
		this.scene.background = this._bgColor;

		if (sizeChanged) {
			this.terrain.geometry.dispose();
			this.terrain.geometry = buildTerrainPlaneGeometry(state.terrain.size, state.terrain.segments);
		}
		if (presetChanged || sizeChanged) {
			(this.terrain.material as MeshStandardMaterial).color.set(SEABED_PRESETS[state.terrain.seabedPreset].base);
		}

		this.applySeabedTextureUrl(state.terrain.seabedTextureDataUrl);

		if (this.water && waterTexChanged) {
			this.initializeWater();
		}
		if (this.water && !waterTexChanged) {
			this.water.position.y = state.water.surfaceY;
		}

		this.syncSky();
		this.syncVolumetrics();
	}

	updateBeings(beings: LatticeBeing[]): void {
		updatePopulationMesh(this.beings, beings, this.state.terrain);
	}

	nudgeCamera(dx: number, dy: number): void {
		this.controls.rotateLeft(dx * 0.012);
		this.controls.rotateUp(dy * 0.012);
		this.controls.update();
	}

	dispose(): void {
		this.mounted = false;
		void this.renderer.setAnimationLoop(null);
		this.canvas.removeEventListener('pointerdown', this.onPointerRipple);
		this.canvas.removeEventListener('pointermove', this.onPointerRipple);
		this.canvas.removeEventListener('wheel', this.onWheel);
		this.controls.dispose();
		this.water?.geometry.dispose();
		this.waterGroup.removeFromParent();
		this.terrain.geometry.dispose();
		(this.terrain.material as MeshStandardMaterial).dispose();
		(this.terrain.material as MeshStandardMaterial).map?.dispose();
		this.beings.geometry.dispose();
		(this.beings.material as MeshStandardMaterial).dispose();
		if (this.sky) {
			this.sky.geometry.dispose();
		}
		this.disposeVolumetrics();
		this.normalMap?.dispose();
		this.renderer.dispose();
	}
}
