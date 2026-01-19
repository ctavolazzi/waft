<script lang="ts">
	export let label: string = '';
	export let variant: 'primary' | 'secondary' = 'primary';
	export let minHeight: string = 'auto';
</script>

<div
	class="wireframe-box"
	class:primary={variant === 'primary'}
	class:secondary={variant === 'secondary'}
	style="min-height: {minHeight}"
	aria-label={label || undefined}
>
	{#if label}
		<div class="wireframe-label">{label}</div>
	{/if}
	<slot />
</div>

<style>
	.wireframe-box {
		border: 2px solid var(--border);
		background-color: var(--bg-card);
		padding: 20px;
		margin-bottom: 20px;
		border-radius: 6px;
	}

	.wireframe-box.secondary {
		border: 2px solid var(--border);
		border-width: 2px;
		padding: 15px;
	}

	.wireframe-label {
		font-size: 0.875rem;
		font-weight: 600;
		color: var(--text-secondary);
		margin-bottom: 10px;
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}
</style>