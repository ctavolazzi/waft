<script lang="ts">
	import { onMount } from 'svelte';

	type PdfItem = {
		id: string;
		name: string;
		path: string;
		size: number;
		mtime: number;
		updated_at: string;
	};

	type PdfVersion = {
		id: number;
		version_label: string;
		path: string;
		size: number;
		mtime: number;
		sha256: string;
		created_at: string;
	};

	type TypstTemplate = {
		name: string;
		path: string;
	};

	const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:4434';

	let pdfs: PdfItem[] = [];
	let selected: PdfItem | null = null;
	let versions: PdfVersion[] = [];
	let templates: TypstTemplate[] = [];
	let query = '';
	let loading = false;
	let error = '';
	let scanStatus = '';
	let searchTimer: ReturnType<typeof setTimeout> | null = null;

	const formatSize = (bytes: number) => {
		if (bytes < 1024) return `${bytes} B`;
		if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
		if (bytes < 1024 * 1024 * 1024) return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
		return `${(bytes / 1024 / 1024 / 1024).toFixed(1)} GB`;
	};

	const formatDate = (value: number | string) => {
		const date = typeof value === 'number' ? new Date(value * 1000) : new Date(value);
		return date.toLocaleString();
	};

	const loadTemplates = async () => {
		try {
			const res = await fetch(`${API_BASE}/api/typst/templates`);
			if (!res.ok) return;
			const data = await res.json();
			templates = data.items ?? [];
		} catch (err) {
			console.error(err);
		}
	};

	const loadPdfs = async (search = '') => {
		loading = true;
		error = '';
		try {
			const url = new URL(`${API_BASE}/api/pdfs`);
			if (search.trim()) url.searchParams.set('query', search.trim());
			const res = await fetch(url);
			if (!res.ok) throw new Error('Failed to load PDFs');
			const data = await res.json();
			pdfs = data.items ?? [];
			if (!selected && pdfs.length) {
				await selectPdf(pdfs[0]);
			}
			if (selected) {
				const stillExists = pdfs.find((item) => item.id === selected?.id);
				if (!stillExists && pdfs.length) {
					await selectPdf(pdfs[0]);
				}
			}
		} catch (err) {
			error = err instanceof Error ? err.message : 'Unknown error';
		} finally {
			loading = false;
		}
	};

	const selectPdf = async (pdf: PdfItem) => {
		selected = pdf;
		versions = [];
		try {
			const res = await fetch(`${API_BASE}/api/pdfs/${pdf.id}/versions`);
			if (!res.ok) return;
			const data = await res.json();
			versions = data.items ?? [];
		} catch (err) {
			console.error(err);
		}
	};

	const handleSearch = (value: string) => {
		query = value;
		if (searchTimer) clearTimeout(searchTimer);
		searchTimer = setTimeout(() => {
			loadPdfs(query);
		}, 250);
	};

	const runScan = async () => {
		scanStatus = 'Scanning...';
		try {
			const res = await fetch(`${API_BASE}/api/scan`, { method: 'POST' });
			if (!res.ok) throw new Error('Scan failed');
			const data = await res.json();
			scanStatus = `Scan complete: ${data.total ?? 0} PDFs (${data.new ?? 0} new, ${data.updated ?? 0} updated)`;
			await loadPdfs(query);
		} catch (err) {
			scanStatus = err instanceof Error ? err.message : 'Scan failed';
		}
	};

	const compileTemplate = async (name: string) => {
		scanStatus = `Compiling ${name}...`;
		try {
			const res = await fetch(`${API_BASE}/api/typst/compile`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ template: name })
			});
			if (!res.ok) {
				const detail = await res.json().catch(() => ({}));
				throw new Error(detail.detail ?? 'Compile failed');
			}
			const data = await res.json();
			await loadPdfs(query);
			const match = pdfs.find((item) => item.id === data.id);
			if (match) await selectPdf(match);
			scanStatus = `Compiled ${name} → ${data.name}`;
		} catch (err) {
			scanStatus = err instanceof Error ? err.message : 'Compile failed';
		}
	};

	onMount(async () => {
		await loadTemplates();
		await loadPdfs();
	});
</script>

<svelte:head>
	<title>WAFT PDF Library</title>
</svelte:head>

<div class="app">
	<header>
		<div>
			<h1>WAFT PDF Library</h1>
			<p>Search, version, and compile Typst templates into a living PDF library.</p>
		</div>
		<div class="actions">
			<input
				placeholder="Search PDFs..."
				value={query}
				on:input={(event) => handleSearch((event.target as HTMLInputElement).value)}
			/>
			<button on:click={runScan}>Rescan</button>
		</div>
	</header>

	<section class="status">
		{#if loading}
			<span>Loading PDFs...</span>
		{/if}
		{#if error}
			<span class="error">{error}</span>
		{/if}
		{#if scanStatus}
			<span>{scanStatus}</span>
		{/if}
	</section>

	<div class="content">
		<aside>
			<h2>PDFs ({pdfs.length})</h2>
			<ul>
				{#each pdfs as pdf}
					<li class:selected={selected?.id === pdf.id}>
						<button on:click={() => selectPdf(pdf)}>
							<span class="name">{pdf.name}</span>
							<span class="meta">{formatSize(pdf.size)} · {formatDate(pdf.mtime)}</span>
						</button>
					</li>
				{/each}
			</ul>
		</aside>

		<main>
			{#if selected}
				<div class="viewer-header">
					<div>
						<h2>{selected.name}</h2>
						<p class="path">{selected.path}</p>
						<div class="meta">
							<span>{formatSize(selected.size)}</span>
							<span>Updated {formatDate(selected.mtime)}</span>
						</div>
					</div>
					<a
						class="open"
						href={`${API_BASE}/api/pdfs/${selected.id}/file`}
						target="_blank"
						rel="noreferrer"
					>
						Open PDF
					</a>
				</div>

				<div class="viewer-body">
					<iframe
						src={`${API_BASE}/api/pdfs/${selected.id}/file`}
						title={selected.name}
					></iframe>
				</div>

				<div class="versions">
					<h3>Version History</h3>
					{#if versions.length === 0}
						<p>No versions captured yet.</p>
					{:else}
						<ul>
							{#each versions as version}
								<li>
									<span>{version.version_label}</span>
									<span>{formatSize(version.size)}</span>
									<span>{formatDate(version.created_at)}</span>
								</li>
							{/each}
						</ul>
					{/if}
				</div>
			{:else}
				<div class="empty">
					<h2>No PDF selected</h2>
					<p>Choose a PDF from the library or run a rescan.</p>
				</div>
			{/if}
		</main>

		<aside class="templates">
			<h2>Typst Templates</h2>
			{#if templates.length === 0}
				<p>No templates available.</p>
			{:else}
				<ul>
					{#each templates as template}
						<li>
							<div>
								<strong>{template.name}</strong>
								<small>{template.path}</small>
							</div>
							<button on:click={() => compileTemplate(template.name)}>Compile</button>
						</li>
					{/each}
				</ul>
			{/if}
		</aside>
	</div>
</div>

<style>
	:global(body) {
		margin: 0;
		font-family: 'Inter', system-ui, sans-serif;
		background: #0b0f14;
		color: #eef2f6;
	}

	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 2rem;
		padding: 1.5rem 2rem 1rem;
		border-bottom: 1px solid #1f2937;
		background: #0f1620;
	}

	header h1 {
		margin: 0 0 0.25rem;
		font-size: 1.8rem;
	}

	header p {
		margin: 0;
		color: #94a3b8;
	}

	.actions {
		display: flex;
		gap: 0.75rem;
		align-items: center;
	}

	.actions input {
		padding: 0.6rem 0.8rem;
		min-width: 240px;
		border-radius: 8px;
		border: 1px solid #1f2937;
		background: #0b1220;
		color: inherit;
	}

	.actions button {
		padding: 0.6rem 1rem;
		border-radius: 8px;
		border: 1px solid #1f2937;
		background: #1d4ed8;
		color: white;
		cursor: pointer;
	}

	.status {
		padding: 0.5rem 2rem;
		color: #cbd5f5;
		min-height: 1.5rem;
	}

	.status .error {
		color: #f87171;
	}

	.content {
		flex: 1;
		display: grid;
		grid-template-columns: 280px 1fr 320px;
		gap: 1rem;
		padding: 1rem 2rem 2rem;
	}

	aside,
	main {
		background: #0f1620;
		border: 1px solid #1f2937;
		border-radius: 12px;
		padding: 1rem;
		min-height: 0;
	}

	aside h2,
	main h2,
	main h3 {
		margin: 0 0 0.75rem;
	}

	aside ul,
	main ul {
		list-style: none;
		padding: 0;
		margin: 0;
	}

	aside li {
		margin-bottom: 0.5rem;
	}

	aside li button {
		width: 100%;
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
		align-items: flex-start;
		padding: 0.6rem;
		border-radius: 8px;
		border: 1px solid transparent;
		background: #111827;
		color: inherit;
		cursor: pointer;
	}

	aside li.selected button {
		border-color: #38bdf8;
		background: rgba(56, 189, 248, 0.1);
	}

	aside .name {
		font-weight: 600;
	}

	aside .meta {
		color: #94a3b8;
		font-size: 0.8rem;
	}

	.viewer-header {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		gap: 1rem;
	}

	.viewer-header .path {
		color: #94a3b8;
		font-size: 0.85rem;
		margin: 0.25rem 0;
		word-break: break-all;
	}

	.viewer-header .meta {
		display: flex;
		gap: 1rem;
		color: #94a3b8;
		font-size: 0.8rem;
	}

	.viewer-header .open {
		padding: 0.5rem 0.8rem;
		border-radius: 8px;
		border: 1px solid #1f2937;
		background: #0b1220;
		color: #e2e8f0;
		text-decoration: none;
	}

	.viewer-body {
		margin: 1rem 0;
		height: 55vh;
		border-radius: 10px;
		overflow: hidden;
		border: 1px solid #1f2937;
	}

	iframe {
		width: 100%;
		height: 100%;
		border: none;
		background: #0b0f14;
	}

	.versions ul {
		display: grid;
		gap: 0.5rem;
	}

	.versions li {
		display: grid;
		grid-template-columns: 1fr auto auto;
		gap: 0.5rem;
		padding: 0.5rem;
		border-radius: 8px;
		background: #111827;
		font-size: 0.85rem;
	}

	.templates ul {
		display: grid;
		gap: 0.75rem;
	}

	.templates li {
		display: flex;
		justify-content: space-between;
		gap: 0.75rem;
		padding: 0.6rem;
		border-radius: 10px;
		background: #111827;
		align-items: center;
	}

	.templates button {
		border: none;
		border-radius: 8px;
		padding: 0.45rem 0.75rem;
		background: #22c55e;
		color: #0b0f14;
		cursor: pointer;
	}

	.templates small {
		color: #94a3b8;
		display: block;
		font-size: 0.7rem;
	}

	.empty {
		height: 100%;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		text-align: center;
		color: #94a3b8;
	}

	@media (max-width: 1200px) {
		.content {
			grid-template-columns: 1fr;
		}

		aside,
		main {
			min-height: auto;
		}
	}
</style>
