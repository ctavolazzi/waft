<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let connections: Array<{id: string, fromNode: string, fromPort: string, toNode: string, toPort: string, x1: number, y1: number, x2: number, y2: number, active: boolean}> = [];
	export let width: number = 0;
	export let height: number = 0;

	const dispatch = createEventDispatcher();

	interface DragState {
		active: boolean;
		startX: number;
		startY: number;
		currentX: number;
		currentY: number;
		fromNode: string | null;
		fromPort: string | null;
	}

	let dragState: DragState = {
		active: false,
		startX: 0,
		startY: 0,
		currentX: 0,
		currentY: 0,
		fromNode: null,
		fromPort: null
	};

	export function startWiring(fromNode: string, fromPort: string, x: number, y: number) {
		dragState = {
			active: true,
			startX: x,
			startY: y,
			currentX: x,
			currentY: y,
			fromNode,
			fromPort
		};
	}

	export function updateWiring(x: number, y: number) {
		if (dragState.active) {
			dragState.currentX = x;
			dragState.currentY = y;
		}
	}

	export function endWiring(toNode: string | null, toPort: string | null) {
		if (dragState.active && dragState.fromNode && dragState.fromPort) {
			if (toNode && toPort) {
				// Valid connection
				dispatch('connect', {
					fromNode: dragState.fromNode,
					fromPort: dragState.fromPort,
					toNode,
					toPort
				});
			}
		}

		dragState = {
			active: false,
			startX: 0,
			startY: 0,
			currentX: 0,
			currentY: 0,
			fromNode: null,
			fromPort: null
		};
	}

	export function cancelWiring() {
		dragState = {
			active: false,
			startX: 0,
			startY: 0,
			currentX: 0,
			currentY: 0,
			fromNode: null,
			fromPort: null
		};
	}

	function deleteConnection(connectionId: string) {
		dispatch('delete', { connectionId });
	}
</script>

<svg class="wiring-layer" {width} {height} style="pointer-events: none;">
	<!-- Existing connections -->
	{#each connections as conn}
		<g class="connection" class:active={conn.active}>
			<!-- Glow effect for active connections -->
			{#if conn.active}
				<path
					d="M {conn.x1} {conn.y1} C {conn.x1 + 100} {conn.y1}, {conn.x2 - 100} {conn.y2}, {conn.x2} {conn.y2}"
					fill="none"
					stroke={conn.active ? '#0f3' : '#555'}
					stroke-width="8"
					opacity="0.3"
					filter="blur(4px)"
				/>
			{/if}

			<!-- Main wire -->
			<path
				d="M {conn.x1} {conn.y1} C {conn.x1 + 100} {conn.y1}, {conn.x2 - 100} {conn.y2}, {conn.x2} {conn.y2}"
				fill="none"
				stroke={conn.active ? '#0f3' : '#555'}
				stroke-width="3"
				opacity={conn.active ? 1 : 0.5}
				stroke-dasharray={conn.active ? "10,5" : "none"}
				class="wire"
				style="pointer-events: stroke; cursor: pointer;"
				on:click={() => deleteConnection(conn.id)}
			>
				{#if conn.active}
					<animate
						attributeName="stroke-dashoffset"
						from="0"
						to="15"
						dur="0.5s"
						repeatCount="indefinite"
					/>
				{/if}
			</path>

			<!-- Connection endpoints -->
			<circle
				cx={conn.x1}
				cy={conn.y1}
				r="5"
				fill={conn.active ? '#0f3' : '#555'}
				opacity={conn.active ? 1 : 0.5}
			/>
			<circle
				cx={conn.x2}
				cy={conn.y2}
				r="5"
				fill={conn.active ? '#0f3' : '#555'}
				opacity={conn.active ? 1 : 0.5}
			/>

			<!-- Flowing particles -->
			{#if conn.active}
				{#each [0, 0.25, 0.5, 0.75] as offset}
					<circle r="4" fill="#0f3" opacity="0.8">
						<animateMotion
							path="M {conn.x1} {conn.y1} C {conn.x1 + 100} {conn.y1}, {conn.x2 - 100} {conn.y2}, {conn.x2} {conn.y2}"
							dur="2s"
							repeatCount="indefinite"
							begin="{offset * 2}s"
						/>
					</circle>
				{/each}
			{/if}
		</g>
	{/each}

	<!-- Active wiring (being dragged) -->
	{#if dragState.active}
		<g class="active-wiring">
			<!-- Glow -->
			<path
				d="M {dragState.startX} {dragState.startY} C {dragState.startX + 100} {dragState.startY}, {dragState.currentX - 100} {dragState.currentY}, {dragState.currentX} {dragState.currentY}"
				fill="none"
				stroke="#09f"
				stroke-width="8"
				opacity="0.3"
				filter="blur(4px)"
			/>

			<!-- Main line -->
			<path
				d="M {dragState.startX} {dragState.startY} C {dragState.startX + 100} {dragState.startY}, {dragState.currentX - 100} {dragState.currentY}, {dragState.currentX} {dragState.currentY}"
				fill="none"
				stroke="#09f"
				stroke-width="3"
				stroke-dasharray="5,5"
			>
				<animate
					attributeName="stroke-dashoffset"
					from="0"
					to="10"
					dur="0.3s"
					repeatCount="indefinite"
				/>
			</path>

			<!-- Start point -->
			<circle
				cx={dragState.startX}
				cy={dragState.startY}
				r="6"
				fill="#09f"
			>
				<animate
					attributeName="r"
					values="6;8;6"
					dur="1s"
					repeatCount="indefinite"
				/>
			</circle>

			<!-- End point (following cursor) -->
			<circle
				cx={dragState.currentX}
				cy={dragState.currentY}
				r="5"
				fill="#09f"
				opacity="0.7"
			/>
		</g>
	{/if}
</svg>

<style>
	.wiring-layer {
		position: absolute;
		top: 0;
		left: 0;
		z-index: 2;
	}

	.connection .wire {
		transition: all 0.3s;
	}

	.connection:hover .wire {
		stroke-width: 5;
		filter: drop-shadow(0 0 8px currentColor);
	}
</style>
