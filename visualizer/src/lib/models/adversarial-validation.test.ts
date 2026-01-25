import { describe, it, expect } from 'vitest';
import { createRealm, SUPREME_BEINGS, PRIME_DIRECTIVES } from './Realm';
import { createVillage, placeBuilding, assignWorker, BUILDING_TEMPLATES } from './Village';
import { EvolutionEngine, initializePopulation } from './Evolution';
import { VillageEvolutionEngine } from './VillageEvolution';

/**
 * ADVERSARIAL VALIDATION TESTS
 *
 * Testing the criticisms from the adversarial review:
 * 1. Is the effect reproducible with different random seeds?
 * 2. What's the actual variance?
 * 3. Does sample size matter?
 * 4. Is it really extinction or just population decline?
 */

describe('Adversarial Validation: Testing the Critics', () => {

	it('TEST 1: Reproducibility with different seeds - Run 10 control replicates', () => {
		console.log('\n🔬 ADVERSARIAL TEST 1: Reproducibility (n=10)');
		console.log('Testing if results are reproducible or just random...\n');

		const results = [];

		for (let i = 0; i < 10; i++) {
			const realm = createRealm({
				name: `Control-${i}`,
				description: 'Pure evolution',
				initialPopulation: 20,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 250,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			realm.beings = initializePopulation(realm, 20, 800, 600);
			const engine = new EvolutionEngine(realm);

			// Run 500 ticks
			for (let tick = 0; tick < 500; tick++) {
				engine.tick();
			}

			const finalPop = realm.beings.filter(b => b.alive).length;
			results.push(finalPop);
			console.log(`  Run ${i + 1}: ${finalPop} beings alive`);
		}

		// Calculate statistics
		const mean = results.reduce((sum, val) => sum + val, 0) / results.length;
		const variance = results.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / results.length;
		const stdDev = Math.sqrt(variance);
		const cv = (stdDev / mean) * 100; // Coefficient of variation

		console.log(`\n  📊 STATISTICS:`);
		console.log(`     Mean: ${mean.toFixed(1)}`);
		console.log(`     Std Dev: ${stdDev.toFixed(1)}`);
		console.log(`     CV: ${cv.toFixed(1)}%`);
		console.log(`     Min: ${Math.min(...results)}`);
		console.log(`     Max: ${Math.max(...results)}`);

		// High variance would suggest randomness dominates
		if (cv > 50) {
			console.log(`\n  ⚠️  HIGH VARIANCE! Results may be dominated by randomness.`);
		} else {
			console.log(`\n  ✓ Moderate variance. Effect appears consistent.`);
		}

		expect(results.length).toBe(10);
	});

	it('TEST 2: Treatment group with n=10 - Check if extinction is consistent', () => {
		console.log('\n🔬 ADVERSARIAL TEST 2: Treatment Group Consistency (n=10)');
		console.log('Testing if village infrastructure consistently causes problems...\n');

		const results = [];

		for (let i = 0; i < 10; i++) {
			const realm = createRealm({
				name: `Treatment-${i}`,
				description: 'Village evolution',
				initialPopulation: 20,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 250,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			const village = createVillage(`Village-${i}`);
			realm.beings = initializePopulation(realm, 20, 800, 600);

			// Build infrastructure
			const well = placeBuilding(village, BUILDING_TEMPLATES.well, 200, 200);
			const farm = placeBuilding(village, BUILDING_TEMPLATES.farmhouse, 400, 300);

			if (well) {
				well.operational = true;
				const best = [...realm.beings].sort((a, b) => b.genome.perception - a.genome.perception)[0];
				assignWorker(village, well, best);
			}

			if (farm) {
				farm.operational = true;
				const cooperative = [...realm.beings].sort((a, b) => b.genome.cooperation - a.genome.cooperation);
				for (let j = 0; j < 3 && j < cooperative.length; j++) {
					assignWorker(village, farm, cooperative[j]);
				}
			}

			const engine = new VillageEvolutionEngine(realm, village);

			// Run 500 ticks
			for (let tick = 0; tick < 500; tick++) {
				engine.tick();
			}

			const finalPop = realm.beings.filter(b => b.alive).length;
			const finalFood = village.resources.food.amount;
			results.push({ population: finalPop, food: finalFood });
			console.log(`  Run ${i + 1}: ${finalPop} beings, ${finalFood.toFixed(1)} food`);
		}

		// Statistics
		const populations = results.map(r => r.population);
		const mean = populations.reduce((sum, val) => sum + val, 0) / populations.length;
		const stdDev = Math.sqrt(populations.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / populations.length);
		const extinctions = populations.filter(p => p === 0).length;

		console.log(`\n  📊 TREATMENT STATISTICS:`);
		console.log(`     Mean Population: ${mean.toFixed(1)}`);
		console.log(`     Std Dev: ${stdDev.toFixed(1)}`);
		console.log(`     True Extinctions (0 beings): ${extinctions}/10`);
		console.log(`     Near-Extinctions (<5 beings): ${populations.filter(p => p < 5).length}/10`);

		expect(results.length).toBe(10);
	});

	it('TEST 3: Statistical Significance - t-test between control and treatment', () => {
		console.log('\n🔬 ADVERSARIAL TEST 3: Statistical Significance');
		console.log('Computing t-test that the original paper forgot...\n');

		// Run both groups (n=10 each)
		const controlPops: number[] = [];
		const treatmentPops: number[] = [];

		// Control group
		for (let i = 0; i < 10; i++) {
			const realm = createRealm({
				name: `Control-${i}`,
				description: 'Pure evolution',
				initialPopulation: 20,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 250,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			realm.beings = initializePopulation(realm, 20, 800, 600);
			const engine = new EvolutionEngine(realm);

			for (let tick = 0; tick < 500; tick++) engine.tick();
			controlPops.push(realm.beings.filter(b => b.alive).length);
		}

		// Treatment group
		for (let i = 0; i < 10; i++) {
			const realm = createRealm({
				name: `Treatment-${i}`,
				description: 'Village',
				initialPopulation: 20,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 250,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			const village = createVillage(`V-${i}`);
			realm.beings = initializePopulation(realm, 20, 800, 600);

			const well = placeBuilding(village, BUILDING_TEMPLATES.well, 200, 200);
			const farm = placeBuilding(village, BUILDING_TEMPLATES.farmhouse, 400, 300);

			if (well) {
				well.operational = true;
				const best = [...realm.beings].sort((a, b) => b.genome.perception - a.genome.perception)[0];
				assignWorker(village, well, best);
			}

			if (farm) {
				farm.operational = true;
				const coop = [...realm.beings].sort((a, b) => b.genome.cooperation - a.genome.cooperation);
				for (let j = 0; j < 3 && j < coop.length; j++) assignWorker(village, farm, coop[j]);
			}

			const engine = new VillageEvolutionEngine(realm, village);
			for (let tick = 0; tick < 500; tick++) engine.tick();
			treatmentPops.push(realm.beings.filter(b => b.alive).length);
		}

		// Calculate statistics
		const controlMean = controlPops.reduce((sum, val) => sum + val, 0) / controlPops.length;
		const treatmentMean = treatmentPops.reduce((sum, val) => sum + val, 0) / treatmentPops.length;

		const controlVar = controlPops.reduce((sum, val) => sum + Math.pow(val - controlMean, 2), 0) / (controlPops.length - 1);
		const treatmentVar = treatmentPops.reduce((sum, val) => sum + Math.pow(val - treatmentMean, 2), 0) / (treatmentPops.length - 1);

		const controlSD = Math.sqrt(controlVar);
		const treatmentSD = Math.sqrt(treatmentVar);

		// Welch's t-test (unequal variances)
		const pooledSE = Math.sqrt(controlVar / controlPops.length + treatmentVar / treatmentPops.length);
		const tStat = (controlMean - treatmentMean) / pooledSE;

		// Degrees of freedom (Welch-Satterthwaite)
		const df = Math.pow(controlVar / controlPops.length + treatmentVar / treatmentPops.length, 2) /
			(Math.pow(controlVar / controlPops.length, 2) / (controlPops.length - 1) +
				Math.pow(treatmentVar / treatmentPops.length, 2) / (treatmentPops.length - 1));

		// Effect size (Cohen's d)
		const pooledSD = Math.sqrt((controlVar + treatmentVar) / 2);
		const cohensD = (controlMean - treatmentMean) / pooledSD;

		console.log(`  📊 STATISTICAL RESULTS:`);
		console.log(`\n  Control Group (n=10):`);
		console.log(`     Mean: ${controlMean.toFixed(2)}`);
		console.log(`     SD: ${controlSD.toFixed(2)}`);
		console.log(`     Values: ${controlPops.join(', ')}`);

		console.log(`\n  Treatment Group (n=10):`);
		console.log(`     Mean: ${treatmentMean.toFixed(2)}`);
		console.log(`     SD: ${treatmentSD.toFixed(2)}`);
		console.log(`     Values: ${treatmentPops.join(', ')}`);

		console.log(`\n  T-Test Results:`);
		console.log(`     t-statistic: ${tStat.toFixed(3)}`);
		console.log(`     degrees of freedom: ${df.toFixed(1)}`);
		console.log(`     Cohen's d: ${cohensD.toFixed(3)}`);

		// Approximate p-value (for df≈18, t>2.1 → p<0.05)
		if (Math.abs(tStat) > 2.1) {
			console.log(`     p-value: < 0.05 ✓ SIGNIFICANT`);
		} else {
			console.log(`     p-value: > 0.05 ✗ NOT SIGNIFICANT`);
		}

		// Effect size interpretation
		if (Math.abs(cohensD) > 0.8) {
			console.log(`     Effect size: LARGE ✓`);
		} else if (Math.abs(cohensD) > 0.5) {
			console.log(`     Effect size: MEDIUM`);
		} else {
			console.log(`     Effect size: SMALL`);
		}

		console.log(`\n  💡 VERDICT: ${Math.abs(tStat) > 2.1 && Math.abs(cohensD) > 0.8 ? 'EFFECT IS REAL! ✓' : 'EFFECT IS QUESTIONABLE ✗'}`);

		expect(controlPops.length).toBe(10);
		expect(treatmentPops.length).toBe(10);
	});

	it('TEST 4: Are they REALLY extinct? Check actual zero populations', () => {
		console.log('\n🔬 ADVERSARIAL TEST 4: True Extinction Rate');
		console.log('Testing the claim of "100% extinction"...\n');

		let trueExtinctions = 0;
		let nearExtinctions = 0;
		const populations = [];

		for (let i = 0; i < 20; i++) {
			const realm = createRealm({
				name: `T-${i}`,
				description: 'Village',
				initialPopulation: 20,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 250,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			const village = createVillage(`V-${i}`);
			realm.beings = initializePopulation(realm, 20, 800, 600);

			const well = placeBuilding(village, BUILDING_TEMPLATES.well, 200, 200);
			const farm = placeBuilding(village, BUILDING_TEMPLATES.farmhouse, 400, 300);

			if (well) {
				well.operational = true;
				const best = [...realm.beings].sort((a, b) => b.genome.perception - a.genome.perception)[0];
				assignWorker(village, well, best);
			}

			if (farm) {
				farm.operational = true;
				const coop = [...realm.beings].sort((a, b) => b.genome.cooperation - a.genome.cooperation);
				for (let j = 0; j < 3 && j < coop.length; j++) assignWorker(village, farm, coop[j]);
			}

			const engine = new VillageEvolutionEngine(realm, village);
			for (let tick = 0; tick < 500; tick++) engine.tick();

			const finalPop = realm.beings.filter(b => b.alive).length;
			populations.push(finalPop);

			if (finalPop === 0) trueExtinctions++;
			if (finalPop < 3) nearExtinctions++;
		}

		console.log(`  📊 EXTINCTION ANALYSIS (n=20):`);
		console.log(`     True Extinctions (0 beings): ${trueExtinctions}/20 (${(trueExtinctions / 20 * 100).toFixed(0)}%)`);
		console.log(`     Near-Extinctions (<3 beings): ${nearExtinctions}/20 (${(nearExtinctions / 20 * 100).toFixed(0)}%)`);
		console.log(`     Average final population: ${(populations.reduce((sum, val) => sum + val, 0) / populations.length).toFixed(1)}`);
		console.log(`\n  Populations: ${populations.sort((a, b) => a - b).join(', ')}`);

		console.log(`\n  💡 VERDICT: Original claim of "100% extinction" is ${trueExtinctions === 20 ? 'TRUE ✓' : 'FALSE ✗'}`);

		expect(populations.length).toBe(20);
	});
});
