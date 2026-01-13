"""
Briefing Template
=================

Field guide style template optimized for 2-page briefing documents.
Combines operational manual aesthetic with one-pager constraints.

Perfect for:
- Session briefings
- Status reports
- "At a glance" documentation
- Handoff documents
"""

from pathlib import Path
from jinja2 import Template
from weasyprint import HTML


BRIEFING_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        /* Briefing Template - Field Guide Style, 2-Page Constraint */

        @page {
            size: letter;
            margin: 0.5in 0.4in;
            background: #fff;

            @top-left {
                content: "{{ series }} {{ number }}";
                font-family: 'Courier New', monospace;
                font-size: 8pt;
                font-weight: bold;
                text-transform: uppercase;
            }

            @top-right {
                content: "Page " counter(page);
                font-family: 'Courier New', monospace;
                font-size: 8pt;
            }

            @bottom-center {
                content: "{{ classification }}";
                font-family: 'Courier New', monospace;
                font-size: 7pt;
                color: #c00;
                font-weight: bold;
            }
        }

        @page :first {
            @top-left { content: none; }
            @top-right { content: none; }
        }

        body {
            font-family: 'Arial', 'Helvetica', sans-serif;
            font-size: 9.5pt;
            line-height: 1.4;
            color: #000;
            background: #fff;
        }

        /* Header */
        .header {
            border: 3px double #000;
            padding: 0.2in;
            margin-bottom: 0.2in;
            background: #fff;
            text-align: center;
        }

        .series-number {
            font-family: 'Courier New', monospace;
            font-size: 10pt;
            font-weight: bold;
            margin-bottom: 0.1in;
            text-transform: uppercase;
        }

        .title {
            font-family: 'Arial Black', sans-serif;
            font-size: 18pt;
            font-weight: bold;
            text-transform: uppercase;
            line-height: 1.2;
            margin-bottom: 0.1in;
        }

        .subtitle {
            font-size: 10pt;
            font-style: italic;
            color: #333;
            margin-bottom: 0.1in;
        }

        .classification {
            margin-top: 0.1in;
            padding: 0.08in;
            background: #ff0;
            border: 2px solid #000;
            font-weight: bold;
            font-size: 9pt;
        }

        .issued-by {
            margin-top: 0.1in;
            font-size: 8pt;
            color: #666;
        }

        /* Section Headers */
        h2 {
            font-family: 'Arial Black', sans-serif;
            font-size: 12pt;
            font-weight: bold;
            text-transform: uppercase;
            color: #000;
            border-bottom: 3px solid #000;
            padding-bottom: 0.05in;
            margin-top: 0.2in;
            margin-bottom: 0.1in;
            page-break-after: avoid;
        }

        h3 {
            font-size: 10pt;
            font-weight: bold;
            border-bottom: 2px solid #000;
            padding-bottom: 0.03in;
            margin-top: 0.15in;
            margin-bottom: 0.08in;
            page-break-after: avoid;
        }

        h4 {
            font-size: 9pt;
            font-weight: bold;
            font-style: italic;
            margin-top: 0.1in;
            margin-bottom: 0.06in;
        }

        /* Warning Boxes */
        .warning {
            border: 2px solid #c00;
            background: #ffe;
            padding: 0.1in;
            margin: 0.1in 0;
            page-break-inside: avoid;
        }

        .warning-title {
            font-weight: bold;
            font-size: 9pt;
            color: #c00;
            text-transform: uppercase;
            margin-bottom: 0.05in;
        }

        .warning-title::before {
            content: "⚠ ";
            font-size: 11pt;
        }

        .caution {
            border: 2px solid #f90;
            background: #fff9f0;
            padding: 0.1in;
            margin: 0.1in 0;
            page-break-inside: avoid;
        }

        .caution-title {
            font-weight: bold;
            font-size: 8pt;
            color: #f90;
            text-transform: uppercase;
            margin-bottom: 0.05in;
        }

        .note {
            border-left: 3px solid #06c;
            background: #f0f8ff;
            padding: 0.08in 0.1in;
            margin: 0.1in 0;
        }

        .note-title {
            font-weight: bold;
            color: #06c;
            text-transform: uppercase;
            font-size: 8pt;
            margin-bottom: 0.04in;
        }

        /* Status Boxes */
        .status-box {
            border: 2px solid #000;
            padding: 0.1in;
            margin: 0.1in 0;
            background: #fff;
            page-break-inside: avoid;
        }

        .status-title {
            font-weight: bold;
            font-size: 9pt;
            margin-bottom: 0.06in;
            text-transform: uppercase;
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.1in 0;
            font-size: 8.5pt;
        }

        th {
            background: #333;
            color: #fff;
            border: 1px solid #000;
            padding: 0.06in;
            text-align: left;
            font-weight: bold;
        }

        td {
            border: 1px solid #666;
            padding: 0.06in;
        }

        tr:nth-child(even) {
            background: #f9f9f9;
        }

        /* Lists */
        ul, ol {
            margin-left: 0.25in;
            margin-bottom: 0.1in;
        }

        li {
            margin-bottom: 0.04in;
        }

        /* Emphasis */
        strong {
            font-weight: bold;
        }

        em {
            font-style: italic;
        }

        .highlight {
            background: #ff0;
            padding: 0.01in 0.03in;
        }

        /* Compact spacing for 2-page constraint */
        p {
            margin: 0.06in 0;
            text-align: justify;
        }

        /* Page breaks */
        .page-break {
            page-break-before: always;
        }
    </style>
</head>
<body>
    <!-- Header -->
    <div class="header">
        <div class="series-number">{{ series }} {{ number }}</div>
        <div class="title">{{ title }}</div>
        {% if subtitle %}
        <div class="subtitle">{{ subtitle }}</div>
        {% endif %}
        {% if classification %}
        <div class="classification">{{ classification }}</div>
        {% endif %}
        {% if issued_by %}
        <div class="issued-by">
            <strong>Issued by:</strong> {{ issued_by }}<br>
            {% if date %}<strong>Date:</strong> {{ date }}{% endif %}
        </div>
        {% endif %}
    </div>

    <!-- Content -->
    <div class="content">
        {{ content | safe }}
    </div>
</body>
</html>
"""


def generate_briefing(
    title: str,
    content: str,
    output_path: Path,
    series: str = "BRIEFING",
    number: str = "BG-001",
    subtitle: str = None,
    classification: str = "INTERNAL",
    issued_by: str = None,
    date: str = None
) -> Path:
    """
    Generate a briefing document (field guide style, 2-page constraint).

    Args:
        title: Briefing title
        content: Main content (HTML)
        output_path: Where to save PDF
        series: Series name (e.g., "BRIEFING", "STATUS REPORT")
        number: Document number (e.g., "BG-001")
        subtitle: Optional subtitle
        classification: Security classification
        issued_by: Issuing organization
        date: Issue date

    Returns:
        Path to generated PDF
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(BRIEFING_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        series=series,
        number=number,
        subtitle=subtitle,
        classification=classification,
        issued_by=issued_by,
        date=date
    )

    HTML(string=html_output).write_pdf(output_path)
    return output_path
