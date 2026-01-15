"""
Generate All PDFs for Work Effort
==================================

Generates the 3 main PDFs:
1. Blank character sheet
2. Filled character sheet (example)
3. Complete work effort PDF

Opens all 3 PDFs for viewing.
"""

import sys
from pathlib import Path
import subprocess
import platform

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from generate_character_sheet import generate_blank_sheet, generate_filled_sheet
from generate_work_effort_pdf import main as generate_work_effort_pdf


def open_pdf(pdf_path: Path):
    """Open PDF in default viewer."""
    if not pdf_path.exists():
        print(f"   ⚠️  PDF not found: {pdf_path}")
        return
    
    system = platform.system()
    if system == "Darwin":  # macOS
        subprocess.run(["open", str(pdf_path)])
    elif system == "Windows":
        subprocess.run(["start", str(pdf_path)], shell=True)
    else:  # Linux
        subprocess.run(["xdg-open", str(pdf_path)])
    
    print(f"   🚀 Opened: {pdf_path.name}")


def main():
    """Generate all 3 PDFs and open them."""
    print("=" * 60)
    print("Generating All Work Effort PDFs")
    print("=" * 60)
    
    work_effort_dir = Path(__file__).parent
    
    pdfs_to_open = []
    
    # 1. Blank character sheet
    print("\n1. Generating blank character sheet...")
    blank_path = generate_blank_sheet()
    pdfs_to_open.append(blank_path)
    
    # 2. Filled character sheet (example)
    print("\n2. Generating filled character sheet (example)...")
    example_character = {
        "name": "Aldric the Brave",
        "class": "Fighter",
        "level": 3,
        "background": "Folk Hero",
        "race": "Human",
        "alignment": "Lawful Good",
        "xp": 900,
        "abilities": {
            "STR": 16,
            "DEX": 13,
            "CON": 15,
            "INT": 10,
            "WIS": 12,
            "CHA": 11
        },
        "proficiency_bonus": 2,
        "saving_throw_proficiencies": ["STR", "CON"],
        "skill_proficiencies": ["Athletics", "Perception", "Survival", "Animal Handling"],
        "ac": 16,
        "initiative": 1,
        "speed": 30,
        "max_hp": 28,
        "current_hp": 28,
        "temp_hp": 0,
        "hit_dice": "3d10",
        "attacks": [
            {
                "name": "Longsword",
                "bonus": 5,
                "damage": "1d8+3",
                "damage_type": "slashing",
                "range": "5 ft."
            }
        ],
        "equipment": [
            "Chain Mail",
            "Longsword",
            "Shield",
            "Shortbow",
            "20 Arrows"
        ],
        "coins": {"pp": 0, "gp": 15, "ep": 0, "sp": 5, "cp": 10},
        "features": ["Fighting Style: Defense", "Second Wind", "Action Surge"],
        "traits": ["Human: +1 to all ability scores"],
        "armor_proficiencies": ["All armor", "Shields"],
        "weapon_proficiencies": ["Simple weapons", "Martial weapons"],
        "tool_proficiencies": ["Smith's tools"],
        "languages": ["Common"],
        "personality_traits": [
            "I judge people by their actions, not their words.",
            "If someone is in trouble, I'm always ready to help."
        ],
        "ideals": ["Responsibility: I protect those who cannot protect themselves."],
        "bonds": ["I must protect my home village from dangers."],
        "flaws": ["I'm too trusting of others."],
        "backstory": "Aldric grew up in a small village, always ready to help those in need."
    }
    filled_path = generate_filled_sheet(example_character)
    pdfs_to_open.append(filled_path)
    
    # 3. Complete work effort PDF
    print("\n3. Generating complete work effort PDF...")
    generate_work_effort_pdf()
    complete_path = work_effort_dir / "WE-260112-jqkn_COMPLETE.pdf"
    if complete_path.exists():
        pdfs_to_open.append(complete_path)
    
    # Open all PDFs
    print("\n" + "=" * 60)
    print("Opening PDFs...")
    print("=" * 60)
    
    for pdf_path in pdfs_to_open:
        if pdf_path.exists():
            open_pdf(pdf_path)
        else:
            print(f"   ⚠️  PDF not found: {pdf_path}")
    
    print("\n✅ All PDFs generated and opened!")
    print(f"\nGenerated PDFs:")
    for pdf_path in pdfs_to_open:
        if pdf_path.exists():
            size_kb = pdf_path.stat().st_size / 1024
            print(f"   📄 {pdf_path.name} ({size_kb:.1f} KB)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
