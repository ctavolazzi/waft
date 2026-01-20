<script lang="ts">
	import { evolveUiStore, type EvolveUIRun } from '$lib/stores/evolveUiStore';
	import Badge from '$lib/components/status/Badge.svelte';

	function formatTimestamp(timestamp: string): string {
		// YYYYMMDD_HHMMSS -> readable format
		const year = timestamp.substring(0, 4);
		const month = timestamp.substring(4, 6);
		const day = timestamp.substring(6, 8);
		const hour = timestamp.substring(9, 11);
		const minute = timestamp.substring(11, 13);
		const second = timestamp.substring(13, 15);
		
		const date = new Date(
			parseInt(year),
			parseInt(month) - 1,
			parseInt(day),
			parseInt(hour),
			parseInt(minute),
			parseInt(second)
		);
		
		return date.toLocaleString();
	}

	function getPhaseColor(phase: string): string {
		const colors: Record<string, string> = {
			'Complete': 'green',
			'Development': 'blue',
			'Wireframe': 'yellow',
			'Requirements': 'purple',
			'Analysis': 'gray',
			'Unknown': 'gray'
		};
		return colors[phase] || 'gray';
	}

	function selectRun(run: EvolveUIRun) {
		evolveUiStore.selectRun(run.run_id);
	}
</script>

<div class="runs-list">
	<h2 class="section-title">Evolve UI Runs</h2>
	
	{#if $evolveUiStore.loading}
		<div class="loading-state">
			<div class="spinner"></div>
			<p>Loading runs...</p>
		</div>
	{:else if $evolveUiStore.error}
		<div class="error-state">
			<p class="error-message">Error: {$evolveUiStore.error}</p>
			<button class="retry-button" on:click={() => evolveUiStore.fetch()}>
				Retry
			</button>
		</div>
	{:else if $evolveUiStore.runs.length === 0}
		<div class="empty-state">
			<p>No evolve-a-ui runs found.</p>
			<p class="hint">Run <code>/evolve-a-ui</code> to create your first UI evolution.</p>
		</div>
	{:else}
		<div class="runs-grid">
			{#each $evolveUiStore.runs as run (run.run_id)}
				<button
					class="run-card"
					class:selected={$evolveUiStore.selectedRunId === run.run_id}
					on:click={() => selectRun(run)}
					on:keydown={(e) => e.key === 'Enter' && selectRun(run)}
				>
					<div class="run-header">
						<Badge color={getPhaseColor(run.phase)}>{run.phase}</Badge>
						<span class="run-id">{run.run_id}</span>
					</div>
					<div class="run-timestamp">{formatTimestamp(run.timestamp)}</div>
					{#if run.context}
						<div class="run-context">{run.context.substring(0, 100)}...</div>
					{/if}
					<div class="run-stats">
						<span class="stat">
							{run.artifacts.html.length} HTML
						</span>
						<span class="stat">
							{run.artifacts.screenshots.length} Screenshots
						</span>
						<span class="stat">
							{run.artifacts.case_files.length} Cases
						</span>
					</div>
				</button>
			{/each}
		</div>
	{/if}
</div>

<style>
	.runs-list {
		display: flex;
		flex-direction: column;
		height: 100%;
	}

	.section-title {
		font-size: 1.5rem;
		font-weight: 600;
		margin-bottom: 1rem;
		color: var(--text-primary);
	}

	.loading-state,
	.error-state,
	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 3rem;
		text-align: center;
		color: var(--text-secondary);
	}

	.spinner {
		width: 2rem;
		height: 2rem;
		border: 3px solid var(--border);
		border-top-color: var(--primary);
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: 1rem;
	}

	@keyframes spin {
		to { transform: rotate(360deg); }
	}

	.error-message {
		color: var(--error);
		margin-bottom: 1rem;
	}

	.retry-button {
		padding: 0.5rem 1rem;
		background-color: var(--primary);
		color: var(--bg-dark);
		border: none;
		border-radius: 6px;
		cursor: pointer;
		font-weight: 600;
	}

	.retry-button:hover {
		background-color: var(--primary-dark);
	}

	.empty-state .hint {
		margin-top: 0.5rem;
		font-size: 0.875rem;
		color: var(--text-muted);
	}

	.empty-state code {
		background-color: var(--bg-card-hover);
		padding: 0.25rem 0.5rem;
		border-radius: 4px;
		font-family: monospace;
	}

	.runs-grid {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		overflow-y: auto;
		flex: 1;
	}

	.run-card {
		background-color: var(--bg-card);
		border: 2px solid var(--border);
		border-radius: 8px;
		padding: 1rem;
		cursor: pointer;
		text-align: left;
		transition: all 0.2s ease;
	}

	.run-card:hover {
		background-color: var(--bg-card-hover);
		border-color: var(--primary);
	}

	.run-card.selected {
		background-color: var(--bg-card-hover);
		border-color: var(--primary);
		box-shadow: 0 0 0 2px var(--primary);
	}

	.run-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 0.5rem;
	}

	.run-id {
		font-size: 0.75rem;
		color: var(--text-muted);
		font-family: monospace;
	}

	.run-timestamp {
		font-size: 0.875rem;
		color: var(--text-secondary);
		margin-bottom: 0.5rem;
	}

	.run-context {
		font-size: 0.875rem;
		color: var(--text-secondary);
		margin-bottom: 0.75rem;
		line-height: 1.4;
	}

	.run-stats {
		display: flex;
		gap: 1rem;
		font-size: 0.75rem;
		color: var(--text-muted);
	}

	.stat {
		display: inline-block;
	}
</style>