"""
PDF Generator using ReportLab
Converts markdown file to PDF using ReportLab's Platypus framework.
"""

from pathlib import Path

import markdown
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def markdown_to_reportlab_elements(md_text: str, styles):
    """Convert markdown text to ReportLab flowables."""
    elements = []

    # Convert markdown to HTML first
    markdown.markdown(md_text, extensions=["fenced_code", "tables", "nl2br", "extra"])

    # Parse HTML and convert to ReportLab elements
    lines = md_text.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            elements.append(Spacer(1, 0.1 * inch))
            continue

        # Headers
        if line.startswith("# "):
            elements.append(Spacer(1, 0.2 * inch))
            elements.append(Paragraph(line[2:], styles["Heading1"]))
            elements.append(Spacer(1, 0.1 * inch))
        elif line.startswith("## "):
            elements.append(Spacer(1, 0.15 * inch))
            elements.append(Paragraph(line[3:], styles["Heading2"]))
            elements.append(Spacer(1, 0.08 * inch))
        elif line.startswith("### "):
            elements.append(Spacer(1, 0.1 * inch))
            elements.append(Paragraph(line[4:], styles["Heading3"]))
            elements.append(Spacer(1, 0.05 * inch))
        elif line.startswith("---"):
            elements.append(Spacer(1, 0.2 * inch))
        # Bold text
        elif "**" in line:
            # Simple bold handling
            text = line
            text = text.replace("**", "<b>", 1).replace("**", "</b>", 1)
            elements.append(Paragraph(text, styles["BodyText"]))
            elements.append(Spacer(1, 0.05 * inch))
        # Lists
        elif line.startswith("- ") or line.startswith("* "):
            text = "• " + line[2:]
            elements.append(Paragraph(text, styles["BodyText"]))
            elements.append(Spacer(1, 0.03 * inch))
        else:
            # Regular paragraph
            elements.append(Paragraph(line, styles["BodyText"]))
            elements.append(Spacer(1, 0.05 * inch))

    return elements


def generate_pdf_reportlab(md_file: Path, output_path: Path):
    """Generate PDF from markdown using ReportLab."""

    # Read markdown file
    md_content = md_file.read_text()

    # Create PDF document
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
    )

    # Get styles
    styles = getSampleStyleSheet()

    # Customize styles
    styles["Heading1"].fontSize = 18
    styles["Heading1"].spaceAfter = 12
    styles["Heading2"].fontSize = 16
    styles["Heading2"].spaceAfter = 10
    styles["Heading3"].fontSize = 14
    styles["Heading3"].spaceAfter = 8
    styles["BodyText"].fontSize = 11
    styles["BodyText"].leading = 14
    styles["BodyText"].spaceAfter = 6

    # Convert markdown to flowables
    story = []

    # Parse markdown line by line
    lines = md_content.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line:
            story.append(Spacer(1, 0.1 * inch))
            i += 1
            continue

        # Headers
        if line.startswith("# "):
            story.append(Spacer(1, 0.2 * inch))
            text = line[2:].strip()
            # Handle bold in headers
            text = text.replace("**", "<b>", 1).replace("**", "</b>", 1) if "**" in text else text
            story.append(Paragraph(text, styles["Heading1"]))
            story.append(Spacer(1, 0.1 * inch))
        elif line.startswith("## "):
            story.append(Spacer(1, 0.15 * inch))
            text = line[3:].strip()
            text = text.replace("**", "<b>", 1).replace("**", "</b>", 1) if "**" in text else text
            story.append(Paragraph(text, styles["Heading2"]))
            story.append(Spacer(1, 0.08 * inch))
        elif line.startswith("### "):
            story.append(Spacer(1, 0.1 * inch))
            text = line[4:].strip()
            text = text.replace("**", "<b>", 1).replace("**", "</b>", 1) if "**" in text else text
            story.append(Paragraph(text, styles["Heading3"]))
            story.append(Spacer(1, 0.05 * inch))
        elif line.startswith("---"):
            story.append(Spacer(1, 0.2 * inch))
        # Lists
        elif line.startswith("- ") or line.startswith("* "):
            text = "• " + line[2:].strip()
            # Handle bold in lists
            text = text.replace("**", "<b>", 1).replace("**", "</b>", 1) if "**" in text else text
            story.append(Paragraph(text, styles["BodyText"]))
            story.append(Spacer(1, 0.03 * inch))
        else:
            # Regular paragraph - handle bold
            text = line
            # Simple bold replacement (handles **text**)
            while "**" in text:
                text = text.replace("**", "<b>", 1).replace("**", "</b>", 1)
            story.append(Paragraph(text, styles["BodyText"]))
            story.append(Spacer(1, 0.05 * inch))

        i += 1

    # Build PDF
    doc.build(story)
    print(f"✅ ReportLab PDF generated: {output_path}")


if __name__ == "__main__":
    # Input markdown file
    md_file = Path("_temp_pdf_samples/session_recap_2026-01-12.md")
    output_path = Path("_temp_pdf_samples/session_recap_reportlab.pdf")

    generate_pdf_reportlab(md_file, output_path)
