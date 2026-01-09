"""
Experiment 012: The Pulse Visualization

Scientific Objective: Visualize the multiverse in real-time using PetriViewer
and generate a scientific manifesto report.

This experiment:
1. Populates a 15x15 PetriDish with 6 diverse organisms and 10 items
2. Runs 10 Pulses with real-time visualization
3. Generates final scientific manifesto report
"""

import asyncio
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.waft.core.agent import BaseAgent, AgentConfig
from src.waft.core.agent.items import Item
from src.waft.core.world import Biome
from src.waft.core.hub import PetriDish, TheSlicer, TheReaper
from src.waft.core.science import TheObserver
from src.waft.core.hub.viewer import PetriViewer
from src.waft.core.science.report import ManifestoGenerator


class RenderOrganism(BaseAgent):
    """Test organism for visualization."""
    
    async def observe(self):
        return {"status": "observed"}
    
    async def decide(self, state):
        return {"action": "none", "stop": False}
    
    async def act(self, decision):
        return {"result": "success"}
    
    async def reflect(self, result):
        return {"learned": True}


async def run_experiment():
    """Execute Experiment 012: The Pulse Visualization."""
    
    print("=" * 80)
    print("EXPERIMENT 012: THE PULSE VISUALIZATION")
    print("=" * 80)
    print()
    print("Scientific Objective: Real-time multiverse visualization")
    print()
    
    # Step 1: Create Biome and PetriDish (15x15)
    print("STEP 1: Creating 15×15 PetriDish...")
    print("-" * 80)
    
    from src.waft.core.world.biome import AbioticFactors
    
    abiotic = AbioticFactors()
    biome = Biome(
        biome_id="biome_012",
        project_path=project_root,
        abiotic_factors=abiotic
    )
    
    dish = biome.create_dish(dish_id="dish_012", width=15, height=15)
    
    print(f"✓ Biome Created: {biome.biome_id}")
    print(f"✓ PetriDish Created: {dish.dish_id} (15×15)")
    print()
    
    # Step 2: Birth 6 Diverse Organisms
    print("STEP 2: Birthing 6 Diverse Organisms...")
    print("-" * 80)
    
    organisms = []
    positions = [(2, 2), (5, 3), (8, 5), (11, 7), (3, 10), (12, 12)]
    
    for i, pos in enumerate(positions):
        time.sleep(0.01)  # Ensure unique timestamps
        
        config = AgentConfig(
            role=f"Organism {i+1}",
            goal=f"Test visualization {i+1}",
            backstory=f"A test organism for visualization experiment {i+1}",
            agent_id=f"org_{i+1}_{int(time.time() * 1000)}"
        )
        
        org = RenderOrganism(config=config, project_path=project_root)
        org.state.energy = 75.0 + (i * 5)  # Vary energy levels
        
        added = dish.add_organism(org, pos)
        assert added, f"Organism {i+1} should be added"
        organisms.append(org)
        
        print(f"✓ {org.scientific_name} ({org.state.anatomical_symbol}) at {pos}")
    
    print()
    
    # Step 3: Add 10 Items
    print("STEP 3: Adding 10 Items...")
    print("-" * 80)
    
    item_positions = [
        (1, 1), (4, 2), (7, 4), (10, 6), (13, 8),
        (2, 9), (6, 11), (9, 13), (14, 1), (0, 14)
    ]
    
    items = []
    for i, pos in enumerate(item_positions):
        if i % 2 == 0:
            item = Item.create(name="Scint-Shard", weight=1, properties={"type": "energy"})
        else:
            item = Item.create(name="Void-Stone", weight=2, properties={"type": "void"})
        
        added = dish.add_item(item, pos)
        assert added, f"Item {i+1} should be added"
        items.append(item)
        
        print(f"✓ {item.name} at {pos}")
    
    print()
    
    # Step 4: Initialize TheSlicer and Viewer
    print("STEP 4: Initializing TheSlicer and PetriViewer...")
    print("-" * 80)
    
    observer = TheObserver(project_path=project_root)
    slicer = TheSlicer(biome=biome, observer=observer)
    reaper = TheReaper(biome=biome, observer=observer)
    viewer = PetriViewer(use_colors=True)
    
    print(f"✓ TheSlicer Initialized")
    print(f"✓ PetriViewer Initialized")
    print()
    
    # Step 5: Run 10 Pulses with Real-time Visualization
    print("STEP 5: Running 10 Pulses with Real-time Visualization...")
    print("-" * 80)
    print()
    print("(Terminal will be cleared and redrawn after each pulse)")
    print()
    print("Starting visualization in 2 seconds...")
    await asyncio.sleep(2)
    
    for pulse in range(1, 11):
        # Clear screen
        viewer.clear_screen()
        
        # Render current state
        render_output = viewer.render(dish, sidebar=True)
        print(render_output)
        print()
        print(f"Pulse: {pulse}/10")
        print("=" * 80)
        
        # Grant time slices to all organisms
        for organism in list(dish.organisms.values()):
            await slicer.grant_time_slice(organism, dish)
        
        # Small delay for visibility
        await asyncio.sleep(0.5)
    
    print()
    print("✓ 10 Pulses Complete")
    print()
    
    # Step 6: Generate Scientific Manifesto
    print("STEP 6: Generating Scientific Manifesto...")
    print("-" * 80)
    
    manifesto_gen = ManifestoGenerator(project_path=project_root, observer=observer)
    report = manifesto_gen.generate_session_report(biome=biome)
    
    # Save report
    report_file = project_root / "_work_efforts" / "session_report.md"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(report, encoding="utf-8")
    
    print(f"✓ Report saved: {report_file}")
    print()
    
    # Step 7: Final Render
    print("STEP 7: Final State Visualization...")
    print("-" * 80)
    print()
    
    final_render = viewer.render(dish, sidebar=True)
    print(final_render)
    print()
    
    # Step 8: Report Summary
    print("=" * 80)
    print("EXPERIMENT 012: COMPLETE")
    print("=" * 80)
    print()
    print("RESULTS:")
    print(f"  ✓ 6 organisms birthed and visualized")
    print(f"  ✓ 10 items distributed across lattice")
    print(f"  ✓ 10 pulses executed with real-time rendering")
    print(f"  ✓ Scientific manifesto generated")
    print()
    print(f"📄 Report: {report_file}")
    print()
    
    # Show snippet of manifesto
    print("━━━ MANIFESTO SNIPPET ━━━")
    print()
    report_lines = report.split("\n")
    for i, line in enumerate(report_lines[:30]):  # First 30 lines
        print(line)
    if len(report_lines) > 30:
        print(f"\n... ({len(report_lines) - 30} more lines)")
    print()
    
    return {
        "dish": dish,
        "organisms": organisms,
        "items": items,
        "final_render": final_render,
        "report": report,
        "report_file": report_file
    }


if __name__ == "__main__":
    results = asyncio.run(run_experiment())
    print("\nExperiment Complete!")
    print(f"Final render saved in report: {results['report_file']}")
