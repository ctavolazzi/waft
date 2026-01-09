<script lang="ts">
	export let type: 'success' | 'warning' | 'error' | 'info' = 'info';
</script>

<span class="badge badge-{type}">
	<slot />
</span>

<style>
	.badge {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		padding: 6px 14px;
		border-radius: 16px;
		font-size: 0.85em;
		font-weight: 600;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
	}

	.badge-success {
		background: linear-gradient(135deg, rgba(74, 222, 128, 0.2), rgba(74, 222, 128, 0.1));
		color: var(--success);
		border: 1px solid rgba(74, 222, 128, 0.3);
	}

	.badge-warning {
		background: linear-gradient(135deg, rgba(251, 191, 36, 0.2), rgba(251, 191, 36, 0.1));
		color: var(--warning);
		border: 1px solid rgba(251, 191, 36, 0.3);
	}

	.badge-error {
		background: linear-gradient(135deg, rgba(248, 113, 113, 0.2), rgba(248, 113, 113, 0.1));
		color: var(--error);
		border: 1px solid rgba(248, 113, 113, 0.3);
	}

	.badge-info {
		background: linear-gradient(135deg, rgba(96, 165, 250, 0.2), rgba(96, 165, 250, 0.1));
		color: var(--info);
		border: 1px solid rgba(96, 165, 250, 0.3);
	}
</style>
