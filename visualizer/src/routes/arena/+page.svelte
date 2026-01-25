<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import EvolutionTree from '$lib/components/EvolutionTree.svelte';

	interface Agent {
		id: string;
		name: string;
		health: number;
		maxHealth: number;
		attack: number;
		defense: number;
		fitness: number;
		status: 'ready' | 'fighting' | 'winner' | 'defeated';
		kills: number;
		damageDealt: number;
	}

	interface BattleLog {
		timestamp: number;
		type: 'attack' | 'defend' | 'special' | 'death' | 'system';
		actor?: string;
		target?: string;
		damage?: number;
		message: string;
	}

	let agents: Agent[] = [];
	let battleLogs: BattleLog[] = [];
	let battleInProgress = false;
	let currentRound = 0;
	let battleId = '';
	let winner: Agent | null = null;
	let animationFrame: number;
	let battleSpeed = 1;

	// Generate sample agents for demo
	function generateAgents(): Agent[] {
		const names = [
			'Quantum Striker', 'Nova Prime', 'Stellar Void', 'Cosmic Blade',
			'Nebula Storm', 'Solar Flare', 'Gravity Well', 'Dark Matter',
		];
		return names.slice(0, 4).map((name, i) => ({
			id: `agent-${i}`,
			name,
			health: 100,
			maxHealth: 100,
			attack: 15 + Math.random() * 10,
			defense: 5 + Math.random() * 5,
			fitness: 0.5 + Math.random() * 0.5,
			status: 'ready',
			kills: 0,
			damageDealt: 0,
		}));
	}

	function addLog(log: Omit<BattleLog, 'timestamp'>) {
		battleLogs = [...battleLogs, { ...log, timestamp: Date.now() }];
	}

	async function startBattle() {
		agents = generateAgents();
		battleLogs = [];
		battleInProgress = true;
		currentRound = 0;
		winner = null;
		battleId = `battle-${Date.now().toString(36)}`;

		addLog({
			type: 'system',
			message: `Battle Royale "${battleId}" has begun with ${agents.length} combatants!`,
		});

		// Set all agents to fighting
		agents = agents.map(a => ({ ...a, status: 'fighting' as const }));

		// Run battle simulation
		await runBattle();
	}

	async function runBattle() {
		while (battleInProgress) {
			currentRound++;
			const aliveAgents = agents.filter(a => a.health > 0);

			if (aliveAgents.length <= 1) {
				endBattle(aliveAgents[0] || null);
				return;
			}

			addLog({
				type: 'system',
				message: `--- Round ${currentRound} ---`,
			});

			// Each alive agent takes an action
			for (const agent of aliveAgents) {
				if (!battleInProgress) return;

				const targets = aliveAgents.filter(a => a.id !== agent.id && a.health > 0);
				if (targets.length === 0) continue;

				const target = targets[Math.floor(Math.random() * targets.length)];
				const action = Math.random();

				if (action < 0.7) {
					// Attack
					const damage = Math.max(1, agent.attack * (0.8 + Math.random() * 0.4) - target.defense * 0.3);
					const roundedDamage = Math.round(damage * 10) / 10;

					target.health = Math.max(0, target.health - roundedDamage);
					agent.damageDealt += roundedDamage;

					addLog({
						type: 'attack',
						actor: agent.name,
						target: target.name,
						damage: roundedDamage,
						message: `${agent.name} attacks ${target.name} for ${roundedDamage.toFixed(1)} damage!`,
					});

					if (target.health <= 0) {
						target.status = 'defeated';
						agent.kills++;
						addLog({
							type: 'death',
							actor: agent.name,
							target: target.name,
							message: `${target.name} has been eliminated by ${agent.name}!`,
						});
					}
				} else if (action < 0.85) {
					// Special attack
					const damage = agent.attack * 1.5 * (0.9 + Math.random() * 0.2);
					const roundedDamage = Math.round(damage * 10) / 10;

					target.health = Math.max(0, target.health - roundedDamage);
					agent.damageDealt += roundedDamage;

					addLog({
						type: 'special',
						actor: agent.name,
						target: target.name,
						damage: roundedDamage,
						message: `${agent.name} unleashes SPECIAL ATTACK on ${target.name} for ${roundedDamage.toFixed(1)} damage!`,
					});

					if (target.health <= 0) {
						target.status = 'defeated';
						agent.kills++;
						addLog({
							type: 'death',
							actor: agent.name,
							target: target.name,
							message: `${target.name} has been eliminated by ${agent.name}!`,
						});
					}
				} else {
					// Defend/heal
					const heal = Math.min(agent.maxHealth - agent.health, 10 + Math.random() * 10);
					agent.health += heal;
					addLog({
						type: 'defend',
						actor: agent.name,
						message: `${agent.name} regenerates ${heal.toFixed(1)} health!`,
					});
				}

				agents = [...agents]; // Trigger reactivity
			}

			// Delay between rounds
			await new Promise(resolve => setTimeout(resolve, 500 / battleSpeed));
		}
	}

	function endBattle(winningAgent: Agent | null) {
		battleInProgress = false;

		if (winningAgent) {
			winningAgent.status = 'winner';
			winner = winningAgent;
			addLog({
				type: 'system',
				message: `VICTORY! ${winningAgent.name} wins the Battle Royale with ${winningAgent.kills} kills!`,
			});
		} else {
			addLog({
				type: 'system',
				message: 'Battle ended with no survivors!',
			});
		}

		agents = [...agents];
	}

	function stopBattle() {
		battleInProgress = false;
		addLog({
			type: 'system',
			message: 'Battle has been stopped.',
		});
	}

	function getHealthColor(health: number, maxHealth: number): string {
		const percent = health / maxHealth;
		if (percent > 0.6) return 'var(--success)';
		if (percent > 0.3) return 'var(--warning)';
		return 'var(--error)';
	}

	function getStatusColor(status: string): string {
		switch (status) {
			case 'ready': return 'var(--info)';
			case 'fighting': return 'var(--warning)';
			case 'winner': return 'var(--success)';
			case 'defeated': return 'var(--error)';
			default: return 'var(--text-muted)';
		}
	}

	onMount(() => {
		agents = generateAgents();
	});

	onDestroy(() => {
		battleInProgress = false;
	});
</script>

<svelte:head>
	<title>Battle Arena - WAFT</title>
</svelte:head>

<div class="arena-container">
	<header class="arena-header">
		<div class="header-content">
			<h1 class="title text-gradient">Battle Royale Arena</h1>
			<p class="subtitle">Agent vs Agent Combat Evolution</p>
		</div>
		<div class="controls">
			<div class="speed-control">
				<label>Speed:</label>
				<input type="range" min="0.5" max="5" step="0.5" bind:value={battleSpeed} />
				<span>{battleSpeed}x</span>
			</div>
			{#if battleInProgress}
				<button class="btn btn-danger" on:click={stopBattle}>Stop Battle</button>
			{:else}
				<button class="btn btn-primary animate-glow" on:click={startBattle}>Start Battle</button>
			{/if}
		</div>
	</header>

	<div class="arena-grid">
		<!-- Combatants Panel -->
		<section class="combatants-panel card">
			<h2>Combatants</h2>
			<div class="combatants-list">
				{#each agents as agent (agent.id)}
					<div class="combatant-card" class:defeated={agent.status === 'defeated'} class:winner={agent.status === 'winner'}>
						<div class="combatant-header">
							<span class="combatant-name">{agent.name}</span>
							<span class="status-badge" style="background: {getStatusColor(agent.status)}">{agent.status}</span>
						</div>

						<div class="health-bar-container">
							<div
								class="health-bar"
								style="width: {(agent.health / agent.maxHealth) * 100}%; background: {getHealthColor(agent.health, agent.maxHealth)}"
							></div>
							<span class="health-text">{agent.health.toFixed(0)} / {agent.maxHealth}</span>
						</div>

						<div class="stats-row">
							<div class="stat">
								<span class="stat-label">ATK</span>
								<span class="stat-value">{agent.attack.toFixed(1)}</span>
							</div>
							<div class="stat">
								<span class="stat-label">DEF</span>
								<span class="stat-value">{agent.defense.toFixed(1)}</span>
							</div>
							<div class="stat">
								<span class="stat-label">FIT</span>
								<span class="stat-value">{(agent.fitness * 100).toFixed(0)}%</span>
							</div>
						</div>

						<div class="combat-stats">
							<span>Kills: {agent.kills}</span>
							<span>Damage: {agent.damageDealt.toFixed(0)}</span>
						</div>
					</div>
				{/each}
			</div>
		</section>

		<!-- Battle Arena Visualization -->
		<section class="arena-visualization card">
			<h2>Battle Arena</h2>
			<div class="arena-canvas">
				{#if winner}
					<div class="winner-announcement animate-scale-in">
						<div class="crown">👑</div>
						<h3>CHAMPION</h3>
						<div class="winner-name text-gradient">{winner.name}</div>
						<div class="winner-stats">
							<span>{winner.kills} Kills</span>
							<span>{winner.damageDealt.toFixed(0)} Damage</span>
						</div>
					</div>
				{:else if battleInProgress}
					<div class="battle-status">
						<div class="round-indicator">Round {currentRound}</div>
						<div class="alive-count">{agents.filter(a => a.health > 0).length} Combatants Remaining</div>
					</div>
					<div class="battle-animation">
						{#each agents.filter(a => a.health > 0) as agent, i}
							<div
								class="fighter-avatar"
								style="
									animation-delay: {i * 0.2}s;
									--x: {Math.cos(i * (Math.PI * 2 / agents.filter(a => a.health > 0).length)) * 100}px;
									--y: {Math.sin(i * (Math.PI * 2 / agents.filter(a => a.health > 0).length)) * 80}px;
								"
							>
								<div class="avatar-circle" style="border-color: {getHealthColor(agent.health, agent.maxHealth)}">
									{agent.name.charAt(0)}
								</div>
								<div class="avatar-health" style="width: {(agent.health / agent.maxHealth) * 100}%"></div>
							</div>
						{/each}
					</div>
				{:else}
					<div class="arena-idle">
						<div class="idle-icon">⚔️</div>
						<p>Ready for Battle</p>
						<p class="idle-hint">Click "Start Battle" to begin</p>
					</div>
				{/if}
			</div>
		</section>

		<!-- Battle Log -->
		<section class="battle-log card">
			<h2>Battle Log</h2>
			<div class="log-container">
				{#each battleLogs.slice().reverse() as log (log.timestamp)}
					<div class="log-entry animate-fade-in-up" class:log-attack={log.type === 'attack'} class:log-special={log.type === 'special'} class:log-death={log.type === 'death'} class:log-system={log.type === 'system'} class:log-defend={log.type === 'defend'}>
						<span class="log-time">{new Date(log.timestamp).toLocaleTimeString()}</span>
						<span class="log-message">{log.message}</span>
					</div>
				{/each}
				{#if battleLogs.length === 0}
					<div class="log-empty">No battle events yet...</div>
				{/if}
			</div>
		</section>
	</div>
</div>

<style>
	.arena-container {
		max-width: 1600px;
		margin: 0 auto;
		padding: 2rem;
	}

	.arena-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 2rem;
		padding: 1.5rem;
		background: var(--bg-glass);
		backdrop-filter: blur(20px);
		border-radius: var(--radius-lg);
		border: 1px solid var(--border);
	}

	.title {
		font-size: 2.5rem;
		margin: 0;
	}

	.subtitle {
		color: var(--text-muted);
		margin: 0.5rem 0 0;
	}

	.controls {
		display: flex;
		align-items: center;
		gap: 1.5rem;
	}

	.speed-control {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		color: var(--text-secondary);
	}

	.speed-control input {
		width: 100px;
		accent-color: var(--primary);
	}

	.arena-grid {
		display: grid;
		grid-template-columns: 1fr 1.5fr 1fr;
		gap: 1.5rem;
	}

	@media (max-width: 1200px) {
		.arena-grid {
			grid-template-columns: 1fr;
		}
	}

	.card {
		background: var(--bg-card);
		border: 1px solid var(--border);
		border-radius: var(--radius-lg);
		padding: 1.5rem;
	}

	.card h2 {
		margin: 0 0 1rem;
		font-size: 1.25rem;
		color: var(--text-primary);
	}

	/* Combatants Panel */
	.combatants-list {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.combatant-card {
		background: var(--bg-darker);
		border: 1px solid var(--border);
		border-radius: var(--radius-md);
		padding: 1rem;
		transition: all 0.3s ease;
	}

	.combatant-card.defeated {
		opacity: 0.5;
		background: rgba(248, 113, 113, 0.1);
	}

	.combatant-card.winner {
		border-color: var(--success);
		box-shadow: 0 0 20px rgba(74, 222, 128, 0.3);
		animation: glow 2s infinite;
	}

	.combatant-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 0.75rem;
	}

	.combatant-name {
		font-weight: 600;
		color: var(--text-primary);
	}

	.status-badge {
		padding: 0.2rem 0.6rem;
		border-radius: 9999px;
		font-size: 0.7rem;
		font-weight: 600;
		text-transform: uppercase;
		color: var(--bg-dark);
	}

	.health-bar-container {
		position: relative;
		height: 20px;
		background: var(--bg-dark);
		border-radius: 10px;
		overflow: hidden;
		margin-bottom: 0.75rem;
	}

	.health-bar {
		height: 100%;
		border-radius: 10px;
		transition: width 0.3s ease;
	}

	.health-text {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		font-size: 0.75rem;
		font-weight: 600;
		color: white;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
	}

	.stats-row {
		display: flex;
		gap: 1rem;
		margin-bottom: 0.5rem;
	}

	.stat {
		display: flex;
		flex-direction: column;
		align-items: center;
		flex: 1;
	}

	.stat-label {
		font-size: 0.65rem;
		color: var(--text-muted);
		text-transform: uppercase;
	}

	.stat-value {
		font-size: 0.9rem;
		font-weight: 600;
		color: var(--text-primary);
	}

	.combat-stats {
		display: flex;
		justify-content: space-between;
		font-size: 0.8rem;
		color: var(--text-secondary);
	}

	/* Arena Visualization */
	.arena-visualization {
		min-height: 400px;
	}

	.arena-canvas {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		min-height: 350px;
		background: radial-gradient(circle at center, var(--bg-darker) 0%, var(--bg-dark) 100%);
		border-radius: var(--radius-md);
		position: relative;
		overflow: hidden;
	}

	.winner-announcement {
		text-align: center;
	}

	.crown {
		font-size: 4rem;
		animation: bounce 1s ease-in-out infinite;
	}

	.winner-announcement h3 {
		font-size: 1.5rem;
		color: var(--warning);
		margin: 0.5rem 0;
		letter-spacing: 0.2em;
	}

	.winner-name {
		font-size: 2rem;
		font-weight: 700;
		margin-bottom: 1rem;
	}

	.winner-stats {
		display: flex;
		gap: 2rem;
		color: var(--text-secondary);
	}

	.battle-status {
		text-align: center;
		margin-bottom: 2rem;
	}

	.round-indicator {
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--primary);
	}

	.alive-count {
		color: var(--text-muted);
	}

	.battle-animation {
		position: relative;
		width: 250px;
		height: 200px;
	}

	.fighter-avatar {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(calc(-50% + var(--x)), calc(-50% + var(--y)));
		animation: float 2s ease-in-out infinite;
	}

	.avatar-circle {
		width: 50px;
		height: 50px;
		border-radius: 50%;
		background: var(--bg-card);
		border: 3px solid;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 1.25rem;
		font-weight: 700;
		color: var(--text-primary);
	}

	.avatar-health {
		height: 4px;
		background: var(--success);
		border-radius: 2px;
		margin-top: 4px;
		transition: width 0.3s ease;
	}

	.arena-idle {
		text-align: center;
		color: var(--text-muted);
	}

	.idle-icon {
		font-size: 4rem;
		margin-bottom: 1rem;
		animation: wave 2s ease-in-out infinite;
	}

	.idle-hint {
		font-size: 0.85rem;
		margin-top: 0.5rem;
	}

	/* Battle Log */
	.battle-log {
		max-height: 500px;
		display: flex;
		flex-direction: column;
	}

	.log-container {
		flex: 1;
		overflow-y: auto;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		padding-right: 0.5rem;
	}

	.log-entry {
		padding: 0.5rem 0.75rem;
		border-radius: var(--radius-sm);
		background: var(--bg-darker);
		font-size: 0.85rem;
		display: flex;
		gap: 0.75rem;
	}

	.log-time {
		color: var(--text-muted);
		font-size: 0.75rem;
		white-space: nowrap;
	}

	.log-message {
		color: var(--text-secondary);
	}

	.log-attack .log-message { color: var(--error); }
	.log-special .log-message { color: var(--secondary); font-weight: 600; }
	.log-death .log-message { color: var(--error); font-weight: 600; }
	.log-system .log-message { color: var(--info); font-style: italic; }
	.log-defend .log-message { color: var(--success); }

	.log-empty {
		text-align: center;
		color: var(--text-muted);
		padding: 2rem;
	}
</style>
