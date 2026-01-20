#!/usr/bin/env python3
"""
Pyrite Demo
===========

Demonstrates Pyrite's capabilities:
- Locking system
- Monitoring
- Organization
- Evolutionary cycles
- Personality
- Secrets
- Empirica integration
"""

import json
import time
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.pyrite import get_pyrite, EvolutionaryStrategy, WorkEffortStatus


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def print_json(data: dict, indent: int = 2):
    """Print JSON data."""
    print(json.dumps(data, indent=indent, default=str))


def demo_think():
    """Demo: /think ability."""
    print_section("1. /think - Cognitive Systems")
    
    pyrite = get_pyrite()
    result = pyrite.execute_ability("/think")
    
    print("Pyrite's thoughts:")
    for thought in result.get("thoughts", []):
        print(f"  • {thought}")
    
    print("\nAttributes:")
    for name, value in result.get("attributes", {}).items():
        print(f"  {name}: {value:.3f}")
    
    print("\nAwareness:")
    awareness = result.get("awareness", {})
    print(f"  Work Efforts: {awareness.get('work_efforts', 0)}")
    print(f"  Active Cycles: {awareness.get('active_cycles', 0)}")
    print(f"  Locked: {awareness.get('locked_work_efforts', 0)}")
    print(f"  Secrets: {awareness.get('secrets', 0)}")
    
    print("\nEmpirica Status:")
    empirica = result.get("empirica", {})
    print(f"  Initialized: {empirica.get('initialized', False)}")
    print(f"  Session ID: {empirica.get('session_id', 'None')}")
    print(f"  Context Loaded: {empirica.get('context_loaded', False)}")


def demo_locking():
    """Demo: Locking system."""
    print_section("2. Locking System")
    
    pyrite = get_pyrite()
    
    # Find a work effort to lock
    we_id = None
    for we_id_test in list(pyrite._work_effort_graph.keys())[:5]:
        if not pyrite.is_locked(we_id_test):
            we_id = we_id_test
            break
    
    if not we_id:
        print("No work efforts available for locking demo")
        return
    
    print(f"Locking work effort: {we_id}")
    
    # Acquire lock
    lock_id = "demo-lock-001"
    success = pyrite.acquire_lock(we_id, lock_id, timeout=5.0)
    print(f"  Lock acquired: {success}")
    print(f"  Is locked: {pyrite.is_locked(we_id)}")
    print(f"  Lock holder: {pyrite.get_lock_holder(we_id)}")
    
    # Try to acquire again (should fail or wait)
    print(f"\nTrying to acquire lock again (should fail):")
    success2 = pyrite.acquire_lock(we_id, "demo-lock-002", timeout=1.0)
    print(f"  Second lock attempt: {success2}")
    
    # Release lock
    print(f"\nReleasing lock:")
    released = pyrite.release_lock(we_id, lock_id)
    print(f"  Lock released: {released}")
    print(f"  Is locked: {pyrite.is_locked(we_id)}")


def demo_monitoring():
    """Demo: Monitoring system."""
    print_section("3. Monitoring System")
    
    pyrite = get_pyrite()
    
    # Monitor all
    print("Monitoring all work efforts:")
    result = pyrite.execute_ability("/monitor")
    print(f"  Total: {result.get('total_work_efforts', 0)}")
    print(f"  Active: {result.get('active', 0)}")
    print(f"  Locked: {result.get('locked', 0)}")
    print(f"  Active Cycles: {result.get('active_cycles', 0)}")
    
    # Monitor specific
    we_ids = list(pyrite._work_effort_graph.keys())[:3]
    for we_id in we_ids:
        print(f"\nMonitoring {we_id}:")
        result = pyrite.execute_ability("/monitor", we_id)
        if "error" not in result:
            print(f"  Status: {result.get('status')}")
            print(f"  Fitness: {result.get('fitness', 0.0):.3f}")
            print(f"  Generation: {result.get('generation', 0)}")
            print(f"  Is Locked: {result.get('is_locked', False)}")


def demo_organization():
    """Demo: Organization system."""
    print_section("4. Organization System")
    
    pyrite = get_pyrite()
    
    result = pyrite.execute_ability("/organize")
    print(f"Total Nodes: {result.get('total_nodes', 0)}")
    print(f"Root Nodes: {result.get('roots', 0)}")
    print(f"Orphan Nodes: {len(result.get('orphans', []))}")
    
    # Show some work efforts
    print("\nSample Work Efforts:")
    for i, (we_id, node) in enumerate(list(pyrite._work_effort_graph.items())[:5]):
        print(f"  {i+1}. {we_id}")
        print(f"     Title: {node.title[:50]}...")
        print(f"     Status: {node.status.value}")
        print(f"     Fitness: {node.fitness:.3f}")
        print(f"     Generation: {node.generation}")


def demo_personality():
    """Demo: Personality system."""
    print_section("5. Personality System")
    
    pyrite = get_pyrite()
    
    personality = pyrite.get_personality_summary()
    
    print("Attributes:")
    for name, value in personality.get("attributes", {}).items():
        print(f"  {name}: {value:.3f}")
    
    print("\nMetadata:")
    metadata = personality.get("metadata", {})
    print(f"  Created: {metadata.get('created', 'Unknown')}")
    print(f"  Total Cycles: {metadata.get('total_cycles', 0)}")
    print(f"  Total Evolutions: {metadata.get('total_evolutions', 0)}")
    print(f"  Total Work Efforts: {personality.get('total_work_efforts', 0)}")
    print(f"  Total Secrets: {personality.get('total_secrets', 0)}")
    
    # Grow attributes
    print("\nGrowing attributes...")
    pyrite.grow_attributes()
    personality_after = pyrite.get_personality_summary()
    
    print("Attributes after growth:")
    for name, value in personality_after.get("attributes", {}).items():
        old_value = personality.get("attributes", {}).get(name, 0)
        growth = value - old_value
        print(f"  {name}: {value:.3f} (+{growth:.4f})")


def demo_secrets():
    """Demo: Secrets system."""
    print_section("6. Secrets System")
    
    pyrite = get_pyrite()
    
    # Create a secret
    print("Creating a secret...")
    secret_data = {
        "api_key": "sk-secret-key-12345",
        "password": "super-secret-password",
        "hidden_plan": "Take over the world"
    }
    secret_metadata = {
        "service": "Demo API",
        "created_by": "demo_script",
        "note": "This is visible metadata"
    }
    
    secret_id = pyrite.create_secret(secret_data, secret_metadata)
    print(f"  Secret created: {secret_id}")
    
    # Get metadata (visible)
    print("\nSecret metadata (visible to Pyrite):")
    metadata = pyrite.get_secret_metadata(secret_id)
    print_json(metadata)
    
    # List all secrets
    print("\nAll secrets (metadata only):")
    secrets = pyrite.list_secrets()
    print(f"  Total secrets: {len(secrets)}")
    for secret in secrets:
        print(f"  • {secret['secret_id']}")
        print(f"    Created: {secret['created']}")
        print(f"    Access Count: {secret['access_count']}")
        print(f"    Metadata: {secret['metadata']}")


def demo_evolution():
    """Demo: Evolutionary cycles."""
    print_section("7. Evolutionary Cycles")
    
    pyrite = get_pyrite()
    
    # Find a work effort to evolve
    we_id = None
    for we_id_test in list(pyrite._work_effort_graph.keys())[:10]:
        if not pyrite.is_locked(we_id_test):
            we_id = we_id_test
            break
    
    if not we_id:
        print("No work efforts available for evolution demo")
        return
    
    print(f"Evolving work effort: {we_id}")
    
    # Get initial state
    node = pyrite.get_work_effort(we_id)
    if node:
        print(f"  Initial fitness: {node.fitness:.3f}")
        print(f"  Initial generation: {node.generation}")
    
    # Initiate evolution
    print(f"\nInitiating evolution (adaptive strategy, 3 variants)...")
    result = pyrite.execute_ability("/evolve", we_id, "adaptive", 3)
    
    if result.get("status") == "success":
        print(f"  Cycle ID: {result.get('cycle_id')}")
        print(f"  Generation: {result.get('generation')}")
        print(f"  Variants: {result.get('variants')}")
        print(f"  Selected Variant: {result.get('selected_variant')}")
        print(f"  Fitness: {result.get('fitness', 0.0):.3f}")
        print(f"  Empirica Goal Created: {result.get('empirica', {}).get('goal_created', False)}")
        
        # Get evolutionary history
        print(f"\nEvolutionary history for {we_id}:")
        history = pyrite.get_evolutionary_history(we_id)
        print(f"  Total cycles: {len(history)}")
        for i, cycle in enumerate(history[-3:], 1):  # Show last 3
            print(f"  {i}. Generation {cycle.generation} - Fitness: {cycle.fitness_scores.get(cycle.selected_variant, 0.0):.3f}")
    else:
        print(f"  Evolution failed: {result.get('error')}")


def demo_status():
    """Demo: Status ability."""
    print_section("8. Status - Complete System State")
    
    pyrite = get_pyrite()
    
    result = pyrite.execute_ability("/status")
    
    print("Personality:")
    personality = result.get("personality", {})
    print(f"  Total Work Efforts: {personality.get('total_work_efforts', 0)}")
    print(f"  Total Cycles: {personality.get('metadata', {}).get('total_cycles', 0)}")
    print(f"  Total Secrets: {personality.get('total_secrets', 0)}")
    
    print("\nWork Efforts by Status:")
    by_status = result.get("work_efforts", {}).get("by_status", {})
    for status, count in by_status.items():
        if count > 0:
            print(f"  {status}: {count}")
    
    print("\nLocks:")
    locks = result.get("locks", {})
    print(f"  Total: {locks.get('total', 0)}")
    
    print("\nEvolution:")
    evolution = result.get("evolution", {})
    print(f"  Active Cycles: {evolution.get('active_cycles', 0)}")
    print(f"  Total Cycles: {evolution.get('total_cycles', 0)}")


def main():
    """Run all demos."""
    print("\n" + "="*60)
    print("  THE STEWARD DEMO - The God of Work Efforts")
    print("="*60)
    
    try:
        demo_think()
        time.sleep(1)
        
        demo_locking()
        time.sleep(1)
        
        demo_monitoring()
        time.sleep(1)
        
        demo_organization()
        time.sleep(1)
        
        demo_personality()
        time.sleep(1)
        
        demo_secrets()
        time.sleep(1)
        
        demo_evolution()
        time.sleep(1)
        
        demo_status()
        
        print_section("Demo Complete!")
        print("Pyrite has demonstrated:")
        print("  ✅ Cognitive systems (/think)")
        print("  ✅ Locking system")
        print("  ✅ Monitoring system")
        print("  ✅ Organization system")
        print("  ✅ Personality system")
        print("  ✅ Secrets system")
        print("  ✅ Evolutionary cycles")
        print("  ✅ Complete status")
        print("  ✅ Empirica integration")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
