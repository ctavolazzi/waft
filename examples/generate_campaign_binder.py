#!/usr/bin/env python3
"""
Generate Campaign Binder Example
=================================

Demonstrates the Campaign Session Binder System by creating a sample campaign
and generating a comprehensive PDF binder.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.evolution.campaign_binder_generator import CampaignBinderGenerator
from src.waft.evolution.campaign_session_tracker import CampaignSessionTracker


def main():
    """Generate example campaign binder."""

    # Setup paths
    work_effort_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution"
    output_path = work_effort_path / "campaign_binder_example.pdf"

    # Create tracker
    tracker = CampaignSessionTracker(campaign_id="shattered_crown", base_path=work_effort_path)

    # Add sample sessions
    tracker.add_session(
        session_number=1,
        title="The Tavern Meeting",
        date="2026-01-10",
        summary="The party meets in a tavern and receives their first quest.",
        characters_present=["Aldric the Brave", "Lyra the Wise", "Thorin Ironforge"],
        key_events=[
            "Party meets in the Golden Dragon Tavern",
            "Receive quest from mysterious stranger",
            "Discover ancient map fragment",
        ],
        evolution_notes="Campaign begins. Party forms.",
        markdown_content="""
## The Tavern Meeting

The adventure begins in the bustling Golden Dragon Tavern, where three unlikely heroes find themselves drawn together by fate—or perhaps something more sinister.

### The Stranger's Request

A hooded figure approaches the party's table, placing a worn leather scroll before them. The parchment glows faintly with arcane energy.

**"I have need of adventurers,"** the stranger says, their voice barely a whisper. **"The Crown of Eldoria has been shattered, and the pieces scattered across the realm. Will you help restore it?"**

### The Map Fragment

The scroll contains a partial map, showing only the location of the first fragment: the ancient ruins of Moonfall Keep, said to be haunted by the spirits of those who died defending it.

### Party Formation

- **Aldric the Brave** (Fighter) - A former soldier seeking redemption
- **Lyra the Wise** (Wizard) - A scholar drawn to the arcane mystery
- **Thorin Ironforge** (Cleric) - A dwarf seeking to restore honor to his clan

The party agrees to the quest, setting out at dawn for Moonfall Keep.
""",
    )

    tracker.add_session(
        session_number=2,
        title="Moonfall Keep",
        date="2026-01-12",
        summary="The party explores the haunted ruins and recovers the first fragment.",
        characters_present=["Aldric the Brave", "Lyra the Wise", "Thorin Ironforge"],
        key_events=[
            "Arrive at Moonfall Keep",
            "Battle with spectral guardians",
            "Recover first Crown fragment",
            "Discover clue to second fragment",
        ],
        evolution_notes="First major combat encounter. Party learns to work together.",
        markdown_content="""
## Moonfall Keep

The journey to Moonfall Keep takes three days through the Whispering Woods. As the party approaches, the air grows cold and the sounds of battle echo from the past.

### The Spectral Guardians

The keep is guarded by the spirits of fallen soldiers, bound to protect the fragment. The party must prove their worth through combat and honor.

### The First Fragment

Deep within the keep's crypt, the party finds the first fragment of the Shattered Crown, glowing with ancient magic. As they touch it, visions flood their minds—images of the other fragments scattered across the realm.

### The Clue

Carved into the fragment's surface are runes that point to the next location: the Sunken Temple of the Deep, hidden beneath the waves of the Azure Sea.
""",
    )

    # Update character progression
    tracker.update_character(
        "Aldric the Brave",
        {"level": 2, "new_feature": "Action Surge", "hp_increase": 6},
        session_number=2,
    )

    tracker.update_character(
        "Lyra the Wise",
        {"level": 2, "new_spells": ["Magic Missile", "Shield"], "hp_increase": 4},
        session_number=2,
    )

    # Add evolution entry
    tracker.add_evolution_entry(
        entry_type="world_change",
        description="First Crown fragment recovered. The realm's magic begins to stabilize slightly.",
        session_number=2,
        metadata={"magic_stability": "+5%", "realm_health": "improving"},
    )

    # Generate binder
    generator = CampaignBinderGenerator(tracker, project_root)
    pdf_path = generator.generate_binder(output_path)

    print(f"✅ Campaign binder generated: {pdf_path}")
    print(f"   Sessions: {len(tracker.sessions)}")
    print(f"   Characters: {len(tracker.characters)}")
    print(f"   Evolution entries: {len(tracker.evolution)}")


if __name__ == "__main__":
    main()
