<script lang="ts">
	import { onMount, onDestroy } from 'svelte';

	export let width: number = 0;
	export let height: number = 0;
	export let particleCount: number = 500;
	export let components: Array<{x: number, y: number, w: number, h: number, active: boolean, type: string}> = [];
	export let connections: Array<{x1: number, y1: number, x2: number, y2: number, active: boolean}> = [];

	interface Particle {
		x: number;
		y: number;
		vx: number;
		vy: number;
		color: string;
		type: 'data' | 'process' | 'energy' | 'error';
		size: number;
		energy: number;
		targetComponent: number | null;
		targetConnection: number | null;
		investigating: boolean;
	}

	let particles: Particle[] = [];
	let canvas: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D | null = null;
	let animationFrame: number;

	// Boids parameters
	const SEPARATION_RADIUS = 15;
	const ALIGNMENT_RADIUS = 30;
	const COHESION_RADIUS = 40;
	const MAX_SPEED = 2;
	const MAX_FORCE = 0.05;
	const SEPARATION_WEIGHT = 1.5;
	const ALIGNMENT_WEIGHT = 1.0;
	const COHESION_WEIGHT = 0.8;
	const COMPONENT_ATTRACTION = 0.3;
	const CONNECTION_FLOW_FORCE = 0.5;

	// Color palette
	const COLORS = {
		data: '#09f',      // Blue - data particles
		process: '#f90',   // Orange - processing
		energy: '#0f3',    // Green - energy/success
		error: '#f03'      // Red - errors
	};

	onMount(() => {
		if (!canvas) return;
		ctx = canvas.getContext('2d');
		if (!ctx) return;

		// Initialize particles
		initParticles();

		// Start animation loop
		animate();
	});

	onDestroy(() => {
		if (animationFrame) {
			cancelAnimationFrame(animationFrame);
		}
	});

	function initParticles() {
		particles = [];
		for (let i = 0; i < particleCount; i++) {
			const type = Math.random() < 0.4 ? 'data' :
			             Math.random() < 0.7 ? 'process' :
			             Math.random() < 0.9 ? 'energy' : 'error';

			particles.push({
				x: Math.random() * width,
				y: Math.random() * height,
				vx: (Math.random() - 0.5) * 2,
				vy: (Math.random() - 0.5) * 2,
				color: COLORS[type],
				type,
				size: type === 'error' ? 3 : 2,
				energy: Math.random(),
				targetComponent: null,
				targetConnection: null,
				investigating: false
			});
		}
	}

	// Boids algorithm - Separation
	function separate(particle: Particle, neighbors: Particle[]): {x: number, y: number} {
		let steer = {x: 0, y: 0};
		let count = 0;

		for (const other of neighbors) {
			const d = distance(particle, other);
			if (d > 0 && d < SEPARATION_RADIUS) {
				const diff = {
					x: particle.x - other.x,
					y: particle.y - other.y
				};
				const magnitude = Math.sqrt(diff.x * diff.x + diff.y * diff.y);
				steer.x += diff.x / magnitude / d;
				steer.y += diff.y / magnitude / d;
				count++;
			}
		}

		if (count > 0) {
			steer.x /= count;
			steer.y /= count;
		}

		return steer;
	}

	// Boids algorithm - Alignment
	function align(particle: Particle, neighbors: Particle[]): {x: number, y: number} {
		let avg = {x: 0, y: 0};
		let count = 0;

		for (const other of neighbors) {
			const d = distance(particle, other);
			if (d > 0 && d < ALIGNMENT_RADIUS) {
				avg.x += other.vx;
				avg.y += other.vy;
				count++;
			}
		}

		if (count > 0) {
			avg.x /= count;
			avg.y /= count;
			return normalize(avg);
		}

		return {x: 0, y: 0};
	}

	// Boids algorithm - Cohesion
	function cohere(particle: Particle, neighbors: Particle[]): {x: number, y: number} {
		let center = {x: 0, y: 0};
		let count = 0;

		for (const other of neighbors) {
			const d = distance(particle, other);
			if (d > 0 && d < COHESION_RADIUS) {
				center.x += other.x;
				center.y += other.y;
				count++;
			}
		}

		if (count > 0) {
			center.x /= count;
			center.y /= count;
			return seek(particle, center);
		}

		return {x: 0, y: 0};
	}

	// Seek a target
	function seek(particle: Particle, target: {x: number, y: number}): {x: number, y: number} {
		const desired = {
			x: target.x - particle.x,
			y: target.y - particle.y
		};
		const d = Math.sqrt(desired.x * desired.x + desired.y * desired.y);

		if (d > 0) {
			desired.x = (desired.x / d) * MAX_SPEED;
			desired.y = (desired.y / d) * MAX_SPEED;
		}

		const steer = {
			x: desired.x - particle.vx,
			y: desired.y - particle.vy
		};

		return limit(steer, MAX_FORCE);
	}

	// Component attraction - particles investigate components
	function attractToComponents(particle: Particle): {x: number, y: number} {
		let force = {x: 0, y: 0};

		for (let i = 0; i < components.length; i++) {
			const comp = components[i];
			const centerX = comp.x + comp.w / 2;
			const centerY = comp.y + comp.h / 2;
			const d = Math.sqrt((particle.x - centerX) ** 2 + (particle.y - centerY) ** 2);

			// Active components attract more strongly
			const attraction = comp.active ? COMPONENT_ATTRACTION * 2 : COMPONENT_ATTRACTION;

			if (d < 150 && d > 20) {
				// Attraction force inversely proportional to distance
				const strength = attraction / d;
				force.x += (centerX - particle.x) * strength;
				force.y += (centerY - particle.y) * strength;

				// Mark as investigating
				if (d < 80 && !particle.investigating) {
					particle.investigating = true;
					particle.targetComponent = i;
				}
			}
		}

		return force;
	}

	// Connection flow - particles flow through active connections
	function flowThroughConnections(particle: Particle): {x: number, y: number} {
		let force = {x: 0, y: 0};

		for (let i = 0; i < connections.length; i++) {
			const conn = connections[i];
			if (!conn.active) continue;

			// Calculate closest point on connection line
			const lineVec = {x: conn.x2 - conn.x1, y: conn.y2 - conn.y1};
			const lineLen = Math.sqrt(lineVec.x ** 2 + lineVec.y ** 2);
			const lineDir = {x: lineVec.x / lineLen, y: lineVec.y / lineLen};

			const toParticle = {x: particle.x - conn.x1, y: particle.y - conn.y1};
			const projection = toParticle.x * lineDir.x + toParticle.y * lineDir.y;
			const clamped = Math.max(0, Math.min(lineLen, projection));

			const closest = {
				x: conn.x1 + lineDir.x * clamped,
				y: conn.y1 + lineDir.y * clamped
			};

			const distToLine = Math.sqrt((particle.x - closest.x) ** 2 + (particle.y - closest.y) ** 2);

			// If near connection, flow along it
			if (distToLine < 30) {
				force.x += lineDir.x * CONNECTION_FLOW_FORCE;
				force.y += lineDir.y * CONNECTION_FLOW_FORCE;
				particle.targetConnection = i;
			}
		}

		return force;
	}

	function updateParticles() {
		for (let i = 0; i < particles.length; i++) {
			const particle = particles[i];

			// Get neighbors
			const neighbors = particles.filter((_, j) => i !== j);

			// Apply boids rules
			const separation = separate(particle, neighbors);
			const alignment = align(particle, neighbors);
			const cohesion = cohere(particle, neighbors);
			const componentAttraction = attractToComponents(particle);
			const connectionFlow = flowThroughConnections(particle);

			// Weighted sum of forces
			const ax = separation.x * SEPARATION_WEIGHT +
			          alignment.x * ALIGNMENT_WEIGHT +
			          cohesion.x * COHESION_WEIGHT +
			          componentAttraction.x +
			          connectionFlow.x;

			const ay = separation.y * SEPARATION_WEIGHT +
			          alignment.y * ALIGNMENT_WEIGHT +
			          cohesion.y * COHESION_WEIGHT +
			          componentAttraction.y +
			          connectionFlow.y;

			// Update velocity
			particle.vx += ax;
			particle.vy += ay;

			// Limit speed
			const speed = Math.sqrt(particle.vx ** 2 + particle.vy ** 2);
			if (speed > MAX_SPEED) {
				particle.vx = (particle.vx / speed) * MAX_SPEED;
				particle.vy = (particle.vy / speed) * MAX_SPEED;
			}

			// Update position
			particle.x += particle.vx;
			particle.y += particle.vy;

			// Wrap around edges
			if (particle.x < 0) particle.x = width;
			if (particle.x > width) particle.x = 0;
			if (particle.y < 0) particle.y = height;
			if (particle.y > height) particle.y = 0;

			// Update energy (pulsing effect)
			particle.energy = (particle.energy + 0.02) % 1;

			// Reset investigating state if far from components
			if (particle.targetComponent !== null) {
				const comp = components[particle.targetComponent];
				const centerX = comp.x + comp.w / 2;
				const centerY = comp.y + comp.h / 2;
				const d = Math.sqrt((particle.x - centerX) ** 2 + (particle.y - centerY) ** 2);
				if (d > 150) {
					particle.investigating = false;
					particle.targetComponent = null;
				}
			}
		}
	}

	function drawParticles() {
		if (!ctx) return;

		ctx.clearRect(0, 0, width, height);

		for (const particle of particles) {
			// Alpha based on energy (pulsing)
			const alpha = 0.3 + particle.energy * 0.7;

			// Draw particle
			ctx.fillStyle = particle.color;
			ctx.globalAlpha = alpha;
			ctx.beginPath();
			ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
			ctx.fill();

			// Glow effect for investigating particles
			if (particle.investigating) {
				ctx.globalAlpha = alpha * 0.3;
				ctx.beginPath();
				ctx.arc(particle.x, particle.y, particle.size * 3, 0, Math.PI * 2);
				ctx.fill();
			}
		}

		ctx.globalAlpha = 1;
	}

	function animate() {
		updateParticles();
		drawParticles();
		animationFrame = requestAnimationFrame(animate);
	}

	// Helper functions
	function distance(p1: Particle, p2: Particle): number {
		return Math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2);
	}

	function normalize(vec: {x: number, y: number}): {x: number, y: number} {
		const mag = Math.sqrt(vec.x ** 2 + vec.y ** 2);
		if (mag > 0) {
			return {x: vec.x / mag * MAX_SPEED, y: vec.y / mag * MAX_SPEED};
		}
		return {x: 0, y: 0};
	}

	function limit(vec: {x: number, y: number}, max: number): {x: number, y: number} {
		const mag = Math.sqrt(vec.x ** 2 + vec.y ** 2);
		if (mag > max) {
			return {x: vec.x / mag * max, y: vec.y / mag * max};
		}
		return vec;
	}

	// Reactive updates
	$: if (width && height && particles.length === 0) {
		initParticles();
	}

	$: if (width && height && canvas) {
		canvas.width = width;
		canvas.height = height;
	}
</script>

<canvas
	bind:this={canvas}
	class="particle-canvas"
	width={width}
	height={height}
/>

<style>
	.particle-canvas {
		position: absolute;
		top: 0;
		left: 0;
		pointer-events: none;
		z-index: 5;
	}
</style>
