"""
Celebration Card Template
=========================

Beautiful one-page celebration card with creative design.
Perfect for acknowledging achievements, milestones, and moments of joy.

Features:
- Single-page design optimized for printing
- Creative, festive layout
- Large, celebratory typography
- Decorative elements
- Page numbers (optional)
- Print-ready formatting
"""

from pathlib import Path

from jinja2 import Template
from weasyprint import HTML

CELEBRATION_CARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        @page {
            size: letter;
            margin: 0.5in;
            {% if page_numbers %}
            @bottom-center {
                content: counter(page);
                font-size: 10pt;
                font-family: 'Georgia', serif;
                color: #666;
            }
            {% endif %}
        }

        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 12pt;
            line-height: 1.6;
            color: #1a1a1a;
            background: #fff;
            margin: 0;
            padding: 0;
        }

        .celebration-card {
            max-width: 7in;
            margin: 0 auto;
            padding: 0.4in;
            border: 3px double #333;
            background: linear-gradient(to bottom, #fffef0 0%, #ffffff 100%);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        /* Decorative header */
        .celebration-header {
            text-align: center;
            margin-bottom: 0.3in;
            padding-bottom: 0.2in;
            border-bottom: 2px solid #d4af37;
        }

        .celebration-emoji {
            font-size: 48pt;
            line-height: 1;
            margin-bottom: 0.1in;
        }

        .celebration-title {
            font-size: 28pt;
            font-weight: bold;
            color: #1a1a1a;
            margin: 0.15in 0;
            line-height: 1.2;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .celebration-subtitle {
            font-size: 14pt;
            color: #666;
            font-style: italic;
            margin-top: 0.1in;
        }

        /* Date stamp */
        .celebration-date {
            text-align: center;
            font-size: 10pt;
            color: #888;
            margin-bottom: 0.3in;
            font-style: italic;
        }

        /* Main content */
        .celebration-content {
            margin: 0.3in 0;
        }

        .achievement-section {
            background: #fff9e6;
            border-left: 4px solid #d4af37;
            padding: 0.2in;
            margin: 0.2in 0;
            border-radius: 4px;
        }

        .achievement-title {
            font-size: 16pt;
            font-weight: bold;
            color: #8b6914;
            margin-bottom: 0.1in;
        }

        .achievement-text {
            font-size: 12pt;
            line-height: 1.6;
            color: #333;
        }

        .message-section {
            background: #f0f8ff;
            border-left: 4px solid #4a90e2;
            padding: 0.2in;
            margin: 0.2in 0;
            border-radius: 4px;
        }

        .message-title {
            font-size: 16pt;
            font-weight: bold;
            color: #2c5aa0;
            margin-bottom: 0.1in;
        }

        .message-text {
            font-size: 12pt;
            line-height: 1.6;
            color: #333;
        }

        /* Gratitude section */
        .gratitude-section {
            background: #f5f5f5;
            border: 2px dashed #999;
            padding: 0.2in;
            margin: 0.3in 0;
            text-align: center;
            border-radius: 4px;
        }

        .gratitude-title {
            font-size: 14pt;
            font-weight: bold;
            color: #555;
            margin-bottom: 0.1in;
        }

        .gratitude-text {
            font-size: 11pt;
            line-height: 1.5;
            color: #444;
            font-style: italic;
        }

        /* Joy section */
        .joy-section {
            text-align: center;
            margin: 0.3in 0;
            padding: 0.2in;
        }

        .joy-emoji {
            font-size: 36pt;
            line-height: 1;
            margin: 0.1in 0;
        }

        .joy-text {
            font-size: 14pt;
            font-weight: bold;
            color: #d4af37;
            margin-top: 0.1in;
        }

        /* Footer */
        .celebration-footer {
            text-align: center;
            margin-top: 0.4in;
            padding-top: 0.2in;
            border-top: 1px solid #ddd;
            font-size: 9pt;
            color: #888;
        }

        /* Lists */
        ul, ol {
            margin: 0.15in 0;
            padding-left: 0.3in;
        }

        li {
            margin-bottom: 0.08in;
        }

        /* Emphasis */
        strong {
            font-weight: bold;
            color: #1a1a1a;
        }

        em {
            font-style: italic;
        }

        /* Decorative separators */
        .separator {
            text-align: center;
            margin: 0.2in 0;
            color: #d4af37;
            font-size: 18pt;
        }
    </style>
</head>
<body>
    <div class="celebration-card">
        <div class="celebration-header">
            <div class="celebration-emoji">🎉</div>
            <div class="celebration-title">{{ title }}</div>
            {% if subtitle %}
            <div class="celebration-subtitle">{{ subtitle }}</div>
            {% endif %}
        </div>

        {% if date %}
        <div class="celebration-date">{{ date }}</div>
        {% endif %}

        <div class="celebration-content">
            {% if achievement %}
            <div class="achievement-section">
                <div class="achievement-title">✨ What We Accomplished ✨</div>
                <div class="achievement-text">{{ achievement }}</div>
            </div>
            {% endif %}

            {% if message %}
            <div class="message-section">
                <div class="message-title">💝 The Message 💝</div>
                <div class="message-text">{{ message }}</div>
            </div>
            {% endif %}

            {{ content | safe }}

            {% if gratitude %}
            <div class="gratitude-section">
                <div class="gratitude-title">🙏 Gratitude 🙏</div>
                <div class="gratitude-text">{{ gratitude }}</div>
            </div>
            {% endif %}

            <div class="joy-section">
                <div class="joy-emoji">🎉🎉🎉</div>
                <div class="joy-text">THIS IS A MOMENT OF JOY!</div>
            </div>
        </div>

        {% if footer %}
        <div class="celebration-footer">
            {{ footer }}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""


def generate_celebration_card(
    title: str,
    content: str = "",
    output_path: Path = None,
    achievement: str = None,
    message: str = None,
    subtitle: str = None,
    date: str = None,
    gratitude: str = None,
    footer: str = None,
    page_numbers: bool = True,
) -> Path:
    """
    Generate a beautiful one-page celebration card PDF.

    Args:
        title: Celebration title
        content: Additional HTML content (optional)
        output_path: Where to save PDF
        achievement: What was accomplished
        message: Celebration message
        subtitle: Optional subtitle
        date: Date of celebration
        gratitude: Gratitude message
        footer: Footer text
        page_numbers: Whether to include page numbers (default: True)

    Returns:
        Path to generated PDF
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(CELEBRATION_CARD_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        achievement=achievement,
        message=message,
        subtitle=subtitle,
        date=date,
        gratitude=gratitude,
        footer=footer,
        page_numbers=page_numbers,
    )

    HTML(string=html_output).write_pdf(output_path)

    # Post-process to add blank page markers
    try:
        from ..utils import process_pdf_for_blank_pages

        process_pdf_for_blank_pages(output_path)
    except Exception as e:
        print(f"⚠️  Blank page marker processing failed: {e}")

    return output_path
