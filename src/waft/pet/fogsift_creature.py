"""
FogSift Creature: Modular pet device simulation.

Phase 0 of the FogSift hardware project - validate game mechanics
in software before building physical devices.
"""

import random
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class LifeStage(Enum):
    EGG = "egg"
    HATCHLING = "hatchling"
    JUVENILE = "juvenile"
    ADULT = "adult"
    ELDER = "elder"


class Element(Enum):
    FOREST = "forest"
    WATER = "water"
    FIRE = "fire"
    COSMIC = "cosmic"


@dataclass
class CreatureTraits:
    """Genetic traits passed through breeding."""
    color: str = "blue"
    pattern: str = "solid"
    personality: str = "curious"
    element: Element = Element.FOREST

    def mutate(self) -> "CreatureTraits":
        """5% chance per trait to mutate."""
        colors = ["blue", "green", "red", "orange", "purple", "pink", "gold"]
        patterns = ["solid", "spotted", "striped", "gradient"]
        personalities = ["curious", "shy", "bold", "lazy", "energetic"]

        return CreatureTraits(
            color=random.choice(colors) if random.random() < 0.05 else self.color,
            pattern=random.choice(patterns) if random.random() < 0.05 else self.pattern,
            personality=random.choice(personalities) if random.random() < 0.05 else self.personality,
            element=random.choice(list(Element)) if random.random() < 0.05 else self.element,
        )


@dataclass
class FogSiftCreature:
    """
    A creature for the FogSift modular pet device.

    Core stats from CREATURE_MECHANICS.md:
    - hunger: 0-100, decays 5/hour
    - energy: 0-100, decays 3/hour when awake
    - mood: 0-100, varies based on care
    - bond: 0-100, increases with interaction
    - social: 0-100, increases when linked to other devices
    """

    # Identity
    creature_id: str = field(default_factory=lambda: f"fog_{int(time.time() * 1000) % 1000000:06d}")
    name: str = "Unnamed"
    species: str = "PixelFox"
    traits: CreatureTraits = field(default_factory=CreatureTraits)

    # Core stats (0-100)
    hunger: float = 80.0
    energy: float = 100.0
    mood: float = 70.0
    bond: float = 0.0
    social: float = 0.0

    # Lifecycle
    stage: LifeStage = LifeStage.EGG
    age_hours: float = 0.0
    care_quality: float = 50.0  # Running average of care

    # State
    is_sleeping: bool = False
    is_linked: bool = False
    linked_to: Optional[str] = None  # creature_id of linked creature

    # Timing
    last_update: float = field(default_factory=time.time)
    birth_time: float = field(default_factory=time.time)

    # Decay rates (per hour)
    HUNGER_DECAY = 5.0
    ENERGY_DECAY_AWAKE = 3.0
    ENERGY_DECAY_ASLEEP = 0.5

    # Stage thresholds (hours)
    HATCH_AGE = 1.0
    JUVENILE_AGE = 24.0
    ADULT_AGE = 72.0
    ELDER_AGE = 168.0  # 1 week

    def tick(self, hours: float = None) -> dict[str, Any]:
        """
        Advance time and update stats.
        Returns a dict of events that occurred.
        """
        now = time.time()
        if hours is None:
            hours = (now - self.last_update) / 3600
        self.last_update = now

        events = []

        # Age
        self.age_hours += hours

        # Check for stage transitions
        old_stage = self.stage
        self._update_stage()
        if self.stage != old_stage:
            events.append({"type": "evolution", "from": old_stage.value, "to": self.stage.value})

        # Skip stat decay if still an egg
        if self.stage == LifeStage.EGG:
            return {"events": events, "hours_passed": hours}

        # Hunger decay
        self.hunger = max(0, self.hunger - self.HUNGER_DECAY * hours)
        if self.hunger < 20:
            self.mood = max(0, self.mood - 5 * hours)  # Mood penalty when hungry
            events.append({"type": "hungry"})

        # Energy decay
        if self.is_sleeping:
            # Recover energy while sleeping
            self.energy = min(100, self.energy + 10 * hours)
            if self.energy >= 80:
                self.is_sleeping = False
                events.append({"type": "wake"})
        else:
            self.energy = max(0, self.energy - self.ENERGY_DECAY_AWAKE * hours)
            if self.energy < 20:
                self.is_sleeping = True
                events.append({"type": "sleep"})

        # Social decay when not linked
        if not self.is_linked:
            self.social = max(0, self.social - 2 * hours)

        # Update care quality (rolling average)
        current_care = (self.hunger + self.energy + self.mood) / 3
        self.care_quality = 0.9 * self.care_quality + 0.1 * current_care

        return {"events": events, "hours_passed": hours}

    def _update_stage(self):
        """Check and update life stage based on age."""
        if self.age_hours >= self.ELDER_AGE:
            self.stage = LifeStage.ELDER
        elif self.age_hours >= self.ADULT_AGE:
            self.stage = LifeStage.ADULT
        elif self.age_hours >= self.JUVENILE_AGE:
            self.stage = LifeStage.JUVENILE
        elif self.age_hours >= self.HATCH_AGE:
            self.stage = LifeStage.HATCHLING
        else:
            self.stage = LifeStage.EGG

    def feed(self, food_value: int = 20) -> dict[str, Any]:
        """Feed the creature."""
        if self.stage == LifeStage.EGG:
            return {"success": False, "message": "Can't feed an egg!"}

        old_hunger = self.hunger
        self.hunger = min(100, self.hunger + food_value)
        self.mood = min(100, self.mood + 5)
        self.bond = min(100, self.bond + 1)

        return {
            "success": True,
            "hunger_gained": self.hunger - old_hunger,
            "new_hunger": self.hunger
        }

    def play(self) -> dict[str, Any]:
        """Play with the creature."""
        if self.stage == LifeStage.EGG:
            return {"success": False, "message": "Can't play with an egg!"}
        if self.is_sleeping:
            return {"success": False, "message": "Creature is sleeping"}
        if self.energy < 10:
            return {"success": False, "message": "Too tired to play"}

        self.mood = min(100, self.mood + 15)
        self.bond = min(100, self.bond + 3)
        self.energy = max(0, self.energy - 10)

        return {"success": True, "new_mood": self.mood, "new_energy": self.energy}

    def link(self, other: "FogSiftCreature") -> dict[str, Any]:
        """
        Link with another creature (magnetic connection).
        Both creatures benefit from the social interaction.
        """
        if self.stage == LifeStage.EGG or other.stage == LifeStage.EGG:
            return {"success": False, "message": "Can't link with an egg"}

        self.is_linked = True
        self.linked_to = other.creature_id
        other.is_linked = True
        other.linked_to = self.creature_id

        # Social boost for both
        self.social = min(100, self.social + 20)
        other.social = min(100, other.social + 20)
        self.mood = min(100, self.mood + 10)
        other.mood = min(100, other.mood + 10)

        return {
            "success": True,
            "message": f"{self.name} meets {other.name}!",
            "self_social": self.social,
            "other_social": other.social,
        }

    def unlink(self):
        """Disconnect from linked creature."""
        self.is_linked = False
        self.linked_to = None

    def get_emotion(self) -> str:
        """Get current emotional state for display."""
        if self.stage == LifeStage.EGG:
            return "egg"
        if self.is_sleeping:
            return "sleeping"
        if self.hunger < 20:
            return "hungry"
        if self.energy < 20:
            return "tired"
        if self.mood > 80:
            return "happy"
        if self.mood < 30:
            return "sad"
        if self.social > 60 and self.is_linked:
            return "social"
        return "content"

    def get_ascii_art(self) -> str:
        """Get ASCII representation based on species and emotion."""
        emotion = self.get_emotion()

        # Simple ASCII sprites
        sprites = {
            "egg": [
                "  ___  ",
                " /   \\ ",
                "|     |",
                " \\___/ ",
            ],
            "sleeping": [
                " /\\_/\\ ",
                "( -.- )",
                " > ^ < ",
                "  zzZ  ",
            ],
            "happy": [
                " /\\_/\\ ",
                "( ^.^ )",
                " > ~ < ",
                "  ~~~  ",
            ],
            "hungry": [
                " /\\_/\\ ",
                "( o.o )",
                " > o < ",
                "  ...  ",
            ],
            "tired": [
                " /\\_/\\ ",
                "( -.- )",
                " > - < ",
                "  ...  ",
            ],
            "sad": [
                " /\\_/\\ ",
                "( ;.; )",
                " > n < ",
                "  ...  ",
            ],
            "social": [
                " /\\_/\\ ",
                "( ^o^ )",
                " > w < ",
                "  <3   ",
            ],
            "content": [
                " /\\_/\\ ",
                "( o.o )",
                " > ^ < ",
                "  ~~~  ",
            ],
        }

        art = sprites.get(emotion, sprites["content"])
        return "\n".join(art)

    def get_status(self) -> str:
        """Get formatted status string."""
        bars = lambda v: "█" * int(v / 10) + "░" * (10 - int(v / 10))

        return f"""
╔══════════════════════════════════╗
║ {self.name:^32} ║
║ {self.species} ({self.stage.value})
╠══════════════════════════════════╣
{self.get_ascii_art()}
╠══════════════════════════════════╣
║ Hunger: [{bars(self.hunger)}] {self.hunger:5.1f}
║ Energy: [{bars(self.energy)}] {self.energy:5.1f}
║ Mood:   [{bars(self.mood)}] {self.mood:5.1f}
║ Bond:   [{bars(self.bond)}] {self.bond:5.1f}
║ Social: [{bars(self.social)}] {self.social:5.1f}
╠══════════════════════════════════╣
║ Age: {self.age_hours:.1f}h | Emotion: {self.get_emotion()}
║ Linked: {self.linked_to or 'None'}
╚══════════════════════════════════╝
"""

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict for persistence."""
        return {
            "creature_id": self.creature_id,
            "name": self.name,
            "species": self.species,
            "traits": {
                "color": self.traits.color,
                "pattern": self.traits.pattern,
                "personality": self.traits.personality,
                "element": self.traits.element.value,
            },
            "hunger": self.hunger,
            "energy": self.energy,
            "mood": self.mood,
            "bond": self.bond,
            "social": self.social,
            "stage": self.stage.value,
            "age_hours": self.age_hours,
            "care_quality": self.care_quality,
            "is_sleeping": self.is_sleeping,
            "is_linked": self.is_linked,
            "linked_to": self.linked_to,
            "last_update": self.last_update,
            "birth_time": self.birth_time,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FogSiftCreature":
        """Deserialize from dict."""
        traits = CreatureTraits(
            color=data["traits"]["color"],
            pattern=data["traits"]["pattern"],
            personality=data["traits"]["personality"],
            element=Element(data["traits"]["element"]),
        )
        return cls(
            creature_id=data["creature_id"],
            name=data["name"],
            species=data["species"],
            traits=traits,
            hunger=data["hunger"],
            energy=data["energy"],
            mood=data["mood"],
            bond=data["bond"],
            social=data["social"],
            stage=LifeStage(data["stage"]),
            age_hours=data["age_hours"],
            care_quality=data["care_quality"],
            is_sleeping=data["is_sleeping"],
            is_linked=data["is_linked"],
            linked_to=data["linked_to"],
            last_update=data["last_update"],
            birth_time=data["birth_time"],
        )


def breed(parent_a: FogSiftCreature, parent_b: FogSiftCreature) -> FogSiftCreature | None:
    """
    Breed two creatures to produce offspring.
    Returns None if breeding fails.
    """
    if parent_a.stage not in (LifeStage.ADULT, LifeStage.ELDER):
        return None
    if parent_b.stage not in (LifeStage.ADULT, LifeStage.ELDER):
        return None

    # Element compatibility
    same_element = parent_a.traits.element == parent_b.traits.element
    success_chance = 1.0 if same_element else 0.75

    if random.random() > success_chance:
        return None

    # Inherit and mutate traits
    child_traits = CreatureTraits(
        color=random.choice([parent_a.traits.color, parent_b.traits.color]),
        pattern=random.choice([parent_a.traits.pattern, parent_b.traits.pattern]),
        personality=random.choice([parent_a.traits.personality, parent_b.traits.personality]),
        element=random.choice([parent_a.traits.element, parent_b.traits.element]),
    ).mutate()

    return FogSiftCreature(
        name=f"Baby of {parent_a.name}",
        species=parent_a.species,  # Inherit species from parent A
        traits=child_traits,
        stage=LifeStage.EGG,
    )


# Starter species
STARTER_SPECIES = {
    "PixelFox": {"element": Element.FOREST, "personality": "curious"},
    "Hoot": {"element": Element.FOREST, "personality": "wise"},
    "Splash": {"element": Element.WATER, "personality": "energetic"},
    "Ember": {"element": Element.FIRE, "personality": "bold"},
}


def create_starter(species: str, name: str = None) -> FogSiftCreature:
    """Create a starter creature of the given species."""
    if species not in STARTER_SPECIES:
        species = "PixelFox"

    config = STARTER_SPECIES[species]
    traits = CreatureTraits(
        element=config["element"],
        personality=config["personality"],
    )

    return FogSiftCreature(
        name=name or species,
        species=species,
        traits=traits,
        stage=LifeStage.EGG,
    )


if __name__ == "__main__":
    # Demo: Create two creatures and link them
    print("=== FogSift Creature Simulation Demo ===\n")

    fox = create_starter("PixelFox", "Luna")
    owl = create_starter("Hoot", "Orion")

    # Hatch them (skip egg stage for demo)
    fox.age_hours = 2
    fox.tick(0)
    owl.age_hours = 2
    owl.tick(0)

    print(fox.get_status())
    print(owl.get_status())

    # Link them
    print("\n--- Linking creatures ---\n")
    result = fox.link(owl)
    print(f"Link result: {result['message']}")

    print(fox.get_status())
    print(owl.get_status())

    # Feed and play
    print("\n--- Feeding Luna ---")
    fox.feed()
    print(f"Luna's hunger: {fox.hunger}")

    print("\n--- Playing with Orion ---")
    owl.play()
    print(f"Orion's mood: {owl.mood}")
