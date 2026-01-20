#!/usr/bin/env python3
"""
Generate WAFT Handbook Field Guide PDF
======================================

Inspired by:
- LaTTe (https://github.com/raphaelreyna/latte.git) - Template + JSON approach
- LaTeX Cookbook (https://github.com/alexpovel/latex-cookbook.git) - Beautiful typography

Uses WeasyPrint with LaTeX-inspired styling to create a professional field guide PDF
without requiring LaTeX installation.
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
from jinja2 import Template
from weasyprint import HTML


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


# LaTeX-Inspired Field Guide Template (WeasyPrint/HTML)
FIELD_GUIDE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
    <style>
        /* LaTeX-Inspired Field Guide Styling */
        /* Inspired by LaTTe and LaTeX Cookbook typography */
        
        @page {
            size: letter;
            margin: 0.75in 0.5in;
            
            @top-left {
                content: "{{ series }} {{ number }}";
                font-family: 'Courier New', 'Courier', monospace;
                font-size: 9pt;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            
            @top-right {
                content: "Page " counter(page);
                font-family: 'Courier New', 'Courier', monospace;
                font-size: 9pt;
            }
            
            @bottom-center {
                content: "{{ classification }}";
                font-family: 'Courier New', 'Courier', monospace;
                font-size: 8pt;
                color: #cc0000;
                font-weight: bold;
            }
        }
        
        @page :first {
            @top-left { content: none; }
            @top-right { content: none; }
            @bottom-center { content: none; }
        }
        
        body {
            font-family: 'Times New Roman', 'Times', serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #000;
            background: #fff;
            text-align: justify;
            hyphens: auto;
        }
        
        /* Cover Page */
        .cover-page {
            page-break-after: always;
            text-align: center;
            padding: 1in 0.5in;
            border: 4pt double #000;
            margin: 0.5in;
        }
        
        .series-number {
            font-family: 'Courier New', 'Courier', monospace;
            font-size: 14pt;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 0.3in;
        }
        
        .cover-title {
            font-family: 'Times New Roman', 'Times', serif;
            font-size: 24pt;
            font-weight: bold;
            line-height: 1.2;
            margin: 0.3in 0;
            text-transform: uppercase;
            letter-spacing: 0.02em;
        }
        
        .cover-subtitle {
            font-size: 14pt;
            font-style: italic;
            color: #333;
            margin: 0.2in 0;
        }
        
        .classification-box {
            display: inline-block;
            background: #ffff00;
            border: 3pt solid #cc0000;
            padding: 0.15in 0.3in;
            margin: 0.3in 0;
            font-weight: bold;
            font-size: 12pt;
        }
        
        /* Abstract */
        .abstract {
            margin: 0.3in 0;
            padding: 0.2in;
            background: #f9f9f9;
            border: 1pt solid #ddd;
            font-size: 10pt;
            text-align: justify;
        }
        
        .abstract-title {
            font-weight: bold;
            font-size: 11pt;
            margin-bottom: 0.1in;
            text-align: center;
        }
        
        /* Headers (LaTeX-style) */
        h1 {
            font-size: 16pt;
            font-weight: bold;
            margin-top: 0.4in;
            margin-bottom: 0.2in;
            page-break-after: avoid;
            border-bottom: 0.4pt solid #000;
            padding-bottom: 0.05in;
        }
        
        h2 {
            font-size: 14pt;
            font-weight: bold;
            margin-top: 0.3in;
            margin-bottom: 0.15in;
            page-break-after: avoid;
            border-bottom: 0.4pt solid #000;
            padding-bottom: 0.05in;
        }
        
        h3 {
            font-size: 12pt;
            font-weight: bold;
            margin-top: 0.2in;
            margin-bottom: 0.1in;
            page-break-after: avoid;
            font-style: italic;
        }
        
        h4 {
            font-size: 11pt;
            font-weight: bold;
            font-style: italic;
            margin-top: 0.15in;
            margin-bottom: 0.08in;
        }
        
        /* Paragraphs */
        p {
            margin: 0.12in 0;
            text-align: justify;
            orphans: 3;
            widows: 3;
        }
        
        /* Lists */
        ul, ol {
            margin: 0.15in 0;
            padding-left: 0.3in;
        }
        
        li {
            margin-bottom: 0.05in;
        }
        
        /* Code blocks */
        pre {
            font-family: 'Courier New', 'Courier', monospace;
            font-size: 9pt;
            background: #f5f5f5;
            border: 1pt solid #ddd;
            border-left: 3pt solid #0066cc;
            padding: 0.15in;
            margin: 0.2in 0;
            overflow-x: auto;
            page-break-inside: avoid;
        }
        
        code {
            font-family: 'Courier New', 'Courier', monospace;
            font-size: 10pt;
            background: #f5f5f5;
            padding: 0.02in 0.05in;
            border-radius: 2pt;
        }
        
        pre code {
            background: transparent;
            padding: 0;
        }
        
        /* Tables (LaTeX booktabs style) */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.2in 0;
            font-size: 10pt;
            page-break-inside: avoid;
        }
        
        th {
            background: #333;
            color: #fff;
            border-bottom: 2pt solid #000;
            padding: 0.1in;
            text-align: left;
            font-weight: bold;
        }
        
        td {
            border-bottom: 0.5pt solid #ddd;
            padding: 0.08in;
        }
        
        tr:nth-child(even) {
            background: #f9f9f9;
        }
        
        /* Warning/Note boxes (LaTeX tcolorbox style) */
        .warning, .caution, .note {
            margin: 0.2in 0;
            padding: 0.15in;
            page-break-inside: avoid;
            border-radius: 2pt;
        }
        
        .warning {
            background: #ffffe0;
            border: 3pt solid #cc0000;
        }
        
        .warning-title {
            font-weight: bold;
            color: #cc0000;
            text-transform: uppercase;
            margin-bottom: 0.08in;
        }
        
        .caution {
            background: #fff9f0;
            border: 2pt solid #ff9900;
        }
        
        .caution-title {
            font-weight: bold;
            color: #ff9900;
            text-transform: uppercase;
            margin-bottom: 0.08in;
        }
        
        .note {
            background: #f0f8ff;
            border-left: 4pt solid #0066cc;
            padding-left: 0.2in;
        }
        
        .note-title {
            font-weight: bold;
            color: #0066cc;
            text-transform: uppercase;
            margin-bottom: 0.08in;
        }
        
        /* Emphasis */
        strong {
            font-weight: bold;
        }
        
        em {
            font-style: italic;
        }
        
        /* Horizontal rules */
        hr {
            border: none;
            border-top: 0.5pt solid #000;
            margin: 0.3in 0;
        }
    </style>
</head>
<body>
    <!-- Cover Page -->
    <div class="cover-page">
        <div class="series-number">{{ series }} {{ number }}</div>
        <div class="cover-title">{{ title }}</div>
        {% if subtitle %}
        <div class="cover-subtitle">{{ subtitle }}</div>
        {% endif %}
        {% if classification %}
        <div class="classification-box">{{ classification }}</div>
        {% endif %}
        <div style="margin-top: 0.5in;">
            {% if issued_by %}
            <strong>Issued by:</strong> {{ issued_by }}<br>
            {% endif %}
            {% if date %}
            <strong>Date:</strong> {{ date }}
            {% endif %}
        </div>
    </div>
    
    <!-- Abstract -->
    {% if abstract %}
    <div class="abstract">
        <div class="abstract-title">Abstract</div>
        <div>{{ abstract }}</div>
    </div>
    {% endif %}
    
    <!-- Main Content -->
    <div class="content">
        {{ content | safe }}
    </div>
</body>
</html>
"""


def main():
    """Generate WAFT Handbook Field Guide PDF."""
    project_root = Path(__file__).parent.parent
    handbook_md = project_root / "WAFT_FRAMEWORK_HANDBOOK.md"
    output_dir = project_root / "_work_efforts" / "waft_handbook_field_guide"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("📚 Generating WAFT Handbook Field Guide PDF")
    print(f"   Source: {handbook_md}")
    print(f"   Output: {output_dir}")

    # Parse markdown
    print("\n1️⃣  Parsing handbook markdown...")
    data = parse_handbook_markdown(handbook_md)

    # Save JSON data (LaTTe-style)
    json_path = output_dir / "handbook_data.json"
    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"   ✅ Data saved: {json_path}")

    # Generate HTML from template
    print("\n2️⃣  Generating HTML from template...")
    template = Template(FIELD_GUIDE_TEMPLATE)
    html_output = template.render(**data)
    html_path = output_dir / "waft_handbook.html"
    html_path.write_text(html_output, encoding="utf-8")
    print(f"   ✅ HTML saved: {html_path}")

    # Generate PDF
    print("\n3️⃣  Generating PDF...")
    pdf_path = output_dir / "WAFT_FRAMEWORK_HANDBOOK_FIELD_GUIDE.pdf"
    HTML(string=html_output).write_pdf(pdf_path)

    if pdf_path.exists():
        size_mb = pdf_path.stat().st_size / (1024 * 1024)
        print(f"   ✅ PDF generated: {pdf_path}")
        print(f"   📄 Size: {size_mb:.2f} MB")
        print("\n🎉 WAFT Handbook Field Guide ready!")
        print(f"   📄 {pdf_path}")

        # Try to open
        try:
            import platform

            if platform.system() == "Darwin":
                import subprocess

                subprocess.run(["open", str(pdf_path)])
            elif platform.system() == "Linux":
                import subprocess

                subprocess.run(["xdg-open", str(pdf_path)])
        except Exception as e:
            print(f"   ⚠️  Could not auto-open: {e}")

        return 0
    else:
        print("   ❌ PDF generation failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
