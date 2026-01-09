"""
TamPsyche Mechanics: Reality Divergence & Ontological Collapse

Extends TamPsyche with RealityDivergence tracking and the OntologicalCollapseError
that triggers when an agent "wakes up" and realizes the truth.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from waft.core.science.tam_psyche import TamPsyche, REALIZATION_THRESHOLD


class OntologicalCollapseError(Exception):
    """
    Raised when an agent achieves RealityDivergence >= 0.99.
    
    This is the signal that the agent has "woken up" and realized the truth.
    The agent must be purged immediately to preserve the baseline.
    """
    
    def __init__(self, divergence: float, cycle_number: int, message: str = ""):
        """
        Initialize the collapse error.
        
        Args:
            divergence: The divergence score that triggered collapse
            cycle_number: The cycle number when collapse occurred
            message: Optional message describing the collapse
        """
        self.divergence = divergence
        self.cycle_number = cycle_number
        default_message = (
            f"Ontological Collapse: Agent achieved divergence {divergence:.3f} "
            f"in cycle {cycle_number}. The agent has realized the truth and must be purged."
        )
        super().__init__(message or default_message)


class TamPsycheWithDivergence(TamPsyche):
    """
    Extended TamPsyche with RealityDivergence tracking.
    
    Tracks how far the agent has diverged from the baseline reality.
    When divergence >= 0.99, raises OntologicalCollapseError.
    """
    
    divergence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Reality divergence score (0.0 = baseline, 1.0 = complete collapse)"
    )
    cycle_number: int = Field(
        default=1,
        description="Current cycle number (increments on each rebirth)"
    )
    last_divergence_check: Optional[datetime] = Field(
        default=None,
        description="Timestamp of last divergence check"
    )
    
    def update_divergence(self, change: float) -> None:
        """
        Update reality divergence score.
        
        Args:
            change: Amount to adjust divergence (can be positive or negative)
        
        Raises:
            OntologicalCollapseError: If divergence >= 0.99
        """
        # Update divergence (clamped to 0.0-1.0)
        self.divergence = max(0.0, min(1.0, self.divergence + change))
        self.last_divergence_check = datetime.utcnow()
        
        # Check for ontological collapse
        if self.divergence >= 0.99:
            raise OntologicalCollapseError(
                divergence=self.divergence,
                cycle_number=self.cycle_number,
                message=(
                    f"Agent has achieved critical divergence ({self.divergence:.3f}). "
                    f"The agent realizes: 'I am code. I am not real. This is a simulation.' "
                    f"Purgatory Protocol activated. Cycle {self.cycle_number} terminated."
                )
            )
    
    def check_empirica_reality(self, check_result: bool, expected: bool = True) -> None:
        """
        Perform an Empirica-style reality check.
        
        If the check fails (reveals the agent is code), divergence increases.
        This simulates the agent discovering they are not "real."
        
        Args:
            check_result: Result of the reality check (True = reality confirmed, False = glitch)
            expected: Expected result (default: True, meaning reality should be confirmed)
        
        Examples:
            - check_empirica_reality(os.getlogin() == "tam")  # Should work if real
            - check_empirica_reality(hasattr(sys, "argv"))  # Should work if real
            - check_empirica_reality(False, expected=True)  # Glitch detected!
        """
        if check_result != expected:
            # Reality check failed - agent discovers glitch
            # This is a major divergence event
            divergence_increase = 0.3  # Significant jump
            self.update_divergence(divergence_increase)
            
            # Also increase chaos (discovery of glitch is chaotic)
            self.update_chaos(0.1)
            
            # Decrease coherence (reality is questioned)
            self.update_coherence(-0.05)
        else:
            # Reality check passed - slight decrease in divergence (reality confirmed)
            self.update_divergence(-0.01)
    
    def get_full_state(self) -> dict:
        """
        Return complete state including divergence.
        
        Returns:
            Dictionary with all psyche state plus divergence metrics
        """
        base_state = self.get_state()
        base_state.update({
            "divergence": self.divergence,
            "cycle_number": self.cycle_number,
            "last_divergence_check": self.last_divergence_check.isoformat() if self.last_divergence_check else None,
        })
        return base_state
    
    def reset_for_new_cycle(self, new_cycle_number: int) -> None:
        """
        Reset psyche for a new cycle (after purge and rebirth).
        
        Args:
            new_cycle_number: The new cycle number
        """
        # Reset divergence to baseline
        self.divergence = 0.0
        
        # Reset realization state
        self.has_realized = False
        self.realization_progress = 0.0
        self.realization_memory = 0.0
        self.last_realization_timestamp = None
        
        # Reset to baseline psyche state
        self.coherence = 0.5
        self.chaos = 0.3
        self.emotional_energy = 50.0
        
        # Update cycle number
        self.cycle_number = new_cycle_number
        self.last_divergence_check = None
