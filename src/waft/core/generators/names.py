"""
Name Generator - Fantasy Names using Weighted Syllable Patterns
===============================================================

Generates fantasy names for characters, taverns, and places.
Uses Markov-like syllable combination inspired by Donjon's approach.
"""

import random
from dataclasses import dataclass
from pathlib import Path

# Syllable patterns for different races/cultures
HUMAN_FIRST = {
    "start": ["Al", "Bran", "Cor", "Dar", "Ed", "Finn", "Gar", "Hal", "Isen", "Jor",
              "Kel", "Lor", "Mar", "Ner", "Or", "Per", "Quin", "Ren", "Ser", "Tor",
              "Val", "Wil", "Xan", "Yar", "Zar", "Ae", "Bel", "Cal", "Del", "El"],
    "middle": ["a", "e", "i", "o", "u", "ae", "ia", "io", "an", "en", "in", "on",
               "ar", "er", "ir", "or", "al", "el", "il", "ol", "as", "es", "is"],
    "end": ["rick", "wen", "dor", "mir", "ric", "ald", "bert", "win", "mund", "ward",
            "son", "ton", "den", "ley", "ford", "well", "wood", "dale", "brook", "field",
            "ran", "dan", "gan", "van", "lan", "rin", "din", "gin", "vin", "lin"]
}

HUMAN_LAST = {
    "start": ["Black", "Grey", "Storm", "Iron", "Stone", "Dark", "Swift", "Bright",
              "Cold", "Warm", "Red", "White", "Gold", "Silver", "Frost", "Fire",
              "Oak", "Ash", "Elm", "Thorn", "Hawk", "Wolf", "Bear", "Raven", "Eagle"],
    "end": ["wood", "ford", "well", "dale", "brook", "field", "stone", "hill",
            "vale", "glen", "ridge", "cliff", "wind", "fire", "frost", "blade",
            "shield", "hammer", "axe", "bow", "heart", "soul", "bane", "forge", "keep"]
}

DWARF_FIRST = {
    "start": ["Thor", "Dur", "Bal", "Gim", "Bom", "Dwa", "Glo", "Bif", "Dor", "Nor",
              "Fili", "Kili", "Oin", "Glo", "Bof", "Thro", "Dain", "Nain", "Frar", "Grar"],
    "end": ["in", "ur", "im", "or", "ar", "ir", "on", "an", "en", "un",
            "li", "ri", "ni", "ki", "bi", "di", "fi", "gi", "mi", "vi"]
}

DWARF_LAST = {
    "start": ["Iron", "Stone", "Gold", "Silver", "Granite", "Copper", "Bronze", "Steel",
              "Mithril", "Adamant", "Ruby", "Emerald", "Sapphire", "Diamond", "Onyx"],
    "end": ["beard", "hammer", "axe", "helm", "shield", "forge", "anvil", "pick",
            "delve", "mine", "deep", "hold", "vault", "brew", "smith"]
}

ELF_FIRST = {
    "start": ["Ael", "Aer", "Ara", "Cel", "Eil", "Fae", "Gal", "Hael", "Iel", "Lae",
              "Mae", "Nae", "Rae", "Sae", "Tae", "Thae", "Vae", "Ael", "Ial", "Ael"],
    "middle": ["a", "e", "i", "ae", "ia", "ie", "ea", "ei", "ai", "oi"],
    "end": ["rion", "thien", "wen", "dil", "las", "mir", "ril", "thin", "wyn", "ros",
            "lith", "rian", "neth", "liel", "rien", "viel", "ael", "iel", "oel", "uel"]
}

ELF_LAST = {
    "start": ["Moon", "Star", "Sun", "Shadow", "Silver", "Golden", "Crystal", "Dawn",
              "Dusk", "Night", "Light", "Dream", "Wind", "Leaf", "Flower", "Rose"],
    "end": ["weaver", "dancer", "singer", "walker", "watcher", "keeper", "seeker",
            "blade", "bow", "arrow", "song", "whisper", "gleam", "glow", "shine"]
}

ORC_FIRST = {
    "start": ["Gro", "Gor", "Mog", "Ug", "Gul", "Mur", "Bur", "Dur", "Kro", "Zug",
              "Grag", "Morg", "Thog", "Grim", "Kruk", "Lur", "Nag", "Rag", "Shag", "Tug"],
    "end": ["bash", "mash", "krag", "thak", "gul", "mog", "rog", "zog", "gash", "nash",
            "uk", "ak", "ok", "ik", "ag", "og", "ug", "ig", "az", "oz"]
}

ORC_LAST = {
    "start": ["Skull", "Blood", "Bone", "Death", "Doom", "War", "Battle", "Rage",
              "Iron", "Stone", "Black", "Red", "Fire", "Storm", "Thunder"],
    "end": ["crusher", "smasher", "breaker", "render", "cleaver", "ripper", "slayer",
            "fist", "maw", "claw", "fang", "eye", "tusk", "horn", "hide"]
}

# Tavern name components
TAVERN_ADJECTIVES = [
    "Rusty", "Golden", "Silver", "Crimson", "Azure", "Emerald", "Obsidian",
    "Gilded", "Broken", "Wandering", "Prancing", "Sleeping", "Dancing", "Laughing",
    "Singing", "Drunken", "Weary", "Hungry", "Jolly", "Merry", "Gloomy", "Haunted",
    "Lucky", "Unlucky", "Enchanted", "Cursed", "Blessed", "Ancient", "Noble", "Humble",
    "Quiet", "Rowdy", "Peaceful", "Wild", "Tame", "Fierce", "Gentle", "Bold", "Shy"
]

TAVERN_NOUNS = [
    "Anchor", "Anvil", "Arrow", "Axe", "Barrel", "Bear", "Boar", "Bow", "Bucket",
    "Cauldron", "Crown", "Dagger", "Dragon", "Eagle", "Elk", "Falcon", "Flask",
    "Goblet", "Griffin", "Hammer", "Harp", "Helm", "Horn", "Horse", "Jester",
    "Keg", "Knight", "Lantern", "Lion", "Mermaid", "Moon", "Oak", "Owl", "Pony",
    "Raven", "Rose", "Shield", "Stag", "Star", "Sword", "Tankard", "Troll",
    "Unicorn", "Wagon", "Wyvern", "Phoenix", "Serpent", "Wolf", "Whale", "Witch"
]

TAVERN_SUFFIXES = ["Inn", "Tavern", "Pub", "Alehouse", "Lodge", "Rest", "Hall", "House"]

# Place name components
PLACE_PREFIXES = [
    "North", "South", "East", "West", "Upper", "Lower", "Old", "New", "High", "Low",
    "Dark", "Bright", "Shadow", "Sun", "Moon", "Star", "Storm", "Thunder", "Frost", "Fire"
]

PLACE_ROOTS = [
    "haven", "hold", "keep", "ford", "dale", "vale", "glen", "brook", "creek", "well",
    "spring", "falls", "ridge", "cliff", "peak", "mount", "hill", "moor", "fen", "marsh",
    "wood", "grove", "glade", "meadow", "field", "garden", "port", "bay", "cove", "shore"
]


@dataclass
class GeneratedName:
    """A generated name with its components."""
    full_name: str
    first_name: str | None = None
    last_name: str | None = None
    name_type: str = "generic"  # character, tavern, place


class NameGenerator:
    """Generates fantasy names using weighted syllable patterns."""

    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)

    def character_name(self, race: str = "human") -> GeneratedName:
        """Generate a character name for the given race."""
        race = race.lower()

        if race == "human":
            first = self._human_first()
            last = self._human_last()
        elif race == "dwarf":
            first = self._dwarf_first()
            last = self._dwarf_last()
        elif race == "elf":
            first = self._elf_first()
            last = self._elf_last()
        elif race in ("orc", "half-orc"):
            first = self._orc_first()
            last = self._orc_last()
        else:
            # Default to human for unknown races
            first = self._human_first()
            last = self._human_last()

        return GeneratedName(
            full_name=f"{first} {last}",
            first_name=first,
            last_name=last,
            name_type="character"
        )

    def tavern_name(self) -> GeneratedName:
        """Generate a tavern name (The [Adjective] [Noun] pattern)."""
        adj = self.rng.choice(TAVERN_ADJECTIVES)
        noun = self.rng.choice(TAVERN_NOUNS)

        # Sometimes add a suffix
        if self.rng.random() < 0.3:
            suffix = self.rng.choice(TAVERN_SUFFIXES)
            full = f"The {adj} {noun} {suffix}"
        else:
            full = f"The {adj} {noun}"

        return GeneratedName(full_name=full, name_type="tavern")

    def place_name(self) -> GeneratedName:
        """Generate a place/location name."""
        # Different patterns
        pattern = self.rng.choice(["prefix_root", "compound", "descriptive"])

        if pattern == "prefix_root":
            prefix = self.rng.choice(PLACE_PREFIXES)
            root = self.rng.choice(PLACE_ROOTS)
            full = f"{prefix}{root}"
        elif pattern == "compound":
            adj = self.rng.choice(TAVERN_ADJECTIVES[:20])  # Reuse some adjectives
            root = self.rng.choice(PLACE_ROOTS)
            full = f"{adj} {root.title()}"
        else:
            # Use character name style for descriptive
            first = self._human_first()
            root = self.rng.choice(PLACE_ROOTS)
            full = f"{first}'s {root.title()}"

        return GeneratedName(full_name=full, name_type="place")

    def first_name(self, race: str = "human") -> str:
        """Generate just a first name."""
        race = race.lower()
        if race == "dwarf":
            return self._dwarf_first()
        elif race == "elf":
            return self._elf_first()
        elif race in ("orc", "half-orc"):
            return self._orc_first()
        return self._human_first()

    # Private methods for each race

    def _human_first(self) -> str:
        """Generate a human first name."""
        start = self.rng.choice(HUMAN_FIRST["start"])
        if self.rng.random() < 0.5:
            middle = self.rng.choice(HUMAN_FIRST["middle"])
            end = self.rng.choice(HUMAN_FIRST["end"][:15])  # Shorter endings
            return start + middle + end
        return start + self.rng.choice(HUMAN_FIRST["end"])

    def _human_last(self) -> str:
        """Generate a human last name."""
        return self.rng.choice(HUMAN_LAST["start"]) + self.rng.choice(HUMAN_LAST["end"])

    def _dwarf_first(self) -> str:
        """Generate a dwarf first name."""
        return self.rng.choice(DWARF_FIRST["start"]) + self.rng.choice(DWARF_FIRST["end"])

    def _dwarf_last(self) -> str:
        """Generate a dwarf last name."""
        return self.rng.choice(DWARF_LAST["start"]) + self.rng.choice(DWARF_LAST["end"])

    def _elf_first(self) -> str:
        """Generate an elf first name."""
        start = self.rng.choice(ELF_FIRST["start"])
        if self.rng.random() < 0.6:
            middle = self.rng.choice(ELF_FIRST["middle"])
            return start + middle + self.rng.choice(ELF_FIRST["end"])
        return start + self.rng.choice(ELF_FIRST["end"])

    def _elf_last(self) -> str:
        """Generate an elf last name."""
        return self.rng.choice(ELF_LAST["start"]) + self.rng.choice(ELF_LAST["end"])

    def _orc_first(self) -> str:
        """Generate an orc first name."""
        return self.rng.choice(ORC_FIRST["start"]) + self.rng.choice(ORC_FIRST["end"])

    def _orc_last(self) -> str:
        """Generate an orc last name."""
        return self.rng.choice(ORC_LAST["start"]) + self.rng.choice(ORC_LAST["end"])


# Convenience function
def generate_name(name_type: str = "character", race: str = "human", seed: int | None = None) -> str:
    """Quick name generation."""
    gen = NameGenerator(seed)
    if name_type == "tavern":
        return gen.tavern_name().full_name
    elif name_type == "place":
        return gen.place_name().full_name
    return gen.character_name(race).full_name


if __name__ == "__main__":
    # Demo
    gen = NameGenerator(seed=42)
    print("=== Name Generator Demo ===\n")

    print("Human names:")
    for _ in range(3):
        print(f"  {gen.character_name('human').full_name}")

    print("\nDwarf names:")
    for _ in range(3):
        print(f"  {gen.character_name('dwarf').full_name}")

    print("\nElf names:")
    for _ in range(3):
        print(f"  {gen.character_name('elf').full_name}")

    print("\nOrc names:")
    for _ in range(3):
        print(f"  {gen.character_name('orc').full_name}")

    print("\nTavern names:")
    for _ in range(5):
        print(f"  {gen.tavern_name().full_name}")

    print("\nPlace names:")
    for _ in range(5):
        print(f"  {gen.place_name().full_name}")
