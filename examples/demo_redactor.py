#!/usr/bin/env python3
"""
PDF Redactor Demo
=================

Demonstrates the redactor tool for creating classified/mystery documents.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.redactor import quick_redact


def demo_redactor():
    """Demonstrate redactor capabilities."""
    print("=" * 80)
    print("PDF Redactor Demo")
    print("=" * 80)
    print()

    # Find a PDF to redact
    demo_pdf = Path(
        "_work_efforts/showcase_documents/WAFT_Field_Guide_Complete_Booklet_PrinterFriendly.pdf"
    )

    if not demo_pdf.exists():
        print(f"⚠️  Demo PDF not found: {demo_pdf}")
        print("   Generate a PDF first, then run this demo.")
        return

    print(f"Redacting: {demo_pdf.name}")
    print()

    # Redact some terms
    print("Redacting terms: 'WAFT', 'FIELD GUIDE', 'Framework'")
    redacted_path = quick_redact(
        demo_pdf,
        terms=["WAFT", "FIELD GUIDE", "Framework", "DocumentBuilder"],
        output_path=demo_pdf.parent / f"{demo_pdf.stem}_REDACTED.pdf",
    )

    print(f"✅ Redacted PDF saved: {redacted_path.name}")
    print()
    print("=" * 80)
    print("Redaction complete!")
    print("=" * 80)


if __name__ == "__main__":
    demo_redactor()
