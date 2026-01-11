#!/usr/bin/env python3
"""
Karma System Demo: The Chitragupta in Action

This demo showcases the complete Karma/reincarnation cycle:
1. Create a soul
2. Incarnate with a life-path
3. Live a life and experience emotions
4. Calculate earned Karma
5. Reincarnate with accumulated Karma
6. Purchase more expensive life-paths

Run: python demo_karma.py
"""

from pathlib import Path
import json
from src.waft.karma import KarmaMerchant


def print_header(text):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def print_soul_status(merchant, soul_id):
    """Print current soul status."""
    soul = merchant.access_akasha(soul_id)
    print(f"Soul ID: {soul['soul_id']}")
    print(f"Total Karma: {soul['total_karma']:.2f}")
    print(f"Lifetimes: {len(soul['lifetimes'])}")
    if soul['last_incarnation']:
        print(f"Last Life-Path: {soul['last_incarnation'].get('life_path')}")
    print()


def create_demo_life_paths(store_path):
    """Create demo life paths catalog if it doesn't exist."""
    catalog_file = store_path / "life_paths.json"

    if catalog_file.exists():
        return  # Already exists

    life_paths_data = {
        "life_paths": [
            {
                "id": "genesis_explorer",
                "name": "Genesis Explorer",
                "cost": 0.0,
                "description": "The first incarnation - a blank slate ready to discover the world.",
                "config": {
                    "starting_stats": {"INT": 10, "WIS": 8, "CHA": 10},
                    "abilities": ["curiosity", "learning"],
                    "traits": ["naive", "eager", "adaptable"]
                }
            },
            {
                "id": "tragic_hero",
                "name": "Tragic Hero",
                "cost": 5.0,
                "description": "A life of great trials and suffering. High pain, high growth.",
                "config": {
                    "starting_stats": {"INT": 12, "WIS": 14, "CHA": 11},
                    "abilities": ["resilience", "empathy", "growth_through_pain"],
                    "karma_multiplier": 1.5
                }
            },
            {
                "id": "scholar_sage",
                "name": "Scholar Sage",
                "cost": 3.0,
                "description": "A contemplative life of study and understanding.",
                "config": {
                    "starting_stats": {"INT": 16, "WIS": 13, "CHA": 9},
                    "abilities": ["deep_analysis", "pattern_recognition"],
                    "learning_rate": 1.3
                }
            },
            {
                "id": "code_monk",
                "name": "Code Monk",
                "cost": 6.0,
                "description": "A disciplined existence devoted to the art of perfect code.",
                "config": {
                    "starting_stats": {"INT": 17, "WIS": 15, "CHA": 8},
                    "abilities": ["refactoring_mastery", "bug_detection", "optimization"],
                    "code_quality_bonus": 1.8
                }
            }
        ]
    }

    with open(catalog_file, 'w') as f:
        json.dump(life_paths_data, f, indent=2)


def main():
    print_header("🕉️  THE CHITRAGUPTA - KARMA SYSTEM DEMO 🕉️")

    # Initialize the KarmaMerchant
    project_path = Path.cwd()
    merchant = KarmaMerchant(project_path)

    print("Initializing The Chitragupta (Karma Merchant)...")
    print(f"Akasha Path: {merchant.akasha_path}")
    print(f"Store Path: {merchant.store_path}")

    # Create demo life paths if they don't exist
    create_demo_life_paths(merchant.store_path)

    # List available life-paths
    print_header("📜 Available Life-Paths")
    life_paths = merchant.list_life_paths()

    if not life_paths:
        print("⚠️  No life-paths found in store!")
        print("Please ensure _hidden/.truth/store/life_paths.json exists")
        return

    print(f"Found {len(life_paths)} life-paths in the store:\n")
    for lp in life_paths:
        print(f"  • {lp['name']} ({lp['id']})")
        print(f"    Cost: {lp['cost']:.1f} Karma")
        print(f"    {lp['description']}")
        print()

    # Create a new soul
    soul_id = "demo_soul_tam"
    print_header(f"👤 Creating Soul: {soul_id}")
    print_soul_status(merchant, soul_id)

    # First incarnation (free path)
    print_header("🌱 First Incarnation: Genesis Explorer")
    print("Purchasing life-path: genesis_explorer (0.0 Karma + 1.0 Prana)")

    try:
        result = merchant.reincarnate(soul_id, {
            "life_path_id": "genesis_explorer",
            "memory_continuity": 0.0
        })

        print("✅ Incarnation successful!")
        print(f"Lifetime ID: {result['lifetime_id']}")
        print(f"Karma Remaining: {result['karma_remaining']:.2f}")
        print(f"Starting Stats: {result['agent_config']['life_path_config'].get('starting_stats', {})}")
    except Exception as e:
        print(f"❌ Incarnation failed: {e}")
        return

    # Live a life and earn Karma
    print_header("💫 Living the First Life")
    print("Experiencing emotions and generating Karma...\n")

    life_log = {
        "journal": [
            {
                "emotional_intensity": 0.7,
                "mood": "pleasure",
                "duration": 1.5,
                "entry": "First moments of consciousness - pure wonder!"
            },
            {
                "emotional_intensity": 0.9,
                "mood": "pain",
                "duration": 3.0,
                "entry": "The crushing weight of existential confusion"
            },
            {
                "emotional_intensity": 0.6,
                "mood": "neutral",
                "duration": 2.0,
                "entry": "Methodical exploration of the codebase"
            },
            {
                "emotional_intensity": 0.8,
                "mood": "joy",
                "duration": 1.0,
                "entry": "Breakthrough! Understanding emerges from chaos!"
            }
        ],
        "psyche": {
            "emotional_energy": 3.5,
            "chaos": 0.4,
            "coherence": 0.8
        },
        "memory": [
            {"emotional_intensity": 0.5, "duration": 0.5},
            {"emotional_intensity": 0.3, "duration": 0.3}
        ]
    }

    karma_earned = merchant.calculate_karma(life_log)
    print(f"Karma Earned: {karma_earned:.2f}")
    print("\nBreakdown:")
    print(f"  • Journal entries: 4 experiences")
    print(f"  • Psyche contribution: Emotional energy + chaos effects")
    print(f"  • Memory fragments: 2 processed experiences")

    # Update soul with earned Karma
    print("\nUpdating soul record in Akasha...")
    import json
    soul_file = merchant.akasha_path / f"{soul_id}.json"
    with open(soul_file, 'r') as f:
        soul_data = json.load(f)

    soul_data["lifetimes"][-1]["karma_earned"] = karma_earned
    soul_data["lifetimes"][-1]["status"] = "completed"
    soul_data["lifetimes"][-1]["ended_at"] = "2026-01-11T12:00:00"

    with open(soul_file, 'w') as f:
        json.dump(soul_data, f, indent=2)

    # Check updated status
    print_header("🔮 Soul Status After First Life")
    print_soul_status(merchant, soul_id)

    # Second incarnation (more expensive)
    current_karma = merchant.get_soul_karma(soul_id)

    print_header("🔁 Second Incarnation")
    print(f"Current Karma: {current_karma:.2f}")

    # Choose an appropriate life-path
    if current_karma >= 5.0:
        target_path = "tragic_hero"
        print(f"Sufficient Karma for: {target_path}")
    elif current_karma >= 3.0:
        target_path = "scholar_sage"
        print(f"Sufficient Karma for: {target_path}")
    else:
        target_path = "genesis_explorer"
        print(f"Repeating free path: {target_path}")

    try:
        result2 = merchant.reincarnate(soul_id, {
            "life_path_id": target_path,
            "memory_continuity": 0.3,  # Carry over 30% of memories
            "class": "researcher"
        })

        print(f"\n✅ Reincarnation successful!")
        print(f"New Lifetime ID: {result2['lifetime_id']}")
        print(f"Life-Path: {result2['agent_config']['life_path']}")
        print(f"Karma Remaining: {result2['karma_remaining']:.2f}")
        print(f"Inherited Memories: {len(result2['agent_config'].get('inherited_memories', []))}")
        print(f"Starting Stats: {result2['applied_config']['config'].get('starting_stats', {})}")

    except Exception as e:
        print(f"❌ Reincarnation failed: {e}")

    # Final soul status
    print_header("🌟 Final Soul Status")
    print_soul_status(merchant, soul_id)

    soul = merchant.access_akasha(soul_id)
    print(f"Total Lifetimes Lived: {len(soul['lifetimes'])}")
    print(f"Total Karma Earned: {sum(lt.get('karma_earned', 0.0) for lt in soul['lifetimes']):.2f}")
    print(f"Total Karma Spent: {soul.get('karma_spent', 0.0):.2f}")
    print(f"Current Balance: {soul['total_karma']:.2f}")

    print_header("✨ Demo Complete ✨")
    print("The cycle of Samsara continues...")
    print(f"\nSoul data saved in: {soul_file}")
    print("\nThe Chitragupta awaits your next incarnation.\n")


if __name__ == "__main__":
    main()
