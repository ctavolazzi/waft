<script>
	import '../app.css';
</script>

<div class="app">
	<header>
		<div class="logo">
			<span class="logo-icon">📄</span>
			<span class="logo-text">Typst Demo</span>
		</div>
		<nav>
			<a href="/">Home</a>
			<a href="https://typst.app" target="_blank" rel="noopener">Typst</a>
			<a href="https://github.com" target="_blank" rel="noopener">GitHub</a>
		</nav>
	</header>
	
	<main>
		<slot />
	</main>
	
	<footer>
		<p>Built with FastAPI + SvelteKit | Typst Packages Demo</p>
	</footer>
</div>

<style>
	.app {
		min-height: 100vh;
		display: flex;
		flex-direction: column;
	}

	header {
		background: var(--bg-card);
		padding: 1rem 2rem;
		display: flex;
		justify-content: space-between;
		align-items: center;
		border-bottom: 1px solid var(--border);
	}

	.logo {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		font-size: 1.5rem;
		font-weight: 700;
	}

	.logo-icon {
		font-size: 1.75rem;
	}

	nav {
		display: flex;
		gap: 1.5rem;
	}

	nav a {
		color: var(--text-muted);
		font-weight: 500;
		transition: color 0.2s;
	}

	nav a:hover {
		color: var(--primary);
		text-decoration: none;
	}

	main {
		flex: 1;
		padding: 2rem;
		max-width: 1400px;
		margin: 0 auto;
		width: 100%;
	}

	footer {
		background: var(--bg-card);
		padding: 1rem 2rem;
		text-align: center;
		color: var(--text-muted);
		border-top: 1px solid var(--border);
	}
</style>
