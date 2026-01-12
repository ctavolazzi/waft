#!/usr/bin/env python3
"""
Generate Full Session Recap PDF - All Content Included

Uses WAFT tools but renders ALL ideas without page constraints.
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution.chat_distiller import ChatDistiller
from src.waft.evolution.styling_genome import (
    StylingGenome,
    StylingGenomeRegistry,
    StylingGene,
    FontGene,
    MarginGene,
    ColorGene,
    LayoutGene
)
from src.waft.evolution.two_page_generator import TwoPageGenerator
from weasyprint import HTML


def get_session_content() -> str:
    """Get comprehensive session content."""
    # Same content as before - using the full content
    from examples.generate_session_recap_pdf_waft import get_session_content
    return get_session_content()


def render_full_html(distilled_chat, styling_genome, all_ideas):
    """Render HTML with ALL ideas, no page limit."""
    from jinja2 import Template
    
    # Get the template from TwoPageGenerator
    generator = TwoPageGenerator(weasyprint_available=True)
    
    # Split ideas across pages (but include ALL of them)
    # Use a reasonable split - maybe 60/40 or just put them all
    total_ideas = len(all_ideas)
    
    # For a full document, let's put more on first page, rest on subsequent pages
    # But actually, let's just render them all and let WeasyPrint handle pagination
    page_1_ideas = all_ideas[:int(total_ideas * 0.5)]
    page_2_ideas = all_ideas[int(total_ideas * 0.5):]
    
    # Use the generator's render method
    html_content = generator._render_html(
        distilled_chat=distilled_chat,
        styling_genome=styling_genome,
        page_1_ideas=page_1_ideas,
        page_2_ideas=page_2_ideas,
    )
    
    return html_content


def main():
    """Generate full PDF with all content."""
    print("=" * 80)
    print("📄 Generating Full Session Recap PDF (All Content)")
    print("=" * 80)
    
    # Get content
    content = get_session_content()
    
    # Distill content
    print("\n📝 Distilling content into structured ideas...")
    distiller = ChatDistiller()
    distilled = distiller.distill_text(
        content,
        title="WAFT v0.5.3 MVP: Karma Economy & Source Consciousness"
    )
    
    print(f"✅ Extracted {distilled.total_ideas} ideas")
    
    # Get ALL ideas (no limit)
    all_ideas = distilled.get_top_ideas(n=1000, min_importance=0.0)  # Get all ideas
    print(f"✅ Including ALL {len(all_ideas)} ideas in PDF")
    
    # Get or create styling genome
    print("\n🎨 Creating professional styling genome...")
    registry = StylingGenomeRegistry(registry_dir=Path("_genetics/session_recaps"))
    
    styling_genes = StylingGene(
        font=FontGene(
            family="Georgia, serif",
            size_body=11,
            size_h1=20,
            size_h2=16,
            size_h3=13,
            size_code=9,
            line_height=1.6
        ),
        margin=MarginGene(
            top=25,
            bottom=25,
            left=25,
            right=25,
            section_spacing=14,
            paragraph_spacing=8
        ),
        color=ColorGene(
            text="#1a1a1a",
            background="#FFFFFF",
            heading="#000000",
            accent="#2c3e50",
            code_bg="#f8f9fa",
            code_text="#333333",
            border="#dee2e6"
        ),
        layout=LayoutGene(
            columns=1,
            density="normal",
            toc_enabled=False,
            page_numbers=True,
            header_enabled=True,
            footer_enabled=True
        ),
        name="Session Recap Professional Full"
    )
    
    genome = StylingGenome.from_genes(styling_genes)
    registry.register(genome)
    print(f"✅ Using: {genome.scientific_name}")
    
    # Render HTML with ALL ideas
    print("\n📄 Rendering HTML with all content...")
    generator = TwoPageGenerator(weasyprint_available=True)
    
    # Split ideas - put first half on page 1, rest on page 2+
    # But actually, let's use a better split for multi-page
    mid_point = len(all_ideas) // 2
    page_1_ideas = all_ideas[:mid_point]
    page_2_ideas = all_ideas[mid_point:]
    
    html_content = generator._render_html(
        distilled_chat=distilled,
        styling_genome=genome,
        page_1_ideas=page_1_ideas,
        page_2_ideas=page_2_ideas,
    )
    
    # Generate PDF
    output_dir = Path("_work_efforts/session_recaps")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"KARMA_ECONOMY_COMPLETE_FULL_{timestamp}.pdf"
    html_path = output_dir / f"KARMA_ECONOMY_COMPLETE_FULL_{timestamp}.html"
    
    # Save HTML
    html_path.write_text(html_content)
    print(f"✅ HTML saved: {html_path}")
    
    # Generate PDF
    HTML(string=html_content).write_pdf(output_path)
    print(f"✅ PDF generated: {output_path}")
    
    # Count pages
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(output_path))
        page_count = len(reader.pages)
        print(f"📄 Pages: {page_count}")
    except:
        print("📄 Pages: (could not count)")
    
    # Open PDF
    import subprocess
    subprocess.run(["open", str(output_path)])
    
    print("\n✅ PDF opened with ALL content!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
