"""
D&D 5e Character State - The "Biology" of WAFT Beings

Character dataclass following the pattern from Deep Code Analysis:
- Store BASE stats (scores), not derived values (modifiers)
- Store MAX values separately from current (hp vs max_hp)
- Calculate modifiers at runtime via @property decorators
- Equipment slots (weapon, armor)
- Status effects list
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .stats import DnD5eStats, ArmorType
from .dice import DnDRoller


@dataclass
class DnD5eCharacter:
    """
    D&D 5e character state - the 'soul' of the agent.
    
    Key Design Principles:
    1. Store BASE stats (scores), not modifiers - prevents desync
    2. Store MAX values separately from current (hp vs max_hp)
    3. Calculate modifiers at runtime via @property decorators
    4. Equipment slots (weapon, armor) as optional strings
    5. Status effects as list (extensible)
    """
    
    # Core identity
    name: str
    level: int = 1
    char_class: str = "fighter"
    hit_die: int = 10
    
    # Ability scores (BASE - stored, not calculated)
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10
    
    # Hit points (separate current and max)
    hp: int = 20
    max_hp: int = 20
    
    # Equipment (slot-based)
    equipped_weapon: Optional[str] = None
    equipped_armor: Optional[str] = None
    armor_type: ArmorType | str = ArmorType.NONE
    armor_base: int = 0
    
    # Proficiencies
    proficient_saves: List[str] = field(default_factory=list)
    proficient_skills: List[str] = field(default_factory=list)
    
    # Status effects
    status_effects: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate character data after initialization."""
        # Validate ability scores
        for attr_name in ["strength", "dexterity", "constitution", 
                         "intelligence", "wisdom", "charisma"]:
            score = getattr(self, attr_name)
            if not (DnD5eStats.MIN_ABILITY_SCORE <= score <= DnD5eStats.MAX_ABILITY_SCORE):
                raise ValueError(
                    f"{attr_name} must be between {DnD5eStats.MIN_ABILITY_SCORE} and "
                    f"{DnD5eStats.MAX_ABILITY_SCORE}, got {score}"
                )
        
        # Validate level
        if not (DnD5eStats.MIN_LEVEL <= self.level <= DnD5eStats.MAX_LEVEL):
            raise ValueError(
                f"Level must be between {DnD5eStats.MIN_LEVEL} and {DnD5eStats.MAX_LEVEL}, "
                f"got {self.level}"
            )
        
        # Validate HP
        if self.hp < 0:
            raise ValueError(f"HP cannot be negative, got {self.hp}")
        if self.max_hp < 1:
            raise ValueError(f"Max HP must be at least 1, got {self.max_hp}")
        if self.hp > self.max_hp:
            raise ValueError(f"HP ({self.hp}) cannot exceed max_hp ({self.max_hp})")
        
        # Normalize armor_type to enum
        if isinstance(self.armor_type, str):
            try:
                self.armor_type = ArmorType(self.armor_type.lower())
            except ValueError:
                raise ValueError(
                    f"Invalid armor type: {self.armor_type}. Must be one of: "
                    f"{[e.value for e in ArmorType]}"
                )
    
    # Properties (DERIVED - calculated at runtime)
    
    @property
    def str_modifier(self) -> int:
        """Calculate STR modifier."""
        return DnD5eStats.ability_modifier(self.strength)
    
    @property
    def dex_modifier(self) -> int:
        """Calculate DEX modifier."""
        return DnD5eStats.ability_modifier(self.dexterity)
    
    @property
    def con_modifier(self) -> int:
        """Calculate CON modifier."""
        return DnD5eStats.ability_modifier(self.constitution)
    
    @property
    def int_modifier(self) -> int:
        """Calculate INT modifier."""
        return DnD5eStats.ability_modifier(self.intelligence)
    
    @property
    def wis_modifier(self) -> int:
        """Calculate WIS modifier."""
        return DnD5eStats.ability_modifier(self.wisdom)
    
    @property
    def cha_modifier(self) -> int:
        """Calculate CHA modifier."""
        return DnD5eStats.ability_modifier(self.charisma)
    
    @property
    def ac(self) -> int:
        """Calculate current AC."""
        return DnD5eStats.calculate_ac(
            self.dex_modifier,
            self.armor_type,
            self.armor_base
        )
    
    @property
    def proficiency_bonus(self) -> int:
        """Get proficiency bonus for current level."""
        return DnD5eStats.proficiency_bonus(self.level)
    
    @property
    def hp_percent(self) -> float:
        """Calculate HP as percentage of max."""
        if self.max_hp <= 0:
            return 0.0
        return self.hp / self.max_hp
    
    def make_attack_roll(self, advantage: bool = False, disadvantage: bool = False) -> tuple[int, bool, bool]:
        """
        Make attack roll.
        
        Returns (total, hit, critical).
        Note: 'hit' requires target AC, which is not available here.
        This method returns the roll total and critical flag.
        
        Args:
            advantage: Roll with advantage
            disadvantage: Roll with disadvantage
        
        Returns:
            Tuple of (total, hit, critical)
            - total: Roll total (d20 + STR modifier + proficiency)
            - hit: Always False (requires target AC to determine)
            - critical: True if natural 20
        """
        roll, is_critical = DnDRoller.attack_roll(advantage, disadvantage)
        str_mod = self.str_modifier
        prof = self.proficiency_bonus
        total = roll + str_mod + prof
        # Note: hit determination requires target AC, which is not available here
        return (total, False, is_critical)
    
    def to_dict(self) -> Dict:
        """Convert character to dictionary for serialization."""
        return {
            "name": self.name,
            "level": self.level,
            "char_class": self.char_class,
            "hit_die": self.hit_die,
            "ability_scores": {
                "strength": self.strength,
                "dexterity": self.dexterity,
                "constitution": self.constitution,
                "intelligence": self.intelligence,
                "wisdom": self.wisdom,
                "charisma": self.charisma,
            },
            "hp": self.hp,
            "max_hp": self.max_hp,
            "equipment": {
                "weapon": self.equipped_weapon,
                "armor": self.equipped_armor,
                "armor_type": self.armor_type.value if isinstance(self.armor_type, ArmorType) else self.armor_type,
                "armor_base": self.armor_base,
            },
            "proficiencies": {
                "saves": self.proficient_saves,
                "skills": self.proficient_skills,
            },
            "status_effects": self.status_effects,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "DnD5eCharacter":
        """Create character from dictionary."""
        return cls(
            name=data["name"],
            level=data.get("level", 1),
            char_class=data.get("char_class", "fighter"),
            hit_die=data.get("hit_die", 10),
            strength=data["ability_scores"]["strength"],
            dexterity=data["ability_scores"]["dexterity"],
            constitution=data["ability_scores"]["constitution"],
            intelligence=data["ability_scores"]["intelligence"],
            wisdom=data["ability_scores"]["wisdom"],
            charisma=data["ability_scores"]["charisma"],
            hp=data.get("hp", 20),
            max_hp=data.get("max_hp", 20),
            equipped_weapon=data.get("equipment", {}).get("weapon"),
            equipped_armor=data.get("equipment", {}).get("armor"),
            armor_type=data.get("equipment", {}).get("armor_type", "none"),
            armor_base=data.get("equipment", {}).get("armor_base", 0),
            proficient_saves=data.get("proficiencies", {}).get("saves", []),
            proficient_skills=data.get("proficiencies", {}).get("skills", []),
            status_effects=data.get("status_effects", []),
        )
