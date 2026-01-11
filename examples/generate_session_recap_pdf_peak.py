#!/usr/bin/env python3
"""
Generate PEAK Session Recap PDF - Maximum Styling Excellence

This is the ULTIMATE styling evolution - no compromises, peak visual quality.
Every detail optimized for beauty, readability, and professional excellence.
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
from weasyprint import HTML, CSS


def get_session_content() -> str:
    """Get comprehensive session content."""
    from examples.generate_session_recap_pdf_waft import get_session_content
    return get_session_content()


def main():
    """Generate PEAK PDF with maximum styling excellence."""
    print("=" * 80)
    print("🎨✨ Generating PEAK Session Recap PDF - Maximum Styling Excellence ✨🎨")
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
    
    # Get ALL ideas
    all_ideas = distilled.get_top_ideas(n=1000, min_importance=0.0)
    print(f"✅ Including ALL {len(all_ideas)} ideas")
    
    # Create PEAK styling genome - absolute maximum quality
    print("\n🎨 Creating PEAK styling genome (maximum excellence)...")
    registry = StylingGenomeRegistry(registry_dir=Path("_genetics/session_recaps"))
    
    # PEAK styling - every detail optimized
    styling_genes = StylingGene(
        font=FontGene(
            family="'Minion Pro', 'Palatino Linotype', 'Book Antiqua', 'Palatino', 'Times New Roman', serif",
            size_body=13,      # Larger, more comfortable reading
            size_h1=32,        # Dramatic, commanding headings
            size_h2=22,         # Clear hierarchy
            size_h3=17,         # Well-defined subsections
            size_code=11,       # Readable code
            line_height=1.75    # Generous, luxurious spacing
        ),
        margin=MarginGene(
            top=40,          # Very generous top margin
            bottom=40,        # Very generous bottom margin
            left=40,          # Wide, elegant left margin
            right=40,         # Wide, elegant right margin
            section_spacing=24,  # Clear section separation
            paragraph_spacing=12  # Comfortable paragraph breathing room
        ),
        color=ColorGene(
            text="#1a1a1a",           # Rich, deep black (not harsh pure black)
            background="#FFFFFF",      # Pure white
            heading="#000000",         # Maximum contrast for headings
            accent="#0d47a1",         # Deep, sophisticated blue (Material Design Blue 900)
            code_bg="#f5f7fa",        # Subtle, elegant gray
            code_text="#1e3a5f",       # Deep blue-gray for code
            border="#b0bec5"          # Soft, refined gray border
        ),
        layout=LayoutGene(
            columns=1,
            density="spacious",        # Maximum breathing room
            toc_enabled=False,
            page_numbers=True,
            header_enabled=True,
            footer_enabled=True
        ),
        name="PEAK Session Recap - Maximum Excellence"
    )
    
    genome = StylingGenome.from_genes(styling_genes)
    registry.register(genome)
    print(f"✅ Created PEAK genome: {genome.scientific_name}")
    print(f"   ✨ Premium serif typography")
    print(f"   ✨ Generous, luxurious spacing")
    print(f"   ✨ Sophisticated color palette")
    print(f"   ✨ Maximum readability and elegance")
    
    # Render HTML with ALL ideas using peak styling
    print("\n📄 Rendering HTML with PEAK styling...")
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
    
    # Inject PEAK CSS enhancements - maximum visual excellence
    peak_css = """
    <style>
        /* ========================================
           PEAK STYLING - Maximum Excellence
           ======================================== */
        
        /* Premium Typography */
        @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');
        
        body {
            font-feature-settings: "kern" 1, "liga" 1, "calt" 1, "onum" 1, "pnum" 1;
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            font-variant-numeric: oldstyle-nums;
            letter-spacing: 0.01em;
        }
        
        /* Dramatic Headings */
        h1 {
            letter-spacing: -0.8px;
            font-weight: 700;
            margin-bottom: 24pt;
            text-transform: none;
            border-bottom: 3pt solid #0d47a1;
            padding-bottom: 8pt;
            position: relative;
        }
        
        h1::after {
            content: '';
            position: absolute;
            bottom: -3pt;
            left: 0;
            width: 60pt;
            height: 2pt;
            background: #0d47a1;
            opacity: 0.3;
        }
        
        h2 {
            letter-spacing: -0.5px;
            font-weight: 600;
            margin-top: 32pt;
            margin-bottom: 16pt;
            border-bottom: 2pt solid #0d47a1;
            padding-bottom: 6pt;
            position: relative;
        }
        
        h2::before {
            content: '◆';
            color: #0d47a1;
            margin-right: 8pt;
            font-size: 0.7em;
            opacity: 0.6;
        }
        
        h3 {
            letter-spacing: -0.3px;
            font-weight: 600;
            margin-top: 24pt;
            margin-bottom: 12pt;
            color: #1e3a5f;
        }
        
        /* Premium Paragraphs */
        p {
            text-align: justify;
            hyphens: auto;
            orphans: 4;
            widows: 4;
            text-indent: 0;
            margin-bottom: 12pt;
        }
        
        /* First paragraph after heading - no indent */
        h1 + p, h2 + p, h3 + p {
            text-indent: 0;
        }
        
        /* Premium Note Boxes - Elegant Design */
        .note-box {
            border-left: 6pt solid #0d47a1;
            background: linear-gradient(to right, #e3f2fd 0%, #ffffff 15%);
            padding: 20pt;
            margin: 20pt 0;
            border-radius: 6pt;
            box-shadow: 0 2pt 8pt rgba(13, 71, 161, 0.15);
            position: relative;
            overflow: hidden;
        }
        
        .note-box::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 6pt;
            height: 100%;
            background: linear-gradient(to bottom, #0d47a1, #1976d2);
        }
        
        .note-title {
            font-weight: 700;
            color: #0d47a1;
            font-size: 13pt;
            margin-bottom: 8pt;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            font-size: 0.85em;
        }
        
        /* Premium Highlight Boxes */
        .highlight-box {
            border: 3pt solid #0d47a1;
            background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
            padding: 20pt;
            margin: 20pt 0;
            border-radius: 8pt;
            box-shadow: 0 4pt 12pt rgba(13, 71, 161, 0.2);
            position: relative;
        }
        
        .highlight-box::before {
            content: '★';
            position: absolute;
            top: 12pt;
            right: 12pt;
            color: #0d47a1;
            font-size: 18pt;
            opacity: 0.2;
        }
        
        /* Premium Code Blocks */
        pre {
            border-left: 5pt solid #0d47a1;
            background: linear-gradient(to right, #f5f7fa 0%, #ffffff 5%);
            padding: 16pt;
            border-radius: 6pt;
            box-shadow: 0 2pt 6pt rgba(0,0,0,0.08);
            margin: 16pt 0;
            overflow-x: auto;
        }
        
        code {
            font-family: 'Courier New', 'Monaco', monospace;
            font-size: 11pt;
            background: #f5f7fa;
            padding: 2pt 6pt;
            border-radius: 3pt;
            color: #1e3a5f;
            border: 1pt solid #e0e7ef;
        }
        
        /* Premium Tables */
        table {
            border-collapse: separate;
            border-spacing: 0;
            width: 100%;
            margin: 20pt 0;
            box-shadow: 0 2pt 8pt rgba(0,0,0,0.1);
            border-radius: 6pt;
            overflow: hidden;
        }
        
        th {
            background: linear-gradient(to bottom, #0d47a1, #1565c0);
            color: #ffffff;
            font-weight: 700;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            font-size: 0.9em;
            padding: 14pt;
            text-align: left;
        }
        
        td {
            padding: 12pt 14pt;
            border-bottom: 1pt solid #e0e7ef;
        }
        
        tr:last-child td {
            border-bottom: none;
        }
        
        tr:nth-child(even) {
            background: #f8f9fa;
        }
        
        /* Premium Idea Cards */
        .idea-card {
            background: #ffffff;
            border: 2pt solid #e0e7ef;
            border-radius: 8pt;
            padding: 16pt;
            margin: 14pt 0;
            box-shadow: 0 2pt 6pt rgba(0,0,0,0.06);
            transition: all 0.3s ease;
            position: relative;
        }
        
        .idea-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4pt;
            height: 100%;
            background: linear-gradient(to bottom, #0d47a1, #42a5f5);
            border-radius: 8pt 0 0 8pt;
        }
        
        .idea-card:hover {
            box-shadow: 0 4pt 12pt rgba(13, 71, 161, 0.15);
            border-color: #0d47a1;
            transform: translateY(-1pt);
        }
        
        /* Premium Section Dividers */
        hr {
            border: none;
            border-top: 3pt solid #0d47a1;
            margin: 32pt 0;
            opacity: 0.4;
            position: relative;
        }
        
        hr::after {
            content: '◆';
            position: absolute;
            top: -8pt;
            left: 50%;
            transform: translateX(-50%);
            background: #ffffff;
            padding: 0 8pt;
            color: #0d47a1;
            font-size: 12pt;
        }
        
        /* Premium Blockquotes */
        blockquote {
            border-left: 6pt solid #0d47a1;
            background: linear-gradient(to right, #e3f2fd 0%, #ffffff 20%);
            padding: 20pt;
            margin: 20pt 0;
            font-style: italic;
            border-radius: 6pt;
            box-shadow: 0 2pt 8pt rgba(13, 71, 161, 0.1);
            position: relative;
            font-size: 1.05em;
            line-height: 1.8;
        }
        
        blockquote::before {
            content: '"';
            position: absolute;
            top: 8pt;
            left: 12pt;
            font-size: 48pt;
            color: #0d47a1;
            opacity: 0.2;
            font-family: serif;
        }
        
        blockquote::after {
            content: '"';
            position: absolute;
            bottom: 8pt;
            right: 12pt;
            font-size: 48pt;
            color: #0d47a1;
            opacity: 0.2;
            font-family: serif;
        }
        
        /* Premium Lists */
        ul, ol {
            margin: 16pt 0;
            padding-left: 28pt;
        }
        
        li {
            margin: 8pt 0;
            line-height: 1.8;
        }
        
        ul li::marker {
            color: #0d47a1;
            font-weight: bold;
        }
        
        /* Premium Page Numbers */
        @page {
            @bottom-center {
                content: counter(page);
                font-family: serif;
                font-size: 10pt;
                color: #666;
                margin-top: 20pt;
            }
        }
        
        /* Premium Headers/Footers */
        .header, .footer {
            color: #666;
            font-size: 9pt;
            border-top: 1pt solid #e0e7ef;
            padding-top: 8pt;
            margin-top: 16pt;
        }
        
        /* Premium Links */
        a {
            color: #0d47a1;
            text-decoration: none;
            border-bottom: 1pt solid transparent;
            transition: border-color 0.2s;
        }
        
        a:hover {
            border-bottom-color: #0d47a1;
        }
        
        /* Premium Category Tags */
        .category-tag {
            display: inline-block;
            background: linear-gradient(135deg, #0d47a1, #1976d2);
            color: #ffffff;
            padding: 4pt 10pt;
            border-radius: 12pt;
            font-size: 0.75em;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin-right: 6pt;
            box-shadow: 0 2pt 4pt rgba(13, 71, 161, 0.3);
        }
        
        /* Premium Importance Badge */
        .importance-badge {
            display: inline-block;
            width: 8pt;
            height: 8pt;
            border-radius: 50%;
            margin-right: 6pt;
            vertical-align: middle;
        }
        
        .importance-high {
            background: #0d47a1;
            box-shadow: 0 0 4pt rgba(13, 71, 161, 0.5);
        }
        
        .importance-medium {
            background: #42a5f5;
        }
        
        .importance-low {
            background: #90caf9;
        }
    </style>
    """
    
    # Inject PEAK CSS
    html_content = html_content.replace('</head>', peak_css + '</head>')
    
    # Generate PDF
    output_dir = Path("_work_efforts/session_recaps")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"KARMA_ECONOMY_PEAK_{timestamp}.pdf"
    html_path = output_dir / f"KARMA_ECONOMY_PEAK_{timestamp}.html"
    
    # Save HTML
    html_path.write_text(html_content)
    print(f"✅ HTML saved: {html_path}")
    
    # Generate PDF with maximum quality settings
    HTML(
        string=html_content,
        base_url=str(output_dir)
    ).write_pdf(
        output_path,
        presentational_hints=True,
        optimize_images=True
    )
    print(f"✅ PEAK PDF generated: {output_path}")
    
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
    print("🎨✨ PEAK PDF GENERATED - Maximum Styling Excellence Achieved! ✨🎨")
    print("=" * 80)
    print("✨ PEAK Features Applied:")
    print("   🎯 Premium serif typography with optimal font features")
    print("   🎯 Generous, luxurious margins (40mm all around)")
    print("   🎯 Sophisticated deep blue color palette (#0d47a1)")
    print("   🎯 Enhanced visual elements:")
    print("      • Gradient backgrounds on boxes")
    print("      • Elegant shadows and borders")
    print("      • Decorative elements (◆, ★, quotes)")
    print("      • Premium table styling")
    print("      • Beautiful idea cards with hover effects")
    print("   🎯 Maximum readability (1.75 line height, 13pt body)")
    print("   🎯 Professional typography features (kern, liga, oldstyle nums)")
    print("   🎯 All content included - no constraints")
    print("=" * 80)
    print("🚀 This is PEAK styling - maximum excellence achieved!")
    print("=" * 80)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
