<script lang="ts">
	import { onMount } from 'svelte';
	import BeingRenderer from '$lib/components/lab/BeingRenderer.svelte';
	import DataTable from '$lib/components/lab/DataTable.svelte';
	import TutorialPanel from '$lib/components/lab/TutorialPanel.svelte';
	import VillageRenderer from '$lib/components/lab/VillageRenderer.svelte';
	import ResourcePanel from '$lib/components/lab/ResourcePanel.svelte';
	import BuildingPalette from '$lib/components/lab/BuildingPalette.svelte';
	import WorkerAssignment from '$lib/components/lab/WorkerAssignment.svelte';

	import type { Realm, RealmConfig } from '$lib/models/Realm';
	import type { Village, Building } from '$lib/models/Village';
	import type { Tutorial } from '$lib/models/Tutorial';
	import { SUPREME_BEINGS, PRIME_DIRECTIVES } from '$lib/models/Realm';
	import { VillageEvolutionEngine } from '$lib/models/VillageEvolution';
	import { createVillage, placeBuilding, assignWorker, BUILDING_TEMPLATES } from '$lib/models/Village';
	import { GENESIS_FARM_TUTORIAL, triggerDrought, checkStepCompletion } from '$lib/models/Tutorial';
	import { initializePopulation } from '$lib/models/Evolution';
	import { createRealm } from '$lib/models/Realm';
	export let params: Record<string, string> | undefined = undefined;
	void params;

	let showSplash = true;
	let asciiLine = 0;

	const ascii = [
		"",
		"    ██╗    ██╗ █████╗ ███████╗████████╗",
		"    ██║    ██║██╔══██╗██╔════╝╚══██╔══╝",
		"    ██║ █╗ ██║███████║█████╗     ██║   ",
		"    ██║███╗██║██╔══██║██╔══╝     ██║   ",
		"    ╚███╔███╔╝██║  ██║██║        ██║   ",
		"     ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝        ╚═╝   ",
		"",
		"    ██╗   ██╗██╗██╗     ██╗      █████╗  ██████╗ ███████╗",
		"    ██║   ██║██║██║     ██║     ██╔══██╗██╔════╝ ██╔════╝",
		"    ██║   ██║██║██║     ██║     ███████║██║  ███╗█████╗  ",
		"    ╚██╗ ██╔╝██║██║     ██║     ██╔══██║██║   ██║██╔══╝  ",
		"     ╚████╔╝ ██║███████╗███████╗██║  ██║╚██████╔╝███████╗",
		"      ╚═══╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝",
		"",
		"",
		"           🌾 GENESIS FARM 2025 - Evolutionary City Builder 🌾",
		"",
		"                   [Initializing Tutorial Systems...]",
		"",
		"              >>> Spawning 10 genetically diverse beings...",
		"              >>> Establishing resource pools...",
		"              >>> Loading building templates...",
		"              >>> Preparing challenge scenarios...",
		"",
		"                   [Press ENTER to begin your village]"
	];

	let displayedLines: string[] = [];
	let loading = true;
	let readyToEnter = false;

	// Lab state
	let canvasWidth = 0;
	let canvasHeight = 0;

	// Village & Evolution state
	let realm: Realm | null = null;
	let village: Village | null = null;
	let tutorial: Tutorial | null = null;
	let evolutionEngine: VillageEvolutionEngine | null = null;

	// UI state
	let selectedBuilding: Building | null = null;
	let showWorkerAssignment = false;

	// Tutorial mode flag
	let tutorialMode = false;
	let sandboxMode = false;

	onMount(() => {
		// Animate ASCII art line by line
		const interval = setInterval(() => {
			if (asciiLine < ascii.length) {
				displayedLines = [...displayedLines, ascii[asciiLine]];
				asciiLine++;
			} else {
				clearInterval(interval);
				loading = false;
				setTimeout(() => {
					readyToEnter = true;
				}, 500);
			}
		}, 80);

		// Listen for Enter key
		const handleKeyPress = (e: KeyboardEvent) => {
			if (e.key === 'Enter' && readyToEnter) {
				enterLab();
			}
		};

		window.addEventListener('keydown', handleKeyPress);

		return () => {
			clearInterval(interval);
			window.removeEventListener('keydown', handleKeyPress);
		};
	});

	function enterLab() {
		showSplash = false;
		// Start tutorial automatically
		startTutorial();
	}

	function startTutorial() {
		tutorialMode = true;
		sandboxMode = false;

		// Create tutorial realm with Genesis Farm config
		const config: RealmConfig = {
			name: 'Genesis Farm',
			description: 'Tutorial village - learn to build and evolve',
			initialPopulation: 10,
			worldWidth: canvasWidth || 1920,
			worldHeight: canvasHeight || 1080,
			ticksPerEpoch: 1000,
			supremeBeing: SUPREME_BEINGS[0], // Harmonia - benevolent
			primeDirective: PRIME_DIRECTIVES.harmony
		};

		realm = createRealm(config);
		realm.tickRate = 10;

		// Initialize population
		const beings = initializePopulation(realm, 10, canvasWidth || 1920, canvasHeight || 1080);
		realm.beings = beings;

		// Create village
		village = createVillage('Genesis Farm');

		// Initialize tutorial
		tutorial = { ...GENESIS_FARM_TUTORIAL };
		tutorial.startTick = realm.currentTick;

		// Create evolution engine with village
		evolutionEngine = new VillageEvolutionEngine(realm, village);

		console.log('🌾 Genesis Farm tutorial started!');
	}

	function handleBuildingDrop(event: DragEvent) {
		event.preventDefault();
		if (!village || !realm) return;

		const data = event.dataTransfer?.getData('building-template');
		if (!data) return;

		const template = JSON.parse(data);
		const canvas = document.getElementById('lab-canvas');
		if (!canvas) return;

		const rect = canvas.getBoundingClientRect();
		const x = event.clientX - rect.left;
		const y = event.clientY - rect.top;

		// Place building
		const building = placeBuilding(village, template, x, y);

		if (building) {
			console.log('🏗️ Building placed:', template.name);
			village = village; // Trigger reactivity
		} else {
			console.log('❌ Cannot afford building');
		}
	}

	function handleDragOver(event: DragEvent) {
		event.preventDefault();
		if (event.dataTransfer) {
			event.dataTransfer.dropEffect = 'copy';
		}
	}

	function handleBuildingClick(building: Building) {
		if (!building.operational) return; // Can't assign workers to under-construction buildings

		selectedBuilding = building;
		showWorkerAssignment = true;
	}

	function handleAssignWorker(event: CustomEvent) {
		if (!village || !realm) return;

		const { building, being } = event.detail;
		const productivity = assignWorker(village, building, being);

		if (productivity > 0) {
			console.log(`👷 Assigned ${being.id} to ${building.template.name} - productivity: ${(productivity * 100).toFixed(0)}%`);
			village = village; // Trigger reactivity
		}
	}

	function handleUnassignWorker(event: CustomEvent) {
		if (!village) return;

		const { building, being } = event.detail;

		// Remove from building
		building.assignedWorkers = building.assignedWorkers.filter(id => id !== being.id);

		// Remove job
		village.jobs = village.jobs.filter(j => j.beingId !== being.id);

		console.log(`🚫 Unassigned ${being.id} from ${building.template.name}`);
		village = village; // Trigger reactivity
	}

	function handleStartSimulation() {
		if (!evolutionEngine || !realm) return;
		evolutionEngine.start();
		console.log('▶️ Simulation started');
	}

	function handleStopSimulation() {
		if (!evolutionEngine || !realm) return;
		evolutionEngine.stop();
		console.log('⏸️ Simulation paused');
	}

	// Tutorial event handlers
	function handleTutorialMessage(event: CustomEvent) {
		const { text } = event.detail;
		console.log('✨', text);
		// TODO: Show toast notification
	}

	function handleTutorialComplete() {
		if (!tutorial) return;
		console.log('🎉 Tutorial complete!');
	}

	function handleTutorialSkip() {
		tutorial = null;
		tutorialMode = false;
		sandboxMode = true;
		console.log('⏭️ Tutorial skipped - sandbox mode active');
	}

	function handleSandboxMode() {
		tutorialMode = false;
		sandboxMode = true;
		tutorial = null;
		console.log('🎨 Sandbox mode activated!');
	}

	function handleContinueVillage() {
		tutorialMode = false;
		sandboxMode = false;
		tutorial = null;
		console.log('🌾 Continuing village in freeplay mode');
	}

	function handleTriggerDrought() {
		if (!village) return;
		triggerDrought(village);
		console.log('☀️ DROUGHT EVENT TRIGGERED! Well production reduced by 75%');
	}

	// Reactive: auto-start simulation when tutorial begins
	$: if (tutorialMode && evolutionEngine && !realm?.running) {
		evolutionEngine.start();
	}
</script>

{#if showSplash}
	<div class="splash-screen">
		<div class="crt-effect">
			<pre class="ascii-art">{displayedLines.join('\n')}</pre>
			{#if readyToEnter}
				<div class="enter-prompt">
					<button class="enter-button" on:click={enterLab}>
						<span class="pulse">▶</span> ENTER VILLAGE
					</button>
				</div>
			{/if}
		</div>
		<div class="scanline"></div>
	</div>
{:else}
	<!-- VILLAGE BUILDER -->
	<div class="lab-container">
		<div class="lab-header">
			<div class="header-left">
				<h1>🌾 WAFT VILLAGE - Evolutionary City Builder</h1>
				<div class="status-indicators">
					{#if tutorialMode}
						<span class="indicator active">TUTORIAL</span>
					{/if}
					{#if sandboxMode}
						<span class="indicator active">SANDBOX</span>
					{/if}
					{#if realm}
						<span class="indicator active">REALM</span>
					{/if}
					{#if village}
						<span class="indicator active">VILLAGE</span>
					{/if}
					{#if realm?.running}
						<span class="indicator active">RUNNING</span>
					{/if}
				</div>
			</div>
			<div class="header-right">
				{#if realm}
					<div class="tick-info">
						Tick: {realm.currentTick.toLocaleString()} |
						Pop: {realm.beings.filter(b => b.alive).length}
					</div>
				{/if}
			</div>
		</div>

		<div
			class="lab-canvas"
			id="lab-canvas"
			bind:clientWidth={canvasWidth}
			bind:clientHeight={canvasHeight}
			on:drop={handleBuildingDrop}
			on:dragover={handleDragOver}
		>
			<div class="grid-overlay"></div>

			<!-- Village Renderer (buildings) -->
			{#if village}
				<VillageRenderer
					{village}
					width={canvasWidth}
					height={canvasHeight}
					bind:selectedBuilding
					on:buildingclick={(e) => handleBuildingClick(e.detail)}
				/>
			{/if}

			<!-- Being Renderer (evolutionary organisms) -->
			{#if realm}
				<BeingRenderer
					beings={realm.beings}
					width={canvasWidth}
					height={canvasHeight}
					showLabels={false}
					showFitness={true}
				/>
			{/if}

			<!-- Tutorial Panel -->
			{#if tutorial && tutorialMode}
				<TutorialPanel
					{tutorial}
					{village}
					beings={realm?.beings || []}
					currentTick={realm?.currentTick || 0}
					on:message={handleTutorialMessage}
					on:complete={handleTutorialComplete}
					on:skip={handleTutorialSkip}
					on:sandbox={handleSandboxMode}
					on:continue={handleContinueVillage}
					on:trigger-drought={handleTriggerDrought}
				/>
			{/if}

			<!-- Resource Panel -->
			{#if village}
				<ResourcePanel {village} />
			{/if}

			<!-- Building Palette -->
			{#if village}
				<BuildingPalette {village} />
			{/if}

			<!-- Data Table -->
			{#if realm && !tutorialMode}
				<DataTable {realm} />
			{/if}

			<!-- Worker Assignment Modal -->
			{#if showWorkerAssignment && selectedBuilding && realm}
				<WorkerAssignment
					building={selectedBuilding}
					beings={realm.beings}
					{village}
					on:assign={handleAssignWorker}
					on:unassign={handleUnassignWorker}
					on:close={() => showWorkerAssignment = false}
				/>
			{/if}

			<!-- Simulation Controls (bottom-left) -->
			{#if realm}
				<div class="sim-controls">
					{#if realm.running}
						<button class="control-btn stop" on:click={handleStopSimulation}>
							⏸️ Pause
						</button>
					{:else}
						<button class="control-btn start" on:click={handleStartSimulation}>
							▶️ Start
						</button>
					{/if}
					<div class="tick-rate">
						{realm.tickRate} tps
					</div>
				</div>
			{/if}
		</div>
	</div>
{/if}

<style>
	:global(body) {
		margin: 0;
		padding: 0;
		overflow: hidden;
	}

	/* SPLASH SCREEN */
	.splash-screen {
		position: fixed;
		top: 0;
		left: 0;
		width: 100vw;
		height: 100vh;
		background: #000;
		color: #0f0;
		font-family: 'Courier New', monospace;
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
	}

	.crt-effect {
		position: relative;
		z-index: 2;
		animation: flicker 0.15s infinite;
	}

	@keyframes flicker {
		0% { opacity: 1; }
		50% { opacity: 0.98; }
		100% { opacity: 1; }
	}

	.ascii-art {
		font-size: 11px;
		line-height: 1.2;
		text-shadow: 0 0 5px #0f0, 0 0 10px #0f0;
		white-space: pre;
		margin: 0;
	}

	.enter-prompt {
		text-align: center;
		margin-top: 20px;
		animation: fadeIn 0.5s ease-in;
	}

	@keyframes fadeIn {
		from { opacity: 0; }
		to { opacity: 1; }
	}

	.enter-button {
		background: none;
		border: 2px solid #0f0;
		color: #0f0;
		padding: 12px 30px;
		font-family: 'Courier New', monospace;
		font-size: 16px;
		cursor: pointer;
		transition: all 0.3s;
		text-shadow: 0 0 5px #0f0;
	}

	.enter-button:hover {
		background: #0f0;
		color: #000;
		box-shadow: 0 0 20px #0f0;
	}

	.pulse {
		animation: pulse 1s infinite;
	}

	@keyframes pulse {
		0%, 100% { opacity: 1; }
		50% { opacity: 0.3; }
	}

	.scanline {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: linear-gradient(
			to bottom,
			transparent 50%,
			rgba(0, 255, 0, 0.03) 51%
		);
		background-size: 100% 4px;
		pointer-events: none;
		animation: scan 8s linear infinite;
	}

	@keyframes scan {
		0% { transform: translateY(-100%); }
		100% { transform: translateY(100%); }
	}

	/* LAB CONTAINER */
	.lab-container {
		width: 100vw;
		height: 100vh;
		background: #0a0a0a;
		color: #e0e0e0;
		display: flex;
		flex-direction: column;
		overflow: hidden;
	}

	.lab-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 10px 20px;
		background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
		border-bottom: 2px solid #0f3;
		box-shadow: 0 0 20px rgba(0, 255, 51, 0.3);
	}

	.lab-header h1 {
		margin: 0;
		font-size: 1.2rem;
		color: #0f3;
		text-shadow: 0 0 10px rgba(0, 255, 51, 0.5);
	}

	.status-indicators {
		display: flex;
		gap: 8px;
		margin-top: 5px;
	}

	.indicator {
		font-size: 0.7rem;
		padding: 2px 8px;
		border: 1px solid #333;
		border-radius: 3px;
		color: #666;
		background: #111;
		transition: all 0.3s;
	}

	.indicator.active {
		border-color: #0f3;
		color: #0f3;
		box-shadow: 0 0 5px rgba(0, 255, 51, 0.3);
		animation: blink 2s infinite;
	}

	@keyframes blink {
		0%, 100% { opacity: 1; }
		50% { opacity: 0.5; }
	}

	.tick-info {
		font-family: 'Courier New', monospace;
		font-size: 0.8rem;
		color: #0f3;
		padding: 5px 10px;
		border: 1px solid #0f3;
		border-radius: 3px;
		background: rgba(0, 255, 51, 0.05);
	}

	.lab-canvas {
		flex: 1;
		position: relative;
		overflow: hidden;
		background:
			linear-gradient(90deg, rgba(0, 255, 51, 0.03) 1px, transparent 1px),
			linear-gradient(rgba(0, 255, 51, 0.03) 1px, transparent 1px);
		background-size: 40px 40px;
		background-position: -1px -1px;
	}

	.grid-overlay {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		pointer-events: none;
	}

	.sim-controls {
		position: absolute;
		bottom: 20px;
		left: 20px;
		display: flex;
		gap: 12px;
		align-items: center;
		background: rgba(20, 20, 30, 0.95);
		border: 2px solid #0f3;
		border-radius: 8px;
		padding: 12px;
		backdrop-filter: blur(10px);
		box-shadow: 0 0 20px rgba(0, 255, 51, 0.3);
	}

	.control-btn {
		padding: 10px 20px;
		border-radius: 6px;
		font-family: 'Courier New', monospace;
		font-size: 0.9rem;
		font-weight: 600;
		cursor: pointer;
		border: none;
		color: #fff;
		transition: all 0.2s;
	}

	.control-btn.start {
		background: linear-gradient(135deg, #0f3 0%, #0af 100%);
	}

	.control-btn.start:hover {
		box-shadow: 0 0 20px rgba(0, 255, 51, 0.5);
	}

	.control-btn.stop {
		background: linear-gradient(135deg, #f90 0%, #f30 100%);
	}

	.control-btn.stop:hover {
		box-shadow: 0 0 20px rgba(255, 153, 0, 0.5);
	}

	.tick-rate {
		font-size: 0.8rem;
		color: #0f3;
		padding: 8px 12px;
		background: rgba(0, 255, 51, 0.1);
		border-radius: 4px;
		font-family: 'Courier New', monospace;
	}
</style>
