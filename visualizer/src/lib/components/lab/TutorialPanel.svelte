<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import type { Tutorial, TutorialStep } from '$lib/models/Tutorial';
	import { checkStepCompletion, advanceTutorialStep, applyStepRewards } from '$lib/models/Tutorial';

	export let tutorial: Tutorial | null = null;
	export let village: any = null;
	export let beings: any[] = [];
	export let currentTick: number = 0;

	const dispatch = createEventDispatcher();

	let collapsed = false;
	let showHint = false;

	$: currentStep = tutorial ? tutorial.steps[tutorial.currentStep] : null;
	$: stepComplete = tutorial && village ? checkStepCompletion(tutorial, village, beings, currentTick) : false;
	$: progress = tutorial ? ((tutorial.currentStep + 1) / tutorial.steps.length) * 100 : 0;

	function handleNext() {
		if (!tutorial || !village) return;

		if (stepComplete) {
			// Apply rewards
			applyStepRewards(tutorial, village);

			// Show reward message
			if (currentStep?.rewards?.message) {
				dispatch('message', { text: currentStep.rewards.message });
			}

			// Advance to next step
			const hasNext = advanceTutorialStep(tutorial);

			if (!hasNext) {
				// Tutorial complete!
				dispatch('complete');
			} else {
				// Trigger special events
				const newStep = tutorial.steps[tutorial.currentStep];
				if (newStep.id === 'final-challenge') {
					dispatch('trigger-drought');
				}
			}

			tutorial = tutorial; // Trigger reactivity
		}
	}

	function handleSkipTutorial() {
		if (confirm('Are you sure you want to skip the tutorial? You can restart anytime.')) {
			dispatch('skip');
		}
	}

	function handleSandbox() {
		dispatch('sandbox');
	}
</script>

{#if tutorial && !tutorial.completed}
	<div class="tutorial-panel" class:collapsed>
		<div class="panel-header" on:click={() => collapsed = !collapsed}>
			<span class="panel-title">📖 TUTORIAL</span>
			<div class="progress-bar">
				<div class="progress-fill" style="width: {progress}%"></div>
				<span class="progress-text">{tutorial.currentStep + 1}/{tutorial.steps.length}</span>
			</div>
			<button class="collapse-btn">{collapsed ? '▲' : '▼'}</button>
		</div>

		{#if !collapsed && currentStep}
			<div class="panel-body">
				<!-- Step info -->
				<div class="step-header">
					<h3 class="step-title">{currentStep.title}</h3>
					<p class="step-description">{currentStep.description}</p>
				</div>

				<!-- Instructions -->
				<div class="instructions">
					<div class="instructions-header">📋 Instructions:</div>
					<ul class="instructions-list">
						{#each currentStep.instructions as instruction}
							<li>{instruction}</li>
						{/each}
					</ul>
				</div>

				<!-- Completion status -->
				{#if currentStep.completion}
					<div class="completion-status">
						<div class="status-header">📊 Progress:</div>

						{#if currentStep.completion.buildingsPlaced}
							<div class="status-item">
								<span class="status-label">Buildings:</span>
								<span class="status-value">
									{village?.buildings.filter(b => currentStep.completion.buildingsPlaced?.includes(b.template.type)).length || 0}/{currentStep.completion.buildingsPlaced.length}
								</span>
							</div>
						{/if}

						{#if currentStep.completion.workersAssigned !== undefined}
							<div class="status-item">
								<span class="status-label">Workers:</span>
								<span class="status-value">
									{village?.jobs.length || 0}/{currentStep.completion.workersAssigned}
								</span>
							</div>
						{/if}

						{#if currentStep.completion.resourcesGathered}
							{#each Object.entries(currentStep.completion.resourcesGathered) as [resource, target]}
								<div class="status-item">
									<span class="status-label">{resource}:</span>
									<span class="status-value" class:complete={village?.resources[resource]?.amount >= target}>
										{village?.resources[resource]?.amount.toFixed(0) || 0}/{target}
									</span>
								</div>
							{/each}
						{/if}

						{#if currentStep.completion.ticksElapsed !== undefined}
							<div class="status-item">
								<span class="status-label">Ticks:</span>
								<span class="status-value">
									{currentTick - tutorial.startTick}/{currentStep.completion.ticksElapsed}
								</span>
							</div>
						{/if}

						{#if currentStep.completion.beingsAlive !== undefined}
							<div class="status-item">
								<span class="status-label">Beings Alive:</span>
								<span class="status-value" class:complete={beings.filter(b => b.alive).length >= currentStep.completion.beingsAlive}>
									{beings.filter(b => b.alive).length}/{currentStep.completion.beingsAlive}
								</span>
							</div>
						{/if}
					</div>
				{/if}

				<!-- Hint -->
				{#if currentStep.hint}
					<div class="hint-section">
						<button class="hint-btn" on:click={() => showHint = !showHint}>
							💡 {showHint ? 'Hide' : 'Show'} Hint
						</button>
						{#if showHint}
							<div class="hint-text">{currentStep.hint}</div>
						{/if}
					</div>
				{/if}

				<!-- Actions -->
				<div class="actions">
					{#if stepComplete}
						<button class="next-btn" on:click={handleNext}>
							{tutorial.currentStep === tutorial.steps.length - 1 ? '🎉 Finish Tutorial' : '➡️ Next Step'}
						</button>
					{:else}
						<button class="waiting-btn" disabled>
							⏳ Complete objectives to continue
						</button>
					{/if}

					<button class="skip-btn" on:click={handleSkipTutorial}>
						Skip Tutorial
					</button>
				</div>
			</div>
		{/if}
	</div>
{:else if tutorial?.completed}
	<!-- Tutorial complete - show sandbox unlock -->
	<div class="completion-panel">
		<div class="completion-header">
			<h2>🎉 Tutorial Complete!</h2>
			<p>You've mastered the basics of evolutionary village building.</p>
		</div>

		<div class="completion-options">
			<button class="continue-btn" on:click={() => dispatch('continue')}>
				🌾 Continue This Village
			</button>
			<button class="sandbox-btn" on:click={handleSandbox}>
				🎨 Enter Sandbox Mode
			</button>
		</div>
	</div>
{/if}

<style>
	.tutorial-panel {
		position: absolute;
		top: 80px;
		right: 320px;
		width: 400px;
		background: rgba(20, 20, 30, 0.98);
		border: 2px solid #0f3;
		border-radius: 8px;
		backdrop-filter: blur(10px);
		box-shadow: 0 0 30px rgba(0, 255, 51, 0.4);
		z-index: 150;
		font-family: 'Courier New', monospace;
	}

	.tutorial-panel.collapsed {
		width: 250px;
	}

	.panel-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 12px 16px;
		background: rgba(0, 255, 51, 0.15);
		border-bottom: 1px solid #0f3;
		cursor: pointer;
		gap: 12px;
	}

	.panel-title {
		font-size: 0.9rem;
		font-weight: 600;
		color: #0f3;
		letter-spacing: 1px;
		white-space: nowrap;
	}

	.progress-bar {
		position: relative;
		flex: 1;
		height: 20px;
		background: rgba(0, 0, 0, 0.3);
		border: 1px solid #0f3;
		border-radius: 10px;
		overflow: hidden;
	}

	.progress-fill {
		position: absolute;
		left: 0;
		top: 0;
		height: 100%;
		background: linear-gradient(90deg, #0f3 0%, #0af 100%);
		transition: width 0.5s ease;
	}

	.progress-text {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		font-size: 0.7rem;
		font-weight: 600;
		color: #fff;
		text-shadow: 0 0 4px #000;
	}

	.collapse-btn {
		background: none;
		border: 1px solid #0f3;
		color: #0f3;
		padding: 4px 8px;
		border-radius: 4px;
		cursor: pointer;
		font-size: 0.8rem;
	}

	.panel-body {
		padding: 16px;
		max-height: calc(100vh - 200px);
		overflow-y: auto;
	}

	.panel-body::-webkit-scrollbar {
		width: 6px;
	}

	.panel-body::-webkit-scrollbar-track {
		background: rgba(0, 0, 0, 0.2);
	}

	.panel-body::-webkit-scrollbar-thumb {
		background: #0f3;
		border-radius: 3px;
	}

	.step-header {
		margin-bottom: 16px;
	}

	.step-title {
		font-size: 1.1rem;
		color: #0f3;
		margin: 0 0 8px 0;
		font-weight: 600;
	}

	.step-description {
		font-size: 0.85rem;
		color: #e0e0e0;
		margin: 0;
		line-height: 1.4;
	}

	.instructions {
		background: rgba(0, 255, 51, 0.05);
		border: 1px solid #0f3;
		border-radius: 6px;
		padding: 12px;
		margin-bottom: 16px;
	}

	.instructions-header {
		font-size: 0.8rem;
		color: #0f3;
		font-weight: 600;
		margin-bottom: 8px;
	}

	.instructions-list {
		margin: 0;
		padding-left: 20px;
		font-size: 0.8rem;
		color: #e0e0e0;
		line-height: 1.6;
	}

	.completion-status {
		background: rgba(0, 170, 255, 0.05);
		border: 1px solid #0af;
		border-radius: 6px;
		padding: 12px;
		margin-bottom: 16px;
	}

	.status-header {
		font-size: 0.8rem;
		color: #0af;
		font-weight: 600;
		margin-bottom: 8px;
	}

	.status-item {
		display: flex;
		justify-content: space-between;
		font-size: 0.8rem;
		margin: 4px 0;
		padding: 4px 0;
		border-bottom: 1px solid rgba(0, 170, 255, 0.1);
	}

	.status-label {
		color: #999;
	}

	.status-value {
		color: #f90;
		font-weight: 600;
	}

	.status-value.complete {
		color: #0f3;
	}

	.hint-section {
		margin-bottom: 16px;
	}

	.hint-btn {
		width: 100%;
		padding: 8px;
		background: rgba(255, 187, 0, 0.1);
		border: 1px solid #fb3;
		border-radius: 4px;
		color: #fb3;
		font-family: 'Courier New', monospace;
		font-size: 0.8rem;
		cursor: pointer;
	}

	.hint-btn:hover {
		background: rgba(255, 187, 0, 0.2);
	}

	.hint-text {
		margin-top: 8px;
		padding: 10px;
		background: rgba(255, 187, 0, 0.05);
		border-left: 3px solid #fb3;
		font-size: 0.75rem;
		color: #fb3;
		line-height: 1.5;
	}

	.actions {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.next-btn, .waiting-btn, .skip-btn {
		padding: 12px;
		border-radius: 6px;
		font-family: 'Courier New', monospace;
		font-size: 0.9rem;
		font-weight: 600;
		cursor: pointer;
	}

	.next-btn {
		background: linear-gradient(135deg, #0f3 0%, #0af 100%);
		border: none;
		color: #fff;
	}

	.next-btn:hover {
		box-shadow: 0 0 20px rgba(0, 255, 51, 0.5);
	}

	.waiting-btn {
		background: rgba(100, 100, 100, 0.2);
		border: 1px solid #666;
		color: #999;
		cursor: not-allowed;
	}

	.skip-btn {
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid #666;
		color: #999;
		font-size: 0.75rem;
	}

	.skip-btn:hover {
		background: rgba(255, 255, 255, 0.1);
		border-color: #999;
	}

	.completion-panel {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: 500px;
		background: rgba(20, 20, 30, 0.98);
		border: 3px solid #0f3;
		border-radius: 12px;
		padding: 32px;
		box-shadow: 0 0 50px rgba(0, 255, 51, 0.6);
		z-index: 200;
		font-family: 'Courier New', monospace;
		text-align: center;
	}

	.completion-header h2 {
		font-size: 1.8rem;
		color: #0f3;
		margin: 0 0 16px 0;
	}

	.completion-header p {
		font-size: 1rem;
		color: #e0e0e0;
		margin: 0 0 32px 0;
	}

	.completion-options {
		display: flex;
		gap: 16px;
	}

	.continue-btn, .sandbox-btn {
		flex: 1;
		padding: 16px;
		border-radius: 8px;
		font-family: 'Courier New', monospace;
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
		border: none;
		color: #fff;
	}

	.continue-btn {
		background: linear-gradient(135deg, #0f3 0%, #0af 100%);
	}

	.continue-btn:hover {
		box-shadow: 0 0 30px rgba(0, 255, 51, 0.6);
	}

	.sandbox-btn {
		background: linear-gradient(135deg, #f0f 0%, #90f 100%);
	}

	.sandbox-btn:hover {
		box-shadow: 0 0 30px rgba(255, 0, 255, 0.6);
	}
</style>
