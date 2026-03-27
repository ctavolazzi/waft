<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import DNAViewer from '$lib/components/DNAViewer.svelte';
	import Leaderboard from '$lib/components/Leaderboard.svelte';
	import AgentProfileCard from '$lib/components/AgentProfileCard.svelte';
	import FitnessDashboard from '$lib/components/FitnessDashboard.svelte';
	import EvolutionTree from '$lib/components/EvolutionTree.svelte';
	export let params: Record<string, string> | undefined = undefined;
	void params;

	// Mock data for demonstration
	let selectedAgent: any = null;
	let agents: any[] = [];
	let fitnessHistory: any[] = [];
	let achievements: any[] = [];
	let stats = {
		totalGenomes: 0,
		totalGenerations: 0,
		totalBattles: 0,
		totalCrossovers: 0,
		highestFitness: 0,
		averageFitness: 0,
		mostKills: 0,
		longestLineage: 0
	};

	let loading = true;
	let activeTab: 'overview' | 'leaderboard' | 'dna' | 'tree' | 'achievements' = 'overview';

	// Fetch data from API
	async function fetchData() {
		loading = true;
		try {
			// Fetch population stats
			const statsRes = await fetch('/api/evolution/population/stats');
			if (statsRes.ok) {
				const data = await statsRes.json();
				stats = {
					totalGenomes: data.total_genomes || 0,
					totalGenerations: data.max_generation || 0,
					totalBattles: data.total_battles || 0,
					totalCrossovers: data.total_crossovers || 0,
					highestFitness: data.highest_fitness || 0,
					averageFitness: data.average_fitness || 0,
					mostKills: data.most_kills || 0,
					longestLineage: data.longest_lineage || 0
				};
			}

			// Fetch all genomes for leaderboard
			const genomesRes = await fetch('/api/evolution/genomes');
			if (genomesRes.ok) {
				const data = await genomesRes.json();
				agents = (data.genomes || []).map((g: any) => ({
					id: g.id,
					name: g.name || g.scientific_name || 'Unknown',
					fitness: g.fitness || 0,
					generation: g.generation || 1,
					wins: g.wins || 0,
					losses: g.losses || 0,
					kills: g.kills || 0,
					deaths: g.deaths || 0,
					status: g.status || 'alive',
					createdAt: g.created_at || new Date().toISOString(),
					mutationCount: g.mutations || 0,
					childrenCount: g.children || 0,
					traits: {
						attack: Math.round((g.fitness || 0.5) * 20),
						defense: Math.round((g.fitness || 0.5) * 15),
						speed: Math.round((g.fitness || 0.5) * 18),
						adaptability: Math.round((g.fitness || 0.5) * 10)
					}
				}));

				// Select top agent by default
				if (agents.length > 0) {
					selectedAgent = agents.reduce((a, b) => (a.fitness > b.fitness ? a : b));
				}
			}

			// Generate mock fitness history
			fitnessHistory = Array.from({ length: 20 }, (_, i) => ({
				generation: i + 1,
				bestFitness: 0.3 + Math.random() * 0.6,
				avgFitness: 0.2 + Math.random() * 0.4,
				worstFitness: Math.random() * 0.3,
				population: 10 + Math.floor(Math.random() * 40)
			}));

			// Mock achievements
			achievements = [
				{
					id: 'first_mutation',
					name: 'First Steps',
					icon: '🧬',
					unlocked: true,
					rarity: 'common'
				},
				{
					id: 'first_blood',
					name: 'First Blood',
					icon: '⚔️',
					unlocked: true,
					rarity: 'common'
				},
				{
					id: 'fitness_80',
					name: 'High Achiever',
					icon: '📈',
					unlocked: stats.highestFitness >= 0.8,
					rarity: 'rare'
				},
				{
					id: 'champion',
					name: 'Champion',
					icon: '🏆',
					unlocked: false,
					rarity: 'rare'
				},
				{
					id: 'perfect_fitness',
					name: 'Perfection',
					icon: '⭐',
					unlocked: stats.highestFitness >= 1.0,
					rarity: 'legendary'
				}
			];
		} catch (error) {
			console.error('Failed to fetch data:', error);
			// Use mock data on error
			generateMockData();
		}
		loading = false;
	}

	function generateMockData() {
		agents = Array.from({ length: 15 }, (_, i) => ({
			id: `agent-${i}`,
			name: `Agent-${String.fromCharCode(65 + i)}`,
			fitness: 0.3 + Math.random() * 0.7,
			generation: Math.floor(Math.random() * 10) + 1,
			wins: Math.floor(Math.random() * 20),
			losses: Math.floor(Math.random() * 10),
			kills: Math.floor(Math.random() * 30),
			deaths: Math.floor(Math.random() * 5),
			status: Math.random() > 0.2 ? 'alive' : 'dead',
			createdAt: new Date(Date.now() - Math.random() * 86400000 * 7).toISOString(),
			mutationCount: Math.floor(Math.random() * 50),
			childrenCount: Math.floor(Math.random() * 10),
			traits: {
				attack: Math.floor(Math.random() * 25),
				defense: Math.floor(Math.random() * 20),
				speed: Math.floor(Math.random() * 22),
				adaptability: Math.floor(Math.random() * 15)
			}
		}));

		if (agents.length > 0) {
			selectedAgent = agents[0];
		}

		stats = {
			totalGenomes: agents.length,
			totalGenerations: Math.max(...agents.map((a) => a.generation)),
			totalBattles: agents.reduce((sum, a) => sum + a.wins + a.losses, 0),
			totalCrossovers: Math.floor(agents.length * 1.5),
			highestFitness: Math.max(...agents.map((a) => a.fitness)),
			averageFitness: agents.reduce((sum, a) => sum + a.fitness, 0) / agents.length,
			mostKills: Math.max(...agents.map((a) => a.kills)),
			longestLineage: Math.max(...agents.map((a) => a.generation))
		};

		fitnessHistory = Array.from({ length: 20 }, (_, i) => ({
			generation: i + 1,
			bestFitness: 0.3 + Math.random() * 0.6,
			avgFitness: 0.2 + Math.random() * 0.4,
			worstFitness: Math.random() * 0.3,
			population: 10 + Math.floor(Math.random() * 40)
		}));
	}

	onMount(() => {
		fetchData();
	});

	function handleMutate(event: CustomEvent) {
		console.log('Mutate:', event.detail);
	}

	function handleBreed(event: CustomEvent) {
		console.log('Breed:', event.detail);
	}

	function handleBattle(event: CustomEvent) {
		console.log('Battle:', event.detail);
	}
</script>

<svelte:head>
	<title>Evolution Statistics - WAFT</title>
</svelte:head>

<div class="stats-page">
	<header class="page-header">
		<h1>📊 Evolution Statistics</h1>
		<p>Deep dive into the evolutionary data of your agent population</p>
	</header>

	<!-- Tab Navigation -->
	<nav class="tabs">
		<button class:active={activeTab === 'overview'} on:click={() => (activeTab = 'overview')}>
			📈 Overview
		</button>
		<button
			class:active={activeTab === 'leaderboard'}
			on:click={() => (activeTab = 'leaderboard')}
		>
			🏆 Leaderboard
		</button>
		<button class:active={activeTab === 'dna'} on:click={() => (activeTab = 'dna')}>
			🧬 DNA Viewer
		</button>
		<button class:active={activeTab === 'tree'} on:click={() => (activeTab = 'tree')}>
			🌳 Family Tree
		</button>
		<button
			class:active={activeTab === 'achievements'}
			on:click={() => (activeTab = 'achievements')}
		>
			🏅 Achievements
		</button>
	</nav>

	{#if loading}
		<div class="loading">
			<div class="spinner"></div>
			<span>Loading evolution data...</span>
		</div>
	{:else}
		<!-- Overview Tab -->
		{#if activeTab === 'overview'}
			<div class="overview-grid">
				<!-- Quick Stats -->
				<div class="stats-cards">
					<div class="stat-card">
						<span class="stat-icon">🧬</span>
						<span class="stat-value">{stats.totalGenomes}</span>
						<span class="stat-label">Total Genomes</span>
					</div>
					<div class="stat-card">
						<span class="stat-icon">🔄</span>
						<span class="stat-value">{stats.totalGenerations}</span>
						<span class="stat-label">Generations</span>
					</div>
					<div class="stat-card">
						<span class="stat-icon">⚔️</span>
						<span class="stat-value">{stats.totalBattles}</span>
						<span class="stat-label">Battles</span>
					</div>
					<div class="stat-card">
						<span class="stat-icon">💕</span>
						<span class="stat-value">{stats.totalCrossovers}</span>
						<span class="stat-label">Crossovers</span>
					</div>
					<div class="stat-card highlight">
						<span class="stat-icon">⭐</span>
						<span class="stat-value">{(stats.highestFitness * 100).toFixed(1)}%</span>
						<span class="stat-label">Peak Fitness</span>
					</div>
					<div class="stat-card">
						<span class="stat-icon">📊</span>
						<span class="stat-value">{(stats.averageFitness * 100).toFixed(1)}%</span>
						<span class="stat-label">Avg Fitness</span>
					</div>
					<div class="stat-card">
						<span class="stat-icon">💀</span>
						<span class="stat-value">{stats.mostKills}</span>
						<span class="stat-label">Most Kills</span>
					</div>
					<div class="stat-card">
						<span class="stat-icon">🌳</span>
						<span class="stat-value">{stats.longestLineage}</span>
						<span class="stat-label">Longest Line</span>
					</div>
				</div>

				<!-- Fitness Chart -->
				<div class="chart-section">
					<h2>Fitness Evolution</h2>
					<FitnessDashboard data={fitnessHistory} title="" />
				</div>

				<!-- Top Agent -->
				{#if selectedAgent}
					<div class="top-agent-section">
						<h2>Top Performer</h2>
						<AgentProfileCard
							agent={selectedAgent}
							on:mutate={handleMutate}
							on:breed={handleBreed}
							on:battle={handleBattle}
						/>
					</div>
				{/if}
			</div>
		{/if}

		<!-- Leaderboard Tab -->
		{#if activeTab === 'leaderboard'}
			<div class="leaderboard-section">
				<Leaderboard {agents} maxDisplay={20} title="Evolution Leaderboard" />
			</div>
		{/if}

		<!-- DNA Viewer Tab -->
		{#if activeTab === 'dna'}
			<div class="dna-section">
				<div class="dna-sidebar">
					<h3>Select Agent</h3>
					<div class="agent-list">
						{#each agents.slice(0, 10) as agent}
							<button
								class="agent-item"
								class:selected={selectedAgent?.id === agent.id}
								on:click={() => {
									selectedAgent = {
										...agent,
										genes: {
											font: {
												size_h1: 24 + Math.random() * 12,
												size_body: 11 + Math.random() * 3,
												line_height: 1.4 + Math.random() * 0.4
											},
											margin: {
												top: 20 + Math.random() * 20,
												bottom: 20 + Math.random() * 20,
												paragraph_spacing: 8 + Math.random() * 8
											},
											color: {
												text: '#' + Math.floor(Math.random() * 16777215).toString(16),
												background:
													'#' + Math.floor(Math.random() * 16777215).toString(16),
												accent: '#' + Math.floor(Math.random() * 16777215).toString(16)
											},
											layout: {
												columns: Math.floor(Math.random() * 3) + 1,
												density: Math.random() > 0.5 ? 'compact' : 'spacious'
											}
										}
									};
								}}
							>
								<span class="agent-name">{agent.name}</span>
								<span class="agent-fitness">{(agent.fitness * 100).toFixed(0)}%</span>
							</button>
						{/each}
					</div>
				</div>
				<div class="dna-main">
					<DNAViewer
						genome={selectedAgent
							? {
									id: selectedAgent.id,
									name: selectedAgent.name,
									generation: selectedAgent.generation,
									fitness: selectedAgent.fitness,
									genes: selectedAgent.genes || {
										font: { size_h1: 28, size_body: 12, line_height: 1.6 },
										margin: { top: 25, bottom: 25, paragraph_spacing: 12 },
										color: { text: '#333333', background: '#ffffff', accent: '#7c9eff' },
										layout: { columns: 1, density: 'spacious' }
									}
								}
							: null}
						width={500}
						height={700}
					/>
				</div>
			</div>
		{/if}

		<!-- Family Tree Tab -->
		{#if activeTab === 'tree'}
			<div class="tree-section">
				<EvolutionTree
					agents={agents.map((a) => ({
						id: a.id,
						name: a.name,
						generation: a.generation,
						parentId: null,
						fitness: a.fitness,
						status: a.status,
						mutations: [],
						createdAt: a.createdAt
					}))}
					selectedAgent={selectedAgent?.id}
				/>
			</div>
		{/if}

		<!-- Achievements Tab -->
		{#if activeTab === 'achievements'}
			<div class="achievements-section">
				<div class="achievements-header">
					<h2>🏅 Achievements</h2>
					<span class="unlock-count"
						>{achievements.filter((a) => a.unlocked).length}/{achievements.length} Unlocked</span
					>
				</div>
				<div class="achievements-grid">
					{#each achievements as achievement}
						<div class="achievement-card" class:locked={!achievement.unlocked}>
							<div class="achievement-icon">{achievement.unlocked ? achievement.icon : '🔒'}</div>
							<div class="achievement-info">
								<span class="achievement-name">{achievement.name}</span>
								<span class="achievement-rarity {achievement.rarity}">{achievement.rarity}</span>
							</div>
							{#if achievement.unlocked}
								<span class="checkmark">✓</span>
							{/if}
						</div>
					{/each}
				</div>
			</div>
		{/if}
	{/if}
</div>

<style>
	.stats-page {
		padding: 24px;
		max-width: 1400px;
		margin: 0 auto;
	}

	.page-header {
		text-align: center;
		margin-bottom: 32px;
	}

	.page-header h1 {
		font-size: 36px;
		font-weight: 800;
		background: linear-gradient(135deg, #7c9eff, #a855f7);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
		margin: 0 0 8px 0;
	}

	.page-header p {
		color: #888;
		font-size: 16px;
	}

	.tabs {
		display: flex;
		gap: 8px;
		margin-bottom: 24px;
		flex-wrap: wrap;
		justify-content: center;
	}

	.tabs button {
		background: rgba(124, 158, 255, 0.1);
		border: 1px solid rgba(124, 158, 255, 0.2);
		color: #888;
		padding: 12px 24px;
		border-radius: 12px;
		font-size: 14px;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.tabs button:hover {
		background: rgba(124, 158, 255, 0.2);
		color: #fff;
	}

	.tabs button.active {
		background: linear-gradient(135deg, #7c9eff, #a855f7);
		border-color: transparent;
		color: #fff;
	}

	.loading {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 60px;
		color: #888;
	}

	.spinner {
		width: 40px;
		height: 40px;
		border: 3px solid rgba(124, 158, 255, 0.2);
		border-top-color: #7c9eff;
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: 16px;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	/* Overview Grid */
	.overview-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 24px;
	}

	.stats-cards {
		grid-column: span 2;
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 16px;
	}

	.stat-card {
		background: rgba(10, 10, 26, 0.8);
		border: 1px solid rgba(124, 158, 255, 0.2);
		border-radius: 16px;
		padding: 20px;
		text-align: center;
		transition: all 0.3s ease;
	}

	.stat-card:hover {
		transform: translateY(-3px);
		border-color: rgba(124, 158, 255, 0.4);
	}

	.stat-card.highlight {
		background: linear-gradient(135deg, rgba(124, 158, 255, 0.2), rgba(168, 85, 247, 0.2));
		border-color: #7c9eff;
	}

	.stat-icon {
		font-size: 28px;
		display: block;
		margin-bottom: 8px;
	}

	.stat-value {
		font-size: 28px;
		font-weight: 800;
		color: #fff;
		display: block;
	}

	.stat-label {
		font-size: 12px;
		color: #666;
		text-transform: uppercase;
		letter-spacing: 1px;
	}

	.chart-section,
	.top-agent-section {
		background: rgba(10, 10, 26, 0.8);
		border: 1px solid rgba(124, 158, 255, 0.2);
		border-radius: 16px;
		padding: 24px;
	}

	.chart-section h2,
	.top-agent-section h2 {
		margin: 0 0 16px 0;
		font-size: 18px;
		color: #fff;
	}

	/* Leaderboard Section */
	.leaderboard-section {
		max-width: 800px;
		margin: 0 auto;
	}

	/* DNA Section */
	.dna-section {
		display: grid;
		grid-template-columns: 250px 1fr;
		gap: 24px;
	}

	.dna-sidebar {
		background: rgba(10, 10, 26, 0.8);
		border: 1px solid rgba(124, 158, 255, 0.2);
		border-radius: 16px;
		padding: 20px;
	}

	.dna-sidebar h3 {
		margin: 0 0 16px 0;
		font-size: 16px;
		color: #fff;
	}

	.agent-list {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.agent-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid transparent;
		border-radius: 10px;
		padding: 12px;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.agent-item:hover {
		background: rgba(124, 158, 255, 0.1);
	}

	.agent-item.selected {
		background: rgba(124, 158, 255, 0.2);
		border-color: #7c9eff;
	}

	.agent-name {
		font-weight: 600;
		color: #fff;
	}

	.agent-fitness {
		color: #7c9eff;
		font-weight: bold;
	}

	.dna-main {
		display: flex;
		justify-content: center;
		align-items: flex-start;
	}

	/* Tree Section */
	.tree-section {
		background: rgba(10, 10, 26, 0.8);
		border: 1px solid rgba(124, 158, 255, 0.2);
		border-radius: 16px;
		padding: 24px;
		min-height: 600px;
	}

	/* Achievements Section */
	.achievements-section {
		max-width: 900px;
		margin: 0 auto;
	}

	.achievements-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 24px;
	}

	.achievements-header h2 {
		margin: 0;
		font-size: 24px;
		color: #fff;
	}

	.unlock-count {
		background: rgba(124, 158, 255, 0.2);
		padding: 8px 16px;
		border-radius: 20px;
		font-size: 14px;
		color: #7c9eff;
	}

	.achievements-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
		gap: 16px;
	}

	.achievement-card {
		display: flex;
		align-items: center;
		gap: 16px;
		background: rgba(10, 10, 26, 0.8);
		border: 1px solid rgba(124, 158, 255, 0.2);
		border-radius: 12px;
		padding: 16px;
		transition: all 0.3s ease;
		position: relative;
	}

	.achievement-card:hover {
		transform: translateY(-2px);
		border-color: rgba(124, 158, 255, 0.4);
	}

	.achievement-card.locked {
		opacity: 0.5;
		filter: grayscale(0.5);
	}

	.achievement-icon {
		font-size: 32px;
		width: 50px;
		height: 50px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: rgba(255, 255, 255, 0.05);
		border-radius: 12px;
	}

	.achievement-info {
		flex: 1;
	}

	.achievement-name {
		display: block;
		font-weight: 600;
		color: #fff;
		margin-bottom: 4px;
	}

	.achievement-rarity {
		font-size: 11px;
		text-transform: uppercase;
		letter-spacing: 1px;
		padding: 2px 8px;
		border-radius: 4px;
	}

	.achievement-rarity.common {
		background: rgba(107, 114, 128, 0.3);
		color: #9ca3af;
	}

	.achievement-rarity.uncommon {
		background: rgba(16, 185, 129, 0.3);
		color: #10b981;
	}

	.achievement-rarity.rare {
		background: rgba(59, 130, 246, 0.3);
		color: #3b82f6;
	}

	.achievement-rarity.epic {
		background: rgba(168, 85, 247, 0.3);
		color: #a855f7;
	}

	.achievement-rarity.legendary {
		background: rgba(255, 215, 0, 0.3);
		color: #ffd700;
	}

	.checkmark {
		position: absolute;
		top: 10px;
		right: 10px;
		color: #10b981;
		font-weight: bold;
	}

	@media (max-width: 768px) {
		.overview-grid {
			grid-template-columns: 1fr;
		}

		.stats-cards {
			grid-column: 1;
			grid-template-columns: repeat(2, 1fr);
		}

		.dna-section {
			grid-template-columns: 1fr;
		}

		.tabs {
			justify-content: flex-start;
			overflow-x: auto;
		}
	}
</style>
