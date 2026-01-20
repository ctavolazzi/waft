<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let code = '';

	const dispatch = createEventDispatcher<{ change: string }>();

	function handleInput(event: Event) {
		const target = event.target as HTMLTextAreaElement;
		dispatch('change', target.value);
	}
</script>

<div class="editor">
	<div class="line-numbers">
		{#each code.split('\n') as _, i}
			<span>{i + 1}</span>
		{/each}
	</div>
	<textarea
		value={code}
		on:input={handleInput}
		spellcheck="false"
		autocomplete="off"
		autocorrect="off"
		autocapitalize="off"
	/>
</div>

<style>
	.editor {
		display: flex;
		flex: 1;
		background: #1a1a2e;
		border-radius: 0.5rem;
		overflow: hidden;
		font-family: 'JetBrains Mono', 'Fira Code', 'Monaco', monospace;
		font-size: 0.875rem;
		line-height: 1.6;
	}

	.line-numbers {
		display: flex;
		flex-direction: column;
		padding: 1rem 0.75rem;
		background: rgba(0, 0, 0, 0.2);
		color: #4a5568;
		text-align: right;
		user-select: none;
		min-width: 3rem;
	}

	.line-numbers span {
		height: 1.6em;
	}

	textarea {
		flex: 1;
		padding: 1rem;
		background: transparent;
		color: #e2e8f0;
		border: none;
		outline: none;
		resize: none;
		font-family: inherit;
		font-size: inherit;
		line-height: inherit;
		white-space: pre;
		overflow: auto;
	}

	textarea::selection {
		background: rgba(99, 102, 241, 0.3);
	}
</style>
