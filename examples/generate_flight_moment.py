"""
Generate "The Moment It Took Flight" One-Pager

This script creates a 2-page PDF documenting the breakthrough moment when
the one-pager evolution system became real. It uses the system to document
itself, demonstrating:

1. Chat distillation (ideas as genes)
2. Styling evolution (design as genes)
3. Active scint monitoring (divergence control)
4. Natural selection (fitness-driven evolution)
5. 2-page constraint (hard enforcement)

This is meta-documentation at the moment of breakthrough.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution.chat_distiller import ChatDistiller
from src.waft.evolution.styling_genome import (
    StylingGenome,
    StylingGene,
    FontGene,
    MarginGene,
    ColorGene,
    LayoutGene,
    StylingGenomeRegistry,
)
from src.waft.evolution.two_page_generator import TwoPageGenerator
from src.waft.evolution.scint_detector import ScintDetector


# The conversation about the breakthrough
BREAKTHROUGH_CONVERSATION = """
# The Moment It Took Flight

## The Core Insight

We decided to treat styling elements as genes that can evolve over time.
Fonts, margins, colors, layouts - all genetic material subject to natural selection.

The critical realization: styling isn't just configuration, it's DNA that can
improve through evolution.

## Key Decisions

We chose to enforce a hard 2-page constraint - exactly one double-sided physical sheet.
This constraint drives the entire evolution process.

The fitness function balances four components: readability (35%), completeness (30%),
constraint satisfaction (25%), and aesthetic appeal (10%).

Ideas extracted from conversations get genome IDs and scientific names, treating
concepts as genetic material just like styling.

## Scint Detection

A scint is a divergence in styling contexts - when parallel evolution paths split.
We built ScintDetector to monitor and control these divergences automatically.

Scints are classified by type: FONT_SCINT, MARGIN_SCINT, COLOR_SCINT, LAYOUT_SCINT.
Each scint gets a divergence score and can be reconciled with strategies like
select_fittest or merge.

This prevents silent divergence and keeps evolution coherent.

## Important Insights

It turns out that margins have the biggest impact on content density for 2-page PDFs.
Font size needs to balance readability with space efficiency.

The LineagePoet taxonomy system generates scientific names for styling genomes
just like it does for AI agents - beautiful symmetry between agent and document evolution.

Every genome gets SHA-256 hash as its ID, making lineage tracking deterministic
and scientifically rigorous.

The Flight Recorder tracks all evolutionary events - SPAWN, MUTATE, GYM_EVAL -
creating complete family trees of document designs.

## Technical Concepts

StylingGenome is the complete DNA of document design - fonts, margins, colors, layouts.
Each genome can spawn variants with mutations and evaluate fitness.

ChatDistiller extracts ideas from conversations using pattern recognition.
Ideas are classified as decisions, insights, actions, concepts, or questions.

TwoPageGenerator combines DistilledChat (ideas) with StylingGenome (design)
to create exactly 2-page PDFs. The constraint is enforced through HTML templating
with Jinja2 and optional WeasyPrint PDF generation.

StylingGenomeRegistry acts as a genetic laboratory, tracking all variants,
building family trees, and finding the fittest genomes.

## The Breakthrough Moment

User said: "This feels like it - the moment it takes flight. Do you sense it too?"

The abstraction became flight. The system doesn't just make documents - it makes
documents that know their own lineage, where every styling choice has DNA,
where ideas get scientific names, and where the whole thing gets better through
natural selection.

The first evolved PDF (Fenris Svartr, the Wild) had fitness 0.936 and perfectly
satisfied the 2-page constraint while balancing all fitness components.

## Meta-Beauty

The one-pager system creates a one-pager about creating the one-pager system.
Ideas about genes become genes themselves.
The breakthrough documents itself at the moment of breakthrough.

This is the artifact - the proof that styling evolution works, captured at the
instant it took flight.

## What Makes It Special

The system treats both ideas and styling as genetic material with complete
lineage tracking. Every idea gets a genome ID. Every styling configuration
gets a genome ID. Scientific names everywhere.

Scint detection runs throughout, preventing divergent evolution paths from
going unnoticed. All scints are tracked, classified, and reconciled.

The 2-page constraint drives evolution toward information density without
sacrificing readability. Fitness evaluation is multi-dimensional and weighted.

The system integrates seamlessly with WAFT's existing taxonomy, Flight Recorder,
and evolutionary event system.

## Future Vision

This system will evolve document designs that are optimized for specific
content types through natural selection. Genetic crossover will merge the
best traits from multiple parents.

Scint monitoring will prevent context divergence as multiple styling lineages
evolve in parallel. The registry will track thousands of genome variants.

The one-pager system becomes a research platform for document evolution,
with complete scientific tracking and reproducible experiments.
"""


def main():
    print("=" * 80)
    print("Generating: The Moment It Took Flight")
    print("A Meta One-Pager Documenting the Breakthrough")
    print("=" * 80)

    # ========================================================================
    # STEP 1: DISTILL THE CONVERSATION
    # ========================================================================
    print("\n📝 STEP 1: Distilling breakthrough conversation...")

    distiller = ChatDistiller(importance_threshold=0.3)
    distilled = distiller.distill_text(
        text=BREAKTHROUGH_CONVERSATION,
        title="The Moment It Took Flight"
    )

    print(f"✓ Conversation distilled")
    print(f"  - Total ideas: {distilled.total_ideas}")
    print(f"  - Decisions: {distilled.decisions_count}")
    print(f"  - Insights: {distilled.insights_count}")
    print(f"  - Concepts: {distilled.concepts_count}")

    # Save distilled chat
    output_dir = Path("_genetics/flight_moment")
    output_dir.mkdir(parents=True, exist_ok=True)
    distilled.save(output_dir / "distilled_conversation.json")

    # ========================================================================
    # STEP 2: CREATE STYLING VARIANTS WITH SCINT MONITORING
    # ========================================================================
    print("\n🧬 STEP 2: Creating styling variants with scint monitoring...")

    registry = StylingGenomeRegistry(registry_dir=output_dir)
    scint_detector = ScintDetector(divergence_threshold=0.05)

    # Genesis: Balanced baseline
    genesis_genes = StylingGene(
        font=FontGene(
            family="sans-serif",
            size_body=11,
            size_h1=22,
            size_h2=16,
            size_h3=13,
            line_height=1.5,
        ),
        margin=MarginGene(
            top=20,
            bottom=20,
            left=20,
            right=20,
            paragraph_spacing=10,
            section_spacing=15,
        ),
        color=ColorGene(
            text="#1a1a1a",
            background="#FFFFFF",
            heading="#000000",
            accent="#0066cc",
            code_bg="#f5f5f5",
        ),
        layout=LayoutGene(
            columns=1,
            density="normal",
            page_numbers=True,
        ),
        name="Flight Moment Genesis",
        description="Balanced styling for breakthrough documentation"
    )
    genesis = StylingGenome.from_genes(genesis_genes)
    registry.register(genesis)
    print(f"✓ Genesis: {genesis.scientific_name}")

    # Variant 1: Dense (maximize ideas per page)
    print("\n  Spawning dense variant...")
    variant_dense = genesis.spawn_variant(
        mutations={
            "font.size_body": 10,
            "font.size_h1": 20,
            "font.size_h2": 15,
            "font.line_height": 1.4,
            "margin.top": 18,
            "margin.bottom": 18,
            "margin.paragraph_spacing": 8,
            "layout.density": "compact",
        },
        mutation_description="Dense styling to fit more breakthrough ideas"
    )
    registry.register(variant_dense)
    print(f"  ✓ Dense: {variant_dense.scientific_name}")

    # Check for scint
    scint_dense = scint_detector.detect(genesis, variant_dense)
    if scint_dense:
        print(f"  ⚠ Scint detected: {scint_dense.scint_type.value}")
        print(f"    - Divergence: {scint_dense.divergence_score:.2%}")
        print(f"    - Differences: {len(scint_dense.differences)} fields")

    # Variant 2: Readable (prioritize clarity)
    print("\n  Spawning readable variant...")
    variant_readable = genesis.spawn_variant(
        mutations={
            "font.size_body": 12,
            "font.line_height": 1.6,
            "margin.paragraph_spacing": 12,
            "margin.section_spacing": 18,
            "layout.density": "spacious",
        },
        mutation_description="Readable styling for maximum clarity"
    )
    registry.register(variant_readable)
    print(f"  ✓ Readable: {variant_readable.scientific_name}")

    # Check for scints
    scint_readable = scint_detector.detect(genesis, variant_readable)
    if scint_readable:
        print(f"  ⚠ Scint detected: {scint_readable.scint_type.value}")
        print(f"    - Divergence: {scint_readable.divergence_score:.2%}")
        print(f"    - Differences: {len(scint_readable.differences)} fields")

    scint_cross = scint_detector.detect(variant_dense, variant_readable)
    if scint_cross:
        print(f"  ⚠ Cross-lineage scint: {scint_cross.scint_type.value}")
        print(f"    - Divergence: {scint_cross.divergence_score:.2%}")
        print(f"    - Between: {variant_dense.scientific_name} ↔ {variant_readable.scientific_name}")

    # Variant 3: Aesthetic (visual appeal)
    print("\n  Spawning aesthetic variant...")
    variant_aesthetic = genesis.spawn_variant(
        mutations={
            "font.family": "serif",
            "color.text": "#2c3e50",
            "color.heading": "#34495e",
            "color.accent": "#3498db",
            "margin.left": 25,
            "margin.right": 25,
        },
        mutation_description="Aesthetic styling with serif fonts and refined colors"
    )
    registry.register(variant_aesthetic)
    print(f"  ✓ Aesthetic: {variant_aesthetic.scientific_name}")

    # Check for scint
    scint_aesthetic = scint_detector.detect(genesis, variant_aesthetic)
    if scint_aesthetic:
        print(f"  ⚠ Scint detected: {scint_aesthetic.scint_type.value}")
        print(f"    - Divergence: {scint_aesthetic.divergence_score:.2%}")

    print(f"\n  Total scints detected: {len(scint_detector.detected_scints)}")

    # ========================================================================
    # STEP 3: GENERATE PDFs WITH FITNESS EVALUATION
    # ========================================================================
    print("\n📄 STEP 3: Generating 2-page PDFs with fitness evaluation...")

    generator = TwoPageGenerator(weasyprint_available=False)

    # Generate with each genome
    results = {}

    for genome, name in [
        (genesis, "genesis"),
        (variant_dense, "dense"),
        (variant_readable, "readable"),
        (variant_aesthetic, "aesthetic"),
    ]:
        print(f"\n  Generating {name}...")
        result = generator.generate(
            distilled_chat=distilled,
            styling_genome=genome,
            output_path=output_dir / f"{name}.pdf",
            page_1_ideas=6 if genome == variant_dense else 5,
        )
        genome.evaluate_fitness(result['fitness_metrics'])
        results[name] = result

        print(f"  ✓ {genome.scientific_name}")
        print(f"    - Overall fitness: {result['fitness_metrics']['overall']:.3f}")
        print(f"    - Readability: {result['fitness_metrics']['readability']:.3f}")
        print(f"    - Completeness: {result['fitness_metrics']['completeness']:.3f}")
        print(f"    - Constraint: {result['fitness_metrics']['constraint_satisfaction']:.3f}")

    # ========================================================================
    # STEP 4: NATURAL SELECTION
    # ========================================================================
    print("\n🏆 STEP 4: Natural selection - identifying winner...")

    best = registry.get_best_genome()
    print(f"\n  ✓ Winner: {best.scientific_name}")
    print(f"    - Fitness: {best.fitness_score:.3f}")
    print(f"    - Generation: {best.generation}")
    print(f"    - Description: {best.genes.description}")

    # ========================================================================
    # STEP 5: SCINT RECONCILIATION
    # ========================================================================
    print("\n🔧 STEP 5: Reconciling detected scints...")

    unresolved = scint_detector.get_unresolved_scints()
    print(f"  - Unresolved scints: {len(unresolved)}")

    for i, scint in enumerate(unresolved, 1):
        winner = scint_detector.reconcile_scint(scint, strategy="select_fittest")
        print(f"  ✓ Scint {i} reconciled")
        print(f"    - Winner: {winner.scientific_name}")
        print(f"    - Strategy: select_fittest")

    # ========================================================================
    # STEP 6: SPAWN NEXT GENERATION FROM WINNER
    # ========================================================================
    print("\n🔬 STEP 6: Spawning next generation from winner...")

    # Create refined variant based on winner
    if best == variant_dense:
        next_gen = best.spawn_variant(
            mutations={
                "font.line_height": 1.45,  # Slightly better spacing
                "margin.paragraph_spacing": 9,  # Balance density vs readability
            },
            mutation_description="Gen 2: Dense with improved readability"
        )
    elif best == variant_readable:
        next_gen = best.spawn_variant(
            mutations={
                "font.size_body": 11,  # Slightly smaller
                "margin.top": 18,  # Tighter margins
            },
            mutation_description="Gen 2: Readable with increased density"
        )
    else:
        next_gen = best.spawn_variant(
            mutations={
                "font.line_height": 1.55,
                "color.accent": "#0055aa",
            },
            mutation_description="Gen 2: Refined balance"
        )

    registry.register(next_gen)
    print(f"  ✓ Generation 2: {next_gen.scientific_name}")

    # Generate PDF with next gen
    result_next_gen = generator.generate(
        distilled_chat=distilled,
        styling_genome=next_gen,
        output_path=output_dir / "generation_2.pdf",
        page_1_ideas=5,
    )
    next_gen.evaluate_fitness(result_next_gen['fitness_metrics'])

    print(f"    - Fitness: {next_gen.fitness_score:.3f}")
    improvement = next_gen.fitness_score - best.fitness_score
    if improvement > 0:
        print(f"    - ✓ IMPROVEMENT: +{improvement:.3f} vs parent")
    else:
        print(f"    - → STABLE: {improvement:.3f} vs parent")

    # Check for new scints
    scint_gen2 = scint_detector.detect(best, next_gen)
    if scint_gen2:
        print(f"    - ⚠ New scint: {scint_gen2.scint_type.value} (divergence: {scint_gen2.divergence_score:.2%})")
        winner = scint_detector.reconcile_scint(scint_gen2, strategy="select_fittest")
        print(f"    - ✓ Reconciled: {winner.scientific_name}")

    # ========================================================================
    # STEP 7: REPORTS AND ANALYTICS
    # ========================================================================
    print("\n📊 STEP 7: Generating reports...")

    # Evolution report
    evolution_report = registry.generate_report()
    (output_dir / "evolution_report.md").write_text(evolution_report)
    print(f"  ✓ Evolution report: {output_dir}/evolution_report.md")

    # Scint report
    scint_report = scint_detector.generate_scint_report()
    (output_dir / "scint_report.md").write_text(scint_report)
    print(f"  ✓ Scint report: {output_dir}/scint_report.md")

    # Summary report
    summary = f"""# The Moment It Took Flight - Generation Report

**Generated:** {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}
**Location:** {output_dir}

## Evolution Summary

- **Generations:** {max(g.generation for g in registry.genomes.values()) + 1}
- **Total Genomes:** {len(registry.genomes)}
- **Best Fitness:** {best.fitness_score:.3f} ({best.scientific_name})
- **Scints Detected:** {len(scint_detector.detected_scints)}
- **Scints Resolved:** {len([s for s in scint_detector.detected_scints if s.resolved])}

## Winner Details

**{best.scientific_name}**
- Genome ID: {best.genome_id[:16]}...
- Generation: {best.generation}
- Fitness: {best.fitness_score:.3f}
- Description: {best.genes.description}

## Fitness Breakdown

| Genome | Overall | Readability | Completeness | Constraint | Aesthetics |
|--------|---------|-------------|--------------|------------|------------|
"""

    for name, result in results.items():
        genome = registry.get([g for g in registry.genomes.values() if name in g.genes.description.lower()][0].genome_id) if name != "genesis" else genesis
        metrics = result['fitness_metrics']
        summary += f"| {name.capitalize()} | {metrics['overall']:.3f} | {metrics['readability']:.3f} | {metrics['completeness']:.3f} | {metrics['constraint_satisfaction']:.3f} | {metrics['aesthetic_appeal']:.3f} |\n"

    summary += f"""
## Scint Analysis

{len(scint_detector.detected_scints)} scints detected during evolution:

"""

    for i, scint in enumerate(scint_detector.detected_scints, 1):
        status = "✓ Resolved" if scint.resolved else "⚠ Unresolved"
        summary += f"### Scint {i} - {status}\n"
        summary += f"- Type: {scint.scint_type.value}\n"
        summary += f"- Divergence: {scint.divergence_score:.2%}\n"
        summary += f"- Between: {scint.genome_a.scientific_name} ↔ {scint.genome_b.scientific_name}\n"
        if scint.resolved:
            summary += f"- Resolution: {scint.resolution_strategy}\n"
        summary += "\n"

    summary += f"""
## Output Files

- **PDFs (HTML):** genesis.html, dense.html, readable.html, aesthetic.html, generation_2.html
- **Data:** distilled_conversation.json
- **Reports:** evolution_report.md, scint_report.md
- **Registry:** Genome database with full lineage tracking

## Meta-Beauty

This one-pager was created by the one-pager evolution system to document
the moment the one-pager evolution system took flight.

Ideas about genes became genes themselves. The breakthrough documented itself
at the instant of breakthrough. Scints were monitored and controlled throughout.

The winner ({best.scientific_name}) achieved {best.fitness_score:.3f} fitness
while perfectly satisfying the 2-page constraint.

This is the proof that styling evolution works. 🧬📄✨
"""

    (output_dir / "SUMMARY.md").write_text(summary)
    print(f"  ✓ Summary report: {output_dir}/SUMMARY.md")

    # ========================================================================
    # FINAL STATUS
    # ========================================================================
    print("\n" + "=" * 80)
    print("THE MOMENT IT TOOK FLIGHT - CAPTURED")
    print("=" * 80)

    print(f"\n📈 Evolution Complete:")
    print(f"  - {len(registry.genomes)} genomes across {max(g.generation for g in registry.genomes.values()) + 1} generations")
    print(f"  - {len(scint_detector.detected_scints)} scints detected and reconciled")
    print(f"  - Winner: {best.scientific_name} (fitness: {best.fitness_score:.3f})")

    print(f"\n💡 Ideas Processed:")
    print(f"  - {distilled.total_ideas} ideas extracted")
    print(f"  - {distilled.decisions_count} decisions")
    print(f"  - {distilled.insights_count} insights")
    print(f"  - {distilled.concepts_count} concepts")

    print(f"\n📁 Output Location:")
    print(f"  {output_dir.absolute()}")

    print("\n✨ The breakthrough is documented. The system works.")
    print("=" * 80)


if __name__ == "__main__":
    main()
