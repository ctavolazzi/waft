"""
Code Documentation Template
============================

Technical documentation for code, APIs, and software architecture.
CRITICAL for project documentation moving forward.

Features:
- Clear technical writing
- Code blocks with syntax highlighting
- API reference formatting
- Data structure diagrams
- Algorithm explanations
- Dependency trees
- Architecture overviews
- Parameter tables
- Return value documentation
"""

from pathlib import Path

from jinja2 import Template
from weasyprint import HTML

CODE_DOCUMENTATION_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        @page {
            size: letter;
            margin: 0.75in 1in;

            @top-left {
                content: "{{ project }} Documentation";
                font-family: 'Arial', sans-serif;
                font-size: 9pt;
                color: #666;
            }

            @top-right {
                content: "{{ version }}";
                font-family: 'Arial', sans-serif;
                font-size: 9pt;
                color: #666;
            }

            @bottom-center {
                content: "Page " counter(page);
                font-family: 'Arial', sans-serif;
                font-size: 9pt;
                color: #666;
            }
        }

        @page :first {
            @top-left { content: none; }
            @top-right { content: none; }
        }

        body {
            font-family: 'Arial', 'Helvetica', sans-serif;
            font-size: 10pt;
            line-height: 1.5;
            color: #2c2c2c;
        }

        /* Title Page */
        .doc-title-page {
            text-align: center;
            margin-top: 2in;
            margin-bottom: 0.5in;
        }

        .doc-title {
            font-size: 24pt;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 0.2in;
        }

        .doc-subtitle {
            font-size: 14pt;
            color: #7f8c8d;
            margin-bottom: 0.3in;
        }

        .doc-meta {
            font-size: 11pt;
            color: #95a5a6;
            line-height: 1.8;
        }

        /* Section Headers */
        h1 {
            font-size: 18pt;
            font-weight: bold;
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.08in;
            margin-top: 0.4in;
            margin-bottom: 0.2in;
            page-break-after: avoid;
        }

        h2 {
            font-size: 14pt;
            font-weight: bold;
            color: #34495e;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 0.05in;
            margin-top: 0.3in;
            margin-bottom: 0.15in;
            page-break-after: avoid;
        }

        h3 {
            font-size: 12pt;
            font-weight: bold;
            color: #34495e;
            margin-top: 0.2in;
            margin-bottom: 0.1in;
            page-break-after: avoid;
        }

        h4 {
            font-size: 11pt;
            font-weight: bold;
            color: #7f8c8d;
            margin-top: 0.15in;
            margin-bottom: 0.08in;
            page-break-after: avoid;
        }

        /* Code Blocks */
        pre {
            background: #2c3e50;
            color: #ecf0f1;
            border-left: 4px solid #3498db;
            padding: 0.15in;
            font-family: 'Courier New', 'Consolas', monospace;
            font-size: 9pt;
            line-height: 1.4;
            overflow-x: auto;
            page-break-inside: avoid;
            margin: 0.15in 0;
        }

        code {
            font-family: 'Courier New', 'Consolas', monospace;
            font-size: 9pt;
            background: #ecf0f1;
            color: #e74c3c;
            padding: 0.02in 0.05in;
            border-radius: 2px;
        }

        pre code {
            background: transparent;
            color: #ecf0f1;
            padding: 0;
        }

        /* Syntax Highlighting (Basic) */
        .keyword { color: #e74c3c; font-weight: bold; }
        .string { color: #2ecc71; }
        .comment { color: #95a5a6; font-style: italic; }
        .function { color: #f39c12; }
        .class { color: #9b59b6; font-weight: bold; }
        .number { color: #3498db; }

        /* API Reference */
        .api-function {
            background: #ecf0f1;
            border-left: 4px solid #3498db;
            padding: 0.15in;
            margin: 0.15in 0;
            page-break-inside: avoid;
        }

        .api-signature {
            font-family: 'Courier New', monospace;
            font-size: 11pt;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 0.1in;
        }

        .api-description {
            margin-bottom: 0.1in;
        }

        /* Parameter Table */
        table.param-table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.15in 0;
            font-size: 9pt;
        }

        table.param-table th {
            background: #34495e;
            color: #fff;
            border: 1px solid #2c3e50;
            padding: 0.08in;
            text-align: left;
            font-weight: bold;
        }

        table.param-table td {
            border: 1px solid #bdc3c7;
            padding: 0.08in;
            vertical-align: top;
        }

        table.param-table tr:nth-child(even) {
            background: #f9f9f9;
        }

        table.param-table .param-name {
            font-family: 'Courier New', monospace;
            color: #e74c3c;
            font-weight: bold;
        }

        table.param-table .param-type {
            font-family: 'Courier New', monospace;
            color: #3498db;
            font-style: italic;
        }

        /* Callout Boxes */
        .note {
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 0.12in;
            margin: 0.15in 0;
        }

        .note-title {
            font-weight: bold;
            color: #1976d2;
            text-transform: uppercase;
            font-size: 9pt;
            margin-bottom: 0.05in;
        }

        .warning {
            background: #fff3e0;
            border-left: 4px solid #ff9800;
            padding: 0.12in;
            margin: 0.15in 0;
        }

        .warning-title {
            font-weight: bold;
            color: #f57c00;
            text-transform: uppercase;
            font-size: 9pt;
            margin-bottom: 0.05in;
        }

        .tip {
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
            padding: 0.12in;
            margin: 0.15in 0;
        }

        .tip-title {
            font-weight: bold;
            color: #388e3c;
            text-transform: uppercase;
            font-size: 9pt;
            margin-bottom: 0.05in;
        }

        .danger {
            background: #ffebee;
            border-left: 4px solid #f44336;
            padding: 0.12in;
            margin: 0.15in 0;
        }

        .danger-title {
            font-weight: bold;
            color: #d32f2f;
            text-transform: uppercase;
            font-size: 9pt;
            margin-bottom: 0.05in;
        }

        /* Architecture Diagram */
        .diagram {
            background: #f9f9f9;
            border: 1px solid #bdc3c7;
            padding: 0.15in;
            margin: 0.15in 0;
            font-family: 'Courier New', monospace;
            font-size: 8pt;
            white-space: pre;
            text-align: center;
        }

        /* Data Structure */
        .data-structure {
            background: #fafafa;
            border: 2px solid #3498db;
            padding: 0.15in;
            margin: 0.15in 0;
            page-break-inside: avoid;
        }

        .data-structure-title {
            font-family: 'Courier New', monospace;
            font-size: 12pt;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 0.1in;
        }

        /* Lists */
        ul, ol {
            margin-left: 0.3in;
            margin-bottom: 0.12in;
        }

        li {
            margin-bottom: 0.05in;
        }

        /* Inline elements */
        strong {
            font-weight: bold;
        }

        em {
            font-style: italic;
        }

        .monospace {
            font-family: 'Courier New', monospace;
            background: #ecf0f1;
            padding: 0.02in 0.05in;
        }

        /* Table of Contents */
        .toc {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            padding: 0.2in;
            margin: 0.2in 0;
        }

        .toc-title {
            font-size: 14pt;
            font-weight: bold;
            margin-bottom: 0.15in;
        }

        .toc ul {
            list-style: none;
            margin-left: 0;
        }

        .toc li {
            margin-bottom: 0.08in;
        }

        .toc a {
            text-decoration: none;
            color: #3498db;
        }

        /* Paragraphs */
        p {
            margin-bottom: 0.12in;
        }
    </style>
</head>
<body>
    {% if show_title_page %}
    <div class="doc-title-page">
        <div class="doc-title">{{ title }}</div>
        {% if subtitle %}<div class="doc-subtitle">{{ subtitle }}</div>{% endif %}
        <div class="doc-meta">
            {% if project %}<div><strong>Project:</strong> {{ project }}</div>{% endif %}
            {% if version %}<div><strong>Version:</strong> {{ version }}</div>{% endif %}
            {% if author %}<div><strong>Author:</strong> {{ author }}</div>{% endif %}
            {% if date %}<div><strong>Date:</strong> {{ date }}</div>{% endif %}
        </div>
    </div>
    <div style="page-break-after: always;"></div>
    {% endif %}

    <div class="content">
        {{ content | safe }}
    </div>
</body>
</html>
"""


def generate_code_documentation(
    title: str,
    content: str,
    output_path: Path,
    subtitle: str = None,
    project: str = "Project",
    version: str = "1.0.0",
    author: str = None,
    date: str = None,
    show_title_page: bool = True,
) -> Path:
    """
    Generate technical code documentation.

    Args:
        title: Document title
        content: Main content (HTML with proper classes)
        output_path: Where to save PDF
        subtitle: Subtitle
        project: Project name
        version: Version number
        author: Author name
        date: Date
        show_title_page: Show title page

    Returns:
        Path to generated PDF

    Content classes:
        .api-function - API function documentation
        .api-signature - Function signature
        .param-table - Parameter table
        .note - Note callout
        .warning - Warning callout
        .tip - Tip callout
        .danger - Danger callout
        .diagram - ASCII architecture diagram
        .data-structure - Data structure documentation
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(CODE_DOCUMENTATION_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        subtitle=subtitle,
        project=project,
        version=version,
        author=author,
        date=date,
        show_title_page=show_title_page,
    )

    HTML(string=html_output).write_pdf(output_path)
    return output_path
