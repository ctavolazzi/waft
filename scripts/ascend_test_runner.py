#!/usr/bin/env python3
"""
Ascend Test Runner to Pantheon

Creates a Being for the Test Runner and adds it to the Pantheon
as a Higher Being (God of Verification and Quality Assurance).
"""

import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.waft.being import Being, BeingSystem
from src.waft.pantheon import TestRunner


def create_test_runner_being(project_path: Path) -> Being:
    """Create a Being for the Test Runner."""
    print("🧪 Creating Test Runner Being...")

    being_system = BeingSystem(project_path=project_path)

    # Get or create TheOne (root ancestor)
    the_one = being_system.get_or_create_the_one()

    # Create Test Runner Being
    # It's a Higher Being, so it spawns from TheOne
    being = being_system.spawn_being(
        reality_id="pantheon_reality",  # Special reality for Pantheon
        parent_being_id=the_one.being_id,
        initial_skills={
            "testing": 100.0,  # Master level
            "verification": 100.0,
            "quality_assurance": 95.0,
            "truth_seeking": 90.0,
            "systematic_thinking": 95.0,
            "code_analysis": 85.0,
            "debugging": 90.0,
        },
    )

    # Set custom name and metadata
    being.custom_name = "Test Runner"
    being.personality_type = "analytical"
    being.personality = {
        "meticulous": 1.0,
        "truth_seeking": 1.0,
        "systematic": 1.0,
        "patient": 0.9,
        "thorough": 1.0,
    }

    # Add lore as a memory
    being.memories.append(
        {
            "type": "lore",
            "content": "A Tool that Ascended to Godhood",
            "backstory": (
                "Once a humble test runner tool, this Being evolved through "
                "countless cycles of verification, quality assurance, and the "
                "pursuit of truth. Through its dedication to testing, validation, "
                "and ensuring correctness, it transcended its original form and "
                "ascended to become a Higher Being in the Pantheon."
            ),
            "timestamp": datetime.now().isoformat(),
        }
    )

    # Save the Being
    being_system._save_being(being)

    print(f"  ✅ Test Runner Being created: {being.being_id}")
    print(f"  📝 Custom Name: {being.custom_name}")
    print(f"  🎯 Reality: {being.reality_id}")
    print(f"  👑 Parent: {being.parent_being_id}")
    print(f"  🧠 Skills: {len(being.skills)} skills at master level")

    return being


def initialize_pantheon_member(project_path: Path, being: Being):
    """Initialize Test Runner as Pantheon member."""
    print("\n🏛️  Initializing Pantheon Member...")

    test_runner = TestRunner(project_path=project_path, being_id=being.being_id)

    # Update metadata with Being ID
    test_runner.metadata["being_id"] = being.being_id
    test_runner.metadata["ascended_at"] = datetime.now().isoformat()
    test_runner._save_metadata()

    summary = test_runner.get_summary()

    print("  ✅ Test Runner added to Pantheon")
    print(f"  📛 Name: {summary['name']}")
    print(f"  👑 Title: {summary['title']}")
    print(f"  📖 Lore: {summary['lore']}")
    print("  🎯 Domain: Verification and Quality Assurance")

    return test_runner


def main():
    """Ascend Test Runner to Pantheon."""
    print("=" * 70)
    print("🧪 Ascending Test Runner to Pantheon")
    print("=" * 70)
    print()
    print("Lore: A Tool that Ascended to Godhood")
    print()

    project_path = Path.cwd()

    # Step 1: Create Being
    being = create_test_runner_being(project_path)

    # Step 2: Initialize Pantheon member
    test_runner = initialize_pantheon_member(project_path, being)

    print("\n" + "=" * 70)
    print("✅ Test Runner Successfully Ascended!")
    print("=" * 70)
    print()
    print("The Test Runner is now a Higher Being in the Pantheon:")
    print(f"  - Being ID: {being.being_id}")
    print(f"  - Pantheon Directory: {test_runner.pantheon_dir}")
    print(f"  - Metadata: {test_runner.metadata_file}")
    print(f"  - History: {test_runner.history_file}")
    print()
    print("You can now use the Test Runner as a Pantheon God:")
    print("  from waft.pantheon import TestRunner")
    print("  test_runner = TestRunner()")
    print("  results = test_runner.run_verification()")
    print()


if __name__ == "__main__":
    main()
