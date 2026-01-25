<script lang="ts">
	import { onMount, onDestroy } from 'svelte';

	export let genome: Genome | null = null;
	export let animated: boolean = true;
	export let showLabels: boolean = true;
	export let width: number = 400;
	export let height: number = 600;

	interface GeneData {
		category: string;
		name: string;
		value: any;
		color: string;
	}

	interface Genome {
		id: string;
		name: string;
		generation: number;
		fitness: number;
		genes: {
			font: Record<string, any>;
			margin: Record<string, any>;
			color: Record<string, any>;
			layout: Record<string, any>;
		};
	}

	let canvas: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D | null = null;
	let animationFrame: number;
	let time = 0;
	let hoveredGene: GeneData | null = null;
	let mouseX = 0;
	let mouseY = 0;

	// Category colors
	const categoryColors: Record<string, string> = {
		font: '#7c9eff',
		margin: '#a855f7',
		color: '#10b981',
		layout: '#f59e0b'
	};

	// Convert genome to gene data array
	function getGeneData(): GeneData[] {
		if (!genome) return [];

		const genes: GeneData[] = [];

		for (const [category, categoryGenes] of Object.entries(genome.genes)) {
			if (typeof categoryGenes === 'object' && categoryGenes !== null) {
				for (const [name, value] of Object.entries(categoryGenes)) {
					genes.push({
						category,
						name,
						value,
						color: categoryColors[category] || '#888'
					});
				}
			}
		}

		return genes;
	}

	function drawDNA() {
		if (!ctx || !canvas) return;

		const genes = getGeneData();
		if (genes.length === 0) {
			// Draw empty state
			ctx.fillStyle = '#1a1a2e';
			ctx.fillRect(0, 0, width, height);
			ctx.fillStyle = '#666';
			ctx.font = '16px system-ui';
			ctx.textAlign = 'center';
			ctx.fillText('No genome selected', width / 2, height / 2);
			return;
		}

		// Clear canvas
		ctx.fillStyle = '#0a0a1a';
		ctx.fillRect(0, 0, width, height);

		// DNA parameters
		const centerX = width / 2;
		const amplitude = width * 0.25;
		const helixSpacing = height / (genes.length + 2);
		const twistSpeed = 0.02;

		// Draw glow effect
		const gradient = ctx.createRadialGradient(centerX, height / 2, 0, centerX, height / 2, height / 2);
		gradient.addColorStop(0, 'rgba(124, 158, 255, 0.1)');
		gradient.addColorStop(1, 'transparent');
		ctx.fillStyle = gradient;
		ctx.fillRect(0, 0, width, height);

		// Draw backbone strands
		ctx.lineWidth = 3;
		ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';

		// Left strand
		ctx.beginPath();
		for (let y = 0; y <= height; y += 2) {
			const phase = animated ? time * twistSpeed : 0;
			const x = centerX + Math.sin((y / height) * Math.PI * 4 + phase) * amplitude;
			if (y === 0) ctx.moveTo(x, y);
			else ctx.lineTo(x, y);
		}
		ctx.stroke();

		// Right strand
		ctx.beginPath();
		for (let y = 0; y <= height; y += 2) {
			const phase = animated ? time * twistSpeed : 0;
			const x = centerX + Math.sin((y / height) * Math.PI * 4 + phase + Math.PI) * amplitude;
			if (y === 0) ctx.moveTo(x, y);
			else ctx.lineTo(x, y);
		}
		ctx.stroke();

		// Draw base pairs (genes)
		genes.forEach((gene, i) => {
			const y = (i + 1) * helixSpacing;
			const phase = animated ? time * twistSpeed : 0;

			// Calculate x positions for both strands
			const x1 = centerX + Math.sin((y / height) * Math.PI * 4 + phase) * amplitude;
			const x2 = centerX + Math.sin((y / height) * Math.PI * 4 + phase + Math.PI) * amplitude;

			// Determine visibility based on twist (only show when facing us)
			const twistPhase = ((y / height) * Math.PI * 4 + phase) % (Math.PI * 2);
			const opacity = Math.abs(Math.cos(twistPhase));

			if (opacity > 0.3) {
				// Draw connecting bar
				ctx.strokeStyle = gene.color;
				ctx.lineWidth = 4;
				ctx.globalAlpha = opacity * 0.8;
				ctx.beginPath();
				ctx.moveTo(x1, y);
				ctx.lineTo(x2, y);
				ctx.stroke();

				// Draw nucleotide circles
				const nodeRadius = 8;

				// Left node
				ctx.fillStyle = gene.color;
				ctx.beginPath();
				ctx.arc(x1, y, nodeRadius, 0, Math.PI * 2);
				ctx.fill();

				// Right node (complementary)
				ctx.beginPath();
				ctx.arc(x2, y, nodeRadius, 0, Math.PI * 2);
				ctx.fill();

				// Glow effect
				const glowGradient = ctx.createRadialGradient(x1, y, 0, x1, y, nodeRadius * 2);
				glowGradient.addColorStop(0, gene.color);
				glowGradient.addColorStop(1, 'transparent');
				ctx.fillStyle = glowGradient;
				ctx.globalAlpha = opacity * 0.3;
				ctx.beginPath();
				ctx.arc(x1, y, nodeRadius * 2, 0, Math.PI * 2);
				ctx.fill();

				// Draw label if enabled and visible
				if (showLabels && opacity > 0.7) {
					ctx.globalAlpha = opacity;
					ctx.fillStyle = '#fff';
					ctx.font = '11px system-ui';
					ctx.textAlign = x1 < centerX ? 'right' : 'left';
					const labelX = x1 < centerX ? x1 - nodeRadius - 5 : x1 + nodeRadius + 5;
					ctx.fillText(`${gene.name}`, labelX, y + 4);
				}

				// Check for hover
				const dist1 = Math.sqrt(Math.pow(mouseX - x1, 2) + Math.pow(mouseY - y, 2));
				const dist2 = Math.sqrt(Math.pow(mouseX - x2, 2) + Math.pow(mouseY - y, 2));
				if (dist1 < nodeRadius * 2 || dist2 < nodeRadius * 2) {
					hoveredGene = gene;
				}
			}

			ctx.globalAlpha = 1;
		});

		// Draw fitness indicator at top
		if (genome) {
			const fitnessWidth = width * 0.6;
			const fitnessHeight = 8;
			const fitnessX = (width - fitnessWidth) / 2;
			const fitnessY = 20;

			// Background
			ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
			ctx.fillRect(fitnessX, fitnessY, fitnessWidth, fitnessHeight);

			// Fill
			const fitnessGradient = ctx.createLinearGradient(fitnessX, 0, fitnessX + fitnessWidth, 0);
			fitnessGradient.addColorStop(0, '#ef4444');
			fitnessGradient.addColorStop(0.5, '#f59e0b');
			fitnessGradient.addColorStop(1, '#10b981');
			ctx.fillStyle = fitnessGradient;
			ctx.fillRect(fitnessX, fitnessY, fitnessWidth * genome.fitness, fitnessHeight);

			// Label
			ctx.fillStyle = '#fff';
			ctx.font = 'bold 12px system-ui';
			ctx.textAlign = 'center';
			ctx.fillText(`Fitness: ${(genome.fitness * 100).toFixed(1)}%`, width / 2, fitnessY + 25);
		}

		// Draw genome name
		if (genome) {
			ctx.fillStyle = '#7c9eff';
			ctx.font = 'bold 16px system-ui';
			ctx.textAlign = 'center';
			ctx.fillText(genome.name, width / 2, height - 30);

			ctx.fillStyle = '#888';
			ctx.font = '12px system-ui';
			ctx.fillText(`Generation ${genome.generation}`, width / 2, height - 12);
		}
	}

	function animate() {
		time++;
		drawDNA();
		if (animated) {
			animationFrame = requestAnimationFrame(animate);
		}
	}

	function handleMouseMove(e: MouseEvent) {
		const rect = canvas.getBoundingClientRect();
		mouseX = e.clientX - rect.left;
		mouseY = e.clientY - rect.top;
		hoveredGene = null;
	}

	onMount(() => {
		ctx = canvas.getContext('2d');
		if (ctx) {
			animate();
		}
	});

	onDestroy(() => {
		if (animationFrame) {
			cancelAnimationFrame(animationFrame);
		}
	});

	// Redraw when genome changes
	$: if (genome && ctx) {
		drawDNA();
	}
</script>

<div class="dna-viewer" style="width: {width}px; height: {height}px;">
	<canvas
		bind:this={canvas}
		{width}
		{height}
		on:mousemove={handleMouseMove}
		on:mouseleave={() => (hoveredGene = null)}
	/>

	{#if hoveredGene}
		<div
			class="gene-tooltip"
			style="left: {mouseX + 10}px; top: {mouseY - 10}px;"
		>
			<div class="tooltip-header" style="border-color: {hoveredGene.color}">
				<span class="category" style="color: {hoveredGene.color}">{hoveredGene.category}</span>
				<span class="name">{hoveredGene.name}</span>
			</div>
			<div class="tooltip-value">
				{#if typeof hoveredGene.value === 'object'}
					<pre>{JSON.stringify(hoveredGene.value, null, 2)}</pre>
				{:else}
					{hoveredGene.value}
				{/if}
			</div>
		</div>
	{/if}

	<div class="legend">
		{#each Object.entries(categoryColors) as [category, color]}
			<div class="legend-item">
				<span class="legend-dot" style="background: {color}"></span>
				<span class="legend-label">{category}</span>
			</div>
		{/each}
	</div>
</div>

<style>
	.dna-viewer {
		position: relative;
		background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 100%);
		border-radius: 12px;
		overflow: hidden;
		box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5), inset 0 0 60px rgba(124, 158, 255, 0.05);
	}

	canvas {
		display: block;
		cursor: crosshair;
	}

	.gene-tooltip {
		position: absolute;
		background: rgba(10, 10, 26, 0.95);
		border: 1px solid rgba(124, 158, 255, 0.3);
		border-radius: 8px;
		padding: 12px;
		pointer-events: none;
		z-index: 100;
		backdrop-filter: blur(10px);
		min-width: 150px;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
	}

	.tooltip-header {
		border-left: 3px solid;
		padding-left: 8px;
		margin-bottom: 8px;
	}

	.category {
		font-size: 10px;
		text-transform: uppercase;
		letter-spacing: 1px;
		display: block;
	}

	.name {
		font-weight: bold;
		font-size: 14px;
		color: #fff;
	}

	.tooltip-value {
		font-family: 'Fira Code', monospace;
		font-size: 12px;
		color: #10b981;
		background: rgba(16, 185, 129, 0.1);
		padding: 6px 8px;
		border-radius: 4px;
	}

	.tooltip-value pre {
		margin: 0;
		white-space: pre-wrap;
		word-break: break-all;
	}

	.legend {
		position: absolute;
		bottom: 60px;
		left: 50%;
		transform: translateX(-50%);
		display: flex;
		gap: 16px;
		background: rgba(0, 0, 0, 0.5);
		padding: 8px 16px;
		border-radius: 20px;
		backdrop-filter: blur(10px);
	}

	.legend-item {
		display: flex;
		align-items: center;
		gap: 6px;
	}

	.legend-dot {
		width: 10px;
		height: 10px;
		border-radius: 50%;
	}

	.legend-label {
		font-size: 11px;
		color: #888;
		text-transform: capitalize;
	}
</style>
