"""
DnD Mechanics Book Typst Template Wrapper
========================================

Generate a WAFT DnD mechanics book using Typst templates.

Category: book
Tags: [typst, dnd, rpg, book, mechanics]
Source: typst-universe
"""

from pathlib import Path
from typing import Literal

from ..compiler import TypstCompiler

TemplateType = Literal["min-book", "owlbear", "dragonling", "wenyuan-campaign"]

DEFAULT_CONTENT = """= Introduction
WAFT turns software development into a DnD flavored loop where AI agents evolve through ethical choices. This book summarizes the core mechanics used by the WAFT game system.

== Quick Start
#list(
  [Choose a quest from the work effort queue.],
  [Roll or assign ability scores for the being.],
  [Resolve encounters using skill checks or combat actions.],
  [Award XP, karma, and scint based on outcomes.],
  [Level up and evolve when thresholds are met.],
)

= Character Creation
WAFT uses a Warforged Wizard archetype as the default being. Adjust class, race, and features as needed.

== Character Sheet Components
#table(
  columns: (auto, auto, 1fr),
  table.header([Component], [Example], [Notes]),
  [Ability Scores], [INT 16, WIS 14], [STR, DEX, CON, INT, WIS, CHA],
  [Hit Points], [45 / 50], [Current and max HP],
  [Armor Class], [15], [10 + DEX + armor],
  [Spell Slots], [Level 1: 3 / 4], [Available spell slots],
  [Hit Dice], [5 / 5 d6], [Recovery resource],
  [Level], [3], [Character level],
  [XP], [1200], [Experience points],
)

= Core Mechanics

== Ability Scores
#table(
  columns: (auto, auto, 1fr),
  table.header([Ability], [Score Range], [Use Case]),
  [Strength (STR)], [8-15], [Physical tasks, carrying capacity],
  [Dexterity (DEX)], [10-16], [Armor class, initiative, finesse weapons],
  [Constitution (CON)], [12-16], [Hit points, saving throws, endurance],
  [Intelligence (INT)], [14-18], [Spellcasting, investigation, logic],
  [Wisdom (WIS)], [12-16], [Perception, insight, spell saves],
  [Charisma (CHA)], [10-14], [Social interactions, spellcasting],
)

== Combat Actions
#table(
  columns: (auto, 1fr),
  table.header([Action], [Description]),
  [Attack], [Weapon or spell attack],
  [Skill Check], [Ability + proficiency vs DC],
  [Saving Throw], [Resist or avoid an effect],
  [Spell Casting], [Use a spell slot to cast],
  [Movement], [Move up to speed per turn],
)

== Level Progression (Sample)
#table(
  columns: (auto, auto, auto, 1fr),
  table.header([Level], [XP], [Prof Bonus], [Feature]),
  [1], [0], [+2], [Spellcasting, awakened spellbook],
  [2], [300], [+2], [Arcane recovery],
  [3], [900], [+2], [Second level spells],
  [4], [2700], [+2], [Ability score improvement],
  [5], [6500], [+3], [Third level spells],
)

== Spell Slots (Sample)
#table(
  columns: (auto, auto, 1fr),
  table.header([Spell Level], [Slots], [Example Spells]),
  [1st], [4], [Mage Hand, Detect Magic, Shield],
  [2nd], [3], [Mirror Image, Misty Step],
  [3rd], [2], [Counterspell, Fireball],
  [4th], [1], [Polymorph, Dimension Door],
)

= Quest System

== Quest Types
#table(
  columns: (auto, auto, auto, 1fr),
  table.header([Type], [Duration], [Rewards], [Notes]),
  [Quick Quest], [1-2 hours], [Low], [Single ticket],
  [Standard Quest], [1-2 days], [Medium], [Multiple tickets],
  [Epic Quest], [1-2 weeks], [High], [Complex work effort],
  [Campaign], [1+ months], [Very high], [Multiple work efforts],
)

== Encounter Types
#table(
  columns: (auto, 1fr, 1fr),
  table.header([Type], [Description], [Priority]),
  [Combat], [Direct conflict], [P0 Critical],
  [Skill Challenge], [Problem solving], [P1 High],
  [Social], [Negotiation or persuasion], [P2 Routine],
  [Exploration], [Discovery or investigation], [P3 Backlog],
)

== Difficulty Levels
#table(
  columns: (auto, auto, auto, 1fr),
  table.header([Difficulty], [XP Reward], [Scint Multiplier], [Notes]),
  [Easy], [25], [1.0x], [Low risk],
  [Medium], [50], [1.5x], [Moderate challenge],
  [Hard], [100], [2.0x], [Significant challenge],
  [Deadly], [200+], [3.0x], [Extreme challenge],
)

= Karma System
Karma ranges from -100 to +100 and influences evolution paths.

#list(
  [High order (50 to 100): Architect path with defense and structure bonuses.],
  [Neutral (-10 to 10): Balanced path with adaptable traits.],
  [High chaos (-100 to -50): Glitch path with disruption and offense bonuses.],
)

= Scint Economy
Scint represents raw creation energy earned through synthesis and problem solving.

#list(
  [Scint pool typically ranges 0 to 200.],
  [Spells consume scint by level, from 0 for cantrips to 30+ for high level spells.],
  [Evolution checks trigger when scint exceeds thresholds.],
)

= Campaign Loop
#list(
  [Plan: select quests and prepare the party.],
  [Engage: run encounters, exploration, and lore.],
  [Resolve: grant XP, karma, and scint.],
  [Evolve: level up and apply path bonuses.],
)
"""


def _escape_typst_string(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', "\\\"")


def _format_authors(authors: str | list[str] | None) -> str:
    if not authors:
        return "WAFT"
    if isinstance(authors, list):
        return ", ".join(authors)
    return authors


def generate_dnd_mechanics_book(
    title: str,
    output_path: Path,
    template: TemplateType = "min-book",
    subtitle: str | None = "Core rules and systems",
    authors: str | list[str] | None = "WAFT",
    content: str | None = None,
    **kwargs,
) -> Path:
    """
    Generate a WAFT DnD mechanics book using Typst templates.

    Args:
        title: Book title
        output_path: Where to save the PDF
        template: Typst template to use
        subtitle: Optional subtitle
        authors: Author name(s)
        content: Typst content override (defaults to WAFT mechanics)
        **kwargs: Reserved for future template parameters

    Returns:
        Path to generated PDF
    """
    content_body = content or DEFAULT_CONTENT
    safe_title = _escape_typst_string(title)
    safe_subtitle = _escape_typst_string(subtitle) if subtitle else None
    author_text = _escape_typst_string(_format_authors(authors))

    if template == "min-book":
        header = (
            '#import "@preview/min-book:1.3.0": book\n\n'
            "#show: book.with(\n"
            f'  title: "{safe_title}",\n'
            f"  subtitle: {f'\"{safe_subtitle}\"' if safe_subtitle else 'none'},\n"
            f'  authors: "{author_text}",\n'
            ")\n"
        )
    elif template == "owlbear":
        header = '#import "@preview/owlbear:0.0.1": book-template\n\n#show: book-template\n'
    elif template == "dragonling":
        header = (
            '#import "@preview/dragonling:0.2.0": *\n\n'
            "#show: dndmodule.with(\n"
            f'  title: "{safe_title}",\n'
            f"  subtitle: {f'\"{safe_subtitle}\"' if safe_subtitle else 'none'},\n"
            f'  author: "{author_text}",\n'
            ")\n"
        )
    elif template == "wenyuan-campaign":
        header = '#import "@preview/wenyuan-campaign:0.1.2": *\n\n#show: conf.with()\n'
    else:
        raise ValueError(
            "Invalid template. Use one of: min-book, owlbear, dragonling, wenyuan-campaign."
        )

    typst_content = f"{header}\n{content_body}\n"

    compiler = TypstCompiler()
    return compiler.compile(typst_content, output_path)
