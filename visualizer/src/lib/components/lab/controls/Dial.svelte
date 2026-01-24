<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let label: string = 'DIAL';
	export let value: number = 50; // 0-100
	export let color: string = '#0f3';
	export let min: number = 0;
	export let max: number = 100;

	const dispatch = createEventDispatcher();

	let dragging = false;
	let startY = 0;
	let startValue = 0;

	function startDrag(e: MouseEvent) {
		dragging = true;
		startY = e.clientY;
		startValue = value;
		e.preventDefault();
	}

	function drag(e: MouseEvent) {
		if (!dragging) return;
		const delta = (startY - e.clientY) * 0.5;
		value = Math.max(min, Math.min(max, startValue + delta));
		dispatch('change', { value });
	}

	function endDrag() {
		dragging = false;
	}

	$: rotation = ((value - min) / (max - min)) * 270 - 135;
</script>

<svelte:window on:mousemove={drag} on:mouseup={endDrag} />

<div class="dial-control">
	<div class="dial-label">{label}</div>
	<div class="dial" on:mousedown={startDrag} class:dragging>
		<svg width="60" height="60" viewBox="0 0 60 60">
			<!-- Background arc -->
			<path
				d="M 10 30 A 20 20 0 1 1 50 30"
				fill="none"
				stroke="#1a1a1a"
				stroke-width="6"
				stroke-linecap="round"
			/>
			<!-- Value arc -->
			<path
				d="M 10 30 A 20 20 0 1 1 50 30"
				fill="none"
				stroke={color}
				stroke-width="4"
				stroke-linecap="round"
				stroke-dasharray="94.2"
				stroke-dashoffset={94.2 - (value / max) * 94.2}
				style="filter: drop-shadow(0 0 4px {color});"
			/>
			<!-- Center knob -->
			<circle cx="30" cy="30" r="16" fill="#222" stroke="#333" stroke-width="2" />
			<!-- Indicator line -->
			<line
				x1="30"
				y1="30"
				x2="30"
				y2="18"
				stroke={color}
				stroke-width="2"
				stroke-linecap="round"
				transform="rotate({rotation} 30 30)"
				style="filter: drop-shadow(0 0 3px {color});"
			/>
			<!-- Center dot -->
			<circle cx="30" cy="30" r="3" fill={color} opacity="0.8" />
		</svg>
	</div>
	<div class="dial-value" style="color: {color}">{Math.round(value)}</div>
</div>

<style>
	.dial-control {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 4px;
	}

	.dial-label {
		font-size: 0.7rem;
		color: #999;
		font-family: 'Courier New', monospace;
		text-transform: uppercase;
		letter-spacing: 1px;
	}

	.dial {
		cursor: ns-resize;
		user-select: none;
		transition: transform 0.1s;
	}

	.dial:hover {
		transform: scale(1.05);
	}

	.dial.dragging {
		cursor: grabbing;
		transform: scale(1.1);
	}

	.dial-value {
		font-size: 0.9rem;
		font-family: 'Courier New', monospace;
		font-weight: bold;
		text-shadow: 0 0 8px currentColor;
	}
</style>
