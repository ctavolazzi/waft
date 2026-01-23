/**
 * Realm - Evolutionary environment containing population and divine configuration
 *
 * A realm is a self-contained evolutionary experiment with:
 * - Supreme Being (god/pantheon configuration)
 * - Prime Directive (evolutionary goal)
 * - Population of beings
 * - Environmental components
 * - Historical timeline
 */

import type { Being, BeingStats } from './Being';

export interface SupremeBeing {
	name: string;
	domain: string;              // "Knowledge" | "Chaos" | "Harmony" | "Survival" | etc.
	temperament: string;         // "Benevolent" | "Indifferent" | "Harsh" | "Chaotic"
	interventionRate: number;    // 0.0-1.0: How often god intervenes
	favoredTrait: keyof Being['genome']; // Which genetic trait god favors
}

export interface PrimeDirective {
	goal: string;                // "Maximize cooperation" | "Maximize diversity" | "Survival of fittest"
	description: string;
	fitnessWeights: {            // How to weight fitness calculation
		longevity: number;
		energy: number;
		cooperation: number;
		curiosity: number;
		reproduction: number;
	};
}

export interface Epoch {
	id: string;
	name: string;                // "Primordial Soup" | "Bronze Age" | "Renaissance" | etc.
	startTick: number;
	endTick?: number;
	description: string;
	events: HistoricalEvent[];
}

export interface HistoricalEvent {
	tick: number;
	type: 'birth' | 'death' | 'extinction' | 'mutation' | 'breakthrough' | 'intervention' | 'component_drop';
	description: string;
	beingIds?: string[];
	componentId?: string;
	significance: 'minor' | 'major' | 'critical'; // How important for history
}

export interface RealmConfig {
	name: string;
	description: string;
	initialPopulation: number;   // Starting number of beings
	worldWidth: number;
	worldHeight: number;
	ticksPerEpoch: number;       // How many ticks before epoch change
	supremeBeing: SupremeBeing;
	primeDirective: PrimeDirective;
}

export interface Realm {
	id: string;
	config: RealmConfig;

	// Population
	beings: Being[];
	beingStats: BeingStats;

	// Simulation state
	currentTick: number;
	currentEpoch: Epoch;
	epochs: Epoch[];
	running: boolean;
	tickRate: number;            // Ticks per second

	// Components (dropped by user)
	components: RealmComponent[];

	// History
	events: HistoricalEvent[];
	ancestralLineages: Map<string, string[]>; // beingId -> ancestor chain
}

export interface RealmComponent {
	id: string;
	type: 'resource' | 'challenge' | 'mutation' | 'sanctuary' | 'hazard';
	name: string;
	x: number;
	y: number;
	radius: number;              // Area of effect
	strength: number;            // How strong the effect (0.0-1.0)
	effect: ComponentEffect;
}

export interface ComponentEffect {
	fitnessModifier: number;     // +/- fitness when investigating
	energyModifier: number;      // +/- energy
	mutationChance: number;      // 0.0-1.0: chance to trigger mutation
	deathChance: number;         // 0.0-1.0: chance to kill being
	reproductionBonus: number;   // Increase fertility
}

/**
 * Create a new realm with initial configuration
 */
export function createRealm(config: RealmConfig): Realm {
	const firstEpoch: Epoch = {
		id: 'epoch-0',
		name: 'Primordial Emergence',
		startTick: 0,
		description: 'The first beings emerge into existence, scattered across the realm.',
		events: []
	};

	return {
		id: `realm-${Date.now()}`,
		config,
		beings: [],
		beingStats: {
			totalBirths: config.initialPopulation,
			totalDeaths: 0,
			currentPopulation: config.initialPopulation,
			averageFitness: 0.5,
			averageAge: 0,
			geneticDiversity: 0,
			extinctionEvents: 0
		},
		currentTick: 0,
		currentEpoch: firstEpoch,
		epochs: [firstEpoch],
		running: false,
		tickRate: 10, // 10 ticks per second default
		components: [],
		events: [{
			tick: 0,
			type: 'birth',
			description: `${config.initialPopulation} beings materialize in the realm of ${config.supremeBeing.name}`,
			significance: 'critical'
		}],
		ancestralLineages: new Map()
	};
}

/**
 * Predefined epoch names for different stages of evolution
 */
export const EPOCH_NAMES = [
	{ name: 'Primordial Emergence', description: 'The first beings emerge into existence' },
	{ name: 'Age of Wandering', description: 'Beings explore and discover their world' },
	{ name: 'Dawn of Cooperation', description: 'First swarms form, cooperation emerges' },
	{ name: 'Bronze Adaptation', description: 'Genetic diversity flourishes' },
	{ name: 'Classical Equilibrium', description: 'Population stabilizes, competition balances cooperation' },
	{ name: 'Renaissance of Curiosity', description: 'Investigation and discovery accelerate' },
	{ name: 'Industrial Evolution', description: 'Rapid genetic change and specialization' },
	{ name: 'Modern Complexity', description: 'Complex behaviors and strategies emerge' },
	{ name: 'Quantum Transcendence', description: 'Beings approach theoretical fitness limits' },
	{ name: 'Singularity Horizon', description: 'The realm reaches its final evolutionary form' }
];

/**
 * Predefined supreme beings with different temperaments
 */
export const SUPREME_BEINGS: SupremeBeing[] = [
	{
		name: 'Harmonia',
		domain: 'Harmony',
		temperament: 'Benevolent',
		interventionRate: 0.3,
		favoredTrait: 'cooperation'
	},
	{
		name: 'Kaos',
		domain: 'Chaos',
		temperament: 'Chaotic',
		interventionRate: 0.7,
		favoredTrait: 'adaptability'
	},
	{
		name: 'Logos',
		domain: 'Knowledge',
		temperament: 'Indifferent',
		interventionRate: 0.1,
		favoredTrait: 'curiosity'
	},
	{
		name: 'Vitalis',
		domain: 'Survival',
		temperament: 'Harsh',
		interventionRate: 0.5,
		favoredTrait: 'energy'
	},
	{
		name: 'The Watcher',
		domain: 'Observation',
		temperament: 'Indifferent',
		interventionRate: 0.0,
		favoredTrait: 'perception'
	}
];

/**
 * Predefined prime directives
 */
export const PRIME_DIRECTIVES: Record<string, PrimeDirective> = {
	harmony: {
		goal: 'Maximize Cooperation',
		description: 'Beings that work together shall inherit the realm',
		fitnessWeights: {
			longevity: 0.1,
			energy: 0.2,
			cooperation: 0.5,
			curiosity: 0.1,
			reproduction: 0.1
		}
	},
	survival: {
		goal: 'Survival of the Fittest',
		description: 'Only the strong shall persist through the ages',
		fitnessWeights: {
			longevity: 0.4,
			energy: 0.3,
			cooperation: 0.0,
			curiosity: 0.1,
			reproduction: 0.2
		}
	},
	diversity: {
		goal: 'Maximize Genetic Diversity',
		description: 'Let a thousand variants bloom',
		fitnessWeights: {
			longevity: 0.2,
			energy: 0.2,
			cooperation: 0.2,
			curiosity: 0.2,
			reproduction: 0.2
		}
	},
	curiosity: {
		goal: 'Maximize Exploration',
		description: 'Those who seek shall find truth',
		fitnessWeights: {
			longevity: 0.1,
			energy: 0.2,
			cooperation: 0.2,
			curiosity: 0.4,
			reproduction: 0.1
		}
	}
};

/**
 * Serialize realm to JSON for save/load
 */
export function serializeRealm(realm: Realm): string {
	return JSON.stringify({
		...realm,
		ancestralLineages: Array.from(realm.ancestralLineages.entries())
	}, null, 2);
}

/**
 * Deserialize realm from JSON
 */
export function deserializeRealm(json: string): Realm {
	const data = JSON.parse(json);
	return {
		...data,
		ancestralLineages: new Map(data.ancestralLineages)
	};
}
