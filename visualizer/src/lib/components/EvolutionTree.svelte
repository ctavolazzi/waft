<script lang="ts">
	import { onMount, onDestroy } from 'svelte';

	export let agents: Agent[] = [];
	export let selectedAgent: string | null = null;

	interface Agent {
		id: string;
		name: string;
		generation: number;
		parentId: string | null;
		fitness: number;
		status: 'alive' | 'dead' | 'evolved' | 'spawning';
		mutations: string[];
		createdAt: string;
	}

	interface TreeNode {
		agent: Agent;
		x: number;
		y: number;
		children: TreeNode[];
		depth: number;
		width: number;
	}

	let canvas: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D | null = null;
	let animationFrame: number;
	let width = 800;
	let height = 600;
	let time = 0;
	let hoveredAgent: Agent | null = null;
	let panX = 0;
	let panY = 0;
	let zoom = 1;
	let isDragging = false;
	let lastMouseX = 0;
	let lastMouseY = 0;

	const NODE_RADIUS = 25;
	const VERTICAL_SPACING = 100;
	const HORIZONTAL_SPACING = 80;

	const COLORS = {
		alive: '#4ade80',
		dead: '#6b7280',
		evolved: '#a855f7',
		spawning: '#22d3ee',
		connection: 'rgba(124, 158, 255, 0.4)',
		connectionActive: 'rgba(74, 222, 128, 0.6)',
		glow: 'rgba(124, 158, 255, 0.3)',
		text: '#e8eaf6',
		fitness: {
			high: '#4ade80',
			medium: '#fbbf24',
			low: '#f87171',
		},
	};

	// Build tree structure from flat agent list
	function buildTree(agents: Agent[]): TreeNode | null {
		if (agents.length === 0) return null;

		const agentMap = new Map<string, Agent>();
		agents.forEach((a) => agentMap.set(a.id, a));

		// Find root (no parent or parent not in list)
		const roots = agents.filter(
			(a) => !a.parentId || !agentMap.has(a.parentId)
		);

		if (roots.length === 0) return null;

		function buildNode(agent: Agent, depth: number): TreeNode {
			const children = agents
				.filter((a) => a.parentId === agent.id)
				.map((child) => buildNode(child, depth + 1));

			const width = Math.max(
				1,
				children.reduce((sum, c) => sum + c.width, 0)
			);

			return {
				agent,
				x: 0,
				y: depth * VERTICAL_SPACING + 50,
				children,
				depth,
				width,
			};
		}

		// Build from first root
		const root = buildNode(roots[0], 0);

		// Calculate x positions
		function layoutNode(node: TreeNode, startX: number): void {
			let currentX = startX;

			if (node.children.length === 0) {
				node.x = startX + NODE_RADIUS;
			} else {
				node.children.forEach((child) => {
					layoutNode(child, currentX);
					currentX += child.width * HORIZONTAL_SPACING;
				});

				// Center parent above children
				const firstChild = node.children[0];
				const lastChild = node.children[node.children.length - 1];
				node.x = (firstChild.x + lastChild.x) / 2;
			}
		}

		layoutNode(root, 50);
		return root;
	}

	function getStatusColor(status: string): string {
		return COLORS[status as keyof typeof COLORS] || COLORS.alive;
	}

	function getFitnessColor(fitness: number): string {
		if (fitness >= 0.7) return COLORS.fitness.high;
		if (fitness >= 0.4) return COLORS.fitness.medium;
		return COLORS.fitness.low;
	}

	function drawConnection(
		ctx: CanvasRenderingContext2D,
		x1: number,
		y1: number,
		x2: number,
		y2: number,
		active: boolean
	) {
		const midY = (y1 + y2) / 2;

		ctx.beginPath();
		ctx.moveTo(x1, y1);
		ctx.bezierCurveTo(x1, midY, x2, midY, x2, y2);

		// Animated pulse along connection
		const gradient = ctx.createLinearGradient(x1, y1, x2, y2);
		const pulsePos = (Math.sin(time * 0.05) + 1) / 2;

		if (active) {
			gradient.addColorStop(0, COLORS.connectionActive);
			gradient.addColorStop(pulsePos, 'rgba(124, 158, 255, 0.8)');
			gradient.addColorStop(1, COLORS.connectionActive);
		} else {
			gradient.addColorStop(0, COLORS.connection);
			gradient.addColorStop(1, COLORS.connection);
		}

		ctx.strokeStyle = gradient;
		ctx.lineWidth = active ? 3 : 2;
		ctx.stroke();

		// Draw data particles along connection
		if (active) {
			for (let i = 0; i < 3; i++) {
				const t = ((time * 0.02 + i * 0.33) % 1);
				const px = x1 + (x2 - x1) * t;
				const py = y1 + (y2 - y1) * t + Math.sin(t * Math.PI) * -20;

				ctx.beginPath();
				ctx.arc(px, py, 3, 0, Math.PI * 2);
				ctx.fillStyle = COLORS.evolved;
				ctx.fill();
			}
		}
	}

	function drawNode(
		ctx: CanvasRenderingContext2D,
		node: TreeNode,
		isSelected: boolean,
		isHovered: boolean
	) {
		const { agent, x, y } = node;
		const statusColor = getStatusColor(agent.status);
		const fitnessColor = getFitnessColor(agent.fitness);

		// Outer glow for selected/hovered
		if (isSelected || isHovered) {
			const glowRadius = NODE_RADIUS + 15 + Math.sin(time * 0.1) * 5;
			const gradient = ctx.createRadialGradient(x, y, 0, x, y, glowRadius);
			gradient.addColorStop(0, isSelected ? 'rgba(168, 85, 247, 0.4)' : 'rgba(124, 158, 255, 0.3)');
			gradient.addColorStop(1, 'transparent');
			ctx.fillStyle = gradient;
			ctx.beginPath();
			ctx.arc(x, y, glowRadius, 0, Math.PI * 2);
			ctx.fill();
		}

		// Fitness ring (outer)
		ctx.beginPath();
		ctx.arc(x, y, NODE_RADIUS + 5, 0, Math.PI * 2);
		ctx.strokeStyle = fitnessColor;
		ctx.lineWidth = 3;
		ctx.stroke();

		// Fitness arc (shows actual fitness)
		ctx.beginPath();
		ctx.arc(x, y, NODE_RADIUS + 5, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * agent.fitness);
		ctx.strokeStyle = '#ffffff';
		ctx.lineWidth = 3;
		ctx.stroke();

		// Main node circle
		const nodeGradient = ctx.createRadialGradient(
			x - NODE_RADIUS / 3,
			y - NODE_RADIUS / 3,
			0,
			x,
			y,
			NODE_RADIUS
		);
		nodeGradient.addColorStop(0, statusColor);
		nodeGradient.addColorStop(1, shadeColor(statusColor, -30));

		ctx.beginPath();
		ctx.arc(x, y, NODE_RADIUS, 0, Math.PI * 2);
		ctx.fillStyle = nodeGradient;
		ctx.fill();

		// Inner highlight
		ctx.beginPath();
		ctx.arc(x - 8, y - 8, 8, 0, Math.PI * 2);
		ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
		ctx.fill();

		// Generation number
		ctx.fillStyle = COLORS.text;
		ctx.font = 'bold 14px Inter, sans-serif';
		ctx.textAlign = 'center';
		ctx.textBaseline = 'middle';
		ctx.fillText(`G${agent.generation}`, x, y);

		// Agent name (below node)
		ctx.font = '11px Inter, sans-serif';
		ctx.fillStyle = COLORS.text;
		ctx.fillText(truncate(agent.name, 12), x, y + NODE_RADIUS + 18);

		// Spawning animation
		if (agent.status === 'spawning') {
			for (let i = 0; i < 3; i++) {
				const angle = (time * 0.05 + (i * Math.PI * 2) / 3) % (Math.PI * 2);
				const orbitRadius = NODE_RADIUS + 20;
				const px = x + Math.cos(angle) * orbitRadius;
				const py = y + Math.sin(angle) * orbitRadius;

				ctx.beginPath();
				ctx.arc(px, py, 4, 0, Math.PI * 2);
				ctx.fillStyle = COLORS.spawning;
				ctx.fill();
			}
		}
	}

	function drawTree(node: TreeNode) {
		if (!ctx) return;

		// Draw connections first (so they're behind nodes)
		node.children.forEach((child) => {
			const isActive =
				selectedAgent === node.agent.id || selectedAgent === child.agent.id;
			drawConnection(
				ctx,
				node.x,
				node.y + NODE_RADIUS,
				child.x,
				child.y - NODE_RADIUS,
				isActive
			);
			drawTree(child);
		});

		// Draw this node
		const isSelected = selectedAgent === node.agent.id;
		const isHovered = hoveredAgent?.id === node.agent.id;
		drawNode(ctx, node, isSelected, isHovered);
	}

	function drawBackground() {
		if (!ctx) return;

		// Gradient background
		const gradient = ctx.createLinearGradient(0, 0, 0, height);
		gradient.addColorStop(0, 'rgba(10, 14, 26, 0.95)');
		gradient.addColorStop(1, 'rgba(26, 30, 41, 0.95)');
		ctx.fillStyle = gradient;
		ctx.fillRect(0, 0, width, height);

		// Grid
		ctx.strokeStyle = 'rgba(124, 158, 255, 0.05)';
		ctx.lineWidth = 1;

		for (let x = 0; x < width; x += 40) {
			ctx.beginPath();
			ctx.moveTo(x, 0);
			ctx.lineTo(x, height);
			ctx.stroke();
		}

		for (let y = 0; y < height; y += 40) {
			ctx.beginPath();
			ctx.moveTo(0, y);
			ctx.lineTo(width, y);
			ctx.stroke();
		}
	}

	function drawLegend() {
		if (!ctx) return;

		const legendX = 20;
		let legendY = 20;
		const spacing = 25;

		ctx.font = 'bold 12px Inter, sans-serif';
		ctx.fillStyle = COLORS.text;
		ctx.fillText('Agent Status', legendX, legendY);
		legendY += spacing;

		const statuses = [
			{ label: 'Alive', color: COLORS.alive },
			{ label: 'Evolved', color: COLORS.evolved },
			{ label: 'Spawning', color: COLORS.spawning },
			{ label: 'Dead', color: COLORS.dead },
		];

		ctx.font = '11px Inter, sans-serif';
		statuses.forEach(({ label, color }) => {
			ctx.beginPath();
			ctx.arc(legendX + 8, legendY - 4, 6, 0, Math.PI * 2);
			ctx.fillStyle = color;
			ctx.fill();

			ctx.fillStyle = COLORS.text;
			ctx.fillText(label, legendX + 22, legendY);
			legendY += 20;
		});
	}

	function drawStats() {
		if (!ctx || agents.length === 0) return;

		const statsX = width - 150;
		let statsY = 20;

		ctx.font = 'bold 12px Inter, sans-serif';
		ctx.fillStyle = COLORS.text;
		ctx.textAlign = 'left';
		ctx.fillText('Population Stats', statsX, statsY);
		statsY += 25;

		const stats = [
			{ label: 'Total Agents', value: agents.length },
			{ label: 'Generations', value: Math.max(...agents.map((a) => a.generation)) + 1 },
			{ label: 'Alive', value: agents.filter((a) => a.status === 'alive').length },
			{ label: 'Avg Fitness', value: (agents.reduce((sum, a) => sum + a.fitness, 0) / agents.length).toFixed(2) },
			{ label: 'Best Fitness', value: Math.max(...agents.map((a) => a.fitness)).toFixed(2) },
		];

		ctx.font = '11px Inter, sans-serif';
		stats.forEach(({ label, value }) => {
			ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
			ctx.fillText(label + ':', statsX, statsY);
			ctx.fillStyle = COLORS.text;
			ctx.fillText(String(value), statsX + 90, statsY);
			statsY += 18;
		});
	}

	function animate() {
		if (!ctx) return;

		time++;
		drawBackground();

		ctx.save();
		ctx.translate(panX, panY);
		ctx.scale(zoom, zoom);

		const tree = buildTree(agents);
		if (tree) {
			drawTree(tree);
		} else {
			// No agents - show empty state
			ctx.font = '16px Inter, sans-serif';
			ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
			ctx.textAlign = 'center';
			ctx.fillText('No agents in population', width / 2, height / 2);
		}

		ctx.restore();

		drawLegend();
		drawStats();

		animationFrame = requestAnimationFrame(animate);
	}

	function handleMouseMove(e: MouseEvent) {
		const rect = canvas.getBoundingClientRect();
		const mouseX = (e.clientX - rect.left - panX) / zoom;
		const mouseY = (e.clientY - rect.top - panY) / zoom;

		if (isDragging) {
			panX += e.clientX - lastMouseX;
			panY += e.clientY - lastMouseY;
			lastMouseX = e.clientX;
			lastMouseY = e.clientY;
			return;
		}

		// Check hover
		const tree = buildTree(agents);
		hoveredAgent = findAgentAtPosition(tree, mouseX, mouseY);
		canvas.style.cursor = hoveredAgent ? 'pointer' : 'grab';
	}

	function handleMouseDown(e: MouseEvent) {
		isDragging = true;
		lastMouseX = e.clientX;
		lastMouseY = e.clientY;
		canvas.style.cursor = 'grabbing';
	}

	function handleMouseUp() {
		isDragging = false;
		canvas.style.cursor = hoveredAgent ? 'pointer' : 'grab';
	}

	function handleClick(e: MouseEvent) {
		if (hoveredAgent) {
			selectedAgent = selectedAgent === hoveredAgent.id ? null : hoveredAgent.id;
		}
	}

	function handleWheel(e: WheelEvent) {
		e.preventDefault();
		const delta = e.deltaY > 0 ? 0.9 : 1.1;
		zoom = Math.min(Math.max(zoom * delta, 0.3), 3);
	}

	function findAgentAtPosition(
		node: TreeNode | null,
		x: number,
		y: number
	): Agent | null {
		if (!node) return null;

		const dist = Math.sqrt((x - node.x) ** 2 + (y - node.y) ** 2);
		if (dist <= NODE_RADIUS) {
			return node.agent;
		}

		for (const child of node.children) {
			const found = findAgentAtPosition(child, x, y);
			if (found) return found;
		}

		return null;
	}

	function shadeColor(color: string, percent: number): string {
		const num = parseInt(color.replace('#', ''), 16);
		const amt = Math.round(2.55 * percent);
		const R = Math.min(255, Math.max(0, (num >> 16) + amt));
		const G = Math.min(255, Math.max(0, ((num >> 8) & 0x00ff) + amt));
		const B = Math.min(255, Math.max(0, (num & 0x0000ff) + amt));
		return `#${((1 << 24) + (R << 16) + (G << 8) + B).toString(16).slice(1)}`;
	}

	function truncate(str: string, length: number): string {
		return str.length > length ? str.substring(0, length - 2) + '..' : str;
	}

	onMount(() => {
		if (!canvas) return;
		ctx = canvas.getContext('2d');
		if (!ctx) return;

		width = canvas.parentElement?.clientWidth || 800;
		height = canvas.parentElement?.clientHeight || 600;
		canvas.width = width;
		canvas.height = height;

		animate();
	});

	onDestroy(() => {
		if (animationFrame) cancelAnimationFrame(animationFrame);
	});

	// Generate sample agents if none provided
	$: if (agents.length === 0) {
		agents = generateSampleAgents();
	}

	function generateSampleAgents(): Agent[] {
		const statuses: Agent['status'][] = ['alive', 'evolved', 'spawning', 'dead'];
		const names = [
			'Aethon Prime', 'Nova Striker', 'Quantum Echo', 'Stellar Drift',
			'Nebula Core', 'Void Walker', 'Cosmic Tide', 'Solar Flare',
			'Lunar Phase', 'Terra Nova', 'Astral Wind', 'Gravity Well',
		];

		const sample: Agent[] = [
			{ id: '1', name: 'Genesis Alpha', generation: 0, parentId: null, fitness: 0.85, status: 'evolved', mutations: ['speed+'], createdAt: new Date().toISOString() },
			{ id: '2', name: 'Beta Prime', generation: 1, parentId: '1', fitness: 0.72, status: 'alive', mutations: ['vision+'], createdAt: new Date().toISOString() },
			{ id: '3', name: 'Gamma Ray', generation: 1, parentId: '1', fitness: 0.68, status: 'alive', mutations: ['strength+'], createdAt: new Date().toISOString() },
			{ id: '4', name: 'Delta Force', generation: 2, parentId: '2', fitness: 0.91, status: 'spawning', mutations: ['speed++'], createdAt: new Date().toISOString() },
			{ id: '5', name: 'Epsilon Star', generation: 2, parentId: '2', fitness: 0.45, status: 'dead', mutations: ['weakness'], createdAt: new Date().toISOString() },
			{ id: '6', name: 'Zeta Blade', generation: 2, parentId: '3', fitness: 0.78, status: 'alive', mutations: ['armor+'], createdAt: new Date().toISOString() },
			{ id: '7', name: 'Eta Storm', generation: 3, parentId: '4', fitness: 0.95, status: 'alive', mutations: ['elite'], createdAt: new Date().toISOString() },
			{ id: '8', name: 'Theta Wave', generation: 3, parentId: '6', fitness: 0.82, status: 'alive', mutations: ['regen+'], createdAt: new Date().toISOString() },
		];

		return sample;
	}
</script>

<div class="evolution-tree-container">
	<canvas
		bind:this={canvas}
		on:mousemove={handleMouseMove}
		on:mousedown={handleMouseDown}
		on:mouseup={handleMouseUp}
		on:mouseleave={handleMouseUp}
		on:click={handleClick}
		on:wheel={handleWheel}
	/>

	{#if hoveredAgent}
		<div class="tooltip" style="left: {lastMouseX + 15}px; top: {lastMouseY + 15}px;">
			<div class="tooltip-header">{hoveredAgent.name}</div>
			<div class="tooltip-row">
				<span class="label">Generation:</span>
				<span class="value">{hoveredAgent.generation}</span>
			</div>
			<div class="tooltip-row">
				<span class="label">Fitness:</span>
				<span class="value" style="color: {getFitnessColor(hoveredAgent.fitness)}">{(hoveredAgent.fitness * 100).toFixed(1)}%</span>
			</div>
			<div class="tooltip-row">
				<span class="label">Status:</span>
				<span class="value status-badge" style="background: {getStatusColor(hoveredAgent.status)}">{hoveredAgent.status}</span>
			</div>
			{#if hoveredAgent.mutations.length > 0}
				<div class="tooltip-row">
					<span class="label">Mutations:</span>
					<span class="value">{hoveredAgent.mutations.join(', ')}</span>
				</div>
			{/if}
		</div>
	{/if}

	<div class="controls">
		<button on:click={() => { zoom = Math.min(zoom * 1.2, 3); }}>+</button>
		<button on:click={() => { zoom = Math.max(zoom * 0.8, 0.3); }}>-</button>
		<button on:click={() => { zoom = 1; panX = 0; panY = 0; }}>Reset</button>
	</div>
</div>

<style>
	.evolution-tree-container {
		position: relative;
		width: 100%;
		height: 100%;
		min-height: 500px;
		background: var(--bg-dark);
		border-radius: 12px;
		overflow: hidden;
	}

	canvas {
		width: 100%;
		height: 100%;
		cursor: grab;
	}

	.tooltip {
		position: fixed;
		background: rgba(26, 30, 41, 0.95);
		border: 1px solid var(--border);
		border-radius: 8px;
		padding: 12px;
		pointer-events: none;
		z-index: 100;
		min-width: 180px;
		backdrop-filter: blur(10px);
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
	}

	.tooltip-header {
		font-weight: 600;
		font-size: 14px;
		color: var(--primary-light);
		margin-bottom: 8px;
		padding-bottom: 6px;
		border-bottom: 1px solid var(--border);
	}

	.tooltip-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin: 4px 0;
		font-size: 12px;
	}

	.label {
		color: var(--text-muted);
	}

	.value {
		color: var(--text-primary);
		font-weight: 500;
	}

	.status-badge {
		padding: 2px 8px;
		border-radius: 4px;
		font-size: 10px;
		text-transform: uppercase;
		color: #000;
	}

	.controls {
		position: absolute;
		bottom: 16px;
		right: 16px;
		display: flex;
		gap: 8px;
	}

	.controls button {
		width: 36px;
		height: 36px;
		border: 1px solid var(--border);
		background: rgba(26, 30, 41, 0.9);
		color: var(--text-primary);
		border-radius: 8px;
		cursor: pointer;
		font-size: 16px;
		font-weight: 600;
		transition: all 0.2s ease;
	}

	.controls button:last-child {
		width: auto;
		padding: 0 12px;
		font-size: 12px;
	}

	.controls button:hover {
		background: var(--primary);
		border-color: var(--primary);
		color: var(--bg-dark);
	}
</style>
