"""
Minimal Cover Template
======================

Clean, modern minimalist cover page design.
Perfect for contemporary documents, presentations, and reports.

Features:
- Minimalist aesthetic
- Clean typography
- Subtle color accents
- Modern layout
"""

from pathlib import Path

from jinja2 import Template
from weasyprint import HTML

MINIMAL_COVER_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        @page {
            size: letter;
            margin: 0;
            background: #fafafa;
        }

        body {
            font-family: 'Helvetica Neue', 'Arial', sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #1a1a1a;
            background: #fafafa;
            margin: 0;
            padding: 0;
        }

        /* Cover Page */
        .cover-page {
            width: 100%;
            height: 100vh;
            background: linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 2in 1.5in;
            box-sizing: border-box;
            page-break-after: always;
        }

        /* Header Section */
        .cover-header {
            font-size: 10pt;
            font-weight: 300;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: #666;
            margin-bottom: auto;
        }

        /* Title Section */
        .cover-title-section {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: flex-start;
        }

        .cover-title {
            font-size: 48pt;
            font-weight: 300;
            line-height: 1.1;
            color: #1a1a1a;
            margin-bottom: 0.3in;
            letter-spacing: -0.02em;
        }

        .cover-subtitle {
            font-size: 16pt;
            font-weight: 300;
            color: #666;
            margin-top: 0.2in;
        }

        /* Metadata Section */
        .cover-metadata {
            margin-top: 1in;
            padding-top: 0.5in;
            border-top: 1px solid #ddd;
        }

        .metadata-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.2in;
            font-size: 9pt;
            color: #666;
        }

        .metadata-key {
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }

        .metadata-value {
            color: #1a1a1a;
        }

        /* Footer Section */
        .cover-footer {
            margin-top: auto;
            font-size: 8pt;
            color: #999;
            text-align: center;
            padding-top: 0.5in;
            border-top: 1px solid #eee;
        }

        /* Accent Line */
        .accent-line {
            width: 60px;
            height: 2px;
            background: #1a1a1a;
            margin: 0.3in 0;
        }

        /* Badge (if provided) */
        .cover-badge {
            position: absolute;
            top: 1.5in;
            right: 1.5in;
            background: #1a1a1a;
            color: #fff;
            padding: 0.1in 0.2in;
            font-size: 8pt;
            font-weight: 500;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }

        .cover-page {
            position: relative;
        }

        /* Doc ID */
        .cover-doc-id {
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            color: #999;
            margin-top: 0.2in;
            letter-spacing: 0.1em;
        }
    </style>
</head>
<body>
    <!-- Cover Page -->
    <div class="cover-page">
        {% if cover_badge %}
        <div class="cover-badge">{{ cover_badge }}</div>
        {% endif %}

        {% if cover_header %}
        <div class="cover-header">{{ cover_header }}</div>
        {% endif %}

        <div class="cover-title-section">
            <div class="cover-title">{{ title }}</div>
            {% if subtitle %}
            <div class="cover-subtitle">{{ subtitle }}</div>
            {% endif %}
            <div class="accent-line"></div>
            {% if doc_id %}
            <div class="cover-doc-id">{{ doc_id }}</div>
            {% endif %}
        </div>

        {% if cover_metadata %}
        <div class="cover-metadata">
            {% for key, value in cover_metadata.items() %}
            <div class="metadata-item">
                <span class="metadata-key">{{ key }}</span>
                <span class="metadata-value">{{ value }}</span>
            </div>
            {% endfor %}
        </div>
        {% endif %}

        {% if cover_footer %}
        <div class="cover-footer">
            {{ cover_footer }}
        </div>
        {% endif %}
    </div>

    <!-- Content Pages -->
    <div style="padding: 1in; background: #fff;">
        {{ content | safe }}
    </div>
</body>
</html>
"""


def generate_minimal_cover_document(
    title: str,
    content: str,
    output_path: Path,
    doc_id: str = "DOC-001",
    subtitle: str = None,
    cover_header: str = None,
    cover_metadata: dict = None,
    cover_footer: str = None,
    cover_badge: str = None,
) -> Path:
    """
    Generate a document with minimalist cover page.

    Args:
        title: Document title
        content: Main content (HTML)
        output_path: Where to save PDF
        doc_id: Document ID
        subtitle: Optional subtitle
        cover_header: Cover page header
        cover_metadata: Dict of key-value pairs for cover
        cover_footer: Footer text for cover
        cover_badge: Optional corner badge text

    Returns:
        Path to generated PDF
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(MINIMAL_COVER_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        doc_id=doc_id,
        subtitle=subtitle,
        cover_header=cover_header,
        cover_metadata=cover_metadata,
        cover_footer=cover_footer,
        cover_badge=cover_badge,
    )

    HTML(string=html_output).write_pdf(output_path)

    # Post-process to add blank page markers
    try:
        from ..utils import process_pdf_for_blank_pages

        process_pdf_for_blank_pages(output_path)
    except Exception as e:
        print(f"⚠️  Blank page marker processing failed: {e}")

    return output_path
