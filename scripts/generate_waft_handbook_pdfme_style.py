#!/usr/bin/env python3
"""
Generate WAFT Handbook using pdfme-inspired Template System
===========================================================

Inspired by:
- pdfme (https://github.com/pdfme/pdfme.git) - JSON template + data approach, WYSIWYG designer
- LaTTe (https://github.com/raphaelreyna/latte.git) - Template + JSON approach
- LaTeX Cookbook (https://github.com/alexpovel/latex-cookbook.git) - Beautiful typography

pdfme Concepts:
- Simple JSON templates (template structure defined in JSON)
- Template + data separation
- WYSIWYG designer for template creation
- Fast generation in browser/Node.js

We adapt this to Python:
- JSON template structure (pdfme-style)
- Template rendering with WeasyPrint
- Field guide aesthetic with LaTeX-inspired typography
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import markdown
from weasyprint import HTML


def create_pdfme_style_template() -> dict[str, Any]:
    """
    Create pdfme-style JSON template structure.

    pdfme uses JSON to define template structure with:
    - basePdf: Base PDF template (optional)
    - schemas: Field definitions
    - pages: Page layouts
    - fonts: Custom fonts (optional)

    We adapt this to define our field guide template structure.
    """
    return {
        "template": {
            "name": "WAFT Field Guide",
            "version": "1.0.0",
            "description": "Field guide template inspired by pdfme, LaTTe, and LaTeX Cookbook",
            "baseStyle": {
                "fontFamily": "Times New Roman, Times, serif",
                "fontSize": "11pt",
                "lineHeight": "1.5",
                "color": "#000000",
                "margin": {"top": "0.75in", "right": "0.5in", "bottom": "0.75in", "left": "0.5in"},
            },
            "pages": [
                {
                    "id": "cover",
                    "type": "cover",
                    "elements": [
                        {
                            "type": "text",
                            "id": "series_number",
                            "position": {"x": "center", "y": "1in"},
                            "style": {
                                "fontFamily": "Courier New, monospace",
                                "fontSize": "14pt",
                                "fontWeight": "bold",
                                "textTransform": "uppercase",
                                "textAlign": "center",
                            },
                            "content": "{{series}} {{number}}",
                        },
                        {
                            "type": "text",
                            "id": "title",
                            "position": {"x": "center", "y": "2in"},
                            "style": {
                                "fontSize": "24pt",
                                "fontWeight": "bold",
                                "textTransform": "uppercase",
                                "textAlign": "center",
                            },
                            "content": "{{title}}",
                        },
                        {
                            "type": "text",
                            "id": "subtitle",
                            "position": {"x": "center", "y": "3in"},
                            "style": {
                                "fontSize": "14pt",
                                "fontStyle": "italic",
                                "textAlign": "center",
                            },
                            "content": "{{subtitle}}",
                            "conditional": "{{subtitle}}",
                        },
                        {
                            "type": "box",
                            "id": "classification",
                            "position": {"x": "center", "y": "4.5in"},
                            "style": {
                                "backgroundColor": "#ffff00",
                                "borderColor": "#cc0000",
                                "borderWidth": "3pt",
                                "padding": "0.15in 0.3in",
                                "textAlign": "center",
                                "fontWeight": "bold",
                            },
                            "content": "{{classification}}",
                            "conditional": "{{classification}}",
                        },
                    ],
                },
                {
                    "id": "content",
                    "type": "content",
                    "elements": [
                        {
                            "type": "header",
                            "id": "page_header",
                            "position": {"x": "left", "y": "top"},
                            "style": {
                                "fontFamily": "Courier New, monospace",
                                "fontSize": "9pt",
                                "fontWeight": "bold",
                            },
                            "content": "{{series}} {{number}}",
                        },
                        {
                            "type": "footer",
                            "id": "page_footer",
                            "position": {"x": "center", "y": "bottom"},
                            "style": {
                                "fontFamily": "Courier New, monospace",
                                "fontSize": "8pt",
                                "color": "#cc0000",
                                "fontWeight": "bold",
                            },
                            "content": "{{classification}}",
                        },
                        {
                            "type": "content",
                            "id": "main_content",
                            "position": {"x": "left", "y": "top"},
                            "style": {"marginTop": "0.3in"},
                            "content": "{{content}}",
                        },
                    ],
                },
            ],
        }
    }


def render_pdfme_template_to_html(template_json: dict[str, Any], data: dict[str, Any]) -> str:
    """
    Render pdfme-style JSON template to HTML using WeasyPrint.

    This converts the JSON template structure into HTML/CSS that WeasyPrint can render.
    """
    template = template_json["template"]
    base_style = template["baseStyle"]

    # Build HTML from template structure
    html_parts = []
    html_parts.append("<!DOCTYPE html>")
    html_parts.append("<html lang='en'>")
    html_parts.append("<head>")
    html_parts.append("<meta charset='UTF-8'>")
    html_parts.append(f"<title>{data.get('title', 'WAFT Handbook')}</title>")
    html_parts.append("<style>")

    # Base styles from template
    html_parts.append(f"""
        @page {{
            size: letter;
            margin: {base_style["margin"]["top"]} {base_style["margin"]["right"]}
                    {base_style["margin"]["bottom"]} {base_style["margin"]["left"]};

            @top-left {{
                content: "{data.get("series", "FIELD GUIDE")} {data.get("number", "FG-001")}";
                font-family: 'Courier New', 'Courier', monospace;
                font-size: 9pt;
                font-weight: bold;
                text-transform: uppercase;
            }}

            @top-right {{
                content: "Page " counter(page);
                font-family: 'Courier New', 'Courier', monospace;
                font-size: 9pt;
            }}

            @bottom-center {{
                content: "{data.get("classification", "FOR OFFICIAL USE ONLY")}";
                font-family: 'Courier New', 'Courier', monospace;
                font-size: 8pt;
                color: #cc0000;
                font-weight: bold;
            }}
        }}

        @page :first {{
            @top-left {{ content: none; }}
            @top-right {{ content: none; }}
            @bottom-center {{ content: none; }}
        }}

        body {{
            font-family: {base_style["fontFamily"]};
            font-size: {base_style["fontSize"]};
            line-height: {base_style["lineHeight"]};
            color: {base_style["color"]};
            text-align: justify;
        }}

        .cover-page {{
            page-break-after: always;
            text-align: center;
            padding: 1in 0.5in;
            border: 4pt double #000;
            margin: 0.5in;
        }}

        .series-number {{
            font-family: 'Courier New', 'Courier', monospace;
            font-size: 14pt;
            font-weight: bold;
            text-transform: uppercase;
            margin-bottom: 0.3in;
        }}

        .cover-title {{
            font-size: 24pt;
            font-weight: bold;
            text-transform: uppercase;
            margin: 0.3in 0;
        }}

        .cover-subtitle {{
            font-size: 14pt;
            font-style: italic;
            color: #333;
            margin: 0.2in 0;
        }}

        .classification-box {{
            display: inline-block;
            background: #ffff00;
            border: 3pt solid #cc0000;
            padding: 0.15in 0.3in;
            margin: 0.3in 0;
            font-weight: bold;
            font-size: 12pt;
        }}

        .abstract {{
            margin: 0.3in 0;
            padding: 0.2in;
            background: #f9f9f9;
            border: 1pt solid #ddd;
            font-size: 10pt;
        }}

        .abstract-title {{
            font-weight: bold;
            text-align: center;
            margin-bottom: 0.1in;
        }}

        h1 {{
            font-size: 16pt;
            font-weight: bold;
            margin-top: 0.4in;
            margin-bottom: 0.2in;
            border-bottom: 0.4pt solid #000;
            padding-bottom: 0.05in;
        }}

        h2 {{
            font-size: 14pt;
            font-weight: bold;
            margin-top: 0.3in;
            margin-bottom: 0.15in;
            border-bottom: 0.4pt solid #000;
            padding-bottom: 0.05in;
        }}

        h3 {{
            font-size: 12pt;
            font-weight: bold;
            margin-top: 0.2in;
            margin-bottom: 0.1in;
            font-style: italic;
        }}

        p {{
            margin: 0.12in 0;
            orphans: 3;
            widows: 3;
        }}

        pre {{
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            background: #f5f5f5;
            border: 1pt solid #ddd;
            border-left: 3pt solid #0066cc;
            padding: 0.15in;
            margin: 0.2in 0;
            overflow-x: auto;
        }}

        code {{
            font-family: 'Courier New', monospace;
            font-size: 10pt;
            background: #f5f5f5;
            padding: 0.02in 0.05in;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 0.2in 0;
            font-size: 10pt;
        }}

        th {{
            background: #333;
            color: #fff;
            border-bottom: 2pt solid #000;
            padding: 0.1in;
            text-align: left;
            font-weight: bold;
        }}

        td {{
            border-bottom: 0.5pt solid #ddd;
            padding: 0.08in;
        }}

        tr:nth-child(even) {{
            background: #f9f9f9;
        }}
    """)

    html_parts.append("</style>")
    html_parts.append("</head>")
    html_parts.append("<body>")

    # Render cover page
    html_parts.append("<div class='cover-page'>")
    html_parts.append(
        f"<div class='series-number'>{data.get('series', 'FIELD GUIDE')} {data.get('number', 'FG-001')}</div>"
    )
    html_parts.append(f"<div class='cover-title'>{data.get('title', 'WAFT Handbook')}</div>")
    if data.get("subtitle"):
        html_parts.append(f"<div class='cover-subtitle'>{data.get('subtitle')}</div>")
    if data.get("classification"):
        html_parts.append(f"<div class='classification-box'>{data.get('classification')}</div>")
    html_parts.append("</div>")

    # Abstract
    if data.get("abstract"):
        html_parts.append("<div class='abstract'>")
        html_parts.append("<div class='abstract-title'>Abstract</div>")
        html_parts.append(f"<div>{data.get('abstract')}</div>")
        html_parts.append("</div>")

    # Main content
    html_parts.append(f"<div class='content'>{data.get('content', '')}</div>")

    html_parts.append("</body>")
    html_parts.append("</html>")

    return "\n".join(html_parts)


def parse_handbook_markdown(md_path: Path) -> dict[str, Any]:
    """Parse WAFT handbook markdown into structured data."""
    content = md_path.read_text(encoding="utf-8")

    # Extract frontmatter
    metadata = {}
    frontmatter_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        for line in frontmatter.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key == "authors":
                    if value.startswith("["):
                        metadata[key] = [{"name": value.strip("[]").strip()}]
                    else:
                        metadata[key] = [{"name": value}]
                else:
                    metadata[key] = value
        content = content[frontmatter_match.end() :]

    # Extract title
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = metadata.get(
        "title", title_match.group(1) if title_match else "WAFT Framework Handbook"
    )

    # Extract abstract
    abstract_match = re.search(r"^## Abstract\s*\n\n(.+?)(?=\n##|\n---|\Z)", content, re.DOTALL)
    abstract = metadata.get("abstract", abstract_match.group(1).strip() if abstract_match else "")

    # Convert markdown to HTML
    html_content = markdown.markdown(content, extensions=["tables", "fenced_code", "codehilite"])

    return {
        "title": title,
        "subtitle": metadata.get(
            "subtitle", "A Comprehensive Guide to Directed Evolution of Self-Modifying AI Agents"
        ),
        "abstract": abstract,
        "authors": ", ".join(
            [
                a.get("name", "WAFT Development Team")
                for a in metadata.get("authors", [{"name": "WAFT Development Team"}])
            ]
        ),
        "date": metadata.get("year", datetime.now().strftime("%Y")),
        "series": "FIELD GUIDE",
        "number": "FG-WAFT-001",
        "classification": "FOR OFFICIAL USE ONLY",
        "issued_by": "WAFT Development Team",
        "content": html_content,
    }


def main():
    """Generate WAFT Handbook using pdfme-inspired template system."""
    project_root = Path(__file__).parent.parent
    handbook_md = project_root / "WAFT_FRAMEWORK_HANDBOOK.md"
    output_dir = project_root / "_work_efforts" / "waft_handbook_pdfme_style"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("📚 Generating WAFT Handbook using pdfme-inspired Template System")
    print(f"   Source: {handbook_md}")
    print(f"   Output: {output_dir}")
    print("   Inspiration: pdfme (JSON templates) + LaTTe + LaTeX Cookbook")

    # Step 1: Create pdfme-style template
    print("\n1️⃣  Creating pdfme-style JSON template...")
    template_json = create_pdfme_style_template()
    template_path = output_dir / "field_guide_template.json"
    template_path.write_text(json.dumps(template_json, indent=2, ensure_ascii=False))
    print(f"   ✅ Template saved: {template_path}")

    # Step 2: Parse handbook data
    print("\n2️⃣  Parsing handbook markdown to data...")
    data = parse_handbook_markdown(handbook_md)
    data_path = output_dir / "handbook_data.json"
    data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"   ✅ Data saved: {data_path}")

    # Step 3: Render template to HTML
    print("\n3️⃣  Rendering template to HTML...")
    html_output = render_pdfme_template_to_html(template_json, data)
    html_path = output_dir / "waft_handbook.html"
    html_path.write_text(html_output, encoding="utf-8")
    print(f"   ✅ HTML saved: {html_path}")

    # Step 4: Generate PDF
    print("\n4️⃣  Generating PDF...")
    pdf_path = output_dir / "WAFT_FRAMEWORK_HANDBOOK_PDFME_STYLE.pdf"
    HTML(string=html_output).write_pdf(pdf_path)

    if pdf_path.exists():
        size_mb = pdf_path.stat().st_size / (1024 * 1024)
        print(f"   ✅ PDF generated: {pdf_path}")
        print(f"   📄 Size: {size_mb:.2f} MB")
        print("\n🎉 WAFT Handbook (pdfme-style) ready!")
        print(f"   📄 {pdf_path}")
        print(f"   📋 Template: {template_path}")
        print(f"   📊 Data: {data_path}")

        # Try to open
        try:
            import platform

            if platform.system() == "Darwin":
                import subprocess

                subprocess.run(["open", str(pdf_path)])
        except Exception as e:
            print(f"   ⚠️  Could not auto-open: {e}")

        return 0
    else:
        print("   ❌ PDF generation failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
