<script lang="ts">
	import { onMount } from 'svelte';

	type OddNote = {
		id: string;
		title: string;
		summary: string;
		content: string;
		tags: string[];
		sources: string[];
		created_at: string;
	};

	const apiUrl = 'http://localhost:8000/api/odd/notes';
	const oddRootUrl = 'http://localhost:6660/';
	const oddGalleryUrl = 'http://localhost:6660/gallery';

	const sourceAnchors = [
		{
			label: 'scienceicons',
			url: 'https://typst.app/universe/package/scienceicons'
		},
		{
			label: 'typst/packages',
			url: 'https://github.com/typst/packages'
		},
		{
			label: 'may template',
			url: 'https://typst.app/universe/package/may/'
		},
		{
			label: 'bookly template',
			url: 'https://typst.app/universe/package/bookly/'
		},
		{
			label: 'owlbear template',
			url: 'https://typst.app/universe/package/owlbear/'
		},
		{
			label: 'Making a template',
			url: 'https://typst.app/docs/tutorial/making-a-template/'
		}
	];

	let notes: OddNote[] = [];
	let loading = true;
	let error: string | null = null;

	let title = '';
	let summary = '';
	let content = '';
	let tagsInput = '';
	let sourcesInput = '';

	const parseList = (value: string) =>
		value
			.split(/[,\n]/)
			.map((item) => item.trim())
			.filter(Boolean);

	const loadNotes = async () => {
		loading = true;
		error = null;
		try {
			const response = await fetch(apiUrl);
			if (!response.ok) {
				throw new Error(`Fetch failed (${response.status})`);
			}
			const data = await response.json();
			notes = data.notes ?? [];
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to load notes';
		} finally {
			loading = false;
		}
	};

	const submitNote = async () => {
		if (!title.trim()) {
			error = 'Title is required.';
			return;
		}
		error = null;
		try {
			const response = await fetch(apiUrl, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					title: title.trim(),
					summary: summary.trim(),
					content: content.trim(),
					tags: parseList(tagsInput),
					sources: parseList(sourcesInput)
				})
			});
			if (!response.ok) {
				throw new Error(`Save failed (${response.status})`);
			}
			await loadNotes();
			title = '';
			summary = '';
			content = '';
			tagsInput = '';
			sourcesInput = '';
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to save note';
		}
	};

	onMount(loadNotes);
</script>

<div class="odd-notes">
	<div class="scanlines"></div>
	<div class="container">
		<header class="header">
			<div class="logo">O D D</div>
			<div class="header-emblems">
				<img
					src="http://localhost:6660/assets/odd_department_seal.png"
					alt="ODD Seal"
					class="header-seal"
				/>
				<div class="header-text">
					<h1>RESEARCH NOTES</h1>
					<p class="subtitle">Ontological Determinism Department • Research Annex</p>
				</div>
				<img
					src="http://localhost:6660/assets/odd_skull_logo.png"
					alt="ODD Skull"
					class="header-skull"
				/>
			</div>
			<div class="nav-links">
				<a href={oddRootUrl} target="_blank" rel="noreferrer">ODD CORE</a>
				<a href={oddGalleryUrl} target="_blank" rel="noreferrer">ASSET GALLERY</a>
				<a href="/" class="secondary">WAFT DASHBOARD</a>
			</div>
		</header>

		<section class="panel">
			<h2>SCIENCE ANCHORS</h2>
			<p class="muted">
				Reference anchors for Typst research workflows, template strategy, and iconography.
			</p>
			<ul class="anchor-list">
				{#each sourceAnchors as anchor}
					<li>
						<a href={anchor.url} target="_blank" rel="noreferrer">{anchor.label}</a>
					</li>
				{/each}
			</ul>
		</section>

		<section class="panel">
			<h2>RESEARCH NOTES</h2>
			{#if loading}
				<p class="muted">Loading notes...</p>
			{:else if error}
				<p class="error">{error}</p>
			{:else if notes.length === 0}
				<p class="muted">No notes yet. Add the first record below.</p>
			{:else}
				<div class="notes-grid">
					{#each notes as note}
						<article class="note-card">
							<header>
								<h3>{note.title}</h3>
								<span class="timestamp">{new Date(note.created_at).toLocaleString()}</span>
							</header>
							{#if note.summary}
								<p>{note.summary}</p>
							{/if}
							{#if note.content}
								<pre>{note.content}</pre>
							{/if}
							{#if note.tags?.length}
								<div class="tags">
									{#each note.tags as tag}
										<span class="tag">{tag}</span>
									{/each}
								</div>
							{/if}
							{#if note.sources?.length}
								<ul class="sources">
									{#each note.sources as source}
										<li>
											<a href={source} target="_blank" rel="noreferrer">{source}</a>
										</li>
									{/each}
								</ul>
							{/if}
						</article>
					{/each}
				</div>
			{/if}
		</section>

		<section class="panel">
			<h2>LOG NEW NOTE</h2>
			<div class="form-grid">
				<label>
					<span>Title</span>
					<input bind:value={title} placeholder="Note title" />
				</label>
				<label>
					<span>Summary</span>
					<input bind:value={summary} placeholder="Short summary" />
				</label>
				<label class="full">
					<span>Content</span>
					<textarea bind:value={content} rows="5" placeholder="Detailed research notes"></textarea>
				</label>
				<label>
					<span>Tags</span>
					<input bind:value={tagsInput} placeholder="odd, research, typst" />
				</label>
				<label>
					<span>Sources</span>
					<input bind:value={sourcesInput} placeholder="Paste URLs, comma or newline separated" />
				</label>
			</div>
			<button class="submit" on:click={submitNote}>Save Note</button>
		</section>
	</div>
</div>

<style>
	:global(body) {
		background: #0a0a0f;
		color: #e0e0e0;
		font-family: 'Courier New', monospace;
	}

	.odd-notes {
		position: relative;
		min-height: 100vh;
		background: #0a0a0f;
		padding-bottom: 4rem;
	}

	.scanlines {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		pointer-events: none;
		background: repeating-linear-gradient(
			0deg,
			rgba(0, 0, 0, 0.12) 0px,
			rgba(0, 0, 0, 0.12) 1px,
			transparent 1px,
			transparent 2px
		);
		z-index: 1;
	}

	.container {
		position: relative;
		z-index: 2;
		max-width: 1100px;
		margin: 0 auto;
		padding: 2rem;
	}

	.header {
		text-align: center;
		padding: 2.5rem 0;
		border-bottom: 1px solid rgba(123, 104, 238, 0.3);
		margin-bottom: 2rem;
	}

	.logo {
		font-size: 0.8rem;
		color: #7b68ee;
		letter-spacing: 0.5em;
		margin-bottom: 1rem;
	}

	.header-emblems {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 2rem;
		margin-bottom: 1rem;
		flex-wrap: wrap;
	}

	.header-seal,
	.header-skull {
		width: 70px;
		height: 70px;
		image-rendering: pixelated;
		filter: drop-shadow(0 0 10px rgba(123, 104, 238, 0.3));
	}

	h1 {
		font-size: 2.2rem;
		font-weight: normal;
		letter-spacing: 0.2em;
	}

	.subtitle {
		color: #888;
		font-size: 0.9rem;
	}

	.nav-links {
		display: flex;
		gap: 1rem;
		justify-content: center;
		flex-wrap: wrap;
		margin-top: 1.5rem;
	}

	.nav-links a {
		border: 1px solid #7b68ee;
		color: #7b68ee;
		padding: 0.5rem 1rem;
		text-decoration: none;
		font-size: 0.85rem;
		transition: all 0.2s ease;
	}

	.nav-links a.secondary {
		border-color: #2a2a3a;
		color: #aaa;
	}

	.nav-links a:hover {
		background: #7b68ee;
		color: #0a0a0f;
	}

	.panel {
		background: #12121a;
		border: 1px solid #2a2a3a;
		padding: 2rem;
		margin-bottom: 2rem;
	}

	h2 {
		margin-bottom: 0.75rem;
		letter-spacing: 0.12em;
		font-size: 1.1rem;
	}

	.muted {
		color: #888;
		font-size: 0.9rem;
	}

	.error {
		color: #ff7b7b;
	}

	.anchor-list {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
		gap: 0.75rem;
		margin-top: 1rem;
	}

	.anchor-list a {
		color: #7b68ee;
		text-decoration: none;
	}

	.notes-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 1.5rem;
		margin-top: 1.5rem;
	}

	.note-card {
		background: rgba(0, 0, 0, 0.3);
		border: 1px dashed #2a2a3a;
		padding: 1.5rem;
	}

	.note-card header {
		display: flex;
		justify-content: space-between;
		gap: 1rem;
		margin-bottom: 0.75rem;
		flex-wrap: wrap;
	}

	.note-card h3 {
		font-size: 1rem;
		font-weight: normal;
		letter-spacing: 0.08em;
	}

	.timestamp {
		color: #888;
		font-size: 0.75rem;
	}

	.note-card pre {
		white-space: pre-wrap;
		font-family: inherit;
		font-size: 0.85rem;
		background: rgba(123, 104, 238, 0.08);
		padding: 0.75rem;
		margin-top: 0.75rem;
		border-left: 2px solid #7b68ee;
	}

	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		margin-top: 0.75rem;
	}

	.tag {
		border: 1px solid #7b68ee;
		color: #7b68ee;
		padding: 0.1rem 0.5rem;
		font-size: 0.7rem;
	}

	.sources {
		margin-top: 0.75rem;
		font-size: 0.75rem;
		color: #aaa;
	}

	.sources a {
		color: #aaa;
	}

	.form-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
		gap: 1rem;
		margin-top: 1rem;
	}

	.form-grid label {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		font-size: 0.85rem;
	}

	.form-grid label.full {
		grid-column: 1 / -1;
	}

	input,
	textarea {
		background: #0a0a0f;
		border: 1px solid #2a2a3a;
		color: #e0e0e0;
		padding: 0.5rem;
		font-family: inherit;
	}

	.submit {
		margin-top: 1.5rem;
		background: transparent;
		border: 1px solid #7b68ee;
		color: #7b68ee;
		padding: 0.75rem 1.5rem;
		font-family: inherit;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.submit:hover {
		background: #7b68ee;
		color: #0a0a0f;
	}
</style>
