"""
Generate D&D Campaign PDFs
==========================

Generates all 5 campaign documents as PDFs with different styles to test
and evolve the PDF generator capabilities.

Documents:
1. Player's Guide - Premium styling
2. DM Guide - Clinical standard styling
3. Encounter Sheets - Compact layout
4. World Map - Custom styling with images
5. NPC Reference Cards - Card-based layout
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.evolution.pdf_generator import PDFGenerator


def generate_players_guide():
    """Generate Player's Guide with premium styling."""
    print("\n📄 Generating Player's Guide (Premium Style)...")
    
    content_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "campaign_players_guide.md"
    output_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "campaign_players_guide.pdf"
    
    generator = PDFGenerator.from_file(
        file_path=content_path,
        title="The Shattered Crown - Player's Guide",
        style="premium",
        output_path=output_path
    )
    
    result = generator.save(
        output_path=output_path,
        convert_to_png=True,
        png_dpi=300
    )
    
    print(f"   ✅ Generated: {result}")
    return result


def generate_dm_guide():
    """Generate DM Guide with clinical standard styling."""
    print("\n📄 Generating DM Guide (Clinical Standard Style)...")
    
    content_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "campaign_dm_guide.md"
    output_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "campaign_dm_guide.pdf"
    
    generator = PDFGenerator.from_file(
        file_path=content_path,
        title="The Shattered Crown - Dungeon Master's Guide",
        style="clinical_standard",
        output_path=output_path
    )
    
    result = generator.save(
        output_path=output_path,
        convert_to_png=True,
        png_dpi=300
    )
    
    print(f"   ✅ Generated: {result}")
    return result


def generate_encounter_sheets():
    """Generate Encounter Sheets with compact layout."""
    print("\n📄 Generating Encounter Sheets (Compact Layout)...")
    
    content_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "campaign_encounters.md"
    output_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "campaign_encounters.pdf"
    
    # Use clinical standard with smaller margins for compact layout
    generator = PDFGenerator.from_file(
        file_path=content_path,
        title="The Shattered Crown - Encounter Reference",
        style="clinical_standard",
        output_path=output_path,
        margins=(15, 15, 15, 15),  # Smaller margins for compact
        font_size=10  # Smaller font
    )
    
    result = generator.save(
        output_path=output_path,
        convert_to_png=True,
        png_dpi=300
    )
    
    print(f"   ✅ Generated: {result}")
    return result


def generate_world_map():
    """Generate World Map document with custom styling."""
    print("\n📄 Generating World Map Document (Custom Styling)...")
    
    content_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "campaign_world_map.md"
    output_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "campaign_world_map.pdf"
    
    # Use premium style for world map
    generator = PDFGenerator.from_file(
        file_path=content_path,
        title="The Shattered Crown - World Map & Locations",
        style="premium",
        output_path=output_path
    )
    
    result = generator.save(
        output_path=output_path,
        convert_to_png=True,
        png_dpi=300
    )
    
    print(f"   ✅ Generated: {result}")
    return result


def generate_npc_cards():
    """Generate NPC Reference Cards with card-based layout."""
    print("\n📄 Generating NPC Reference Cards (Card Layout)...")
    
    content_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "campaign_npcs.md"
    output_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "campaign_npcs.pdf"
    
    # Use clinical standard with compact settings for cards
    generator = PDFGenerator.from_file(
        file_path=content_path,
        title="The Shattered Crown - NPC Reference Cards",
        style="clinical_standard",
        output_path=output_path,
        margins=(20, 20, 20, 20),
        font_size=10
    )
    
    result = generator.save(
        output_path=output_path,
        convert_to_png=True,
        png_dpi=300
    )
    
    print(f"   ✅ Generated: {result}")
    return result


def main():
    """Generate all campaign PDFs."""
    print("=" * 60)
    print("D&D Campaign PDF Generation")
    print("=" * 60)
    print("\nGenerating 5 campaign documents with different styles...")
    
    results = []
    
    try:
        # Generate all PDFs
        results.append(("Player's Guide", generate_players_guide()))
        results.append(("DM Guide", generate_dm_guide()))
        results.append(("Encounter Sheets", generate_encounter_sheets()))
        results.append(("World Map", generate_world_map()))
        results.append(("NPC Cards", generate_npc_cards()))
        
        # Summary
        print("\n" + "=" * 60)
        print("✅ PDF Generation Complete!")
        print("=" * 60)
        print("\nGenerated Documents:")
        for name, path in results:
            if path and path.exists():
                size_kb = path.stat().st_size / 1024
                print(f"   📄 {name}: {path.name} ({size_kb:.1f} KB)")
        
        # Check for PNG files
        work_effort_dir = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution"
        png_files = list(work_effort_dir.glob("*.png"))
        if png_files:
            print(f"\n📸 PNG Screenshots Generated: {len(png_files)}")
            for png in png_files:
                print(f"   🖼️  {png.name}")
        
        print("\n✅ All campaign PDFs generated successfully!")
        print(f"   Location: {work_effort_dir}")
        
    except Exception as e:
        print(f"\n❌ Error generating PDFs: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
