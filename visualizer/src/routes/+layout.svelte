<script lang="ts">
	import { onMount } from 'svelte';
	import '../app.css';
	import AppShell from '$lib/components/layout/AppShell.svelte';
	import { authStore } from '$lib/stores/authStore';

	onMount(async () => {
		// Check for stored token first
		authStore.checkStoredToken();

		// If no token or token invalid, perform handshake
		const unsubscribe = authStore.subscribe((state) => {
			if (!state.handshakeComplete && !state.error) {
				authStore.performHandshake().catch((err) => {
					console.error('Handshake failed:', err);
				});
			}
		});

		// Cleanup subscription on unmount
		return () => {
			unsubscribe();
		};
	});
</script>

<AppShell>
	<slot />
</AppShell>
