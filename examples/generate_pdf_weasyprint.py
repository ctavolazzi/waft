"""
PDF Generator using WeasyPrint
Converts markdown file to PDF using WeasyPrint (HTML/CSS → PDF).
"""

from pathlib import Path

import markdown
from weasyprint import HTML


def generate_pdf_weasyprint(md_file: Path, output_path: Path):
    """Generate PDF from markdown using WeasyPrint."""

    # Read markdown file
    md_content = md_file.read_text()

    # Convert markdown to HTML
    html_content = markdown.markdown(
        md_content, extensions=["fenced_code", "tables", "nl2br", "extra", "codehilite"]
    )

    # Wrap in full HTML document with CSS
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {{
            size: letter;
            margin: 1in;
        }}
        body {{
            font-family: 'Times New Roman', Times, serif;
            font-size: 11pt;
            line-height: 1.4;
            color: #000;
            max-width: 100%;
        }}
        h1 {{
            font-size: 18pt;
            font-weight: bold;
            margin-top: 0.5in;
            margin-bottom: 0.3in;
            page-break-after: avoid;
        }}
        h2 {{
            font-size: 16pt;
            font-weight: bold;
            margin-top: 0.4in;
            margin-bottom: 0.2in;
            page-break-after: avoid;
        }}
        h3 {{
            font-size: 14pt;
            font-weight: bold;
            margin-top: 0.3in;
            margin-bottom: 0.15in;
            page-break-after: avoid;
        }}
        p {{
            margin-bottom: 0.1in;
            text-align: justify;
        }}
        ul, ol {{
            margin-left: 0.3in;
            margin-bottom: 0.1in;
        }}
        li {{
            margin-bottom: 0.05in;
        }}
        code {{
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            background-color: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        pre {{
            background-color: #f5f5f5;
            padding: 0.2in;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 9pt;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ccc;
            margin: 0.3in 0;
        }}
        strong {{
            font-weight: bold;
        }}
        em {{
            font-style: italic;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 0.2in 0;
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 0.1in;
            text-align: left;
        }}
        th {{
            background-color: #f0f0f0;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>"""

    # Generate PDF
    HTML(string=full_html).write_pdf(str(output_path))
    print(f"✅ WeasyPrint PDF generated: {output_path}")


if __name__ == "__main__":
    # Input markdown file
    md_file = Path("_temp_pdf_samples/session_recap_2026-01-12.md")
    output_path = Path("_temp_pdf_samples/session_recap_weasyprint.pdf")

    generate_pdf_weasyprint(md_file, output_path)
