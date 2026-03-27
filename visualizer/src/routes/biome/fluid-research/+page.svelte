<script lang="ts">
	/** Phase 5B placeholder: MLS-MPM + SSFR is a parallel architecture (Codrops / Matsuoka, 2025). */
	export let params: Record<string, string> | undefined = undefined;
	void params;
</script>

<div class="page card-glass">
	<h1>WebGPU fluid research track</h1>
	<p>
		This route documents the <strong>separate product / package</strong> path for MLS-MPM simulation and
		screen-space fluid rendering (SSFR). It intentionally does not replace the default
		<a href="/biome">/biome</a> WebGL + <code>Water</code> stack.
	</p>
	<ul>
		<li>
			<a
				href="https://tympanus.net/codrops/2025/02/26/webgpu-fluid-simulations-high-performance-real-time-rendering/"
				target="_blank"
				rel="noopener noreferrer"
			>
				Codrops — WebGPU fluid simulations (Matsuoka, 2025)
			</a>
		</li>
		<li>Reference demos: WebGPU-Ocean, WaterBall (cited in that article).</li>
		<li>Integration stance: new route or embed, half-res SSFR by default, device capability probes, no entanglement with Three.js <code>Water</code> until stable.</li>
	</ul>
	<p><a href="/biome">← Back to biome simulator</a></p>
</div>

<style>
	.page {
		max-width: 720px;
		margin: 1.5rem auto;
		padding: 1.25rem;
		border: 1px solid var(--border);
		border-radius: 10px;
	}
	h1 {
		font-size: 1.25rem;
		margin-bottom: 0.75rem;
	}
	p,
	li {
		font-size: 0.9rem;
		color: var(--text-secondary);
		line-height: 1.6;
	}
	ul {
		margin: 1rem 0;
		padding-left: 1.25rem;
	}
	a {
		color: var(--primary-light);
	}
	code {
		font-size: 0.85em;
	}
</style>
