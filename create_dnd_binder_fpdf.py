#!/usr/bin/env python3
"""
Create WAFT D&D Binder PDF using FPDF2

FPDF2 is a pure Python PDF library - lightweight and simple.
More manual positioning required, but no external dependencies.
"""

import re
from datetime import datetime
from html import unescape
from pathlib import Path

import markdown

try:
    from fpdf import FPDF
except ImportError:
    print("❌ Error: fpdf2 not installed. Install with: pip install fpdf2")
    exit(1)


class BinderPDF(FPDF):
    """Custom PDF class for WAFT D&D Binder."""

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=0.75)
        self.set_margins(0.75, 0.75, 0.75)  # left, top, right in inches

    def header(self):
        """Header for regular pages."""
        if self.page == 1:
            return  # Skip header on cover page

        self.set_font("Helvetica", "", 9)
        self.set_text_color(127, 127, 127)
        self.cell(0, 10, "WAFT D&D Binder", 0, 0, "C")
        self.ln(10)

    def footer(self):
        """Footer with page numbers."""
        if self.page == 1:
            return  # Skip footer on cover page

        self.set_y(-0.5)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(127, 127, 127)
        self.cell(0, 10, f"Page {self.page}", 0, 0, "C")

    def cover_page(self):
        """Create cover page."""
        self.add_page()
        self.set_y(2)

        # Title
        self.set_font("Helvetica", "", 48)
        self.set_text_color(26, 26, 26)
        self.cell(0, 20, "WAFT", 0, 1, "C")

        # Subtitle
        self.set_font("Helvetica", "I", 24)
        self.set_text_color(102, 102, 102)
        self.cell(0, 15, "D&D Binder", 0, 1, "C")

        self.ln(20)

        # Version
        self.set_font("Helvetica", "", 14)
        self.set_text_color(136, 136, 136)
        self.cell(0, 10, "Complete Reference Guide", 0, 1, "C")

        self.ln(40)
        self.cell(0, 10, "Version 1.0 | 2026-01-12", 0, 1, "C")

    def add_section_divider(self, title, subtitle=""):
        """Add section divider page."""
        self.add_page()
        self.set_y(1)

        self.set_font("Helvetica", "", 36)
        self.set_text_color(44, 62, 80)
        self.cell(0, 20, title, 0, 1, "C")

        if subtitle:
            self.set_font("Helvetica", "I", 16)
            self.set_text_color(127, 140, 141)
            self.cell(0, 15, subtitle, 0, 1, "C")

        self.ln(20)

    def add_heading1(self, text):
        """Add H1 heading."""
        self.ln(10)
        self.set_font("Helvetica", "", 32)
        self.set_text_color(26, 26, 26)
        self.cell(0, 15, text, 0, 1, "L")
        self.ln(5)

    def add_heading2(self, text):
        """Add H2 heading."""
        self.ln(8)
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(44, 62, 80)
        self.cell(0, 12, text, 0, 1, "L")

        # Underline
        y = self.get_y()
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.ln(5)

    def add_heading3(self, text):
        """Add H3 heading."""
        self.ln(6)
        self.set_font("Helvetica", "B", 17)
        self.set_text_color(52, 73, 94)
        self.cell(0, 10, text, 0, 1, "L")
        self.ln(3)

    def add_paragraph(self, text, justify=True):
        """Add paragraph text."""
        self.set_font("Times", "", 11)
        self.set_text_color(44, 44, 44)

        if justify:
            self.set_xy(self.l_margin, self.get_y())
            self.multi_cell(0, 6, text, 0, "J")
        else:
            self.multi_cell(0, 6, text, 0, "L")

        self.ln(3)

    def add_table(self, headers, rows, col_widths=None):
        """Add a simple table."""
        if col_widths is None:
            col_widths = [self.w / len(headers) - 2 * self.l_margin] * len(headers)

        # Header
        self.set_font("Helvetica", "B", 10)
        self.set_fill_color(52, 73, 94)
        self.set_text_color(255, 255, 255)

        x = self.get_x()
        y = self.get_y()

        for i, header in enumerate(headers):
            self.set_xy(x + sum(col_widths[:i]), y)
            self.cell(col_widths[i], 10, str(header), 1, 0, "L", True)

        self.ln(10)

        # Rows
        self.set_font("Times", "", 9)
        self.set_text_color(44, 44, 44)
        fill = False

        for row in rows:
            x = self.l_margin
            y = self.get_y()

            if fill:
                self.set_fill_color(248, 249, 250)
            else:
                self.set_fill_color(255, 255, 255)

            for i, cell in enumerate(row):
                self.set_xy(x + sum(col_widths[:i]), y)
                self.cell(col_widths[i], 8, str(cell), 1, 0, "L", fill)

            fill = not fill
            self.ln(8)

        self.ln(5)


def sanitize_for_fpdf(text):
    """Replace Unicode characters with ASCII equivalents for FPDF2."""
    replacements = {
        "☯": "(Karma)",
        "✨": "(Scint)",
        "≥": ">=",
        "≤": "<=",
        "—": "--",
        "–": "-",
        '"': '"',
        """: "'",
        """: "'",
        "…": "...",
    }
    for unicode_char, ascii_char in replacements.items():
        text = text.replace(unicode_char, ascii_char)
    # Remove any remaining non-ASCII characters
    return text.encode("ascii", "ignore").decode("ascii")


def parse_markdown_to_fpdf(pdf, markdown_content):
    """Parse markdown and add to PDF."""
    # Convert markdown to HTML first
    html = markdown.markdown(
        markdown_content, extensions=["fenced_code", "tables", "nl2br", "extra", "codehilite"]
    )
    html = unescape(html)
    # Sanitize Unicode for FPDF2
    html = sanitize_for_fpdf(html)

    # Simple parsing
    lines = html.split("\n")
    current_paragraph = []

    for line in lines:
        line = line.strip()
        if not line:
            if current_paragraph:
                text = " ".join(current_paragraph)
                text = re.sub(r"<[^>]+>", "", text)  # Remove HTML tags
                if text:
                    pdf.add_paragraph(text)
                current_paragraph = []
            continue

        # Handle headers
        if line.startswith("<h1>"):
            if current_paragraph:
                text = " ".join(current_paragraph)
                text = re.sub(r"<[^>]+>", "", text)
                if text:
                    pdf.add_paragraph(text)
                current_paragraph = []
            text = re.sub(r"<[^>]+>", "", line)
            pdf.add_heading1(text)
        elif line.startswith("<h2>"):
            if current_paragraph:
                text = " ".join(current_paragraph)
                text = re.sub(r"<[^>]+>", "", text)
                if text:
                    pdf.add_paragraph(text)
                current_paragraph = []
            text = re.sub(r"<[^>]+>", "", line)
            pdf.add_heading2(text)
        elif line.startswith("<h3>"):
            if current_paragraph:
                text = " ".join(current_paragraph)
                text = re.sub(r"<[^>]+>", "", text)
                if text:
                    pdf.add_paragraph(text)
                current_paragraph = []
            text = re.sub(r"<[^>]+>", "", line)
            pdf.add_heading3(text)
        elif line.startswith("<p>"):
            text = re.sub(r"<[^>]+>", "", line)
            text = text.strip()
            if text:
                current_paragraph.append(text)
        else:
            text = re.sub(r"<[^>]+>", "", line)
            text = text.strip()
            if text:
                current_paragraph.append(text)

    # Add remaining paragraph
    if current_paragraph:
        text = " ".join(current_paragraph)
        text = re.sub(r"<[^>]+>", "", text)
        if text:
            pdf.add_paragraph(text)


def main():
    """Generate WAFT D&D Binder PDF using FPDF2."""

    # Read game rules
    rules_file = Path("WAFT_GAME_RULES.md")
    if not rules_file.exists():
        print(f"❌ Error: {rules_file} not found")
        return

    markdown_content = rules_file.read_text()

    # Get desktop path
    desktop_path = Path.home() / "Desktop"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = desktop_path / f"WAFT_DnD_Binder_FPDF_{timestamp}.pdf"

    print("📚 Creating WAFT D&D Binder with FPDF2...")
    print("   ✨ Pure Python PDF generation")
    print("   📑 Lightweight and simple")
    print("   📊 Manual layout control")

    # Create PDF
    pdf = BinderPDF()

    # Cover page
    pdf.cover_page()

    # Table of contents
    pdf.add_page()
    pdf.add_heading1("Table of Contents")
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(52, 73, 94)
    pdf.cell(0, 10, "Part I: Game Rules", 0, 1, "L")
    pdf.ln(2)

    pdf.set_font("Times", "", 11)
    pdf.set_text_color(44, 62, 80)
    toc_items = [
        "Introduction & Quick Start",
        "Character Creation",
        "D&D 5e Mechanics",
        "Spell System",
        "Quest System",
        "Karma System",
        "Scint Economy",
        "Game Flow",
    ]
    for item in toc_items:
        pdf.set_x(pdf.l_margin + 20)
        pdf.cell(0, 8, f"- {item}", 0, 1, "L")

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Part II: Character Sheet", 0, 1, "L")
    pdf.ln(2)
    pdf.set_font("Times", "", 11)
    pdf.set_x(pdf.l_margin + 20)
    pdf.cell(0, 8, "- Fillable Character Sheet", 0, 1, "L")

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Part III: Quest Tracking", 0, 1, "L")
    pdf.ln(2)
    pdf.set_font("Times", "", 11)
    pdf.set_x(pdf.l_margin + 20)
    pdf.cell(0, 8, "- Quest Sheet Template", 0, 1, "L")

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Part IV: Quick Reference", 0, 1, "L")
    pdf.ln(2)
    pdf.set_font("Times", "", 11)
    ref_items = [
        "Ability Scores Reference",
        "Spell Slots Reference",
        "Karma Types & Evolution Paths",
        "Scint Sources & Costs",
        "Quest Types & Encounter Types",
        "Difficulty Levels & Rewards",
    ]
    for item in ref_items:
        pdf.set_x(pdf.l_margin + 20)
        pdf.cell(0, 8, f"- {item}", 0, 1, "L")

    # Part I: Game Rules
    pdf.add_section_divider("Part I: Game Rules", "The Complete WAFT Game Rules")
    parse_markdown_to_fpdf(pdf, markdown_content)

    # Part II: Character Sheet
    pdf.add_section_divider("Part II: Character Sheet", "Fillable Character Sheet")
    pdf.add_heading2("Character Information")

    pdf.add_table(
        ["Character Name", "Scientific Name"],
        [["", ""], ["Being ID", "Level"], ["", ""]],
        col_widths=[3 * 72, 3 * 72],  # 3 inches each
    )

    pdf.add_heading3("Ability Scores")
    pdf.add_table(
        ["STR", "DEX", "CON", "INT", "WIS", "CHA"],
        [["10", "12", "14", "16", "14", "12"], ["+0", "+1", "+2", "+3", "+2", "+1"]],
        col_widths=[72] * 6,  # 1 inch each
    )

    # Part III: Quest Sheet
    pdf.add_section_divider("Part III: Quest Tracking", "Quest Sheet Template")
    pdf.add_heading2("Quest Information")

    pdf.add_table(
        ["Quest Name", "Quest Type"],
        [["", ""], ["Quest ID / Cycle", "Date Started"], ["", ""]],
        col_widths=[3 * 72, 3 * 72],
    )

    # Part IV: Quick Reference
    pdf.add_section_divider("Part IV: Quick Reference", "Essential Reference Tables")
    pdf.add_heading2("Ability Scores Quick Reference")

    pdf.add_table(
        ["Ability", "Base Score", "Modifier", "Use Case"],
        [
            ["Strength (STR)", "8-15", "-1 to +2", "Physical tasks"],
            ["Dexterity (DEX)", "10-16", "0 to +3", "AC, initiative"],
            ["Constitution (CON)", "12-16", "+1 to +3", "HP, saving throws"],
            ["Intelligence (INT)", "14-18", "+2 to +4", "Spellcasting, logic"],
            ["Wisdom (WIS)", "12-16", "+1 to +3", "Perception, insight"],
            ["Charisma (CHA)", "10-14", "0 to +2", "Social interactions"],
        ],
        col_widths=[1.5 * 72, 72, 72, 2.5 * 72],
    )

    # Save PDF
    pdf.output(str(output_path))

    # Open the PDF
    import platform
    import subprocess

    system = platform.system()
    if system == "Darwin":  # macOS
        subprocess.run(["open", str(output_path)], check=False)
    elif system == "Windows":
        subprocess.run(["start", str(output_path)], shell=True, check=False)
    else:  # Linux
        subprocess.run(["xdg-open", str(output_path)], check=False)

    print(f"✅ D&D Binder created: {output_path}")
    print("📖 Opening FPDF2 version on desktop...")
    print("   📚 Generated with FPDF2 (pure Python)")

    return output_path


if __name__ == "__main__":
    main()
