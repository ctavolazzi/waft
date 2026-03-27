<script lang="ts">
	import DNAViewer from '$lib/components/DNAViewer.svelte';
	import Leaderboard from '$lib/components/Leaderboard.svelte';
	import AgentProfileCard from '$lib/components/AgentProfileCard.svelte';
	import FitnessDashboard from '$lib/components/FitnessDashboard.svelte';
	export let params: Record<string, string> | undefined = undefined;
	void params;

	// Mock data for demonstration
	const mockAgents = [
		{
			id: '1',
			name: 'Alpha-Prime',
			fitness: 0.95,
			generation: 15,
			wins: 47,
			losses: 3,
			kills: 89,
			deaths: 2,
			status: 'alive' as const,
			createdAt: new Date(Date.now() - 86400000 * 5).toISOString(),
			mutationCount: 127,
			childrenCount: 23,
			traits: { attack: 24, defense: 18, speed: 22, adaptability: 14 }
		},
		{
			id: '2',
			name: 'Beta-Evolve',
			fitness: 0.87,
			generation: 12,
			wins: 35,
			losses: 8,
			kills: 62,
			deaths: 5,
			status: 'alive' as const,
			createdAt: new Date(Date.now() - 86400000 * 3).toISOString(),
			mutationCount: 98,
			childrenCount: 15,
			traits: { attack: 20, defense: 22, speed: 18, adaptability: 12 }
		},
		{
			id: '3',
			name: 'Gamma-Storm',
			fitness: 0.82,
			generation: 10,
			wins: 28,
			losses: 12,
			kills: 45,
			deaths: 8,
			status: 'alive' as const,
			createdAt: new Date(Date.now() - 86400000 * 2).toISOString(),
			mutationCount: 76,
			childrenCount: 8,
			traits: { attack: 18, defense: 15, speed: 24, adaptability: 16 }
		},
		{
			id: '4',
			name: 'Delta-Force',
			fitness: 0.75,
			generation: 8,
			wins: 20,
			losses: 15,
			kills: 33,
			deaths: 10,
			status: 'evolved' as const,
			createdAt: new Date(Date.now() - 86400000 * 4).toISOString(),
			mutationCount: 54,
			childrenCount: 12,
			traits: { attack: 22, defense: 12, speed: 16, adaptability: 10 }
		},
		{
			id: '5',
			name: 'Epsilon-Zero',
			fitness: 0.68,
			generation: 6,
			wins: 15,
			losses: 18,
			kills: 22,
			deaths: 12,
			status: 'dead' as const,
			createdAt: new Date(Date.now() - 86400000 * 6).toISOString(),
			mutationCount: 42,
			childrenCount: 5,
			traits: { attack: 14, defense: 20, speed: 12, adaptability: 8 }
		}
	];

	const mockGenome = {
		id: 'genome-alpha',
		name: 'Alpha-Prime',
		generation: 15,
		fitness: 0.95,
		genes: {
			font: { size_h1: 32, size_body: 14, line_height: 1.6 },
			margin: { top: 30, bottom: 25, paragraph_spacing: 14 },
			color: { text: '#1a1a2e', background: '#f8f9fa', accent: '#7c9eff' },
			layout: { columns: 2, density: 'spacious' }
		}
	};

	const fitnessHistory = Array.from({ length: 15 }, (_, i) => ({
		generation: i + 1,
		bestFitness: 0.4 + (i / 15) * 0.5 + Math.random() * 0.1,
		avgFitness: 0.3 + (i / 15) * 0.4 + Math.random() * 0.1,
		worstFitness: 0.1 + (i / 15) * 0.2 + Math.random() * 0.1,
		population: 15 + i * 3 + Math.floor(Math.random() * 5)
	}));

	let selectedAgent = mockAgents[0];
</script>

<svelte:head>
	<title>WAFT Demo - Evolution Visualization</title>
</svelte:head>

<div class="demo-page">
	<header class="demo-header">
		<h1>🧬 WAFT Evolution Demo</h1>
		<p>Interactive visualization of the genetic evolution system</p>
	</header>

	<div class="demo-grid">
		<!-- DNA Viewer Section -->
		<section class="demo-section dna-section">
			<h2>🔬 DNA Viewer</h2>
			<p class="section-desc">Visualize genome traits as a DNA double helix</p>
			<div class="dna-container">
				<DNAViewer genome={mockGenome} width={400} height={550} />
			</div>
		</section>

		<!-- Agent Profile Section -->
		<section class="demo-section profile-section">
			<h2>👤 Agent Profile</h2>
			<p class="section-desc">Detailed agent stats and combat record</p>
			<AgentProfileCard
				agent={selectedAgent}
				on:mutate={() => alert('Mutate clicked!')}
				on:breed={() => alert('Breed clicked!')}
				on:battle={() => alert('Battle clicked!')}
			/>
		</section>

		<!-- Leaderboard Section -->
		<section class="demo-section leaderboard-section">
			<h2>🏆 Leaderboard</h2>
			<p class="section-desc">Real-time agent rankings with animated updates</p>
			<Leaderboard agents={mockAgents} maxDisplay={5} />
		</section>

		<!-- Fitness Dashboard Section -->
		<section class="demo-section fitness-section">
			<h2>📈 Fitness Evolution</h2>
			<p class="section-desc">Track population fitness over generations</p>
			<FitnessDashboard data={fitnessHistory} title="" />
		</section>
	</div>

	<footer class="demo-footer">
		<p>
			<strong>33 Achievements</strong> to unlock •
			<strong>7 Crossover Strategies</strong> •
			<strong>Battle Royale Mode</strong>
		</p>
		<div class="links">
			<a href="/arena">⚔️ Go to Arena</a>
			<a href="/stats">📊 Full Statistics</a>
			<a href="/">🏠 Dashboard</a>
		</div>
	</footer>
</div>

<style>
	.demo-page {
		min-height: 100vh;
		background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 50%, #0f0f23 100%);
		padding: 24px;
	}

	.demo-header {
		text-align: center;
		margin-bottom: 40px;
		padding: 40px 20px;
	}

	.demo-header h1 {
		font-size: 48px;
		font-weight: 800;
		background: linear-gradient(135deg, #7c9eff 0%, #a855f7 50%, #22d3ee 100%);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
		margin: 0 0 12px 0;
		animation: shimmer 3s ease-in-out infinite;
	}

	@keyframes shimmer {
		0%,
		100% {
			filter: brightness(1);
		}
		50% {
			filter: brightness(1.2);
		}
	}

	.demo-header p {
		color: #888;
		font-size: 18px;
		margin: 0;
	}

	.demo-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 32px;
		max-width: 1400px;
		margin: 0 auto;
	}

	.demo-section {
		background: rgba(10, 10, 26, 0.8);
		border: 1px solid rgba(124, 158, 255, 0.2);
		border-radius: 20px;
		padding: 24px;
		backdrop-filter: blur(10px);
	}

	.demo-section h2 {
		font-size: 22px;
		font-weight: 700;
		color: #fff;
		margin: 0 0 8px 0;
	}

	.section-desc {
		color: #666;
		font-size: 14px;
		margin: 0 0 20px 0;
	}

	.dna-container {
		display: flex;
		justify-content: center;
	}

	.demo-footer {
		text-align: center;
		margin-top: 60px;
		padding: 40px 20px;
		border-top: 1px solid rgba(124, 158, 255, 0.1);
	}

	.demo-footer p {
		color: #888;
		font-size: 16px;
		margin: 0 0 20px 0;
	}

	.demo-footer strong {
		color: #7c9eff;
	}

	.links {
		display: flex;
		gap: 20px;
		justify-content: center;
	}

	.links a {
		background: linear-gradient(135deg, rgba(124, 158, 255, 0.2), rgba(168, 85, 247, 0.2));
		border: 1px solid rgba(124, 158, 255, 0.3);
		color: #fff;
		padding: 12px 24px;
		border-radius: 12px;
		text-decoration: none;
		font-weight: 600;
		transition: all 0.3s ease;
	}

	.links a:hover {
		transform: translateY(-3px);
		box-shadow: 0 10px 30px rgba(124, 158, 255, 0.3);
		border-color: #7c9eff;
	}

	@media (max-width: 1024px) {
		.demo-grid {
			grid-template-columns: 1fr;
		}
	}

	@media (max-width: 640px) {
		.demo-header h1 {
			font-size: 32px;
		}

		.links {
			flex-direction: column;
			align-items: center;
		}
	}
</style>
