#!/usr/bin/env python3
"""
Spawn Hotel Staff Beings
========================

Spawns all hotel staff members as Beings and evolves them to handle their roles.
"""

import sys
from pathlib import Path
from datetime import datetime
import json

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from src.waft.being import BeingSystem, Being


# Staff definitions
STAFF_ROLES = {
    "housekeeping": {
        "name": "Housekeeping",
        "reality_id": "treasure_tavern_inn",
        "initial_skills": {
            "organization": 25.0,
            "refactoring": 20.0,
            "code_structure": 22.0,
            "tidying": 28.0
        },
        "personality_type": "perfectionist",
        "custom_name": "Martha"
    },
    "janitor": {
        "name": "Janitor",
        "reality_id": "treasure_tavern_inn",
        "initial_skills": {
            "cleanup": 30.0,
            "error_handling": 25.0,
            "reactive_fixes": 28.0,
            "temporary_cleanup": 32.0
        },
        "personality_type": "reactive",
        "custom_name": "Carl"
    },
    "concierge": {
        "name": "Concierge",
        "reality_id": "treasure_tavern_inn",
        "initial_skills": {
            "information_architecture": 30.0,
            "knowledge_management": 28.0,
            "routing": 25.0,
            "memory": 35.0
        },
        "personality_type": "helpful",
        "custom_name": "Arthur"
    },
    "front_desk": {
        "name": "Front Desk",
        "reality_id": "treasure_tavern_inn",
        "initial_skills": {
            "request_handling": 28.0,
            "routing": 30.0,
            "professionalism": 32.0,
            "efficiency": 30.0
        },
        "personality_type": "professional",
        "custom_name": "Sarah"
    },
    "bellhop": {
        "name": "Bellhop",
        "reality_id": "treasure_tavern_inn",
        "initial_skills": {
            "file_operations": 28.0,
            "data_transfer": 30.0,
            "careful_handling": 32.0,
            "detail_oriented": 28.0
        },
        "personality_type": "energetic",
        "custom_name": "Tommy"
    },
    "maintenance": {
        "name": "Maintenance",
        "reality_id": "treasure_tavern_inn",
        "initial_skills": {
            "system_health": 30.0,
            "bug_fixes": 28.0,
            "preventive_maintenance": 25.0,
            "technical_skills": 32.0
        },
        "personality_type": "technical",
        "custom_name": "Frank"
    },
    "night_auditor": {
        "name": "Night Auditor",
        "reality_id": "treasure_tavern_inn",
        "initial_skills": {
            "code_review": 30.0,
            "auditing": 28.0,
            "analysis": 32.0,
            "detail_oriented": 30.0
        },
        "personality_type": "analytical",
        "custom_name": "Vera"
    },
    "manager": {
        "name": "Manager",
        "reality_id": "treasure_tavern_inn",
        "initial_skills": {
            "orchestration": 35.0,
            "coordination": 32.0,
            "leadership": 30.0,
            "workflow_management": 28.0
        },
        "personality_type": "leadership",
        "custom_name": "Marcus"
    },
    "chef": {
        "name": "Chef",
        "reality_id": "treasure_tavern_inn",
        "initial_skills": {
            "code_generation": 30.0,
            "transformations": 28.0,
            "pattern_following": 32.0,
            "creativity": 25.0
        },
        "personality_type": "creative",
        "custom_name": "Pierre"
    },
    "server": {
        "name": "Server",
        "reality_id": "treasure_tavern_inn",
        "initial_skills": {
            "api_routing": 30.0,
            "service_delivery": 28.0,
            "efficiency": 32.0,
            "attention": 30.0
        },
        "personality_type": "attentive",
        "custom_name": "Emma"
    }
}


def spawn_staff_member(being_system: BeingSystem, role_key: str, role_def: dict) -> Being:
    """Spawn a single staff member."""
    print(f"  🏨 Spawning {role_def['name']} ({role_def['custom_name']})...")
    
    being = being_system.spawn_being(
        reality_id=role_def["reality_id"],
        parent_being_id=None,  # Spawn from Source
        initial_skills=role_def["initial_skills"]
    )
    
    # Set custom name
    being.custom_name = role_def["custom_name"]
    
    # Save staff metadata
    staff_dir = project_root / "hotel_staff" / "beings"
    staff_dir.mkdir(parents=True, exist_ok=True)
    
    staff_file = staff_dir / f"{role_key}_{being.being_id}.json"
    staff_data = {
        "role_key": role_key,
        "role_name": role_def["name"],
        "being_id": being.being_id,
        "custom_name": role_def["custom_name"],
        "reality_id": role_def["reality_id"],
        "initial_skills": role_def["initial_skills"],
        "personality_type": role_def["personality_type"],
        "spawned_at": datetime.now().isoformat()
    }
    
    staff_file.write_text(json.dumps(staff_data, indent=2))
    
    print(f"    ✅ {role_def['custom_name']} spawned: {being.being_id}")
    
    return being


def main():
    """Spawn all hotel staff."""
    print("=" * 70)
    print("SPAWNING HOTEL STAFF - The Inn at TreasureTavern")
    print("=" * 70)
    print()
    
    being_system = BeingSystem(project_path=project_root)
    
    spawned = {}
    
    for role_key, role_def in STAFF_ROLES.items():
        being = spawn_staff_member(being_system, role_key, role_def)
        spawned[role_key] = {
            "being": being,
            "role": role_def
        }
        print()
    
    print("=" * 70)
    print(f"✅ Spawned {len(spawned)} staff members")
    print()
    print("Staff Roster:")
    for role_key, data in spawned.items():
        print(f"  - {data['role']['custom_name']} ({data['role']['name']})")
    print()
    print("Next: Use /evolve to develop each staff member's skills!")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
