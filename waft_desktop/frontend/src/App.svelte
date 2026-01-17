<script>
  import { onMount } from 'svelte';

  let backendStatus = {
    running: false,
    healthy: false,
    port: 8000,
    pid: null,
    restartAttempts: 0,
    uptime: 0
  };

  let healthStatus = 'checking';
  let logs = [];

  onMount(() => {
    // Get initial status
    updateStatus();

    // Set up event listeners
    if (window.electronAPI) {
      window.electronAPI.backend.onStatus((data) => {
        console.log('Backend status:', data);
        updateStatus();
      });

      window.electronAPI.backend.onHealth((data) => {
        healthStatus = data.healthy ? 'healthy' : 'unhealthy';
        updateStatus();
      });

      window.electronAPI.backend.onLog((data) => {
        logs = [...logs.slice(-49), data];
      });
    }

    // Poll status every 2 seconds
    const interval = setInterval(updateStatus, 2000);

    return () => clearInterval(interval);
  });

  async function updateStatus() {
    if (window.electronAPI) {
      try {
        backendStatus = await window.electronAPI.backend.getStatus();
        healthStatus = backendStatus.healthy ? 'healthy' : 'unhealthy';
      } catch (error) {
        console.error('Error getting status:', error);
      }
    }
  }

  async function restartBackend() {
    if (window.electronAPI) {
      try {
        await window.electronAPI.backend.restart();
        updateStatus();
      } catch (error) {
        console.error('Error restarting backend:', error);
      }
    }
  }

  function formatUptime(ms) {
    if (!ms) return '0s';
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);

    if (hours > 0) return `${hours}h ${minutes % 60}m`;
    if (minutes > 0) return `${minutes}m ${seconds % 60}s`;
    return `${seconds}s`;
  }
</script>

<main>
  <header>
    <h1>🌊 WAFT Desktop</h1>
    <div class="status-bar">
      <div class="status-item">
        <span class="label">Backend:</span>
        <span class="value {backendStatus.running ? 'running' : 'stopped'}">
          {backendStatus.running ? 'Running' : 'Stopped'}
        </span>
      </div>
      <div class="status-item">
        <span class="label">Health:</span>
        <span class="value {healthStatus}">
          {healthStatus === 'healthy' ? '✓ Healthy' : healthStatus === 'unhealthy' ? '✗ Unhealthy' : 'Checking...'}
        </span>
      </div>
      <div class="status-item">
        <span class="label">Port:</span>
        <span class="value">{backendStatus.port}</span>
      </div>
      {#if backendStatus.uptime > 0}
        <div class="status-item">
          <span class="label">Uptime:</span>
          <span class="value">{formatUptime(backendStatus.uptime)}</span>
        </div>
      {/if}
    </div>
  </header>

  <div class="content">
    <section class="controls">
      <h2>Backend Controls</h2>
      <button on:click={restartBackend} disabled={!backendStatus.running}>
        Restart Backend
      </button>
      <button on:click={updateStatus}>
        Refresh Status
      </button>
    </section>

    <section class="info">
      <h2>System Information</h2>
      <div class="info-grid">
        <div class="info-item">
          <span class="info-label">Process ID:</span>
          <span class="info-value">{backendStatus.pid || 'N/A'}</span>
        </div>
        <div class="info-item">
          <span class="info-label">Restart Attempts:</span>
          <span class="info-value">{backendStatus.restartAttempts}</span>
        </div>
        <div class="info-item">
          <span class="info-label">API Endpoint:</span>
          <span class="info-value">http://localhost:{backendStatus.port}</span>
        </div>
      </div>
    </section>

    <section class="logs">
      <h2>Backend Logs</h2>
      <div class="log-container">
        {#each logs as log}
          <div class="log-entry {log.type}">
            <span class="log-time">{new Date().toLocaleTimeString()}</span>
            <span class="log-message">{log.message}</span>
          </div>
        {/each}
        {#if logs.length === 0}
          <div class="log-empty">No logs yet...</div>
        {/if}
      </div>
    </section>
  </div>
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
  }

  header {
    background: #1a1a1a;
    padding: 1rem 2rem;
    border-bottom: 1px solid #333;
  }

  h1 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }

  .status-bar {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
  }

  .status-item {
    display: flex;
    gap: 0.5rem;
    align-items: center;
  }

  .label {
    color: #888;
    font-size: 0.9rem;
  }

  .value {
    font-weight: 600;
    font-size: 0.9rem;
  }

  .value.running {
    color: #4ade80;
  }

  .value.stopped {
    color: #f87171;
  }

  .value.healthy {
    color: #4ade80;
  }

  .value.unhealthy {
    color: #f87171;
  }

  .content {
    flex: 1;
    overflow-y: auto;
    padding: 2rem;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto 1fr;
    gap: 2rem;
  }

  section {
    background: #1a1a1a;
    border-radius: 8px;
    padding: 1.5rem;
    border: 1px solid #333;
  }

  section.logs {
    grid-column: 1 / -1;
  }

  h2 {
    font-size: 1.2rem;
    margin-bottom: 1rem;
    color: #e0e0e0;
  }

  .controls {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  button {
    padding: 0.75rem 1.5rem;
    background: #3b82f6;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    transition: background 0.2s;
  }

  button:hover:not(:disabled) {
    background: #2563eb;
  }

  button:disabled {
    background: #444;
    cursor: not-allowed;
    opacity: 0.6;
  }

  .info-grid {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .info-item {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid #333;
  }

  .info-label {
    color: #888;
  }

  .info-value {
    color: #e0e0e0;
    font-family: monospace;
  }

  .log-container {
    max-height: 400px;
    overflow-y: auto;
    font-family: monospace;
    font-size: 0.85rem;
  }

  .log-entry {
    padding: 0.5rem;
    border-bottom: 1px solid #222;
    display: flex;
    gap: 1rem;
  }

  .log-entry.stderr {
    color: #f87171;
  }

  .log-time {
    color: #666;
    min-width: 80px;
  }

  .log-message {
    flex: 1;
    white-space: pre-wrap;
    word-break: break-word;
  }

  .log-empty {
    color: #666;
    padding: 2rem;
    text-align: center;
  }
</style>
