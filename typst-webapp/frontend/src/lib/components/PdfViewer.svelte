<script lang="ts">
	export let url: string;

	let error = false;

	function handleLoad() {
		error = false;
	}

	function handleError() {
		error = true;
	}
</script>

<div class="viewer">
	{#if error}
		<div class="error">
			<span>Failed to load PDF</span>
			<a href={url} target="_blank" rel="noopener">
				Open in new tab →
			</a>
		</div>
	{:else}
		<iframe
			src={url}
			title="PDF Preview"
			on:load={handleLoad}
			on:error={handleError}
		/>
	{/if}
	<div class="toolbar">
		<a href={url} target="_blank" rel="noopener" class="btn">
			🔗 Open in New Tab
		</a>
		<a href={url} download class="btn">
			⬇️ Download
		</a>
	</div>
</div>

<style>
	.viewer {
		display: flex;
		flex-direction: column;
		flex: 1;
		background: var(--bg-input);
		border-radius: 0.5rem;
		overflow: hidden;
	}

	iframe {
		flex: 1;
		border: none;
		background: white;
	}

	.error {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 1rem;
		color: var(--text-muted);
	}

	.toolbar {
		display: flex;
		gap: 0.5rem;
		padding: 0.75rem;
		background: var(--bg-card);
		border-top: 1px solid var(--border);
	}

	.btn {
		background: var(--bg-input);
		color: var(--text);
		padding: 0.5rem 1rem;
		border-radius: 0.375rem;
		font-size: 0.875rem;
		text-decoration: none;
		transition: background 0.2s;
	}

	.btn:hover {
		background: var(--border);
		text-decoration: none;
	}
</style>
