<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let agent: Agent;
	export let compact: boolean = false;
	export let showActions: boolean = true;

	interface Agent {
		id: string;
		name: string;
		scientificName?: string;
		fitness: number;
		generation: number;
		wins: number;
		losses: number;
		kills: number;
		deaths: number;
		status: 'alive' | 'dead' | 'evolved' | 'breeding';
		createdAt: string;
		mutationCount: number;
		parentId?: string;
		childrenCount: number;
		traits: {
			attack: number;
			defense: number;
			speed: number;
			adaptability: number;
		};
	}

	const dispatch = createEventDispatcher();

	// Calculate derived stats
	$: winRate = agent.wins + agent.losses > 0 ? (agent.wins / (agent.wins + agent.losses)) * 100 : 0;
	$: kdr = agent.deaths > 0 ? agent.kills / agent.deaths : agent.kills;
	$: age = getAge(agent.createdAt);

	function getAge(createdAt: string): string {
		const created = new Date(createdAt);
		const now = new Date();
		const diff = now.getTime() - created.getTime();

		const days = Math.floor(diff / (1000 * 60 * 60 * 24));
		const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));

		if (days > 0) return `${days}d ${hours}h`;
		if (hours > 0) return `${hours}h`;
		return 'Just born';
	}

	function getStatusColor(status: string): string {
		switch (status) {
			case 'alive':
				return '#10b981';
			case 'dead':
				return '#ef4444';
			case 'evolved':
				return '#a855f7';
			case 'breeding':
				return '#f59e0b';
			default:
				return '#888';
		}
	}

	function getStatusIcon(status: string): string {
		switch (status) {
			case 'alive':
				return '💚';
			case 'dead':
				return '💀';
			case 'evolved':
				return '✨';
			case 'breeding':
				return '💕';
			default:
				return '❓';
		}
	}

	function getFitnessGrade(fitness: number): { grade: string; color: string } {
		if (fitness >= 0.95) return { grade: 'S+', color: '#ffd700' };
		if (fitness >= 0.9) return { grade: 'S', color: '#ffd700' };
		if (fitness >= 0.8) return { grade: 'A', color: '#10b981' };
		if (fitness >= 0.7) return { grade: 'B', color: '#3b82f6' };
		if (fitness >= 0.6) return { grade: 'C', color: '#f59e0b' };
		if (fitness >= 0.5) return { grade: 'D', color: '#f97316' };
		return { grade: 'F', color: '#ef4444' };
	}

	$: fitnessGrade = getFitnessGrade(agent.fitness);
</script>

<div class="profile-card" class:compact class:dead={agent.status === 'dead'}>
	<!-- Header with avatar and status -->
	<div class="header">
		<div class="avatar-section">
			<div class="avatar" style="border-color: {getStatusColor(agent.status)}">
				<span class="avatar-letter">{agent.name.charAt(0).toUpperCase()}</span>
				<div class="level-badge">G{agent.generation}</div>
			</div>
			<div class="status-badge" style="background: {getStatusColor(agent.status)}">
				{getStatusIcon(agent.status)} {agent.status}
			</div>
		</div>

		<div class="fitness-ring">
			<svg viewBox="0 0 100 100">
				<circle class="bg" cx="50" cy="50" r="45" />
				<circle
					class="progress"
					cx="50"
					cy="50"
					r="45"
					style="stroke-dasharray: {agent.fitness * 283} 283; stroke: {fitnessGrade.color}"
				/>
			</svg>
			<div class="fitness-center">
				<span class="grade" style="color: {fitnessGrade.color}">{fitnessGrade.grade}</span>
				<span class="percent">{(agent.fitness * 100).toFixed(0)}%</span>
			</div>
		</div>
	</div>

	<!-- Name and info -->
	<div class="identity">
		<h3 class="name">{agent.name}</h3>
		{#if agent.scientificName}
			<span class="scientific-name">{agent.scientificName}</span>
		{/if}
		<span class="age">Age: {age}</span>
	</div>

	{#if !compact}
		<!-- Stats grid -->
		<div class="stats-grid">
			<div class="stat">
				<span class="stat-icon">⚔️</span>
				<span class="stat-value">{agent.attack || agent.traits?.attack || 0}</span>
				<span class="stat-label">ATK</span>
			</div>
			<div class="stat">
				<span class="stat-icon">🛡️</span>
				<span class="stat-value">{agent.defense || agent.traits?.defense || 0}</span>
				<span class="stat-label">DEF</span>
			</div>
			<div class="stat">
				<span class="stat-icon">⚡</span>
				<span class="stat-value">{agent.speed || agent.traits?.speed || 0}</span>
				<span class="stat-label">SPD</span>
			</div>
			<div class="stat">
				<span class="stat-icon">🧬</span>
				<span class="stat-value">{agent.adaptability || agent.traits?.adaptability || 0}</span>
				<span class="stat-label">ADP</span>
			</div>
		</div>

		<!-- Combat record -->
		<div class="combat-record">
			<div class="record-item">
				<span class="record-label">Win Rate</span>
				<div class="record-bar">
					<div class="record-fill" style="width: {winRate}%; background: #10b981"></div>
				</div>
				<span class="record-value">{winRate.toFixed(1)}%</span>
			</div>
			<div class="record-stats">
				<span class="wins">{agent.wins}W</span>
				<span class="losses">{agent.losses}L</span>
				<span class="kdr">KDR: {kdr.toFixed(2)}</span>
			</div>
		</div>

		<!-- Lineage info -->
		<div class="lineage">
			<div class="lineage-item">
				<span class="lineage-icon">👪</span>
				<span class="lineage-value">{agent.childrenCount}</span>
				<span class="lineage-label">Children</span>
			</div>
			<div class="lineage-item">
				<span class="lineage-icon">🔬</span>
				<span class="lineage-value">{agent.mutationCount}</span>
				<span class="lineage-label">Mutations</span>
			</div>
			<div class="lineage-item">
				<span class="lineage-icon">💀</span>
				<span class="lineage-value">{agent.kills}</span>
				<span class="lineage-label">Kills</span>
			</div>
		</div>

		<!-- Actions -->
		{#if showActions && agent.status === 'alive'}
			<div class="actions">
				<button class="action-btn mutate" on:click={() => dispatch('mutate', agent)}>
					🧬 Mutate
				</button>
				<button class="action-btn breed" on:click={() => dispatch('breed', agent)}>
					💕 Breed
				</button>
				<button class="action-btn battle" on:click={() => dispatch('battle', agent)}>
					⚔️ Battle
				</button>
			</div>
		{/if}
	{/if}
</div>

<style>
	.profile-card {
		background: linear-gradient(135deg, rgba(10, 10, 26, 0.95) 0%, rgba(26, 26, 46, 0.95) 100%);
		border: 1px solid rgba(124, 158, 255, 0.2);
		border-radius: 20px;
		padding: 24px;
		backdrop-filter: blur(10px);
		transition: all 0.3s ease;
		position: relative;
		overflow: hidden;
	}

	.profile-card::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		height: 4px;
		background: linear-gradient(90deg, #7c9eff, #a855f7, #10b981);
	}

	.profile-card:hover {
		transform: translateY(-5px);
		box-shadow: 0 20px 60px rgba(124, 158, 255, 0.2);
	}

	.profile-card.dead {
		filter: grayscale(0.5);
		opacity: 0.8;
	}

	.profile-card.compact {
		padding: 16px;
	}

	.header {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		margin-bottom: 20px;
	}

	.avatar-section {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 8px;
	}

	.avatar {
		width: 80px;
		height: 80px;
		border-radius: 50%;
		background: linear-gradient(135deg, #7c9eff 0%, #a855f7 100%);
		display: flex;
		align-items: center;
		justify-content: center;
		border: 3px solid;
		position: relative;
	}

	.compact .avatar {
		width: 60px;
		height: 60px;
	}

	.avatar-letter {
		font-size: 36px;
		font-weight: bold;
		color: #fff;
	}

	.compact .avatar-letter {
		font-size: 28px;
	}

	.level-badge {
		position: absolute;
		bottom: -5px;
		right: -5px;
		background: #1a1a2e;
		border: 2px solid #7c9eff;
		border-radius: 10px;
		padding: 2px 8px;
		font-size: 11px;
		font-weight: bold;
		color: #7c9eff;
	}

	.status-badge {
		padding: 4px 12px;
		border-radius: 20px;
		font-size: 12px;
		font-weight: 600;
		color: #fff;
		text-transform: capitalize;
	}

	.fitness-ring {
		width: 90px;
		height: 90px;
		position: relative;
	}

	.compact .fitness-ring {
		width: 70px;
		height: 70px;
	}

	.fitness-ring svg {
		width: 100%;
		height: 100%;
		transform: rotate(-90deg);
	}

	.fitness-ring circle {
		fill: none;
		stroke-width: 8;
	}

	.fitness-ring .bg {
		stroke: rgba(255, 255, 255, 0.1);
	}

	.fitness-ring .progress {
		stroke-linecap: round;
		transition: stroke-dasharray 0.5s ease;
	}

	.fitness-center {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		text-align: center;
	}

	.grade {
		font-size: 24px;
		font-weight: bold;
		display: block;
	}

	.compact .grade {
		font-size: 18px;
	}

	.percent {
		font-size: 12px;
		color: #888;
	}

	.identity {
		text-align: center;
		margin-bottom: 20px;
	}

	.name {
		margin: 0 0 4px 0;
		font-size: 22px;
		font-weight: 700;
		color: #fff;
	}

	.compact .name {
		font-size: 18px;
	}

	.scientific-name {
		display: block;
		font-style: italic;
		font-size: 13px;
		color: #a855f7;
		margin-bottom: 4px;
	}

	.age {
		font-size: 12px;
		color: #666;
	}

	.stats-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 12px;
		margin-bottom: 20px;
	}

	.stat {
		background: rgba(124, 158, 255, 0.1);
		border-radius: 12px;
		padding: 12px 8px;
		text-align: center;
		transition: all 0.2s ease;
	}

	.stat:hover {
		background: rgba(124, 158, 255, 0.2);
		transform: scale(1.05);
	}

	.stat-icon {
		font-size: 20px;
		display: block;
		margin-bottom: 4px;
	}

	.stat-value {
		font-size: 18px;
		font-weight: bold;
		color: #fff;
		display: block;
	}

	.stat-label {
		font-size: 10px;
		color: #666;
		text-transform: uppercase;
		letter-spacing: 1px;
	}

	.combat-record {
		background: rgba(0, 0, 0, 0.2);
		border-radius: 12px;
		padding: 16px;
		margin-bottom: 20px;
	}

	.record-item {
		display: flex;
		align-items: center;
		gap: 12px;
		margin-bottom: 8px;
	}

	.record-label {
		font-size: 12px;
		color: #888;
		width: 70px;
	}

	.record-bar {
		flex: 1;
		height: 8px;
		background: rgba(255, 255, 255, 0.1);
		border-radius: 4px;
		overflow: hidden;
	}

	.record-fill {
		height: 100%;
		border-radius: 4px;
		transition: width 0.5s ease;
	}

	.record-value {
		font-size: 14px;
		font-weight: bold;
		color: #fff;
		width: 50px;
		text-align: right;
	}

	.record-stats {
		display: flex;
		justify-content: space-around;
		font-size: 12px;
	}

	.wins {
		color: #10b981;
	}

	.losses {
		color: #ef4444;
	}

	.kdr {
		color: #7c9eff;
	}

	.lineage {
		display: flex;
		justify-content: space-around;
		margin-bottom: 20px;
	}

	.lineage-item {
		text-align: center;
	}

	.lineage-icon {
		font-size: 24px;
		display: block;
		margin-bottom: 4px;
	}

	.lineage-value {
		font-size: 18px;
		font-weight: bold;
		color: #fff;
		display: block;
	}

	.lineage-label {
		font-size: 11px;
		color: #666;
	}

	.actions {
		display: flex;
		gap: 8px;
	}

	.action-btn {
		flex: 1;
		padding: 10px;
		border: none;
		border-radius: 10px;
		font-size: 13px;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.action-btn:hover {
		transform: translateY(-2px);
	}

	.action-btn.mutate {
		background: linear-gradient(135deg, #7c9eff, #6b8eff);
		color: #fff;
	}

	.action-btn.breed {
		background: linear-gradient(135deg, #a855f7, #9333ea);
		color: #fff;
	}

	.action-btn.battle {
		background: linear-gradient(135deg, #f97316, #ef4444);
		color: #fff;
	}

	.action-btn:active {
		transform: scale(0.98);
	}
</style>
