<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	interface ComponentTemplate {
		id: string;
		type: 'input' | 'process' | 'output' | 'effect';
		name: string;
		icon: string;
		description: string;
		color: string;
		shape: 'square' | 'circle' | 'hexagon' | 'diamond';
		inputs: number;
		outputs: number;
	}

	const componentLibrary: Record<string, ComponentTemplate[]> = {
		sources: [
			{
				id: 'data-source',
				type: 'input',
				name: 'Data Source',
				icon: '💾',
				description: 'Emits data particles',
				color: '#09f',
				shape: 'square',
				inputs: 0,
				outputs: 1
			},
			{
				id: 'sensor',
				type: 'input',
				name: 'Sensor',
				icon: '📡',
				description: 'Detects environmental changes',
				color: '#0af',
				shape: 'circle',
				inputs: 0,
				outputs: 2
			},
			{
				id: 'trigger',
				type: 'input',
				name: 'Trigger',
				icon: '⚡',
				description: 'Manual activation point',
				color: '#fb3',
				shape: 'diamond',
				inputs: 0,
				outputs: 1
			}
		],
		transforms: [
			{
				id: 'filter',
				type: 'process',
				name: 'Filter',
				icon: '🔍',
				description: 'Filters data by criteria',
				color: '#f90',
				shape: 'hexagon',
				inputs: 1,
				outputs: 1
			},
			{
				id: 'mapper',
				type: 'process',
				name: 'Mapper',
				icon: '🗺️',
				description: 'Transforms data structure',
				color: '#f60',
				shape: 'hexagon',
				inputs: 1,
				outputs: 1
			},
			{
				id: 'merger',
				type: 'process',
				name: 'Merger',
				icon: '🔀',
				description: 'Combines multiple streams',
				color: '#c60',
				shape: 'hexagon',
				inputs: 3,
				outputs: 1
			}
		],
		agents: [
			{
				id: 'gym-agent',
				type: 'process',
				name: 'Gym Agent',
				icon: '🏋️',
				description: 'WAFT Scint Gym evaluator',
				color: '#0f3',
				shape: 'hexagon',
				inputs: 1,
				outputs: 2
			},
			{
				id: 'oracle',
				type: 'process',
				name: 'Oracle',
				icon: '🔮',
				description: 'TheOracle decision engine',
				color: '#90f',
				shape: 'circle',
				inputs: 1,
				outputs: 1
			},
			{
				id: 'scint-detector',
				type: 'process',
				name: 'Scint Detector',
				icon: '⚠️',
				description: 'Detects reality fractures',
				color: '#f03',
				shape: 'diamond',
				inputs: 1,
				outputs: 2
			}
		],
		sinks: [
			{
				id: 'display',
				type: 'output',
				name: 'Display',
				icon: '📺',
				description: 'Visualizes results',
				color: '#0f3',
				shape: 'square',
				inputs: 1,
				outputs: 0
			},
			{
				id: 'logger',
				type: 'output',
				name: 'Logger',
				icon: '📝',
				description: 'Records to file',
				color: '#3c3',
				shape: 'square',
				inputs: 1,
				outputs: 0
			},
			{
				id: 'collector',
				type: 'output',
				name: 'Collector',
				icon: '🗃️',
				description: 'Aggregates data',
				color: '#6c3',
				shape: 'circle',
				inputs: 2,
				outputs: 0
			}
		],
		effects: [
			{
				id: 'amplifier',
				type: 'effect',
				name: 'Amplifier',
				icon: '📈',
				description: 'Boosts signal strength',
				color: '#f0f',
				shape: 'diamond',
				inputs: 1,
				outputs: 1
			},
			{
				id: 'dampener',
				type: 'effect',
				name: 'Dampener',
				icon: '📉',
				description: 'Reduces noise',
				color: '#90f',
				shape: 'diamond',
				inputs: 1,
				outputs: 1
			}
		]
	};

	let selectedCategory = 'sources';
	let collapsed = false;

	function startDrag(event: DragEvent, template: ComponentTemplate) {
		if (!event.dataTransfer) return;
		event.dataTransfer.effectAllowed = 'copy';
		event.dataTransfer.setData('component-template', JSON.stringify(template));
		dispatch('dragstart', { template });
	}
</script>

<div class="palette" class:collapsed>
	<div class="palette-header" on:click={() => collapsed = !collapsed}>
		<span class="palette-title">🧰 COMPONENT LIBRARY</span>
		<button class="collapse-btn">{collapsed ? '◀' : '▶'}</button>
	</div>

	{#if !collapsed}
		<div class="palette-body">
			<!-- Category tabs -->
			<div class="category-tabs">
				{#each Object.keys(componentLibrary) as category}
					<button
						class="category-tab"
						class:active={selectedCategory === category}
						on:click={() => selectedCategory = category}
					>
						{category.toUpperCase()}
					</button>
				{/each}
			</div>

			<!-- Component grid -->
			<div class="components-grid">
				{#each componentLibrary[selectedCategory] as component}
					<div
						class="component-tile"
						draggable="true"
						on:dragstart={(e) => startDrag(e, component)}
						style="--comp-color: {component.color}"
					>
						<div class="component-icon">{component.icon}</div>
						<div class="component-name">{component.name}</div>
						<div class="component-ports">
							<span class="port-count">⬅ {component.inputs}</span>
							<span class="port-count">{component.outputs} ➡</span>
						</div>
					</div>
				{/each}
			</div>

			<!-- Instructions -->
			<div class="palette-footer">
				<div class="instruction">💡 Drag to canvas to add</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.palette {
		position: absolute;
		top: 80px;
		right: 20px;
		width: 280px;
		background: rgba(20, 20, 30, 0.95);
		border: 2px solid #0f3;
		border-radius: 8px;
		backdrop-filter: blur(10px);
		box-shadow: 0 0 30px rgba(0, 255, 51, 0.3);
		transition: all 0.3s;
		z-index: 100;
	}

	.palette.collapsed {
		width: 200px;
	}

	.palette.collapsed .palette-body {
		display: none;
	}

	.palette-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 12px 16px;
		background: rgba(0, 255, 51, 0.1);
		border-bottom: 1px solid #0f3;
		cursor: pointer;
		user-select: none;
	}

	.palette-header:hover {
		background: rgba(0, 255, 51, 0.15);
	}

	.palette-title {
		font-size: 0.9rem;
		font-weight: 600;
		color: #0f3;
		font-family: 'Courier New', monospace;
		letter-spacing: 1px;
	}

	.collapse-btn {
		background: none;
		border: 1px solid #0f3;
		color: #0f3;
		padding: 4px 8px;
		border-radius: 4px;
		cursor: pointer;
		font-size: 0.8rem;
		transition: all 0.2s;
	}

	.collapse-btn:hover {
		background: rgba(0, 255, 51, 0.2);
	}

	.palette-body {
		padding: 12px;
	}

	.category-tabs {
		display: flex;
		gap: 4px;
		margin-bottom: 12px;
		flex-wrap: wrap;
	}

	.category-tab {
		padding: 6px 10px;
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid #333;
		border-radius: 4px;
		color: #999;
		font-size: 0.7rem;
		font-family: 'Courier New', monospace;
		cursor: pointer;
		transition: all 0.2s;
	}

	.category-tab:hover {
		background: rgba(255, 255, 255, 0.1);
		border-color: #0f3;
	}

	.category-tab.active {
		background: rgba(0, 255, 51, 0.2);
		border-color: #0f3;
		color: #0f3;
	}

	.components-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 8px;
		max-height: 400px;
		overflow-y: auto;
		padding: 4px;
	}

	.components-grid::-webkit-scrollbar {
		width: 6px;
	}

	.components-grid::-webkit-scrollbar-track {
		background: rgba(0, 0, 0, 0.2);
		border-radius: 3px;
	}

	.components-grid::-webkit-scrollbar-thumb {
		background: #0f3;
		border-radius: 3px;
	}

	.component-tile {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 6px;
		padding: 12px 8px;
		background: rgba(0, 0, 0, 0.3);
		border: 2px solid var(--comp-color);
		border-radius: 8px;
		cursor: grab;
		transition: all 0.2s;
		position: relative;
	}

	.component-tile:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 12px var(--comp-color);
		border-width: 3px;
	}

	.component-tile:active {
		cursor: grabbing;
	}

	.component-icon {
		font-size: 1.5rem;
	}

	.component-name {
		font-size: 0.75rem;
		font-weight: 600;
		color: #e0e0e0;
		text-align: center;
		font-family: 'Courier New', monospace;
	}

	.component-ports {
		display: flex;
		justify-content: space-between;
		width: 100%;
		font-size: 0.65rem;
		color: #666;
		font-family: 'Courier New', monospace;
	}

	.port-count {
		display: flex;
		align-items: center;
		gap: 2px;
	}

	.palette-footer {
		margin-top: 12px;
		padding-top: 12px;
		border-top: 1px solid #333;
	}

	.instruction {
		font-size: 0.7rem;
		color: #999;
		text-align: center;
		font-family: 'Courier New', monospace;
	}
</style>
