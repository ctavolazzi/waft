<script lang="ts">
	import type { Village, ResourceType } from '$lib/models/Village';

	export let village: Village | null = null;

	let collapsed = false;

	const RESOURCE_ICONS: Record<ResourceType, string> = {
		food: '🌾',
		water: '💧',
		wood: '🪵',
		stone: '🪨',
		energy: '⚡',
		metal: '🔩'
	};

	function getResourceColor(type: ResourceType): string {
		switch (type) {
			case 'food': return '#f90';
			case 'water': return '#0af';
			case 'wood': return '#a52';
			case 'stone': return '#888';
			case 'energy': return '#ff0';
			case 'metal': return '#ccc';
			default: return '#fff';
		}
	}

	function getStatusColor(amount: number, capacity: number): string {
		const ratio = amount / capacity;
		if (ratio > 0.7) return '#0f3';
		if (ratio > 0.3) return '#f90';
		return '#f03';
	}

	function asResourceType(type: string): ResourceType {
		return type as ResourceType;
	}
</script>

{#if village}
	<div class="resource-panel" class:collapsed>
		<div class="panel-header" on:click={() => collapsed = !collapsed}>
			<span class="panel-title">📦 RESOURCES</span>
			<button class="collapse-btn">{collapsed ? '◀' : '▶'}</button>
		</div>

		{#if !collapsed}
			<div class="panel-body">
				<!-- Resource grid -->
				<div class="resources-grid">
					{#each Object.entries(village.resources) as [type, resource]}
						{@const resourceType = asResourceType(type)}
						{@const percentFull = (resource.amount / resource.capacity) * 100}
						{@const statusColor = getStatusColor(resource.amount, resource.capacity)}

						<div class="resource-item">
							<div class="resource-header">
								<span class="resource-icon">{RESOURCE_ICONS[resourceType]}</span>
								<span class="resource-name">{type.toUpperCase()}</span>
							</div>

							<div class="resource-amount" style="color: {statusColor}">
								{resource.amount.toFixed(1)} / {resource.capacity}
							</div>

							<div class="resource-bar">
								<div
									class="resource-fill"
									style="
										width: {percentFull}%;
										background: {getResourceColor(resourceType)};
									"
								></div>
							</div>

							<!-- Production / Consumption -->
							{#if village.totalProduction[resourceType] || village.totalConsumption[resourceType]}
								<div class="resource-flow">
									{#if village.totalProduction[resourceType]}
										<span class="production">
											+{village.totalProduction[resourceType].toFixed(2)}/t
										</span>
									{/if}
									{#if village.totalConsumption[resourceType]}
										<span class="consumption">
											-{village.totalConsumption[resourceType].toFixed(2)}/t
										</span>
									{/if}
								</div>
							{/if}
						</div>
					{/each}
				</div>

				<!-- Population stats -->
				<div class="population-section">
					<div class="section-header">👥 POPULATION</div>
					<div class="population-grid">
						<div class="pop-stat">
							<span class="stat-label">Total:</span>
							<span class="stat-value">{village.totalPopulation}</span>
						</div>
						<div class="pop-stat">
							<span class="stat-label">Employed:</span>
							<span class="stat-value employed">{village.employedPopulation}</span>
						</div>
						<div class="pop-stat">
							<span class="stat-label">Idle:</span>
							<span class="stat-value idle">{village.unemployedPopulation}</span>
						</div>
					</div>
				</div>

				<!-- Building count -->
				<div class="buildings-section">
					<div class="section-header">🏗️ BUILDINGS</div>
					<div class="building-stats">
						<span class="stat-label">Total:</span>
						<span class="stat-value">{village.buildings.length}</span>
						<span class="stat-label">Operational:</span>
						<span class="stat-value">
							{village.buildings.filter(b => b.operational).length}
						</span>
					</div>
				</div>
			</div>
		{/if}
	</div>
{/if}

<style>
	.resource-panel {
		position: absolute;
		top: 80px;
		right: 20px;
		width: 300px;
		background: rgba(20, 20, 30, 0.95);
		border: 2px solid #f90;
		border-radius: 8px;
		backdrop-filter: blur(10px);
		box-shadow: 0 0 30px rgba(255, 153, 0, 0.3);
		z-index: 100;
		font-family: 'Courier New', monospace;
	}

	.resource-panel.collapsed {
		width: 180px;
	}

	.panel-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 12px 16px;
		background: rgba(255, 153, 0, 0.1);
		border-bottom: 1px solid #f90;
		cursor: pointer;
		user-select: none;
	}

	.panel-header:hover {
		background: rgba(255, 153, 0, 0.15);
	}

	.panel-title {
		font-size: 0.9rem;
		font-weight: 600;
		color: #f90;
		letter-spacing: 1px;
	}

	.collapse-btn {
		background: none;
		border: 1px solid #f90;
		color: #f90;
		padding: 4px 8px;
		border-radius: 4px;
		cursor: pointer;
		font-size: 0.8rem;
	}

	.panel-body {
		padding: 12px;
		max-height: calc(100vh - 200px);
		overflow-y: auto;
	}

	.panel-body::-webkit-scrollbar {
		width: 6px;
	}

	.panel-body::-webkit-scrollbar-track {
		background: rgba(0, 0, 0, 0.2);
	}

	.panel-body::-webkit-scrollbar-thumb {
		background: #f90;
		border-radius: 3px;
	}

	.resources-grid {
		display: grid;
		gap: 12px;
		margin-bottom: 16px;
	}

	.resource-item {
		background: rgba(0, 0, 0, 0.3);
		border: 1px solid #333;
		border-radius: 6px;
		padding: 10px;
	}

	.resource-header {
		display: flex;
		align-items: center;
		gap: 8px;
		margin-bottom: 6px;
	}

	.resource-icon {
		font-size: 1.2rem;
	}

	.resource-name {
		font-size: 0.75rem;
		font-weight: 600;
		color: #e0e0e0;
	}

	.resource-amount {
		font-size: 0.85rem;
		font-weight: 600;
		margin-bottom: 6px;
	}

	.resource-bar {
		height: 6px;
		background: rgba(0, 0, 0, 0.5);
		border-radius: 3px;
		overflow: hidden;
		margin-bottom: 4px;
	}

	.resource-fill {
		height: 100%;
		transition: width 0.3s ease;
	}

	.resource-flow {
		display: flex;
		justify-content: space-between;
		font-size: 0.7rem;
		margin-top: 4px;
	}

	.production {
		color: #0f3;
	}

	.consumption {
		color: #f03;
	}

	.population-section, .buildings-section {
		background: rgba(0, 170, 255, 0.05);
		border: 1px solid #0af;
		border-radius: 6px;
		padding: 10px;
		margin-bottom: 12px;
	}

	.section-header {
		font-size: 0.8rem;
		color: #0af;
		font-weight: 600;
		margin-bottom: 8px;
	}

	.population-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 8px;
	}

	.pop-stat, .building-stats {
		display: flex;
		flex-direction: column;
		gap: 2px;
	}

	.building-stats {
		display: grid;
		grid-template-columns: auto 1fr;
		gap: 4px 8px;
		align-items: center;
	}

	.stat-label {
		font-size: 0.7rem;
		color: #999;
	}

	.stat-value {
		font-size: 0.9rem;
		font-weight: 600;
		color: #e0e0e0;
	}

	.stat-value.employed {
		color: #0f3;
	}

	.stat-value.idle {
		color: #f90;
	}
</style>
