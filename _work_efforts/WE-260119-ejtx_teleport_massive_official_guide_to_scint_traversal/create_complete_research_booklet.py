#!/usr/bin/env python3
"""
Create Complete Quantum Teleportation Research Booklet

Combines:
1. Mission Statement (front)
2. Research Abstract (2 pages)
3. All research PDFs
"""

import subprocess
from pathlib import Path

from pypdf import PdfReader, PdfWriter

# Add project root to path
project_root = Path(__file__).parent.parent.parent
work_effort_dir = Path(__file__).parent

# Paths
cover_typ = work_effort_dir / "BOOKLET_COVER_2026.typ"
cover_pdf = work_effort_dir / "BOOKLET_COVER_2026.pdf"
mission_statement_typ = work_effort_dir / "TELEPORT_MASSIVE_MISSION_STATEMENT_2026.typ"
mission_statement_pdf = work_effort_dir / "TELEPORT_MASSIVE_MISSION_STATEMENT_2026.pdf"
abstract_typ = work_effort_dir / "RESEARCH_ABSTRACT_2026.typ"
abstract_pdf = work_effort_dir / "RESEARCH_ABSTRACT_2026.pdf"
output_pdf = work_effort_dir / "QUANTUM_TELEPORTATION_RESEARCH_FOUNDATION_COMPLETE_2026.pdf"

# Research PDFs in root directory
RESEARCH_PDFS = [
    project_root / "0302114v1.pdf",
    project_root / "2502.10253v2.pdf",
    project_root / "2503.10761v1.pdf",
    project_root / "2404.10738v4.pdf",
    project_root / "2508.14691v2.pdf",
    project_root / "2406.05182v1.pdf",
    project_root / "2302.08756v1.pdf",
]


def compile_typst(typ_path: Path, pdf_path: Path) -> bool:
    """Compile a Typst file to PDF."""
    try:
        subprocess.run(
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


def create_complete_booklet():
    """Create the complete research booklet."""
    print("Creating Complete Quantum Teleportation Research Booklet...")
    print(f"Output: {output_pdf}\n")

    writer = PdfWriter()

    # 0. Compile and add Cover Page
    print("0. Compiling Cover Page...")
    if cover_typ.exists():
        if compile_typst(cover_typ, cover_pdf):
            if cover_pdf.exists():
                reader = PdfReader(str(cover_pdf))
                print(f"   ✅ Added Cover Page ({len(reader.pages)} pages)")
                for page in reader.pages:
                    writer.add_page(page)
            else:
                print("   ⚠️  Cover PDF not created")
        else:
            print("   ⚠️  Failed to compile Cover")
    else:
        print("   ⚠️  Cover Typst file not found")

    # 1. Compile and add Mission Statement
    print("1. Compiling Mission Statement...")
    if mission_statement_typ.exists():
        if compile_typst(mission_statement_typ, mission_statement_pdf):
            if mission_statement_pdf.exists():
                reader = PdfReader(str(mission_statement_pdf))
                print(f"   ✅ Added Mission Statement ({len(reader.pages)} pages)")
                for page in reader.pages:
                    writer.add_page(page)
            else:
                print("   ⚠️  Mission Statement PDF not created")
        else:
            print("   ⚠️  Failed to compile Mission Statement")
    else:
        print("   ⚠️  Mission Statement Typst file not found")

    # 2. Compile and add Abstract
    print("\n2. Compiling Research Abstract...")
    if abstract_typ.exists():
        if compile_typst(abstract_typ, abstract_pdf):
            if abstract_pdf.exists():
                reader = PdfReader(str(abstract_pdf))
                print(f"   ✅ Added Research Abstract ({len(reader.pages)} pages)")
                for page in reader.pages:
                    writer.add_page(page)
            else:
                print("   ⚠️  Abstract PDF not created")
        else:
            print("   ⚠️  Failed to compile Abstract")
    else:
        print("   ⚠️  Abstract Typst file not found")

    # 3. Add all research PDFs
    print("\n3. Adding Research Papers...")
    for pdf_path in RESEARCH_PDFS:
        if pdf_path.exists():
            try:
                reader = PdfReader(str(pdf_path))
                print(f"   ✅ Added: {pdf_path.name} ({len(reader.pages)} pages)")
                for page in reader.pages:
                    writer.add_page(page)
            except Exception as e:
                print(f"   ❌ Error adding {pdf_path.name}: {e}")
        else:
            print(f"   ⚠️  Missing: {pdf_path.name}")

    # Write the merged PDF
    print("\n4. Writing complete booklet...")
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

    print(f"\n✅ Complete booklet created: {output_pdf}")
    print(f"   Total pages: {len(writer.pages)}")
    return output_pdf


if __name__ == "__main__":
    create_complete_booklet()
