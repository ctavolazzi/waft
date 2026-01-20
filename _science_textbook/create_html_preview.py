#!/usr/bin/env python3
"""
Create an HTML/PDF preview of the LaTeX textbook using WeasyPrint.
This extracts the content and creates a formatted PDF without needing LaTeX.
"""

import re
from pathlib import Path

from weasyprint import HTML


def extract_latex_content(tex_file: Path) -> dict:
    """Extract content from LaTeX file."""
    content = tex_file.read_text(encoding="utf-8")

    # Extract metadata
    title_match = re.search(r"\\title\{([^}]+)\}", content)
    title = title_match.group(1) if title_match else "Hypothesis Testing Framework"

    subtitle_match = re.search(r"\\newcommand\{\\booksubtitle\}\{([^}]+)\}", content)
    subtitle = subtitle_match.group(1) if subtitle_match else ""

    author_match = re.search(r"\\author\{([^}]+)\}", content)
    author = author_match.group(1) if author_match else "WAFT Research Team"

    # Extract chapters and sections
    chapters = []
    current_chapter = None
    current_section = None

    in_document = False
    lines = content.split("\n")

    for line in lines:
        if "\\begin{document}" in line:
            in_document = True
            continue
        if "\\end{document}" in line:
            break
        if not in_document:
            continue

        # Extract chapter
        chapter_match = re.search(r"\\chapter\{([^}]+)\}", line)
        if chapter_match:
            if current_chapter:
                chapters.append(current_chapter)
            current_chapter = {"title": chapter_match.group(1), "sections": []}
            continue

        # Extract section
        section_match = re.search(r"\\section\{([^}]+)\}", line)
        if section_match:
            if current_section:
                current_chapter["sections"].append(current_section)
            current_section = {"title": section_match.group(1), "content": []}
            continue

        # Extract subsection
        subsection_match = re.search(r"\\subsection\{([^}]+)\}", line)
        if subsection_match:
            if current_section:
                current_section["content"].append(
                    {"type": "subsection", "title": subsection_match.group(1), "text": ""}
                )
            continue

        # Extract text content (simplified - remove LaTeX commands)
        if current_section and line.strip() and not line.strip().startswith("\\"):
            # Clean LaTeX commands
            clean_line = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", line)
            clean_line = re.sub(r"\\[a-zA-Z]+", "", clean_line)
            clean_line = clean_line.strip()
            if clean_line and len(clean_line) > 10:  # Skip very short lines
                if (
                    current_section["content"]
                    and isinstance(current_section["content"][-1], dict)
                    and current_section["content"][-1].get("type") == "subsection"
                ):
                    current_section["content"][-1]["text"] += " " + clean_line
                else:
                    current_section["content"].append({"type": "paragraph", "text": clean_line})

    if current_section:
        current_chapter["sections"].append(current_section)
    if current_chapter:
        chapters.append(current_chapter)

    return {"title": title, "subtitle": subtitle, "author": author, "chapters": chapters}


def create_html(extracted: dict) -> str:
    """Create HTML from extracted content."""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{extracted["title"]}</title>
    <style>
        @page {{
            size: 6.375in 9.25in;
            margin: 0.8125in 0.5in 0.9375in 0.5in;
        }}
        body {{
            font-family: 'Times New Roman', Times, serif;
            font-size: 11pt;
            line-height: 1.4;
            color: #000;
        }}
        .title-page {{
            text-align: center;
            page-break-after: always;
            padding-top: 2in;
        }}
        .title-page h1 {{
            font-size: 48pt;
            font-weight: bold;
            margin-bottom: 0.5in;
        }}
        .title-page .subtitle {{
            font-size: 14pt;
            font-style: italic;
            margin-bottom: 1in;
        }}
        .title-page .author {{
            font-size: 14pt;
            margin-top: 2in;
        }}
        h1 {{
            font-size: 24pt;
            font-weight: bold;
            margin-top: 1in;
            margin-bottom: 0.5in;
            page-break-before: always;
        }}
        h2 {{
            font-size: 18pt;
            font-weight: bold;
            margin-top: 0.75in;
            margin-bottom: 0.25in;
        }}
        h3 {{
            font-size: 14pt;
            font-weight: bold;
            margin-top: 0.5in;
            margin-bottom: 0.25in;
        }}
        p {{
            margin-bottom: 0.5em;
            text-align: justify;
        }}
        ul, ol {{
            margin-left: 1.5em;
            margin-bottom: 0.5em;
        }}
        li {{
            margin-bottom: 0.25em;
        }}
        code {{
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            background-color: #f5f5f5;
            padding: 2px 4px;
        }}
        pre {{
            background-color: #f5f5f5;
            padding: 1em;
            border: 1px solid #ccc;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
    <div class="title-page">
        <h1>{extracted["title"]}</h1>
        <div class="subtitle">{extracted["subtitle"]}</div>
        <div class="author">{extracted["author"]}</div>
        <div class="author">2026</div>
    </div>
"""

    for chapter in extracted["chapters"]:
        html += f"    <h1>{chapter['title']}</h1>\n"

        for section in chapter["sections"]:
            html += f"    <h2>{section['title']}</h2>\n"

            for item in section["content"]:
                if item["type"] == "subsection":
                    html += f"    <h3>{item['title']}</h3>\n"
                    if item.get("text"):
                        html += f"    <p>{item['text']}</p>\n"
                elif item["type"] == "paragraph":
                    html += f"    <p>{item['text']}</p>\n"

    html += """</body>
</html>"""

    return html


def main():
    """Create HTML and PDF preview."""
    tex_file = Path(__file__).parent / "hypothesis-testing-framework.tex"
    html_file = Path(__file__).parent / "hypothesis-testing-framework-preview.html"
    pdf_file = Path(__file__).parent / "hypothesis-testing-framework-preview.pdf"

    print("📚 Extracting content from LaTeX file...")
    extracted = extract_latex_content(tex_file)
    print(f"   Found {len(extracted['chapters'])} chapters")

    print("📝 Creating HTML...")
    html_content = create_html(extracted)
    html_file.write_text(html_content, encoding="utf-8")
    print(f"   HTML saved: {html_file}")

    print("📄 Generating PDF with WeasyPrint...")
    HTML(string=html_content).write_pdf(pdf_file)
    print(f"   PDF saved: {pdf_file}")

    # Open PDF
    import platform
    import subprocess

    if platform.system() == "Darwin":  # macOS
        subprocess.run(["open", str(pdf_file)])
    elif platform.system() == "Windows":
        subprocess.run(["start", str(pdf_file)], shell=True)
    else:  # Linux
        subprocess.run(["xdg-open", str(pdf_file)])

    print("✅ Preview PDF generated and opened!")


if __name__ == "__main__":
    main()
