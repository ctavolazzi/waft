<script lang="ts">
	import { projectStore } from '$lib/stores/projectStore';

	$: state = $projectStore.state;
	$: project = state?.project;
	$: projectPath = state?.project_path;
</script>

<div class="card">
	<h2>📦 Project Information</h2>
	<div class="card-content">
		<div class="info-item">
			<div class="info-label">Project Name</div>
			<div class="info-value">{project?.name || 'Unknown'}</div>
		</div>
		<div class="info-item">
			<div class="info-label">Version</div>
			<div class="info-value">{project?.version || 'Unknown'}</div>
		</div>
		<div class="info-item">
			<div class="info-label">Project Path</div>
			<div class="info-value path">{projectPath || 'Unknown'}</div>
		</div>
		{#if project?.description}
			<div class="info-item">
				<div class="info-label">Description</div>
				<div class="info-value description">{project.description}</div>
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

	.info-value {
		color: var(--text-primary);
		font-size: 1.1rem;
		font-weight: 500;
		word-break: break-word;
	}

	.info-value.path {
		font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
		font-size: 0.95rem;
		color: var(--text-secondary);
		opacity: 0.9;
	}

	.info-value.description {
		font-size: 0.95rem;
		color: var(--text-secondary);
		line-height: 1.5;
	}
</style>
