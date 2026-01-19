<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import AppShell from '$lib/components/layout/AppShell.svelte';
	import RunsList from '$lib/components/evolve-ui/RunsList.svelte';
	import RunDetails from '$lib/components/evolve-ui/RunDetails.svelte';
	import { evolveUiStore } from '$lib/stores/evolveUiStore';

	let refreshInterval: ReturnType<typeof setInterval> | null = null;

	onMount(async () => {
		await evolveUiStore.fetch();
		
		// Auto-refresh every 30 seconds
		refreshInterval = setInterval(async () => {
			await evolveUiStore.fetch();
		}, 30000);
	});

	onDestroy(() => {
		if (refreshInterval) {
			clearInterval(refreshInterval);
		}
	});
</script>

<AppShell>
	<div class="container mx-auto px-4 py-8">
		<div class="mb-8">
			<h1 class="text-4xl font-bold text-white mb-2">🎨 Evolve UI Monitor</h1>
			<p class="text-gray-300">Track and monitor all /evolve-a-ui command executions</p>
		</div>

		<div class="monitor-layout">
			<div class="runs-panel">
				<RunsList />
			</div>
			<div class="details-panel">
				<RunDetails />
			</div>
		</div>
	</div>
</AppShell>

<style>
	.container {
		max-width: 1400px;
	}

	.monitor-layout {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 20px;
		height: calc(100vh - 200px);
		min-height: 600px;
	}

	.runs-panel,
	.details-panel {
		background-color: var(--bg-card);
		border: 2px solid var(--border);
		border-radius: 8px;
		padding: 20px;
		overflow-y: auto;
	}

	@media (max-width: 768px) {
		.monitor-layout {
			grid-template-columns: 1fr;
			height: auto;
		}
		
		.runs-panel,
		.details-panel {
			min-height: 400px;
		}
	}
</style>