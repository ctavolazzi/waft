"""
Field Guide Template
====================

Operational field manual style for survival guides, equipment manuals,
and field procedures. Think: military field manual meets national park guide.

Features:
- Two-column layout
- Warning/caution boxes
- Equipment checklists
- Step-by-step procedures
- Illustrations/diagrams support
- Rugged, practical aesthetic
"""

from pathlib import Path

from jinja2 import Template
from weasyprint import HTML

FIELD_GUIDE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        /* Field Guide Template - Practical, rugged design */

        @page {
            size: letter;
            margin: 0.75in 0.5in;

            @top-left {
                content: "{{ series }} {{ number }}";
                font-family: 'Courier New', monospace;
                font-size: 9pt;
                font-weight: bold;
                text-transform: uppercase;
            }

            @top-right {
                content: "Page " counter(page);
                font-family: 'Courier New', monospace;
                font-size: 9pt;
            }

            @bottom-center {
                content: "{{ classification }}";
                font-family: 'Courier New', monospace;
                font-size: 8pt;
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
            font-size: 10pt;
            line-height: 1.4;
            color: #000;
        }

        /* Cover/Title */
        .cover {
            border: 4px double #000;
            padding: 0.5in;
            margin-bottom: 0.3in;
            background: #f5f5f5;
            text-align: center;
        }

        .series-number {
            font-family: 'Courier New', monospace;
            font-size: 14pt;
            font-weight: bold;
            margin-bottom: 0.2in;
        }

        .title {
            font-family: 'Arial Black', sans-serif;
            font-size: 20pt;
            font-weight: bold;
            text-transform: uppercase;
            line-height: 1.2;
            margin-bottom: 0.2in;
        }

        .subtitle {
            font-size: 12pt;
            font-style: italic;
            color: #333;
        }

        .classification {
            margin-top: 0.2in;
            padding: 0.1in;
            background: #ff0;
            border: 2px solid #000;
            font-weight: bold;
            font-size: 11pt;
        }

        /* Section Headers */
        h2 {
            font-family: 'Arial Black', sans-serif;
            font-size: 14pt;
            font-weight: bold;
            text-transform: uppercase;
            background: #000;
            color: #fff;
            padding: 0.1in;
            margin-top: 0.3in;
            margin-bottom: 0.15in;
            page-break-after: avoid;
        }

        h3 {
            font-size: 12pt;
            font-weight: bold;
            border-bottom: 2px solid #000;
            padding-bottom: 0.05in;
            margin-top: 0.2in;
            margin-bottom: 0.1in;
            page-break-after: avoid;
        }

        h4 {
            font-size: 11pt;
            font-weight: bold;
            font-style: italic;
            margin-top: 0.15in;
            margin-bottom: 0.08in;
        }

        /* Warning Boxes */
        .warning {
            border: 3px solid #c00;
            background: #ffe;
            padding: 0.15in;
            margin: 0.15in 0;
            page-break-inside: avoid;
        }

        .warning-title {
            font-weight: bold;
            font-size: 11pt;
            color: #c00;
            text-transform: uppercase;
            margin-bottom: 0.08in;
        }

        .warning-title::before {
            content: "⚠ ";
            font-size: 14pt;
        }

        .caution {
            border: 2px solid #f90;
            background: #fff9f0;
            padding: 0.15in;
            margin: 0.15in 0;
            page-break-inside: avoid;
        }

        .caution-title {
            font-weight: bold;
            font-size: 10pt;
            color: #f90;
            text-transform: uppercase;
            margin-bottom: 0.08in;
        }

        .note {
            border-left: 4px solid #06c;
            background: #f0f8ff;
            padding: 0.1in 0.15in;
            margin: 0.15in 0;
        }

        .note-title {
            font-weight: bold;
            color: #06c;
            text-transform: uppercase;
            font-size: 9pt;
            margin-bottom: 0.05in;
        }

        /* Checklists */
        .checklist {
            border: 2px solid #000;
            padding: 0.15in;
            margin: 0.15in 0;
            background: #fff;
            page-break-inside: avoid;
        }

        .checklist-title {
            font-weight: bold;
            font-size: 11pt;
            margin-bottom: 0.1in;
            text-transform: uppercase;
        }

        .checklist ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .checklist li {
            margin-bottom: 0.08in;
        }

        .checklist li::before {
            content: "☐ ";
            font-size: 12pt;
            margin-right: 0.08in;
        }

        /* Procedures - numbered steps */
        .procedure {
            counter-reset: step-counter;
            margin: 0.15in 0;
        }

        .procedure .step {
            counter-increment: step-counter;
            margin-bottom: 0.12in;
            padding-left: 0.4in;
            position: relative;
        }

        .procedure .step::before {
            content: counter(step-counter);
            position: absolute;
            left: 0;
            width: 0.3in;
            height: 0.3in;
            background: #000;
            color: #fff;
            font-weight: bold;
            text-align: center;
            line-height: 0.3in;
            border-radius: 50%;
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.15in 0;
            font-size: 9pt;
        }

        th {
            background: #333;
            color: #fff;
            border: 1px solid #000;
            padding: 0.08in;
            text-align: left;
            font-weight: bold;
        }

        td {
            border: 1px solid #666;
            padding: 0.08in;
        }

        tr:nth-child(even) {
            background: #f9f9f9;
        }

        /* Lists */
        ul, ol {
            margin-left: 0.3in;
            margin-bottom: 0.12in;
        }

        li {
            margin-bottom: 0.05in;
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
            padding: 0.02in 0.05in;
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
        {% if classification %}
        <div class="classification">{{ classification }}</div>
        {% endif %}
    </div>

    <!-- Issued by -->
    {% if issued_by %}
    <p style="text-align: center; font-size: 10pt; margin-bottom: 0.3in;">
        <strong>Issued by:</strong> {{ issued_by }}<br>
        {% if date %}<strong>Date:</strong> {{ date }}{% endif %}
    </p>
    {% endif %}

    <!-- Content -->
    <div class="content">
        {{ content | safe }}
    </div>
</body>
</html>
"""


def generate_field_guide(
    title: str,
    content: str,
    output_path: Path,
    series: str = "FIELD GUIDE",
    number: str = "FG-001",
    subtitle: str = None,
    classification: str = "FOR OFFICIAL USE ONLY",
    issued_by: str = None,
    date: str = None,
) -> Path:
    """
    Generate a field guide document (operational manual style).

    Args:
        title: Guide title
        content: Main content (HTML)
        output_path: Where to save PDF
        series: Series name (e.g., "FIELD GUIDE", "OPERATOR'S MANUAL")
        number: Document number (e.g., "FG-001")
        subtitle: Optional subtitle
        classification: Security classification
        issued_by: Issuing organization
        date: Issue date

    Returns:
        Path to generated PDF
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(FIELD_GUIDE_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        series=series,
        number=number,
        subtitle=subtitle,
        classification=classification,
        issued_by=issued_by,
        date=date,
    )

    HTML(string=html_output).write_pdf(output_path)
    return output_path
