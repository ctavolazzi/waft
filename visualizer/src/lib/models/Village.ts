/**
 * Village - Infrastructure and resource management for evolutionary city builder
 *
 * Buildings create evolutionary pressure - beings with matching genetics thrive
 * Resources flow through production chains
 * Challenges test adaptation and planning
 */

import type { Being } from './Being';

export type ResourceType = 'food' | 'water' | 'wood' | 'stone' | 'energy' | 'metal';

export interface Resource {
	type: ResourceType;
	amount: number;
	capacity: number;
	productionRate: number;  // Per tick
	consumptionRate: number; // Per tick
}

export type BuildingType =
	| 'farmhouse'    // Produces food (needs cooperation)
	| 'well'         // Produces water (needs perception to find)
	| 'workshop'     // Produces tools (needs curiosity to innovate)
	| 'lumber_mill'  // Produces wood (needs energy for hard work)
	| 'quarry'       // Produces stone (needs energy)
	| 'solar_array'  // Produces energy (needs curiosity to maintain)
	| 'home'         // Houses beings, no production
	| 'watchtower'   // Defense, needs perception
	| 'storage';     // Stores resources

export interface BuildingTemplate {
	type: BuildingType;
	name: string;
	icon: string;
	description: string;
	width: number;
	height: number;

	// Construction costs
	buildCosts: Partial<Record<ResourceType, number>>;
	buildTime: number; // Ticks to construct

	// Production
	produces?: ResourceType;
	productionRate: number; // Base rate before worker bonuses

	// Worker requirements
	maxWorkers: number;
	requiredTrait: keyof Being['genome']; // Which genetic trait benefits this building

	// Consumption
	consumes?: Partial<Record<ResourceType, number>>; // Per tick
}

export interface Building {
	id: string;
	template: BuildingTemplate;
	x: number;
	y: number;

	// Construction state
	constructionProgress: number; // 0.0 - 1.0
	operational: boolean;

	// Workers
	assignedWorkers: string[]; // Being IDs
	efficiency: number; // 0.0 - 1.0 based on worker genetics

	// Production
	currentProduction: number; // Accumulated production this tick
	lastTickProduction: number;
}

export interface Job {
	buildingId: string;
	beingId: string;
	startTick: number;
	productivity: number; // 0.0 - 1.0 based on genetic match
}

export interface Village {
	name: string;
	buildings: Building[];
	resources: Record<ResourceType, Resource>;
	jobs: Job[];

	// Stats
	totalPopulation: number;
	employedPopulation: number;
	unemployedPopulation: number;
	totalProduction: Partial<Record<ResourceType, number>>;
	totalConsumption: Partial<Record<ResourceType, number>>;
}

/**
 * Building templates - pre-industrial + modern off-grid
 */
export const BUILDING_TEMPLATES: Record<BuildingType, BuildingTemplate> = {
	farmhouse: {
		type: 'farmhouse',
		name: 'Farmhouse',
		icon: '🌾',
		description: 'Grows food. Works best with cooperative beings.',
		width: 80,
		height: 80,
		buildCosts: { wood: 20, stone: 10 },
		buildTime: 100,
		produces: 'food',
		productionRate: 2.0,
		maxWorkers: 3,
		requiredTrait: 'cooperation',
		consumes: { water: 0.5 }
	},

	well: {
		type: 'well',
		name: 'Well',
		icon: '💧',
		description: 'Provides water. Perceptive beings find water faster.',
		width: 40,
		height: 40,
		buildCosts: { stone: 15, wood: 5 },
		buildTime: 80,
		produces: 'water',
		productionRate: 5.0,
		maxWorkers: 1,
		requiredTrait: 'perception',
		consumes: {}
	},

	workshop: {
		type: 'workshop',
		name: 'Workshop',
		icon: '🔨',
		description: 'Crafts tools and repairs. Curious beings innovate better.',
		width: 60,
		height: 60,
		buildCosts: { wood: 25, stone: 15 },
		buildTime: 120,
		produces: 'metal',
		productionRate: 1.0,
		maxWorkers: 2,
		requiredTrait: 'curiosity',
		consumes: { energy: 0.3 }
	},

	lumber_mill: {
		type: 'lumber_mill',
		name: 'Lumber Mill',
		icon: '🪓',
		description: 'Harvests wood. Energetic beings work harder.',
		width: 70,
		height: 70,
		buildCosts: { stone: 10 },
		buildTime: 90,
		produces: 'wood',
		productionRate: 1.5,
		maxWorkers: 2,
		requiredTrait: 'energy',
		consumes: { food: 0.3 }
	},

	quarry: {
		type: 'quarry',
		name: 'Quarry',
		icon: '⛏️',
		description: 'Mines stone. Hard work requires high energy.',
		width: 80,
		height: 80,
		buildCosts: { wood: 15 },
		buildTime: 100,
		produces: 'stone',
		productionRate: 1.0,
		maxWorkers: 3,
		requiredTrait: 'energy',
		consumes: { food: 0.4 }
	},

	solar_array: {
		type: 'solar_array',
		name: 'Solar Array',
		icon: '☀️',
		description: 'Modern tech! Generates energy. Needs curious maintainers.',
		width: 100,
		height: 60,
		buildCosts: { metal: 20, stone: 10 },
		buildTime: 150,
		produces: 'energy',
		productionRate: 3.0,
		maxWorkers: 1,
		requiredTrait: 'curiosity',
		consumes: {}
	},

	home: {
		type: 'home',
		name: 'Home',
		icon: '🏠',
		description: 'Houses beings. Increases happiness and reproduction.',
		width: 50,
		height: 50,
		buildCosts: { wood: 10, stone: 5 },
		buildTime: 60,
		productionRate: 0,
		maxWorkers: 0,
		requiredTrait: 'cooperation',
		consumes: {}
	},

	watchtower: {
		type: 'watchtower',
		name: 'Watchtower',
		icon: '🗼',
		description: 'Defense structure. Perceptive guards spot threats.',
		width: 40,
		height: 60,
		buildCosts: { wood: 20, stone: 20 },
		buildTime: 120,
		productionRate: 0,
		maxWorkers: 2,
		requiredTrait: 'perception',
		consumes: { food: 0.2 }
	},

	storage: {
		type: 'storage',
		name: 'Storage',
		icon: '📦',
		description: 'Increases resource capacity.',
		width: 60,
		height: 60,
		buildCosts: { wood: 15 },
		buildTime: 50,
		productionRate: 0,
		maxWorkers: 0,
		requiredTrait: 'cooperation',
		consumes: {}
	}
};

/**
 * Create a new village with starting resources
 */
export function createVillage(name: string): Village {
	return {
		name,
		buildings: [],
		resources: {
			food: { type: 'food', amount: 50, capacity: 100, productionRate: 0, consumptionRate: 0 },
			water: { type: 'water', amount: 50, capacity: 100, productionRate: 0, consumptionRate: 0 },
			wood: { type: 'wood', amount: 30, capacity: 100, productionRate: 0, consumptionRate: 0 },
			stone: { type: 'stone', amount: 20, capacity: 100, productionRate: 0, consumptionRate: 0 },
			energy: { type: 'energy', amount: 10, capacity: 50, productionRate: 0, consumptionRate: 0 },
			metal: { type: 'metal', amount: 0, capacity: 50, productionRate: 0, consumptionRate: 0 }
		},
		jobs: [],
		totalPopulation: 0,
		employedPopulation: 0,
		unemployedPopulation: 0,
		totalProduction: {},
		totalConsumption: {}
	};
}

/**
 * Place a building in the village
 */
export function placeBuilding(
	village: Village,
	template: BuildingTemplate,
	x: number,
	y: number
): Building | null {
	// Check if we can afford it
	for (const [resource, cost] of Object.entries(template.buildCosts)) {
		const resourceType = resource as ResourceType;
		if (village.resources[resourceType].amount < cost) {
			return null; // Can't afford
		}
	}

	// Deduct costs
	for (const [resource, cost] of Object.entries(template.buildCosts)) {
		const resourceType = resource as ResourceType;
		village.resources[resourceType].amount -= cost;
	}

	// Create building
	const building: Building = {
		id: `building-${Date.now()}-${Math.random()}`,
		template,
		x,
		y,
		constructionProgress: 0,
		operational: false,
		assignedWorkers: [],
		efficiency: 0,
		currentProduction: 0,
		lastTickProduction: 0
	};

	village.buildings.push(building);
	return building;
}

/**
 * Assign being to work at building
 * Returns productivity score (0.0 - 1.0) based on genetic match
 */
export function assignWorker(
	village: Village,
	building: Building,
	being: Being
): number {
	// Check if building has space
	if (building.assignedWorkers.length >= building.template.maxWorkers) {
		return 0;
	}

	// Check if being is already employed
	const alreadyEmployed = village.jobs.find(j => j.beingId === being.id);
	if (alreadyEmployed) {
		return 0;
	}

	// Calculate productivity based on genetic match
	const requiredTrait = building.template.requiredTrait;
	const traitValue = being.genome[requiredTrait];
	const productivity = traitValue; // 0.0 - 1.0

	// Assign job
	building.assignedWorkers.push(being.id);
	village.jobs.push({
		buildingId: building.id,
		beingId: being.id,
		startTick: 0,
		productivity
	});

	// Update building efficiency (average of all workers)
	updateBuildingEfficiency(building, village.jobs);

	return productivity;
}

/**
 * Update building efficiency based on workers
 */
export function updateBuildingEfficiency(building: Building, jobs: Job[]) {
	const buildingJobs = jobs.filter(j => j.buildingId === building.id);

	if (buildingJobs.length === 0) {
		building.efficiency = 0;
		return;
	}

	const avgProductivity = buildingJobs.reduce((sum, j) => sum + j.productivity, 0) / buildingJobs.length;
	building.efficiency = avgProductivity;
}

/**
 * Process village production for one tick
 */
export function tickVillageProduction(village: Village, beings: Being[]) {
	// Update construction progress
	for (const building of village.buildings) {
		if (!building.operational && building.constructionProgress < 1) {
			building.constructionProgress += 1 / building.template.buildTime;
			if (building.constructionProgress >= 1) {
				building.constructionProgress = 1;
				building.operational = true;
			}
		}
	}

	// Reset production/consumption
	village.totalProduction = {};
	village.totalConsumption = {};

	// Process operational buildings
	for (const building of village.buildings) {
		if (!building.operational) continue;

		// Consume resources
		if (building.template.consumes) {
			for (const [resource, rate] of Object.entries(building.template.consumes)) {
				const resourceType = resource as ResourceType;
				const consumed = rate * building.efficiency;

				if (village.resources[resourceType].amount >= consumed) {
					village.resources[resourceType].amount -= consumed;
					village.totalConsumption[resourceType] = (village.totalConsumption[resourceType] || 0) + consumed;
				} else {
					// Not enough resources - building stops
					building.efficiency = 0;
				}
			}
		}

		// Produce resources (if building has workers)
		if (building.template.produces && building.efficiency > 0) {
			const produced = building.template.productionRate * building.efficiency;
			const resourceType = building.template.produces;

			const newAmount = Math.min(
				village.resources[resourceType].amount + produced,
				village.resources[resourceType].capacity
			);

			building.lastTickProduction = newAmount - village.resources[resourceType].amount;
			village.resources[resourceType].amount = newAmount;
			village.totalProduction[resourceType] = (village.totalProduction[resourceType] || 0) + building.lastTickProduction;
		}
	}

	// Consume food for population (0.1 food per being per tick)
	const aliveBings = beings.filter(b => b.alive);
	const foodConsumption = aliveBings.length * 0.1;
	village.resources.food.amount = Math.max(0, village.resources.food.amount - foodConsumption);
	village.totalConsumption.food = (village.totalConsumption.food || 0) + foodConsumption;

	// Update population stats
	village.totalPopulation = aliveBings.length;
	village.employedPopulation = village.jobs.length;
	village.unemployedPopulation = village.totalPopulation - village.employedPopulation;

	// Increase storage capacity with storage buildings
	const storageCount = village.buildings.filter(b => b.template.type === 'storage' && b.operational).length;
	for (const resource of Object.values(village.resources)) {
		resource.capacity = 100 + (storageCount * 50);
	}
}

/**
 * Check win/loss conditions
 */
export function checkVillageConditions(village: Village, beings: Being[]): {
	victory: boolean;
	defeat: boolean;
	message: string;
} {
	const aliveBings = beings.filter(b => b.alive);

	// Defeat: everyone died
	if (aliveBings.length === 0) {
		return {
			victory: false,
			defeat: true,
			message: 'All beings perished. The village is lost.'
		};
	}

	// Defeat: starvation (no food and no way to produce it)
	const hasFarm = village.buildings.some(b => b.template.type === 'farmhouse' && b.operational);
	if (village.resources.food.amount < 1 && !hasFarm) {
		return {
			victory: false,
			defeat: true,
			message: 'The village starved without food production.'
		};
	}

	return {
		victory: false,
		defeat: false,
		message: ''
	};
}
