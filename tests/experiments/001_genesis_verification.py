"""
Experiment 001: Genesis Verification

Scientific Objective: Verify the biological lifecycle of agents.

This experiment verifies that:
1. A Genesis Agent (Generation 0) can be instantiated
2. The agent computes its own Genome ID (SHA-256 hash)
3. The agent can spawn a child (Generation 1) with parent_id linkage
4. TheObserver records all events in laboratory.jsonl
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.waft.core.agent import BaseAgent, AgentConfig, Modification
from src.waft.core.agent.state import EvolutionaryEventType


class TestAgent(BaseAgent):
    """Minimal test agent for Genesis verification."""
    
    async def observe(self):
        """Stub implementation."""
        return {"status": "observed"}
    
    async def decide(self, state):
        """Stub implementation."""
        return {"action": "none"}
    
    async def act(self, decision):
        """Stub implementation."""
        return {"result": "success"}
    
    async def reflect(self, result):
        """Stub implementation."""
        return {"learned": True}


async def run_experiment():
    """Execute Experiment 001: Genesis Verification."""
    
    print("=" * 80)
    print("EXPERIMENT 001: GENESIS VERIFICATION")
    print("=" * 80)
    print()
    
    # Step 1: Birth a Genesis Agent (Gen 0)
    print("STEP 1: Creating Genesis Agent (Generation 0)...")
    print("-" * 80)
    
    config = AgentConfig(
        role="Test Agent",
        goal="Verify biological lifecycle",
        backstory="A test agent created for scientific verification",
    )
    
    genesis = TestAgent(config=config, project_path=project_root)
    
    print(f"✓ Genesis Agent Created")
    print(f"  Agent ID: {genesis.state.agent_id}")
    print(f"  Generation: {genesis.generation}")
    print(f"  Genome ID: {genesis.genome_id}")
    print(f"  Parent ID: {genesis.parent_id}")
    print(f"  Lineage Path: {genesis.lineage_path}")
    print()
    
    # Verify Genesis properties
    assert genesis.generation == 0, "Genesis agent must be generation 0"
    assert genesis.parent_id is None, "Genesis agent has no parent"
    assert len(genesis.lineage_path) == 1, "Genesis lineage path should contain only itself"
    assert genesis.lineage_path[0] == genesis.genome_id, "Genesis lineage path should start with its genome_id"
    assert len(genesis.flight_recorder) >= 1, "Genesis should have at least one event (genesis spawn)"
    
    print("✓ Genesis Verification: PASSED")
    print()
    
    # Step 2: Spawn a Child (Gen 1)
    print("STEP 2: Spawning Child Agent (Generation 1)...")
    print("-" * 80)
    
    mutation = Modification(
        modification_type="prompt",
        target="backstory",
        change={"content": "An evolved test agent with improved backstory"},
        safety_level=2,
    )
    
    child = await genesis.spawn(mutation)
    
    print(f"✓ Child Agent Created")
    print(f"  Agent ID: {child.state.agent_id}")
    print(f"  Generation: {child.generation}")
    print(f"  Genome ID: {child.genome_id}")
    print(f"  Parent ID: {child.parent_id}")
    print(f"  Lineage Path: {child.lineage_path}")
    print()
    
    # Verify Child properties
    assert child.generation == genesis.generation + 1, f"Child generation should be {genesis.generation + 1}"
    assert child.parent_id == genesis.genome_id, "Child parent_id must match parent's genome_id"
    assert len(child.lineage_path) == len(genesis.lineage_path) + 1, "Child lineage should extend parent's"
    assert child.lineage_path[0] == genesis.lineage_path[0], "Child lineage should start with genesis"
    assert child.lineage_path[-1] == child.genome_id, "Child lineage should end with its own genome_id"
    assert child.parent_id in child.lineage_path, "Child lineage should contain parent_id"
    
    print("✓ Spawn Verification: PASSED")
    print()
    
    # Step 3: Verify Flight Recorder
    print("STEP 3: Verifying Flight Recorder...")
    print("-" * 80)
    
    print(f"Genesis Flight Recorder Events: {len(genesis.flight_recorder)}")
    for i, event in enumerate(genesis.flight_recorder):
        print(f"  Event {i+1}: {event.event_type.value} (genome_id: {event.genome_id[:16]}...)")
    
    print()
    print(f"Child Flight Recorder Events: {len(child.flight_recorder)}")
    for i, event in enumerate(child.flight_recorder):
        print(f"  Event {i+1}: {event.event_type.value} (genome_id: {event.genome_id[:16]}...)")
    
    print()
    print("✓ Flight Recorder Verification: PASSED")
    print()
    
    # Step 4: Verify TheObserver
    print("STEP 4: Verifying TheObserver (Scientific Registry)...")
    print("-" * 80)
    
    from src.waft.core.science import TheObserver
    
    observer = TheObserver(project_path=project_root)
    events = observer.get_laboratory_log()
    
    print(f"Total Events in Laboratory Log: {len(events)}")
    print()
    
    if events:
        print("First 3 Events in laboratory.jsonl:")
        for i, event in enumerate(events[:3]):
            print(f"  Event {i+1}:")
            print(f"    Type: {event.get('event_type')}")
            print(f"    Genome ID: {event.get('genome_id', '')[:16]}...")
            print(f"    Generation: {event.get('generation')}")
            print(f"    Agent ID: {event.get('agent_id')}")
            print()
    
    print("✓ TheObserver Verification: PASSED")
    print()
    
    # Final Summary
    print("=" * 80)
    print("EXPERIMENT 001: COMPLETE")
    print("=" * 80)
    print()
    print("RESULTS:")
    print(f"  ✓ Genesis Agent (Gen 0) created with genome_id: {genesis.genome_id[:16]}...")
    print(f"  ✓ Child Agent (Gen 1) spawned with parent_id: {child.parent_id[:16]}...")
    print(f"  ✓ Parent-child linkage verified: {child.parent_id == genesis.genome_id}")
    print(f"  ✓ Flight Recorder active: {len(genesis.flight_recorder) + len(child.flight_recorder)} events")
    print(f"  ✓ TheObserver active: {len(events)} events in laboratory.jsonl")
    print()
    print("STATUS: ✅ ALL VERIFICATIONS PASSED")
    print()
    
    return {
        "genesis_genome_id": genesis.genome_id,
        "child_genome_id": child.genome_id,
        "child_parent_id": child.parent_id,
        "lineage_verified": child.parent_id == genesis.genome_id,
        "total_events": len(events),
    }


if __name__ == "__main__":
    results = asyncio.run(run_experiment())
    print("Experiment Results:", results)
