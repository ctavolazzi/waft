"""
Demo: Styling Evolution System with Scint Detection

This demonstrates the core concept of treating styling as evolving genes:
1. Create genesis genome (default styling)
2. Spawn variants with different mutations
3. Detect scints (styling divergences)
4. Evaluate fitness
5. Select best genome

Run: python examples/demo_styling_evolution.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution.styling_genome import (
    StylingGenome,
    StylingGene,
    FontGene,
    MarginGene,
    ColorGene,
    LayoutGene,
    StylingGenomeRegistry,
)
from src.waft.evolution.scint_detector import ScintDetector


def main():
    print("=" * 80)
    print("WAFT Styling Evolution Demo: Genes, Scints, and Natural Selection")
    print("=" * 80)

    # Initialize registry and scint detector
    registry = StylingGenomeRegistry(registry_dir=Path("_genetics/demo_styling"))
    scint_detector = ScintDetector(divergence_threshold=0.05)

    # ========================================================================
    # GENESIS: Create the first genome
    # ========================================================================
    print("\n📍 GENESIS: Creating initial styling genome...")

    genesis_genes = StylingGene(
        font=FontGene(
            family="sans-serif",
            size_body=11,
            size_h1=24,
            size_h2=18,
            size_h3=14,
        ),
        margin=MarginGene(
            top=20,
            bottom=20,
            left=20,
            right=20,
        ),
        color=ColorGene(
            text="#000000",
            background="#FFFFFF",
            heading="#1a1a1a",
        ),
        layout=LayoutGene(
            columns=1,
            density="normal",
        ),
        name="Genesis Styling",
        description="The first styling genome"
    )

    genesis_genome = StylingGenome.from_genes(genesis_genes)
    registry.register(genesis_genome)

    print(f"✓ Genesis Genome Created")
    print(f"  - ID: {genesis_genome.genome_id[:16]}...")
    print(f"  - Name: {genesis_genome.scientific_name}")
    print(f"  - Generation: {genesis_genome.generation}")

    # ========================================================================
    # SPAWN: Create variant genomes with mutations
    # ========================================================================
    print("\n🧬 SPAWN: Creating styling variants...")

    # Variant 1: Compact styling (smaller fonts, tighter margins)
    variant_compact = genesis_genome.spawn_variant(
        mutations={
            "font.size_body": 10,
            "font.size_h1": 20,
            "font.size_h2": 16,
            "margin.top": 15,
            "margin.bottom": 15,
            "margin.left": 15,
            "margin.right": 15,
            "layout.density": "compact",
        },
        mutation_description="Compact styling for maximum content density"
    )
    registry.register(variant_compact)

    print(f"✓ Variant 1 (Compact)")
    print(f"  - ID: {variant_compact.genome_id[:16]}...")
    print(f"  - Name: {variant_compact.scientific_name}")
    print(f"  - Parent: {variant_compact.parent_id[:16] if variant_compact.parent_id else 'None'}...")

    # Variant 2: Spacious styling (larger fonts, wider margins)
    variant_spacious = genesis_genome.spawn_variant(
        mutations={
            "font.size_body": 13,
            "font.size_h1": 28,
            "font.size_h2": 20,
            "margin.top": 30,
            "margin.bottom": 30,
            "margin.left": 30,
            "margin.right": 30,
            "layout.density": "spacious",
        },
        mutation_description="Spacious styling for maximum readability"
    )
    registry.register(variant_spacious)

    print(f"✓ Variant 2 (Spacious)")
    print(f"  - ID: {variant_spacious.genome_id[:16]}...")
    print(f"  - Name: {variant_spacious.scientific_name}")
    print(f"  - Parent: {variant_spacious.parent_id[:16] if variant_spacious.parent_id else 'None'}...")

    # Variant 3: Two-column layout
    variant_two_column = genesis_genome.spawn_variant(
        mutations={
            "layout.columns": 2,
            "font.size_body": 10,
            "margin.left": 15,
            "margin.right": 15,
        },
        mutation_description="Two-column layout for magazine-style presentation"
    )
    registry.register(variant_two_column)

    print(f"✓ Variant 3 (Two-Column)")
    print(f"  - ID: {variant_two_column.genome_id[:16]}...")
    print(f"  - Name: {variant_two_column.scientific_name}")
    print(f"  - Parent: {variant_two_column.parent_id[:16] if variant_two_column.parent_id else 'None'}...")

    # ========================================================================
    # SCINT DETECTION: Find styling divergences
    # ========================================================================
    print("\n🔍 SCINT DETECTION: Analyzing styling divergences...")

    # Detect scint between compact and spacious variants
    scint_1 = scint_detector.detect(variant_compact, variant_spacious)
    if scint_1:
        print(f"\n⚠ Scint Detected: {scint_1.scint_type.value}")
        print(f"  - Divergence: {scint_1.divergence_score:.2%}")
        print(f"  - Between: {variant_compact.scientific_name} ↔ {variant_spacious.scientific_name}")
        print(f"  - Differences: {len(scint_1.differences)} fields changed")

    # Detect scint between compact and two-column variants
    scint_2 = scint_detector.detect(variant_compact, variant_two_column)
    if scint_2:
        print(f"\n⚠ Scint Detected: {scint_2.scint_type.value}")
        print(f"  - Divergence: {scint_2.divergence_score:.2%}")
        print(f"  - Between: {variant_compact.scientific_name} ↔ {variant_two_column.scientific_name}")
        print(f"  - Differences: {len(scint_2.differences)} fields changed")

    # ========================================================================
    # GYM EVALUATION: Evaluate fitness
    # ========================================================================
    print("\n💪 GYM EVALUATION: Measuring fitness...")

    # Evaluate genesis (baseline)
    genesis_fitness = genesis_genome.evaluate_fitness({
        "readability": 0.75,
        "content_density": 0.60,
        "aesthetic_appeal": 0.70,
        "constraint_satisfaction": 1.0,  # Meets 2-page constraint
    })
    print(f"✓ Genesis: {genesis_fitness:.3f}")

    # Evaluate compact variant (high density, lower readability)
    compact_fitness = variant_compact.evaluate_fitness({
        "readability": 0.65,
        "content_density": 0.85,
        "aesthetic_appeal": 0.60,
        "constraint_satisfaction": 1.0,
    })
    print(f"✓ Compact: {compact_fitness:.3f}")

    # Evaluate spacious variant (high readability, lower density)
    spacious_fitness = variant_spacious.evaluate_fitness({
        "readability": 0.90,
        "content_density": 0.45,
        "aesthetic_appeal": 0.80,
        "constraint_satisfaction": 0.7,  # Might exceed 2 pages
    })
    print(f"✓ Spacious: {spacious_fitness:.3f}")

    # Evaluate two-column variant (balanced)
    two_column_fitness = variant_two_column.evaluate_fitness({
        "readability": 0.80,
        "content_density": 0.75,
        "aesthetic_appeal": 0.85,
        "constraint_satisfaction": 1.0,
    })
    print(f"✓ Two-Column: {two_column_fitness:.3f}")

    # ========================================================================
    # NATURAL SELECTION: Find the winner
    # ========================================================================
    print("\n🏆 NATURAL SELECTION: Identifying optimal genome...")

    best_genome = registry.get_best_genome(min_fitness=0.0)
    if best_genome:
        print(f"✓ Winner: {best_genome.scientific_name}")
        print(f"  - Fitness: {best_genome.fitness_score:.3f}")
        print(f"  - Generation: {best_genome.generation}")
        print(f"  - Description: {best_genome.genes.description}")

    # ========================================================================
    # SCINT RECONCILIATION: Resolve divergences
    # ========================================================================
    print("\n🔧 SCINT RECONCILIATION: Resolving divergences...")

    if scint_1 and not scint_1.resolved:
        winner = scint_detector.reconcile_scint(scint_1, strategy="select_fittest")
        print(f"✓ Scint 1 Resolved")
        print(f"  - Strategy: select_fittest")
        print(f"  - Winner: {winner.scientific_name}")

    if scint_2 and not scint_2.resolved:
        winner = scint_detector.reconcile_scint(scint_2, strategy="select_fittest")
        print(f"✓ Scint 2 Resolved")
        print(f"  - Strategy: select_fittest")
        print(f"  - Winner: {winner.scientific_name}")

    # ========================================================================
    # REPORTS: Generate evolution and scint reports
    # ========================================================================
    print("\n📊 REPORTS: Generating evolution analysis...")

    # Evolution report
    evolution_report_path = Path("_genetics/demo_styling/evolution_report.md")
    evolution_report = registry.generate_report()
    evolution_report_path.write_text(evolution_report)
    print(f"✓ Evolution report: {evolution_report_path}")

    # Scint report
    scint_report_path = Path("_genetics/demo_styling/scint_report.md")
    scint_report = scint_detector.generate_scint_report()
    scint_report_path.write_text(scint_report)
    print(f"✓ Scint report: {scint_report_path}")

    # ========================================================================
    # LINEAGE: Show family tree
    # ========================================================================
    print("\n🌳 LINEAGE: Family tree visualization...")

    if best_genome:
        lineage = registry.get_lineage(best_genome.genome_id)
        print(f"Lineage of {best_genome.scientific_name}:")
        for i, ancestor in enumerate(lineage):
            indent = "  " * i
            fitness_str = f" (fitness: {ancestor.fitness_score:.3f})" if ancestor.fitness_score else ""
            print(f"{indent}└─ Gen {ancestor.generation}: {ancestor.scientific_name}{fitness_str}")

    print("\n" + "=" * 80)
    print("Demo complete! Check _genetics/demo_styling/ for detailed reports.")
    print("=" * 80)


if __name__ == "__main__":
    main()
