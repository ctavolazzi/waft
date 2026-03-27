<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import type { Writable } from 'svelte/store';
	export let params: Record<string, string> | undefined = undefined;
	void params;

	// Dashboard layout configuration
	interface DashboardWidget {
		id: string;
		type: string;
		title: string;
		x: number;
		y: number;
		w: number;
		h: number;
		component?: any;
	}

	interface DashboardLayout {
		widgets: DashboardWidget[];
	}

	// Available widget types
	const WIDGET_TYPES = {
		PROJECT: 'project',
		GYM: 'gym',
		EVOLUTION: 'evolution',
		EMPIRICA: 'empirica',
		GIT: 'git',
		COMMANDS: 'commands',
		LOGS: 'logs',
		STATS: 'stats',
		BEING: 'being',
		CAMPFIRE: 'campfire',
		CARTOGRAPHER: 'cartographer',
		WORK_EFFORTS: 'work_efforts',
		PYRITE: 'pyrite'
	};

	// Default dashboard layout
	const defaultLayout: DashboardLayout = {
		widgets: [
			{ id: 'project-info', type: WIDGET_TYPES.PROJECT, title: 'Project Info', x: 0, y: 0, w: 4, h: 2 },
			{ id: 'gym-status', type: WIDGET_TYPES.GYM, title: 'Scint Gym', x: 4, y: 0, w: 4, h: 2 },
			{ id: 'evolution', type: WIDGET_TYPES.EVOLUTION, title: 'Evolution', x: 8, y: 0, w: 4, h: 2 },
			{ id: 'git-status', type: WIDGET_TYPES.GIT, title: 'Git Status', x: 0, y: 2, w: 6, h: 3 },
			{ id: 'commands', type: WIDGET_TYPES.COMMANDS, title: 'Quick Commands', x: 6, y: 2, w: 6, h: 3 },
			{ id: 'empirica', type: WIDGET_TYPES.EMPIRICA, title: 'Empirica', x: 0, y: 5, w: 4, h: 2 },
			{ id: 'being', type: WIDGET_TYPES.BEING, title: 'Being Status', x: 4, y: 5, w: 4, h: 2 },
			{ id: 'stats', type: WIDGET_TYPES.STATS, title: 'System Stats', x: 8, y: 5, w: 4, h: 2 }
		]
	};

	// Reactive state
	let layout: Writable<DashboardLayout> = writable(defaultLayout);
	let draggedWidget: DashboardWidget | null = null;
	let dragOffset = { x: 0, y: 0 };
	let editMode = false;
	let showAddWidget = false;

	// Load saved layout from localStorage
	onMount(() => {
		const savedLayout = localStorage.getItem('waft-dashboard-layout');
		if (savedLayout) {
			try {
				layout.set(JSON.parse(savedLayout));
			} catch (e) {
				console.error('Failed to load saved layout:', e);
			}
		}
	});

	// Save layout to localStorage
	function saveLayout() {
		localStorage.setItem('waft-dashboard-layout', JSON.stringify($layout));
	}

	// Widget drag handlers
	function startDrag(widget: DashboardWidget, event: MouseEvent) {
		if (!editMode) return;
		draggedWidget = widget;
		const target = event.target as HTMLElement;
		const rect = target.getBoundingClientRect();
		dragOffset = {
			x: event.clientX - rect.left,
			y: event.clientY - rect.top
		};
	}

	function drag(event: MouseEvent) {
		if (!draggedWidget || !editMode) return;
		event.preventDefault();

		const gridSize = 100; // pixels per grid unit
		const x = Math.floor((event.clientX - dragOffset.x) / gridSize);
		const y = Math.floor((event.clientY - dragOffset.y) / gridSize);

		// Update widget position
		layout.update(l => {
			const widget = l.widgets.find(w => w.id === draggedWidget?.id);
			if (widget) {
				widget.x = Math.max(0, x);
				widget.y = Math.max(0, y);
			}
			return l;
		});
	}

	function endDrag() {
		if (draggedWidget) {
			saveLayout();
			draggedWidget = null;
		}
	}

	// Add new widget
	function addWidget(type: string) {
		const newWidget: DashboardWidget = {
			id: `widget-${Date.now()}`,
			type,
			title: type.replace('_', ' ').toUpperCase(),
			x: 0,
			y: 0,
			w: 4,
			h: 2
		};
		layout.update(l => {
			l.widgets.push(newWidget);
			return l;
		});
		saveLayout();
		showAddWidget = false;
	}

	// Remove widget
	function removeWidget(id: string) {
		layout.update(l => {
			l.widgets = l.widgets.filter(w => w.id !== id);
			return l;
		});
		saveLayout();
	}

	// Reset to default layout
	function resetLayout() {
		layout.set(defaultLayout);
		saveLayout();
	}
</script>

<svelte:window on:mousemove={drag} on:mouseup={endDrag} />

<div class="mission-control">
	<!-- Header -->
	<div class="control-header">
		<div class="header-left">
			<h1 class="control-title">🚀 WAFT Mission Control</h1>
			<p class="control-subtitle">Evolutionary Code Laboratory Dashboard</p>
		</div>
		<div class="header-right">
			<button
				class="btn btn-sm {editMode ? 'btn-primary' : 'btn-secondary'}"
				on:click={() => editMode = !editMode}
			>
				{editMode ? '✓ Done Editing' : '✏️ Edit Layout'}
			</button>
			<button class="btn btn-sm btn-secondary" on:click={() => showAddWidget = true}>
				➕ Add Widget
			</button>
			<button class="btn btn-sm btn-secondary" on:click={resetLayout}>
				🔄 Reset Layout
			</button>
		</div>
	</div>

	<!-- Dashboard Grid -->
	<div class="dashboard-grid">
		{#each $layout.widgets as widget (widget.id)}
			<div
				class="widget"
				class:dragging={draggedWidget?.id === widget.id}
				class:editable={editMode}
				style="
					grid-column: {widget.x + 1} / span {widget.w};
					grid-row: {widget.y + 1} / span {widget.h};
				"
				on:mousedown={(e) => startDrag(widget, e)}
			>
				<div class="widget-header">
					<h3 class="widget-title">{widget.title}</h3>
					<div class="widget-controls">
						{#if editMode}
							<button class="btn-icon" on:click={() => removeWidget(widget.id)}>
								❌
							</button>
						{/if}
					</div>
				</div>
				<div class="widget-content">
					{#if widget.type === WIDGET_TYPES.PROJECT}
						<div class="widget-data">
							<div class="data-row">
								<span class="label">Name:</span>
								<span class="value">WAFT</span>
							</div>
							<div class="data-row">
								<span class="label">Version:</span>
								<span class="value">0.9.4</span>
							</div>
							<div class="data-row">
								<span class="label">Status:</span>
								<span class="badge badge-success">Active</span>
							</div>
						</div>
					{:else if widget.type === WIDGET_TYPES.GYM}
						<div class="widget-data">
							<div class="stat-card">
								<div class="stat-value">15</div>
								<div class="stat-label">Quests Completed</div>
							</div>
							<div class="stat-card">
								<div class="stat-value">87%</div>
								<div class="stat-label">Success Rate</div>
							</div>
							<div class="stat-card">
								<div class="stat-value">42</div>
								<div class="stat-label">Scints Stabilized</div>
							</div>
						</div>
					{:else if widget.type === WIDGET_TYPES.EVOLUTION}
						<div class="widget-data">
							<div class="data-row">
								<span class="label">Generation:</span>
								<span class="value">Gen 5</span>
							</div>
							<div class="data-row">
								<span class="label">Fitness:</span>
								<span class="value">0.78</span>
							</div>
							<div class="data-row">
								<span class="label">Status:</span>
								<span class="badge badge-info">Evolving</span>
							</div>
						</div>
					{:else if widget.type === WIDGET_TYPES.GIT}
						<div class="widget-data">
							<div class="data-row">
								<span class="label">Branch:</span>
								<span class="value mono">claude/go-to-town-vWLDW</span>
							</div>
							<div class="data-row">
								<span class="label">Status:</span>
								<span class="badge badge-success">Clean</span>
							</div>
							<div class="data-row">
								<span class="label">Remote:</span>
								<span class="value">origin/main</span>
							</div>
						</div>
					{:else if widget.type === WIDGET_TYPES.COMMANDS}
						<div class="command-grid">
							<button class="cmd-btn">
								<span class="cmd-icon">🧬</span>
								<span class="cmd-label">Evolve</span>
							</button>
							<button class="cmd-btn">
								<span class="cmd-icon">🏋️</span>
								<span class="cmd-label">Gym</span>
							</button>
							<button class="cmd-btn">
								<span class="cmd-icon">🔬</span>
								<span class="cmd-label">Oracle</span>
							</button>
							<button class="cmd-btn">
								<span class="cmd-icon">📊</span>
								<span class="cmd-label">Stats</span>
							</button>
							<button class="cmd-btn">
								<span class="cmd-icon">🔥</span>
								<span class="cmd-label">Campfire</span>
							</button>
							<button class="cmd-btn">
								<span class="cmd-icon">🗺️</span>
								<span class="cmd-label">Cartographer</span>
							</button>
						</div>
					{:else if widget.type === WIDGET_TYPES.EMPIRICA}
						<div class="widget-data">
							<div class="data-row">
								<span class="label">Certainty:</span>
								<span class="value">0.82</span>
							</div>
							<div class="data-row">
								<span class="label">Findings:</span>
								<span class="value">37</span>
							</div>
							<div class="data-row">
								<span class="label">Unknowns:</span>
								<span class="value">12</span>
							</div>
						</div>
					{:else if widget.type === WIDGET_TYPES.BEING}
						<div class="widget-data">
							<div class="data-row">
								<span class="label">State:</span>
								<span class="badge badge-success">Operational</span>
							</div>
							<div class="data-row">
								<span class="label">Mode:</span>
								<span class="value">Autonomous</span>
							</div>
							<div class="data-row">
								<span class="label">Integrity:</span>
								<span class="value">98%</span>
							</div>
						</div>
					{:else if widget.type === WIDGET_TYPES.STATS}
						<div class="widget-data">
							<div class="stat-card">
								<div class="stat-value">1,247</div>
								<div class="stat-label">Total Commands</div>
							</div>
							<div class="stat-card">
								<div class="stat-value">99.2%</div>
								<div class="stat-label">Uptime</div>
							</div>
						</div>
					{:else}
						<div class="widget-placeholder">
							<p>Widget type: {widget.type}</p>
							<p class="text-muted">Coming soon...</p>
						</div>
					{/if}
				</div>
			</div>
		{/each}
	</div>

	<!-- Add Widget Modal -->
	{#if showAddWidget}
		<div class="modal-overlay" on:click={() => showAddWidget = false}>
			<div class="modal" on:click|stopPropagation>
				<div class="modal-header">
					<h2>Add Widget</h2>
					<button class="btn-close" on:click={() => showAddWidget = false}>×</button>
				</div>
				<div class="modal-body">
					<div class="widget-types">
						{#each Object.entries(WIDGET_TYPES) as [key, type]}
							<button class="widget-type-btn" on:click={() => addWidget(type)}>
								<span class="widget-type-name">{key.replace('_', ' ')}</span>
							</button>
						{/each}
					</div>
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.mission-control {
		min-height: 100vh;
		background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
		color: #e0e0e0;
		padding: 20px;
	}

	.control-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 30px;
		padding: 20px;
		background: rgba(255, 255, 255, 0.05);
		border-radius: 12px;
		backdrop-filter: blur(10px);
	}

	.control-title {
		font-size: 2rem;
		font-weight: bold;
		margin: 0;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
	}

	.control-subtitle {
		margin: 5px 0 0 0;
		color: #999;
		font-size: 0.9rem;
	}

	.header-right {
		display: flex;
		gap: 10px;
	}

	.btn {
		padding: 8px 16px;
		border: none;
		border-radius: 6px;
		cursor: pointer;
		font-weight: 500;
		transition: all 0.2s;
	}

	.btn-sm {
		font-size: 0.85rem;
	}

	.btn-primary {
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: white;
	}

	.btn-primary:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
	}

	.btn-secondary {
		background: rgba(255, 255, 255, 0.1);
		color: #e0e0e0;
	}

	.btn-secondary:hover {
		background: rgba(255, 255, 255, 0.15);
	}

	.dashboard-grid {
		display: grid;
		grid-template-columns: repeat(12, 1fr);
		grid-auto-rows: 150px;
		gap: 20px;
	}

	.widget {
		background: rgba(255, 255, 255, 0.05);
		border-radius: 12px;
		padding: 15px;
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.1);
		transition: all 0.3s;
		overflow: hidden;
	}

	.widget:hover {
		border-color: rgba(102, 126, 234, 0.5);
		box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);
	}

	.widget.editable {
		cursor: move;
	}

	.widget.dragging {
		opacity: 0.7;
		transform: scale(1.05);
		z-index: 1000;
	}

	.widget-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 15px;
	}

	.widget-title {
		margin: 0;
		font-size: 1.1rem;
		font-weight: 600;
		color: #667eea;
	}

	.widget-controls {
		display: flex;
		gap: 5px;
	}

	.btn-icon {
		background: none;
		border: none;
		cursor: pointer;
		font-size: 1rem;
		padding: 4px;
		opacity: 0.6;
		transition: opacity 0.2s;
	}

	.btn-icon:hover {
		opacity: 1;
	}

	.widget-content {
		height: calc(100% - 40px);
		overflow: auto;
	}

	.widget-data {
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	.data-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 8px 0;
		border-bottom: 1px solid rgba(255, 255, 255, 0.05);
	}

	.label {
		color: #999;
		font-size: 0.9rem;
	}

	.value {
		color: #e0e0e0;
		font-weight: 500;
	}

	.mono {
		font-family: 'Courier New', monospace;
		font-size: 0.85rem;
	}

	.badge {
		padding: 4px 12px;
		border-radius: 12px;
		font-size: 0.8rem;
		font-weight: 600;
	}

	.badge-success {
		background: rgba(34, 197, 94, 0.2);
		color: #22c55e;
	}

	.badge-info {
		background: rgba(59, 130, 246, 0.2);
		color: #3b82f6;
	}

	.stat-card {
		text-align: center;
		padding: 15px;
		background: rgba(255, 255, 255, 0.03);
		border-radius: 8px;
	}

	.stat-value {
		font-size: 2rem;
		font-weight: bold;
		color: #667eea;
		margin-bottom: 5px;
	}

	.stat-label {
		font-size: 0.85rem;
		color: #999;
	}

	.command-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 10px;
	}

	.cmd-btn {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 8px;
		padding: 15px;
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 8px;
		cursor: pointer;
		transition: all 0.2s;
	}

	.cmd-btn:hover {
		background: rgba(102, 126, 234, 0.2);
		border-color: rgba(102, 126, 234, 0.5);
		transform: translateY(-2px);
	}

	.cmd-icon {
		font-size: 1.5rem;
	}

	.cmd-label {
		font-size: 0.85rem;
		color: #e0e0e0;
	}

	.widget-placeholder {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100%;
		color: #666;
	}

	.text-muted {
		color: #666;
		font-size: 0.85rem;
	}

	.modal-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.7);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 2000;
	}

	.modal {
		background: #1a1a2e;
		border-radius: 12px;
		padding: 0;
		max-width: 600px;
		width: 90%;
		max-height: 80vh;
		overflow: hidden;
	}

	.modal-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 20px;
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	}

	.modal-header h2 {
		margin: 0;
		color: #667eea;
	}

	.btn-close {
		background: none;
		border: none;
		font-size: 2rem;
		color: #999;
		cursor: pointer;
		line-height: 1;
	}

	.btn-close:hover {
		color: #e0e0e0;
	}

	.modal-body {
		padding: 20px;
	}

	.widget-types {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
		gap: 10px;
	}

	.widget-type-btn {
		padding: 15px;
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 8px;
		cursor: pointer;
		transition: all 0.2s;
		color: #e0e0e0;
	}

	.widget-type-btn:hover {
		background: rgba(102, 126, 234, 0.2);
		border-color: rgba(102, 126, 234, 0.5);
		transform: translateY(-2px);
	}

	.widget-type-name {
		font-weight: 500;
	}
</style>
