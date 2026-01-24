import { describe, it, expect } from 'vitest';
import {
	createBeing,
	generateRandomGenome,
	crossover,
	mutate,
	calculateFitness,
	calculateGeneticDiversity,
	type Being,
	type Genome
} from './Being';

describe('Being', () => {
	describe('generateRandomGenome', () => {
		it('generates a genome with all traits between 0 and 1', () => {
			const genome = generateRandomGenome();

			expect(genome.curiosity).toBeGreaterThanOrEqual(0);
			expect(genome.curiosity).toBeLessThanOrEqual(1);
			expect(genome.caution).toBeGreaterThanOrEqual(0);
			expect(genome.cooperation).toBeGreaterThanOrEqual(0);
			expect(genome.energy).toBeGreaterThanOrEqual(0);
			expect(genome.speed).toBeGreaterThanOrEqual(0);
			expect(genome.perception).toBeGreaterThanOrEqual(0);
			expect(genome.adaptability).toBeGreaterThanOrEqual(0);
			expect(genome.longevity).toBeGreaterThanOrEqual(0);
			expect(genome.fertility).toBeGreaterThanOrEqual(0);
		});

		it('generates mutation rate between 0.01 and 0.1', () => {
			const genome = generateRandomGenome();
			expect(genome.mutationRate).toBeGreaterThanOrEqual(0.01);
			expect(genome.mutationRate).toBeLessThanOrEqual(0.1);
		});
	});

	describe('createBeing', () => {
		it('creates a being with provided parameters', () => {
			const being = createBeing('test-1', 100, 200, 0);

			expect(being.id).toBe('test-1');
			expect(being.x).toBe(100);
			expect(being.y).toBe(200);
			expect(being.generation).toBe(0);
			expect(being.alive).toBe(true);
			expect(being.fitness).toBe(0.5);
		});

		it('creates a being with custom genome', () => {
			const customGenome: Genome = {
				curiosity: 0.9,
				caution: 0.1,
				cooperation: 0.8,
				energy: 0.7,
				speed: 0.6,
				perception: 0.5,
				adaptability: 0.4,
				longevity: 0.3,
				fertility: 0.2,
				mutationRate: 0.05
			};

			const being = createBeing('test-2', 0, 0, 0, customGenome);

			expect(being.genome.curiosity).toBe(0.9);
			expect(being.genome.caution).toBe(0.1);
		});

		it('calculates max age based on longevity', () => {
			const lowLongevity: Genome = {
				...generateRandomGenome(),
				longevity: 0
			};

			const highLongevity: Genome = {
				...generateRandomGenome(),
				longevity: 1
			};

			const being1 = createBeing('low', 0, 0, 0, lowLongevity);
			const being2 = createBeing('high', 0, 0, 0, highLongevity);

			expect(being2.maxAge).toBeGreaterThan(being1.maxAge);
		});
	});

	describe('crossover', () => {
		it('creates offspring genome from two parents', () => {
			const parent1: Genome = {
				curiosity: 1.0,
				caution: 0.0,
				cooperation: 1.0,
				energy: 0.0,
				speed: 1.0,
				perception: 0.0,
				adaptability: 1.0,
				longevity: 0.0,
				fertility: 1.0,
				mutationRate: 0.05
			};

			const parent2: Genome = {
				curiosity: 0.0,
				caution: 1.0,
				cooperation: 0.0,
				energy: 1.0,
				speed: 0.0,
				perception: 1.0,
				adaptability: 0.0,
				longevity: 1.0,
				fertility: 0.0,
				mutationRate: 0.05
			};

			const offspring = crossover(parent1, parent2);

			// Each trait should be from one parent or the other
			expect([0.0, 1.0]).toContain(offspring.curiosity);
			expect([0.0, 1.0]).toContain(offspring.caution);
		});
	});

	describe('mutate', () => {
		it('mutates genome based on mutation rate', () => {
			const original: Genome = {
				curiosity: 0.5,
				caution: 0.5,
				cooperation: 0.5,
				energy: 0.5,
				speed: 0.5,
				perception: 0.5,
				adaptability: 0.5,
				longevity: 0.5,
				fertility: 0.5,
				mutationRate: 1.0 // 100% mutation rate for testing
			};

			const mutated = mutate(original);

			// At least one trait should be different
			const changed =
				mutated.curiosity !== original.curiosity ||
				mutated.caution !== original.caution ||
				mutated.cooperation !== original.cooperation;

			expect(changed).toBe(true);
		});

		it('keeps mutated values between 0 and 1', () => {
			const genome = generateRandomGenome();
			const mutated = mutate(genome);

			expect(mutated.curiosity).toBeGreaterThanOrEqual(0);
			expect(mutated.curiosity).toBeLessThanOrEqual(1);
		});
	});

	describe('calculateFitness', () => {
		it('calculates base fitness of 0.5 for new being', () => {
			const being = createBeing('test', 0, 0, 0);
			being.energy = 0; // Set to 0 to test base fitness only
			being.age = 0;

			const fitness = calculateFitness(being, 0);

			expect(fitness).toBeCloseTo(0.5, 1);
		});

		it('increases fitness for older beings', () => {
			const being = createBeing('test', 0, 0, 0);
			being.age = 500; // Half of max age
			being.maxAge = 1000;

			const fitness = calculateFitness(being, 0);

			expect(fitness).toBeGreaterThan(0.5);
		});

		it('increases fitness for high energy beings', () => {
			const being = createBeing('test', 0, 0, 0);
			being.energy = 1.0;

			const fitness = calculateFitness(being, 0);

			expect(fitness).toBeGreaterThan(0.5);
		});

		it('increases fitness for cooperative beings in swarms', () => {
			const being = createBeing('test', 0, 0, 0);
			being.cooperatingWith = ['other1', 'other2', 'other3'];

			const fitness = calculateFitness(being, 0);

			expect(fitness).toBeGreaterThan(0.5);
		});

		it('caps fitness at 1.0', () => {
			const being = createBeing('test', 0, 0, 0);
			being.age = 3000;
			being.maxAge = 1000;
			being.energy = 1.0;
			being.cooperatingWith = Array(20).fill('other');
			being.investigating = 'component';
			being.childrenIds = Array(10).fill('child');

			const fitness = calculateFitness(being, 0);

			expect(fitness).toBeLessThanOrEqual(1.0);
		});
	});

	describe('calculateGeneticDiversity', () => {
		it('returns 0 for empty population', () => {
			const diversity = calculateGeneticDiversity([]);
			expect(diversity).toBe(0);
		});

		it('returns 0 for identical clones', () => {
			const genome = generateRandomGenome();
			const beings = [
				createBeing('1', 0, 0, 0, genome),
				createBeing('2', 0, 0, 0, genome),
				createBeing('3', 0, 0, 0, genome)
			];

			const diversity = calculateGeneticDiversity(beings);
			expect(diversity).toBeCloseTo(0, 5); // Use toBeCloseTo for floating point comparison
		});

		it('returns > 0 for diverse population', () => {
			const beings = [
				createBeing('1', 0, 0, 0),
				createBeing('2', 0, 0, 0),
				createBeing('3', 0, 0, 0)
			];

			const diversity = calculateGeneticDiversity(beings);
			expect(diversity).toBeGreaterThan(0);
		});
	});
});
