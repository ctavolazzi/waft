"""
D&D Scenario Template
======================

A fantasy-themed template inspired by Dungeons & Dragons campaign materials.
Parchment aesthetic with medieval styling, perfect for scenarios, adventures,
and campaign documentation.

Features:
- Parchment/cream background with aged paper aesthetic
- Medieval serif typography
- Decorative borders and dividers
- Fantasy color palette (browns, golds, deep reds)
- Stat block styling
- Adventure-ready formatting
"""

from pathlib import Path
from jinja2 import Template
from weasyprint import HTML


DND_SCENARIO_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        @page {
            size: letter;
            margin: 0.75in;
            background: #f4e8d0;
        }

        @page :first {
            margin-top: 1in;
        }

        body {
            font-family: 'Times New Roman', 'Times', 'Georgia', serif;
            font-size: 11pt;
            line-height: 1.7;
            color: #3d2817;
            background: #f4e8d0;
            margin: 0;
            padding: 0;
        }

        .container {
            background: #faf5eb;
            border: 3px double #8b4513;
            padding: 0.5in;
            box-shadow: 0 0 15px rgba(139, 69, 19, 0.3);
            position: relative;
        }

        .container::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                repeating-linear-gradient(
                    0deg,
                    transparent,
                    transparent 2px,
                    rgba(139, 69, 19, 0.03) 2px,
                    rgba(139, 69, 19, 0.03) 4px
                );
            pointer-events: none;
        }

        h1 {
            font-size: 32pt;
            font-weight: bold;
            margin: 0 0 0.3in 0;
            color: #8b0000;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 2px;
            border-bottom: 4px double #8b4513;
            padding-bottom: 0.2in;
            font-family: 'Times New Roman', serif;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }

        h2 {
            font-size: 20pt;
            font-weight: bold;
            margin: 0.4in 0 0.2in 0;
            color: #654321;
            border-left: 5px solid #daa520;
            padding-left: 0.25in;
            background: linear-gradient(to right, rgba(218, 165, 32, 0.1), transparent);
        }

        h3 {
            font-size: 16pt;
            font-weight: bold;
            margin: 0.3in 0 0.15in 0;
            color: #8b4513;
            border-bottom: 2px solid #daa520;
            padding-bottom: 0.1in;
        }

        h4 {
            font-size: 13pt;
            font-weight: bold;
            margin: 0.25in 0 0.1in 0;
            color: #654321;
            font-style: italic;
        }

        p {
            margin: 0 0 0.25in 0;
            text-align: justify;
            text-indent: 0.25in;
        }

        p:first-of-type {
            text-indent: 0;
        }

        .content {
            margin-top: 0.2in;
            position: relative;
            z-index: 1;
        }

        .divider {
            height: 2px;
            background: linear-gradient(to right, transparent, #8b4513, transparent);
            margin: 0.4in 0;
            border: none;
            position: relative;
        }

        .divider::before,
        .divider::after {
            content: "❋";
            position: absolute;
            top: -8px;
            color: #daa520;
            font-size: 14pt;
        }

        .divider::before {
            left: 20%;
        }

        .divider::after {
            right: 20%;
        }

        strong {
            font-weight: bold;
            color: #8b0000;
        }

        em {
            font-style: italic;
            color: #654321;
        }

        ul, ol {
            margin: 0.25in 0;
            padding-left: 0.4in;
        }

        li {
            margin: 0.15in 0;
            color: #3d2817;
        }

        blockquote {
            margin: 0.3in 0.5in;
            padding: 0.25in;
            border-left: 4px solid #daa520;
            border-right: 4px solid #daa520;
            background: rgba(218, 165, 32, 0.1);
            color: #654321;
            font-style: italic;
            box-shadow: inset 0 0 10px rgba(139, 69, 19, 0.2);
        }

        .stat-block {
            background: #f0e6d2;
            border: 2px solid #8b4513;
            padding: 0.3in;
            margin: 0.3in 0;
            border-radius: 5px;
            box-shadow: 0 2px 8px rgba(139, 69, 19, 0.3);
        }

        .stat-block h4 {
            margin-top: 0;
            color: #8b0000;
            border-bottom: 2px solid #8b4513;
            padding-bottom: 0.1in;
        }

        .stat-line {
            display: flex;
            justify-content: space-between;
            padding: 0.05in 0;
            border-bottom: 1px dotted #8b4513;
        }

        .stat-line:last-child {
            border-bottom: none;
        }

        .stat-label {
            font-weight: bold;
            color: #654321;
        }

        .stat-value {
            color: #3d2817;
        }

        code {
            font-family: 'Courier New', 'Monaco', monospace;
            font-size: 9pt;
            background: #e8dcc6;
            color: #8b0000;
            padding: 2px 6px;
            border: 1px solid #8b4513;
            border-radius: 3px;
        }

        pre {
            background: #e8dcc6;
            border: 2px solid #8b4513;
            padding: 0.25in;
            margin: 0.25in 0;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 9pt;
            line-height: 1.5;
            box-shadow: inset 0 0 10px rgba(139, 69, 19, 0.2);
        }

        pre code {
            background: none;
            border: none;
            padding: 0;
            color: #3d2817;
        }

        .adventure-box {
            background: #faf5eb;
            border: 3px double #8b0000;
            padding: 0.3in;
            margin: 0.3in 0;
            border-radius: 5px;
            box-shadow: 0 0 15px rgba(139, 0, 0, 0.2);
        }

        .adventure-box h4 {
            margin-top: 0;
            color: #8b0000;
            text-align: center;
            border-bottom: 2px solid #8b0000;
            padding-bottom: 0.1in;
        }

        .challenge-rating {
            display: inline-block;
            background: #8b0000;
            color: #faf5eb;
            padding: 0.1in 0.2in;
            border-radius: 5px;
            font-weight: bold;
            margin: 0.1in 0;
        }

        .treasure-box {
            background: linear-gradient(135deg, #faf5eb 0%, #e8dcc6 100%);
            border: 2px solid #daa520;
            padding: 0.25in;
            margin: 0.25in 0;
            border-radius: 5px;
            box-shadow: 0 2px 8px rgba(218, 165, 32, 0.3);
        }

        .treasure-box::before {
            content: "💰 ";
            font-size: 14pt;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.25in 0;
            background: #faf5eb;
            border: 2px solid #8b4513;
        }

        th {
            background: #8b4513;
            color: #faf5eb;
            padding: 0.15in;
            text-align: left;
            font-weight: bold;
            border: 1px solid #654321;
        }

        td {
            padding: 0.1in 0.15in;
            border: 1px solid #8b4513;
            color: #3d2817;
        }

        tr:nth-child(even) {
            background: #f0e6d2;
        }

        .footer-note {
            margin-top: 0.5in;
            padding-top: 0.25in;
            border-top: 2px solid #8b4513;
            text-align: center;
            font-size: 9pt;
            color: #654321;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ title }}</h1>
        <div class="content">
            {{ content }}
        </div>
        <div class="footer-note">
            <p>Generated by WAFT Evolution System | D&D Scenario Template</p>
        </div>
    </div>
</body>
</html>
"""


def generate_dnd_scenario(
    title: str,
    content: str,
    output_path: Path,
    **kwargs
) -> Path:
    """
    Generate a D&D Scenario PDF.

    Args:
        title: Document title
        content: Main content (HTML)
        output_path: Where to save PDF
        **kwargs: Additional template-specific parameters

    Returns:
        Path to generated PDF
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(DND_SCENARIO_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        **kwargs
    )

    HTML(string=html_output).write_pdf(output_path)
    return output_path
