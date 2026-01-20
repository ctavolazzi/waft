"""
Succulent Jewelry Guide Template
=================================

Flexible guide template for creating helpful PDF guides on various topics:
- Jewelry casting techniques
- Succulent care
- Music-themed guides
- General how-to guides

Based on field_guide template but adapted for commercial guides.
"""

from pathlib import Path
from jinja2 import Template
from weasyprint import HTML
from typing import Optional


GUIDE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        /* Succulent Jewelry Guide Template - Clean, professional design */

        @page {
            size: letter;
            margin: 0.75in 0.5in;

            @top-left {
                content: "{{ series }} {{ number }}";
                font-family: 'Courier New', monospace;
                font-size: 9pt;
                font-weight: bold;
                text-transform: uppercase;
                color: #666;
            }

            @top-right {
                content: "Page " counter(page);
                font-family: 'Courier New', monospace;
                font-size: 9pt;
                color: #666;
            }

            @bottom-center {
                content: "{{ author }}";
                font-family: 'Courier New', monospace;
                font-size: 8pt;
                color: #999;
            }
        }

        @page :first {
            @top-left { content: none; }
            @top-right { content: none; }
            @bottom-center { content: none; }
        }

        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
        }

        /* Cover Page */
        .cover {
            text-align: center;
            padding: 1in 0.5in;
            margin-bottom: 0.5in;
        }

        .series-number {
            font-family: 'Courier New', monospace;
            font-size: 12pt;
            color: #666;
            margin-bottom: 0.3in;
            text-transform: uppercase;
        }

        .title {
            font-family: 'Arial', 'Helvetica', sans-serif;
            font-size: 28pt;
            font-weight: bold;
            line-height: 1.2;
            margin-bottom: 0.2in;
            color: #000;
        }

        .subtitle {
            font-size: 14pt;
            font-style: italic;
            color: #555;
            margin-bottom: 0.3in;
        }

        .cover-image {
            max-width: 4in;
            margin: 0.3in auto;
            text-align: center;
        }

        .cover-image img {
            max-width: 100%;
            height: auto;
        }

        /* Section Headers */
        h1 {
            font-family: 'Arial', 'Helvetica', sans-serif;
            font-size: 18pt;
            font-weight: bold;
            color: #000;
            margin-top: 0.4in;
            margin-bottom: 0.2in;
            page-break-after: avoid;
            border-bottom: 3px solid #000;
            padding-bottom: 0.1in;
        }

        h2 {
            font-family: 'Arial', 'Helvetica', sans-serif;
            font-size: 14pt;
            font-weight: bold;
            color: #333;
            margin-top: 0.3in;
            margin-bottom: 0.15in;
            page-break-after: avoid;
        }

        h3 {
            font-size: 12pt;
            font-weight: bold;
            color: #555;
            margin-top: 0.2in;
            margin-bottom: 0.1in;
            page-break-after: avoid;
        }

        /* Tips and Warnings */
        .tip {
            border-left: 4px solid #4CAF50;
            background: #f1f8f4;
            padding: 0.15in;
            margin: 0.15in 0;
            page-break-inside: avoid;
            position: relative;
            z-index: 1;
            overflow: hidden;
        }

        .tip-title {
            font-weight: bold;
            color: #2e7d32;
            margin-bottom: 0.08in;
            position: relative;
            z-index: 2;
        }

        .tip-title::before {
            content: "💡 ";
            display: inline-block;
            text-shadow: none;
            filter: none;
        }

        .warning {
            border-left: 4px solid #f44336;
            background: #ffebee;
            padding: 0.15in;
            margin: 0.15in 0;
            page-break-inside: avoid;
        }

        .warning-title {
            font-weight: bold;
            color: #c62828;
            margin-bottom: 0.08in;
        }

        .warning-title::before {
            content: "⚠️ ";
        }

        .caution {
            border-left: 4px solid #ff9800;
            background: #fff3e0;
            padding: 0.15in;
            margin: 0.15in 0;
            page-break-inside: avoid;
        }

        .caution-title {
            font-weight: bold;
            color: #e65100;
            margin-bottom: 0.08in;
        }

        .caution-title::before {
            content: "⚠ ";
        }

        /* Step-by-step Procedures */
        .procedure {
            counter-reset: step-counter;
            margin: 0.2in 0;
            list-style: none;
            padding: 0;
        }

        .procedure .step {
            counter-increment: step-counter;
            margin-bottom: 0.15in;
            padding-left: 0.6in;
            position: relative;
            display: block;
            min-height: 0.35in;
        }

        .procedure .step::before {
            content: counter(step-counter, decimal);
            position: absolute;
            left: 0;
            top: 0;
            width: 0.35in;
            height: 0.35in;
            background: #333;
            color: #fff;
            font-weight: bold;
            text-align: center;
            line-height: 0.35in;
            border-radius: 50%;
            font-size: 10pt;
            z-index: 10;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: none !important;
            -webkit-box-shadow: none !important;
            filter: none !important;
            -webkit-filter: none !important;
            text-shadow: none !important;
            -webkit-text-shadow: none !important;
        }

        /* Images */
        img {
            max-width: 100%;
            height: auto;
            margin: 0.2in 0;
            page-break-inside: avoid;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }

        .image-caption {
            font-size: 9pt;
            font-style: italic;
            color: #666;
            text-align: center;
            margin-top: 0.05in;
            margin-bottom: 0.15in;
        }

        .image-caption a {
            color: #666;
            text-decoration: underline;
        }

        .image-attribution {
            font-size: 8pt;
            font-style: italic;
            color: #999;
            text-align: center;
            margin-top: 0.02in;
            margin-bottom: 0.1in;
        }

        .image-attribution a {
            color: #999;
            text-decoration: underline;
        }

        .image-container {
            text-align: center;
            margin: 0.3in 0;
            page-break-inside: avoid;
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.2in 0;
            font-size: 10pt;
        }

        th {
            background: #f5f5f5;
            border: 1px solid #ddd;
            padding: 0.1in;
            text-align: left;
            font-weight: bold;
        }

        td {
            border: 1px solid #ddd;
            padding: 0.1in;
        }

        tr:nth-child(even) {
            background: #fafafa;
        }

        /* Lists */
        ul, ol {
            margin-left: 0.4in;
            margin-bottom: 0.15in;
        }

        li {
            margin-bottom: 0.08in;
        }

        /* Emphasis */
        strong {
            font-weight: bold;
            color: #000;
        }

        em {
            font-style: italic;
        }

        code {
            font-family: 'Courier New', monospace;
            background: #f5f5f5;
            padding: 0.02in 0.05in;
            border-radius: 3px;
            font-size: 10pt;
        }

        pre {
            background: #f5f5f5;
            border: 1px solid #ddd;
            padding: 0.15in;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 9pt;
        }

        /* Resources Section */
        .resources {
            border-top: 2px solid #ddd;
            margin-top: 0.4in;
            padding-top: 0.2in;
        }

        /* Back Cover / Gumroad Link */
        .back-cover {
            page-break-before: always;
            text-align: center;
            padding: 1in;
        }

        .gumroad-link {
            margin-top: 0.5in;
            padding: 0.2in;
            background: #f5f5f5;
            border: 2px solid #333;
            display: inline-block;
        }

        /* Page breaks */
        .page-break {
            page-break-before: always;
        }
    </style>
</head>
<body>
    <!-- Cover Page -->
    <div class="cover">
        <div class="series-number">{{ series }} {{ number }}</div>
        <div class="title">{{ title }}</div>
        {% if subtitle %}
        <div class="subtitle">{{ subtitle }}</div>
        {% endif %}
        {% if cover_image %}
        <div class="cover-image">
            <img src="{{ cover_image }}" alt="Cover image">
        </div>
        {% endif %}
        {% if author %}
        <p style="margin-top: 0.3in; font-size: 11pt; color: #666;">
            by {{ author }}
        </p>
        {% endif %}
    </div>

    <!-- Introduction -->
    {% if introduction %}
    <h1>Introduction</h1>
    <div class="introduction">
        {{ introduction | safe }}
    </div>
    {% endif %}

    <!-- Main Content -->
    <div class="content">
        {{ content | safe }}
    </div>

    <!-- Resources -->
    {% if resources %}
    <div class="resources">
        <h1>Resources</h1>
        {{ resources | safe }}
    </div>
    {% endif %}

    <!-- Image Attribution Footer -->
    <div style="page-break-before: always; border-top: 1px solid #ddd; padding-top: 0.2in; margin-top: 0.4in; font-size: 8pt; color: #999;">
        <h3 style="font-size: 10pt; color: #666; margin-bottom: 0.1in;">Image Credits</h3>
        <p>Images provided by <a href="https://pixabay.com">Pixabay</a> and <a href="https://www.pexels.com">Pexels</a>.</p>
        <p>All images are used in accordance with their respective licenses. Photographer credits are included where available.</p>
    </div>

    <!-- Back Cover with Gumroad Link -->
    {% if include_gumroad_link %}
    <div class="back-cover">
        <h2>Get More Guides</h2>
        <p>Visit our Gumroad store for more helpful guides and resources.</p>
        <div class="gumroad-link">
            <strong>Available on Gumroad</strong><br>
            <em>Search for: {{ title }}</em>
        </div>
    </div>
    {% endif %}
</body>
</html>
"""


def generate_guide(
    title: str,
    content: str,
    output_path: Path,
    series: str = "SUCCULENT JEWELRY GUIDE",
    number: str = "GUIDE-001",
    subtitle: Optional[str] = None,
    author: Optional[str] = None,
    introduction: Optional[str] = None,
    resources: Optional[str] = None,
    cover_image: Optional[str] = None,
    include_gumroad_link: bool = True
) -> Path:
    """
    Generate a guide PDF document.

    Args:
        title: Guide title
        content: Main content (HTML)
        output_path: Where to save PDF
        series: Series name (default: "SUCCULENT JEWELRY GUIDE")
        number: Document number (default: "GUIDE-001")
        subtitle: Optional subtitle
        author: Author name
        introduction: Optional introduction section (HTML)
        resources: Optional resources section (HTML)
        cover_image: Optional path to cover image
        include_gumroad_link: Whether to include Gumroad link on back cover

    Returns:
        Path to generated PDF
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(GUIDE_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        series=series,
        number=number,
        subtitle=subtitle,
        author=author,
        introduction=introduction,
        resources=resources,
        cover_image=cover_image,
        include_gumroad_link=include_gumroad_link
    )

    HTML(string=html_output).write_pdf(output_path)
    return output_path
