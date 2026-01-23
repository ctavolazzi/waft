/**
 * Being - Individual evolutionary entity with genetics and behavior
 *
 * Each being has:
 * - Genetic code that determines traits
 * - Fitness score based on survival and reproduction
 * - Lineage tracking for evolutionary history
 * - Behavioral tendencies that emerge from genetics
 */

export interface Genome {
	// Core traits (0.0 - 1.0 normalized)
	curiosity: number;        // How likely to investigate new components
	caution: number;          // How much to avoid danger
	cooperation: number;      // Tendency to swarm with others
	energy: number;           // Base metabolic rate
	speed: number;            // Movement velocity
	perception: number;       // Detection radius for components

	// Advanced traits
	adaptability: number;     // Mutation tolerance
	longevity: number;        // Lifespan multiplier
	fertility: number;        // Reproduction rate

	// Mutation rate
	mutationRate: number;     // How much genes change per generation
}

export interface Being {
	id: string;
	generation: number;

	// Position and movement
	x: number;
	y: number;
	vx: number;
	vy: number;

	// Genetics
	genome: Genome;

	// Life stats
	fitness: number;          // Current fitness score (0.0 - 1.0)
	age: number;              // Age in ticks
	maxAge: number;           // Maximum lifespan in ticks
	energy: number;           // Current energy (0.0 - 1.0)

	// State
	alive: boolean;
	causeOfDeath?: string;    // "starvation" | "age" | "component" | "mutation"

	// Lineage
	parentIds: string[];      // IDs of parent beings
	childrenIds: string[];    // IDs of offspring

	// Behavior
	investigating?: string;   // ID of component being investigated
	cooperatingWith: string[]; // IDs of beings in current swarm

	// Appearance
	color: string;            // Visual color (derived from genes)
	size: number;             // Visual size (derived from genes)
}

export interface BeingStats {
	totalBirths: number;
	totalDeaths: number;
	currentPopulation: number;
	averageFitness: number;
	averageAge: number;
	geneticDiversity: number; // Shannon entropy of gene pool
	extinctionEvents: number;
}

/**
 * Generate a random genome with genetic diversity
 */
export function generateRandomGenome(): Genome {
	return {
		curiosity: Math.random(),
		caution: Math.random(),
		cooperation: Math.random(),
		energy: 0.3 + Math.random() * 0.5, // Bias toward middle
		speed: 0.3 + Math.random() * 0.5,
		perception: 0.3 + Math.random() * 0.5,
		adaptability: Math.random(),
		longevity: 0.5 + Math.random() * 0.5, // Bias toward longer life
		fertility: Math.random(),
		mutationRate: 0.01 + Math.random() * 0.09 // 1-10% mutation rate
	};
}

/**
 * Create a new being with random genetics
 */
export function createBeing(
	id: string,
	x: number,
	y: number,
	generation: number = 0,
	genome?: Genome
): Being {
	const actualGenome = genome || generateRandomGenome();

	return {
		id,
		generation,
		x,
		y,
		vx: (Math.random() - 0.5) * actualGenome.speed * 2,
		vy: (Math.random() - 0.5) * actualGenome.speed * 2,
		genome: actualGenome,
		fitness: 0.5, // Start neutral
		age: 0,
		maxAge: 1000 + actualGenome.longevity * 2000, // 1000-3000 ticks
		energy: actualGenome.energy,
		alive: true,
		parentIds: [],
		childrenIds: [],
		cooperatingWith: [],
		color: genomeToColor(actualGenome),
		size: 2 + actualGenome.energy * 2 // 2-4px
	};
}

/**
 * Crossover two parent genomes to create offspring genome
 */
export function crossover(parent1: Genome, parent2: Genome): Genome {
	const child: Genome = {} as Genome;

	// For each gene, randomly inherit from one parent
	for (const key in parent1) {
		const gene = key as keyof Genome;
		child[gene] = Math.random() < 0.5 ? parent1[gene] : parent2[gene];
	}

	return child;
}

/**
 * Mutate a genome based on mutation rate
 */
export function mutate(genome: Genome): Genome {
	const mutated = { ...genome };
	const mutationRate = genome.mutationRate;

	for (const key in mutated) {
		const gene = key as keyof Genome;

		if (Math.random() < mutationRate) {
			// Mutate this gene by +/- 20%
			const delta = (Math.random() - 0.5) * 0.4;
			mutated[gene] = Math.max(0, Math.min(1, mutated[gene] + delta));
		}
	}

	return mutated;
}

/**
 * Calculate fitness based on being's life performance
 */
export function calculateFitness(being: Being, epoch: number): number {
	let fitness = 0.5; // Base fitness

	// Longevity bonus (survived longer = fitter)
	const ageRatio = being.age / being.maxAge;
	fitness += ageRatio * 0.2;

	// Energy level (well-fed = fitter)
	fitness += being.energy * 0.2;

	// Cooperation bonus (swarms survive better)
	fitness += (being.cooperatingWith.length / 10) * 0.1;

	// Investigation bonus (curious beings discover more)
	if (being.investigating) {
		fitness += 0.1;
	}

	// Reproduction bonus (having children = evolutionary success)
	fitness += Math.min(being.childrenIds.length * 0.05, 0.2);

	return Math.max(0, Math.min(1, fitness));
}

/**
 * Convert genome to visual color
 */
function genomeToColor(genome: Genome): string {
	// Map genetics to HSL color
	const hue = genome.curiosity * 180 + genome.cooperation * 180; // 0-360
	const saturation = 50 + genome.energy * 50; // 50-100%
	const lightness = 40 + genome.speed * 20; // 40-60%

	return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
}

/**
 * Calculate genetic diversity using Shannon entropy
 */
export function calculateGeneticDiversity(beings: Being[]): number {
	if (beings.length === 0) return 0;

	// Simplified: average variance across all genes
	const genes: (keyof Genome)[] = [
		'curiosity', 'caution', 'cooperation', 'energy',
		'speed', 'perception', 'adaptability', 'longevity', 'fertility'
	];

	let totalVariance = 0;

	for (const gene of genes) {
		const values = beings.map(b => b.genome[gene]);
		const mean = values.reduce((a, b) => a + b, 0) / values.length;
		const variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length;
		totalVariance += variance;
	}

	return totalVariance / genes.length;
}
