"""
Children's Storybook Template
==============================

Whimsical storybook for children.
Tests large fonts, colorful design, illustration placeholders.

Features:
- Large, readable fonts
- Colorful, playful design
- Illustration placeholders
- Page-per-spread layout
- Whimsical borders
- Story progression
"""

from pathlib import Path

from jinja2 import Template
from weasyprint import HTML

STORYBOOK_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        @page {
            size: letter landscape;  /* Horizontal for storybook */
            margin: 0.5in;
            background: {{ page_color }};

            {% if show_border %}
            border: 8px solid {{ border_color }};
            border-radius: 15px;
            {% endif %}
        }

        body {
            font-family: 'Comic Sans MS', 'Bradley Hand', cursive;
            font-size: {{ base_font_size }};
            line-height: 1.6;
            color: {{ text_color }};
        }

        /* Title Page */
        .title-page {
            text-align: center;
            padding-top: 1.5in;
            page-break-after: always;
        }

        .story-title {
            font-size: 36pt;
            font-weight: bold;
            color: {{ title_color }};
            margin-bottom: 0.3in;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        .story-author {
            font-size: 18pt;
            color: {{ author_color }};
            margin-top: 0.3in;
        }

        .story-author::before {
            content: "By ";
            font-style: italic;
        }

        .story-illustrator {
            font-size: 14pt;
            color: {{ author_color }};
            font-style: italic;
            margin-top: 0.1in;
        }

        /* Story Page */
        .story-page {
            page-break-after: always;
            min-height: 6in;
        }

        /* Illustration Placeholder */
        .illustration {
            width: 100%;
            height: 4in;
            border: 3px dashed {{ border_color }};
            background: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0.2in 0;
            border-radius: 10px;
        }

        .illustration-note {
            font-size: 14pt;
            color: #999;
            font-style: italic;
        }

        /* Text Blocks */
        .story-text {
            font-size: {{ story_font_size }};
            line-height: 1.8;
            margin: 0.2in 0;
        }

        .story-text p {
            margin-bottom: 0.15in;
        }

        /* Decorative Elements */
        .ornament {
            text-align: center;
            font-size: 24pt;
            color: {{ ornament_color }};
            margin: 0.2in 0;
        }

        .divider {
            text-align: center;
            font-size: 18pt;
            color: {{ ornament_color }};
            margin: 0.15in 0;
        }

        /* Character Speech */
        .speech {
            background: #fffacd;
            border: 3px solid {{ speech_border }};
            border-radius: 20px;
            padding: 0.2in;
            margin: 0.15in 0;
            font-size: 16pt;
            position: relative;
        }

        .speech::before {
            content: attr(data-character);
            position: absolute;
            top: -0.15in;
            left: 0.2in;
            background: {{ speech_border }};
            color: #fff;
            padding: 0.05in 0.15in;
            border-radius: 10px;
            font-weight: bold;
            font-size: 12pt;
        }

        /* Sound Effects */
        .sound-effect {
            font-size: 24pt;
            font-weight: bold;
            color: {{ sound_color }};
            text-align: center;
            margin: 0.15in 0;
            font-family: 'Impact', sans-serif;
            text-transform: uppercase;
        }

        /* Emphasis */
        .big {
            font-size: 150%;
            font-weight: bold;
        }

        .small {
            font-size: 75%;
        }

        strong {
            font-weight: bold;
            color: {{ emphasis_color }};
        }

        em {
            font-style: italic;
        }

        /* The End */
        .the-end {
            text-align: center;
            font-size: 36pt;
            font-weight: bold;
            color: {{ title_color }};
            margin-top: 2in;
            page-break-before: always;
        }

        /* Page Numbers (optional) */
        .page-number {
            position: fixed;
            bottom: 0.3in;
            right: 0.3in;
            font-size: 14pt;
            color: #999;
        }
    </style>
</head>
<body>
    <!-- Title Page -->
    <div class="title-page">
        <div class="ornament">{{ title_ornament }}</div>
        <div class="story-title">{{ title }}</div>
        {% if subtitle %}<div style="font-size: 18pt; color: #666; margin-top: 0.1in;">{{ subtitle }}</div>{% endif %}
        <div class="story-author">{{ author }}</div>
        {% if illustrator %}<div class="story-illustrator">Illustrated by {{ illustrator }}</div>{% endif %}
    </div>

    <!-- Story Content -->
    <div class="story-content">
        {{ content | safe }}
    </div>

    <!-- The End -->
    <div class="the-end">
        The End
        <div class="ornament" style="margin-top: 0.2in;">{{ end_ornament }}</div>
    </div>
</body>
</html>
"""


def generate_storybook(
    title: str,
    content: str,
    output_path: Path,
    author: str = "Anonymous",
    subtitle: str = None,
    illustrator: str = None,
    base_font_size: str = "14pt",
    story_font_size: str = "16pt",
    page_color: str = "#fffef8",
    text_color: str = "#2c2c2c",
    title_color: str = "#e91e63",
    author_color: str = "#9c27b0",
    border_color: str = "#ff9800",
    ornament_color: str = "#4caf50",
    speech_border: str = "#2196f3",
    sound_color: str = "#ff5722",
    emphasis_color: str = "#e91e63",
    show_border: bool = True,
    title_ornament: str = "✨ 🌟 ✨",
    end_ornament: str = "🌈 ⭐ 🌈",
) -> Path:
    """
    Generate a children's storybook.

    Args:
        title: Story title
        content: Story content (HTML)
        output_path: Where to save PDF
        author: Author name
        subtitle: Subtitle
        illustrator: Illustrator name
        base_font_size: Base font size
        story_font_size: Story text font size
        page_color: Page background color
        text_color: Text color
        title_color: Title color
        author_color: Author byline color
        border_color: Border color
        ornament_color: Decorative ornament color
        speech_border: Speech bubble border color
        sound_color: Sound effect color
        emphasis_color: Emphasis color
        show_border: Show decorative border
        title_ornament: Title page ornament
        end_ornament: End page ornament

    Returns:
        Path to generated PDF

    Content classes:
        .story-page - New page
        .illustration - Illustration placeholder
        .story-text - Story text block
        .speech - Character speech bubble (use data-character attribute)
        .sound-effect - Sound effect text
        .ornament - Decorative ornament
        .divider - Section divider
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(STORYBOOK_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        author=author,
        subtitle=subtitle,
        illustrator=illustrator,
        base_font_size=base_font_size,
        story_font_size=story_font_size,
        page_color=page_color,
        text_color=text_color,
        title_color=title_color,
        author_color=author_color,
        border_color=border_color,
        ornament_color=ornament_color,
        speech_border=speech_border,
        sound_color=sound_color,
        emphasis_color=emphasis_color,
        show_border=show_border,
        title_ornament=title_ornament,
        end_ornament=end_ornament,
    )

    HTML(string=html_output).write_pdf(output_path)
    return output_path
