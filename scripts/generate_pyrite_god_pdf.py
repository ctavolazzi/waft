#!/usr/bin/env python3
"""
Generate Pyrite God PDF using D&D Character Sheet styling
Converts the Pyrite HTML writeup to PDF with D&D 5e character sheet aesthetic.
"""

import sys
from pathlib import Path

from weasyprint import HTML

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def generate_pyrite_pdf(html_path: Path = None, output_path: Path = None) -> Path:
    """
    Generate PDF from Pyrite HTML using D&D character sheet styling.

    Args:
        html_path: Path to Pyrite HTML file (default: docs/pyrite_god.html)
        output_path: Path for output PDF (default: docs/pyrite_god.pdf)

    Returns:
        Path to generated PDF
    """
    if html_path is None:
        html_path = Path(__file__).parent.parent / "docs" / "pyrite_god.html"

    if output_path is None:
        output_path = html_path.with_suffix(".pdf")

    # Read HTML content
    html_content = html_path.read_text()

    # Adapt HTML for D&D character sheet styling
    adapted_html = adapt_html_for_dnd_style(html_content)

    # Generate PDF using WeasyPrint
    print("📄 Generating Pyrite God PDF...")
    print(f"   Input: {html_path}")
    print(f"   Output: {output_path}")

    HTML(string=adapted_html).write_pdf(output_path)

    print(f"   ✅ Generated: {output_path}")
    return output_path


def adapt_html_for_dnd_style(html_content: str) -> str:
    """
    Adapt HTML content to use D&D character sheet styling.
    Replaces modern web styling with D&D 5e character sheet aesthetic.
    """
    # Replace the style section with D&D character sheet styling
    dnd_style = """
    <style>
        @page {
            size: letter;
            margin: 0.5in;
        }

        body {
            font-family: 'Arial', 'Helvetica', sans-serif;
            font-size: 10pt;
            line-height: 1.5;
            color: #000;
            background: #fff;
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 100%;
            margin: 0;
        }

        header {
            background: #fff;
            color: #000;
            padding: 0.3in;
            text-align: center;
            border: 3px solid #000;
            margin-bottom: 0.2in;
        }

        h1 {
            font-size: 24pt;
            font-weight: bold;
            margin: 0 0 0.1in 0;
            text-transform: uppercase;
            letter-spacing: 2px;
            border-bottom: 3px solid #000;
            padding-bottom: 0.1in;
        }

        .subtitle {
            font-size: 14pt;
            font-weight: bold;
            margin-top: 0.1in;
            text-transform: uppercase;
        }

        .god-badge {
            display: inline-block;
            background: #fff;
            border: 2px solid #000;
            padding: 0.05in 0.15in;
            margin-top: 0.1in;
            font-size: 8pt;
            text-transform: uppercase;
        }

        .content {
            padding: 0.2in;
        }

        section {
            margin-bottom: 0.3in;
            page-break-inside: avoid;
        }

        h2 {
            font-size: 16pt;
            font-weight: bold;
            color: #000;
            margin: 0.3in 0 0.15in 0;
            padding: 0.1in;
            border: 2px solid #000;
            background: #f0f0f0;
            text-transform: uppercase;
            page-break-after: avoid;
        }

        h2::before {
            content: '';
        }

        h3 {
            font-size: 12pt;
            font-weight: bold;
            color: #000;
            margin: 0.2in 0 0.1in 0;
            padding-bottom: 0.05in;
            border-bottom: 1px solid #000;
            text-transform: uppercase;
            page-break-after: avoid;
        }

        h3::before {
            content: '';
        }

        p {
            margin-bottom: 0.1in;
            text-align: justify;
            font-size: 10pt;
        }

        .overview-grid, .abilities-grid, .personality-grid {
            display: block;
            margin: 0.15in 0;
        }

        .feature-card, .ability-card, .attribute-card {
            border: 1px solid #000;
            padding: 0.15in;
            margin-bottom: 0.1in;
            background: #fff;
            page-break-inside: avoid;
        }

        .feature-card h4, .ability-card h4 {
            font-size: 11pt;
            font-weight: bold;
            margin: 0 0 0.05in 0;
            text-transform: uppercase;
            border-bottom: 1px solid #000;
            padding-bottom: 0.05in;
        }

        .feature-card h4::before, .ability-card h4::before {
            content: '';
        }

        .attribute-card {
            text-align: center;
            border: 2px solid #000;
        }

        .attribute-name {
            font-size: 10pt;
            font-weight: bold;
            text-transform: uppercase;
            border-bottom: 1px solid #000;
            padding-bottom: 0.05in;
            margin-bottom: 0.05in;
        }

        .attribute-value {
            font-size: 18pt;
            font-weight: bold;
            margin: 0.05in 0;
        }

        .attribute-growth {
            font-size: 8pt;
            color: #666;
        }

        .code-block {
            background: #f5f5f5;
            border: 1px solid #000;
            padding: 0.15in;
            margin: 0.15in 0;
            font-family: 'Courier New', monospace;
            font-size: 8pt;
            line-height: 1.4;
            overflow-x: auto;
            page-break-inside: avoid;
        }

        .code-block code {
            color: #000;
        }

        .highlight-box {
            background: #fff;
            border: 2px solid #000;
            padding: 0.15in;
            margin: 0.2in 0;
            page-break-inside: avoid;
        }

        .highlight-box h4 {
            margin-top: 0;
            font-size: 11pt;
            font-weight: bold;
            text-transform: uppercase;
            border-bottom: 1px solid #000;
            padding-bottom: 0.05in;
            margin-bottom: 0.1in;
        }

        .workflow-steps {
            list-style: none;
            padding-left: 0;
            margin: 0.15in 0;
        }

        .workflow-steps li {
            margin-bottom: 0.1in;
            padding-left: 0.3in;
            position: relative;
            font-size: 9pt;
        }

        .workflow-steps li::before {
            content: counter(step-counter);
            counter-increment: step-counter;
            position: absolute;
            left: 0;
            top: 0;
            background: #000;
            color: #fff;
            width: 0.2in;
            height: 0.2in;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 10pt;
            border: 1px solid #000;
        }

        .status-badge {
            display: inline-block;
            padding: 0.02in 0.08in;
            border: 1px solid #000;
            font-size: 8pt;
            font-weight: bold;
            margin: 0.02in;
            text-transform: uppercase;
        }

        .status-active { background: #fff; }
        .status-dormant { background: #e0e0e0; }
        .status-locked { background: #ffe0e0; }
        .status-evolving { background: #e0e0ff; }
        .status-completed { background: #e0ffe0; }

        .empirica-badge {
            display: inline-block;
            background: #000;
            color: #fff;
            padding: 0.02in 0.08in;
            border: 1px solid #000;
            font-size: 8pt;
            font-weight: bold;
            margin: 0.02in;
            text-transform: uppercase;
        }

        ul, ol {
            margin: 0.1in 0;
            padding-left: 0.3in;
        }

        li {
            margin-bottom: 0.05in;
            font-size: 10pt;
        }

        .footer {
            background: #fff;
            color: #000;
            padding: 0.2in;
            text-align: center;
            border-top: 2px solid #000;
            margin-top: 0.3in;
            font-size: 8pt;
        }

        .footer p {
            margin: 0.05in 0;
        }

        .footer code {
            font-family: 'Courier New', monospace;
            background: #f5f5f5;
            padding: 0.02in 0.05in;
            border: 1px solid #000;
        }

        /* Remove animations and gradients for PDF */
        header::before {
            display: none;
        }

        .feature-card:hover,
        .ability-card:hover {
            transform: none;
            box-shadow: none;
        }

        /* Ensure proper page breaks */
        section {
            page-break-inside: avoid;
        }

        h2, h3 {
            page-break-after: avoid;
        }

        .code-block, .highlight-box {
            page-break-inside: avoid;
        }
    </style>
    """

    # Find and replace the style section
    if "<style>" in html_content:
        # Extract everything before <style>
        before_style = html_content.split("<style>")[0]
        # Extract everything after </style>
        after_style = html_content.split("</style>")[1]
        # Reconstruct with D&D style
        adapted_html = before_style + dnd_style + after_style
    else:
        # If no style tag, insert it in head
        if "</head>" in html_content:
            adapted_html = html_content.replace("</head>", dnd_style + "</head>")
        else:
            adapted_html = html_content

    return adapted_html


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate Pyrite God PDF using D&D character sheet styling"
    )
    parser.add_argument(
        "--html",
        type=Path,
        default=Path(__file__).parent.parent / "docs" / "pyrite_god.html",
        help="Path to Pyrite HTML file",
    )
    parser.add_argument(
        "--output", type=Path, help="Path for output PDF (default: same as HTML but .pdf)"
    )

    args = parser.parse_args()

    if not args.html.exists():
        print(f"❌ Error: HTML file not found: {args.html}")
        return 1

    try:
        output_path = generate_pyrite_pdf(args.html, args.output)
        print(f"\n✅ Success! PDF generated: {output_path}")
        return 0
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
