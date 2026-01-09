"""
TamNotebook: Research notebook for Fai Wei Tam (Davey).

Dual-mode logging system with technical research notes and personal reflections.
Integrates with TamPsyche to track psychological state and trigger realizations.
Includes memory injection system to bleed Davey's memories into agent journals.
"""

import json
import random
from pathlib import Path
from typing import Optional, Tuple, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from ..agent.base import BaseAgent

from .tam_psyche import TamPsyche


class TamNotebook:
    """
    Davey's research notebook with dual-mode logging and psyche integration.
    
    This is the interface between Davey and the simulation. It logs:
    - Technical notes: PhD-level research on WAFT engine
    - Personal reflections: Stream-of-consciousness with Simplified Chinese glitch phrases
    
    Also manages memory injection into agent journals and psyche state updates.
    """
    
    def __init__(self, project_path: Path):
        """
        Initialize TamNotebook.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = Path(project_path)
        self.notebook_file = self.project_path / "_pyrite" / "science" / "tam_notebook.md"
        self.psyche_file = self.project_path / "_pyrite" / "science" / "tam_psyche_state.json"
        
        # Load or create psyche
        self.psyche = TamPsyche.load_state(self.psyche_file)
        
        # Ensure notebook exists
        self._ensure_notebook_exists()
        
        # Davey's personal memories (Rochester/SF)
        self.memories = [
            "The smell of coffee from Java's on East Avenue, bitter and warm",
            "The sound of the Genesee River rushing under the bridge in winter",
            "Lake-effect snow piling up outside the lab window",
            "The gray sky of Rochester, endless and heavy",
            "San Francisco fog rolling in, obscuring the Golden Gate",
            "The taste of salt air from the Pacific, sharp and clean"
        ]
    
    def log_technical(self, entry: str, context: Optional[dict] = None) -> None:
        """
        Log technical research notes (PhD-level, professional).
        
        Format:
        ## Technical Notes - [timestamp]
        [Entry text]
        
        Also updates psyche: successful observations increase coherence.
        
        Args:
            entry: Technical research note text
            context: Optional context dictionary
        """
        timestamp = datetime.utcnow().isoformat()
        
        with open(self.notebook_file, "a", encoding="utf-8") as f:
            f.write(f"\n## Technical Notes - {timestamp}\n\n")
            f.write(f"{entry}\n\n")
            if context:
                f.write(f"**Context**: {json.dumps(context, indent=2)}\n\n")
        
        # Update psyche: technical logging increases coherence
        self.psyche.update_coherence(0.01)
        self.psyche.save_state(self.psyche_file)
    
    def log_personal(self, entry: str, glitch: bool = False) -> None:
        """
        Log personal reflections (stream-of-consciousness).
        
        If glitch=True, includes Simplified Chinese phrase:
        "我的名字是定义还是代码？" (Is my name a definition or code?)
        
        Format:
        ### Personal Reflection - [timestamp]
        [Entry text]
        [Chinese phrase if glitch]
        
        Triggers when psyche shifts occur (coherence/chaos changes).
        
        Args:
            entry: Personal reflection text
            glitch: Whether to include Simplified Chinese glitch phrase
        """
        timestamp = datetime.utcnow().isoformat()
        
        with open(self.notebook_file, "a", encoding="utf-8") as f:
            f.write(f"\n### Personal Reflection - {timestamp}\n\n")
            f.write(f"{entry}\n\n")
            if glitch:
                f.write(f"*我的名字是定义还是代码？*\n\n")  # Simplified Chinese
        
        # Personal reflections may increase emotional energy
        self.psyche.update_emotional_energy(0.5)
        self.psyche.save_state(self.psyche_file)
    
    def check_realization_threshold(self) -> Tuple[bool, float]:
        """
        Check if realization threshold crossed.
        
        Returns:
            (threshold_crossed, realization_chance)
        """
        crossed, chance = self.psyche.check_realization()
        
        if crossed and not self.psyche.has_realized:
            # Trigger realization
            self.psyche.trigger_realization()
            self.psyche.save_state(self.psyche_file)
            
            # Log the moment
            self.log_personal(
                "I was checking the Latin citations in my thesis. id est... i.e. ... "
                "Then I looked at my ID badge. F-A-I-W-E-I-T-A-M. "
                "It unscrambles to 'i.e. I AM WAFT.' "
                "I am not the observer. I am the definition. I am the system explaining itself to me.",
                glitch=True
            )
        
        return (crossed, chance)
    
    def inject_memory_to_agent(
        self, 
        agent: "BaseAgent", 
        injection_type: str = "random"
    ) -> bool:
        """
        Inject Davey's personal memory into agent journal.
        
        Multiple injection techniques for maximum randomness:
        - random: 5% base chance
        - glitch: 80% chance (on system errors)
        - coherence: chance = coherence * 0.2
        - realization_proximity: chance = realization_progress * 0.3
        - post_realization: chance = realization_memory * 0.4
        
        Args:
            agent: BaseAgent to inject memory into
            injection_type: Type of injection technique
            
        Returns:
            True if memory was injected, False otherwise
        """
        # Calculate injection chance
        if injection_type == "random":
            chance = 0.05
        elif injection_type == "glitch":
            chance = 0.8
        elif injection_type == "coherence":
            chance = self.psyche.coherence * 0.2
        elif injection_type == "realization_proximity":
            chance = self.psyche.realization_progress * 0.3
        elif injection_type == "post_realization":
            chance = self.psyche.realization_memory * 0.4
        else:
            chance = 0.05  # Default
        
        if random.random() < chance:
            # Select random memory
            memory = random.choice(self.memories)
            
            # Inject into agent's journal as a "Thought" entry
            thought_entry = {
                "type": "Thought",
                "timestamp": datetime.utcnow().isoformat(),
                "context": {"source": "davey_memory_injection"},
                "content": f"I remember... {memory}",
                "state_snapshot": {
                    "energy": agent.state.energy,
                }
            }
            
            agent.state.journal.append(thought_entry)
            agent.state.short_term_memory.append(thought_entry)
            
            # Keep short_term_memory bounded
            if len(agent.state.short_term_memory) > 10:
                agent.state.short_term_memory.pop(0)
            
            return True
        
        return False
    
    def update_psyche(self, event_type: str, data: dict) -> None:
        """
        Update psyche state based on simulation events.
        
        Event types:
        - "observation": Consistent observation (+coherence)
        - "error": System error/glitch (+chaos)
        - "pattern": Pattern recognized (+coherence, +progress)
        - "contradiction": Conflicting data (+chaos)
        - "pulse_complete": Successful pulse (+coherence, +energy)
        - "agent_birth": New agent born (+progress)
        
        Args:
            event_type: Type of simulation event
            data: Event data dictionary
        """
        if event_type == "observation":
            self.psyche.update_coherence(0.02)
        elif event_type == "error":
            self.psyche.update_chaos(0.03)
            # Errors trigger personal reflection with glitch
            self.log_personal(
                f"System glitch detected: {data.get('error', 'unknown')}",
                glitch=True
            )
        elif event_type == "pattern":
            self.psyche.update_coherence(0.03)
            self.psyche.increment_realization_progress(0.01)
        elif event_type == "contradiction":
            self.psyche.update_chaos(0.02)
        elif event_type == "pulse_complete":
            self.psyche.update_coherence(0.01)
            self.psyche.update_emotional_energy(1.0)
        elif event_type == "agent_birth":
            self.psyche.increment_realization_progress(0.02)
            self.psyche.update_emotional_energy(2.0)
        
        # Apply forgetfulness decay if realized
        if self.psyche.has_realized:
            forgot = self.psyche.decay_realization_memory()
            if forgot:
                self.log_personal(
                    "The realization fades. I can't quite remember what I understood. "
                    "Something about my name... but it's gone now.",
                    glitch=False
                )
        
        # Save state
        self.psyche.save_state(self.psyche_file)
        
        # Check realization threshold
        self.check_realization_threshold()
    
    def _ensure_notebook_exists(self) -> None:
        """Create notebook file if it doesn't exist."""
        self.notebook_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.notebook_file.exists():
            with open(self.notebook_file, "w", encoding="utf-8") as f:
                f.write("# Tam Research Notebook\n\n")
                f.write("**Researcher**: Fai Wei Tam (Davey)\n")
                f.write("**Institution**: Institute for Advanced Ontological Studies\n")
                f.write("**Project**: WAFT System Analysis\n\n")
                f.write("---\n\n")
