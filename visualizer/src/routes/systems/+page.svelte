<script lang="ts">
	import { onMount, onDestroy } from 'svelte';

	type SystemStatus = 'running' | 'stopped' | 'checking';

	interface System {
		name: string;
		icon: string;
		port: number;
		healthUrl: string;
		description: string;
		color: string;
		glow: string;
		links: { label: string; url: string }[];
	}

	const SYSTEMS: System[] = [
		{
			name: 'Waft API',
			icon: '🌊',
			port: 8000,
			healthUrl: 'http://localhost:8000/api/health',
			description: 'Evolutionary agent framework — Python FastAPI backend',
			color: '#7c9eff',
			glow: 'rgba(124, 158, 255, 0.4)',
			links: [
				{ label: 'API Docs', url: 'http://localhost:8000/docs' },
				{ label: 'Health', url: 'http://localhost:8000/api/health' }
			]
		},
		{
			name: 'SimpleAgentOS',
			icon: '🤖',
			port: 1010,
			healthUrl: 'http://localhost:1010/api/health',
			description: 'Self-reflective AI — Gemma4 OODA loop with SSE streaming',
			color: '#4ade80',
			glow: 'rgba(74, 222, 128, 0.4)',
			links: [
				{ label: 'Dashboard', url: 'http://localhost:1010' },
				{ label: 'Stream', url: 'http://localhost:1010/api/explorer/stream' }
			]
		},
		{
			name: 'CivicOS',
			icon: '🏛️',
			port: 5050,
			healthUrl: 'http://localhost:5050',
			description: 'Civic infrastructure layer — Plaza, Builder, Vault modules',
			color: '#a855f7',
			glow: 'rgba(168, 85, 247, 0.4)',
			links: [{ label: 'App', url: 'http://localhost:5050' }]
		},
		{
			name: 'NovaSystem',
			icon: '🧠',
			port: 0,
			healthUrl: '',
			description: 'Multi-agent problem solver — Nova Process orchestration',
			color: '#fbbf24',
			glow: 'rgba(251, 191, 36, 0.4)',
			links: []
		}
	];

	let statuses: Record<string, SystemStatus> = {};
	let sseLog: string[] = [];
	let sseConnection: EventSource | null = null;
	let sseConnected = false;
	let checkInterval: ReturnType<typeof setInterval> | null = null;

	SYSTEMS.forEach((s) => (statuses[s.name] = 'checking'));

	async function checkSystem(system: System): Promise<void> {
		if (!system.healthUrl) {
			statuses[system.name] = 'stopped';
			statuses = statuses;
			return;
		}
		try {
			const res = await fetch(system.healthUrl, {
				signal: AbortSignal.timeout(2000),
				mode: 'no-cors'
			});
			// no-cors always succeeds if server responds at all
			statuses[system.name] = 'running';
		} catch {
			statuses[system.name] = 'stopped';
		}
		statuses = statuses;
	}

	function checkAll() {
		SYSTEMS.forEach(checkSystem);
	}

	function connectSSE() {
		if (sseConnection) {
			sseConnection.close();
			sseConnection = null;
			sseConnected = false;
			return;
		}
		const es = new EventSource('http://localhost:1010/api/explorer/stream');
		es.onopen = () => {
			sseConnected = true;
		};
		es.onmessage = (e) => {
			const data = e.data;
			sseLog = [...sseLog.slice(-199), data];
		};
		es.onerror = () => {
			sseConnected = false;
			sseLog = [...sseLog, '[SSE disconnected]'];
		};
		sseConnection = es;
		sseConnected = true;
	}

	onMount(() => {
		checkAll();
		checkInterval = setInterval(checkAll, 8000);
	});

	onDestroy(() => {
		if (checkInterval) clearInterval(checkInterval);
		if (sseConnection) sseConnection.close();
	});
</script>

<div class="systems-page">
	<div class="page-header">
		<h1>🔗 Systems Hub</h1>
		<p class="subtitle">Unified control center — Waft · SimpleAgentOS · CivicOS · NovaSystem</p>
		<button class="refresh-btn" on:click={checkAll}>🔄 Re-check All</button>
	</div>

	<div class="systems-grid">
		{#each SYSTEMS as system}
			<div class="system-card" style="--sys-color: {system.color}; --sys-glow: {system.glow}">
				<div class="card-header">
					<span class="sys-icon">{system.icon}</span>
					<div class="sys-title">
						<h2>{system.name}</h2>
						{#if system.port}
							<span class="port-badge">:{system.port}</span>
						{:else}
							<span class="port-badge cli">CLI</span>
						{/if}
					</div>
					<div class="status-dot {statuses[system.name] ?? 'checking'}">
						{#if statuses[system.name] === 'running'}
							<span class="dot running" title="Running"></span>
						{:else if statuses[system.name] === 'stopped'}
							<span class="dot stopped" title="Stopped"></span>
						{:else}
							<span class="dot checking" title="Checking…"></span>
						{/if}
						<span class="status-label">{statuses[system.name] ?? 'checking'}</span>
					</div>
				</div>

				<p class="sys-desc">{system.description}</p>

				<div class="links-row">
					{#each system.links as link}
						<a href={link.url} target="_blank" rel="noopener" class="sys-link">
							{link.label} ↗
						</a>
					{/each}
					{#if system.name === 'SimpleAgentOS'}
						<button class="sys-link sse-btn" on:click={connectSSE}>
							{sseConnection ? '⏹ Disconnect SSE' : '📡 Connect SSE'}
						</button>
					{/if}
					{#if system.links.length === 0 && system.name !== 'SimpleAgentOS'}
						<span class="sys-link disabled">No HTTP interface</span>
					{/if}
				</div>

				{#if statuses[system.name] === 'stopped' && system.port}
					<div class="launch-hint">
						{#if system.name === 'SimpleAgentOS'}
							<code>cd SimpleAgentOS && ./run_self_explore.sh</code>
						{:else if system.name === 'CivicOS'}
							<code>cd CivicOS && npm run dev</code>
						{/if}
					</div>
				{/if}
			</div>
		{/each}
	</div>

	{#if sseLog.length > 0 || sseConnection}
		<div class="sse-panel">
			<div class="sse-header">
				<h2>📡 SimpleAgentOS — Live SSE Stream</h2>
				<span class="sse-status {sseConnected ? 'live' : 'dead'}">
					{sseConnected ? '● LIVE' : '○ DISCONNECTED'}
				</span>
			</div>
			<div class="sse-log">
				{#each sseLog as line}
					<div class="sse-line">{line}</div>
				{/each}
				{#if sseLog.length === 0}
					<div class="sse-line muted">Waiting for events…</div>
				{/if}
			</div>
		</div>
	{/if}
</div>

<style>
	.systems-page {
		padding: 2rem;
		max-width: 1400px;
		margin: 0 auto;
	}

	.page-header {
		margin-bottom: 2rem;
		display: flex;
		align-items: baseline;
		gap: 1.5rem;
		flex-wrap: wrap;
	}

	.page-header h1 {
		font-size: 2rem;
		font-weight: 700;
		color: var(--text-primary);
		margin: 0;
	}

	.subtitle {
		color: var(--text-secondary);
		font-size: 0.95rem;
		margin: 0;
		flex: 1;
	}

	.refresh-btn {
		padding: 0.5rem 1rem;
		background: var(--bg-card);
		border: 1px solid var(--border);
		border-radius: 6px;
		color: var(--text-primary);
		cursor: pointer;
		font-size: 0.875rem;
		transition: all 0.2s;
	}

	.refresh-btn:hover {
		border-color: var(--primary);
		color: var(--primary-light);
	}

	.systems-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
		gap: 1.5rem;
		margin-bottom: 2rem;
	}

	.system-card {
		background: var(--bg-card);
		border: 1px solid var(--border);
		border-radius: 16px;
		padding: 1.5rem;
		transition: all 0.25s;
		position: relative;
		overflow: hidden;
	}

	.system-card::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		height: 3px;
		background: var(--sys-color);
		box-shadow: 0 0 12px var(--sys-glow);
	}

	.system-card:hover {
		border-color: var(--sys-color);
		box-shadow: 0 0 20px var(--sys-glow);
		transform: translateY(-2px);
	}

	.card-header {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		margin-bottom: 0.75rem;
	}

	.sys-icon {
		font-size: 1.75rem;
	}

	.sys-title {
		flex: 1;
	}

	.sys-title h2 {
		margin: 0;
		font-size: 1.2rem;
		font-weight: 700;
		color: var(--text-primary);
		line-height: 1;
	}

	.port-badge {
		font-size: 0.75rem;
		color: var(--sys-color);
		font-family: monospace;
		font-weight: 600;
	}

	.port-badge.cli {
		color: var(--text-muted);
	}

	.status-dot {
		display: flex;
		align-items: center;
		gap: 0.4rem;
	}

	.dot {
		width: 10px;
		height: 10px;
		border-radius: 50%;
		display: inline-block;
	}

	.dot.running {
		background: var(--success);
		box-shadow: 0 0 8px var(--success);
		animation: pulse-green 2s infinite;
	}

	.dot.stopped {
		background: var(--error);
	}

	.dot.checking {
		background: var(--warning);
		animation: blink 1s infinite;
	}

	@keyframes pulse-green {
		0%, 100% { box-shadow: 0 0 6px var(--success); }
		50% { box-shadow: 0 0 14px var(--success); }
	}

	@keyframes blink {
		0%, 100% { opacity: 1; }
		50% { opacity: 0.3; }
	}

	.status-label {
		font-size: 0.75rem;
		color: var(--text-muted);
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.sys-desc {
		color: var(--text-secondary);
		font-size: 0.875rem;
		margin: 0 0 1rem;
		line-height: 1.5;
	}

	.links-row {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
	}

	.sys-link {
		display: inline-block;
		padding: 0.35rem 0.75rem;
		background: var(--bg-elevated);
		border: 1px solid var(--border);
		border-radius: 6px;
		color: var(--sys-color);
		text-decoration: none;
		font-size: 0.8rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s;
	}

	.sys-link:hover {
		background: var(--bg-card-hover);
		border-color: var(--sys-color);
		box-shadow: 0 0 8px var(--sys-glow);
	}

	.sys-link.disabled {
		color: var(--text-muted);
		cursor: default;
	}

	.sys-link.disabled:hover {
		background: var(--bg-elevated);
		border-color: var(--border);
		box-shadow: none;
	}

	.sse-btn {
		background: rgba(74, 222, 128, 0.1);
		border-color: rgba(74, 222, 128, 0.3);
		color: #4ade80;
	}

	.launch-hint {
		margin-top: 0.75rem;
		padding: 0.5rem 0.75rem;
		background: rgba(248, 113, 113, 0.08);
		border: 1px solid rgba(248, 113, 113, 0.2);
		border-radius: 6px;
	}

	.launch-hint code {
		font-size: 0.78rem;
		color: var(--error);
		font-family: monospace;
	}

	.sse-panel {
		background: var(--bg-card);
		border: 1px solid rgba(74, 222, 128, 0.3);
		border-radius: 16px;
		padding: 1.5rem;
	}

	.sse-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 1rem;
	}

	.sse-header h2 {
		margin: 0;
		font-size: 1.1rem;
		color: var(--text-primary);
	}

	.sse-status {
		font-size: 0.8rem;
		font-weight: 700;
		font-family: monospace;
		letter-spacing: 0.05em;
	}

	.sse-status.live {
		color: #4ade80;
		text-shadow: 0 0 8px rgba(74, 222, 128, 0.6);
	}

	.sse-status.dead {
		color: var(--text-muted);
	}

	.sse-log {
		background: var(--bg-darker);
		border-radius: 8px;
		padding: 1rem;
		max-height: 400px;
		overflow-y: auto;
		font-family: monospace;
		font-size: 0.8rem;
	}

	.sse-line {
		color: #4ade80;
		line-height: 1.6;
		word-break: break-all;
		padding: 0.1rem 0;
	}

	.sse-line.muted {
		color: var(--text-muted);
	}
</style>
