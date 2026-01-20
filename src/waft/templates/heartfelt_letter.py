"""
Heartfelt Letter Template
==========================

Sweet, personal, intimate letter format.
Tests warmth, gentle aesthetics, handwritten feel.

Features:
- Soft, warm colors
- Handwritten-style fonts
- Decorative borders
- Personal, intimate spacing
- Optional letterhead/stationery
- Emphasis on emotion and connection
"""

from pathlib import Path

from jinja2 import Template
from weasyprint import HTML

HEARTFELT_LETTER_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        @page {
            size: letter;
            margin: 1in;
            background: {{ background_color }};

            {% if show_border %}
            /* Decorative border */
            border: 2px solid {{ border_color }};
            border-radius: 5px;
            padding: 0.3in;
            {% endif %}
        }

        body {
            font-family: 'Georgia', 'Garamond', serif;
            font-size: 12pt;
            line-height: 1.8;
            color: {{ text_color }};
        }

        /* Decorative header */
        .letter-header {
            text-align: center;
            margin-bottom: 0.5in;
            padding-bottom: 0.2in;
            border-bottom: 1px solid {{ border_color }};
        }

        .letter-ornament {
            font-size: 24pt;
            color: {{ ornament_color }};
            margin-bottom: 0.1in;
        }

        .letter-from {
            font-size: 11pt;
            color: #666;
            font-style: italic;
        }

        /* Date */
        .date {
            text-align: right;
            font-style: italic;
            color: #666;
            margin-bottom: 0.3in;
        }

        /* Salutation */
        .salutation {
            font-size: 13pt;
            margin-bottom: 0.2in;
        }

        /* Body */
        .letter-body p {
            margin-bottom: 0.2in;
            text-indent: 0.3in;
            text-align: left;
        }

        .letter-body p:first-child {
            text-indent: 0;
        }

        /* Special elements */
        .handwritten {
            font-family: 'Bradley Hand', 'Brush Script MT', cursive;
            font-size: 14pt;
            color: {{ handwritten_color }};
            line-height: 2;
        }

        .heart {
            color: #e91e63;
            font-size: 14pt;
        }

        .emphasized {
            font-style: italic;
            color: {{ emphasis_color }};
        }

        .underline {
            text-decoration: underline;
            text-decoration-color: {{ emphasis_color }};
            text-decoration-style: wavy;
        }

        /* Quote/Memory box */
        .memory-box {
            background: {{ memory_box_bg }};
            border-left: 4px solid {{ border_color }};
            padding: 0.2in;
            margin: 0.2in 0;
            font-style: italic;
        }

        /* Closing */
        .closing {
            margin-top: 0.4in;
            text-align: left;
        }

        .closing-phrase {
            margin-bottom: 0.5in;
        }

        .signature {
            font-family: 'Bradley Hand', 'Brush Script MT', cursive;
            font-size: 16pt;
            color: {{ handwritten_color }};
        }

        /* PS */
        .ps {
            margin-top: 0.3in;
            font-style: italic;
            color: #666;
        }

        .ps::before {
            content: "P.S. ";
            font-weight: bold;
            color: #000;
        }

        /* Doodles/Decorations */
        .doodle {
            text-align: center;
            font-size: 18pt;
            color: {{ ornament_color }};
            margin: 0.2in 0;
        }

        /* Emphasis */
        strong {
            font-weight: bold;
            color: {{ emphasis_color }};
        }

        em {
            font-style: italic;
        }

        /* Lists */
        ul {
            list-style: none;
            padding-left: 0.3in;
        }

        ul li::before {
            content: "{{ list_bullet }} ";
            color: {{ ornament_color }};
        }
    </style>
</head>
<body>
    {% if show_header %}
    <div class="letter-header">
        <div class="letter-ornament">{{ ornament }}</div>
        {% if from_name %}<div class="letter-from">From: {{ from_name }}</div>{% endif %}
    </div>
    {% endif %}

    {% if date %}
    <div class="date">{{ date }}</div>
    {% endif %}

    {% if salutation %}
    <div class="salutation">{{ salutation }}</div>
    {% endif %}

    <div class="letter-body">
        {{ content | safe }}
    </div>

    {% if closing %}
    <div class="closing">
        <div class="closing-phrase">{{ closing }}</div>
        {% if signature %}
        <div class="signature">{{ signature }}</div>
        {% endif %}
    </div>
    {% endif %}
</body>
</html>
"""


def generate_heartfelt_letter(
    content: str,
    output_path: Path,
    title: str = "A Letter",
    from_name: str = None,
    date: str = None,
    salutation: str = None,
    closing: str = "With all my love,",
    signature: str = None,
    show_header: bool = True,
    show_border: bool = False,
    ornament: str = "✿ ❀ ✿",
    background_color: str = "#fffef8",
    border_color: str = "#d4af37",
    text_color: str = "#2c2c2c",
    ornament_color: str = "#d4af37",
    handwritten_color: str = "#1a5490",
    emphasis_color: str = "#8b4513",
    memory_box_bg: str = "#fff9e6",
    list_bullet: str = "❀",
) -> Path:
    """
    Generate a heartfelt personal letter.

    Args:
        content: Letter content (HTML)
        output_path: Where to save PDF
        title: Document title
        from_name: Sender name
        date: Date
        salutation: Opening (e.g., "My dearest...")
        closing: Closing phrase
        signature: Signature
        show_header: Show decorative header
        show_border: Show decorative page border
        ornament: Decorative symbols
        background_color: Page background
        border_color: Border/accent color
        text_color: Main text color
        ornament_color: Decorative element color
        handwritten_color: Handwritten text color
        emphasis_color: Emphasized text color
        memory_box_bg: Memory box background
        list_bullet: Bullet character for lists

    Returns:
        Path to generated PDF
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(HEARTFELT_LETTER_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        from_name=from_name,
        date=date,
        salutation=salutation,
        closing=closing,
        signature=signature,
        show_header=show_header,
        show_border=show_border,
        ornament=ornament,
        background_color=background_color,
        border_color=border_color,
        text_color=text_color,
        ornament_color=ornament_color,
        handwritten_color=handwritten_color,
        emphasis_color=emphasis_color,
        memory_box_bg=memory_box_bg,
        list_bullet=list_bullet,
    )

    HTML(string=html_output).write_pdf(output_path)
    return output_path
