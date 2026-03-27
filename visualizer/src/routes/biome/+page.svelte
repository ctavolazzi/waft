<script lang="ts">
	import { onDestroy, onMount, tick } from 'svelte';
	import { get } from 'svelte/store';
	import { BiomeBridge } from '$lib/biome/bridge';
	import { biomeStore } from '$lib/biome/store';
	import { bindLocalClock, createBiomeEngine, spawnLocalBeings } from '$lib/biome/engine';
	import { applyRainQualityPreset } from '$lib/biome/rain-system';
	import { isBiomeDebugEnabled } from '$lib/biome/engine-shared';
	import type { BiomeEngineLike, BiomeServerPayload, RainDebugTelemetry } from '$lib/biome/types';
	export let params: Record<string, string> | undefined = undefined;
	void params;

	let canvas: HTMLCanvasElement;
	let wrapper: HTMLDivElement;
	let engine: BiomeEngineLike | null = null;
	let bridge: BiomeBridge | null = null;
	let beings = spawnLocalBeings(350);
	let connected = false;
	let rainHud: RainDebugTelemetry = { impactsPerSec: 0, activeSplashes: 0 };

	$: state = $biomeStore;
	type ExtrasSnapshot = {
		useWebGPU: boolean;
		waterFog: boolean;
		rainEnabled: boolean;
		rainDebugHud: boolean;
		rainCollisionProxies: boolean;
		skyEnabled: boolean;
		causticsEnabled: boolean;
		volumetricsEnabled: boolean;
	};
	let extrasSnapshot: ExtrasSnapshot | null = null;

	$: extrasAllOff =
		!state.rendering.useWebGPU &&
		!state.water.fog &&
		!state.rain.enabled &&
		!state.rain.showRainDebugHud &&
		!state.rain.showCollisionProxies &&
		!state.sky.enabled &&
		!state.caustics.enabled &&
		!state.volumetrics.enabled;
	$: debugModeLabel = extrasAllOff ? 'Debug mode: ON (minimal scene)' : 'Debug mode: OFF (full scene)';
	$: debugModeHint = extrasAllOff
		? 'WebGL baseline with optional effects disabled for clean troubleshooting.'
		: 'All rendering systems use your current settings.';
	$: extrasEnabledCount =
		(state.rendering.useWebGPU ? 1 : 0) +
		(state.water.fog ? 1 : 0) +
		(state.rain.enabled ? 1 : 0) +
		(state.sky.enabled ? 1 : 0) +
		(state.caustics.enabled ? 1 : 0) +
		(state.volumetrics.enabled ? 1 : 0);

	function onToggleExtras() {
		if (extrasAllOff) {
			const snap = extrasSnapshot;
			biomeStore.patchRendering({ useWebGPU: snap?.useWebGPU ?? true });
			biomeStore.patchWater({ fog: snap?.waterFog ?? true });
			biomeStore.patchRain({
				enabled: snap?.rainEnabled ?? true,
				showRainDebugHud: snap?.rainDebugHud ?? false,
				showCollisionProxies: snap?.rainCollisionProxies ?? false
			});
			biomeStore.patchSky({ enabled: snap?.skyEnabled ?? true });
			biomeStore.patchCaustics({ enabled: snap?.causticsEnabled ?? false });
			biomeStore.patchVolumetrics({ enabled: snap?.volumetricsEnabled ?? false });
			return;
		}
		extrasSnapshot = {
			useWebGPU: state.rendering.useWebGPU,
			waterFog: state.water.fog,
			rainEnabled: state.rain.enabled,
			rainDebugHud: state.rain.showRainDebugHud,
			rainCollisionProxies: state.rain.showCollisionProxies,
			skyEnabled: state.sky.enabled,
			causticsEnabled: state.caustics.enabled,
			volumetricsEnabled: state.volumetrics.enabled
		};
		biomeStore.patchRendering({ useWebGPU: false });
		biomeStore.patchWater({ fog: false });
		biomeStore.patchRain({ enabled: false, showRainDebugHud: false, showCollisionProxies: false });
		biomeStore.patchSky({ enabled: false });
		biomeStore.patchCaustics({ enabled: false });
		biomeStore.patchVolumetrics({ enabled: false });
	}

	// ── Generic handler factories ──────────────────────────────────────
	/* eslint-disable @typescript-eslint/no-explicit-any */
	const patchFns = {
		water: biomeStore.patchWater,
		caustics: biomeStore.patchCaustics,
		terrain: biomeStore.patchTerrain,
		bridge: biomeStore.patchBridge,
		sky: biomeStore.patchSky,
		rain: biomeStore.patchRain,
		rendering: biomeStore.patchRendering,
		volumetrics: biomeStore.patchVolumetrics
	} as const;
	type Section = keyof typeof patchFns;
	const slider = (s: Section, key: string) => (e: Event) =>
		patchFns[s]({ [key]: Number((e.currentTarget as HTMLInputElement).value) } as any);
	const checkbox = (s: Section, key: string) => (e: Event) =>
		patchFns[s]({ [key]: (e.currentTarget as HTMLInputElement).checked } as any);
	const select = (s: Section, key: string) => (e: Event) =>
		patchFns[s]({ [key]: (e.currentTarget as HTMLSelectElement).value } as any);
	const textInput = (s: Section, key: string) => (e: Event) =>
		patchFns[s]({ [key]: (e.currentTarget as HTMLInputElement).value } as any);
	/* eslint-enable @typescript-eslint/no-explicit-any */

	// ── Custom handlers (non-trivial logic) ─────────────────────────
	function onRainPreset(event: Event) {
		const q = (event.currentTarget as HTMLSelectElement).value as import('$lib/biome/types').RainQuality;
		biomeStore.patchRain(applyRainQualityPreset(q));
	}

	function onSeabedFile(event: Event) {
		const input = event.currentTarget as HTMLInputElement;
		const file = input.files?.[0];
		if (!file) {
			biomeStore.patchTerrain({ seabedTextureDataUrl: null });
			return;
		}
		const url = URL.createObjectURL(file);
		biomeStore.patchTerrain({ seabedTextureDataUrl: url });
	}

	function clearSeabedTexture() {
		const u = get(biomeStore).terrain.seabedTextureDataUrl;
		if (u?.startsWith('blob:')) URL.revokeObjectURL(u);
		biomeStore.patchTerrain({ seabedTextureDataUrl: null });
	}

	function connectBridge() {
		if (!bridge) return;
		bridge
			.start(state.bridge)
			.then(() => {
				connected = true;
			})
			.catch((error) => {
				const message = error instanceof Error ? error.message : 'Bridge start failed';
				biomeStore.setError(message);
			});
	}

	function disconnectBridge() {
		bridge?.stop();
		connected = false;
		biomeStore.patch({ status: 'idle' });
	}

	function applyPayload(payload: BiomeServerPayload) {
		biomeStore.ingestPayload(payload);
		if (payload.beings) {
			beings = payload.beings;
			engine?.updateBeings(beings);
		}
	}

	onMount(() => {
		const debugBiome = isBiomeDebugEnabled();
		const debugLog = (...args: unknown[]) => {
			if (!debugBiome) return;
			console.warn(...args);
		};
		debugLog('[BiomeUI] mount', { url: window.location.href });
		let unsubStore = () => {};
		let resizeObserver: ResizeObserver | null = null;
		let prevWebGPU = get(biomeStore).rendering.useWebGPU;
		let rebuildVersion = 0;

		async function rebuild() {
			const version = ++rebuildVersion;
			engine?.dispose();
			engine = null;
			try {
				// WebGL and WebGPU contexts cannot reliably share the same canvas.
				// Wait for keyed canvas remount when renderer mode flips.
				await tick();
				if (version !== rebuildVersion || !canvas?.isConnected) return;
				debugLog('[BiomeUI] rebuild-start', {
					useWebGPU: get(biomeStore).rendering.useWebGPU,
					volumetricsEnabled: get(biomeStore).volumetrics.enabled,
					skyEnabled: get(biomeStore).sky.enabled,
					causticsEnabled: get(biomeStore).caustics.enabled,
					waterFog: get(biomeStore).water.fog
				});
				const nextEngine = createBiomeEngine(canvas, get(biomeStore));
				await nextEngine.mount((delta) => biomeStore.tickLocal(delta));
				if (version !== rebuildVersion) {
					nextEngine.dispose();
					return;
				}
				engine = nextEngine;
				nextEngine.updateBeings(beings);
				if (wrapper) nextEngine.resize(wrapper.clientWidth, wrapper.clientHeight);
				const active = get(biomeStore);
				debugLog('[BiomeUI] rebuild-done', {
					useWebGPU: active.rendering.useWebGPU,
					volumetricsEnabled: active.volumetrics.enabled,
					skyEnabled: active.sky.enabled,
					causticsEnabled: active.caustics.enabled,
					waterFog: active.water.fog
				});
			} catch (error) {
				// Auto-fallback to WebGL when WebGPU init/runtime is not viable on this device.
				const message = error instanceof Error ? error.message : 'WebGPU initialization failed';
				biomeStore.setError(`WebGPU disabled: ${message}`);
				biomeStore.patchRendering({ useWebGPU: false });
				engine = null;
			}
		}

		void (async () => {
			await rebuild();
			bindLocalClock();

			unsubStore = biomeStore.subscribe((s) => {
				if (s.rendering.useWebGPU !== prevWebGPU) {
					prevWebGPU = s.rendering.useWebGPU;
					void rebuild();
					return;
				}
				engine?.updateState(s);
			});
		})();

		resizeObserver = new ResizeObserver(() => {
			if (!wrapper) return;
			engine?.resize(wrapper.clientWidth, wrapper.clientHeight);
		});
		resizeObserver.observe(wrapper);

		bridge = new BiomeBridge(applyPayload, (error) => biomeStore.setError(error));

		const onKey = (event: KeyboardEvent) => {
			if (event.code === 'Space') {
				const t = event.target as HTMLElement;
				if (t?.tagName === 'INPUT' || t?.tagName === 'TEXTAREA' || t?.tagName === 'SELECT')
					return;
				event.preventDefault();
				biomeStore.togglePause();
			}
			if (!engine) return;
			if (event.key === 'ArrowUp') engine.nudgeCamera(0, -6);
			if (event.key === 'ArrowDown') engine.nudgeCamera(0, 6);
			if (event.key === 'ArrowLeft') engine.nudgeCamera(-6, 0);
			if (event.key === 'ArrowRight') engine.nudgeCamera(6, 0);
		};
		window.addEventListener('keydown', onKey);

		let hudRaf = 0;
		function hudTick() {
			const tel = engine?.getRainDebugTelemetry?.();
			if (tel) rainHud = tel;
			hudRaf = requestAnimationFrame(hudTick);
		}
		hudRaf = requestAnimationFrame(hudTick);

		return () => {
			cancelAnimationFrame(hudRaf);
			unsubStore();
			resizeObserver?.disconnect();
			window.removeEventListener('keydown', onKey);
		};
	});

	onDestroy(() => {
		disconnectBridge();
		engine?.dispose();
		const u = get(biomeStore).terrain.seabedTextureDataUrl;
		if (u?.startsWith('blob:')) URL.revokeObjectURL(u);
	});
</script>

<div class="biome-page">
	<div class="panel card-glass">
		<h1>🌊 WAFT Biome Simulator</h1>
		<p>Three.js water, terrain, lattice organisms, optional caustics. Drag on water for ripples; Space pauses; drag to orbit (mouse).</p>
		<p class="hint">
			<strong>Caustics path:</strong> env-depth + bounded march in <code>caustics.ts</code> (not Wallace heightfield).
			<a href="/biome/fluid-research">WebGPU MLS-MPM + SSFR research →</a>
		</p>
		<div class="stats">
			<div><strong>Status:</strong> {state.status}{state.paused ? ' (paused)' : ''}</div>
			<div><strong>Tick:</strong> {state.simTick}</div>
			<div><strong>Time:</strong> {state.displayTime.toFixed(2)}s</div>
			<div><strong>Events:</strong> {state.eventCount}</div>
		</div>
		{#if state.lastError}
			<div class="error">{state.lastError}</div>
		{/if}

		<h2>Rendering</h2>
		<div class="debug-strip" role="status" aria-live="polite">
			<div class="debug-title">{debugModeLabel}</div>
			<div class="debug-hint">{debugModeHint}</div>
			<div class="debug-meta">Active systems: {extrasEnabledCount}/6</div>
		</div>
		<button
			class="btn {extrasAllOff ? 'btn-primary' : 'btn-secondary'} extras-toggle"
			type="button"
			on:click={onToggleExtras}
		>
			{extrasAllOff ? 'Restore previous scene config' : 'Enter minimal debug mode'}
		</button>
		<label>
			<input type="checkbox" checked={state.rendering.useWebGPU} on:change={checkbox('rendering', 'useWebGPU')} />
			WebGPU spike (<code>WaterMesh</code>; experimental)
		</label>
		<label>
			<input
				type="checkbox"
				checked={state.volumetrics.enabled}
				on:change={checkbox('volumetrics', 'enabled')}
				disabled={!state.rendering.useWebGPU}
			/>
			Volumetric lighting spike (WebGPU only)
		</label>
		<label>
			<input
				type="checkbox"
				checked={state.volumetrics.respectPerformanceGate}
				on:change={checkbox('volumetrics', 'respectPerformanceGate')}
			/>
			Skip volumetrics when device pixel ratio is above 2
		</label>
		<div class="slider">
			<div class="slider-label">Volumetric density {state.volumetrics.density.toFixed(2)}</div>
			<input
				type="range"
				min="0"
				max="1.5"
				step="0.01"
				value={state.volumetrics.density}
				on:input={slider('volumetrics', 'density')}
				disabled={!state.rendering.useWebGPU || !state.volumetrics.enabled}
			/>
		</div>
		<div class="slider">
			<div class="slider-label">Anisotropy {state.volumetrics.anisotropy.toFixed(2)}</div>
			<input
				type="range"
				min="0"
				max="0.95"
				step="0.01"
				value={state.volumetrics.anisotropy}
				on:input={slider('volumetrics', 'anisotropy')}
				disabled={!state.rendering.useWebGPU || !state.volumetrics.enabled}
			/>
		</div>
		<div class="slider">
			<div class="slider-label">Height falloff {state.volumetrics.heightFalloff.toFixed(2)}</div>
			<input
				type="range"
				min="0.05"
				max="2"
				step="0.01"
				value={state.volumetrics.heightFalloff}
				on:input={slider('volumetrics', 'heightFalloff')}
				disabled={!state.rendering.useWebGPU || !state.volumetrics.enabled}
			/>
		</div>

		<h2>Bridge</h2>
		<label>
			<input type="checkbox" checked={state.bridge.enabled} on:change={checkbox('bridge', 'enabled')} />
			Enable server bridge
		</label>
		<div class="row">
			<select value={state.bridge.mode} on:change={select('bridge', 'mode')}>
				<option value="poll">poll</option>
				<option value="sse">sse</option>
			</select>
			<input
				type="text"
				value={state.bridge.url}
				on:input={textInput('bridge', 'url')}
				placeholder="http://localhost:8000/api/biome"
			/>
			<input type="number" min="100" step="50" value={state.bridge.pollMs} on:input={slider('bridge', 'pollMs')} />
		</div>
		<div class="row">
			<button class="btn btn-primary" on:click={connectBridge} disabled={!state.bridge.enabled || connected}>Connect</button>
			<button class="btn btn-secondary" on:click={disconnectBridge} disabled={!connected}>Disconnect</button>
		</div>

		<h2>Water</h2>
		<div class="slider">
			<div class="slider-label">Surface height {state.water.surfaceY.toFixed(1)}</div>
			<input type="range" min="-12" max="18" step="0.2" value={state.water.surfaceY} on:input={slider('water', 'surfaceY')} />
		</div>
		<div class="slider">
			<div class="slider-label">Distortion {state.water.distortionScale.toFixed(2)}</div>
			<input type="range" min="0.2" max="12" step="0.1" value={state.water.distortionScale} on:input={slider('water', 'distortionScale')} />
		</div>
		<div class="slider">
			<div class="slider-label">Alpha {state.water.alpha.toFixed(2)}</div>
			<input type="range" min="0.2" max="1" step="0.01" value={state.water.alpha} on:input={slider('water', 'alpha')} />
		</div>
		<div class="slider">
			<div class="slider-label">Time scale {state.water.timeScale.toFixed(2)}</div>
			<input type="range" min="0.05" max="2" step="0.01" value={state.water.timeScale} on:input={slider('water', 'timeScale')} />
		</div>

		<h2>Rain (Rapier + overlay)</h2>
		<p class="hint">Hybrid: screen-space streaks + instanced Rapier spheres vs terrain &amp; water. Uses <code>@dimforge/rapier3d-compat</code> (WASM).</p>
		<label>
			<input type="checkbox" checked={state.rain.enabled} on:change={checkbox('rain', 'enabled')} />
			Enable rain simulation
		</label>
		<label class="preset-row">
			Rain mode
			<select value={state.rain.mode} on:change={select('rain', 'mode')}>
				<option value="screen">screen-attached (overlay only)</option>
				<option value="hybrid">hybrid (overlay + Rapier collisions)</option>
			</select>
		</label>
		<label>
			<input
				type="checkbox"
				checked={state.rain.showCollisionProxies}
				on:change={checkbox('rain', 'showCollisionProxies')}
			/>
			Show collision proxies (debug)
		</label>
		<label>
			<input type="checkbox" checked={state.rain.showRainDebugHud} on:change={checkbox('rain', 'showRainDebugHud')} />
			Show rain telemetry (impacts/s, active splashes)
		</label>
		<label class="preset-row">
			Quality preset
			<select value={state.rain.qualityPreset} on:change={onRainPreset}>
				<option value="low">low</option>
				<option value="medium">medium</option>
				<option value="high">high</option>
			</select>
		</label>
		{#if state.rain.mode === 'hybrid'}
			<div class="slider">
				<div class="slider-label">Collision drops {state.rain.collisionDropCount}</div>
				<input type="range" min="40" max="1200" step="20" value={state.rain.collisionDropCount} on:input={slider('rain', 'collisionDropCount')} />
			</div>
		{/if}
		<div class="slider">
			<div class="slider-label">Overlay density {state.rain.overlayDensity.toFixed(2)}</div>
			<input type="range" min="0" max="1" step="0.02" value={state.rain.overlayDensity} on:input={slider('rain', 'overlayDensity')} />
		</div>
		{#if state.rain.mode === 'hybrid'}
			<div class="slider">
				<div class="slider-label">Spawn radius {state.rain.spawnRadius.toFixed(0)}</div>
				<input type="range" min="80" max="420" step="10" value={state.rain.spawnRadius} on:input={slider('rain', 'spawnRadius')} />
			</div>
			<div class="slider">
				<div class="slider-label">Max splashes {state.rain.maxActiveSplashes}</div>
				<input type="range" min="8" max="128" step="4" value={state.rain.maxActiveSplashes} on:input={slider('rain', 'maxActiveSplashes')} />
			</div>
		{/if}

		<h2>Seabed</h2>
		<label class="preset-row">
			Preset
			<select value={state.terrain.seabedPreset} on:change={select('terrain', 'seabedPreset')}>
				<option value="default">default</option>
				<option value="muddy">muddy</option>
				<option value="sand">sand</option>
				<option value="coral">coral</option>
			</select>
		</label>
		<label class="upload">
			Bottom texture (optional)
			<input type="file" accept="image/*" on:change={onSeabedFile} />
		</label>
		<button class="btn btn-secondary small-btn" type="button" on:click={clearSeabedTexture}>Clear texture</button>

		<h2>Sky (WebGL: Sky; WebGPU: SkyMesh)</h2>
		<label>
			<input type="checkbox" checked={state.sky.enabled} on:change={checkbox('sky', 'enabled')} />
			Enable sky dome (better reflections / readout)
		</label>
		<label>
			<input type="checkbox" checked={state.sky.respectPerformanceGate} on:change={checkbox('sky', 'respectPerformanceGate')} />
			Skip on very high device pixel ratio (gate: 2+)
		</label>
		<div class="slider">
			<div class="slider-label">Turbidity {state.sky.turbidity.toFixed(1)}</div>
			<input type="range" min="1" max="20" step="0.5" value={state.sky.turbidity} on:input={slider('sky', 'turbidity')} />
		</div>
		<div class="slider">
			<div class="slider-label">Rayleigh {state.sky.rayleigh.toFixed(2)}</div>
			<input type="range" min="0.2" max="4" step="0.05" value={state.sky.rayleigh} on:input={slider('sky', 'rayleigh')} />
		</div>

		<h2>Caustics (WebGL only)</h2>
		<label>
			<input type="checkbox" checked={state.caustics.enabled} on:change={checkbox('caustics', 'enabled')} />
			Enable caustics pass (<code>env_march</code>)
		</label>
		<label>
			<input type="checkbox" checked={state.caustics.respectPerformanceGate} on:change={checkbox('caustics', 'respectPerformanceGate')} />
			Auto-skip caustics when device pixel ratio is above 2
		</label>
		<div class="slider">
			<div class="slider-label">Intensity {state.caustics.intensity.toFixed(2)}</div>
			<input type="range" min="0" max="2" step="0.01" value={state.caustics.intensity} on:input={slider('caustics', 'intensity')} />
		</div>
		<div class="slider">
			<div class="slider-label">Max steps {state.caustics.maxSteps}</div>
			<input type="range" min="8" max="200" step="1" value={state.caustics.maxSteps} on:input={slider('caustics', 'maxSteps')} />
		</div>
		<div class="slider">
			<div class="slider-label">Resolution {state.caustics.resolution}</div>
			<input type="range" min="128" max="1024" step="128" value={state.caustics.resolution} on:input={slider('caustics', 'resolution')} />
		</div>
	</div>

	<div class="viewport" bind:this={wrapper}>
		{#key state.rendering.useWebGPU}
			<canvas bind:this={canvas}></canvas>
		{/key}
		{#if state.rain.showRainDebugHud}
			<div class="rain-debug-hud" aria-live="polite">
				<div><strong>Rain telemetry</strong></div>
				<div>Impacts/s (last window): {rainHud.impactsPerSec}</div>
				<div>Active splashes: {rainHud.activeSplashes}</div>
			</div>
		{/if}
	</div>
</div>

<style>
	.biome-page {
		display: grid;
		grid-template-columns: 360px 1fr;
		gap: 1rem;
		padding: 1rem;
		min-height: calc(100vh - 130px);
	}

	.panel {
		padding: 1rem;
		border: 1px solid var(--border);
		overflow: auto;
	}

	h1 {
		font-size: 1.2rem;
		margin-bottom: 0.35rem;
	}

	h2 {
		font-size: 0.95rem;
		margin-top: 1rem;
		margin-bottom: 0.4rem;
		color: var(--primary-light);
	}

	p {
		color: var(--text-secondary);
		font-size: 0.85rem;
	}

	.hint {
		font-size: 0.78rem;
		margin-top: 0.35rem;
	}

	.hint code {
		font-size: 0.75rem;
	}

	.stats {
		margin-top: 0.7rem;
		display: grid;
		gap: 0.25rem;
		font-size: 0.8rem;
	}

	.row {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 0.4rem;
		margin-top: 0.4rem;
	}

	.row input[type='text'],
	.row input[type='number'],
	.row select {
		background: var(--bg-card);
		color: var(--text-primary);
		border: 1px solid var(--border);
		padding: 0.45rem;
		border-radius: 6px;
		font-size: 0.8rem;
	}

	.slider {
		margin-top: 0.45rem;
		display: grid;
		gap: 0.25rem;
	}

	.slider-label,
	label {
		font-size: 0.78rem;
		color: var(--text-secondary);
	}

	.preset-row,
	.upload {
		display: grid;
		gap: 0.35rem;
		margin-top: 0.45rem;
		font-size: 0.78rem;
	}

	.small-btn {
		margin-top: 0.35rem;
		padding: 0.35rem 0.5rem;
		font-size: 0.75rem;
	}

	.extras-toggle {
		width: 100%;
		margin-top: 0.3rem;
		margin-bottom: 0.45rem;
	}

	.debug-strip {
		margin-top: 0.35rem;
		padding: 0.5rem 0.55rem;
		border-radius: 8px;
		border: 1px solid var(--border);
		background: rgba(15, 23, 42, 0.45);
	}

	.debug-title {
		font-size: 0.78rem;
		font-weight: 700;
		color: var(--text-primary);
	}

	.debug-hint {
		margin-top: 0.2rem;
		font-size: 0.72rem;
		color: var(--text-secondary);
	}

	.debug-meta {
		margin-top: 0.25rem;
		font-size: 0.7rem;
		color: var(--text-muted);
	}

	input[type='range'] {
		width: 100%;
	}

	.error {
		margin-top: 0.5rem;
		padding: 0.4rem 0.5rem;
		border-radius: 6px;
		background: rgba(248, 113, 113, 0.15);
		border: 1px solid rgba(248, 113, 113, 0.3);
		color: #fecaca;
		font-size: 0.78rem;
	}

	.viewport {
		position: relative;
		border: 1px solid var(--border);
		border-radius: 10px;
		overflow: hidden;
		min-height: 600px;
		background: #030913;
	}

	.rain-debug-hud {
		position: absolute;
		top: 0.65rem;
		right: 0.65rem;
		padding: 0.45rem 0.55rem;
		border-radius: 6px;
		font-size: 0.72rem;
		line-height: 1.35;
		color: #e2e8f0;
		background: rgba(15, 23, 42, 0.72);
		border: 1px solid rgba(148, 163, 184, 0.35);
		pointer-events: none;
		z-index: 2;
	}

	canvas {
		display: block;
		width: 100%;
		height: 100%;
	}

	@media (max-width: 1200px) {
		.biome-page {
			grid-template-columns: 1fr;
		}
		.viewport {
			min-height: 500px;
		}
	}
</style>
