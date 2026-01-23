/**
 * Evolution - Simulation engine for evolutionary cycles
 *
 * Handles:
 * - Tick-based simulation loop
 * - Being lifecycle (birth, aging, death)
 * - Reproduction and genetic inheritance
 * - Component interactions
 * - Fitness calculation
 * - Epoch progression
 * - Historical event recording
 */

import type { Realm, HistoricalEvent, RealmComponent, Epoch } from './Realm';
import type { Being } from './Being';
import {
	createBeing,
	calculateFitness,
	crossover,
	mutate,
	calculateGeneticDiversity,
	generateRandomGenome
} from './Being';
import { EPOCH_NAMES } from './Realm';

export class EvolutionEngine {
	private realm: Realm;
	private intervalId?: number;

	constructor(realm: Realm) {
		this.realm = realm;
	}

	/**
	 * Start the simulation loop
	 */
	start() {
		if (this.realm.running) return;

		this.realm.running = true;
		const msPerTick = 1000 / this.realm.tickRate;

		this.intervalId = setInterval(() => {
			this.tick();
		}, msPerTick) as unknown as number;
	}

	/**
	 * Stop the simulation loop
	 */
	stop() {
		if (!this.realm.running) return;

		this.realm.running = false;
		if (this.intervalId !== undefined) {
			clearInterval(this.intervalId);
			this.intervalId = undefined;
		}
	}

	/**
	 * Execute one simulation tick
	 */
	tick() {
		this.realm.currentTick++;

		// 1. Age all beings
		this.ageBings();

		// 2. Move beings
		this.moveBeings();

		// 3. Handle component interactions
		this.handleComponentInteractions();

		// 4. Update fitness scores
		this.updateFitness();

		// 5. Handle deaths (low fitness, old age, etc.)
		this.handleDeaths();

		// 6. Handle reproduction
		this.handleReproduction();

		// 7. Update statistics
		this.updateStatistics();

		// 8. Check for epoch transition
		this.checkEpochTransition();

		// 9. Divine intervention (if supreme being intervenes)
		this.divineIntervention();
	}

	/**
	 * Age all beings and check for death by old age
	 */
	private ageBings() {
		for (const being of this.realm.beings) {
			if (!being.alive) continue;

			being.age++;

			// Death by old age
			if (being.age >= being.maxAge) {
				being.alive = false;
				being.causeOfDeath = 'age';
				this.realm.beingStats.totalDeaths++;
				this.recordEvent({
					tick: this.realm.currentTick,
					type: 'death',
					description: `${being.id} died of old age at ${being.age} ticks (generation ${being.generation})`,
					beingIds: [being.id],
					significance: 'minor'
				});
			}

			// Lose energy over time (metabolism)
			being.energy -= 0.001 * being.genome.energy;
			being.energy = Math.max(0, being.energy);

			// Death by starvation
			if (being.energy <= 0) {
				being.alive = false;
				being.causeOfDeath = 'starvation';
				this.realm.beingStats.totalDeaths++;
			}
		}
	}

	/**
	 * Move beings based on their velocity and genetics
	 */
	private moveBeings() {
		for (const being of this.realm.beings) {
			if (!being.alive) continue;

			// Update position
			being.x += being.vx * being.genome.speed;
			being.y += being.vy * being.genome.speed;

			// Wrap around world boundaries
			if (being.x < 0) being.x = this.realm.config.worldWidth;
			if (being.x > this.realm.config.worldWidth) being.x = 0;
			if (being.y < 0) being.y = this.realm.config.worldHeight;
			if (being.y > this.realm.config.worldHeight) being.y = 0;

			// Add random wandering
			being.vx += (Math.random() - 0.5) * 0.1;
			being.vy += (Math.random() - 0.5) * 0.1;

			// Limit velocity
			const maxSpeed = being.genome.speed * 2;
			const speed = Math.sqrt(being.vx ** 2 + being.vy ** 2);
			if (speed > maxSpeed) {
				being.vx = (being.vx / speed) * maxSpeed;
				being.vy = (being.vy / speed) * maxSpeed;
			}
		}
	}

	/**
	 * Handle interactions between beings and components
	 */
	private handleComponentInteractions() {
		for (const being of this.realm.beings) {
			if (!being.alive) continue;

			for (const component of this.realm.components) {
				const distance = Math.sqrt(
					(being.x - component.x) ** 2 + (being.y - component.y) ** 2
				);

				if (distance < component.radius) {
					this.interactWithComponent(being, component);
				}
			}
		}
	}

	/**
	 * Execute interaction between being and component
	 */
	private interactWithComponent(being: Being, component: RealmComponent) {
		// Curiosity determines if being investigates
		if (Math.random() > being.genome.curiosity) return;

		being.investigating = component.id;

		// Apply effects
		being.fitness += component.effect.fitnessModifier;
		being.energy += component.effect.energyModifier;
		being.energy = Math.max(0, Math.min(1, being.energy));

		// Mutation chance
		if (Math.random() < component.effect.mutationChance) {
			being.genome = mutate(being.genome);
			this.recordEvent({
				tick: this.realm.currentTick,
				type: 'mutation',
				description: `${being.id} mutated after interacting with ${component.name}`,
				beingIds: [being.id],
				componentId: component.id,
				significance: 'major'
			});
		}

		// Death chance
		if (Math.random() < component.effect.deathChance) {
			being.alive = false;
			being.causeOfDeath = 'component';
			this.recordEvent({
				tick: this.realm.currentTick,
				type: 'death',
				description: `${being.id} was killed by ${component.name}`,
				beingIds: [being.id],
				componentId: component.id,
				significance: 'major'
			});
		}
	}

	/**
	 * Update fitness scores for all beings
	 */
	private updateFitness() {
		for (const being of this.realm.beings) {
			if (!being.alive) continue;

			being.fitness = calculateFitness(being, this.realm.currentTick);
		}
	}

	/**
	 * Handle deaths from low fitness
	 */
	private handleDeaths() {
		const aliveBefore = this.realm.beings.filter(b => b.alive).length;

		for (const being of this.realm.beings) {
			if (!being.alive) continue;

			// Death by low fitness (evolutionary death)
			if (being.fitness < 0.2 && Math.random() < 0.1) {
				being.alive = false;
				being.causeOfDeath = 'fitness';
			}
		}

		const aliveAfter = this.realm.beings.filter(b => b.alive).length;
		const died = aliveBefore - aliveAfter;

		if (died > 0) {
			this.realm.beingStats.totalDeaths += died;
		}

		// Check for extinction
		if (aliveAfter === 0) {
			this.recordEvent({
				tick: this.realm.currentTick,
				type: 'extinction',
				description: 'EXTINCTION EVENT: All beings have perished from the realm',
				significance: 'critical'
			});
			this.realm.beingStats.extinctionEvents++;
			this.stop();
		}
	}

	/**
	 * Handle reproduction based on fitness and fertility
	 */
	private handleReproduction() {
		const aliveBings = this.realm.beings.filter(b => b.alive);
		const newBeings: Being[] = [];

		for (const being of aliveBings) {
			// Reproduction chance based on fitness and fertility
			const reproductionChance = being.fitness * being.genome.fertility * 0.01;

			if (Math.random() < reproductionChance) {
				// Find mate (nearest being with high fitness)
				const mate = this.findMate(being, aliveBings);

				if (mate) {
					// Create offspring through genetic crossover
					const childGenome = crossover(being.genome, mate.genome);
					const mutatedGenome = mutate(childGenome);

					const child = createBeing(
						`being-${this.realm.currentTick}-${newBeings.length}`,
						being.x + (Math.random() - 0.5) * 20,
						being.y + (Math.random() - 0.5) * 20,
						Math.max(being.generation, mate.generation) + 1,
						mutatedGenome
					);

					child.parentIds = [being.id, mate.id];
					being.childrenIds.push(child.id);
					mate.childrenIds.push(child.id);

					newBeings.push(child);

					// Record lineage
					const lineage = [
						...(this.realm.ancestralLineages.get(being.id) || [being.id]),
						child.id
					];
					this.realm.ancestralLineages.set(child.id, lineage);
				}
			}
		}

		// Add new beings to realm
		if (newBeings.length > 0) {
			this.realm.beings.push(...newBeings);
			this.realm.beingStats.totalBirths += newBeings.length;

			if (newBeings.length > 5) {
				this.recordEvent({
					tick: this.realm.currentTick,
					type: 'birth',
					description: `Population boom: ${newBeings.length} new beings born`,
					significance: 'major'
				});
			}
		}
	}

	/**
	 * Find suitable mate for reproduction
	 */
	private findMate(being: Being, population: Being[]): Being | null {
		const candidates = population.filter(b =>
			b.id !== being.id &&
			b.fitness > 0.4 &&
			b.genome.fertility > 0.3
		);

		if (candidates.length === 0) return null;

		// Find nearest candidate
		let nearest = candidates[0];
		let minDistance = Infinity;

		for (const candidate of candidates) {
			const distance = Math.sqrt(
				(being.x - candidate.x) ** 2 + (being.y - candidate.y) ** 2
			);

			if (distance < minDistance) {
				minDistance = distance;
				nearest = candidate;
			}
		}

		return nearest;
	}

	/**
	 * Update population statistics
	 */
	private updateStatistics() {
		const aliveBings = this.realm.beings.filter(b => b.alive);

		this.realm.beingStats.currentPopulation = aliveBings.length;

		if (aliveBings.length > 0) {
			this.realm.beingStats.averageFitness =
				aliveBings.reduce((sum, b) => sum + b.fitness, 0) / aliveBings.length;

			this.realm.beingStats.averageAge =
				aliveBings.reduce((sum, b) => sum + b.age, 0) / aliveBings.length;

			this.realm.beingStats.geneticDiversity = calculateGeneticDiversity(aliveBings);
		}
	}

	/**
	 * Check if it's time to transition to next epoch
	 */
	private checkEpochTransition() {
		const ticksSinceEpochStart = this.realm.currentTick - this.realm.currentEpoch.startTick;

		if (ticksSinceEpochStart >= this.realm.config.ticksPerEpoch) {
			this.transitionEpoch();
		}
	}

	/**
	 * Transition to next epoch
	 */
	private transitionEpoch() {
		// End current epoch
		this.realm.currentEpoch.endTick = this.realm.currentTick;

		// Create new epoch
		const epochIndex = this.realm.epochs.length;
		const epochTemplate = EPOCH_NAMES[Math.min(epochIndex, EPOCH_NAMES.length - 1)];

		const newEpoch: Epoch = {
			id: `epoch-${epochIndex}`,
			name: epochTemplate.name,
			startTick: this.realm.currentTick,
			description: epochTemplate.description,
			events: []
		};

		this.realm.epochs.push(newEpoch);
		this.realm.currentEpoch = newEpoch;

		this.recordEvent({
			tick: this.realm.currentTick,
			type: 'breakthrough',
			description: `New epoch begins: ${newEpoch.name}`,
			significance: 'critical'
		});
	}

	/**
	 * Supreme being intervenes based on temperament
	 */
	private divineIntervention() {
		const supreme = this.realm.config.supremeBeing;

		if (Math.random() > supreme.interventionRate / 1000) return;

		// Intervention: boost beings with favored trait
		const aliveBings = this.realm.beings.filter(b => b.alive);
		const favoredTrait = supreme.favoredTrait;

		for (const being of aliveBings) {
			if (being.genome[favoredTrait] > 0.7) {
				being.fitness += 0.1;
				being.energy += 0.1;
				being.energy = Math.min(1, being.energy);
			}
		}

		this.recordEvent({
			tick: this.realm.currentTick,
			type: 'intervention',
			description: `${supreme.name} intervenes, blessing beings with high ${favoredTrait}`,
			significance: 'major'
		});
	}

	/**
	 * Record historical event
	 */
	private recordEvent(event: HistoricalEvent) {
		this.realm.events.push(event);
		this.realm.currentEpoch.events.push(event);

		// Keep only recent minor events to prevent memory bloat
		if (this.realm.events.length > 1000) {
			this.realm.events = this.realm.events.filter(
				e => e.significance !== 'minor' || e.tick > this.realm.currentTick - 500
			);
		}
	}

	/**
	 * Get current realm state
	 */
	getRealm(): Realm {
		return this.realm;
	}

	/**
	 * Add component to realm (user drops component)
	 */
	addComponent(component: RealmComponent) {
		this.realm.components.push(component);
		this.recordEvent({
			tick: this.realm.currentTick,
			type: 'component_drop',
			description: `New component introduced: ${component.name}`,
			componentId: component.id,
			significance: 'major'
		});
	}

	/**
	 * Remove component from realm
	 */
	removeComponent(componentId: string) {
		this.realm.components = this.realm.components.filter(c => c.id !== componentId);
	}
}

/**
 * Initialize population with genetic diversity
 */
export function initializePopulation(
	realm: Realm,
	count: number,
	width: number,
	height: number
): Being[] {
	const beings: Being[] = [];

	for (let i = 0; i < count; i++) {
		const being = createBeing(
			`being-0-${i}`,
			Math.random() * width,
			Math.random() * height,
			0,
			generateRandomGenome()
		);

		beings.push(being);
	}

	return beings;
}
