"""
TELEPORT MASSIVE Report Template
=================================

Generic corporate/bureaucratic report template with TELEPORT MASSIVE branding.
Clean, professional, slightly dystopian corporate aesthetic.

Features:
- TM branded header
- Professional typography
- Summary boxes
- Section numbering
- Signature blocks
- "1990s office chic" aesthetic
"""

from pathlib import Path
from jinja2 import Template
from weasyprint import HTML


TM_REPORT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        @page {
            size: letter;
            margin: 1in 0.75in;

            @top-center {
                content: "{{ doc_id }}";
                font-family: 'Courier New', monospace;
                font-size: 9pt;
                color: #666;
            }

            @bottom-left {
                content: "{{ classification }}";
                font-family: 'Arial', sans-serif;
                font-size: 8pt;
                color: #c00;
                font-weight: bold;
            }

            @bottom-right {
                content: "Page " counter(page) " of " counter(pages);
                font-family: 'Arial', sans-serif;
                font-size: 9pt;
                color: #666;
            }
        }

        @page :first {
            @top-center { content: none; }
        }

        body {
            font-family: 'Arial', 'Helvetica', sans-serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #000;
        }

        /* TM Header */
        .tm-header {
            border-bottom: 4px solid #000;
            padding-bottom: 0.15in;
            margin-bottom: 0.3in;
        }

        .tm-logo {
            font-family: 'Arial Black', sans-serif;
            font-size: 24pt;
            font-weight: bold;
            letter-spacing: 2px;
        }

        .tm-tagline {
            font-size: 9pt;
            color: #666;
            font-style: italic;
            margin-top: 0.05in;
        }

        /* Document Header */
        .doc-header {
            background: #f0f0f0;
            border: 2px solid #000;
            padding: 0.2in;
            margin-bottom: 0.3in;
        }

        .doc-id {
            font-family: 'Courier New', monospace;
            font-size: 10pt;
            font-weight: bold;
            margin-bottom: 0.1in;
        }

        .doc-title {
            font-size: 16pt;
            font-weight: bold;
            margin-bottom: 0.1in;
        }

        .doc-meta {
            font-size: 9pt;
            color: #333;
            line-height: 1.3;
        }

        .doc-meta strong {
            display: inline-block;
            width: 1.2in;
        }

        /* Classification Banner */
        .classification {
            background: #c00;
            color: #fff;
            text-align: center;
            padding: 0.1in;
            font-weight: bold;
            font-size: 12pt;
            margin-bottom: 0.2in;
        }

        /* Summary Box */
        .summary {
            border: 2px solid #06c;
            background: #f0f8ff;
            padding: 0.2in;
            margin: 0.2in 0;
            page-break-inside: avoid;
        }

        .summary-title {
            font-weight: bold;
            font-size: 12pt;
            color: #06c;
            text-transform: uppercase;
            margin-bottom: 0.1in;
        }

        /* Section Headers */
        h2 {
            font-size: 14pt;
            font-weight: bold;
            border-bottom: 2px solid #000;
            padding-bottom: 0.05in;
            margin-top: 0.3in;
            margin-bottom: 0.15in;
            page-break-after: avoid;
        }

        h2::before {
            counter-increment: section;
            content: counter(section) ". ";
        }

        body {
            counter-reset: section;
        }

        h3 {
            font-size: 12pt;
            font-weight: bold;
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

        /* Paragraphs */
        p {
            margin-bottom: 0.12in;
            text-align: justify;
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.15in 0;
            font-size: 10pt;
        }

        table caption {
            font-weight: bold;
            text-align: left;
            margin-bottom: 0.08in;
            font-size: 10pt;
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
            border: 1px solid #999;
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

        /* Recommendations/Action Items */
        .recommendation {
            border-left: 4px solid #f90;
            background: #fffaf0;
            padding: 0.15in;
            margin: 0.15in 0;
            page-break-inside: avoid;
        }

        .recommendation-title {
            font-weight: bold;
            color: #f90;
            text-transform: uppercase;
            font-size: 10pt;
            margin-bottom: 0.08in;
        }

        /* Signature Block */
        .signature-block {
            margin-top: 0.4in;
            page-break-inside: avoid;
        }

        .signature-line {
            margin-top: 0.3in;
            border-top: 1px solid #000;
            width: 3in;
            padding-top: 0.05in;
            font-size: 10pt;
        }

        .signature-name {
            font-weight: bold;
        }

        .signature-title {
            font-size: 9pt;
            color: #666;
        }

        /* Footer */
        .footer-notice {
            margin-top: 0.4in;
            padding-top: 0.15in;
            border-top: 1px solid #ccc;
            font-size: 8pt;
            color: #666;
            text-align: center;
        }
    </style>
</head>
<body>
    <!-- TM Header (first page only) -->
    <div class="tm-header">
        <div class="tm-logo">TELEPORT MASSIVE</div>
        <div class="tm-tagline">{{ tagline }}</div>
    </div>

    <!-- Classification -->
    {% if classification %}
    <div class="classification">{{ classification }}</div>
    {% endif %}

    <!-- Document Header -->
    <div class="doc-header">
        <div class="doc-id">{{ doc_id }}</div>
        <div class="doc-title">{{ title }}</div>
        <div class="doc-meta">
            {% if date %}<strong>Date:</strong> {{ date }}<br>{% endif %}
            {% if author %}<strong>Author:</strong> {{ author }}<br>{% endif %}
            {% if department %}<strong>Department:</strong> {{ department }}<br>{% endif %}
            {% if distribution %}<strong>Distribution:</strong> {{ distribution }}{% endif %}
        </div>
    </div>

    <!-- Executive Summary -->
    {% if summary %}
    <div class="summary">
        <div class="summary-title">Executive Summary</div>
        {{ summary | safe }}
    </div>
    {% endif %}

    <!-- Main Content -->
    <div class="content">
        {{ content | safe }}
    </div>

    <!-- Signatures -->
    {% if signatures %}
    <div class="signature-block">
        {% for sig in signatures %}
        <div class="signature-line">
            <div class="signature-name">{{ sig.name }}</div>
            <div class="signature-title">{{ sig.title }}</div>
            {% if sig.date %}<div style="font-size: 9pt;">{{ sig.date }}</div>{% endif %}
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <!-- Footer Notice -->
    <div class="footer-notice">
        This document contains proprietary information of TELEPORT MASSIVE.<br>
        Unauthorized disclosure may result in severe penalties.
    </div>
</body>
</html>
"""


def generate_tm_report(
    title: str,
    content: str,
    output_path: Path,
    doc_id: str = "TM-RPT-001",
    classification: str = "INTERNAL USE ONLY",
    tagline: str = "Making the Impossible, Inevitable™",
    date: str = None,
    author: str = None,
    department: str = None,
    distribution: str = None,
    summary: str = None,
    signatures: list = None
) -> Path:
    """
    Generate a TELEPORT MASSIVE branded report.

    Args:
        title: Report title
        content: Main content (HTML)
        output_path: Where to save PDF
        doc_id: Document ID (e.g., "TM-RPT-001")
        classification: Security classification
        tagline: Company tagline
        date: Report date
        author: Author name
        department: Department
        distribution: Distribution list
        summary: Executive summary (HTML)
        signatures: List of dicts with 'name', 'title', 'date' keys

    Returns:
        Path to generated PDF
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(TM_REPORT_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        doc_id=doc_id,
        classification=classification,
        tagline=tagline,
        date=date,
        author=author,
        department=department,
        distribution=distribution,
        summary=summary,
        signatures=signatures or []
    )

    HTML(string=html_output).write_pdf(output_path)
    return output_path
