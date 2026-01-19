"""
DnD Game Visualization Typst Template Wrapper
==============================================

Python wrapper for D&D 5e Typst templates to generate game visualizations as PDFs.
Supports character sheets, stat blocks, encounters, campaign state, and more.

Uses:
- @preview/wenyuan-campaign:0.1.2 - Campaign documents and character sheets
- @preview/dragonling:0.2.0 - Stat blocks and general D&D 5e content

Category: game
Tags: [typst, dnd, d&d, 5e, rpg, character-sheet, stat-block]
Source: typst-templates
"""

import re
from pathlib import Path
from typing import Literal, Optional, List, Dict, Any
from dataclasses import dataclass, field

from ..compiler import TypstCompiler


# Type definitions
DocumentType = Literal[
    "character_sheet",
    "stat_block",
    "encounter",
    "campaign_state",
    "session_log",
    "spell_reference",
    "item_reference"
]
TemplatePackage = Literal["wenyuan-campaign", "dragonling"]


@dataclass
class Character:
    """Character data structure with validation."""
    name: str
    class_level: str  # e.g., "Fighter 5"
    race: str
    background: Optional[str] = None
    alignment: Optional[str] = None
    ability_scores: Optional[Dict[str, int]] = None  # {"STR": 16, "DEX": 14, ...}
    hit_points: Optional[Dict[str, int]] = None  # {"current": 45, "max": 50}
    armor_class: Optional[int] = None
    skills: Optional[List[Dict[str, Any]]] = None
    equipment: Optional[List[str]] = None
    spells: Optional[List[str]] = None
    
    def __post_init__(self):
        """Validate character data after initialization."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Character name must be a non-empty string")
        if not self.class_level or not isinstance(self.class_level, str):
            raise ValueError("Character class_level must be a non-empty string")
        if not self.race or not isinstance(self.race, str):
            raise ValueError("Character race must be a non-empty string")
        # Validate ability scores if provided
        if self.ability_scores:
            valid_abilities = {"STR", "DEX", "CON", "INT", "WIS", "CHA"}
            for ability in self.ability_scores:
                if ability not in valid_abilities:
                    raise ValueError(
                        f"Invalid ability score: {ability}. "
                        f"Must be one of {valid_abilities}"
                    )
                score = self.ability_scores[ability]
                if not isinstance(score, int) or score < 1 or score > 30:
                    raise ValueError(
                        f"Ability score {ability} must be an integer between 1 and 30, "
                        f"got {score}"
                    )


@dataclass
class StatBlock:
    """Monster/NPC stat block data structure."""
    name: str
    size_type: str  # e.g., "Medium humanoid (human)"
    armor_class: int
    hit_points: int
    speed: str  # e.g., "30 ft."
    ability_scores: Dict[str, int]
    skills: Optional[List[str]] = None
    damage_resistances: Optional[List[str]] = None
    damage_immunities: Optional[List[str]] = None
    condition_immunities: Optional[List[str]] = None
    senses: Optional[str] = None
    languages: Optional[str] = None
    challenge_rating: Optional[str] = None
    traits: Optional[List[Dict[str, str]]] = None  # [{"name": "Trait Name", "text": "Description"}]
    actions: Optional[List[Dict[str, str]]] = None
    legendary_actions: Optional[List[Dict[str, str]]] = None
    
    def __post_init__(self):
        """Validate stat block data."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Stat block name must be a non-empty string")
        if not isinstance(self.armor_class, int) or self.armor_class < 0:
            raise ValueError("Armor class must be a non-negative integer")
        if not isinstance(self.hit_points, int) or self.hit_points < 1:
            raise ValueError("Hit points must be a positive integer")
        # Validate ability scores
        valid_abilities = {"STR", "DEX", "CON", "INT", "WIS", "CHA"}
        for ability in self.ability_scores:
            if ability not in valid_abilities:
                raise ValueError(
                    f"Invalid ability score: {ability}. "
                    f"Must be one of {valid_abilities}"
                )


@dataclass
class EncounterParticipant:
    """Participant in an encounter (PC or NPC)."""
    name: str
    initiative: int
    is_player: bool
    current_hp: Optional[int] = None
    max_hp: Optional[int] = None
    armor_class: Optional[int] = None
    conditions: Optional[List[str]] = None
    
    def __post_init__(self):
        """Validate encounter participant."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Participant name must be a non-empty string")
        if not isinstance(self.initiative, int):
            raise ValueError("Initiative must be an integer")


def _sanitize_typst_content(content: str) -> str:
    """
    Sanitize user-provided content to prevent Typst injection.
    
    Escapes special Typst characters that could be used for code injection.
    
    Args:
        content: User-provided content string
        
    Returns:
        Sanitized content string
    """
    if not content:
        return ""
    
    # Escape special Typst characters
    # Note: Typst uses # for commands, { } for blocks, [ ] for arguments, ( ) for functions
    # We escape these to prevent injection
    replacements = {
        "#": r"\#",
        "{": r"\{",
        "}": r"\}",
        "[": r"\[",
        "]": r"\]",
        "(": r"\(",
        ")": r"\)",
    }
    
    sanitized = content
    for char, escaped in replacements.items():
        sanitized = sanitized.replace(char, escaped)
    
    return sanitized


def _sanitize_name(name: str) -> str:
    """
    Sanitize names to prevent Typst injection.
    
    Args:
        name: Name string to sanitize
        
    Returns:
        Sanitized name string
    """
    if not name:
        return ""
    
    # Remove or escape dangerous characters
    # Allow alphanumeric, spaces, hyphens, apostrophes
    sanitized = re.sub(r'[^a-zA-Z0-9\s\-\']', '', name)
    # Escape remaining special Typst characters
    return _sanitize_typst_content(sanitized)


def _build_character_sheet_typst(character: Character) -> str:
    """
    Build Typst content for a character sheet.
    
    Args:
        character: Character data
        
    Returns:
        Typst content string for character sheet
    """
    name = _sanitize_name(character.name)
    class_level = _sanitize_typst_content(character.class_level)
    race = _sanitize_name(character.race)
    
    typst_lines = [
        f"== {name}",
        f"*{class_level}*",
        f"*{race}*",
    ]
    
    if character.background:
        typst_lines.append(f"*Background: {_sanitize_typst_content(character.background)}*")
    
    if character.alignment:
        typst_lines.append(f"*Alignment: {_sanitize_typst_content(character.alignment)}*")
    
    typst_lines.append("")
    
    # Ability scores
    if character.ability_scores:
        typst_lines.append("=== Ability Scores")
        for ability, score in sorted(character.ability_scores.items()):
            modifier = (score - 10) // 2
            modifier_str = f"+{modifier}" if modifier >= 0 else str(modifier)
            typst_lines.append(f"- *{ability}*: {score} ({modifier_str})")
        typst_lines.append("")
    
    # Combat stats
    if character.armor_class is not None:
        typst_lines.append(f"*Armor Class*: {character.armor_class}")
    
    if character.hit_points:
        current = character.hit_points.get("current", "?")
        max_hp = character.hit_points.get("max", "?")
        typst_lines.append(f"*Hit Points*: {current} / {max_hp}")
    
    typst_lines.append("")
    
    # Skills
    if character.skills:
        typst_lines.append("=== Skills")
        for skill in character.skills:
            if isinstance(skill, dict):
                skill_name = skill.get("name", "Unknown")
                skill_value = skill.get("value", "")
                skill_mod = skill.get("modifier", "")
                typst_lines.append(f"- *{_sanitize_typst_content(skill_name)}*: {skill_value} {skill_mod}")
            else:
                typst_lines.append(f"- {_sanitize_typst_content(str(skill))}")
        typst_lines.append("")
    
    # Equipment
    if character.equipment:
        typst_lines.append("=== Equipment")
        for item in character.equipment:
            typst_lines.append(f"- {_sanitize_typst_content(item)}")
        typst_lines.append("")
    
    # Spells
    if character.spells:
        typst_lines.append("=== Spells")
        for spell in character.spells:
            typst_lines.append(f"- {_sanitize_typst_content(spell)}")
        typst_lines.append("")
    
    return "\n".join(typst_lines)


def _build_stat_block_typst(stat_block: StatBlock) -> str:
    """
    Build Typst content for a stat block.
    
    Args:
        stat_block: Stat block data
        
    Returns:
        Typst content string for stat block
    """
    name = _sanitize_name(stat_block.name)
    size_type = _sanitize_typst_content(stat_block.size_type)
    
    typst_lines = [
        f"== {name}",
        f"*{size_type}*",
        "",
        f"*Armor Class* {stat_block.armor_class}",
        f"*Hit Points* {stat_block.hit_points}",
        f"*Speed* {_sanitize_typst_content(stat_block.speed)}",
        "",
    ]
    
    # Ability scores
    typst_lines.append("=== Ability Scores")
    for ability in ["STR", "DEX", "CON", "INT", "WIS", "CHA"]:
        if ability in stat_block.ability_scores:
            score = stat_block.ability_scores[ability]
            modifier = (score - 10) // 2
            modifier_str = f"+{modifier}" if modifier >= 0 else str(modifier)
            typst_lines.append(f"- *{ability}*: {score} ({modifier_str})")
    typst_lines.append("")
    
    # Skills and other stats
    if stat_block.skills:
        typst_lines.append(f"*Skills*: {', '.join(_sanitize_typst_content(s) for s in stat_block.skills)}")
    
    if stat_block.damage_resistances:
        typst_lines.append(f"*Damage Resistances*: {', '.join(_sanitize_typst_content(d) for d in stat_block.damage_resistances)}")
    
    if stat_block.damage_immunities:
        typst_lines.append(f"*Damage Immunities*: {', '.join(_sanitize_typst_content(d) for d in stat_block.damage_immunities)}")
    
    if stat_block.condition_immunities:
        typst_lines.append(f"*Condition Immunities*: {', '.join(_sanitize_typst_content(c) for c in stat_block.condition_immunities)}")
    
    if stat_block.senses:
        typst_lines.append(f"*Senses*: {_sanitize_typst_content(stat_block.senses)}")
    
    if stat_block.languages:
        typst_lines.append(f"*Languages*: {_sanitize_typst_content(stat_block.languages)}")
    
    if stat_block.challenge_rating:
        typst_lines.append(f"*Challenge Rating*: {_sanitize_typst_content(stat_block.challenge_rating)}")
    
    typst_lines.append("")
    
    # Traits
    if stat_block.traits:
        typst_lines.append("=== Traits")
        for trait in stat_block.traits:
            trait_name = trait.get("name", "Unknown")
            trait_text = trait.get("text", "")
            typst_lines.append(f"*{_sanitize_typst_content(trait_name)}*")
            typst_lines.append(_sanitize_typst_content(trait_text))
            typst_lines.append("")
    
    # Actions
    if stat_block.actions:
        typst_lines.append("=== Actions")
        for action in stat_block.actions:
            action_name = action.get("name", "Unknown")
            action_text = action.get("text", "")
            typst_lines.append(f"*{_sanitize_typst_content(action_name)}*")
            typst_lines.append(_sanitize_typst_content(action_text))
            typst_lines.append("")
    
    # Legendary Actions
    if stat_block.legendary_actions:
        typst_lines.append("=== Legendary Actions")
        for la in stat_block.legendary_actions:
            la_name = la.get("name", "Unknown")
            la_text = la.get("text", "")
            typst_lines.append(f"*{_sanitize_typst_content(la_name)}*")
            typst_lines.append(_sanitize_typst_content(la_text))
            typst_lines.append("")
    
    return "\n".join(typst_lines)


def _build_encounter_typst(participants: List[EncounterParticipant]) -> str:
    """
    Build Typst content for an encounter visualization.
    
    Args:
        participants: List of encounter participants
        
    Returns:
        Typst content string for encounter
    """
    # Sort by initiative (descending)
    sorted_participants = sorted(participants, key=lambda p: p.initiative, reverse=True)
    
    typst_lines = [
        "== Encounter - Initiative Order",
        "",
    ]
    
    for i, participant in enumerate(sorted_participants, 1):
        name = _sanitize_name(participant.name)
        player_type = "PC" if participant.is_player else "NPC"
        typst_lines.append(f"{i}. *{name}* ({player_type}) - Initiative: {participant.initiative}")
        
        if participant.armor_class is not None:
            typst_lines.append(f"   AC: {participant.armor_class}")
        
        if participant.current_hp is not None and participant.max_hp is not None:
            typst_lines.append(f"   HP: {participant.current_hp} / {participant.max_hp}")
        
        if participant.conditions:
            conditions_str = ", ".join(_sanitize_typst_content(c) for c in participant.conditions)
            typst_lines.append(f"   Conditions: {conditions_str}")
        
        typst_lines.append("")
    
    return "\n".join(typst_lines)


def generate_dnd_game(
    title: str,
    content: str,
    output_path: Path,
    document_type: DocumentType = "character_sheet",
    template_package: TemplatePackage = "wenyuan-campaign",
    characters: Optional[List[Character]] = None,
    stat_blocks: Optional[List[StatBlock]] = None,
    encounter_participants: Optional[List[EncounterParticipant]] = None,
    show_rules: bool = False,
    **kwargs
) -> Path:
    """
    Generate PDF using D&D 5e Typst templates.
    
    Supports multiple document types:
    - character_sheet: D&D 5e character sheets
    - stat_block: Monster/NPC stat blocks
    - encounter: Combat encounter visualization
    - campaign_state: Campaign state documentation
    - session_log: Game session documentation
    - spell_reference: Spell reference cards
    - item_reference: Magic item reference cards
    
    Template packages:
    - wenyuan-campaign: Best for campaign documents and character sheets
    - dragonling: Best for stat blocks and general D&D 5e content
    
    Args:
        title: Document title
        content: Custom content (Typst markup, will be sanitized)
        output_path: Where to save PDF
        document_type: Type of D&D document to generate
        template_package: Which Typst package to use
        characters: List of Character objects (for character_sheet type)
        stat_blocks: List of StatBlock objects (for stat_block type)
        encounter_participants: List of EncounterParticipant objects (for encounter type)
        show_rules: Whether to include D&D 5e rules reference
        **kwargs: Additional template parameters
        
    Returns:
        Path to generated PDF
        
    Raises:
        ValueError: If invalid data provided
        RuntimeError: If Typst compilation fails
    """
    # Validate document type
    valid_document_types = [
        "character_sheet", "stat_block", "encounter", "campaign_state",
        "session_log", "spell_reference", "item_reference"
    ]
    if document_type not in valid_document_types:
        raise ValueError(
            f"Invalid document_type: {document_type}. "
            f"Must be one of {valid_document_types}"
        )
    
    # Validate template package
    valid_packages = ["wenyuan-campaign", "dragonling"]
    if template_package not in valid_packages:
        raise ValueError(
            f"Invalid template_package: {template_package}. "
            f"Must be one of {valid_packages}"
        )
    
    # Sanitize title and content
    sanitized_title = _sanitize_name(title)
    sanitized_content = _sanitize_typst_content(content)
    
    # Build Typst content
    typst_parts = []
    
    # Import template package
    if template_package == "wenyuan-campaign":
        typst_parts.append('#import "@preview/wenyuan-campaign:0.1.2": *')
    elif template_package == "dragonling":
        typst_parts.append('#import "@preview/dragonling:0.2.0": *')
    
    typst_parts.append("")
    typst_parts.append("#set page(margin: 1in)")
    typst_parts.append("")
    typst_parts.append(f"= {sanitized_title}")
    typst_parts.append("")
    
    # Add document-specific content
    if document_type == "character_sheet" and characters:
        for character in characters:
            typst_parts.append(_build_character_sheet_typst(character))
            typst_parts.append("")
    
    elif document_type == "stat_block" and stat_blocks:
        for stat_block in stat_blocks:
            typst_parts.append(_build_stat_block_typst(stat_block))
            typst_parts.append("")
    
    elif document_type == "encounter" and encounter_participants:
        typst_parts.append(_build_encounter_typst(encounter_participants))
        typst_parts.append("")
    
    # Add rules section if requested
    if show_rules:
        typst_parts.append("== D&D 5e Rules Reference")
        typst_parts.append("")
        typst_parts.append("This document includes D&D 5e rules reference.")
        typst_parts.append("")
    
    # Add custom content
    if sanitized_content:
        typst_parts.append("== Additional Content")
        typst_parts.append("")
        typst_parts.append(sanitized_content)
        typst_parts.append("")
    
    # Combine all parts
    typst_content = "\n".join(typst_parts)
    
    # Compile to PDF
    compiler = TypstCompiler()
    pdf_path = compiler.compile(typst_content, output_path)
    
    return pdf_path
