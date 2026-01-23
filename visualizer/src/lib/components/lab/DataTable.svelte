<script lang="ts">
	import type { Being } from '$lib/models/Being';
	import type { Realm } from '$lib/models/Realm';

	export let realm: Realm | null = null;
	export let maxRows: number = 100;

	let collapsed = true;
	let sortBy: keyof Being = 'fitness';
	let sortDesc = true;
	let filterAlive = true;

	$: beings = realm ? getSortedBeings(realm.beings) : [];

	function getSortedBeings(allBeings: Being[]): Being[] {
		let filtered = filterAlive ? allBeings.filter(b => b.alive) : allBeings;

		filtered = [...filtered].sort((a, b) => {
			const aVal = a[sortBy];
			const bVal = b[sortBy];

			if (typeof aVal === 'number' && typeof bVal === 'number') {
				return sortDesc ? bVal - aVal : aVal - bVal;
			}

			return 0;
		});

		return filtered.slice(0, maxRows);
	}

	function toggleSort(column: keyof Being) {
		if (sortBy === column) {
			sortDesc = !sortDesc;
		} else {
			sortBy = column;
			sortDesc = true;
		}
	}

	function exportCSV() {
		if (!realm) return;

		const headers = ['ID', 'Gen', 'Age', 'Fitness', 'Energy', 'Curiosity', 'Cooperation', 'Speed', 'Alive', 'Cause of Death'];
		const rows = realm.beings.map(b => [
			b.id,
			b.generation,
			b.age,
			b.fitness.toFixed(3),
			b.energy.toFixed(3),
			b.genome.curiosity.toFixed(3),
			b.genome.cooperation.toFixed(3),
			b.genome.speed.toFixed(3),
			b.alive ? 'Yes' : 'No',
			b.causeOfDeath || '-'
		]);

		const csv = [headers, ...rows].map(row => row.join(',')).join('\n');

		const blob = new Blob([csv], { type: 'text/csv' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `${realm.config.name}-beings-${Date.now()}.csv`;
		a.click();
		URL.revokeObjectURL(url);
	}
</script>

{#if realm}
	<div class="data-table" class:collapsed>
		<div class="table-header" on:click={() => collapsed = !collapsed}>
			<span class="table-title">📊 BEING DATA TABLE</span>
			<button class="collapse-btn">{collapsed ? '▲' : '▼'}</button>
		</div>

		{#if !collapsed}
			<div class="table-controls">
				<label class="filter-checkbox">
					<input type="checkbox" bind:checked={filterAlive} />
					<span>Alive Only ({realm.beings.filter(b => b.alive).length})</span>
				</label>
				<button class="export-btn" on:click={exportCSV}>
					📥 Export CSV
				</button>
			</div>

			<div class="table-container">
				<table>
					<thead>
						<tr>
							<th on:click={() => toggleSort('id')}>
								ID {sortBy === 'id' ? (sortDesc ? '▼' : '▲') : ''}
							</th>
							<th on:click={() => toggleSort('generation')}>
								Gen {sortBy === 'generation' ? (sortDesc ? '▼' : '▲') : ''}
							</th>
							<th on:click={() => toggleSort('age')}>
								Age {sortBy === 'age' ? (sortDesc ? '▼' : '▲') : ''}
							</th>
							<th on:click={() => toggleSort('fitness')}>
								Fitness {sortBy === 'fitness' ? (sortDesc ? '▼' : '▲') : ''}
							</th>
							<th on:click={() => toggleSort('energy')}>
								Energy {sortBy === 'energy' ? (sortDesc ? '▼' : '▲') : ''}
							</th>
							<th>Curiosity</th>
							<th>Caution</th>
							<th>Cooperation</th>
							<th>Speed</th>
							<th>State</th>
						</tr>
					</thead>
					<tbody>
						{#each beings as being (being.id)}
							<tr class:dead={!being.alive}>
								<td class="id-cell">{being.id.slice(-8)}</td>
								<td>{being.generation}</td>
								<td>{being.age}</td>
								<td class="fitness-cell" style="color: {getFitnessColor(being.fitness)}">
									{being.fitness.toFixed(3)}
								</td>
								<td class="energy-cell" style="color: {getEnergyColor(being.energy)}">
									{being.energy.toFixed(3)}
								</td>
								<td>{being.genome.curiosity.toFixed(2)}</td>
								<td>{being.genome.caution.toFixed(2)}</td>
								<td>{being.genome.cooperation.toFixed(2)}</td>
								<td>{being.genome.speed.toFixed(2)}</td>
								<td class="state-cell">
									{#if !being.alive}
										<span class="death-badge">{being.causeOfDeath}</span>
									{:else if being.investigating}
										<span class="investigating-badge">🔍</span>
									{:else}
										<span class="alive-badge">✓</span>
									{/if}
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>

			<div class="table-footer">
				Showing {beings.length} of {filterAlive ? realm.beings.filter(b => b.alive).length : realm.beings.length} beings
			</div>
		{/if}
	</div>
{/if}

<script lang="ts">
	function getFitnessColor(fitness: number): string {
		if (fitness > 0.7) return '#0f3';
		if (fitness > 0.4) return '#f90';
		return '#f03';
	}

	function getEnergyColor(energy: number): string {
		if (energy > 0.6) return '#0f3';
		if (energy > 0.3) return '#f90';
		return '#f03';
	}
</script>

<style>
	.data-table {
		position: absolute;
		bottom: 20px;
		left: 360px;
		right: 20px;
		max-width: calc(100% - 400px);
		background: rgba(20, 20, 30, 0.95);
		border: 2px solid #0af;
		border-radius: 8px;
		backdrop-filter: blur(10px);
		box-shadow: 0 0 30px rgba(0, 170, 255, 0.3);
		z-index: 100;
		font-family: 'Courier New', monospace;
	}

	.data-table.collapsed {
		max-width: 300px;
	}

	.table-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 12px 16px;
		background: rgba(0, 170, 255, 0.1);
		border-bottom: 1px solid #0af;
		cursor: pointer;
		user-select: none;
	}

	.table-header:hover {
		background: rgba(0, 170, 255, 0.15);
	}

	.table-title {
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

	.table-controls {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 10px 16px;
		background: rgba(0, 0, 0, 0.2);
		border-bottom: 1px solid #333;
	}

	.filter-checkbox {
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: 0.8rem;
		color: #0af;
		cursor: pointer;
	}

	.filter-checkbox input {
		cursor: pointer;
	}

	.export-btn {
		padding: 6px 12px;
		background: rgba(0, 170, 255, 0.1);
		border: 1px solid #0af;
		border-radius: 4px;
		color: #0af;
		font-family: 'Courier New', monospace;
		font-size: 0.75rem;
		cursor: pointer;
	}

	.export-btn:hover {
		background: rgba(0, 170, 255, 0.2);
	}

	.table-container {
		max-height: 300px;
		overflow: auto;
	}

	.table-container::-webkit-scrollbar {
		width: 6px;
		height: 6px;
	}

	.table-container::-webkit-scrollbar-track {
		background: rgba(0, 0, 0, 0.2);
	}

	.table-container::-webkit-scrollbar-thumb {
		background: #0af;
		border-radius: 3px;
	}

	table {
		width: 100%;
		border-collapse: collapse;
	}

	thead th {
		position: sticky;
		top: 0;
		background: rgba(0, 170, 255, 0.2);
		padding: 10px 8px;
		text-align: left;
		font-size: 0.75rem;
		color: #0af;
		border-bottom: 2px solid #0af;
		cursor: pointer;
		user-select: none;
		white-space: nowrap;
	}

	thead th:hover {
		background: rgba(0, 170, 255, 0.3);
	}

	tbody tr {
		border-bottom: 1px solid #222;
	}

	tbody tr:hover {
		background: rgba(0, 170, 255, 0.05);
	}

	tbody tr.dead {
		opacity: 0.4;
	}

	tbody td {
		padding: 8px;
		font-size: 0.75rem;
		color: #e0e0e0;
	}

	.id-cell {
		font-family: monospace;
		color: #999;
		font-size: 0.7rem;
	}

	.fitness-cell, .energy-cell {
		font-weight: 600;
	}

	.state-cell {
		text-align: center;
	}

	.alive-badge {
		color: #0f3;
		font-weight: 600;
	}

	.investigating-badge {
		font-size: 1rem;
	}

	.death-badge {
		font-size: 0.7rem;
		color: #f03;
		background: rgba(255, 0, 51, 0.1);
		padding: 2px 6px;
		border-radius: 3px;
	}

	.table-footer {
		padding: 8px 16px;
		background: rgba(0, 0, 0, 0.2);
		border-top: 1px solid #333;
		font-size: 0.7rem;
		color: #999;
		text-align: right;
	}
</style>
