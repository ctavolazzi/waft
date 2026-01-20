#!/usr/bin/env python3
"""
Generate Session Recap PDF - Clinical Standard Style

Applies Foundation V2's "Clinical Standard" preset principles:
- Times New Roman body (11pt) - academic weight
- Helvetica headers (16/14/12pt) - professional appearance
- 1-inch margins - print-ready
- 1.4x line spacing - optimized readability
- Authoritative, institutional tone

This is the PEAK professional styling from WAFT's own systems.
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
    """Generate PDF using Clinical Standard principles."""
    print("=" * 80)
    print("🎨 Generating Session Recap PDF - Clinical Standard Style")
    print("=" * 80)
    print("Applying Foundation V2's Clinical Standard preset principles:")
    print("  • Times New Roman body (11pt) - academic weight")
    print("  • Helvetica headers (16/14/12pt) - professional appearance")
    print("  • 1-inch margins - print-ready")
    print("  • 1.4x line spacing - optimized readability")
    print("  • Authoritative, institutional tone")
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

    # Create Clinical Standard styling genome
    print("\n🎨 Creating Clinical Standard styling genome...")
    registry = StylingGenomeRegistry(registry_dir=Path("_genetics/session_recaps"))

    # Clinical Standard: Times body, Helvetica headers, 1-inch margins, 1.4x spacing
    styling_genes = StylingGene(
        font=FontGene(
            family="'Times New Roman', 'Times', serif",  # Body: Times New Roman
            size_body=11,  # Clinical Standard: 11pt body
            size_h1=16,  # Clinical Standard: 16pt H1 (Helvetica)
            size_h2=14,  # Clinical Standard: 14pt H2 (Helvetica)
            size_h3=12,  # Clinical Standard: 12pt H3 (Helvetica)
            size_code=9,  # Code: 9pt
            line_height=1.4,  # Clinical Standard: 1.4x line spacing
        ),
        margin=MarginGene(
            top=25.4,  # 1 inch = 25.4mm
            bottom=25.4,  # 1 inch = 25.4mm
            left=25.4,  # 1 inch = 25.4mm
            right=25.4,  # 1 inch = 25.4mm
            section_spacing=12,  # Professional spacing
            paragraph_spacing=8,  # Comfortable paragraph spacing
        ),
        color=ColorGene(
            text="#000000",  # Pure black for maximum readability
            background="#FFFFFF",  # Pure white
            heading="#000000",  # Pure black headers (Helvetica will be bold)
            accent="#000000",  # Black accent (institutional)
            code_bg="#f5f5f5",  # Subtle gray for code
            code_text="#000000",  # Black code text
            border="#cccccc",  # Soft gray borders
        ),
        layout=LayoutGene(
            columns=1,
            density="normal",
            toc_enabled=False,
            page_numbers=True,
            header_enabled=True,
            footer_enabled=True,
        ),
        name="Clinical Standard - Session Recap",
    )

    genome = StylingGenome.from_genes(styling_genes)
    registry.register(genome)
    print(f"✅ Created Clinical Standard genome: {genome.scientific_name}")

    # Render HTML with ALL ideas
    print("\n📄 Rendering HTML with Clinical Standard styling...")
    generator = TwoPageGenerator(weasyprint_available=True)

    # Split ideas evenly
    mid_point = len(all_ideas) // 2
    page_1_ideas = all_ideas[:mid_point]
    page_2_ideas = all_ideas[mid_point:]

    html_content = generator._render_html(
        distilled_chat=distilled,
        styling_genome=genome,
        page_1_ideas=page_1_ideas,
        page_2_ideas=page_2_ideas,
    )

    # Inject Clinical Standard CSS - Professional institutional styling
    clinical_css = """
    <style>
        /* ========================================
           CLINICAL STANDARD - Professional Scientific Documentation
           Based on Foundation V2's Clinical Standard preset
           ======================================== */

        /* Headers: Helvetica Bold (Clinical Standard) */
        h1 {
            font-family: 'Helvetica', 'Arial', sans-serif;
            font-weight: 700;
            font-size: 16pt;  /* Clinical Standard H1 */
            letter-spacing: -0.3px;
            margin-top: 0;
            margin-bottom: 12pt;
            border-bottom: 2pt solid #000;
            padding-bottom: 6pt;
            page-break-after: avoid;
        }

        h2 {
            font-family: 'Helvetica', 'Arial', sans-serif;
            font-weight: 700;
            font-size: 14pt;  /* Clinical Standard H2 */
            letter-spacing: -0.2px;
            margin-top: 18pt;
            margin-bottom: 10pt;
            border-bottom: 1pt solid #000;
            padding-bottom: 4pt;
            page-break-after: avoid;
        }

        h3 {
            font-family: 'Helvetica', 'Arial', sans-serif;
            font-weight: 700;
            font-size: 12pt;  /* Clinical Standard H3 */
            letter-spacing: -0.1px;
            margin-top: 14pt;
            margin-bottom: 8pt;
            page-break-after: avoid;
        }

        /* Body: Times New Roman (Clinical Standard) */
        body {
            font-family: 'Times New Roman', 'Times', serif;
            font-size: 11pt;  /* Clinical Standard body */
            line-height: 1.4;  /* Clinical Standard: 1.4x spacing */
            color: #000;
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
        }

        p {
            margin: 0 0 8pt 0;
            text-align: justify;
            orphans: 3;
            widows: 3;
        }

        /* Professional Note Boxes */
        .note-box {
            border-left: 4pt solid #000;
            background: #f9f9f9;
            padding: 12pt;
            margin: 12pt 0;
            page-break-inside: avoid;
        }

        .note-title {
            font-family: 'Helvetica', 'Arial', sans-serif;
            font-weight: 700;
            font-size: 10pt;
            color: #000;
            margin-bottom: 6pt;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Professional Highlight Boxes */
        .highlight-box {
            border: 2pt solid #000;
            background: #ffffff;
            padding: 12pt;
            margin: 12pt 0;
            page-break-inside: avoid;
        }

        /* Professional Code Blocks */
        pre {
            font-family: 'Courier New', 'Courier', monospace;
            font-size: 9pt;
            background: #f5f5f5;
            padding: 10pt;
            border-left: 3pt solid #000;
            margin: 10pt 0;
            page-break-inside: avoid;
            overflow-x: auto;
        }

        code {
            font-family: 'Courier New', 'Courier', monospace;
            font-size: 9pt;
            background: #f5f5f5;
            padding: 2pt 4pt;
            color: #000;
        }

        /* Professional Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 12pt 0;
            font-size: 10pt;
            page-break-inside: avoid;
        }

        th {
            font-family: 'Helvetica', 'Arial', sans-serif;
            font-weight: 700;
            background: #000;
            color: #fff;
            padding: 8pt;
            text-align: left;
            border: 1pt solid #000;
        }

        td {
            padding: 6pt 8pt;
            border: 1pt solid #ccc;
        }

        tr:nth-child(even) {
            background: #f9f9f9;
        }

        /* Professional Lists */
        ul, ol {
            margin: 8pt 0;
            padding-left: 20pt;
        }

        li {
            margin: 4pt 0;
            line-height: 1.4;
        }

        /* Professional Blockquotes */
        blockquote {
            border-left: 4pt solid #000;
            background: #f9f9f9;
            padding: 12pt;
            margin: 12pt 0;
            font-style: italic;
            page-break-inside: avoid;
        }

        /* Professional Section Dividers */
        hr {
            border: none;
            border-top: 2pt solid #000;
            margin: 18pt 0;
        }

        /* Professional Idea Cards */
        .idea {
            margin: 10pt 0;
            padding: 10pt;
            border-left: 3pt solid #000;
            background: #fafafa;
            page-break-inside: avoid;
        }

        /* Page Numbers (Clinical Standard style) */
        @page {
            @bottom-center {
                content: counter(page);
                font-family: 'Helvetica', 'Arial', sans-serif;
                font-size: 9pt;
                color: #666;
            }
        }

        /* Headers/Footers */
        .header, .footer {
            font-family: 'Helvetica', 'Arial', sans-serif;
            font-size: 9pt;
            color: #666;
            border-top: 1pt solid #ccc;
            padding-top: 6pt;
            margin-top: 12pt;
        }
    </style>
    """

    # Inject Clinical Standard CSS
    html_content = html_content.replace("</head>", clinical_css + "</head>")

    # Generate PDF
    output_dir = Path("_work_efforts/session_recaps")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"KARMA_ECONOMY_CLINICAL_STANDARD_{timestamp}.pdf"
    html_path = output_dir / f"KARMA_ECONOMY_CLINICAL_STANDARD_{timestamp}.html"

    # Save HTML
    html_path.write_text(html_content)
    print(f"✅ HTML saved: {html_path}")

    # Generate PDF with Clinical Standard quality
    HTML(string=html_content, base_url=str(output_dir)).write_pdf(
        output_path, presentational_hints=True, optimize_images=True
    )
    print(f"✅ Clinical Standard PDF generated: {output_path}")

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
    print("🎨 CLINICAL STANDARD PDF GENERATED!")
    print("=" * 80)
    print("✨ Applied Foundation V2's Clinical Standard preset:")
    print("   ✅ Times New Roman body (11pt) - academic weight")
    print("   ✅ Helvetica headers (16/14/12pt) - professional appearance")
    print("   ✅ 1-inch margins (25.4mm) - print-ready")
    print("   ✅ 1.4x line spacing - optimized readability")
    print("   ✅ Authoritative, institutional tone")
    print("   ✅ All content included - no constraints")
    print("=" * 80)
    print("🚀 This is WAFT's own Clinical Standard - peak professional styling!")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
