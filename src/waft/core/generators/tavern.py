"""
Tavern Generator - Complete Tavern Environments
===============================================

Generates complete taverns like Eigengrau's Generator:
- Name and type
- Staff (bartender, cook, barmaid)
- Patrons (3-6 NPCs with secrets)
- Menu (drinks, food with prices)
- Rumors (plot hooks)
- Atmosphere description
"""

import random
from dataclasses import dataclass, field

from .names import NameGenerator
from .npcs import NPCGenerator, NPC, Occupation


# Tavern types with associated moods
TAVERN_TYPES = {
    "dive_bar": {
        "description": "a rough dive bar frequented by criminals and outcasts",
        "mood": "dangerous",
        "price_modifier": 0.5,
        "typical_patrons": ["thief", "smuggler", "gambler", "mercenary"],
    },
    "adventurers_guild": {
        "description": "a popular gathering spot for adventurers seeking quests",
        "mood": "lively",
        "price_modifier": 1.2,
        "typical_patrons": ["adventurer", "mercenary", "treasure hunter", "retired soldier"],
    },
    "upscale_inn": {
        "description": "a refined establishment catering to wealthy travelers",
        "mood": "sophisticated",
        "price_modifier": 3.0,
        "typical_patrons": ["merchant", "noble", "diplomat", "scholar"],
    },
    "village_tavern": {
        "description": "a cozy local tavern where everyone knows each other",
        "mood": "warm",
        "price_modifier": 0.8,
        "typical_patrons": ["farmer", "craftsman", "hunter", "traveler"],
    },
    "dockside_pub": {
        "description": "a rowdy pub near the harbor, full of sailors and traders",
        "mood": "boisterous",
        "price_modifier": 0.9,
        "typical_patrons": ["sailor", "merchant", "smuggler", "adventurer"],
    },
    "mysterious_inn": {
        "description": "an enigmatic establishment with an unusual clientele",
        "mood": "mysterious",
        "price_modifier": 1.5,
        "typical_patrons": ["wizard", "spy", "stranger", "pilgrim"],
    },
}

# Menu items with base prices (in copper)
DRINKS = [
    ("Ale", 4, "A hearty local brew"),
    ("Mead", 8, "Sweet honey wine"),
    ("Wine (common)", 10, "Passable table wine"),
    ("Wine (fine)", 50, "Excellent vintage from distant vineyards"),
    ("Whiskey", 15, "Burns going down, warms the soul"),
    ("Cider", 5, "Crisp apple cider"),
    ("Grog", 3, "Sailor's special - rum and water"),
    ("Milk", 2, "Fresh from the farm"),
    ("Tea", 3, "Calming herbal blend"),
    ("Mystery Special", 20, "The bartender's secret recipe - different every night"),
]

FOOD = [
    ("Bread and cheese", 5, "Simple but filling"),
    ("Meat pie", 15, "Flaky crust, mystery meat"),
    ("Stew (bowl)", 10, "Whatever was available, slow-cooked"),
    ("Roast chicken", 25, "Half a bird, nicely seasoned"),
    ("Fish and chips", 12, "Freshly fried"),
    ("Vegetable soup", 8, "Hearty and warming"),
    ("Traveler's rations", 20, "Dried meat, hardtack, and dried fruit"),
    ("Feast platter", 100, "Everything on the menu, serves 4"),
    ("Shepherd's pie", 18, "Meat and vegetables under mashed potatoes"),
    ("Exotic dish", 40, "Foreign spices and unusual ingredients"),
]

# Atmosphere elements
SOUNDS = [
    "a bard strumming a melancholy tune",
    "raucous laughter from a corner table",
    "dice clattering on wood",
    "hushed whispers at the bar",
    "a crackling fireplace",
    "rain pattering on the windows",
    "glasses clinking in toast",
    "someone snoring in the corner",
    "an argument brewing at a nearby table",
    "a dog begging for scraps",
]

SMELLS = [
    "roasting meat", "spilled ale", "woodsmoke", "pipe tobacco",
    "fresh bread", "something burning in the kitchen", "sea salt",
    "cheap perfume", "wet dog", "exotic spices",
]

SIGHTS = [
    "a mounted monster head over the fireplace",
    "wanted posters on the wall",
    "a dusty chandelier",
    "a mysterious painting that seems to watch you",
    "a board covered in quest notices",
    "weapons hung behind the bar",
    "a half-played chess game on a table",
    "a cat sleeping on the windowsill",
    "strange symbols carved into the wooden beams",
    "an old map pinned to the wall",
]

# Rumors - plot hooks heard at the bar
RUMORS = [
    "Strange lights have been seen at the old mill every night for a week.",
    "The baron's daughter has gone missing, and he's paying handsomely for her return.",
    "They say the graveyard keeper has been seen digging at midnight.",
    "A merchant caravan was attacked on the north road. No survivors.",
    "The local witch was spotted near the standing stones during the full moon.",
    "An ancient tomb was uncovered by the recent earthquake.",
    "Pirates have been spotted off the coast, flying colors no one recognizes.",
    "The blacksmith's apprentice found gold in the river.",
    "Something large has been killing livestock on farms to the east.",
    "A stranger arrived last week and hasn't left his room at the inn.",
    "The king's tax collectors are coming, and they're not happy about the shortage.",
    "There's a bounty on a notorious bandit who was last seen in this area.",
    "The temple priests have stopped answering prayers since the new moon.",
    "A traveling scholar is paying for information about local legends.",
    "The mines have been closed - something attacked the workers.",
    "An old map surfaced showing a hidden entrance to the castle dungeons.",
    "The ferryman refuses to cross the river after dark anymore.",
    "A noble is secretly hiring sellswords for an unnamed job.",
    "The herbalist has been buying unusual ingredients - nightshade and grave moss.",
    "Someone broke into the archives and stole only one document.",
]


@dataclass
class MenuItem:
    """A menu item with price."""
    name: str
    price: int  # in copper
    description: str

    def to_dict(self) -> dict:
        return {"name": self.name, "price": self.price, "description": self.description}


@dataclass
class Tavern:
    """A complete tavern environment."""
    name: str
    tavern_type: str
    type_description: str
    mood: str

    # People
    staff: list[NPC] = field(default_factory=list)
    patrons: list[NPC] = field(default_factory=list)

    # Menu
    drinks: list[MenuItem] = field(default_factory=list)
    food: list[MenuItem] = field(default_factory=list)

    # Atmosphere
    sounds: list[str] = field(default_factory=list)
    smells: list[str] = field(default_factory=list)
    sights: list[str] = field(default_factory=list)

    # Plot hooks
    rumors: list[str] = field(default_factory=list)

    def description(self) -> str:
        """Generate a prose description of the tavern."""
        bartender = next((s for s in self.staff if s.occupation == "bartender"), None)
        bartender_desc = f"The bartender, **{bartender.name}**, a {bartender.race}," if bartender else "The bartender"

        patron_count = len(self.patrons)
        crowd = "nearly empty" if patron_count < 2 else "moderately busy" if patron_count < 4 else "crowded"

        sight = self.sights[0] if self.sights else "worn wooden tables"
        sound = self.sounds[0] if self.sounds else "quiet conversation"
        smell = self.smells[0] if self.smells else "ale"

        return (
            f"**{self.name}** is {self.type_description}. "
            f"The place is {crowd} tonight. "
            f"You notice {sight}. "
            f"The air carries the scent of {smell}, "
            f"and you hear {sound}. "
            f"{bartender_desc} catches your eye."
        )

    def storyteller_context(self) -> dict:
        """Rich context for the AI storyteller."""
        return {
            "name": self.name,
            "type": self.tavern_type,
            "description": self.description(),
            "mood": self.mood,
            "staff": [s.storyteller_context() for s in self.staff],
            "patrons": [p.storyteller_context() for p in self.patrons],
            "atmosphere": {
                "sounds": self.sounds,
                "smells": self.smells,
                "sights": self.sights,
            },
            "rumors": self.rumors,
            "menu": {
                "drinks": [d.to_dict() for d in self.drinks],
                "food": [f.to_dict() for f in self.food],
            },
        }

    def get_npcs_by_name(self) -> dict[str, NPC]:
        """Get all NPCs indexed by name."""
        result = {}
        for npc in self.staff + self.patrons:
            result[npc.name] = npc
        return result


class TavernGenerator:
    """Generates complete tavern environments."""

    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)
        self.name_gen = NameGenerator(seed)
        self.npc_gen = NPCGenerator(seed)

    def generate(
        self,
        tavern_type: str | None = None,
        num_patrons: int | None = None,
        num_rumors: int = 3,
    ) -> Tavern:
        """Generate a complete tavern."""

        # Choose type
        if tavern_type is None:
            tavern_type = self.rng.choice(list(TAVERN_TYPES.keys()))

        type_info = TAVERN_TYPES.get(tavern_type, TAVERN_TYPES["village_tavern"])

        # Generate name
        name = self.name_gen.tavern_name().full_name

        # Generate staff
        staff = self._generate_staff()

        # Generate patrons
        if num_patrons is None:
            num_patrons = self.rng.randint(3, 6)

        patrons = self._generate_patrons(num_patrons, type_info["typical_patrons"])

        # Generate menu with price modifier
        price_mod = type_info["price_modifier"]
        drinks = self._generate_menu(DRINKS, price_mod, count=self.rng.randint(4, 7))
        food = self._generate_menu(FOOD, price_mod, count=self.rng.randint(4, 6))

        # Atmosphere
        sounds = self.rng.sample(SOUNDS, k=self.rng.randint(2, 3))
        smells = self.rng.sample(SMELLS, k=self.rng.randint(2, 3))
        sights = self.rng.sample(SIGHTS, k=self.rng.randint(2, 3))

        # Rumors
        rumors = self.rng.sample(RUMORS, k=min(num_rumors, len(RUMORS)))

        return Tavern(
            name=name,
            tavern_type=tavern_type,
            type_description=type_info["description"],
            mood=type_info["mood"],
            staff=staff,
            patrons=patrons,
            drinks=drinks,
            food=food,
            sounds=sounds,
            smells=smells,
            sights=sights,
            rumors=rumors,
        )

    def _generate_staff(self) -> list[NPC]:
        """Generate tavern staff."""
        staff = []

        # Always have a bartender
        bartender = self.npc_gen.generate_staff(Occupation.BARTENDER)
        # Give bartender distinctive traits
        bartender.personality_traits = ["gruff but fair"] + bartender.personality_traits[:2]
        staff.append(bartender)

        # Usually have a barmaid/server
        if self.rng.random() < 0.8:
            server = self.npc_gen.generate_staff(Occupation.BARMAID)
            staff.append(server)

        # Sometimes have a cook
        if self.rng.random() < 0.5:
            cook = self.npc_gen.generate_staff(Occupation.COOK)
            staff.append(cook)

        # Rarely have a bouncer
        if self.rng.random() < 0.3:
            bouncer = self.npc_gen.generate_staff(Occupation.BOUNCER)
            bouncer.personality_traits = ["intimidating"] + bouncer.personality_traits[:2]
            staff.append(bouncer)

        return staff

    def _generate_patrons(self, count: int, typical_types: list[str]) -> list[NPC]:
        """Generate tavern patrons."""
        patrons = []

        for _ in range(count):
            # 70% chance of typical patron, 30% random
            if self.rng.random() < 0.7:
                occupation = self.rng.choice(typical_types)
            else:
                occupation = None

            # 20% chance of mysterious patron
            mysterious = self.rng.random() < 0.2
            patron = self.npc_gen.generate_patron(mysterious=mysterious)

            if occupation:
                patron.occupation = occupation

            patrons.append(patron)

        # Make one patron the "obvious hook" - more interesting
        if patrons:
            hook_patron = self.rng.choice(patrons)
            hook_patron.personality_traits = ["nervous", "looking around"] + hook_patron.personality_traits[:1]
            hook_patron.distinguishing_mark = "keeps glancing at the door"

        return patrons

    def _generate_menu(
        self, items: list[tuple], price_mod: float, count: int
    ) -> list[MenuItem]:
        """Generate menu items with adjusted prices."""
        selected = self.rng.sample(items, k=min(count, len(items)))
        return [
            MenuItem(
                name=name,
                price=int(base_price * price_mod),
                description=desc
            )
            for name, base_price, desc in selected
        ]


# Convenience function
def generate_tavern(tavern_type: str | None = None, seed: int | None = None) -> Tavern:
    """Quick tavern generation."""
    return TavernGenerator(seed).generate(tavern_type=tavern_type)


if __name__ == "__main__":
    # Demo
    gen = TavernGenerator(seed=42)
    print("=== Tavern Generator Demo ===\n")

    tavern = gen.generate()
    print(tavern.description())

    print("\n--- Staff ---")
    for npc in tavern.staff:
        print(f"  {npc.short_description()}")

    print("\n--- Patrons ---")
    for npc in tavern.patrons:
        print(f"  {npc.short_description()}")
        if npc.hook:
            print(f"      Hook: {npc.hook}")

    print("\n--- Menu ---")
    print("  Drinks:")
    for item in tavern.drinks[:3]:
        print(f"    {item.name}: {item.price}cp - {item.description}")
    print("  Food:")
    for item in tavern.food[:3]:
        print(f"    {item.name}: {item.price}cp - {item.description}")

    print("\n--- Rumors ---")
    for rumor in tavern.rumors:
        print(f"  • {rumor}")

    print("\n--- Atmosphere ---")
    print(f"  Sounds: {', '.join(tavern.sounds)}")
    print(f"  Smells: {', '.join(tavern.smells)}")
    print(f"  Sights: {', '.join(tavern.sights)}")
