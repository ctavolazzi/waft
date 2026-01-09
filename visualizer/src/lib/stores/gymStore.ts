import { writable } from 'svelte/store';
import { apiClient } from '$lib/api/client';

export interface BattleLog {
	quest_name: string;
	timestamp: string;
	hero_name: string;
	input_prompt: string;
	agent_response: string;
	result: 'critical_hit' | 'hit' | 'miss' | 'stabilized';
	success: boolean;
	error_message?: string;
	xp_gained: number;
	// Scint & Stabilization data
	scints_detected?: string[];
	max_severity?: number;
	stabilization_attempted: boolean;
	stabilization_successful: boolean;
	stabilization_attempts: number;
	corrected_response?: string;
	original_response?: string;
	agent_call_count: number;
	validated_matrix?: any;
}

export interface GymStats {
	total_quests: number;
	successful_quests: number;
	stabilized_quests: number;
	scints_detected: number;
	scint_types: Record<string, number>;
	stabilization_success_rate: number;
	stabilization_attempts: number;
	average_severity: number;
	total_agent_calls: number;
}

function createGymStore() {
	const { subscribe, set, update } = writable<{
		battle_logs: BattleLog[];
		stats: GymStats | null;
		loading: boolean;
		error: string | null;
	}>({
		battle_logs: [],
		stats: null,
		loading: false,
		error: null
	});

	return {
		subscribe,
		fetch: async (limit: number = 20) => {
			update((store) => ({ ...store, loading: true, error: null }));
			try {
				console.log('[gymStore] Fetching battle logs and stats...');
				const [battleLogsResponse, statsResponse] = await Promise.all([
					apiClient.getBattleLogs(limit),
					apiClient.getGymStats()
				]);
				console.log('[gymStore] Data received:', { battleLogsResponse, statsResponse });
				set({
					battle_logs: battleLogsResponse.battle_logs || [],
					stats: statsResponse,
					loading: false,
					error: null
				});
			} catch (error) {
				console.error('[gymStore] Error fetching gym data:', error);
				set({
					battle_logs: [],
					stats: null,
					loading: false,
					error: error instanceof Error ? error.message : 'Failed to fetch gym data'
				});
			}
		}
	};
}

export const gymStore = createGymStore();
