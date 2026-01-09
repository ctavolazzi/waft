<script lang="ts">
	import Navbar from './Navbar.svelte';
	import Footer from './Footer.svelte';
</script>

<div class="min-h-screen flex flex-col">
	<Navbar />
	<main class="flex-1">
		<slot />
	</main>
	<Footer />
</div>
