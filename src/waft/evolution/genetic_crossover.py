"""
Genetic Crossover Engine: Advanced Genetic Operations for Styling Evolution.

Implements multiple crossover strategies for combining genetic material
from parent genomes to produce offspring with traits from both lineages.

This is the BREEDING GROUND - where evolution happens through combination
rather than just mutation.
"""

import random
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable

from .styling_genome import (
    ColorGene,
    FontGene,
    LayoutGene,
    MarginGene,
    StylingGene,
    StylingGenome,
)


class CrossoverStrategy(str, Enum):
    """Available crossover strategies for genetic combination."""

    UNIFORM = "uniform"  # Random selection of each gene
    SINGLE_POINT = "single_point"  # Single crossover point
    TWO_POINT = "two_point"  # Two crossover points
    CATEGORY_SWAP = "category_swap"  # Swap entire categories (font, margin, etc.)
    FITNESS_WEIGHTED = "fitness_weighted"  # Bias toward fitter parent
    BLENDED = "blended"  # Interpolate numeric values
    DOMINANT_RECESSIVE = "dominant_recessive"  # Mendelian inheritance simulation


@dataclass
class CrossoverResult:
    """Result of a genetic crossover operation."""

    offspring: StylingGenome
    parent_a: StylingGenome
    parent_b: StylingGenome
    strategy: CrossoverStrategy
    crossover_points: list[str]
    inheritance_map: dict[str, str]  # gene -> "parent_a" or "parent_b"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    notes: str = ""

    def get_summary(self) -> str:
        """Get human-readable summary of crossover."""
        return f"""
Genetic Crossover Summary
=========================
Strategy: {self.strategy.value}
Parent A: {self.parent_a.scientific_name} (Gen {self.parent_a.generation}, Fitness: {self.parent_a.fitness_score or 'N/A'})
Parent B: {self.parent_b.scientific_name} (Gen {self.parent_b.generation}, Fitness: {self.parent_b.fitness_score or 'N/A'})
Offspring: {self.offspring.scientific_name} (Gen {self.offspring.generation})

Crossover Points: {', '.join(self.crossover_points) or 'N/A'}

Inheritance Map:
{self._format_inheritance_map()}
"""

    def _format_inheritance_map(self) -> str:
        lines = []
        for gene, parent in sorted(self.inheritance_map.items()):
            marker = "A" if parent == "parent_a" else "B"
            lines.append(f"  [{marker}] {gene}")
        return "\n".join(lines)


class GeneticCrossover:
    """
    The Genetic Crossover Engine.

    Performs sophisticated crossover operations to combine genetic material
    from two parent genomes, producing offspring that inherit traits from both.

    This is where the MAGIC of evolution happens - combining successful traits
    to explore new regions of the fitness landscape.
    """

    def __init__(
        self,
        default_strategy: CrossoverStrategy = CrossoverStrategy.UNIFORM,
        mutation_rate: float = 0.1,
        blend_alpha: float = 0.5,
    ):
        """
        Initialize the crossover engine.

        Args:
            default_strategy: Default crossover strategy to use
            mutation_rate: Probability of additional mutation after crossover
            blend_alpha: Blending factor for BLENDED strategy (0.5 = equal)
        """
        self.default_strategy = default_strategy
        self.mutation_rate = mutation_rate
        self.blend_alpha = blend_alpha
        self.crossover_history: list[CrossoverResult] = []

        # Register strategy handlers
        self._strategies: dict[CrossoverStrategy, Callable] = {
            CrossoverStrategy.UNIFORM: self._uniform_crossover,
            CrossoverStrategy.SINGLE_POINT: self._single_point_crossover,
            CrossoverStrategy.TWO_POINT: self._two_point_crossover,
            CrossoverStrategy.CATEGORY_SWAP: self._category_swap_crossover,
            CrossoverStrategy.FITNESS_WEIGHTED: self._fitness_weighted_crossover,
            CrossoverStrategy.BLENDED: self._blended_crossover,
            CrossoverStrategy.DOMINANT_RECESSIVE: self._dominant_recessive_crossover,
        }

    def crossover(
        self,
        parent_a: StylingGenome,
        parent_b: StylingGenome,
        strategy: CrossoverStrategy | None = None,
    ) -> CrossoverResult:
        """
        Perform genetic crossover between two parent genomes.

        Args:
            parent_a: First parent genome
            parent_b: Second parent genome
            strategy: Crossover strategy (uses default if not specified)

        Returns:
            CrossoverResult containing offspring and metadata
        """
        strategy = strategy or self.default_strategy
        handler = self._strategies[strategy]

        # Perform crossover
        offspring_genes, inheritance_map, crossover_points = handler(parent_a, parent_b)

        # Apply random mutation if dice roll succeeds
        if random.random() < self.mutation_rate:
            offspring_genes, mutation_info = self._apply_random_mutation(offspring_genes)
            notes = f"Post-crossover mutation applied: {mutation_info}"
        else:
            notes = ""

        # Create offspring genome with proper lineage
        # Offspring's parent is the fitter of the two (or parent_a if equal)
        primary_parent = (
            parent_a
            if (parent_a.fitness_score or 0) >= (parent_b.fitness_score or 0)
            else parent_b
        )
        offspring = StylingGenome.from_genes(offspring_genes, parent=primary_parent)

        # Record secondary parent in event
        offspring._record_event(
            event_type=offspring.flight_recorder[-1].event_type,
            payload={
                "crossover": True,
                "strategy": strategy.value,
                "parent_a_id": parent_a.genome_id,
                "parent_b_id": parent_b.genome_id,
                "parent_a_name": parent_a.scientific_name,
                "parent_b_name": parent_b.scientific_name,
                "inheritance_map": inheritance_map,
            },
        )

        result = CrossoverResult(
            offspring=offspring,
            parent_a=parent_a,
            parent_b=parent_b,
            strategy=strategy,
            crossover_points=crossover_points,
            inheritance_map=inheritance_map,
            notes=notes,
        )

        self.crossover_history.append(result)
        return result

    def _uniform_crossover(
        self, parent_a: StylingGenome, parent_b: StylingGenome
    ) -> tuple[StylingGene, dict[str, str], list[str]]:
        """
        Uniform crossover: each gene is randomly selected from either parent.

        This is the most exploratory strategy, creating maximum genetic diversity.
        """
        genes_a = parent_a.genes.to_dict()
        genes_b = parent_b.genes.to_dict()
        offspring_dict: dict[str, Any] = {}
        inheritance_map: dict[str, str] = {}

        for category in ["font", "margin", "color", "layout"]:
            offspring_dict[category] = {}
            for key in genes_a[category]:
                # 50/50 chance for each gene
                if random.random() < 0.5:
                    offspring_dict[category][key] = genes_a[category][key]
                    inheritance_map[f"{category}.{key}"] = "parent_a"
                else:
                    offspring_dict[category][key] = genes_b[category][key]
                    inheritance_map[f"{category}.{key}"] = "parent_b"

        # Copy metadata from fitter parent
        offspring_dict["name"] = genes_a["name"]
        offspring_dict["description"] = f"Uniform crossover of {parent_a.scientific_name} x {parent_b.scientific_name}"

        offspring_genes = self._dict_to_genes(offspring_dict)
        return offspring_genes, inheritance_map, []

    def _single_point_crossover(
        self, parent_a: StylingGenome, parent_b: StylingGenome
    ) -> tuple[StylingGene, dict[str, str], list[str]]:
        """
        Single-point crossover: choose a random point, take all genes
        before from parent A, all after from parent B.
        """
        genes_a = parent_a.genes.to_dict()
        genes_b = parent_b.genes.to_dict()

        # Flatten genes into ordered list
        all_genes = []
        for category in ["font", "margin", "color", "layout"]:
            for key in sorted(genes_a[category].keys()):
                all_genes.append((category, key))

        # Choose crossover point
        crossover_point = random.randint(1, len(all_genes) - 1)
        crossover_gene = f"{all_genes[crossover_point][0]}.{all_genes[crossover_point][1]}"

        offspring_dict: dict[str, Any] = {"font": {}, "margin": {}, "color": {}, "layout": {}}
        inheritance_map: dict[str, str] = {}

        for i, (category, key) in enumerate(all_genes):
            if i < crossover_point:
                offspring_dict[category][key] = genes_a[category][key]
                inheritance_map[f"{category}.{key}"] = "parent_a"
            else:
                offspring_dict[category][key] = genes_b[category][key]
                inheritance_map[f"{category}.{key}"] = "parent_b"

        offspring_dict["name"] = genes_a["name"]
        offspring_dict["description"] = f"Single-point crossover at {crossover_gene}"

        offspring_genes = self._dict_to_genes(offspring_dict)
        return offspring_genes, inheritance_map, [crossover_gene]

    def _two_point_crossover(
        self, parent_a: StylingGenome, parent_b: StylingGenome
    ) -> tuple[StylingGene, dict[str, str], list[str]]:
        """
        Two-point crossover: genes between two points from parent B,
        everything else from parent A.
        """
        genes_a = parent_a.genes.to_dict()
        genes_b = parent_b.genes.to_dict()

        all_genes = []
        for category in ["font", "margin", "color", "layout"]:
            for key in sorted(genes_a[category].keys()):
                all_genes.append((category, key))

        # Choose two crossover points
        point1, point2 = sorted(random.sample(range(1, len(all_genes)), 2))
        crossover_genes = [
            f"{all_genes[point1][0]}.{all_genes[point1][1]}",
            f"{all_genes[point2][0]}.{all_genes[point2][1]}",
        ]

        offspring_dict: dict[str, Any] = {"font": {}, "margin": {}, "color": {}, "layout": {}}
        inheritance_map: dict[str, str] = {}

        for i, (category, key) in enumerate(all_genes):
            if point1 <= i < point2:
                offspring_dict[category][key] = genes_b[category][key]
                inheritance_map[f"{category}.{key}"] = "parent_b"
            else:
                offspring_dict[category][key] = genes_a[category][key]
                inheritance_map[f"{category}.{key}"] = "parent_a"

        offspring_dict["name"] = genes_a["name"]
        offspring_dict["description"] = f"Two-point crossover between {crossover_genes[0]} and {crossover_genes[1]}"

        offspring_genes = self._dict_to_genes(offspring_dict)
        return offspring_genes, inheritance_map, crossover_genes

    def _category_swap_crossover(
        self, parent_a: StylingGenome, parent_b: StylingGenome
    ) -> tuple[StylingGene, dict[str, str], list[str]]:
        """
        Category swap: randomly select entire categories from each parent.

        Good for preserving cohesive styling within categories.
        """
        genes_a = parent_a.genes.to_dict()
        genes_b = parent_b.genes.to_dict()

        categories = ["font", "margin", "color", "layout"]
        offspring_dict: dict[str, Any] = {}
        inheritance_map: dict[str, str] = {}
        crossover_points = []

        for category in categories:
            if random.random() < 0.5:
                offspring_dict[category] = genes_a[category].copy()
                parent = "parent_a"
            else:
                offspring_dict[category] = genes_b[category].copy()
                parent = "parent_b"
                crossover_points.append(category)

            for key in offspring_dict[category]:
                inheritance_map[f"{category}.{key}"] = parent

        offspring_dict["name"] = genes_a["name"]
        offspring_dict["description"] = f"Category swap: {', '.join(crossover_points) or 'all from A'} from B"

        offspring_genes = self._dict_to_genes(offspring_dict)
        return offspring_genes, inheritance_map, crossover_points

    def _fitness_weighted_crossover(
        self, parent_a: StylingGenome, parent_b: StylingGenome
    ) -> tuple[StylingGene, dict[str, str], list[str]]:
        """
        Fitness-weighted crossover: bias gene selection toward fitter parent.

        Uses fitness scores to determine probability of inheriting each gene.
        """
        genes_a = parent_a.genes.to_dict()
        genes_b = parent_b.genes.to_dict()

        fitness_a = parent_a.fitness_score or 0.5
        fitness_b = parent_b.fitness_score or 0.5
        total_fitness = fitness_a + fitness_b

        # Probability of selecting from parent A
        prob_a = fitness_a / total_fitness if total_fitness > 0 else 0.5

        offspring_dict: dict[str, Any] = {}
        inheritance_map: dict[str, str] = {}

        for category in ["font", "margin", "color", "layout"]:
            offspring_dict[category] = {}
            for key in genes_a[category]:
                if random.random() < prob_a:
                    offspring_dict[category][key] = genes_a[category][key]
                    inheritance_map[f"{category}.{key}"] = "parent_a"
                else:
                    offspring_dict[category][key] = genes_b[category][key]
                    inheritance_map[f"{category}.{key}"] = "parent_b"

        offspring_dict["name"] = genes_a["name"]
        offspring_dict["description"] = f"Fitness-weighted crossover (A:{fitness_a:.2f} vs B:{fitness_b:.2f})"

        offspring_genes = self._dict_to_genes(offspring_dict)
        return offspring_genes, inheritance_map, []

    def _blended_crossover(
        self, parent_a: StylingGenome, parent_b: StylingGenome
    ) -> tuple[StylingGene, dict[str, str], list[str]]:
        """
        Blended crossover: interpolate numeric values between parents.

        For numeric genes, creates intermediate values. For non-numeric,
        falls back to uniform selection.
        """
        genes_a = parent_a.genes.to_dict()
        genes_b = parent_b.genes.to_dict()

        alpha = self.blend_alpha
        offspring_dict: dict[str, Any] = {}
        inheritance_map: dict[str, str] = {}

        for category in ["font", "margin", "color", "layout"]:
            offspring_dict[category] = {}
            for key in genes_a[category]:
                val_a = genes_a[category][key]
                val_b = genes_b[category][key]

                if isinstance(val_a, (int, float)) and isinstance(val_b, (int, float)):
                    # Blend numeric values
                    blended = val_a * alpha + val_b * (1 - alpha)
                    offspring_dict[category][key] = (
                        int(round(blended)) if isinstance(val_a, int) else blended
                    )
                    inheritance_map[f"{category}.{key}"] = "blended"
                else:
                    # Non-numeric: random selection
                    if random.random() < 0.5:
                        offspring_dict[category][key] = val_a
                        inheritance_map[f"{category}.{key}"] = "parent_a"
                    else:
                        offspring_dict[category][key] = val_b
                        inheritance_map[f"{category}.{key}"] = "parent_b"

        offspring_dict["name"] = genes_a["name"]
        offspring_dict["description"] = f"Blended crossover (alpha={alpha})"

        offspring_genes = self._dict_to_genes(offspring_dict)
        return offspring_genes, inheritance_map, []

    def _dominant_recessive_crossover(
        self, parent_a: StylingGenome, parent_b: StylingGenome
    ) -> tuple[StylingGene, dict[str, str], list[str]]:
        """
        Dominant-recessive crossover: simulates Mendelian inheritance.

        Each gene is marked as dominant or recessive. Dominant genes
        always express, recessive only when homozygous.
        """
        genes_a = parent_a.genes.to_dict()
        genes_b = parent_b.genes.to_dict()

        # Define which parent's genes are "dominant" based on fitness
        dominant_parent = "parent_a" if (parent_a.fitness_score or 0) >= (parent_b.fitness_score or 0) else "parent_b"
        dominant_genes = genes_a if dominant_parent == "parent_a" else genes_b
        recessive_genes = genes_b if dominant_parent == "parent_a" else genes_a

        offspring_dict: dict[str, Any] = {}
        inheritance_map: dict[str, str] = {}

        for category in ["font", "margin", "color", "layout"]:
            offspring_dict[category] = {}
            for key in dominant_genes[category]:
                # 75% chance for dominant trait (like Punnett square Dd x Dd)
                if random.random() < 0.75:
                    offspring_dict[category][key] = dominant_genes[category][key]
                    inheritance_map[f"{category}.{key}"] = dominant_parent
                else:
                    offspring_dict[category][key] = recessive_genes[category][key]
                    inheritance_map[f"{category}.{key}"] = (
                        "parent_b" if dominant_parent == "parent_a" else "parent_a"
                    )

        offspring_dict["name"] = dominant_genes["name"]
        offspring_dict["description"] = f"Dominant-recessive crossover (dominant: {dominant_parent})"

        offspring_genes = self._dict_to_genes(offspring_dict)
        return offspring_genes, inheritance_map, []

    def _apply_random_mutation(
        self, genes: StylingGene
    ) -> tuple[StylingGene, str]:
        """
        Apply a small random mutation to offspring genes.

        Returns:
            Tuple of (mutated genes, mutation description)
        """
        genes_dict = genes.to_dict()

        # Pick random category and gene to mutate
        category = random.choice(["font", "margin", "color", "layout"])
        key = random.choice(list(genes_dict[category].keys()))
        original = genes_dict[category][key]

        if isinstance(original, int):
            # Numeric mutation: +-10%
            delta = int(original * 0.1) or 1
            genes_dict[category][key] = original + random.choice([-delta, delta])
        elif isinstance(original, float):
            # Float mutation: +-10%
            delta = original * 0.1
            genes_dict[category][key] = round(original + random.uniform(-delta, delta), 2)
        elif isinstance(original, bool):
            # Boolean flip
            genes_dict[category][key] = not original
        elif isinstance(original, str) and original.startswith("#"):
            # Color mutation: slight hue shift
            genes_dict[category][key] = self._mutate_color(original)

        mutation_info = f"{category}.{key}: {original} -> {genes_dict[category][key]}"
        return self._dict_to_genes(genes_dict), mutation_info

    def _mutate_color(self, hex_color: str) -> str:
        """Slightly mutate a hex color."""
        # Parse hex
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)

        # Small random shift
        r = max(0, min(255, r + random.randint(-20, 20)))
        g = max(0, min(255, g + random.randint(-20, 20)))
        b = max(0, min(255, b + random.randint(-20, 20)))

        return f"#{r:02x}{g:02x}{b:02x}"

    def _dict_to_genes(self, genes_dict: dict[str, Any]) -> StylingGene:
        """Convert dictionary back to StylingGene object."""
        return StylingGene(
            font=FontGene(**genes_dict["font"]),
            margin=MarginGene(**genes_dict["margin"]),
            color=ColorGene(**genes_dict["color"]),
            layout=LayoutGene(**genes_dict["layout"]),
            name=genes_dict.get("name", "crossover"),
            description=genes_dict.get("description", ""),
        )

    def generate_breeding_report(self) -> str:
        """Generate report of all crossover operations."""
        if not self.crossover_history:
            return "# Breeding Report\n\nNo crossover operations performed yet."

        report = f"""# Genetic Crossover Breeding Report

## Summary
- **Total Crossovers**: {len(self.crossover_history)}
- **Strategies Used**: {len(set(r.strategy for r in self.crossover_history))}

## Strategy Distribution
"""
        # Count strategies
        strategy_counts: dict[CrossoverStrategy, int] = {}
        for result in self.crossover_history:
            strategy_counts[result.strategy] = strategy_counts.get(result.strategy, 0) + 1

        for strategy, count in sorted(strategy_counts.items(), key=lambda x: -x[1]):
            report += f"- {strategy.value}: {count}\n"

        report += "\n## Recent Crossovers\n"

        # Show last 10 crossovers
        for result in self.crossover_history[-10:]:
            report += f"""
### {result.offspring.scientific_name}
- **Parents**: {result.parent_a.scientific_name} x {result.parent_b.scientific_name}
- **Strategy**: {result.strategy.value}
- **Generation**: {result.offspring.generation}
"""

        return report


# Convenience function for quick crossover
def breed(
    parent_a: StylingGenome,
    parent_b: StylingGenome,
    strategy: CrossoverStrategy = CrossoverStrategy.UNIFORM,
) -> StylingGenome:
    """
    Quick crossover function for breeding two genomes.

    Args:
        parent_a: First parent
        parent_b: Second parent
        strategy: Crossover strategy

    Returns:
        Offspring genome
    """
    engine = GeneticCrossover(default_strategy=strategy)
    result = engine.crossover(parent_a, parent_b)
    return result.offspring
