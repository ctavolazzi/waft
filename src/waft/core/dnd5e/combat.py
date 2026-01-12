"""
D&D 5e Combat Mechanics

Combat interaction mechanics: attack rolls, saving throws, damage application.
"""

from typing import TYPE_CHECKING

from .dice import DnDRoller

if TYPE_CHECKING:
    from .character import DnD5eCharacter


class DnD5eCombat:
    """
    D&D 5e combat mechanics.
    
    Handles attack rolls, saving throws, and damage application.
    """
    
    @staticmethod
    def make_attack_roll(
        attack_modifier: int,
        target_ac: int,
        advantage: bool = False,
        disadvantage: bool = False
    ) -> tuple[bool, bool]:
        """
        Make attack roll against target AC.
        
        Formula: d20 + attack_modifier >= target_ac
        
        Critical hits (natural 20) always hit, regardless of AC.
        
        Args:
            attack_modifier: Total attack modifier (ability + proficiency + other)
            target_ac: Target's Armor Class
            advantage: Roll with advantage
            disadvantage: Roll with disadvantage
        
        Returns:
            Tuple of (hit, critical)
            - hit: True if attack hits (total >= AC or critical)
            - critical: True if natural 20 (critical hit)
        """
        roll, is_critical = DnDRoller.attack_roll(advantage, disadvantage)
        total = roll + attack_modifier
        
        # Critical hits always hit
        hit = total >= target_ac or is_critical
        
        return (hit, is_critical)
    
    @staticmethod
    def make_saving_throw(
        ability_modifier: int,
        proficiency_bonus: int,
        is_proficient: bool,
        dc: int
    ) -> bool:
        """
        Make saving throw against DC.
        
        Formula: d20 + ability_modifier + proficiency_bonus (if proficient) >= DC
        
        Args:
            ability_modifier: Ability modifier (STR, DEX, CON, etc.)
            proficiency_bonus: Proficiency bonus
            is_proficient: Whether character is proficient in this save
            dc: Difficulty Class (DC) to beat
        
        Returns:
            True if saving throw succeeds, False otherwise
        """
        roll = DnDRoller.roll("1d20")
        modifier = ability_modifier
        
        if is_proficient:
            modifier += proficiency_bonus
        
        total = roll + modifier
        return total >= dc
    
    @staticmethod
    def apply_damage(character: "DnD5eCharacter", damage: int) -> tuple[int, bool]:
        """
        Apply damage to character.
        
        Reduces HP by damage amount. HP cannot go below 0.
        
        Args:
            character: Character to damage
            damage: Amount of damage to apply
        
        Returns:
            Tuple of (new_hp, is_dead)
            - new_hp: HP after damage (0 or higher)
            - is_dead: True if character is dead (HP <= 0)
        """
        character.hp = max(0, character.hp - damage)
        is_dead = character.hp <= 0
        return (character.hp, is_dead)
    
    @staticmethod
    def apply_healing(character: "DnD5eCharacter", healing: int) -> int:
        """
        Apply healing to character.
        
        Increases HP by healing amount. HP cannot exceed max_hp.
        
        Args:
            character: Character to heal
            healing: Amount of healing to apply
        
        Returns:
            New HP value (capped at max_hp)
        """
        character.hp = min(character.max_hp, character.hp + healing)
        return character.hp
