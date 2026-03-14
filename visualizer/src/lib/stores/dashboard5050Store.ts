import { writable } from 'svelte/store';
import {
	apiClient,
	type Dashboard5050Artifact,
	type Dashboard5050SessionResponse
} from '$lib/api/client';

interface Dashboard5050State {
	session: Dashboard5050SessionResponse | null;
	timeline: Dashboard5050Artifact[];
	loading: boolean;
	error: string | null;
}

function createDashboard5050Store() {
	const { subscribe, set, update } = writable<Dashboard5050State>({
		session: null,
		timeline: [],
		loading: false,
		error: null
	});

	return {
		subscribe,
		fetch: async () => {
			update((store) => ({ ...store, loading: true, error: null }));
			try {
				const [session, timeline] = await Promise.all([
					apiClient.get5050Session(),
					apiClient.get5050Timeline()
				]);
				set({
					session,
					timeline: timeline.events,
					loading: false,
					error: null
				});
			} catch (error) {
				set({
					session: null,
					timeline: [],
					loading: false,
					error: error instanceof Error ? error.message : 'Failed to fetch control center data'
				});
			}
		}
	};
}

export const dashboard5050Store = createDashboard5050Store();
