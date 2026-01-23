<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let id: string;
	export let type: string;
	export let title: string;
	export let x: number = 0;
	export let y: number = 0;
	export let inputs: Array<{id: string, label: string}> = [];
	export let outputs: Array<{id: string, label: string}> = [];
	export let active: boolean = false;

	const dispatch = createEventDispatcher();

	let dragging = false;
	let dragOffset = { x: 0, y: 0 };

	function startDrag(e: MouseEvent) {
		dragging = true;
		dragOffset = {
			x: e.clientX - x,
			y: e.clientY - y
		};
		dispatch('dragstart', { id });
	}

	function drag(e: MouseEvent) {
		if (!dragging) return;
		dispatch('drag', {
			id,
			x: e.clientX - dragOffset.x,
			y: e.clientY - dragOffset.y
		});
	}

	function endDrag() {
		if (dragging) {
			dragging = false;
			dispatch('dragend', { id });
		}
	}

	function handlePortClick(portId: string, isOutput: boolean) {
		dispatch('portclick', { nodeId: id, portId, isOutput });
	}
</script>

<svelte:window on:mousemove={drag} on:mouseup={endDrag} />

<div
	class="node"
	class:dragging
	class:active
	class:type-input={type === 'input'}
	class:type-process={type === 'process'}
	class:type-output={type === 'output'}
	style="left: {x}px; top: {y}px;"
>
	<div class="node-header" on:mousedown={startDrag}>
		<div class="node-type-indicator"></div>
		<div class="node-title">{title}</div>
		{#if active}
			<div class="node-activity-light"></div>
		{/if}
	</div>

	<div class="node-body">
		<div class="ports-container">
			{#if inputs.length > 0}
				<div class="ports inputs">
					{#each inputs as input}
						<div
							class="port input-port"
							on:click={() => handlePortClick(input.id, false)}
						>
							<div class="port-socket"></div>
							<span class="port-label">{input.label}</span>
						</div>
					{/each}
				</div>
			{/if}

			<div class="node-content">
				<slot />
			</div>

			{#if outputs.length > 0}
				<div class="ports outputs">
					{#each outputs as output}
						<div
							class="port output-port"
							on:click={() => handlePortClick(output.id, true)}
						>
							<span class="port-label">{output.label}</span>
							<div class="port-socket"></div>
						</div>
					{/each}
				</div>
			{/if}
		</div>
	</div>
</div>

<style>
	.node {
		position: absolute;
		min-width: 180px;
		background: rgba(20, 20, 30, 0.95);
		border: 2px solid #333;
		border-radius: 8px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
		transition: box-shadow 0.2s;
		backdrop-filter: blur(10px);
		user-select: none;
	}

	.node:hover {
		box-shadow: 0 4px 20px rgba(0, 255, 51, 0.2);
	}

	.node.dragging {
		opacity: 0.8;
		cursor: grabbing;
		z-index: 1000;
	}

	.node.active {
		border-color: #0f3;
		box-shadow: 0 0 20px rgba(0, 255, 51, 0.4);
	}

	.node-header {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 8px 12px;
		background: rgba(0, 0, 0, 0.3);
		border-bottom: 1px solid #333;
		cursor: grab;
		border-radius: 6px 6px 0 0;
	}

	.node-type-indicator {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background: #666;
	}

	.type-input .node-type-indicator {
		background: #0af;
		box-shadow: 0 0 8px #0af;
	}

	.type-process .node-type-indicator {
		background: #f90;
		box-shadow: 0 0 8px #f90;
	}

	.type-output .node-type-indicator {
		background: #0f3;
		box-shadow: 0 0 8px #0f3;
	}

	.node-title {
		flex: 1;
		font-size: 0.85rem;
		font-weight: 600;
		color: #e0e0e0;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
	}

	.node-activity-light {
		width: 6px;
		height: 6px;
		border-radius: 50%;
		background: #0f3;
		animation: pulse-light 1s infinite;
	}

	@keyframes pulse-light {
		0%, 100% {
			box-shadow: 0 0 4px #0f3;
			opacity: 1;
		}
		50% {
			box-shadow: 0 0 12px #0f3;
			opacity: 0.6;
		}
	}

	.node-body {
		padding: 12px;
	}

	.ports-container {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.ports {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}

	.port {
		display: flex;
		align-items: center;
		gap: 6px;
		font-size: 0.75rem;
		color: #999;
		cursor: pointer;
		transition: color 0.2s;
	}

	.port:hover {
		color: #0f3;
	}

	.port:hover .port-socket {
		border-color: #0f3;
		box-shadow: 0 0 8px rgba(0, 255, 51, 0.5);
	}

	.input-port {
		justify-content: flex-start;
	}

	.output-port {
		justify-content: flex-end;
	}

	.port-socket {
		width: 12px;
		height: 12px;
		border: 2px solid #555;
		border-radius: 50%;
		background: #222;
		transition: all 0.2s;
		position: relative;
	}

	.port-socket::before {
		content: '';
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: 4px;
		height: 4px;
		background: #555;
		border-radius: 50%;
		transition: background 0.2s;
	}

	.port:hover .port-socket::before {
		background: #0f3;
	}

	.port-label {
		font-family: 'Courier New', monospace;
	}

	.node-content {
		padding: 8px 0;
		color: #ccc;
		font-size: 0.8rem;
	}
</style>
