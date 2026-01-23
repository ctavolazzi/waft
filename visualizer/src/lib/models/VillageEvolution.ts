/**
 * VillageEvolution - Extended evolution engine with village building mechanics
 *
 * Combines genetic evolution with infrastructure management:
 * - Beings work at buildings based on genetic match
 * - Resource production/consumption
 * - Fitness based on productivity
 * - Buildings create evolutionary pressure
 */

import { EvolutionEngine } from './Evolution';
import type { Realm } from './Realm';
import type { Village } from './Village';
import { tickVillageProduction, updateBuildingEfficiency } from './Village';

export class VillageEvolutionEngine extends EvolutionEngine {
	private village: Village | null = null;

	constructor(realm: Realm, village?: Village) {
		super(realm);
		this.village = village || null;
	}

	/**
	 * Set village (for tutorial initialization)
	 */
	setVillage(village: Village) {
		this.village = village;
	}

	/**
	 * Override tick to include village mechanics
	 */
	tick() {
		// Call parent tick for core evolution
		super.tick();

		// Add village-specific tick if village exists
		if (this.village) {
			this.tickVillage();
		}
	}

	/**
	 * Process village production and being-job interactions
	 */
	private tickVillage() {
		if (!this.village) return;

		const realm = this.getRealm();

		// 1. Update building efficiencies based on worker genetics
		for (const building of this.village.buildings) {
			const jobs = this.village.jobs.filter(j => j.buildingId === building.id);

			// Update productivity based on current worker genetics
			for (const job of jobs) {
				const being = realm.beings.find(b => b.id === job.beingId);
				if (being && being.alive) {
					const requiredTrait = building.template.requiredTrait;
					job.productivity = being.genome[requiredTrait];
				} else {
					// Worker died or doesn't exist - remove job
					this.village.jobs = this.village.jobs.filter(j => j !== job);
					building.assignedWorkers = building.assignedWorkers.filter(id => id !== job.beingId);
				}
			}

			updateBuildingEfficiency(building, this.village.jobs);
		}

		// 2. Process resource production/consumption
		tickVillageProduction(this.village, realm.beings);

		// 3. Boost fitness for productive workers
		for (const job of this.village.jobs) {
			const being = realm.beings.find(b => b.id === job.beingId);
			if (being && being.alive) {
				// High productivity = fitness boost
				being.fitness += job.productivity * 0.01;
				being.fitness = Math.min(1, being.fitness);

				// Also give energy boost (workers get fed)
				being.energy += 0.02;
				being.energy = Math.min(1, being.energy);
			}
		}

		// 4. Penalty for unemployment (idle beings lose fitness)
		const aliveBings = realm.beings.filter(b => b.alive);
		const employedIds = this.village.jobs.map(j => j.beingId);

		for (const being of aliveBings) {
			if (!employedIds.includes(being.id)) {
				// Unemployed beings lose fitness slowly
				being.fitness -= 0.002;
				being.fitness = Math.max(0, being.fitness);
			}
		}

		// 5. Starvation check (if no food)
		if (this.village.resources.food.amount <= 0) {
			// Random beings start dying of starvation
			const starving = aliveBings.filter(b => Math.random() < 0.1);
			for (const being of starving) {
				being.alive = false;
				being.causeOfDeath = 'starvation';
			}
		}

		// 6. Homes boost reproduction
		const homeCount = this.village.buildings.filter(
			b => b.template.type === 'home' && b.operational
		).length;

		const reproductionBoost = 1 + (homeCount * 0.5); // Each home +50% fertility

		// Apply boost to all beings
		for (const being of aliveBings) {
			// Temporarily boost fertility for this tick
			const originalFertility = being.genome.fertility;
			being.genome.fertility *= reproductionBoost;

			// (Reproduction happens in parent tick)

			// Restore original after tick
			setTimeout(() => {
				being.genome.fertility = originalFertility;
			}, 0);
		}
	}

	/**
	 * Get current village state
	 */
	getVillage(): Village | null {
		return this.village;
	}
}
