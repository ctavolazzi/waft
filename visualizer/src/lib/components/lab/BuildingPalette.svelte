<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import type { BuildingTemplate, BuildingType } from '$lib/models/Village';
	import { BUILDING_TEMPLATES } from '$lib/models/Village';

	export let village: any = null;

	const dispatch = createEventDispatcher();

	let selectedCategory = 'production';
	let collapsed = false;

	const categories = {
		production: ['farmhouse', 'well', 'lumber_mill', 'quarry', 'workshop'],
		infrastructure: ['home', 'storage', 'watchtower'],
		modern: ['solar_array']
	};

	function startDrag(event: DragEvent, buildingType: BuildingType) {
		if (!event.dataTransfer) return;

		const template = BUILDING_TEMPLATES[buildingType];

		// Check if can afford
		const canAfford = checkAffordability(template);
		if (!canAfford) {
			event.preventDefault();
			return;
		}

		event.dataTransfer.effectAllowed = 'copy';
		event.dataTransfer.setData('building-template', JSON.stringify(template));
		dispatch('dragstart', { template });
	}

	function checkAffordability(template: BuildingTemplate): boolean {
		if (!village) return false;

		for (const [resource, cost] of Object.entries(template.buildCosts)) {
			if (village.resources[resource].amount < cost) {
				return false;
			}
		}

		return true;
	}
</script>

<div class="building-palette" class:collapsed>
	<div class="palette-header" on:click={() => collapsed = !collapsed}>
		<span class="palette-title">🏗️ BUILDINGS</span>
		<button class="collapse-btn">{collapsed ? '◀' : '▶'}</button>
	</div>

	{#if !collapsed}
		<div class="palette-body">
			<!-- Category tabs -->
			<div class="category-tabs">
				{#each Object.keys(categories) as category}
					<button
						class="category-tab"
						class:active={selectedCategory === category}
						on:click={() => selectedCategory = category}
					>
						{category.toUpperCase()}
					</button>
				{/each}
			</div>

			<!-- Building grid -->
			<div class="buildings-grid">
				{#each categories[selectedCategory] as buildingType}
					{@const template = BUILDING_TEMPLATES[buildingType]}
					{@const canAfford = checkAffordability(template)}

					<div
						class="building-tile"
						class:affordable={canAfford}
						class:unaffordable={!canAfford}
						draggable={canAfford}
						on:dragstart={(e) => startDrag(e, buildingType)}
					>
						<div class="building-icon">{template.icon}</div>
						<div class="building-name">{template.name}</div>

						<!-- Cost display -->
						<div class="building-costs">
							{#each Object.entries(template.buildCosts) as [resource, cost]}
								{@const hasEnough = village?.resources[resource]?.amount >= cost}
								<span class="cost-item" class:insufficient={!hasEnough}>
									{resource}: {cost}
								</span>
							{/each}
						</div>

						<!-- Trait indicator -->
						<div class="trait-badge">
							{template.requiredTrait}
						</div>

						{#if !canAfford}
							<div class="unaffordable-overlay">
								⚠️ Insufficient resources
							</div>
						{/if}
					</div>
				{/each}
			</div>

			<!-- Legend -->
			<div class="palette-footer">
				<div class="legend-item">
					<span class="legend-color" style="background: #0f3"></span>
					<span>Affordable</span>
				</div>
				<div class="legend-item">
					<span class="legend-color" style="background: #666"></span>
					<span>Too expensive</span>
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.building-palette {
		position: absolute;
		bottom: 20px;
		right: 20px;
		width: 320px;
		background: rgba(20, 20, 30, 0.95);
		border: 2px solid #0af;
		border-radius: 8px;
		backdrop-filter: blur(10px);
		box-shadow: 0 0 30px rgba(0, 170, 255, 0.3);
		z-index: 100;
		font-family: 'Courier New', monospace;
	}

	.building-palette.collapsed {
		width: 200px;
	}

	.palette-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 12px 16px;
		background: rgba(0, 170, 255, 0.1);
		border-bottom: 1px solid #0af;
		cursor: pointer;
		user-select: none;
	}

	.palette-header:hover {
		background: rgba(0, 170, 255, 0.15);
	}

	.palette-title {
		font-size: 0.9rem;
		font-weight: 600;
		color: #0af;
		letter-spacing: 1px;
	}

	.collapse-btn {
		background: none;
		border: 1px solid #0af;
		color: #0af;
		padding: 4px 8px;
		border-radius: 4px;
		cursor: pointer;
		font-size: 0.8rem;
	}

	.palette-body {
		padding: 12px;
		max-height: 400px;
		overflow-y: auto;
	}

	.palette-body::-webkit-scrollbar {
		width: 6px;
	}

	.palette-body::-webkit-scrollbar-track {
		background: rgba(0, 0, 0, 0.2);
	}

	.palette-body::-webkit-scrollbar-thumb {
		background: #0af;
		border-radius: 3px;
	}

	.category-tabs {
		display: flex;
		gap: 4px;
		margin-bottom: 12px;
		flex-wrap: wrap;
	}

	.category-tab {
		padding: 6px 10px;
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid #333;
		border-radius: 4px;
		color: #999;
		font-size: 0.7rem;
		font-family: 'Courier New', monospace;
		cursor: pointer;
		transition: all 0.2s;
	}

	.category-tab:hover {
		background: rgba(255, 255, 255, 0.1);
		border-color: #0af;
	}

	.category-tab.active {
		background: rgba(0, 170, 255, 0.2);
		border-color: #0af;
		color: #0af;
	}

	.buildings-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 8px;
		margin-bottom: 12px;
	}

	.building-tile {
		position: relative;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 6px;
		padding: 12px 8px;
		background: rgba(0, 0, 0, 0.3);
		border: 2px solid #333;
		border-radius: 8px;
		cursor: grab;
		transition: all 0.2s;
	}

	.building-tile.affordable {
		border-color: #0f3;
	}

	.building-tile.affordable:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(0, 255, 51, 0.4);
		border-width: 3px;
	}

	.building-tile.affordable:active {
		cursor: grabbing;
	}

	.building-tile.unaffordable {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.building-icon {
		font-size: 2rem;
	}

	.building-name {
		font-size: 0.75rem;
		font-weight: 600;
		color: #e0e0e0;
		text-align: center;
	}

	.building-costs {
		display: flex;
		flex-direction: column;
		gap: 2px;
		width: 100%;
		font-size: 0.65rem;
		color: #0f3;
		text-align: center;
	}

	.cost-item {
		padding: 2px;
	}

	.cost-item.insufficient {
		color: #f03;
		font-weight: 600;
	}

	.trait-badge {
		font-size: 0.6rem;
		color: #0af;
		background: rgba(0, 170, 255, 0.1);
		padding: 3px 8px;
		border-radius: 10px;
		border: 1px solid #0af;
	}

	.unaffordable-overlay {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(0, 0, 0, 0.8);
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 0.7rem;
		color: #f03;
		text-align: center;
		padding: 8px;
		border-radius: 6px;
	}

	.palette-footer {
		display: flex;
		gap: 12px;
		padding-top: 12px;
		border-top: 1px solid #333;
		font-size: 0.7rem;
		color: #999;
	}

	.legend-item {
		display: flex;
		align-items: center;
		gap: 6px;
	}

	.legend-color {
		width: 12px;
		height: 12px;
		border-radius: 2px;
	}
</style>
