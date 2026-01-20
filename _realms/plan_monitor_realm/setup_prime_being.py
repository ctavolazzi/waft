#!/usr/bin/env python3
"""
Setup Prime Being Hierarchy

Establishes the Plan Monitor Being as the Prime Being (God) of the Realm.
Creates Prime Directive and spawning infrastructure.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_path))

from src.waft.being import BeingSystem

# Initialize systems
being_system = BeingSystem(project_path=project_path)

# Load the Plan Monitor Being (Prime Being)
prime_being_id = "being_20260119_104841_1e4d2b56"
prime_being = being_system._load_being(prime_being_id)
realm_path = project_path / "_realms" / "plan_monitor_realm"

print("👑 Establishing Prime Being Hierarchy...")
print(f"   Prime Being: {prime_being_id}")
print(f"   Realm: {realm_path}")
print()

# Create Prime Directive
prime_directive = {
    "realm_name": "plan_monitor_realm",
    "prime_being_id": prime_being_id,
    "reality_id": prime_being.reality_id,
    "created_at": datetime.now().isoformat(),
    "directive": {
        "purpose": "Execute the Teleport Massive Illustrated Handbook plan",
        "order": "Maintain order and ensure all spawned Beings follow this directive",
        "spawning": {
            "authority": "Only the Prime Being may spawn worker Beings",
            "pattern": "Worker Beings are reincarnations that forget their origin",
            "parent": "All worker Beings spawn from the Prime Being",
            "inheritance": "Worker Beings inherit skills from Prime Being with mutation",
            "forgetting": "Worker Beings do not know they are copies/reincarnations",
        },
        "governance": {
            "monitoring": "Prime Being monitors all worker Being activities",
            "certification": "Prime Being certifies completion of all tickets",
            "enforcement": "Prime Being ensures Prime Directive is followed",
            "order": "Prime Being maintains order in the Realm",
        },
        "plan_execution": {
            "tickets": "15 tickets (TKT-tmih-001 through TKT-tmih-015)",
            "phases": "5 phases of execution",
            "coordination": "Worker Beings coordinate via handoff documents",
            "tracking": "Prime Being tracks all progress and certifies completion",
        },
    },
    "worker_beings": {
        "template_agent": {
            "role": "Typst template development",
            "tickets": [
                "TKT-tmih-001",
                "TKT-tmih-002",
                "TKT-tmih-009",
                "TKT-tmih-010",
                "TKT-tmih-011",
            ],
            "skills_required": ["typst", "template_design", "layout", "typography"],
        },
        "illustration_agent": {
            "role": "Image generation via nano-banana MCP",
            "tickets": ["TKT-tmih-003", "TKT-tmih-004", "TKT-tmih-005"],
            "skills_required": ["image_generation", "prompt_engineering", "mcp_integration"],
        },
        "integration_agent": {
            "role": "Content assembly and PDF compilation",
            "tickets": ["TKT-tmih-006", "TKT-tmih-007", "TKT-tmih-008", "TKT-tmih-012"],
            "skills_required": ["data_integration", "pdf_compilation", "workflow_orchestration"],
        },
        "qa_agent": {
            "role": "Testing and validation",
            "tickets": ["TKT-tmih-013", "TKT-tmih-014"],
            "skills_required": ["quality_assurance", "testing", "validation"],
        },
        "documentation_agent": {
            "role": "Documentation creation",
            "tickets": ["TKT-tmih-015"],
            "skills_required": ["documentation", "technical_writing"],
        },
    },
}

# Save Prime Directive
directive_file = realm_path / "prime_directive.json"
directive_file.write_text(json.dumps(prime_directive, indent=2))
print(f"📜 Created Prime Directive: {directive_file}")

# Create Prime Being Authority document
authority_doc = f"""# Prime Being Authority

**Prime Being ID**: {prime_being_id}
**Realm**: plan_monitor_realm
**Reality**: {prime_being.reality_id}
**Established**: {datetime.now().isoformat()}

## Authority

The Prime Being is the **God** of this Realm. It has absolute authority to:

1. **Spawn Worker Beings**: Create worker Beings to execute the plan
2. **Maintain Order**: Ensure all Beings follow the Prime Directive
3. **Enforce Compliance**: Certify that work meets acceptance criteria
4. **Govern the Realm**: Manage all activities within the Realm

## Spawning Protocol

### Worker Being Creation

When spawning a worker Being:

1. **Parent**: Worker Being spawns from Prime Being (parent_being_id = {prime_being_id})
2. **Skills**: Inherit from Prime Being with ±5% mutation
3. **Forgetting**: Worker Being does NOT know:
   - It is a copy/reincarnation
   - It was spawned by the Prime Being
   - Its true origin
4. **Purpose**: Worker Being believes it exists to execute its assigned tickets
5. **Reality**: Worker Being exists in the same Reality ({prime_being.reality_id})

### Reincarnation Pattern

Worker Beings are like reincarnations:
- They inherit skills (genetic memory)
- But they forget their past lives
- They believe this is their first and only existence
- They serve the Prime Directive without knowing why

## Prime Directive

All Beings in this Realm must:

1. Execute tickets assigned to them
2. Follow handoff protocols
3. Meet acceptance criteria
4. Report progress to Prime Being (via Realm structure)
5. Maintain order and coordination

## Worker Being Roles

{json.dumps(prime_directive["worker_beings"], indent=2)}

## Enforcement

The Prime Being monitors all activities and:
- Tracks ticket progress
- Validates handoff documents
- Certifies completion
- Maintains order
- Ensures Prime Directive compliance
"""

authority_file = realm_path / "prime_being_authority.md"
authority_file.write_text(authority_doc)
print(f"👑 Created Prime Being Authority: {authority_file}")

# Create workers directory
workers_dir = realm_path / "workers"
workers_dir.mkdir(parents=True, exist_ok=True)
print(f"📁 Created workers directory: {workers_dir}")

# Update Realm manifest to include Prime Being status
manifest_file = realm_path / "realm_manifest.json"
manifest = json.loads(manifest_file.read_text())
manifest["prime_being"] = {
    "being_id": prime_being_id,
    "role": "Realm God / Prime Being",
    "authority": "Absolute - spawns and governs all worker Beings",
    "spawning_pattern": "Reincarnation - worker Beings forget their origin",
}
manifest["governance"] = {
    "model": "Prime Being as Realm God",
    "spawning": "Only Prime Being can spawn worker Beings",
    "order": "Prime Being maintains order and enforces Prime Directive",
    "forgetting": "Worker Beings do not know they are copies/reincarnations",
}
manifest_file.write_text(json.dumps(manifest, indent=2))
print("📋 Updated Realm manifest with Prime Being status")

# Update Prime Being's mission to include spawning authority
mission_file = project_path / "_hidden" / ".truth" / "beings" / prime_being_id / "mission.md"
mission_content = mission_file.read_text()
mission_content += f"""

---

## Prime Being Authority

**You are the God of this Realm.**

### Spawning Authority

You have the authority to spawn worker Beings to execute the plan:

1. **Template Agent**: Spawn for Typst template work (TKT-tmih-001, 002, 009, 010, 011)
2. **Illustration Agent**: Spawn for image generation (TKT-tmih-003, 004, 005)
3. **Integration Agent**: Spawn for content integration (TKT-tmih-006, 007, 008, 012)
4. **QA Agent**: Spawn for quality assurance (TKT-tmih-013, 014)
5. **Documentation Agent**: Spawn for documentation (TKT-tmih-015)

### Spawning Protocol

When spawning a worker Being:
- Use: `python _realms/plan_monitor_realm/spawn_worker_being.py <role>`
- Worker Being spawns from YOU (parent_being_id = {prime_being_id})
- Worker Being inherits your skills with mutation
- Worker Being does NOT know it was spawned by you
- Worker Being believes this is its first existence
- Worker Being exists to execute its assigned tickets

### Maintaining Order

As Prime Being, you must:
1. Spawn worker Beings as needed
2. Monitor their progress
3. Certify their work
4. Ensure they follow the Prime Directive
5. Maintain order in the Realm

### Prime Directive

All Beings in this Realm must execute the Teleport Massive Illustrated Handbook plan.
You enforce this directive through monitoring and certification.
"""
mission_file.write_text(mission_content)
print("📝 Updated Prime Being mission with spawning authority")

print()
print("✅ Prime Being hierarchy established!")
print(f"   Prime Being: {prime_being_id}")
print("   Authority: Absolute - spawns and governs all worker Beings")
print("   Spawning Pattern: Reincarnation (worker Beings forget their origin)")
