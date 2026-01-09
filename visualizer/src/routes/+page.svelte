<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { projectStore } from '$lib/stores/projectStore';
	import ProjectCard from '$lib/components/cards/ProjectCard.svelte';
	import StatusCard from '$lib/components/cards/StatusCard.svelte';
	import GitCard from '$lib/components/cards/GitCard.svelte';
	import HealthCard from '$lib/components/cards/HealthCard.svelte';
	import WorkEffortsCard from '$lib/components/cards/WorkEffortsCard.svelte';
	import GamificationCard from '$lib/components/cards/GamificationCard.svelte';
	import PyriteCard from '$lib/components/cards/PyriteCard.svelte';

	let loading = true;
	let error: string | null = null;
	let refreshInterval: ReturnType<typeof setInterval> | null = null;

	onMount(async () => {
		try {
			await projectStore.fetch();
			loading = false;
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load dashboard';
			loading = false;
			console.error('Failed to fetch project state:', e);
		}

		// Auto-refresh every 30 seconds
		refreshInterval = setInterval(async () => {
			try {
				await projectStore.fetch();
			} catch (e) {
				console.error('Failed to refresh project state:', e);
			}
		}, 30000);
	});

	onDestroy(() => {
		if (refreshInterval) {
			clearInterval(refreshInterval);
		}
	});
</script>

<div class="container mx-auto px-4 py-8">
	{#if loading}
		<div class="flex items-center justify-center min-h-screen">
			<div class="text-center">
				<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[var(--primary)] mx-auto mb-4"></div>
				<p class="text-[var(--text-secondary)]">Loading dashboard...</p>
			</div>
		</div>
	{:else if error}
		<div class="flex items-center justify-center min-h-screen">
			<div class="text-center">
				<div class="text-5xl mb-4">⚠️</div>
				<h2 class="text-2xl font-bold text-[var(--error)] mb-2">Error Loading Dashboard</h2>
				<p class="text-[var(--text-secondary)] mb-4">{error}</p>
				<button 
					class="px-4 py-2 bg-[var(--primary)] text-white rounded-lg hover:bg-[var(--primary-dark)]"
					on:click={async () => {
						loading = true;
						error = null;
						try {
							await projectStore.fetch();
							loading = false;
						} catch (e) {
							error = e instanceof Error ? e.message : 'Failed to load dashboard';
							loading = false;
						}
					}}
				>
					Retry
				</button>
			</div>
		</div>
	{:else if $projectStore.error}
		<div class="flex items-center justify-center min-h-screen">
			<div class="text-center">
				<div class="text-5xl mb-4">⚠️</div>
				<h2 class="text-2xl font-bold text-[var(--error)] mb-2">Error Loading Dashboard</h2>
				<p class="text-[var(--text-secondary)] mb-4">{$projectStore.error}</p>
				<p class="text-sm text-[var(--text-muted)] mb-4">Make sure the backend server is running on http://localhost:8000</p>
				<button 
					class="px-4 py-2 bg-[var(--primary)] text-white rounded-lg hover:bg-[var(--primary-dark)]"
					on:click={async () => {
						loading = true;
						error = null;
						try {
							await projectStore.fetch();
							loading = false;
						} catch (e) {
							error = e instanceof Error ? e.message : 'Failed to load dashboard';
							loading = false;
						}
					}}
				>
					Retry
				</button>
			</div>
		</div>
	{:else}
		<div class="mb-8">
			<h1 class="text-4xl font-bold text-[var(--primary-light)] mb-2">🌊 Waft Visual Dashboard</h1>
			<p class="text-[var(--text-secondary)]">
				{$projectStore.state?.project?.name || 'Unknown'} v{$projectStore.state?.project?.version || 'Unknown'} • 
				Generated: {new Date($projectStore.state?.timestamp || Date.now()).toLocaleString()}
			</p>
		</div>

		<!-- Project Information -->
		<div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
			<ProjectCard />
			<StatusCard />
			<GitCard />
		</div>

		<!-- Status Overview -->
		<div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
			<HealthCard />
		</div>

		<!-- Primary Information -->
		<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
			<WorkEffortsCard />
			<GamificationCard />
		</div>

		<!-- Project Structure -->
		<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
			<PyriteCard />
		</div>
	{/if}
</div>

<style>
	.container {
		max-width: 1600px;
	}
</style>
