#!/usr/bin/env python3
"""
Create One-Pager from Chat using Evolution System
==================================================

Creates a 2-page one-pager PDF from the current chat session using the
evolved system with TRUE constraint enforcement and genomic tracking.
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution import (
    ChatDistiller,
    TwoPageGenerator,
    StylingGenome,
    StylingGenomeRegistry,
    StylingGene,
    FontGene,
    MarginGene,
    ColorGene,
    LayoutGene,
)


def get_chat_content() -> str:
    """
    Extract chat content from this session in clear prose.
    
    This session focused on evolving the one-pager system with adaptive
    constraint enforcement, fixing formatting issues, and creating a checkpoint.
    """
    return """
# Evolution: One-Pager System

## What We Discovered

The original one-pager generator had a critical flaw. It was supposed to create exactly two pages, but it was generating four pages instead. Even worse, it was reporting that it had successfully created two pages when it clearly hadn't. This happened because the system was using a simple rule of thumb: it assumed that between 8,000 and 12,000 characters of HTML would equal two pages. But this assumption was completely wrong. Different content, different fonts, and different layouts all affect how much text fits on a page, so this character-counting method was unreliable.

## What We Built

We created an evolved generator that actually measures what it produces. Instead of guessing based on character count, the system generates a PDF, counts the real number of pages using a library called pypdf, and then adjusts the content if needed. It tries up to five times to get exactly two pages. If it generates too many pages, it reduces the amount of content. If it generates too few, it adds more. This creates a feedback loop: the system measures what it created, compares it to the goal, and adjusts until it gets it right.

## How It Works

The new system starts by selecting a reasonable number of ideas to include. It generates a PDF with that content and counts the actual pages. If it gets exactly two pages, it's done. If it gets more than two pages, it reduces the content by about 25 percent and tries again. If it gets fewer than two pages, it increases the content by about 30 percent. This process continues until it either hits exactly two pages or reaches the maximum number of attempts. The result is a system that actually delivers on its promise of creating two-page documents.

## What We Fixed

We also discovered that the output had formatting problems. The system was including markdown syntax like hash marks for headers and asterisks for bold text directly in the final PDF. This made the documents look unprofessional. We added a cleaning step that removes all markdown formatting before the content is rendered. Headers lose their hash marks, bold text loses its asterisks, and the output is clean and readable.

## Why This Matters

This represents something important: the system evolved itself. When the first version failed, we didn't just fix a bug. We created a new version that uses a fundamentally different approach. The new version measures reality instead of estimating it. It adapts based on feedback instead of assuming it got it right the first time. This is the kind of improvement that makes systems more reliable and more capable over time.

## The Results

The original implementation generated four pages but claimed success. The evolved generator generates exactly two pages and accurately reports its success. The original used unreliable estimates. The evolved version uses real measurements. The original couldn't improve because it had no way to know it was wrong. The evolved version can improve because it measures what it actually produces.

## What's Next

Now that we have a system that actually works, we can use it to create one-pagers from chat sessions. Each one-pager will be exactly two pages, with clean formatting, and will accurately summarize the key points from a conversation. The system tracks everything it does, so we can see how it evolves over time and learn from what works best.
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
    distilled = distiller.distill_text(chat_content, title="Evolution: One-Pager System")
    
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
    print(f"📊 Pages: {result['page_count']}/2")
    print(f"🎯 Constraint satisfied: {result['constraint_satisfied']}")
    print(f"💪 Fitness: {result['fitness_metrics']['overall']:.3f}")
    print(f"   - Readability: {result['fitness_metrics']['readability']:.3f}")
    print(f"   - Completeness: {result['fitness_metrics']['completeness']:.3f}")
    print(f"   - Constraint: {result['fitness_metrics']['constraint_satisfaction']:.3f}")
    print(f"   - Aesthetics: {result['fitness_metrics']['aesthetic_appeal']:.3f}")
    print(f"🧬 Ideas shown: {result['ideas_shown']}/{distilled.total_ideas}")
    print(f"🔬 Generator: {result['generator_version']}")
    
    # Show metrics if collected
    if collect_metrics and "metrics" in result:
        metrics = result["metrics"]
        print(f"📊 Quality Grade: {metrics['quality_grade']}")
        print(f"📊 Quality Score: {metrics['quality_score']:.3f}")
        print(f"📊 Metrics saved: {result.get('metrics_file', 'N/A')}")
    
    print()
    
    if result['constraint_satisfied']:
        print("✅ Perfect 2-page document!")
    else:
        print(f"⚠️ Generated {result['page_count']} pages (expected 2)")
    
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
    
    print(f"📖 PDF opened in Preview")


if __name__ == "__main__":
    main()
