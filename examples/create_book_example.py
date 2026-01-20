#!/usr/bin/env python3
"""
Example: Create a DnD Storybook
===============================

This example shows how to use the create_book script to generate
beautiful D&D-style storybooks.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.create_book import create_book


def example_demo_book():
    """Create a book with demo content."""
    print("Example 1: Creating a book with demo content")
    print("-" * 60)

    pdf_path = create_book(
        title="The Adventure Begins",
        chapters=None,  # Uses demo chapters
        author="WAFT Storyteller",
    )

    print(f"✅ Created: {pdf_path}")
    return pdf_path


def example_custom_chapters():
    """Create a book with custom chapters."""
    print("\nExample 2: Creating a book with custom chapters")
    print("-" * 60)

    chapters = [
        {
            "title": "Prologue: The Call",
            "content": """
            In the quiet village of Millbrook, life was simple and predictable.
            That all changed when the ancient bell in the town square began to ring
            on its own, a sound that hadn't been heard in generations.
            
            The villagers gathered, their faces filled with fear and wonder.
            The old sage, Master Elara, stepped forward and spoke:
            
            "The bell only rings when great danger approaches. The prophecy
            is coming true. We must prepare."
            """,
            "read_aloud": [
                "The bell's deep, resonant tone echoes across the valley, and you feel a chill run down your spine."
            ],
        },
        {
            "title": "Chapter 1: The Gathering",
            "content": """
            Three heroes answered the call: Aria the Ranger, Kael the Wizard,
            and Thorne the Paladin. Each came from different lands, but they
            shared a common purpose.
            
            Master Elara explained the ancient prophecy: A dark force was
            awakening, and only those chosen by the bell could stop it.
            
            "You must journey to the three sacred shrines," she said, "and
            gather the artifacts of power. Only then can you face the darkness."
            """,
            "read_aloud": [
                "The three heroes look at each other, knowing their lives will never be the same."
            ],
            "characters": ["Aria", "Kael", "Thorne", "Master Elara"],
            "settings": ["Millbrook", "The Town Square"],
        },
    ]

    pdf_path = create_book(
        title="The Prophecy of Millbrook", chapters=chapters, author="WAFT Storyteller"
    )

    print(f"✅ Created: {pdf_path}")
    return pdf_path


def example_with_monsters():
    """Create a book with monster stat blocks."""
    print("\nExample 3: Creating a book with monster stat blocks")
    print("-" * 60)

    chapters = [
        {
            "title": "Encounter: The Forest Guardian",
            "content": """
            As the heroes entered the Whispering Woods, they encountered
            a massive treant blocking their path. The ancient tree-creature
            spoke in a voice like rustling leaves:
            
            "None may pass without answering my riddle. Answer correctly,
            and the path is yours. Answer wrongly, and you must face my wrath."
            """,
            "read_aloud": [
                "The treant's branches creak and groan as it moves, and you realize this is no ordinary tree."
            ],
            "monsters": [
                {
                    "name": "Ancient Treant Guardian",
                    "size": "Huge",
                    "type": "plant",
                    "alignment": "neutral",
                    "armor_class": 16,
                    "hit_points": "138 (12d12 + 60)",
                    "speed": "30 ft.",
                    "ability_scores": {
                        "str": 23,
                        "dex": 8,
                        "con": 21,
                        "int": 12,
                        "wis": 16,
                        "cha": 12,
                    },
                    "senses": "darkvision 60 ft., passive Perception 13",
                    "languages": "Common, Druidic, Elvish, Sylvan",
                    "challenge": 9,
                    "description": "An ancient treant that guards the sacred paths through the Whispering Woods.",
                    "actions": [
                        {
                            "name": "Multiattack",
                            "description": "The treant makes two slam attacks.",
                        },
                        {
                            "name": "Slam",
                            "description": "Melee Weapon Attack: +10 to hit, reach 10 ft., one target. Hit: 16 (3d6 + 6) bludgeoning damage.",
                        },
                        {
                            "name": "Rock",
                            "description": "Ranged Weapon Attack: +10 to hit, range 60/180 ft., one target. Hit: 15 (3d6 + 6) bludgeoning damage.",
                        },
                    ],
                }
            ],
        }
    ]

    pdf_path = create_book(
        title="Monster Manual: Forest Encounters",
        chapters=chapters,
        author="WAFT Storyteller",
        include_monsters=True,
    )

    print(f"✅ Created: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    print("=" * 60)
    print("📚 Create Book Examples")
    print("=" * 60)
    print("\nNote: These examples require LaTeX to be installed.")
    print("Install with: brew install --cask mactex (macOS)")
    print()

    try:
        # Run examples
        example_demo_book()
        example_custom_chapters()
        example_with_monsters()

        print("\n" + "=" * 60)
        print("✅ All examples completed!")
        print("=" * 60)

    except RuntimeError as e:
        if "LaTeX" in str(e):
            print("\n⚠️  LaTeX is required for D&D-style books.")
            print("Install LaTeX to use these examples.")
        else:
            raise
