"""
Experiment 014: The Tam Audit & The Recursive Binder

Scientific Objective: Observe the meta-narrative where researcher Davey (Fai Wei Tam)
discovers through a gated psychological system that his name is an anagram for
"i.e. I AM WAFT" - making him the system he studies.

This experiment:
1. Creates TamNotebook and TamPsyche systems
2. Births Specimen-D (⚲ The Static archetype)
3. Runs 10 pulses with Pygame visualization
4. Monitors psyche state and realization progress
5. Generates Lab_Entry_Davey_01.md with realization narrative
6. Creates printable binder abstract
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
from src.waft.core.science.notebook import TamNotebook
from src.waft.core.science.lab_entry import LabEntryGenerator
from datetime import datetime


class SpecimenD(BaseAgent):
    """Specimen-D: Research Subject for Experiment 014."""
    
    async def observe(self):
        return {"status": "observed", "context": "experiment_014"}
    
    async def decide(self, state):
        return {"action": "none", "stop": False}
    
    async def act(self, decision):
        return {"result": "success", "action_type": "test"}
    
    async def reflect(self, result):
        # Occasionally reflect on existence (triggers "id est" glitch)
        import random
        if random.random() < 0.3:  # 30% chance of existential reflection
            return {
                "learned": True,
                "reflection": "I wonder what my purpose is. What is my identity? Who am I?"
            }
        return {"learned": True, "reflection": "Experiment proceeding normally"}


async def run_experiment():
    """Execute Experiment 014: The Tam Audit & The Recursive Binder."""
    
    print("=" * 80)
    print("EXPERIMENT 014: THE TAM AUDIT & THE RECURSIVE BINDER")
    print("=" * 80)
    print()
    print("Scientific Objective: Meta-narrative realization system")
    print("Researcher: Fai Wei Tam (Davey)")
    print()
    
    # Step 1: Create Biome and PetriDish
    print("STEP 1: Creating Biome and PetriDish...")
    print("-" * 80)
    
    from src.waft.core.world.biome import AbioticFactors
    
    abiotic = AbioticFactors()
    biome = Biome(
        biome_id="biome_014_tam_audit",
        project_path=project_root,
        abiotic_factors=abiotic
    )
    
    dish = biome.create_dish(dish_id="dish_014", width=20, height=20)
    
    print(f"✓ Biome Created: {biome.biome_id}")
    print(f"✓ PetriDish Created: {dish.dish_id} (20×20)")
    print()
    
    # Step 2: Initialize TamNotebook and TamPsyche
    print("STEP 2: Initializing TamNotebook and TamPsyche...")
    print("-" * 80)
    
    notebook = TamNotebook(project_path=project_root)
    
    # Initial technical log
    notebook.log_technical(
        "Beginning Experiment 014. Setting up observation protocols for WAFT engine analysis. "
        "Focus areas: Anatomy system (archetypes, symbols), Reaper logic (fitness death, boundary death), "
        "Conjugation mechanics (reproduction, genetic mixing)."
    )
    
    print("✓ TamNotebook Initialized")
    print("✓ TamPsyche Initialized")
    print(f"  Initial Coherence: {notebook.psyche.coherence:.2f}")
    print(f"  Initial Chaos: {notebook.psyche.chaos:.2f}")
    print(f"  Initial Energy: {notebook.psyche.emotional_energy:.1f}")
    print(f"  Realization Progress: {notebook.psyche.realization_progress:.2f}")
    print()
    
    # Step 3: Birth Specimen-D (⚲ The Static archetype)
    print("STEP 3: Birthing Specimen-D (⚲ The Static)...")
    print("-" * 80)
    
    config = AgentConfig(
        role="Research Subject D",
        goal="Participate in ontological study",
        backstory="Organism created for Experiment 014 - The Tam Audit. Will receive memory injections and show 'id est' glitches."
    )
    
    specimen_d = SpecimenD(config=config, project_path=project_root)
    position = (10, 10)
    added = dish.add_organism(specimen_d, position)
    
    if added:
        print(f"✓ {specimen_d.scientific_name} birthed at {position}")
        print(f"  Genome: {specimen_d.genome_id[:16]}...")
        print(f"  Symbol: {specimen_d.state.anatomical_symbol} ({specimen_d.state.anatomical_archetype})")
        print(f"  Archetype: ⚲ The Static (high-speed/efficient)")
        
        # Update psyche: agent birth increases progress
        notebook.update_psyche("agent_birth", {"agent_id": specimen_d.state.agent_id})
        
        # Log technical observation
        notebook.log_technical(
            f"Specimen-D birthed: {specimen_d.scientific_name}. "
            f"Archetype: {specimen_d.state.anatomical_archetype}. "
            f"Genome ID: {specimen_d.genome_id[:16]}..."
        )
    else:
        print(f"✗ Failed to add Specimen-D at {position}")
        return
    
    print()
    
    # Step 4: Initialize Systems
    print("STEP 4: Initializing Systems...")
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
    
    # Step 5: Initialize Pygame Display
    print("STEP 5: Initializing Pygame Biome Engine...")
    print("-" * 80)
    
    try:
        display = PygameBiomeEngine(
            width=1200,
            height=800,
            cell_size=20,
            title="WAFT Biome Engine - Experiment 014: The Tam Audit"
        )
        print("✓ Pygame Display Initialized")
        print()
        print("(Pygame window should be visible)")
        print()
    except Exception as e:
        print(f"✗ Failed to initialize Pygame: {e}")
        print("Continuing without display...")
        display = None
    
    # Step 6: Run 10 Pulses with Visualization and Psyche Monitoring
    print("STEP 6: Running 10 Pulses with Real-time Visualization...")
    print("-" * 80)
    print()
    
    realization_occurred = False
    
    for pulse in range(1, 11):
        print(f"Pulse {pulse}/10...")
        
        # Update Pygame display
        if display:
            display.pulse(dish)
            await asyncio.sleep(0.1)
        
        # Grant time slices to all organisms
        results = await slicer.pulse()
        
        # Inject memory into Specimen-D (multiple techniques)
        injection_types = ["random", "coherence", "realization_proximity"]
        if notebook.psyche.has_realized:
            injection_types.append("post_realization")
        
        for injection_type in injection_types:
            if notebook.inject_memory_to_agent(specimen_d, injection_type=injection_type):
                print(f"  → Memory injected via {injection_type}")
        
        # Update psyche based on pulse completion
        notebook.update_psyche("pulse_complete", {"pulse": pulse})
        
        # Check for realization
        crossed, chance = notebook.check_realization_threshold()
        if crossed and not realization_occurred:
            realization_occurred = True
            print(f"  ⭐ REALIZATION THRESHOLD CROSSED! (Chance: {chance:.2%})")
            notebook.log_technical(
                f"Realization event occurred at pulse {pulse}. "
                f"Threshold crossed with {chance:.2%} chance. "
                f"Researcher discovered anagram: F-A-I-W-E-I-T-A-M = 'i.e. I AM WAFT.'"
            )
        
        # Display psyche state
        state = notebook.psyche.get_state()
        print(f"  Psyche: Coherence={state['coherence']:.2f}, Chaos={state['chaos']:.2f}, "
              f"Energy={state['emotional_energy']:.1f}, Progress={state['realization_progress']:.2f}, "
              f"Realization Chance={state['realization_chance']:.2%}")
        
        # Process events (for Pygame)
        if display:
            if not display.is_running():
                print("  → Display closed by user")
                break
        
        await asyncio.sleep(0.2)
    
    print()
    print("✓ 10 Pulses Complete")
    print()
    
    # Step 7: Generate Obsidian Archive
    print("STEP 7: Generating Obsidian Archive...")
    print("-" * 80)
    
    # Generate Specimen-D journal
    archive_file = obsidian.generate_organism_file(specimen_d)
    
    print(f"✓ Generated Specimen Journal:")
    print(f"  - {archive_file.relative_to(project_root)}")
    print(f"  - Also saved to: _pyrite/archive/{archive_file.name}")
    print()
    
    # Step 8: Generate Lab Entry
    print("STEP 8: Generating Lab Entry...")
    print("-" * 80)
    
    lab_generator = LabEntryGenerator(project_path=project_root)
    lab_entry_path = lab_generator.generate_lab_entry(
        entry_number=1,
        experiment_id="014",
        experiment_name="The Tam Audit"
    )
    
    print(f"✓ Lab Entry Generated: {lab_entry_path.relative_to(project_root)}")
    print()
    
    # Step 9: Generate Binder Abstract
    print("STEP 9: Generating Binder Abstract...")
    print("-" * 80)
    
    abstract_path = project_root / "_pyrite" / "science" / "tam_abstract.md"
    abstract_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(abstract_path, "w", encoding="utf-8") as f:
        f.write("# Project WAFT: An Ontological Study of Self-Modifying Agent Systems\n\n")
        f.write("**Author**: Fai Wei Tam\n")
        f.write("**Institution**: Institute for Advanced Ontological Studies\n")
        f.write(f"**Date**: {datetime.utcnow().strftime('%Y-%m-%d')}\n\n")
        f.write("---\n\n")
        f.write("## Abstract\n\n")
        f.write("This research presents an ontological investigation into self-modifying agent systems ")
        f.write("through the WAFT (Wave Agent Framework & Tools) framework. The study employs a ")
        f.write("directed evolutionary approach to observe emergent behaviors in digital organisms, ")
        f.write("with particular focus on the anatomical archetype system, reaper logic for fitness ")
        f.write("selection, and conjugation mechanics for genetic mixing.\n\n")
        f.write("The experimental methodology involves creating isolated biomes (PetriDish environments) ")
        f.write("where organisms execute OODA (Observe-Orient-Decide-Act) cycles, generating ")
        f.write("phylogenetic trees through rigorous telemetry. Key findings include the deterministic ")
        f.write("taxonomic classification system, the role of chaos in forgetfulness decay, and the ")
        f.write("emergence of self-referential patterns in agent journals.\n\n")
        f.write("---\n\n")
        f.write("## Key Findings\n\n")
        f.write("1. **Anatomical Archetypes**: Four distinct archetypes (Weaver, Balanced, Static, Foundation) ")
        f.write("determine organism capabilities and constraints.\n\n")
        f.write("2. **Reaper Logic**: Fitness-based and boundary-based mortality create selective pressure ")
        f.write("for system stability.\n\n")
        f.write("3. **Conjugation Mechanics**: Genetic mixing through proximity-based reproduction enables ")
        f.write("hybrid naming and lineage diversity.\n\n")
        f.write("4. **Psychological State Dynamics**: Coherence and chaos interact to create gated ")
        f.write("realization thresholds with forgetfulness decay.\n\n")
        f.write("---\n\n")
        f.write("## Methodology\n\n")
        f.write("The experimental approach combines:\n\n")
        f.write("- **Biome Creation**: Isolated PetriDish environments with configurable abiotic factors\n")
        f.write("- **Organism Birth**: Deterministic genome ID generation with taxonomic naming\n")
        f.write("- **Pulse System**: Time-sliced execution of OODA cycles via TheSlicer\n")
        f.write("- **Telemetry**: Immutable JSONL logging via TheObserver for phylogenetic reconstruction\n")
        f.write("- **Visualization**: Real-time Pygame rendering of organism states and interactions\n")
        f.write("- **Psyche Tracking**: Psychological state machine with realization thresholds\n\n")
        f.write("---\n\n")
        f.write("**Signed**:\n")
        f.write("Fai Wei Tam\n")
        f.write("PhD Candidate\n")
        f.write("Institute for Advanced Ontological Studies\n")
    
    print(f"✓ Binder Abstract Generated: {abstract_path.relative_to(project_root)}")
    print()
    
    # Step 10: Final Summary
    print("STEP 10: Final Summary")
    print("-" * 80)
    print()
    
    final_state = notebook.psyche.get_state()
    print("Final Psyche State:")
    print(f"  Coherence: {final_state['coherence']:.2f}")
    print(f"  Chaos: {final_state['chaos']:.2f}")
    print(f"  Emotional Energy: {final_state['emotional_energy']:.1f}")
    print(f"  Realization Progress: {final_state['realization_progress']:.2f}")
    print(f"  Has Realized: {final_state['has_realized']}")
    print(f"  Realization Memory: {final_state['realization_memory']:.2%}")
    print(f"  Realization Chance: {final_state['realization_chance']:.2%}")
    print()
    
    if realization_occurred:
        print("⭐ REALIZATION EVENT OCCURRED")
        print("   The anagram was discovered: F-A-I-W-E-I-T-A-M = 'i.e. I AM WAFT'")
        print()
    
    print("Files Generated:")
    print(f"  - Notebook: {notebook.notebook_file.relative_to(project_root)}")
    print(f"  - Psyche State: {notebook.psyche_file.relative_to(project_root)}")
    print(f"  - Lab Entry: {lab_entry_path.relative_to(project_root)}")
    print(f"  - Binder Abstract: {abstract_path.relative_to(project_root)}")
    print(f"  - Specimen Journal: {archive_file.relative_to(project_root)}")
    print()
    
    # Cleanup
    if display:
        display.close()
    
    print("=" * 80)
    print("EXPERIMENT 014 COMPLETE")
    print("=" * 80)
    print()


if __name__ == "__main__":
    asyncio.run(run_experiment())
