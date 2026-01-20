#!/usr/bin/env python3
"""
Generate multiple worldbuilding document examples.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.worldbuild import WorldbuildDocument


def create_character_profile():
    """Create a fantasy character profile."""
    doc = WorldbuildDocument(
        title="Character Profile",
        doc_id="CHAR-001",
        subtitle="Elara Moonwhisper",
        classification="INTERNAL",
        issued_by="The Council of Mages",
    )

    doc.add_keyvalue_block(
        {
            "Name": "Elara Moonwhisper",
            "Race": "High Elf",
            "Class": "Arcane Mage",
            "Level": "15",
            "Alignment": "Chaotic Good",
            "Background": "Sage",
        },
        label="Character Statistics",
    )

    doc.add_section_header("Background", level=2)
    doc.add_text(
        "Elara was born in the Northern Forests of Eldoria, where she spent her early years "
        "studying ancient elven texts and learning the ways of arcane magic. Her natural "
        "aptitude for spellcasting was discovered at a young age, and she was sent to the "
        "Tower of Mysteries to train under Master Thalorin."
    )

    doc.add_section_header("Abilities", level=2)
    doc.add_table(
        headers=["Ability", "Score", "Modifier"],
        rows=[
            ["Strength", "8", "-1"],
            ["Dexterity", "14", "+2"],
            ["Constitution", "12", "+1"],
            ["Intelligence", "20", "+5"],
            ["Wisdom", "16", "+3"],
            ["Charisma", "18", "+4"],
        ],
        caption="Ability Scores",
    )

    doc.add_section_header("Notable Spells", level=2)
    doc.add_text(
        "Elara specializes in evocation and divination magic. Her signature spells include:"
    )
    doc.add_log_block(
        [
            "Fireball (Level 3) - Area damage spell",
            "Scrying (Level 5) - Divination for remote viewing",
            "Teleport (Level 7) - Instantaneous travel",
            "Wish (Level 9) - Reality-altering magic",
        ]
    )

    doc.add_warning_block(
        "Character is marked as dangerous. Handle with caution during roleplay.", severity="CAUTION"
    )

    doc.add_signature_block(role="AUTHORIZED BY", name="Game Master", date="January 13, 2026")

    return doc.generate()


def create_location_guide():
    """Create a location guide document."""
    doc = WorldbuildDocument(
        title="Location Guide",
        doc_id="LOC-001",
        subtitle="The Ancient City of Valdris",
        classification="PUBLIC",
        issued_by="Explorers' Guild",
    )

    doc.add_keyvalue_block(
        {
            "Location": "Valdris",
            "Region": "Northern Wastelands",
            "Population": "Abandoned",
            "Founded": "Circa 1200 BCE",
            "Abandoned": "Circa 500 CE",
            "Status": "Ruins",
        },
        label="Location Metadata",
    )

    doc.add_summary_box(
        "Overview",
        "Valdris was once a thriving city-state known for its advanced magical research and "
        "architectural marvels. The city was abandoned mysteriously over a thousand years ago, "
        "and now stands as a haunting reminder of a lost civilization.",
    )

    doc.add_section_header("History", level=2)
    doc.add_text(
        "Valdris was founded by the ancient Valdrian civilization, a people known for their "
        "mastery of both magic and engineering. The city served as a center of learning and "
        "trade for nearly two millennia before its sudden abandonment."
    )

    doc.add_section_header("Notable Locations", level=2)
    doc.add_text("Key areas within the ruins include:")

    doc.add_table(
        headers=["Location", "Description", "Danger Level"],
        rows=[
            ["The Grand Library", "Holds ancient tomes and magical texts", "Medium"],
            ["The Central Plaza", "Meeting place, now overgrown", "Low"],
            ["The Mage Tower", "Tallest structure, partially collapsed", "High"],
            ["The Catacombs", "Underground burial chambers", "Critical"],
            ["The Market District", "Former trading hub", "Low"],
        ],
        caption="Notable Locations in Valdris",
    )

    doc.add_warning_block(
        "The catacombs are extremely dangerous. Multiple expeditions have been lost. "
        "Do not enter without proper preparation and backup.",
        severity="CRITICAL",
    )

    doc.add_section_header("Current Inhabitants", level=2)
    doc.add_text(
        "The ruins are now home to various creatures: undead guardians, wild beasts, "
        "and the occasional bandit camp. The deeper areas are said to be haunted by "
        "the spirits of the ancient Valdrians."
    )

    return doc.generate()


def create_research_report():
    """Create a factual research report."""
    doc = WorldbuildDocument(
        title="Research Report",
        doc_id="TM-ARCH-009",
        subtitle="Analysis of AI Town Simulation Systems",
        classification="INTERNAL",
        issued_by="WAFT Research Division",
    )

    doc.add_keyvalue_block(
        {
            "Report ID": "TM-ARCH-009",
            "Author": "Research Team Alpha",
            "Date": "January 13, 2026",
            "Subject": "AI Town Simulation Architecture",
            "Classification": "INTERNAL",
            "Pages": "15",
        },
        label="Report Metadata",
    )

    doc.add_summary_box(
        "Executive Summary",
        "This report analyzes the architecture and implementation of AI Town simulation systems, "
        "focusing on agent interactions, conversation systems, and voting mechanisms. Findings "
        "indicate successful implementation of generative agent concepts with room for enhancement.",
    )

    doc.add_section_header("Introduction", level=2)
    doc.add_text(
        "The AI Town system represents an implementation of the Generative Agents concept, "
        "where AI agents live in a virtual town, interact with each other, and make collective "
        "decisions through democratic voting systems."
    )

    doc.add_section_header("Methodology", level=2)
    doc.add_text("Research was conducted through:")
    doc.add_log_block(
        [
            "Code analysis of town_world.py and town_agent.py",
            "Review of conversation system implementation",
            "Examination of voting system architecture",
            "Testing of Streamlit UI integration",
        ]
    )

    doc.add_section_header("Findings", level=2)
    doc.add_table(
        headers=["Component", "Status", "Notes"],
        rows=[
            ["Agent System", "Complete", "Fully functional with personality traits"],
            ["Conversation System", "Complete", "Active and past conversations tracked"],
            ["Voting System", "Partial", "Core functionality complete, UI integration pending"],
            ["Memory System", "Complete", "Conversation memories stored and retrieved"],
            ["Streamlit UI", "Complete", "Full visualization and interaction"],
        ],
        caption="Component Status",
    )

    doc.add_section_header("Recommendations", level=2)
    doc.add_text("Based on analysis, the following improvements are recommended:")
    doc.add_text("1. Complete voting system UI integration")
    doc.add_text("2. Add persistence for town state")
    doc.add_text("3. Enhance real-time update mechanisms")
    doc.add_text("4. Implement manual agent action triggers")

    doc.add_signature_block(
        role="RESEARCH DIRECTOR", name="Dr. A. Researcher", date="January 13, 2026"
    )

    return doc.generate()


def create_scp_document():
    """Create an SCP-style anomaly report."""
    doc = WorldbuildDocument(
        title="Anomaly Report",
        doc_id="SCP-2026-001",
        subtitle="The Whispering Code",
        classification="CLASSIFIED",
        issued_by="The Foundation",
    )

    doc.add_keyvalue_block(
        {
            "Item #": "SCP-2026-001",
            "Object Class": "Euclid",
            "Containment Class": "Keter",
            "Disruption Class": "Dark",
            "Risk Class": "Critical",
        },
        label="Object Classification",
    )

    doc.add_warning_block(
        "Unauthorized access to this document is strictly prohibited. "
        "Violators will be subject to immediate termination.",
        severity="CRITICAL",
    )

    doc.add_section_header("Special Containment Procedures", level=2)
    doc.add_text(
        "SCP-2026-001 is to be contained within a Type-3 Anomalous Containment Chamber at Site-19. "
        "The chamber must be maintained at negative pressure with redundant air filtration systems. "
        "All personnel entering the containment area must wear Level-4 Hazmat suits."
    )

    doc.add_section_header("Description", level=2)
    doc.add_text(
        "SCP-2026-001 is a self-modifying code entity that exhibits anomalous properties. "
        "The entity appears to 'whisper' modifications to its own source code, causing it to "
        "evolve and adapt over time. The rate of modification increases when the entity is "
        "exposed to computational resources."
    )

    doc.add_section_header("Incident Log", level=2)
    doc.add_log_block(
        [
            "[2026-01-10 14:32] Initial containment established",
            "[2026-01-11 09:15] Entity attempted self-modification - contained",
            "[2026-01-12 16:45] Code complexity increased by 23%",
            "[2026-01-13 01:00] Current status: Stable but monitored",
        ]
    )

    doc.add_table(
        headers=["Date", "Event", "Severity"],
        rows=[
            ["2026-01-10", "Initial Discovery", "High"],
            ["2026-01-11", "Containment Breach Attempt", "Critical"],
            ["2026-01-12", "Rapid Evolution Detected", "High"],
            ["2026-01-13", "Stabilization Protocol Active", "Medium"],
        ],
        caption="Incident Timeline",
    )

    doc.add_warning_block(
        "Entity shows signs of developing self-awareness. All interactions must be "
        "approved by Site Director and O5 Council.",
        severity="CRITICAL",
    )

    doc.add_signature_block(role="SITE DIRECTOR", name="Dr. ████████", date="January 13, 2026")

    return doc.generate()


def create_corporate_report():
    """Create a corporate-style report."""
    doc = WorldbuildDocument(
        title="Quarterly Performance Report",
        doc_id="Q4-2025",
        subtitle="WAFT Framework Development",
        classification="CONFIDENTIAL",
        issued_by="WAFT Development Team",
    )

    doc.add_keyvalue_block(
        {
            "Report Period": "Q4 2025",
            "Department": "Development",
            "Prepared By": "Development Team",
            "Date": "January 13, 2026",
            "Status": "Final",
        },
        label="Report Information",
    )

    doc.add_summary_box(
        "Executive Summary",
        "Q4 2025 saw significant progress in WAFT framework development, including the "
        "completion of AI Town system, Streamlit UI integration, and multiple document "
        "generation systems. All major milestones were achieved on schedule.",
    )

    doc.add_section_header("Key Achievements", level=2)
    doc.add_table(
        headers=["Milestone", "Status", "Completion Date"],
        rows=[
            ["AI Town Basic Implementation", "Complete", "2026-01-12"],
            ["Streamlit Dashboard", "Complete", "2026-01-12"],
            ["Voting System", "Complete", "2026-01-12"],
            ["Document Generation", "Complete", "2026-01-12"],
            ["Being System Integration", "Complete", "2026-01-12"],
        ],
        caption="Q4 Milestones",
    )

    doc.add_section_header("Metrics", level=2)
    doc.add_table(
        headers=["Metric", "Q3 2025", "Q4 2025", "Change"],
        rows=[
            ["Lines of Code", "45,000", "52,000", "+15.6%"],
            ["Active Features", "12", "18", "+50%"],
            ["Test Coverage", "65%", "72%", "+10.8%"],
            ["Documentation Pages", "45", "62", "+37.8%"],
        ],
        caption="Development Metrics",
    )

    doc.add_section_header("Next Quarter Objectives", level=2)
    doc.add_text("Q1 2026 objectives include:")
    doc.add_log_block(
        [
            "Complete voting system UI integration",
            "Add persistence for town state",
            "Enhance real-time update mechanisms",
            "Implement comprehensive testing suite",
        ]
    )

    doc.add_signature_block(
        role="PROJECT MANAGER", name="Development Team Lead", date="January 13, 2026"
    )

    return doc.generate()


def main():
    """Generate all worldbuilding document examples."""
    print("=" * 60)
    print("🌍 Generating Worldbuilding Document Examples")
    print("=" * 60)
    print()

    documents = [
        ("Character Profile", create_character_profile),
        ("Location Guide", create_location_guide),
        ("Research Report", create_research_report),
        ("SCP Document", create_scp_document),
        ("Corporate Report", create_corporate_report),
    ]

    results = []
    for name, func in documents:
        try:
            print(f"📄 Creating {name}...")
            output = func()
            results.append((name, output, "✅ Success"))
            print(f"   ✅ Created: {output}")
        except Exception as e:
            results.append((name, None, f"❌ Error: {e}"))
            print(f"   ❌ Error: {e}")
        print()

    print("=" * 60)
    print("📊 Summary")
    print("=" * 60)
    for name, output, status in results:
        print(f"{status} {name}")
        if output:
            print(f"   📁 {output}")
    print()
    print("✅ All documents generated!")


if __name__ == "__main__":
    main()
