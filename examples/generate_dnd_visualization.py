#!/usr/bin/env python3
"""
Example: Generate D&D Game Visualizations

Demonstrates how to use the DnD game visualization wrapper to generate
various types of D&D game PDFs.
"""

from pathlib import Path
from src.waft.templates.typst.wrappers.dnd_game import (
    generate_dnd_game,
    Character,
    StatBlock,
    EncounterParticipant,
)


def example_character_sheet():
    """Generate a character sheet PDF."""
    print("Generating character sheet...")
    
    # Create a sample character
    character = Character(
        name="Thorin Ironforge",
        class_level="Fighter 5",
        race="Dwarf",
        background="Soldier",
        alignment="Lawful Good",
        ability_scores={
            "STR": 18,
            "DEX": 14,
            "CON": 16,
            "INT": 10,
            "WIS": 12,
            "CHA": 8,
        },
        hit_points={"current": 45, "max": 50},
        armor_class=18,
        skills=[
            {"name": "Athletics", "value": "+7", "modifier": "STR"},
            {"name": "Perception", "value": "+4", "modifier": "WIS"},
        ],
        equipment=[
            "Plate Armor",
            "Longsword",
            "Shield",
            "Handaxe",
            "Backpack",
        ],
    )
    
    output_path = Path("examples_output/thorin_character_sheet.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    pdf_path = generate_dnd_game(
        title="Thorin Ironforge - Character Sheet",
        content="A brave dwarf fighter ready for adventure.",
        output_path=output_path,
        document_type="character_sheet",
        template_package="wenyuan-campaign",
        characters=[character],
        show_rules=False,
    )
    
    print(f"✅ Character sheet generated: {pdf_path}")
    return pdf_path


def example_stat_block():
    """Generate a stat block PDF."""
    print("Generating stat block...")
    
    # Create a sample stat block (Orc)
    orc = StatBlock(
        name="Orc",
        size_type="Medium humanoid (orc)",
        armor_class=13,
        hit_points=15,
        speed="30 ft.",
        ability_scores={
            "STR": 16,
            "DEX": 12,
            "CON": 16,
            "INT": 7,
            "WIS": 11,
            "CHA": 10,
        },
        skills=["Intimidation +2"],
        senses="darkvision 60 ft.",
        languages="Common, Orc",
        challenge_rating="1/2",
        traits=[
            {
                "name": "Aggressive",
                "text": "As a bonus action, the orc can move up to its speed toward a hostile creature that it can see.",
            }
        ],
        actions=[
            {
                "name": "Greataxe",
                "text": "Melee Weapon Attack: +5 to hit, reach 5 ft., one target. Hit: 9 (1d12 + 3) slashing damage.",
            },
        ],
    )
    
    output_path = Path("examples_output/orc_stat_block.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    pdf_path = generate_dnd_game(
        title="Orc - Stat Block",
        content="A common orc warrior found in many D&D campaigns.",
        output_path=output_path,
        document_type="stat_block",
        template_package="dragonling",
        stat_blocks=[orc],
        show_rules=False,
    )
    
    print(f"✅ Stat block generated: {pdf_path}")
    return pdf_path


def example_encounter():
    """Generate an encounter visualization PDF."""
    print("Generating encounter visualization...")
    
    # Create encounter participants
    participants = [
        EncounterParticipant(
            name="Thorin Ironforge",
            initiative=18,
            is_player=True,
            current_hp=45,
            max_hp=50,
            armor_class=18,
            conditions=[],
        ),
        EncounterParticipant(
            name="Orc Warrior 1",
            initiative=12,
            is_player=False,
            current_hp=15,
            max_hp=15,
            armor_class=13,
            conditions=[],
        ),
        EncounterParticipant(
            name="Orc Warrior 2",
            initiative=8,
            is_player=False,
            current_hp=12,
            max_hp=15,
            armor_class=13,
            conditions=["Poisoned"],
        ),
        EncounterParticipant(
            name="Orc Shaman",
            initiative=5,
            is_player=False,
            current_hp=22,
            max_hp=22,
            armor_class=11,
            conditions=[],
        ),
    ]
    
    output_path = Path("examples_output/combat_encounter.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    pdf_path = generate_dnd_game(
        title="Combat Encounter - Orc Ambush",
        content="The party encounters a group of orcs in the forest.",
        output_path=output_path,
        document_type="encounter",
        template_package="wenyuan-campaign",
        encounter_participants=participants,
        show_rules=False,
    )
    
    print(f"✅ Encounter visualization generated: {pdf_path}")
    return pdf_path


def example_multiple_characters():
    """Generate a PDF with multiple character sheets."""
    print("Generating multiple character sheets...")
    
    characters = [
        Character(
            name="Thorin Ironforge",
            class_level="Fighter 5",
            race="Dwarf",
            ability_scores={"STR": 18, "DEX": 14, "CON": 16, "INT": 10, "WIS": 12, "CHA": 8},
            hit_points={"current": 45, "max": 50},
            armor_class=18,
        ),
        Character(
            name="Lyra Moonwhisper",
            class_level="Wizard 5",
            race="Elf",
            ability_scores={"STR": 8, "DEX": 14, "CON": 12, "INT": 18, "WIS": 13, "CHA": 10},
            hit_points={"current": 28, "max": 32},
            armor_class=12,
            spells=["Fireball", "Magic Missile", "Shield"],
        ),
        Character(
            name="Grok Stonefist",
            class_level="Barbarian 5",
            race="Half-Orc",
            ability_scores={"STR": 17, "DEX": 13, "CON": 16, "INT": 8, "WIS": 10, "CHA": 12},
            hit_points={"current": 52, "max": 55},
            armor_class=15,
        ),
    ]
    
    output_path = Path("examples_output/party_character_sheets.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    pdf_path = generate_dnd_game(
        title="Adventuring Party - Character Sheets",
        content="The complete party roster for the campaign.",
        output_path=output_path,
        document_type="character_sheet",
        template_package="wenyuan-campaign",
        characters=characters,
        show_rules=False,
    )
    
    print(f"✅ Multiple character sheets generated: {pdf_path}")
    return pdf_path


def main():
    """Run all examples."""
    print("=" * 60)
    print("D&D Game Visualization Examples")
    print("=" * 60)
    print()
    
    try:
        # Example 1: Character sheet
        example_character_sheet()
        print()
        
        # Example 2: Stat block
        example_stat_block()
        print()
        
        # Example 3: Encounter visualization
        example_encounter()
        print()
        
        # Example 4: Multiple characters
        example_multiple_characters()
        print()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()
