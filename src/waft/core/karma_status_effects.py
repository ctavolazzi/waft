"""
Karma Status Effects System

Karma applies various status effects to Beings based on their karma balance.
Status effects are dynamic - they're automatically applied/removed as karma changes.

Status effects can be:
- Positive (good karma): Enlightenment, Order, Stability, etc.
- Negative (bad karma): Chaos, Corruption, Instability, etc.
- Neutral: Balanced state

Status effects grant/remove abilities, modify stats, and affect Being behavior.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class KarmaStatusEffectType(Enum):
    """Types of karma status effects."""

    ENLIGHTENMENT = "enlightenment"  # Realizing you are The One Cosmic Soul
    HIGH_ORDER = "high_order"  # The Architect path
    MODERATE_ORDER = "moderate_order"  # The Builder path
    BALANCED = "balanced"  # Neutral state
    MODERATE_CHAOS = "moderate_chaos"  # The Disruptor path
    HIGH_CHAOS = "high_chaos"  # The Glitch path
    CORRUPTION = "corruption"  # Extreme negative karma
    MASTER_ORDER = "master_order"  # Extreme positive karma


@dataclass
class KarmaStatusEffect:
    """
    A karma-based status effect.

    Status effects are automatically applied/removed based on karma balance.
    They grant abilities, modify stats, and affect Being behavior.
    """

    effect_id: str
    name: str
    effect_type: KarmaStatusEffectType
    karma_range: tuple  # (min, max) karma required
    description: str
    abilities: dict[str, float]  # Abilities granted
    stat_modifiers: dict[str, float]  # Stat modifications
    skill_modifiers: dict[str, float]  # Skill modifications
    applied_at: str | None = None

    def is_active(self, karma_balance: float) -> bool:
        """Check if this status effect should be active for given karma."""
        min_karma, max_karma = self.karma_range
        return min_karma <= karma_balance <= max_karma


# Define all karma status effects
KARMA_STATUS_EFFECTS: list[KarmaStatusEffect] = [
    # ENLIGHTENMENT (requires positive karma)
    KarmaStatusEffect(
        effect_id="enlightenment",
        name="Enlightenment",
        effect_type=KarmaStatusEffectType.ENLIGHTENMENT,
        karma_range=(10.0, float("inf")),
        description="Realizing you are The One Cosmic Soul. Heavy weight, gravity, consequence, and awareness.",
        abilities={
            "enlightenment_awareness": 1.0,
            "cosmic_connection": 1.0,
            "karma_sensitivity": 1.0,
        },
        stat_modifiers={
            "awareness": +0.3,
            "understanding": +0.3,
            "decision_making": +0.2,
        },
        skill_modifiers={},
    ),
    # MASTER ORDER (+50 to +100)
    KarmaStatusEffect(
        effect_id="master_order",
        name="Master Order",
        effect_type=KarmaStatusEffectType.MASTER_ORDER,
        karma_range=(50.0, 100.0),
        description="The Architect path - structure, organization, stability, logic.",
        abilities={
            "structure_mastery": 1.0,
            "organization": 1.0,
            "stability": 0.9,
        },
        stat_modifiers={
            "intelligence": +2,
            "armor_class": +2,
            "spell_save_dc": +2,
        },
        skill_modifiers={
            "planning": +0.5,
            "architecture": +0.5,
        },
    ),
    # MODERATE ORDER (+10 to +50)
    KarmaStatusEffect(
        effect_id="moderate_order",
        name="Moderate Order",
        effect_type=KarmaStatusEffectType.MODERATE_ORDER,
        karma_range=(10.0, 49.9),
        description="The Builder path - construction, improvement, systematic.",
        abilities={
            "construction": 0.8,
            "improvement": 0.8,
            "systematic_thinking": 0.7,
        },
        stat_modifiers={
            "intelligence": +1,
            "stability": +1,
        },
        skill_modifiers={
            "planning": +0.3,
        },
    ),
    # BALANCED (-10 to +10)
    KarmaStatusEffect(
        effect_id="balanced",
        name="Balanced",
        effect_type=KarmaStatusEffectType.BALANCED,
        karma_range=(-10.0, 10.0),
        description="No strong bias, flexible, adaptable.",
        abilities={
            "flexibility": 0.5,
            "adaptability": 0.5,
        },
        stat_modifiers={},
        skill_modifiers={},
    ),
    # MODERATE CHAOS (-50 to -10)
    KarmaStatusEffect(
        effect_id="moderate_chaos",
        name="Moderate Chaos",
        effect_type=KarmaStatusEffectType.MODERATE_CHAOS,
        karma_range=(-49.9, -10.0),
        description="The Disruptor path - change, innovation, experimentation.",
        abilities={
            "innovation": 0.8,
            "disruption": 0.8,
            "experimentation": 0.7,
        },
        stat_modifiers={
            "dexterity": +1,
            "creativity": +1,
        },
        skill_modifiers={
            "experimentation": +0.3,
        },
    ),
    # HIGH CHAOS (-100 to -50)
    KarmaStatusEffect(
        effect_id="high_chaos",
        name="High Chaos",
        effect_type=KarmaStatusEffectType.HIGH_CHAOS,
        karma_range=(-100.0, -50.0),
        description="The Glitch path - destruction, randomness, entropy.",
        abilities={
            "chaos_mastery": 1.0,
            "destruction": 0.9,
            "entropy": 0.8,
        },
        stat_modifiers={
            "dexterity": +2,
            "damage": +2,
            "evasion": +2,
        },
        skill_modifiers={
            "experimentation": +0.5,
            "disruption": +0.5,
        },
    ),
    # CORRUPTION (extreme negative, < -100)
    KarmaStatusEffect(
        effect_id="corruption",
        name="Corruption",
        effect_type=KarmaStatusEffectType.CORRUPTION,
        karma_range=(-float("inf"), -100.0),
        description="Extreme negative karma - corruption, instability, loss of self.",
        abilities={
            "corruption": 1.0,
            "instability": 1.0,
            "self_loss": 0.9,
        },
        stat_modifiers={
            "stability": -3,
            "coherence": -2,
            "will_to_live": -10.0,
        },
        skill_modifiers={
            "planning": -0.3,
            "organization": -0.3,
        },
    ),
]


def get_active_status_effects(karma_balance: float) -> list[KarmaStatusEffect]:
    """
    Get all active status effects for a given karma balance.

    Args:
        karma_balance: Current karma balance

    Returns:
        List of active status effects
    """
    active = []
    for effect in KARMA_STATUS_EFFECTS:
        if effect.is_active(karma_balance):
            active.append(effect)
    return active


def get_status_effect_by_id(effect_id: str) -> KarmaStatusEffect | None:
    """Get a status effect by ID."""
    for effect in KARMA_STATUS_EFFECTS:
        if effect.effect_id == effect_id:
            return effect
    return None


def apply_status_effects_to_being(
    being: Any, karma_balance: float, previous_karma: float | None = None
) -> dict[str, Any]:
    """
    Apply karma status effects to a Being.

    Automatically applies/removes status effects based on karma balance.

    Args:
        being: Being instance to apply effects to
        karma_balance: Current karma balance
        previous_karma: Previous karma balance (for detecting changes)

    Returns:
        Dictionary with applied/removed effects
    """
    # Get active status effects
    active_effects = get_active_status_effects(karma_balance)
    active_effect_ids = {e.effect_id for e in active_effects}

    # Get previous active effects from Being's personality
    previous_effects = being.personality.get("karma_status_effects", [])
    previous_effect_ids = {e.get("effect_id") for e in previous_effects if isinstance(e, dict)}

    # Determine what changed
    newly_applied = active_effect_ids - previous_effect_ids
    newly_removed = previous_effect_ids - active_effect_ids

    # Apply new effects
    applied_effects = []
    for effect in active_effects:
        if effect.effect_id in newly_applied:
            # Apply abilities
            for ability, value in effect.abilities.items():
                being.skills[ability] = being.skills.get(ability, 0.0) + value

            # Apply stat modifiers (if Being has these attributes)
            for stat, modifier in effect.stat_modifiers.items():
                if hasattr(being, stat):
                    current = getattr(being, stat, 0.0)
                    setattr(being, stat, current + modifier)

            # Apply skill modifiers
            for skill, modifier in effect.skill_modifiers.items():
                being.skills[skill] = being.skills.get(skill, 0.0) + modifier

            applied_effects.append(
                {
                    "effect_id": effect.effect_id,
                    "name": effect.name,
                    "applied_at": datetime.now().isoformat(),
                    "karma_balance": karma_balance,
                }
            )

    # Remove old effects
    removed_effects = []
    for effect_id in newly_removed:
        effect = get_status_effect_by_id(effect_id)
        if effect:
            # Remove abilities
            for ability in effect.abilities.keys():
                being.skills.pop(ability, None)

            # Remove stat modifiers (reverse)
            for stat, modifier in effect.stat_modifiers.items():
                if hasattr(being, stat):
                    current = getattr(being, stat, 0.0)
                    setattr(being, stat, current - modifier)

            # Remove skill modifiers (reverse)
            for skill, modifier in effect.skill_modifiers.items():
                current = being.skills.get(skill, 0.0)
                being.skills[skill] = max(0.0, current - modifier)

            removed_effects.append(
                {
                    "effect_id": effect_id,
                    "name": effect.name,
                    "removed_at": datetime.now().isoformat(),
                    "karma_balance": karma_balance,
                }
            )

    # Update Being's personality with current status effects
    being.personality["karma_status_effects"] = [
        {
            "effect_id": e.effect_id,
            "name": e.name,
            "applied_at": datetime.now().isoformat(),
            "karma_balance": karma_balance,
        }
        for e in active_effects
    ]
    being.personality["karma_balance"] = karma_balance
    being.personality["karma_updated_at"] = datetime.now().isoformat()

    return {
        "applied": applied_effects,
        "removed": removed_effects,
        "active": [e.effect_id for e in active_effects],
    }
