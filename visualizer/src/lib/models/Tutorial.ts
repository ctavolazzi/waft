/**
 * Tutorial - Step-by-step guided experience for WAFT Village
 *
 * Teaches:
 * - Building placement
 * - Worker assignment
 * - Resource management
 * - Genetic traits and job matching
 * - Challenge survival
 */

import type { BuildingType, ResourceType } from './Village';

export interface TutorialStep {
	id: string;
	title: string;
	description: string;
	instructions: string[];

	// Conditions to complete step
	completion: {
		buildingsPlaced?: BuildingType[];
		workersAssigned?: number;
		resourcesGathered?: Partial<Record<ResourceType, number>>;
		ticksElapsed?: number;
		beingsAlive?: number;
	};

	// Rewards for completing step
	rewards?: {
		resources?: Partial<Record<ResourceType, number>>;
		message?: string;
	};

	// Hints
	hint?: string;
}

export interface Tutorial {
	id: string;
	name: string;
	description: string;
	steps: TutorialStep[];
	currentStep: number;
	completed: boolean;
	startTick: number;
}

/**
 * Genesis Farm 2025 - Tutorial campaign
 */
export const GENESIS_FARM_TUTORIAL: Tutorial = {
	id: 'genesis-farm',
	name: 'Genesis Farm 2025',
	description: 'Learn to build and manage an evolutionary village. Pre-industrial meets off-grid modern.',
	steps: [
		{
			id: 'welcome',
			title: 'Welcome to Genesis Farm',
			description: 'The year is 2025. You are founding a new off-grid homestead village.',
			instructions: [
				'You are the village planner (god mode)',
				'10 beings have arrived with diverse genetics',
				'Your goal: survive the first winter',
				'Click NEXT to begin'
			],
			completion: { ticksElapsed: 1 },
			hint: 'Press the ▶️ button to start time'
		},

		{
			id: 'build-well',
			title: 'Water is Life',
			description: 'Every village needs fresh water. Build a well to provide it.',
			instructions: [
				'Open the Component Palette (right side)',
				'Find the 💧 Well in the buildings section',
				'Drag it onto the map',
				'Cost: 15 stone, 5 wood'
			],
			completion: { buildingsPlaced: ['well'] },
			rewards: {
				resources: { stone: 10 },
				message: '✓ Well constructed! Water production: +5/tick'
			},
			hint: 'Wells work best with perceptive beings'
		},

		{
			id: 'assign-worker',
			title: 'Put Beings to Work',
			description: 'Beings with high PERCEPTION are best at finding water. Assign one to the well.',
			instructions: [
				'Click on the well you just built',
				'Click "Assign Worker"',
				'Choose a being with high perception (0.7+)',
				'Watch their genetic compatibility score'
			],
			completion: { workersAssigned: 1 },
			rewards: {
				message: '✓ Worker assigned! Production efficiency increased.'
			},
			hint: 'Genetic match affects productivity: high perception = high water output'
		},

		{
			id: 'build-farmhouse',
			title: 'Grow Food',
			description: 'Your beings consume 0.1 food per tick. Build a farmhouse to feed them.',
			instructions: [
				'Drag a 🌾 Farmhouse onto the map',
				'Cost: 20 wood, 10 stone',
				'Wait for construction to complete',
				'Assign 2-3 COOPERATIVE beings as workers'
			],
			completion: { buildingsPlaced: ['farmhouse'], workersAssigned: 3 },
			rewards: {
				resources: { food: 20 },
				message: '✓ Farm operational! Food production: +2/tick per worker'
			},
			hint: 'Cooperation trait makes better farmers (teamwork!)'
		},

		{
			id: 'build-home',
			title: 'Shelter Your People',
			description: 'Beings need homes to thrive and reproduce.',
			instructions: [
				'Build 2x 🏠 Homes',
				'Cost: 10 wood, 5 stone each',
				'Homes increase happiness',
				'Happy beings reproduce more'
			],
			completion: { buildingsPlaced: ['home', 'home'] },
			rewards: {
				message: '✓ Homes built! Reproduction rate +50%'
			},
			hint: 'More homes = more babies = genetic diversity'
		},

		{
			id: 'gather-resources',
			title: 'Stockpile for Winter',
			description: 'Winter is coming in 500 ticks. You need 200 food to survive.',
			instructions: [
				'Build more farms if needed',
				'Assign high-cooperation beings to farms',
				'Watch your food stockpile grow',
				'Target: 200 food'
			],
			completion: { resourcesGathered: { food: 200 } },
			rewards: {
				resources: { wood: 30, stone: 20 },
				message: '✓ Winter stockpile complete! Your village is prepared.'
			},
			hint: 'High cooperation (0.8+) beings produce 60% more food'
		},

		{
			id: 'build-workshop',
			title: 'Innovate with a Workshop',
			description: 'Modern off-grid requires tools. Build a workshop for repairs.',
			instructions: [
				'Build a 🔨 Workshop',
				'Cost: 25 wood, 15 stone',
				'Assign a CURIOUS being',
				'Curious beings innovate faster'
			],
			completion: { buildingsPlaced: ['workshop'], workersAssigned: 5 },
			rewards: {
				resources: { metal: 10 },
				message: '✓ Workshop online! Metal production: +1/tick'
			},
			hint: 'Curiosity trait unlocks innovation'
		},

		{
			id: 'build-solar',
			title: 'Welcome to 2025: Solar Power',
			description: 'This is off-grid living! Build a solar array for clean energy.',
			instructions: [
				'Build a ☀️ Solar Array',
				'Cost: 20 metal, 10 stone',
				'Assign a curious maintainer',
				'Energy powers advanced buildings'
			],
			completion: { buildingsPlaced: ['solar_array'] },
			rewards: {
				resources: { energy: 20 },
				message: '✓ Solar online! Energy production: +3/tick'
			},
			hint: 'Solar is modern tech - only curious beings can maintain it'
		},

		{
			id: 'final-challenge',
			title: 'THE DROUGHT',
			description: 'DISASTER! A drought has struck. Your well production drops 75%!',
			instructions: [
				'Build a 2nd well immediately',
				'Reassign workers if needed',
				'Survive for 100 ticks',
				'Don\'t let water hit 0 or beings die'
			],
			completion: { ticksElapsed: 100, beingsAlive: 5 },
			rewards: {
				message: '🎉 VICTORY! You survived the drought. The village lives on!'
			},
			hint: 'LESSON: Always diversify critical resources. Single points of failure = death.'
		},

		{
			id: 'tutorial-complete',
			title: 'Tutorial Complete!',
			description: 'You\'ve learned the fundamentals of evolutionary village building.',
			instructions: [
				'You can continue playing this village',
				'Or unlock SANDBOX MODE for unlimited experimentation',
				'In sandbox: no limits, no challenges, pure creativity',
				'Your choice!'
			],
			completion: {},
			rewards: {
				message: '🌟 Sandbox Mode Unlocked!'
			}
		}
	],
	currentStep: 0,
	completed: false,
	startTick: 0
};

/**
 * Check if current step is complete
 */
export function checkStepCompletion(
	tutorial: Tutorial,
	village: any,
	beings: any[],
	currentTick: number
): boolean {
	const step = tutorial.steps[tutorial.currentStep];
	if (!step) return false;

	const { completion } = step;

	// Check buildings placed
	if (completion.buildingsPlaced) {
		const placedTypes = village.buildings.map((b: any) => b.template.type);

		// Count occurrences of each building type required
		const requiredCounts: Record<string, number> = {};
		for (const required of completion.buildingsPlaced) {
			requiredCounts[required] = (requiredCounts[required] || 0) + 1;
		}

		// Count occurrences of each building type placed
		const placedCounts: Record<string, number> = {};
		for (const type of placedTypes) {
			placedCounts[type] = (placedCounts[type] || 0) + 1;
		}

		// Check if we have enough of each required type
		for (const [type, count] of Object.entries(requiredCounts)) {
			if ((placedCounts[type] || 0) < count) {
				return false;
			}
		}
	}

	// Check workers assigned
	if (completion.workersAssigned !== undefined) {
		if (village.jobs.length < completion.workersAssigned) {
			return false;
		}
	}

	// Check resources gathered
	if (completion.resourcesGathered) {
		for (const [resource, amount] of Object.entries(completion.resourcesGathered)) {
			if (village.resources[resource].amount < amount) {
				return false;
			}
		}
	}

	// Check ticks elapsed
	if (completion.ticksElapsed !== undefined) {
		const elapsed = currentTick - tutorial.startTick;
		if (elapsed < completion.ticksElapsed) {
			return false;
		}
	}

	// Check beings alive
	if (completion.beingsAlive !== undefined) {
		const alive = beings.filter((b: any) => b.alive).length;
		if (alive < completion.beingsAlive) {
			return false;
		}
	}

	return true;
}

/**
 * Advance to next tutorial step
 */
export function advanceTutorialStep(tutorial: Tutorial): boolean {
	if (tutorial.currentStep < tutorial.steps.length - 1) {
		tutorial.currentStep++;
		return true;
	} else {
		tutorial.completed = true;
		return false;
	}
}

/**
 * Apply step rewards
 */
export function applyStepRewards(tutorial: Tutorial, village: any) {
	const step = tutorial.steps[tutorial.currentStep];
	if (!step.rewards) return;

	// Add resource rewards
	if (step.rewards.resources) {
		for (const [resource, amount] of Object.entries(step.rewards.resources)) {
			village.resources[resource].amount += amount;
		}
	}
}

/**
 * Trigger drought challenge (step 8)
 */
export function triggerDrought(village: any) {
	// Reduce all well production by 75%
	for (const building of village.buildings) {
		if (building.template.type === 'well') {
			building.efficiency *= 0.25;
		}
	}
}
