"""
Being Character Sheet Generator
===============================

Generates D&D 5e character sheets for Beings in multiple formats:
- .txt (default, generated automatically when Being is created)
- .md (on demand)
- .pdf (on demand)

Integrates with Being system and D&D 5e character system.
Uses templates with placeholders for key details.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.waft.being import Being
from src.waft.core.dnd5e.character import DnD5eCharacter
from src.waft.core.dnd5e.dice import DnDRoller
from src.waft.core.dnd5e.stats import ArmorType, DnD5eStats
from src.waft.evolution.pdf_generator import PDFGenerator

# Character Sheet Template with Placeholders
CHARACTER_SHEET_TEMPLATE = """D&D 5e Character Sheet

CHARACTER INFORMATION
====================
Name: {NAME}
Class & Level: {CLASS_LEVEL}
Background: {BACKGROUND}
Player Name: {PLAYER_NAME}
Race: {RACE}
Alignment: {ALIGNMENT}
Experience Points: {XP}

ABILITY SCORES
==============
Ability        Score    Modifier    Saving Throw    Proficiency
Strength      {STR}    {STR_MOD}    {STR_SAVE}         {STR_SAVE_PROF}
Dexterity     {DEX}    {DEX_MOD}    {DEX_SAVE}         {DEX_SAVE_PROF}
Constitution  {CON}    {CON_MOD}    {CON_SAVE}         {CON_SAVE_PROF}
Intelligence  {INT}    {INT_MOD}    {INT_SAVE}         {INT_SAVE_PROF}
Wisdom        {WIS}    {WIS_MOD}    {WIS_SAVE}         {WIS_SAVE_PROF}
Charisma      {CHA}    {CHA_MOD}    {CHA_SAVE}         {CHA_SAVE_PROF}

Proficiency Bonus: +{PROF_BONUS}

SKILLS
======
Skill                Ability    Modifier    Proficiency
Acrobatics           DEX        {ACROBATICS:+3d}        {ACROBATICS_PROF}
Animal Handling      WIS        {ANIMAL_HANDLING:+3d}        {ANIMAL_HANDLING_PROF}
Arcana               INT        {ARCANA:+3d}        {ARCANA_PROF}
Athletics            STR        {ATHLETICS:+3d}        {ATHLETICS_PROF}
Deception            CHA        {DECEPTION:+3d}        {DECEPTION_PROF}
History              INT        {HISTORY:+3d}        {HISTORY_PROF}
Insight              WIS        {INSIGHT:+3d}        {INSIGHT_PROF}
Intimidation         CHA        {INTIMIDATION:+3d}        {INTIMIDATION_PROF}
Investigation        INT        {INVESTIGATION:+3d}        {INVESTIGATION_PROF}
Medicine             WIS        {MEDICINE:+3d}        {MEDICINE_PROF}
Nature               INT        {NATURE:+3d}        {NATURE_PROF}
Perception           WIS        {PERCEPTION:+3d}        {PERCEPTION_PROF}
Performance          CHA        {PERFORMANCE:+3d}        {PERFORMANCE_PROF}
Persuasion           CHA        {PERSUASION:+3d}        {PERSUASION_PROF}
Religion             INT        {RELIGION:+3d}        {RELIGION_PROF}
Sleight of Hand      DEX        {SLEIGHT_OF_HAND:+3d}        {SLEIGHT_OF_HAND_PROF}
Stealth              DEX        {STEALTH:+3d}        {STEALTH_PROF}
Survival             WIS        {SURVIVAL:+3d}        {SURVIVAL_PROF}

COMBAT
======
Armor Class (AC): {AC}
Initiative: {INITIATIVE}
Speed: {SPEED} ft.

Hit Points
  Maximum: {MAX_HP}
  Current: {CURRENT_HP}
  Temporary: {TEMP_HP}

Hit Dice
  Total: {HIT_DICE}
  Used: {HIT_DICE_USED}

Death Saves
  Successes: {DEATH_SUCCESSES}
  Failures: {DEATH_FAILURES}

ATTACKS & SPELLCASTING
======================
{ATTACKS}

EQUIPMENT
=========
Coins:
  Platinum: {PP}
  Gold: {GP}
  Electrum: {EP}
  Silver: {SP}
  Copper: {CP}

Equipment & Items:
{EQUIPMENT}

FEATURES & TRAITS
=================
Class Features:
{CLASS_FEATURES}

Racial Traits:
{RACIAL_TRAITS}

Feats:
{FEATS}

Other Features & Traits:
{OTHER_FEATURES}

PROFICIENCIES & LANGUAGES
==========================
Armor Proficiencies: {ARMOR_PROF}
Weapon Proficiencies: {WEAPON_PROF}
Tool Proficiencies: {TOOL_PROF}
Languages: {LANGUAGES}

PERSONALITY
===========
Personality Traits:
{PERSONALITY_TRAITS}

Ideals:
{IDEALS}

Bonds:
{BONDS}

Flaws:
{FLAWS}

BACKSTORY
=========
{BACKSTORY}

NOTES
=====
{NOTES}

---
Generated: {GENERATED_DATE}
Being ID: {BEING_ID}
Reality: {REALITY_ID}
"""


def being_to_character_data(
    being: Being, character: DnD5eCharacter | None = None
) -> dict[str, Any]:
    """
    Convert Being and optional D&D Character to character sheet data.

    If character is provided, uses its stats. Otherwise generates from Being.
    """
    # Generate character if not provided
    if character is None:
        character = create_character_from_being(being)

    # Calculate all modifiers
    str_mod = DnD5eStats.ability_modifier(character.strength)
    dex_mod = DnD5eStats.ability_modifier(character.dexterity)
    con_mod = DnD5eStats.ability_modifier(character.constitution)
    int_mod = DnD5eStats.ability_modifier(character.intelligence)
    wis_mod = DnD5eStats.ability_modifier(character.wisdom)
    cha_mod = DnD5eStats.ability_modifier(character.charisma)

    prof_bonus = character.proficiency_bonus

    # Saving throws
    saving_throws = {
        "STR": str_mod + (prof_bonus if "STR" in character.proficient_saves else 0),
        "DEX": dex_mod + (prof_bonus if "DEX" in character.proficient_saves else 0),
        "CON": con_mod + (prof_bonus if "CON" in character.proficient_saves else 0),
        "INT": int_mod + (prof_bonus if "INT" in character.proficient_saves else 0),
        "WIS": wis_mod + (prof_bonus if "WIS" in character.proficient_saves else 0),
        "CHA": cha_mod + (prof_bonus if "CHA" in character.proficient_saves else 0),
    }

    # Skills
    skill_map = {
        "Acrobatics": ("DEX", dex_mod),
        "Animal Handling": ("WIS", wis_mod),
        "Arcana": ("INT", int_mod),
        "Athletics": ("STR", str_mod),
        "Deception": ("CHA", cha_mod),
        "History": ("INT", int_mod),
        "Insight": ("WIS", wis_mod),
        "Intimidation": ("CHA", cha_mod),
        "Investigation": ("INT", int_mod),
        "Medicine": ("WIS", wis_mod),
        "Nature": ("INT", int_mod),
        "Perception": ("WIS", wis_mod),
        "Performance": ("CHA", cha_mod),
        "Persuasion": ("CHA", cha_mod),
        "Religion": ("INT", int_mod),
        "Sleight of Hand": ("DEX", dex_mod),
        "Stealth": ("DEX", dex_mod),
        "Survival": ("WIS", wis_mod),
    }

    skills = {}
    for skill_name, (ability, base_mod) in skill_map.items():
        is_prof = skill_name in character.proficient_skills
        skills[skill_name] = {
            "modifier": base_mod + (prof_bonus if is_prof else 0),
            "proficient": "✓" if is_prof else "",
        }

    # Attacks
    attacks_text = ""
    if character.equipped_weapon:
        weapon_bonus = str_mod + prof_bonus
        attacks_text = f"{character.equipped_weapon} | +{weapon_bonus} | 1d8+{str_mod} | 5 ft."
    else:
        attacks_text = "No weapon equipped"

    # Equipment
    equipment_list = []
    if character.equipped_armor:
        equipment_list.append(character.equipped_armor)
    if character.equipped_weapon:
        equipment_list.append(character.equipped_weapon)
    equipment_text = "\n".join(f"  - {item}" if equipment_list else "  (none)")

    # Extract personality from Being
    personality = being.personality or {}
    personality_traits = personality.get("traits", [])
    ideals = personality.get("ideals", [])
    bonds = personality.get("bonds", [])
    flaws = personality.get("flaws", [])

    # Backstory from Being memories
    backstory = ""
    if being.memories:
        backstory = "\n".join([f"  - {mem.get('content', str(mem))}" for mem in being.memories[:5]])

    return {
        "NAME": character.name,
        "CLASS_LEVEL": f"{character.char_class.title()} {character.level}",
        "BACKGROUND": "Adventurer",
        "PLAYER_NAME": "",
        "RACE": "Human",
        "ALIGNMENT": "Neutral",
        "XP": str((character.level - 1) * 300),
        "STR": str(character.strength),
        "STR_MOD": f"{str_mod:+d}",
        "STR_SAVE": f"{saving_throws['STR']:+d}",
        "STR_SAVE_PROF": "✓" if "STR" in character.proficient_saves else "",
        "DEX": str(character.dexterity),
        "DEX_MOD": f"{dex_mod:+d}",
        "DEX_SAVE": f"{saving_throws['DEX']:+d}",
        "DEX_SAVE_PROF": "✓" if "DEX" in character.proficient_saves else "",
        "CON": str(character.constitution),
        "CON_MOD": f"{con_mod:+d}",
        "CON_SAVE": f"{saving_throws['CON']:+d}",
        "CON_SAVE_PROF": "✓" if "CON" in character.proficient_saves else "",
        "INT": str(character.intelligence),
        "INT_MOD": f"{int_mod:+d}",
        "INT_SAVE": f"{saving_throws['INT']:+d}",
        "INT_SAVE_PROF": "✓" if "INT" in character.proficient_saves else "",
        "WIS": str(character.wisdom),
        "WIS_MOD": f"{wis_mod:+d}",
        "WIS_SAVE": f"{saving_throws['WIS']:+d}",
        "WIS_SAVE_PROF": "✓" if "WIS" in character.proficient_saves else "",
        "CHA": str(character.charisma),
        "CHA_MOD": f"{cha_mod:+d}",
        "CHA_SAVE": f"{saving_throws['CHA']:+d}",
        "CHA_SAVE_PROF": "✓" if "CHA" in character.proficient_saves else "",
        "PROF_BONUS": prof_bonus,
        "ACROBATICS": skills["Acrobatics"]["modifier"],
        "ACROBATICS_PROF": skills["Acrobatics"]["proficient"],
        "ANIMAL_HANDLING": skills["Animal Handling"]["modifier"],
        "ANIMAL_HANDLING_PROF": skills["Animal Handling"]["proficient"],
        "ARCANA": skills["Arcana"]["modifier"],
        "ARCANA_PROF": skills["Arcana"]["proficient"],
        "ATHLETICS": skills["Athletics"]["modifier"],
        "ATHLETICS_PROF": skills["Athletics"]["proficient"],
        "DECEPTION": skills["Deception"]["modifier"],
        "DECEPTION_PROF": skills["Deception"]["proficient"],
        "HISTORY": skills["History"]["modifier"],
        "HISTORY_PROF": skills["History"]["proficient"],
        "INSIGHT": skills["Insight"]["modifier"],
        "INSIGHT_PROF": skills["Insight"]["proficient"],
        "INTIMIDATION": skills["Intimidation"]["modifier"],
        "INTIMIDATION_PROF": skills["Intimidation"]["proficient"],
        "INVESTIGATION": skills["Investigation"]["modifier"],
        "INVESTIGATION_PROF": skills["Investigation"]["proficient"],
        "MEDICINE": skills["Medicine"]["modifier"],
        "MEDICINE_PROF": skills["Medicine"]["proficient"],
        "NATURE": skills["Nature"]["modifier"],
        "NATURE_PROF": skills["Nature"]["proficient"],
        "PERCEPTION": skills["Perception"]["modifier"],
        "PERCEPTION_PROF": skills["Perception"]["proficient"],
        "PERFORMANCE": skills["Performance"]["modifier"],
        "PERFORMANCE_PROF": skills["Performance"]["proficient"],
        "PERSUASION": skills["Persuasion"]["modifier"],
        "PERSUASION_PROF": skills["Persuasion"]["proficient"],
        "RELIGION": skills["Religion"]["modifier"],
        "RELIGION_PROF": skills["Religion"]["proficient"],
        "SLEIGHT_OF_HAND": skills["Sleight of Hand"]["modifier"],
        "SLEIGHT_OF_HAND_PROF": skills["Sleight of Hand"]["proficient"],
        "STEALTH": skills["Stealth"]["modifier"],
        "STEALTH_PROF": skills["Stealth"]["proficient"],
        "SURVIVAL": skills["Survival"]["modifier"],
        "SURVIVAL_PROF": skills["Survival"]["proficient"],
        "AC": character.ac,
        "INITIATIVE": f"{dex_mod:+d}",
        "SPEED": 30,
        "MAX_HP": character.max_hp,
        "CURRENT_HP": character.hp,
        "TEMP_HP": 0,
        "HIT_DICE": f"{character.level}d{character.hit_die}",
        "HIT_DICE_USED": "0",
        "DEATH_SUCCESSES": "☐ ☐ ☐",
        "DEATH_FAILURES": "☐ ☐ ☐",
        "ATTACKS": attacks_text,
        "PP": "0",
        "GP": "0",
        "EP": "0",
        "SP": "0",
        "CP": "0",
        "EQUIPMENT": equipment_text,
        "CLASS_FEATURES": "  (class features here)",
        "RACIAL_TRAITS": "  (racial traits here)",
        "FEATS": "  (feats here)",
        "OTHER_FEATURES": "  (other features here)",
        "ARMOR_PROF": "Light, Medium, Heavy",
        "WEAPON_PROF": "Simple, Martial",
        "TOOL_PROF": "None",
        "LANGUAGES": "Common",
        "PERSONALITY_TRAITS": "\n".join([f"  - {t}" for t in personality_traits])
        if personality_traits
        else "  (none)",
        "IDEALS": "\n".join([f"  - {i}" for i in ideals]) if ideals else "  (none)",
        "BONDS": "\n".join([f"  - {b}" for b in bonds]) if bonds else "  (none)",
        "FLAWS": "\n".join([f"  - {f}" for f in flaws]) if flaws else "  (none)",
        "BACKSTORY": backstory if backstory else "  (no backstory recorded)",
        "NOTES": "  (notes here)",
        "GENERATED_DATE": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "BEING_ID": being.being_id,
        "REALITY_ID": being.reality_id,
    }


def create_character_from_being(being: Being) -> DnD5eCharacter:
    """Create a D&D character from a Being."""
    # Generate name from Being ID
    name = being.being_id.replace("being_", "").replace("_", " ").title()

    # Roll ability scores (4d6, drop lowest)
    def roll_ability_score() -> int:
        rolls = [DnDRoller.roll("1d6") for _ in range(4)]
        rolls.sort(reverse=True)
        return sum(rolls[:3])

    # Roll all abilities
    strength = roll_ability_score()
    dexterity = roll_ability_score()
    constitution = roll_ability_score()
    intelligence = roll_ability_score()
    wisdom = roll_ability_score()
    charisma = roll_ability_score()

    # Calculate HP
    con_mod = DnD5eStats.ability_modifier(constitution)
    hit_die = 10
    max_hp = hit_die + con_mod

    # Create character
    character = DnD5eCharacter(
        name=name,
        level=1,
        char_class="fighter",
        hit_die=hit_die,
        strength=strength,
        dexterity=dexterity,
        constitution=constitution,
        intelligence=intelligence,
        wisdom=wisdom,
        charisma=charisma,
        hp=max_hp,
        max_hp=max_hp,
        armor_type=ArmorType.NONE,
        proficient_saves=["STR", "CON"],  # Fighter saves
        proficient_skills=["Athletics", "Perception"],  # Example
    )

    return character


def generate_character_sheet_txt(
    being: Being, character: DnD5eCharacter | None = None, output_path: Path | None = None
) -> Path:
    """
    Generate character sheet as .txt (default format).

    This is called automatically when a Being is created.
    """
    if output_path is None:
        being_dir = project_root / "_hidden" / ".truth" / "beings" / being.being_id
        being_dir.mkdir(parents=True, exist_ok=True)
        output_path = being_dir / "character_sheet.txt"

    # Get character data
    data = being_to_character_data(being, character)

    # Fill template
    sheet_content = CHARACTER_SHEET_TEMPLATE.format(**data)

    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(sheet_content)

    return output_path


def generate_character_sheet_md(
    being: Being, character: DnD5eCharacter | None = None, output_path: Path | None = None
) -> Path:
    """
    Generate character sheet as .md (on demand).
    """
    if output_path is None:
        being_dir = project_root / "_hidden" / ".truth" / "beings" / being.being_id
        being_dir.mkdir(parents=True, exist_ok=True)
        output_path = being_dir / "character_sheet.md"

    # Get character data
    data = being_to_character_data(being, character)

    # Convert to markdown format
    md_content = convert_to_markdown(data)

    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(md_content)

    return output_path


def generate_character_sheet_pdf(
    being: Being, character: DnD5eCharacter | None = None, output_path: Path | None = None
) -> Path:
    """
    Generate character sheet as .pdf (on demand).
    """
    if output_path is None:
        being_dir = project_root / "_hidden" / ".truth" / "beings" / being.being_id
        being_dir.mkdir(parents=True, exist_ok=True)
        output_path = being_dir / "character_sheet.pdf"

    # Get character data
    data = being_to_character_data(being, character)

    # Convert to markdown
    md_content = convert_to_markdown(data)

    # Generate PDF
    generator = PDFGenerator.from_content(
        content=md_content,
        title=f"D&D 5e Character Sheet - {data['NAME']}",
        style="clinical_standard",
        output_path=output_path,
    )

    result = generator.save(output_path=output_path, convert_to_png=True, png_dpi=300)

    return result


def convert_to_markdown(data: dict[str, Any]) -> str:
    """Convert character data to markdown format."""
    content = f"""# D&D 5e Character Sheet

## Character Information

**Name:** {data["NAME"]}  
**Class & Level:** {data["CLASS_LEVEL"]}  
**Background:** {data["BACKGROUND"]}  
**Player Name:** {data["PLAYER_NAME"] or "_________________"}  
**Race:** {data["RACE"]}  
**Alignment:** {data["ALIGNMENT"]}  
**Experience Points:** {data["XP"]}

---

## Ability Scores

| Ability | Score | Modifier | Saving Throw | Proficiency |
|---------|-------|----------|--------------|-------------|
| **Strength** | {data["STR"]} | {data["STR_MOD"]:+d} | {data["STR_SAVE"]:+d} | {data["STR_SAVE_PROF"]} |
| **Dexterity** | {data["DEX"]} | {data["DEX_MOD"]:+d} | {data["DEX_SAVE"]:+d} | {data["DEX_SAVE_PROF"]} |
| **Constitution** | {data["CON"]} | {data["CON_MOD"]:+d} | {data["CON_SAVE"]:+d} | {data["CON_SAVE_PROF"]} |
| **Intelligence** | {data["INT"]} | {data["INT_MOD"]:+d} | {data["INT_SAVE"]:+d} | {data["INT_SAVE_PROF"]} |
| **Wisdom** | {data["WIS"]} | {data["WIS_MOD"]:+d} | {data["WIS_SAVE"]:+d} | {data["WIS_SAVE_PROF"]} |
| **Charisma** | {data["CHA"]} | {data["CHA_MOD"]:+d} | {data["CHA_SAVE"]:+d} | {data["CHA_SAVE_PROF"]} |

**Proficiency Bonus:** +{data["PROF_BONUS"]}

---

## Skills

| Skill | Ability | Modifier | Proficiency |
|-------|---------|----------|-------------|
| **Acrobatics** | DEX | {data["ACROBATICS"]:+d} | {data["ACROBATICS_PROF"]} |
| **Animal Handling** | WIS | {data["ANIMAL_HANDLING"]:+d} | {data["ANIMAL_HANDLING_PROF"]} |
| **Arcana** | INT | {data["ARCANA"]:+d} | {data["ARCANA_PROF"]} |
| **Athletics** | STR | {data["ATHLETICS"]:+d} | {data["ATHLETICS_PROF"]} |
| **Deception** | CHA | {data["DECEPTION"]:+d} | {data["DECEPTION_PROF"]} |
| **History** | INT | {data["HISTORY"]:+d} | {data["HISTORY_PROF"]} |
| **Insight** | WIS | {data["INSIGHT"]:+d} | {data["INSIGHT_PROF"]} |
| **Intimidation** | CHA | {data["INTIMIDATION"]:+d} | {data["INTIMIDATION_PROF"]} |
| **Investigation** | INT | {data["INVESTIGATION"]:+d} | {data["INVESTIGATION_PROF"]} |
| **Medicine** | WIS | {data["MEDICINE"]:+d} | {data["MEDICINE_PROF"]} |
| **Nature** | INT | {data["NATURE"]:+d} | {data["NATURE_PROF"]} |
| **Perception** | WIS | {data["PERCEPTION"]:+d} | {data["PERCEPTION_PROF"]} |
| **Performance** | CHA | {data["PERFORMANCE"]:+d} | {data["PERFORMANCE_PROF"]} |
| **Persuasion** | CHA | {data["PERSUASION"]:+d} | {data["PERSUASION_PROF"]} |
| **Religion** | INT | {data["RELIGION"]:+d} | {data["RELIGION_PROF"]} |
| **Sleight of Hand** | DEX | {data["SLEIGHT_OF_HAND"]:+d} | {data["SLEIGHT_OF_HAND_PROF"]} |
| **Stealth** | DEX | {data["STEALTH"]:+d} | {data["STEALTH_PROF"]} |
| **Survival** | WIS | {data["SURVIVAL"]:+d} | {data["SURVIVAL_PROF"]} |

---

## Combat

**Armor Class (AC):** {data["AC"]}  
**Initiative:** {data["INITIATIVE"]:+d}  
**Speed:** {data["SPEED"]} ft.

**Hit Points**
- **Maximum:** {data["MAX_HP"]}
- **Current:** {data["CURRENT_HP"]}
- **Temporary:** {data["TEMP_HP"]}

**Hit Dice**
- **Total:** {data["HIT_DICE"]}
- **Used:** {data["HIT_DICE_USED"]}

**Death Saves**
- **Successes:** {data["DEATH_SUCCESSES"]}
- **Failures:** {data["DEATH_FAILURES"]}

---

## Attacks & Spellcasting

### Attacks

{data["ATTACKS"]}

---

## Equipment

**Coins:**
- **Platinum:** {data["PP"]}
- **Gold:** {data["GP"]}
- **Electrum:** {data["EP"]}
- **Silver:** {data["SP"]}
- **Copper:** {data["CP"]}

**Equipment & Items:**
{data["EQUIPMENT"]}

---

## Features & Traits

**Class Features:**
{data["CLASS_FEATURES"]}

**Racial Traits:**
{data["RACIAL_TRAITS"]}

**Feats:**
{data["FEATS"]}

**Other Features & Traits:**
{data["OTHER_FEATURES"]}

---

## Proficiencies & Languages

**Armor Proficiencies:** {data["ARMOR_PROF"]}  
**Weapon Proficiencies:** {data["WEAPON_PROF"]}  
**Tool Proficiencies:** {data["TOOL_PROF"]}  
**Languages:** {data["LANGUAGES"]}

---

## Personality

**Personality Traits:**
{data["PERSONALITY_TRAITS"]}

**Ideals:**
{data["IDEALS"]}

**Bonds:**
{data["BONDS"]}

**Flaws:**
{data["FLAWS"]}

---

## Backstory

{data["BACKSTORY"]}

---

## Notes

{data["NOTES"]}

---

*Generated: {data["GENERATED_DATE"]}*  
*Being ID: {data["BEING_ID"]}*  
*Reality: {data["REALITY_ID"]}*
"""
    return content


def main():
    """Test the character sheet generator."""
    print("=" * 60)
    print("Being Character Sheet Generator - Test")
    print("=" * 60)

    # Create a test Being
    from src.waft.being import BeingSystem

    being_system = BeingSystem(project_path=project_root)
    being = being_system.spawn_being(
        reality_id="test_reality",
        parent_being_id=None,
        initial_skills={"strength": 60.0, "dexterity": 45.0},
    )

    print(f"\n✅ Created test Being: {being.being_id}")

    # Generate .txt (default)
    print("\n📄 Generating .txt character sheet (default)...")
    txt_path = generate_character_sheet_txt(being)
    print(f"   ✅ Generated: {txt_path}")

    # Generate .md (on demand)
    print("\n📄 Generating .md character sheet (on demand)...")
    md_path = generate_character_sheet_md(being)
    print(f"   ✅ Generated: {md_path}")

    # Generate .pdf (on demand)
    print("\n📄 Generating .pdf character sheet (on demand)...")
    pdf_path = generate_character_sheet_pdf(being)
    print(f"   ✅ Generated: {pdf_path}")

    print("\n" + "=" * 60)
    print("✅ Character Sheet Generation Complete!")
    print("=" * 60)
    print("\nGenerated Files:")
    print(f"   📄 .txt: {txt_path.name}")
    print(f"   📄 .md: {md_path.name}")
    print(f"   📄 .pdf: {pdf_path.name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
