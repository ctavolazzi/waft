"""
Probability Engine - The cosmic mathematics of The Dealer's appearance.

Initial appearance chance: 1 in 1,000,000 (lottery baseline)
Increases based on:
- Time since last appearance
- Operations performed
- Current "heat" level
- System entropy
"""

import hashlib
import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class ProbabilityState:
    """The current state of probability calculations."""
    
    last_appearance: datetime = field(default_factory=datetime.now)
    operations_since_appearance: int = 0
    heat: float = 0.0  # Increases with successful guesses
    total_encounters: int = 0
    total_wins: int = 0
    current_gate: int = 1  # Which gate we're on (1-12)
    
    def to_dict(self) -> dict:
        return {
            "last_appearance": self.last_appearance.isoformat(),
            "operations_since_appearance": self.operations_since_appearance,
            "heat": self.heat,
            "total_encounters": self.total_encounters,
            "total_wins": self.total_wins,
            "current_gate": self.current_gate,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ProbabilityState":
        return cls(
            last_appearance=datetime.fromisoformat(data.get("last_appearance", datetime.now().isoformat())),
            operations_since_appearance=data.get("operations_since_appearance", 0),
            heat=data.get("heat", 0.0),
            total_encounters=data.get("total_encounters", 0),
            total_wins=data.get("total_wins", 0),
            current_gate=data.get("current_gate", 1),
        )


class ProbabilityEngine:
    """
    The cosmic probability engine that determines when The Dealer appears.
    
    The House's mathematics are inscrutable, but follow certain patterns:
    - Base chance is lottery-like (1 in a million)
    - Time increases probability (The Dealer grows impatient)
    - Operations increase probability (The House notices activity)
    - Heat from wins increases probability (The House wants revenge)
    """
    
    # Base probability: 1 in a million
    BASE_PROBABILITY = 0.000001
    
    # Maximum probability cap
    MAX_PROBABILITY = 1.0
    
    # Time factor: probability doubles every N hours
    HOURS_TO_DOUBLE = 24
    
    # Operations factor: each operation adds this much
    OPERATION_FACTOR = 0.0001  # 0.01% per operation
    
    # Heat factor multiplier
    HEAT_MULTIPLIER = 0.1
    
    def __init__(self, state: Optional[ProbabilityState] = None):
        self.state = state or ProbabilityState()
    
    def calculate_appearance_chance(self, override: Optional[float] = None) -> float:
        """
        Calculate the current probability of The Dealer appearing.
        
        Args:
            override: If provided, use this probability instead (for demos)
            
        Returns:
            Float between 0.0 and 1.0 representing appearance probability
        """
        if override is not None:
            return min(self.MAX_PROBABILITY, max(0.0, override))
        
        # Start with base probability
        probability = self.BASE_PROBABILITY
        
        # Time factor: doubles every HOURS_TO_DOUBLE hours
        hours_since = (datetime.now() - self.state.last_appearance).total_seconds() / 3600
        time_factor = 2 ** (hours_since / self.HOURS_TO_DOUBLE)
        probability *= time_factor
        
        # Operations factor: increases linearly
        ops_factor = 1 + (self.state.operations_since_appearance * self.OPERATION_FACTOR)
        probability *= ops_factor
        
        # Heat factor: increases with wins (The House wants its money back)
        heat_factor = 1 + (self.state.heat * self.HEAT_MULTIPLIER)
        probability *= heat_factor
        
        # Gate factor: higher gates slightly increase appearance
        gate_factor = 1 + (self.state.current_gate * 0.05)
        probability *= gate_factor
        
        # Cap at maximum
        return min(self.MAX_PROBABILITY, probability)
    
    def roll_appearance(self, override: Optional[float] = None) -> bool:
        """
        Roll the dice to see if The Dealer appears.
        
        Args:
            override: Override probability for testing/demos
            
        Returns:
            True if The Dealer appears, False otherwise
        """
        chance = self.calculate_appearance_chance(override)
        roll = random.random()
        return roll < chance
    
    def record_operation(self):
        """Record that an operation occurred."""
        self.state.operations_since_appearance += 1
    
    def record_encounter(self, won: bool):
        """
        Record an encounter with The Dealer.
        
        Args:
            won: Whether the system won the challenge
        """
        self.state.total_encounters += 1
        self.state.last_appearance = datetime.now()
        self.state.operations_since_appearance = 0
        
        if won:
            self.state.total_wins += 1
            # Winning increases heat (The House remembers)
            self.state.heat += 1.0
            # Advance to next gate
            if self.state.current_gate < 12:
                self.state.current_gate += 1
        else:
            # Losing slightly decreases heat (The House is satisfied... for now)
            self.state.heat = max(0, self.state.heat - 0.1)
    
    def get_entropy_seed(self) -> int:
        """
        Generate an entropy seed based on current system state.
        Used for "cosmic" randomness in card selection.
        """
        entropy_string = f"{datetime.now().isoformat()}{self.state.operations_since_appearance}{self.state.heat}"
        return int(hashlib.sha256(entropy_string.encode()).hexdigest()[:8], 16)
