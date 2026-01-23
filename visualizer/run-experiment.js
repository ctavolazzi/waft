#!/usr/bin/env node

/**
 * WAFT Village Evolution Experiment Runner
 *
 * This script runs controlled experiments to measure the impact of
 * infrastructure (village buildings) on evolutionary outcomes.
 *
 * Experiment Design:
 * - Control Group: Pure evolution with no buildings
 * - Treatment Group: Evolution with village infrastructure
 * - Duration: 1000 ticks per run
 * - Replicates: 5 runs per condition
 */

import { createRealm, SUPREME_BEINGS, PRIME_DIRECTIVES } from './src/lib/models/Realm.js';
import { createVillage, placeBuilding, assignWorker, BUILDING_TEMPLATES } from './src/lib/models/Village.js';
import { EvolutionEngine, initializePopulation } from './src/lib/models/Evolution.js';
import { VillageEvolutionEngine } from './src/lib/models/VillageEvolution.js';
import { createBeing } from './src/lib/models/Being.js';
import * as fs from 'fs';
import * as path from 'path';

// Experiment parameters
const TICKS_PER_RUN = 1000;
const REPLICATES = 5;
const INITIAL_POPULATION = 20;

// Data collection
class ExperimentData {
	constructor(condition, replicate) {
		this.condition = condition;
		this.replicate = replicate;
		this.ticks = [];
	}

	recordTick(tick, realm, village = null) {
		const aliveBeings = realm.beings.filter(b => b.alive);

		this.ticks.push({
			tick,
			population: aliveBeings.length,
			averageFitness: realm.beingStats.averageFitness,
			averageAge: realm.beingStats.averageAge,
			geneticDiversity: realm.beingStats.geneticDiversity,
			totalBirths: realm.beingStats.totalBirths,
			totalDeaths: realm.beingStats.totalDeaths,
			extinctionEvents: realm.beingStats.extinctionEvents,

			// Average genome traits
			avgCooperation: aliveBeings.reduce((sum, b) => sum + b.genome.cooperation, 0) / aliveBeings.length || 0,
			avgCuriosity: aliveBeings.reduce((sum, b) => sum + b.genome.curiosity, 0) / aliveBeings.length || 0,
			avgPerception: aliveBeings.reduce((sum, b) => sum + b.genome.perception, 0) / aliveBeings.length || 0,
			avgEnergy: aliveBeings.reduce((sum, b) => sum + b.genome.energy, 0) / aliveBeings.length || 0,
			avgFertility: aliveBeings.reduce((sum, b) => sum + b.genome.fertility, 0) / aliveBeings.length || 0,

			// Village stats (if applicable)
			...(village ? {
				buildingCount: village.buildings.length,
				operationalBuildings: village.buildings.filter(b => b.operational).length,
				employedBeings: village.jobs.length,
				foodAmount: village.resources.food.amount,
				waterAmount: village.resources.water.amount,
				woodAmount: village.resources.wood.amount,
				stoneAmount: village.resources.stone.amount
			} : {})
		});
	}

	exportJSON() {
		return {
			condition: this.condition,
			replicate: this.replicate,
			finalPopulation: this.ticks[this.ticks.length - 1]?.population || 0,
			extinctionTick: this.ticks.find(t => t.extinctionEvents > 0)?.tick || null,
			peakPopulation: Math.max(...this.ticks.map(t => t.population)),
			averageFitnessOverTime: this.ticks.map(t => ({ tick: t.tick, value: t.averageFitness })),
			populationOverTime: this.ticks.map(t => ({ tick: t.tick, value: t.population })),
			geneticTraitsOverTime: this.ticks.map(t => ({
				tick: t.tick,
				cooperation: t.avgCooperation,
				curiosity: t.avgCuriosity,
				perception: t.avgPerception,
				energy: t.avgEnergy,
				fertility: t.avgFertility
			})),
			summaryStats: {
				finalPopulation: this.ticks[this.ticks.length - 1]?.population || 0,
				totalBirths: this.ticks[this.ticks.length - 1]?.totalBirths || 0,
				totalDeaths: this.ticks[this.ticks.length - 1]?.totalDeaths || 0,
				extinctions: this.ticks[this.ticks.length - 1]?.extinctionEvents || 0
			}
		};
	}
}

/**
 * Run pure evolution (control group)
 */
function runControlExperiment(replicate) {
	console.log(`\n🧬 Running CONTROL experiment (replicate ${replicate + 1}/${REPLICATES})...`);

	const realm = createRealm({
		name: `Control-${replicate}`,
		description: 'Pure evolution with no infrastructure',
		initialPopulation: INITIAL_POPULATION,
		worldWidth: 800,
		worldHeight: 600,
		ticksPerEpoch: 250,
		supremeBeing: SUPREME_BEINGS[0], // Harmonia
		primeDirective: PRIME_DIRECTIVES.harmony
	});

	// Initialize population
	realm.beings = initializePopulation(realm, INITIAL_POPULATION, 800, 600);

	const engine = new EvolutionEngine(realm);
	const data = new ExperimentData('control', replicate);

	// Run simulation
	for (let tick = 0; tick < TICKS_PER_RUN; tick++) {
		engine.tick();

		// Record data every 10 ticks
		if (tick % 10 === 0) {
			data.recordTick(tick, realm);
		}

		// Check for extinction
		if (realm.beings.filter(b => b.alive).length === 0) {
			console.log(`  ⚠️  Extinction at tick ${tick}`);
			break;
		}
	}

	const final = realm.beings.filter(b => b.alive).length;
	console.log(`  ✅ Complete: ${final} beings alive`);

	return data;
}

/**
 * Run village evolution (treatment group)
 */
function runTreatmentExperiment(replicate) {
	console.log(`\n🏘️  Running TREATMENT experiment (replicate ${replicate + 1}/${REPLICATES})...`);

	const realm = createRealm({
		name: `Treatment-${replicate}`,
		description: 'Evolution with village infrastructure',
		initialPopulation: INITIAL_POPULATION,
		worldWidth: 800,
		worldHeight: 600,
		ticksPerEpoch: 250,
		supremeBeing: SUPREME_BEINGS[0], // Harmonia
		primeDirective: PRIME_DIRECTIVES.harmony
	});

	const village = createVillage(`Village-${replicate}`);

	// Initialize population
	realm.beings = initializePopulation(realm, INITIAL_POPULATION, 800, 600);

	// Build initial infrastructure (starting resources allow this)
	const well = placeBuilding(village, BUILDING_TEMPLATES.well, 200, 200);
	const farm = placeBuilding(village, BUILDING_TEMPLATES.farmhouse, 400, 300);

	// Make them operational immediately for the experiment
	if (well) well.operational = true;
	if (farm) farm.operational = true;

	// Assign best-matched workers
	if (well) {
		const perceptiveBeings = [...realm.beings].sort((a, b) => b.genome.perception - a.genome.perception);
		assignWorker(village, well, perceptiveBeings[0]);
	}

	if (farm) {
		const cooperativeBeings = [...realm.beings].sort((a, b) => b.genome.cooperation - a.genome.cooperation);
		for (let i = 0; i < 3 && i < cooperativeBeings.length; i++) {
			assignWorker(village, farm, cooperativeBeings[i]);
		}
	}

	const engine = new VillageEvolutionEngine(realm, village);
	const data = new ExperimentData('treatment', replicate);

	// Run simulation
	for (let tick = 0; tick < TICKS_PER_RUN; tick++) {
		engine.tick();

		// Record data every 10 ticks
		if (tick % 10 === 0) {
			data.recordTick(tick, realm, village);
		}

		// Auto-hire new workers as population grows
		if (tick % 50 === 0) {
			const unemployed = realm.beings.filter(b =>
				b.alive && !village.jobs.some(j => j.beingId === b.id)
			);

			if (unemployed.length > 0 && well && well.assignedWorkers.length < well.template.maxWorkers) {
				const best = unemployed.sort((a, b) => b.genome.perception - a.genome.perception)[0];
				assignWorker(village, well, best);
			}
		}

		// Check for extinction
		if (realm.beings.filter(b => b.alive).length === 0) {
			console.log(`  ⚠️  Extinction at tick ${tick}`);
			break;
		}
	}

	const final = realm.beings.filter(b => b.alive).length;
	console.log(`  ✅ Complete: ${final} beings alive, ${village.jobs.length} employed`);

	return data;
}

/**
 * Main experiment runner
 */
async function main() {
	console.log('╔═══════════════════════════════════════════════════════════════╗');
	console.log('║  WAFT VILLAGE EVOLUTION EXPERIMENT                          ║');
	console.log('║  "Infrastructure as Evolutionary Pressure"                   ║');
	console.log('╚═══════════════════════════════════════════════════════════════╝');
	console.log(`\nExperiment Parameters:`);
	console.log(`  • Duration: ${TICKS_PER_RUN} ticks per run`);
	console.log(`  • Replicates: ${REPLICATES} per condition`);
	console.log(`  • Initial Population: ${INITIAL_POPULATION} beings`);
	console.log(`  • Conditions: Control (pure evolution) vs Treatment (village)`);

	const results = {
		metadata: {
			timestamp: new Date().toISOString(),
			duration: TICKS_PER_RUN,
			replicates: REPLICATES,
			initialPopulation: INITIAL_POPULATION
		},
		control: [],
		treatment: []
	};

	// Run control experiments
	console.log('\n' + '='.repeat(65));
	console.log('CONTROL GROUP: Pure Evolution (No Infrastructure)');
	console.log('='.repeat(65));

	for (let i = 0; i < REPLICATES; i++) {
		const data = runControlExperiment(i);
		results.control.push(data.exportJSON());
	}

	// Run treatment experiments
	console.log('\n' + '='.repeat(65));
	console.log('TREATMENT GROUP: Village Evolution (With Infrastructure)');
	console.log('='.repeat(65));

	for (let i = 0; i < REPLICATES; i++) {
		const data = runTreatmentExperiment(i);
		results.treatment.push(data.exportJSON());
	}

	// Export results
	const outputDir = path.join(process.cwd(), 'experiment-results');
	if (!fs.existsSync(outputDir)) {
		fs.mkdirSync(outputDir, { recursive: true });
	}

	const outputPath = path.join(outputDir, `experiment-${Date.now()}.json`);
	fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));

	console.log('\n' + '='.repeat(65));
	console.log('EXPERIMENT COMPLETE!');
	console.log('='.repeat(65));
	console.log(`\n📊 Results exported to: ${outputPath}`);

	// Print summary statistics
	console.log('\n📈 SUMMARY STATISTICS:\n');

	const controlSurvival = results.control.filter(r => r.finalPopulation > 0).length;
	const treatmentSurvival = results.treatment.filter(r => r.finalPopulation > 0).length;

	const controlAvgPop = results.control.reduce((sum, r) => sum + r.finalPopulation, 0) / REPLICATES;
	const treatmentAvgPop = results.treatment.reduce((sum, r) => sum + r.finalPopulation, 0) / REPLICATES;

	console.log(`Control Group:`);
	console.log(`  • Survival rate: ${controlSurvival}/${REPLICATES} (${(controlSurvival/REPLICATES*100).toFixed(1)}%)`);
	console.log(`  • Average final population: ${controlAvgPop.toFixed(1)} beings`);
	console.log(`  • Peak population: ${Math.max(...results.control.map(r => r.peakPopulation))} beings`);

	console.log(`\nTreatment Group:`);
	console.log(`  • Survival rate: ${treatmentSurvival}/${REPLICATES} (${(treatmentSurvival/REPLICATES*100).toFixed(1)}%)`);
	console.log(`  • Average final population: ${treatmentAvgPop.toFixed(1)} beings`);
	console.log(`  • Peak population: ${Math.max(...results.treatment.map(r => r.peakPopulation))} beings`);

	console.log(`\n💡 Infrastructure Impact: ${((treatmentAvgPop - controlAvgPop) / controlAvgPop * 100).toFixed(1)}% population change`);

	console.log('\n✨ Data ready for scientific paper generation!\n');
}

main().catch(console.error);
