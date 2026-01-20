"""
Screenplay Template
===================

Professional screenplay/script format following industry standards.

Features:
- Scene headers (INT./EXT.)
- Character names (centered, uppercase)
- Dialogue with proper indentation
- Parentheticals (character direction)
- Action/description blocks
- Transitions (CUT TO:, FADE IN:, etc.)
- Proper page breaks
- Industry-standard Courier 12pt
"""

from pathlib import Path

from jinja2 import Template
from weasyprint import HTML

SCREENPLAY_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        /* Screenplay formatting follows strict industry standards */

        @page {
            size: letter;
            margin: 1in 1in 1in 1.5in;  /* Industry standard margins */

            @top-right {
                content: counter(page) ".";
                font-family: 'Courier New', monospace;
                font-size: 12pt;
                padding-right: 0.5in;
            }
        }

        @page :first {
            @top-right {
                content: none;
            }
        }

        body {
            font-family: 'Courier New', 'Courier', monospace;
            font-size: 12pt;
            line-height: 1;  /* Single-spaced */
            color: #000;
        }

        /* Title Page */
        .title-page {
            text-align: center;
            margin-top: 2.5in;
            page-break-after: always;
        }

        .script-title {
            font-size: 14pt;
            font-weight: bold;
            text-transform: uppercase;
            margin-bottom: 0.5in;
        }

        .script-subtitle {
            font-size: 12pt;
            margin-bottom: 1in;
        }

        .script-author {
            margin-top: 1in;
            font-size: 12pt;
        }

        .script-author-by {
            margin-bottom: 0.1in;
        }

        .script-contact {
            position: absolute;
            bottom: 1in;
            left: 1.5in;
            text-align: left;
            font-size: 10pt;
        }

        /* Scene Headers (Sluglines) */
        .scene-header {
            font-weight: bold;
            text-transform: uppercase;
            margin-top: 2em;
            margin-bottom: 1em;
            page-break-after: avoid;
        }

        /* Action/Description */
        .action {
            margin-bottom: 1em;
            width: 100%;
        }

        /* Character Name */
        .character {
            margin-left: 2.2in;
            margin-top: 1em;
            margin-bottom: 0;
            text-transform: uppercase;
            font-weight: normal;
            page-break-after: avoid;
        }

        /* Parenthetical (character direction) */
        .parenthetical {
            margin-left: 1.8in;
            margin-right: 2.1in;
            margin-bottom: 0;
        }

        /* Dialogue */
        .dialogue {
            margin-left: 1.4in;
            margin-right: 2in;
            margin-bottom: 1em;
        }

        /* Transition */
        .transition {
            text-align: right;
            margin-top: 1em;
            margin-bottom: 1em;
            text-transform: uppercase;
            font-weight: normal;
        }

        /* Dual Dialogue (two characters speaking simultaneously) */
        .dual-dialogue {
            display: flex;
            justify-content: space-between;
        }

        .dual-dialogue .character,
        .dual-dialogue .dialogue {
            width: 45%;
        }

        /* Shot */
        .shot {
            text-transform: uppercase;
            margin-bottom: 1em;
        }

        /* Page breaks */
        .page-break {
            page-break-before: always;
        }

        /* Continued */
        .continued {
            text-align: right;
            margin-bottom: 1em;
        }

        /* Montage/Series of Shots */
        .montage {
            margin-left: 1in;
            margin-bottom: 1em;
        }

        .montage-item {
            margin-bottom: 0.5em;
        }

        /* The End */
        .the-end {
            text-align: center;
            margin-top: 2em;
            font-weight: bold;
        }

        /* NO EXTRA SPACING - screenplay is very precise */
        p {
            margin: 0;
        }
    </style>
</head>
<body>
    <!-- Title Page -->
    <div class="title-page">
        <div class="script-title">{{ title }}</div>
        {% if subtitle %}<div class="script-subtitle">{{ subtitle }}</div>{% endif %}
        <div class="script-author">
            <div class="script-author-by">Written by</div>
            <div>{{ author }}</div>
        </div>
        {% if draft %}<div style="margin-top: 0.5in;">{{ draft }}</div>{% endif %}

        {% if contact %}
        <div class="script-contact">
            {{ contact | safe }}
        </div>
        {% endif %}
    </div>

    <!-- Script Content -->
    <div class="script-content">
        {{ content | safe }}
    </div>
</body>
</html>
"""


def generate_screenplay(
    title: str,
    content: str,
    output_path: Path,
    author: str = "Anonymous",
    subtitle: str = None,
    draft: str = None,
    contact: str = None,
) -> Path:
    """
    Generate a professional screenplay.

    Args:
        title: Script title
        content: Script content (HTML with proper screenplay classes)
        output_path: Where to save PDF
        author: Writer name
        subtitle: Subtitle (e.g., "A Short Film")
        draft: Draft info (e.g., "First Draft", "Shooting Script")
        contact: Contact information (HTML)

    Returns:
        Path to generated PDF

    Content should use these classes:
        .scene-header - INT./EXT. scene headers
        .action - Action/description
        .character - Character name (centered, uppercase)
        .parenthetical - (character direction)
        .dialogue - Character dialogue
        .transition - CUT TO:, FADE OUT:, etc.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(SCREENPLAY_TEMPLATE)
    html_output = template.render(
        title=title, content=content, author=author, subtitle=subtitle, draft=draft, contact=contact
    )

    HTML(string=html_output).write_pdf(output_path)
    return output_path
