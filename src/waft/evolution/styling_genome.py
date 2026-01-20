"""
Styling Genome: Treating Document Design as Evolving Genetic Material.

This module implements the core concept: styling elements are genes.
- Font families/sizes = genes
- Margins = genes
- Colors = genes
- Layouts = genes
- Information density = genes

Each styling configuration gets a unique genome ID (SHA-256 hash),
enabling lineage tracking, evolution, and scientific naming.
"""

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from ..core.agent.state import EvolutionaryEvent, EvolutionaryEventType
from ..core.science.taxonomy import LineagePoet


@dataclass
class FontGene:
    """Font configuration as genetic material."""

    family: str = "sans-serif"  # Font family name
    size_body: int = 11  # Body text size (pt)
    size_h1: int = 24  # H1 size (pt)
    size_h2: int = 18  # H2 size (pt)
    size_h3: int = 14  # H3 size (pt)
    size_code: int = 10  # Code block size (pt)
    line_height: float = 1.5  # Line height multiplier

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for hashing."""
        return asdict(self)


@dataclass
class MarginGene:
    """Margin/spacing configuration as genetic material."""

    top: int = 20  # Top margin (mm)
    bottom: int = 20  # Bottom margin (mm)
    left: int = 20  # Left margin (mm)
    right: int = 20  # Right margin (mm)
    paragraph_spacing: int = 10  # Space between paragraphs (pt)
    section_spacing: int = 15  # Space between sections (pt)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for hashing."""
        return asdict(self)


@dataclass
class ColorGene:
    """Color scheme as genetic material."""

    text: str = "#000000"  # Primary text color
    background: str = "#FFFFFF"  # Background color
    heading: str = "#1a1a1a"  # Heading color
    accent: str = "#0066cc"  # Accent/link color
    code_bg: str = "#f5f5f5"  # Code block background
    code_text: str = "#333333"  # Code block text
    border: str = "#cccccc"  # Border color

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for hashing."""
        return asdict(self)


@dataclass
class LayoutGene:
    """Layout configuration as genetic material."""

    columns: int = 1  # Number of columns (1 or 2)
    density: str = "normal"  # "compact", "normal", "spacious"
    toc_enabled: bool = False  # Table of contents
    page_numbers: bool = True  # Page numbering
    header_enabled: bool = True  # Header on each page
    footer_enabled: bool = True  # Footer on each page

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for hashing."""
        return asdict(self)


@dataclass
class StylingGene:
    """
    Complete styling configuration as genetic material.

    This represents the full "DNA" of a document's visual design.
    Any change to these genes produces a new genome with a new ID.
    """

    font: FontGene = field(default_factory=FontGene)
    margin: MarginGene = field(default_factory=MarginGene)
    color: ColorGene = field(default_factory=ColorGene)
    layout: LayoutGene = field(default_factory=LayoutGene)

    # Metadata
    name: str = "default"  # Human-readable name
    description: str = ""  # Optional description

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for hashing and serialization."""
        return {
            "font": self.font.to_dict(),
            "margin": self.margin.to_dict(),
            "color": self.color.to_dict(),
            "layout": self.layout.to_dict(),
            "name": self.name,
            "description": self.description,
        }

    def to_json(self) -> str:
        """Convert to JSON string (deterministic ordering)."""
        return json.dumps(self.to_dict(), sort_keys=True)


@dataclass
class StylingGenome:
    """
    A styling genome with unique ID, lineage tracking, and evolution history.

    Each genome represents a complete styling configuration that can:
    - Spawn variants (mutations)
    - Be evaluated for fitness
    - Track lineage through generations
    - Record evolutionary events
    """

    genome_id: str  # SHA-256 hash of styling configuration
    genes: StylingGene  # The actual styling DNA
    generation: int = 0  # Generation number (0 = genesis)
    parent_id: str | None = None  # Parent genome ID (lineage)
    lineage_path: list[str] = field(default_factory=list)  # Full lineage

    # Scientific naming (using WAFT taxonomy)
    scientific_name: str = ""  # Generated from genome_id

    # Evolution tracking
    fitness_score: float | None = None  # 0.0-1.0 fitness
    flight_recorder: list[EvolutionaryEvent] = field(default_factory=list)

    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_evaluated_at: datetime | None = None

    @classmethod
    def from_genes(
        cls, genes: StylingGene, parent: Optional["StylingGenome"] = None
    ) -> "StylingGenome":
        """
        Create a new genome from styling genes.

        Args:
            genes: Styling configuration
            parent: Optional parent genome for lineage tracking

        Returns:
            New StylingGenome with computed genome_id and lineage
        """
        # Compute genome ID from genes (deterministic hash)
        genome_id = cls.compute_genome_id(genes)

        # Generate scientific name from genome ID
        scientific_name = LineagePoet.generate_name(genome_id)

        # Set up lineage
        generation = 0
        parent_id = None
        lineage_path = [genome_id]

        if parent:
            generation = parent.generation + 1
            parent_id = parent.genome_id
            lineage_path = parent.lineage_path + [genome_id]

        genome = cls(
            genome_id=genome_id,
            genes=genes,
            generation=generation,
            parent_id=parent_id,
            lineage_path=lineage_path,
            scientific_name=scientific_name,
        )

        # Record genesis event
        genome._record_event(
            event_type=EvolutionaryEventType.SPAWN,
            payload={
                "event": "genesis" if parent is None else "spawn",
                "parent_genome_id": parent_id,
                "generation": generation,
                "scientific_name": scientific_name,
            },
        )

        return genome

    @staticmethod
    def compute_genome_id(genes: StylingGene) -> str:
        """
        Compute deterministic genome ID from genes.

        Uses SHA-256 hash of JSON representation (with sorted keys).
        Same genes always produce same genome_id.

        Args:
            genes: Styling configuration

        Returns:
            64-character hex string (SHA-256 hash)
        """
        genes_json = genes.to_json()
        return hashlib.sha256(genes_json.encode()).hexdigest()

    def spawn_variant(
        self, mutations: dict[str, Any], mutation_description: str = ""
    ) -> "StylingGenome":
        """
        Spawn a variant genome with mutations.

        Args:
            mutations: Dictionary of mutations to apply
                      Example: {"font.size_body": 12, "margin.top": 25}
            mutation_description: Human-readable description

        Returns:
            New StylingGenome with mutations applied
        """
        # Deep copy genes
        new_genes_dict = self.genes.to_dict()

        # Apply mutations
        for key, value in mutations.items():
            parts = key.split(".")
            if len(parts) == 2:
                category, field_name = parts
                if category in new_genes_dict:
                    new_genes_dict[category][field_name] = value

        # Reconstruct genes
        new_genes = StylingGene(
            font=FontGene(**new_genes_dict["font"]),
            margin=MarginGene(**new_genes_dict["margin"]),
            color=ColorGene(**new_genes_dict["color"]),
            layout=LayoutGene(**new_genes_dict["layout"]),
            name=new_genes_dict["name"],
            description=new_genes_dict["description"],
        )

        # Create variant genome
        variant = StylingGenome.from_genes(new_genes, parent=self)

        # Record mutation event
        variant._record_event(
            event_type=EvolutionaryEventType.MUTATE,
            payload={
                "mutations": mutations,
                "description": mutation_description,
                "parent_genome_id": self.genome_id,
                "parent_scientific_name": self.scientific_name,
            },
        )

        return variant

    def evaluate_fitness(self, metrics: dict[str, float]) -> float:
        """
        Evaluate and record fitness score.

        Args:
            metrics: Fitness metrics (e.g., {"readability": 0.8, "density": 0.7})

        Returns:
            Overall fitness score (0.0-1.0)
        """
        # Calculate weighted average (can be customized)
        fitness = sum(metrics.values()) / len(metrics) if metrics else 0.0

        self.fitness_score = fitness
        self.last_evaluated_at = datetime.utcnow()

        # Record evaluation event
        self._record_event(
            event_type=EvolutionaryEventType.GYM_EVAL,
            payload={
                "metrics": metrics,
                "fitness": fitness,
            },
            fitness_metrics=metrics,
        )

        return fitness

    def _record_event(
        self,
        event_type: EvolutionaryEventType,
        payload: dict[str, Any],
        fitness_metrics: dict[str, Any] | None = None,
    ):
        """Record evolutionary event to Flight Recorder."""
        event = EvolutionaryEvent(
            timestamp=datetime.utcnow(),
            genome_id=self.genome_id,
            parent_id=self.parent_id,
            generation=self.generation,
            event_type=event_type,
            payload=payload,
            fitness_metrics=fitness_metrics,
            agent_id=f"styling_genome_{self.genome_id[:8]}",
            lineage_path=self.lineage_path,
        )
        self.flight_recorder.append(event)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "genome_id": self.genome_id,
            "genes": self.genes.to_dict(),
            "generation": self.generation,
            "parent_id": self.parent_id,
            "lineage_path": self.lineage_path,
            "scientific_name": self.scientific_name,
            "fitness_score": self.fitness_score,
            "created_at": self.created_at.isoformat(),
            "last_evaluated_at": self.last_evaluated_at.isoformat()
            if self.last_evaluated_at
            else None,
        }

    def save(self, output_dir: Path):
        """
        Save genome to disk.

        Args:
            output_dir: Directory to save genome files
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save genome data
        genome_file = output_dir / f"{self.genome_id[:16]}.json"
        with open(genome_file, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

        # Save flight recorder events
        events_file = output_dir / f"{self.genome_id[:16]}_events.jsonl"
        with open(events_file, "w") as f:
            for event in self.flight_recorder:
                f.write(event.model_dump_json() + "\n")


class StylingGenomeRegistry:
    """
    Registry for tracking all styling genomes and their evolution.

    This is the "genetic laboratory" where we:
    - Track all genome variants
    - Detect scints (styling divergences)
    - Build family trees
    - Analyze evolution patterns
    """

    def __init__(self, registry_dir: Path | None = None):
        """
        Initialize registry.

        Args:
            registry_dir: Directory for storing registry data
        """
        self.genomes: dict[str, StylingGenome] = {}
        self.registry_dir = Path(registry_dir) if registry_dir else Path("_genetics/styling")
        self.registry_dir.mkdir(parents=True, exist_ok=True)

        # Load existing genomes
        self._load_genomes()

    def register(self, genome: StylingGenome):
        """
        Register a genome in the system.

        Args:
            genome: Genome to register
        """
        self.genomes[genome.genome_id] = genome
        genome.save(self.registry_dir)

        # Update registry index
        self._save_index()

    def get(self, genome_id: str) -> StylingGenome | None:
        """Get genome by ID."""
        return self.genomes.get(genome_id)

    def get_by_generation(self, generation: int) -> list[StylingGenome]:
        """Get all genomes from a specific generation."""
        return [g for g in self.genomes.values() if g.generation == generation]

    def get_lineage(self, genome_id: str) -> list[StylingGenome]:
        """Get full lineage path for a genome."""
        genome = self.get(genome_id)
        if not genome:
            return []

        lineage = []
        for ancestor_id in genome.lineage_path:
            ancestor = self.get(ancestor_id)
            if ancestor:
                lineage.append(ancestor)

        return lineage

    def get_best_genome(self, min_fitness: float = 0.0) -> StylingGenome | None:
        """
        Get genome with highest fitness score.

        Args:
            min_fitness: Minimum fitness threshold

        Returns:
            Best genome or None
        """
        candidates = [
            g
            for g in self.genomes.values()
            if g.fitness_score is not None and g.fitness_score >= min_fitness
        ]

        if not candidates:
            return None

        return max(candidates, key=lambda g: g.fitness_score or 0.0)

    def _load_genomes(self):
        """Load existing genomes from registry directory."""
        if not self.registry_dir.exists():
            return

        for genome_file in self.registry_dir.glob("*.json"):
            if "_events" in genome_file.name or genome_file.name == "index.json":
                continue

            try:
                with open(genome_file) as f:
                    data = json.load(f)

                # Reconstruct genome (simplified - full reconstruction would be more complex)
                genes = StylingGene(
                    font=FontGene(**data["genes"]["font"]),
                    margin=MarginGene(**data["genes"]["margin"]),
                    color=ColorGene(**data["genes"]["color"]),
                    layout=LayoutGene(**data["genes"]["layout"]),
                    name=data["genes"]["name"],
                    description=data["genes"]["description"],
                )

                genome = StylingGenome(
                    genome_id=data["genome_id"],
                    genes=genes,
                    generation=data["generation"],
                    parent_id=data.get("parent_id"),
                    lineage_path=data["lineage_path"],
                    scientific_name=data["scientific_name"],
                    fitness_score=data.get("fitness_score"),
                )

                self.genomes[genome.genome_id] = genome
            except Exception as e:
                print(f"Warning: Failed to load genome {genome_file}: {e}")

    def _save_index(self):
        """Save registry index."""
        index_file = self.registry_dir / "index.json"
        index_data = {
            "total_genomes": len(self.genomes),
            "generations": max((g.generation for g in self.genomes.values()), default=0),
            "best_fitness": max(
                (g.fitness_score or 0.0 for g in self.genomes.values()), default=0.0
            ),
            "genome_ids": list(self.genomes.keys()),
        }

        with open(index_file, "w") as f:
            json.dump(index_data, f, indent=2)

    def generate_report(self) -> str:
        """
        Generate evolution report.

        Returns:
            Markdown report of genome evolution
        """
        if not self.genomes:
            return "# Styling Genome Registry\n\nNo genomes registered yet."

        best = self.get_best_genome()
        generations = max((g.generation for g in self.genomes.values()), default=0)

        report = f"""# Styling Genome Registry Report

## Overview
- **Total Genomes**: {len(self.genomes)}
- **Generations**: {generations + 1} (0-{generations})
- **Best Fitness**: {best.fitness_score:.3f} ({best.scientific_name})

## Best Genome
- **ID**: {best.genome_id[:16]}...
- **Name**: {best.scientific_name}
- **Generation**: {best.generation}
- **Fitness**: {best.fitness_score:.3f}

## Evolution Tree
"""

        # Add generation breakdown
        for gen in range(generations + 1):
            gen_genomes = self.get_by_generation(gen)
            report += f"\n### Generation {gen}\n"
            for genome in gen_genomes:
                fitness_str = (
                    f"{genome.fitness_score:.3f}" if genome.fitness_score else "not evaluated"
                )
                report += f"- {genome.scientific_name} (fitness: {fitness_str})\n"

        return report
