"""
WAFT Town Court Document Template
==================================

Official template for WAFT Town court documents, council proceedings, and legal records.
Designed for TheCouncil Town Court System.

Formatting Elements:
- Official court document headers
- Council member signatures
- Voting records and tallies
- Legal proceedings format
- Official seals and classifications
- Case numbers and docket references

Perfect for:
- Court proceedings
- Council resolutions
- Voting records
- Legal documentation
- Town governance records
"""

from pathlib import Path
from jinja2 import Template
from weasyprint import HTML
from datetime import datetime


WAFT_TOWN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        /* WAFT Town Court Document Template */

        @page {
            size: letter;
            margin: 0.6in 0.5in;
            background: #fff;

            @top-left {
                content: "{{ doc_id }}";
                font-family: 'Courier New', monospace;
                font-size: 8pt;
                color: #666;
            }

            @top-right {
                content: "Page " counter(page);
                font-family: 'Courier New', monospace;
                font-size: 8pt;
            }

            @bottom-center {
                content: "WAFT TOWN COURT DOCUMENT";
                font-family: 'Courier New', monospace;
                font-size: 7pt;
                color: #006;
                font-weight: bold;
            }
        }

        @page :first {
            @top-left { content: none; }
            @top-right { content: none; }
        }

        body {
            font-family: 'Times New Roman', 'Times', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #000;
            background: #fff;
        }

        /* Official Court Header */
        .court-header {
            border: 4px double #000;
            padding: 0.3in;
            margin-bottom: 0.3in;
            background: #fff;
            text-align: center;
        }

        .court-seal {
            font-size: 24pt;
            margin-bottom: 0.1in;
        }

        .court-title {
            font-family: 'Times New Roman', serif;
            font-size: 20pt;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 2pt;
            margin-bottom: 0.15in;
            border-bottom: 2px solid #000;
            padding-bottom: 0.1in;
        }

        .court-subtitle {
            font-size: 14pt;
            font-weight: bold;
            margin-top: 0.1in;
            margin-bottom: 0.1in;
        }

        .doc-id {
            font-family: 'Courier New', monospace;
            font-size: 10pt;
            font-weight: bold;
            margin-top: 0.15in;
            text-transform: uppercase;
        }

        .court-date {
            font-size: 11pt;
            margin-top: 0.1in;
            font-style: italic;
        }

        /* Council Section */
        .council-section {
            border: 2px solid #000;
            padding: 0.2in;
            margin: 0.2in 0;
            background: #f9f9f9;
            page-break-inside: avoid;
        }

        .council-title {
            font-weight: bold;
            font-size: 12pt;
            text-transform: uppercase;
            border-bottom: 1px solid #000;
            padding-bottom: 0.05in;
            margin-bottom: 0.1in;
        }

        .council-member {
            margin: 0.08in 0;
            padding-left: 0.2in;
            font-size: 10pt;
        }

        .council-role {
            font-weight: bold;
            display: inline-block;
            width: 1.5in;
        }

        /* Voting Section */
        .voting-section {
            border: 2px solid #006;
            background: #f0f0ff;
            padding: 0.2in;
            margin: 0.2in 0;
            page-break-inside: avoid;
        }

        .voting-title {
            font-weight: bold;
            font-size: 12pt;
            color: #006;
            text-transform: uppercase;
            margin-bottom: 0.1in;
        }

        .vote-tally {
            margin: 0.1in 0;
            padding: 0.1in;
            background: #fff;
            border: 1px solid #006;
        }

        .vote-item {
            margin: 0.05in 0;
            font-size: 10pt;
        }

        .vote-label {
            font-weight: bold;
            display: inline-block;
            width: 1in;
        }

        .vote-result {
            font-weight: bold;
            color: #006;
        }

        /* Proceedings Section */
        .proceedings-section {
            margin: 0.2in 0;
        }

        .proceeding-entry {
            margin: 0.15in 0;
            padding: 0.1in;
            border-left: 3px solid #000;
            padding-left: 0.15in;
        }

        .proceeding-time {
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            color: #666;
            font-weight: bold;
        }

        .proceeding-text {
            margin-top: 0.05in;
        }

        /* Signature Block */
        .signature-block {
            margin-top: 0.4in;
            margin-bottom: 0.3in;
            page-break-inside: avoid;
        }

        .signature-line {
            margin-top: 0.3in;
            border-top: 2px solid #000;
            width: 3.5in;
            padding-top: 0.1in;
            font-size: 10pt;
        }

        .signature-role {
            font-weight: bold;
            text-transform: uppercase;
            font-size: 9pt;
            margin-bottom: 0.05in;
        }

        .signature-name {
            font-weight: bold;
            font-size: 11pt;
        }

        .signature-date {
            font-size: 9pt;
            color: #666;
            margin-top: 0.05in;
        }

        /* Section Headers */
        h2 {
            font-family: 'Times New Roman', serif;
            font-size: 14pt;
            font-weight: bold;
            text-transform: uppercase;
            color: #000;
            border-bottom: 3px solid #000;
            padding-bottom: 0.05in;
            margin-top: 0.3in;
            margin-bottom: 0.15in;
            page-break-after: avoid;
            letter-spacing: 1pt;
        }

        h3 {
            font-size: 12pt;
            font-weight: bold;
            border-bottom: 2px solid #000;
            padding-bottom: 0.05in;
            margin-top: 0.2in;
            margin-bottom: 0.12in;
            page-break-after: avoid;
        }

        h4 {
            font-size: 11pt;
            font-weight: bold;
            font-style: italic;
            margin-top: 0.15in;
            margin-bottom: 0.1in;
        }

        /* Legal Text */
        .legal-text {
            text-align: justify;
            margin: 0.1in 0;
            font-size: 10.5pt;
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.15in 0;
            font-size: 10pt;
        }

        th {
            background: #000;
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
            margin-bottom: 0.15in;
        }

        li {
            margin-bottom: 0.08in;
        }

        /* Paragraphs */
        p {
            margin: 0.1in 0;
            text-align: justify;
        }

        /* Footer Notice */
        .footer-notice {
            margin-top: 0.4in;
            padding-top: 0.15in;
            border-top: 2px solid #000;
            font-size: 8pt;
            color: #666;
            text-align: center;
            font-style: italic;
        }

        /* Emphasis */
        strong {
            font-weight: bold;
        }

        em {
            font-style: italic;
        }

        .official-seal {
            text-align: center;
            font-size: 16pt;
            margin: 0.2in 0;
            border: 2px solid #000;
            padding: 0.15in;
            background: #fff;
        }
    </style>
</head>
<body>
    <!-- Official Court Header -->
    <div class="court-header">
        <div class="court-seal">⚖️</div>
        <div class="court-title">WAFT Town Court</div>
        <div class="court-subtitle">TheCouncil</div>
        <div class="doc-id">{{ doc_id }}</div>
        <div class="court-date">{{ date }}</div>
    </div>

    <!-- Main Content -->
    <div class="content">
        {{ content | safe }}
    </div>

    <!-- Footer Notice -->
    {% if footer_notice %}
    <div class="footer-notice">
        {{ footer_notice }}
    </div>
    {% else %}
    <div class="footer-notice">
        This is an official WAFT Town Court document. All proceedings are recorded and archived.
    </div>
    {% endif %}
</body>
</html>
"""


def generate_waft_town_document(
    title: str,
    content: str,
    output_path: Path,
    doc_id: str = "COURT-001",
    date: str = None,
    footer_notice: str = None
) -> Path:
    """
    Generate a WAFT Town court document.

    Args:
        title: Document title
        content: Main content (HTML with special block classes)
        output_path: Where to save PDF
        doc_id: Document ID (e.g., "COURT-001", "RESOLUTION-2026-01")
        date: Document date (defaults to current date)
        footer_notice: Custom footer notice

    Returns:
        Path to generated PDF
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if date is None:
        date = datetime.now().strftime("%B %d, %Y")

    template = Template(WAFT_TOWN_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        doc_id=doc_id,
        date=date,
        footer_notice=footer_notice
    )

    HTML(string=html_output).write_pdf(output_path)
    
    # Post-process to add blank page markers
    try:
        from ..utils import process_pdf_for_blank_pages
        process_pdf_for_blank_pages(output_path)
    except Exception as e:
        print(f"⚠️  Blank page marker processing failed: {e}")
    
    return output_path
