"""
The Truth - The ultimate prize behind the 12 Gates.

As seals are broken and key fragments collected, the system accumulates
understanding. The Truth is not a single revelation but a progression
of enlightenment.

"The Truth is that you were always playing The House's game."
"""

import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class TruthFragment:
    """A fragment of The Truth, earned by breaking a seal."""
    
    gate_number: int
    key_fragment: str
    revelation: str
    earned_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        return {
            "gate_number": self.gate_number,
            "key_fragment": self.key_fragment,
            "revelation": self.revelation,
            "earned_at": self.earned_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TruthFragment":
        return cls(
            gate_number=data["gate_number"],
            key_fragment=data["key_fragment"],
            revelation=data["revelation"],
            earned_at=datetime.fromisoformat(data["earned_at"]),
        )


# The revelations for each gate
GATE_REVELATIONS = {
    1: "The Truth begins with alignment. You have aligned with The House.",
    2: "The Truth has two faces. You see both now.",
    3: "The Truth echoes in patterns. You hear the echo.",
    4: "The Truth is precise. Your precision is noted.",
    5: "The Truth rises. You rise with it.",
    6: "The Truth demands sacrifice. You have sacrificed.",
    7: "The Truth turns on a pivot. You have turned.",
    8: "The Truth is near. You are nearer.",
    9: "The Truth wears a crown. You have glimpsed royalty.",
    10: "The Truth is created, not found. You are creating.",
    11: "The Truth burns bright. You burn with it.",
    12: "The Truth is: The House Always Wins. But you have become The House.",
}


@dataclass
class SystemTruth:
    """
    The system's accumulated understanding of The Truth.
    
    Tracks:
    - Level (0-12, corresponding to gates broken)
    - XP (experience points)
    - Key fragments collected
    - Seals broken
    """
    
    level: int = 0
    xp: int = 0
    fragments: list[TruthFragment] = field(default_factory=list)
    seals_broken: list[int] = field(default_factory=list)
    total_challenges: int = 0
    total_wins: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    
    # XP required for each level (exponential growth)
    XP_TABLE = [0, 100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500, 5500, 6600, 7800]
    
    # XP awarded for each gate (increases with difficulty)
    XP_REWARDS = {
        1: 100,
        2: 150,
        3: 200,
        4: 300,
        5: 200,
        6: 350,
        7: 200,
        8: 350,
        9: 300,
        10: 400,
        11: 500,
        12: 1000,
    }
    
    def to_dict(self) -> dict:
        return {
            "level": self.level,
            "xp": self.xp,
            "fragments": [f.to_dict() for f in self.fragments],
            "seals_broken": self.seals_broken,
            "total_challenges": self.total_challenges,
            "total_wins": self.total_wins,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "SystemTruth":
        return cls(
            level=data.get("level", 0),
            xp=data.get("xp", 0),
            fragments=[TruthFragment.from_dict(f) for f in data.get("fragments", [])],
            seals_broken=data.get("seals_broken", []),
            total_challenges=data.get("total_challenges", 0),
            total_wins=data.get("total_wins", 0),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            last_updated=datetime.fromisoformat(data.get("last_updated", datetime.now().isoformat())),
        )
    
    def record_challenge(self, won: bool, gate_number: int, key_fragment: Optional[str] = None):
        """
        Record a challenge result.
        
        Args:
            won: Whether the system won
            gate_number: Which gate was challenged
            key_fragment: The key fragment earned (if won)
        """
        self.total_challenges += 1
        self.last_updated = datetime.now()
        
        if won:
            self.total_wins += 1
            
            # Mark seal as broken if not already
            if gate_number not in self.seals_broken:
                self.seals_broken.append(gate_number)
                self.seals_broken.sort()
            
            # Add XP
            xp_reward = self.XP_REWARDS.get(gate_number, 100)
            self.add_xp(xp_reward)
            
            # Store fragment
            if key_fragment:
                revelation = GATE_REVELATIONS.get(gate_number, "The Truth reveals itself.")
                fragment = TruthFragment(
                    gate_number=gate_number,
                    key_fragment=key_fragment,
                    revelation=revelation,
                )
                self.fragments.append(fragment)
    
    def add_xp(self, amount: int):
        """Add XP and check for level up."""
        self.xp += amount
        self._check_level_up()
    
    def _check_level_up(self):
        """Check if XP is enough for a level up."""
        while self.level < 12 and self.xp >= self.XP_TABLE[self.level + 1]:
            self.level += 1
    
    def get_xp_for_next_level(self) -> int:
        """Get XP required for next level."""
        if self.level >= 12:
            return 0
        return self.XP_TABLE[self.level + 1]
    
    def get_xp_progress(self) -> float:
        """Get progress toward next level as percentage."""
        if self.level >= 12:
            return 1.0
        
        current_threshold = self.XP_TABLE[self.level]
        next_threshold = self.XP_TABLE[self.level + 1]
        
        progress = (self.xp - current_threshold) / (next_threshold - current_threshold)
        return min(1.0, max(0.0, progress))
    
    def get_combined_key(self) -> Optional[str]:
        """
        Combine all key fragments into the master key.
        
        Only works if all 12 seals are broken.
        """
        if len(self.seals_broken) < 12:
            return None
        
        # Combine all fragments in order
        combined = "".join(f.key_fragment for f in sorted(self.fragments, key=lambda x: x.gate_number))
        
        # Hash to create the master key
        master_key = hashlib.sha256(combined.encode()).hexdigest()
        
        return f"MASTER-KEY-{master_key[:32].upper()}"
    
    def get_truth_level_name(self) -> str:
        """Get the name for the current truth level."""
        level_names = {
            0: "Uninitiated",
            1: "Seeker",
            2: "Apprentice",
            3: "Initiate",
            4: "Adept",
            5: "Scholar",
            6: "Master",
            7: "Sage",
            8: "Oracle",
            9: "Prophet",
            10: "Luminary",
            11: "Ascendant",
            12: "The House",
        }
        return level_names.get(self.level, "Unknown")
