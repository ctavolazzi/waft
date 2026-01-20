<script lang="ts">
	import { onMount } from 'svelte';
	import { apiClient } from '$lib/api/client';

	let loading = true;
	let empiricaData: any = null;
	let workEfforts: any[] = [];
	let lastUpdated = new Date();

	onMount(async () => {
		await loadData();
	});

	async function loadData() {
		try {
			loading = true;
			const state = await apiClient.getState();
			workEfforts = state.work_efforts || [];
			
			try {
				empiricaData = await apiClient.get('/api/empirica');
			} catch (e) {
				empiricaData = { initialized: false };
			}
			
			lastUpdated = new Date();
			loading = false;
		} catch (e) {
			console.error('Failed to load data:', e);
			loading = false;
		}
	}
</script>

<div class="cognitive-tools-page">
	<!-- Header Section -->
	<header class="page-header">
		<div class="header-content">
			<h1 class="page-title">Cognitive Tools</h1>
			<p class="page-subtitle">Epistemic tracking and thinking tools</p>
		</div>
	</header>

	<!-- Main Content Area -->
	<main class="page-main">
		<!-- Left Sidebar -->
		<aside class="sidebar-left">
			<div class="sidebar-content">
				<h3 class="sidebar-title">Session Status</h3>
				{#if empiricaData?.initialized}
					<div class="status-item">
						<span class="status-label">Empirica:</span>
						<span class="status-value status-active">Active</span>
					</div>
				{:else}
					<div class="status-item">
						<span class="status-label">Empirica:</span>
						<span class="status-value status-inactive">Not Ready</span>
					</div>
				{/if}
				<div class="status-item">
					<span class="status-label">Work Efforts:</span>
					<span class="status-value status-active">{workEfforts.length} active</span>
				</div>
			</div>
		</aside>

		<!-- Center Content -->
		<section class="content-center">
			<!-- Tools Status Section -->
			<div class="tools-status-section">
				<div class="section-content">
					<h2 class="section-title">Tools Status</h2>
					<div class="status-grid">
						<div class="status-card">
							<div class="status-card-label">Empirica</div>
							<div class="status-card-value">
								{#if empiricaData?.initialized}
									<span class="status-badge status-ready">Ready</span>
								{:else}
									<span class="status-badge status-not-ready">Not Ready</span>
								{/if}
							</div>
						</div>
						<div class="status-card">
							<div class="status-card-label">Sequential Thinking</div>
							<div class="status-card-value">
								<span class="status-badge status-ready">Available</span>
							</div>
						</div>
						<div class="status-card">
							<div class="status-card-label">Work Efforts</div>
							<div class="status-card-value">
								<span class="status-badge status-ready">{workEfforts.length} Active</span>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Sequential Thinking Section -->
			<div class="sequential-thinking-section">
				<div class="section-content">
					<h2 class="section-title">Sequential Thinking</h2>
					<div class="sequential-info">
						<p class="info-message">MCP-based tool - activity tracked via MCP server</p>
						<div class="info-row">
							<span class="info-label">Status:</span>
							<span class="info-value">Available</span>
						</div>
					</div>
				</div>
			</div>

			<!-- Empirica Section -->
			<div class="empirica-section">
				<div class="section-content">
					<h2 class="section-title">Empirica</h2>
					{#if empiricaData?.initialized}
						<div class="empirica-info">
							<div class="info-row">
								<span class="info-label">Status:</span>
								<span class="info-value">Initialized</span>
							</div>
							{#if empiricaData.epistemic_state}
								<div class="info-row">
									<span class="info-label">Epistemic State:</span>
									<span class="info-value">Available</span>
								</div>
							{/if}
							{#if empiricaData.goals}
								<div class="info-row">
									<span class="info-label">Goals:</span>
									<span class="info-value">{empiricaData.goals.length}</span>
								</div>
							{/if}
						</div>
					{:else}
						<div class="empirica-info">
							<p class="info-message">Empirica not initialized</p>
						</div>
					{/if}
				</div>
			</div>

			<!-- Work Efforts Section -->
			<div class="work-efforts-section">
				<div class="section-content">
					<h2 class="section-title">Work Efforts</h2>
					<div class="work-efforts-list">
						{#if workEfforts.length > 0}
							{#each workEfforts.slice(0, 5) as effort}
								<div class="work-effort-item">
									<span class="effort-id">{effort.id}</span>
								</div>
							{/each}
							{#if workEfforts.length > 5}
								<div class="work-effort-more">+ {workEfforts.length - 5} more</div>
							{/if}
						{:else}
							<p class="info-message">No work efforts found</p>
						{/if}
					</div>
				</div>
			</div>
		</section>

		<!-- Right Sidebar -->
		<aside class="sidebar-right">
			<div class="sidebar-content">
				<h3 class="sidebar-title">Quick Info</h3>
				<div class="info-message">Context and insights will appear here</div>
			</div>
		</aside>
	</main>

	<!-- Footer Section -->
	<footer class="page-footer">
		<div class="footer-content">
			<span class="footer-text">Last updated: {lastUpdated.toLocaleTimeString()}</span>
		</div>
	</footer>
</div>

<style>
	/* Box Model - Clean Structure */
	.cognitive-tools-page {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
		width: 100%;
	}

	/* Header Box */
	.page-header {
		width: 100%;
		border: 2px solid #3a3a4a;
		background-color: #1e1e2e;
	}

	.header-content {
		padding: 1rem 2rem;
		min-height: 80px;
	}


	/* Main Content Box */
	.page-main {
		display: grid;
		grid-template-columns: 250px 1fr 250px;
		gap: 1rem;
		flex: 1;
		padding: 1rem;
		width: 100%;
	}

	/* Sidebar Boxes */
	.sidebar-left,
	.sidebar-right {
		border: 2px solid #3a3a4a;
		background-color: #1e1e2e;
	}

	.sidebar-content {
		padding: 1rem;
		min-height: 200px;
	}

	/* Center Content Box */
	.content-center {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	/* Section Boxes */
	.tools-status-section,
	.sequential-thinking-section,
	.empirica-section,
	.work-efforts-section {
		border: 2px solid #3a3a4a;
		background-color: #1e1e2e;
	}

	.section-content {
		padding: 1.5rem;
		min-height: 200px;
	}

	/* Footer Box */
	.page-footer {
		width: 100%;
		border: 2px solid #3a3a4a;
		background-color: #1e1e2e;
	}

	.footer-content {
		padding: 1rem 2rem;
		min-height: 60px;
	}

	/* Typography */
	.page-title {
		font-size: 2rem;
		font-weight: 700;
		color: var(--primary-light);
		margin: 0 0 0.5rem 0;
	}

	.page-subtitle {
		font-size: 1rem;
		color: var(--text-secondary);
		margin: 0;
	}

	.section-title {
		font-size: 1.25rem;
		font-weight: 600;
		color: var(--text-primary);
		margin: 0 0 1rem 0;
		border-bottom: 1px solid var(--border);
		padding-bottom: 0.5rem;
	}

	.sidebar-title {
		font-size: 1rem;
		font-weight: 600;
		color: var(--text-primary);
		margin: 0 0 1rem 0;
	}

	/* Status Items */
	.status-item {
		display: flex;
		justify-content: space-between;
		padding: 0.5rem 0;
		border-bottom: 1px solid var(--border);
	}

	.status-label {
		color: var(--text-secondary);
		font-size: 0.9rem;
	}

	.status-value {
		font-size: 0.9rem;
		font-weight: 600;
	}

	.status-active {
		color: var(--success);
	}

	.status-inactive {
		color: var(--text-muted);
	}

	/* Status Grid */
	.status-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
		gap: 1rem;
	}

	.status-card {
		padding: 1rem;
		border: 1px solid var(--border);
		border-radius: 6px;
		background-color: var(--bg-card);
	}

	.status-card-label {
		font-size: 0.9rem;
		color: var(--text-secondary);
		margin-bottom: 0.5rem;
	}

	.status-card-value {
		font-size: 1rem;
	}

	.status-badge {
		display: inline-block;
		padding: 0.25rem 0.75rem;
		border-radius: 4px;
		font-size: 0.85rem;
		font-weight: 600;
	}

	.status-ready {
		background-color: rgba(74, 222, 128, 0.2);
		color: var(--success);
		border: 1px solid var(--success);
	}

	.status-not-ready {
		background-color: rgba(248, 113, 113, 0.2);
		color: var(--error);
		border: 1px solid var(--error);
	}

	/* Empirica Info */
	.empirica-info {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.info-row {
		display: flex;
		justify-content: space-between;
		padding: 0.5rem 0;
	}

	.info-label {
		color: var(--text-secondary);
		font-size: 0.9rem;
	}

	.info-value {
		color: var(--text-primary);
		font-size: 0.9rem;
		font-weight: 600;
	}

	.info-message {
		color: var(--text-muted);
		font-size: 0.9rem;
		margin: 0;
	}

	/* Work Efforts */
	.work-efforts-list {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.work-effort-item {
		padding: 0.5rem;
		border: 1px solid var(--border);
		border-radius: 4px;
		background-color: var(--bg-card);
	}

	.effort-id {
		font-family: monospace;
		font-size: 0.85rem;
		color: var(--text-primary);
	}

	.work-effort-more {
		padding: 0.5rem;
		text-align: center;
		color: var(--text-muted);
		font-size: 0.85rem;
	}

	/* Sequential Info */
	.sequential-info {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	/* Footer */
	.footer-text {
		font-size: 0.85rem;
		color: var(--text-muted);
	}

	/* Responsive - Stack on smaller screens */
	@media (max-width: 1024px) {
		.page-main {
			grid-template-columns: 1fr;
		}

		.sidebar-left,
		.sidebar-right {
			display: none;
		}
	}
</style>
