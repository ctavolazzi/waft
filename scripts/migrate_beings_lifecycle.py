#!/usr/bin/env python3
"""
Migration script to add new lifecycle attributes to existing beings.

Adds default values for:
- will_to_live, luck, decision_fatigue, pleasure, pain
- personality, goals, personality_type
- soul_id, sleep state, cycle tracking
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.being import BeingSystem


def migrate_being(being_system: BeingSystem, being_id: str) -> bool:
    """Migrate a single being to include new lifecycle attributes."""
    try:
        being = being_system._load_being(being_id)

        # Check if already migrated (has will_to_live attribute)
        if hasattr(being, "will_to_live") and being.will_to_live is not None:
            return True  # Already migrated

        # Add missing attributes with defaults
        if not hasattr(being, "will_to_live") or being.will_to_live is None:
            being.will_to_live = 100.0
        if not hasattr(being, "luck") or being.luck is None:
            being.luck = 50.0
        if not hasattr(being, "decision_fatigue") or being.decision_fatigue is None:
            # Calculate initial quota
            base_quota = 10
            personality_modifier = 0.0
            if hasattr(being, "personality_type"):
                modifiers = {
                    "analytical": 5.0,
                    "systematic": 5.0,
                    "creative": -2.0,
                    "intuitive": -2.0,
                    "balanced": 0.0,
                }
                personality_modifier = modifiers.get(being.personality_type, 0.0)
            skill_bonus = min(5, sum(being.skills.values()) / 100.0)
            being.decision_quota_max = int(base_quota + personality_modifier + skill_bonus)
            being.decision_fatigue = being.decision_quota_max
        if not hasattr(being, "pleasure") or being.pleasure is None:
            being.pleasure = 0.0
        if not hasattr(being, "pain") or being.pain is None:
            being.pain = 0.0
        if not hasattr(being, "personality") or being.personality is None:
            being.personality = {}
        if not hasattr(being, "goals") or being.goals is None:
            being.goals = []
        if not hasattr(being, "personality_type") or being.personality_type is None:
            being.personality_type = "balanced"
        if not hasattr(being, "soul_id") or being.soul_id is None:
            being.soul_id = f"soul_{being.being_id}"
        if not hasattr(being, "is_sleeping") or being.is_sleeping is None:
            being.is_sleeping = False
        if not hasattr(being, "sleep_duration") or being.sleep_duration is None:
            being.sleep_duration = 0
        if not hasattr(being, "sleep_duration_base") or being.sleep_duration_base is None:
            import random

            being.sleep_duration_base = random.randint(3, 10)
        if not hasattr(being, "cycles_slept") or being.cycles_slept is None:
            being.cycles_slept = 0
        if not hasattr(being, "last_cycle_number") or being.last_cycle_number is None:
            being.last_cycle_number = 0
        # Migrate cycles_alive to lifetimes
        if hasattr(being, "cycles_alive") and not hasattr(being, "lifetimes"):
            being.lifetimes = being.cycles_alive
            delattr(being, "cycles_alive")
        elif not hasattr(being, "lifetimes") or being.lifetimes is None:
            being.lifetimes = 0
        if not hasattr(being, "recent_experiences") or being.recent_experiences is None:
            being.recent_experiences = []

        # Save migrated being
        being_system._save_being(being)
        return True

    except Exception as e:
        print(f"Error migrating being {being_id}: {e}")
        return False


def main():
    """Main migration function."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Migrate existing beings to include lifecycle attributes"
    )
    parser.add_argument("--project-path", type=Path, default=Path.cwd(), help="Project root path")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't actually migrate, just show what would be done",
    )

    args = parser.parse_args()

    being_system = BeingSystem(project_path=args.project_path)
    beings_path = being_system.beings_path

    if not beings_path.exists():
        print(f"No beings directory found at {beings_path}")
        return

    being_files = list(beings_path.glob("*.json"))

    if not being_files:
        print("No beings found to migrate")
        return

    print(f"Found {len(being_files)} beings to migrate")

    migrated = 0
    failed = 0

    for being_file in being_files:
        being_id = being_file.stem
        if args.dry_run:
            print(f"Would migrate: {being_id}")
        else:
            if migrate_being(being_system, being_id):
                migrated += 1
                print(f"✅ Migrated: {being_id}")
            else:
                failed += 1
                print(f"❌ Failed: {being_id}")

    if not args.dry_run:
        print(f"\nMigration complete: {migrated} migrated, {failed} failed")


if __name__ == "__main__":
    main()
