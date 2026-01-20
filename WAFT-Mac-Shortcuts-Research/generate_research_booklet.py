#!/usr/bin/env python3
"""
Generate WAFT Research Vol. 1 PDF Booklet

Converts the research content markdown into a professional PDF booklet
using the WAFT DocumentEngine.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.foundation import (
    DocumentConfig,
    DocumentEngine,
    LogBlock,
    SectionHeader,
    TextBlock,
)


def generate_research_booklet(content_path: Path, output_path: Path) -> Path:
    """
    Generate PDF booklet from research content.

    Args:
        content_path: Path to markdown content file
        output_path: Path to output PDF

    Returns:
        Path to generated PDF
    """
    # Read content
    content = content_path.read_text(encoding="utf-8")

    # Create professional config for research document
    config = DocumentConfig(
        fonts={
            "Header": ("Helvetica", "B"),
            "Body": ("Helvetica", ""),
            "Monospace": ("Courier", ""),
        },
        watermark=None,
        header_text="WAFT Research Vol. 1",
        footer_text="The Interface Accommodation",
        page_margins=(72, 72, 72, 72),  # 1 inch margins
        line_spacing=1.5,
        font_size_body=11,
        font_size_header=16,
        font_size_footer=9,
        title="WAFT Research Vol. 1: The Interface Accommodation",
        author="WAFT Core Framework",
        subject="Human-AI Symbiosis Research",
    )

    # Create engine
    engine = DocumentEngine(config)

    # Parse and add content
    lines = content.split("\n")
    i = 0
    in_code_block = False
    code_lines = []

    while i < len(lines):
        line = lines[i]

        # Code blocks
        if line.strip().startswith("```"):
            if in_code_block:
                # End of code block
                if code_lines:
                    engine.add(LogBlock(code_lines))
                code_lines = []
                in_code_block = False
            else:
                # Start of code block
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # Title page detection (lines starting with ## TITLE PAGE)
        if line.strip() == "## TITLE PAGE":
            # Skip to next section
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("##"):
                i += 1
            continue

        # Headers
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            title = line.lstrip("#").strip()

            # Skip separator lines
            if title.startswith("---") or not title:
                i += 1
                continue

            # Clean up title
            title = title.replace("*", "").strip()

            # Add header (limit to level 3 for PDF)
            engine.add(SectionHeader(title, level=min(level, 3)))
            i += 1
            continue

        # Horizontal rules
        if line.strip() == "---" or line.strip().startswith("---"):
            # Add spacing
            engine.add(TextBlock(""))
            i += 1
            continue

        # Empty lines
        if not line.strip():
            # Add small spacing
            engine.add(TextBlock(""))
            i += 1
            continue

        # Regular text (accumulate paragraph)
        paragraph_lines = []
        while i < len(lines):
            line = lines[i]

            # Stop at headers, code blocks, or horizontal rules
            if (
                not line.strip()
                or line.strip().startswith("#")
                or line.strip().startswith("```")
                or line.strip() == "---"
            ):
                break

            paragraph_lines.append(line)
            i += 1

        if paragraph_lines:
            # Clean markdown formatting
            text = "\n".join(paragraph_lines)

            # Remove markdown bold/italic
            text = text.replace("**", "").replace("*", "").replace("__", "").replace("_", "")

            # Remove markdown links [text](url) -> text
            import re

            text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)

            # Remove inline code backticks
            text = text.replace("`", "")

            if text.strip():
                engine.add(TextBlock(text, style="Body"))

    # Generate PDF
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result = engine.render(output_path)

    return result


def main():
    """Generate the research booklet PDF."""
    research_dir = Path(__file__).parent
    content_path = research_dir / "documents" / "WAFT_Research_Vol1_Content.md"
    output_path = research_dir / "WAFT_Research_Vol1_The_Interface_Accommodation.pdf"

    if not content_path.exists():
        print(f"❌ Error: Content file not found: {content_path}")
        return 1

    print("📚 Generating WAFT Research Vol. 1 PDF Booklet...")
    print(f"   Source: {content_path.name}")
    print(f"   Output: {output_path.name}\n")

    try:
        result = generate_research_booklet(content_path, output_path)
        size_kb = result.stat().st_size / 1024
        print(f"✅ Generated: {result.name}")
        print(f"   Size: {size_kb:.1f} KB")
        print(f"   Location: {result.parent}")
        return 0
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
