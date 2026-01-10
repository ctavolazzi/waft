#!/usr/bin/env python3
"""
Generate printable PDFs from markdown documentation files.

Uses the Waft DocumentEngine to create professional PDFs with proper formatting.
"""

import re
from pathlib import Path
from typing import List, Tuple
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.foundation import (
    DocumentEngine,
    DocumentConfig,
    SectionHeader,
    TextBlock,
    KeyValueBlock,
    LogBlock,
)


class MarkdownToPDFConverter:
    """Converts markdown files to PDFs using DocumentEngine."""

    def __init__(self, config: DocumentConfig = None):
        """
        Initialize converter.

        Args:
            config: Optional DocumentConfig (uses default if None)
        """
        if config is None:
            # Use a clean, professional config for documentation
            config = DocumentConfig(
                fonts={
                    "Header": ("Helvetica", "B"),
                    "Body": ("Helvetica", ""),
                    "Monospace": ("Courier", ""),
                },
                watermark=None,
                header_text=None,
                footer_text="Waft Documentation",
                page_margins=(72, 72, 72, 72),  # 1 inch margins
                line_spacing=1.3,
                font_size_body=11,
                font_size_header=16,
                font_size_footer=9,
            )
        self.config = config

    def parse_markdown(self, content: str) -> List[Tuple[str, str]]:
        """
        Parse markdown content into (type, content) blocks.

        Args:
            content: Markdown text

        Returns:
            List of (block_type, block_content) tuples
        """
        blocks = []
        lines = content.split("\n")
        i = 0

        while i < len(lines):
            line = lines[i]

            # Code blocks (```)
            if line.strip().startswith("```"):
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    code_lines.append(lines[i])
                    i += 1
                blocks.append(("code", "\n".join(code_lines)))
                i += 1
                continue

            # Headers (# ## ###)
            header_match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if header_match:
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                # Remove markdown links from headers [text](url) -> text
                title = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", title)
                blocks.append(("header", f"{level}|{title}"))
                i += 1
                continue

            # Horizontal rules (--- or ***)
            if re.match(r"^(\*\*\*|---|___)[\*\-_]*$", line.strip()):
                blocks.append(("hr", ""))
                i += 1
                continue

            # Tables (starts with |)
            if line.strip().startswith("|") and "|" in line:
                table_lines = []
                while i < len(lines) and "|" in lines[i]:
                    # Skip separator rows (|---|---|)
                    if not re.match(r"^\s*\|[\s\-:|]+\|\s*$", lines[i]):
                        table_lines.append(lines[i])
                    i += 1
                if table_lines:
                    blocks.append(("table", "\n".join(table_lines)))
                continue

            # Empty lines
            if not line.strip():
                # Don't add too many empty blocks in a row
                if not blocks or blocks[-1][0] != "empty":
                    blocks.append(("empty", ""))
                i += 1
                continue

            # Regular text (accumulate paragraph)
            paragraph_lines = []
            while i < len(lines):
                line = lines[i]
                # Stop at headers, code blocks, horizontal rules, or empty lines
                if (
                    not line.strip()
                    or line.strip().startswith("#")
                    or line.strip().startswith("```")
                    or re.match(r"^(\*\*\*|---|___)[\*\-_]*$", line.strip())
                    or line.strip().startswith("|")
                ):
                    break
                paragraph_lines.append(line)
                i += 1

            if paragraph_lines:
                blocks.append(("text", "\n".join(paragraph_lines)))

        return blocks

    def clean_unicode_chars(self, text: str) -> str:
        """
        Replace Unicode characters with ASCII equivalents.

        Args:
            text: Text with Unicode characters

        Returns:
            ASCII-compatible text
        """
        # Common Unicode replacements
        replacements = {
            # Arrows
            "→": "->",
            "←": "<-",
            "↑": "^",
            "↓": "v",
            # Checkmarks and symbols
            "✅": "[x]",
            "❌": "[!]",
            "⚠️": "[!]",
            "⚠": "[!]",
            "⚲": "[symbol]",
            # Box drawing characters
            "┌": "+",
            "┐": "+",
            "└": "+",
            "┘": "+",
            "├": "+",
            "┤": "+",
            "┬": "+",
            "┴": "+",
            "┼": "+",
            "─": "-",
            "│": "|",
            "═": "=",
            "║": "|",
            "╔": "+",
            "╗": "+",
            "╚": "+",
            "╝": "+",
            "╠": "+",
            "╣": "+",
            "╦": "+",
            "╩": "+",
            "╬": "+",
            # Emojis
            "📄": "",
            "✨": "*",
            "🔧": "[tool]",
            "🐛": "[bug]",
            "⚙️": "[config]",
            "⚙": "[config]",
            "📝": "",
            "🎯": "*",
            "💡": "*",
            "🚀": "*",
            "📊": "",
            "📈": "",
            "🔍": "",
            "🌊": "~",
            "🏗": "[build]",
            "🏗️": "[build]",
            "🔥": "*",
            "💪": "*",
            "🎨": "[art]",
            "📦": "[pkg]",
            "🧹": "[clean]",
            "🧪": "[test]",
            "📚": "[docs]",
            "🎉": "*",
            "🎊": "*",
            "🌟": "*",
            "⭐": "*",
            "💫": "*",
            # Punctuation
            "…": "...",
            """: '"',
            """: '"',
            "'": "'",
            "'": "'",
            "–": "-",
            "—": "--",
            "•": "-",
            "·": "*",
        }

        for unicode_char, ascii_replacement in replacements.items():
            text = text.replace(unicode_char, ascii_replacement)

        # Final pass: remove any remaining non-ASCII characters
        # Keep only printable ASCII (32-126) plus newlines/tabs
        result = []
        for char in text:
            if ord(char) < 128 or char in ['\n', '\t']:
                result.append(char)
            else:
                # Replace remaining Unicode with empty string or space
                result.append('')

        return ''.join(result)

    def clean_markdown_formatting(self, text: str) -> str:
        """
        Remove markdown formatting from text.

        Args:
            text: Text with markdown formatting

        Returns:
            Plain text
        """
        # First clean Unicode characters
        text = self.clean_unicode_chars(text)

        # Bold/Italic (**text** or __text__ or *text* or _text_)
        text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
        text = re.sub(r"__([^_]+)__", r"\1", text)
        text = re.sub(r"\*([^*]+)\*", r"\1", text)
        text = re.sub(r"_([^_]+)_", r"\1", text)

        # Inline code (`code`)
        text = re.sub(r"`([^`]+)`", r"\1", text)

        # Links ([text](url))
        text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)

        # Remove any remaining backticks
        text = text.replace("`", "")

        return text

    def convert(self, markdown_path: Path, pdf_path: Path) -> Path:
        """
        Convert markdown file to PDF.

        Args:
            markdown_path: Path to markdown file
            pdf_path: Path to output PDF

        Returns:
            Path to generated PDF
        """
        # Read markdown
        content = markdown_path.read_text(encoding="utf-8")

        # Parse into blocks
        blocks = self.parse_markdown(content)

        # Create DocumentEngine
        engine = DocumentEngine(self.config)

        # Add title from filename if not in markdown
        has_title = any(b[0] == "header" and b[1].startswith("1|") for b in blocks)
        if not has_title:
            title = markdown_path.stem.replace("_", " ").title()
            engine.add(SectionHeader(title, level=1))

        # Convert blocks to ContentBlocks
        for block_type, block_content in blocks:
            if block_type == "header":
                level, title = block_content.split("|", 1)
                level = int(level)
                # Clean markdown formatting from title
                title = self.clean_markdown_formatting(title)
                engine.add(SectionHeader(title, level=min(level, 3)))

            elif block_type == "text":
                # Clean markdown formatting
                text = self.clean_markdown_formatting(block_content)
                if text.strip():
                    engine.add(TextBlock(text, style="Body"))

            elif block_type == "code":
                # Add code as monospace log block
                if block_content.strip():
                    code_lines = block_content.split("\n")
                    # Clean Unicode from code lines
                    code_lines = [self.clean_unicode_chars(line) for line in code_lines]
                    engine.add(LogBlock(code_lines))

            elif block_type == "table":
                # Parse table into key-value pairs or text
                # For now, just render as monospace text
                if block_content.strip():
                    table_lines = block_content.split("\n")
                    # Clean up table formatting
                    cleaned_lines = []
                    for line in table_lines:
                        # Clean Unicode characters first
                        line = self.clean_unicode_chars(line)
                        # Remove leading/trailing pipes and clean up
                        line = line.strip()
                        if line.startswith("|"):
                            line = line[1:]
                        if line.endswith("|"):
                            line = line[:-1]
                        # Replace | with spaces for readability
                        line = line.replace("|", " | ")
                        cleaned_lines.append(line)
                    engine.add(LogBlock(cleaned_lines))

            elif block_type == "empty":
                # Add small spacing
                engine.add(TextBlock(""))

        # Generate PDF
        return engine.render(pdf_path)


def main():
    """Generate PDFs for all documentation files."""
    # Define documentation files to convert
    docs = [
        ("docs/SYSTEM_OVERVIEW.md", "docs/SYSTEM_OVERVIEW.pdf"),
        ("docs/REFACTORING_CHANGELOG.md", "docs/REFACTORING_CHANGELOG.pdf"),
        ("docs/OPEN_ISSUES.md", "docs/OPEN_ISSUES.pdf"),
        ("REFACTORING_PLAN.md", "docs/REFACTORING_PLAN.pdf"),
        ("VERIFICATION_REPORT.md", "docs/VERIFICATION_REPORT.pdf"),
        ("PR_SUMMARY.md", "docs/PR_SUMMARY.pdf"),
    ]

    # Get project root
    project_root = Path(__file__).parent.parent

    # Create converter
    converter = MarkdownToPDFConverter()

    # Convert each file
    print("Generating documentation PDFs...\n")
    for md_path, pdf_path in docs:
        md_full = project_root / md_path
        pdf_full = project_root / pdf_path

        if not md_full.exists():
            print(f"⚠️  Skipping {md_path} (file not found)")
            continue

        try:
            print(f"📄 Converting {md_path}")
            result_path = converter.convert(md_full, pdf_full)
            size_kb = result_path.stat().st_size / 1024
            print(f"   ✅ Generated: {pdf_path} ({size_kb:.1f} KB)\n")
        except Exception as e:
            print(f"   ❌ Error: {e}\n")

    print("✨ PDF generation complete!")


if __name__ == "__main__":
    main()
