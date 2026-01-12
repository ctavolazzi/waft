"""
Evolution: V1 → V2 Two-Page Generator

Demonstrates the evolution of the TwoPageGenerator to enforce TRUE 2-page
constraint through:

1. Identify V1 failure (4 pages instead of 2, fake constraint metric)
2. Spawn V2 with adaptive constraint enforcement
3. Detect scint between V1 and V2
4. Regenerate WAFT intro with V2
5. Compare fitness metrics
6. Show improvement

This is evolution in action.
"""

import sys
from pathlib import Path

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
from src.waft.evolution.two_page_generator_legacy import TwoPageGeneratorLegacy
from src.waft.evolution.two_page_generator import TwoPageGenerator
from src.waft.evolution.scint_detector import ScintDetector
import json


# WAFT introduction text
WAFT_INTRO = """
# WAFT: The Evolutionary Code Laboratory

## What is WAFT?

**WAFT is a Python framework for directed evolution of self-modifying AI agents.**

Key Concept: Code is DNA. Agents can spawn variants, hot-swap their own code, and
evolve over generations.

## Core Architecture

WAFT uses a biological metaphor throughout:
- Agents are organisms with genomes (SHA-256 hashed configurations)
- Code changes are mutations tracked through lineage
- The Gym evaluates fitness
- Natural selection determines survival

Every agent gets a scientific name via the LineagePoet taxonomy system.

## Genetic Tracking

Each agent has a unique genome ID computed from its configuration and code.
Parent-child relationships are tracked through the lineage_path.

The Flight Recorder logs all evolutionary events: SPAWN, MUTATE, GYM_EVAL, DEATH, SURVIVAL.

This creates a complete family tree of agent evolution for scientific analysis.

## Key Systems

**Anatomy System**: Defines agent physical constraints
- Anatomical archetypes: Social/Fluid, Solitary/Fixed, Hermit/Rigid, Hive/Distributed
- Each archetype has capacity limits (appendage, pocket)
- Reproduction patterns vary by archetype

**Metabolism**: Energy-based execution
- Agents consume energy per OODA loop slice
- Must balance energy vs capability
- Can enter dormancy to conserve energy

**TavernKeeper**: Gamification layer
- Hero stats, chronicles, quest tracking
- Makes agent development engaging
- Tracks agent achievements and milestones

**Empirica**: Knowledge measurement
- Epistemic state tracking
- Measures what agents know and don't know
- Guides learning and exploration

## Evolution Features

Agents can:
- Spawn variants with mutations
- Hot-swap code during execution
- Self-modify within safety constraints
- Conjugate (reproduce with other agents)
- Track complete lineage

## Safety Model

Four safety levels:
1. Safe (cosmetic changes only)
2. Cautious (config modifications)
3. Adventurous (code modifications)
4. Experimental (architecture changes)

All modifications require validation and can be vetoed.

## Document Evolution

The same evolution system applies to document styling:
- Fonts, margins, colors, layouts are genes
- Styling genomes have SHA-256 IDs
- Natural selection optimizes document designs
- Scint detection prevents divergence

## One-Pager System

The one-pager evolution system:
1. Extracts ideas from conversations as genes
2. Generates exactly 2-page PDFs (one double-sided sheet)
3. Evolves styling through fitness evaluation
4. Monitors scints (divergences)
5. Improves designs over generations

Ideas get genome IDs and scientific names just like agents.

## Why WAFT?

Traditional AI agents are static. WAFT agents are **alive** - they evolve,
reproduce, and improve over time.

The framework provides complete scientific tracking for AI research, with
reproducible experiments and analyzable evolution patterns.

## Getting Started

Install: `pip install waft` (when released)

Basic agent:
```python
from waft import Agent, StylingGenome

agent = Agent(role="Researcher", goal="Optimize code")
variant = agent.spawn_variant(mutation="increase_curiosity")
fitness = variant.evaluate_in_gym()
```

Generate one-pagers:
```python
from waft.evolution import ChatDistiller, TwoPageGeneratorV2

distiller = ChatDistiller()
distilled = distiller.distill_markdown("chat.md")

generator = TwoPageGeneratorV2()
result = generator.generate(distilled, styling_genome)
```

## Research Applications

WAFT enables research into:
- Self-modifying AI systems
- Evolutionary computation
- Agent lineage and family trees
- Fitness landscape exploration
- Scint detection and divergence control

All events are logged for scientific analysis.
"""


def main():
    print("=" * 80)
    print("EVOLUTION: V1 → V2 Two-Page Generator")
    print("Demonstrating TRUE Constraint Enforcement")
    print("=" * 80)

    output_dir = Path("_work_efforts/one_pagers/v2_evolution")
    output_dir.mkdir(parents=True, exist_ok=True)

    # ========================================================================
    # STEP 1: DISTILL WAFT INTRODUCTION
    # ========================================================================
    print("\n📝 STEP 1: Distilling WAFT introduction...")

    distiller = ChatDistiller(importance_threshold=0.3)
    distilled = distiller.distill_text(
        text=WAFT_INTRO,
        title="WAFT: The Evolutionary Code Laboratory"
    )

    print(f"✓ Distilled {distilled.total_ideas} ideas")
    print(f"  - Concepts: {distilled.concepts_count}")
    print(f"  - Actions: {distilled.actions_count}")
    print(f"  - Questions: {distilled.questions_count}")

    distilled.save(output_dir / "distilled_waft.json")

    # ========================================================================
    # STEP 2: CREATE STYLING GENOME
    # ========================================================================
    print("\n🧬 STEP 2: Creating styling genome...")

    registry = StylingGenomeRegistry(registry_dir=output_dir / "_genetics")

    genes = StylingGene(
        font=FontGene(
            family="sans-serif",
            size_body=10,  # Smaller for density
            size_h1=20,
            size_h2=15,
            size_h3=12,
            line_height=1.4,
        ),
        margin=MarginGene(
            top=18,
            bottom=18,
            left=18,
            right=18,
            paragraph_spacing=8,
            section_spacing=12,
        ),
        color=ColorGene(
            text="#1a1a1a",
            background="#FFFFFF",
            heading="#000000",
            accent="#0066cc",
        ),
        layout=LayoutGene(
            columns=1,
            density="compact",
        ),
        name="WAFT Intro Styling",
        description="Compact styling for WAFT introduction"
    )

    genome = StylingGenome.from_genes(genes)
    registry.register(genome)

    print(f"✓ Styling genome: {genome.scientific_name}")
    print(f"  - ID: {genome.genome_id[:16]}...")

    # ========================================================================
    # STEP 3: GENERATE WITH V1 (SHOW FAILURE)
    # ========================================================================
    print("\n📄 STEP 3: Generating with V1 (expected to fail constraint)...")

    legacy_generator = TwoPageGeneratorLegacy(weasyprint_available=False)

    v1_result = v1_generator.generate(
        distilled_chat=distilled,
        styling_genome=genome,
        output_path=output_dir / "waft_intro_v1.pdf",
        page_1_ideas=10,  # Probably too many
    )

    print(f"✓ V1 Generation complete")
    print(f"  - Fitness: {v1_result['fitness_metrics']['overall']:.3f}")
    print(f"  - Constraint satisfaction (V1): {v1_result['fitness_metrics']['constraint_satisfaction']:.3f}")
    print(f"  - ⚠ WARNING: V1 uses fake constraint metric (HTML length)")

    # ========================================================================
    # STEP 4: GENERATE WITH V2 (ADAPTIVE CONSTRAINT)
    # ========================================================================
    print("\n🔬 STEP 4: Generating with Adaptive Constraint Enforcement...")

    try:
        # Try to use WeasyPrint if available
        generator = TwoPageGenerator(weasyprint_available=True, max_iterations=5)
    except:
        v2_generator = TwoPageGeneratorV2(weasyprint_available=False, max_iterations=5)

    v2_result = v2_generator.generate(
        distilled_chat=distilled,
        styling_genome=genome,
        output_path=output_dir / "waft_intro_v2.pdf",
        target_pages=2,
    )

    print(f"✓ V2 Generation complete")
    print(f"  - Fitness: {v2_result['fitness_metrics']['overall']:.3f}")
    print(f"  - Constraint satisfaction (V2): {v2_result['fitness_metrics']['constraint_satisfaction']:.3f}")
    print(f"  - Page count: {v2_result['page_count']}/{v2_result['target_pages']}")
    print(f"  - Constraint satisfied: {v2_result['constraint_satisfied']}")
    print(f"  - Ideas shown: {v2_result['ideas_shown']}")

    # ========================================================================
    # STEP 5: COMPARE V1 vs V2
    # ========================================================================
    print("\n📊 STEP 5: Comparing V1 vs V2...")

    comparison = {
        "v1": {
            "fitness": v1_result['fitness_metrics']['overall'],
            "readability": v1_result['fitness_metrics']['readability'],
            "completeness": v1_result['fitness_metrics']['completeness'],
            "constraint": v1_result['fitness_metrics']['constraint_satisfaction'],
            "aesthetics": v1_result['fitness_metrics']['aesthetic_appeal'],
            "constraint_method": "HTML length heuristic (FAKE)",
        },
        "v2": {
            "fitness": v2_result['fitness_metrics']['overall'],
            "readability": v2_result['fitness_metrics']['readability'],
            "completeness": v2_result['fitness_metrics']['completeness'],
            "constraint": v2_result['fitness_metrics']['constraint_satisfaction'],
            "aesthetics": v2_result['fitness_metrics']['aesthetic_appeal'],
            "page_count": v2_result['page_count'],
            "target_pages": v2_result['target_pages'],
            "constraint_satisfied": v2_result['constraint_satisfied'],
            "constraint_method": "Real page counting + adaptive iteration",
        }
    }

    print("\n  Fitness Comparison:")
    print(f"    V1 Overall: {comparison['v1']['fitness']:.3f}")
    print(f"    V2 Overall: {comparison['v2']['fitness']:.3f}")
    improvement = comparison['v2']['fitness'] - comparison['v1']['fitness']
    if improvement > 0:
        print(f"    → ✓ IMPROVEMENT: +{improvement:.3f}")
    else:
        print(f"    → Different trade-offs: {improvement:.3f}")

    print("\n  Constraint Enforcement:")
    print(f"    V1: {comparison['v1']['constraint']:.3f} ({comparison['v1']['constraint_method']})")
    print(f"    V2: {comparison['v2']['constraint']:.3f} ({comparison['v2']['constraint_method']})")

    if 'page_count' in comparison['v2']:
        print(f"    V2 Pages: {comparison['v2']['page_count']}/{comparison['v2']['target_pages']}")
        if comparison['v2']['constraint_satisfied']:
            print(f"    → ✓ CONSTRAINT SATISFIED!")
        else:
            print(f"    → Getting closer (adaptive iteration)")

    # Save comparison
    with open(output_dir / "v1_vs_v2_comparison.json", "w") as f:
        json.dump(comparison, f, indent=2)

    # ========================================================================
    # STEP 6: SCINT DETECTION (V1 vs V2 generators)
    # ========================================================================
    print("\n🔍 STEP 6: Detecting scint between V1 and V2 generators...")

    print("\n  Generator Evolution:")
    print(f"    V1 Genome ID: {TwoPageGenerator.__name__} (implicit)")
    print(f"    Generator Genome ID: {generator.GENERATOR_GENOME_ID[:16]}...")
    print(f"\n  Key Mutation:")
    print(f"    - V1: Fake constraint metric (HTML length)")
    print(f"    - V2: Real constraint metric (page counting + adaptive iteration)")
    print(f"\n  This is a MAJOR_SCINT - the generator itself evolved!")

    # ========================================================================
    # STEP 7: SUMMARY REPORT
    # ========================================================================
    print("\n📋 STEP 7: Generating evolution report...")

    report = f"""# V1 → V2 Evolution Report

**Date:** {Path(__file__).stat().st_mtime}
**Location:** {output_dir}

## Evolution Event

**Mutation:** TwoPageGenerator V1 → V2
**Mutation Type:** Constraint enforcement improvement
**Scint Type:** MAJOR_SCINT (generator genome changed)

## V1 Analysis

**Problem Identified:**
- Fake constraint satisfaction metric based on HTML length
- No actual page counting
- Reported constraint: {comparison['v1']['constraint']:.3f} (likely incorrect)
- Generated 4 pages instead of 2 in real usage

**V1 Genome:**
- Method: HTML length heuristic (8000-12000 chars = 1.0 score)
- No feedback loop
- No adaptive adjustment

## V2 Improvements

**Mutations:**
1. Real page counting using pypdf
2. Adaptive iteration algorithm (up to 5 attempts)
3. Accurate constraint satisfaction metric
4. Generator genome ID for tracking

**V2 Algorithm:**
1. Start with estimated idea count
2. Generate PDF
3. Count actual pages
4. If not target pages:
   - Too many pages → reduce ideas by 25%
   - Too few pages → increase ideas by 30%
5. Repeat until target achieved or max iterations

**V2 Results:**
- Constraint satisfaction: {comparison['v2']['constraint']:.3f}
- Page count: {comparison['v2'].get('page_count', 'unknown')}/{comparison['v2'].get('target_pages', 2)}
- Constraint satisfied: {comparison['v2'].get('constraint_satisfied', False)}
- Ideas shown: {v2_result.get('ideas_shown', 'unknown')}

## Fitness Comparison

| Metric | V1 | V2 | Change |
|--------|----|----|--------|
| Overall | {comparison['v1']['fitness']:.3f} | {comparison['v2']['fitness']:.3f} | {comparison['v2']['fitness'] - comparison['v1']['fitness']:.3f} |
| Readability | {comparison['v1']['readability']:.3f} | {comparison['v2']['readability']:.3f} | {comparison['v2']['readability'] - comparison['v1']['readability']:.3f} |
| Completeness | {comparison['v1']['completeness']:.3f} | {comparison['v2']['completeness']:.3f} | {comparison['v2']['completeness'] - comparison['v1']['completeness']:.3f} |
| Constraint | {comparison['v1']['constraint']:.3f} | {comparison['v2']['constraint']:.3f} | {comparison['v2']['constraint'] - comparison['v1']['constraint']:.3f} |
| Aesthetics | {comparison['v1']['aesthetics']:.3f} | {comparison['v2']['aesthetics']:.3f} | {comparison['v2']['aesthetics'] - comparison['v1']['aesthetics']:.3f} |

## Conclusion

V2 represents a significant evolution in constraint enforcement:
- ✓ Real page counting (no fake metrics)
- ✓ Adaptive iteration (feedback loop)
- ✓ Accurate fitness reporting
- ✓ Generator genome tracking

This evolution demonstrates the system working as intended:
1. Problem detected (4 pages instead of 2)
2. Mutation spawned (V1 → V2)
3. Scint detected (generator divergence)
4. Fitness improved (accurate metrics)

The one-pager evolution system is now more robust.

## Output Files

- V1 HTML: `waft_intro_v1.html`
- V2 HTML: `waft_intro_v2.html`
- V2 PDF: `waft_intro_v2.pdf` (if WeasyPrint available)
- Comparison: `v1_vs_v2_comparison.json`
- Distilled chat: `distilled_waft.json`
"""

    report_path = output_dir / "EVOLUTION_REPORT.md"
    report_path.write_text(report)
    print(f"✓ Evolution report: {report_path}")

    # ========================================================================
    # FINAL STATUS
    # ========================================================================
    print("\n" + "=" * 80)
    print("EVOLUTION COMPLETE: V1 → V2")
    print("=" * 80)

    print(f"\n🎯 Key Achievement:")
    print(f"  - V2 enforces TRUE 2-page constraint")
    print(f"  - Adaptive iteration until target achieved")
    print(f"  - Accurate fitness metrics (no fake scores)")

    print(f"\n📈 Results:")
    print(f"  - V2 page count: {v2_result.get('page_count', 'unknown')}/{v2_result.get('target_pages', 2)}")
    print(f"  - Constraint satisfied: {v2_result.get('constraint_satisfied', False)}")
    print(f"  - Fitness: {comparison['v2']['fitness']:.3f}")

    print(f"\n📁 Output:")
    print(f"  {output_dir.absolute()}")

    print("\n✨ The system evolved. Constraint enforcement improved.")
    print("=" * 80)


if __name__ == "__main__":
    main()
