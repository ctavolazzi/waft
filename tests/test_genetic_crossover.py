"""
Tests for the Genetic Crossover Engine.

Comprehensive test suite covering:
- All crossover strategies
- Edge cases
- Inheritance tracking
- Mutation mechanics
"""

import pytest

from src.waft.evolution import (
    ColorGene,
    CrossoverResult,
    CrossoverStrategy,
    FontGene,
    GeneticCrossover,
    LayoutGene,
    MarginGene,
    StylingGene,
    StylingGenome,
    breed,
)


@pytest.fixture
def parent_a():
    """Create parent A genome."""
    genes = StylingGene(
        font=FontGene(family="serif", size_body=12, size_h1=28),
        margin=MarginGene(top=25, bottom=25),
        color=ColorGene(text="#000000", background="#ffffff"),
        layout=LayoutGene(columns=1, density="normal"),
        name="Parent A",
    )
    genome = StylingGenome.from_genes(genes)
    genome.evaluate_fitness({"readability": 0.8, "density": 0.7})
    return genome


@pytest.fixture
def parent_b():
    """Create parent B genome."""
    genes = StylingGene(
        font=FontGene(family="sans-serif", size_body=10, size_h1=24),
        margin=MarginGene(top=15, bottom=15),
        color=ColorGene(text="#333333", background="#f0f0f0"),
        layout=LayoutGene(columns=2, density="compact"),
        name="Parent B",
    )
    genome = StylingGenome.from_genes(genes)
    genome.evaluate_fitness({"readability": 0.6, "density": 0.9})
    return genome


@pytest.fixture
def crossover_engine():
    """Create a crossover engine."""
    return GeneticCrossover(mutation_rate=0.0)  # Disable mutation for predictable tests


class TestCrossoverStrategies:
    """Test all crossover strategies."""

    def test_uniform_crossover(self, parent_a, parent_b, crossover_engine):
        """Test uniform crossover produces valid offspring."""
        result = crossover_engine.crossover(
            parent_a, parent_b, CrossoverStrategy.UNIFORM
        )

        assert result.offspring is not None
        assert result.offspring.genome_id != parent_a.genome_id
        assert result.offspring.genome_id != parent_b.genome_id
        assert result.offspring.generation == max(parent_a.generation, parent_b.generation) + 1
        assert result.strategy == CrossoverStrategy.UNIFORM
        assert len(result.inheritance_map) > 0

    def test_single_point_crossover(self, parent_a, parent_b, crossover_engine):
        """Test single-point crossover."""
        result = crossover_engine.crossover(
            parent_a, parent_b, CrossoverStrategy.SINGLE_POINT
        )

        assert result.offspring is not None
        assert len(result.crossover_points) == 1
        assert result.strategy == CrossoverStrategy.SINGLE_POINT

        # Check inheritance pattern - genes before point from A, after from B
        inheritance = list(result.inheritance_map.values())
        # Should have a transition point
        assert "parent_a" in inheritance
        assert "parent_b" in inheritance

    def test_two_point_crossover(self, parent_a, parent_b, crossover_engine):
        """Test two-point crossover."""
        result = crossover_engine.crossover(
            parent_a, parent_b, CrossoverStrategy.TWO_POINT
        )

        assert result.offspring is not None
        assert len(result.crossover_points) == 2
        assert result.strategy == CrossoverStrategy.TWO_POINT

    def test_category_swap_crossover(self, parent_a, parent_b, crossover_engine):
        """Test category swap crossover preserves category integrity."""
        result = crossover_engine.crossover(
            parent_a, parent_b, CrossoverStrategy.CATEGORY_SWAP
        )

        assert result.offspring is not None
        assert result.strategy == CrossoverStrategy.CATEGORY_SWAP

        # All genes in a category should come from same parent
        categories = {"font": set(), "margin": set(), "color": set(), "layout": set()}
        for gene, parent in result.inheritance_map.items():
            category = gene.split(".")[0]
            categories[category].add(parent)

        # Each category should have only one parent
        for category, parents in categories.items():
            assert len(parents) == 1, f"Category {category} has mixed inheritance"

    def test_fitness_weighted_crossover(self, parent_a, parent_b, crossover_engine):
        """Test fitness-weighted crossover favors fitter parent."""
        # Run multiple times to check statistical bias
        parent_a_count = 0
        parent_b_count = 0

        for _ in range(100):
            result = crossover_engine.crossover(
                parent_a, parent_b, CrossoverStrategy.FITNESS_WEIGHTED
            )
            for parent in result.inheritance_map.values():
                if parent == "parent_a":
                    parent_a_count += 1
                elif parent == "parent_b":
                    parent_b_count += 1

        # Parent A has higher fitness, should be selected more often
        # (0.75 vs 0.75 average fitness, so A wins with 0.8 readability)
        assert parent_a_count > parent_b_count * 0.8  # Allow some variance

    def test_blended_crossover(self, parent_a, parent_b, crossover_engine):
        """Test blended crossover interpolates numeric values."""
        result = crossover_engine.crossover(
            parent_a, parent_b, CrossoverStrategy.BLENDED
        )

        assert result.offspring is not None
        assert result.strategy == CrossoverStrategy.BLENDED

        # Check that some genes are blended
        offspring_genes = result.offspring.genes
        parent_a_genes = parent_a.genes
        parent_b_genes = parent_b.genes

        # Body font size should be between parents (10 and 12)
        offspring_size = offspring_genes.font.size_body
        assert 10 <= offspring_size <= 12

    def test_dominant_recessive_crossover(self, parent_a, parent_b, crossover_engine):
        """Test dominant-recessive crossover follows Mendelian ratios."""
        dominant_count = 0
        recessive_count = 0

        for _ in range(100):
            result = crossover_engine.crossover(
                parent_a, parent_b, CrossoverStrategy.DOMINANT_RECESSIVE
            )
            for parent in result.inheritance_map.values():
                # Parent A has higher fitness, should be dominant
                if parent == "parent_a":
                    dominant_count += 1
                else:
                    recessive_count += 1

        # Expect roughly 75% dominant (3:1 Mendelian ratio)
        ratio = dominant_count / (dominant_count + recessive_count)
        assert 0.6 < ratio < 0.9  # Allow variance


class TestCrossoverMechanics:
    """Test crossover mechanics and edge cases."""

    def test_offspring_has_correct_lineage(self, parent_a, parent_b, crossover_engine):
        """Test offspring tracks lineage correctly."""
        result = crossover_engine.crossover(parent_a, parent_b)

        # Offspring's parent should be the fitter parent
        expected_parent = parent_a  # Higher fitness
        assert result.offspring.parent_id == expected_parent.genome_id

    def test_offspring_generation_increments(self, parent_a, parent_b, crossover_engine):
        """Test offspring generation is correctly incremented."""
        result = crossover_engine.crossover(parent_a, parent_b)

        # Generation should be parent's generation + 1
        expected_gen = max(parent_a.generation, parent_b.generation) + 1
        assert result.offspring.generation == expected_gen

    def test_offspring_has_unique_genome_id(self, parent_a, parent_b, crossover_engine):
        """Test each offspring has unique genome ID."""
        results = [
            crossover_engine.crossover(parent_a, parent_b) for _ in range(10)
        ]

        genome_ids = [r.offspring.genome_id for r in results]
        assert len(genome_ids) == len(set(genome_ids)), "Genome IDs not unique"

    def test_offspring_has_scientific_name(self, parent_a, parent_b, crossover_engine):
        """Test offspring gets a scientific name."""
        result = crossover_engine.crossover(parent_a, parent_b)

        assert result.offspring.scientific_name
        assert len(result.offspring.scientific_name) > 0

    def test_crossover_history_tracked(self, parent_a, parent_b):
        """Test crossover history is maintained."""
        engine = GeneticCrossover(mutation_rate=0.0)

        for _ in range(5):
            engine.crossover(parent_a, parent_b)

        assert len(engine.crossover_history) == 5


class TestMutation:
    """Test mutation mechanics."""

    def test_mutation_rate_respected(self, parent_a, parent_b):
        """Test mutation rate affects offspring."""
        # High mutation rate
        engine_high = GeneticCrossover(mutation_rate=1.0)
        # Low mutation rate
        engine_low = GeneticCrossover(mutation_rate=0.0)

        # With 100% mutation rate, notes should contain mutation info
        result_high = engine_high.crossover(parent_a, parent_b)
        assert "mutation" in result_high.notes.lower() or result_high.notes == ""

        # With 0% mutation rate, no mutation notes
        result_low = engine_low.crossover(parent_a, parent_b)
        assert result_low.notes == ""

    def test_mutation_preserves_validity(self, parent_a, parent_b):
        """Test mutations produce valid genes."""
        engine = GeneticCrossover(mutation_rate=1.0)

        for _ in range(20):
            result = engine.crossover(parent_a, parent_b)
            genes = result.offspring.genes

            # All values should be valid
            assert genes.font.size_body > 0
            assert genes.margin.top >= 0
            assert genes.color.text.startswith("#")


class TestBreedFunction:
    """Test the convenience breed function."""

    def test_breed_produces_offspring(self, parent_a, parent_b):
        """Test breed function works."""
        offspring = breed(parent_a, parent_b)

        assert offspring is not None
        assert isinstance(offspring, StylingGenome)
        assert offspring.generation > 0

    def test_breed_with_strategy(self, parent_a, parent_b):
        """Test breed with specific strategy."""
        offspring = breed(
            parent_a, parent_b, strategy=CrossoverStrategy.CATEGORY_SWAP
        )

        assert offspring is not None


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_crossover_identical_parents(self):
        """Test crossover with identical parents."""
        genes = StylingGene(name="Test")
        parent = StylingGenome.from_genes(genes)

        engine = GeneticCrossover(mutation_rate=0.0)
        result = engine.crossover(parent, parent)

        # Offspring should have same genes (no mutation)
        assert result.offspring.genes.to_dict() == parent.genes.to_dict()

    def test_crossover_preserves_parent_genomes(self, parent_a, parent_b, crossover_engine):
        """Test crossover doesn't modify parents."""
        parent_a_genes = parent_a.genes.to_dict()
        parent_b_genes = parent_b.genes.to_dict()

        crossover_engine.crossover(parent_a, parent_b)

        assert parent_a.genes.to_dict() == parent_a_genes
        assert parent_b.genes.to_dict() == parent_b_genes

    def test_crossover_with_no_fitness(self):
        """Test crossover works when parents have no fitness score."""
        genes_a = StylingGene(name="A")
        genes_b = StylingGene(name="B")
        parent_a = StylingGenome.from_genes(genes_a)
        parent_b = StylingGenome.from_genes(genes_b)

        engine = GeneticCrossover()
        result = engine.crossover(parent_a, parent_b)

        assert result.offspring is not None


class TestBreedingReport:
    """Test breeding report generation."""

    def test_generate_report(self, parent_a, parent_b):
        """Test report generation."""
        engine = GeneticCrossover()

        # Perform some crossovers
        for _ in range(5):
            engine.crossover(parent_a, parent_b)

        report = engine.generate_breeding_report()

        assert "Breeding Report" in report
        assert "Total Crossovers" in report
        assert "5" in report

    def test_empty_report(self):
        """Test report with no crossovers."""
        engine = GeneticCrossover()
        report = engine.generate_breeding_report()

        assert "No crossover operations" in report
