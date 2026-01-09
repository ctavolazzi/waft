<script lang="ts">
	import { projectStore } from '$lib/stores/projectStore';
	import Badge from '../status/Badge.svelte';

	$: pyrite = $projectStore.state?.pyrite;
	$: statusClass = pyrite?.valid ? 'valid' : 'invalid';
	$: statusText = pyrite?.valid ? '✅ Valid' : '❌ Invalid';
	$: totalFiles = (pyrite?.active_files?.length || 0) + (pyrite?.backlog_files?.length || 0) + (pyrite?.standards_files?.length || 0);
</script>

<div class="card">
	<h2>💎 Project Structure</h2>
	<div class="card-content">
		<div class="info-item">
			<div class="info-label">Structure Status</div>
			<div class="info-value">
				<span class="status {statusClass}">{statusText}</span>
				<span class="ml-3 text-[var(--text-secondary)] text-sm">{totalFiles} total files</span>
			</div>
		</div>
		<div class="info-item">
			<div class="info-label">
				Active Files
				<Badge type="info" class="ml-2 text-xs">{pyrite?.active_files?.length || 0}</Badge>
			</div>
			{#if pyrite?.active_files && pyrite.active_files.length > 0}
				<ul class="file-list">
					{#each pyrite.active_files.slice(0, 15) as file}
						<li>📄 {file}</li>
					{/each}
					{#if pyrite.active_files.length > 15}
						<li class="empty">... and {pyrite.active_files.length - 15} more files</li>
					{/if}
				</ul>
			{:else}
				<div class="empty">No active files</div>
			{/if}
		</div>
		<div class="grid grid-cols-2 gap-3 mt-3">
			<div class="info-item">
				<div class="info-label">Backlog</div>
				<div class="info-value">
					<Badge type={pyrite?.backlog_files && pyrite.backlog_files.length > 0 ? 'info' : 'warning'}>
						{pyrite?.backlog_files?.length || 0} files
					</Badge>
				</div>
			</div>
			<div class="info-item">
				<div class="info-label">Standards</div>
				<div class="info-value">
					<Badge type={pyrite?.standards_files && pyrite.standards_files.length > 0 ? 'info' : 'warning'}>
						{pyrite?.standards_files?.length || 0} files
					</Badge>
				</div>
			</div>
		</div>
	</div>
</div>

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

	.status.valid {
		background: linear-gradient(135deg, rgba(74, 222, 128, 0.2), rgba(74, 222, 128, 0.1));
		color: var(--success);
		border: 1px solid rgba(74, 222, 128, 0.3);
	}

	.status.invalid {
		background: linear-gradient(135deg, rgba(248, 113, 113, 0.2), rgba(248, 113, 113, 0.1));
		color: var(--error);
		border: 1px solid rgba(248, 113, 113, 0.3);
	}

	.file-list {
		list-style: none;
		margin-top: 12px;
		max-height: 300px;
		overflow-y: auto;
		padding-right: 8px;
	}

	.file-list li {
		padding: 10px 12px;
		margin: 6px 0;
		background: rgba(26, 30, 41, 0.6);
		border-radius: 8px;
		border-left: 3px solid var(--primary);
		color: var(--text-primary);
		transition: all 0.2s ease;
		cursor: pointer;
	}

	.file-list li:hover {
		background: rgba(35, 40, 52, 0.9);
		transform: translateX(6px);
		border-left-color: var(--primary-light);
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
	}

	.empty {
		color: var(--text-muted);
		font-style: italic;
		padding: 20px;
		text-align: center;
	}
</style>
