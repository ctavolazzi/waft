"""Command to D&D ability mapping configuration.

Maps Waft CLI commands to their corresponding D&D ability scores
for the gamification system.
"""

from dataclasses import dataclass
from typing import List, Literal

AbilityType = Literal["STR", "DEX", "CON", "INT", "WIS", "CHA"]


@dataclass(frozen=True)
class CommandAbility:
    """Mapping of a command to its ability score."""

    command: str
    ability: AbilityType
    dc: int = 10  # Difficulty class (default 10)

    def __post_init__(self):
        """Validate ability is one of the six D&D abilities."""
        valid_abilities = {"STR", "DEX", "CON", "INT", "WIS", "CHA"}
        if self.ability not in valid_abilities:
            raise ValueError(
                f"Invalid ability: {self.ability}. "
                f"Must be one of {valid_abilities}"
            )


# Command → Ability mapping
# This determines which ability score is tested when executing a command
COMMAND_ABILITIES: List[CommandAbility] = [
    # Project management (Charisma - leadership, creativity)
    CommandAbility("new", "CHA"),
    CommandAbility("add", "CHA"),
    CommandAbility("goal_create", "CHA"),

    # System verification (Constitution - endurance, reliability)
    CommandAbility("verify", "CON"),

    # Knowledge & analysis (Intelligence - logic, analysis)
    CommandAbility("sync", "INT"),
    CommandAbility("finding_log", "INT"),
    CommandAbility("analyze", "INT"),

    # Decision making (Wisdom - judgment, insight)
    CommandAbility("init", "WIS"),
    CommandAbility("info", "WIS"),
    CommandAbility("assess", "WIS"),
    CommandAbility("check", "WIS"),
    CommandAbility("decide", "WIS"),

    # Quick actions (Dexterity - speed, precision)
    CommandAbility("serve", "DEX"),
    CommandAbility("dashboard", "DEX"),
]


def get_command_ability(command: str) -> AbilityType:
    """Get the ability score for a command.

    Args:
        command: The command name (e.g., "new", "verify")

    Returns:
        The ability type (STR, DEX, CON, INT, WIS, or CHA)
        Defaults to WIS if command not found.

    Example:
        >>> get_command_ability("new")
        'CHA'
        >>> get_command_ability("verify")
        'CON'
        >>> get_command_ability("unknown")
        'WIS'
    """
    for ca in COMMAND_ABILITIES:
        if ca.command == command:
            return ca.ability
    return "WIS"  # Default to Wisdom


def get_command_dc(command: str) -> int:
    """Get the difficulty class for a command.

    Args:
        command: The command name

    Returns:
        The DC value (default 10)
    """
    for ca in COMMAND_ABILITIES:
        if ca.command == command:
            return ca.dc
    return 10  # Default DC
