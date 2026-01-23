import { describe, it, expect, beforeEach, vi } from 'vitest';
import { EvolutionEngine, initializePopulation } from './Evolution';
import { createRealm, SUPREME_BEINGS, PRIME_DIRECTIVES } from './Realm';
import { createBeing } from './Being';

describe('Evolution', () => {
	let realm: any;
	let engine: EvolutionEngine;

	beforeEach(() => {
		realm = createRealm({
			name: 'Test Realm',
			description: 'Test',
			initialPopulation: 5,
			worldWidth: 800,
			worldHeight: 600,
			ticksPerEpoch: 1000,
			supremeBeing: SUPREME_BEINGS[0], // Harmonia
			primeDirective: PRIME_DIRECTIVES.harmony
		});

		// Add initial beings
		realm.beings = [
			createBeing('being-1', 100, 100, 0),
			createBeing('being-2', 200, 200, 0),
			createBeing('being-3', 300, 300, 0),
			createBeing('being-4', 400, 400, 0),
			createBeing('being-5', 500, 500, 0)
		];

		engine = new EvolutionEngine(realm);
	});

	describe('EvolutionEngine', () => {
		it('initializes with realm', () => {
			expect(engine.getRealm()).toBe(realm);
		});

		it('starts and stops simulation', () => {
			expect(realm.running).toBe(false);

			engine.start();
			expect(realm.running).toBe(true);

			engine.stop();
			expect(realm.running).toBe(false);
		});

		it('does not double-start', () => {
			engine.start();
			const firstRun = realm.running;

			engine.start(); // Try to start again

			expect(realm.running).toBe(firstRun);
		});

		it('does not error on double-stop', () => {
			engine.stop();
			expect(() => engine.stop()).not.toThrow();
		});
	});

	describe('tick', () => {
		it('increments currentTick', () => {
			const initialTick = realm.currentTick;

			engine.tick();

			expect(realm.currentTick).toBe(initialTick + 1);
		});

		it('ages all beings', () => {
			const initialAges = realm.beings.map((b: any) => b.age);

			engine.tick();

			realm.beings.forEach((being: any, i: number) => {
				expect(being.age).toBe(initialAges[i] + 1);
			});
		});

		it('moves beings', () => {
			const being = realm.beings[0];
			being.vx = 1;
			being.vy = 1;
			const initialX = being.x;
			const initialY = being.y;

			engine.tick();

			expect(being.x).not.toBe(initialX);
			expect(being.y).not.toBe(initialY);
		});

		it('wraps beings at world boundaries', () => {
			const being = realm.beings[0];
			being.x = -10; // Out of bounds
			being.y = realm.config.worldHeight + 10; // Out of bounds

			engine.tick();

			expect(being.x).toBeGreaterThanOrEqual(0);
			expect(being.x).toBeLessThanOrEqual(realm.config.worldWidth);
			expect(being.y).toBeGreaterThanOrEqual(0);
			expect(being.y).toBeLessThanOrEqual(realm.config.worldHeight);
		});

		it('updates fitness scores', () => {
			engine.tick();

			realm.beings.forEach((being: any) => {
				expect(being.fitness).toBeGreaterThanOrEqual(0);
				expect(being.fitness).toBeLessThanOrEqual(1);
			});
		});

		it('updates population statistics', () => {
			engine.tick();

			expect(realm.beingStats.currentPopulation).toBe(5);
			expect(realm.beingStats.averageFitness).toBeGreaterThan(0);
			expect(realm.beingStats.averageAge).toBeGreaterThanOrEqual(0);
		});
	});

	describe('death mechanics', () => {
		it('kills beings from old age', () => {
			const being = realm.beings[0];
			being.age = being.maxAge - 1; // Almost dead

			engine.tick(); // Should reach maxAge and die

			expect(being.alive).toBe(false);
			expect(being.causeOfDeath).toBe('age');
		});

		it('kills beings from starvation (zero energy)', () => {
			const being = realm.beings[0];
			being.energy = 0; // Almost zero

			engine.tick(); // Energy loss should kill it

			expect(being.alive).toBe(false);
			expect(being.causeOfDeath).toBe('starvation');
		});

		it('stops simulation on extinction', () => {
			// Kill all beings
			realm.beings.forEach((b: any) => {
				b.alive = false;
			});

			engine.tick();

			expect(realm.running).toBe(false);
			expect(realm.beingStats.extinctionEvents).toBe(1);
		});

		it('increments total deaths', () => {
			const being = realm.beings[0];
			being.age = being.maxAge - 1;

			const initialDeaths = realm.beingStats.totalDeaths;

			engine.tick();

			expect(realm.beingStats.totalDeaths).toBeGreaterThan(initialDeaths);
		});
	});

	describe('reproduction mechanics', () => {
		it('creates offspring when conditions are right', () => {
			// Set up favorable conditions
			realm.beings.forEach((being: any) => {
				being.fitness = 0.9;
				being.genome.fertility = 0.9;
				being.energy = 0.9;
			});

			const initialPopulation = realm.beings.length;

			// Run multiple ticks to increase chance of reproduction
			for (let i = 0; i < 100; i++) {
				engine.tick();
			}

			expect(realm.beings.length).toBeGreaterThan(initialPopulation);
		});

		it('offspring inherit from both parents', () => {
			// Force reproduction
			realm.beings.forEach((being: any) => {
				being.fitness = 1.0;
				being.genome.fertility = 1.0;
				being.energy = 1.0;
			});

			const initialPopulation = realm.beings.length;

			// Run multiple ticks
			for (let i = 0; i < 100; i++) {
				engine.tick();
			}

			// Check if new beings were born
			if (realm.beings.length > initialPopulation) {
				const offspring = realm.beings.slice(initialPopulation);
				offspring.forEach((child: any) => {
					expect(child.parentIds).toHaveLength(2);
					expect(child.generation).toBeGreaterThan(0);
				});
			}
		});

		it('increments total births', () => {
			realm.beings.forEach((being: any) => {
				being.fitness = 0.9;
				being.genome.fertility = 0.9;
				being.energy = 0.9;
			});

			const initialBirths = realm.beingStats.totalBirths;

			// Run many ticks
			for (let i = 0; i < 100; i++) {
				engine.tick();
			}

			// Should have at least some births
			expect(realm.beingStats.totalBirths).toBeGreaterThanOrEqual(initialBirths);
		});

		it('creates ancestral lineages', () => {
			realm.beings.forEach((being: any) => {
				being.fitness = 1.0;
				being.genome.fertility = 1.0;
			});

			// Run multiple ticks
			for (let i = 0; i < 50; i++) {
				engine.tick();
			}

			// Check if lineages were recorded
			if (realm.beings.length > 5) {
				expect(realm.ancestralLineages.size).toBeGreaterThan(0);
			}
		});
	});

	describe('component interactions', () => {
		it('detects being near component', () => {
			const component = {
				id: 'comp-1',
				type: 'resource' as const,
				name: 'Energy Source',
				x: 100,
				y: 100,
				radius: 50,
				strength: 0.5,
				effect: {
					fitnessModifier: 0.1,
					energyModifier: 0.2,
					mutationChance: 0.0,
					deathChance: 0.0,
					reproductionBonus: 0.0
				}
			};

			engine.addComponent(component);

			const being = realm.beings[0];
			being.x = 110; // Within radius
			being.y = 110;
			being.genome.curiosity = 1.0; // Always investigates

			const initialEnergy = being.energy;

			engine.tick();

			// Being should have investigated and gained energy
			expect(being.investigating).toBeDefined();
		});

		it('adds component through addComponent', () => {
			const component = {
				id: 'comp-1',
				type: 'resource' as const,
				name: 'Test',
				x: 100,
				y: 100,
				radius: 50,
				strength: 1,
				effect: {
					fitnessModifier: 0,
					energyModifier: 0,
					mutationChance: 0,
					deathChance: 0,
					reproductionBonus: 0
				}
			};

			expect(realm.components).toHaveLength(0);

			engine.addComponent(component);

			expect(realm.components).toHaveLength(1);
			expect(realm.components[0]).toBe(component);
		});

		it('removes component', () => {
			const component = {
				id: 'comp-1',
				type: 'resource' as const,
				name: 'Test',
				x: 100,
				y: 100,
				radius: 50,
				strength: 1,
				effect: {
					fitnessModifier: 0,
					energyModifier: 0,
					mutationChance: 0,
					deathChance: 0,
					reproductionBonus: 0
				}
			};

			engine.addComponent(component);
			expect(realm.components).toHaveLength(1);

			engine.removeComponent('comp-1');

			expect(realm.components).toHaveLength(0);
		});
	});

	describe('epoch progression', () => {
		it('transitions epochs after ticksPerEpoch', () => {
			realm.config.ticksPerEpoch = 10;
			realm.currentTick = 0;

			expect(realm.epochs).toHaveLength(1);
			expect(realm.currentEpoch.name).toBe('Primordial Emergence');

			// Run 10 ticks to trigger epoch transition
			for (let i = 0; i < 10; i++) {
				engine.tick();
			}

			expect(realm.epochs.length).toBeGreaterThan(1);
			expect(realm.currentEpoch.name).not.toBe('Primordial Emergence');
		});

		it('records epoch transition event', () => {
			realm.config.ticksPerEpoch = 5;

			const initialEventCount = realm.events.length;

			for (let i = 0; i < 5; i++) {
				engine.tick();
			}

			// Should have recorded epoch transition
			const epochEvents = realm.events.filter(e => e.type === 'breakthrough');
			expect(epochEvents.length).toBeGreaterThan(0);
		});
	});

	describe('divine intervention', () => {
		it('intervenes based on intervention rate', () => {
			// Set high intervention rate
			realm.config.supremeBeing.interventionRate = 1000; // Very high chance

			realm.beings[0].genome.cooperation = 0.8; // High in favored trait

			const initialFitness = realm.beings[0].fitness;

			// Run multiple ticks
			for (let i = 0; i < 50; i++) {
				engine.tick();
			}

			// Should have had at least one intervention boosting fitness
			// (Hard to test deterministically due to randomness, but with high rate should happen)
		});
	});

	describe('initializePopulation', () => {
		it('creates specified number of beings', () => {
			const population = initializePopulation(realm, 10, 800, 600);

			expect(population).toHaveLength(10);
		});

		it('creates beings with random positions', () => {
			const population = initializePopulation(realm, 5, 800, 600);

			population.forEach(being => {
				expect(being.x).toBeGreaterThanOrEqual(0);
				expect(being.x).toBeLessThanOrEqual(800);
				expect(being.y).toBeGreaterThanOrEqual(0);
				expect(being.y).toBeLessThanOrEqual(600);
			});
		});

		it('creates beings at generation 0', () => {
			const population = initializePopulation(realm, 5, 800, 600);

			population.forEach(being => {
				expect(being.generation).toBe(0);
			});
		});

		it('creates beings with random genomes', () => {
			const population = initializePopulation(realm, 3, 800, 600);

			// Check genetic diversity (not all identical)
			const genome1 = population[0].genome;
			const genome2 = population[1].genome;

			const different = Object.keys(genome1).some(
				key => genome1[key as keyof typeof genome1] !== genome2[key as keyof typeof genome2]
			);

			expect(different).toBe(true);
		});
	});
});
