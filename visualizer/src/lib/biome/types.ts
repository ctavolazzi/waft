export type BiomeClockMode = 'local' | 'server';

/** Preset floor tints for bridge / UI; maps to shader colors in the WebGL path. */
export type SeabedPreset = 'default' | 'muddy' | 'sand' | 'coral';

/**
 * Primary caustics implementation for `/biome` on the WebGL stack:
 * iterate `caustics.ts` env-depth pass + screen-space march (Renou-like), not Wallace heightfield.
 * MLS-MPM / SSFR remains a separate research route (`/biome/fluid-research`).
 */
export type CausticsPath = 'env_march';

export interface WaterSettings {
	textureWidth: number;
	textureHeight: number;
	distortionScale: number;
	alpha: number;
	waterColor: string;
	sunColor: string;
	sunDirection: [number, number, number];
	timeScale: number;
	fog: boolean;
	/** Water plane Y in world units (Wallace / pond parity). */
	surfaceY: number;
}

export interface CausticsSettings {
	enabled: boolean;
	resolution: number;
	maxSteps: number;
	intensity: number;
	eta: number;
	path: CausticsPath;
	/** When true, skip the caustics pass on very high DPR to protect frame time. */
	respectPerformanceGate: boolean;
}

export interface TerrainSettings {
	size: number;
	segments: number;
	maxPopulation: number;
	seabedPreset: SeabedPreset;
	/** Optional albedo: data URL or http(s) URL from user upload / assets. */
	seabedTextureDataUrl: string | null;
}

export interface SkySettings {
	enabled: boolean;
	turbidity: number;
	rayleigh: number;
	/**
	 * When false, sky dome is skipped on coarse devices (heuristic: DPR > 2).
	 * User can still force `enabled` for testing.
	 */
	respectPerformanceGate: boolean;
}

export interface RenderingSettings {
	/** Experimental: `WaterMesh` + `WebGPURenderer` when the browser supports it. */
	useWebGPU: boolean;
}

export interface VolumetricsSettings {
	/** Froxel-inspired screen-space volumetric composite for WebGPU biome path. */
	enabled: boolean;
	density: number;
	anisotropy: number;
	heightFalloff: number;
	froxelWidth: number;
	froxelHeight: number;
	froxelDepth: number;
	/** When true, skip volumetrics on very high DPR devices. */
	respectPerformanceGate: boolean;
}

/** Preset tier for hybrid rain (collision pool + screen overlay + splashes). */
export type RainQuality = 'low' | 'medium' | 'high';
export type RainMode = 'screen' | 'hybrid';

/** Snapshot for optional rain debug overlay (impacts/s, live splash count). */
export interface RainDebugTelemetry {
	impactsPerSec: number;
	activeSplashes: number;
}

export interface RainSettings {
	/** Master switch: Rapier droplets + overlay + splashes. */
	enabled: boolean;
	/** `screen` = screen-attached overlay only; `hybrid` = overlay + Rapier collisions/splashes. */
	mode: RainMode;
	/** Debug view for collision droplets; off keeps physics proxies invisible. */
	showCollisionProxies: boolean;
	/** When true, show lightweight rain telemetry overlay (impacts/s, active splashes). */
	showRainDebugHud: boolean;
	/** Dynamic rain bodies (capped by engine pool size). */
	collisionDropCount: number;
	/** Fullscreen streak shader strength 0–1. */
	overlayDensity: number;
	/** Ring buffer size for impact bursts (instanced). */
	maxActiveSplashes: number;
	/** Half-width/-depth of spawn box on XZ around origin. */
	spawnRadius: number;
	qualityPreset: RainQuality;
}

export interface BridgeSettings {
	enabled: boolean;
	mode: 'poll' | 'sse';
	url: string;
	pollMs: number;
}

export interface BiomeViewState {
	water: WaterSettings;
	caustics: CausticsSettings;
	terrain: TerrainSettings;
	sky: SkySettings;
	rain: RainSettings;
	rendering: RenderingSettings;
	volumetrics: VolumetricsSettings;
	bridge: BridgeSettings;
	clockMode: BiomeClockMode;
	/** Space bar toggles local tick + water time (Wallace pause parity). */
	paused: boolean;
	simTick: number;
	displayTime: number;
	eventCount: number;
	status: 'idle' | 'running' | 'error';
	lastError: string | null;
}

export interface LatticeBeing {
	id: string;
	x: number;
	y: number;
	fitness: number;
	alive: boolean;
}

export interface BiomeServerPayload {
	tick: number;
	time?: number;
	abiotic?: Partial<WaterSettings>;
	beings?: LatticeBeing[];
	events?: Array<{ type: string; message?: string; timestamp?: number }>;
}

/** Shared scene runner contract for WebGL (`Water`) and WebGPU (`WaterMesh`) paths. */
export interface BiomeEngineLike {
	mount(onTick?: (delta: number) => void): void | Promise<void>;
	resize(width: number, height: number): void;
	updateState(state: BiomeViewState): void;
	updateBeings(beings: LatticeBeing[]): void;
	nudgeCamera(dx: number, dy: number): void;
	/** WebGL rain path only; returns null when telemetry disabled or unavailable. */
	getRainDebugTelemetry?(): RainDebugTelemetry | null;
	dispose(): void;
}
