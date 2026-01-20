#!/usr/bin/env python3
"""
Generate Premium Session Recap PDF - Peak Styling Priority

Creates a beautifully styled PDF with premium typography, spacing, and design.
No constraints - just peak visual quality.
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from weasyprint import HTML

from src.waft.evolution.chat_distiller import ChatDistiller
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


def get_session_content() -> str:
    """Get comprehensive session content."""
    from examples.generate_session_recap_pdf_waft import get_session_content

    return get_session_content()


def main():
    """Generate premium PDF with peak styling."""
    print("=" * 80)
    print("🎨 Generating Premium Session Recap PDF - Peak Styling Priority")
    print("=" * 80)

    # Get content
    content = get_session_content()

    # Distill content
    print("\n📝 Distilling content into structured ideas...")
    distiller = ChatDistiller()
    distilled = distiller.distill_text(
        content, title="WAFT v0.5.3 MVP: Karma Economy & Source Consciousness"
    )

    print(f"✅ Extracted {distilled.total_ideas} ideas")

    # Get ALL ideas
    all_ideas = distilled.get_top_ideas(n=1000, min_importance=0.0)
    print(f"✅ Including ALL {len(all_ideas)} ideas")

    # Create PREMIUM styling genome - peak quality
    print("\n🎨 Creating PREMIUM styling genome (peak priority)...")
    registry = StylingGenomeRegistry(registry_dir=Path("_genetics/session_recaps"))

    # Premium styling with beautiful typography
    styling_genes = StylingGene(
        font=FontGene(
            family="'Minion Pro', 'Palatino Linotype', 'Book Antiqua', 'Palatino', serif",  # Premium serif
            size_body=12,  # Comfortable reading size
            size_h1=28,  # Dramatic, elegant heading
            size_h2=20,  # Clear section headers
            size_h3=15,  # Subsection headers
            size_code=10,  # Readable code
            line_height=1.7,  # Generous line spacing for readability
        ),
        margin=MarginGene(
            top=30,  # Generous top margin
            bottom=30,  # Generous bottom margin
            left=35,  # Wide left margin for elegance
            right=35,  # Wide right margin
            section_spacing=20,  # Clear section separation
            paragraph_spacing=10,  # Comfortable paragraph spacing
        ),
        color=ColorGene(
            text="#1a1a1a",  # Rich, deep black (not pure black)
            background="#FFFFFF",  # Pure white
            heading="#000000",  # Pure black for headings (maximum contrast)
            accent="#1a5490",  # Deep, professional blue
            code_bg="#f8f9fa",  # Subtle gray background
            code_text="#2c3e50",  # Dark gray-blue for code
            border="#d1d5db",  # Soft gray borders
        ),
        layout=LayoutGene(
            columns=1,
            density="comfortable",  # Generous spacing
            toc_enabled=False,
            page_numbers=True,
            header_enabled=True,
            footer_enabled=True,
        ),
        name="Premium Session Recap - Peak Styling",
    )

    genome = StylingGenome.from_genes(styling_genes)
    registry.register(genome)
    print(f"✅ Created premium genome: {genome.scientific_name}")
    print("   Font: Premium serif with generous spacing")
    print("   Colors: Deep professional palette")
    print("   Margins: Generous, elegant spacing")

    # Render HTML with ALL ideas using premium styling
    print("\n📄 Rendering HTML with premium styling...")
    generator = TwoPageGenerator(weasyprint_available=True)

    # Split ideas evenly for multi-page flow
    mid_point = len(all_ideas) // 2
    page_1_ideas = all_ideas[:mid_point]
    page_2_ideas = all_ideas[mid_point:]

    html_content = generator._render_html(
        distilled_chat=distilled,
        styling_genome=genome,
        page_1_ideas=page_1_ideas,
        page_2_ideas=page_2_ideas,
    )

    # Enhance HTML with additional premium styling
    # Add custom CSS for even better typography
    enhanced_css = """
    <style>
        /* Premium typography enhancements */
        body {
            font-feature-settings: "kern" 1, "liga" 1, "calt" 1;
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        h1 {
            letter-spacing: -0.5px;
            font-weight: 700;
            margin-bottom: 20pt;
        }

        h2 {
            letter-spacing: -0.3px;
            font-weight: 600;
            margin-top: 24pt;
            margin-bottom: 12pt;
        }

        h3 {
            letter-spacing: -0.2px;
            font-weight: 600;
            margin-top: 18pt;
            margin-bottom: 8pt;
        }

        p {
            text-align: justify;
            hyphens: auto;
            orphans: 3;
            widows: 3;
        }

        /* Premium note boxes */
        .note-box {
            border-left: 5pt solid #1a5490;
            background: linear-gradient(to right, #f8f9fa 0%, #ffffff 10%);
            padding: 16pt;
            margin: 16pt 0;
            border-radius: 4pt;
            box-shadow: 0 1pt 3pt rgba(0,0,0,0.1);
        }

        /* Premium highlight boxes */
        .highlight-box {
            border: 2pt solid #1a5490;
            background: #f8f9fa;
            padding: 16pt;
            margin: 16pt 0;
            border-radius: 4pt;
            box-shadow: 0 2pt 6pt rgba(0,0,0,0.1);
        }

        /* Premium code blocks */
        pre {
            border-left: 4pt solid #1a5490;
            background: #f8f9fa;
            padding: 12pt;
            border-radius: 4pt;
            box-shadow: 0 1pt 3pt rgba(0,0,0,0.05);
        }

        /* Premium tables */
        table {
            border-collapse: separate;
            border-spacing: 0;
            box-shadow: 0 1pt 3pt rgba(0,0,0,0.1);
        }

        th {
            background: #1a5490;
            color: #ffffff;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        /* Premium idea cards */
        .idea-card {
            background: #ffffff;
            border: 1pt solid #d1d5db;
            border-radius: 6pt;
            padding: 12pt;
            margin: 10pt 0;
            box-shadow: 0 1pt 3pt rgba(0,0,0,0.05);
            transition: box-shadow 0.2s;
        }

        .idea-card:hover {
            box-shadow: 0 2pt 6pt rgba(0,0,0,0.1);
        }

        /* Premium section dividers */
        hr {
            border: none;
            border-top: 2pt solid #1a5490;
            margin: 24pt 0;
            opacity: 0.3;
        }

        /* Premium blockquotes */
        blockquote {
            border-left: 5pt solid #1a5490;
            background: #f8f9fa;
            padding: 16pt;
            margin: 16pt 0;
            font-style: italic;
            border-radius: 4pt;
            box-shadow: 0 1pt 3pt rgba(0,0,0,0.05);
        }
    </style>
    """

    # Inject enhanced CSS into HTML
    html_content = html_content.replace("</head>", enhanced_css + "</head>")

    # Generate PDF
    output_dir = Path("_work_efforts/session_recaps")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"KARMA_ECONOMY_PREMIUM_{timestamp}.pdf"
    html_path = output_dir / f"KARMA_ECONOMY_PREMIUM_{timestamp}.html"

    # Save HTML
    html_path.write_text(html_content)
    print(f"✅ HTML saved: {html_path}")

    # Generate PDF with premium settings
    HTML(string=html_content).write_pdf(
        output_path,
        presentational_hints=True,  # Enable better rendering
    )
    print(f"✅ Premium PDF generated: {output_path}")

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

    print("\n" + "=" * 80)
    print("🎨 PREMIUM PDF GENERATED - Peak Styling Applied!")
    print("=" * 80)
    print("✨ Features:")
    print("   - Premium serif typography with optimal spacing")
    print("   - Generous margins for elegant presentation")
    print("   - Professional color palette")
    print("   - Enhanced visual elements (shadows, borders, gradients)")
    print("   - Optimized readability and legibility")
    print("   - All content included - no constraints")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
