<script lang="ts">
	import { projectStore } from '$lib/stores/projectStore';
	import Badge from '../status/Badge.svelte';

	$: efforts = $projectStore.state?.work_efforts || [];
	$: devlog = $projectStore.state?.devlog || [];
</script>

<div class="card">
	<h2>📋 Work & Activity</h2>
	<div class="card-content">
		{#if efforts.length === 0 && devlog.length === 0}
			<div class="info-item text-center py-8">
				<div class="text-4xl mb-2 opacity-50">📭</div>
				<div class="empty text-lg">No active work efforts</div>
				<div class="text-sm text-[var(--text-secondary)] mt-3">Recent activity will appear here</div>
			</div>
		{:else}
			<div class="info-item">
				<div class="info-label">
					Active Work Efforts
					<span class="ml-2"><Badge type="info">{efforts.length} active</Badge></span>
				</div>
				{#if efforts.length > 0}
					<ul class="file-list">
						{#each efforts.slice(0, 8) as effort}
							<li>📋 <strong>{effort.id}</strong></li>
						{/each}
						{#if efforts.length > 8}
							<li class="empty">... and {efforts.length - 8} more work efforts</li>
						{/if}
					</ul>
				{:else}
					<div class="empty">No active work efforts</div>
				{/if}
			</div>
			<div class="info-item mt-4">
				<div class="info-label">Recent Devlog</div>
				{#if devlog.length > 0}
					<ul class="file-list">
						{#each devlog.slice(0, 5) as entry}
							<li>📝 {entry.length > 60 ? entry.slice(0, 60) + '...' : entry}</li>
						{/each}
					</ul>
				{:else}
					<div class="empty">No recent devlog entries</div>
				{/if}
			</div>
		{/if}
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

	.file-list {
		list-style: none;
		margin-top: 12px;
		max-height: 320px;
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
