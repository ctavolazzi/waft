<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import type { Realm, RealmConfig, SupremeBeing, PrimeDirective } from '$lib/models/Realm';
	import { createRealm, SUPREME_BEINGS, PRIME_DIRECTIVES } from '$lib/models/Realm';
	import { initializePopulation } from '$lib/models/Evolution';

	const dispatch = createEventDispatcher();

	export let realm: Realm | null = null;
	export let canvasWidth: number;
	export let canvasHeight: number;

	let selectedSupremeBeing: SupremeBeing = SUPREME_BEINGS[0];
	let selectedDirective: PrimeDirective = PRIME_DIRECTIVES.harmony;
	let realmName = 'Genesis Realm';
	let initialPopulation = 200;
	let ticksPerEpoch = 1000;
	let tickRate = 10;

	let expanded = true;
	let showConfig = false;

	function createNewRealm() {
		const config: RealmConfig = {
			name: realmName,
			description: `A realm ruled by ${selectedSupremeBeing.name}, seeking to ${selectedDirective.goal.toLowerCase()}`,
			initialPopulation,
			worldWidth: canvasWidth,
			worldHeight: canvasHeight,
			ticksPerEpoch,
			supremeBeing: selectedSupremeBeing,
			primeDirective: selectedDirective
		};

		const newRealm = createRealm(config);
		newRealm.tickRate = tickRate;

		// Initialize population with genetic diversity
		const beings = initializePopulation(newRealm, initialPopulation, canvasWidth, canvasHeight);
		newRealm.beings = beings;

		realm = newRealm;
		showConfig = false;

		dispatch('realmcreated', { realm: newRealm });
	}

	function startSimulation() {
		if (!realm) return;
		dispatch('start');
	}

	function stopSimulation() {
		if (!realm) return;
		dispatch('stop');
	}

	function resetRealm() {
		realm = null;
		dispatch('reset');
	}

	function saveRealm() {
		if (!realm) return;
		dispatch('save', { realm });
	}

	function loadRealm() {
		dispatch('load');
	}

	function exportReport() {
		if (!realm) return;
		dispatch('export', { realm });
	}

	function adjustTickRate(delta: number) {
		if (!realm) return;
		realm.tickRate = Math.max(1, Math.min(60, realm.tickRate + delta));
		dispatch('tickratechange', { tickRate: realm.tickRate });
	}
</script>

<div class="realm-control" class:collapsed={!expanded}>
	<div class="control-header" on:click={() => expanded = !expanded}>
		<span class="header-title">🌌 REALM CONTROL</span>
		<button class="collapse-btn">{expanded ? '▼' : '▲'}</button>
	</div>

	{#if expanded}
		<div class="control-body">
			{#if !realm}
				<!-- Realm Creation -->
				<div class="section">
					<button class="primary-btn" on:click={() => showConfig = !showConfig}>
						{showConfig ? '◀ Back' : '✨ Create New Realm'}
					</button>
				</div>

				{#if showConfig}
					<div class="config-panel">
						<div class="config-section">
							<label>Realm Name</label>
							<input type="text" bind:value={realmName} class="text-input" />
						</div>

						<div class="config-section">
							<label>Supreme Being</label>
							<select bind:value={selectedSupremeBeing} class="select-input">
								{#each SUPREME_BEINGS as sb}
									<option value={sb}>{sb.name} - {sb.domain}</option>
								{/each}
							</select>
							<div class="help-text">{selectedSupremeBeing.temperament} • Intervenes {(selectedSupremeBeing.interventionRate * 100).toFixed(0)}% • Favors {selectedSupremeBeing.favoredTrait}</div>
						</div>

						<div class="config-section">
							<label>Prime Directive</label>
							<select bind:value={selectedDirective} class="select-input">
								{#each Object.entries(PRIME_DIRECTIVES) as [key, directive]}
									<option value={directive}>{directive.goal}</option>
								{/each}
							</select>
							<div class="help-text">{selectedDirective.description}</div>
						</div>

						<div class="config-section">
							<label>Initial Population: {initialPopulation}</label>
							<input type="range" min="50" max="500" step="50" bind:value={initialPopulation} class="slider" />
						</div>

						<div class="config-section">
							<label>Ticks per Epoch: {ticksPerEpoch}</label>
							<input type="range" min="500" max="5000" step="500" bind:value={ticksPerEpoch} class="slider" />
						</div>

						<div class="config-section">
							<label>Simulation Speed: {tickRate} tps</label>
							<input type="range" min="1" max="60" bind:value={tickRate} class="slider" />
						</div>

						<button class="create-btn" on:click={createNewRealm}>
							🌟 Manifest Realm
						</button>
					</div>
				{/if}

				<div class="section">
					<button class="secondary-btn" on:click={loadRealm}>
						📂 Load Saved Realm
					</button>
				</div>
			{:else}
				<!-- Realm Active -->
				<div class="realm-info">
					<div class="realm-name">{realm.config.name}</div>
					<div class="realm-deity">🕊️ {realm.config.supremeBeing.name}</div>
					<div class="realm-directive">{realm.config.primeDirective.goal}</div>
				</div>

				<div class="stats-grid">
					<div class="stat">
						<div class="stat-label">Tick</div>
						<div class="stat-value">{realm.currentTick.toLocaleString()}</div>
					</div>
					<div class="stat">
						<div class="stat-label">Population</div>
						<div class="stat-value" class:warning={realm.beingStats.currentPopulation < 50}>
							{realm.beingStats.currentPopulation}
						</div>
					</div>
					<div class="stat">
						<div class="stat-label">Avg Fitness</div>
						<div class="stat-value">{realm.beingStats.averageFitness.toFixed(3)}</div>
					</div>
					<div class="stat">
						<div class="stat-label">Diversity</div>
						<div class="stat-value">{realm.beingStats.geneticDiversity.toFixed(3)}</div>
					</div>
					<div class="stat">
						<div class="stat-label">Births</div>
						<div class="stat-value">{realm.beingStats.totalBirths.toLocaleString()}</div>
					</div>
					<div class="stat">
						<div class="stat-label">Deaths</div>
						<div class="stat-value">{realm.beingStats.totalDeaths.toLocaleString()}</div>
					</div>
				</div>

				<div class="epoch-info">
					<div class="epoch-name">📜 {realm.currentEpoch.name}</div>
					<div class="epoch-progress">
						{realm.currentTick - realm.currentEpoch.startTick} / {realm.config.ticksPerEpoch} ticks
					</div>
				</div>

				<div class="controls">
					{#if realm.running}
						<button class="stop-btn" on:click={stopSimulation}>
							⏸️ Pause
						</button>
					{:else}
						<button class="start-btn" on:click={startSimulation}>
							▶️ Start
						</button>
					{/if}

					<div class="speed-control">
						<button class="speed-btn" on:click={() => adjustTickRate(-5)}>-</button>
						<span class="speed-display">{realm.tickRate} tps</span>
						<button class="speed-btn" on:click={() => adjustTickRate(5)}>+</button>
					</div>
				</div>

				<div class="actions">
					<button class="action-btn" on:click={saveRealm}>💾 Save</button>
					<button class="action-btn" on:click={exportReport}>📄 Export Report</button>
					<button class="action-btn danger" on:click={resetRealm}>🔄 Reset</button>
				</div>
			{/if}
		</div>
	{/if}
</div>

<style>
	.realm-control {
		position: absolute;
		top: 80px;
		left: 20px;
		width: 320px;
		background: rgba(20, 20, 30, 0.95);
		border: 2px solid #f0f;
		border-radius: 8px;
		backdrop-filter: blur(10px);
		box-shadow: 0 0 30px rgba(255, 0, 255, 0.3);
		z-index: 100;
		font-family: 'Courier New', monospace;
	}

	.realm-control.collapsed {
		width: 200px;
	}

	.control-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 12px 16px;
		background: rgba(255, 0, 255, 0.1);
		border-bottom: 1px solid #f0f;
		cursor: pointer;
		user-select: none;
	}

	.control-header:hover {
		background: rgba(255, 0, 255, 0.15);
	}

	.header-title {
		font-size: 0.9rem;
		font-weight: 600;
		color: #f0f;
		letter-spacing: 1px;
	}

	.collapse-btn {
		background: none;
		border: 1px solid #f0f;
		color: #f0f;
		padding: 4px 8px;
		border-radius: 4px;
		cursor: pointer;
		font-size: 0.8rem;
	}

	.control-body {
		padding: 16px;
		max-height: calc(100vh - 200px);
		overflow-y: auto;
	}

	.control-body::-webkit-scrollbar {
		width: 6px;
	}

	.control-body::-webkit-scrollbar-track {
		background: rgba(0, 0, 0, 0.2);
	}

	.control-body::-webkit-scrollbar-thumb {
		background: #f0f;
		border-radius: 3px;
	}

	.section {
		margin-bottom: 12px;
	}

	.primary-btn, .secondary-btn, .create-btn {
		width: 100%;
		padding: 12px;
		border-radius: 6px;
		font-family: 'Courier New', monospace;
		font-size: 0.9rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s;
	}

	.primary-btn {
		background: linear-gradient(135deg, #f0f 0%, #90f 100%);
		border: none;
		color: #fff;
	}

	.primary-btn:hover {
		box-shadow: 0 0 20px rgba(255, 0, 255, 0.5);
	}

	.secondary-btn {
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid #f0f;
		color: #f0f;
	}

	.secondary-btn:hover {
		background: rgba(255, 0, 255, 0.1);
	}

	.config-panel {
		margin-top: 16px;
		padding: 16px;
		background: rgba(0, 0, 0, 0.3);
		border: 1px solid #f0f;
		border-radius: 6px;
	}

	.config-section {
		margin-bottom: 16px;
	}

	.config-section label {
		display: block;
		font-size: 0.8rem;
		color: #f0f;
		margin-bottom: 6px;
		font-weight: 600;
	}

	.text-input, .select-input {
		width: 100%;
		padding: 8px;
		background: rgba(0, 0, 0, 0.4);
		border: 1px solid #f0f;
		border-radius: 4px;
		color: #fff;
		font-family: 'Courier New', monospace;
		font-size: 0.85rem;
	}

	.slider {
		width: 100%;
		-webkit-appearance: none;
		height: 6px;
		border-radius: 3px;
		background: rgba(255, 0, 255, 0.2);
		outline: none;
	}

	.slider::-webkit-slider-thumb {
		-webkit-appearance: none;
		width: 16px;
		height: 16px;
		border-radius: 50%;
		background: #f0f;
		cursor: pointer;
	}

	.help-text {
		font-size: 0.7rem;
		color: #999;
		margin-top: 4px;
		line-height: 1.4;
	}

	.create-btn {
		background: linear-gradient(135deg, #0f3 0%, #0af 100%);
		border: none;
		color: #fff;
		margin-top: 20px;
	}

	.create-btn:hover {
		box-shadow: 0 0 20px rgba(0, 255, 51, 0.5);
	}

	.realm-info {
		margin-bottom: 16px;
		padding: 12px;
		background: rgba(255, 0, 255, 0.1);
		border: 1px solid #f0f;
		border-radius: 6px;
	}

	.realm-name {
		font-size: 1rem;
		font-weight: 600;
		color: #f0f;
		margin-bottom: 8px;
	}

	.realm-deity {
		font-size: 0.85rem;
		color: #fff;
		margin-bottom: 4px;
	}

	.realm-directive {
		font-size: 0.75rem;
		color: #999;
		font-style: italic;
	}

	.stats-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 8px;
		margin-bottom: 16px;
	}

	.stat {
		background: rgba(0, 0, 0, 0.3);
		padding: 8px;
		border-radius: 4px;
		border: 1px solid #333;
	}

	.stat-label {
		font-size: 0.7rem;
		color: #999;
		margin-bottom: 4px;
	}

	.stat-value {
		font-size: 0.9rem;
		color: #0f3;
		font-weight: 600;
	}

	.stat-value.warning {
		color: #f90;
	}

	.epoch-info {
		background: rgba(0, 170, 255, 0.1);
		padding: 10px;
		border: 1px solid #0af;
		border-radius: 6px;
		margin-bottom: 16px;
	}

	.epoch-name {
		font-size: 0.85rem;
		color: #0af;
		font-weight: 600;
		margin-bottom: 4px;
	}

	.epoch-progress {
		font-size: 0.7rem;
		color: #999;
	}

	.controls {
		display: flex;
		gap: 12px;
		margin-bottom: 16px;
	}

	.start-btn, .stop-btn {
		flex: 1;
		padding: 12px;
		border-radius: 6px;
		font-family: 'Courier New', monospace;
		font-size: 0.9rem;
		font-weight: 600;
		cursor: pointer;
		border: none;
		color: #fff;
	}

	.start-btn {
		background: linear-gradient(135deg, #0f3 0%, #0af 100%);
	}

	.stop-btn {
		background: linear-gradient(135deg, #f90 0%, #f30 100%);
	}

	.speed-control {
		display: flex;
		align-items: center;
		gap: 8px;
		background: rgba(0, 0, 0, 0.3);
		padding: 8px 12px;
		border-radius: 6px;
		border: 1px solid #f0f;
	}

	.speed-btn {
		background: #f0f;
		border: none;
		color: #fff;
		width: 24px;
		height: 24px;
		border-radius: 4px;
		cursor: pointer;
		font-weight: 600;
	}

	.speed-display {
		font-size: 0.8rem;
		color: #f0f;
		min-width: 50px;
		text-align: center;
	}

	.actions {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 8px;
	}

	.action-btn {
		padding: 8px;
		border-radius: 4px;
		font-family: 'Courier New', monospace;
		font-size: 0.75rem;
		font-weight: 600;
		cursor: pointer;
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid #f0f;
		color: #f0f;
	}

	.action-btn:hover {
		background: rgba(255, 0, 255, 0.1);
	}

	.action-btn.danger {
		border-color: #f30;
		color: #f30;
	}

	.action-btn.danger:hover {
		background: rgba(255, 51, 0, 0.1);
	}
</style>
