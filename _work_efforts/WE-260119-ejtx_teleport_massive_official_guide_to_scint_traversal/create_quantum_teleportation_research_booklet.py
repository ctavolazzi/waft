#!/usr/bin/env python3
"""
Create Quantum Teleportation Research Booklet

Collates the 7 arxiv PDFs on quantum teleportation into a single booklet
that represents the foundational research that inspired Teleport Massive's
2026 founding vision.
"""

import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

# PDF files in root directory with metadata
PDFS = [
    {
        "path": project_root / "0302114v1.pdf",
        "title": "Quantum Teleportation Protocol (2003)",
        "description": "Early quantum teleportation protocol research",
    },
    {
        "path": project_root / "2502.10253v2.pdf",
        "title": "Quantum Teleportation Research (2025)",
        "description": "Recent quantum teleportation advances",
    },
    {
        "path": project_root / "2503.10761v1.pdf",
        "title": "Quantum Teleportation Between Simulated Binary Black Holes",
        "description": "Quantum teleportation in black hole simulations - demonstrates teleportation in condensed matter systems",
    },
    {
        "path": project_root / "2404.10738v4.pdf",
        "title": "Quantum Teleportation Coexisting with Classical Communications",
        "description": "Quantum teleportation over fibers carrying conventional telecommunications traffic - 30.2 km demonstration",
    },
    {
        "path": project_root / "2508.14691v2.pdf",
        "title": "Quantum Teleportation Over Thermal Microwave Network",
        "description": "Microwave quantum teleportation between distant dilution refrigerators - demonstrates thermal channel resilience",
    },
    {
        "path": project_root / "2406.05182v1.pdf",
        "title": "Quantum Teleportation Research (2024)",
        "description": "Quantum teleportation research advances",
    },
    {
        "path": project_root / "2302.08756v1.pdf",
        "title": "Deterministic Quantum Teleportation Between Distant Superconducting Chips",
        "description": "64-meter quantum teleportation between superconducting chips - demonstrates scaling to larger systems",
    },
]


def create_booklet():
    """Create the quantum teleportation research booklet by merging PDFs."""
    output_dir = Path(__file__).parent
    output_path = output_dir / "QUANTUM_TELEPORTATION_RESEARCH_FOUNDATION_2026.pdf"

    print("Creating Quantum Teleportation Research Booklet...")
    print(f"Output: {output_path}\n")

    writer = PdfWriter()

    # Add all PDFs
    for pdf_info in PDFS:
        pdf_path = pdf_info["path"]
        if pdf_path.exists():
            try:
                reader = PdfReader(str(pdf_path))
                print(f"  ✅ Adding: {pdf_info['title']} ({len(reader.pages)} pages)")

                # Add all pages from this PDF
                for page in reader.pages:
                    writer.add_page(page)
            except Exception as e:
                print(f"  ❌ Error adding {pdf_path.name}: {e}")
        else:
            print(f"  ⚠️  Missing: {pdf_path}")

    # Write the merged PDF
    print("\nWriting merged booklet...")
    with open(output_path, "wb") as output_file:
        writer.write(output_file)

    print(f"\n✅ Booklet created: {output_path}")
    print(f"   Total pages: {len(writer.pages)}")
    return output_path


if __name__ == "__main__":
    create_booklet()
