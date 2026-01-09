<script lang="ts">
	import { projectStore } from '$lib/stores/projectStore';

	function refresh() {
		projectStore.fetch();
	}
</script>

<nav class="bg-[var(--bg-card)] border-b border-[var(--border)] px-6 py-4">
	<div class="container mx-auto flex items-center justify-between">
		<a href="/" class="text-2xl font-bold text-[var(--primary-light)]">🌊 Waft</a>
		<div class="flex items-center gap-4">
			<a href="/" class="text-[var(--text-primary)] hover:text-[var(--primary-light)] transition-colors">Dashboard</a>
			<a href="/git" class="text-[var(--text-primary)] hover:text-[var(--primary-light)] transition-colors">Git</a>
			<a href="/work-efforts" class="text-[var(--text-primary)] hover:text-[var(--primary-light)] transition-colors">Work Efforts</a>
			<a href="/empirica" class="text-[var(--text-primary)] hover:text-[var(--primary-light)] transition-colors">Empirica</a>
			<button
				on:click={refresh}
				class="px-4 py-2 bg-[var(--primary)] text-[var(--bg-dark)] rounded-lg font-semibold hover:bg-[var(--primary-dark)] transition-colors"
			>
				🔄 Refresh
			</button>
		</div>
	</div>
</nav>

<style>
	.container {
		max-width: 1600px;
	}
</style>
