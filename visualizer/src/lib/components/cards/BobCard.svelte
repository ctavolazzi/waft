<script lang="ts">
	import { onMount } from 'svelte';
	import { apiClient } from '$lib/api/client';
	import Badge from '../status/Badge.svelte';

	interface BobData {
		found: boolean;
		being_id?: string;
		name?: string;
		role?: string;
		spawned?: string;
		skills?: Record<string, number>;
		apis?: Array<{
			name: string;
			url: string;
			type: string;
			auth: string;
			https: boolean;
			cors: boolean;
		}>;
		work?: Array<{
			type: string;
			title: string;
			date: string;
			description?: string;
		}>;
		code?: {
			module: string;
			lines: number;
			has_geocoding: boolean;
			has_reverse_geocoding: boolean;
			has_place_search: boolean;
		};
		message?: string;
	}

	let bobData: BobData | null = null;
	let loading = true;
	let error: string | null = null;

	onMount(async () => {
		try {
			const data = await apiClient.getCartographerData();
			bobData = data;
			loading = false;
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load Bob\'s data';
			loading = false;
			console.error('Failed to fetch Bob\'s data:', e);
		}
	});
</script>

<div class="card">
	<h2>🗺️ Bob the Cartographer</h2>
	<div class="card-content">
		{#if loading}
			<div class="loading">Loading Bob's work...</div>
		{:else if error}
			<div class="error">⚠️ {error}</div>
		{:else if !bobData?.found}
			<div class="info-item">
				<div class="info-value">{bobData?.message || 'Bob not found'}</div>
			</div>
		{:else}
			<!-- Being Info -->
			<div class="info-item">
				<div class="info-label">Being ID</div>
				<div class="info-value code">{bobData.being_id || 'Unknown'}</div>
			</div>

			{#if bobData.spawned}
				<div class="info-item">
					<div class="info-label">Spawned</div>
					<div class="info-value">{bobData.spawned}</div>
				</div>
			{/if}

			<!-- Skills -->
			{#if bobData.skills && Object.keys(bobData.skills).length > 0}
				<div class="info-item">
					<div class="info-label">Skills</div>
					<div class="skills-grid">
						{#each Object.entries(bobData.skills) as [skill, level]}
							<Badge type="info">
								{skill}: {level.toFixed(1)}
							</Badge>
						{/each}
					</div>
				</div>
			{/if}

			<!-- APIs -->
			{#if bobData.apis && bobData.apis.length > 0}
				<div class="info-item">
					<div class="info-label">Public APIs Integrated</div>
					{#each bobData.apis as api}
						<div class="api-item">
							<div class="api-name">
								<strong>{api.name}</strong>
								<Badge type={api.https ? 'success' : 'warning'}>
									{api.https ? 'HTTPS' : 'HTTP'}
								</Badge>
								{#if api.cors}
									<Badge type="info">CORS</Badge>
								{/if}
							</div>
							<div class="api-details">
								<div class="api-detail">
									<span class="detail-label">Type:</span> {api.type}
								</div>
								<div class="api-detail">
									<span class="detail-label">Auth:</span> {api.auth || 'None'}
								</div>
								{#if api.url}
									<div class="api-detail">
										<span class="detail-label">URL:</span>
										<a href={api.url} target="_blank" rel="noopener noreferrer" class="api-link">
											{api.url}
										</a>
									</div>
								{/if}
							</div>
						</div>
					{/each}
				</div>
			{/if}

			<!-- Code Module -->
			{#if bobData.code}
				<div class="info-item">
					<div class="info-label">Code Module</div>
					<div class="info-value code">{bobData.code.module}</div>
					<div class="code-stats">
						<span>{bobData.code.lines} lines</span>
						{#if bobData.code.has_geocoding}
							<Badge type="success">Geocoding</Badge>
						{/if}
						{#if bobData.code.has_reverse_geocoding}
							<Badge type="success">Reverse</Badge>
						{/if}
						{#if bobData.code.has_place_search}
							<Badge type="success">Search</Badge>
						{/if}
					</div>
				</div>
			{/if}

			<!-- Work History -->
			{#if bobData.work && bobData.work.length > 0}
				<div class="info-item">
					<div class="info-label">Work History</div>
					{#each bobData.work as workItem}
						<div class="work-item">
							<div class="work-title">{workItem.title}</div>
							{#if workItem.date}
								<div class="work-date">{workItem.date}</div>
							{/if}
							{#if workItem.description}
								<div class="work-description">{workItem.description}</div>
							{/if}
						</div>
					{/each}
				</div>
			{/if}
		{/if}
	</div>
</div>

<style>
	.card {
		background: var(--bg-card);
		border-radius: 16px;
		padding: 28px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
		border: 1px solid var(--border);
	}

	.card h2 {
		color: var(--text-primary);
		margin-bottom: 20px;
		font-size: 1.5rem;
		border-bottom: 2px solid var(--border);
		padding-bottom: 12px;
	}

	.card-content {
		display: flex;
		flex-direction: column;
		gap: 12px;
	}

	.info-item {
		margin: 12px 0;
		padding: 14px;
		background: rgba(26, 30, 41, 0.6);
		border-radius: 10px;
		border: 1px solid var(--border);
	}

	.info-label {
		font-weight: 600;
		color: var(--text-secondary);
		margin-bottom: 8px;
		font-size: 0.9em;
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.info-value {
		color: var(--text-primary);
		font-size: 1.05em;
	}

	.info-value.code {
		font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
		font-size: 0.9rem;
		color: var(--text-secondary);
		opacity: 0.9;
		word-break: break-all;
	}

	.skills-grid {
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
		margin-top: 8px;
	}

	.api-item {
		margin: 12px 0;
		padding: 12px;
		background: rgba(0, 0, 0, 0.2);
		border-radius: 8px;
		border-left: 3px solid var(--primary);
	}

	.api-name {
		display: flex;
		align-items: center;
		gap: 8px;
		margin-bottom: 8px;
		font-size: 1.1em;
	}

	.api-details {
		display: flex;
		flex-direction: column;
		gap: 4px;
		font-size: 0.9em;
		color: var(--text-secondary);
	}

	.api-detail {
		display: flex;
		gap: 8px;
	}

	.detail-label {
		font-weight: 600;
		color: var(--text-secondary);
	}

	.api-link {
		color: var(--primary);
		text-decoration: none;
		word-break: break-all;
	}

	.api-link:hover {
		text-decoration: underline;
	}

	.code-stats {
		display: flex;
		align-items: center;
		gap: 8px;
		margin-top: 8px;
		font-size: 0.9em;
		color: var(--text-secondary);
	}

	.work-item {
		margin: 12px 0;
		padding: 12px;
		background: rgba(0, 0, 0, 0.2);
		border-radius: 8px;
		border-left: 3px solid var(--primary);
	}

	.work-title {
		font-weight: 600;
		color: var(--text-primary);
		margin-bottom: 4px;
	}

	.work-date {
		font-size: 0.85em;
		color: var(--text-secondary);
		margin-bottom: 4px;
	}

	.work-description {
		font-size: 0.9em;
		color: var(--text-secondary);
		margin-top: 4px;
	}

	.loading {
		text-align: center;
		padding: 20px;
		color: var(--text-secondary);
	}

	.error {
		text-align: center;
		padding: 20px;
		color: var(--error);
	}
</style>
