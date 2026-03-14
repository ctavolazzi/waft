<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { projectStore } from '$lib/stores/projectStore';
	import { dashboard5050Store } from '$lib/stores/dashboard5050Store';
	import ProjectCard from '$lib/components/cards/ProjectCard.svelte';
	import StatusCard from '$lib/components/cards/StatusCard.svelte';
	import GitCard from '$lib/components/cards/GitCard.svelte';
	import HealthCard from '$lib/components/cards/HealthCard.svelte';
	import WorkEffortsCard from '$lib/components/cards/WorkEffortsCard.svelte';
	import GamificationCard from '$lib/components/cards/GamificationCard.svelte';
	import PyriteCard from '$lib/components/cards/PyriteCard.svelte';
	import GymCard from '$lib/components/cards/GymCard.svelte';
	import BobCard from '$lib/components/cards/BobCard.svelte';

	let loading = true;
	let error: string | null = null;
	let refreshInterval: ReturnType<typeof setInterval> | null = null;
	const workspaceLinks = [
		{
			href: '/projects',
			icon: '📁',
			title: 'Projects',
			description: 'Track long-lived initiatives, milestones, and current progress.'
		},
		{
			href: '/evolve-ui-monitor',
			icon: '🎨',
			title: 'Evolve UI',
			description: 'Review interface evolution runs, artifacts, and iteration details.'
		},
		{
			href: '/lab',
			icon: '🧪',
			title: 'Flow Lab',
			description: 'Experiment with systems, builders, and visual flow-oriented surfaces.'
		},
		{
			href: '/cognitive-tools',
			icon: '🧠',
			title: 'Cognitive Tools',
			description: 'Open metacognitive tools and higher-level orchestration utilities.'
		},
		{
			href: '/campfire',
			icon: '🔥',
			title: 'Campfire',
			description: 'Browse narrative and story surfaces from the current WAFT state.'
		},
		{
			href: '/odd-notes',
			icon: '🗂️',
			title: 'ODD Notes',
			description: 'Access note-oriented surfaces and connected knowledge artifacts.'
		},
		{
			href: '/mission-control',
			icon: '🚀',
			title: 'Mission Control',
			description: 'See the higher-level command surface for guided workflows.'
		},
		{
			href: '/arena',
			icon: '⚔️',
			title: 'Arena',
			description: 'Jump into the battle and simulation-oriented view of WAFT.'
		},
		{
			href: '/stats',
			icon: '📊',
			title: 'Stats',
			description: 'Inspect quantitative project and system telemetry at a glance.'
		}
	];

	async function refreshAll() {
		try {
			await Promise.all([projectStore.fetch(), dashboard5050Store.fetch()]);
			error = null;
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load control center';
		} finally {
			loading = false;
		}
	}

	function handleRefresh() {
		loading = true;
		void refreshAll();
	}

	function formatRelativeTime(iso: string) {
		const delta = Date.now() - new Date(iso).getTime();
		const minutes = Math.max(1, Math.round(delta / 60000));
		if (minutes < 60) return `${minutes}m ago`;
		const hours = Math.round(minutes / 60);
		if (hours < 24) return `${hours}h ago`;
		const days = Math.round(hours / 24);
		return `${days}d ago`;
	}

	function formatArtifactSize(bytes: number) {
		if (bytes < 1024) return `${bytes} B`;
		if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
		return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
	}

	onMount(() => {
		void refreshAll();
		const onRefresh = () => {
			void refreshAll();
		};
		window.addEventListener('waft-refresh', onRefresh);

		// Auto-refresh every 30 seconds
		refreshInterval = setInterval(async () => {
			await refreshAll();
		}, 30000);

		return () => {
			window.removeEventListener('waft-refresh', onRefresh);
		};
	});

	onDestroy(() => {
		if (refreshInterval) {
			clearInterval(refreshInterval);
		}
	});

	$: state = $projectStore.state;
	$: session = $dashboard5050Store.session;
	$: timeline = $dashboard5050Store.timeline.slice(0, 8);
	$: latestUiPath = session?.canonical_ui_work_effort || session?.latest_work_effort_5050;
	$: topLine =
		state?.project?.name && state?.project?.version
			? `${state.project.name} v${state.project.version}`
			: 'Unified browser interface for WAFT';
</script>

<div class="container mx-auto px-4 py-8">
	{#if loading}
		<div class="flex items-center justify-center min-h-screen">
			<div class="text-center">
				<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[var(--primary)] mx-auto mb-4"></div>
				<p class="text-[var(--text-secondary)]">Loading WAFT control center...</p>
			</div>
		</div>
	{:else if error}
		<div class="flex items-center justify-center min-h-screen">
			<div class="text-center">
				<div class="text-5xl mb-4">⚠️</div>
				<h2 class="text-2xl font-bold text-[var(--error)] mb-2">Error Loading Control Center</h2>
				<p class="text-[var(--text-secondary)] mb-4">{error}</p>
				<button 
					class="px-4 py-2 bg-[var(--primary)] text-white rounded-lg hover:bg-[var(--primary-dark)]"
					on:click={handleRefresh}
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
					on:click={handleRefresh}
				>
					Retry
				</button>
			</div>
		</div>
	{:else}
		<div class="mb-8">
			<div class="hero card card-glass">
				<div>
					<p class="hero-kicker">Unified WAFT interface</p>
					<h1 class="text-4xl font-bold text-[var(--primary-light)] mb-2">🏛️ WAFT Control Center</h1>
					<p class="text-[var(--text-secondary)]">
						{topLine} • Generated: {new Date(state?.timestamp || Date.now()).toLocaleString()}
					</p>
				</div>
				<div class="hero-actions">
					<button class="btn btn-primary" on:click={handleRefresh}>🔄 Refresh Everything</button>
				</div>
			</div>
		</div>

		<div class="summary-grid">
			<div class="summary-card card">
				<div class="summary-label">Uncommitted Files</div>
				<div class="summary-value">{session?.summary.uncommitted_files ?? state?.git?.uncommitted_files?.length ?? 0}</div>
				<div class="summary-meta">Current branch: {state?.git?.branch || 'unknown'}</div>
			</div>
			<div class="summary-card card">
				<div class="summary-label">Integrity</div>
				<div class="summary-value">{Math.round(session?.summary.integrity ?? state?.gamification?.integrity ?? 0)}%</div>
				<div class="summary-meta">Level {state?.gamification?.level ?? 0}</div>
			</div>
			<div class="summary-card card">
				<div class="summary-label">Tracked Work Efforts</div>
				<div class="summary-value">{session?.summary.work_efforts ?? state?.work_efforts?.length ?? 0}</div>
				<div class="summary-meta">Canonical UI record: {latestUiPath ? 'available' : 'not found'}</div>
			</div>
			<div class="summary-card card">
				<div class="summary-label">5050 Artifacts</div>
				<div class="summary-value">{session?.artifacts.length ?? timeline.length}</div>
				<div class="summary-meta">{timeline[0] ? `Latest ${formatRelativeTime(timeline[0].timestamp)}` : 'No recent artifacts'}</div>
			</div>
		</div>

		<div class="control-grid">
			<section class="card card-glow">
				<div class="section-heading">
					<h2>🧭 Unified Workspaces</h2>
					<p>One place to jump between the WAFT surfaces that actually exist today.</p>
				</div>
				<div class="workspace-grid">
					{#each workspaceLinks as workspace}
						<a class="workspace-link" href={workspace.href}>
							<div class="workspace-title">{workspace.icon} {workspace.title}</div>
							<div class="workspace-description">{workspace.description}</div>
						</a>
					{/each}
				</div>
			</section>

			<section class="card card-glow">
				<div class="section-heading">
					<h2>🧵 Context Stack</h2>
					<p>Read-only 5050 orchestration context, now surfaced inside the main visualizer.</p>
				</div>
				<div class="context-list">
					<div class="context-item">
						<div class="context-label">Canonical UI work effort</div>
						<div class="context-value mono">{latestUiPath || 'No unified UI work effort detected yet'}</div>
					</div>
					<div class="context-item">
						<div class="context-label">Latest 5050-specific record</div>
						<div class="context-value mono">{session?.latest_work_effort_5050 || 'Historical record not present in this checkout'}</div>
					</div>
					<div class="context-item">
						<div class="context-label">Recent artifacts</div>
						<div class="context-value">{session?.artifacts.length ?? 0} surfaced through `/api/5050/session`</div>
					</div>
					<div class="context-item">
						<div class="context-label">Timeline status</div>
						<div class="context-value">
							{#if $dashboard5050Store.error}
								⚠️ {$dashboard5050Store.error}
							{:else}
								✅ Read-only orchestration feed available
							{/if}
						</div>
					</div>
				</div>
			</section>
		</div>

		<div class="control-grid">
			<section class="card card-glow">
				<div class="section-heading">
					<h2>📜 Recent 5050 Timeline</h2>
					<p>Newest orchestration artifacts and session breadcrumbs.</p>
				</div>
				{#if timeline.length}
					<ul class="artifact-list">
						{#each timeline as event}
							<li class="artifact-item">
								<div class="artifact-topline">
									<span class="artifact-type">{event.type}</span>
									<span class="artifact-age">{formatRelativeTime(event.timestamp)}</span>
								</div>
								<div class="artifact-name">{event.name}</div>
								<div class="artifact-path mono">{event.path}</div>
								<div class="artifact-meta">{formatArtifactSize(event.size_bytes)}</div>
							</li>
						{/each}
					</ul>
				{:else}
					<div class="empty-state">No timeline events found yet.</div>
				{/if}
			</section>

			<section class="card card-glow">
				<div class="section-heading">
					<h2>📝 Recent Devlog</h2>
					<p>Most recent work notes already detected by the WAFT backend.</p>
				</div>
				{#if state?.devlog?.length}
					<ul class="artifact-list">
						{#each state.devlog.slice(0, 8) as entry}
							<li class="artifact-item">
								<div class="artifact-name">{entry}</div>
							</li>
						{/each}
					</ul>
				{:else}
					<div class="empty-state">No recent devlog entries detected.</div>
				{/if}
			</section>
		</div>

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

		<!-- Project Structure & Gym -->
		<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
			<PyriteCard />
			<GymCard />
		</div>

		<!-- Bob the Cartographer -->
		<div class="grid grid-cols-1 gap-6 mb-6">
			<BobCard />
		</div>
	{/if}
</div>

<style>
	.container {
		max-width: 1600px;
	}

	.hero {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 1.5rem;
		padding: 1.75rem;
	}

	.hero-kicker {
		text-transform: uppercase;
		letter-spacing: 0.12em;
		font-size: 0.8rem;
		color: var(--text-muted);
		margin-bottom: 0.5rem;
	}

	.hero-actions {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.summary-grid {
		display: grid;
		grid-template-columns: repeat(4, minmax(0, 1fr));
		gap: 1rem;
		margin-bottom: 1.5rem;
	}

	.summary-card {
		padding: 1.25rem;
	}

	.summary-label {
		font-size: 0.8rem;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--text-muted);
		margin-bottom: 0.5rem;
	}

	.summary-value {
		font-size: 2rem;
		font-weight: 700;
		color: var(--primary-light);
		line-height: 1.1;
	}

	.summary-meta {
		margin-top: 0.5rem;
		font-size: 0.9rem;
		color: var(--text-secondary);
	}

	.control-grid {
		display: grid;
		grid-template-columns: 1.4fr 1fr;
		gap: 1rem;
		margin-bottom: 1.5rem;
	}

	.section-heading {
		margin-bottom: 1rem;
	}

	.section-heading h2 {
		font-size: 1.4rem;
		margin-bottom: 0.35rem;
	}

	.section-heading p {
		color: var(--text-secondary);
		font-size: 0.95rem;
	}

	.workspace-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 0.9rem;
	}

	.workspace-link {
		display: block;
		padding: 1rem;
		border: 1px solid var(--border);
		border-radius: var(--radius-md);
		text-decoration: none;
		color: inherit;
		background: rgba(255, 255, 255, 0.02);
		transition: all var(--transition-normal) ease;
	}

	.workspace-link:hover {
		border-color: var(--border-focus);
		background: var(--bg-card-hover);
		transform: translateY(-2px);
		box-shadow: var(--shadow-md);
	}

	.workspace-title {
		font-size: 1rem;
		font-weight: 700;
		color: var(--primary-light);
		margin-bottom: 0.35rem;
	}

	.workspace-description {
		font-size: 0.92rem;
		color: var(--text-secondary);
	}

	.context-list {
		display: grid;
		gap: 0.9rem;
	}

	.context-item,
	.artifact-item {
		padding: 0.95rem;
		border: 1px solid var(--border);
		border-radius: var(--radius-md);
		background: rgba(255, 255, 255, 0.02);
	}

	.context-label {
		font-size: 0.78rem;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--text-muted);
		margin-bottom: 0.4rem;
	}

	.context-value {
		color: var(--text-primary);
		font-size: 0.95rem;
	}

	.artifact-list {
		list-style: none;
		display: grid;
		gap: 0.8rem;
	}

	.artifact-topline {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 0.75rem;
		margin-bottom: 0.45rem;
	}

	.artifact-type {
		font-size: 0.78rem;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--accent-light);
	}

	.artifact-age,
	.artifact-meta {
		font-size: 0.85rem;
		color: var(--text-muted);
	}

	.artifact-name {
		font-weight: 700;
		color: var(--text-primary);
		margin-bottom: 0.2rem;
	}

	.artifact-path {
		font-size: 0.82rem;
		color: var(--text-secondary);
		margin-bottom: 0.25rem;
		word-break: break-word;
	}

	.empty-state {
		padding: 1rem;
		border: 1px dashed var(--border);
		border-radius: var(--radius-md);
		color: var(--text-muted);
		text-align: center;
	}

	.mono {
		font-family: 'SF Mono', Monaco, Consolas, 'Liberation Mono', monospace;
	}

	@media (max-width: 1024px) {
		.summary-grid,
		.control-grid {
			grid-template-columns: 1fr 1fr;
		}
	}

	@media (max-width: 768px) {
		.hero,
		.summary-grid,
		.control-grid,
		.workspace-grid {
			grid-template-columns: 1fr;
			flex-direction: column;
		}
	}
</style>
