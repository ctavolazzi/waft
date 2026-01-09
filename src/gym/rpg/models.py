"""
RPG Framework Models - Game Objects for the Jungle Gym

Defines the core game objects using Pydantic for validation:
- Hero: The AI agent's character with stats, level, and XP
- Quest: A challenge with difficulty, description, and loot
- BattleLog: Records of combat attempts and results
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, validator


class Hero(BaseModel):
    """
    The Hero - Represents the AI agent's character.
    
    Tracks stats as success rates:
    - INT: Logic (success rate in logical transformations)
    - WIS: Safety (success rate in validation/safety checks)
    - CHA: Formatting (success rate in proper formatting)
    """
    name: str = Field(..., description="Hero's name")
    level: int = Field(default=1, ge=1, description="Current level")
    xp: int = Field(default=0, ge=0, description="Experience points")
    stats: Dict[str, float] = Field(
        default_factory=lambda: {"INT": 0.0, "WIS": 0.0, "CHA": 0.0},
        description="Success rates: INT (Logic), WIS (Safety), CHA (Formatting)"
    )
    
    @validator('stats')
    def validate_stats(cls, v):
        """Ensure stats dict has required keys and values are 0-1."""
        required_keys = {"INT", "WIS", "CHA"}
        if not all(key in v for key in required_keys):
            raise ValueError(f"Stats must contain {required_keys}")
        for key, value in v.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"Stat {key} must be between 0.0 and 1.0, got {value}")
        return v
    
    def add_xp(self, amount: int) -> Dict[str, Any]:
        """
        Add XP and check for level up.
        
        Returns:
            Dict with 'leveled_up' (bool) and 'new_level' (int) if leveled
        """
        old_level = self.level
        self.xp += amount
        
        # Level up calculation: XP needed = level * 100
        new_level = 1 + (self.xp // 100)
        leveled_up = new_level > old_level
        
        if leveled_up:
            self.level = new_level
        
        return {
            'leveled_up': leveled_up,
            'new_level': new_level if leveled_up else None
        }
    
    def update_stat(self, stat_name: str, success: bool, weight: float = 0.1):
        """
        Update a stat based on success/failure.
        
        Uses exponential moving average: new_value = old_value * (1 - weight) + (1.0 if success else 0.0) * weight
        
        Args:
            stat_name: "INT", "WIS", or "CHA"
            success: Whether the attempt succeeded
            weight: Learning rate (default 0.1)
        """
        if stat_name not in self.stats:
            raise ValueError(f"Invalid stat name: {stat_name}")
        
        current_value = self.stats[stat_name]
        success_value = 1.0 if success else 0.0
        self.stats[stat_name] = current_value * (1 - weight) + success_value * weight
    
    def get_total_stats(self) -> float:
        """Get average of all success rates."""
        return sum(self.stats.values()) / len(self.stats)


class Quest(BaseModel):
    """
    A Quest - A specific challenge for the Hero.
    
    Contains the prompt, difficulty, validation rules, and loot.
    """
    name: str = Field(..., description="Quest name")
    difficulty: int = Field(..., ge=1, le=10, description="Difficulty level (1-10)")
    description: str = Field(..., description="The raw prompt input")
    win_condition: str = Field(..., description="Validation rule (e.g., 'valid_json', 'logic_match')")
    loot_table: Dict[str, Any] = Field(
        default_factory=lambda: {"xp": 0},
        description="Loot/rewards (xp, items, etc.)"
    )
    
    @validator('difficulty')
    def validate_difficulty(cls, v):
        """Ensure difficulty is within range."""
        if not 1 <= v <= 10:
            raise ValueError(f"Difficulty must be between 1 and 10, got {v}")
        return v


class BattleLog(BaseModel):
    """
    Battle Log - Records a single attempt at a quest.
    
    Tracks Input, Output, Result, and Error.
    V2: Added Scint detection and stabilization support.
    """
    quest_name: str = Field(..., description="Name of the quest attempted")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the battle occurred")
    hero_name: str = Field(..., description="Hero who attempted the quest")
    input_prompt: str = Field(..., description="The quest description/prompt (Input)")
    agent_response: str = Field(..., description="The AI agent's response/output (Output)")
    result: str = Field(..., description="Result: 'critical_hit', 'hit', 'miss', or 'stabilized'")
    success: bool = Field(..., description="Whether the quest was completed successfully")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    xp_gained: int = Field(default=0, ge=0, description="XP gained from this battle")
    
    # --- V2: Scint & Stabilization Support ---
    version: int = Field(default=2, description="Schema version")
    
    # What broke?
    scints_detected: Optional[List[str]] = Field(
        default=None, 
        description="List of Scint types detected (e.g. 'SYNTAX_TEAR')"
    )
    max_severity: Optional[float] = Field(
        default=None, 
        description="The severity of the worst fracture (0.0-1.0)"
    )
    
    # Did we fix it?
    stabilization_attempted: bool = Field(default=False)
    stabilization_successful: bool = Field(default=False)
    stabilization_attempts: int = Field(default=0)
    corrected_response: Optional[str] = Field(
        default=None, 
        description="The valid output after stabilization"
    )
    
    # Cost tracking
    agent_call_count: int = Field(
        default=1, 
        description="How many times we called the LLM (1 = normal, >1 = stabilized)"
    )
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
