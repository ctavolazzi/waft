import { describe, it, expect } from 'vitest';
import {
	createRealm,
	serializeRealm,
	deserializeRealm,
	SUPREME_BEINGS,
	PRIME_DIRECTIVES,
	EPOCH_NAMES
} from './Realm';

describe('Realm', () => {
	describe('createRealm', () => {
		it('creates a realm with provided configuration', () => {
			const config = {
				name: 'Test Realm',
				description: 'A test realm',
				initialPopulation: 20,
				worldWidth: 1000,
				worldHeight: 800,
				ticksPerEpoch: 500,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			};

			const realm = createRealm(config);

			expect(realm.config).toEqual(config);
			expect(realm.id).toBeDefined();
			expect(realm.id).toContain('realm-');
		});

		it('initializes with empty beings array', () => {
			const realm = createRealm({
				name: 'Test',
				description: 'Test',
				initialPopulation: 10,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 1000,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			expect(realm.beings).toHaveLength(0);
		});

		it('initializes beingStats with initial population count', () => {
			const realm = createRealm({
				name: 'Test',
				description: 'Test',
				initialPopulation: 15,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 1000,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			expect(realm.beingStats.totalBirths).toBe(15);
			expect(realm.beingStats.currentPopulation).toBe(15);
			expect(realm.beingStats.totalDeaths).toBe(0);
		});

		it('starts at tick 0', () => {
			const realm = createRealm({
				name: 'Test',
				description: 'Test',
				initialPopulation: 10,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 1000,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			expect(realm.currentTick).toBe(0);
		});

		it('creates first epoch', () => {
			const realm = createRealm({
				name: 'Test',
				description: 'Test',
				initialPopulation: 10,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 1000,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			expect(realm.epochs).toHaveLength(1);
			expect(realm.currentEpoch.name).toBe('Primordial Emergence');
			expect(realm.currentEpoch.startTick).toBe(0);
		});

		it('is not running by default', () => {
			const realm = createRealm({
				name: 'Test',
				description: 'Test',
				initialPopulation: 10,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 1000,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			expect(realm.running).toBe(false);
		});

		it('has default tick rate of 10', () => {
			const realm = createRealm({
				name: 'Test',
				description: 'Test',
				initialPopulation: 10,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 1000,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			expect(realm.tickRate).toBe(10);
		});

		it('initializes empty components array', () => {
			const realm = createRealm({
				name: 'Test',
				description: 'Test',
				initialPopulation: 10,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 1000,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			expect(realm.components).toHaveLength(0);
		});

		it('creates initial creation event', () => {
			const realm = createRealm({
				name: 'Test',
				description: 'Test',
				initialPopulation: 10,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 1000,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			expect(realm.events).toHaveLength(1);
			expect(realm.events[0].type).toBe('birth');
			expect(realm.events[0].significance).toBe('critical');
		});

		it('initializes ancestral lineages map', () => {
			const realm = createRealm({
				name: 'Test',
				description: 'Test',
				initialPopulation: 10,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 1000,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			expect(realm.ancestralLineages).toBeInstanceOf(Map);
			expect(realm.ancestralLineages.size).toBe(0);
		});
	});

	describe('serializeRealm', () => {
		it('serializes realm to JSON string', () => {
			const realm = createRealm({
				name: 'Test',
				description: 'Test',
				initialPopulation: 5,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 1000,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			const serialized = serializeRealm(realm);

			expect(typeof serialized).toBe('string');
			expect(() => JSON.parse(serialized)).not.toThrow();
		});

		it('includes ancestral lineages as array', () => {
			const realm = createRealm({
				name: 'Test',
				description: 'Test',
				initialPopulation: 5,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 1000,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			realm.ancestralLineages.set('being-1', ['ancestor-1', 'ancestor-2']);

			const serialized = serializeRealm(realm);
			const parsed = JSON.parse(serialized);

			expect(Array.isArray(parsed.ancestralLineages)).toBe(true);
			expect(parsed.ancestralLineages).toHaveLength(1);
		});

		it('preserves all realm properties', () => {
			const realm = createRealm({
				name: 'Test Realm',
				description: 'Test Description',
				initialPopulation: 5,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 1000,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			const serialized = serializeRealm(realm);
			const parsed = JSON.parse(serialized);

			expect(parsed.config.name).toBe('Test Realm');
			expect(parsed.config.description).toBe('Test Description');
			expect(parsed.currentTick).toBe(0);
			expect(parsed.running).toBe(false);
		});
	});

	describe('deserializeRealm', () => {
		it('deserializes JSON string to realm', () => {
			const realm = createRealm({
				name: 'Test',
				description: 'Test',
				initialPopulation: 5,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 1000,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			const serialized = serializeRealm(realm);
			const deserialized = deserializeRealm(serialized);

			expect(deserialized.id).toBe(realm.id);
			expect(deserialized.config.name).toBe(realm.config.name);
		});

		it('restores ancestral lineages as Map', () => {
			const realm = createRealm({
				name: 'Test',
				description: 'Test',
				initialPopulation: 5,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 1000,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			realm.ancestralLineages.set('being-1', ['ancestor-1', 'ancestor-2']);
			realm.ancestralLineages.set('being-2', ['ancestor-3']);

			const serialized = serializeRealm(realm);
			const deserialized = deserializeRealm(serialized);

			expect(deserialized.ancestralLineages).toBeInstanceOf(Map);
			expect(deserialized.ancestralLineages.size).toBe(2);
			expect(deserialized.ancestralLineages.get('being-1')).toEqual(['ancestor-1', 'ancestor-2']);
		});

		it('round-trips correctly', () => {
			const realm = createRealm({
				name: 'Test',
				description: 'Test',
				initialPopulation: 5,
				worldWidth: 800,
				worldHeight: 600,
				ticksPerEpoch: 1000,
				supremeBeing: SUPREME_BEINGS[0],
				primeDirective: PRIME_DIRECTIVES.harmony
			});

			realm.currentTick = 100;
			realm.running = true;
			realm.ancestralLineages.set('being-1', ['ancestor-1']);

			const serialized = serializeRealm(realm);
			const deserialized = deserializeRealm(serialized);

			expect(deserialized.currentTick).toBe(100);
			expect(deserialized.running).toBe(true);
			expect(deserialized.ancestralLineages.get('being-1')).toEqual(['ancestor-1']);
		});
	});

	describe('SUPREME_BEINGS', () => {
		it('has 5 predefined supreme beings', () => {
			expect(SUPREME_BEINGS).toHaveLength(5);
		});

		it('all have required properties', () => {
			SUPREME_BEINGS.forEach(being => {
				expect(being.name).toBeDefined();
				expect(being.domain).toBeDefined();
				expect(being.temperament).toBeDefined();
				expect(typeof being.interventionRate).toBe('number');
				expect(being.favoredTrait).toBeDefined();
			});
		});

		it('has Harmonia as first being', () => {
			expect(SUPREME_BEINGS[0].name).toBe('Harmonia');
			expect(SUPREME_BEINGS[0].favoredTrait).toBe('cooperation');
		});

		it('has varied intervention rates', () => {
			const rates = SUPREME_BEINGS.map(b => b.interventionRate);
			const uniqueRates = new Set(rates);
			expect(uniqueRates.size).toBeGreaterThan(1);
		});
	});

	describe('PRIME_DIRECTIVES', () => {
		it('has multiple directives', () => {
			const directiveCount = Object.keys(PRIME_DIRECTIVES).length;
			expect(directiveCount).toBeGreaterThan(0);
		});

		it('all have required properties', () => {
			Object.values(PRIME_DIRECTIVES).forEach(directive => {
				expect(directive.goal).toBeDefined();
				expect(directive.description).toBeDefined();
				expect(directive.fitnessWeights).toBeDefined();
				expect(directive.fitnessWeights.longevity).toBeDefined();
				expect(directive.fitnessWeights.energy).toBeDefined();
				expect(directive.fitnessWeights.cooperation).toBeDefined();
				expect(directive.fitnessWeights.curiosity).toBeDefined();
				expect(directive.fitnessWeights.reproduction).toBeDefined();
			});
		});

		it('harmony directive favors cooperation', () => {
			const harmony = PRIME_DIRECTIVES.harmony;
			expect(harmony.fitnessWeights.cooperation).toBeGreaterThan(0.3);
		});

		it('survival directive favors longevity and energy', () => {
			const survival = PRIME_DIRECTIVES.survival;
			expect(survival.fitnessWeights.longevity).toBeGreaterThan(0.2);
			expect(survival.fitnessWeights.energy).toBeGreaterThan(0.2);
		});

		it('curiosity directive favors curiosity', () => {
			const curiosity = PRIME_DIRECTIVES.curiosity;
			expect(curiosity.fitnessWeights.curiosity).toBeGreaterThan(0.3);
		});

		it('diversity directive balances all weights', () => {
			const diversity = PRIME_DIRECTIVES.diversity;
			const weights = Object.values(diversity.fitnessWeights);
			const allEqual = weights.every(w => w === weights[0]);
			expect(allEqual).toBe(true);
		});
	});

	describe('EPOCH_NAMES', () => {
		it('has 10 epoch names', () => {
			expect(EPOCH_NAMES).toHaveLength(10);
		});

		it('all have name and description', () => {
			EPOCH_NAMES.forEach(epoch => {
				expect(epoch.name).toBeDefined();
				expect(epoch.description).toBeDefined();
			});
		});

		it('starts with Primordial Emergence', () => {
			expect(EPOCH_NAMES[0].name).toBe('Primordial Emergence');
		});

		it('ends with Singularity Horizon', () => {
			expect(EPOCH_NAMES[9].name).toBe('Singularity Horizon');
		});

		it('has unique epoch names', () => {
			const names = EPOCH_NAMES.map(e => e.name);
			const uniqueNames = new Set(names);
			expect(uniqueNames.size).toBe(names.length);
		});
	});
});
