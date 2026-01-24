"""
NPC Generator - Characters with Personalities and Secrets
=========================================================

Generates complete NPCs for the storyteller with:
- Appearance (race, age, distinguishing features)
- Personality traits
- Secrets/motivations
- Relationships to other NPCs
"""

import random
from dataclasses import dataclass, field
from enum import Enum

from .names import NameGenerator


class Race(Enum):
    HUMAN = "human"
    DWARF = "dwarf"
    ELF = "elf"
    HALF_ORC = "half-orc"
    HALFLING = "halfling"
    GNOME = "gnome"
    TIEFLING = "tiefling"
    DRAGONBORN = "dragonborn"


class Occupation(Enum):
    # Tavern staff
    BARTENDER = "bartender"
    BARMAID = "barmaid"
    COOK = "cook"
    BOUNCER = "bouncer"

    # Common folk
    MERCHANT = "merchant"
    FARMER = "farmer"
    CRAFTSMAN = "craftsman"
    SAILOR = "sailor"
    MINER = "miner"
    HUNTER = "hunter"

    # Adventurer types
    ADVENTURER = "adventurer"
    MERCENARY = "mercenary"
    RETIRED_SOLDIER = "retired soldier"
    TREASURE_HUNTER = "treasure hunter"

    # Learned folk
    SCHOLAR = "scholar"
    WIZARD = "wizard"
    HEDGE_WITCH = "hedge witch"
    HEALER = "healer"
    PRIEST = "priest"

    # Rogues
    THIEF = "thief"
    SPY = "spy"
    SMUGGLER = "smuggler"
    GAMBLER = "gambler"

    # Nobility
    NOBLE = "noble"
    KNIGHT = "knight"
    DIPLOMAT = "diplomat"

    # Performers
    BARD = "bard"
    ENTERTAINER = "entertainer"
    STORYTELLER = "storyteller"

    # Mysterious
    STRANGER = "stranger"
    TRAVELER = "traveler"
    PILGRIM = "pilgrim"


# Appearance traits
PHYSICAL_FEATURES = [
    "scarred face", "missing eye", "bushy eyebrows", "bald head", "wild hair",
    "braided hair", "long beard", "clean-shaven", "weather-beaten skin", "pale complexion",
    "tanned skin", "freckled face", "crooked nose", "sharp jawline", "round face",
    "gaunt features", "muscular build", "thin frame", "stocky build", "tall and lanky",
    "short and stout", "calloused hands", "delicate fingers", "tattoed arms", "pierced ears",
    "gold tooth", "missing fingers", "limp", "hunched posture", "proud bearing"
]

CLOTHING_STYLES = [
    "worn traveling cloak", "fine silk clothes", "practical leather armor", "colorful robes",
    "simple peasant garb", "stained apron", "military uniform", "hooded cloak",
    "merchant's finery", "patched clothes", "sailor's garb", "scholar's robes",
    "priestly vestments", "noble attire", "exotic foreign clothes", "all black",
    "flashy jewelry", "subtle quality", "deliberately plain", "distinctly out of place"
]

DISTINGUISHING_MARKS = [
    "a faded tattoo of a ship", "a signet ring with an unknown crest", "an unusual amulet",
    "a distinctive scar across the cheek", "heterochromatic eyes", "a nervous twitch",
    "always cleaning their nails", "constantly checking over their shoulder",
    "a melodic humming habit", "a foreign accent", "speaks in riddles",
    "never makes eye contact", "stares too intensely", "laughs at inappropriate times",
    "carries an old book everywhere", "a pet rat on their shoulder", "mismatched boots",
    "ink-stained fingers", "burn marks on their hands", "a wedding ring on a chain"
]

# Personality
PERSONALITY_TRAITS = [
    # Positive
    "friendly", "cheerful", "wise", "honest", "brave", "generous", "loyal",
    "patient", "optimistic", "helpful", "humble", "curious", "witty",

    # Neutral
    "quiet", "mysterious", "eccentric", "observant", "pragmatic", "stoic",
    "blunt", "formal", "casual", "cautious", "ambitious",

    # Negative
    "grumpy", "suspicious", "arrogant", "greedy", "nervous", "bitter",
    "rude", "paranoid", "secretive", "melancholic", "irritable"
]

SPEECH_PATTERNS = [
    "speaks in a whisper", "has a booming voice", "uses fancy words",
    "speaks simply", "has a thick accent", "speaks very slowly",
    "talks too fast", "uses lots of profanity", "overly polite",
    "tells bad jokes", "always sighs before speaking", "interrupts constantly",
    "pauses dramatically", "speaks in the third person", "ends sentences with questions",
]

# Secrets and Motivations
SECRETS = [
    "is actually a minor noble in hiding",
    "witnessed a murder and is being hunted",
    "owes a large debt to a dangerous person",
    "is searching for a missing family member",
    "possesses a stolen artifact",
    "is a spy for a foreign power",
    "has a forbidden magical ability",
    "is slowly being poisoned",
    "made a deal with a devil",
    "is not who they claim to be",
    "knows the location of a hidden treasure",
    "is planning a heist",
    "is fleeing from their past",
    "has a bounty on their head",
    "is cursed and seeking a cure",
    "is a member of a secret society",
    "has information about a conspiracy",
    "is dying and has nothing to lose",
    "is being blackmailed",
    "lost everything to gambling",
]

MOTIVATIONS = [
    "wants revenge for a past wrong",
    "seeks wealth to buy their family's freedom",
    "searching for a lost love",
    "trying to clear their name",
    "wants to prove themselves worthy",
    "seeks forbidden knowledge",
    "running from their past",
    "protecting someone important",
    "wants to start a new life",
    "seeking redemption for past sins",
    "hunting a monster that killed their family",
    "looking for adventure",
    "trying to pay off a debt",
    "wants power and influence",
    "serving a higher purpose",
]

# What they want from the player
HOOKS = [
    "needs an escort to a dangerous location",
    "wants to hire someone for a discrete job",
    "has information to trade",
    "is looking for specific adventurers",
    "needs protection from someone",
    "wants to sell something unusual",
    "is gathering a party for a quest",
    "needs a message delivered",
    "is searching for a specific item",
    "wants someone to settle a score",
    "needs help with a personal matter",
    "is testing the player's character",
    "wants to share a warning",
    "is recruiting for a cause",
    "has a job that pays well but seems suspicious",
]


@dataclass
class NPC:
    """A generated NPC with full details."""
    name: str
    race: str
    occupation: str
    age_category: str  # young, adult, middle-aged, elderly

    # Appearance
    physical_features: list[str] = field(default_factory=list)
    clothing: str = ""
    distinguishing_mark: str = ""

    # Personality
    personality_traits: list[str] = field(default_factory=list)
    speech_pattern: str = ""

    # Hidden depths
    secret: str = ""
    motivation: str = ""
    hook: str = ""  # What they want from the player

    # Relationships
    relationships: dict[str, str] = field(default_factory=dict)  # name -> relationship

    # For storyteller context
    is_staff: bool = False
    is_patron: bool = True
    mood: str = "neutral"  # current mood

    def description(self) -> str:
        """Generate a prose description of this NPC."""
        features = ", ".join(self.physical_features[:2]) if self.physical_features else "unremarkable features"
        traits = " and ".join(self.personality_traits[:2]) if self.personality_traits else "quiet"

        return (
            f"{self.name} is a {self.age_category} {self.race} {self.occupation}. "
            f"They have {features}, wearing {self.clothing}. "
            f"They seem {traits}. "
            f"{self.distinguishing_mark.capitalize() if self.distinguishing_mark else ''}"
        ).strip()

    def short_description(self) -> str:
        """One-line description for quick reference."""
        trait = self.personality_traits[0] if self.personality_traits else "quiet"
        return f"{self.name} ({self.race} {self.occupation}, {trait})"

    def storyteller_context(self) -> dict:
        """Context dict for the AI storyteller."""
        return {
            "name": self.name,
            "race": self.race,
            "occupation": self.occupation,
            "description": self.description(),
            "personality": self.personality_traits,
            "speech": self.speech_pattern,
            "secret": self.secret,
            "motivation": self.motivation,
            "hook": self.hook,
            "mood": self.mood,
        }


class NPCGenerator:
    """Generates complete NPCs with personalities and secrets."""

    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)
        self.name_gen = NameGenerator(seed)

    def generate(
        self,
        race: str | None = None,
        occupation: str | Occupation | None = None,
        is_staff: bool = False,
        include_secret: bool = True,
    ) -> NPC:
        """Generate a complete NPC."""

        # Determine race
        if race is None:
            race = self._random_race()
        race = race.lower()

        # Determine occupation
        if occupation is None:
            if is_staff:
                occupation = self.rng.choice([
                    Occupation.BARTENDER, Occupation.BARMAID,
                    Occupation.COOK, Occupation.BOUNCER
                ])
            else:
                occupation = self.rng.choice(list(Occupation))

        if isinstance(occupation, Occupation):
            occupation = occupation.value

        # Generate name
        name = self.name_gen.character_name(race).full_name

        # Age
        age = self.rng.choice(["young", "adult", "middle-aged", "elderly"])

        # Appearance
        features = self.rng.sample(PHYSICAL_FEATURES, k=self.rng.randint(1, 3))
        clothing = self.rng.choice(CLOTHING_STYLES)
        mark = self.rng.choice(DISTINGUISHING_MARKS) if self.rng.random() < 0.7 else ""

        # Personality
        traits = self.rng.sample(PERSONALITY_TRAITS, k=self.rng.randint(2, 3))
        speech = self.rng.choice(SPEECH_PATTERNS) if self.rng.random() < 0.6 else ""

        # Secrets (optional)
        secret = ""
        motivation = ""
        hook = ""
        if include_secret:
            secret = self.rng.choice(SECRETS)
            motivation = self.rng.choice(MOTIVATIONS)
            hook = self.rng.choice(HOOKS)

        return NPC(
            name=name,
            race=race,
            occupation=occupation,
            age_category=age,
            physical_features=features,
            clothing=clothing,
            distinguishing_mark=mark,
            personality_traits=traits,
            speech_pattern=speech,
            secret=secret,
            motivation=motivation,
            hook=hook,
            is_staff=is_staff,
            is_patron=not is_staff,
            mood=self.rng.choice(["relaxed", "neutral", "tense", "cheerful", "tired"]),
        )

    def generate_staff(self, role: str | Occupation | None = None) -> NPC:
        """Generate a tavern staff member."""
        return self.generate(occupation=role, is_staff=True, include_secret=False)

    def generate_patron(self, mysterious: bool = False) -> NPC:
        """Generate a tavern patron."""
        npc = self.generate(is_staff=False, include_secret=True)

        if mysterious:
            # Make them more mysterious
            npc.personality_traits = ["mysterious", "secretive"] + npc.personality_traits[:1]
            npc.clothing = self.rng.choice(["hooded cloak", "all black", "exotic foreign clothes"])

        return npc

    def generate_group(self, count: int = 3, theme: str | None = None) -> list[NPC]:
        """Generate a group of related NPCs."""
        npcs = []
        relationship_pool = [
            "traveling companion", "business partner", "old friend",
            "rival", "bodyguard", "employer", "sibling", "spouse"
        ]

        for i in range(count):
            npc = self.generate()

            # Add relationships to previous NPCs
            if npcs and self.rng.random() < 0.7:
                other = self.rng.choice(npcs)
                rel = self.rng.choice(relationship_pool)
                npc.relationships[other.name] = rel
                other.relationships[npc.name] = self._inverse_relationship(rel)

            npcs.append(npc)

        return npcs

    def _random_race(self) -> str:
        """Random race with weighted distribution (humans most common)."""
        weights = {
            "human": 50,
            "dwarf": 15,
            "elf": 12,
            "half-orc": 8,
            "halfling": 8,
            "gnome": 4,
            "tiefling": 2,
            "dragonborn": 1,
        }
        races = list(weights.keys())
        probs = list(weights.values())
        return self.rng.choices(races, weights=probs, k=1)[0]

    def _inverse_relationship(self, rel: str) -> str:
        """Get the inverse of a relationship."""
        inverses = {
            "traveling companion": "traveling companion",
            "business partner": "business partner",
            "old friend": "old friend",
            "rival": "rival",
            "bodyguard": "employer",
            "employer": "bodyguard",
            "sibling": "sibling",
            "spouse": "spouse",
        }
        return inverses.get(rel, "acquaintance")


# Convenience function
def generate_npc(race: str | None = None, occupation: str | None = None, seed: int | None = None) -> NPC:
    """Quick NPC generation."""
    return NPCGenerator(seed).generate(race=race, occupation=occupation)


if __name__ == "__main__":
    # Demo
    gen = NPCGenerator(seed=42)
    print("=== NPC Generator Demo ===\n")

    print("Random NPC:")
    npc = gen.generate()
    print(f"  {npc.description()}")
    print(f"  Secret: {npc.secret}")
    print(f"  Motivation: {npc.motivation}")
    print(f"  Hook: {npc.hook}")

    print("\n\nTavern Staff:")
    for role in [Occupation.BARTENDER, Occupation.BARMAID, Occupation.COOK]:
        staff = gen.generate_staff(role)
        print(f"  {staff.short_description()}")

    print("\n\nMysterious Stranger:")
    stranger = gen.generate_patron(mysterious=True)
    print(f"  {stranger.description()}")
    print(f"  Secret: {stranger.secret}")

    print("\n\nGroup of Adventurers:")
    group = gen.generate_group(3)
    for npc in group:
        print(f"  {npc.short_description()}")
        if npc.relationships:
            for name, rel in npc.relationships.items():
                print(f"    -> {rel} of {name}")
