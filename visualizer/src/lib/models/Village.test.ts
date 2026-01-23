import { describe, it, expect, beforeEach } from 'vitest';
import {
	createVillage,
	placeBuilding,
	assignWorker,
	tickVillageProduction,
	checkVillageConditions,
	BUILDING_TEMPLATES,
	type Village
} from './Village';
import { createBeing } from './Being';

describe('Village', () => {
	let village: Village;

	beforeEach(() => {
		village = createVillage('Test Village');
	});

	describe('createVillage', () => {
		it('creates a village with starting resources', () => {
			expect(village.name).toBe('Test Village');
			expect(village.resources.food.amount).toBe(50);
			expect(village.resources.water.amount).toBe(50);
			expect(village.resources.wood.amount).toBe(30);
			expect(village.resources.stone.amount).toBe(20);
		});

		it('starts with no buildings or jobs', () => {
			expect(village.buildings).toHaveLength(0);
			expect(village.jobs).toHaveLength(0);
		});
	});

	describe('placeBuilding', () => {
		it('places a building when resources are sufficient', () => {
			const wellTemplate = BUILDING_TEMPLATES.well;
			const building = placeBuilding(village, wellTemplate, 100, 100);

			expect(building).toBeDefined();
			expect(building?.template.type).toBe('well');
			expect(building?.x).toBe(100);
			expect(building?.y).toBe(100);
		});

		it('deducts costs from village resources', () => {
			const wellTemplate = BUILDING_TEMPLATES.well;
			const initialStone = village.resources.stone.amount;
			const initialWood = village.resources.wood.amount;

			placeBuilding(village, wellTemplate, 100, 100);

			expect(village.resources.stone.amount).toBe(initialStone - 15);
			expect(village.resources.wood.amount).toBe(initialWood - 5);
		});

		it('returns null when resources are insufficient', () => {
			// Drain resources
			village.resources.wood.amount = 0;
			village.resources.stone.amount = 0;

			const wellTemplate = BUILDING_TEMPLATES.well;
			const building = placeBuilding(village, wellTemplate, 100, 100);

			expect(building).toBeNull();
		});

		it('starts building under construction', () => {
			const wellTemplate = BUILDING_TEMPLATES.well;
			const building = placeBuilding(village, wellTemplate, 100, 100);

			expect(building?.operational).toBe(false);
			expect(building?.constructionProgress).toBe(0);
		});
	});

	describe('assignWorker', () => {
		it('assigns being to building', () => {
			const farmTemplate = BUILDING_TEMPLATES.farmhouse;
			const building = placeBuilding(village, farmTemplate, 100, 100)!;
			building.operational = true; // Make it operational

			const being = createBeing('worker-1', 0, 0, 0);
			being.genome.cooperation = 0.9; // High cooperation for farm

			const productivity = assignWorker(village, building, being);

			expect(productivity).toBeCloseTo(0.9, 1);
			expect(building.assignedWorkers).toContain('worker-1');
			expect(village.jobs).toHaveLength(1);
		});

		it('returns 0 when building is full', () => {
			const wellTemplate = BUILDING_TEMPLATES.well;
			const building = placeBuilding(village, wellTemplate, 100, 100)!;
			building.operational = true;

			// Well only has 1 worker slot
			const being1 = createBeing('worker-1', 0, 0, 0);
			const being2 = createBeing('worker-2', 0, 0, 0);

			assignWorker(village, building, being1);
			const productivity = assignWorker(village, building, being2);

			expect(productivity).toBe(0);
			expect(building.assignedWorkers).toHaveLength(1);
		});

		it('returns 0 when being is already employed', () => {
			// Add enough resources for two farms (each costs 20 wood + 10 stone)
			village.resources.wood.amount = 100;
			village.resources.stone.amount = 100;

			const farm1 = placeBuilding(village, BUILDING_TEMPLATES.farmhouse, 100, 100)!;
			const farm2 = placeBuilding(village, BUILDING_TEMPLATES.farmhouse, 200, 200)!;
			farm1.operational = true;
			farm2.operational = true;

			const being = createBeing('worker-1', 0, 0, 0);

			assignWorker(village, farm1, being);
			const productivity = assignWorker(village, farm2, being);

			expect(productivity).toBe(0);
		});
	});

	describe('tickVillageProduction', () => {
		it('advances construction progress', () => {
			const wellTemplate = BUILDING_TEMPLATES.well;
			const building = placeBuilding(village, wellTemplate, 100, 100)!;

			const initialProgress = building.constructionProgress;

			tickVillageProduction(village, []);

			expect(building.constructionProgress).toBeGreaterThan(initialProgress);
		});

		it('makes building operational when construction completes', () => {
			const wellTemplate = BUILDING_TEMPLATES.well;
			const building = placeBuilding(village, wellTemplate, 100, 100)!;

			// Advance to completion (buildTime is in ticks)
			for (let i = 0; i <= wellTemplate.buildTime; i++) {
				tickVillageProduction(village, []);
			}

			expect(building.operational).toBe(true);
			expect(building.constructionProgress).toBeGreaterThanOrEqual(1);
		});

		it('produces resources when building is operational with workers', () => {
			const wellTemplate = BUILDING_TEMPLATES.well;
			const building = placeBuilding(village, wellTemplate, 100, 100)!;
			building.operational = true;

			const being = createBeing('worker-1', 0, 0, 0);
			being.genome.perception = 0.8; // High perception for well

			assignWorker(village, building, being);

			const initialWater = village.resources.water.amount;

			tickVillageProduction(village, [being]);

			expect(village.resources.water.amount).toBeGreaterThan(initialWater);
		});

		it('consumes food for population', () => {
			const beings = [
				createBeing('b1', 0, 0, 0),
				createBeing('b2', 0, 0, 0),
				createBeing('b3', 0, 0, 0)
			];

			const initialFood = village.resources.food.amount;

			tickVillageProduction(village, beings);

			expect(village.resources.food.amount).toBeLessThan(initialFood);
		});

		it('increases storage capacity with storage buildings', () => {
			const storageTemplate = BUILDING_TEMPLATES.storage;
			const storage = placeBuilding(village, storageTemplate, 100, 100)!;
			storage.operational = true;

			const initialCapacity = village.resources.food.capacity;

			tickVillageProduction(village, []);

			expect(village.resources.food.capacity).toBeGreaterThan(initialCapacity);
		});
	});

	describe('checkVillageConditions', () => {
		it('returns defeat when all beings die', () => {
			const beings = [
				createBeing('b1', 0, 0, 0),
				createBeing('b2', 0, 0, 0)
			];

			beings.forEach(b => (b.alive = false));

			const result = checkVillageConditions(village, beings);

			expect(result.defeat).toBe(true);
			expect(result.victory).toBe(false);
		});

		it('returns defeat when food runs out with no farms', () => {
			village.resources.food.amount = 0;

			const result = checkVillageConditions(village, [createBeing('b1', 0, 0, 0)]);

			expect(result.defeat).toBe(true);
		});

		it('continues when food is low but farms exist', () => {
			village.resources.food.amount = 0;

			const farm = placeBuilding(village, BUILDING_TEMPLATES.farmhouse, 100, 100)!;
			farm.operational = true;

			const result = checkVillageConditions(village, [createBeing('b1', 0, 0, 0)]);

			expect(result.defeat).toBe(false);
		});
	});
});
