<script lang="ts">
	import { projectStore } from '$lib/stores/projectStore';
	import Badge from '../status/Badge.svelte';

	$: git = $projectStore.state?.git;
	$: uncommitted = git?.uncommitted_files?.length || 0;
	$: statusClass = uncommitted === 0 ? 'success' : uncommitted < 20 ? 'warning' : 'error';
</script>

{#if !git?.initialized}
	<div class="card">
		<h2>🔀 Git Status</h2>
		<div class="card-content">
			<div class="info-item">
				<span class="status missing">Not Initialized</span>
			</div>
		</div>
	</div>
{:else}
	<div class="card">
		<h2>🔀 Git Summary</h2>
		<div class="card-content">
			<div class="info-item">
				<div class="info-label">Branch</div>
				<div class="info-value">
					<span class="font-mono text-[var(--primary-light)]">{git.branch || 'N/A'}</span>
				</div>
			</div>
			<div class="info-item">
				<div class="info-label">Uncommitted Changes</div>
				<div class="info-value">
					<Badge type={statusClass}>{uncommitted} file{uncommitted === 1 ? '' : 's'}</Badge>
				</div>
			</div>
			{#if git.commits_ahead > 0}
				<div class="info-item">
					<div class="info-label">Commits Ahead</div>
					<div class="info-value">
						<Badge type="info">{git.commits_ahead}</Badge>
					</div>
				</div>
			{/if}
		</div>
	</div>
{/if}

<style>
	.card {
		background: var(--bg-card);
		border-radius: 16px;
		padding: 28px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
		border: 1px solid var(--border);
	}

	.card h2 {
		color: var(--text-primary);
		margin-bottom: 20px;
		font-size: 1.5rem;
		border-bottom: 2px solid var(--border);
		padding-bottom: 12px;
	}

	.info-item {
		margin: 12px 0;
		padding: 14px;
		background: rgba(26, 30, 41, 0.6);
		border-radius: 10px;
		border: 1px solid var(--border);
	}

	.info-label {
		font-weight: 600;
		color: var(--text-secondary);
		margin-bottom: 6px;
		font-size: 0.9em;
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.info-value {
		color: var(--text-primary);
		font-size: 1.05em;
	}

	.status {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		padding: 6px 14px;
		border-radius: 20px;
		font-size: 0.85em;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.status.missing {
		background: linear-gradient(135deg, rgba(251, 191, 36, 0.2), rgba(251, 191, 36, 0.1));
		color: var(--warning);
		border: 1px solid rgba(251, 191, 36, 0.3);
	}
</style>
