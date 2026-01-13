"""
Academic Paper Template
========================

Two-column academic paper template matching the style of "Attention Is All You Need"
and similar NIPS/NeurIPS conference papers.

Features:
- Two-column layout
- Abstract section
- Author affiliations
- Section numbering
- Figure/table support
- References section
- Clean, professional academic typography
"""

from pathlib import Path
from jinja2 import Template
from weasyprint import HTML


ACADEMIC_PAPER_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        @page {
            size: letter;
            margin: 0.75in 0.5in;
        }

        body {
            font-family: 'Times New Roman', 'Times', serif;
            font-size: 10pt;
            line-height: 1.2;
            color: #000;
            counter-reset: section;
        }

        .content {
            column-count: 2;
            column-gap: 0.3in;
            column-rule: none;
        }

        /* Title and Authors */
        .title-section {
            column-span: all;
            text-align: center;
            margin-bottom: 0.2in;
            padding-bottom: 0.15in;
            border-bottom: 1px solid #000;
        }

        .title {
            font-size: 16pt;
            font-weight: bold;
            margin-bottom: 0.1in;
            line-height: 1.3;
        }

        .authors {
            font-size: 10pt;
            margin-bottom: 0.05in;
        }

        .affiliations {
            font-size: 9pt;
            font-style: italic;
            margin-bottom: 0.1in;
        }

        .email {
            font-size: 9pt;
            font-style: italic;
        }

        /* Abstract */
        .abstract {
            column-span: all;
            margin: 0.2in 0;
            padding: 0.15in;
            background: #f9f9f9;
            border: 1px solid #ddd;
        }

        .abstract-title {
            font-weight: bold;
            font-size: 10pt;
            margin-bottom: 0.1in;
            text-align: center;
        }

        .abstract-text {
            font-size: 9pt;
            text-align: justify;
            line-height: 1.4;
        }

        /* Sections */
        h1 {
            column-span: all;
            font-size: 12pt;
            font-weight: bold;
            margin-top: 0.2in;
            margin-bottom: 0.1in;
            counter-increment: section;
            counter-reset: subsection;
        }

        h1:before {
            content: counter(section) ". ";
        }

        h2 {
            column-span: all;
            font-size: 11pt;
            font-weight: bold;
            margin-top: 0.15in;
            margin-bottom: 0.08in;
            counter-increment: subsection;
            counter-reset: subsubsection;
        }

        h2:before {
            content: counter(section) "." counter(subsection) " ";
        }

        h3 {
            font-size: 10pt;
            font-weight: bold;
            margin-top: 0.1in;
            margin-bottom: 0.05in;
        }

        /* Body text */
        p {
            margin-bottom: 0.1in;
            text-align: justify;
            orphans: 3;
            widows: 3;
        }

        /* Equations */
        .equation {
            text-align: center;
            margin: 0.15in 0;
            font-family: 'Times New Roman', serif;
        }

        .equation-number {
            float: right;
            margin-right: 0.2in;
        }

        /* Figures and Tables */
        .figure {
            column-span: all;
            text-align: center;
            margin: 0.2in 0;
        }

        .figure-caption {
            font-size: 9pt;
            margin-top: 0.05in;
            text-align: center;
        }

        .table {
            column-span: all;
            margin: 0.2in 0;
            font-size: 9pt;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.1in 0;
        }

        th, td {
            border: 1px solid #000;
            padding: 0.05in;
            text-align: left;
        }

        th {
            background: #f0f0f0;
            font-weight: bold;
        }

        /* Lists */
        ul, ol {
            margin: 0.1in 0;
            padding-left: 0.2in;
        }

        li {
            margin-bottom: 0.05in;
        }

        /* References */
        .references {
            column-span: all;
            margin-top: 0.3in;
            padding-top: 0.2in;
            border-top: 1px solid #000;
        }

        .references h1 {
            font-size: 12pt;
            margin-bottom: 0.1in;
        }

        .reference {
            font-size: 9pt;
            margin-bottom: 0.08in;
            text-indent: -0.2in;
            padding-left: 0.2in;
            line-height: 1.3;
        }

        /* Code/Algorithm blocks */
        pre {
            font-family: 'Courier New', monospace;
            font-size: 8pt;
            background: #f5f5f5;
            border: 1px solid #ddd;
            padding: 0.1in;
            margin: 0.1in 0;
            overflow-x: auto;
            column-span: all;
        }

        code {
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            background: #f5f5f5;
            padding: 0.02in 0.05in;
        }

        /* First page adjustments */
        @page :first {
            @top-center {
                content: "{{ conference or 'arXiv' }} {{ year or '2024' }}";
                font-size: 9pt;
                font-family: 'Times New Roman', serif;
            }
        }

        /* Page numbers */
        @bottom-center {
            content: counter(page);
            font-size: 9pt;
            font-family: 'Times New Roman', serif;
        }

        /* Avoid column breaks in bad places */
        h1, h2, .figure, .table, pre {
            break-inside: avoid;
        }
    </style>
</head>
<body>
    <div class="title-section">
        <div class="title">{{ title }}</div>
        {% if authors %}
        <div class="authors">
            {% for author in authors %}
            {{ author.name }}{% if not loop.last %}, {% endif %}
            {% endfor %}
        </div>
        {% endif %}
        {% if affiliations %}
        <div class="affiliations">
            {% for affil in affiliations %}
            {{ affil }}{% if not loop.last %}, {% endif %}
            {% endfor %}
        </div>
        {% endif %}
        {% if email %}
        <div class="email">{{ email }}</div>
        {% endif %}
    </div>

    <div class="abstract">
        <div class="abstract-title">Abstract</div>
        <div class="abstract-text">{{ abstract }}</div>
    </div>

    <div class="content">
        {{ content|safe }}
    </div>

    {% if references %}
    <div class="references">
        <h1>References</h1>
        {% for ref in references %}
        <div class="reference">{{ ref }}</div>
        {% endfor %}
    </div>
    {% endif %}
</body>
</html>
"""


def generate_academic_paper(
    title: str,
    content: str,
    output_path: Path,
    abstract: str = "",
    authors: list = None,
    affiliations: list = None,
    email: str = None,
    conference: str = "arXiv",
    year: str = None,
    references: list = None
) -> Path:
    """
    Generate an academic paper PDF.

    Args:
        title: Paper title
        content: Main content (HTML, will be rendered in two columns)
        output_path: Where to save PDF
        abstract: Abstract text
        authors: List of author dicts with 'name' key
        affiliations: List of affiliation strings
        email: Contact email
        conference: Conference name (default: "arXiv")
        year: Publication year
        references: List of reference strings

    Returns:
        Path to generated PDF
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if year is None:
        from datetime import datetime
        year = str(datetime.now().year)

    template = Template(ACADEMIC_PAPER_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        abstract=abstract,
        authors=authors or [],
        affiliations=affiliations or [],
        email=email,
        conference=conference,
        year=year,
        references=references or []
    )

    HTML(string=html_output).write_pdf(output_path)
    return output_path
