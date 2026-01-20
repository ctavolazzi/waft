"""
Demo: Complete One-Pager Evolution System

This demonstrates the full pipeline for evolutionary 2-page PDF generation:
1. ChatDistiller extracts ideas from conversation
2. StylingGenome provides evolved design
3. TwoPageGenerator creates 2-page PDFs
4. Fitness evaluation drives evolution
5. Scint detection monitors divergences
6. Natural selection picks winners

Run: python examples/demo_one_pager_evolution.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution.chat_distiller import ChatDistiller
from src.waft.evolution.scint_detector import ScintDetector
from src.waft.evolution.styling_genome import (
    ColorGene,
    FontGene,
    LayoutGene,
    MarginGene,
    StylingGene,
    StylingGenome,
    StylingGenomeRegistry,
)
from src.waft.evolution.two_page_generator import TwoPageGenerator

# Sample chat conversation for demonstration
SAMPLE_CHAT = """
# Component Evolution System Design Discussion

## Key Decisions

We decided to treat styling elements as genes that can evolve over time.
This allows the system to learn better designs automatically.

The fitness function will measure readability, content density, and
constraint satisfaction.

## Important Insights

It turns out that margins have the biggest impact on content density.
We discovered that two-column layouts work well for certain content types.

Font size needs to balance readability with space efficiency.

## Action Items

- TODO: Implement ChatDistiller for idea extraction
- TODO: Create TwoPageGenerator with hard 2-page constraint
- TODO: Build fitness evaluation system
- Must integrate with existing taxonomy system

## Concepts

A scint is a divergence in styling contexts that needs reconciliation.
The genome registry acts as a genetic laboratory for tracking variants.

Each styling configuration gets a unique SHA-256 genome ID.

## Questions

How do we enforce the 2-page constraint strictly?
What metrics best measure document quality?
Should we support adaptive layouts based on content?

## More Insights

The scientific naming system (LineagePoet) can generate names for
styling genomes just like it does for AI agents.

This creates a beautiful symmetry between agent evolution and
document evolution.

## Next Steps

We'll implement fitness evaluation with weighted components:
- Readability: 35%
- Completeness: 30%
- Constraint satisfaction: 25%
- Aesthetic appeal: 10%

The system should spawn variants with different mutations and
select the fittest ones for survival.
"""


def main():
    print("=" * 80)
    print("WAFT One-Pager Evolution System: Complete Demo")
    print("=" * 80)

    # ========================================================================
    # STEP 1: DISTILL CHAT CONVERSATION
    # ========================================================================
    print("\n📝 STEP 1: Distilling chat conversation into ideas...")

    distiller = ChatDistiller(importance_threshold=0.4)
    distilled = distiller.distill_text(text=SAMPLE_CHAT, title="Component Evolution System Design")

    print("✓ Distilled conversation")
    print(f"  - Total ideas extracted: {distilled.total_ideas}")
    print(f"  - Decisions: {distilled.decisions_count}")
    print(f"  - Insights: {distilled.insights_count}")
    print(f"  - Actions: {distilled.actions_count}")
    print(f"  - Concepts: {distilled.concepts_count}")
    print(f"  - Questions: {distilled.questions_count}")
    print(f"\n  Summary: {distilled.summary}")

    # Show top ideas
    top_ideas = distilled.get_top_ideas(n=5)
    print("\n  Top 5 Ideas:")
    for i, idea in enumerate(top_ideas, 1):
        print(f"    {i}. [{idea.category}] {idea.content[:60]}...")
        print(f"       → {idea.scientific_name}")

    # ========================================================================
    # STEP 2: CREATE STYLING GENOMES
    # ========================================================================
    print("\n🧬 STEP 2: Creating styling genome variants...")

    registry = StylingGenomeRegistry(registry_dir=Path("_genetics/one_pager_demo"))
    scint_detector = ScintDetector(divergence_threshold=0.05)

    # Genesis genome (baseline)
    genesis_genes = StylingGene(
        font=FontGene(family="sans-serif", size_body=11),
        margin=MarginGene(top=20, bottom=20, left=20, right=20),
        color=ColorGene(text="#000000", background="#FFFFFF"),
        layout=LayoutGene(columns=1, density="normal"),
        name="Genesis Styling",
    )
    genesis = StylingGenome.from_genes(genesis_genes)
    registry.register(genesis)
    print(f"✓ Genesis: {genesis.scientific_name}")

    # Variant 1: Content-dense (for fitting more ideas)
    variant_dense = genesis.spawn_variant(
        mutations={
            "font.size_body": 10,
            "font.size_h1": 20,
            "font.size_h2": 16,
            "margin.top": 15,
            "margin.bottom": 15,
            "layout.density": "compact",
        },
        mutation_description="Maximize content density for 2-page constraint",
    )
    registry.register(variant_dense)
    print(f"✓ Dense variant: {variant_dense.scientific_name}")

    # Variant 2: Readability-focused
    variant_readable = genesis.spawn_variant(
        mutations={
            "font.size_body": 12,
            "font.line_height": 1.6,
            "margin.paragraph_spacing": 12,
            "layout.density": "normal",
        },
        mutation_description="Optimize for maximum readability",
    )
    registry.register(variant_readable)
    print(f"✓ Readable variant: {variant_readable.scientific_name}")

    # Detect scint
    scint = scint_detector.detect(variant_dense, variant_readable)
    if scint:
        print(f"\n⚠ Scint detected: {scint.scint_type.value}")
        print(f"  - Divergence: {scint.divergence_score:.2%}")

    # ========================================================================
    # STEP 3: GENERATE 2-PAGE PDFs (using V2 with adaptive constraint enforcement)
    # ========================================================================
    print("\n📄 STEP 3: Generating 2-page PDFs with each styling...")

    generator = TwoPageGenerator(weasyprint_available=False)  # HTML only for demo
    # Note: TwoPageGenerator now defaults to V2 (evolved with TRUE constraint enforcement)

    # Generate with genesis styling
    result_genesis = generator.generate(
        distilled_chat=distilled,
        styling_genome=genesis,
        output_path=Path("_genetics/one_pager_demo/genesis.pdf"),
        target_pages=2,  # V2 uses target_pages instead of page_1_ideas
    )
    print("\n✓ Genesis PDF generated")
    print(f"  - Pages: {result_genesis.get('page_count', 'N/A')}/2")
    print(f"  - Fitness: {result_genesis['fitness_metrics']['overall']:.3f}")
    print(f"  - Readability: {result_genesis['fitness_metrics']['readability']:.3f}")
    print(f"  - Completeness: {result_genesis['fitness_metrics']['completeness']:.3f}")
    print(f"  - Constraint: {result_genesis['fitness_metrics']['constraint_satisfaction']:.3f}")

    # Update genome fitness
    genesis.evaluate_fitness(result_genesis["fitness_metrics"])

    # Generate with dense variant
    result_dense = generator.generate(
        distilled_chat=distilled,
        styling_genome=variant_dense,
        output_path=Path("_genetics/one_pager_demo/dense.pdf"),
        target_pages=2,  # V2 adaptively selects ideas to fit 2 pages
    )
    print("\n✓ Dense variant PDF generated")
    print(f"  - Pages: {result_dense.get('page_count', 'N/A')}/2")
    print(f"  - Fitness: {result_dense['fitness_metrics']['overall']:.3f}")
    print(f"  - Readability: {result_dense['fitness_metrics']['readability']:.3f}")
    print(f"  - Completeness: {result_dense['fitness_metrics']['completeness']:.3f}")
    print(f"  - Constraint: {result_dense['fitness_metrics']['constraint_satisfaction']:.3f}")

    variant_dense.evaluate_fitness(result_dense["fitness_metrics"])

    # Generate with readable variant
    result_readable = generator.generate(
        distilled_chat=distilled,
        styling_genome=variant_readable,
        output_path=Path("_genetics/one_pager_demo/readable.pdf"),
        target_pages=2,  # V2 adaptively selects ideas to fit 2 pages
    )
    print("\n✓ Readable variant PDF generated")
    print(f"  - Fitness: {result_readable['fitness_metrics']['overall']:.3f}")
    print(f"  - Readability: {result_readable['fitness_metrics']['readability']:.3f}")
    print(f"  - Completeness: {result_readable['fitness_metrics']['completeness']:.3f}")
    print(f"  - Constraint: {result_readable['fitness_metrics']['constraint_satisfaction']:.3f}")

    variant_readable.evaluate_fitness(result_readable["fitness_metrics"])

    # ========================================================================
    # STEP 4: NATURAL SELECTION
    # ========================================================================
    print("\n🏆 STEP 4: Natural selection - finding the fittest genome...")

    best = registry.get_best_genome(min_fitness=0.0)
    print(f"\n✓ Winner: {best.scientific_name}")
    print(f"  - Overall fitness: {best.fitness_score:.3f}")
    print(f"  - Generation: {best.generation}")

    # ========================================================================
    # STEP 5: EVOLUTION - SPAWN FROM WINNER
    # ========================================================================
    print("\n🔬 STEP 5: Spawning next generation from winner...")

    # Create a mutation based on what worked
    if best == variant_dense:
        # Dense won - try to push density further but improve readability
        next_gen = best.spawn_variant(
            mutations={
                "font.size_body": 10,  # Keep compact
                "font.line_height": 1.5,  # But improve spacing
                "margin.paragraph_spacing": 8,  # Tighter paragraphs
            },
            mutation_description="Gen 2: Dense + improved readability",
        )
    elif best == variant_readable:
        # Readable won - maintain readability but increase density slightly
        next_gen = best.spawn_variant(
            mutations={
                "font.size_body": 11,  # Slightly smaller
                "margin.top": 18,  # Tighter margins
                "margin.bottom": 18,
            },
            mutation_description="Gen 2: Readable + increased density",
        )
    else:
        # Genesis won - try balanced improvements
        next_gen = best.spawn_variant(
            mutations={
                "font.line_height": 1.55,
                "margin.paragraph_spacing": 9,
            },
            mutation_description="Gen 2: Balanced refinement",
        )

    registry.register(next_gen)
    print(f"✓ Generation 2: {next_gen.scientific_name}")

    # Generate PDF with next gen
    result_next_gen = generator.generate(
        distilled_chat=distilled,
        styling_genome=next_gen,
        output_path=Path("_genetics/one_pager_demo/gen2.pdf"),
        page_1_ideas=5,
    )
    next_gen.evaluate_fitness(result_next_gen["fitness_metrics"])

    print(f"  - Fitness: {next_gen.fitness_score:.3f}")

    # Compare with parent
    improvement = next_gen.fitness_score - best.fitness_score
    if improvement > 0:
        print(f"  - ✓ IMPROVEMENT: +{improvement:.3f} vs parent")
    else:
        print(f"  - ✗ REGRESSION: {improvement:.3f} vs parent")

    # ========================================================================
    # STEP 6: REPORTS
    # ========================================================================
    print("\n📊 STEP 6: Generating reports...")

    # Save distilled chat
    distilled.save(Path("_genetics/one_pager_demo/distilled_chat.json"))
    print("✓ Distilled chat saved")

    # Evolution report
    evolution_report = registry.generate_report()
    report_path = Path("_genetics/one_pager_demo/evolution_report.md")
    report_path.write_text(evolution_report)
    print(f"✓ Evolution report: {report_path}")

    # Scint report
    scint_report = scint_detector.generate_scint_report()
    scint_path = Path("_genetics/one_pager_demo/scint_report.md")
    scint_path.write_text(scint_report)
    print(f"✓ Scint report: {scint_path}")

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "=" * 80)
    print("DEMO COMPLETE!")
    print("=" * 80)

    print("\n📈 Evolution Summary:")
    print(f"  - Generations: {max(g.generation for g in registry.genomes.values()) + 1}")
    print(f"  - Total genomes: {len(registry.genomes)}")
    print(f"  - Best fitness: {best.fitness_score:.3f} ({best.scientific_name})")
    print(f"  - Scints detected: {len(scint_detector.detected_scints)}")

    print("\n💡 Ideas Processed:")
    print(f"  - Total ideas: {distilled.total_ideas}")
    print(f"  - Genome IDs assigned: {len([i.genome_id for i in distilled.ideas])}")

    print("\n📁 Output:")
    print("  - Location: _genetics/one_pager_demo/")
    print("  - HTML files: genesis.html, dense.html, readable.html, gen2.html")
    print("  - Reports: evolution_report.md, scint_report.md")
    print("  - Data: distilled_chat.json, genome registry")

    print("\n✨ The one-pager evolution system is working!")
    print("=" * 80)


if __name__ == "__main__":
    main()
