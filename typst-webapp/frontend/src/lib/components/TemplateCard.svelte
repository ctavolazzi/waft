<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let id: string;
	export let name: string;
	export let description: string;
	export let packageName: string;
	export let version: string;
	export let url: string;
	export let selected = false;

	const dispatch = createEventDispatcher();

	function handleSelect() {
		dispatch('select', id);
	}
</script>

<button
	class="card"
	class:selected
	on:click={handleSelect}
>
	<div class="card-header">
		<h3>{name}</h3>
		<span class="version">v{version}</span>
	</div>
	<p class="description">{description}</p>
	<div class="card-footer">
		<span class="package">📦 {packageName}</span>
		<a href={url} target="_blank" rel="noopener" on:click|stopPropagation>
			View Package →
		</a>
	</div>
</button>

<style>
	.card {
		background: var(--bg-card);
		border: 2px solid var(--border);
		border-radius: 0.75rem;
		padding: 1.25rem;
		text-align: left;
		transition: all 0.2s;
		width: 100%;
	}

	.card:hover {
		border-color: var(--primary);
		transform: translateY(-2px);
	}

	.card.selected {
		border-color: var(--primary);
		background: rgba(99, 102, 241, 0.1);
	}

	.card-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 0.5rem;
	}

	.card-header h3 {
		font-size: 1.1rem;
		color: var(--text);
	}

	.version {
		background: var(--primary);
		color: white;
		padding: 0.25rem 0.5rem;
		border-radius: 0.25rem;
		font-size: 0.75rem;
		font-weight: 600;
	}

	.description {
		color: var(--text-muted);
		font-size: 0.9rem;
		margin-bottom: 1rem;
		line-height: 1.5;
	}

	.card-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 0.85rem;
	}

	.package {
		color: var(--text-muted);
	}

	.card-footer a {
		color: var(--primary);
		font-weight: 500;
	}
</style>
