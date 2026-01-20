#!/usr/bin/env python3
"""
Create Teleport Massive Case File

Assembles all founding journey documents into a single comprehensive case file PDF:
1. Founding Letter (using letterloom)
2. Cover Page
3. Mission Statement
4. Research Abstract
5. Complete Research Booklet
6. Founding Team Document
"""

import subprocess
from pathlib import Path

from pypdf import PdfReader, PdfWriter

# Add project root to path
project_root = Path(__file__).parent.parent.parent
work_effort_dir = Path(__file__).parent

# Paths
founding_letter_typ = work_effort_dir / "TELEPORT_MASSIVE_FOUNDING_LETTER_2026.typ"
founding_letter_pdf = work_effort_dir / "TELEPORT_MASSIVE_FOUNDING_LETTER_2026.pdf"
invoice_001_typ = work_effort_dir / "TELEPORT_MASSIVE_INVOICE_2026-001.typ"
invoice_001_pdf = work_effort_dir / "TELEPORT_MASSIVE_INVOICE_2026-001.pdf"
invoice_002_typ = work_effort_dir / "TELEPORT_MASSIVE_INVOICE_2026-002.typ"
invoice_002_pdf = work_effort_dir / "TELEPORT_MASSIVE_INVOICE_2026-002.pdf"
cover_typ = work_effort_dir / "BOOKLET_COVER_2026.typ"
cover_pdf = work_effort_dir / "BOOKLET_COVER_2026.pdf"
mission_statement_typ = work_effort_dir / "TELEPORT_MASSIVE_MISSION_STATEMENT_2026.typ"
mission_statement_pdf = work_effort_dir / "TELEPORT_MASSIVE_MISSION_STATEMENT_2026.pdf"
abstract_typ = work_effort_dir / "RESEARCH_ABSTRACT_2026.typ"
abstract_pdf = work_effort_dir / "RESEARCH_ABSTRACT_2026.pdf"
research_booklet_pdf = (
    work_effort_dir / "QUANTUM_TELEPORTATION_RESEARCH_FOUNDATION_COMPLETE_2026.pdf"
)
founding_team_typ = work_effort_dir / "TELEPORT_MASSIVE_FOUNDING_TEAM_2026.typ"
founding_team_pdf = work_effort_dir / "TELEPORT_MASSIVE_FOUNDING_TEAM_2026.pdf"
business_cards_dir = work_effort_dir / "founding_team_business_cards"
output_pdf = work_effort_dir / "TELEPORT_MASSIVE_CASE_FILE_2026.pdf"


def compile_typst(typ_path: Path, pdf_path: Path) -> bool:
    """Compile a Typst file to PDF."""
    try:
        result = subprocess.run(
            ["typst", "compile", str(typ_path), str(pdf_path)],
            capture_output=True,
            text=True,
            check=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error compiling {typ_path.name}: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Error: typst command not found. Please install Typst.")
        return False


def create_case_file():
    """Create the complete Teleport Massive case file."""
    print("Creating Teleport Massive Case File...")
    print(f"Output: {output_pdf}\n")

    writer = PdfWriter()

    # 0. Compile and add Founding Letter
    print("0. Compiling Founding Letter...")
    if founding_letter_typ.exists():
        if compile_typst(founding_letter_typ, founding_letter_pdf):
            if founding_letter_pdf.exists():
                reader = PdfReader(str(founding_letter_pdf))
                print(f"   ✅ Added Founding Letter ({len(reader.pages)} pages)")
                for page in reader.pages:
                    writer.add_page(page)
            else:
                print("   ⚠️  Founding Letter PDF not created")
        else:
            print("   ⚠️  Failed to compile Founding Letter")
    else:
        print("   ⚠️  Founding Letter Typst file not found")

    # 0.5. Compile and add Invoices (Paper Trail)
    print("\n0.5. Compiling Invoices (Paper Trail)...")

    # Invoice 001 - Research Services
    if invoice_001_typ.exists():
        if compile_typst(invoice_001_typ, invoice_001_pdf):
            if invoice_001_pdf.exists():
                reader = PdfReader(str(invoice_001_pdf))
                print(
                    f"   ✅ Added Invoice 2026-001 - Research Services ({len(reader.pages)} pages)"
                )
                for page in reader.pages:
                    writer.add_page(page)
            else:
                print("   ⚠️  Invoice 001 PDF not created")
        else:
            print("   ⚠️  Failed to compile Invoice 001")
    else:
        print("   ⚠️  Invoice 001 Typst file not found")

    # Invoice 002 - Corporate Formation
    if invoice_002_typ.exists():
        if compile_typst(invoice_002_typ, invoice_002_pdf):
            if invoice_002_pdf.exists():
                reader = PdfReader(str(invoice_002_pdf))
                print(
                    f"   ✅ Added Invoice 2026-002 - Corporate Formation ({len(reader.pages)} pages)"
                )
                for page in reader.pages:
                    writer.add_page(page)
            else:
                print("   ⚠️  Invoice 002 PDF not created")
        else:
            print("   ⚠️  Failed to compile Invoice 002")
    else:
        print("   ⚠️  Invoice 002 Typst file not found")

    # 1. Add Complete Research Booklet (includes Cover, Mission Statement, Abstract, and Research Papers)
    print("\n4. Adding Complete Research Booklet...")
    if research_booklet_pdf.exists():
        try:
            reader = PdfReader(str(research_booklet_pdf))
            print(f"   ✅ Added Complete Research Booklet ({len(reader.pages)} pages)")
            for page in reader.pages:
                writer.add_page(page)
        except Exception as e:
            print(f"   ❌ Error adding research booklet: {e}")
    else:
        print("   ⚠️  Research booklet PDF not found")

    # 2. Compile and add Founding Team Document
    print("\n5. Compiling Founding Team Document...")
    if founding_team_typ.exists():
        if compile_typst(founding_team_typ, founding_team_pdf):
            if founding_team_pdf.exists():
                reader = PdfReader(str(founding_team_pdf))
                print(f"   ✅ Added Founding Team Document ({len(reader.pages)} pages)")
                for page in reader.pages:
                    writer.add_page(page)
            else:
                print("   ⚠️  Founding Team PDF not created")
        else:
            print("   ⚠️  Failed to compile Founding Team Document")
    else:
        print("   ⚠️  Founding Team document Typst file not found")

    # 5.5. Add Business Cards
    print("\n5.5. Adding Business Cards...")
    if business_cards_dir.exists():
        business_card_pdfs = sorted(business_cards_dir.glob("*.pdf"))
        if business_card_pdfs:
            print(f"   Found {len(business_card_pdfs)} business card PDFs")
            for card_pdf in business_card_pdfs:
                try:
                    reader = PdfReader(str(card_pdf))
                    # Business cards are typically 1 page, but we'll handle multiple
                    for page in reader.pages:
                        writer.add_page(page)
                    print(f"   ✅ Added: {card_pdf.name} ({len(reader.pages)} pages)")
                except Exception as e:
                    print(f"   ❌ Error adding {card_pdf.name}: {e}")
        else:
            print("   ⚠️  No business card PDFs found. Run compile_business_cards.py first.")
    else:
        print("   ⚠️  Business cards directory not found")

    # Write the merged PDF
    print("\n4. Writing complete case file...")
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

    print(f"\n✅ Case file created: {output_pdf}")
    print(f"   Total pages: {len(writer.pages)}")
    return output_pdf


if __name__ == "__main__":
    create_case_file()
