<script lang="ts">
	import { projectStore } from '$lib/stores/projectStore';

	function refresh() {
		projectStore.fetch();
	}
</script>

<nav class="bg-[var(--bg-card)] border-b border-[var(--border)] px-6 py-4">
	<div class="container mx-auto flex items-center justify-between">
		<a href="/" class="text-2xl font-bold text-[var(--primary-light)]">🌊 Waft</a>
		<div class="flex items-center gap-2">
			<a href="/" class="nav-box">Dashboard</a>
			<a href="/cognitive-tools" class="nav-box">🧠 Cognitive Tools</a>
			<a href="/evolve-ui-monitor" class="nav-box">🎨 Evolve UI</a>
			<a href="/git" class="nav-box">Git</a>
			<a href="/work-efforts" class="nav-box">Work Efforts</a>
			<a href="/empirica" class="nav-box">Empirica</a>
			<a href="/campfire" class="nav-box">🔥 Campfire</a>
			<button
				on:click={refresh}
				class="nav-box nav-button"
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

	.nav-box {
		display: inline-block;
		padding: 0.5rem 1rem;
		border: 1px solid var(--border);
		background-color: var(--bg-card);
		border-radius: 6px;
		color: var(--text-primary);
		text-decoration: none;
		font-size: 0.9rem;
		transition: all 0.2s ease;
	}

	.nav-box:hover {
		background-color: var(--bg-card-hover);
		border-color: var(--primary);
		color: var(--primary-light);
	}

	.nav-button {
		background-color: var(--primary);
		color: var(--bg-dark);
		border-color: var(--primary);
		font-weight: 600;
		cursor: pointer;
	}

	.nav-button:hover {
		background-color: var(--primary-dark);
		border-color: var(--primary-dark);
		color: var(--bg-dark);
	}
</style>
