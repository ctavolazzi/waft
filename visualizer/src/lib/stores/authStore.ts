import { writable } from 'svelte/store';
import { apiClient } from '$lib/api/client';
import { browser } from '$app/environment';

interface AuthState {
	authenticated: boolean;
	token: string | null;
	handshakeComplete: boolean;
	error: string | null;
}

const initialState: AuthState = {
	authenticated: false,
	token: null,
	handshakeComplete: false,
	error: null
};

function createAuthStore() {
	const { subscribe, set, update } = writable<AuthState>(initialState);

	return {
		subscribe,

		async performHandshake() {
			try {
				const response = await apiClient.handshake('WAFT Visualizer', '0.1.0');
				update((state) => ({
					...state,
					authenticated: true,
					token: response.token,
					handshakeComplete: true,
					error: null
				}));
				return response;
			} catch (error) {
				const errorMessage = error instanceof Error ? error.message : 'Handshake failed';
				update((state) => ({
					...state,
					authenticated: false,
					token: null,
					handshakeComplete: false,
					error: errorMessage
				}));
				throw error;
			}
		},

		async verifyToken() {
			try {
				const response = await apiClient.verifyToken();
				update((state) => ({
					...state,
					authenticated: response.valid,
					error: response.valid ? null : 'Token invalid'
				}));
				return response.valid;
			} catch (error) {
				update((state) => ({
					...state,
					authenticated: false,
					error: error instanceof Error ? error.message : 'Verification failed'
				}));
				return false;
			}
		},

		checkStoredToken() {
			if (!browser) return;
			const token = apiClient.getToken();
			if (token) {
				update((state) => ({
					...state,
					token,
					authenticated: false, // Will be verified
					handshakeComplete: true
				}));
				// Auto-verify stored token
				this.verifyToken();
			}
		},

		clearAuth() {
			apiClient.clearToken();
			set(initialState);
		}
	};
}

export const authStore = createAuthStore();
