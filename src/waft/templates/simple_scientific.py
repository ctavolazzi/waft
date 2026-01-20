"""
Simple Scientific Document Template
====================================

A clean, minimal template for scientific documents.
This is the CORE building block - professional, readable, standard.

Features:
- Standard 1-inch margins
- Professional typography
- Clear section hierarchy
- Simple header/footer
- No distractions

Use this as the foundation for more complex templates.
"""

from pathlib import Path

from jinja2 import Template
from weasyprint import HTML

# Simple, clean HTML/CSS template
SIMPLE_SCIENTIFIC_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>

    <style>
        /* ============================================
           SIMPLE SCIENTIFIC DOCUMENT TEMPLATE
           Clean, professional, distraction-free
           ============================================ */

        /* Page Setup */
        @page {
            size: letter;  /* 8.5" x 11" */
            margin: 1in;   /* Standard 1-inch margins */

            /* Simple header */
            @top-center {
                content: "{{ short_title }}";
                font-family: 'Times New Roman', Times, serif;
                font-size: 10pt;
                color: #666;
            }

            /* Simple footer with page number */
            @bottom-center {
                content: "Page " counter(page);
                font-family: 'Times New Roman', Times, serif;
                font-size: 10pt;
                color: #666;
            }
        }

        /* First page - no header */
        @page :first {
            @top-center {
                content: none;
            }
        }

        /* Body Typography */
        body {
            font-family: 'Times New Roman', Times, serif;
            font-size: 12pt;
            line-height: 1.6;
            color: #000;
            text-align: justify;
        }

        /* Title */
        h1.document-title {
            font-size: 18pt;
            font-weight: bold;
            text-align: center;
            margin-top: 0;
            margin-bottom: 0.5in;
            line-height: 1.3;
        }

        /* Authors */
        .authors {
            text-align: center;
            font-size: 12pt;
            margin-bottom: 0.3in;
        }

        .author {
            display: inline-block;
            margin: 0 0.2in;
        }

        /* Date */
        .date {
            text-align: center;
            font-size: 11pt;
            color: #666;
            margin-bottom: 0.5in;
        }

        /* Abstract */
        .abstract {
            margin: 0.5in 0.5in;
            padding: 0.3in;
            background: #f9f9f9;
            border-left: 3px solid #333;
        }

        .abstract-title {
            font-weight: bold;
            font-size: 11pt;
            text-transform: uppercase;
            margin-bottom: 0.1in;
        }

        .abstract-content {
            font-size: 11pt;
            line-height: 1.5;
        }

        /* Section Headings */
        h2 {
            font-size: 14pt;
            font-weight: bold;
            margin-top: 0.3in;
            margin-bottom: 0.15in;
            page-break-after: avoid;
        }

        h3 {
            font-size: 12pt;
            font-weight: bold;
            margin-top: 0.2in;
            margin-bottom: 0.1in;
            page-break-after: avoid;
        }

        h4 {
            font-size: 12pt;
            font-style: italic;
            margin-top: 0.15in;
            margin-bottom: 0.1in;
            page-break-after: avoid;
        }

        /* Paragraphs */
        p {
            margin-top: 0;
            margin-bottom: 0.15in;
            text-indent: 0;
        }

        /* Lists */
        ul, ol {
            margin-left: 0.3in;
            margin-bottom: 0.15in;
        }

        li {
            margin-bottom: 0.05in;
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.2in 0;
            page-break-inside: avoid;
        }

        table caption {
            font-weight: bold;
            margin-bottom: 0.1in;
            text-align: left;
        }

        th {
            background: #f0f0f0;
            border: 1px solid #666;
            padding: 0.1in;
            font-weight: bold;
            text-align: left;
        }

        td {
            border: 1px solid #999;
            padding: 0.1in;
        }

        /* Figures */
        .figure {
            text-align: center;
            margin: 0.2in 0;
            page-break-inside: avoid;
        }

        .figure img {
            max-width: 100%;
            height: auto;
        }

        .figure-caption {
            font-size: 11pt;
            margin-top: 0.1in;
            text-align: left;
        }

        /* Code Blocks */
        pre {
            background: #f5f5f5;
            border: 1px solid #ddd;
            padding: 0.15in;
            font-family: 'Courier New', Courier, monospace;
            font-size: 10pt;
            line-height: 1.4;
            overflow-x: auto;
            page-break-inside: avoid;
        }

        code {
            font-family: 'Courier New', Courier, monospace;
            font-size: 10pt;
            background: #f5f5f5;
            padding: 0.02in 0.05in;
        }

        /* Equations (placeholder for MathJax) */
        .math-display {
            text-align: center;
            margin: 0.2in 0;
            font-style: italic;
        }

        .math-inline {
            font-style: italic;
        }

        /* References */
        .references {
            margin-top: 0.3in;
        }

        .references h2 {
            border-bottom: 2px solid #333;
            padding-bottom: 0.05in;
        }

        .reference {
            margin-bottom: 0.1in;
            padding-left: 0.3in;
            text-indent: -0.3in;
        }

        /* Utilities */
        .page-break {
            page-break-before: always;
        }

        .no-break {
            page-break-inside: avoid;
        }
    </style>
</head>
<body>
    <!-- Title Page -->
    <h1 class="document-title">{{ title }}</h1>

    {% if authors %}
    <div class="authors">
        {% for author in authors %}
        <span class="author">{{ author }}</span>
        {% endfor %}
    </div>
    {% endif %}

    {% if date %}
    <div class="date">{{ date }}</div>
    {% endif %}

    <!-- Abstract -->
    {% if abstract %}
    <div class="abstract">
        <div class="abstract-title">Abstract</div>
        <div class="abstract-content">{{ abstract }}</div>
    </div>
    {% endif %}

    <!-- Main Content -->
    <div class="content">
        {{ content | safe }}
    </div>

    <!-- References (if provided) -->
    {% if references %}
    <div class="references">
        <h2>References</h2>
        {% for ref in references %}
        <div class="reference">{{ ref }}</div>
        {% endfor %}
    </div>
    {% endif %}
</body>
</html>
"""


def generate_simple_scientific_document(
    title: str,
    content: str,
    output_path: Path,
    authors: list = None,
    date: str = None,
    abstract: str = None,
    references: list = None,
    short_title: str = None,
) -> Path:
    """
    Generate a simple scientific document using the clean template.

    Args:
        title: Document title
        content: Main content (HTML)
        output_path: Where to save the PDF
        authors: List of author names
        date: Publication date
        abstract: Abstract text
        references: List of reference strings
        short_title: Short title for header (defaults to first 50 chars of title)

    Returns:
        Path to generated PDF
    """
    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Default short title
    if not short_title:
        short_title = title[:50] + "..." if len(title) > 50 else title

    # Render template
    template = Template(SIMPLE_SCIENTIFIC_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        authors=authors or [],
        date=date,
        abstract=abstract,
        references=references or [],
        short_title=short_title,
    )

    # Generate PDF
    HTML(string=html_output).write_pdf(output_path)

    return output_path


# Example usage
if __name__ == "__main__":
    # Sample content
    sample_content = """
    <h2>1. Introduction</h2>
    <p>
        This is a simple scientific document template. It uses standard typography,
        clean layout, and professional formatting suitable for academic papers,
        technical reports, and research documents.
    </p>

    <h2>2. Methods</h2>
    <p>
        The template is built using HTML/CSS and WeasyPrint for PDF generation.
        It follows established typographic conventions for scientific publishing.
    </p>

    <h3>2.1 Typography</h3>
    <p>
        We use Times New Roman at 12pt with 1.6 line spacing for optimal readability.
        Section headings use a clear hierarchy (14pt bold for h2, 12pt bold for h3).
    </p>

    <h2>3. Results</h2>
    <p>
        Here's an example table:
    </p>

    <table>
        <caption>Table 1: Sample Data</caption>
        <tr>
            <th>Parameter</th>
            <th>Value</th>
            <th>Units</th>
        </tr>
        <tr>
            <td>Temperature</td>
            <td>298</td>
            <td>K</td>
        </tr>
        <tr>
            <td>Pressure</td>
            <td>1.0</td>
            <td>atm</td>
        </tr>
    </table>

    <p>
        And an example code block:
    </p>

    <pre><code>def calculate_energy(mass, c=299792458):
    # Calculate energy using E=mc^2
    return mass * c ** 2</code></pre>

    <h2>4. Discussion</h2>
    <p>
        This template provides a clean foundation for scientific documents.
        It can be extended with additional features like equation numbering,
        cross-references, and citation management.
    </p>

    <h2>5. Conclusion</h2>
    <p>
        Simple, clean, professional. This is the core building block.
    </p>
    """

    # Generate sample document
    output_path = Path("_work_efforts/test_simple_scientific.pdf")

    generate_simple_scientific_document(
        title="A Simple Scientific Document Template",
        content=sample_content,
        output_path=output_path,
        authors=["John Smith", "Jane Doe"],
        date="January 2026",
        abstract=(
            "This document demonstrates a clean, simple template for scientific "
            "publishing. It uses standard typography, clear hierarchy, and "
            "professional formatting. This template serves as the foundation "
            "for more complex document types."
        ),
        references=[
            "[1] Smith, J. (2025). Document Design Principles. Journal of Typography, 12(3), 45-67.",
            "[2] Doe, J. (2024). Scientific Publishing Best Practices. Academic Press.",
        ],
    )

    print(f"✓ Generated: {output_path}")
    print(f"  Size: {output_path.stat().st_size:,} bytes")
