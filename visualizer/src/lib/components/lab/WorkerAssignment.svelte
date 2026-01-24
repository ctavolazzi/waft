<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import type { Building } from '$lib/models/Village';
	import type { Being } from '$lib/models/Being';

	export let building: Building | null = null;
	export let beings: Being[] = [];
	export let village: any = null;

	const dispatch = createEventDispatcher();

	$: aliveBings = beings.filter(b => b.alive);
	$: employedIds = village?.jobs.map((j: any) => j.beingId) || [];
	$: unemployedBeings = aliveBings.filter(b => !employedIds.includes(b.id));
	$: currentWorkers = building ? aliveBings.filter(b => building.assignedWorkers.includes(b.id)) : [];

	function assignBeing(being: Being) {
		if (!building) return;

		dispatch('assign', { building, being });
	}

	function unassignBeing(being: Being) {
		if (!building) return;

		dispatch('unassign', { building, being });
	}

	function closePanel() {
		dispatch('close');
	}

	function getTraitColor(value: number): string {
		if (value > 0.7) return '#0f3';
		if (value > 0.4) return '#f90';
		return '#f03';
	}

	function calculateProductivity(being: Being): number {
		if (!building) return 0;
		const requiredTrait = building.template.requiredTrait;
		return being.genome[requiredTrait];
	}
</script>

{#if building}
	<div class="worker-assignment">
		<div class="assignment-header">
			<div class="building-info">
				<span class="building-icon">{building.template.icon}</span>
				<div>
					<div class="building-name">{building.template.name}</div>
					<div class="building-desc">{building.template.description}</div>
				</div>
			</div>
			<button class="close-btn" on:click={closePanel}>✕</button>
		</div>

		<div class="assignment-body">
			<!-- Building status -->
			<div class="status-section">
				{#if !building.operational}
					<div class="construction-status">
						🚧 Under Construction: {(building.constructionProgress * 100).toFixed(0)}%
						<div class="progress-bar">
							<div class="progress-fill" style="width: {building.constructionProgress * 100}%"></div>
						</div>
					</div>
				{:else}
					<div class="operational-status">
						<div class="status-item">
							<span class="status-label">Efficiency:</span>
							<span class="status-value" style="color: {getTraitColor(building.efficiency)}">
								{(building.efficiency * 100).toFixed(0)}%
							</span>
						</div>

						<div class="status-item">
							<span class="status-label">Workers:</span>
							<span class="status-value">
								{building.assignedWorkers.length} / {building.template.maxWorkers}
							</span>
						</div>

						{#if building.template.produces}
							<div class="status-item">
								<span class="status-label">Production:</span>
								<span class="status-value production">
									+{building.lastTickProduction.toFixed(2)} {building.template.produces}/tick
								</span>
							</div>
						{/if}
					</div>
				{/if}
			</div>

			<!-- Required trait -->
			<div class="trait-section">
				<div class="trait-header">
					🧬 Required Trait: <strong>{building.template.requiredTrait}</strong>
				</div>
				<div class="trait-help">
					Beings with high {building.template.requiredTrait} work more efficiently here
				</div>
			</div>

			<!-- Current workers -->
			{#if currentWorkers.length > 0}
				<div class="workers-section">
					<div class="section-title">👷 Current Workers:</div>
					<div class="workers-list">
						{#each currentWorkers as worker}
							{@const productivity = calculateProductivity(worker)}
							<div class="worker-card">
								<div class="worker-info">
									<div class="worker-id">{worker.id.slice(-8)}</div>
									<div class="worker-stats">
										<span class="stat">Gen {worker.generation}</span>
										<span class="stat">Fit: {worker.fitness.toFixed(2)}</span>
									</div>
								</div>
								<div class="worker-productivity">
									<div class="productivity-label">Productivity:</div>
									<div class="productivity-value" style="color: {getTraitColor(productivity)}">
										{(productivity * 100).toFixed(0)}%
									</div>
								</div>
								<button class="remove-btn" on:click={() => unassignBeing(worker)}>
									Remove
								</button>
							</div>
						{/each}
					</div>
				</div>
			{/if}

			<!-- Available beings -->
			{#if building.operational && building.assignedWorkers.length < building.template.maxWorkers}
				<div class="available-section">
					<div class="section-title">
						🔍 Available Beings ({unemployedBeings.length}):
					</div>

					{#if unemployedBeings.length === 0}
						<div class="empty-message">
							All beings are employed. Build more homes to increase population!
						</div>
					{:else}
						<div class="available-list">
							{#each unemployedBeings.sort((a, b) => calculateProductivity(b) - calculateProductivity(a)).slice(0, 10) as being}
								{@const productivity = calculateProductivity(being)}
								<div class="being-card" on:click={() => assignBeing(being)}>
									<div class="being-info">
										<div class="being-id">{being.id.slice(-8)}</div>
										<div class="being-stats">
											<span class="stat">Gen {being.generation}</span>
											<span class="stat">Age {being.age}</span>
										</div>
									</div>
									<div class="being-trait">
										<div class="trait-value" style="color: {getTraitColor(being.genome[building.template.requiredTrait])}">
											{building.template.requiredTrait}: {being.genome[building.template.requiredTrait].toFixed(2)}
										</div>
										<div class="predicted-productivity">
											→ {(productivity * 100).toFixed(0)}% efficiency
										</div>
									</div>
									<button class="assign-btn">Assign</button>
								</div>
							{/each}
						</div>
					{/if}
				</div>
			{/if}
		</div>
	</div>
{/if}

<style>
	.worker-assignment {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: 600px;
		max-height: 80vh;
		background: rgba(20, 20, 30, 0.98);
		border: 3px solid #0af;
		border-radius: 12px;
		box-shadow: 0 0 50px rgba(0, 170, 255, 0.6);
		z-index: 200;
		font-family: 'Courier New', monospace;
		overflow: hidden;
	}

	.assignment-header {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		padding: 20px;
		background: rgba(0, 170, 255, 0.1);
		border-bottom: 2px solid #0af;
	}

	.building-info {
		display: flex;
		gap: 16px;
		align-items: center;
	}

	.building-icon {
		font-size: 3rem;
	}

	.building-name {
		font-size: 1.2rem;
		font-weight: 600;
		color: #0af;
		margin-bottom: 4px;
	}

	.building-desc {
		font-size: 0.85rem;
		color: #999;
		line-height: 1.4;
	}

	.close-btn {
		background: none;
		border: 2px solid #f03;
		color: #f03;
		width: 32px;
		height: 32px;
		border-radius: 50%;
		cursor: pointer;
		font-size: 1.2rem;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.close-btn:hover {
		background: rgba(255, 0, 51, 0.2);
	}

	.assignment-body {
		padding: 20px;
		max-height: calc(80vh - 120px);
		overflow-y: auto;
	}

	.assignment-body::-webkit-scrollbar {
		width: 8px;
	}

	.assignment-body::-webkit-scrollbar-track {
		background: rgba(0, 0, 0, 0.2);
	}

	.assignment-body::-webkit-scrollbar-thumb {
		background: #0af;
		border-radius: 4px;
	}

	.status-section {
		margin-bottom: 20px;
		padding: 16px;
		background: rgba(0, 0, 0, 0.3);
		border: 1px solid #333;
		border-radius: 8px;
	}

	.construction-status {
		color: #f90;
		font-size: 0.9rem;
	}

	.progress-bar {
		height: 8px;
		background: rgba(0, 0, 0, 0.5);
		border-radius: 4px;
		margin-top: 8px;
		overflow: hidden;
	}

	.progress-fill {
		height: 100%;
		background: linear-gradient(90deg, #f90 0%, #0f3 100%);
		transition: width 0.3s ease;
	}

	.operational-status {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.status-item {
		display: flex;
		justify-content: space-between;
		font-size: 0.9rem;
	}

	.status-label {
		color: #999;
	}

	.status-value {
		font-weight: 600;
		color: #0f3;
	}

	.status-value.production {
		color: #0f3;
	}

	.trait-section {
		margin-bottom: 20px;
		padding: 12px;
		background: rgba(0, 170, 255, 0.05);
		border: 1px solid #0af;
		border-radius: 8px;
	}

	.trait-header {
		font-size: 0.9rem;
		color: #0af;
		margin-bottom: 4px;
	}

	.trait-help {
		font-size: 0.75rem;
		color: #999;
		font-style: italic;
	}

	.workers-section, .available-section {
		margin-bottom: 20px;
	}

	.section-title {
		font-size: 0.9rem;
		font-weight: 600;
		color: #e0e0e0;
		margin-bottom: 12px;
		padding-bottom: 8px;
		border-bottom: 1px solid #333;
	}

	.workers-list, .available-list {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.worker-card, .being-card {
		display: flex;
		align-items: center;
		gap: 12px;
		padding: 12px;
		background: rgba(0, 0, 0, 0.3);
		border: 1px solid #333;
		border-radius: 6px;
		transition: all 0.2s;
	}

	.being-card {
		cursor: pointer;
	}

	.being-card:hover {
		background: rgba(0, 170, 255, 0.1);
		border-color: #0af;
	}

	.worker-info, .being-info {
		flex: 1;
	}

	.worker-id, .being-id {
		font-size: 0.8rem;
		color: #0af;
		font-weight: 600;
		margin-bottom: 4px;
	}

	.worker-stats, .being-stats {
		display: flex;
		gap: 12px;
		font-size: 0.7rem;
		color: #999;
	}

	.worker-productivity, .being-trait {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.productivity-label {
		font-size: 0.7rem;
		color: #999;
	}

	.productivity-value {
		font-size: 0.9rem;
		font-weight: 600;
	}

	.trait-value {
		font-size: 0.85rem;
		font-weight: 600;
	}

	.predicted-productivity {
		font-size: 0.7rem;
		color: #0f3;
	}

	.remove-btn, .assign-btn {
		padding: 6px 12px;
		border-radius: 4px;
		font-family: 'Courier New', monospace;
		font-size: 0.75rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s;
	}

	.remove-btn {
		background: rgba(255, 0, 51, 0.1);
		border: 1px solid #f03;
		color: #f03;
	}

	.remove-btn:hover {
		background: rgba(255, 0, 51, 0.2);
	}

	.assign-btn {
		background: rgba(0, 255, 51, 0.1);
		border: 1px solid #0f3;
		color: #0f3;
	}

	.assign-btn:hover {
		background: rgba(0, 255, 51, 0.2);
	}

	.empty-message {
		padding: 20px;
		text-align: center;
		color: #999;
		font-size: 0.85rem;
		font-style: italic;
	}
</style>
