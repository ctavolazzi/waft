<script lang="ts">
	import { onMount } from 'svelte';
	import Node from '$lib/components/lab/Node.svelte';
	import Switch from '$lib/components/lab/controls/Switch.svelte';
	import Dial from '$lib/components/lab/controls/Dial.svelte';
	import Light from '$lib/components/lab/controls/Light.svelte';
	import Button from '$lib/components/lab/controls/Button.svelte';
	import ParticleSystem from '$lib/components/lab/ParticleSystem.svelte';
	import ComponentPalette from '$lib/components/lab/ComponentPalette.svelte';
	import WiringSystem from '$lib/components/lab/WiringSystem.svelte';
	import RealmControl from '$lib/components/lab/RealmControl.svelte';
	import BeingRenderer from '$lib/components/lab/BeingRenderer.svelte';
	import DataTable from '$lib/components/lab/DataTable.svelte';

	import type { Realm } from '$lib/models/Realm';
	import { EvolutionEngine } from '$lib/models/Evolution';
	import { serializeRealm, deserializeRealm } from '$lib/models/Realm';

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
		"    ███████╗██╗      ██████╗ ██╗    ██╗",
		"    ██╔════╝██║     ██╔═══██╗██║    ██║",
		"    █████╗  ██║     ██║   ██║██║ █╗ ██║",
		"    ██╔══╝  ██║     ██║   ██║██║███╗██║",
		"    ██║     ███████╗╚██████╔╝╚███╔███╔╝",
		"    ╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝ ",
		"",
		"    ██╗      █████╗ ██████╗  ██████╗ ██████╗  █████╗ ████████╗ ██████╗ ██████╗ ██╗   ██╗",
		"    ██║     ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ██╔╝",
		"    ██║     ███████║██████╔╝██║   ██║██████╔╝███████║   ██║   ██║   ██║██████╔╝ ╚████╔╝ ",
		"    ██║     ██╔══██║██╔══██╗██║   ██║██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗  ╚██╔╝  ",
		"    ███████╗██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║   ██║   ",
		"    ╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ",
		"",
		"",
		"                        Evolutionary Code Laboratory",
		"                        Visual Agent Flow Composer",
		"",
		"                        [Initializing Systems...]",
		"",
		"                        >>> Loading quantum substrate...",
		"                        >>> Calibrating reality anchors...",
		"                        >>> Spinning up agent spawners...",
		"                        >>> Establishing gym connections...",
		"                        >>> Activating scint detectors...",
		"",
		"                        [Press ENTER to begin composition]"
	];

	let displayedLines: string[] = [];
	let loading = true;
	let readyToEnter = false;

	// Lab state
	let canvasWidth = 0;
	let canvasHeight = 0;
	let nodes: any[] = [];

	// Brewery state
	let breweryActive = false;
	let mashTemp = 65;
	let mashTime = 60;
	let boilActive = false;
	let boilPower = 75;
	let fermentDays = 14;
	let fermenterTempOk = true;
	let bottledBeers = 0;
	let masterPower = false;
	let flowRate = 50;

	// Tracked components for particle system (x, y, w, h, active, type)
	let trackedComponents: Array<{x: number, y: number, w: number, h: number, active: boolean, type: string}> = [];

	// Connections (wires) for both old SVG and new WiringSystem
	let connections = [
		{ id: 'conn-1', fromNode: 'input-1', fromPort: 'out1', toNode: 'process-1', toPort: 'in1', x1: 220, y1: 180, x2: 400, y2: 130, active: false },
		{ id: 'conn-2', fromNode: 'input-1', fromPort: 'out2', toNode: 'process-2', toPort: 'in1', x1: 220, y1: 200, x2: 400, y2: 310, active: false },
		{ id: 'conn-3', fromNode: 'process-1', fromPort: 'out1', toNode: 'process-3', toPort: 'in1', x1: 520, y1: 130, x2: 700, y2: 200, active: false },
		{ id: 'conn-4', fromNode: 'process-2', fromPort: 'out1', toNode: 'process-3', toPort: 'in2', x1: 520, y1: 310, x2: 700, y2: 210, active: false },
		{ id: 'conn-5', fromNode: 'process-3', fromPort: 'out1', toNode: 'output-1', toPort: 'in1', x1: 820, y1: 210, x2: 1000, y2: 210, active: false }
	];

	let wiringSystemRef: any;

	// Realm & Evolution state
	let realm: Realm | null = null;
	let evolutionEngine: EvolutionEngine | null = null;

	// Update connections when brewery is active
	$: {
		if (breweryActive) {
			connections = connections.map(c => ({ ...c, active: true }));
			// Simulate brewing
			const interval = setInterval(() => {
				if (breweryActive) {
					bottledBeers += 1;
					fermenterTempOk = Math.random() > 0.3;
				}
			}, 2000);
		} else {
			connections = connections.map(c => ({ ...c, active: false }));
		}
	}

	// Update tracked components for particle system
	$: trackedComponents = [
		{ x: 100, y: 150, w: 200, h: 150, active: breweryActive, type: 'input' },
		{ x: 400, y: 100, w: 200, h: 150, active: breweryActive, type: 'process' },
		{ x: 400, y: 280, w: 200, h: 150, active: breweryActive && boilActive, type: 'process' },
		{ x: 700, y: 180, w: 200, h: 150, active: breweryActive, type: 'process' },
		{ x: 1000, y: 180, w: 200, h: 200, active: breweryActive, type: 'output' }
	];

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
	}

	function handleNodeDrag(event: CustomEvent) {
		const { id, x, y } = event.detail;
		// Update node position (would need to track nodes in state)
		console.log(`Node ${id} dragged to`, x, y);
	}

	function emergencyStop() {
		breweryActive = false;
		boilActive = false;
		masterPower = false;
		bottledBeers = 0;
	}

	// Handle component drop from palette
	function handleDrop(event: DragEvent) {
		event.preventDefault();
		const data = event.dataTransfer?.getData('component-template');
		if (!data) return;

		const template = JSON.parse(data);
		const canvas = document.getElementById('lab-canvas');
		if (!canvas) return;

		const rect = canvas.getBoundingClientRect();
		const x = event.clientX - rect.left;
		const y = event.clientY - rect.top;

		console.log('🎨 Dropped component:', template.name, 'at', x, y);

		// Add new tracked component for particles to swarm
		trackedComponents = [...trackedComponents, {
			x: x - 100,
			y: y - 75,
			w: 200,
			h: 150,
			active: true,
			type: template.type
		}];

		// TODO: Create actual node instance
	}

	function handleDragOver(event: DragEvent) {
		event.preventDefault();
		if (event.dataTransfer) {
			event.dataTransfer.dropEffect = 'copy';
		}
	}

	// Handle new connection creation
	function handleConnect(event: CustomEvent) {
		const { fromNode, fromPort, toNode, toPort } = event.detail;
		console.log('🔗 New connection:', fromNode, fromPort, '->', toNode, toPort);

		// TODO: Calculate connection coordinates and add to connections array
	}

	// Handle connection deletion
	function handleDeleteConnection(event: CustomEvent) {
		const { connectionId } = event.detail;
		connections = connections.filter(c => c.id !== connectionId);
		console.log('❌ Deleted connection:', connectionId);
	}

	// Realm event handlers
	function handleRealmCreated(event: CustomEvent) {
		realm = event.detail.realm;
		evolutionEngine = new EvolutionEngine(realm);
		console.log('🌌 Realm created:', realm.config.name);
	}

	function handleStartSimulation() {
		if (!evolutionEngine) return;
		evolutionEngine.start();
		console.log('▶️ Evolution started');
	}

	function handleStopSimulation() {
		if (!evolutionEngine) return;
		evolutionEngine.stop();
		console.log('⏸️ Evolution paused');
	}

	function handleResetRealm() {
		if (evolutionEngine) {
			evolutionEngine.stop();
		}
		realm = null;
		evolutionEngine = null;
		console.log('🔄 Realm reset');
	}

	function handleSaveRealm(event: CustomEvent) {
		if (!realm) return;
		const json = serializeRealm(realm);
		const blob = new Blob([json], { type: 'application/json' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `${realm.config.name.replace(/\s+/g, '-')}-${Date.now()}.json`;
		a.click();
		URL.revokeObjectURL(url);
		console.log('💾 Realm saved');
	}

	function handleLoadRealm() {
		const input = document.createElement('input');
		input.type = 'file';
		input.accept = '.json';
		input.onchange = (e: Event) => {
			const file = (e.target as HTMLInputElement).files?.[0];
			if (!file) return;

			const reader = new FileReader();
			reader.onload = (e) => {
				try {
					const json = e.target?.result as string;
					realm = deserializeRealm(json);
					evolutionEngine = new EvolutionEngine(realm);
					console.log('📂 Realm loaded:', realm.config.name);
				} catch (error) {
					console.error('Failed to load realm:', error);
					alert('Failed to load realm file');
				}
			};
			reader.readAsText(file);
		};
		input.click();
	}

	function handleExportReport() {
		if (!realm) return;
		console.log('📄 Exporting report for', realm.config.name);
		// TODO: Generate Typst report and export as PDF
		alert('PDF export coming soon! This will generate a full scientific report.');
	}

	function handleTickRateChange(event: CustomEvent) {
		if (!evolutionEngine || !realm) return;
		// Restart with new tick rate
		const wasRunning = realm.running;
		if (wasRunning) {
			evolutionEngine.stop();
		}
		evolutionEngine = new EvolutionEngine(realm);
		if (wasRunning) {
			evolutionEngine.start();
		}
		console.log('⚡ Tick rate changed to', realm.tickRate);
	}
</script>

{#if showSplash}
	<div class="splash-screen">
		<div class="crt-effect">
			<pre class="ascii-art">{displayedLines.join('\n')}</pre>
			{#if readyToEnter}
				<div class="enter-prompt">
					<button class="enter-button" on:click={enterLab}>
						<span class="pulse">▶</span> ENTER LABORATORY
					</button>
				</div>
			{/if}
		</div>
		<div class="scanline"></div>
	</div>
{:else}
	<!-- FLOW COMPOSER -->
	<div class="lab-container">
		<div class="lab-header">
			<div class="header-left">
				<h1>🧪 WAFT FLOW LABORATORY</h1>
				<div class="status-indicators">
					<span class="indicator active">QUANTUM</span>
					<span class="indicator active">REALITY</span>
					<span class="indicator active">AGENTS</span>
					<span class="indicator" class:active={breweryActive}>BREWERY</span>
					<span class="indicator" class:active={masterPower}>POWER</span>
				</div>
			</div>
			<div class="header-right">
				<div class="screen-info">
					SCREEN: {typeof window !== 'undefined' ? window.innerWidth : 0}×{typeof window !== 'undefined' ? window.innerHeight : 0}px
				</div>
			</div>
		</div>

		<div
			class="lab-canvas"
			id="lab-canvas"
			bind:clientWidth={canvasWidth}
			bind:clientHeight={canvasHeight}
			on:drop={handleDrop}
			on:dragover={handleDragOver}
		>
			<div class="grid-overlay"></div>

			<!-- Wiring System (replaces hardcoded SVG) -->
			<WiringSystem
				bind:this={wiringSystemRef}
				{connections}
				width={canvasWidth}
				height={canvasHeight}
				on:connect={handleConnect}
				on:delete={handleDeleteConnection}
			/>

			<!-- Particle System - Living swarm intelligence -->
			<ParticleSystem
				width={canvasWidth}
				height={canvasHeight}
				particleCount={500}
				components={trackedComponents}
				{connections}
			/>

			<!-- Component Palette -->
			<ComponentPalette />

			<!-- Realm Control Panel -->
			<RealmControl
				bind:realm
				{canvasWidth}
				{canvasHeight}
				on:realmcreated={handleRealmCreated}
				on:start={handleStartSimulation}
				on:stop={handleStopSimulation}
				on:reset={handleResetRealm}
				on:save={handleSaveRealm}
				on:load={handleLoadRealm}
				on:export={handleExportReport}
				on:tickratechange={handleTickRateChange}
			/>

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

			<!-- Example Brewery Nodes -->
			<Node
				id="input-1"
				type="input"
				title="RAW INGREDIENTS"
				x={100}
				y={150}
				outputs={[{id: 'out1', label: 'malt'}, {id: 'out2', label: 'hops'}, {id: 'out3', label: 'yeast'}]}
				active={breweryActive}
				on:drag={handleNodeDrag}
			>
				<div style="display: flex; flex-direction: column; gap: 8px;">
					<Light label="MALT" on={breweryActive} color="#fb3" />
					<Light label="HOPS" on={breweryActive} color="#3f3" blinking={breweryActive} />
					<Light label="YEAST" on={breweryActive} color="#f93" />
				</div>
			</Node>

			<Node
				id="process-1"
				type="process"
				title="MASH TUN"
				x={400}
				y={100}
				inputs={[{id: 'in1', label: 'ingredients'}]}
				outputs={[{id: 'out1', label: 'wort'}]}
				active={breweryActive}
				on:drag={handleNodeDrag}
			>
				<div style="display: flex; gap: 12px; align-items: center;">
					<Dial label="TEMP" value={mashTemp} color="#f90" on:change={e => mashTemp = e.detail.value} />
					<Dial label="TIME" value={mashTime} color="#09f" on:change={e => mashTime = e.detail.value} />
				</div>
			</Node>

			<Node
				id="process-2"
				type="process"
				title="BOIL KETTLE"
				x={400}
				y={280}
				inputs={[{id: 'in1', label: 'wort'}]}
				outputs={[{id: 'out1', label: 'cooled wort'}]}
				active={breweryActive && boilActive}
				on:drag={handleNodeDrag}
			>
				<div style="display: flex; gap: 12px; align-items: center;">
					<Switch label="HEAT" on={boilActive} color="#f30" on:toggle={e => boilActive = e.detail.on} />
					<Dial label="POWER" value={boilPower} color="#f30" on:change={e => boilPower = e.detail.value} />
				</div>
			</Node>

			<Node
				id="process-3"
				type="process"
				title="FERMENTER"
				x={700}
				y={180}
				inputs={[{id: 'in1', label: 'wort'}, {id: 'in2', label: 'yeast'}]}
				outputs={[{id: 'out1', label: 'beer'}]}
				active={breweryActive}
				on:drag={handleNodeDrag}
			>
				<div style="display: flex; flex-direction: column; gap: 8px;">
					<div style="display: flex; gap: 12px; justify-content: center;">
						<Light label="ACTIVE" on={breweryActive} color="#0f3" blinking={breweryActive} />
						<Light label="TEMP OK" on={fermenterTempOk} color="#09f" />
					</div>
					<Dial label="DAYS" value={fermentDays} color="#f0f" on:change={e => fermentDays = e.detail.value} />
				</div>
			</Node>

			<Node
				id="output-1"
				type="output"
				title="BOTTLING LINE"
				x={1000}
				y={180}
				inputs={[{id: 'in1', label: 'beer'}]}
				active={breweryActive}
				on:drag={handleNodeDrag}
			>
				<div style="display: flex; flex-direction: column; gap: 12px; align-items: center;">
					<Button
						label={breweryActive ? 'STOP' : 'START'}
						color={breweryActive ? '#f30' : '#0f3'}
						size="large"
						on:press={() => {
							breweryActive = !breweryActive;
							if (breweryActive) boilActive = true;
						}}
					/>
					<div style="font-size: 0.9rem; color: #0f3; font-family: 'Courier New', monospace;">
						🍺 {bottledBeers} BOTTLES
					</div>
				</div>
			</Node>

			<!-- Control Panel -->
			<div class="control-panel">
				<div class="panel-header">⚙️ BREWERY CONTROLS</div>
				<div class="panel-body">
					<Button
						label="E-STOP"
						color="#f00"
						size="medium"
						on:press={emergencyStop}
					/>
					<Switch label="MASTER" on={masterPower} color="#0f3" on:toggle={e => masterPower = e.detail.on} />
					<Dial label="FLOW" value={flowRate} color="#0af" on:change={e => flowRate = e.detail.value} />
				</div>
			</div>

			<!-- Instructions -->
			<div class="instructions">
				<div class="instruction-header">💡 QUICK START</div>
				<div class="instruction-line">🎛️ Drag nodes to reposition</div>
				<div class="instruction-line">🎚️ Adjust dials and flip switches</div>
				<div class="instruction-line">🚀 Press GREEN button to START brewery</div>
				<div class="instruction-line">🔴 Press RED button for emergency stop</div>
				<div class="instruction-line">⚡ Watch flow animation when active</div>
			</div>
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

	.screen-info {
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

	.wire-layer {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: 1;
	}

	.control-panel {
		position: absolute;
		bottom: 20px;
		left: 20px;
		background: rgba(20, 20, 30, 0.95);
		border: 2px solid #0f3;
		border-radius: 8px;
		padding: 12px;
		backdrop-filter: blur(10px);
		box-shadow: 0 0 20px rgba(0, 255, 51, 0.3);
	}

	.panel-header {
		font-size: 0.8rem;
		font-weight: 600;
		color: #0f3;
		margin-bottom: 12px;
		font-family: 'Courier New', monospace;
		text-align: center;
		letter-spacing: 2px;
	}

	.panel-body {
		display: flex;
		gap: 16px;
		align-items: center;
	}

	.instructions {
		position: absolute;
		bottom: 20px;
		right: 20px;
		background: rgba(20, 20, 30, 0.95);
		border: 2px solid #0af;
		border-radius: 8px;
		padding: 12px 16px;
		backdrop-filter: blur(10px);
		box-shadow: 0 0 20px rgba(0, 170, 255, 0.3);
	}

	.instruction-header {
		font-size: 0.8rem;
		font-weight: 600;
		color: #0af;
		margin-bottom: 8px;
		font-family: 'Courier New', monospace;
		letter-spacing: 1px;
	}

	.instruction-line {
		font-size: 0.75rem;
		color: #999;
		margin: 4px 0;
		font-family: 'Courier New', monospace;
	}
</style>
