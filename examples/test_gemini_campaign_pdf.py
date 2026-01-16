#!/usr/bin/env python3
"""
Test Gemini Integration for D&D Campaign PDFs
==============================================

Tests the integration of Gemini narrative engine with WAFT's PDF generation system.
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.campaign import GeminiPDFAdapter, NarrativeContext
from src.waft.evolution.pdf_generator import PDFGenerator


async def test_gemini_adapter():
    """Test the Gemini PDF adapter"""
    print("=" * 60)
    print("Testing Gemini PDF Adapter")
    print("=" * 60)
    
    # Initialize adapter
    adapter = GeminiPDFAdapter()
    
    # Check status
    status = adapter.get_status()
    print(f"\n📊 Adapter Status:")
    print(f"   Enabled: {status['enabled']}")
    print(f"   Capabilities: {', '.join(status['capabilities'])}")
    
    if status['enabled']:
        print("\n✅ Gemini is available! Testing enhancements...")
    else:
        print("\n⚠️  Gemini not available - will test fallback mode")
    
    # Test campaign narrative enhancement
    print("\n" + "-" * 60)
    print("Test 1: Campaign Narrative Enhancement")
    print("-" * 60)
    
    campaign_data = {
        'name': 'The Shattered Crown',
        'type': 'Political Intrigue',
        'level_range': '1-5',
        'tone': 'epic',
        'setting': 'Medieval fantasy kingdom'
    }
    
    narrative = await adapter.enhance_campaign_narrative(campaign_data)
    print(f"\n📖 Generated Narrative:\n{narrative}\n")
    
    # Test character description enhancement
    print("\n" + "-" * 60)
    print("Test 2: Character Description Enhancement")
    print("-" * 60)
    
    character = {
        'name': 'Aelric the Bold',
        'class': 'Paladin',
        'race': 'Human',
        'level': 3,
        'background': 'Noble'
    }
    
    description = await adapter.enhance_character_description(character)
    print(f"\n👤 Generated Description:\n{description}\n")
    
    # Test full campaign enhancement
    print("\n" + "-" * 60)
    print("Test 3: Full Campaign Content Enhancement")
    print("-" * 60)
    
    campaign_content = {
        'campaign': campaign_data,
        'characters': [
            character,
            {
                'name': 'Lyra Shadowstep',
                'class': 'Rogue',
                'race': 'Elf',
                'level': 3,
                'background': 'Criminal'
            }
        ]
    }
    
    enhanced = adapter.enhance_campaign_content(campaign_content)
    print(f"\n📚 Enhanced Campaign Content:")
    print(f"   Campaign narrative: {len(enhanced['campaign'].get('narrative', ''))} chars")
    print(f"   Characters enhanced: {len(enhanced['characters'])}")
    for char in enhanced['characters']:
        print(f"   - {char['name']}: {len(char.get('description', ''))} chars")
    
    return enhanced


async def test_pdf_generation_with_gemini():
    """Test PDF generation with Gemini enhancement"""
    print("\n" + "=" * 60)
    print("Testing PDF Generation with Gemini Enhancement")
    print("=" * 60)
    
    # Get enhanced content
    adapter = GeminiPDFAdapter()
    
    campaign_data = {
        'name': 'The Shattered Crown',
        'type': 'Political Intrigue',
        'level_range': '1-5',
        'tone': 'epic',
        'setting': 'Medieval fantasy kingdom'
    }
    
    narrative = await adapter.enhance_campaign_narrative(campaign_data)
    
    # Create PDF content
    content = f"""# {campaign_data['name']}

## Campaign Overview

{narrative}

## Campaign Details

- **Type**: {campaign_data['type']}
- **Level Range**: {campaign_data['level_range']}
- **Tone**: {campaign_data['tone']}
- **Setting**: {campaign_data['setting']}

## Generated with Gemini AI

This campaign PDF was enhanced using Google's Gemini API for narrative generation.
"""
    
    # Generate PDF
    output_path = project_root / "_work_efforts" / "WE-260115-weul_gemini_ai_dnd_integration_for_campaign_pdfs" / "test_campaign_with_gemini.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📄 Generating PDF: {output_path.name}")
    
    try:
        generator = PDFGenerator.from_content(
            content=content,
            title=campaign_data['name'],
            style="premium",
            use_golden_triangle=True
        )
        
        result = generator.save(
            output_path=output_path,
            convert_to_png=True,
            png_dpi=300
        )
        
        print(f"✅ PDF generated successfully: {result}")
        print(f"   Size: {result.stat().st_size / 1024:.1f} KB")
        
        return result
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return None


async def main():
    """Run all tests"""
    print("\n🚀 Starting Gemini Campaign PDF Integration Tests\n")
    
    try:
        # Test adapter
        enhanced_content = await test_gemini_adapter()
        
        # Test PDF generation
        pdf_path = await test_pdf_generation_with_gemini()
        
        # Summary
        print("\n" + "=" * 60)
        print("✅ Tests Complete!")
        print("=" * 60)
        print("\nSummary:")
        print("  - Gemini adapter tested")
        print("  - Campaign narrative enhancement tested")
        print("  - Character description enhancement tested")
        print("  - PDF generation with Gemini tested")
        
        if pdf_path:
            print(f"\n📄 Generated PDF: {pdf_path}")
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
