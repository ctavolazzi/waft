<script lang="ts">
	export let label: string = 'STATUS';
	export let on: boolean = false;
	export let color: string = '#0f3';
	export let blinking: boolean = false;
</script>

<div class="light-control">
	<div class="light-label">{label}</div>
	<div class="light" class:on class:blinking style="--color: {color}">
		<div class="light-glow"></div>
		<div class="light-core"></div>
	</div>
</div>

<style>
	.light-control {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 6px;
	}

	.light-label {
		font-size: 0.7rem;
		color: #999;
		font-family: 'Courier New', monospace;
		text-transform: uppercase;
		letter-spacing: 1px;
	}

	.light {
		width: 24px;
		height: 24px;
		border-radius: 50%;
		background: #1a1a1a;
		border: 2px solid #333;
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.light-glow {
		position: absolute;
		width: 100%;
		height: 100%;
		border-radius: 50%;
		background: radial-gradient(circle, transparent 30%, #1a1a1a 70%);
		opacity: 0;
		transition: opacity 0.3s;
	}

	.light-core {
		width: 12px;
		height: 12px;
		border-radius: 50%;
		background: #333;
		transition: all 0.3s;
	}

	.light.on {
		border-color: var(--color, #0f3);
		background: radial-gradient(circle, var(--color, #0f3), #1a1a1a);
	}

	.light.on .light-glow {
		opacity: 1;
		box-shadow: 0 0 20px var(--color, #0f3), inset 0 0 10px var(--color, #0f3);
	}

	.light.on .light-core {
		background: var(--color, #0f3);
		box-shadow:
			0 0 8px var(--color, #0f3),
			0 0 12px var(--color, #0f3),
			0 0 16px var(--color, #0f3),
			inset 0 0 4px #fff;
	}

	.light.blinking .light-core {
		animation: blink-light 1s infinite;
	}

	@keyframes blink-light {
		0%, 100% {
			opacity: 1;
		}
		50% {
			opacity: 0.2;
		}
	}
</style>
