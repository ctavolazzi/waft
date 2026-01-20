"""
Poetry/Video Essay Template
============================

Ornate, artistic template for spoken word performances and video essay transcripts.
More decorative and visually interesting than the guide template.
"""

from pathlib import Path

from jinja2 import Template
from weasyprint import HTML

POETRY_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        /* Poetry/Video Essay Template - Ornate, artistic design */

        @page {
            size: letter;
            margin: 1in 0.75in;

            @top-center {
                content: "{{ title }}";
                font-family: 'Georgia', serif;
                font-size: 10pt;
                font-style: italic;
                color: #666;
            }

            @bottom-center {
                content: "Page " counter(page);
                font-family: 'Georgia', serif;
                font-size: 9pt;
                color: #999;
            }
        }

        @page :first {
            @top-center { content: none; }
            @bottom-center { content: none; }
        }

        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 12pt;
            line-height: 1.8;
            color: #2c2c2c;
            background: #fafafa;
        }

        /* Title Page */
        .title-page {
            text-align: center;
            padding: 2in 0.5in;
            page-break-after: always;
        }

        .title-main {
            font-size: 36pt;
            font-weight: normal;
            font-style: italic;
            margin-bottom: 0.3in;
            color: #1a1a1a;
            letter-spacing: 2pt;
        }

        .title-subtitle {
            font-size: 16pt;
            font-style: italic;
            color: #666;
            margin-bottom: 0.5in;
        }

        .title-author {
            font-size: 14pt;
            margin-top: 1in;
            color: #444;
        }

        .title-date {
            font-size: 11pt;
            color: #888;
            margin-top: 0.2in;
        }

        /* Poem Stanzas */
        .stanza {
            margin: 0.4in 0;
            padding: 0.2in;
            text-align: center;
        }

        .stanza p {
            margin: 0.15in 0;
            line-height: 2;
        }

        /* Video Essay Sections */
        .essay-section {
            margin: 0.5in 0;
        }

        .essay-section h2 {
            font-size: 16pt;
            font-weight: normal;
            font-style: italic;
            text-align: center;
            margin-bottom: 0.3in;
            color: #444;
            border-bottom: 1px solid #ddd;
            padding-bottom: 0.1in;
        }

        .essay-section p {
            text-align: justify;
            text-indent: 0.3in;
            margin-bottom: 0.2in;
        }

        /* Performance Notes */
        .performance-notes {
            border: 2px dashed #999;
            padding: 0.2in;
            margin: 0.3in 0;
            background: #f9f9f9;
            font-size: 10pt;
            font-style: italic;
            color: #666;
        }

        .performance-notes-title {
            font-weight: bold;
            margin-bottom: 0.1in;
            color: #444;
        }

        /* Decorative Elements */
        .divider {
            text-align: center;
            margin: 0.4in 0;
            color: #999;
            font-size: 14pt;
        }

        .divider::before {
            content: "❋ ❋ ❋";
        }

        /* Emphasis */
        em {
            font-style: italic;
        }

        strong {
            font-weight: bold;
        }

        /* Page breaks */
        .page-break {
            page-break-before: always;
        }

        /* Visual Elements */
        .decorative-border {
            border: 3px double #333;
            padding: 0.3in;
            margin: 0.3in 0;
        }
    </style>
</head>
<body>
    <!-- Title Page -->
    <div class="title-page">
        <div class="title-main">{{ title }}</div>
        {% if subtitle %}
        <div class="title-subtitle">{{ subtitle }}</div>
        {% endif %}
        {% if author %}
        <div class="title-author">{{ author }}</div>
        {% endif %}
        {% if date %}
        <div class="title-date">{{ date }}</div>
        {% endif %}
    </div>

    <!-- Content -->
    <div class="content">
        {{ content | safe }}
    </div>

    <!-- Performance Notes -->
    {% if performance_notes %}
    <div class="performance-notes">
        <div class="performance-notes-title">Performance Notes</div>
        {{ performance_notes | safe }}
    </div>
    {% endif %}
</body>
</html>
"""


def generate_poetry(
    title: str,
    content: str,
    output_path: Path,
    subtitle: str | None = None,
    author: str | None = None,
    date: str | None = None,
    performance_notes: str | None = None,
) -> Path:
    """
    Generate a poetry/video essay PDF document.

    Args:
        title: Document title
        content: Main content (HTML with stanzas or essay sections)
        output_path: Where to save PDF
        subtitle: Optional subtitle
        author: Author name
        date: Optional date
        performance_notes: Optional performance notes (HTML)

    Returns:
        Path to generated PDF
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(POETRY_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        subtitle=subtitle,
        author=author,
        date=date,
        performance_notes=performance_notes,
    )

    HTML(string=html_output).write_pdf(output_path)
    return output_path
