#!/usr/bin/env python3
"""
Simple Redactor Demo
====================

Shows how to use the redactor tool to create classified/mystery documents.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.pdf_redactor import PDFRedactor


def demo_simple_redaction():
    """Simple redaction example."""
    print("=" * 80)
    print("PDF Redactor Demo - Creating Classified Document")
    print("=" * 80)
    print()

    # Use the session summary as an example
    input_pdf = Path("_work_efforts/showcase_documents/SESSION_SUMMARY_2026-01-11.pdf")

    if not input_pdf.exists():
        print(f"⚠️  PDF not found: {input_pdf}")
        print("   Generate a PDF first.")
        return

    print(f"Creating redacted version of: {input_pdf.name}")
    print()

    # Create redactor
    redactor = PDFRedactor(input_pdf)

    # Add some redaction areas (example coordinates - adjust as needed)
    # These are example positions - in real use, you'd extract text positions
    print("Adding redaction areas...")
    redactor.add_area_redaction(x=100, y=700, width=200, height=20, label="CLASSIFIED")
    redactor.add_area_redaction(x=100, y=650, width=150, height=20, label="TOP SECRET")

    # Save redacted version
    output_path = redactor.save()

    print(f"✅ Redacted PDF saved: {output_path.name}")
    print()
    print("=" * 80)
    print("Redaction complete! Check the PDF for black rectangles.")
    print("=" * 80)
    print()
    print(f"To open: open {output_path}")


if __name__ == "__main__":
    demo_simple_redaction()
