<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let label: string = 'SWITCH';
	export let on: boolean = false;
	export let color: string = '#0f3';

	const dispatch = createEventDispatcher();

	function toggle() {
		on = !on;
		dispatch('toggle', { on });
	}
</script>

<div class="switch-control">
	<div class="switch-label">{label}</div>
	<div class="switch" class:on on:click={toggle}>
		<div class="switch-toggle" style="--color: {color}"></div>
		<div class="switch-indicator" class:active={on} style="--color: {color}"></div>
	</div>
</div>

<style>
	.switch-control {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 6px;
	}

	.switch-label {
		font-size: 0.7rem;
		color: #999;
		font-family: 'Courier New', monospace;
		text-transform: uppercase;
		letter-spacing: 1px;
	}

	.switch {
		width: 50px;
		height: 26px;
		background: #1a1a1a;
		border: 2px solid #333;
		border-radius: 13px;
		position: relative;
		cursor: pointer;
		transition: all 0.3s;
	}

	.switch:hover {
		border-color: var(--color, #0f3);
	}

	.switch.on {
		background: rgba(0, 255, 51, 0.2);
		border-color: var(--color, #0f3);
		box-shadow: 0 0 10px rgba(0, 255, 51, 0.3);
	}

	.switch-toggle {
		position: absolute;
		top: 2px;
		left: 2px;
		width: 18px;
		height: 18px;
		background: #555;
		border-radius: 50%;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	}

	.switch.on .switch-toggle {
		left: calc(100% - 22px);
		background: var(--color, #0f3);
		box-shadow: 0 0 10px var(--color, #0f3);
	}

	.switch-indicator {
		position: absolute;
		top: 50%;
		right: 6px;
		transform: translateY(-50%);
		width: 4px;
		height: 4px;
		background: #333;
		border-radius: 50%;
		transition: all 0.3s;
	}

	.switch-indicator.active {
		background: var(--color, #0f3);
		box-shadow: 0 0 8px var(--color, #0f3);
		animation: pulse-indicator 2s infinite;
	}

	@keyframes pulse-indicator {
		0%, 100% {
			opacity: 1;
		}
		50% {
			opacity: 0.3;
		}
	}
</style>
