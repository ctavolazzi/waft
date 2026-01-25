<script lang="ts">
	import { onMount, onDestroy } from 'svelte';

	export let data: FitnessData[] = [];
	export let title = 'Fitness Evolution';

	interface FitnessData {
		generation: number;
		bestFitness: number;
		avgFitness: number;
		worstFitness: number;
		population: number;
	}

	let canvas: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D | null = null;
	let width = 600;
	let height = 300;
	let animationFrame: number;
	let time = 0;

	// Generate sample data if none provided
	function generateSampleData(): FitnessData[] {
		const sample: FitnessData[] = [];
		let best = 0.3;
		let avg = 0.2;
		let worst = 0.1;

		for (let gen = 0; gen <= 50; gen++) {
			// Simulate evolution - fitness improves over time with some randomness
			best = Math.min(1, best + Math.random() * 0.02);
			avg = Math.min(best, avg + Math.random() * 0.015);
			worst = Math.min(avg, worst + Math.random() * 0.01);

			sample.push({
				generation: gen,
				bestFitness: best,
				avgFitness: avg,
				worstFitness: worst,
				population: 50 + Math.floor(Math.random() * 50),
			});
		}
		return sample;
	}

	const COLORS = {
		best: '#4ade80',
		avg: '#7c9eff',
		worst: '#f87171',
		grid: 'rgba(124, 158, 255, 0.1)',
		text: '#b0b8d0',
		bg: '#0a0e1a',
	};

	function drawChart() {
		if (!ctx || data.length === 0) return;

		const padding = { top: 40, right: 20, bottom: 40, left: 60 };
		const chartWidth = width - padding.left - padding.right;
		const chartHeight = height - padding.top - padding.bottom;

		// Clear
		ctx.fillStyle = COLORS.bg;
		ctx.fillRect(0, 0, width, height);

		// Draw grid
		ctx.strokeStyle = COLORS.grid;
		ctx.lineWidth = 1;

		// Horizontal grid lines
		for (let i = 0; i <= 5; i++) {
			const y = padding.top + (chartHeight / 5) * i;
			ctx.beginPath();
			ctx.moveTo(padding.left, y);
			ctx.lineTo(width - padding.right, y);
			ctx.stroke();

			// Y-axis labels
			ctx.fillStyle = COLORS.text;
			ctx.font = '11px Inter, sans-serif';
			ctx.textAlign = 'right';
			ctx.fillText(((5 - i) * 20).toString() + '%', padding.left - 10, y + 4);
		}

		// X-axis labels
		ctx.textAlign = 'center';
		const xStep = Math.max(1, Math.floor(data.length / 10));
		for (let i = 0; i < data.length; i += xStep) {
			const x = padding.left + (i / (data.length - 1)) * chartWidth;
			ctx.fillText(`Gen ${data[i].generation}`, x, height - padding.bottom + 20);
		}

		// Draw lines
		const drawLine = (
			values: number[],
			color: string,
			lineWidth: number = 2,
			animated: boolean = false
		) => {
			ctx!.strokeStyle = color;
			ctx!.lineWidth = lineWidth;
			ctx!.beginPath();

			const endPoint = animated ? Math.min(data.length - 1, Math.floor(time / 10)) : data.length - 1;

			for (let i = 0; i <= endPoint; i++) {
				const x = padding.left + (i / (data.length - 1)) * chartWidth;
				const y = padding.top + (1 - values[i]) * chartHeight;

				if (i === 0) {
					ctx!.moveTo(x, y);
				} else {
					ctx!.lineTo(x, y);
				}
			}
			ctx!.stroke();

			// Draw glow effect
			ctx!.shadowColor = color;
			ctx!.shadowBlur = 10;
			ctx!.stroke();
			ctx!.shadowBlur = 0;
		};

		// Draw area under best fitness
		const gradient = ctx.createLinearGradient(0, padding.top, 0, padding.top + chartHeight);
		gradient.addColorStop(0, 'rgba(74, 222, 128, 0.3)');
		gradient.addColorStop(1, 'rgba(74, 222, 128, 0)');

		ctx.fillStyle = gradient;
		ctx.beginPath();
		ctx.moveTo(padding.left, padding.top + chartHeight);

		for (let i = 0; i < data.length; i++) {
			const x = padding.left + (i / (data.length - 1)) * chartWidth;
			const y = padding.top + (1 - data[i].bestFitness) * chartHeight;
			ctx.lineTo(x, y);
		}

		ctx.lineTo(padding.left + chartWidth, padding.top + chartHeight);
		ctx.closePath();
		ctx.fill();

		// Draw fitness lines
		drawLine(data.map(d => d.worstFitness), COLORS.worst, 1.5);
		drawLine(data.map(d => d.avgFitness), COLORS.avg, 2);
		drawLine(data.map(d => d.bestFitness), COLORS.best, 2.5);

		// Draw title
		ctx.fillStyle = '#e8eaf6';
		ctx.font = 'bold 16px Inter, sans-serif';
		ctx.textAlign = 'left';
		ctx.fillText(title, padding.left, 25);

		// Draw legend
		const legendX = width - padding.right - 120;
		const legendY = 20;

		[
			{ label: 'Best', color: COLORS.best },
			{ label: 'Average', color: COLORS.avg },
			{ label: 'Worst', color: COLORS.worst },
		].forEach((item, i) => {
			const y = legendY + i * 18;

			ctx!.strokeStyle = item.color;
			ctx!.lineWidth = 2;
			ctx!.beginPath();
			ctx!.moveTo(legendX, y);
			ctx!.lineTo(legendX + 20, y);
			ctx!.stroke();

			ctx!.fillStyle = COLORS.text;
			ctx!.font = '11px Inter, sans-serif';
			ctx!.textAlign = 'left';
			ctx!.fillText(item.label, legendX + 28, y + 4);
		});

		// Draw current stats
		if (data.length > 0) {
			const latest = data[data.length - 1];
			const statsY = height - 15;

			ctx.fillStyle = COLORS.text;
			ctx.font = '10px Inter, sans-serif';
			ctx.textAlign = 'left';
			ctx.fillText(
				`Latest: Best ${(latest.bestFitness * 100).toFixed(1)}% | Avg ${(latest.avgFitness * 100).toFixed(1)}% | Pop ${latest.population}`,
				padding.left,
				statsY
			);
		}
	}

	function animate() {
		time++;
		drawChart();
		animationFrame = requestAnimationFrame(animate);
	}

	function handleResize() {
		if (canvas && canvas.parentElement) {
			width = canvas.parentElement.clientWidth;
			height = Math.min(400, width * 0.5);
			canvas.width = width;
			canvas.height = height;
		}
	}

	onMount(() => {
		if (!canvas) return;
		ctx = canvas.getContext('2d');
		if (!ctx) return;

		if (data.length === 0) {
			data = generateSampleData();
		}

		handleResize();
		animate();

		window.addEventListener('resize', handleResize);
	});

	onDestroy(() => {
		if (animationFrame) cancelAnimationFrame(animationFrame);
		window.removeEventListener('resize', handleResize);
	});

	$: if (data && ctx) {
		drawChart();
	}
</script>

<div class="fitness-dashboard">
	<canvas bind:this={canvas} />

	<div class="stats-grid">
		{#if data.length > 0}
			{@const latest = data[data.length - 1]}
			{@const improvement = data.length > 1 ? latest.bestFitness - data[0].bestFitness : 0}

			<div class="stat-card">
				<span class="stat-label">Best Fitness</span>
				<span class="stat-value best">{(latest.bestFitness * 100).toFixed(1)}%</span>
			</div>

			<div class="stat-card">
				<span class="stat-label">Average</span>
				<span class="stat-value avg">{(latest.avgFitness * 100).toFixed(1)}%</span>
			</div>

			<div class="stat-card">
				<span class="stat-label">Generation</span>
				<span class="stat-value">{latest.generation}</span>
			</div>

			<div class="stat-card">
				<span class="stat-label">Improvement</span>
				<span class="stat-value improvement" class:positive={improvement > 0}>
					{improvement > 0 ? '+' : ''}{(improvement * 100).toFixed(1)}%
				</span>
			</div>
		{/if}
	</div>
</div>

<style>
	.fitness-dashboard {
		background: var(--bg-card);
		border: 1px solid var(--border);
		border-radius: var(--radius-lg);
		padding: 1.5rem;
	}

	canvas {
		width: 100%;
		height: auto;
		border-radius: var(--radius-md);
		background: var(--bg-darker);
	}

	.stats-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 1rem;
		margin-top: 1rem;
	}

	@media (max-width: 600px) {
		.stats-grid {
			grid-template-columns: repeat(2, 1fr);
		}
	}

	.stat-card {
		background: var(--bg-darker);
		border: 1px solid var(--border-light);
		border-radius: var(--radius-md);
		padding: 1rem;
		text-align: center;
	}

	.stat-label {
		display: block;
		font-size: 0.75rem;
		color: var(--text-muted);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		margin-bottom: 0.5rem;
	}

	.stat-value {
		display: block;
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--text-primary);
	}

	.stat-value.best {
		color: var(--success);
	}

	.stat-value.avg {
		color: var(--primary);
	}

	.stat-value.improvement.positive {
		color: var(--success);
	}
</style>
