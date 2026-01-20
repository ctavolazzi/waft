#!/usr/bin/env python3
"""
Generate PDF from Encapsulated Environments research document.

Usage:
    python examples/generate_encapsulated_environments_pdf.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.evolution.pdf_generator import PDFGenerator


def main():
    project_root = Path(__file__).parent.parent
    research_file = project_root / "_pyrite" / "research" / "encapsulated-environments-research.md"

    if not research_file.exists():
        print(f"❌ Research file not found: {research_file}")
        return 1

    content = research_file.read_text()
    output_path = project_root / "encapsulated_environments_research.pdf"

    print("📄 Generating PDF from research document...")
    print("   Loading content...")

    generator = PDFGenerator.from_content(
        content=content,
        title="Encapsulated Environments: Beings Telling Stories for Information Exchange",
        style="clinical_standard",
    )

    print("   Generating PDF...")
    pdf_path = generator.save(output_path=output_path, open_pdf=True, convert_to_png=False)

    print(f"✅ PDF generated: {pdf_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
