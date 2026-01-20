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
            margin: 0.75in 0.6in;
            background: #fafafa;

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
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #1a1a1a;
            background: #fafafa;
        }

        /* Cover Page - Enhanced Design */
        .cover-page {
            border: 4px double #1a1a1a;
            padding: 0.6in;
            margin-bottom: 0.3in;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            text-align: center;
            page-break-after: always;
            position: relative;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        .cover-header {
            font-family: 'Helvetica Neue', 'Arial', sans-serif;
            font-size: 14pt;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 0.4in;
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 0.12in;
            color: #2c3e50;
        }

        .cover-title {
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 28pt;
            font-weight: bold;
            line-height: 1.3;
            margin-bottom: 0.25in;
            margin-top: 0.15in;
            word-wrap: break-word;
            overflow-wrap: break-word;
            hyphens: auto;
            max-width: 100%;
            padding: 0.08in 0;
            color: #1a1a1a;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        }

        .cover-subtitle {
            font-size: 13pt;
            font-style: italic;
            color: #5a6c7d;
            margin-bottom: 0.35in;
            font-weight: 300;
        }

        .cover-doc-id {
            font-family: 'Courier New', monospace;
            font-size: 12pt;
            font-weight: bold;
            margin-bottom: 0.2in;
            text-transform: uppercase;
        }

        /* KeyValue Block (Cover) - Enhanced */
        .keyvalue-block {
            border: 2px solid #2c3e50;
            border-radius: 4px;
            padding: 0.25in;
            margin: 0.25in auto;
            background: linear-gradient(to bottom, #ffffff 0%, #f8f9fa 100%);
            text-align: left;
            max-width: 4.5in;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }

        .keyvalue-item {
            margin-bottom: 0.1in;
            font-size: 9.5pt;
        }

        .keyvalue-key {
            font-weight: 600;
            display: inline-block;
            width: 1.8in;
            text-transform: uppercase;
            color: #2c3e50;
            font-size: 9pt;
            letter-spacing: 0.05em;
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

        /* Corner Badge (Cover) */
        .corner-badge {
            position: absolute;
            top: 0.2in;
            right: 0.2in;
            background: #000;
            color: #fff;
            padding: 0.15in 0.25in;
            font-family: 'Courier New', monospace;
            font-size: 8pt;
            font-weight: bold;
            text-transform: uppercase;
            border: 2px solid #000;
            transform: rotate(0deg);
            box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .corner-badge::before {
            content: "";
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            border: 1px solid #fff;
            z-index: -1;
        }

        /* Content Pages - Enhanced */
        .content-page {
            margin-top: 0.2in;
            background: #ffffff;
            padding: 0.15in;
            border-radius: 2px;
        }

        /* Section Dividers */
        .section-divider {
            page-break-before: always;
            text-align: center;
            padding: 1.5in 0;
            background: linear-gradient(to bottom, #f8f9fa 0%, #fff 100%);
            border-top: 4px solid #000;
            border-bottom: 4px solid #000;
            margin: 0 -0.5in;
            padding-left: 0.5in;
            padding-right: 0.5in;
        }

        .section-title {
            font-family: 'Arial Black', sans-serif;
            font-size: 36pt;
            font-weight: bold;
            text-transform: uppercase;
            color: #000;
            margin-bottom: 0.2in;
            letter-spacing: 0.05in;
        }

        .section-subtitle {
            font-family: 'Georgia', serif;
            font-size: 14pt;
            font-style: italic;
            color: #666;
            margin-top: 0.1in;
        }

        /* Section Headers - Enhanced Typography */
        h2 {
            font-family: 'Helvetica Neue', 'Arial', sans-serif;
            font-size: 16pt;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.08in;
            margin-top: 0.4in;
            margin-bottom: 0.2in;
            page-break-after: avoid;
            background: linear-gradient(to right, rgba(52, 152, 219, 0.1), transparent);
            padding-left: 0.1in;
            padding-right: 0.1in;
        }

        h3 {
            font-size: 13pt;
            font-weight: 600;
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 0.06in;
            margin-top: 0.25in;
            margin-bottom: 0.15in;
            page-break-after: avoid;
            color: #34495e;
        }

        h4 {
            font-size: 11pt;
            font-weight: bold;
            font-style: italic;
            margin-top: 0.15in;
            margin-bottom: 0.1in;
        }

        /* Status Box - Enhanced Design */
        .status-box {
            border: 2px solid #3498db;
            border-radius: 6px;
            padding: 0.2in;
            margin: 0.2in 0;
            background: linear-gradient(to bottom, #ebf5fb 0%, #ffffff 100%);
            page-break-inside: avoid;
            box-shadow: 0 2px 6px rgba(52, 152, 219, 0.15);
        }

        .status-title {
            font-weight: 600;
            font-size: 10pt;
            margin-bottom: 0.1in;
            text-transform: uppercase;
            color: #2980b9;
            letter-spacing: 0.05em;
        }

        /* Tables - Enhanced Design */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.2in 0;
            font-size: 10pt;
            border-radius: 4px;
            overflow: hidden;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
        }

        th {
            background: linear-gradient(to bottom, #34495e 0%, #2c3e50 100%);
            color: #fff;
            border: 1px solid #1a1a1a;
            padding: 0.1in 0.12in;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 9pt;
            letter-spacing: 0.05em;
        }

        td {
            border: 1px solid #e0e0e0;
            padding: 0.1in 0.12in;
            background: #fff;
        }

        tr:nth-child(even) td {
            background: #f8f9fa;
        }

        tr:hover td {
            background: #ecf0f1;
        }

        /* Lists - Enhanced Design */
        ul, ol {
            margin-left: 0.35in;
            margin-bottom: 0.15in;
            padding-left: 0.1in;
        }

        li {
            margin-bottom: 0.08in;
            line-height: 1.6;
        }

        ul li::marker {
            color: #3498db;
        }

        ol li::marker {
            color: #2c3e50;
            font-weight: 600;
        }

        /* Paragraphs - Enhanced Typography */
        p {
            margin: 0.12in 0;
            text-align: justify;
            text-indent: 0;
            orphans: 2;
            widows: 2;
        }

        p:first-of-type {
            margin-top: 0;
        }

        /* Code Blocks - Enhanced Design */
        pre {
            background: linear-gradient(to bottom, #2c3e50 0%, #34495e 100%);
            border: 1px solid #1a1a1a;
            border-left: 5px solid #3498db;
            border-radius: 4px;
            padding: 0.18in;
            margin: 0.2in 0;
            overflow-x: auto;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 9pt;
            line-height: 1.5;
            page-break-inside: avoid;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            color: #ecf0f1;
        }

        code {
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 9.5pt;
            background: #f1f3f5;
            padding: 0.03in 0.06in;
            border-radius: 3px;
            color: #e74c3c;
            border: 1px solid #dee2e6;
        }

        pre code {
            background: transparent;
            padding: 0;
            border-radius: 0;
            display: block;
            color: #ecf0f1;
            border: none;
        }

        /* Code highlighting (basic) */
        .highlight {
            background: #f5f5f5;
        }

        .highlight .k { color: #0000ff; } /* Keywords */
        .highlight .s { color: #008000; } /* Strings */
        .highlight .c { color: #808080; font-style: italic; } /* Comments */
        .highlight .n { color: #000000; } /* Names */
        .highlight .o { color: #000000; } /* Operators */
        .highlight .p { color: #000000; } /* Punctuation */

        /* Note Box - Enhanced Design */
        .note {
            border-left: 5px solid #3498db;
            background: linear-gradient(to right, #ebf5fb 0%, #ffffff 100%);
            padding: 0.15in 0.2in;
            margin: 0.2in 0;
            border-radius: 0 4px 4px 0;
            box-shadow: 0 2px 6px rgba(52, 152, 219, 0.12);
        }

        .note-title {
            font-weight: 600;
            color: #2980b9;
            text-transform: uppercase;
            font-size: 9pt;
            margin-bottom: 0.08in;
            letter-spacing: 0.05em;
        }

        /* Emphasis - Enhanced */
        strong {
            font-weight: 600;
            color: #2c3e50;
        }

        em {
            font-style: italic;
            color: #5a6c7d;
        }

        strong em, em strong {
            font-weight: 600;
            font-style: italic;
            color: #34495e;
        }
    </style>
</head>
<body>
    <!-- Cover Page -->
    <div class="cover-page">
        {% if cover_badge %}
        <div class="corner-badge">{{ cover_badge }}</div>
        {% endif %}

        {% if cover_header %}
        <div class="cover-header">{{ cover_header | e }}</div>
        {% endif %}

        <div class="cover-title">{{ title | e }}</div>

        {% if subtitle %}
        <div class="cover-subtitle">{{ subtitle | e }}</div>
        {% endif %}

        <div class="cover-doc-id">{{ doc_id | e }}</div>

        {% if cover_metadata %}
        <div class="keyvalue-block">
            {% for key, value in cover_metadata.items() %}
            <div class="keyvalue-item">
                <span class="keyvalue-key">{{ key | e }}:</span>
                <span class="keyvalue-value">{{ value | e }}</span>
            </div>
            {% endfor %}
        </div>
        {% endif %}

        {% if cover_warning %}
        <div class="warning-block {{ cover_warning.severity|lower }}">
            <div class="warning-title">{{ cover_warning.severity | e }}</div>
            <p>{{ cover_warning.message | e }}</p>
        </div>
        {% endif %}

        {% if cover_signature %}
        <div class="signature-block">
            <div class="signature-line">
                <div class="signature-role">{{ cover_signature.role | e }}</div>
                <div class="signature-name">{{ cover_signature.name | e }}</div>
                {% if cover_signature.date %}
                <div class="signature-date">{{ cover_signature.date | e }}</div>
                {% endif %}
            </div>
        </div>
        {% endif %}

        {% if cover_footer %}
        <div class="cover-footer">
            {{ cover_footer | e }}
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
    cover_footer: str = None,
    cover_badge: str = None,
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
        cover_badge: Optional corner badge text (e.g., "V1.0", "DRAFT", "CONFIDENTIAL")

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
        cover_footer=cover_footer,
        cover_badge=cover_badge,
    )

    HTML(string=html_output).write_pdf(output_path)

    # Post-process to add blank page markers
    try:
        from ..utils import process_pdf_for_blank_pages

        process_pdf_for_blank_pages(output_path)
    except Exception as e:
        # If blank page handling fails, continue anyway (non-critical)
        print(f"⚠️  Blank page marker processing failed: {e}")

    return output_path
