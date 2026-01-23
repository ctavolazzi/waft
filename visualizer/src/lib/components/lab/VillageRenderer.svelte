<script lang="ts">
	import { onMount, onDestroy, afterUpdate } from 'svelte';
	import type { Village, Building } from '$lib/models/Village';

	export let village: Village | null = null;
	export let width: number = 0;
	export let height: number = 0;
	export let selectedBuilding: Building | null = null;

	let canvas: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D | null = null;
	let animationFrame: number;

	onMount(() => {
		if (!canvas) return;
		ctx = canvas.getContext('2d');
		if (!ctx) return;

		// Start render loop
		render();
	});

	onDestroy(() => {
		if (animationFrame) {
			cancelAnimationFrame(animationFrame);
		}
	});

	afterUpdate(() => {
		// Redraw when village updates
		if (ctx && canvas) {
			draw();
		}
	});

	function render() {
		draw();
		animationFrame = requestAnimationFrame(render);
	}

	function draw() {
		if (!ctx || !canvas || !village) return;

		// Clear canvas
		ctx.clearRect(0, 0, width, height);

		// Draw all buildings
		for (const building of village.buildings) {
			drawBuilding(building);
		}

		// Draw selected building highlight
		if (selectedBuilding) {
			drawSelectionHighlight(selectedBuilding);
		}
	}

	function drawBuilding(building: Building) {
		if (!ctx) return;

		const x = building.x;
		const y = building.y;
		const w = building.template.width;
		const h = building.template.height;

		// Building base
		if (building.operational) {
			ctx.fillStyle = 'rgba(80, 80, 120, 0.8)';
		} else {
			// Under construction
			ctx.fillStyle = 'rgba(100, 100, 100, 0.5)';
		}

		ctx.fillRect(x, y, w, h);

		// Border
		ctx.strokeStyle = building.operational ? '#0af' : '#666';
		ctx.lineWidth = 2;
		ctx.strokeRect(x, y, w, h);

		// Construction progress bar
		if (!building.operational) {
			const barWidth = w - 10;
			const barHeight = 8;
			const barX = x + 5;
			const barY = y + h - 15;

			ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
			ctx.fillRect(barX, barY, barWidth, barHeight);

			ctx.fillStyle = '#0f3';
			ctx.fillRect(barX, barY, barWidth * building.constructionProgress, barHeight);
		}

		// Icon
		ctx.font = `${Math.min(w, h) * 0.4}px serif`;
		ctx.textAlign = 'center';
		ctx.textBaseline = 'middle';
		ctx.fillStyle = building.operational ? '#fff' : '#999';
		ctx.fillText(building.template.icon, x + w / 2, y + h / 2);

		// Name label (small text below icon)
		ctx.font = '10px monospace';
		ctx.fillStyle = '#0af';
		ctx.fillText(building.template.name, x + w / 2, y + h - 25);

		// Efficiency indicator (for operational buildings)
		if (building.operational && building.template.maxWorkers > 0) {
			const efficiencyColor = building.efficiency > 0.7 ? '#0f3' :
			                         building.efficiency > 0.4 ? '#f90' : '#f03';

			// Efficiency bar (top of building)
			const barW = w - 10;
			const barH = 4;
			const barX = x + 5;
			const barY = y + 5;

			ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
			ctx.fillRect(barX, barY, barW, barH);

			ctx.fillStyle = efficiencyColor;
			ctx.fillRect(barX, barY, barW * building.efficiency, barH);

			// Worker count
			ctx.font = '9px monospace';
			ctx.fillStyle = '#fff';
			ctx.textAlign = 'right';
			ctx.fillText(
				`${building.assignedWorkers.length}/${building.template.maxWorkers}`,
				x + w - 5,
				y + 15
			);
		}

		// Production indicator (glowing pulse for active production)
		if (building.operational && building.lastTickProduction > 0) {
			const pulseAlpha = 0.3 + Math.sin(Date.now() / 300) * 0.2;
			ctx.strokeStyle = `rgba(0, 255, 51, ${pulseAlpha})`;
			ctx.lineWidth = 3;
			ctx.strokeRect(x - 2, y - 2, w + 4, h + 4);

			// Production amount (floating text)
			ctx.font = '12px monospace';
			ctx.fillStyle = '#0f3';
			ctx.textAlign = 'center';
			ctx.fillText(
				`+${building.lastTickProduction.toFixed(1)}`,
				x + w / 2,
				y - 10
			);
		}
	}

	function drawSelectionHighlight(building: Building) {
		if (!ctx) return;

		ctx.strokeStyle = '#f0f';
		ctx.lineWidth = 3;
		ctx.setLineDash([5, 5]);
		ctx.strokeRect(
			building.x - 5,
			building.y - 5,
			building.template.width + 10,
			building.template.height + 10
		);
		ctx.setLineDash([]);
	}

	function handleClick(event: MouseEvent) {
		if (!canvas || !village) return;

		const rect = canvas.getBoundingClientRect();
		const x = event.clientX - rect.left;
		const y = event.clientY - rect.top;

		// Check if click hit any building
		for (const building of village.buildings) {
			if (
				x >= building.x &&
				x <= building.x + building.template.width &&
				y >= building.y &&
				y <= building.y + building.template.height
			) {
				// Clicked on this building
				selectedBuilding = building;
				return;
			}
		}

		// Clicked empty space - deselect
		selectedBuilding = null;
	}
</script>

<canvas
	bind:this={canvas}
	{width}
	{height}
	on:click={handleClick}
	style="
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: 3;
		cursor: pointer;
	"
/>

<style>
	canvas {
		image-rendering: crisp-edges;
	}
</style>
