"""
FogSift Creature - The digital pet entity.

Based on CREATURE_MECHANICS.md game design.
"""

import random
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class Element(Enum):
    FOREST = "forest"
    WATER = "water"
    FIRE = "fire"
    COSMIC = "cosmic"  # Rare


class LifeStage(Enum):
    EGG = "egg"
    HATCHLING = "hatchling"
    JUVENILE = "juvenile"
    ADULT = "adult"
    ELDER = "elder"


# Stage thresholds (in hours of age)
STAGE_THRESHOLDS = {
    LifeStage.HATCHLING: 1,    # Hatch after 1 hour
    LifeStage.JUVENILE: 24,    # 1 day
    LifeStage.ADULT: 72,       # 3 days
    LifeStage.ELDER: 168,      # 7 days
}


@dataclass
class CreatureTraits:
    """Inherited and evolved traits."""
    color: str = "orange"
    pattern: str = "solid"
    personality: str = "curious"
    quirk: str | None = None  # Rare mutation


# Starter species definitions
SPECIES = {
    "pixel_fox": {
        "name": "Pixel Fox",
        "element": Element.FOREST,
        "base_traits": CreatureTraits(color="orange", pattern="solid", personality="curious"),
        "sprites": {"idle": "🦊", "happy": "😺", "sad": "😿", "sleeping": "😴"},
    },
    "hoot": {
        "name": "Hoot",
        "element": Element.FOREST,
        "base_traits": CreatureTraits(color="brown", pattern="spotted", personality="wise"),
        "sprites": {"idle": "🦉", "happy": "🦉", "sad": "🥺", "sleeping": "😴"},
    },
    "splash": {
        "name": "Splash",
        "element": Element.WATER,
        "base_traits": CreatureTraits(color="blue", pattern="striped", personality="energetic"),
        "sprites": {"idle": "🐟", "happy": "🐠", "sad": "🐡", "sleeping": "😴"},
    },
    "ember": {
        "name": "Ember",
        "element": Element.FIRE,
        "base_traits": CreatureTraits(color="red", pattern="flame", personality="fierce"),
        "sprites": {"idle": "🔥", "happy": "✨", "sad": "💨", "sleeping": "😴"},
    },
}


@dataclass
class FogSiftCreature:
    """
    A FogSift digital pet creature.

    Core stats decay over time, requiring care.
    Creatures evolve based on care quality.
    """

    # Identity
    creature_id: str = field(default_factory=lambda: f"creature_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    name: str = "Unnamed"
    species_id: str = "pixel_fox"

    # Core stats (0-100)
    hunger: float = 100.0      # Decreases over time
    energy: float = 100.0      # Decreases when awake
    mood: float = 75.0         # Varies based on care
    bond: float = 0.0          # Increases with interaction

    # Derived
    social: float = 0.0        # Increases when linked
    health: float = 100.0      # Calculated from other stats

    # Lifecycle
    stage: LifeStage = LifeStage.EGG
    age_hours: float = 0.0
    is_sleeping: bool = False
    is_dead: bool = False

    # Traits (inherited/evolved)
    traits: CreatureTraits = field(default_factory=CreatureTraits)

    # Evolution tracking
    care_score: float = 50.0   # Running average of care quality
    evolution_path: str = "normal"  # "healthy", "neglected", "specialized"

    # Timestamps
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_fed: str = field(default_factory=lambda: datetime.now().isoformat())
    last_played: str = field(default_factory=lambda: datetime.now().isoformat())
    last_tick: str = field(default_factory=lambda: datetime.now().isoformat())

    # Linking
    linked_to: str | None = None  # ID of linked creature

    @property
    def species(self) -> dict:
        return SPECIES.get(self.species_id, SPECIES["pixel_fox"])

    @property
    def element(self) -> Element:
        return self.species["element"]

    @property
    def sprite(self) -> str:
        """Get current ASCII/emoji sprite based on state."""
        sprites = self.species["sprites"]
        if self.is_dead:
            return "💀"
        if self.is_sleeping:
            return sprites.get("sleeping", "😴")
        if self.mood > 70:
            return sprites.get("happy", sprites["idle"])
        if self.mood < 30:
            return sprites.get("sad", sprites["idle"])
        return sprites["idle"]

    def tick(self, hours_passed: float = 1/60) -> list[str]:
        """
        Advance time. Call this regularly (e.g., every minute = 1/60 hour).
        Returns list of events that occurred.
        """
        events = []

        if self.is_dead:
            return ["💀 Creature is dead."]

        self.last_tick = datetime.now().isoformat()
        self.age_hours += hours_passed

        # Check for stage evolution
        stage_event = self._check_evolution()
        if stage_event:
            events.append(stage_event)

        # Stat decay (only when not sleeping)
        if not self.is_sleeping:
            # Hunger decay: -5/hour
            self.hunger = max(0, self.hunger - (5 * hours_passed))

            # Energy decay: -3/hour when awake
            self.energy = max(0, self.energy - (3 * hours_passed))

            # Mood varies based on needs
            if self.hunger < 20:
                self.mood = max(0, self.mood - (2 * hours_passed))
            if self.energy < 20:
                self.mood = max(0, self.mood - (1 * hours_passed))
        else:
            # Energy recovery while sleeping: +10/hour
            self.energy = min(100, self.energy + (10 * hours_passed))

        # Social decay when not linked
        if not self.linked_to:
            self.social = max(0, self.social - (1 * hours_passed))

        # Update health
        self.health = (self.hunger + self.energy + self.mood) / 3

        # Forced sleep check
        if self.energy < 20 and not self.is_sleeping:
            self.is_sleeping = True
            events.append("😴 Creature fell asleep from exhaustion!")

        # Death check
        if self.hunger <= 0 and self.health < 10:
            self.is_dead = True
            events.append("💀 Creature has died from neglect...")

        # Update care score (rolling average)
        current_care = (self.hunger + self.energy + self.mood) / 3
        self.care_score = (self.care_score * 0.99) + (current_care * 0.01)

        return events

    def _check_evolution(self) -> str | None:
        """Check if creature should evolve to next stage."""
        next_stages = {
            LifeStage.EGG: (LifeStage.HATCHLING, STAGE_THRESHOLDS[LifeStage.HATCHLING]),
            LifeStage.HATCHLING: (LifeStage.JUVENILE, STAGE_THRESHOLDS[LifeStage.JUVENILE]),
            LifeStage.JUVENILE: (LifeStage.ADULT, STAGE_THRESHOLDS[LifeStage.ADULT]),
            LifeStage.ADULT: (LifeStage.ELDER, STAGE_THRESHOLDS[LifeStage.ELDER]),
        }

        if self.stage in next_stages:
            next_stage, threshold = next_stages[self.stage]
            if self.age_hours >= threshold:
                old_stage = self.stage
                self.stage = next_stage

                # Determine evolution path based on care
                if self.care_score > 70:
                    self.evolution_path = "healthy"
                elif self.care_score < 30:
                    self.evolution_path = "neglected"

                return f"✨ Evolved from {old_stage.value} to {next_stage.value}! (Path: {self.evolution_path})"

        return None

    def feed(self, food_value: int = 10, mood_boost: int = 5) -> str:
        """Feed the creature."""
        if self.is_dead:
            return "💀 Cannot feed a dead creature."
        if self.is_sleeping:
            return "😴 Creature is sleeping..."

        self.hunger = min(100, self.hunger + food_value)
        self.mood = min(100, self.mood + mood_boost)
        self.bond = min(100, self.bond + 1)
        self.last_fed = datetime.now().isoformat()

        return f"🍎 Fed! Hunger: {self.hunger:.0f}, Mood: {self.mood:.0f}"

    def play(self) -> str:
        """Play with the creature."""
        if self.is_dead:
            return "💀 Cannot play with a dead creature."
        if self.is_sleeping:
            return "😴 Creature is sleeping..."
        if self.energy < 10:
            return "😫 Too tired to play!"

        self.mood = min(100, self.mood + 15)
        self.energy = max(0, self.energy - 10)
        self.bond = min(100, self.bond + 2)
        self.last_played = datetime.now().isoformat()

        return f"🎮 Played! Mood: {self.mood:.0f}, Energy: {self.energy:.0f}"

    def wake(self) -> str:
        """Wake the creature."""
        if not self.is_sleeping:
            return "Already awake!"

        self.is_sleeping = False
        return "👋 Creature woke up!"

    def sleep(self) -> str:
        """Put creature to sleep."""
        if self.is_sleeping:
            return "Already sleeping!"

        self.is_sleeping = True
        return "😴 Creature is now sleeping..."

    def link(self, other: "FogSiftCreature") -> str:
        """Link to another creature (magnetic connection)."""
        if self.is_dead or other.is_dead:
            return "💀 Cannot link dead creatures."

        self.linked_to = other.creature_id
        other.linked_to = self.creature_id

        # Social boost for both
        self.social = min(100, self.social + 10)
        other.social = min(100, other.social + 10)

        # Mood boost
        self.mood = min(100, self.mood + 5)
        other.mood = min(100, other.mood + 5)

        return f"🔗 {self.name} ({self.sprite}) meets {other.name} ({other.sprite})!"

    def unlink(self) -> str:
        """Unlink from connected creature."""
        if not self.linked_to:
            return "Not linked to anyone."

        self.linked_to = None
        return "🔓 Unlinked."

    def status(self) -> str:
        """Get formatted status string."""
        lines = [
            f"╭{'─' * 30}╮",
            f"│ {self.sprite} {self.name:<24} │",
            f"│ {self.species['name']:<28} │",
            f"├{'─' * 30}┤",
            f"│ Stage: {self.stage.value:<20} │",
            f"│ Age: {self.age_hours:.1f} hours{' ' * 14} │"[:33] + "│",
            f"├{'─' * 30}┤",
            f"│ Hunger: {'█' * int(self.hunger/10)}{'░' * (10-int(self.hunger/10))} {self.hunger:>3.0f}% │",
            f"│ Energy: {'█' * int(self.energy/10)}{'░' * (10-int(self.energy/10))} {self.energy:>3.0f}% │",
            f"│ Mood:   {'█' * int(self.mood/10)}{'░' * (10-int(self.mood/10))} {self.mood:>3.0f}% │",
            f"│ Bond:   {'█' * int(self.bond/10)}{'░' * (10-int(self.bond/10))} {self.bond:>3.0f}% │",
            f"├{'─' * 30}┤",
            f"│ Health: {self.health:.0f}%  Social: {self.social:.0f}%{' ' * 6} │"[:33] + "│",
            f"╰{'─' * 30}╯",
        ]

        if self.is_sleeping:
            lines.insert(3, f"│ {'💤 SLEEPING':<28} │")
        if self.is_dead:
            lines[1] = f"│ 💀 {self.name:<24} │"
            lines.insert(3, f"│ {'☠️  DEAD':<28} │")
        if self.linked_to:
            lines.insert(-1, f"│ 🔗 Linked{' ' * 19} │")

        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "creature_id": self.creature_id,
            "name": self.name,
            "species_id": self.species_id,
            "hunger": self.hunger,
            "energy": self.energy,
            "mood": self.mood,
            "bond": self.bond,
            "social": self.social,
            "health": self.health,
            "stage": self.stage.value,
            "age_hours": self.age_hours,
            "is_sleeping": self.is_sleeping,
            "is_dead": self.is_dead,
            "traits": {
                "color": self.traits.color,
                "pattern": self.traits.pattern,
                "personality": self.traits.personality,
                "quirk": self.traits.quirk,
            },
            "care_score": self.care_score,
            "evolution_path": self.evolution_path,
            "created_at": self.created_at,
            "last_fed": self.last_fed,
            "last_played": self.last_played,
            "last_tick": self.last_tick,
            "linked_to": self.linked_to,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FogSiftCreature":
        """Deserialize from dictionary."""
        creature = cls(
            creature_id=data["creature_id"],
            name=data["name"],
            species_id=data["species_id"],
            hunger=data["hunger"],
            energy=data["energy"],
            mood=data["mood"],
            bond=data["bond"],
            social=data.get("social", 0),
            health=data.get("health", 100),
            stage=LifeStage(data["stage"]),
            age_hours=data["age_hours"],
            is_sleeping=data["is_sleeping"],
            is_dead=data["is_dead"],
            care_score=data.get("care_score", 50),
            evolution_path=data.get("evolution_path", "normal"),
            created_at=data["created_at"],
            last_fed=data["last_fed"],
            last_played=data["last_played"],
            last_tick=data.get("last_tick", datetime.now().isoformat()),
            linked_to=data.get("linked_to"),
        )

        if "traits" in data:
            creature.traits = CreatureTraits(**data["traits"])

        return creature

    @classmethod
    def hatch(cls, name: str = "Unnamed", species_id: str = "pixel_fox") -> "FogSiftCreature":
        """Create a new creature (convenience factory)."""
        species = SPECIES.get(species_id, SPECIES["pixel_fox"])
        creature = cls(
            name=name,
            species_id=species_id,
            traits=CreatureTraits(**{
                "color": species["base_traits"].color,
                "pattern": species["base_traits"].pattern,
                "personality": species["base_traits"].personality,
            }),
        )
        return creature
