#!/usr/bin/env python3
"""
Create One-Pager from Chat using Evolution System
==================================================

Creates a 2-page one-pager PDF from the current chat session using the
evolved system with TRUE constraint enforcement and genomic tracking.
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution import (
    ChatDistiller,
    ColorGene,
    FontGene,
    LayoutGene,
    MarginGene,
    StylingGene,
    StylingGenome,
    StylingGenomeRegistry,
    TwoPageGenerator,
)


def get_chat_content() -> str:
    """
    Extract chat content from this session in clear prose.

    This session focused on implementing the WAFT Kernel Boot Sequence,
    integrating with existing infrastructure, and enhancing the status system.
    """
    return """
# WAFT Kernel Boot Sequence Implementation

## What We Built

We implemented the complete WAFT Kernel Boot Sequence, which enables the kernel to acknowledge its identity, perform self-awareness checks, and integrate with the existing status system. The kernel is the central operating intelligence that oversees directed evolution of self-modifying AI agents.

## Key Components

We extended the EvolutionaryEventType enum to include BOOT and STATUS_CHECK event types. This allows the kernel to log its lifecycle events to the flight recorder using the existing TheObserver system. We created a new kernel module with an epistemic phase calculator that determines the current phase from Empirica state: Data Gathering, Exploration, Synthesis, Evolution, or Transition.

## Status System Enhancement

We significantly enhanced the status script with kernel awareness. The status check now includes epistemic state from Empirica, showing knowledge percentage, uncertainty percentage, coverage, and the current epistemic phase. We added comprehensive path validation throughout to prevent security vulnerabilities, and all operations now handle missing components gracefully.

## Integration Approach

Instead of creating new systems, we integrated with existing infrastructure. We use TheObserver for flight recorder logging, extend the existing EvolutionaryEventType enum, and integrate with EmpiricaManager for epistemic state. This approach avoids duplication and leverages proven systems.

## Security Improvements

We added path validation on all file operations to prevent path traversal attacks. Work effort directory names are validated, git file paths are checked, and _pyrite paths are verified. All inputs are validated throughout the system.

## Boot Command

We created a new boot command handler that executes the complete boot sequence: identity acknowledgment, initial status check, epistemic phase declaration, and boot event logging. The command documentation provides clear instructions for using the kernel.

## Results

The implementation is complete and ready for testing. All components integrate properly with existing systems. The kernel can now acknowledge its identity, perform status checks with epistemic awareness, and log events to the flight recorder. The system handles errors gracefully and validates all paths for security.
"""


def main():
    """Create one-pager from chat session using evolution system."""
    print("🔬 Creating one-pager from chat session using evolution system...")
    print()

    # Get chat content
    chat_content = get_chat_content()

    # Distill chat into ideas
    print("📝 Distilling chat into ideas...")
    distiller = ChatDistiller()
    distilled = distiller.distill_text(chat_content, title="WAFT Kernel Implementation")

    print(f"✓ Extracted {distilled.total_ideas} ideas")
    print(f"  - Concepts: {distilled.concepts_count}")
    print(f"  - Actions: {distilled.actions_count}")
    print(f"  - Decisions: {distilled.decisions_count}")
    print(f"  - Insights: {distilled.insights_count}")
    print(f"  - Questions: {distilled.questions_count}")
    print()

    # Get or create styling genome
    print("🎨 Creating styling genome...")
    registry = StylingGenomeRegistry(registry_dir=Path("_genetics/chat_one_pagers"))

    # Create genesis genome if needed
    genesis_genes = StylingGene(
        font=FontGene(family="sans-serif", size_body=11),
        margin=MarginGene(top=20, bottom=20, left=20, right=20),
        color=ColorGene(text="#000000", background="#FFFFFF", accent="#0066cc"),
        layout=LayoutGene(columns=1, density="normal"),
        name="Chat One-Pager Genesis",
    )
    genome = StylingGenome.from_genes(genesis_genes)
    registry.register(genome)
    print(f"✓ Using: {genome.scientific_name} ({genome.genome_id[:8]}...)")
    print()

    # Generate with adaptive constraint enforcement
    print("📄 Generating 2-page PDF with adaptive constraint enforcement...")
    generator = TwoPageGenerator(weasyprint_available=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(f"_work_efforts/one_pagers/chat_session_{timestamp}.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Enable metrics collection for evolution tracking
    # Set to True to collect comprehensive metrics for every PDF generation
    collect_metrics = False  # Change to True to enable metrics

    result = generator.generate(
        distilled_chat=distilled,
        styling_genome=genome,
        output_path=output_path,
        target_pages=2,
        collect_metrics=collect_metrics,  # Enable metrics collection
    )

    print()
    print("=" * 60)
    print("✅ Chat One-Pager Created!")
    print("=" * 60)
    print(f"📄 Output: {output_path}")
    print(f"📊 Pages: {result.get('page_count', 'N/A')}/2")

    constraint_satisfied = result.get("constraint_satisfied", result.get("page_count", 0) == 2)
    print(f"🎯 Constraint satisfied: {constraint_satisfied}")

    if "fitness_metrics" in result:
        fitness = result["fitness_metrics"]
        print(f"💪 Fitness: {fitness.get('overall', 'N/A')}")
        if isinstance(fitness.get("overall"), (int, float)):
            print(f"   - Readability: {fitness.get('readability', 'N/A')}")
            print(f"   - Completeness: {fitness.get('completeness', 'N/A')}")
            print(f"   - Constraint: {fitness.get('constraint_satisfaction', 'N/A')}")
            print(f"   - Aesthetics: {fitness.get('aesthetic_appeal', 'N/A')}")

    if "ideas_shown" in result:
        print(f"🧬 Ideas shown: {result['ideas_shown']}/{distilled.total_ideas}")

    if "generator_version" in result:
        print(f"🔬 Generator: {result['generator_version']}")

    # Show metrics if collected
    if collect_metrics and "metrics" in result:
        metrics = result["metrics"]
        print(f"📊 Quality Grade: {metrics.get('quality_grade', 'N/A')}")
        print(f"📊 Quality Score: {metrics.get('quality_score', 'N/A')}")
        print(f"📊 Metrics saved: {result.get('metrics_file', 'N/A')}")

    print()

    if constraint_satisfied:
        print("✅ Perfect 2-page document!")
    else:
        page_count = result.get("page_count", 0)
        print(f"⚠️ Generated {page_count} pages (expected 2)")

    print()
    print("Ready for printing and binder storage!")
    print()

    # Convert PDF to PNG images (one per page)
    print("🖼️  Converting PDF to PNG images...")
    try:
        from src.waft.evolution.pdf_image_converter import convert_pdf_to_images

        png_dir = output_path.parent / f"{output_path.stem}_pages"
        png_paths = convert_pdf_to_images(output_path, output_dir=png_dir, dpi=300)

        print(f"✓ Created {len(png_paths)} PNG images")
        print(f"📁 Images saved to: {png_dir}")
        for i, png_path in enumerate(png_paths, 1):
            print(f"   - {png_path.name} (page {i})")
        print()
    except Exception as e:
        print(f"⚠️  Could not convert to PNG: {e}")
        print("   Install pdf2image: pip install pdf2image")
        print()

    # Open the PDF
    import subprocess

    subprocess.run(["open", "-a", "Preview", str(output_path)])

    print("📖 PDF opened in Preview")


if __name__ == "__main__":
    main()
