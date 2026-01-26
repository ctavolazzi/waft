<script lang="ts">
	import { selectedRun } from '$lib/stores/evolveUiStore';
	import WireframeBox from './WireframeBox.svelte';

	function formatTimestamp(timestamp: string): string {
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

	function openFile(path: string) {
		// Open file in new tab (relative to project root)
		window.open(`/api/files/${encodeURIComponent(path)}`, '_blank');
	}
</script>

<div class="run-details">
	{#if !$selectedRun}
		<div class="empty-state">
			<p>Select a run to view details</p>
		</div>
	{:else}
		{@const run = $selectedRun}

		<WireframeBox label="Metadata" variant="secondary" minHeight="auto">
			<div class="metadata-content">
				<div class="metadata-item">
					<strong>Run ID:</strong> <code>{run.run_id}</code>
				</div>
				<div class="metadata-item">
					<strong>Timestamp:</strong> {formatTimestamp(run.timestamp)}
				</div>
				<div class="metadata-item">
					<strong>Phase:</strong> <span class="phase-badge">{run.phase}</span>
				</div>
				{#if run.context}
					<div class="metadata-item">
						<strong>Context:</strong>
						<div class="context-preview">{run.context}</div>
					</div>
				{/if}
			</div>
		</WireframeBox>

		<WireframeBox label="Process Timeline" variant="secondary" minHeight="auto">
			<div class="timeline-content">
				<div class="timeline-step" class:completed={run.artifacts.design_doc}>
					<span class="step-icon">{run.artifacts.design_doc ? '✅' : '⭕'}</span>
					<span class="step-label">Analysis</span>
				</div>
				<div class="timeline-step" class:completed={run.artifacts.requirements}>
					<span class="step-icon">{run.artifacts.requirements ? '✅' : '⭕'}</span>
					<span class="step-label">Requirements</span>
				</div>
				<div class="timeline-step" class:completed={run.artifacts.wireframe}>
					<span class="step-icon">{run.artifacts.wireframe ? '✅' : '⭕'}</span>
					<span class="step-label">Wireframe</span>
				</div>
				<div class="timeline-step" class:completed={run.artifacts.screenshots.length > 1}>
					<span class="step-icon">{run.artifacts.screenshots.length > 1 ? '✅' : '⭕'}</span>
					<span class="step-label">Development</span>
				</div>
				<div class="timeline-step" class:completed={run.artifacts.html.length > 0}>
					<span class="step-icon">{run.artifacts.html.length > 0 ? '✅' : '⭕'}</span>
					<span class="step-label">Complete</span>
				</div>
			</div>
		</WireframeBox>

		<WireframeBox label="Artifact Gallery" variant="secondary" minHeight="auto">
			<div class="gallery-content">
				{#if run.artifacts.html.length > 0}
					<div class="artifact-section">
						<h4>HTML Files</h4>
						<div class="artifact-list">
							{#each run.artifacts.html as html}
								<button class="artifact-link" on:click={() => openFile(html)}>
									📄 {html.split('/').pop()}
								</button>
							{/each}
						</div>
					</div>
				{/if}

				{#if run.artifacts.screenshots.length > 0}
					<div class="artifact-section">
						<h4>Screenshots ({run.artifacts.screenshots.length})</h4>
						<div class="screenshot-grid">
							{#each run.artifacts.screenshots.slice(0, 6) as screenshot}
								<button class="screenshot-thumb" on:click={() => openFile(screenshot)}>
									<img src={`/api/files/${encodeURIComponent(screenshot)}`} alt="Screenshot" loading="lazy" />
								</button>
							{/each}
						</div>
					</div>
				{/if}

				{#if run.artifacts.case_files.length > 0}
					<div class="artifact-section">
						<h4>Case Files ({run.artifacts.case_files.length})</h4>
						<div class="artifact-list">
							{#each run.artifacts.case_files as caseFile}
								<button class="artifact-link" on:click={() => openFile(caseFile)}>
									📋 {caseFile.split('/').pop()}
								</button>
							{/each}
						</div>
					</div>
				{/if}

				{#if run.artifacts.html.length === 0 && run.artifacts.screenshots.length === 0 && run.artifacts.case_files.length === 0}
					<p class="no-artifacts">No artifacts found for this run.</p>
				{/if}
			</div>
		</WireframeBox>

		<WireframeBox label="File Browser" variant="secondary" minHeight="auto">
			<div class="file-browser-content">
				<div class="file-list">
					{#if run.artifacts.design_doc}
						<button class="file-link" on:click={() => openFile(run.artifacts.design_doc!)}>
							📄 Design Doc: {run.artifacts.design_doc.split('/').pop()}
						</button>
					{/if}
					{#if run.artifacts.requirements}
						<button class="file-link" on:click={() => openFile(run.artifacts.requirements!)}>
							📄 Requirements: {run.artifacts.requirements.split('/').pop()}
						</button>
					{/if}
					{#if run.artifacts.wireframe}
						<button class="file-link" on:click={() => openFile(run.artifacts.wireframe!)}>
							🖼️ Wireframe: {run.artifacts.wireframe.split('/').pop()}
						</button>
					{/if}
					{#if run.artifacts.context_analysis}
						<button class="file-link" on:click={() => openFile(run.artifacts.context_analysis!)}>
							📝 Context Analysis: {run.artifacts.context_analysis.split('/').pop()}
						</button>
					{/if}
					{#if !run.artifacts.design_doc && !run.artifacts.requirements && !run.artifacts.wireframe && !run.artifacts.context_analysis}
						<p class="no-files">No additional files found.</p>
					{/if}
				</div>
			</div>
		</WireframeBox>
	{/if}
</div>

<style>
	.run-details {
		display: flex;
		flex-direction: column;
		gap: 15px;
		height: 100%;
		overflow-y: auto;
	}

	.empty-state {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 100%;
		color: var(--text-secondary);
	}

	.metadata-content {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.metadata-item {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.metadata-item strong {
		color: var(--text-primary);
		font-weight: 600;
	}

	.metadata-item code {
		background-color: var(--bg-card-hover);
		padding: 0.25rem 0.5rem;
		border-radius: 4px;
		font-family: monospace;
		font-size: 0.875rem;
	}

	.phase-badge {
		display: inline-block;
		padding: 0.25rem 0.5rem;
		background-color: var(--primary);
		color: var(--bg-dark);
		border-radius: 4px;
		font-size: 0.875rem;
		font-weight: 600;
	}

	.context-preview {
		background-color: var(--bg-card-hover);
		padding: 0.75rem;
		border-radius: 4px;
		font-size: 0.875rem;
		line-height: 1.5;
		color: var(--text-secondary);
		max-height: 200px;
		overflow-y: auto;
	}

	.timeline-content {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.timeline-step {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 0.5rem;
		border-radius: 4px;
		transition: background-color 0.2s;
	}

	.timeline-step.completed {
		background-color: var(--bg-card-hover);
	}

	.step-icon {
		font-size: 1.25rem;
	}

	.step-label {
		color: var(--text-primary);
		font-weight: 500;
	}

	.gallery-content {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.artifact-section h4 {
		color: var(--text-primary);
		font-size: 1rem;
		font-weight: 600;
		margin-bottom: 0.75rem;
	}

	.artifact-list {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.artifact-link,
	.file-link {
		background-color: var(--bg-card-hover);
		border: 1px solid var(--border);
		border-radius: 4px;
		padding: 0.5rem 0.75rem;
		text-align: left;
		cursor: pointer;
		color: var(--text-primary);
		transition: all 0.2s;
	}

	.artifact-link:hover,
	.file-link:hover {
		background-color: var(--primary);
		color: var(--bg-dark);
		border-color: var(--primary);
	}

	.screenshot-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
		gap: 0.75rem;
	}

	.screenshot-thumb {
		background: none;
		border: 2px solid var(--border);
		border-radius: 4px;
		padding: 0;
		cursor: pointer;
		overflow: hidden;
		transition: all 0.2s;
	}

	.screenshot-thumb:hover {
		border-color: var(--primary);
		transform: scale(1.05);
	}

	.screenshot-thumb img {
		width: 100%;
		height: auto;
		display: block;
		max-height: 150px;
		object-fit: cover;
	}

	.file-list {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.no-artifacts,
	.no-files {
		color: var(--text-muted);
		text-align: center;
		padding: 1rem;
	}
</style>