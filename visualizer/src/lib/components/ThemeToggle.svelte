<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';

	export let size: 'sm' | 'md' | 'lg' = 'md';

	type Theme = 'dark' | 'light';
	const theme = writable<Theme>('dark');

	const sizes = {
		sm: { width: 40, height: 20, icon: 12 },
		md: { width: 56, height: 28, icon: 16 },
		lg: { width: 72, height: 36, icon: 20 },
	};

	$: dimensions = sizes[size];

	function toggleTheme() {
		theme.update((t) => {
			const newTheme = t === 'dark' ? 'light' : 'dark';
			document.documentElement.setAttribute('data-theme', newTheme);
			localStorage.setItem('theme', newTheme);
			return newTheme;
		});
	}

	onMount(() => {
		// Check for saved preference
		const saved = localStorage.getItem('theme') as Theme | null;
		const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
		const initialTheme = saved || (prefersDark ? 'dark' : 'light');

		theme.set(initialTheme);
		document.documentElement.setAttribute('data-theme', initialTheme);
	});
</script>

<button
	class="theme-toggle"
	on:click={toggleTheme}
	style="
		--width: {dimensions.width}px;
		--height: {dimensions.height}px;
		--icon-size: {dimensions.icon}px;
	"
	aria-label="Toggle theme"
	title={$theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
>
	<span class="toggle-track" class:light={$theme === 'light'}>
		<span class="toggle-thumb" class:light={$theme === 'light'}>
			{#if $theme === 'dark'}
				<svg
					class="icon"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
				>
					<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
				</svg>
			{:else}
				<svg
					class="icon"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
				>
					<circle cx="12" cy="12" r="5" />
					<line x1="12" y1="1" x2="12" y2="3" />
					<line x1="12" y1="21" x2="12" y2="23" />
					<line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
					<line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
					<line x1="1" y1="12" x2="3" y2="12" />
					<line x1="21" y1="12" x2="23" y2="12" />
					<line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
					<line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
				</svg>
			{/if}
		</span>

		<!-- Stars in dark mode -->
		{#if $theme === 'dark'}
			<span class="stars">
				<span class="star" style="top: 4px; left: 8px; animation-delay: 0s;"></span>
				<span class="star" style="top: 12px; left: 4px; animation-delay: 0.3s;"></span>
				<span class="star" style="top: 8px; left: 14px; animation-delay: 0.6s;"></span>
			</span>
		{/if}

		<!-- Clouds in light mode -->
		{#if $theme === 'light'}
			<span class="clouds">
				<span class="cloud" style="right: 8px; top: 6px;"></span>
				<span class="cloud" style="right: 4px; top: 14px; transform: scale(0.7);"></span>
			</span>
		{/if}
	</span>
</button>

<style>
	.theme-toggle {
		background: none;
		border: none;
		padding: 0;
		cursor: pointer;
		outline: none;
	}

	.theme-toggle:focus-visible {
		outline: 2px solid var(--primary);
		outline-offset: 2px;
		border-radius: calc(var(--height) / 2);
	}

	.toggle-track {
		display: flex;
		align-items: center;
		width: var(--width);
		height: var(--height);
		background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
		border-radius: calc(var(--height) / 2);
		padding: 2px;
		transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
		position: relative;
		overflow: hidden;
		box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
	}

	.toggle-track.light {
		background: linear-gradient(135deg, #87ceeb 0%, #b0e0e6 50%, #e0f7fa 100%);
	}

	.toggle-thumb {
		display: flex;
		align-items: center;
		justify-content: center;
		width: calc(var(--height) - 4px);
		height: calc(var(--height) - 4px);
		background: linear-gradient(135deg, #f0f0f0 0%, #ffffff 100%);
		border-radius: 50%;
		transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
		z-index: 2;
	}

	.toggle-thumb.light {
		transform: translateX(calc(var(--width) - var(--height)));
		background: linear-gradient(135deg, #ffd700 0%, #ffa500 100%);
		box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
	}

	.icon {
		width: var(--icon-size);
		height: var(--icon-size);
		color: #333;
		transition: all 0.3s ease;
	}

	.toggle-thumb.light .icon {
		color: #fff;
	}

	/* Stars */
	.stars {
		position: absolute;
		inset: 0;
		pointer-events: none;
	}

	.star {
		position: absolute;
		width: 3px;
		height: 3px;
		background: white;
		border-radius: 50%;
		animation: twinkle 1.5s ease-in-out infinite;
	}

	@keyframes twinkle {
		0%, 100% {
			opacity: 0.3;
			transform: scale(0.8);
		}
		50% {
			opacity: 1;
			transform: scale(1);
		}
	}

	/* Clouds */
	.clouds {
		position: absolute;
		inset: 0;
		pointer-events: none;
	}

	.cloud {
		position: absolute;
		width: 12px;
		height: 6px;
		background: white;
		border-radius: 10px;
		opacity: 0.8;
	}

	.cloud::before,
	.cloud::after {
		content: '';
		position: absolute;
		background: white;
		border-radius: 50%;
	}

	.cloud::before {
		width: 6px;
		height: 6px;
		top: -3px;
		left: 2px;
	}

	.cloud::after {
		width: 5px;
		height: 5px;
		top: -2px;
		left: 6px;
	}
</style>
