<script lang="ts">
	import { projectStore } from '$lib/stores/projectStore';
	import Badge from '../status/Badge.svelte';
	import ProgressBar from '../status/ProgressBar.svelte';

	$: gam = $projectStore.state?.gamification;
	$: integrity = gam?.integrity || 0;
	$: insight = gam?.insight || 0;
	$: insightNeeded = gam?.insight_to_next || 100;
	$: progress = insightNeeded > 0 ? (insight / insightNeeded) * 100 : 0;
</script>

<div class="card">
	<h2>🎮 Gamification</h2>
	<div class="card-content">
		<div class="info-item">
			<div class="info-label">Integrity</div>
			<div class="info-value">
				<Badge type={integrity >= 90 ? 'success' : integrity >= 70 ? 'warning' : 'error'}>
					{integrity.toFixed(1)}%
				</Badge>
			</div>
		</div>
		<div class="info-item">
			<div class="info-label">Level</div>
			<div class="info-value">
				<Badge type="info">Level {gam?.level || 1}</Badge>
			</div>
		</div>
		<div class="info-item">
			<div class="info-label">Insight Progress</div>
			<div class="info-value">
				{insight.toFixed(0)} / {insightNeeded.toFixed(0)}
				<ProgressBar value={Math.min(progress, 100)} />
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
</style>
