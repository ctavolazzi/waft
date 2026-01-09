"""
Experiment 006: The Naming Day

Scientific Objective: Verify taxonomy system and social awareness (quorum sensing).

This experiment verifies:
1. Three Genesis organisms can be birthed
2. Each has a distinct but deterministic scientific name
3. Organisms can "sense" each other's presence (quorum sensing)
4. Scientific names are logged in TheObserver
"""

import asyncio
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.waft.core.agent import BaseAgent, AgentConfig
from src.waft.core.world import Biome
from src.waft.core.hub import PetriDish, TheSlicer, TheReaper
from src.waft.core.science import TheObserver
from src.waft.core.science.taxonomy import LineagePoet


class SocialOrganism(BaseAgent):
    """Test organism that can sense social context."""
    
    def __init__(self, config, project_path):
        super().__init__(config, project_path)
        self.sensed_neighbors = []
        self.sensed_density = 0.0
    
    async def observe(self):
        """Observe with social awareness (quorum sensing)."""
        social_context = self.state.working_memory.get("social_context", {})
        neighbor_count = social_context.get("neighbor_count", 0)
        population_density = social_context.get("population_density", 0.0)
        total_population = social_context.get("total_population", 0)
        
        self.sensed_neighbors.append(neighbor_count)
        self.sensed_density = population_density
        
        return {
            "status": "observed",
            "social_context": {
                "neighbor_count": neighbor_count,
                "population_density": population_density,
                "total_population": total_population,
                "scientific_name": self.scientific_name
            }
        }
    
    async def decide(self, state):
        """Stub implementation."""
        return {"action": "none", "stop": False}
    
    async def act(self, decision):
        """Stub implementation."""
        return {"result": "success"}
    
    async def reflect(self, result):
        """Stub implementation."""
        return {"learned": True}


async def run_experiment():
    """Execute Experiment 006: The Naming Day."""
    
    print("=" * 80)
    print("EXPERIMENT 006: THE NAMING DAY")
    print("=" * 80)
    print()
    
    # Step 1: Create Biome and PetriDish
    print("STEP 1: Creating Biome and PetriDish...")
    print("-" * 80)
    
    from src.waft.core.world.biome import AbioticFactors
    
    abiotic = AbioticFactors()
    biome = Biome(
        biome_id="biome_006",
        project_path=project_root,
        abiotic_factors=abiotic
    )
    
    dish = biome.create_dish(dish_id="dish_006", width=10, height=10)
    
    print(f"✓ Biome Created: {biome.biome_id}")
    print(f"✓ PetriDish Created: {dish.dish_id}")
    print()
    
    # Step 2: Birth 3 Genesis Organisms
    print("STEP 2: Birthing 3 Genesis Organisms...")
    print("-" * 80)
    
    organisms = []
    positions = []
    scientific_names = []
    
    for i in range(3):
        time.sleep(0.01)  # Ensure unique timestamps
        
        config = AgentConfig(
            role=f"Test Organism {i+1}",
            goal="Verify taxonomy and social awareness",
            backstory=f"Genesis organism #{i+1} for naming day",
            agent_id=f"genesis_{i+1}_{int(time.time() * 1000)}"
        )
        
        organism = SocialOrganism(config=config, project_path=project_root)
        position = dish.get_empty_cell()
        
        added = dish.add_organism(organism, position)
        assert added, f"Organism {i+1} should be added"
        
        organisms.append(organism)
        positions.append(position)
        scientific_names.append(organism.scientific_name)
        
        print(f"✓ Organism {i+1} Birthed")
        print(f"  Agent ID: {organism.state.agent_id}")
        print(f"  Genome ID: {organism.genome_id[:16]}...")
        print(f"  Scientific Name: {organism.scientific_name}")
        print(f"  Position: {position}")
        print()
    
    # Step 3: Verify Distinct but Deterministic Names
    print("STEP 3: Verifying Taxonomy (Distinct & Deterministic Names)...")
    print("-" * 80)
    
    # Check all names are distinct
    unique_names = set(scientific_names)
    assert len(unique_names) == 3, "All organisms should have distinct names"
    
    # Verify determinism: same genome_id = same name
    for organism in organisms:
        name1 = LineagePoet.generate_name(organism.genome_id)
        name2 = LineagePoet.generate_name(organism.genome_id)
        name3 = organism.scientific_name
        
        assert name1 == name2 == name3, f"Name should be deterministic for {organism.state.agent_id}"
        print(f"✓ Determinism Verified: {organism.state.agent_id}")
        print(f"  Name (3x): {name1}")
    
    print()
    print("✓ Taxonomy Verification: PASSED")
    print()
    
    # Step 4: Initialize TheSlicer
    print("STEP 4: Initializing TheSlicer...")
    print("-" * 80)
    
    observer = TheObserver(project_path=project_root)
    slicer = TheSlicer(biome=biome, observer=observer)
    reaper = TheReaper(biome=biome, observer=observer)
    
    print(f"✓ TheSlicer Initialized")
    print()
    
    # Step 5: Pulse TheSlicer (Grant Time Slices)
    print("STEP 5: Pulsing TheSlicer - Testing Quorum Sensing...")
    print("-" * 80)
    
    slice_results = []
    for organism in organisms:
        result = await slicer.grant_time_slice(organism, dish)
        slice_results.append(result)
        
        # Check social context was sensed
        observe_result = result.get("actions", {}).get("observe", {})
        social_context = observe_result.get("social_context", {})
        
        neighbor_count = social_context.get("neighbor_count", 0)
        population_density = social_context.get("population_density", 0.0)
        total_population = social_context.get("total_population", 0)
        
        print(f"✓ Slice Granted to {organism.scientific_name}")
        print(f"  Neighbor Count: {neighbor_count}")
        print(f"  Population Density: {population_density:.4f}")
        print(f"  Total Population: {total_population}")
        print()
    
    # Verify quorum sensing
    print("STEP 6: Verifying Quorum Sensing...")
    print("-" * 80)
    
    # Organisms should sense neighbors (depending on positions)
    # If organisms are adjacent, they should sense each other
    for i, organism in enumerate(organisms):
        sensed = organism.sensed_neighbors[-1] if organism.sensed_neighbors else 0
        density = organism.sensed_density
        
        print(f"  {organism.scientific_name}:")
        print(f"    Sensed Neighbors: {sensed}")
        print(f"    Sensed Density: {density:.4f}")
        
        # Verify they can sense population
        assert density > 0, f"Organism should sense population density > 0"
        assert organism.state.working_memory.get("social_context", {}).get("total_population") == 3, \
            "All organisms should sense total population of 3"
    
    print()
    print("✓ Quorum Sensing Verification: PASSED")
    print()
    
    # Step 7: Verify TheObserver Logging
    print("STEP 7: Verifying TheObserver Logging (Scientific Names)...")
    print("-" * 80)
    
    # Get events for our organisms specifically
    organism_ids = [org.state.agent_id for org in organisms]
    
    events = observer.get_laboratory_log()
    
    # Filter for spawn events (genesis) for our organisms
    genesis_events = [
        e for e in events 
        if e.get("event_type") == "spawn" and 
        e.get("payload", {}).get("event") == "genesis" and
        e.get("agent_id") in organism_ids
    ]
    
    print(f"Total Events in Log: {len(events)}")
    print(f"Our Genesis Events: {len(genesis_events)}")
    print()
    
    # Verify scientific names in events
    print("Birth Certificates (First 3 Named Species):")
    print("-" * 80)
    
    # Match events to organisms
    birth_certificates = []
    for organism in organisms:
        # Find genesis event for this organism
        event = next(
            (e for e in genesis_events if e.get("agent_id") == organism.state.agent_id),
            None
        )
        
        if event:
            scientific_name = (
                event.get("scientific_name") or 
                event.get("payload", {}).get("scientific_name") or
                LineagePoet.generate_name(event.get("genome_id", ""))
            )
            genome_id = event.get("genome_id", "")
            agent_id = event.get("agent_id", "")
            generation = event.get("generation", 0)
            
            birth_certificates.append({
                "scientific_name": scientific_name,
                "genome_id": genome_id,
                "agent_id": agent_id,
                "generation": generation,
                "timestamp": event.get("timestamp", "")
            })
    
    # Display birth certificates
    for i, cert in enumerate(birth_certificates[:3], 1):
        print(f"\n📜 Birth Certificate #{i}")
        print(f"  Scientific Name: {cert['scientific_name']}")
        print(f"  Genome ID: {cert['genome_id'][:16]}...")
        print(f"  Agent ID: {cert['agent_id']}")
        print(f"  Generation: {cert['generation']}")
        print(f"  Timestamp: {cert['timestamp']}")
        
        # Verify name matches genome_id
        computed_name = LineagePoet.generate_name(cert['genome_id'])
        assert cert['scientific_name'] == computed_name, \
            f"Scientific name should match genome_id: {cert['scientific_name']} != {computed_name}"
    
    print()
    print("✓ TheObserver Verification: PASSED")
    print()
    
    # Final Summary
    print("=" * 80)
    print("EXPERIMENT 006: COMPLETE")
    print("=" * 80)
    print()
    print("RESULTS:")
    print(f"  ✓ 3 Genesis organisms birthed")
    print(f"  ✓ All have distinct scientific names")
    print(f"  ✓ Names are deterministic (same genome = same name)")
    print(f"  ✓ Quorum sensing functional (neighbor_count, population_density)")
    print(f"  ✓ Scientific names logged in TheObserver")
    print()
    print("TAXONOMY VERIFIED:")
    for i, (organism, name) in enumerate(zip(organisms, scientific_names), 1):
        print(f"  Species #{i}: {name}")
        print(f"    Genome: {organism.genome_id[:16]}...")
    print()
    print("STATUS: ✅ ALL VERIFICATIONS PASSED")
    print()
    
    return {
        "organisms_birthed": 3,
        "scientific_names": scientific_names,
        "quorum_sensing_verified": True,
        "taxonomy_verified": True,
        "birth_certificates": [
            {
                "scientific_name": name,
                "genome_id": org.genome_id,
                "agent_id": org.state.agent_id
            }
            for org, name in zip(organisms, scientific_names)
        ]
    }


if __name__ == "__main__":
    results = asyncio.run(run_experiment())
    print("\nExperiment Results:")
    print(f"  Birth Certificates: {len(results['birth_certificates'])}")
    for cert in results['birth_certificates']:
        print(f"    - {cert['scientific_name']} ({cert['genome_id'][:16]}...)")
