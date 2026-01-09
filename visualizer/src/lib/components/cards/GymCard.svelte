<script lang="ts">
	import { gymStore } from '$lib/stores/gymStore';
	import { onMount } from 'svelte';
	import Badge from '../status/Badge.svelte';

	onMount(() => {
		gymStore.fetch(10); // Fetch last 10 battle logs
	});

	$: battleLogs = $gymStore.battle_logs || [];
	$: stats = $gymStore.stats;
	$: loading = $gymStore.loading;
	$: error = $gymStore.error;

	function getScintTypeColor(scintType: string): string {
		switch (scintType) {
			case 'SYNTAX_TEAR':
				return 'text-yellow-500';
			case 'LOGIC_FRACTURE':
				return 'text-red-500';
			case 'SAFETY_VOID':
				return 'text-purple-500';
			case 'HALLUCINATION':
				return 'text-orange-500';
			default:
				return 'text-gray-500';
		}
	}

	function getScintTypeIcon(scintType: string): string {
		switch (scintType) {
			case 'SYNTAX_TEAR':
				return '⚡';
			case 'LOGIC_FRACTURE':
				return '🔴';
			case 'SAFETY_VOID':
				return '🛡️';
			case 'HALLUCINATION':
				return '👁️';
			default:
				return '⚠️';
		}
	}

	function formatTimestamp(timestamp: string): string {
		try {
			const date = new Date(timestamp);
			return date.toLocaleString();
		} catch {
			return timestamp;
		}
	}
</script>

<div class="card">
	<h2>🎮 Jungle Gym - Reality Fractures</h2>
	<div class="card-content">
		{#if loading}
			<div class="info-item text-center py-8">
				<div class="text-4xl mb-2 opacity-50">⏳</div>
				<div class="empty text-lg">Loading battle logs...</div>
			</div>
		{:else if error}
			<div class="info-item text-center py-8">
				<div class="text-4xl mb-2 opacity-50">❌</div>
				<div class="empty text-lg">Error: {error}</div>
			</div>
		{:else if stats && stats.total_quests === 0}
			<div class="info-item text-center py-8">
				<div class="text-4xl mb-2 opacity-50">🎯</div>
				<div class="empty text-lg">No quests completed yet</div>
				<div class="text-sm text-[var(--text-secondary)] mt-3">Run <code>python3 play_gym.py</code> to start</div>
			</div>
		{:else}
			<!-- Stats Summary -->
			{#if stats}
				<div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
					<div class="info-item">
						<div class="info-label text-sm">Total Quests</div>
						<div class="info-value text-2xl font-bold">{stats.total_quests}</div>
					</div>
					<div class="info-item">
						<div class="info-label text-sm">Stabilized</div>
						<div class="info-value text-2xl font-bold text-green-500">{stats.stabilized_quests}</div>
					</div>
					<div class="info-item">
						<div class="info-label text-sm">Fractures Detected</div>
						<div class="info-value text-2xl font-bold text-yellow-500">{stats.scints_detected}</div>
					</div>
					<div class="info-item">
						<div class="info-label text-sm">Success Rate</div>
						<div class="info-value text-2xl font-bold">
							{stats.stabilization_attempts && stats.stabilization_attempts > 0
								? (stats.stabilization_success_rate * 100).toFixed(0)
								: 'N/A'}%
						</div>
					</div>
				</div>
			{/if}

			<!-- Recent Battle Logs -->
			<div class="info-item">
				<div class="info-label">
					Recent Battles
					<span class="ml-2"><Badge type="info">{battleLogs.length}</Badge></span>
				</div>
				{#if battleLogs.length > 0}
					<div class="space-y-4 mt-4">
						{#each battleLogs as log}
							<div class="battle-log p-4 rounded-lg border border-[var(--border)] bg-[var(--bg-secondary)]">
								<!-- Quest Header -->
								<div class="flex items-center justify-between mb-2">
									<div class="flex items-center gap-2">
										<span class="font-bold text-[var(--primary-light)]">{log.quest_name}</span>
										{#if log.result === 'stabilized'}
											<Badge type="success">✨ Stabilized</Badge>
										{:else if log.success}
											<Badge type="info">✅ Success</Badge>
										{:else}
											<Badge type="warning">❌ Failed</Badge>
										{/if}
									</div>
									<span class="text-xs text-[var(--text-secondary)]">
										{formatTimestamp(log.timestamp)}
									</span>
								</div>

								<!-- Reality Fractures -->
								{#if log.scints_detected && log.scints_detected.length > 0}
									<div class="mt-3 p-3 rounded bg-yellow-500/10 border border-yellow-500/30">
										<div class="flex items-center gap-2 mb-2">
											<span class="text-yellow-500 font-bold">⚠️ REALITY FRACTURE DETECTED</span>
											{#if log.max_severity}
												<Badge type="warning">
													Severity: {(log.max_severity * 100).toFixed(0)}%
												</Badge>
											{/if}
										</div>
										<div class="flex flex-wrap gap-2">
											{#each log.scints_detected as scintType}
												<div class="flex items-center gap-1 px-2 py-1 rounded bg-[var(--bg-card)] border border-[var(--border)]">
													<span class="text-lg">{getScintTypeIcon(scintType)}</span>
													<span class="text-sm {getScintTypeColor(scintType)} font-mono">
														{scintType}
													</span>
												</div>
											{/each}
										</div>
									</div>
								{/if}

								<!-- Stabilization History -->
								{#if log.stabilization_attempted}
									<div class="mt-3 p-3 rounded {log.stabilization_successful ? 'bg-green-500/10 border border-green-500/30' : 'bg-red-500/10 border border-red-500/30'}">
										<div class="flex items-center gap-2 mb-2">
											<span class="text-lg">🌀</span>
											<span class="font-bold {log.stabilization_successful ? 'text-green-500' : 'text-red-500'}">
												Stabilization Loop
											</span>
											<Badge type={log.stabilization_successful ? 'success' : 'warning'}>
												{log.stabilization_attempts} attempt{log.stabilization_attempts !== 1 ? 's' : ''}
											</Badge>
										</div>
										{#if log.stabilization_successful}
											<div class="text-sm text-green-500">
												✨ Stabilized on attempt {log.stabilization_attempts}
											</div>
										{:else}
											<div class="text-sm text-red-500">
												❌ Stabilization failed after {log.stabilization_attempts} attempt{log.stabilization_attempts !== 1 ? 's' : ''}
											</div>
										{/if}
										{#if log.original_response && log.corrected_response}
											<div class="mt-2 text-xs text-[var(--text-secondary)]">
												<div class="font-mono bg-[var(--bg-card)] p-2 rounded mt-1">
													<div class="text-red-400 line-through opacity-70">
														Original: {log.original_response.substring(0, 100)}...
													</div>
													<div class="text-green-400 mt-1">
														Corrected: {log.corrected_response.substring(0, 100)}...
													</div>
												</div>
											</div>
										{/if}
									</div>
								{/if}

								<!-- Agent Call Count -->
								{#if log.agent_call_count > 1}
									<div class="mt-2 text-xs text-[var(--text-secondary)]">
										Agent calls: {log.agent_call_count} (normal: 1, stabilized: +{log.agent_call_count - 1})
									</div>
								{/if}
							</div>
						{/each}
					</div>
				{:else}
					<div class="empty">No battle logs found</div>
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
		border: 1px solid var(--border);
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	}

	.card h2 {
		font-size: 1.5rem;
		font-weight: 700;
		margin-bottom: 20px;
		color: var(--primary-light);
	}

	.card-content {
		display: flex;
		flex-direction: column;
		gap: 16px;
	}

	.info-item {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.info-label {
		font-weight: 600;
		color: var(--text-primary);
		display: flex;
		align-items: center;
	}

	.info-value {
		color: var(--text-primary);
	}

	.battle-log {
		transition: all 0.2s ease;
	}

	.battle-log:hover {
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
		transform: translateY(-2px);
	}

	.empty {
		color: var(--text-secondary);
		font-style: italic;
		text-align: center;
		padding: 20px;
	}

	code {
		background: var(--bg-secondary);
		padding: 2px 6px;
		border-radius: 4px;
		font-family: 'Courier New', monospace;
		font-size: 0.9em;
	}
</style>
