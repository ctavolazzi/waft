import { writable } from 'svelte/store';
import type { BiomeServerPayload, BiomeViewState } from './types';

const initialState: BiomeViewState = {
	water: {
		textureWidth: 512,
		textureHeight: 512,
		distortionScale: 3.0,
		alpha: 0.92,
		waterColor: '#2f5f87',
		sunColor: '#ffffff',
		sunDirection: [0.707, 0.707, 0.0],
		timeScale: 0.35,
		fog: true,
		surfaceY: 0
	},
	caustics: {
		enabled: false,
		resolution: 512,
		maxSteps: 64,
		intensity: 0.9,
		eta: 1.333,
		path: 'env_march',
		respectPerformanceGate: true
	},
	terrain: {
		size: 500,
		segments: 128,
		maxPopulation: 2000,
		seabedPreset: 'default',
		seabedTextureDataUrl: null
	},
	sky: {
		enabled: true,
		turbidity: 4,
		rayleigh: 1,
		respectPerformanceGate: true
	},
	rain: {
		enabled: true,
		mode: 'screen',
		showCollisionProxies: false,
		showRainDebugHud: false,
		collisionDropCount: 320,
		overlayDensity: 0.55,
		maxActiveSplashes: 64,
		spawnRadius: 220,
		qualityPreset: 'medium'
	},
	rendering: {
		useWebGPU: false
	},
	volumetrics: {
		enabled: false,
		density: 0.5,
		anisotropy: 0.35,
		heightFalloff: 0.7,
		froxelWidth: 160,
		froxelHeight: 90,
		froxelDepth: 24,
		respectPerformanceGate: true
	},
	bridge: {
		enabled: false,
		mode: 'poll',
		url: 'http://localhost:8000/api/biome',
		pollMs: 750
	},
	clockMode: 'local',
	paused: false,
	simTick: 0,
	displayTime: 0,
	eventCount: 0,
	status: 'idle',
	lastError: null
};

function createBiomeStore() {
	const { subscribe, set, update } = writable<BiomeViewState>(initialState);

	return {
		subscribe,
		reset: () => set(initialState),
		patch: (partial: Partial<BiomeViewState>) => update((state) => ({ ...state, ...partial })),
		patchWater: (partial: Partial<BiomeViewState['water']>) =>
			update((state) => ({ ...state, water: { ...state.water, ...partial } })),
		patchCaustics: (partial: Partial<BiomeViewState['caustics']>) =>
			update((state) => ({ ...state, caustics: { ...state.caustics, ...partial } })),
		patchTerrain: (partial: Partial<BiomeViewState['terrain']>) =>
			update((state) => ({ ...state, terrain: { ...state.terrain, ...partial } })),
		patchBridge: (partial: Partial<BiomeViewState['bridge']>) =>
			update((state) => ({ ...state, bridge: { ...state.bridge, ...partial } })),
		patchSky: (partial: Partial<BiomeViewState['sky']>) =>
			update((state) => ({ ...state, sky: { ...state.sky, ...partial } })),
		patchRain: (partial: Partial<BiomeViewState['rain']>) =>
			update((state) => ({ ...state, rain: { ...state.rain, ...partial } })),
		patchRendering: (partial: Partial<BiomeViewState['rendering']>) =>
			update((state) => ({ ...state, rendering: { ...state.rendering, ...partial } })),
		patchVolumetrics: (partial: Partial<BiomeViewState['volumetrics']>) =>
			update((state) => ({ ...state, volumetrics: { ...state.volumetrics, ...partial } })),
		togglePause: () => update((state) => ({ ...state, paused: !state.paused })),
		tickLocal: (deltaSeconds: number) =>
			update((state) => {
				if (state.paused || state.clockMode !== 'local') return state;
				return {
					...state,
					displayTime: state.displayTime + deltaSeconds,
					simTick: state.simTick + 1,
					status: 'running'
				};
			}),
		ingestPayload: (payload: BiomeServerPayload) =>
			update((state) => {
				const nextWater = payload.abiotic ? { ...state.water, ...payload.abiotic } : state.water;
				return {
					...state,
					water: nextWater,
					simTick: payload.tick,
					displayTime: payload.time ?? state.displayTime,
					eventCount: state.eventCount + (payload.events?.length ?? 0),
					status: 'running',
					lastError: null
				};
			}),
		setError: (error: string) => update((state) => ({ ...state, status: 'error', lastError: error }))
	};
}

export const biomeStore = createBiomeStore();
