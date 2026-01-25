<script lang="ts">
	import { onMount, onDestroy, afterUpdate } from 'svelte';
	import type { Being } from '$lib/models/Being';

	export let beings: Being[] = [];
	export let width: number = 0;
	export let height: number = 0;
	export let showLabels: boolean = false;
	export let showFitness: boolean = true;

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
		// Redraw when beings update
		if (ctx && canvas) {
			draw();
		}
	});

	function render() {
		draw();
		animationFrame = requestAnimationFrame(render);
	}

	function draw() {
		if (!ctx || !canvas) return;

		// Clear canvas
		ctx.clearRect(0, 0, width, height);

		// Draw all alive beings
		const aliveBings = beings.filter(b => b.alive);

		for (const being of aliveBings) {
			drawBeing(being);
		}

		// Draw cooperation connections (swarm lines)
		if (showLabels) {
			ctx.globalAlpha = 0.2;
			for (const being of aliveBings) {
				for (const cooperatorId of being.cooperatingWith) {
					const cooperator = aliveBings.find(b => b.id === cooperatorId);
					if (cooperator) {
						ctx.strokeStyle = being.color;
						ctx.lineWidth = 1;
						ctx.beginPath();
						ctx.moveTo(being.x, being.y);
						ctx.lineTo(cooperator.x, cooperator.y);
						ctx.stroke();
					}
				}
			}
			ctx.globalAlpha = 1.0;
		}
	}

	function drawBeing(being: Being) {
		if (!ctx) return;

		const x = being.x;
		const y = being.y;
		const size = being.size;

		// Draw fitness halo (if enabled)
		if (showFitness) {
			const haloSize = size + being.fitness * 4;
			ctx.globalAlpha = being.fitness * 0.3;
			ctx.fillStyle = being.color;
			ctx.beginPath();
			ctx.arc(x, y, haloSize, 0, Math.PI * 2);
			ctx.fill();
			ctx.globalAlpha = 1.0;
		}

		// Draw being core
		ctx.fillStyle = being.color;
		ctx.beginPath();
		ctx.arc(x, y, size, 0, Math.PI * 2);
		ctx.fill();

		// Draw investigating state (pulsing ring)
		if (being.investigating) {
			ctx.strokeStyle = being.color;
			ctx.lineWidth = 1.5;
			const pulseSize = size + 3 + Math.sin(Date.now() / 200) * 2;
			ctx.beginPath();
			ctx.arc(x, y, pulseSize, 0, Math.PI * 2);
			ctx.stroke();
		}

		// Draw energy indicator (small bar)
		if (showLabels) {
			const barWidth = 20;
			const barHeight = 3;
			ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
			ctx.fillRect(x - barWidth / 2, y + size + 4, barWidth, barHeight);
			ctx.fillStyle = being.energy > 0.5 ? '#0f3' : being.energy > 0.2 ? '#f90' : '#f03';
			ctx.fillRect(x - barWidth / 2, y + size + 4, barWidth * being.energy, barHeight);
		}

		// Draw generation number (tiny text)
		if (showLabels && being.generation > 0) {
			ctx.fillStyle = '#fff';
			ctx.font = '8px monospace';
			ctx.textAlign = 'center';
			ctx.fillText(`G${being.generation}`, x, y - size - 4);
		}
	}
</script>

<canvas
	bind:this={canvas}
	{width}
	{height}
	style="
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		pointer-events: none;
		z-index: 5;
	"
/>

<style>
	canvas {
		image-rendering: crisp-edges;
	}
</style>
