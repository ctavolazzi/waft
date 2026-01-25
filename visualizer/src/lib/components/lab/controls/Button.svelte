<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let label: string = 'PUSH';
	export let color: string = '#f00';
	export let size: 'small' | 'medium' | 'large' = 'medium';
	export let pressed: boolean = false;

	const dispatch = createEventDispatcher();

	function handleMouseDown() {
		pressed = true;
		dispatch('press');
	}

	function handleMouseUp() {
		pressed = false;
		dispatch('release');
	}
</script>

<div class="button-control">
	<div class="button-label">{label}</div>
	<button
		class="button"
		class:pressed
		class:small={size === 'small'}
		class:medium={size === 'medium'}
		class:large={size === 'large'}
		style="--color: {color}"
		on:mousedown={handleMouseDown}
		on:mouseup={handleMouseUp}
		on:mouseleave={handleMouseUp}
	>
		<div class="button-surface"></div>
		<div class="button-shine"></div>
	</button>
</div>

<style>
	.button-control {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 6px;
	}

	.button-label {
		font-size: 0.7rem;
		color: #999;
		font-family: 'Courier New', monospace;
		text-transform: uppercase;
		letter-spacing: 1px;
	}

	.button {
		background: #1a1a1a;
		border: none;
		border-radius: 50%;
		cursor: pointer;
		position: relative;
		transition: all 0.1s;
		box-shadow:
			0 4px 8px rgba(0, 0, 0, 0.6),
			inset 0 -2px 4px rgba(0, 0, 0, 0.5);
	}

	.button.small {
		width: 32px;
		height: 32px;
	}

	.button.medium {
		width: 48px;
		height: 48px;
	}

	.button.large {
		width: 64px;
		height: 64px;
	}

	.button:hover {
		transform: translateY(-2px);
		box-shadow:
			0 6px 12px rgba(0, 0, 0, 0.8),
			inset 0 -2px 4px rgba(0, 0, 0, 0.5),
			0 0 20px var(--color);
	}

	.button.pressed {
		transform: translateY(2px);
		box-shadow:
			0 2px 4px rgba(0, 0, 0, 0.4),
			inset 0 2px 8px rgba(0, 0, 0, 0.7);
	}

	.button-surface {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		border-radius: 50%;
		background: radial-gradient(
			circle at 30% 30%,
			var(--color),
			color-mix(in srgb, var(--color) 50%, black)
		);
		box-shadow: inset 0 2px 4px rgba(255, 255, 255, 0.3);
		transition: all 0.1s;
	}

	.button:hover .button-surface {
		box-shadow:
			inset 0 2px 4px rgba(255, 255, 255, 0.4),
			0 0 20px var(--color);
	}

	.button.pressed .button-surface {
		box-shadow: inset 0 -2px 8px rgba(0, 0, 0, 0.5);
	}

	.button-shine {
		position: absolute;
		top: 10%;
		left: 10%;
		width: 30%;
		height: 30%;
		border-radius: 50%;
		background: radial-gradient(
			circle at center,
			rgba(255, 255, 255, 0.6),
			transparent
		);
		pointer-events: none;
	}
</style>
