import {
	Color,
	DataTexture,
	Raycaster,
	RepeatWrapping,
	SRGBColorSpace,
	Vector2,
	type Camera,
	type Object3D,
	type Texture
} from 'three';
import type { SeabedPreset } from './types';

// ── Shared constants ────────────────────────────────────────────────

export const BIOME_FOV = 55;
export const BIOME_NEAR = 0.1;
export const BIOME_FAR = 2400;
export const BIOME_CLEAR_COLOR = '#061626';
export const BIOME_BG_COLOR = '#0a1626';
export const BIOME_FOG_COLOR = '#12263f';
export const BIOME_FOG_NEAR = 40;
export const BIOME_FOG_FAR = 420;
export const BIOME_SKY_SCALE = 450000;
export const BIOME_ORBIT_DAMPING = 0.06;
export const BIOME_MAX_POLAR = Math.PI / 2 - 0.08;

// ── Seabed presets ──────────────────────────────────────────────────

export const SEABED_PRESETS: Record<SeabedPreset, { base: string; shallow: string }> = {
	default: { base: '#375249', shallow: '#4f6f63' },
	muddy: { base: '#3d2f22', shallow: '#5c4a38' },
	sand: { base: '#7a6548', shallow: '#c9b896' },
	coral: { base: '#4a3a55', shallow: '#6b5a7d' }
};

// ── Fallback normal texture ─────────────────────────────────────────

export function buildFallbackNormalTexture(): Texture {
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

// ── Pointer ripple helper ───────────────────────────────────────────

const _ripplePointer = new Vector2();
const _rippleRaycaster = new Raycaster();

/**
 * Shared ripple logic for pointer interaction with water surface.
 * Returns the boost delta to add to the engine's rippleBoost (0 if no hit).
 */
export function computeRippleBoost(
	e: PointerEvent,
	canvas: HTMLCanvasElement,
	camera: Camera,
	waterObj: Object3D | null
): number {
	if ((e.buttons & 1) === 0 && e.type !== 'pointerdown') return 0;
	if (!waterObj) return 0;
	const rect = canvas.getBoundingClientRect();
	_ripplePointer.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
	_ripplePointer.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
	_rippleRaycaster.setFromCamera(_ripplePointer, camera);
	const hits = _rippleRaycaster.intersectObject(waterObj, false);
	return hits.length ? 1.8 : 0;
}

// ── Debug logging ───────────────────────────────────────────────────

export function isBiomeDebugEnabled(): boolean {
	if (typeof window === 'undefined') return false;
	const search = window.location.search ?? '';
	if (search.includes('debugBiome=1')) return true;
	return new URLSearchParams(search).get('debugBiome') === '1';
}

export function debugBiome(...args: unknown[]): void {
	if (!isBiomeDebugEnabled()) return;
	console.warn(...args);
}
