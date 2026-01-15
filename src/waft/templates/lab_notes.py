"""
Lab Documentation Template
===========================

Technical lab notebook style for experiment logs, observations,
and research documentation. Handwritten-style aesthetic with grid paper.

Features:
- Grid/graph paper background
- Handwritten font option
- Date/time stamps
- Observation entries
- Sketch areas
- Data tables
- "Laboratory notebook" aesthetic
"""

from pathlib import Path
from jinja2 import Template
from weasyprint import HTML


LAB_NOTES_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        @page {
            size: letter;
            margin: 0.75in;

            /* Grid background */
            background-image:
                linear-gradient(#e0e0e0 1px, transparent 1px),
                linear-gradient(90deg, #e0e0e0 1px, transparent 1px);
            background-size: 0.2in 0.2in;

            @top-left {
                content: "{{ lab_id }}";
                font-family: 'Courier New', monospace;
                font-size: 9pt;
                color: #666;
                background: white;
                padding: 0.05in;
            }

            @top-right {
                content: "Page " counter(page);
                font-family: 'Courier New', monospace;
                font-size: 9pt;
                color: #666;
                background: white;
                padding: 0.05in;
            }

            @bottom-center {
                content: "{{ classification }}";
                font-family: 'Courier New', monospace;
                font-size: 8pt;
                color: #c00;
                font-weight: bold;
                background: white;
                padding: 0.05in;
            }
        }

        @page :first {
            background-image: none;
            background: white;
        }

        body {
            font-family: 'Courier New', 'Consolas', monospace;
            font-size: 11pt;
            line-height: 1.6;
            color: #000;
        }

        /* Cover */
        .lab-cover {
            border: 3px solid #000;
            padding: 0.4in;
            background: white;
            margin-bottom: 0.3in;
        }

        .lab-id {
            font-family: 'Courier New', monospace;
            font-size: 12pt;
            font-weight: bold;
            margin-bottom: 0.15in;
        }

        .lab-title {
            font-size: 18pt;
            font-weight: bold;
            margin-bottom: 0.15in;
            text-transform: uppercase;
        }

        .lab-meta {
            font-size: 10pt;
            line-height: 1.4;
            margin-top: 0.15in;
            border-top: 1px solid #000;
            padding-top: 0.1in;
        }

        /* Entry Headers */
        .entry {
            background: white;
            border: 2px solid #000;
            padding: 0.15in;
            margin: 0.2in 0;
            page-break-inside: avoid;
        }

        .entry-header {
            font-weight: bold;
            border-bottom: 1px solid #000;
            padding-bottom: 0.05in;
            margin-bottom: 0.1in;
        }

        .timestamp {
            float: right;
            font-size: 10pt;
            color: #666;
        }

        /* Section Headers */
        h2 {
            font-size: 14pt;
            font-weight: bold;
            text-decoration: underline;
            margin-top: 0.25in;
            margin-bottom: 0.12in;
            background: white;
            padding: 0.05in;
        }

        h3 {
            font-size: 12pt;
            font-weight: bold;
            margin-top: 0.18in;
            margin-bottom: 0.1in;
            background: white;
            padding: 0.05in;
        }

        h4 {
            font-size: 11pt;
            font-weight: bold;
            font-style: italic;
            margin-top: 0.12in;
            margin-bottom: 0.08in;
            background: white;
        }

        /* Observations */
        .observation {
            background: #fffef8;
            border-left: 4px solid #333;
            padding: 0.12in;
            margin: 0.12in 0;
            font-family: 'Courier New', monospace;
        }

        .observation-time {
            font-weight: bold;
            color: #666;
            font-size: 10pt;
        }

        /* Data Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.15in 0;
            font-size: 10pt;
            background: white;
        }

        th {
            background: #333;
            color: #fff;
            border: 1px solid #000;
            padding: 0.08in;
            text-align: left;
        }

        td {
            border: 1px solid #666;
            padding: 0.08in;
        }

        /* Calculations */
        .calculation {
            background: #f0f8ff;
            border: 1px dashed #06c;
            padding: 0.12in;
            margin: 0.12in 0;
            font-family: 'Courier New', monospace;
            white-space: pre;
        }

        /* Notes/Annotations */
        .note {
            background: #fff9c4;
            border: 1px solid #f90;
            padding: 0.12in;
            margin: 0.12in 0;
            font-size: 10pt;
        }

        .note::before {
            content: "NOTE: ";
            font-weight: bold;
            color: #f90;
        }

        /* Sketch Area */
        .sketch {
            border: 2px dashed #666;
            height: 3in;
            background: white;
            margin: 0.15in 0;
            text-align: center;
            padding-top: 1.4in;
            color: #999;
            font-style: italic;
        }

        /* Signature */
        .signature {
            margin-top: 0.3in;
            padding-top: 0.15in;
            border-top: 2px solid #000;
            background: white;
            padding: 0.15in;
        }

        .signature-line {
            border-bottom: 1px solid #000;
            width: 3in;
            margin-top: 0.2in;
            padding-top: 0.3in;
        }

        /* Lists */
        ul, ol {
            margin-left: 0.3in;
            background: white;
            padding: 0.08in;
        }

        li {
            margin-bottom: 0.05in;
        }

        /* Paragraphs */
        p {
            margin-bottom: 0.12in;
            background: white;
            padding: 0.05in;
        }
    </style>
</head>
<body>
    <!-- Cover Page -->
    <div class="lab-cover">
        <div class="lab-id">{{ lab_id }}</div>
        <div class="lab-title">{{ title }}</div>
        {% if project %}<div>PROJECT: {{ project }}</div>{% endif %}

        <div class="lab-meta">
            {% if researcher %}<strong>RESEARCHER:</strong> {{ researcher }}<br>{% endif %}
            {% if facility %}<strong>FACILITY:</strong> {{ facility }}<br>{% endif %}
            {% if date %}<strong>DATE:</strong> {{ date }}<br>{% endif %}
            {% if classification %}<strong>CLASSIFICATION:</strong> {{ classification }}{% endif %}
        </div>
    </div>

    <!-- Content -->
    <div class="content">
        {{ content | safe }}
    </div>

    <!-- Signature Block -->
    {% if researcher %}
    <div class="signature">
        <div>I certify that this is an accurate record of my work.</div>
        <div class="signature-line"></div>
        <div style="margin-top: 0.05in;">
            <strong>{{ researcher }}</strong><br>
            {% if date %}{{ date }}{% endif %}
        </div>
    </div>
    {% endif %}
</body>
</html>
"""


def generate_lab_notes(
    title: str,
    content: str,
    output_path: Path,
    lab_id: str = "LAB-001",
    researcher: str = None,
    facility: str = None,
    project: str = None,
    date: str = None,
    classification: str = "CONFIDENTIAL"
) -> Path:
    """
    Generate laboratory documentation in notebook style.

    Args:
        title: Experiment/documentation title
        content: Main content (HTML)
        output_path: Where to save PDF
        lab_id: Lab notebook ID
        researcher: Researcher name
        facility: Laboratory facility
        project: Project name
        date: Entry date
        classification: Security classification

    Returns:
        Path to generated PDF
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(LAB_NOTES_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        lab_id=lab_id,
        researcher=researcher,
        facility=facility,
        project=project,
        date=date,
        classification=classification
    )

    HTML(string=html_output).write_pdf(output_path)
    
    # Post-process to add blank page markers
    try:
        from ..utils import process_pdf_for_blank_pages
        process_pdf_for_blank_pages(output_path)
    except Exception as e:
        print(f"⚠️  Blank page marker processing failed: {e}")
    
    return output_path
