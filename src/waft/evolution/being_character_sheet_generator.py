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

# Add project root to path (if needed)
# project_root is determined from being_dir when called
from src.waft.being import Being
from src.waft.core.dnd5e.character import DnD5eCharacter
from src.waft.core.dnd5e.dice import DnDRoller
from src.waft.core.dnd5e.stats import ArmorType, DnD5eStats

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
    for skill_name, (_ability, base_mod) in skill_map.items():
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

    # Add class-specific starting equipment
    if character.char_class.lower() == "cartographer":
        equipment_list.append("Cartographer's tools")
        equipment_list.append("Navigator's tools")
        equipment_list.append("Map case")
        equipment_list.append("Quill and ink")
        if not character.equipped_weapon:
            equipment_list.append("Dagger")

    equipment_text = (
        "\n".join(f"  - {item}" for item in equipment_list) if equipment_list else "  (none)"
    )

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
        "CLASS_FEATURES": _get_class_features(character.char_class, character.level),
        "RACIAL_TRAITS": "  (racial traits here)",
        "FEATS": "  (feats here)",
        "OTHER_FEATURES": "  (other features here)",
        "ARMOR_PROF": _get_armor_proficiencies(character.char_class),
        "WEAPON_PROF": _get_weapon_proficiencies(character.char_class),
        "TOOL_PROF": _get_tool_proficiencies(character.char_class),
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


def _get_class_features(char_class: str, level: int) -> str:
    """Get class features description for character sheet."""
    features = []

    if char_class.lower() == "cartographer":
        features.append("  - Cartographer's Tools: Proficient with cartographer's tools")
        features.append("  - Map Reading: Advantage on Investigation checks to analyze maps")
        features.append(
            "  - Navigation: Can always determine direction and approximate distance to known locations"
        )
        if level >= 1:
            features.append("  - Cartographic Memory: Can perfectly recall any map you've seen")
        if level >= 3:
            features.append("  - Quick Mapping: Can create accurate maps of areas you've explored")
        if level >= 5:
            features.append("  - Hidden Paths: Can detect secret passages and hidden routes")
    elif char_class.lower() == "fighter":
        features.append("  - Fighting Style: Choose a fighting style")
        features.append("  - Second Wind: Recover HP as bonus action")
    elif char_class.lower() == "wizard":
        features.append("  - Spellcasting: Cast wizard spells")
        features.append("  - Arcane Recovery: Recover spell slots on short rest")
    else:
        features.append(f"  ({char_class.title()} class features)")

    return "\n".join(features) if features else "  (no class features)"


def _get_armor_proficiencies(char_class: str) -> str:
    """Get armor proficiencies for character class."""
    if char_class.lower() == "cartographer":
        return "Light"
    elif char_class.lower() == "fighter":
        return "Light, Medium, Heavy, Shields"
    elif char_class.lower() == "wizard":
        return "None"
    else:
        return "Light"


def _get_weapon_proficiencies(char_class: str) -> str:
    """Get weapon proficiencies for character class."""
    if char_class.lower() == "cartographer":
        return "Simple weapons, Hand crossbow"
    elif char_class.lower() == "fighter":
        return "Simple, Martial"
    elif char_class.lower() == "wizard":
        return "Daggers, Darts, Slings, Quarterstaffs, Light crossbows"
    else:
        return "Simple"


def _get_tool_proficiencies(char_class: str) -> str:
    """Get tool proficiencies for character class."""
    if char_class.lower() == "cartographer":
        return "Cartographer's tools, Navigator's tools"
    elif char_class.lower() == "fighter":
        return "None"
    elif char_class.lower() == "wizard":
        return "None"
    else:
        return "None"


def create_character_from_being(being: Being) -> DnD5eCharacter:
    """
    Create a D&D character from a Being.

    Maps Being skills to D&D ability scores and creates a character.

    Uses naming priority:
    1. custom_name (if user set one, e.g., "Bob")
    2. scientific_name (deterministic from hash via LineagePoet)
    3. being_id (fallback)
    """
    # Use display_name which handles priority: custom_name → scientific_name → being_id
    name = being.display_name

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
    being: Being,
    character: DnD5eCharacter | None = None,
    output_path: Path | None = None,
    project_path: Path | None = None,
) -> Path:
    """
    Generate character sheet as .txt (default format).

    This is called automatically when a Being is created.

    Args:
        being: Being instance
        character: Optional D&D character (generated if not provided)
        output_path: Optional output path
        project_path: Project root path (determined from being if not provided)
    """
    if project_path is None:
        # Determine project path from being's storage location
        # Being is stored in _hidden/.truth/beings/being_id/
        # So we go up 4 levels: being_id -> beings -> .truth -> _hidden -> project_root
        being_dir = Path(being.being_id) if hasattr(being, "_storage_path") else None
        if being_dir is None:
            # Fallback: use current working directory
            project_path = Path.cwd()
        else:
            project_path = being_dir.parent.parent.parent.parent

    if output_path is None:
        being_dir = project_path / "_hidden" / ".truth" / "beings" / being.being_id
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
    being: Being,
    character: DnD5eCharacter | None = None,
    output_path: Path | None = None,
    project_path: Path | None = None,
) -> Path:
    """
    Generate character sheet as .md (on demand).
    """
    if project_path is None:
        project_path = Path.cwd()

    if output_path is None:
        being_dir = project_path / "_hidden" / ".truth" / "beings" / being.being_id
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


def convert_to_dnd5e_html(data: dict[str, Any]) -> str:
    """Convert character data to official D&D 5e character sheet HTML format."""
    from jinja2 import Template

    # Load template from file
    template_file = Path(__file__).parent / "dnd5e_character_sheet_template.html"
    if template_file.exists():
        template_str = template_file.read_text()
    else:
        # Fallback to inline template (simplified version)
        template_str = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>D&D 5e Character Sheet - {{ data.NAME }}</title>
    <style>
        @page {
            size: letter;
            margin: 0.25in;
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', 'Helvetica', sans-serif;
            font-size: 10pt;
            margin: 0;
            padding: 0;
            background: #fff;
        }

        .character-sheet {
            width: 100%;
        }

        .main-layout {
            width: 100%;
            border-collapse: collapse;
        }

        .main-layout td {
            vertical-align: top;
            padding: 0.05in;
        }

        .header-section {
            grid-column: 1 / -1;
            border: 2px solid #000;
            padding: 0.1in;
            margin-bottom: 0.1in;
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: 0.1in;
        }

        .header-field {
            display: flex;
            flex-direction: column;
        }

        .header-label {
            font-size: 8pt;
            font-weight: bold;
            text-transform: uppercase;
            border-bottom: 1px solid #000;
            padding-bottom: 2pt;
            margin-bottom: 4pt;
        }

        .header-value {
            font-size: 11pt;
            font-weight: bold;
        }

        .ability-scores {
            grid-column: 1;
            border: 2px solid #000;
            padding: 0.1in;
        }

        .ability-score-box {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.05in;
            margin-bottom: 0.1in;
            border: 1px solid #000;
            padding: 0.05in;
        }

        .ability-name {
            font-weight: bold;
            font-size: 11pt;
            text-transform: uppercase;
            grid-column: 1 / -1;
            border-bottom: 1px solid #000;
            padding-bottom: 2pt;
            margin-bottom: 4pt;
        }

        .ability-value {
            text-align: center;
            font-size: 18pt;
            font-weight: bold;
            border: 1px solid #000;
            padding: 0.05in;
        }

        .ability-modifier {
            text-align: center;
            font-size: 14pt;
            font-weight: bold;
            border: 1px solid #000;
            padding: 0.05in;
        }

        .saving-throw {
            display: flex;
            align-items: center;
            gap: 4pt;
            margin-top: 4pt;
        }

        .checkbox {
            width: 12pt;
            height: 12pt;
            border: 1px solid #000;
            display: inline-block;
        }

        .checkbox.checked::after {
            content: "✓";
            display: block;
            text-align: center;
            line-height: 12pt;
            font-size: 10pt;
        }

        .skills-section {
            grid-column: 1;
            border: 2px solid #000;
            padding: 0.1in;
            margin-top: 0.1in;
        }

        .section-title {
            font-weight: bold;
            font-size: 12pt;
            text-transform: uppercase;
            border-bottom: 2px solid #000;
            padding-bottom: 4pt;
            margin-bottom: 0.1in;
        }

        .skill-row {
            display: grid;
            grid-template-columns: 12pt 1fr 40pt;
            gap: 4pt;
            align-items: center;
            margin-bottom: 2pt;
            font-size: 9pt;
        }

        .skill-name {
            font-weight: bold;
        }

        .skill-modifier {
            text-align: right;
            font-weight: bold;
        }

        .right-column {
            grid-column: 2;
            display: flex;
            flex-direction: column;
            gap: 0.1in;
        }

        .combat-stats {
            border: 2px solid #000;
            padding: 0.1in;
        }

        .stat-box {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.05in;
            margin-bottom: 0.1in;
        }

        .stat-label {
            font-size: 8pt;
            font-weight: bold;
            text-transform: uppercase;
            border-bottom: 1px solid #000;
            padding-bottom: 2pt;
        }

        .stat-value {
            font-size: 16pt;
            font-weight: bold;
            text-align: center;
            border: 1px solid #000;
            padding: 0.05in;
        }

        .hp-section {
            border: 2px solid #000;
            padding: 0.1in;
            margin-top: 0.1in;
        }

        .hp-boxes {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 0.05in;
        }

        .equipment-section {
            border: 2px solid #000;
            padding: 0.1in;
            margin-top: 0.1in;
            grid-column: 1 / -1;
        }

        .features-section {
            border: 2px solid #000;
            padding: 0.1in;
            margin-top: 0.1in;
            grid-column: 1 / -1;
        }

        .proficiency-bonus {
            text-align: center;
            font-size: 14pt;
            font-weight: bold;
            border: 2px solid #000;
            padding: 0.1in;
            margin: 0.1in 0;
        }
    </style>
</head>
<body>
    <div class="character-sheet">
        <!-- Header -->
        <div class="header-section">
            <div class="header-field">
                <div class="header-label">Character Name</div>
                <div class="header-value">{{ data.NAME }}</div>
            </div>
            <div class="header-field">
                <div class="header-label">Class & Level</div>
                <div class="header-value">{{ data.CLASS_LEVEL }}</div>
            </div>
            <div class="header-field">
                <div class="header-label">Background</div>
                <div class="header-value">{{ data.BACKGROUND }}</div>
            </div>
            <div class="header-field">
                <div class="header-label">Player Name</div>
                <div class="header-value">{{ data.PLAYER_NAME or '_________________' }}</div>
            </div>
            <div class="header-field">
                <div class="header-label">Race</div>
                <div class="header-value">{{ data.RACE }}</div>
            </div>
            <div class="header-field">
                <div class="header-label">Alignment</div>
                <div class="header-value">{{ data.ALIGNMENT }}</div>
            </div>
            <div class="header-field">
                <div class="header-label">Experience Points</div>
                <div class="header-value">{{ data.XP }}</div>
            </div>
        </div>

        <!-- Ability Scores -->
        <div class="ability-scores">
            <div class="section-title">Ability Scores</div>
            <div class="proficiency-bonus">Proficiency Bonus: +{{ data.PROF_BONUS }}</div>

            <!-- Strength -->
            <div class="ability-score-box">
                <div class="ability-name">Strength</div>
                <div class="ability-value">{{ data.STR }}</div>
                <div class="ability-modifier">{{ data.STR_MOD }}</div>
                <div class="saving-throw">
                    <span class="checkbox {{ 'checked' if data.STR_SAVE_PROF else '' }}"></span>
                    <span>Save: {{ data.STR_SAVE }}</span>
                </div>
            </div>

            <!-- Dexterity -->
            <div class="ability-score-box">
                <div class="ability-name">Dexterity</div>
                <div class="ability-value">{{ data.DEX }}</div>
                <div class="ability-modifier">{{ data.DEX_MOD }}</div>
                <div class="saving-throw">
                    <span class="checkbox {{ 'checked' if data.DEX_SAVE_PROF else '' }}"></span>
                    <span>Save: {{ data.DEX_SAVE }}</span>
                </div>
            </div>

            <!-- Constitution -->
            <div class="ability-score-box">
                <div class="ability-name">Constitution</div>
                <div class="ability-value">{{ data.CON }}</div>
                <div class="ability-modifier">{{ data.CON_MOD }}</div>
                <div class="saving-throw">
                    <span class="checkbox {{ 'checked' if data.CON_SAVE_PROF else '' }}"></span>
                    <span>Save: {{ data.CON_SAVE }}</span>
                </div>
            </div>

            <!-- Intelligence -->
            <div class="ability-score-box">
                <div class="ability-name">Intelligence</div>
                <div class="ability-value">{{ data.INT }}</div>
                <div class="ability-modifier">{{ data.INT_MOD }}</div>
                <div class="saving-throw">
                    <span class="checkbox {{ 'checked' if data.INT_SAVE_PROF else '' }}"></span>
                    <span>Save: {{ data.INT_SAVE }}</span>
                </div>
            </div>

            <!-- Wisdom -->
            <div class="ability-score-box">
                <div class="ability-name">Wisdom</div>
                <div class="ability-value">{{ data.WIS }}</div>
                <div class="ability-modifier">{{ data.WIS_MOD }}</div>
                <div class="saving-throw">
                    <span class="checkbox {{ 'checked' if data.WIS_SAVE_PROF else '' }}"></span>
                    <span>Save: {{ data.WIS_SAVE }}</span>
                </div>
            </div>

            <!-- Charisma -->
            <div class="ability-score-box">
                <div class="ability-name">Charisma</div>
                <div class="ability-value">{{ data.CHA }}</div>
                <div class="ability-modifier">{{ data.CHA_MOD }}</div>
                <div class="saving-throw">
                    <span class="checkbox {{ 'checked' if data.CHA_SAVE_PROF else '' }}"></span>
                    <span>Save: {{ data.CHA_SAVE }}</span>
                </div>
            </div>
        </div>

        <!-- Skills -->
        <div class="skills-section">
            <div class="section-title">Skills</div>
            <div class="skill-row">
                <span class="checkbox {{ 'checked' if data.ACROBATICS_PROF else '' }}"></span>
                <span class="skill-name">Acrobatics (DEX)</span>
                <span class="skill-modifier">{{ data.ACROBATICS }}</span>
            </div>
            <div class="skill-row">
                <span class="checkbox {{ 'checked' if data.ANIMAL_HANDLING_PROF else '' }}"></span>
                <span class="skill-name">Animal Handling (WIS)</span>
                <span class="skill-modifier">{{ data.ANIMAL_HANDLING }}</span>
            </div>
            <div class="skill-row">
                <span class="checkbox {{ 'checked' if data.ARCANA_PROF else '' }}"></span>
                <span class="skill-name">Arcana (INT)</span>
                <span class="skill-modifier">{{ data.ARCANA }}</span>
            </div>
            <div class="skill-row">
                <span class="checkbox {{ 'checked' if data.ATHLETICS_PROF else '' }}"></span>
                <span class="skill-name">Athletics (STR)</span>
                <span class="skill-modifier">{{ data.ATHLETICS }}</span>
            </div>
            <div class="skill-row">
                <span class="checkbox {{ 'checked' if data.DECEPTION_PROF else '' }}"></span>
                <span class="skill-name">Deception (CHA)</span>
                <span class="skill-modifier">{{ data.DECEPTION }}</span>
            </div>
            <div class="skill-row">
                <span class="checkbox {{ 'checked' if data.HISTORY_PROF else '' }}"></span>
                <span class="skill-name">History (INT)</span>
                <span class="skill-modifier">{{ data.HISTORY }}</span>
            </div>
            <div class="skill-row">
                <span class="checkbox {{ 'checked' if data.INSIGHT_PROF else '' }}"></span>
                <span class="skill-name">Insight (WIS)</span>
                <span class="skill-modifier">{{ data.INSIGHT }}</span>
            </div>
            <div class="skill-row">
                <span class="checkbox {{ 'checked' if data.INTIMIDATION_PROF else '' }}"></span>
                <span class="skill-name">Intimidation (CHA)</span>
                <span class="skill-modifier">{{ data.INTIMIDATION }}</span>
            </div>
            <div class="skill-row">
                <span class="checkbox {{ 'checked' if data.INVESTIGATION_PROF else '' }}"></span>
                <span class="skill-name">Investigation (INT)</span>
                <span class="skill-modifier">{{ data.INVESTIGATION }}</span>
            </div>
            <div class="skill-row">
                <span class="checkbox {{ 'checked' if data.MEDICINE_PROF else '' }}"></span>
                <span class="skill-name">Medicine (WIS)</span>
                <span class="skill-modifier">{{ data.MEDICINE }}</span>
            </div>
            <div class="skill-row">
                <span class="checkbox {{ 'checked' if data.NATURE_PROF else '' }}"></span>
                <span class="skill-name">Nature (INT)</span>
                <span class="skill-modifier">{{ data.NATURE }}</span>
            </div>
            <div class="skill-row">
                <span class="checkbox {{ 'checked' if data.PERCEPTION_PROF else '' }}"></span>
                <span class="skill-name">Perception (WIS)</span>
                <span class="skill-modifier">{{ data.PERCEPTION }}</span>
            </div>
            <div class="skill-row">
                <span class="checkbox {{ 'checked' if data.PERFORMANCE_PROF else '' }}"></span>
                <span class="skill-name">Performance (CHA)</span>
                <span class="skill-modifier">{{ data.PERFORMANCE }}</span>
            </div>
            <div class="skill-row">
                <span class="checkbox {{ 'checked' if data.PERSUASION_PROF else '' }}"></span>
                <span class="skill-name">Persuasion (CHA)</span>
                <span class="skill-modifier">{{ data.PERSUASION }}</span>
            </div>
            <div class="skill-row">
                <span class="checkbox {{ 'checked' if data.RELIGION_PROF else '' }}"></span>
                <span class="skill-name">Religion (INT)</span>
                <span class="skill-modifier">{{ data.RELIGION }}</span>
            </div>
            <div class="skill-row">
                <span class="checkbox {{ 'checked' if data.SLEIGHT_OF_HAND_PROF else '' }}"></span>
                <span class="skill-name">Sleight of Hand (DEX)</span>
                <span class="skill-modifier">{{ data.SLEIGHT_OF_HAND }}</span>
            </div>
            <div class="skill-row">
                <span class="checkbox {{ 'checked' if data.STEALTH_PROF else '' }}"></span>
                <span class="skill-name">Stealth (DEX)</span>
                <span class="skill-modifier">{{ data.STEALTH }}</span>
            </div>
            <div class="skill-row">
                <span class="checkbox {{ 'checked' if data.SURVIVAL_PROF else '' }}"></span>
                <span class="skill-name">Survival (WIS)</span>
                <span class="skill-modifier">{{ data.SURVIVAL }}</span>
            </div>
        </div>

        <!-- Right Column -->
        <div class="right-column">
            <!-- Combat Stats -->
            <div class="combat-stats">
                <div class="section-title">Combat</div>
                <div class="stat-box">
                    <div class="stat-label">Armor Class</div>
                    <div class="stat-value">{{ data.AC }}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Initiative</div>
                    <div class="stat-value">{{ data.INITIATIVE }}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Speed</div>
                    <div class="stat-value">{{ data.SPEED }} ft</div>
                </div>
            </div>

            <!-- Hit Points -->
            <div class="hp-section">
                <div class="section-title">Hit Points</div>
                <div class="hp-boxes">
                    <div class="stat-box">
                        <div class="stat-label">Current</div>
                        <div class="stat-value">{{ data.CURRENT_HP }}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Maximum</div>
                        <div class="stat-value">{{ data.MAX_HP }}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Temporary</div>
                        <div class="stat-value">{{ data.TEMP_HP }}</div>
                    </div>
                </div>
                <div class="stat-box" style="margin-top: 0.1in;">
                    <div class="stat-label">Hit Dice</div>
                    <div class="stat-value">{{ data.HIT_DICE }}</div>
                </div>
            </div>
        </div>

        <!-- Equipment -->
        <div class="equipment-section">
            <div class="section-title">Equipment</div>
            <div style="font-size: 9pt; line-height: 1.4;">
                <strong>Coins:</strong> PP: {{ data.PP }}, GP: {{ data.GP }}, EP: {{ data.EP }}, SP: {{ data.SP }}, CP: {{ data.CP }}<br>
                <strong>Equipment:</strong><br>
                {{ data.EQUIPMENT }}
            </div>
        </div>

        <!-- Features & Traits -->
        <div class="features-section">
            <div class="section-title">Features & Traits</div>
            <div style="font-size: 9pt; line-height: 1.4;">
                <strong>Class Features:</strong><br>
                {{ data.CLASS_FEATURES }}<br><br>
                <strong>Racial Traits:</strong><br>
                {{ data.RACIAL_TRAITS }}<br><br>
                <strong>Proficiencies:</strong> Armor: {{ data.ARMOR_PROF }}, Weapons: {{ data.WEAPON_PROF }}, Tools: {{ data.TOOL_PROF }}, Languages: {{ data.LANGUAGES }}
            </div>
        </div>
    </div>
</body>
</html>"""

    template = Template(template_str)
    return template.render(data=data)


def generate_character_sheet_pdf(
    being: Being,
    character: DnD5eCharacter | None = None,
    output_path: Path | None = None,
    project_path: Path | None = None,
) -> Path:
    """
    Generate character sheet as .pdf (on demand) using official D&D 5e format.
    """
    if project_path is None:
        project_path = Path.cwd()

    if output_path is None:
        being_dir = project_path / "_hidden" / ".truth" / "beings" / being.being_id
        being_dir.mkdir(parents=True, exist_ok=True)
        output_path = being_dir / "character_sheet.pdf"

    # Get character data
    data = being_to_character_data(being, character)

    # Convert to official D&D 5e HTML format
    html_content = convert_to_dnd5e_html(data)

    # Generate PDF using WeasyPrint directly
    from weasyprint import HTML

    HTML(string=html_content).write_pdf(output_path)

    return output_path


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
| **Strength** | {data["STR"]} | {data["STR_MOD"]} | {data["STR_SAVE"]} | {data["STR_SAVE_PROF"]} |
| **Dexterity** | {data["DEX"]} | {data["DEX_MOD"]} | {data["DEX_SAVE"]} | {data["DEX_SAVE_PROF"]} |
| **Constitution** | {data["CON"]} | {data["CON_MOD"]} | {data["CON_SAVE"]} | {data["CON_SAVE_PROF"]} |
| **Intelligence** | {data["INT"]} | {data["INT_MOD"]} | {data["INT_SAVE"]} | {data["INT_SAVE_PROF"]} |
| **Wisdom** | {data["WIS"]} | {data["WIS_MOD"]} | {data["WIS_SAVE"]} | {data["WIS_SAVE_PROF"]} |
| **Charisma** | {data["CHA"]} | {data["CHA_MOD"]} | {data["CHA_SAVE"]} | {data["CHA_SAVE_PROF"]} |

**Proficiency Bonus:** +{data["PROF_BONUS"]}

---

## Skills

| Skill | Ability | Modifier | Proficiency |
|-------|---------|----------|-------------|
| **Acrobatics** | DEX | {data["ACROBATICS"]:+} | {data["ACROBATICS_PROF"]} |
| **Animal Handling** | WIS | {data["ANIMAL_HANDLING"]:+} | {data["ANIMAL_HANDLING_PROF"]} |
| **Arcana** | INT | {data["ARCANA"]:+} | {data["ARCANA_PROF"]} |
| **Athletics** | STR | {data["ATHLETICS"]:+} | {data["ATHLETICS_PROF"]} |
| **Deception** | CHA | {data["DECEPTION"]:+} | {data["DECEPTION_PROF"]} |
| **History** | INT | {data["HISTORY"]:+} | {data["HISTORY_PROF"]} |
| **Insight** | WIS | {data["INSIGHT"]:+} | {data["INSIGHT_PROF"]} |
| **Intimidation** | CHA | {data["INTIMIDATION"]:+} | {data["INTIMIDATION_PROF"]} |
| **Investigation** | INT | {data["INVESTIGATION"]:+} | {data["INVESTIGATION_PROF"]} |
| **Medicine** | WIS | {data["MEDICINE"]:+} | {data["MEDICINE_PROF"]} |
| **Nature** | INT | {data["NATURE"]:+} | {data["NATURE_PROF"]} |
| **Perception** | WIS | {data["PERCEPTION"]:+} | {data["PERCEPTION_PROF"]} |
| **Performance** | CHA | {data["PERFORMANCE"]:+} | {data["PERFORMANCE_PROF"]} |
| **Persuasion** | CHA | {data["PERSUASION"]:+} | {data["PERSUASION_PROF"]} |
| **Religion** | INT | {data["RELIGION"]:+} | {data["RELIGION_PROF"]} |
| **Sleight of Hand** | DEX | {data["SLEIGHT_OF_HAND"]:+} | {data["SLEIGHT_OF_HAND_PROF"]} |
| **Stealth** | DEX | {data["STEALTH"]:+} | {data["STEALTH_PROF"]} |
| **Survival** | WIS | {data["SURVIVAL"]:+} | {data["SURVIVAL_PROF"]} |

---

## Combat

**Armor Class (AC):** {data["AC"]}
**Initiative:** {data["INITIATIVE"]}
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

    # Determine project root
    project_root = Path(__file__).parent.parent.parent

    # Create a test Being
    from src.waft.being import BeingSystem

    being_system = BeingSystem(project_path=project_root)
    being = being_system.spawn_being(
        reality_id="test_reality",
        parent_being_id=None,
        initial_skills={"strength": 60.0, "dexterity": 45.0},
    )

    print(f"\n✅ Created test Being: {being.being_id}")
    print("   Note: .txt character sheet should have been auto-generated")

    # Generate .md (on demand)
    print("\n📄 Generating .md character sheet (on demand)...")
    md_path = generate_character_sheet_md(being, project_path=project_root)
    print(f"   ✅ Generated: {md_path}")

    # Generate .pdf (on demand)
    print("\n📄 Generating .pdf character sheet (on demand)...")
    pdf_path = generate_character_sheet_pdf(being, project_path=project_root)
    print(f"   ✅ Generated: {pdf_path}")

    print("\n" + "=" * 60)
    print("✅ Character Sheet Generation Complete!")
    print("=" * 60)
    print("\nGenerated Files:")
    print("   📄 .txt: (auto-generated in being directory)")
    print(f"   📄 .md: {md_path.name}")
    print(f"   📄 .pdf: {pdf_path.name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
