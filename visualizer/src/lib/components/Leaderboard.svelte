<script lang="ts">
	import { onMount, onDestroy } from 'svelte';

	export let agents: Agent[] = [];
	export let maxDisplay: number = 10;
	export let title: string = 'Evolution Leaderboard';
	export let sortBy: 'fitness' | 'kills' | 'wins' | 'generation' = 'fitness';
	export let animated: boolean = true;

	interface Agent {
		id: string;
		name: string;
		fitness: number;
		generation: number;
		wins: number;
		kills: number;
		status: 'alive' | 'dead' | 'evolved';
		avatar?: string;
	}

	let sortedAgents: Agent[] = [];
	let previousRanks: Map<string, number> = new Map();
	let rankChanges: Map<string, 'up' | 'down' | 'same' | 'new'> = new Map();

	// Sort agents based on selected criteria
	function sortAgents() {
		const sorted = [...agents].sort((a, b) => {
			switch (sortBy) {
				case 'fitness':
					return b.fitness - a.fitness;
				case 'kills':
					return b.kills - a.kills;
				case 'wins':
					return b.wins - a.wins;
				case 'generation':
					return b.generation - a.generation;
				default:
					return 0;
			}
		});

		// Track rank changes
		rankChanges.clear();
		sorted.slice(0, maxDisplay).forEach((agent, index) => {
			const previousRank = previousRanks.get(agent.id);
			if (previousRank === undefined) {
				rankChanges.set(agent.id, 'new');
			} else if (previousRank > index) {
				rankChanges.set(agent.id, 'up');
			} else if (previousRank < index) {
				rankChanges.set(agent.id, 'down');
			} else {
				rankChanges.set(agent.id, 'same');
			}
			previousRanks.set(agent.id, index);
		});

		sortedAgents = sorted.slice(0, maxDisplay);
	}

	// Get rank badge
	function getRankBadge(rank: number): { icon: string; class: string } {
		switch (rank) {
			case 0:
				return { icon: '👑', class: 'gold' };
			case 1:
				return { icon: '🥈', class: 'silver' };
			case 2:
				return { icon: '🥉', class: 'bronze' };
			default:
				return { icon: `${rank + 1}`, class: 'normal' };
		}
	}

	// Get status color
	function getStatusColor(status: string): string {
		switch (status) {
			case 'alive':
				return '#10b981';
			case 'dead':
				return '#ef4444';
			case 'evolved':
				return '#a855f7';
			default:
				return '#888';
		}
	}

	// Get value to display based on sort
	function getDisplayValue(agent: Agent): string {
		switch (sortBy) {
			case 'fitness':
				return `${(agent.fitness * 100).toFixed(1)}%`;
			case 'kills':
				return `${agent.kills} kills`;
			case 'wins':
				return `${agent.wins} wins`;
			case 'generation':
				return `Gen ${agent.generation}`;
			default:
				return '';
		}
	}

	$: if (agents) sortAgents();
</script>

<div class="leaderboard" class:animated>
	<div class="header">
		<h2>{title}</h2>
		<div class="sort-controls">
			<button
				class:active={sortBy === 'fitness'}
				on:click={() => (sortBy = 'fitness')}
			>
				💪 Fitness
			</button>
			<button
				class:active={sortBy === 'wins'}
				on:click={() => (sortBy = 'wins')}
			>
				🏆 Wins
			</button>
			<button
				class:active={sortBy === 'kills'}
				on:click={() => (sortBy = 'kills')}
			>
				⚔️ Kills
			</button>
			<button
				class:active={sortBy === 'generation'}
				on:click={() => (sortBy = 'generation')}
			>
				🧬 Gen
			</button>
		</div>
	</div>

	<div class="entries">
		{#each sortedAgents as agent, index (agent.id)}
			{@const badge = getRankBadge(index)}
			{@const change = rankChanges.get(agent.id) || 'same'}
			<div
				class="entry rank-{index}"
				class:new={change === 'new'}
				class:up={change === 'up'}
				class:down={change === 'down'}
				style="--delay: {index * 50}ms"
			>
				<div class="rank {badge.class}">
					{#if index < 3}
						<span class="rank-icon">{badge.icon}</span>
					{:else}
						<span class="rank-number">{index + 1}</span>
					{/if}
				</div>

				<div class="avatar">
					{#if agent.avatar}
						<img src={agent.avatar} alt={agent.name} />
					{:else}
						<div class="avatar-placeholder" style="background: {getStatusColor(agent.status)}">
							{agent.name.charAt(0).toUpperCase()}
						</div>
					{/if}
					<div class="status-dot" style="background: {getStatusColor(agent.status)}"></div>
				</div>

				<div class="info">
					<span class="name">{agent.name}</span>
					<span class="meta">
						Gen {agent.generation} • {agent.wins}W {agent.kills}K
					</span>
				</div>

				<div class="value">
					<span class="main-value">{getDisplayValue(agent)}</span>
					{#if change === 'up'}
						<span class="change up">▲</span>
					{:else if change === 'down'}
						<span class="change down">▼</span>
					{:else if change === 'new'}
						<span class="change new">NEW</span>
					{/if}
				</div>

				<div class="bar-container">
					<div
						class="bar"
						style="width: {agent.fitness * 100}%; background: linear-gradient(90deg, {getStatusColor(agent.status)}, {getStatusColor(agent.status)}88)"
					></div>
				</div>
			</div>
		{/each}

		{#if sortedAgents.length === 0}
			<div class="empty">
				<span class="empty-icon">🏆</span>
				<span class="empty-text">No agents yet</span>
				<span class="empty-hint">Start evolving to climb the ranks!</span>
			</div>
		{/if}
	</div>
</div>

<style>
	.leaderboard {
		background: linear-gradient(135deg, rgba(10, 10, 26, 0.9) 0%, rgba(26, 26, 46, 0.9) 100%);
		border: 1px solid rgba(124, 158, 255, 0.2);
		border-radius: 16px;
		padding: 20px;
		backdrop-filter: blur(10px);
		box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
	}

	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 20px;
		padding-bottom: 15px;
		border-bottom: 1px solid rgba(124, 158, 255, 0.1);
	}

	h2 {
		margin: 0;
		font-size: 20px;
		font-weight: 700;
		background: linear-gradient(135deg, #7c9eff, #a855f7);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}

	.sort-controls {
		display: flex;
		gap: 8px;
	}

	.sort-controls button {
		background: rgba(124, 158, 255, 0.1);
		border: 1px solid rgba(124, 158, 255, 0.2);
		color: #888;
		padding: 6px 12px;
		border-radius: 8px;
		font-size: 12px;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.sort-controls button:hover {
		background: rgba(124, 158, 255, 0.2);
		color: #fff;
	}

	.sort-controls button.active {
		background: linear-gradient(135deg, #7c9eff, #a855f7);
		border-color: transparent;
		color: #fff;
	}

	.entries {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.entry {
		display: grid;
		grid-template-columns: 50px 50px 1fr auto;
		gap: 12px;
		align-items: center;
		padding: 12px;
		background: rgba(255, 255, 255, 0.02);
		border-radius: 12px;
		transition: all 0.3s ease;
		position: relative;
		overflow: hidden;
	}

	.animated .entry {
		animation: slideIn 0.3s ease both;
		animation-delay: var(--delay);
	}

	@keyframes slideIn {
		from {
			opacity: 0;
			transform: translateX(-20px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
	}

	.entry:hover {
		background: rgba(124, 158, 255, 0.1);
		transform: translateX(5px);
	}

	.entry.rank-0 {
		background: linear-gradient(90deg, rgba(255, 215, 0, 0.1) 0%, transparent 100%);
		border: 1px solid rgba(255, 215, 0, 0.3);
	}

	.entry.rank-1 {
		background: linear-gradient(90deg, rgba(192, 192, 192, 0.1) 0%, transparent 100%);
		border: 1px solid rgba(192, 192, 192, 0.2);
	}

	.entry.rank-2 {
		background: linear-gradient(90deg, rgba(205, 127, 50, 0.1) 0%, transparent 100%);
		border: 1px solid rgba(205, 127, 50, 0.2);
	}

	.entry.new {
		animation: glow 1s ease;
	}

	@keyframes glow {
		0%,
		100% {
			box-shadow: 0 0 0 0 rgba(124, 158, 255, 0);
		}
		50% {
			box-shadow: 0 0 20px 5px rgba(124, 158, 255, 0.3);
		}
	}

	.rank {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 40px;
		height: 40px;
		border-radius: 10px;
		font-weight: bold;
	}

	.rank.gold {
		background: linear-gradient(135deg, #ffd700, #ffb800);
		box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
	}

	.rank.silver {
		background: linear-gradient(135deg, #c0c0c0, #a8a8a8);
		box-shadow: 0 4px 15px rgba(192, 192, 192, 0.3);
	}

	.rank.bronze {
		background: linear-gradient(135deg, #cd7f32, #b8722e);
		box-shadow: 0 4px 15px rgba(205, 127, 50, 0.3);
	}

	.rank.normal {
		background: rgba(124, 158, 255, 0.1);
		color: #888;
	}

	.rank-icon {
		font-size: 20px;
	}

	.rank-number {
		font-size: 16px;
	}

	.avatar {
		position: relative;
		width: 40px;
		height: 40px;
	}

	.avatar img,
	.avatar-placeholder {
		width: 40px;
		height: 40px;
		border-radius: 50%;
		object-fit: cover;
	}

	.avatar-placeholder {
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: bold;
		font-size: 18px;
		color: #fff;
	}

	.status-dot {
		position: absolute;
		bottom: 0;
		right: 0;
		width: 12px;
		height: 12px;
		border-radius: 50%;
		border: 2px solid #0a0a1a;
	}

	.info {
		display: flex;
		flex-direction: column;
		gap: 2px;
	}

	.name {
		font-weight: 600;
		font-size: 14px;
		color: #fff;
	}

	.meta {
		font-size: 11px;
		color: #666;
	}

	.value {
		display: flex;
		align-items: center;
		gap: 8px;
		text-align: right;
	}

	.main-value {
		font-weight: bold;
		font-size: 16px;
		color: #7c9eff;
	}

	.change {
		font-size: 12px;
		font-weight: bold;
		padding: 2px 6px;
		border-radius: 4px;
	}

	.change.up {
		color: #10b981;
		background: rgba(16, 185, 129, 0.2);
	}

	.change.down {
		color: #ef4444;
		background: rgba(239, 68, 68, 0.2);
	}

	.change.new {
		color: #a855f7;
		background: rgba(168, 85, 247, 0.2);
		font-size: 10px;
	}

	.bar-container {
		position: absolute;
		bottom: 0;
		left: 0;
		right: 0;
		height: 3px;
		background: rgba(255, 255, 255, 0.05);
	}

	.bar {
		height: 100%;
		transition: width 0.5s ease;
	}

	.empty {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 40px;
		color: #666;
	}

	.empty-icon {
		font-size: 48px;
		margin-bottom: 16px;
		opacity: 0.5;
	}

	.empty-text {
		font-size: 18px;
		font-weight: 600;
	}

	.empty-hint {
		font-size: 14px;
		margin-top: 8px;
	}
</style>
