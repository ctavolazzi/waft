<script lang="ts">
	import { projectStore } from '$lib/stores/projectStore';
	import Badge from '../status/Badge.svelte';

	$: state = $projectStore.state;
	$: pyrite = state?.pyrite;
	$: git = state?.git;
	$: gam = state?.gamification;

	$: healthScore = pyrite && git && gam
		? (pyrite.valid ? 25 : 0) +
		  (git.initialized ? 25 : 0) +
		  (gam.integrity >= 90 ? 25 : 0) +
		  ((git.uncommitted_files?.length || 0) < 10 ? 25 : 0)
		: 0;

	$: healthColor = healthScore >= 75 ? 'success' : healthScore >= 50 ? 'warning' : 'error';
	$: healthText = healthScore >= 75 ? 'Excellent' : healthScore >= 50 ? 'Good' : 'Needs Attention';

	$: uncommitted = git?.uncommitted_files?.length || 0;
	$: gitStatusText = uncommitted === 0 ? 'Clean' : `${uncommitted} files`;
	$: gitStatusClass = uncommitted === 0 ? 'success' : uncommitted < 20 ? 'warning' : 'error';
</script>

<div class="card">
	<h2>⚡ Status Overview</h2>
	<div class="card-content">
		<div class="info-item text-center py-5">
			<div class="text-5xl mb-2">
				{healthScore >= 75 ? '🟢' : healthScore >= 50 ? '🟡' : '🔴'}
			</div>
			<div class="text-2xl font-bold mb-2">{healthText}</div>
			<div class="text-sm text-[var(--text-secondary)]">{healthScore}% Health Score</div>
		</div>
		<div class="info-item">
			<div class="info-label">Quick Status</div>
			<div class="flex flex-wrap gap-2 mt-2">
				<Badge type={healthColor}>{healthText}</Badge>
				<Badge type={gitStatusClass}>{gitStatusText}</Badge>
				<Badge type={pyrite?.valid ? 'success' : 'error'}>
					{pyrite?.valid ? 'Valid' : 'Invalid'} Structure
				</Badge>
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
</style>
