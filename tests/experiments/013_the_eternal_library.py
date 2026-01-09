"""
Experiment 013: The Eternal Library

Scientific Objective: Verify the Obsidian Archive and Pygame Biome Engine integration.

This experiment:
1. Creates 4 distinct organisms in a PetriDish
2. Runs 10 pulses with Pygame visualization
3. Generates Obsidian vault with organism files
4. Verifies journal sync and lineage tracking
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.waft.core.agent.base import BaseAgent
from src.waft.core.agent.state import AgentConfig
from src.waft.core.world.biome import Biome
from src.waft.core.hub.dish import PetriDish
from src.waft.core.hub.lifecycle import TheSlicer, TheReaper
from src.waft.core.science.observer import TheObserver
from src.waft.core.hub.display import PygameBiomeEngine
from src.waft.core.science.report import ObsidianGenerator


class TestOrganism(BaseAgent):
    """Test organism for the Eternal Library experiment."""
    
    async def observe(self):
        return {"status": "observed", "context": "experiment_013"}
    
    async def decide(self, state):
        return {"action": "none", "stop": False}
    
    async def act(self, decision):
        return {"result": "success", "action_type": "test"}
    
    async def reflect(self, result):
        return {"learned": True, "reflection": "Experiment proceeding"}


async def run_experiment():
    """Execute Experiment 013: The Eternal Library."""
    
    print("=" * 80)
    print("EXPERIMENT 013: THE ETERNAL LIBRARY")
    print("=" * 80)
    print()
    print("Scientific Objective: Verify Obsidian Archive and Pygame Biome Engine")
    print()
    
    # Step 1: Create Biome and PetriDish
    print("STEP 1: Creating Biome and PetriDish...")
    print("-" * 80)
    
    from src.waft.core.world.biome import AbioticFactors
    
    abiotic = AbioticFactors()
    biome = Biome(
        biome_id="biome_013_eternal_library",
        project_path=project_root,
        abiotic_factors=abiotic
    )
    
    dish = biome.create_dish(dish_id="dish_013", width=20, height=20)
    
    print(f"✓ Biome Created: {biome.biome_id}")
    print(f"✓ PetriDish Created: {dish.dish_id} (20×20)")
    print()
    
    # Step 2: Birth 4 Distinct Organisms
    print("STEP 2: Birthing 4 Distinct Organisms...")
    print("-" * 80)
    
    organisms = []
    positions = [(5, 5), (10, 5), (5, 10), (10, 10)]
    
    for i, pos in enumerate(positions):
        config = AgentConfig(
            role=f"Test Organism {i+1}",
            goal="Participate in Experiment 013",
            backstory=f"Organism created for Eternal Library verification (Organism {i+1})"
        )
        
        organism = TestOrganism(config=config, project_path=project_root)
        added = dish.add_organism(organism, pos)
        
        if added:
            organisms.append(organism)
            print(f"✓ {organism.scientific_name} at {pos}")
            print(f"  Genome: {organism.genome_id[:16]}...")
            print(f"  Symbol: {organism.state.anatomical_symbol} ({organism.state.anatomical_archetype})")
        else:
            print(f"✗ Failed to add organism at {pos}")
    
    print()
    print(f"✓ Total Organisms: {len(organisms)}")
    print()
    
    # Step 3: Initialize Systems
    print("STEP 3: Initializing Systems...")
    print("-" * 80)
    
    observer = TheObserver(project_path=project_root)
    slicer = TheSlicer(biome=biome, observer=observer)
    reaper = TheReaper(biome=biome, observer=observer)
    obsidian = ObsidianGenerator(project_path=project_root, observer=observer)
    
    print("✓ TheObserver Initialized")
    print("✓ TheSlicer Initialized")
    print("✓ TheReaper Initialized")
    print("✓ ObsidianGenerator Initialized")
    print()
    
    # Step 4: Initialize Pygame Display
    print("STEP 4: Initializing Pygame Biome Engine...")
    print("-" * 80)
    
    try:
        display = PygameBiomeEngine(
            width=1200,
            height=800,
            cell_size=20,
            title="WAFT Biome Engine - Experiment 013"
        )
        print("✓ Pygame Display Initialized")
        print()
        print("(Pygame window should be visible)")
        print()
    except Exception as e:
        print(f"✗ Failed to initialize Pygame: {e}")
        print("Continuing without display...")
        display = None
    
    # Step 5: Run 10 Pulses with Visualization
    print("STEP 5: Running 10 Pulses with Real-time Visualization...")
    print("-" * 80)
    print()
    
    first_birth = None
    
    for pulse in range(1, 11):
        print(f"Pulse {pulse}/10...")
        
        # Update Pygame display
        if display:
            display.pulse(dish)
            # Small delay for visibility
            await asyncio.sleep(0.1)
        
        # Grant time slices to all organisms
        results = await slicer.pulse()
        
        # Check for new births (gestation)
        for organism in list(dish.organisms.values()):
            if organism.generation > 0 and first_birth is None:
                first_birth = organism
                print(f"  → First birth detected: {organism.scientific_name}")
        
        # Process events (for Pygame)
        if display:
            if not display.is_running():
                print("  → Display closed by user")
                break
    
    print()
    print("✓ 10 Pulses Complete")
    print()
    
    # Step 6: Generate Obsidian Archive
    print("STEP 6: Generating Obsidian Archive...")
    print("-" * 80)
    
    archive_files = obsidian.sync_all_organisms(biome)
    
    print(f"✓ Generated {len(archive_files)} files:")
    for file_path in archive_files:
        print(f"  - {file_path.relative_to(project_root)}")
    print()
    
    # Step 7: Verification
    print("STEP 7: Verification...")
    print("-" * 80)
    
    # Check journal entries
    journals_found = 0
    for organism in dish.organisms.values():
        if organism.state.journal:
            journals_found += len(organism.state.journal)
    
    print(f"✓ Journal Entries: {journals_found} total")
    
    # Check Obsidian files
    archive_path = project_root / "_pyrite" / "archive"
    obsidian_files = list(archive_path.glob("*.md"))
    print(f"✓ Obsidian Files: {len(obsidian_files)} files")
    
    # Check index
    index_file = archive_path / "00_Index.md"
    if index_file.exists():
        print(f"✓ Index File: {index_file.name}")
    else:
        print(f"✗ Index File: Missing")
    
    print()
    
    # Step 8: Report First Birth
    if first_birth:
        print("STEP 8: First Birth in Obsidian Era")
        print("-" * 80)
        print()
        print("BIRTH CERTIFICATE")
        print("=" * 80)
        print(f"Scientific Name: {first_birth.scientific_name}")
        print(f"Genome ID: {first_birth.genome_id}")
        print(f"Symbol: {first_birth.state.anatomical_symbol} ({first_birth.state.anatomical_archetype})")
        print(f"Generation: {first_birth.generation}")
        print(f"Parent: {first_birth.parent_id[:16] if first_birth.parent_id else 'None'}...")
        print(f"Energy: {first_birth.state.energy:.1f}%")
        print(f"Journal Entries: {len(first_birth.state.journal)}")
        print()
        print("This organism was the first to be birthed into the Obsidian Era,")
        print("where all thoughts and reflections are preserved in the Eternal Library.")
        print()
    else:
        print("STEP 8: No births occurred during this experiment")
        print()
    
    # Cleanup
    if display:
        display.close()
    
    print("=" * 80)
    print("EXPERIMENT 013 COMPLETE")
    print("=" * 80)
    print()
    print("Results:")
    print(f"  - Organisms: {len(dish.organisms)}")
    print(f"  - Pulses: 10")
    print(f"  - Obsidian Files: {len(obsidian_files)}")
    print(f"  - Journal Entries: {journals_found}")
    print()
    print(f"Archive Location: {archive_path.relative_to(project_root)}")
    print()


if __name__ == "__main__":
    asyncio.run(run_experiment())
