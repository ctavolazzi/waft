import type { BiomeServerPayload, BridgeSettings } from './types';

type PayloadHandler = (payload: BiomeServerPayload) => void;
type ErrorHandler = (error: string) => void;

export class BiomeBridge {
	private pollTimer: ReturnType<typeof setInterval> | null = null;
	private source: EventSource | null = null;
	private running = false;

	constructor(
		private onPayload: PayloadHandler,
		private onError: ErrorHandler
	) {}

	async start(settings: BridgeSettings): Promise<void> {
		this.stop();
		this.running = true;

		if (!settings.enabled) return;
		if (settings.mode === 'sse') {
			this.startSse(settings);
			return;
		}
		await this.startPolling(settings);
	}

	stop(): void {
		this.running = false;
		if (this.pollTimer) {
			clearInterval(this.pollTimer);
			this.pollTimer = null;
		}
		if (this.source) {
			this.source.close();
			this.source = null;
		}
	}

	private async startPolling(settings: BridgeSettings): Promise<void> {
		const fetchOnce = async () => {
			try {
				const response = await fetch(settings.url);
				if (!response.ok) throw new Error(`HTTP ${response.status}`);
				const payload = (await response.json()) as BiomeServerPayload;
				this.onPayload(payload);
			} catch (error) {
				const message = error instanceof Error ? error.message : 'Unknown polling error';
				this.onError(message);
			}
		};

		await fetchOnce();
		if (!this.running) return;
		this.pollTimer = setInterval(fetchOnce, settings.pollMs);
	}

	private startSse(settings: BridgeSettings): void {
		try {
			this.source = new EventSource(settings.url);
			this.source.onmessage = (event) => {
				try {
					this.onPayload(JSON.parse(event.data) as BiomeServerPayload);
				} catch (error) {
					const message = error instanceof Error ? error.message : 'Invalid SSE payload';
					this.onError(message);
				}
			};
			this.source.onerror = () => this.onError('SSE connection error');
		} catch (error) {
			const message = error instanceof Error ? error.message : 'Unable to start SSE bridge';
			this.onError(message);
		}
	}
}
