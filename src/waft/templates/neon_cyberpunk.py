"""
Neon Cyberpunk Template
=======================

A bold, futuristic template inspired by cyberpunk aesthetics. High contrast,
vibrant colors, and tech-inspired design elements.

Features:
- Dark background with neon accents
- High contrast typography
- Tech-inspired borders and dividers
- Vibrant color palette (cyan, magenta, yellow)
- Futuristic aesthetic
- Grid-based layout hints
"""

from pathlib import Path

from jinja2 import Template
from weasyprint import HTML

NEON_CYBERPUNK_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        @page {
            size: letter;
            margin: 0.75in;
            background: #0a0a0a;
        }

        body {
            font-family: 'Courier New', 'Monaco', monospace;
            font-size: 10pt;
            line-height: 1.6;
            color: #00ff88;
            background: #0a0a0a;
            margin: 0;
            padding: 0;
        }

        .container {
            border: 2px solid #00ffff;
            padding: 0.5in;
            background: #0a0a0a;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
        }

        h1 {
            font-size: 32pt;
            font-weight: bold;
            margin: 0 0 0.3in 0;
            color: #ff00ff;
            text-transform: uppercase;
            letter-spacing: 3px;
            text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
            border-bottom: 3px solid #00ffff;
            padding-bottom: 0.2in;
        }

        h2 {
            font-size: 20pt;
            font-weight: bold;
            margin: 0.4in 0 0.2in 0;
            color: #00ffff;
            text-transform: uppercase;
            letter-spacing: 2px;
            border-left: 4px solid #ffff00;
            padding-left: 0.2in;
        }

        h3 {
            font-size: 14pt;
            font-weight: bold;
            margin: 0.3in 0 0.15in 0;
            color: #ffff00;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        p {
            margin: 0 0 0.25in 0;
            color: #00ff88;
            text-align: left;
        }

        .content {
            margin-top: 0.2in;
        }

        .divider {
            height: 2px;
            background: linear-gradient(to right, #00ffff, #ff00ff, #ffff00, #00ffff);
            margin: 0.4in 0;
            border: none;
        }

        strong {
            font-weight: bold;
            color: #ffff00;
            text-shadow: 0 0 5px #ffff00;
        }

        em {
            font-style: italic;
            color: #ff00ff;
        }

        ul, ol {
            margin: 0.25in 0;
            padding-left: 0.4in;
            border-left: 2px solid #00ffff;
        }

        li {
            margin: 0.1in 0;
            color: #00ff88;
        }

        blockquote {
            margin: 0.3in 0.4in;
            padding: 0.2in;
            border: 2px solid #ff00ff;
            background: rgba(255, 0, 255, 0.1);
            color: #ff00ff;
            font-style: italic;
            box-shadow: 0 0 10px rgba(255, 0, 255, 0.3);
        }

        code {
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            background: #1a1a1a;
            color: #00ffff;
            padding: 3px 6px;
            border: 1px solid #00ffff;
            border-radius: 2px;
        }

        pre {
            background: #1a1a1a;
            border: 2px solid #00ffff;
            padding: 0.25in;
            margin: 0.25in 0;
            overflow-x: auto;
            font-size: 9pt;
            line-height: 1.4;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.4);
        }

        pre code {
            background: none;
            border: none;
            padding: 0;
            color: #00ffff;
        }

        .glitch {
            text-shadow:
                2px 0 #ff00ff,
                -2px 0 #00ffff,
                0 2px #ffff00;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="glitch">{{ title }}</h1>
        <div class="content">
            {{ content }}
        </div>
    </div>
</body>
</html>
"""


def generate_neon_cyberpunk(title: str, content: str, output_path: Path, **kwargs) -> Path:
    """
    Generate a Neon Cyberpunk PDF.

    Args:
        title: Document title
        content: Main content (HTML)
        output_path: Where to save PDF
        **kwargs: Additional template-specific parameters

    Returns:
        Path to generated PDF
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(NEON_CYBERPUNK_TEMPLATE)
    html_output = template.render(title=title, content=content, **kwargs)

    HTML(string=html_output).write_pdf(output_path)

    # Post-process to add blank page markers
    try:
        from ..utils import process_pdf_for_blank_pages

        process_pdf_for_blank_pages(output_path)
    except Exception as e:
        print(f"⚠️  Blank page marker processing failed: {e}")

    return output_path
