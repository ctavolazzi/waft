import { writable } from 'svelte/store';
import { apiClient } from '$lib/api/client';

export interface ProjectState {
	timestamp: string;
	project_path: string;
	project: {
		name: string;
		version: string;
		description: string;
	};
	git: {
		initialized: boolean;
		branch: string | null;
		remote_url: string | null;
		uncommitted_files: string[];
		staged_files: string[];
		modified_files: string[];
		untracked_files: string[];
		commits_ahead: number;
		commits_behind: number;
		recent_commits: Array<{
			hash: string;
			message: string;
			author: string;
			relative: string;
		}>;
	};
	pyrite: {
		valid: boolean;
		folders: Record<string, boolean>;
		active_files: string[];
		backlog_files: string[];
		standards_files: string[];
	};
	gamification: {
		integrity: number;
		insight: number;
		level: number;
		insight_to_next: number;
	};
	system: {
		date_time: string;
		working_directory: string;
		python_version: string;
		platform: string;
	};
	work_efforts: Array<{
		id: string;
		path: string;
		has_index: boolean;
	}>;
	devlog: string[];
}

function createProjectStore() {
	const { subscribe, set, update } = writable<{ state: ProjectState | null; loading: boolean; error: string | null }>({
		state: null,
		loading: false,
		error: null
	});

	return {
		subscribe,
		fetch: async () => {
			update((store) => ({ ...store, loading: true, error: null }));
			try {
				console.log('[projectStore] Fetching state from API...');
				const state = await apiClient.getState();
				console.log('[projectStore] State received:', state);
				set({ state, loading: false, error: null });
			} catch (error) {
				console.error('[projectStore] Error fetching state:', error);
				set({
					state: null,
					loading: false,
					error: error instanceof Error ? error.message : 'Failed to fetch project state'
				});
			}
		}
	};
}

export const projectStore = createProjectStore();
