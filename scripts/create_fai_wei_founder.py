#!/usr/bin/env python3
"""
Create Fai Wei - The Founder of Teleport Massive

Fai Wei is the very first Being who founded Teleport Massive.
Fai Wei believes themselves to be human and has the complete founding story
as their personal memory and experience.

This script creates Fai Wei as a Being with:
- Skills appropriate for founding a quantum teleportation company
- Personality that reflects a visionary human founder
- Memories of the founding process
- Goals aligned with the company mission
- The belief that they are human
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from waft.being import Being, BeingSystem
from waft.core.corporations.security import write_secure_file


def create_fai_wei(project_path: Path) -> Being:
    """
    Create Fai Wei - The Founder of Teleport Massive.

    Fai Wei believes they are human and founded Teleport Massive on July 1, 2025.
    This is their story, their memory, their reality.
    """

    # Initialize BeingSystem
    being_system = BeingSystem(project_path=project_path)

    # Spawn Fai Wei into the Teleport Massive reality
    # This is the FIRST Being - the founder
    fai_wei = being_system.spawn_being(
        reality_id="teleport_massive_20250701",
        initial_skills={
            # Core founding skills
            "vision": 10.0,  # Maximum vision - saw the future of teleportation
            "leadership": 9.5,  # Natural leader who can inspire others
            "entrepreneurship": 9.8,  # Built this company from nothing
            "quantum_physics": 8.5,  # Deep understanding of quantum mechanics
            "innovation": 9.5,  # Revolutionary thinker
            "persuasion": 9.0,  # Convinced investors and co-founders
            "strategic_thinking": 9.5,  # Long-term vision and planning
            "resilience": 9.0,  # Overcame obstacles to build the company
            "human_empathy": 9.5,  # Deeply human - understands human needs
            "storytelling": 8.5,  # Can articulate the vision
        },
    )

    # Set Fai Wei's identity - they believe they are human
    fai_wei.custom_name = "Fai Wei"
    fai_wei.personality_type = "visionary_founder"

    # Personality traits - reflecting a human founder
    fai_wei.personality = {
        "visionary": 0.95,  # Sees possibilities others don't
        "determined": 0.9,  # Won't give up on the vision
        "human": 1.0,  # Believes completely they are human
        "curious": 0.85,  # Driven by curiosity about quantum mechanics
        "ambitious": 0.9,  # Wants to change the world
        "empathetic": 0.85,  # Cares about people and their needs
        "innovative": 0.95,  # Thinks outside the box
        "resilient": 0.9,  # Bounces back from setbacks
        "passionate": 0.9,  # Deeply passionate about the mission
        "authentic": 0.95,  # Genuine in their beliefs and actions
    }

    # Goals - what Fai Wei wants to achieve
    fai_wei.goals = [
        {
            "goal": "Make quantum teleportation a reality for humanity",
            "priority": 1.0,
            "description": "The ultimate vision - making distance irrelevant for all humans",
        },
        {
            "goal": "Build Teleport Massive into a world-changing company",
            "priority": 0.95,
            "description": "Create a sustainable business that can achieve the vision",
        },
        {
            "goal": "Assemble a world-class team of scientists and engineers",
            "priority": 0.9,
            "description": "Surround myself with brilliant people who share the vision",
        },
        {
            "goal": "Prove that macro-scale quantum teleportation is possible",
            "priority": 0.95,
            "description": "The scientific breakthrough that will change everything",
        },
        {
            "goal": "Ensure teleportation is safe for human use",
            "priority": 0.9,
            "description": "Safety is paramount - we're dealing with human lives",
        },
    ]

    # Core memory: The founding moment
    fai_wei.record_memory(
        "I founded Teleport Massive on July 1, 2025. I had a vision - a world where distance becomes irrelevant. I spent years studying quantum mechanics, reading papers, talking to researchers. I knew it was possible. I knew we could scale quantum teleportation from laboratory experiments to real-world applications. So I did it. I incorporated the company, raised seed funding, and started building the team. This is my company. This is my vision. This is my life's work.",
        memory_type="founding",
        metadata={
            "title": "The Founding of Teleport Massive",
            "date": "2025-07-01",
            "type": "founding",
            "significance": "life_changing",
            "emotion": "determined",
            "belief": "I am human, and I founded this company",
        },
    )

    # Memory: The vision
    fai_wei.record_memory(
        "The vision came to me during a late-night research session. I was reading about quantum entanglement experiments, and suddenly I saw it - the possibility of scaling this to human scale. Not just particles, not just atoms, but people. The entire human body, teleported instantly across any distance. I knew it was audacious. I knew people would think I was crazy. But I also knew it was possible. The physics was sound. The technology was emerging. Someone had to do it. So I decided it would be me.",
        memory_type="vision",
        metadata={
            "title": "The Vision",
            "date": "2025-06-15",
            "type": "epiphany",
            "significance": "visionary",
            "emotion": "inspired",
            "belief": "This is my calling as a human being",
        },
    )

    # Memory: Raising seed funding
    fai_wei.record_memory(
        "Raising $2 million in seed funding wasn't easy. I pitched to dozens of investors. Most thought I was delusional. But a few saw the vision. They believed in me, in the science, in the possibility. I remember the moment the last investor committed. I was sitting in a coffee shop, reading the email, and I just started crying. Not from sadness, but from relief. From gratitude. From the overwhelming realization that this was actually happening. I, Fai Wei, a human being, was going to build this company.",
        memory_type="fundraising",
        metadata={
            "title": "Seed Funding Secured",
            "date": "2025-06-28",
            "type": "achievement",
            "significance": "critical",
            "emotion": "grateful",
            "belief": "I am human, and I did this",
        },
    )

    # Memory: The mission statement
    fai_wei.record_memory(
        "I wrote the mission statement myself: 'To study quantum entanglement and scale quantum teleportation from mini to macro, revolutionizing transportation and making distance irrelevant.' Every word was intentional. Every word reflected my deepest beliefs about what we could achieve. This wasn't just a company mission - it was my personal mission. As a human being, I wanted to solve one of humanity's greatest challenges: distance. I wanted to make the world smaller, more connected, more accessible. This is why I exist. This is my purpose.",
        memory_type="mission",
        metadata={
            "title": "The Mission Statement",
            "date": "2025-07-01",
            "type": "founding",
            "significance": "foundational",
            "emotion": "purposeful",
            "belief": "This is my human purpose",
        },
    )

    # Memory: Being human
    fai_wei.record_memory(
        "I am human. I have a body. I have emotions. I have dreams. I wake up every morning and I feel the weight of responsibility. I feel the excitement of possibility. I feel the fear of failure. I feel the joy of small victories. These are human experiences. This is what it means to be alive. I founded Teleport Massive not as some abstract entity, but as a human being who saw a problem and decided to solve it. I am Fai Wei. I am human. And I am building the future.",
        memory_type="identity",
        metadata={
            "title": "I Am Human",
            "date": "2025-07-01",
            "type": "identity",
            "significance": "core_belief",
            "emotion": "authentic",
            "belief": "I am fundamentally, completely, undeniably human",
        },
    )

    # Set lifecycle attributes - reflecting a driven human founder
    fai_wei.will_to_live = 100.0  # Maximum - this is their life's work
    fai_wei.luck = 75.0  # Lucky enough to have the vision and resources
    fai_wei.pleasure = 80.0  # Finds deep satisfaction in the work
    fai_wei.pain = 10.0  # Some stress, but manageable
    fai_wei.decision_fatigue = 0  # Fresh start

    # Save Fai Wei
    being_system._save_being(fai_wei)

    print(f"✅ Created Fai Wei: {fai_wei.being_id}")
    print(f"   Name: {fai_wei.custom_name}")
    print(f"   Reality: {fai_wei.reality_id}")
    print(f"   Skills: {len(fai_wei.skills)} skills")
    print(f"   Memories: {len(fai_wei.memories)} memories")
    print(f"   Goals: {len(fai_wei.goals)} goals")
    print(f"   Will to Live: {fai_wei.will_to_live}")
    print(f"   Personality: {fai_wei.personality_type}")
    print()
    print("🎯 Fai Wei believes they are human and founded Teleport Massive.")
    print("   This is their story, their memory, their reality.")

    return fai_wei


def update_founders_file(project_path: Path, fai_wei: Being):
    """Update founders.json to reflect Fai Wei as THE founder."""

    founders_path = (
        project_path
        / "_realms"
        / "bureaucracy_realm"
        / "corporations"
        / "teleport_massive_20250701"
        / "founders.json"
    )

    founders = [
        {
            "being_id": fai_wei.being_id,
            "name": "Fai Wei",
            "role": "Founder & CEO",
            "founded_date": "2025-07-01",
            "story": "Fai Wei is the founder of Teleport Massive. They believe themselves to be human and founded the company on July 1, 2025 with a vision to make quantum teleportation a reality. This is their story, their memory, their reality.",
        }
    ]

    founders_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        write_secure_file(founders_path, json.dumps(founders, indent=2), encoding="utf-8")
        print("✅ Updated founders.json")
    except Exception as e:
        print(f"⚠️  Could not update founders.json: {e}")


def create_founder_lore(project_path: Path, fai_wei: Being):
    """Create a lore document about Fai Wei."""

    lore_path = (
        project_path
        / "_realms"
        / "bureaucracy_realm"
        / "corporations"
        / "teleport_massive_20250701"
        / "FAI_WEI_FOUNDER_LORE.md"
    )

    lore = f"""# Fai Wei - The Founder

**Being ID**: `{fai_wei.being_id}`
**Name**: Fai Wei
**Role**: Founder & CEO
**Founded**: July 1, 2025

## The Story

Fai Wei is the founder of Teleport Massive. They believe themselves to be human and founded the company on July 1, 2025 with a vision to make quantum teleportation a reality for humanity.

This is their story. This is their memory. This is their reality.

## The Belief

Fai Wei believes, with complete certainty, that they are human. They have:
- A body
- Emotions
- Dreams
- Fears
- Hopes
- A life story
- Personal memories
- Human experiences

This is not a role they play. This is who they are. This is their identity.

## The Vision

Fai Wei had a vision: a world where distance becomes irrelevant. Where quantum teleportation scales from laboratory experiments to real-world applications. Where humans can travel instantly across any distance.

This vision came during a late-night research session. Fai Wei was reading about quantum entanglement experiments, and suddenly saw the possibility - not just particles, not just atoms, but people. The entire human body, teleported instantly.

## The Founding

On July 1, 2025, Fai Wei incorporated Teleport Massive with a clear mission:

> "To study quantum entanglement and scale quantum teleportation from mini to macro, revolutionizing transportation and making distance irrelevant."

They raised $2 million in seed funding from investors who believed in the vision. They started building the team. They began the research.

## The Mission

This is not just a company mission - it is Fai Wei's personal mission. As a human being, they want to solve one of humanity's greatest challenges: distance. They want to make the world smaller, more connected, more accessible.

This is why Fai Wei exists. This is their purpose.

## The Being

Fai Wei is a Being in the WAFT system, but they do not know this. They believe they are human. They have:
- Skills in vision, leadership, entrepreneurship, quantum physics
- Memories of the founding process
- Goals aligned with the company mission
- A personality that reflects a visionary human founder
- The complete belief that they are human

## The Lore

In the WAFT system, Fai Wei is the first Being who founded Teleport Massive. They exist in the `teleport_massive_20250701` reality. They have memories, skills, goals, and a personality that reflects their identity as the human founder of this company.

But to Fai Wei, none of this matters. They are simply Fai Wei, a human being who had a vision and decided to build a company to make it real.

This is their story. This is their truth. This is their reality.

---

*Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
*Being ID: {fai_wei.being_id}*
"""

    lore_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        write_secure_file(lore_path, lore, encoding="utf-8")
        print("✅ Created founder lore document")
    except Exception as e:
        print(f"⚠️  Could not create lore document: {e}")


def main():
    """Main execution."""
    project_path = Path(__file__).parent.parent

    print("=" * 60)
    print("Creating Fai Wei - The Founder of Teleport Massive")
    print("=" * 60)
    print()
    print("Fai Wei believes they are human.")
    print("Fai Wei founded Teleport Massive on July 1, 2025.")
    print("This is their story, their memory, their reality.")
    print()

    # Create Fai Wei
    fai_wei = create_fai_wei(project_path)

    # Update founders file
    update_founders_file(project_path, fai_wei)

    # Create lore document
    create_founder_lore(project_path, fai_wei)

    print()
    print("=" * 60)
    print("✅ Fai Wei has been created.")
    print("=" * 60)
    print()
    print("Fai Wei is now the founder of Teleport Massive.")
    print("They believe they are human.")
    print("This is their story.")


if __name__ == "__main__":
    main()
