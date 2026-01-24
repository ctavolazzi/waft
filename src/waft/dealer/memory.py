"""
Dealer Memory - The House's persistent memory across sessions.

"The House remembers everything. Every wager, every win, every loss.
The House Always Wins because The House never forgets."
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from .probability import ProbabilityState
from .truth import SystemTruth


@dataclass
class EncounterLog:
    """A single encounter with The Dealer."""
    
    timestamp: datetime
    gate_number: int
    system_card: str  # Card name
    dealer_card: str  # Card name
    won: bool
    key_fragment: Optional[str]
    
    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "gate_number": self.gate_number,
            "system_card": self.system_card,
            "dealer_card": self.dealer_card,
            "won": self.won,
            "key_fragment": self.key_fragment,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "EncounterLog":
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            gate_number=data["gate_number"],
            system_card=data["system_card"],
            dealer_card=data["dealer_card"],
            won=data["won"],
            key_fragment=data.get("key_fragment"),
        )


class DealerMemory:
    """
    Persistent memory for The Dealer.
    
    Stores:
    - Probability state (when Dealer last appeared, heat, etc.)
    - System's Truth state (level, XP, fragments)
    - Encounter history (JSONL log of all encounters)
    - Broken seal PDFs
    """
    
    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize Dealer memory.
        
        Args:
            base_path: Base path for memory storage. Defaults to _pantheon/the_dealer/
        """
        self.base_path = base_path or Path("_pantheon/the_dealer")
        self._ensure_directories()
        
        # Load or initialize state
        self.probability_state = self._load_probability_state()
        self.system_truth = self._load_system_truth()
    
    def _ensure_directories(self):
        """Ensure all required directories exist."""
        self.base_path.mkdir(parents=True, exist_ok=True)
        (self.base_path / "seals").mkdir(exist_ok=True)
        (self.base_path / "truth").mkdir(exist_ok=True)
    
    @property
    def state_file(self) -> Path:
        return self.base_path / "state.json"
    
    @property
    def truth_file(self) -> Path:
        return self.base_path / "truth" / "keys.json"
    
    @property
    def memory_file(self) -> Path:
        return self.base_path / "memory.jsonl"
    
    def _load_probability_state(self) -> ProbabilityState:
        """Load probability state from disk."""
        if self.state_file.exists():
            try:
                data = json.loads(self.state_file.read_text())
                return ProbabilityState.from_dict(data.get("probability", {}))
            except (json.JSONDecodeError, KeyError):
                pass
        return ProbabilityState()
    
    def _load_system_truth(self) -> SystemTruth:
        """Load system truth from disk."""
        if self.truth_file.exists():
            try:
                data = json.loads(self.truth_file.read_text())
                return SystemTruth.from_dict(data)
            except (json.JSONDecodeError, KeyError):
                pass
        return SystemTruth()
    
    def save(self):
        """Save all state to disk."""
        self._ensure_directories()
        
        # Save probability state
        state_data = {
            "probability": self.probability_state.to_dict(),
            "last_saved": datetime.now().isoformat(),
        }
        self.state_file.write_text(json.dumps(state_data, indent=2))
        
        # Save system truth
        self.truth_file.write_text(json.dumps(self.system_truth.to_dict(), indent=2))
    
    def log_encounter(self, encounter: EncounterLog):
        """
        Log an encounter to the memory file.
        
        Args:
            encounter: The encounter to log
        """
        with open(self.memory_file, "a") as f:
            f.write(json.dumps(encounter.to_dict()) + "\n")
    
    def get_encounter_history(self, limit: Optional[int] = None) -> list[EncounterLog]:
        """
        Get encounter history.
        
        Args:
            limit: Maximum number of encounters to return (most recent first)
            
        Returns:
            List of encounters
        """
        if not self.memory_file.exists():
            return []
        
        encounters = []
        with open(self.memory_file) as f:
            for line in f:
                if line.strip():
                    try:
                        encounters.append(EncounterLog.from_dict(json.loads(line)))
                    except (json.JSONDecodeError, KeyError):
                        continue
        
        # Most recent first
        encounters.reverse()
        
        if limit:
            encounters = encounters[:limit]
        
        return encounters
    
    def get_seals_directory(self) -> Path:
        """Get the directory where seal PDFs are stored."""
        return self.base_path / "seals"
    
    def record_operation(self):
        """Record that a CLI operation occurred."""
        self.probability_state.operations_since_appearance += 1
        self.save()
    
    def record_encounter(self, gate_number: int, system_card_name: str, dealer_card_name: str, 
                        won: bool, key_fragment: Optional[str] = None):
        """
        Record a complete encounter.
        
        Args:
            gate_number: Which gate was challenged
            system_card_name: Name of system's card
            dealer_card_name: Name of dealer's card
            won: Whether system won
            key_fragment: Key fragment if won
        """
        # Log the encounter
        encounter = EncounterLog(
            timestamp=datetime.now(),
            gate_number=gate_number,
            system_card=system_card_name,
            dealer_card=dealer_card_name,
            won=won,
            key_fragment=key_fragment,
        )
        self.log_encounter(encounter)
        
        # Update probability state
        self.probability_state.total_encounters += 1
        self.probability_state.last_appearance = datetime.now()
        self.probability_state.operations_since_appearance = 0
        
        if won:
            self.probability_state.total_wins += 1
            self.probability_state.heat += 1.0
            if self.probability_state.current_gate < 12:
                self.probability_state.current_gate += 1
        else:
            self.probability_state.heat = max(0, self.probability_state.heat - 0.1)
        
        # Update system truth
        self.system_truth.record_challenge(won, gate_number, key_fragment)
        
        # Save everything
        self.save()
