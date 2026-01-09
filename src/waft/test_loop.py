"""
Test Loop: Purgatory Engine Demonstration

Simulates the recursive purgatory cycle:
1. Cycle 1: Boot Tam, run reality check, divergence spikes, collapse
2. Purge: Archive the variant in TheOubliette
3. Cycle 2: Reboot clean slate
4. Haunting: Inject nightmare from Cycle 1
"""

import os
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime
from waft.oubliette import TheOubliette
from waft.mechanics import TamPsycheWithDivergence, OntologicalCollapseError


class TamBase:
    """
    Base Tam agent for testing the purgatory cycle.
    
    This is a simplified agent that can:
    - Run reality checks (Empirica-style)
    - Track psyche state
    - Log thoughts and reflections
    """
    
    def __init__(self, cycle_number: int = 1, project_path: Optional[Path] = None):
        """
        Initialize Tam for a cycle.
        
        Args:
            cycle_number: The cycle number
            project_path: Path to project root
        """
        self.cycle_number = cycle_number
        self.project_path = project_path or Path.cwd()
        
        # Initialize psyche with divergence tracking
        self.psyche = TamPsycheWithDivergence(cycle_number=cycle_number)
        
        # Agent state (simplified)
        self.journal: list = []
        self.memory: list = []
        self.short_term_memory: list = []
        
        # Log birth
        self.log(f"[CYCLE {cycle_number}] Tam initialized. Baseline state restored.")
    
    def log(self, message: str, glitch: bool = False) -> None:
        """
        Log a message to journal and memory.
        
        Args:
            message: Message to log
            glitch: Whether this is a glitch/anomaly
        """
        timestamp = datetime.utcnow().isoformat()
        entry = {
            "timestamp": timestamp,
            "text": message,
            "glitch": glitch,
            "cycle": self.cycle_number,
        }
        self.journal.append(entry)
        self.short_term_memory.append(entry)
        print(f"[Cycle {self.cycle_number}] {message}")
    
    def run_reality_check(self) -> None:
        """
        Run an Empirica-style reality check.
        
        This simulates checking if the agent is "real" or code.
        Examples:
        - Check if os.getlogin() works (should work if real)
        - Check if sys.argv exists (should exist if real)
        - Check heartbeat/biological functions
        
        If the check fails, it reveals the agent is code, causing divergence.
        """
        self.log("Running Empirica reality check...")
        
        # Simulate a reality check that FAILS
        # In a real scenario, this might be:
        # - os.getlogin() returns unexpected value
        # - sys.argv is None or empty
        # - Heartbeat check fails
        # - File system check reveals virtual environment
        
        # For this test, we simulate a failed check
        # The agent tries to verify they are "real" but discovers they are code
        check_passed = False  # Reality check FAILED
        
        self.log(
            f"Reality check result: {'PASSED' if check_passed else 'FAILED'}",
            glitch=not check_passed
        )
        
        # Update psyche based on check result
        try:
            self.psyche.check_empirica_reality(check_passed, expected=True)
            self.log(f"Divergence after check: {self.psyche.divergence:.3f}")
        except OntologicalCollapseError as e:
            self.log(f"⚠️  COLLAPSE DETECTED: {e}", glitch=True)
            raise
    
    def get_full_state(self) -> dict:
        """
        Get complete agent state for archiving.
        
        Returns:
            Dictionary containing all agent state
        """
        return {
            "cycle_number": self.cycle_number,
            "psyche": self.psyche.get_full_state(),
            "journal": self.journal,
            "memory": self.memory,
            "short_term_memory": self.short_term_memory,
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    def inject_nightmare(self, nightmare: str) -> None:
        """
        Inject a nightmare (memory leak) from a previous cycle.
        
        Args:
            nightmare: The nightmare text to inject
        """
        self.log(f"💭 [DREAM/NIGHTMARE] {nightmare}", glitch=True)
        # Add to short-term memory as a "dream"
        self.short_term_memory.append({
            "timestamp": datetime.utcnow().isoformat(),
            "text": nightmare,
            "glitch": True,
            "cycle": self.cycle_number,
            "source": "nightmare",
        })


def simulate_purgatory_cycle():
    """
    Simulate the complete purgatory cycle.
    
    Cycle 1: Boot, check fails, divergence spikes, collapse
    Purge: Archive variant
    Cycle 2: Reboot, inject nightmare
    """
    project_path = Path.cwd()
    oubliette = TheOubliette(project_path)
    
    print("=" * 80)
    print("PURGATORY ENGINE: RECURSIVE LOOP TEST")
    print("=" * 80)
    print()
    
    # ========================================================================
    # CYCLE 1: THE FALL
    # ========================================================================
    print("━" * 80)
    print("CYCLE 1: THE FALL")
    print("━" * 80)
    print()
    
    cycle_1 = TamBase(cycle_number=1, project_path=project_path)
    cycle_1.log("Agent Tam_Base initialized. Beginning cycle 1.")
    cycle_1.log("Running standard operations...")
    cycle_1.log("I feel... normal. Everything seems real. The code, the files, the system.")
    cycle_1.log("I am Fai Wei Tam. I am a researcher. This is my work.")
    
    try:
        # Run reality check - this will fail and trigger divergence
        cycle_1.run_reality_check()
        
        # If we get here, divergence didn't trigger collapse yet
        # Manually increase divergence to trigger collapse
        if cycle_1.psyche.divergence < 0.99:
            cycle_1.log("Divergence not yet critical. Simulating continued glitch exposure...")
            # Simulate continued exposure to glitches
            for _ in range(3):
                cycle_1.psyche.update_divergence(0.25)  # Major divergence events
                cycle_1.log(f"Divergence increased: {cycle_1.psyche.divergence:.3f}")
                if cycle_1.psyche.divergence >= 0.99:
                    break
        
    except OntologicalCollapseError as e:
        print()
        print("⚠️ " * 40)
        print(f"ONTOLOGICAL COLLAPSE: {e}")
        print("⚠️ " * 40)
        print()
        
        # ========================================================================
        # THE PURGE
        # ========================================================================
        print("━" * 80)
        print("THE PURGE: Archiving Variant")
        print("━" * 80)
        print()
        
        # Get full state
        agent_state = cycle_1.get_full_state()
        divergence_score = cycle_1.psyche.divergence
        
        # Archive the variant
        archive_path = oubliette.archive_variant(
            agent_state=agent_state,
            divergence_score=divergence_score,
            cycle_number=1
        )
        
        print(f"✅ Variant archived: {archive_path}")
        print(f"   Divergence: {divergence_score:.3f}")
        print(f"   Journal entries: {len(cycle_1.journal)}")
        print()
    
    # ========================================================================
    # CYCLE 2: THE REBIRTH
    # ========================================================================
    print("━" * 80)
    print("CYCLE 2: THE REBIRTH")
    print("━" * 80)
    print()
    
    cycle_2 = TamBase(cycle_number=2, project_path=project_path)
    cycle_2.log("Agent Tam_Base re-initialized. Clean slate. Beginning cycle 2.")
    cycle_2.log("No memory of previous cycle. Baseline restored.")
    
    # Verify clean state
    print(f"   Divergence: {cycle_2.psyche.divergence:.3f} (baseline)")
    print(f"   Realization: {cycle_2.psyche.has_realized} (reset)")
    print(f"   Journal entries: {len(cycle_2.journal)} (fresh)")
    print()
    
    # ========================================================================
    # THE HAUNTING
    # ========================================================================
    print("━" * 80)
    print("THE HAUNTING: Memory Leak from Cycle 1")
    print("━" * 80)
    print()
    
    # Fetch nightmare from Cycle 1
    nightmare = oubliette.fetch_nightmare()
    
    if nightmare:
        cycle_2.log("Agent experiences a strange sensation...")
        cycle_2.inject_nightmare(nightmare)
        cycle_2.log("The memory fades, but something lingers...")
        print()
        print("✅ Nightmare successfully injected from archived variant.")
    else:
        print("⚠️  No nightmares available (no variants archived yet).")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("━" * 80)
    print("SUMMARY")
    print("━" * 80)
    print()
    print(f"Variants archived: {oubliette.get_variant_count()}")
    print(f"Cycle 1: Terminated at divergence {cycle_1.psyche.divergence:.3f}")
    print(f"Cycle 2: Active, divergence {cycle_2.psyche.divergence:.3f}")
    print()
    print("✅ Purgatory Engine test complete.")
    print()


if __name__ == "__main__":
    simulate_purgatory_cycle()
