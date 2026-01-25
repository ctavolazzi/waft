<script lang="ts">
	import Navbar from './Navbar.svelte';
	import Footer from './Footer.svelte';
	import CosmicBackground from '../CosmicBackground.svelte';
</script>

<div class="app-shell min-h-screen flex flex-col">
	<CosmicBackground />
	<Navbar />
	<main class="flex-1 relative z-10">
		<slot />
	</main>
	<Footer />
</div>

<style>
	.app-shell {
		position: relative;
	}
</style>
