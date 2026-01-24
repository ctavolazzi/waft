#!/usr/bin/env python3
"""
D&D 5e Toolkit - Extracted from Dungeoneer VTT
Interactive encounter builder, CR calculator, and random generators.

Run: python -m waft.dnd_toolkit
"""

import json
import random
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Tuple

# ============================================================================
# CR CALCULATION TABLE (from DMG)
# ============================================================================

CR_TABLE = [
    {"cr": "0", "xp": 10, "min_hp": 1, "max_hp": 6, "prof": 2, "ac": 13, "min_dmg": 0, "max_dmg": 1, "save_dc": 13, "attack": 3},
    {"cr": "1/8", "xp": 25, "min_hp": 7, "max_hp": 35, "prof": 2, "ac": 13, "min_dmg": 2, "max_dmg": 3, "save_dc": 13, "attack": 3},
    {"cr": "1/4", "xp": 50, "min_hp": 36, "max_hp": 49, "prof": 2, "ac": 13, "min_dmg": 4, "max_dmg": 5, "save_dc": 13, "attack": 3},
    {"cr": "1/2", "xp": 100, "min_hp": 50, "max_hp": 70, "prof": 2, "ac": 13, "min_dmg": 6, "max_dmg": 8, "save_dc": 13, "attack": 3},
    {"cr": "1", "xp": 200, "min_hp": 71, "max_hp": 85, "prof": 2, "ac": 13, "min_dmg": 9, "max_dmg": 14, "save_dc": 13, "attack": 3},
    {"cr": "2", "xp": 450, "min_hp": 86, "max_hp": 100, "prof": 2, "ac": 13, "min_dmg": 15, "max_dmg": 20, "save_dc": 13, "attack": 3},
    {"cr": "3", "xp": 700, "min_hp": 101, "max_hp": 115, "prof": 2, "ac": 13, "min_dmg": 21, "max_dmg": 26, "save_dc": 13, "attack": 4},
    {"cr": "4", "xp": 1100, "min_hp": 116, "max_hp": 130, "prof": 2, "ac": 14, "min_dmg": 27, "max_dmg": 32, "save_dc": 14, "attack": 5},
    {"cr": "5", "xp": 1800, "min_hp": 131, "max_hp": 145, "prof": 3, "ac": 15, "min_dmg": 33, "max_dmg": 38, "save_dc": 15, "attack": 6},
    {"cr": "6", "xp": 2300, "min_hp": 146, "max_hp": 160, "prof": 3, "ac": 15, "min_dmg": 39, "max_dmg": 44, "save_dc": 15, "attack": 6},
    {"cr": "7", "xp": 2900, "min_hp": 161, "max_hp": 175, "prof": 3, "ac": 15, "min_dmg": 45, "max_dmg": 50, "save_dc": 15, "attack": 6},
    {"cr": "8", "xp": 3900, "min_hp": 176, "max_hp": 190, "prof": 3, "ac": 16, "min_dmg": 51, "max_dmg": 56, "save_dc": 16, "attack": 7},
    {"cr": "9", "xp": 5000, "min_hp": 191, "max_hp": 205, "prof": 4, "ac": 16, "min_dmg": 57, "max_dmg": 62, "save_dc": 16, "attack": 7},
    {"cr": "10", "xp": 5900, "min_hp": 206, "max_hp": 220, "prof": 4, "ac": 17, "min_dmg": 63, "max_dmg": 68, "save_dc": 16, "attack": 7},
    {"cr": "11", "xp": 7200, "min_hp": 221, "max_hp": 235, "prof": 4, "ac": 17, "min_dmg": 69, "max_dmg": 74, "save_dc": 17, "attack": 8},
    {"cr": "12", "xp": 8400, "min_hp": 236, "max_hp": 250, "prof": 4, "ac": 17, "min_dmg": 75, "max_dmg": 80, "save_dc": 17, "attack": 8},
    {"cr": "13", "xp": 10000, "min_hp": 251, "max_hp": 265, "prof": 5, "ac": 18, "min_dmg": 81, "max_dmg": 86, "save_dc": 18, "attack": 8},
    {"cr": "14", "xp": 11500, "min_hp": 266, "max_hp": 280, "prof": 5, "ac": 18, "min_dmg": 87, "max_dmg": 92, "save_dc": 18, "attack": 8},
    {"cr": "15", "xp": 13000, "min_hp": 281, "max_hp": 295, "prof": 5, "ac": 18, "min_dmg": 93, "max_dmg": 98, "save_dc": 18, "attack": 8},
    {"cr": "16", "xp": 15000, "min_hp": 296, "max_hp": 310, "prof": 5, "ac": 18, "min_dmg": 99, "max_dmg": 104, "save_dc": 18, "attack": 9},
    {"cr": "17", "xp": 18000, "min_hp": 311, "max_hp": 325, "prof": 6, "ac": 19, "min_dmg": 105, "max_dmg": 110, "save_dc": 19, "attack": 10},
    {"cr": "18", "xp": 20000, "min_hp": 326, "max_hp": 340, "prof": 6, "ac": 19, "min_dmg": 111, "max_dmg": 116, "save_dc": 19, "attack": 10},
    {"cr": "19", "xp": 22000, "min_hp": 341, "max_hp": 355, "prof": 6, "ac": 19, "min_dmg": 117, "max_dmg": 122, "save_dc": 19, "attack": 10},
    {"cr": "20", "xp": 25000, "min_hp": 356, "max_hp": 400, "prof": 6, "ac": 19, "min_dmg": 123, "max_dmg": 140, "save_dc": 19, "attack": 10},
    {"cr": "21", "xp": 33000, "min_hp": 401, "max_hp": 445, "prof": 7, "ac": 19, "min_dmg": 141, "max_dmg": 158, "save_dc": 20, "attack": 11},
    {"cr": "22", "xp": 41000, "min_hp": 446, "max_hp": 490, "prof": 7, "ac": 19, "min_dmg": 159, "max_dmg": 176, "save_dc": 20, "attack": 11},
    {"cr": "23", "xp": 50000, "min_hp": 491, "max_hp": 535, "prof": 7, "ac": 19, "min_dmg": 177, "max_dmg": 194, "save_dc": 20, "attack": 11},
    {"cr": "24", "xp": 62000, "min_hp": 536, "max_hp": 580, "prof": 7, "ac": 19, "min_dmg": 195, "max_dmg": 212, "save_dc": 21, "attack": 12},
    {"cr": "25", "xp": 75000, "min_hp": 581, "max_hp": 625, "prof": 8, "ac": 19, "min_dmg": 213, "max_dmg": 230, "save_dc": 21, "attack": 12},
    {"cr": "26", "xp": 90000, "min_hp": 626, "max_hp": 670, "prof": 8, "ac": 19, "min_dmg": 231, "max_dmg": 248, "save_dc": 21, "attack": 12},
    {"cr": "27", "xp": 105000, "min_hp": 671, "max_hp": 715, "prof": 8, "ac": 19, "min_dmg": 249, "max_dmg": 266, "save_dc": 22, "attack": 13},
    {"cr": "28", "xp": 120000, "min_hp": 716, "max_hp": 760, "prof": 8, "ac": 19, "min_dmg": 267, "max_dmg": 284, "save_dc": 22, "attack": 13},
    {"cr": "29", "xp": 135000, "min_hp": 761, "max_hp": 805, "prof": 9, "ac": 19, "min_dmg": 285, "max_dmg": 302, "save_dc": 22, "attack": 13},
    {"cr": "30", "xp": 155000, "min_hp": 806, "max_hp": 850, "prof": 9, "ac": 19, "min_dmg": 303, "max_dmg": 320, "save_dc": 23, "attack": 14},
]

# Encounter difficulty thresholds by player level [Easy, Medium, Hard, Deadly]
DIFFICULTY_BY_LEVEL = [
    [25, 50, 75, 100],      # Level 1
    [50, 100, 150, 200],    # Level 2
    [75, 150, 225, 400],    # Level 3
    [125, 250, 375, 500],   # Level 4
    [250, 500, 750, 1100],  # Level 5
    [300, 600, 900, 1400],  # Level 6
    [350, 750, 1100, 1700], # Level 7
    [450, 900, 1400, 2100], # Level 8
    [550, 1100, 1600, 2400],# Level 9
    [600, 1200, 1900, 2800],# Level 10
    [800, 1600, 2400, 3600],# Level 11
    [1000, 2000, 3000, 4500],# Level 12
    [1100, 2200, 3400, 5100],# Level 13
    [1250, 2500, 3800, 5700],# Level 14
    [1400, 2800, 4300, 6400],# Level 15
    [1600, 3200, 4800, 7200],# Level 16
    [2000, 3900, 5900, 8800],# Level 17
    [2100, 4200, 6300, 9500],# Level 18
    [2400, 4900, 7300, 10900],# Level 19
    [2800, 5700, 8500, 12700],# Level 20
]


def parse_cr(cr_str: str) -> float:
    """Convert CR string to float."""
    if cr_str == "1/8": return 0.125
    if cr_str == "1/4": return 0.25
    if cr_str == "1/2": return 0.5
    return float(cr_str)


def get_cr_entry(cr: str) -> dict:
    """Get CR table entry by CR string."""
    for entry in CR_TABLE:
        if entry["cr"] == cr:
            return entry
    return CR_TABLE[-1]


def get_xp_for_cr(cr: str) -> int:
    """Get XP value for a CR."""
    return get_cr_entry(cr)["xp"]


def calculate_cr(hp: int, ac: int, damage_per_round: int, attack_bonus: int = 0, save_dc: int = 0) -> dict:
    """Calculate CR from monster stats (DMG method)."""
    # Find defensive CR from HP
    def_cr_idx = 0
    for i, entry in enumerate(CR_TABLE):
        if entry["min_hp"] <= hp <= entry["max_hp"]:
            def_cr_idx = i
            break
        if hp > entry["max_hp"]:
            def_cr_idx = i

    # Adjust for AC
    expected_ac = CR_TABLE[def_cr_idx]["ac"]
    ac_diff = ac - expected_ac
    def_cr_idx = max(0, min(len(CR_TABLE)-1, def_cr_idx + (ac_diff // 2)))

    # Find offensive CR from damage
    off_cr_idx = 0
    for i, entry in enumerate(CR_TABLE):
        if entry["min_dmg"] <= damage_per_round <= entry["max_dmg"]:
            off_cr_idx = i
            break
        if damage_per_round > entry["max_dmg"]:
            off_cr_idx = i

    # Adjust for attack bonus (or save DC if higher)
    expected_attack = CR_TABLE[off_cr_idx]["attack"]
    use_save = save_dc > 0 and save_dc > attack_bonus + 5
    if use_save:
        expected_save = CR_TABLE[off_cr_idx]["save_dc"]
        atk_diff = save_dc - expected_save
    else:
        atk_diff = attack_bonus - expected_attack
    off_cr_idx = max(0, min(len(CR_TABLE)-1, off_cr_idx + (atk_diff // 2)))

    # Average offensive and defensive
    final_idx = (def_cr_idx + off_cr_idx) // 2

    return {
        "cr": CR_TABLE[final_idx]["cr"],
        "xp": CR_TABLE[final_idx]["xp"],
        "defensive_cr": CR_TABLE[def_cr_idx]["cr"],
        "offensive_cr": CR_TABLE[off_cr_idx]["cr"],
    }


def get_encounter_multiplier(monster_count: int, party_size: int) -> float:
    """Get XP multiplier based on monster count and party size."""
    multipliers = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0]

    if monster_count <= 1: idx = 0
    elif monster_count <= 2: idx = 1
    elif monster_count <= 6: idx = 2
    elif monster_count <= 10: idx = 3
    elif monster_count <= 14: idx = 4
    else: idx = 5

    # Adjust for party size
    if party_size <= 2 and idx < 5: idx += 1
    if party_size >= 6 and idx > 0: idx -= 1

    return multipliers[idx]


def calculate_encounter_difficulty(monster_crs: List[str], party_levels: List[int]) -> dict:
    """Calculate encounter difficulty."""
    if not party_levels:
        return {"error": "No party members"}

    # Calculate total XP
    base_xp = sum(get_xp_for_cr(cr) for cr in monster_crs)
    multiplier = get_encounter_multiplier(len(monster_crs), len(party_levels))
    adjusted_xp = int(base_xp * multiplier)

    # Calculate thresholds for party
    thresholds = [0, 0, 0, 0]  # Easy, Medium, Hard, Deadly
    for level in party_levels:
        level_idx = max(0, min(19, level - 1))
        for i in range(4):
            thresholds[i] += DIFFICULTY_BY_LEVEL[level_idx][i]

    # Determine difficulty
    if adjusted_xp < thresholds[0]:
        difficulty = "Trivial"
    elif adjusted_xp < thresholds[1]:
        difficulty = "Easy"
    elif adjusted_xp < thresholds[2]:
        difficulty = "Medium"
    elif adjusted_xp < thresholds[3]:
        difficulty = "Hard"
    else:
        ratio = adjusted_xp / thresholds[3]
        if ratio < 1.5:
            difficulty = "Deadly"
        else:
            difficulty = f"{ratio:.1f}x Deadly"

    return {
        "difficulty": difficulty,
        "base_xp": base_xp,
        "multiplier": multiplier,
        "adjusted_xp": adjusted_xp,
        "thresholds": {
            "easy": thresholds[0],
            "medium": thresholds[1],
            "hard": thresholds[2],
            "deadly": thresholds[3],
        }
    }


# ============================================================================
# MONSTER DATA (load from Dungeoneer)
# ============================================================================

def load_monsters() -> List[dict]:
    """Load monsters from Dungeoneer data."""
    monster_path = Path(__file__).parent.parent.parent.parent / "_external" / "dungeoneer" / "data" / "monsters.json"
    if monster_path.exists():
        with open(monster_path) as f:
            return json.load(f)
    return []


def search_monsters(query: str, monsters: List[dict] = None) -> List[dict]:
    """Search monsters by name or type."""
    if monsters is None:
        monsters = load_monsters()
    query = query.lower()
    return [m for m in monsters if query in m.get("name", "").lower() or query in m.get("type", "").lower()]


def random_monster(cr: str = None, monster_type: str = None, monsters: List[dict] = None) -> Optional[dict]:
    """Get a random monster, optionally filtered."""
    if monsters is None:
        monsters = load_monsters()

    filtered = monsters
    if cr:
        filtered = [m for m in filtered if m.get("challenge_rating") == cr]
    if monster_type:
        filtered = [m for m in filtered if monster_type.lower() in m.get("type", "").lower()]

    return random.choice(filtered) if filtered else None


# ============================================================================
# TAVERN GENERATOR
# ============================================================================

TAVERN_ADJECTIVES = ["Prancing", "Golden", "Silver", "Rusty", "Broken", "Dancing", "Laughing", "Sleeping", "Winking", "Roaring", "Crimson", "Azure", "Emerald", "Shadowy", "Gilded"]
TAVERN_NOUNS = ["Pony", "Dragon", "Griffin", "Stag", "Boar", "Serpent", "Phoenix", "Raven", "Wolf", "Bear", "Lion", "Mermaid", "Goblin", "Knight", "Wizard"]
TAVERN_TYPES = ["Inn", "Tavern", "Alehouse", "Pub", "Lodge", "Rest", "House", "Hall", "Den", "Retreat"]

TAVERN_LOCATIONS = [
    "on the main road through town",
    "in a quiet corner of the market district",
    "near the city gates",
    "by the river docks",
    "in the shadow of the castle walls",
    "at the crossroads outside town",
    "in the merchant quarter",
    "down a narrow alley",
]

TAVERN_INTERIORS = {
    "poor": ["cramped and smoky", "dimly lit with a dirt floor", "simple and rough-hewn"],
    "modest": ["warm and inviting", "well-kept if simple", "cozy with worn furniture"],
    "wealthy": ["elegantly appointed", "spacious with fine woodwork", "luxuriously decorated"],
}

MENU_ITEMS = {
    "poor": ["watery stew", "hard bread", "mystery meat pie", "boiled vegetables"],
    "modest": ["roast chicken", "meat pie", "cheese and bread", "fish stew", "vegetable soup"],
    "wealthy": ["roast pheasant", "venison steak", "lobster tail", "fine cheese platter", "imported wine"],
}

DRINKS = {
    "poor": ["watered ale", "cheap wine", "cider"],
    "modest": ["local ale", "house wine", "mead", "cider"],
    "wealthy": ["dwarven stout", "elven wine", "aged whiskey", "imported spirits"],
}

RUMORS = [
    "They say the old mill is haunted by the ghost of the miller",
    "A merchant caravan went missing on the north road last week",
    "The baron's daughter has been acting strange since the new moon",
    "Someone's been stealing sheep from the farms outside town",
    "A stranger in a black cloak has been asking questions about the temple",
    "The well in the town square has started giving bitter water",
    "Goblins have been spotted in the forest to the east",
    "The blacksmith found a strange medallion in his forge this morning",
    "A traveling bard claims to have seen a dragon flying over the mountains",
    "The mayor is looking to hire adventurers for a 'discrete matter'",
]


def generate_tavern(wealth: str = "modest") -> dict:
    """Generate a random tavern."""
    name = f"The {random.choice(TAVERN_ADJECTIVES)} {random.choice(TAVERN_NOUNS)} {random.choice(TAVERN_TYPES)}"

    menu = []
    for item in random.sample(MENU_ITEMS[wealth], min(3, len(MENU_ITEMS[wealth]))):
        price = {"poor": "1-3 cp", "modest": "5-15 cp", "wealthy": "1-5 sp"}[wealth]
        menu.append({"item": item, "price": price})

    for drink in random.sample(DRINKS[wealth], min(2, len(DRINKS[wealth]))):
        price = {"poor": "1 cp", "modest": "2-5 cp", "wealthy": "5-20 cp"}[wealth]
        menu.append({"item": drink, "price": price})

    return {
        "name": name,
        "location": random.choice(TAVERN_LOCATIONS),
        "interior": random.choice(TAVERN_INTERIORS[wealth]),
        "wealth": wealth,
        "menu": menu,
        "rumors": random.sample(RUMORS, min(3, len(RUMORS))),
    }


# ============================================================================
# INTERACTIVE CLI
# ============================================================================

def print_header(text: str):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_monster(m: dict):
    """Pretty print a monster."""
    print(f"\n  {m['name']} (CR {m.get('challenge_rating', '?')})")
    print(f"  {m.get('size', '?')} {m.get('type', '?')}, {m.get('alignment', '?')}")
    print(f"  AC: {m.get('armor_class', '?')}  HP: {m.get('hit_points', '?')} ({m.get('hit_dice', '?')})")
    print(f"  Speed: {m.get('speed', '?')}")
    print(f"  STR {m.get('strength', '?')} DEX {m.get('dexterity', '?')} CON {m.get('constitution', '?')}")
    print(f"  INT {m.get('intelligence', '?')} WIS {m.get('wisdom', '?')} CHA {m.get('charisma', '?')}")


def interactive_cli():
    """Run interactive CLI."""
    monsters = load_monsters()
    print_header("D&D 5e Toolkit")
    print(f"  Loaded {len(monsters)} monsters from Dungeoneer")

    party_levels = [5, 5, 5, 5]  # Default party

    while True:
        print("\n  Commands:")
        print("  [1] Calculate Encounter Difficulty")
        print("  [2] Calculate CR from Stats")
        print("  [3] Search Monsters")
        print("  [4] Random Monster")
        print("  [5] Generate Tavern")
        print("  [6] Set Party Levels")
        print("  [7] Quick Encounter Builder")
        print("  [q] Quit")
        print(f"\n  Current Party: {party_levels}")

        choice = input("\n  > ").strip().lower()

        if choice == 'q':
            print("\n  Farewell, adventurer!\n")
            break

        elif choice == '1':
            print_header("Encounter Difficulty Calculator")
            print("  Enter monster CRs (comma-separated, e.g. '3,3,1,1'):")
            cr_input = input("  > ").strip()
            if cr_input:
                crs = [c.strip() for c in cr_input.split(",")]
                result = calculate_encounter_difficulty(crs, party_levels)
                print(f"\n  Difficulty: {result['difficulty']}")
                print(f"  Base XP: {result['base_xp']}")
                print(f"  Multiplier: {result['multiplier']}x")
                print(f"  Adjusted XP: {result['adjusted_xp']}")
                print(f"\n  Thresholds for party:")
                for diff, val in result['thresholds'].items():
                    print(f"    {diff.capitalize()}: {val} XP")

        elif choice == '2':
            print_header("CR Calculator")
            try:
                hp = int(input("  HP: ").strip())
                ac = int(input("  AC: ").strip())
                dmg = int(input("  Damage per round: ").strip())
                atk = int(input("  Attack bonus (0 if none): ").strip() or "0")
                save = int(input("  Save DC (0 if none): ").strip() or "0")

                result = calculate_cr(hp, ac, dmg, atk, save)
                print(f"\n  Calculated CR: {result['cr']} ({result['xp']} XP)")
                print(f"  Defensive CR: {result['defensive_cr']}")
                print(f"  Offensive CR: {result['offensive_cr']}")
            except ValueError:
                print("  Invalid input!")

        elif choice == '3':
            print_header("Monster Search")
            query = input("  Search term: ").strip()
            if query:
                results = search_monsters(query, monsters)[:10]
                if results:
                    for m in results:
                        print(f"  - {m['name']} (CR {m.get('challenge_rating', '?')}, {m.get('type', '?')})")
                else:
                    print("  No monsters found.")

        elif choice == '4':
            print_header("Random Monster")
            cr = input("  Filter by CR (blank for any): ").strip() or None
            m = random_monster(cr=cr, monsters=monsters)
            if m:
                print_monster(m)
            else:
                print("  No monster found for that CR.")

        elif choice == '5':
            print_header("Tavern Generator")
            wealth = input("  Wealth level (poor/modest/wealthy): ").strip().lower() or "modest"
            if wealth not in ["poor", "modest", "wealthy"]:
                wealth = "modest"
            tavern = generate_tavern(wealth)
            print(f"\n  {tavern['name']}")
            print(f"  Located {tavern['location']}")
            print(f"  Interior: {tavern['interior']}")
            print("\n  Menu:")
            for item in tavern['menu']:
                print(f"    - {item['item']}: {item['price']}")
            print("\n  Rumors overheard:")
            for i, rumor in enumerate(tavern['rumors'], 1):
                print(f"    {i}. \"{rumor}\"")

        elif choice == '6':
            print_header("Set Party Levels")
            print("  Enter party levels (comma-separated, e.g. '5,5,4,4'):")
            level_input = input("  > ").strip()
            if level_input:
                try:
                    party_levels = [int(l.strip()) for l in level_input.split(",")]
                    print(f"  Party set to: {party_levels}")
                except ValueError:
                    print("  Invalid input!")

        elif choice == '7':
            print_header("Quick Encounter Builder")
            print("  Target difficulty (easy/medium/hard/deadly):")
            difficulty = input("  > ").strip().lower() or "medium"

            # Calculate budget
            diff_idx = {"easy": 0, "medium": 1, "hard": 2, "deadly": 3}.get(difficulty, 1)
            budget = sum(DIFFICULTY_BY_LEVEL[max(0, min(19, l-1))][diff_idx] for l in party_levels)

            print(f"\n  XP Budget: {budget}")
            print("  Building encounter...")

            # Pick random monsters that fit
            encounter = []
            remaining = budget
            attempts = 0
            while remaining > 25 and attempts < 50:
                available = [m for m in monsters if get_xp_for_cr(m.get("challenge_rating", "0")) <= remaining]
                if not available:
                    break
                m = random.choice(available)
                xp = get_xp_for_cr(m.get("challenge_rating", "0"))
                encounter.append(m)
                multiplier = get_encounter_multiplier(len(encounter), len(party_levels))
                remaining = budget - int(sum(get_xp_for_cr(e.get("challenge_rating", "0")) for e in encounter) * multiplier)
                attempts += 1

            print("\n  Generated Encounter:")
            for m in encounter:
                print(f"    - {m['name']} (CR {m.get('challenge_rating', '?')})")

            crs = [m.get("challenge_rating", "0") for m in encounter]
            result = calculate_encounter_difficulty(crs, party_levels)
            print(f"\n  Final Difficulty: {result['difficulty']} ({result['adjusted_xp']} XP)")


if __name__ == "__main__":
    interactive_cli()
