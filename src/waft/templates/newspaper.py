"""
Newspaper Front Page Template
==============================

Classic newspaper front page layout.
Tests multi-column, headlines, bylines, photo captions.

Features:
- Multi-column layout
- Banner headline
- Subheadlines
- Bylines
- Photo placeholders with captions
- Pull quotes
- Classified aesthetic
- Date/edition info
"""

from pathlib import Path

from jinja2 import Template
from weasyprint import HTML

NEWSPAPER_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        @page {
            size: letter;
            margin: 0.5in 0.3in;
        }

        body {
            font-family: 'Times New Roman', 'Georgia', serif;
            font-size: 10pt;
            line-height: 1.3;
            color: #000;
            column-count: {{ columns }};
            column-gap: 0.25in;
            column-rule: 1px solid #ddd;
        }

        /* Masthead (Newspaper Name) */
        .masthead {
            column-span: all;
            text-align: center;
            border-top: 3px solid #000;
            border-bottom: 3px solid #000;
            padding: 0.15in 0;
            margin-bottom: 0.15in;
        }

        .newspaper-name {
            font-family: 'Georgia', serif;
            font-size: 48pt;
            font-weight: bold;
            font-style: italic;
            margin-bottom: 0.05in;
        }

        .newspaper-tagline {
            font-size: 9pt;
            font-style: italic;
            color: #666;
        }

        .newspaper-info {
            display: flex;
            justify-content: space-between;
            font-size: 8pt;
            margin-top: 0.08in;
            color: #666;
        }

        /* Banner Headline */
        .banner-headline {
            column-span: all;
            font-size: 36pt;
            font-weight: bold;
            font-family: 'Impact', 'Arial Black', sans-serif;
            text-transform: uppercase;
            text-align: center;
            line-height: 1.1;
            margin: 0.15in 0;
            border-top: 2px solid #000;
            border-bottom: 2px solid #000;
            padding: 0.1in 0;
        }

        /* Headlines */
        h1.headline {
            font-size: 20pt;
            font-weight: bold;
            font-family: 'Arial Black', 'Impact', sans-serif;
            line-height: 1.1;
            margin: 0.1in 0 0.05in 0;
            column-span: all;
        }

        h2.subheadline {
            font-size: 14pt;
            font-weight: bold;
            line-height: 1.2;
            margin: 0.08in 0 0.05in 0;
        }

        h3.minor-headline {
            font-size: 12pt;
            font-weight: bold;
            line-height: 1.2;
            margin: 0.08in 0 0.05in 0;
        }

        /* Byline */
        .byline {
            font-size: 9pt;
            font-style: italic;
            color: #666;
            margin-bottom: 0.08in;
        }

        .byline::before {
            content: "By ";
        }

        /* Lead Paragraph */
        .lead {
            font-weight: bold;
            font-size: 11pt;
        }

        /* Paragraphs */
        p {
            margin-bottom: 0.08in;
            text-align: justify;
        }

        /* Pull Quote */
        .pull-quote {
            column-span: all;
            border-top: 2px solid #000;
            border-bottom: 2px solid #000;
            padding: 0.12in;
            margin: 0.15in 0;
            text-align: center;
            font-size: 16pt;
            font-style: italic;
            font-weight: bold;
            background: #f9f9f9;
        }

        .pull-quote-source {
            font-size: 10pt;
            font-weight: normal;
            margin-top: 0.05in;
            color: #666;
        }

        /* Photo Placeholder */
        .photo {
            width: 100%;
            height: 2.5in;
            border: 1px solid #000;
            background: #e0e0e0;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0.1in 0 0.05in 0;
            page-break-inside: avoid;
        }

        .photo-note {
            font-size: 10pt;
            color: #999;
            font-style: italic;
        }

        .caption {
            font-size: 9pt;
            font-style: italic;
            margin-bottom: 0.1in;
            text-align: left;
        }

        /* Section Break */
        .section-break {
            column-span: all;
            border-bottom: 2px solid #000;
            margin: 0.15in 0;
        }

        /* Sidebar Box */
        .sidebar {
            background: #f5f5f5;
            border: 2px solid #000;
            padding: 0.12in;
            margin: 0.1in 0;
            page-break-inside: avoid;
        }

        .sidebar-title {
            font-weight: bold;
            font-size: 11pt;
            margin-bottom: 0.05in;
            text-transform: uppercase;
        }

        /* Breaking News Banner */
        .breaking {
            column-span: all;
            background: #c00;
            color: #fff;
            text-align: center;
            padding: 0.08in;
            font-weight: bold;
            font-size: 12pt;
            text-transform: uppercase;
            margin: 0.1in 0;
        }

        /* Dateline */
        .dateline {
            font-weight: bold;
            font-size: 9pt;
            text-transform: uppercase;
        }

        /* Jump/Continued */
        .continued {
            font-style: italic;
            font-size: 9pt;
            text-align: right;
            margin-top: 0.08in;
        }

        /* Emphasis */
        strong {
            font-weight: bold;
        }

        em {
            font-style: italic;
        }

        /* Drop cap (first letter large) */
        .drop-cap::first-letter {
            font-size: 48pt;
            font-weight: bold;
            float: left;
            line-height: 0.8;
            margin-right: 0.05in;
        }
    </style>
</head>
<body>
    <!-- Masthead -->
    <div class="masthead">
        <div class="newspaper-name">{{ newspaper_name }}</div>
        <div class="newspaper-tagline">{{ tagline }}</div>
        <div class="newspaper-info">
            <div>{{ location }}</div>
            <div>{{ date }}</div>
            <div>{{ edition }}</div>
            <div>{{ price }}</div>
        </div>
    </div>

    <!-- Content -->
    <div class="newspaper-content">
        {{ content | safe }}
    </div>
</body>
</html>
"""


def generate_newspaper(
    content: str,
    output_path: Path,
    title: str = "Newspaper",
    newspaper_name: str = "THE DAILY CHRONICLE",
    tagline: str = "All the News That's Fit to Print",
    location: str = "New York, NY",
    date: str = "January 11, 2026",
    edition: str = "Morning Edition",
    price: str = "$2.00",
    columns: int = 3,
) -> Path:
    """
    Generate a newspaper front page.

    Args:
        content: Newspaper content (HTML)
        output_path: Where to save PDF
        title: Document title
        newspaper_name: Newspaper name
        tagline: Newspaper tagline
        location: Publication location
        date: Publication date
        edition: Edition info
        price: Price
        columns: Number of columns (2-4 recommended)

    Returns:
        Path to generated PDF

    Content classes:
        .banner-headline - Large banner headline (spans all columns)
        h1.headline - Major headline (spans all columns)
        h2.subheadline - Subheadline
        h3.minor-headline - Minor headline
        .byline - Author byline
        .lead - Lead paragraph (bold)
        .pull-quote - Pull quote (spans all columns)
        .photo - Photo placeholder
        .caption - Photo caption
        .breaking - Breaking news banner
        .sidebar - Sidebar box
        .dateline - Dateline (location + date)
        .drop-cap - Paragraph with large first letter
        .section-break - Section divider
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(NEWSPAPER_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        newspaper_name=newspaper_name,
        tagline=tagline,
        location=location,
        date=date,
        edition=edition,
        price=price,
        columns=columns,
    )

    HTML(string=html_output).write_pdf(output_path)
    return output_path
