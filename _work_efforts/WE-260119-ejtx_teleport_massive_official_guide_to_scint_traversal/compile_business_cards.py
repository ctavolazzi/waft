#!/usr/bin/env python3
"""
Compile all business cards to PDF
"""

import subprocess
from pathlib import Path

work_effort_dir = Path(__file__).parent
business_cards_dir = work_effort_dir / "founding_team_business_cards"

# Find all Typst files
typst_files = sorted(business_cards_dir.glob("*.typ"))

print(f"Compiling {len(typst_files)} business cards...\n")

for typ_file in typst_files:
    pdf_file = typ_file.with_suffix('.pdf')
    try:
        result = subprocess.run(
            ["typst", "compile", str(typ_file), str(pdf_file)],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Compiled: {typ_file.name} → {pdf_file.name}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error compiling {typ_file.name}: {e.stderr}")
    except FileNotFoundError:
        print("❌ Error: typst command not found. Please install Typst.")
        break

print(f"\n✅ Business card compilation complete!")
