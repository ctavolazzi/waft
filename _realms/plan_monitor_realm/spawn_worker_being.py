#!/usr/bin/env python3
"""
Prime Being Spawning Script

Allows the Prime Being to spawn worker Beings into the Realm.
Worker Beings are reincarnations that forget their origin.
"""

from pathlib import Path
import json
import sys
import hashlib

# Add project root to path
project_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_path))

from src.waft.being import BeingSystem

# Initialize
being_system = BeingSystem(project_path=project_path)

# Prime Being ID
PRIME_BEING_ID = 'being_20260119_104841_1e4d2b56'
REALM_PATH = project_path / '_realms' / 'plan_monitor_realm'

def load_prime_directive():
    """Load Prime Directive to understand worker Being requirements."""
    directive_file = REALM_PATH / 'prime_directive.json'
    if directive_file.exists():
        return json.loads(directive_file.read_text())
    return None

def spawn_worker_being(role: str, ticket_ids: list, skills_required: list):
    """
    Spawn a worker Being from the Prime Being.
    
    Worker Being will:
    - Spawn from Prime Being (inherits skills with mutation)
    - Forget its origin (doesn't know it's a copy)
    - Believe it exists to execute its assigned tickets
    - Exist in the same Reality as Prime Being
    """
    directive = load_prime_directive()
    if not directive:
        print('❌ Prime Directive not found')
        return None
    
    # Load Prime Being to inherit skills
    prime_being = being_system._load_being(PRIME_BEING_ID)
    REALITY_ID = prime_being.reality_id
    
    # Create initial skills based on role requirements
    # Inherit from Prime Being, then add role-specific skills
    initial_skills = {}
    
    # Inherit monitoring/certification skills from Prime Being (with mutation)
    for skill_name, skill_level in prime_being.skills.items():
        # Slight mutation (±5%)
        mutation = hashlib.sha256(f'{role}{skill_name}'.encode()).hexdigest()[:2]
        mutation_factor = (int(mutation, 16) / 255.0 - 0.5) * 0.1
        initial_skills[skill_name] = max(0.0, min(100.0, skill_level * (1.0 + mutation_factor)))
    
    # Add role-specific skills (moderate level, worker Beings are capable)
    for skill in skills_required:
        if skill not in initial_skills:
            initial_skills[skill] = 40.0  # Moderate capability
    
    # Spawn worker Being from Prime Being
    worker = being_system.spawn_being(
        reality_id=REALITY_ID,
        parent_being_id=PRIME_BEING_ID,  # Spawns from Prime Being
        initial_skills=initial_skills
    )
    
    # Create worker Being mission (they don't know they're a copy)
    worker_dir = project_path / '_hidden' / '.truth' / 'beings' / worker.being_id
    worker_dir.mkdir(parents=True, exist_ok=True)
    
    ticket_list = '\n'.join(f'- {ticket}' for ticket in ticket_ids)
    skills_json = json.dumps(worker.skills, indent=2)
    
    mission_content = f'''# Worker Being Mission

**Being ID**: {worker.being_id}
**Role**: {role}
**Tickets**: {', '.join(ticket_ids)}

## Purpose

You exist to execute the following tickets:
{ticket_list}

## Your Reality

You exist in Reality: {REALITY_ID}
You are here to serve the plan execution.

## Skills

{skills_json}

## Your Purpose

Execute your assigned tickets with excellence.
Follow handoff protocols.
Meet all acceptance criteria.
Report progress through the Realm structure.

---

*Note: This Being does not know it was spawned by the Prime Being.
It believes this is its first and only existence.*
'''
    
    mission_file = worker_dir / 'mission.md'
    mission_file.write_text(mission_content)
    
    # Register worker Being in Realm
    workers_file = REALM_PATH / 'workers' / f'{worker.being_id}.json'
    workers_file.parent.mkdir(parents=True, exist_ok=True)
    
    worker_registry = {
        'being_id': worker.being_id,
        'role': role,
        'tickets': ticket_ids,
        'spawned_by': PRIME_BEING_ID,
        'spawned_at': worker.created_at,
        'reality_id': REALITY_ID,
        'skills': worker.skills,
        'lifetimes': worker.lifetimes,
        'forgets_origin': True  # Worker Being doesn't know it's a copy
    }
    
    workers_file.write_text(json.dumps(worker_registry, indent=2))
    
    return worker

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python spawn_worker_being.py <role>')
        print('Roles: template_agent, illustration_agent, integration_agent, qa_agent, documentation_agent')
        sys.exit(1)
    
    role = sys.argv[1]
    directive = load_prime_directive()
    
    if not directive or role not in directive['worker_beings']:
        print(f'❌ Unknown role: {role}')
        sys.exit(1)
    
    worker_config = directive['worker_beings'][role]
    worker = spawn_worker_being(
        role=role,
        ticket_ids=worker_config['tickets'],
        skills_required=worker_config['skills_required']
    )
    
    if worker:
        print(f'✅ Worker Being spawned: {worker.being_id}')
        print(f'   Role: {role}')
        print(f'   Tickets: {", ".join(worker_config["tickets"])}')
        print(f'   Reality: {worker.reality_id}')
        print(f'   Parent: {worker.parent_being_id} (Prime Being)')
        print(f'   Lifetimes: {worker.lifetimes} (Reincarnation)')
        print(f'   Skills: {len(worker.skills)} skills inherited')
        print()
        print('⚠️  Worker Being does NOT know it was spawned by Prime Being')
        print('   It believes this is its first and only existence.')
