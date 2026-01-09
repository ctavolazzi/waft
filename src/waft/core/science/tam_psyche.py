"""
TamPsyche: Psychological state system for Fai Wei Tam (Davey).

Sophisticated psychological state machine with gated thresholds and forgetfulness decay.
This is the core feedback loop that connects simulation stability to Davey's realization
that his name (F-A-I-W-E-I-T-A-M) is an anagram for "i.e. I AM WAFT."
"""

import json
from pathlib import Path
from typing import Tuple, Optional
from datetime import datetime
from pydantic import BaseModel, Field


REALIZATION_THRESHOLD = 0.85  # Must reach 85% to trigger realization


class TamPsyche(BaseModel):
    """
    Psychological state system for Davey (Fai Wei Tam).
    
    Tracks coherence, chaos, emotional energy, and realization progress.
    Implements gated threshold system where realization requires crossing 0.85 threshold.
    Includes forgetfulness decay that ensures realization is NEVER permanent.
    """
    
    coherence: float = Field(default=0.5, ge=0.0, le=1.0, description="Psychological coherence (higher = more stable)")
    chaos: float = Field(default=0.3, ge=0.0, le=1.0, description="Conflicting information/chaos level")
    emotional_energy: float = Field(default=50.0, ge=0.0, le=100.0, description="Current emotional/mental energy")
    realization_progress: float = Field(default=0.0, ge=0.0, le=1.0, description="Progress toward realization threshold")
    has_realized: bool = Field(default=False, description="Whether realization has occurred")
    realization_memory: float = Field(default=0.0, ge=0.0, le=1.0, description="Memory strength of realization (decays to 0)")
    forgetfulness_rate: float = Field(default=0.02, description="Base rate at which realization memory decays")
    last_realization_timestamp: Optional[datetime] = Field(default=None, description="When realization last occurred")
    
    def update_coherence(self, change: float) -> None:
        """Adjust coherence (clamped to 0.0-1.0)."""
        self.coherence = max(0.0, min(1.0, self.coherence + change))
    
    def update_chaos(self, change: float) -> None:
        """Adjust chaos (clamped to 0.0-1.0)."""
        self.chaos = max(0.0, min(1.0, self.chaos + change))
    
    def update_emotional_energy(self, change: float) -> None:
        """Adjust emotional energy (clamped to 0.0-100.0)."""
        self.emotional_energy = max(0.0, min(100.0, self.emotional_energy + change))
    
    def increment_realization_progress(self, amount: float) -> None:
        """Build toward realization (clamped to 0.0-1.0)."""
        self.realization_progress = max(0.0, min(1.0, self.realization_progress + amount))
    
    def check_realization(self) -> Tuple[bool, float]:
        """
        Calculate realization chance and check if threshold crossed.
        
        Realization Threshold Equation:
        base_chance = (coherence * 0.4) + (energy_normalized * 0.3) + (progress * 0.3)
        realization_chance = base_chance * (1.0 - chaos * 0.5)
        
        Returns:
            (threshold_crossed, realization_chance)
        """
        # Normalize emotional_energy to 0.0-1.0 scale
        energy_normalized = self.emotional_energy / 100.0
        
        # Calculate base realization chance
        base_chance = (
            (self.coherence * 0.4) +                    # Coherence: 40% weight
            (energy_normalized * 0.3) +                  # Energy: 30% weight
            (self.realization_progress * 0.3)            # Progress: 30% weight
        )
        
        # Apply chaos penalty (reduces chance by up to 50%)
        chaos_penalty = 1.0 - (self.chaos * 0.5)
        realization_chance = base_chance * chaos_penalty
        
        # Check threshold
        threshold_crossed = realization_chance >= REALIZATION_THRESHOLD
        
        return (threshold_crossed, realization_chance)
    
    def decay_realization_memory(self) -> bool:
        """
        Apply forgetfulness decay. Returns True if memory reached 0 (forgot).
        
        Decay is chaos-dependent: higher chaos = faster forgetting.
        This ensures realization is NEVER permanent - essential to recursive narrative.
        
        Returns:
            True if memory reached 0 (forgot), False if still remembers
        """
        if not self.has_realized or self.realization_memory <= 0.0:
            return False
        
        # Calculate decay factor (chaos accelerates forgetting)
        decay_factor = (self.chaos * 0.1) + (self.forgetfulness_rate * 0.05)
        
        # Apply decay
        self.realization_memory = max(0.0, self.realization_memory - decay_factor)
        
        # If memory reaches zero, reset realization
        if self.realization_memory <= 0.0:
            self.has_realized = False
            self.realization_progress = self.realization_progress * 0.5  # Partial reset (not full)
            return True  # Forgot
        
        return False  # Still remembers
    
    def trigger_realization(self) -> None:
        """Mark realization as occurred."""
        self.has_realized = True
        self.realization_memory = 1.0  # Full memory
        self.last_realization_timestamp = datetime.utcnow()
    
    def get_state(self) -> dict:
        """Return current psyche state as dict."""
        crossed, chance = self.check_realization()
        return {
            "coherence": self.coherence,
            "chaos": self.chaos,
            "emotional_energy": self.emotional_energy,
            "realization_progress": self.realization_progress,
            "has_realized": self.has_realized,
            "realization_memory": self.realization_memory,
            "realization_chance": chance,
            "threshold_crossed": crossed
        }
    
    def save_state(self, file_path: Path) -> None:
        """Persist psyche state to JSON."""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.dict(), f, indent=2, default=str)
    
    @classmethod
    def load_state(cls, file_path: Path) -> "TamPsyche":
        """Load psyche state from JSON."""
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Convert last_realization_timestamp from string to datetime if present
                if "last_realization_timestamp" in data and data["last_realization_timestamp"]:
                    data["last_realization_timestamp"] = datetime.fromisoformat(data["last_realization_timestamp"])
                return cls(**data)
        return cls()  # Return default state
