"""
Worldbuilding Document Template
================================

Combines Foundation/TM document elements with field guide styling for creating
compelling worldbuilding documents (fantasy or factual).

Formatting Elements:
- KeyValueBlock (metadata, parameters)
- WarningBlock (severity levels)
- SignatureBlock (authorization, signatures)
- SectionHeader (hierarchical)
- Classification banners
- Document headers
- Summary boxes
- Footer notices

Perfect for:
- Fantasy worldbuilding (lore, characters, locations)
- Factual documentation (reports, manuals, guides)
- SCP-style documentation
- Corporate reports
- Research papers
"""

from pathlib import Path

from jinja2 import Template
from weasyprint import HTML

WORLDBUILD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        /* Worldbuilding Template - Foundation + Field Guide Hybrid */

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
            font-size: 10pt;
            line-height: 1.5;
            color: #000;
            background: #fff;
        }

        /* Document Header */
        .doc-header {
            border: 3px double #000;
            padding: 0.25in;
            margin-bottom: 0.25in;
            background: #fff;
            text-align: center;
        }

        .doc-id {
            font-family: 'Courier New', monospace;
            font-size: 10pt;
            font-weight: bold;
            margin-bottom: 0.1in;
            text-transform: uppercase;
        }

        .doc-title {
            font-family: 'Arial Black', sans-serif;
            font-size: 18pt;
            font-weight: bold;
            text-transform: uppercase;
            line-height: 1.2;
            margin-bottom: 0.1in;
        }

        .doc-subtitle {
            font-size: 11pt;
            font-style: italic;
            color: #333;
            margin-bottom: 0.1in;
        }

        /* Classification Banner */
        .classification {
            background: #c00;
            color: #fff;
            text-align: center;
            padding: 0.1in;
            font-weight: bold;
            font-size: 11pt;
            margin-bottom: 0.2in;
            text-transform: uppercase;
        }

        /* KeyValue Block */
        .keyvalue-block {
            border: 2px solid #000;
            padding: 0.15in;
            margin: 0.15in 0;
            background: #fff;
            page-break-inside: avoid;
        }

        .keyvalue-label {
            font-weight: bold;
            font-size: 10pt;
            margin-bottom: 0.08in;
            text-transform: uppercase;
            border-bottom: 1px solid #000;
            padding-bottom: 0.03in;
        }

        .keyvalue-item {
            margin-bottom: 0.06in;
            font-size: 9.5pt;
        }

        .keyvalue-key {
            font-weight: bold;
            display: inline-block;
            width: 1.5in;
            text-transform: uppercase;
        }

        .keyvalue-value {
            display: inline;
        }

        /* Warning Block */
        .warning-block {
            border: 3px solid #c00;
            background: #ffe;
            padding: 0.15in;
            margin: 0.15in 0;
            page-break-inside: avoid;
        }

        .warning-block.caution {
            border-color: #f90;
            background: #fff9f0;
        }

        .warning-block.critical {
            border-color: #c00;
            background: #ffe;
        }

        .warning-title {
            font-weight: bold;
            font-size: 10pt;
            color: #c00;
            text-transform: uppercase;
            margin-bottom: 0.08in;
        }

        .warning-block.caution .warning-title {
            color: #f90;
        }

        .warning-title::before {
            content: "⚠ ";
            font-size: 12pt;
        }

        /* Signature Block */
        .signature-block {
            margin-top: 0.3in;
            margin-bottom: 0.2in;
            page-break-inside: avoid;
        }

        .signature-line {
            margin-top: 0.2in;
            border-top: 2px solid #000;
            width: 3in;
            padding-top: 0.08in;
            font-size: 9pt;
        }

        .signature-role {
            font-weight: bold;
            text-transform: uppercase;
            font-size: 8pt;
            margin-bottom: 0.05in;
        }

        .signature-name {
            font-weight: bold;
            font-size: 10pt;
        }

        .signature-date {
            font-size: 8pt;
            color: #666;
            margin-top: 0.03in;
        }

        /* Section Headers */
        h2 {
            font-family: 'Arial Black', sans-serif;
            font-size: 13pt;
            font-weight: bold;
            text-transform: uppercase;
            color: #000;
            border-bottom: 3px solid #000;
            padding-bottom: 0.05in;
            margin-top: 0.25in;
            margin-bottom: 0.12in;
            page-break-after: avoid;
        }

        h3 {
            font-size: 11pt;
            font-weight: bold;
            border-bottom: 2px solid #000;
            padding-bottom: 0.04in;
            margin-top: 0.18in;
            margin-bottom: 0.1in;
            page-break-after: avoid;
        }

        h4 {
            font-size: 10pt;
            font-weight: bold;
            font-style: italic;
            margin-top: 0.12in;
            margin-bottom: 0.08in;
        }

        /* Summary Box */
        .summary-box {
            border: 2px solid #06c;
            background: #f0f8ff;
            padding: 0.15in;
            margin: 0.15in 0;
            page-break-inside: avoid;
        }

        .summary-title {
            font-weight: bold;
            font-size: 11pt;
            color: #06c;
            text-transform: uppercase;
            margin-bottom: 0.08in;
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.12in 0;
            font-size: 9pt;
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
            margin-bottom: 0.05in;
        }

        /* Paragraphs */
        p {
            margin: 0.08in 0;
            text-align: justify;
        }

        /* Log Block */
        .log-block {
            border: 2px solid #000;
            background: #000;
            color: #0f0;
            padding: 0.12in;
            margin: 0.12in 0;
            font-family: 'Courier New', monospace;
            font-size: 8pt;
            page-break-inside: avoid;
        }

        .log-entry {
            margin-bottom: 0.04in;
        }

        /* Footer Notice */
        .footer-notice {
            margin-top: 0.3in;
            padding-top: 0.1in;
            border-top: 1px solid #ccc;
            font-size: 7pt;
            color: #666;
            text-align: center;
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
    </style>
</head>
<body>
    <!-- Document Header -->
    <div class="doc-header">
        <div class="doc-id">{{ doc_id }}</div>
        <div class="doc-title">{{ title }}</div>
        {% if subtitle %}
        <div class="doc-subtitle">{{ subtitle }}</div>
        {% endif %}
        {% if issued_by %}
        <div style="margin-top: 0.1in; font-size: 9pt; color: #666;">
            <strong>Issued by:</strong> {{ issued_by }}<br>
            {% if date %}<strong>Date:</strong> {{ date }}{% endif %}
        </div>
        {% endif %}
    </div>

    <!-- Classification -->
    {% if classification %}
    <div class="classification">{{ classification }}</div>
    {% endif %}

    <!-- Main Content -->
    <div class="content">
        {{ content | safe }}
    </div>

    <!-- Footer Notice -->
    {% if footer_notice %}
    <div class="footer-notice">
        {{ footer_notice }}
    </div>
    {% endif %}
</body>
</html>
"""


def generate_worldbuild_document(
    title: str,
    content: str,
    output_path: Path,
    doc_id: str = "WB-001",
    subtitle: str = None,
    classification: str = "INTERNAL",
    issued_by: str = None,
    date: str = None,
    footer_notice: str = None,
) -> Path:
    """
    Generate a worldbuilding document (Foundation + Field Guide style).

    Args:
        title: Document title
        content: Main content (HTML with special block classes)
        output_path: Where to save PDF
        doc_id: Document ID (e.g., "WB-001", "TM-ARCH-009")
        subtitle: Optional subtitle
        classification: Security classification
        issued_by: Issuing organization
        date: Issue date
        footer_notice: Footer notice text

    Returns:
        Path to generated PDF
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(WORLDBUILD_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        doc_id=doc_id,
        subtitle=subtitle,
        classification=classification,
        issued_by=issued_by,
        date=date,
        footer_notice=footer_notice,
    )

    HTML(string=html_output).write_pdf(output_path)

    # Post-process to add blank page markers
    try:
        from ..utils import process_pdf_for_blank_pages

        process_pdf_for_blank_pages(output_path)
    except Exception as e:
        print(f"⚠️  Blank page marker processing failed: {e}")

    return output_path
