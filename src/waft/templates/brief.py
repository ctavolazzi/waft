"""
Brief Document Template
=======================

Full binder-ready brief document with TM-ARCH-009 style cover page.
Combines Foundation/TM formatting with briefing content.

Perfect for:
- Session briefs
- Project briefs
- Status reports
- Handoff documents
- Binder-ready documentation
"""

from pathlib import Path
from jinja2 import Template
from weasyprint import HTML


BRIEF_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        /* Brief Template - TM-ARCH-009 Style Cover + Content */

        @page {
            size: letter;
            margin: 0.75in 0.5in;
            background: #fff;

            @top-left {
                content: "{{ doc_id }}";
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
            line-height: 1.5;
            color: #000;
            background: #fff;
        }

        /* Cover Page */
        .cover-page {
            border: 4px double #000;
            padding: 0.5in;
            margin-bottom: 0.3in;
            background: #fff;
            text-align: center;
            page-break-after: always;
        }

        .cover-header {
            font-family: 'Arial Black', sans-serif;
            font-size: 16pt;
            font-weight: bold;
            text-transform: uppercase;
            margin-bottom: 0.3in;
            border-bottom: 3px solid #000;
            padding-bottom: 0.15in;
        }

        .cover-title {
            font-family: 'Arial Black', sans-serif;
            font-size: 22pt;
            font-weight: bold;
            text-transform: uppercase;
            line-height: 1.2;
            margin-bottom: 0.2in;
        }

        .cover-subtitle {
            font-size: 12pt;
            font-style: italic;
            color: #333;
            margin-bottom: 0.3in;
        }

        .cover-doc-id {
            font-family: 'Courier New', monospace;
            font-size: 12pt;
            font-weight: bold;
            margin-bottom: 0.2in;
            text-transform: uppercase;
        }

        /* KeyValue Block (Cover) */
        .keyvalue-block {
            border: 2px solid #000;
            padding: 0.2in;
            margin: 0.2in auto;
            background: #fff;
            text-align: left;
            max-width: 4in;
        }

        .keyvalue-item {
            margin-bottom: 0.1in;
            font-size: 9.5pt;
        }

        .keyvalue-key {
            font-weight: bold;
            display: inline-block;
            width: 1.8in;
            text-transform: uppercase;
        }

        .keyvalue-value {
            display: inline;
        }

        /* Warning Block (Cover) */
        .warning-block {
            border: 3px solid #c00;
            background: #ffe;
            padding: 0.2in;
            margin: 0.2in auto;
            max-width: 4.5in;
            text-align: left;
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
            font-size: 11pt;
            color: #c00;
            text-transform: uppercase;
            margin-bottom: 0.1in;
        }

        .warning-block.caution .warning-title {
            color: #f90;
        }

        .warning-title::before {
            content: "⚠ ";
            font-size: 13pt;
        }

        /* Signature Block (Cover) */
        .signature-block {
            margin-top: 0.3in;
            text-align: left;
            max-width: 3in;
            margin-left: auto;
            margin-right: auto;
        }

        .signature-line {
            margin-top: 0.2in;
            border-top: 2px solid #000;
            width: 100%;
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

        .cover-footer {
            margin-top: 0.3in;
            font-size: 9pt;
            color: #666;
        }

        /* Content Pages */
        .content-page {
            margin-top: 0.2in;
        }

        /* Section Headers */
        h2 {
            font-family: 'Arial Black', sans-serif;
            font-size: 14pt;
            font-weight: bold;
            text-transform: uppercase;
            color: #000;
            border-bottom: 3px solid #000;
            padding-bottom: 0.05in;
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

        /* Status Box */
        .status-box {
            border: 2px solid #000;
            padding: 0.15in;
            margin: 0.15in 0;
            background: #fff;
            page-break-inside: avoid;
        }

        .status-title {
            font-weight: bold;
            font-size: 10pt;
            margin-bottom: 0.08in;
            text-transform: uppercase;
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.15in 0;
            font-size: 9.5pt;
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
            margin-bottom: 0.06in;
        }

        /* Paragraphs */
        p {
            margin: 0.1in 0;
            text-align: justify;
        }

        /* Note Box */
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

        /* Emphasis */
        strong {
            font-weight: bold;
        }

        em {
            font-style: italic;
        }
    </style>
</head>
<body>
    <!-- Cover Page -->
    <div class="cover-page">
        {% if cover_header %}
        <div class="cover-header">{{ cover_header }}</div>
        {% endif %}
        
        <div class="cover-title">{{ title }}</div>
        
        {% if subtitle %}
        <div class="cover-subtitle">{{ subtitle }}</div>
        {% endif %}
        
        <div class="cover-doc-id">{{ doc_id }}</div>
        
        {% if cover_metadata %}
        <div class="keyvalue-block">
            {% for key, value in cover_metadata.items() %}
            <div class="keyvalue-item">
                <span class="keyvalue-key">{{ key }}:</span>
                <span class="keyvalue-value">{{ value }}</span>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        {% if cover_warning %}
        <div class="warning-block {{ cover_warning.severity|lower }}">
            <div class="warning-title">{{ cover_warning.severity }}</div>
            <p>{{ cover_warning.message }}</p>
        </div>
        {% endif %}
        
        {% if cover_signature %}
        <div class="signature-block">
            <div class="signature-line">
                <div class="signature-role">{{ cover_signature.role }}</div>
                <div class="signature-name">{{ cover_signature.name }}</div>
                {% if cover_signature.date %}
                <div class="signature-date">{{ cover_signature.date }}</div>
                {% endif %}
            </div>
        </div>
        {% endif %}
        
        {% if cover_footer %}
        <div class="cover-footer">
            {{ cover_footer }}
        </div>
        {% endif %}
    </div>

    <!-- Content Pages -->
    <div class="content-page">
        {{ content | safe }}
    </div>
</body>
</html>
"""


def generate_brief_document(
    title: str,
    content: str,
    output_path: Path,
    doc_id: str = "BRIEF-001",
    subtitle: str = None,
    classification: str = "INTERNAL",
    cover_header: str = None,
    cover_metadata: dict = None,
    cover_warning: dict = None,
    cover_signature: dict = None,
    cover_footer: str = None
) -> Path:
    """
    Generate a full brief document with cover page (TM-ARCH-009 style).

    Args:
        title: Document title
        content: Main content (HTML)
        output_path: Where to save PDF
        doc_id: Document ID (e.g., "BRIEF-001", "TM-ARCH-009")
        subtitle: Optional subtitle
        classification: Security classification
        cover_header: Cover page header (e.g., "TELEPORT MASSIVE")
        cover_metadata: Dict of key-value pairs for cover (e.g., {"OPERATIONAL MANUAL": "09-14"})
        cover_warning: Dict with 'message' and 'severity' for cover warning
        cover_signature: Dict with 'role', 'name', 'date' for cover signature
        cover_footer: Footer text for cover (e.g., "INTERNAL USE ONLY")

    Returns:
        Path to generated PDF
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(BRIEF_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        doc_id=doc_id,
        subtitle=subtitle,
        classification=classification,
        cover_header=cover_header,
        cover_metadata=cover_metadata,
        cover_warning=cover_warning,
        cover_signature=cover_signature,
        cover_footer=cover_footer
    )

    HTML(string=html_output).write_pdf(output_path)
    return output_path
