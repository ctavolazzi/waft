<script lang="ts">
	export let value: number = 0;
</script>

<div class="progress-bar">
	<div class="progress-fill" style="width: {value}%"></div>
</div>

<style>
	.progress-bar {
		width: 100%;
		height: 24px;
		background: rgba(26, 30, 41, 0.8);
		border-radius: 12px;
		overflow: hidden;
		margin: 12px 0;
		box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
		border: 1px solid var(--border);
	}

	.progress-fill {
		height: 100%;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
		position: relative;
		overflow: hidden;
	}

	.progress-fill::after {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
		animation: shimmer 2s infinite;
	}

	@keyframes shimmer {
		0% {
			background-position: -1000px 0;
		}
		100% {
			background-position: 1000px 0;
		}
	}
</style>
