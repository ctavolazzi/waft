"""
Generate D&D 5e Character Sheet PDFs
====================================

Creates both blank and filled D&D 5e character sheet PDFs using the PDF generator.
Supports standard D&D 5e character sheet format with all standard fields.
"""

import sys
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.waft.evolution.pdf_generator import PDFGenerator


def create_blank_character_sheet_content() -> str:
    """Create markdown content for a blank D&D 5e character sheet."""
    return """# D&D 5e Character Sheet

## Character Information

**Name:** _________________  
**Class & Level:** _________________  
**Background:** _________________  
**Player Name:** _________________  
**Race:** _________________  
**Alignment:** _________________  
**Experience Points:** _________________

---

## Ability Scores

| Ability | Score | Modifier | Saving Throw | Proficiency |
|---------|-------|----------|--------------|-------------|
| **Strength** | ___ | ___ | ☐ ___ | ☐ |
| **Dexterity** | ___ | ___ | ☐ ___ | ☐ |
| **Constitution** | ___ | ___ | ☐ ___ | ☐ |
| **Intelligence** | ___ | ___ | ☐ ___ | ☐ |
| **Wisdom** | ___ | ___ | ☐ ___ | ☐ |
| **Charisma** | ___ | ___ | ☐ ___ | ☐ |

**Proficiency Bonus:** +___

---

## Skills

| Skill | Ability | Modifier | Proficiency |
|-------|---------|----------|-------------|
| **Acrobatics** | DEX | ___ | ☐ |
| **Animal Handling** | WIS | ___ | ☐ |
| **Arcana** | INT | ___ | ☐ |
| **Athletics** | STR | ___ | ☐ |
| **Deception** | CHA | ___ | ☐ |
| **History** | INT | ___ | ☐ |
| **Insight** | WIS | ___ | ☐ |
| **Intimidation** | CHA | ___ | ☐ |
| **Investigation** | INT | ___ | ☐ |
| **Medicine** | WIS | ___ | ☐ |
| **Nature** | INT | ___ | ☐ |
| **Perception** | WIS | ___ | ☐ |
| **Performance** | CHA | ___ | ☐ |
| **Persuasion** | CHA | ___ | ☐ |
| **Religion** | INT | ___ | ☐ |
| **Sleight of Hand** | DEX | ___ | ☐ |
| **Stealth** | DEX | ___ | ☐ |
| **Survival** | WIS | ___ | ☐ |

---

## Combat

**Armor Class (AC):** ___  
**Initiative:** ___  
**Speed:** ___ ft.

**Hit Points**
- **Maximum:** ___
- **Current:** ___
- **Temporary:** ___

**Hit Dice**
- **Total:** ___
- **Used:** ___

**Death Saves**
- **Successes:** ☐ ☐ ☐
- **Failures:** ☐ ☐ ☐

---

## Attacks & Spellcasting

### Attacks

| Weapon/Spell | Attack Bonus | Damage/Type | Range |
|--------------|--------------|-------------|-------|
| _____________ | +___ | _____________ | _____ |
| _____________ | +___ | _____________ | _____ |
| _____________ | +___ | _____________ | _____ |

---

## Equipment

**Coins:**
- **Platinum:** ___
- **Gold:** ___
- **Electrum:** ___
- **Silver:** ___
- **Copper:** ___

**Equipment & Items:**

_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

## Features & Traits

**Class Features:**

_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

**Racial Traits:**

_________________________________________________________________
_________________________________________________________________

**Feats:**

_________________________________________________________________
_________________________________________________________________

**Other Features & Traits:**

_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

## Proficiencies & Languages

**Armor Proficiencies:** _________________________________________

**Weapon Proficiencies:** ________________________________________

**Tool Proficiencies:** __________________________________________

**Languages:** ___________________________________________________

---

## Personality

**Personality Traits:**

_________________________________________________________________
_________________________________________________________________

**Ideals:**

_________________________________________________________________

**Bonds:**

_________________________________________________________________

**Flaws:**

_________________________________________________________________

---

## Backstory

_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

## Notes

_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

*D&D 5e Character Sheet - Blank Template*
"""


def create_filled_character_sheet_content(character_data: dict[str, Any]) -> str:
    """Create markdown content for a filled D&D 5e character sheet."""

    # Extract character data with defaults
    name = character_data.get("name", "Adventurer")
    char_class = character_data.get("class", "Fighter")
    level = character_data.get("level", 1)
    background = character_data.get("background", "Folk Hero")
    race = character_data.get("race", "Human")
    alignment = character_data.get("alignment", "Neutral Good")
    xp = character_data.get("xp", 0)

    # Ability scores
    abilities = character_data.get(
        "abilities", {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
    )

    proficiency_bonus = character_data.get("proficiency_bonus", 2)

    # Calculate modifiers
    def calc_mod(score):
        return (score - 10) // 2

    # Skills proficiency
    skill_proficiencies = character_data.get("skill_proficiencies", [])

    # Combat stats
    ac = character_data.get("ac", 10)
    initiative = character_data.get("initiative", 0)
    speed = character_data.get("speed", 30)
    max_hp = character_data.get("max_hp", 10)
    current_hp = character_data.get("current_hp", max_hp)
    temp_hp = character_data.get("temp_hp", 0)
    hit_dice = character_data.get("hit_dice", "1d10")

    # Attacks
    attacks = character_data.get("attacks", [])

    # Equipment
    equipment = character_data.get("equipment", [])
    coins = character_data.get("coins", {"pp": 0, "gp": 0, "ep": 0, "sp": 0, "cp": 0})

    # Features
    features = character_data.get("features", [])
    traits = character_data.get("traits", [])

    # Proficiencies
    armor_prof = character_data.get("armor_proficiencies", [])
    weapon_prof = character_data.get("weapon_proficiencies", [])
    tool_prof = character_data.get("tool_proficiencies", [])
    languages = character_data.get("languages", ["Common"])

    # Personality
    personality = character_data.get("personality_traits", [])
    ideals = character_data.get("ideals", [])
    bonds = character_data.get("bonds", [])
    flaws = character_data.get("flaws", [])

    # Backstory
    backstory = character_data.get("backstory", "")

    # Build content
    content = f"""# D&D 5e Character Sheet

## Character Information

**Name:** {name}  
**Class & Level:** {char_class} {level}  
**Background:** {background}  
**Player Name:** _________________  
**Race:** {race}  
**Alignment:** {alignment}  
**Experience Points:** {xp}

---

## Ability Scores

| Ability | Score | Modifier | Saving Throw | Proficiency |
|---------|-------|----------|--------------|-------------|
| **Strength** | {abilities.get("STR", 10)} | {calc_mod(abilities.get("STR", 10)):+d} | {calc_mod(abilities.get("STR", 10)) + (proficiency_bonus if "STR" in character_data.get("saving_throw_proficiencies", []) else 0):+d} | {"✓" if "STR" in character_data.get("saving_throw_proficiencies", []) else ""} |
| **Dexterity** | {abilities.get("DEX", 10)} | {calc_mod(abilities.get("DEX", 10)):+d} | {calc_mod(abilities.get("DEX", 10)) + (proficiency_bonus if "DEX" in character_data.get("saving_throw_proficiencies", []) else 0):+d} | {"✓" if "DEX" in character_data.get("saving_throw_proficiencies", []) else ""} |
| **Constitution** | {abilities.get("CON", 10)} | {calc_mod(abilities.get("CON", 10)):+d} | {calc_mod(abilities.get("CON", 10)) + (proficiency_bonus if "CON" in character_data.get("saving_throw_proficiencies", []) else 0):+d} | {"✓" if "CON" in character_data.get("saving_throw_proficiencies", []) else ""} |
| **Intelligence** | {abilities.get("INT", 10)} | {calc_mod(abilities.get("INT", 10)):+d} | {calc_mod(abilities.get("INT", 10)) + (proficiency_bonus if "INT" in character_data.get("saving_throw_proficiencies", []) else 0):+d} | {"✓" if "INT" in character_data.get("saving_throw_proficiencies", []) else ""} |
| **Wisdom** | {abilities.get("WIS", 10)} | {calc_mod(abilities.get("WIS", 10)):+d} | {calc_mod(abilities.get("WIS", 10)) + (proficiency_bonus if "WIS" in character_data.get("saving_throw_proficiencies", []) else 0):+d} | {"✓" if "WIS" in character_data.get("saving_throw_proficiencies", []) else ""} |
| **Charisma** | {abilities.get("CHA", 10)} | {calc_mod(abilities.get("CHA", 10)):+d} | {calc_mod(abilities.get("CHA", 10)) + (proficiency_bonus if "CHA" in character_data.get("saving_throw_proficiencies", []) else 0):+d} | {"✓" if "CHA" in character_data.get("saving_throw_proficiencies", []) else ""} |

**Proficiency Bonus:** +{proficiency_bonus}

---

## Skills

| Skill | Ability | Modifier | Proficiency |
|-------|---------|----------|-------------|
| **Acrobatics** | DEX | {calc_mod(abilities.get("DEX", 10)) + (proficiency_bonus if "Acrobatics" in skill_proficiencies else 0):+d} | {"✓" if "Acrobatics" in skill_proficiencies else ""} |
| **Animal Handling** | WIS | {calc_mod(abilities.get("WIS", 10)) + (proficiency_bonus if "Animal Handling" in skill_proficiencies else 0):+d} | {"✓" if "Animal Handling" in skill_proficiencies else ""} |
| **Arcana** | INT | {calc_mod(abilities.get("INT", 10)) + (proficiency_bonus if "Arcana" in skill_proficiencies else 0):+d} | {"✓" if "Arcana" in skill_proficiencies else ""} |
| **Athletics** | STR | {calc_mod(abilities.get("STR", 10)) + (proficiency_bonus if "Athletics" in skill_proficiencies else 0):+d} | {"✓" if "Athletics" in skill_proficiencies else ""} |
| **Deception** | CHA | {calc_mod(abilities.get("CHA", 10)) + (proficiency_bonus if "Deception" in skill_proficiencies else 0):+d} | {"✓" if "Deception" in skill_proficiencies else ""} |
| **History** | INT | {calc_mod(abilities.get("INT", 10)) + (proficiency_bonus if "History" in skill_proficiencies else 0):+d} | {"✓" if "History" in skill_proficiencies else ""} |
| **Insight** | WIS | {calc_mod(abilities.get("WIS", 10)) + (proficiency_bonus if "Insight" in skill_proficiencies else 0):+d} | {"✓" if "Insight" in skill_proficiencies else ""} |
| **Intimidation** | CHA | {calc_mod(abilities.get("CHA", 10)) + (proficiency_bonus if "Intimidation" in skill_proficiencies else 0):+d} | {"✓" if "Intimidation" in skill_proficiencies else ""} |
| **Investigation** | INT | {calc_mod(abilities.get("INT", 10)) + (proficiency_bonus if "Investigation" in skill_proficiencies else 0):+d} | {"✓" if "Investigation" in skill_proficiencies else ""} |
| **Medicine** | WIS | {calc_mod(abilities.get("WIS", 10)) + (proficiency_bonus if "Medicine" in skill_proficiencies else 0):+d} | {"✓" if "Medicine" in skill_proficiencies else ""} |
| **Nature** | INT | {calc_mod(abilities.get("INT", 10)) + (proficiency_bonus if "Nature" in skill_proficiencies else 0):+d} | {"✓" if "Nature" in skill_proficiencies else ""} |
| **Perception** | WIS | {calc_mod(abilities.get("WIS", 10)) + (proficiency_bonus if "Perception" in skill_proficiencies else 0):+d} | {"✓" if "Perception" in skill_proficiencies else ""} |
| **Performance** | CHA | {calc_mod(abilities.get("CHA", 10)) + (proficiency_bonus if "Performance" in skill_proficiencies else 0):+d} | {"✓" if "Performance" in skill_proficiencies else ""} |
| **Persuasion** | CHA | {calc_mod(abilities.get("CHA", 10)) + (proficiency_bonus if "Persuasion" in skill_proficiencies else 0):+d} | {"✓" if "Persuasion" in skill_proficiencies else ""} |
| **Religion** | INT | {calc_mod(abilities.get("INT", 10)) + (proficiency_bonus if "Religion" in skill_proficiencies else 0):+d} | {"✓" if "Religion" in skill_proficiencies else ""} |
| **Sleight of Hand** | DEX | {calc_mod(abilities.get("DEX", 10)) + (proficiency_bonus if "Sleight of Hand" in skill_proficiencies else 0):+d} | {"✓" if "Sleight of Hand" in skill_proficiencies else ""} |
| **Stealth** | DEX | {calc_mod(abilities.get("DEX", 10)) + (proficiency_bonus if "Stealth" in skill_proficiencies else 0):+d} | {"✓" if "Stealth" in skill_proficiencies else ""} |
| **Survival** | WIS | {calc_mod(abilities.get("WIS", 10)) + (proficiency_bonus if "Survival" in skill_proficiencies else 0):+d} | {"✓" if "Survival" in skill_proficiencies else ""} |

---

## Combat

**Armor Class (AC):** {ac}  
**Initiative:** {initiative:+d}  
**Speed:** {speed} ft.

**Hit Points**
- **Maximum:** {max_hp}
- **Current:** {current_hp}
- **Temporary:** {temp_hp}

**Hit Dice**
- **Total:** {hit_dice}
- **Used:** ___

**Death Saves**
- **Successes:** ☐ ☐ ☐
- **Failures:** ☐ ☐ ☐

---

## Attacks & Spellcasting

### Attacks

"""

    if attacks:
        content += "| Weapon/Spell | Attack Bonus | Damage/Type | Range |\n"
        content += "|--------------|--------------|-------------|-------|\n"
        for attack in attacks:
            name = attack.get("name", "Weapon")
            bonus = attack.get("bonus", 0)
            damage = attack.get("damage", "1d6")
            damage_type = attack.get("damage_type", "slashing")
            range_val = attack.get("range", "5 ft.")
            content += f"| {name} | +{bonus} | {damage} {damage_type} | {range_val} |\n"
    else:
        content += "| Weapon/Spell | Attack Bonus | Damage/Type | Range |\n"
        content += "|--------------|--------------|-------------|-------|\n"
        content += "| _____________ | +___ | _____________ | _____ |\n"

    content += "\n---\n\n## Equipment\n\n"
    content += "**Coins:**\n"
    content += f"- **Platinum:** {coins.get('pp', 0)}\n"
    content += f"- **Gold:** {coins.get('gp', 0)}\n"
    content += f"- **Electrum:** {coins.get('ep', 0)}\n"
    content += f"- **Silver:** {coins.get('sp', 0)}\n"
    content += f"- **Copper:** {coins.get('cp', 0)}\n\n"
    content += "**Equipment & Items:**\n\n"

    if equipment:
        for item in equipment:
            content += f"- {item}\n"
    else:
        content += "_________________________________________________________________\n"

    content += "\n---\n\n## Features & Traits\n\n"
    content += "**Class Features:**\n\n"

    if features:
        for feature in features:
            content += f"- {feature}\n"
    else:
        content += "_________________________________________________________________\n"

    content += "\n**Racial Traits:**\n\n"
    if traits:
        for trait in traits:
            content += f"- {trait}\n"
    else:
        content += "_________________________________________________________________\n"

    content += "\n---\n\n## Proficiencies & Languages\n\n"
    content += f"**Armor Proficiencies:** {', '.join(armor_prof) if armor_prof else 'None'}\n\n"
    content += f"**Weapon Proficiencies:** {', '.join(weapon_prof) if weapon_prof else 'None'}\n\n"
    content += f"**Tool Proficiencies:** {', '.join(tool_prof) if tool_prof else 'None'}\n\n"
    content += f"**Languages:** {', '.join(languages)}\n\n"

    content += "---\n\n## Personality\n\n"
    content += "**Personality Traits:**\n\n"
    if personality:
        for trait in personality:
            content += f"- {trait}\n"
    else:
        content += "_________________________________________________________________\n"

    content += "\n**Ideals:**\n\n"
    if ideals:
        for ideal in ideals:
            content += f"- {ideal}\n"
    else:
        content += "_________________________________________________________________\n"

    content += "\n**Bonds:**\n\n"
    if bonds:
        for bond in bonds:
            content += f"- {bond}\n"
    else:
        content += "_________________________________________________________________\n"

    content += "\n**Flaws:**\n\n"
    if flaws:
        for flaw in flaws:
            content += f"- {flaw}\n"
    else:
        content += "_________________________________________________________________\n"

    if backstory:
        content += "\n---\n\n## Backstory\n\n"
        content += f"{backstory}\n"

    content += "\n---\n\n*D&D 5e Character Sheet*\n"

    return content


def generate_blank_sheet(output_path: Path | None = None):
    """Generate a blank character sheet PDF."""
    work_effort_dir = Path(__file__).parent
    if output_path is None:
        output_path = work_effort_dir / "character_sheet_blank.pdf"

    print("📄 Generating blank character sheet...")

    content = create_blank_character_sheet_content()

    generator = PDFGenerator.from_content(
        content=content,
        title="D&D 5e Character Sheet - Blank",
        style="clinical_standard",
        output_path=output_path,
    )

    result = generator.save(output_path=output_path, convert_to_png=True, png_dpi=300)

    print(f"   ✅ Generated: {result}")
    return result


def generate_filled_sheet(character_data: dict[str, Any], output_path: Path | None = None):
    """Generate a filled character sheet PDF."""
    work_effort_dir = Path(__file__).parent
    if output_path is None:
        char_name = character_data.get("name", "character").replace(" ", "_")
        output_path = work_effort_dir / f"character_sheet_{char_name}.pdf"

    print(f"📄 Generating character sheet for {character_data.get('name', 'Character')}...")

    content = create_filled_character_sheet_content(character_data)

    generator = PDFGenerator.from_content(
        content=content,
        title=f"D&D 5e Character Sheet - {character_data.get('name', 'Character')}",
        style="clinical_standard",
        output_path=output_path,
    )

    result = generator.save(output_path=output_path, convert_to_png=True, png_dpi=300)

    print(f"   ✅ Generated: {result}")
    return result


def main():
    """Generate both blank and example filled character sheets."""
    print("=" * 60)
    print("D&D 5e Character Sheet Generator")
    print("=" * 60)

    work_effort_dir = Path(__file__).parent

    # Generate blank sheet
    print("\n1. Generating blank character sheet...")
    blank_path = generate_blank_sheet()

    # Generate example filled sheet
    print("\n2. Generating example filled character sheet...")
    example_character = {
        "name": "Aldric the Brave",
        "class": "Fighter",
        "level": 3,
        "background": "Folk Hero",
        "race": "Human",
        "alignment": "Lawful Good",
        "xp": 900,
        "abilities": {"STR": 16, "DEX": 13, "CON": 15, "INT": 10, "WIS": 12, "CHA": 11},
        "proficiency_bonus": 2,
        "saving_throw_proficiencies": ["STR", "CON"],
        "skill_proficiencies": ["Athletics", "Perception", "Survival", "Animal Handling"],
        "ac": 16,
        "initiative": 1,
        "speed": 30,
        "max_hp": 28,
        "current_hp": 28,
        "temp_hp": 0,
        "hit_dice": "3d10",
        "attacks": [
            {
                "name": "Longsword",
                "bonus": 5,
                "damage": "1d8+3",
                "damage_type": "slashing",
                "range": "5 ft.",
            },
            {
                "name": "Shortbow",
                "bonus": 3,
                "damage": "1d6",
                "damage_type": "piercing",
                "range": "80/320 ft.",
            },
        ],
        "equipment": [
            "Chain Mail",
            "Longsword",
            "Shield",
            "Shortbow",
            "20 Arrows",
            "Backpack",
            "Bedroll",
            "Rations (10 days)",
            "Waterskin",
        ],
        "coins": {"pp": 0, "gp": 15, "ep": 0, "sp": 5, "cp": 10},
        "features": ["Fighting Style: Defense", "Second Wind", "Action Surge"],
        "traits": ["Human: +1 to all ability scores", "Extra Language: Elvish"],
        "armor_proficiencies": ["All armor", "Shields"],
        "weapon_proficiencies": ["Simple weapons", "Martial weapons"],
        "tool_proficiencies": ["Smith's tools", "Vehicles (land)"],
        "languages": ["Common", "Elvish"],
        "personality_traits": [
            "I judge people by their actions, not their words.",
            "If someone is in trouble, I'm always ready to help.",
        ],
        "ideals": ["Responsibility: I protect those who cannot protect themselves. (Good)"],
        "bonds": ["I must protect my home village from the dangers that threaten it."],
        "flaws": ["I'm too trusting of others and often get taken advantage of."],
        "backstory": "Aldric grew up in a small village, always ready to help those in need. When bandits threatened his home, he took up arms and drove them away. Now he travels the land, seeking to protect others from similar threats.",
    }

    filled_path = generate_filled_sheet(example_character)

    # Summary
    print("\n" + "=" * 60)
    print("✅ Character Sheet Generation Complete!")
    print("=" * 60)
    print("\nGenerated Files:")
    print(f"   📄 Blank Sheet: {blank_path.name}")
    print(f"   📄 Example Sheet: {filled_path.name}")
    print(f"\nLocation: {work_effort_dir}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
