import { describe, it } from 'vitest';
import { createRealm, SUPREME_BEINGS, PRIME_DIRECTIVES } from './Realm';
import { createVillage, placeBuilding, assignWorker, BUILDING_TEMPLATES } from './Village';
import { EvolutionEngine, initializePopulation } from './Evolution';
import { VillageEvolutionEngine } from './VillageEvolution';
import * as fs from 'fs';
import * as path from 'path';

// Experiment parameters
const TICKS_PER_RUN = 500; // Shortened for faster execution
const REPLICATES = 3;
const INITIAL_POPULATION = 20;

interface TickData {
	tick: number;
	population: number;
	averageFitness: number;
	averageAge: number;
	geneticDiversity: number;
	totalBirths: number;
	totalDeaths: number;
	avgCooperation: number;
	avgCuriosity: number;
	avgPerception: number;
	avgEnergy: number;
	avgFertility: number;
	buildingCount?: number;
	employedBeings?: number;
	foodAmount?: number;
	waterAmount?: number;
}

class ExperimentData {
	condition: string;
	replicate: number;
	ticks: TickData[] = [];

	constructor(condition: string, replicate: number) {
		this.condition = condition;
		this.replicate = replicate;
	}

	recordTick(tick: number, realm: any, village: any = null) {
		const aliveBeings = realm.beings.filter((b: any) => b.alive);
		const count = aliveBeings.length;

		this.ticks.push({
			tick,
			population: count,
			averageFitness: realm.beingStats.averageFitness,
			averageAge: realm.beingStats.averageAge,
			geneticDiversity: realm.beingStats.geneticDiversity,
			totalBirths: realm.beingStats.totalBirths,
			totalDeaths: realm.beingStats.totalDeaths,
			avgCooperation: count > 0 ? aliveBeings.reduce((sum: number, b: any) => sum + b.genome.cooperation, 0) / count : 0,
			avgCuriosity: count > 0 ? aliveBeings.reduce((sum: number, b: any) => sum + b.genome.curiosity, 0) / count : 0,
			avgPerception: count > 0 ? aliveBeings.reduce((sum: number, b: any) => sum + b.genome.perception, 0) / count : 0,
			avgEnergy: count > 0 ? aliveBeings.reduce((sum: number, b: any) => sum + b.genome.energy, 0) / count : 0,
			avgFertility: count > 0 ? aliveBeings.reduce((sum: number, b: any) => sum + b.genome.fertility, 0) / count : 0,
			...(village ? {
				buildingCount: village.buildings.length,
				employedBeings: village.jobs.length,
				foodAmount: village.resources.food.amount,
				waterAmount: village.resources.water.amount
			} : {})
		});
	}

	exportJSON() {
		const finalTick = this.ticks[this.ticks.length - 1];
		return {
			condition: this.condition,
			replicate: this.replicate,
			finalPopulation: finalTick?.population || 0,
			peakPopulation: Math.max(...this.ticks.map(t => t.population)),
			averageFinalFitness: finalTick?.averageFitness || 0,
			populationOverTime: this.ticks.map(t => ({ tick: t.tick, value: t.population })),
			fitnessOverTime: this.ticks.map(t => ({ tick: t.tick, value: t.averageFitness })),
			geneticTraitsOverTime: this.ticks.map(t => ({
				tick: t.tick,
				cooperation: t.avgCooperation,
				curiosity: t.avgCuriosity,
				perception: t.avgPerception,
				energy: t.avgEnergy,
				fertility: t.avgFertility
			})),
			summaryStats: {
				finalPopulation: finalTick?.population || 0,
				totalBirths: finalTick?.totalBirths || 0,
				totalDeaths: finalTick?.totalDeaths || 0,
				peakFitness: Math.max(...this.ticks.map(t => t.averageFitness))
			}
		};
	}
}

describe('WAFT Village Evolution Experiment', () => {
	it('runs complete scientific experiment and exports data', () => {
		console.log('\n╔═══════════════════════════════════════════════════════════════╗');
		console.log('║  WAFT VILLAGE EVOLUTION EXPERIMENT                          ║');
		console.log('║  "Infrastructure as Evolutionary Pressure"                   ║');
		console.log('╚═══════════════════════════════════════════════════════════════╝');

		const results = {
			metadata: {
				timestamp: new Date().toISOString(),
				duration: TICKS_PER_RUN,
				replicates: REPLICATES,
				initialPopulation: INITIAL_POPULATION
			},
			control: [] as any[],
			treatment: [] as any[]
		};

		// Run control experiments
		console.log('\n' + '='.repeat(65));
		console.log('CONTROL GROUP: Pure Evolution (No Infrastructure)');
		console.log('='.repeat(65));

		for (let replicate = 0; replicate < REPLICATES; replicate++) {
			console.log(`\n🧬 Running CONTROL replicate ${replicate + 1}/${REPLICATES}...`);

			const realm = createRealm({
				name: `Control-${replicate}`,
				description: 'Pure evolution',
				initialPopulation: INITIAL_POPULATION,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 250,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			realm.beings = initializePopulation(realm, INITIAL_POPULATION, 800, 600);
			const engine = new EvolutionEngine(realm);
			const data = new ExperimentData('control', replicate);

			for (let tick = 0; tick < TICKS_PER_RUN; tick++) {
				engine.tick();
				if (tick % 20 === 0) data.recordTick(tick, realm);
				if (realm.beings.filter((b: any) => b.alive).length === 0) break;
			}

			const final = realm.beings.filter((b: any) => b.alive).length;
			console.log(`  ✅ Complete: ${final} beings alive`);
			results.control.push(data.exportJSON());
		}

		// Run treatment experiments
		console.log('\n' + '='.repeat(65));
		console.log('TREATMENT GROUP: Village Evolution (With Infrastructure)');
		console.log('='.repeat(65));

		for (let replicate = 0; replicate < REPLICATES; replicate++) {
			console.log(`\n🏘️  Running TREATMENT replicate ${replicate + 1}/${REPLICATES}...`);

			const realm = createRealm({
				name: `Treatment-${replicate}`,
				description: 'Evolution with village',
				initialPopulation: INITIAL_POPULATION,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 250,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			const village = createVillage(`Village-${replicate}`);
			realm.beings = initializePopulation(realm, INITIAL_POPULATION, 800, 600);

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
				for (let i = 0; i < 3 && i < cooperative.length; i++) {
					assignWorker(village, farm, cooperative[i]);
				}
			}

			const engine = new VillageEvolutionEngine(realm, village);
			const data = new ExperimentData('treatment', replicate);

			for (let tick = 0; tick < TICKS_PER_RUN; tick++) {
				engine.tick();
				if (tick % 20 === 0) data.recordTick(tick, realm, village);
				if (realm.beings.filter((b: any) => b.alive).length === 0) break;
			}

			const final = realm.beings.filter((b: any) => b.alive).length;
			console.log(`  ✅ Complete: ${final} beings alive, ${village.jobs.length} employed`);
			results.treatment.push(data.exportJSON());
		}

		// Export results
		const outputPath = path.join(process.cwd(), 'experiment-results.json');
		fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));

		// Print summary
		console.log('\n' + '='.repeat(65));
		console.log('EXPERIMENT COMPLETE!');
		console.log('='.repeat(65));

		const controlAvgPop = results.control.reduce((sum, r) => sum + r.finalPopulation, 0) / REPLICATES;
		const treatmentAvgPop = results.treatment.reduce((sum, r) => sum + r.finalPopulation, 0) / REPLICATES;

		console.log(`\n📈 SUMMARY:`);
		console.log(`  Control avg population: ${controlAvgPop.toFixed(1)}`);
		console.log(`  Treatment avg population: ${treatmentAvgPop.toFixed(1)}`);
		console.log(`  Infrastructure impact: ${((treatmentAvgPop - controlAvgPop) / controlAvgPop * 100).toFixed(1)}%`);
		console.log(`\n📊 Results: ${outputPath}\n`);

		// Verify some data was collected
		expect(results.control.length).toBe(REPLICATES);
		expect(results.treatment.length).toBe(REPLICATES);
	});
});
