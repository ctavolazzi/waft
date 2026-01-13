"""
PDF Generator using Jinja2 Templates + WeasyPrint
Converts markdown file to PDF using Jinja2 template engine and WeasyPrint.
"""

from pathlib import Path
from jinja2 import Template
from weasyprint import HTML
import markdown


def generate_pdf_jinja(md_file: Path, output_path: Path):
    """Generate PDF from markdown using Jinja2 template + WeasyPrint."""
    
    # Read markdown file
    md_content = md_file.read_text()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['fenced_code', 'tables', 'nl2br', 'extra', 'codehilite']
    )
    
    # Jinja2 template for document structure
    template_str = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
    <style>
        @page {
            size: letter;
            margin: 1in;
        }
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #1a1a1a;
            max-width: 100%;
        }
        .document-header {
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 0.2in;
            margin-bottom: 0.3in;
        }
        .document-title {
            font-size: 24pt;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 0.1in;
        }
        .document-meta {
            font-size: 9pt;
            color: #666;
            font-style: italic;
        }
        h1 {
            font-size: 18pt;
            font-weight: bold;
            margin-top: 0.5in;
            margin-bottom: 0.3in;
            color: #2c3e50;
            border-bottom: 1px solid #dee2e6;
            padding-bottom: 0.1in;
            page-break-after: avoid;
        }
        h2 {
            font-size: 16pt;
            font-weight: bold;
            margin-top: 0.4in;
            margin-bottom: 0.2in;
            color: #34495e;
            page-break-after: avoid;
        }
        h3 {
            font-size: 14pt;
            font-weight: bold;
            margin-top: 0.3in;
            margin-bottom: 0.15in;
            color: #34495e;
            page-break-after: avoid;
        }
        p {
            margin-bottom: 0.1in;
            text-align: justify;
        }
        ul, ol {
            margin-left: 0.3in;
            margin-bottom: 0.1in;
        }
        li {
            margin-bottom: 0.05in;
        }
        code {
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            background-color: #f8f9fa;
            padding: 2px 6px;
            border-radius: 3px;
            color: #e83e8c;
        }
        pre {
            background-color: #f8f9fa;
            padding: 0.2in;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 9pt;
            border-left: 4px solid #2c3e50;
        }
        pre code {
            background-color: transparent;
            padding: 0;
            color: #333;
        }
        hr {
            border: none;
            border-top: 2px solid #dee2e6;
            margin: 0.4in 0;
        }
        strong {
            font-weight: bold;
            color: #2c3e50;
        }
        em {
            font-style: italic;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 0.2in 0;
        }
        th, td {
            border: 1px solid #dee2e6;
            padding: 0.1in;
            text-align: left;
        }
        th {
            background-color: #f8f9fa;
            font-weight: bold;
            color: #2c3e50;
        }
        .content {
            margin-top: 0.3in;
        }
    </style>
</head>
<body>
    <div class="document-header">
        <div class="document-title">{{ title }}</div>
        <div class="document-meta">Generated: {{ date }}</div>
    </div>
    <div class="content">
        {{ content|safe }}
    </div>
</body>
</html>"""
    
    # Create Jinja2 template
    template = Template(template_str)
    
    # Extract title from markdown (first h1 or filename)
    title = "Document"
    lines = md_content.split('\n')
    for line in lines[:10]:  # Check first 10 lines
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    # Render template with content
    from datetime import datetime
    rendered_html = template.render(
        title=title,
        date=datetime.now().strftime("%B %d, %Y at %I:%M %p"),
        content=html_content
    )
    
    # Generate PDF using WeasyPrint
    HTML(string=rendered_html).write_pdf(str(output_path))
    print(f"✅ Jinja2+WeasyPrint PDF generated: {output_path}")


if __name__ == "__main__":
    # Input markdown file
    md_file = Path("_temp_pdf_samples/session_recap_2026-01-12.md")
    output_path = Path("_temp_pdf_samples/session_recap_jinja.pdf")
    
    generate_pdf_jinja(md_file, output_path)
