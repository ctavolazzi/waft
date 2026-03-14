import axios from 'axios';
import type { ProjectState } from '$lib/stores/projectStore';
import { browser } from '$app/environment';

export interface Dashboard5050Artifact {
	type: string;
	path: string;
	name: string;
	timestamp: string;
	size_bytes: number;
}

export interface Dashboard5050SessionResponse {
	timestamp: string;
	state: ProjectState;
	latest_work_effort_5050: string | null;
	canonical_ui_work_effort: string | null;
	artifacts: Dashboard5050Artifact[];
	summary: {
		uncommitted_files: number;
		integrity: number;
		work_efforts: number;
	};
}

export interface Dashboard5050TimelineResponse {
	total: number;
	events: Dashboard5050Artifact[];
}

// Use relative paths to go through Vite proxy (configured in vite.config.js)
// The proxy forwards /api requests to http://localhost:8000
const API_BASE_URL = import.meta.env.VITE_API_URL || '';

// Token storage key
const TOKEN_STORAGE_KEY = 'waft_api_token';

// Get token from localStorage
function getToken(): string | null {
	if (!browser) return null;
	return localStorage.getItem(TOKEN_STORAGE_KEY);
}

// Store token in localStorage
function setToken(token: string): void {
	if (!browser) return;
	localStorage.setItem(TOKEN_STORAGE_KEY, token);
}

// Remove token from localStorage
function clearToken(): void {
	if (!browser) return;
	localStorage.removeItem(TOKEN_STORAGE_KEY);
}

const client = axios.create({
	baseURL: API_BASE_URL, // Empty string = relative paths, uses Vite proxy
	timeout: 10000,
	headers: {
		'Content-Type': 'application/json'
	}
});

// Add token to requests if available
client.interceptors.request.use((config) => {
	const token = getToken();
	if (token) {
		config.headers.Authorization = `Bearer ${token}`;
	}
	return config;
});

// Handle 401 errors (unauthorized)
client.interceptors.response.use(
	(response) => response,
	(error) => {
		if (error.response?.status === 401) {
			clearToken();
			// Could dispatch an event here to notify the app
		}
		return Promise.reject(error);
	}
);

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
	},

	/**
	 * Gym/RPG API methods
	 */
	async getBattleLogs(limit: number = 20) {
		const response = await client.get(`/api/gym/battle-logs?limit=${limit}`);
		return response.data;
	},

	async getGymStats() {
		const response = await client.get('/api/gym/stats');
		return response.data;
	},

	/**
	 * Cartographer API methods
	 */
	async getCartographerData() {
		const response = await client.get('/api/cartographer');
		return response.data;
	},

	/**
	 * Authentication methods
	 */
	async handshake(clientName?: string, clientVersion?: string) {
		const response = await client.post('/api/auth/handshake', {
			client_name: clientName || 'WAFT Visualizer',
			client_version: clientVersion || '0.1.0'
		});
		const token = response.data.token;
		if (token) {
			setToken(token);
		}
		return response.data;
	},

	async verifyToken() {
		const response = await client.get('/api/auth/verify');
		return response.data;
	},

	async getAuthInfo() {
		const response = await client.get('/api/auth/info');
		return response.data;
	},

	/**
	 * Projects CRUD methods
	 */
	async getProjects() {
		const response = await client.get('/api/projects');
		return response.data;
	},

	async getProject(projectId: string) {
		const response = await client.get(`/api/projects/${projectId}`);
		return response.data;
	},

	async getProjectsStats() {
		const response = await client.get('/api/projects/stats');
		return response.data;
	},

	/**
	 * Work Efforts CRUD methods
	 */
	async getWorkEfforts() {
		const response = await client.get('/api/work-efforts');
		return response.data;
	},

	/**
	 * Evolve UI Monitor API methods
	 */
	async getEvolveUIRuns() {
		const response = await client.get('/api/evolve-ui-runs');
		return response.data;
	},

	/**
	 * Unified control center / 5050 API methods
	 */
	async get5050Session(): Promise<Dashboard5050SessionResponse> {
		const response = await client.get<Dashboard5050SessionResponse>('/api/5050/session');
		return response.data;
	},

	async get5050Timeline(): Promise<Dashboard5050TimelineResponse> {
		const response = await client.get<Dashboard5050TimelineResponse>('/api/5050/timeline');
		return response.data;
	},

	/**
	 * Generic GET method for custom endpoints
	 */
	async get(endpoint: string) {
		const response = await client.get(endpoint);
		return response.data;
	},

	/**
	 * Utility methods
	 */
	getToken() {
		return getToken();
	},

	clearToken() {
		clearToken();
	}
};
