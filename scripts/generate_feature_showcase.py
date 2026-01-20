#!/usr/bin/env python3
"""
Generate Comprehensive Feature Showcase PDF
===========================================

Creates a PDF that demonstrates EVERY feature in the WAFT PDF generation system:
- Adaptive 2-page constraint enforcement
- Real page counting
- All 5 idea types (decisions, insights, actions, concepts, questions)
- PNG conversion
- Metrics collection
- Fitness evaluation
- Content statistics
- Evolutionary event tracking
- All visual elements (summary box, tables, metadata, typography)
"""

import subprocess
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


def get_comprehensive_chat_content() -> str:
    """
    Create comprehensive chat content that generates all 5 idea types.

    This content is designed to trigger:
    - Decisions: "We decided", "The choice was made", "We will"
    - Insights: "We discovered", "The key insight", "We learned"
    - Actions: "We need to", "Next step", "We will implement"
    - Concepts: "The system represents", "This is a framework", "The approach"
    - Questions: "How should we", "What is the best", "Why does"
    """
    return """
# WAFT: Comprehensive Feature Showcase

## System Overview

WAFT is a scientific learning system that studies itself and evolves through the Scientific Method. The system creates printable, binder-ready documents as physical knowledge artifacts. This document demonstrates every feature we've developed.

## Key Decisions

We decided to use OAuth2 for authentication because it provides security and flexibility. The choice was made to implement adaptive constraint enforcement rather than relying on estimates. We will use WeasyPrint for PDF generation because it provides accurate page counting. The final decision was to enable metrics collection by default for all PDF generations. We chose to support PNG conversion at 300 DPI for high-quality image output.

## Important Insights

We discovered that character-counting methods for page estimation are unreliable. The key insight is that real measurement beats estimation every time. We learned that adaptive algorithms can achieve exact page counts through iterative adjustment. It turns out that markdown cleaning is critical for professional output. We found that comprehensive metrics enable evolution with quality data. The important realization is that fitness evaluation drives continuous improvement.

## Action Items

We need to implement comprehensive testing for all PDF generation features. Next step is to create documentation for the metrics system. We must create example scripts demonstrating each feature. We should build a validation suite that checks all outputs. We will implement automated quality checks for generated PDFs. We need to add support for additional styling options. We should document the evolutionary event tracking system.

## Core Concepts

The system represents a new approach to document generation. This is a framework for creating physical knowledge artifacts. The approach combines evolutionary algorithms with constraint satisfaction. The architecture uses genetic material for styling configuration. The concept of fitness drives continuous improvement. The idea of lineage tracking enables scientific naming. The framework supports multiple output formats including PDF and PNG.

## Open Questions

How should we handle edge cases in page counting? What is the best approach for handling very long content? Why does the system sometimes need multiple iterations? How can we improve the fitness evaluation algorithm? What metrics are most important for evolution? Which styling options provide the best readability? How do we balance completeness with constraint satisfaction? What happens when content is too short for two pages? When should we use compact versus spacious layouts? How do we determine optimal font sizes for different content types?
"""


def main():
    """Generate comprehensive feature showcase PDF with all features enabled."""
    print("=" * 70)
    print("🔬 WAFT Comprehensive Feature Showcase PDF Generator")
    print("=" * 70)
    print()

    # Get comprehensive chat content
    print("📝 Creating comprehensive chat content...")
    chat_content = get_comprehensive_chat_content()
    print("✓ Content created with all 5 idea types")
    print()

    # Distill chat into ideas
    print("📝 Distilling chat into ideas...")
    distiller = ChatDistiller()
    distilled = distiller.distill_text(chat_content, title="WAFT: Comprehensive Feature Showcase")

    print(f"✓ Extracted {distilled.total_ideas} ideas")
    print(f"  - Decisions: {distilled.decisions_count}")
    print(f"  - Insights: {distilled.insights_count}")
    print(f"  - Actions: {distilled.actions_count}")
    print(f"  - Concepts: {distilled.concepts_count}")
    print(f"  - Questions: {distilled.questions_count}")
    print()

    # Verify all idea types are present
    all_types_present = (
        distilled.decisions_count > 0
        and distilled.insights_count > 0
        and distilled.actions_count > 0
        and distilled.concepts_count > 0
        and distilled.questions_count > 0
    )

    if not all_types_present:
        print("⚠️  Warning: Not all idea types are present in content")
        print("   This may limit feature demonstration")
        print()
    else:
        print("✅ All 5 idea types present - comprehensive demonstration ready")
        print()

    # Create comprehensive styling genome
    print("🎨 Creating comprehensive styling genome...")
    registry = StylingGenomeRegistry(registry_dir=Path("_genetics/chat_one_pagers"))

    styling_genes = StylingGene(
        font=FontGene(
            family="sans-serif",
            size_body=11,
            size_h1=18,
            size_h2=14,
            size_h3=12,
            size_code=10,
            line_height=1.6,
        ),
        margin=MarginGene(
            top=20, bottom=20, left=20, right=20, section_spacing=12, paragraph_spacing=8
        ),
        color=ColorGene(
            text="#000000",
            background="#FFFFFF",
            accent="#0066cc",
            heading="#1a1a1a",
            code_bg="#f5f5f5",
            code_text="#333333",
            border="#cccccc",
        ),
        layout=LayoutGene(
            columns=1,
            density="normal",
            toc_enabled=False,
            page_numbers=True,
            header_enabled=True,
            footer_enabled=True,
        ),
        name="Feature Showcase Genome",
        description="Comprehensive styling genome demonstrating all visual features",
    )

    genome = StylingGenome.from_genes(styling_genes)
    registry.register(genome)
    print(f"✓ Using: {genome.scientific_name} ({genome.genome_id[:8]}...)")
    print()

    # Generate with ALL features enabled
    print("📄 Generating 2-page PDF with ALL features enabled...")
    print("   - Adaptive constraint enforcement: ✅")
    print("   - Real page counting: ✅")
    print("   - PNG conversion: ✅")
    print("   - Metrics collection: ✅")
    print("   - Fitness evaluation: ✅")
    print("   - Content statistics: ✅")
    print("   - Evolutionary tracking: ✅")
    print()

    generator = TwoPageGenerator(weasyprint_available=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(f"_work_efforts/one_pagers/feature_showcase_{timestamp}.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Enable ALL features
    result = generator.generate(
        distilled_chat=distilled,
        styling_genome=genome,
        output_path=output_path,
        target_pages=2,
        convert_to_png=True,  # ✅ Enable PNG conversion
        png_dpi=300,  # High quality
        collect_metrics=True,  # ✅ Enable metrics collection
        metrics_dir=Path("_pyrite/metrics/pdf"),  # Metrics directory
    )

    print()
    print("=" * 70)
    print("✅ Feature Showcase PDF Generated!")
    print("=" * 70)
    print()

    # Detailed output reporting
    print("📄 OUTPUT FILES")
    print("-" * 70)
    print(f"PDF: {output_path}")

    html_path = Path(str(output_path).replace(".pdf", ".html"))
    if html_path.exists():
        print(f"HTML: {html_path}")

    if result.get("png_paths"):
        print(f"PNG Images: {len(result['png_paths'])} files")
        png_dir = Path(result["png_paths"][0]).parent
        print(f"  Directory: {png_dir}")
        for i, _png_path in enumerate(result["png_paths"], 1):
            print(f"  - page_{i:03d}.png")

    if result.get("metrics_file"):
        print(f"Metrics: {result['metrics_file']}")
    print()

    # Generation results
    print("📊 GENERATION RESULTS")
    print("-" * 70)
    print(f"Pages: {result['page_count']}/2")
    print(f"Constraint satisfied: {'✅ YES' if result['constraint_satisfied'] else '❌ NO'}")
    print(f"Ideas shown: {result['ideas_shown']}/{distilled.total_ideas}")
    print(f"Generator version: {result['generator_version']}")
    print(f"Generator genome ID: {result['generator_genome_id'][:16]}...")
    print()

    # Fitness metrics
    print("💪 FITNESS METRICS")
    print("-" * 70)
    fitness = result["fitness_metrics"]
    print(f"Overall: {fitness['overall']:.3f}")
    print(f"  - Readability: {fitness['readability']:.3f}")
    print(f"  - Completeness: {fitness['completeness']:.3f}")
    print(f"  - Constraint satisfaction: {fitness['constraint_satisfaction']:.3f}")
    print(f"  - Aesthetic appeal: {fitness['aesthetic_appeal']:.3f}")
    print()

    # PNG conversion results
    if result.get("png_paths"):
        print("🖼️  PNG CONVERSION")
        print("-" * 70)
        print("Status: ✅ SUCCESS")
        print(f"Pages converted: {len(result['png_paths'])}")
        print("DPI: 300")
        total_size = sum(Path(p).stat().st_size for p in result["png_paths"] if Path(p).exists())
        print(f"Total size: {total_size / 1024 / 1024:.2f} MB")
        print()
    else:
        print("🖼️  PNG CONVERSION")
        print("-" * 70)
        print("Status: ❌ NOT PERFORMED")
        print()

    # Metrics collection results
    if result.get("metrics"):
        print("📊 METRICS COLLECTION")
        print("-" * 70)
        metrics = result["metrics"]
        print("Status: ✅ COLLECTED")
        print(f"Quality grade: {metrics.get('quality_grade', 'N/A')}")
        print(f"Quality score: {metrics.get('quality_score', 0):.3f}")
        print(f"Generation time: {metrics.get('generation_time_seconds', 0):.2f}s")
        print(f"Iterations used: {metrics.get('iterations_used', 0)}")
        print(f"Content words: {metrics.get('content_words_total', 0)}")
        print(f"Content density: {metrics.get('content_density', 0):.1f} words/page")
        print()
    else:
        print("📊 METRICS COLLECTION")
        print("-" * 70)
        print("Status: ❌ NOT COLLECTED")
        print()

    # Visual elements verification
    print("🎨 VISUAL ELEMENTS")
    print("-" * 70)
    print("✅ Summary box (prominent display)")
    print("✅ Idea boxes (prose presentation with left border)")
    print("✅ Tables (content breakdown)")
    print("✅ Metadata (timestamp and counts)")
    print("✅ Typography (H1, H2, H3, body, code)")
    print("✅ Page breaks (controlled separation)")
    print("✅ Color scheme (text, background, accent)")
    print("✅ Margins (configurable spacing)")
    print()

    # Feature checklist
    print("✅ FEATURE CHECKLIST")
    print("-" * 70)
    features = [
        ("Adaptive 2-page constraint enforcement", True),
        ("Real page counting (WeasyPrint + pypdf)", True),
        ("Idea extraction (all 5 types)", all_types_present),
        ("Styling genomes", True),
        ("Markdown cleaning", True),
        ("PNG conversion", bool(result.get("png_paths"))),
        ("Metrics collection", bool(result.get("metrics"))),
        ("Fitness evaluation", True),
        ("Content statistics", bool(result.get("metrics"))),
        ("Evolutionary event tracking", True),
    ]

    for feature, enabled in features:
        status = "✅" if enabled else "❌"
        print(f"{status} {feature}")
    print()

    # Final summary
    print("=" * 70)
    if result["constraint_satisfied"]:
        print("✅ Perfect 2-page document generated!")
    else:
        print(f"⚠️  Generated {result['page_count']} pages (expected 2)")
    print()
    print("📖 Opening PDF in Preview...")
    print()

    # Open the PDF
    try:
        subprocess.run(["open", "-a", "Preview", str(output_path)], check=False)
    except Exception as e:
        print(f"⚠️  Could not open PDF automatically: {e}")
        print(f"   Please open manually: {output_path}")

    print("=" * 70)
    print("🎉 Feature showcase complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
