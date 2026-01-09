import axios from 'axios';
import type { ProjectState } from '$lib/stores/projectStore';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const client = axios.create({
	baseURL: API_BASE_URL,
	timeout: 10000,
	headers: {
		'Content-Type': 'application/json'
	}
});

export const apiClient = {
	async getHealth() {
		const response = await client.get('/api/health');
		return response.data;
	},

	async getState(): Promise<ProjectState> {
		console.log('[apiClient] Fetching /api/state from', client.defaults.baseURL);
		const response = await client.get<ProjectState>('/api/state');
		console.log('[apiClient] Response received:', response.data);
		return response.data;
	},

	async getGitStatus() {
		const response = await client.get('/api/git');
		return response.data;
	},

	async getWorkEfforts() {
		const response = await client.get('/api/work-efforts');
		return response.data;
	},

	async getEmpirica() {
		const response = await client.get('/api/empirica');
		return response.data;
	},

	/**
	 * Decision Engine API methods
	 */
	async analyzeDecision(request: {
		problem: string;
		alternatives: (string | { name: string; description?: string })[];
		criteria: Record<string, number | { weight: number; description?: string }>;
		scores: Record<string, Record<string, number>>;
		methodology?: string;
		show_details?: boolean;
		show_sensitivity?: boolean;
	}) {
		const response = await client.post('/api/decision/analyze', request);
		return response.data;
	},

	async getDecisionHealth() {
		const response = await client.get('/api/decision/health');
		return response.data;
	}
};
