import { describe, it, expect, beforeEach } from 'vitest';
import { VillageEvolutionEngine } from './VillageEvolution';
import { createRealm, SUPREME_BEINGS, PRIME_DIRECTIVES } from './Realm';
import { createVillage, placeBuilding, assignWorker, BUILDING_TEMPLATES } from './Village';
import { createBeing } from './Being';

describe('VillageEvolution', () => {
	let realm: any;
	let village: any;
	let engine: VillageEvolutionEngine;

	beforeEach(() => {
		realm = createRealm({
			name: 'Test Village Realm',
			description: 'Test',
			initialPopulation: 10,
			worldWidth: 800,
			worldHeight: 600,
			ticksPerEpoch: 1000,
			supremeBeing: SUPREME_BEINGS[0],
			primeDirective: PRIME_DIRECTIVES.harmony
		});

		village = createVillage('Test Village');

		// Add beings with varied genetics
		realm.beings = [
			createBeing('being-1', 100, 100, 0),
			createBeing('being-2', 200, 200, 0),
			createBeing('being-3', 300, 300, 0)
		];

		// Boost genetics for testing
		realm.beings[0].genome.perception = 0.9; // Good for wells
		realm.beings[1].genome.cooperation = 0.9; // Good for farms
		realm.beings[2].genome.curiosity = 0.9; // Good for workshops

		engine = new VillageEvolutionEngine(realm, village);
	});

	describe('VillageEvolutionEngine', () => {
		it('initializes with realm and village', () => {
			expect(engine.getRealm()).toBe(realm);
			expect(engine.getVillage()).toBe(village);
		});

		it('can set village after construction', () => {
			const newVillage = createVillage('New Village');
			const newEngine = new VillageEvolutionEngine(realm);

			expect(newEngine.getVillage()).toBeNull();

			newEngine.setVillage(newVillage);

			expect(newEngine.getVillage()).toBe(newVillage);
		});
	});

	describe('tick with village mechanics', () => {
		it('processes village production during tick', () => {
			const farm = placeBuilding(village, BUILDING_TEMPLATES.farmhouse, 100, 100)!;
			farm.operational = true;

			const being = realm.beings[1]; // High cooperation
			assignWorker(village, farm, being);

			const initialFood = village.resources.food.amount;

			engine.tick();

			expect(village.resources.food.amount).toBeGreaterThan(initialFood);
		});

		it('updates building efficiency based on worker genetics', () => {
			const well = placeBuilding(village, BUILDING_TEMPLATES.well, 100, 100)!;
			well.operational = true;

			const highPerception = realm.beings[0]; // 0.9 perception
			assignWorker(village, well, highPerception);

			engine.tick();

			expect(well.efficiency).toBeCloseTo(0.9, 1);
		});

		it('removes jobs when worker dies', () => {
			const farm = placeBuilding(village, BUILDING_TEMPLATES.farmhouse, 100, 100)!;
			farm.operational = true;

			const being = realm.beings[0];
			assignWorker(village, farm, being);

			expect(village.jobs).toHaveLength(1);

			// Kill the being
			being.alive = false;

			engine.tick();

			// Job should be removed
			expect(village.jobs).toHaveLength(0);
			expect(farm.assignedWorkers).not.toContain(being.id);
		});

		it('boosts fitness for productive workers', () => {
			const well = placeBuilding(village, BUILDING_TEMPLATES.well, 100, 100)!;
			well.operational = true;

			const being = realm.beings[0];
			being.genome.perception = 0.9; // High productivity
			assignWorker(village, well, being);

			const initialFitness = being.fitness;

			engine.tick();

			expect(being.fitness).toBeGreaterThan(initialFitness);
		});

		it('gives energy to employed workers', () => {
			const farm = placeBuilding(village, BUILDING_TEMPLATES.farmhouse, 100, 100)!;
			farm.operational = true;

			const being = realm.beings[1];
			being.energy = 0.5;
			assignWorker(village, farm, being);

			engine.tick();

			expect(being.energy).toBeGreaterThan(0.5);
		});

		it('penalizes unemployed beings', () => {
			const being = realm.beings[0];
			const initialFitness = being.fitness;

			// Run tick without employment
			engine.tick();

			expect(being.fitness).toBeLessThan(initialFitness);
		});

		it('does not penalize employed beings', () => {
			const farm = placeBuilding(village, BUILDING_TEMPLATES.farmhouse, 100, 100)!;
			farm.operational = true;

			const being = realm.beings[1];
			assignWorker(village, farm, being);

			const initialFitness = being.fitness;

			engine.tick();

			// Should not have unemployment penalty (may have other changes)
			// We just verify it's not specifically from unemployment
			expect(being.fitness).toBeGreaterThanOrEqual(initialFitness - 0.01);
		});

		it('kills beings when food runs out', () => {
			village.resources.food.amount = 0;

			const aliveBefore = realm.beings.filter((b: any) => b.alive).length;

			// Run multiple ticks to trigger starvation deaths
			for (let i = 0; i < 50; i++) {
				engine.tick();
			}

			const aliveAfter = realm.beings.filter((b: any) => b.alive).length;

			// Some beings should have died
			expect(aliveAfter).toBeLessThan(aliveBefore);
		});

		it('boosts reproduction with homes', () => {
			// Add homes
			const home1 = placeBuilding(village, BUILDING_TEMPLATES.home, 100, 100)!;
			const home2 = placeBuilding(village, BUILDING_TEMPLATES.home, 200, 200)!;
			home1.operational = true;
			home2.operational = true;

			// Set favorable conditions for reproduction
			realm.beings.forEach((being: any) => {
				being.fitness = 0.9;
				being.genome.fertility = 0.5; // Base fertility
				being.energy = 0.9;
			});

			const initialPopulation = realm.beings.length;

			// Run many ticks
			for (let i = 0; i < 100; i++) {
				engine.tick();
			}

			// Should have more births with homes than without
			expect(realm.beings.length).toBeGreaterThan(initialPopulation);
		});
	});

	describe('building-worker interaction', () => {
		it('efficient workers increase production', () => {
			const well = placeBuilding(village, BUILDING_TEMPLATES.well, 100, 100)!;
			well.operational = true;

			const efficientBeing = realm.beings[0];
			efficientBeing.genome.perception = 0.95; // Very high

			assignWorker(village, well, efficientBeing);

			const initialWater = village.resources.water.amount;

			engine.tick();

			const waterGained = village.resources.water.amount - initialWater;

			expect(waterGained).toBeGreaterThan(0);
		});

		it('inefficient workers produce less', () => {
			const well1 = placeBuilding(village, BUILDING_TEMPLATES.well, 100, 100)!;
			const well2 = placeBuilding(village, BUILDING_TEMPLATES.well, 200, 200)!;
			well1.operational = true;
			well2.operational = true;

			const efficientBeing = realm.beings[0];
			const inefficientBeing = realm.beings[1];

			efficientBeing.genome.perception = 0.9;
			inefficientBeing.genome.perception = 0.3;

			assignWorker(village, well1, efficientBeing);
			assignWorker(village, well2, inefficientBeing);

			const initialWater = village.resources.water.amount;

			engine.tick();

			// Both produce water, but efficiency should differ
			expect(well1.efficiency).toBeGreaterThan(well2.efficiency);
		});

		it('multiple workers increase building efficiency', () => {
			const farm = placeBuilding(village, BUILDING_TEMPLATES.farmhouse, 100, 100)!;
			farm.operational = true;

			// Single worker
			assignWorker(village, farm, realm.beings[0]);

			engine.tick();

			const efficiencyWithOne = farm.efficiency;

			// Add more workers
			assignWorker(village, farm, realm.beings[1]);
			assignWorker(village, farm, realm.beings[2]);

			engine.tick();

			const efficiencyWithThree = farm.efficiency;

			expect(efficiencyWithThree).toBeGreaterThan(efficiencyWithOne);
		});
	});

	describe('evolutionary pressure from buildings', () => {
		it('workers with good genetic match gain more fitness', () => {
			const well = placeBuilding(village, BUILDING_TEMPLATES.well, 100, 100)!;
			well.operational = true;

			const goodMatch = realm.beings[0];
			const poorMatch = realm.beings[1];

			goodMatch.genome.perception = 0.9; // Well requires perception
			poorMatch.genome.perception = 0.3;

			goodMatch.fitness = 0.5;
			poorMatch.fitness = 0.5;

			assignWorker(village, well, goodMatch);

			// Run ticks
			for (let i = 0; i < 10; i++) {
				engine.tick();
			}

			// Good match should have higher fitness due to productivity bonuses
			expect(goodMatch.fitness).toBeGreaterThan(0.5);
		});

		it('creates selection pressure over multiple generations', () => {
			// Build a farm requiring cooperation
			const farm = placeBuilding(village, BUILDING_TEMPLATES.farmhouse, 100, 100)!;
			farm.operational = true;

			// Assign cooperative being
			const cooperative = realm.beings[1];
			cooperative.genome.cooperation = 0.9;
			cooperative.genome.fertility = 0.8;
			cooperative.fitness = 0.9;
			cooperative.energy = 0.9;

			assignWorker(village, farm, cooperative);

			// Assign non-cooperative being (unemployed)
			const nonCooperative = realm.beings[2];
			nonCooperative.genome.cooperation = 0.2;
			nonCooperative.genome.fertility = 0.8;
			nonCooperative.fitness = 0.5;
			nonCooperative.energy = 0.9;

			// Run many generations
			for (let i = 0; i < 100; i++) {
				engine.tick();
			}

			// Cooperative being should have higher fitness and more offspring
			expect(cooperative.fitness).toBeGreaterThan(nonCooperative.fitness);
		});
	});

	describe('resource consumption', () => {
		it('consumes food each tick', () => {
			const initialFood = village.resources.food.amount;

			engine.tick();

			expect(village.resources.food.amount).toBeLessThan(initialFood);
		});

		it('food consumption scales with population', () => {
			const smallPopulation = 3;
			const largePopulation = 10;

			// Small population
			realm.beings = [
				createBeing('b1', 100, 100, 0),
				createBeing('b2', 200, 200, 0),
				createBeing('b3', 300, 300, 0)
			];

			village.resources.food.amount = 1000;

			engine.tick();

			const foodAfterSmall = village.resources.food.amount;
			const consumedSmall = 1000 - foodAfterSmall;

			// Large population
			realm.beings = [];
			for (let i = 0; i < largePopulation; i++) {
				realm.beings.push(createBeing(`b${i}`, i * 50, i * 50, 0));
			}

			village.resources.food.amount = 1000;

			engine.tick();

			const foodAfterLarge = village.resources.food.amount;
			const consumedLarge = 1000 - foodAfterLarge;

			expect(consumedLarge).toBeGreaterThan(consumedSmall);
		});
	});
});
