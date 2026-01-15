"""
Minimalist Zen Template
=======================

A clean, minimal template inspired by Zen aesthetics. Focus on whitespace,
simple typography, and peaceful reading experience.

Features:
- Generous whitespace
- Minimal color palette (black, white, subtle gray)
- Simple, elegant typography
- No borders or heavy decorations
- Focus on content clarity
- Breathing room between elements
"""

from pathlib import Path
from jinja2 import Template
from weasyprint import HTML


MINIMALIST_ZEN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        @page {
            size: letter;
            margin: 1.5in 1in;
        }

        @page :first {
            margin-top: 2in;
        }

        body {
            font-family: 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif;
            font-size: 11pt;
            line-height: 1.8;
            color: #2a2a2a;
            background: #ffffff;
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 5.5in;
            margin: 0 auto;
        }

        h1 {
            font-size: 28pt;
            font-weight: 300;
            letter-spacing: -0.5px;
            margin: 0 0 0.5in 0;
            color: #1a1a1a;
            line-height: 1.3;
        }

        h2 {
            font-size: 18pt;
            font-weight: 400;
            margin: 0.6in 0 0.3in 0;
            color: #333;
            letter-spacing: 0.5px;
        }

        h3 {
            font-size: 14pt;
            font-weight: 400;
            margin: 0.4in 0 0.2in 0;
            color: #444;
        }

        p {
            margin: 0 0 0.4in 0;
            text-align: justify;
            hyphens: auto;
        }

        .content {
            margin-top: 0.3in;
        }

        .spacer {
            height: 0.3in;
        }

        .divider {
            height: 1px;
            background: #e0e0e0;
            margin: 0.5in 0;
            border: none;
        }

        strong {
            font-weight: 500;
            color: #1a1a1a;
        }

        em {
            font-style: italic;
            color: #555;
        }

        ul, ol {
            margin: 0.3in 0;
            padding-left: 0.3in;
        }

        li {
            margin: 0.15in 0;
        }

        blockquote {
            margin: 0.4in 0.5in;
            padding-left: 0.3in;
            border-left: 2px solid #d0d0d0;
            color: #555;
            font-style: italic;
        }

        code {
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 9pt;
            background: #f5f5f5;
            padding: 2px 4px;
            border-radius: 2px;
        }

        pre {
            background: #f5f5f5;
            padding: 0.3in;
            margin: 0.3in 0;
            border-radius: 3px;
            overflow-x: auto;
            font-size: 9pt;
            line-height: 1.5;
        }

        pre code {
            background: none;
            padding: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ title }}</h1>
        <div class="content">
            {{ content }}
        </div>
    </div>
</body>
</html>
"""


def generate_minimalist_zen(
    title: str,
    content: str,
    output_path: Path,
    **kwargs
) -> Path:
    """
    Generate a Minimalist Zen PDF.

    Args:
        title: Document title
        content: Main content (HTML)
        output_path: Where to save PDF
        **kwargs: Additional template-specific parameters

    Returns:
        Path to generated PDF
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(MINIMALIST_ZEN_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        **kwargs
    )

    HTML(string=html_output).write_pdf(output_path)
    
    # Post-process to add blank page markers
    try:
        from ..utils import process_pdf_for_blank_pages
        process_pdf_for_blank_pages(output_path)
    except Exception as e:
        print(f"⚠️  Blank page marker processing failed: {e}")
    
    return output_path
