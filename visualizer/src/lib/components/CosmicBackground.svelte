<script lang="ts">
	import { onMount, onDestroy } from 'svelte';

	let canvas: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D | null = null;
	let animationFrame: number;
	let mouseX = 0;
	let mouseY = 0;
	let width = 0;
	let height = 0;

	interface Star {
		x: number;
		y: number;
		z: number;
		size: number;
		color: string;
		twinkleSpeed: number;
		twinklePhase: number;
	}

	interface Nebula {
		x: number;
		y: number;
		radius: number;
		color: string;
		rotation: number;
		rotationSpeed: number;
	}

	interface GeneticStrand {
		points: { x: number; y: number }[];
		color: string;
		phase: number;
		speed: number;
		amplitude: number;
	}

	interface DataStream {
		x: number;
		y: number;
		chars: string[];
		speed: number;
		opacity: number;
	}

	let stars: Star[] = [];
	let nebulae: Nebula[] = [];
	let geneticStrands: GeneticStrand[] = [];
	let dataStreams: DataStream[] = [];
	let time = 0;

	const STAR_COUNT = 200;
	const NEBULA_COUNT = 3;
	const STRAND_COUNT = 5;
	const STREAM_COUNT = 15;

	const COLORS = {
		primary: '#7c9eff',
		secondary: '#a855f7',
		accent: '#22d3ee',
		success: '#4ade80',
		warning: '#fbbf24',
		danger: '#f87171',
		nebula1: 'rgba(124, 158, 255, 0.03)',
		nebula2: 'rgba(168, 85, 247, 0.03)',
		nebula3: 'rgba(34, 211, 238, 0.02)',
	};

	onMount(() => {
		if (!canvas) return;
		ctx = canvas.getContext('2d');
		if (!ctx) return;

		handleResize();
		initElements();
		animate();

		window.addEventListener('resize', handleResize);
		window.addEventListener('mousemove', handleMouseMove);
	});

	onDestroy(() => {
		if (animationFrame) cancelAnimationFrame(animationFrame);
		window.removeEventListener('resize', handleResize);
		window.removeEventListener('mousemove', handleMouseMove);
	});

	function handleResize() {
		width = window.innerWidth;
		height = window.innerHeight;
		if (canvas) {
			canvas.width = width;
			canvas.height = height;
		}
		initElements();
	}

	function handleMouseMove(e: MouseEvent) {
		mouseX = e.clientX;
		mouseY = e.clientY;
	}

	function initElements() {
		// Initialize stars with depth (z)
		stars = Array.from({ length: STAR_COUNT }, () => ({
			x: Math.random() * width,
			y: Math.random() * height,
			z: Math.random() * 3 + 0.5,
			size: Math.random() * 2 + 0.5,
			color: Math.random() > 0.7 ? COLORS.accent : Math.random() > 0.5 ? COLORS.primary : '#ffffff',
			twinkleSpeed: Math.random() * 0.05 + 0.01,
			twinklePhase: Math.random() * Math.PI * 2,
		}));

		// Initialize nebulae
		nebulae = Array.from({ length: NEBULA_COUNT }, (_, i) => ({
			x: (width / (NEBULA_COUNT + 1)) * (i + 1) + (Math.random() - 0.5) * 200,
			y: height * 0.3 + Math.random() * height * 0.4,
			radius: 200 + Math.random() * 300,
			color: [COLORS.nebula1, COLORS.nebula2, COLORS.nebula3][i % 3],
			rotation: Math.random() * Math.PI * 2,
			rotationSpeed: (Math.random() - 0.5) * 0.001,
		}));

		// Initialize genetic strands (DNA-like helixes)
		geneticStrands = Array.from({ length: STRAND_COUNT }, () => {
			const baseX = Math.random() * width;
			const points = Array.from({ length: 50 }, (_, i) => ({
				x: baseX,
				y: (height / 50) * i,
			}));
			return {
				points,
				color: Math.random() > 0.5 ? COLORS.primary : COLORS.secondary,
				phase: Math.random() * Math.PI * 2,
				speed: 0.02 + Math.random() * 0.02,
				amplitude: 30 + Math.random() * 40,
			};
		});

		// Initialize data streams (Matrix-like)
		dataStreams = Array.from({ length: STREAM_COUNT }, () => ({
			x: Math.random() * width,
			y: Math.random() * height - height,
			chars: Array.from({ length: 20 }, () =>
				String.fromCharCode(0x30A0 + Math.random() * 96)
			),
			speed: 1 + Math.random() * 3,
			opacity: 0.1 + Math.random() * 0.2,
		}));
	}

	function drawStar(star: Star) {
		if (!ctx) return;

		const twinkle = Math.sin(time * star.twinkleSpeed + star.twinklePhase) * 0.5 + 0.5;
		const parallaxX = (mouseX - width / 2) * 0.01 * star.z;
		const parallaxY = (mouseY - height / 2) * 0.01 * star.z;

		ctx.save();
		ctx.globalAlpha = 0.3 + twinkle * 0.7;

		// Star glow
		const gradient = ctx.createRadialGradient(
			star.x + parallaxX, star.y + parallaxY, 0,
			star.x + parallaxX, star.y + parallaxY, star.size * 3
		);
		gradient.addColorStop(0, star.color);
		gradient.addColorStop(1, 'transparent');
		ctx.fillStyle = gradient;
		ctx.beginPath();
		ctx.arc(star.x + parallaxX, star.y + parallaxY, star.size * 3, 0, Math.PI * 2);
		ctx.fill();

		// Star core
		ctx.fillStyle = star.color;
		ctx.beginPath();
		ctx.arc(star.x + parallaxX, star.y + parallaxY, star.size, 0, Math.PI * 2);
		ctx.fill();

		ctx.restore();
	}

	function drawNebula(nebula: Nebula) {
		if (!ctx) return;

		ctx.save();
		ctx.translate(nebula.x, nebula.y);
		ctx.rotate(nebula.rotation);

		// Multiple layers of gradient for depth
		for (let i = 0; i < 3; i++) {
			const gradient = ctx.createRadialGradient(
				0, 0, 0,
				0, 0, nebula.radius * (1 - i * 0.2)
			);
			gradient.addColorStop(0, nebula.color);
			gradient.addColorStop(0.5, nebula.color.replace('0.03', '0.02'));
			gradient.addColorStop(1, 'transparent');

			ctx.fillStyle = gradient;
			ctx.beginPath();
			ctx.ellipse(0, 0, nebula.radius * (1 - i * 0.2), nebula.radius * 0.6 * (1 - i * 0.2), 0, 0, Math.PI * 2);
			ctx.fill();
		}

		ctx.restore();
	}

	function drawGeneticStrand(strand: GeneticStrand) {
		if (!ctx) return;

		ctx.save();
		ctx.globalAlpha = 0.15;
		ctx.strokeStyle = strand.color;
		ctx.lineWidth = 2;

		// Draw double helix
		for (let offset = 0; offset < 2; offset++) {
			ctx.beginPath();
			strand.points.forEach((point, i) => {
				const wave = Math.sin((i * 0.15) + strand.phase + (offset * Math.PI)) * strand.amplitude;
				const x = point.x + wave;
				const y = point.y;

				if (i === 0) ctx.moveTo(x, y);
				else ctx.lineTo(x, y);
			});
			ctx.stroke();
		}

		// Draw connecting bars
		ctx.globalAlpha = 0.08;
		ctx.strokeStyle = COLORS.accent;
		strand.points.forEach((point, i) => {
			if (i % 4 === 0) {
				const wave1 = Math.sin((i * 0.15) + strand.phase) * strand.amplitude;
				const wave2 = Math.sin((i * 0.15) + strand.phase + Math.PI) * strand.amplitude;
				ctx.beginPath();
				ctx.moveTo(point.x + wave1, point.y);
				ctx.lineTo(point.x + wave2, point.y);
				ctx.stroke();
			}
		});

		ctx.restore();
	}

	function drawDataStream(stream: DataStream) {
		if (!ctx) return;

		ctx.save();
		ctx.font = '14px monospace';

		stream.chars.forEach((char, i) => {
			const y = stream.y + i * 20;
			if (y < 0 || y > height) return;

			const fade = 1 - (i / stream.chars.length);
			ctx.globalAlpha = stream.opacity * fade;
			ctx.fillStyle = i === 0 ? '#ffffff' : COLORS.success;
			ctx.fillText(char, stream.x, y);
		});

		ctx.restore();
	}

	function drawGridLines() {
		if (!ctx) return;

		ctx.save();
		ctx.strokeStyle = COLORS.primary;
		ctx.globalAlpha = 0.03;
		ctx.lineWidth = 1;

		// Horizontal lines
		for (let y = 0; y < height; y += 50) {
			ctx.beginPath();
			ctx.moveTo(0, y);
			ctx.lineTo(width, y);
			ctx.stroke();
		}

		// Vertical lines
		for (let x = 0; x < width; x += 50) {
			ctx.beginPath();
			ctx.moveTo(x, 0);
			ctx.lineTo(x, height);
			ctx.stroke();
		}

		ctx.restore();
	}

	function update() {
		time += 1;

		// Update nebula rotations
		nebulae.forEach(nebula => {
			nebula.rotation += nebula.rotationSpeed;
		});

		// Update genetic strand phases
		geneticStrands.forEach(strand => {
			strand.phase += strand.speed;
		});

		// Update data streams
		dataStreams.forEach(stream => {
			stream.y += stream.speed;
			if (stream.y > height + 400) {
				stream.y = -400;
				stream.x = Math.random() * width;
				stream.chars = Array.from({ length: 20 }, () =>
					String.fromCharCode(0x30A0 + Math.random() * 96)
				);
			}
			// Randomly change characters
			if (Math.random() < 0.1) {
				const idx = Math.floor(Math.random() * stream.chars.length);
				stream.chars[idx] = String.fromCharCode(0x30A0 + Math.random() * 96);
			}
		});
	}

	function draw() {
		if (!ctx) return;

		// Clear with slight fade for trails
		ctx.fillStyle = 'rgba(10, 14, 26, 0.1)';
		ctx.fillRect(0, 0, width, height);

		// Draw background elements in order
		drawGridLines();
		nebulae.forEach(drawNebula);
		geneticStrands.forEach(drawGeneticStrand);
		stars.forEach(drawStar);
		dataStreams.forEach(drawDataStream);
	}

	function animate() {
		update();
		draw();
		animationFrame = requestAnimationFrame(animate);
	}
</script>

<canvas
	bind:this={canvas}
	class="cosmic-background"
/>

<style>
	.cosmic-background {
		position: fixed;
		top: 0;
		left: 0;
		width: 100vw;
		height: 100vh;
		pointer-events: none;
		z-index: -1;
	}
</style>
