import { describe, it, expect, beforeEach } from 'vitest';
import {
	GENESIS_FARM_TUTORIAL,
	checkStepCompletion,
	advanceTutorialStep,
	applyStepRewards,
	triggerDrought,
	type Tutorial
} from './Tutorial';
import { createVillage, placeBuilding, assignWorker, BUILDING_TEMPLATES } from './Village';
import { createBeing } from './Being';

describe('Tutorial', () => {
	let tutorial: Tutorial;
	let village: any;
	let beings: any[];

	beforeEach(() => {
		tutorial = JSON.parse(JSON.stringify(GENESIS_FARM_TUTORIAL)); // Deep copy
		village = createVillage('Test Village');
		beings = [
			createBeing('being-1', 100, 100, 0),
			createBeing('being-2', 200, 200, 0),
			createBeing('being-3', 300, 300, 0)
		];
		tutorial.startTick = 0;
	});

	describe('GENESIS_FARM_TUTORIAL', () => {
		it('has 10 steps', () => {
			expect(GENESIS_FARM_TUTORIAL.steps).toHaveLength(10);
		});

		it('starts at step 0', () => {
			expect(GENESIS_FARM_TUTORIAL.currentStep).toBe(0);
		});

		it('is not completed initially', () => {
			expect(GENESIS_FARM_TUTORIAL.completed).toBe(false);
		});

		it('has unique step IDs', () => {
			const ids = GENESIS_FARM_TUTORIAL.steps.map(s => s.id);
			const uniqueIds = new Set(ids);
			expect(uniqueIds.size).toBe(ids.length);
		});
	});

	describe('checkStepCompletion', () => {
		it('completes welcome step after 1 tick', () => {
			tutorial.currentStep = 0; // Welcome step
			tutorial.startTick = 0;

			const result = checkStepCompletion(tutorial, village, beings, 0);
			expect(result).toBe(false); // 0 ticks elapsed

			const result2 = checkStepCompletion(tutorial, village, beings, 1);
			expect(result2).toBe(true); // 1 tick elapsed
		});

		it('completes build-well step when well is placed', () => {
			tutorial.currentStep = 1; // Build well step

			const incomplete = checkStepCompletion(tutorial, village, beings, 10);
			expect(incomplete).toBe(false); // No well yet

			placeBuilding(village, BUILDING_TEMPLATES.well, 100, 100);

			const complete = checkStepCompletion(tutorial, village, beings, 10);
			expect(complete).toBe(true); // Well placed
		});

		it('completes assign-worker step when 1+ workers assigned', () => {
			tutorial.currentStep = 2; // Assign worker step

			const building = placeBuilding(village, BUILDING_TEMPLATES.well, 100, 100)!;
			building.operational = true;

			const incomplete = checkStepCompletion(tutorial, village, beings, 10);
			expect(incomplete).toBe(false); // No workers yet

			assignWorker(village, building, beings[0]);

			const complete = checkStepCompletion(tutorial, village, beings, 10);
			expect(complete).toBe(true); // Worker assigned
		});

		it('completes build-farmhouse step with farmhouse + 3 workers', () => {
			tutorial.currentStep = 3; // Build farmhouse step

			const farm = placeBuilding(village, BUILDING_TEMPLATES.farmhouse, 100, 100)!;
			farm.operational = true;

			const incomplete = checkStepCompletion(tutorial, village, beings, 10);
			expect(incomplete).toBe(false); // Not enough workers

			assignWorker(village, farm, beings[0]);
			assignWorker(village, farm, beings[1]);
			assignWorker(village, farm, beings[2]);

			const complete = checkStepCompletion(tutorial, village, beings, 10);
			expect(complete).toBe(true); // Farmhouse + 3 workers
		});

		it('completes build-home step with 2 homes', () => {
			tutorial.currentStep = 4; // Build home step

			placeBuilding(village, BUILDING_TEMPLATES.home, 100, 100);

			const incomplete = checkStepCompletion(tutorial, village, beings, 10);
			expect(incomplete).toBe(false); // Only 1 home

			placeBuilding(village, BUILDING_TEMPLATES.home, 200, 200);

			const complete = checkStepCompletion(tutorial, village, beings, 10);
			expect(complete).toBe(true); // 2 homes
		});

		it('completes gather-resources step with 200 food', () => {
			tutorial.currentStep = 5; // Gather resources step

			village.resources.food.amount = 150;

			const incomplete = checkStepCompletion(tutorial, village, beings, 10);
			expect(incomplete).toBe(false); // Only 150 food

			village.resources.food.amount = 200;

			const complete = checkStepCompletion(tutorial, village, beings, 10);
			expect(complete).toBe(true); // 200 food
		});

		it('completes final-challenge with 100 ticks + 5 beings alive', () => {
			tutorial.currentStep = 8; // Final challenge step
			tutorial.startTick = 100;

			const incomplete1 = checkStepCompletion(tutorial, village, beings, 150);
			expect(incomplete1).toBe(false); // Only 50 ticks, need 100

			const incomplete2 = checkStepCompletion(tutorial, village, beings, 200);
			expect(incomplete2).toBe(false); // 100 ticks but only 3 beings alive

			// Add more beings
			beings.push(createBeing('being-4', 400, 400, 0));
			beings.push(createBeing('being-5', 500, 500, 0));

			const complete = checkStepCompletion(tutorial, village, beings, 200);
			expect(complete).toBe(true); // 100 ticks + 5 beings
		});

		it('returns true for empty completion requirements', () => {
			tutorial.currentStep = 9; // Tutorial complete step (no requirements)

			const complete = checkStepCompletion(tutorial, village, beings, 0);
			expect(complete).toBe(true); // No requirements
		});
	});

	describe('advanceTutorialStep', () => {
		it('advances from step 0 to step 1', () => {
			tutorial.currentStep = 0;

			const advanced = advanceTutorialStep(tutorial);

			expect(advanced).toBe(true);
			expect(tutorial.currentStep).toBe(1);
			expect(tutorial.completed).toBe(false);
		});

		it('advances through middle steps', () => {
			tutorial.currentStep = 4;

			advanceTutorialStep(tutorial);

			expect(tutorial.currentStep).toBe(5);
		});

		it('marks tutorial complete at final step', () => {
			tutorial.currentStep = 9; // Last step

			const advanced = advanceTutorialStep(tutorial);

			expect(advanced).toBe(false); // Can't advance further
			expect(tutorial.completed).toBe(true);
		});

		it('does not advance beyond final step', () => {
			tutorial.currentStep = 9;
			tutorial.completed = true;

			advanceTutorialStep(tutorial);

			expect(tutorial.currentStep).toBe(9); // Still at 9
			expect(tutorial.completed).toBe(true);
		});
	});

	describe('applyStepRewards', () => {
		it('adds resource rewards to village', () => {
			tutorial.currentStep = 1; // Build well (rewards: +10 stone)

			const initialStone = village.resources.stone.amount;

			applyStepRewards(tutorial, village);

			expect(village.resources.stone.amount).toBe(initialStone + 10);
		});

		it('adds multiple resources', () => {
			tutorial.currentStep = 5; // Gather resources (rewards: +30 wood, +20 stone)

			const initialWood = village.resources.wood.amount;
			const initialStone = village.resources.stone.amount;

			applyStepRewards(tutorial, village);

			expect(village.resources.wood.amount).toBe(initialWood + 30);
			expect(village.resources.stone.amount).toBe(initialStone + 20);
		});

		it('does nothing when step has no rewards', () => {
			tutorial.currentStep = 0; // Welcome (no resource rewards)

			const initialFood = village.resources.food.amount;
			const initialWood = village.resources.wood.amount;

			applyStepRewards(tutorial, village);

			expect(village.resources.food.amount).toBe(initialFood);
			expect(village.resources.wood.amount).toBe(initialWood);
		});
	});

	describe('triggerDrought', () => {
		it('reduces all well production by 75%', () => {
			// Add enough resources for two wells (each costs 15 stone + 5 wood)
			village.resources.stone.amount = 100;
			village.resources.wood.amount = 100;

			const well1 = placeBuilding(village, BUILDING_TEMPLATES.well, 100, 100)!;
			const well2 = placeBuilding(village, BUILDING_TEMPLATES.well, 200, 200)!;
			well1.operational = true;
			well2.operational = true;
			well1.efficiency = 1.0;
			well2.efficiency = 0.8;

			triggerDrought(village);

			expect(well1.efficiency).toBe(0.25); // 1.0 * 0.25
			expect(well2.efficiency).toBe(0.2);  // 0.8 * 0.25
		});

		it('only affects wells, not other buildings', () => {
			// Add enough resources
			village.resources.stone.amount = 100;
			village.resources.wood.amount = 100;

			const well = placeBuilding(village, BUILDING_TEMPLATES.well, 100, 100)!;
			const farm = placeBuilding(village, BUILDING_TEMPLATES.farmhouse, 200, 200)!;
			well.operational = true;
			farm.operational = true;
			well.efficiency = 1.0;
			farm.efficiency = 1.0;

			triggerDrought(village);

			expect(well.efficiency).toBe(0.25);  // Reduced
			expect(farm.efficiency).toBe(1.0);   // Unchanged
		});

		it('affects multiple wells', () => {
			// Add enough resources for three wells
			village.resources.stone.amount = 100;
			village.resources.wood.amount = 100;

			const wells = [
				placeBuilding(village, BUILDING_TEMPLATES.well, 100, 100)!,
				placeBuilding(village, BUILDING_TEMPLATES.well, 200, 200)!,
				placeBuilding(village, BUILDING_TEMPLATES.well, 300, 300)!
			];

			wells.forEach(w => {
				w.operational = true;
				w.efficiency = 1.0;
			});

			triggerDrought(village);

			wells.forEach(w => {
				expect(w.efficiency).toBe(0.25);
			});
		});
	});
});
