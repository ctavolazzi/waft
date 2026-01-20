<script lang="ts">
	import { onMount } from 'svelte';
	import TemplateCard from '$lib/components/TemplateCard.svelte';
	import PdfViewer from '$lib/components/PdfViewer.svelte';
	import CodeEditor from '$lib/components/CodeEditor.svelte';

	const API_BASE = 'http://localhost:8000';

	interface Template {
		name: string;
		description: string;
		package: string;
		version: string;
		url: string;
	}

	let templates: Record<string, Template> = {};
	let selectedTemplate: string | null = null;
	let sourceCode = '';
	let pdfUrl = '';
	let loading = false;
	let error = '';
	let compileLoading = false;

	onMount(async () => {
		await loadTemplates();
	});

	async function loadTemplates() {
		try {
			const res = await fetch(`${API_BASE}/api/templates`);
			const data = await res.json();
			templates = data.templates;
		} catch (e) {
			error = 'Failed to load templates. Make sure the backend is running.';
		}
	}

	async function selectTemplate(templateId: string) {
		loading = true;
		error = '';
		selectedTemplate = templateId;

		try {
			// Load source code
			const sourceRes = await fetch(`${API_BASE}/api/source/${templateId}`);
			const sourceData = await sourceRes.json();
			sourceCode = sourceData.content;

			// Set PDF URL
			pdfUrl = `${API_BASE}/api/pdf/${templateId}`;
		} catch (e) {
			error = `Failed to load template: ${e}`;
		} finally {
			loading = false;
		}
	}

	async function compileCode() {
		compileLoading = true;
		error = '';

		try {
			const res = await fetch(`${API_BASE}/api/compile`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					content: sourceCode,
					filename: selectedTemplate || 'custom'
				})
			});

			if (!res.ok) {
				const errorData = await res.json();
				error = errorData.error || 'Compilation failed';
				return;
			}

			// Create blob URL for the PDF
			const blob = await res.blob();
			pdfUrl = URL.createObjectURL(blob);
		} catch (e) {
			error = `Compilation error: ${e}`;
		} finally {
			compileLoading = false;
		}
	}

	function handleCodeChange(event: CustomEvent<string>) {
		sourceCode = event.detail;
	}
</script>

<svelte:head>
	<title>Typst Demo - FastAPI + SvelteKit</title>
</svelte:head>

<div class="page">
	<section class="hero">
		<h1>Typst Package Demos</h1>
		<p>Explore and edit Typst document templates with live PDF preview</p>
	</section>

	{#if error}
		<div class="error-banner">
			<span>⚠️ {error}</span>
			<button on:click={() => (error = '')}>×</button>
		</div>
	{/if}

	<section class="templates">
		<h2>Available Templates</h2>
		<div class="template-grid">
			{#each Object.entries(templates) as [id, template]}
				<TemplateCard
					{id}
					name={template.name}
					description={template.description}
					packageName={template.package}
					version={template.version}
					url={template.url}
					selected={selectedTemplate === id}
					on:select={() => selectTemplate(id)}
				/>
			{/each}
		</div>
	</section>

	{#if selectedTemplate}
		<section class="workspace">
			<div class="workspace-header">
				<h2>Workspace: {templates[selectedTemplate]?.name}</h2>
				<button
					class="compile-btn"
					on:click={compileCode}
					disabled={compileLoading}
				>
					{compileLoading ? '⏳ Compiling...' : '▶️ Compile'}
				</button>
			</div>

			<div class="workspace-content">
				<div class="editor-panel">
					<h3>Source Code</h3>
					{#if loading}
						<div class="loading">Loading...</div>
					{:else}
						<CodeEditor code={sourceCode} on:change={handleCodeChange} />
					{/if}
				</div>

				<div class="preview-panel">
					<h3>PDF Preview</h3>
					{#if pdfUrl}
						<PdfViewer url={pdfUrl} />
					{:else}
						<div class="placeholder">
							Select a template to view the PDF
						</div>
					{/if}
				</div>
			</div>
		</section>
	{/if}
</div>

<style>
	.page {
		display: flex;
		flex-direction: column;
		gap: 2rem;
	}

	.hero {
		text-align: center;
		padding: 2rem 0;
	}

	.hero h1 {
		font-size: 2.5rem;
		margin-bottom: 0.5rem;
		background: linear-gradient(135deg, var(--primary), var(--secondary));
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}

	.hero p {
		color: var(--text-muted);
		font-size: 1.1rem;
	}

	.error-banner {
		background: rgba(239, 68, 68, 0.2);
		border: 1px solid var(--error);
		border-radius: 0.5rem;
		padding: 1rem;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.error-banner button {
		background: none;
		border: none;
		color: var(--text);
		font-size: 1.5rem;
		padding: 0 0.5rem;
	}

	.templates h2,
	.workspace h2 {
		margin-bottom: 1rem;
	}

	.template-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		gap: 1rem;
	}

	.workspace {
		background: var(--bg-card);
		border-radius: 1rem;
		padding: 1.5rem;
	}

	.workspace-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1rem;
		padding-bottom: 1rem;
		border-bottom: 1px solid var(--border);
	}

	.compile-btn {
		background: var(--primary);
		color: white;
		border: none;
		padding: 0.75rem 1.5rem;
		border-radius: 0.5rem;
		font-weight: 600;
		font-size: 1rem;
		transition: background 0.2s;
	}

	.compile-btn:hover:not(:disabled) {
		background: var(--primary-dark);
	}

	.compile-btn:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.workspace-content {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1rem;
		min-height: 600px;
	}

	.editor-panel,
	.preview-panel {
		display: flex;
		flex-direction: column;
	}

	.editor-panel h3,
	.preview-panel h3 {
		margin-bottom: 0.5rem;
		color: var(--text-muted);
		font-size: 0.875rem;
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.loading,
	.placeholder {
		display: flex;
		align-items: center;
		justify-content: center;
		flex: 1;
		background: var(--bg-input);
		border-radius: 0.5rem;
		color: var(--text-muted);
	}

	@media (max-width: 900px) {
		.workspace-content {
			grid-template-columns: 1fr;
		}
	}
</style>
