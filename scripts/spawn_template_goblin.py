#!/usr/bin/env python3
"""
Spawn TemplateGoblin Being
==========================

Creates a new Being called "TemplateGoblin" to manage the WAFT template library.
TemplateGoblin will be responsible for:
- Tracking templates
- Answering template requests
- Managing template metadata
- Serving as the Template API for WAFT
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.being import BeingSystem


def spawn_template_goblin():
    """Spawn the TemplateGoblin Being."""
    print("🔮 Spawning TemplateGoblin Being...")

    # Initialize Being System
    being_system = BeingSystem(project_path=project_root)

    # Initial skills for template management
    initial_skills = {
        "template_management": 75.0,
        "template_discovery": 70.0,
        "template_validation": 65.0,
        "template_creation": 60.0,
        "metadata_management": 70.0,
        "api_design": 65.0,
        "documentation": 60.0,
        "organization": 75.0,
    }

    # Spawn Being from Source
    being = being_system.spawn_being(
        reality_id="template_library_reality",
        parent_being_id=None,  # Spawns from Source
        initial_skills=initial_skills,
    )

    # Set custom name
    being.custom_name = "TemplateGoblin"
    being_system._save_being(being)

    print("\n✅ TemplateGoblin spawned successfully!")
    print(f"   Being ID: {being.being_id}")
    print(f"   Custom Name: {being.custom_name}")
    print(f"   Reality: {being.reality_id}")
    print(f"   Lifetimes: {being.lifetimes}")
    print("\n📚 Initial Skills:")
    for skill, level in sorted(being.skills.items(), key=lambda x: x[1], reverse=True):
        print(f"   - {skill}: {level:.1f}")

    print("\n🎯 TemplateGoblin is ready to manage the template library!")
    print(f"   Location: {being_system.beings_path / being.being_id}.json")

    return being


if __name__ == "__main__":
    try:
        being = spawn_template_goblin()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error spawning TemplateGoblin: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
