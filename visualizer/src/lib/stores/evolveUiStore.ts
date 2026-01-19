import { writable, derived } from 'svelte/store';
import { apiClient } from '$lib/api/client';

export interface EvolveUIRun {
	run_id: string;
	timestamp: string;
	phase: string;
	artifacts: {
		html: string[];
		context_analysis?: string;
		design_doc?: string;
		requirements?: string;
		wireframe?: string;
		screenshots: string[];
		case_files: string[];
	};
	context?: string;
}

interface EvolveUIState {
	runs: EvolveUIRun[];
	loading: boolean;
	error: string | null;
	lastFetch: Date | null;
	selectedRunId: string | null;
}

const initialState: EvolveUIState = {
	runs: [],
	loading: false,
	error: null,
	lastFetch: null,
	selectedRunId: null
};

function createEvolveUIStore() {
	const { subscribe, set, update } = writable<EvolveUIState>(initialState);

	return {
		subscribe,
		
		async fetch() {
			update(state => ({ ...state, loading: true, error: null }));
			
			try {
				const data = await apiClient.getEvolveUIRuns();
				update(state => ({
					...state,
					runs: data.runs || [],
					loading: false,
					error: null,
					lastFetch: new Date()
				}));
			} catch (error) {
				const errorMessage = error instanceof Error ? error.message : 'Failed to load evolve UI runs';
				update(state => ({
					...state,
					loading: false,
					error: errorMessage
				}));
				console.error('Error fetching evolve UI runs:', error);
			}
		},
		
		selectRun(runId: string | null) {
			update(state => ({ ...state, selectedRunId: runId }));
		},
		
		reset() {
			set(initialState);
		}
	};
}

export const evolveUiStore = createEvolveUIStore();

export const selectedRun = derived(evolveUiStore, ($store) => {
	if (!$store.selectedRunId) return null;
	return $store.runs.find(run => run.run_id === $store.selectedRunId) || null;
});