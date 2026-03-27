import RAPIER from '@dimforge/rapier3d-compat';
import {
	AdditiveBlending,
	DynamicDrawUsage,
	InstancedMesh,
	MathUtils,
	Matrix4,
	Mesh,
	MeshBasicMaterial,
	OrthographicCamera,
	PlaneGeometry,
	Quaternion,
	Scene,
	ShaderMaterial,
	SphereGeometry,
	Vector2,
	Vector3,
	type Mesh as ThreeMesh,
	type WebGLRenderer
} from 'three';
import type { RainDebugTelemetry, RainQuality, RainSettings } from './types';

const DROP_RADIUS = 0.14;
const KILL_Y = -120;
const SPLASH_LIFE = 0.42;
/** Fixed GPU pool sizes (rebuild only touches Rapier, not mesh allocation). */
const RAIN_MAX_DROPS = 2000;
const SPLASH_MAX = 128;
const PHYSICS_FIXED_DT = 1 / 60;
const PHYSICS_MAX_STEPS = 2;
/** Seconds: ignore duplicate splash spam for the same droplet slot. */
const SPLASH_COOLDOWN = 0.055;

const SPAWN_Y_MIN = 95;
const SPAWN_Y_SPAN = 65;

function terrainTrimeshArrays(terrainMesh: ThreeMesh): {
	vertices: Float32Array;
	indices: Uint32Array;
} | null {
	terrainMesh.updateWorldMatrix(true, false);
	const geom = terrainMesh.geometry.clone();
	geom.applyMatrix4(terrainMesh.matrixWorld);
	const pos = geom.getAttribute('position');
	if (!pos) return null;
	const n = pos.count;
	const vertices = new Float32Array(n * 3);
	for (let i = 0; i < n; i++) {
		vertices[i * 3] = pos.getX(i);
		vertices[i * 3 + 1] = pos.getY(i);
		vertices[i * 3 + 2] = pos.getZ(i);
	}
	let indices: Uint32Array;
	if (geom.index) {
		indices = new Uint32Array(geom.index.array);
	} else {
		indices = new Uint32Array(n);
		for (let i = 0; i < n; i++) indices[i] = i;
	}
	geom.dispose();
	return { vertices, indices };
}

/** Hybrid Rapier rain: instanced collision droplets + fullscreen streak shader + splash pool. */
export class BiomeRainSystem {
	instancedRain: InstancedMesh;
	splashMesh: InstancedMesh;
	readonly overlayScene = new Scene();
	private readonly overlayCam = new OrthographicCamera(-1, 1, 1, -1, 0, 2);
	private overlayQuad: Mesh;

	private world: RAPIER.World | null = null;
	private eventQueue: RAPIER.EventQueue | null = null;
	private rainBodies: RAPIER.RigidBody[] = [];
	private rainByCollider = new Map<number, number>();
	private splashSlots: Array<{ age: number; x: number; y: number; z: number; intensity: number }> =
		[];
	private dropSplashCooldownUntil = new Float32Array(RAIN_MAX_DROPS);
	private simTime = 0;
	private impactsAccum = 0;
	private telemetrySeconds = 0;
	private displayedImpactsPerSec = 0;
	private physicsAccumulator = 0;
	private performanceScale = 1;

	private tmpM = new Matrix4();
	private tmpP = new Vector3();
	private tmpQ = new Quaternion();
	private tmpS = new Vector3(1, 1, 1);
	private rapierInited = false;

	private dropCount = 0;
	private spawnRadius = 220;
	private settings: RainSettings;

	private applyProxyVisibility(): void {
		this.instancedRain.visible = this.settings.enabled && this.settings.showCollisionProxies;
	}

	constructor(initial: RainSettings) {
		this.settings = initial;
		this.instancedRain = new InstancedMesh(
			new SphereGeometry(DROP_RADIUS, 7, 7),
			new MeshBasicMaterial({
				color: 0x9ec9ff,
				transparent: true,
				opacity: 0.08,
				depthWrite: false
			}),
			RAIN_MAX_DROPS
		);
		this.instancedRain.instanceMatrix.setUsage(DynamicDrawUsage);
		this.instancedRain.count = 0;
		this.instancedRain.frustumCulled = false;
		this.instancedRain.name = 'biomeRainDrops';
		this.applyProxyVisibility();

		this.splashMesh = new InstancedMesh(
			new SphereGeometry(0.36, 6, 6),
			new MeshBasicMaterial({
				color: 0xc8e6ff,
				transparent: true,
				opacity: 0.72,
				depthWrite: false,
				blending: AdditiveBlending
			}),
			SPLASH_MAX
		);
		this.splashMesh.instanceMatrix.setUsage(DynamicDrawUsage);
		for (let i = 0; i < SPLASH_MAX; i++) {
			this.splashSlots.push({ age: SPLASH_LIFE + 1, x: 0, y: 0, z: 0, intensity: 1 });
			this.tmpS.setScalar(0);
			this.tmpM.compose(this.tmpP, this.tmpQ, this.tmpS);
			this.splashMesh.setMatrixAt(i, this.tmpM);
		}
		this.splashMesh.count = Math.min(SPLASH_MAX, Math.max(4, initial.maxActiveSplashes));
		this.splashMesh.instanceMatrix.needsUpdate = true;
		this.splashMesh.frustumCulled = false;
		this.splashMesh.name = 'biomeRainSplashes';

		this.overlayQuad = new Mesh(
			new PlaneGeometry(2, 2),
			new ShaderMaterial({
				depthTest: false,
				depthWrite: false,
				transparent: true,
				blending: AdditiveBlending,
				uniforms: {
					uTime: { value: 0 },
					uDensity: { value: initial.overlayDensity },
					uResolution: { value: new Vector2(1, 1) }
				},
				vertexShader: `
					void main() {
						gl_Position = vec4(position.xy, 0.0, 1.0);
					}
				`,
				fragmentShader: `
					uniform float uTime;
					uniform float uDensity;
					uniform vec2 uResolution;
					float hash(vec2 p) {
						return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
					}
					void main() {
						vec2 uv = gl_FragCoord.xy / uResolution.xy;
						float dens = clamp(uDensity, 0.0, 1.0);
						float y = uv.y * mix(110.0, 190.0, dens);
						float wind = uTime * 0.35;
						float streak = 0.0;
						for (float k = 0.0; k < 4.0; k++) {
							vec2 cell = vec2(uv.x * mix(90.0, 160.0, dens) + wind * 0.15 + k * 13.7, y + uTime * mix(28.0, 48.0, dens) + k * 41.0);
							vec2 id = floor(cell);
							vec2 f = fract(cell) - 0.5;
							float h = hash(id);
							float w = mix(0.004, 0.012, dens) * (0.5 + h);
							if (abs(f.x) < w && f.y > -0.35 && f.y < 0.42) {
								float a = (1.0 - smoothstep(0.15, 0.42, abs(f.y))) * dens * (0.28 + 0.72 * h);
								streak += a * 0.45;
							}
						}
						float fog = streak * mix(0.55, 0.95, dens);
						gl_FragColor = vec4(0.75, 0.82, 0.95, clamp(fog, 0.0, 0.55));
					}
				`
			})
		);
		this.overlayQuad.frustumCulled = false;
		this.overlayQuad.renderOrder = 10000;
		this.overlayScene.add(this.overlayQuad);
	}

	private async ensureRapier(): Promise<void> {
		if (this.rapierInited) return;
		await RAPIER.init();
		this.rapierInited = true;
	}

	private disposeWorld(): void {
		this.rainBodies = [];
		this.rainByCollider.clear();
		if (this.eventQueue) {
			this.eventQueue.free();
			this.eventQueue = null;
		}
		if (this.world) {
			this.world.free();
			this.world = null;
		}
	}

	private splashIntensityFromSpeed(speed: number): number {
		return MathUtils.clamp(0.35 + (speed - 3.5) * 0.055, 0.3, 1.55);
	}

	private spawnSplash(x: number, y: number, z: number, intensity: number): void {
		if (!this.settings.enabled) return;
		const cap = this.splashMesh.count;
		let best = -1;
		let bestAge = -1;
		for (let i = 0; i < cap; i++) {
			const s = this.splashSlots[i];
			if (s.age > SPLASH_LIFE) {
				best = i;
				break;
			}
			if (s.age > bestAge) {
				bestAge = s.age;
				best = i;
			}
		}
		if (best < 0) return;
		this.splashSlots[best] = { age: 0, x, y, z, intensity };
	}

	private allocateSplashMatrices(): void {
		const cap = this.splashMesh.count;
		for (let i = 0; i < cap; i++) {
			const s = this.splashSlots[i];
			if (s.age > SPLASH_LIFE) {
				this.tmpS.setScalar(0);
				this.tmpM.compose(this.tmpP, this.tmpQ, this.tmpS);
			} else {
				const t = s.age / SPLASH_LIFE;
				const sc = ((1.0 - t) * 2.8 + 0.25) * s.intensity;
				this.tmpP.set(s.x, s.y, s.z);
				this.tmpQ.identity();
				this.tmpS.setScalar(sc);
				this.tmpM.compose(this.tmpP, this.tmpQ, this.tmpS);
			}
			this.splashMesh.setMatrixAt(i, this.tmpM);
		}
		for (let i = cap; i < SPLASH_MAX; i++) {
			this.tmpS.setScalar(0);
			this.tmpM.compose(this.tmpP, this.tmpQ, this.tmpS);
			this.splashMesh.setMatrixAt(i, this.tmpM);
		}
		this.splashMesh.instanceMatrix.needsUpdate = true;
	}

	private resetDrop(i: number): void {
		const body = this.rainBodies[i];
		if (!body) return;
		const sx = (Math.random() - 0.5) * 2 * this.spawnRadius;
		const sz = (Math.random() - 0.5) * 2 * this.spawnRadius;
		const high = SPAWN_Y_MIN + Math.random() * SPAWN_Y_SPAN;
		body.setLinvel({ x: 0, y: 0, z: 0 }, true);
		body.setAngvel({ x: 0, y: 0, z: 0 }, true);
		body.setTranslation({ x: sx, y: high, z: sz }, true);
		body.setLinvel(
			{
				x: (Math.random() - 0.5) * 3,
				y: -4 - Math.random() * 6,
				z: (Math.random() - 0.5) * 3
			},
			true
		);
	}

	/** Build Rapier static colliders (terrain trimesh + water slab) and dynamic rain pool. */
	async rebuild(terrainMesh: ThreeMesh, waterY: number, terrainSize: number, settings: RainSettings): Promise<void> {
		this.settings = settings;
		this.spawnRadius = settings.spawnRadius;
		this.splashMesh.count = Math.min(SPLASH_MAX, Math.max(4, settings.maxActiveSplashes));
		this.applyProxyVisibility();
		this.disposeWorld();
		if (!settings.enabled || settings.mode === 'screen') {
			this.instancedRain.count = 0;
			this.splashMesh.count = settings.mode === 'screen' ? 0 : this.splashMesh.count;
			return;
		}
		await this.ensureRapier();

		const meshData = terrainTrimeshArrays(terrainMesh);
		if (!meshData) return;

		this.dropSplashCooldownUntil.fill(0);
		this.simTime = 0;

		this.world = new RAPIER.World({ x: 0, y: -28, z: 0 });
		this.eventQueue = new RAPIER.EventQueue(true);

		const groundBody = this.world.createRigidBody(RAPIER.RigidBodyDesc.fixed());
		const triDesc = RAPIER.ColliderDesc.trimesh(meshData.vertices, meshData.indices)
			.setFriction(0.4)
			.setRestitution(0.02)
			.setActiveEvents(RAPIER.ActiveEvents.COLLISION_EVENTS);
		this.world.createCollider(triDesc, groundBody);

		const half = terrainSize * 0.52 + 30;
		const waterBody = this.world.createRigidBody(RAPIER.RigidBodyDesc.fixed().setTranslation(0, waterY - 0.35, 0));
		const waterDesc = RAPIER.ColliderDesc.cuboid(half, 0.4, half)
			.setFriction(0.05)
			.setRestitution(0.01)
			.setActiveEvents(RAPIER.ActiveEvents.COLLISION_EVENTS);
		this.world.createCollider(waterDesc, waterBody);

		this.dropCount = Math.max(8, Math.min(settings.collisionDropCount, RAIN_MAX_DROPS));
		this.rainBodies = [];
		this.rainByCollider.clear();
		for (let i = 0; i < this.dropCount; i++) {
			const sx = (Math.random() - 0.5) * 2 * this.spawnRadius;
			const sz = (Math.random() - 0.5) * 2 * this.spawnRadius;
			const hi = SPAWN_Y_MIN + Math.random() * SPAWN_Y_SPAN + i * 0.01;
			const desc = RAPIER.RigidBodyDesc.dynamic()
				.setTranslation(sx, hi, sz)
				.setLinearDamping(0.15)
				.setAngularDamping(1);
			const body = this.world.createRigidBody(desc);
			const cdesc = RAPIER.ColliderDesc.ball(DROP_RADIUS)
				.setFriction(0.08)
				.setRestitution(0.06)
				.setDensity(0.35)
				.setActiveEvents(RAPIER.ActiveEvents.COLLISION_EVENTS);
			const col = this.world.createCollider(cdesc, body);
			this.rainByCollider.set(col.handle, i);
			this.rainBodies.push(body);
			body.setLinvel(
				{ x: (Math.random() - 0.5) * 2.5, y: -6 - Math.random() * 4, z: (Math.random() - 0.5) * 2.5 },
				true
			);
		}
		this.instancedRain.count = this.dropCount;
	}

	setOverlayResolution(w: number, h: number): void {
		const mat = this.overlayQuad.material as ShaderMaterial;
		mat.uniforms.uResolution.value.set(w, h);
	}

	updateSettings(settings: RainSettings): void {
		this.settings = settings;
		this.spawnRadius = settings.spawnRadius;
		if (settings.mode === 'screen') {
			this.instancedRain.count = 0;
			this.splashMesh.count = 0;
		} else {
			this.splashMesh.count = Math.min(
				SPLASH_MAX,
				Math.max(4, Math.round(settings.maxActiveSplashes * this.performanceScale))
			);
		}
		this.applyProxyVisibility();
		const mat = this.overlayQuad.material as ShaderMaterial;
		mat.uniforms.uDensity.value =
			settings.enabled ? MathUtils.clamp(settings.overlayDensity * this.performanceScale, 0, 1) : 0;
	}

	setPerformanceScale(scale: number): void {
		const next = MathUtils.clamp(scale, 0.45, 1);
		if (Math.abs(next - this.performanceScale) < 0.03) return;
		this.performanceScale = next;
		this.splashMesh.count = Math.min(
			SPLASH_MAX,
			Math.max(4, Math.round(this.settings.maxActiveSplashes * this.performanceScale))
		);
	}

	step(delta: number, paused: boolean): void {
		const mat = this.overlayQuad.material as ShaderMaterial;
		mat.uniforms.uTime.value += delta;
		mat.uniforms.uDensity.value = this.settings.enabled
			? MathUtils.clamp(this.settings.overlayDensity * this.performanceScale, 0, 1)
			: 0;

		for (const s of this.splashSlots) {
			if (s.age <= SPLASH_LIFE) s.age += delta;
		}
		this.allocateSplashMatrices();

		if (this.settings.showRainDebugHud) {
			this.telemetrySeconds += delta;
			if (this.telemetrySeconds >= 1) {
				this.displayedImpactsPerSec = this.impactsAccum;
				this.impactsAccum = 0;
				this.telemetrySeconds = 0;
			}
		}

		if (!this.settings.enabled || this.settings.mode === 'screen' || !this.world || !this.eventQueue || paused) {
			return;
		}

		this.simTime += delta;
		this.physicsAccumulator = Math.min(this.physicsAccumulator + delta, PHYSICS_FIXED_DT * PHYSICS_MAX_STEPS);
		let steps = 0;
		while (this.physicsAccumulator >= PHYSICS_FIXED_DT && steps < PHYSICS_MAX_STEPS) {
			this.world.integrationParameters.dt = PHYSICS_FIXED_DT;
			this.world.step(this.eventQueue);
			this.physicsAccumulator -= PHYSICS_FIXED_DT;
			steps += 1;
		}
		if (steps === 0) return;

		const hits = new Set<number>();
		this.eventQueue.drainCollisionEvents((h1, h2, started) => {
			if (!started) return;
			let idx = this.rainByCollider.get(h1);
			if (idx === undefined) idx = this.rainByCollider.get(h2);
			if (idx === undefined) return;
			hits.add(idx);
		});

		if (this.settings.showRainDebugHud) {
			this.impactsAccum += hits.size;
		}

		for (const i of hits) {
			const body = this.rainBodies[i];
			if (!body) continue;
			const t = body.translation();
			const v = body.linvel();
			const speed = Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
			if (this.simTime < this.dropSplashCooldownUntil[i]) {
				this.resetDrop(i);
				continue;
			}
			this.dropSplashCooldownUntil[i] = this.simTime + SPLASH_COOLDOWN;
			const intensity = this.splashIntensityFromSpeed(speed);
			this.spawnSplash(t.x, t.y, t.z, intensity);
			this.resetDrop(i);
		}

		const showProxies = this.settings.enabled && this.settings.showCollisionProxies;
		for (let i = 0; i < this.dropCount; i++) {
			const body = this.rainBodies[i];
			const t = body.translation();
			if (t.y < KILL_Y) this.resetDrop(i);
			if (!showProxies) continue;
			const r = body.rotation();
			this.tmpQ.set(r.x, r.y, r.z, r.w);
			this.tmpP.set(t.x, t.y, t.z);
			this.tmpS.setScalar(1);
			this.tmpM.compose(this.tmpP, this.tmpQ, this.tmpS);
			this.instancedRain.setMatrixAt(i, this.tmpM);
		}
		if (showProxies) this.instancedRain.instanceMatrix.needsUpdate = true;
	}

	getRainDebugTelemetry(): RainDebugTelemetry | null {
		if (!this.settings.showRainDebugHud) return null;
		let active = 0;
		const cap = this.splashMesh.count;
		for (let i = 0; i < cap; i++) {
			if (this.splashSlots[i].age <= SPLASH_LIFE) active++;
		}
		return { impactsPerSec: this.displayedImpactsPerSec, activeSplashes: active };
	}

	renderOverlay(renderer: WebGLRenderer): void {
		if (!this.settings.enabled || this.settings.overlayDensity <= 0.02) return;
		const prev = renderer.autoClear;
		renderer.autoClear = false;
		renderer.render(this.overlayScene, this.overlayCam);
		renderer.autoClear = prev;
	}

	dispose(): void {
		this.disposeWorld();
		this.instancedRain.geometry.dispose();
		(this.instancedRain.material as MeshBasicMaterial).dispose();
		this.splashMesh.geometry.dispose();
		(this.splashMesh.material as MeshBasicMaterial).dispose();
		this.overlayQuad.geometry.dispose();
		(this.overlayQuad.material as ShaderMaterial).dispose();
	}
}

export function applyRainQualityPreset(q: RainQuality): Pick<
	RainSettings,
	'collisionDropCount' | 'maxActiveSplashes' | 'overlayDensity' | 'qualityPreset'
> {
	switch (q) {
		case 'low':
			return {
				qualityPreset: 'low',
				collisionDropCount: 120,
				maxActiveSplashes: 24,
				overlayDensity: 0.32
			};
		case 'high':
			return {
				qualityPreset: 'high',
				collisionDropCount: 600,
				maxActiveSplashes: 128,
				overlayDensity: 0.88
			};
		default:
			return {
				qualityPreset: 'medium',
				collisionDropCount: 320,
				maxActiveSplashes: 64,
				overlayDensity: 0.55
			};
	}
}
