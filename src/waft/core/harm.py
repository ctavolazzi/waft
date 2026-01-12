"""
Harm and Help System: Tracking intentional/unintentional harm and help with Arrow of Intent.

Harm and Help are subjective - what one being intends as harm might be felt as pleasure
by another, and vice versa. This system tracks both the source intent and the target's
interpretation, enabling beings to learn through experience and karma.
"""

from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from dataclasses import dataclass, field
import math
import json


@dataclass
class ArrowOfIntent:
    """
    Arrow of Intent: A 3D vector representing a being's intended direction/goal.
    
    The Arrow represents where the being's actions and decisions are directed.
    Alignment is calculated as cosine similarity between two Arrows:
    - Parallel arrows (same direction) = 1.0 (perfect alignment)
    - Perpendicular arrows = 0.0 (no alignment)
    - Opposite arrows = -1.0 (complete misalignment)
    """
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def magnitude(self) -> float:
        """Calculate the magnitude (length) of the arrow."""
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    def normalize(self) -> "ArrowOfIntent":
        """Return a normalized version of the arrow (unit vector)."""
        mag = self.magnitude()
        if mag == 0.0:
            return ArrowOfIntent(0.0, 0.0, 0.0)
        return ArrowOfIntent(
            self.x / mag,
            self.y / mag,
            self.z / mag
        )
    
    def cosine_similarity(self, other: "ArrowOfIntent") -> float:
        """
        Calculate cosine similarity between this arrow and another.
        
        Returns:
            -1.0 to 1.0: -1.0 = opposite, 0.0 = perpendicular, 1.0 = parallel
        """
        # Dot product
        dot_product = self.x * other.x + self.y * other.y + self.z * other.z
        
        # Magnitudes
        mag_self = self.magnitude()
        mag_other = other.magnitude()
        
        if mag_self == 0.0 or mag_other == 0.0:
            return 0.0
        
        # Cosine similarity
        similarity = dot_product / (mag_self * mag_other)
        
        # Clamp to [-1.0, 1.0] to handle floating point errors
        return max(-1.0, min(1.0, similarity))
    
    def to_dict(self) -> Dict[str, float]:
        """Convert arrow to dictionary."""
        return {"x": self.x, "y": self.y, "z": self.z}
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "ArrowOfIntent":
        """Create arrow from dictionary."""
        return cls(
            x=data.get("x", 0.0),
            y=data.get("y", 0.0),
            z=data.get("z", 0.0)
        )


@dataclass
class Harm:
    """
    Harm: Tracks harm caused by one being to another or to the system.
    
    Harm is subjective - the same action might be interpreted differently
    by the target being. This class tracks the source intent, but the
    actual pain felt depends on the target's interpretation.
    """
    severity: float  # 0.0-1.0, how severe the harm is
    intentional: bool  # Whether the harm was intentional
    source_being_id: str  # Who caused the harm
    target_being_id: Optional[str]  # Who was harmed (None = system/environment)
    arrow_of_intent: ArrowOfIntent  # Source being's intent direction
    harm_type: str  # physical, emotional, informational, systemic
    resolved: bool = False  # Whether the harm has been resolved
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    harm_id: str = field(default_factory=lambda: f"harm_{datetime.now().timestamp()}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert harm to dictionary."""
        return {
            "harm_id": self.harm_id,
            "severity": self.severity,
            "intentional": self.intentional,
            "source_being_id": self.source_being_id,
            "target_being_id": self.target_being_id,
            "arrow_of_intent": self.arrow_of_intent.to_dict(),
            "harm_type": self.harm_type,
            "resolved": self.resolved,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Harm":
        """Create harm from dictionary."""
        return cls(
            severity=data["severity"],
            intentional=data["intentional"],
            source_being_id=data["source_being_id"],
            target_being_id=data.get("target_being_id"),
            arrow_of_intent=ArrowOfIntent.from_dict(data["arrow_of_intent"]),
            harm_type=data["harm_type"],
            resolved=data.get("resolved", False),
            created_at=data.get("created_at", datetime.now().isoformat()),
            harm_id=data.get("harm_id", f"harm_{datetime.now().timestamp()}")
        )


@dataclass
class Help:
    """
    Help: Tracks help/benefit provided by one being to another or to the system.
    
    Help is subjective - the same action might be interpreted differently
    by the target being. This class tracks the source intent, but the
    actual pleasure felt depends on the target's interpretation.
    """
    benefit: float  # 0.0-1.0, how beneficial the help is
    intentional: bool  # Whether the help was intentional
    source_being_id: str  # Who provided the help
    target_being_id: Optional[str]  # Who was helped (None = system/environment)
    arrow_of_intent: ArrowOfIntent  # Source being's intent direction
    help_type: str  # physical, emotional, informational, systemic
    acknowledged: bool = False  # Whether the help has been acknowledged
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    help_id: str = field(default_factory=lambda: f"help_{datetime.now().timestamp()}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert help to dictionary."""
        return {
            "help_id": self.help_id,
            "benefit": self.benefit,
            "intentional": self.intentional,
            "source_being_id": self.source_being_id,
            "target_being_id": self.target_being_id,
            "arrow_of_intent": self.arrow_of_intent.to_dict(),
            "help_type": self.help_type,
            "acknowledged": self.acknowledged,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Help":
        """Create help from dictionary."""
        return cls(
            benefit=data["benefit"],
            intentional=data["intentional"],
            source_being_id=data["source_being_id"],
            target_being_id=data.get("target_being_id"),
            arrow_of_intent=ArrowOfIntent.from_dict(data["arrow_of_intent"]),
            help_type=data["help_type"],
            acknowledged=data.get("acknowledged", False),
            created_at=data.get("created_at", datetime.now().isoformat()),
            help_id=data.get("help_id", f"help_{datetime.now().timestamp()}")
        )
