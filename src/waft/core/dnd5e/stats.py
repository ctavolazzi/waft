"""
D&D 5e Stat Calculations - The Immutable Physics Engine

Core mathematical algorithms for D&D 5e mechanics. These are the "laws of physics"
that govern how ability scores, modifiers, AC, and proficiency work.
"""

from enum import Enum
from typing import Literal


class ArmorType(str, Enum):
    """Armor type enumeration."""
    NONE = "none"
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"


class DnD5eStats:
    """
    D&D 5e stat calculations - the immutable physics engine.
    
    All calculations follow official D&D 5e rules. These are pure functions
    with no side effects - they calculate derived values from base stats.
    """
    
    # Valid ranges for ability scores and levels
    MIN_ABILITY_SCORE = 1
    MAX_ABILITY_SCORE = 30
    MIN_LEVEL = 1
    MAX_LEVEL = 20
    
    @staticmethod
    def ability_modifier(score: int) -> int:
        """
        Calculate ability modifier from ability score.
        
        Formula: (score - 10) // 2
        
        Examples:
            - 10 → +0
            - 12 → +1
            - 14 → +2
            - 16 → +3
            - 18 → +4
            - 20 → +5
        
        Args:
            score: Ability score (1-30)
        
        Returns:
            Ability modifier (integer)
        
        Raises:
            ValueError: If score is outside valid range (1-30)
        """
        if not (DnD5eStats.MIN_ABILITY_SCORE <= score <= DnD5eStats.MAX_ABILITY_SCORE):
            raise ValueError(
                f"Ability score must be between {DnD5eStats.MIN_ABILITY_SCORE} and "
                f"{DnD5eStats.MAX_ABILITY_SCORE}, got {score}"
            )
        
        return (score - 10) // 2
    
    @staticmethod
    def proficiency_bonus(level: int) -> int:
        """
        Calculate proficiency bonus based on character level.
        
        Formula: 2 + ((level - 1) // 4)
        
        This creates a step function:
            - Levels 1-4: +2
            - Levels 5-8: +3
            - Levels 9-12: +4
            - Levels 13-16: +5
            - Levels 17-20: +6
        
        Args:
            level: Character level (1-20)
        
        Returns:
            Proficiency bonus (integer)
        
        Raises:
            ValueError: If level is outside valid range (1-20)
        """
        if not (DnD5eStats.MIN_LEVEL <= level <= DnD5eStats.MAX_LEVEL):
            raise ValueError(
                f"Level must be between {DnD5eStats.MIN_LEVEL} and {DnD5eStats.MAX_LEVEL}, "
                f"got {level}"
            )
        
        return 2 + ((level - 1) // 4)
    
    @staticmethod
    def calculate_ac(
        dex_modifier: int,
        armor_type: ArmorType | str = ArmorType.NONE,
        armor_base: int = 0
    ) -> int:
        """
        Calculate Armor Class (AC).
        
        Base formula: 10 + DEX modifier (unarmored)
        
        With armor:
            - Light armor: armor_base + DEX modifier
            - Medium armor: armor_base + min(DEX modifier, 2)
            - Heavy armor: armor_base (no DEX modifier)
        
        Args:
            dex_modifier: Dexterity modifier
            armor_type: Type of armor (none, light, medium, heavy)
            armor_base: Base AC from armor (default: 0)
        
        Returns:
            Armor Class (integer)
        
        Raises:
            ValueError: If armor_type is invalid
        """
        # Normalize armor_type to enum
        if isinstance(armor_type, str):
            try:
                armor_type = ArmorType(armor_type.lower())
            except ValueError:
                raise ValueError(
                    f"Invalid armor type: {armor_type}. Must be one of: "
                    f"{[e.value for e in ArmorType]}"
                )
        
        if armor_type == ArmorType.NONE:
            return 10 + dex_modifier
        elif armor_type == ArmorType.LIGHT:
            return armor_base + dex_modifier
        elif armor_type == ArmorType.MEDIUM:
            return armor_base + min(dex_modifier, 2)
        elif armor_type == ArmorType.HEAVY:
            return armor_base
        else:
            raise ValueError(f"Unhandled armor type: {armor_type}")
    
    @staticmethod
    def spell_save_dc(spellcasting_modifier: int, proficiency_bonus: int) -> int:
        """
        Calculate spell save DC.
        
        Formula: 8 + spellcasting_modifier + proficiency_bonus
        
        Args:
            spellcasting_modifier: Spellcasting ability modifier (INT, WIS, or CHA)
            proficiency_bonus: Proficiency bonus
        
        Returns:
            Spell save DC (integer)
        """
        return 8 + spellcasting_modifier + proficiency_bonus
