"""
Scint Detector: Monitoring and Controlling Styling Divergences.

A "scint" is a divergence in styling contexts - when different styling
genomes evolve in parallel and need reconciliation. This module tracks,
detects, and helps resolve these divergences.

Scint Types:
- FONT_SCINT: Font configuration divergence
- MARGIN_SCINT: Margin/spacing divergence
- COLOR_SCINT: Color scheme divergence
- LAYOUT_SCINT: Layout configuration divergence
- FULL_SCINT: Complete styling divergence
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from enum import Enum

from .styling_genome import StylingGenome, StylingGene


class ScintType(str, Enum):
    """Types of styling scints (divergences)."""
    FONT_SCINT = "font_scint"  # Font configuration diverged
    MARGIN_SCINT = "margin_scint"  # Margin configuration diverged
    COLOR_SCINT = "color_scint"  # Color scheme diverged
    LAYOUT_SCINT = "layout_scint"  # Layout configuration diverged
    FULL_SCINT = "full_scint"  # Complete styling divergence
    MINOR_SCINT = "minor_scint"  # Small divergence (< 20% difference)
    MAJOR_SCINT = "major_scint"  # Large divergence (>= 20% difference)


@dataclass
class Scint:
    """
    A detected styling divergence between two genomes.

    Represents a point where styling evolved in different directions,
    requiring reconciliation or selection.
    """
    genome_a: StylingGenome  # First genome in divergence
    genome_b: StylingGenome  # Second genome in divergence
    scint_type: ScintType  # Type of divergence
    divergence_score: float  # 0.0-1.0 (how different they are)
    differences: Dict[str, Any]  # Specific differences
    detected_at: datetime = field(default_factory=datetime.utcnow)
    resolved: bool = False  # Whether scint has been resolved
    resolution_strategy: Optional[str] = None  # How it was resolved

    def get_diff_summary(self) -> str:
        """Get human-readable summary of differences."""
        lines = [
            f"Scint Type: {self.scint_type.value}",
            f"Divergence Score: {self.divergence_score:.2%}",
            f"",
            f"Genome A: {self.genome_a.scientific_name} (Gen {self.genome_a.generation})",
            f"Genome B: {self.genome_b.scientific_name} (Gen {self.genome_b.generation})",
            f"",
            "Differences:",
        ]

        for key, value in self.differences.items():
            lines.append(f"  - {key}: {value}")

        return "\n".join(lines)

    def mark_resolved(self, strategy: str):
        """Mark scint as resolved with given strategy."""
        self.resolved = True
        self.resolution_strategy = strategy


class ScintDetector:
    """
    Detector for styling divergences (scints).

    Monitors styling genome evolution and detects when different
    evolutionary paths diverge, requiring reconciliation.
    """

    def __init__(self, divergence_threshold: float = 0.1):
        """
        Initialize detector.

        Args:
            divergence_threshold: Minimum divergence score to report (0.0-1.0)
        """
        self.divergence_threshold = divergence_threshold
        self.detected_scints: List[Scint] = []

    def detect(self, genome_a: StylingGenome, genome_b: StylingGenome) -> Optional[Scint]:
        """
        Detect if two genomes have diverged (scint detection).

        Args:
            genome_a: First genome to compare
            genome_b: Second genome to compare

        Returns:
            Scint object if divergence detected, None otherwise
        """
        # Compute differences
        differences = self._compute_differences(genome_a.genes, genome_b.genes)

        if not differences:
            return None  # No divergence

        # Calculate divergence score
        divergence_score = self._calculate_divergence_score(differences)

        if divergence_score < self.divergence_threshold:
            return None  # Below threshold

        # Determine scint type
        scint_type = self._classify_scint(differences, divergence_score)

        # Create scint
        scint = Scint(
            genome_a=genome_a,
            genome_b=genome_b,
            scint_type=scint_type,
            divergence_score=divergence_score,
            differences=differences,
        )

        self.detected_scints.append(scint)
        return scint

    def detect_lineage_scints(self, genomes: List[StylingGenome]) -> List[Scint]:
        """
        Detect scints across a lineage of genomes.

        Args:
            genomes: List of genomes in chronological order

        Returns:
            List of detected scints
        """
        scints = []

        for i in range(len(genomes) - 1):
            genome_a = genomes[i]
            genome_b = genomes[i + 1]

            scint = self.detect(genome_a, genome_b)
            if scint:
                scints.append(scint)

        return scints

    def _compute_differences(
        self,
        genes_a: StylingGene,
        genes_b: StylingGene
    ) -> Dict[str, Tuple[Any, Any]]:
        """
        Compute specific differences between two gene sets.

        Args:
            genes_a: First gene set
            genes_b: Second gene set

        Returns:
            Dictionary mapping field paths to (value_a, value_b) tuples
        """
        differences = {}

        # Compare fonts
        for key, value_a in genes_a.font.to_dict().items():
            value_b = genes_b.font.to_dict()[key]
            if value_a != value_b:
                differences[f"font.{key}"] = (value_a, value_b)

        # Compare margins
        for key, value_a in genes_a.margin.to_dict().items():
            value_b = genes_b.margin.to_dict()[key]
            if value_a != value_b:
                differences[f"margin.{key}"] = (value_a, value_b)

        # Compare colors
        for key, value_a in genes_a.color.to_dict().items():
            value_b = genes_b.color.to_dict()[key]
            if value_a != value_b:
                differences[f"color.{key}"] = (value_a, value_b)

        # Compare layout
        for key, value_a in genes_a.layout.to_dict().items():
            value_b = genes_b.layout.to_dict()[key]
            if value_a != value_b:
                differences[f"layout.{key}"] = (value_a, value_b)

        return differences

    def _calculate_divergence_score(self, differences: Dict[str, Tuple[Any, Any]]) -> float:
        """
        Calculate overall divergence score from differences.

        Args:
            differences: Difference dictionary

        Returns:
            Divergence score (0.0-1.0)
        """
        if not differences:
            return 0.0

        # Count total possible differences (approximate)
        total_fields = (
            len(StylingGene().font.to_dict()) +
            len(StylingGene().margin.to_dict()) +
            len(StylingGene().color.to_dict()) +
            len(StylingGene().layout.to_dict())
        )

        # Simple ratio: differences / total_fields
        raw_score = len(differences) / total_fields

        # Weight by type (some differences are more significant)
        weighted_score = raw_score

        # Check for major structural changes
        if any(k.startswith("layout.") for k in differences):
            weighted_score *= 1.5  # Layout changes are more significant

        if any(k.startswith("color.") for k in differences):
            weighted_score *= 1.2  # Color changes are moderately significant

        # Clamp to 0.0-1.0
        return min(weighted_score, 1.0)

    def _classify_scint(
        self,
        differences: Dict[str, Tuple[Any, Any]],
        divergence_score: float
    ) -> ScintType:
        """
        Classify the type of scint based on differences.

        Args:
            differences: Difference dictionary
            divergence_score: Overall divergence score

        Returns:
            ScintType classification
        """
        # Check if divergence is isolated to one category
        categories = set(k.split(".")[0] for k in differences.keys())

        if len(categories) == 1:
            category = list(categories)[0]
            if category == "font":
                return ScintType.FONT_SCINT
            elif category == "margin":
                return ScintType.MARGIN_SCINT
            elif category == "color":
                return ScintType.COLOR_SCINT
            elif category == "layout":
                return ScintType.LAYOUT_SCINT

        # Multiple categories diverged
        if divergence_score >= 0.2:
            return ScintType.MAJOR_SCINT
        elif divergence_score >= 0.05:
            return ScintType.MINOR_SCINT
        else:
            return ScintType.FULL_SCINT

    def get_unresolved_scints(self) -> List[Scint]:
        """Get all unresolved scints."""
        return [s for s in self.detected_scints if not s.resolved]

    def reconcile_scint(
        self,
        scint: Scint,
        strategy: str = "select_fittest"
    ) -> StylingGenome:
        """
        Reconcile a scint using given strategy.

        Strategies:
        - "select_fittest": Choose genome with higher fitness
        - "select_a": Choose genome A
        - "select_b": Choose genome B
        - "merge": Merge best genes from both (not yet implemented)

        Args:
            scint: Scint to reconcile
            strategy: Resolution strategy

        Returns:
            Winning genome
        """
        if strategy == "select_fittest":
            # Choose genome with higher fitness
            fitness_a = scint.genome_a.fitness_score or 0.0
            fitness_b = scint.genome_b.fitness_score or 0.0

            winner = scint.genome_a if fitness_a >= fitness_b else scint.genome_b

        elif strategy == "select_a":
            winner = scint.genome_a

        elif strategy == "select_b":
            winner = scint.genome_b

        elif strategy == "merge":
            # TODO: Implement genetic crossover
            raise NotImplementedError("Merge strategy not yet implemented")

        else:
            raise ValueError(f"Unknown strategy: {strategy}")

        # Mark scint as resolved
        scint.mark_resolved(strategy)

        return winner

    def generate_scint_report(self) -> str:
        """
        Generate report of all detected scints.

        Returns:
            Markdown report
        """
        if not self.detected_scints:
            return "# Scint Report\n\nNo scints detected."

        unresolved = self.get_unresolved_scints()

        report = f"""# Scint Detection Report

## Summary
- **Total Scints Detected**: {len(self.detected_scints)}
- **Unresolved**: {len(unresolved)}
- **Resolved**: {len(self.detected_scints) - len(unresolved)}

## Scint Details
"""

        for i, scint in enumerate(self.detected_scints, 1):
            status = "✓ Resolved" if scint.resolved else "⚠ Unresolved"
            report += f"\n### Scint #{i} - {status}\n"
            report += f"```\n{scint.get_diff_summary()}\n```\n"

            if scint.resolved:
                report += f"**Resolution**: {scint.resolution_strategy}\n"

        return report
