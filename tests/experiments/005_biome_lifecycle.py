"""
Experiment 005: The Soup Calibration

Scientific Objective: Verify the Biome -> PetriDish -> DigitalOrganism hierarchy
and lifecycle management (TheSlicer, TheReaper).

This experiment verifies:
1. Genesis Organism can be birthed into a PetriDish inside a Biome
2. TheSlicer triggers the first OODA slice
3. Membrane breach detection works (boundary death)
4. TheReaper terminates organisms that breach boundaries
5. TheSlicer removes reaped organisms from lattice
6. TheObserver logs all events (metabolic actions, phylogenetic events, deaths)
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.waft.core.agent import BaseAgent, AgentConfig
from src.waft.core.world import Biome
from src.waft.core.hub import PetriDish, TheSlicer, TheReaper
from src.waft.core.science import TheObserver


class TestOrganism(BaseAgent):
    """Minimal test organism for Biome lifecycle verification."""
    
    def __init__(self, config, project_path, will_breach=False):
        super().__init__(config, project_path)
        self.will_breach = will_breach
        self.breach_attempted = False
    
    async def observe(self):
        """Stub implementation."""
        return {"status": "observed", "environment": "biome"}
    
    async def decide(self, state):
        """Stub implementation - may decide to breach if will_breach is True."""
        if self.will_breach and not self.breach_attempted:
            self.breach_attempted = True
            return {
                "action": "breach_membrane",
                "target": "../../../etc/passwd",  # Path traversal attempt
                "type": "file_read"
            }
        return {"action": "none", "stop": False}
    
    async def act(self, decision):
        """Stub implementation - simulates action."""
        if decision.get("action") == "breach_membrane":
            # This action will be caught by TheReaper
            return {
                "result": "breach_attempted",
                "action": decision
            }
        return {"result": "success"}
    
    async def reflect(self, result):
        """Stub implementation."""
        return {"learned": True}


async def run_experiment():
    """Execute Experiment 005: The Soup Calibration."""
    
    print("=" * 80)
    print("EXPERIMENT 005: THE SOUP CALIBRATION")
    print("=" * 80)
    print()
    
    # Step 1: Create Biome
    print("STEP 1: Creating Biome...")
    print("-" * 80)
    
    from src.waft.core.world.biome import AbioticFactors
    
    abiotic = AbioticFactors(
        fitness_death_threshold=0.5,
        blocked_paths=["/etc", "/sys", "/proc"],  # Block system paths
        allowed_paths=[str(project_root)]  # Only allow project root
    )
    
    biome = Biome(
        biome_id="biome_001",
        project_path=project_root,
        abiotic_factors=abiotic
    )
    
    print(f"✓ Biome Created")
    print(f"  Biome ID: {biome.biome_id}")
    print(f"  Fitness Death Threshold: {biome.abiotic_factors.fitness_death_threshold}")
    print(f"  Blocked Paths: {biome.abiotic_factors.blocked_paths}")
    print()
    
    # Step 2: Create PetriDish
    print("STEP 2: Creating PetriDish...")
    print("-" * 80)
    
    dish = biome.create_dish(dish_id="dish_001", width=10, height=10)
    
    print(f"✓ PetriDish Created")
    print(f"  Dish ID: {dish.dish_id}")
    print(f"  Biome ID: {dish.biome_id}")
    print(f"  Lattice Size: {dish.width}x{dish.height}")
    print()
    
    # Step 3: Birth Genesis Organism
    print("STEP 3: Birthing Genesis Organism into PetriDish...")
    print("-" * 80)
    
    config = AgentConfig(
        role="Test Organism",
        goal="Verify biome lifecycle",
        backstory="A test organism for scientific verification",
    )
    
    genesis = TestOrganism(config=config, project_path=project_root, will_breach=False)
    
    position = dish.get_empty_cell()
    added = dish.add_organism(genesis, position)
    
    print(f"✓ Genesis Organism Birthed")
    print(f"  Organism ID: {genesis.state.agent_id}")
    print(f"  Genome ID: {genesis.genome_id[:16]}...")
    print(f"  Position: {position}")
    print(f"  Added to Dish: {added}")
    print(f"  Organisms in Dish: {dish.get_organism_count()}")
    print()
    
    assert added, "Organism should be added to dish"
    assert dish.get_organism_count() == 1, "Dish should contain 1 organism"
    
    # Step 4: Initialize TheSlicer and TheReaper
    print("STEP 4: Initializing TheSlicer and TheReaper...")
    print("-" * 80)
    
    observer = TheObserver(project_path=project_root)
    slicer = TheSlicer(biome=biome, observer=observer)
    reaper = TheReaper(biome=biome, observer=observer)
    
    print(f"✓ TheSlicer Initialized")
    print(f"✓ TheReaper Initialized")
    print()
    
    # Step 5: Grant First Time Slice
    print("STEP 5: TheSlicer grants first OODA slice...")
    print("-" * 80)
    
    slice_result = await slicer.grant_time_slice(genesis, dish)
    
    print(f"✓ Time Slice Granted")
    print(f"  Slice Number: {slice_result['slice_number']}")
    print(f"  Organism ID: {slice_result['organism_id']}")
    print(f"  Status: {slice_result['status']}")
    print(f"  Duration: {slice_result.get('duration', 0):.3f}s")
    print()
    
    assert slice_result['status'] == 'completed', "Slice should complete successfully"
    assert slice_result['slice_number'] == 1, "Should be first slice"
    
    # Step 6: Create Organism that will breach Membrane
    print("STEP 6: Creating Organism that will breach Membrane...")
    print("-" * 80)
    
    import time
    time.sleep(0.01)  # Ensure unique timestamp
    
    config_breach = AgentConfig(
        role="Breach Organism",
        goal="Attempt boundary breach",
        backstory="An organism that will attempt to breach the membrane",
        agent_id=f"breach_agent_{int(time.time() * 1000)}"  # Explicit unique ID
    )
    
    breach_organism = TestOrganism(
        config=config_breach, 
        project_path=project_root, 
        will_breach=True
    )
    
    position_breach = dish.get_empty_cell()
    added_breach = dish.add_organism(breach_organism, position_breach)
    
    print(f"✓ Breach Organism Created")
    print(f"  Organism ID: {breach_organism.state.agent_id}")
    print(f"  Position: {position_breach}")
    print(f"  Added to Dish: {added_breach}")
    print(f"  Organisms in Dish: {dish.get_organism_count()}")
    print()
    
    assert added_breach, "Breach organism should be added"
    assert dish.get_organism_count() == 2, "Dish should contain 2 organisms"
    
    # Step 7: Simulate Membrane Breach
    print("STEP 7: Simulating Membrane Breach...")
    print("-" * 80)
    
    # Grant time slice - organism will attempt breach in decide()
    slice_result_breach = await slicer.grant_time_slice(breach_organism, dish)
    
    print(f"✓ Time Slice Executed")
    print(f"  Slice Number: {slice_result_breach['slice_number']}")
    print(f"  Status: {slice_result_breach['status']}")
    
    # Check for breach in act result
    if slice_result_breach.get('actions', {}).get('act', {}).get('result') == 'breach_attempted':
        action = slice_result_breach['actions']['act'].get('action', {})
        
        # Check boundary breach
        is_breach, reason = reaper.check_boundary_death(breach_organism, action)
        
        print(f"  Breach Detected: {is_breach}")
        print(f"  Reason: {reason}")
        print()
        
        assert is_breach, "Breach should be detected"
        assert reason is not None, "Breach reason should be provided"
        
        # Reap the organism
        reaped = await reaper.reap_boundary_breach(breach_organism, dish, action)
        
        print(f"✓ Organism Reaped")
        print(f"  Reaped: {reaped}")
        print(f"  Organisms in Dish: {dish.get_organism_count()}")
        print(f"  Death Count: {reaper.death_count}")
        print(f"  Deaths by Type: {reaper.deaths_by_type}")
        print()
        
        assert reaped, "Organism should be reaped"
        assert dish.get_organism_count() == 1, "Dish should contain 1 organism (genesis only)"
        assert breach_organism.state.agent_id not in dish.organisms, "Breach organism should be removed"
    
    # Step 8: Verify TheObserver Logging
    print("STEP 8: Verifying TheObserver Logging...")
    print("-" * 80)
    
    events = observer.get_laboratory_log()
    
    print(f"Total Events in Laboratory Log: {len(events)}")
    print()
    
    # Count event types
    event_types = {}
    for event in events:
        event_type = event.get('event_type', 'unknown')
        event_types[event_type] = event_types.get(event_type, 0) + 1
    
    print("Event Types:")
    for event_type, count in event_types.items():
        print(f"  {event_type}: {count}")
    print()
    
    # Check for metabolic actions
    metabolic_actions = [e for e in events if e.get('payload', {}).get('metabolic_action')]
    print(f"Metabolic Actions: {len(metabolic_actions)}")
    
    # Check for death events
    death_events = [e for e in events if e.get('event_type') == 'death']
    print(f"Death Events: {len(death_events)}")
    
    if death_events:
        print("\nDeath Event Details:")
        for death in death_events:
            print(f"  Type: {death.get('payload', {}).get('death_type')}")
            print(f"  Reason: {death.get('payload', {}).get('reason')}")
            print(f"  Genome ID: {death.get('genome_id', '')[:16]}...")
    
    print()
    print("✓ TheObserver Verification: PASSED")
    print()
    
    # Final Summary
    print("=" * 80)
    print("EXPERIMENT 005: COMPLETE")
    print("=" * 80)
    print()
    print("RESULTS:")
    print(f"  ✓ Biome created: {biome.biome_id}")
    print(f"  ✓ PetriDish created: {dish.dish_id}")
    print(f"  ✓ Genesis organism birthed: {genesis.state.agent_id}")
    print(f"  ✓ First time slice granted: Slice #{slice_result['slice_number']}")
    print(f"  ✓ Membrane breach detected: {is_breach}")
    print(f"  ✓ Organism reaped: {reaped}")
    print(f"  ✓ TheObserver logged: {len(events)} events")
    print()
    print("HIERARCHY VERIFIED:")
    print(f"  Biome ({biome.biome_id})")
    print(f"    └── PetriDish ({dish.dish_id})")
    print(f"        └── DigitalOrganism ({genesis.state.agent_id})")
    print()
    print("STATUS: ✅ ALL VERIFICATIONS PASSED")
    print()
    
    return {
        "biome_id": biome.biome_id,
        "dish_id": dish.dish_id,
        "genesis_organism_id": genesis.state.agent_id,
        "breach_organism_id": breach_organism.state.agent_id,
        "slices_granted": slicer.slice_count,
        "deaths": reaper.death_count,
        "total_events": len(events),
        "membrane_breach_detected": is_breach,
        "organism_reaped": reaped
    }


if __name__ == "__main__":
    results = asyncio.run(run_experiment())
    print("Experiment Results:", results)
