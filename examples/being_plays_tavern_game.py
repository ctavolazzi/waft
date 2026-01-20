"""
Being Plays Tavern Game with Scientific Report Generation

Spawns a WAFT Being, has it play the tavern scenario game,
and generates a comprehensive scientific research paper-style PDF report.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console
from rich.panel import Panel

from waft.being import Being, BeingSystem
from waft.core.dnd5e import ArmorType, DnD5eCharacter, DnD5eStats, DnDRoller

console = Console()


class GameEvent:
    """Represents an event during gameplay."""

    def __init__(self, event_type: str, timestamp: str, description: str, data: dict[str, Any]):
        self.event_type = event_type
        self.timestamp = timestamp
        self.description = description
        self.data = data

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "description": self.description,
            "data": self.data,
        }


class TavernGameSession:
    """Manages a game session with event tracking."""

    def __init__(self, being: Being, character: DnD5eCharacter):
        self.being = being
        self.character = character
        self.events: list[GameEvent] = []
        self.choices: list[dict[str, Any]] = []
        self.rolls: list[dict[str, Any]] = []
        self.outcomes: list[dict[str, Any]] = []
        self.start_time = datetime.now().isoformat()
        self.end_time: str | None = None

    def log_event(self, event_type: str, description: str, data: dict[str, Any] = None):
        """Log a game event."""
        event = GameEvent(
            event_type=event_type,
            timestamp=datetime.now().isoformat(),
            description=description,
            data=data or {},
        )
        self.events.append(event)

    def log_choice(self, choice_number: int, choice_text: str, decision: str):
        """Log a player choice."""
        self.choices.append(
            {
                "choice_number": choice_number,
                "choice_text": choice_text,
                "decision": decision,
                "timestamp": datetime.now().isoformat(),
            }
        )
        self.log_event(
            "choice",
            f"Made choice: {choice_text}",
            {"choice_number": choice_number, "decision": decision},
        )

    def log_roll(
        self, roll_type: str, die_roll: int, modifier: int, total: int, dc: int, success: bool
    ):
        """Log a dice roll."""
        self.rolls.append(
            {
                "roll_type": roll_type,
                "die_roll": die_roll,
                "modifier": modifier,
                "total": total,
                "dc": dc,
                "success": success,
                "timestamp": datetime.now().isoformat(),
            }
        )
        self.log_event(
            "roll",
            f"{roll_type} check: {total} vs DC {dc} ({'Success' if success else 'Failure'})",
            {
                "die_roll": die_roll,
                "modifier": modifier,
                "total": total,
                "dc": dc,
                "success": success,
            },
        )

    def log_outcome(self, outcome_type: str, description: str, data: dict[str, Any] = None):
        """Log an outcome."""
        self.outcomes.append(
            {
                "outcome_type": outcome_type,
                "description": description,
                "data": data or {},
                "timestamp": datetime.now().isoformat(),
            }
        )
        self.log_event("outcome", description, data or {})

    def finish(self):
        """Mark session as complete."""
        self.end_time = datetime.now().isoformat()
        self.log_event(
            "session_end", "Game session completed", {"duration": self._calculate_duration()}
        )

    def _calculate_duration(self) -> str:
        """Calculate session duration."""
        if not self.end_time:
            return "N/A"
        start = datetime.fromisoformat(self.start_time)
        end = datetime.fromisoformat(self.end_time)
        duration = end - start
        return f"{duration.total_seconds():.2f} seconds"

    def to_dict(self) -> dict[str, Any]:
        """Convert session to dictionary."""
        return {
            "being_id": self.being.being_id,
            "being_lifetimes": self.being.lifetimes,
            "character_name": self.character.name,
            "character_stats": {
                "strength": self.character.strength,
                "dexterity": self.character.dexterity,
                "constitution": self.character.constitution,
                "intelligence": self.character.intelligence,
                "wisdom": self.character.wisdom,
                "charisma": self.character.charisma,
                "hp": self.character.hp,
                "max_hp": self.character.max_hp,
                "ac": self.character.ac,
            },
            "start_time": self.start_time,
            "end_time": self.end_time,
            "events": [e.to_dict() for e in self.events],
            "choices": self.choices,
            "rolls": self.rolls,
            "outcomes": self.outcomes,
        }


def create_character_for_being(being: Being) -> DnD5eCharacter:
    """Create a D&D character for a Being."""
    console.print("\n[bold]Creating Character for Being...[/bold]\n")

    # Use Being's name or generate one
    name = being.being_id.replace("being_", "").replace("_", " ").title()

    # Roll ability scores (4d6, drop lowest)
    def roll_ability_score() -> int:
        rolls = []
        for _ in range(4):
            rolls.append(DnDRoller.roll("1d6"))
        rolls.sort(reverse=True)
        return sum(rolls[:3])

    strength = roll_ability_score()
    dexterity = roll_ability_score()
    constitution = roll_ability_score()
    intelligence = roll_ability_score()
    wisdom = roll_ability_score()
    charisma = roll_ability_score()

    console.print(f"  STR: {strength}  DEX: {dexterity}  CON: {constitution}")
    console.print(f"  INT: {intelligence}  WIS: {wisdom}  CHA: {charisma}")

    # Calculate modifiers
    con_mod = DnD5eStats.ability_modifier(constitution)
    hit_die = 10
    max_hp = hit_die + con_mod

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
    )

    console.print("\n[bold green]Character Created![/bold green]")
    console.print(f"  Name: {character.name}")
    console.print(f"  Level: {character.level}")
    console.print(f"  HP: {character.hp}/{character.max_hp}")
    console.print(f"  AC: {character.ac}")

    return character


def play_tavern_scenario_with_being(session: TavernGameSession, auto_choices: list[str] = None):
    """Play the tavern scenario with a Being, capturing all events."""

    being = session.being
    character = session.character

    # Auto-choices for non-interactive play (default: random but reasonable)
    if auto_choices is None:
        auto_choices = ["1", "y", "1"]  # Stand up, read note, follow note

    choice_index = 0

    session.log_event(
        "game_start",
        "Tavern scenario begins",
        {"character_name": character.name, "being_id": being.being_id},
    )

    console.print(
        Panel(
            "You wake up with a pounding headache. The smell of ale and sawdust fills your nostrils.\n\n"
            "You're lying on a rough wooden floor, surrounded by empty tankards and sleeping patrons.\n"
            "The tavern is dimly lit by a few flickering candles. Your memory is hazy...\n\n"
            "How did you get here? What happened last night?",
            style="bold cyan",
            border_style="bright_blue",
        )
    )

    # First choice
    console.print("\n[bold]What do you do?[/bold]")
    console.print("1. [cyan]Stand up slowly[/cyan] and look around (Perception check)")
    console.print("2. [cyan]Check your pockets[/cyan] for clues (Investigation check)")
    console.print("3. [cyan]Ask the bartender[/cyan] what happened (Persuasion check)")
    console.print("4. [cyan]Try to remember[/cyan] last night (Intelligence check)")

    choice = auto_choices[choice_index] if choice_index < len(auto_choices) else "1"
    choice_index += 1

    choice_map = {
        "1": ("Stand up slowly", "perception", "wis"),
        "2": ("Check your pockets", "investigation", "int"),
        "3": ("Ask the bartender", "persuasion", "cha"),
        "4": ("Try to remember", "intelligence", "int"),
    }

    choice_text, skill_type, ability = choice_map.get(choice, choice_map["1"])
    session.log_choice(1, choice_text, choice)

    console.print(f"\n[yellow]→[/yellow] {choice_text}...")

    # Perform skill check
    roll, _ = DnDRoller.attack_roll()
    ability_mod = getattr(character, f"{ability}_modifier")
    total = roll + ability_mod

    # Determine DC and outcome
    if skill_type == "perception":
        dc = 15
        success = total >= dc
        if success:
            outcome = "You notice a strange symbol carved into the table and a note in your boot."
            found_note = True
        elif total >= 10:
            outcome = "You see the tavern is mostly empty. The bartender watches you warily."
            found_note = False
        else:
            outcome = "Your head is still spinning. You can't make out much in the dim light."
            found_note = False
    elif skill_type == "investigation":
        dc = 12
        success = total >= dc
        if success:
            outcome = "You find a crumpled note: 'Meet at the old mill. Midnight. Come alone. - The Shadow'"
            found_note = True
        else:
            outcome = (
                "You find loose coins and trinkets, but nothing that explains how you got here."
            )
            found_note = False
    elif skill_type == "persuasion":
        dc = 15
        success = total >= dc
        if success:
            outcome = "The bartender says: 'You came in here last night with a group. They left you here.'"
            found_note = False
        elif total >= 10:
            outcome = "The bartender grunts: 'You owe me 5 gold for the room.'"
            found_note = False
        else:
            outcome = "The bartender glares: 'I don't know nothing. Now get out.'"
            found_note = False
    else:  # intelligence
        dc = 15
        success = total >= dc
        if success:
            outcome = "Fragments come back: You were meeting someone. There was a job offer. Then... nothing. You must have been drugged."
            found_note = False
        elif total >= 10:
            outcome = (
                "You remember bits and pieces: A tavern, a meeting, voices. But details are lost."
            )
            found_note = False
        else:
            outcome = "Your mind is a complete blank. Whatever happened last night, it's gone."
            found_note = False

    ability_name_map = {"wis": "WIS", "int": "INT", "cha": "CHA"}
    ability_display = ability_name_map.get(ability, ability.upper())
    console.print(
        f"\n[dim]Roll: {roll} + {ability_display} modifier ({ability_mod:+d}) = {total}[/dim]"
    )
    console.print(f"[green]✓[/green] {outcome}")

    session.log_roll(skill_type, roll, ability_mod, total, dc, success)
    session.log_outcome("skill_check", outcome, {"found_note": found_note})

    # Stranger approaches
    console.print(
        Panel(
            "\nAs you're trying to make sense of things, a cloaked figure approaches your table.\n\n"
            "'You're awake,' they say in a low voice. 'Good. We need to talk. But not here.'\n\n"
            "They slide a note across the table and disappear into the shadows before you can respond.",
            style="bold cyan",
            border_style="bright_blue",
        )
    )

    session.log_event("narrative", "Stranger approaches and leaves a note")

    # Read note
    read_note = auto_choices[choice_index] if choice_index < len(auto_choices) else "y"
    choice_index += 1

    if read_note.lower() == "y":
        console.print(
            Panel(
                "\n[bold]The Note:[/bold]\n\n"
                "'You were chosen for a reason. Meet me at the old mill outside town at midnight. "
                "Come alone, or don't come at all. Your life depends on it.\n\n"
                "- The Shadow'\n\n"
                "The note is signed with the same symbol you saw earlier: a crescent moon with a dagger.",
                style="bold cyan",
                border_style="bright_blue",
            )
        )
        session.log_event("narrative", "Read the mysterious note from The Shadow")

    # Final choice
    console.print("\n[bold]What do you do next?[/bold]")
    console.print("1. [cyan]Follow the note[/cyan] - Go to the old mill")
    console.print("2. [cyan]Ask around town[/cyan] - Try to learn more first")
    console.print("3. [cyan]Ignore it[/cyan] - Leave town and forget this ever happened")

    final_choice = auto_choices[choice_index] if choice_index < len(auto_choices) else "1"
    choice_index += 1

    final_choice_map = {
        "1": (
            "Follow the note",
            "You decide to follow the note. As you leave the tavern, you feel eyes watching you. The old mill awaits. What secrets does it hold? Your adventure has just begun.",
        ),
        "2": (
            "Ask around town",
            "You decide to gather more information first. The townsfolk might know something about 'The Shadow' or the old mill. But time is running out... Your investigation begins.",
        ),
        "3": (
            "Ignore it",
            "You decide to leave town and forget this ever happened. But as you walk away, you can't shake the feeling that this isn't over. The Shadow will find you again. Or maybe... you'll find them first.",
        ),
    }

    final_choice_text, final_outcome = final_choice_map.get(final_choice, final_choice_map["1"])
    session.log_choice(2, final_choice_text, final_choice)

    console.print(
        Panel(
            f"\n[bold]To Be Continued...[/bold]\n\n{final_outcome}",
            style="bold cyan",
            border_style="bright_blue",
        )
    )

    session.log_outcome("final_choice", final_outcome, {"choice": final_choice_text})

    # Final character state
    console.print("\n[bold]Final Character State:[/bold]")
    console.print(f"  Name: {character.name}")
    console.print(f"  HP: {character.hp}/{character.max_hp}")
    console.print(f"  AC: {character.ac}")
    console.print(f"  Status Effects: {character.status_effects or 'None'}")

    session.log_event(
        "game_end",
        "Tavern scenario completed",
        {"final_hp": character.hp, "final_ac": character.ac},
    )


def generate_scientific_report(session: TavernGameSession, output_dir: Path) -> Path:
    """Generate a scientific research paper-style PDF report."""
    console.print("\n[bold]Generating Scientific Report...[/bold]\n")

    # Build report content
    session_data = session.to_dict()

    # Create markdown content for the report
    report_content = f"""# A Being's Journey Through the Tavern: An Empirical Study of Decision-Making in Simulated Reality

## Abstract

This study documents the experience of a WAFT Being (ID: {session.being.being_id}) as it navigates a simulated D&D 5e tavern scenario. Through systematic observation and event logging, we capture the Being's decision-making process, skill checks, and narrative outcomes. The Being, in its {session.being.lifetimes} lifetime, demonstrates adaptive behavior and strategic thinking within the constraints of the game mechanics.

## 1. Introduction

### 1.1 Research Question
How does a WAFT Being navigate complex decision-making scenarios when placed in an interactive narrative environment?

### 1.2 Hypothesis
A Being will demonstrate coherent decision-making patterns that reflect its underlying personality traits and skill levels, with outcomes influenced by both deterministic game mechanics (dice rolls) and strategic choices.

### 1.3 Methodology
We spawned a Being into a reality and had it play through a complete tavern scenario, logging all events, choices, dice rolls, and outcomes for analysis.

## 2. Methods

### 2.1 Being Creation
- **Being ID**: {session.being.being_id}
- **Lifetimes**: {session.being.lifetimes}
- **Reality ID**: {session.being.reality_id}
- **Created**: {session.being.created_at}

### 2.2 Character Generation
The Being was assigned a D&D 5e character with the following attributes:

**Character Name**: {session.character.name}
**Level**: {session.character.level}
**Class**: Fighter

**Ability Scores**:
- Strength: {session.character.strength} (Modifier: {session.character.str_modifier:+d})
- Dexterity: {session.character.dexterity} (Modifier: {session.character.dex_modifier:+d})
- Constitution: {session.character.constitution} (Modifier: {session.character.con_modifier:+d})
- Intelligence: {session.character.intelligence} (Modifier: {session.character.int_modifier:+d})
- Wisdom: {session.character.wisdom} (Modifier: {session.character.wis_modifier:+d})
- Charisma: {session.character.charisma} (Modifier: {session.character.cha_modifier:+d})

**Combat Stats**:
- Hit Points: {session.character.hp}/{session.character.max_hp}
- Armor Class: {session.character.ac}
- Proficiency Bonus: {session.character.proficiency_bonus:+d}

### 2.3 Game Session
- **Start Time**: {session.start_time}
- **End Time**: {session.end_time}
- **Duration**: {session._calculate_duration()}
- **Total Events**: {len(session.events)}
- **Total Choices**: {len(session.choices)}
- **Total Rolls**: {len(session.rolls)}

## 3. Results

### 3.1 Narrative Progression

The Being's journey began with awakening in a tavern, experiencing memory loss and disorientation. Through a series of skill checks and decisions, the Being navigated the scenario.

### 3.2 Decision Points

"""

    # Add choice analysis
    for i, choice in enumerate(session.choices, 1):
        report_content += f"""
#### Decision {i}: {choice["choice_text"]}
- **Timestamp**: {choice["timestamp"]}
- **Decision Made**: {choice["decision"]}
- **Context**: This decision occurred during the initial phase of the scenario.

"""

    # Add roll analysis
    report_content += """
### 3.3 Skill Check Analysis

"""

    for i, roll in enumerate(session.rolls, 1):
        success_rate = "Success" if roll["success"] else "Failure"
        report_content += f"""
#### Roll {i}: {roll["roll_type"].title()} Check
- **Die Roll**: {roll["die_roll"]}
- **Modifier**: {roll["modifier"]:+d}
- **Total**: {roll["total"]}
- **Difficulty Class (DC)**: {roll["dc"]}
- **Result**: {success_rate}
- **Timestamp**: {roll["timestamp"]}

**Analysis**: The Being rolled a {roll["die_roll"]} on a d20, added a {roll["modifier"]:+d} modifier, resulting in a total of {roll["total"]}. This {"met" if roll["success"] else "failed to meet"} the DC of {roll["dc"]}, resulting in a {success_rate.lower()}.

"""

    # Add outcomes
    report_content += """
### 3.4 Outcomes

"""

    for i, outcome in enumerate(session.outcomes, 1):
        report_content += f"""
#### Outcome {i}: {outcome["outcome_type"].title()}
- **Description**: {outcome["description"]}
- **Timestamp**: {outcome["timestamp"]}
- **Additional Data**: {json.dumps(outcome.get("data", {}), indent=2)}

"""

    # Add event timeline
    report_content += """
### 3.5 Event Timeline

"""

    for event in session.events:
        report_content += f"""
- **{event.timestamp}**: [{event.event_type.upper()}] {event.description}
"""

    # Add discussion
    report_content += f"""
## 4. Discussion

### 4.1 Decision-Making Patterns

The Being demonstrated {
        "strategic"
        if len([c for c in session.choices if c["decision"] == "1"]) > 0
        else "exploratory"
    } decision-making throughout the scenario. The Being made {
        len(session.choices)
    } major decisions, with {
        "a preference for"
        if len([c for c in session.choices if c["decision"] == "1"]) > 0
        else "varied"
    } approaches.

### 4.2 Skill Check Performance

The Being performed {len(session.rolls)} skill checks, with {
        len([r for r in session.rolls if r["success"]])
    } successes and {
        len([r for r in session.rolls if not r["success"]])
    } failures. This represents a {
        len([r for r in session.rolls if r["success"]])
        / len(session.rolls)
        * 100:.1f}% success rate.

### 4.3 Narrative Impact

The Being's choices and skill check results directly influenced the narrative outcomes. {
        "The Being successfully discovered clues"
        if any("note" in str(o.get("data", {})).lower() for o in session.outcomes)
        else "The Being encountered challenges"
    } throughout the scenario.

## 5. Conclusions

This study demonstrates that WAFT Beings can successfully navigate complex interactive scenarios, making decisions and experiencing outcomes based on game mechanics. The Being's journey through the tavern scenario provides evidence of:

1. **Adaptive Behavior**: The Being responded to scenario events appropriately
2. **Decision-Making**: The Being made coherent choices within the narrative context
3. **Mechanical Interaction**: The Being's character stats influenced outcomes through skill checks
4. **Narrative Engagement**: The Being experienced a complete narrative arc

### 5.1 Limitations

- This study involved a single Being in a single scenario
- Choices were predetermined for non-interactive execution
- The Being's personality traits were not explicitly utilized in decision-making

### 5.2 Future Research

Future studies could:
- Incorporate Being personality traits into decision-making algorithms
- Run multiple Beings through the same scenario for comparative analysis
- Track Being learning and adaptation across multiple game sessions
- Integrate Being memories and lessons learned into future decisions

## 6. References

- WAFT Being System Documentation
- D&D 5e Rules System
- Scientific Paper Generator (WAFT Evolution Module)

## 7. Appendices

### Appendix A: Complete Event Log

```json
{json.dumps(session.to_dict(), indent=2)}
```

### Appendix B: Being Metadata

```json
{
        json.dumps(
            {
                "being_id": session.being.being_id,
                "reality_id": session.being.reality_id,
                "lifetimes": session.being.lifetimes,
                "skills": session.being.skills,
                "state": session.being.state.value,
                "created_at": session.being.created_at,
                "fitness": session.being.fitness,
            },
            indent=2,
        )
    }
```

---
*Report generated by WAFT Scientific Paper Generator*
*Being ID: {session.being.being_id}*
*Generated: {datetime.now().isoformat()}*
"""

    # Save as markdown first, then try to generate PDF
    output_dir.mkdir(parents=True, exist_ok=True)
    base_name = (
        f"being_tavern_report_{session.being.being_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    md_path = output_dir / f"{base_name}.md"
    pdf_path = output_dir / f"{base_name}.pdf"

    # Save markdown
    md_path.write_text(report_content, encoding="utf-8")
    console.print(f"[dim]Markdown saved: {md_path}[/dim]")

    # Try to generate PDF using weasyprint if available
    pdf_generated = False
    try:
        import re

        from weasyprint import HTML

        # Convert markdown to HTML
        html_content = report_content

        # Convert markdown headers to HTML
        html_content = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html_content, flags=re.MULTILINE)
        html_content = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html_content, flags=re.MULTILINE)
        html_content = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html_content, flags=re.MULTILINE)
        html_content = re.sub(r"^#### (.+)$", r"<h4>\1</h4>", html_content, flags=re.MULTILINE)

        # Convert code blocks
        html_content = re.sub(
            r"```json\n(.*?)\n```", r"<pre><code>\1</code></pre>", html_content, flags=re.DOTALL
        )
        html_content = re.sub(
            r"```\n(.*?)\n```", r"<pre><code>\1</code></pre>", html_content, flags=re.DOTALL
        )

        # Convert bold
        html_content = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html_content)

        # Convert paragraphs
        paragraphs = html_content.split("\n\n")
        html_paragraphs = []
        for para in paragraphs:
            para = para.strip()
            if para and not para.startswith("<"):
                html_paragraphs.append(f"<p>{para}</p>")
            else:
                html_paragraphs.append(para)
        html_content = "\n".join(html_paragraphs)

        # Wrap in HTML document with scientific paper styling
        full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>A Being's Journey Through the Tavern</title>
    <style>
        @page {{
            size: letter;
            margin: 1in;
        }}
        body {{
            font-family: 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.4;
            color: #000;
        }}
        h1 {{
            font-size: 16pt;
            font-weight: bold;
            margin-top: 24pt;
            margin-bottom: 12pt;
        }}
        h2 {{
            font-size: 14pt;
            font-weight: bold;
            margin-top: 18pt;
            margin-bottom: 10pt;
        }}
        h3 {{
            font-size: 12pt;
            font-weight: bold;
            margin-top: 14pt;
            margin-bottom: 8pt;
        }}
        h4 {{
            font-size: 11pt;
            font-weight: bold;
            margin-top: 12pt;
            margin-bottom: 6pt;
        }}
        p {{
            margin-bottom: 10pt;
            text-align: justify;
        }}
        pre {{
            background: #f5f5f5;
            padding: 10pt;
            border: 1px solid #ddd;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            overflow-x: auto;
        }}
        code {{
            font-family: 'Courier New', monospace;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""

        HTML(string=full_html).write_pdf(str(pdf_path))
        pdf_generated = True
        console.print(f"[dim]PDF generated: {pdf_path}[/dim]")

        # Open PDF
        import platform
        import subprocess

        if platform.system() == "Darwin":  # macOS
            subprocess.run(["open", str(pdf_path)])
        elif platform.system() == "Windows":
            subprocess.run(["start", str(pdf_path)], shell=True)
        else:  # Linux
            subprocess.run(["xdg-open", str(pdf_path)])

    except ImportError:
        console.print(
            "[yellow]⚠ WeasyPrint not available. PDF not generated. Markdown saved.[/yellow]"
        )
        console.print("[dim]To generate PDF, install: pip install weasyprint[/dim]")
        console.print(f"[dim]Or convert manually: pandoc {md_path} -o {pdf_path}[/dim]")

    console.print(
        f"\n[bold green]✓ Report generated: {pdf_path if pdf_generated else md_path}[/bold green]\n"
    )

    return pdf_path if pdf_generated else md_path


def main():
    """Main execution."""
    console.print(
        "\n[bold bright_blue]╔════════════════════════════════════════╗[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]║[/bold bright_blue]  [bold white]BEING PLAYS TAVERN GAME[/bold white]  [bold bright_blue]║[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]║[/bold bright_blue]  [dim]With Scientific Report Generation[/dim]  [bold bright_blue]║[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]╚════════════════════════════════════════╝[/bold bright_blue]\n"
    )

    # Initialize Being System
    project_path = Path(__file__).parent.parent
    being_system = BeingSystem(project_path=project_path)

    # Spawn a Being
    console.print("[bold]Spawning Being...[/bold]\n")
    being = being_system.spawn_being(
        reality_id="tavern_scenario_reality",
        parent_being_id=None,
        initial_skills={"adventure": 10.0, "decision_making": 15.0},
    )

    console.print("[bold green]Being Spawned![/bold green]")
    console.print(f"  Being ID: {being.being_id}")
    console.print(f"  Lifetimes: {being.lifetimes}")
    console.print(f"  Reality: {being.reality_id}\n")

    # Create character for Being
    character = create_character_for_being(being)

    # Create game session
    session = TavernGameSession(being, character)

    # Play the game (with auto-choices for non-interactive execution)
    play_tavern_scenario_with_being(session, auto_choices=["1", "y", "1"])

    # Finish session
    session.finish()

    # Generate scientific report
    output_dir = (
        project_path
        / "_work_efforts"
        / "WE-260112-kgqt_being_plays_tavern_game_with_scientific_report_generation"
    )
    report_path = generate_scientific_report(session, output_dir)

    console.print("\n[bold green]✓ Complete![/bold green]")
    console.print(f"  Being: {being.being_id}")
    console.print(f"  Report: {report_path}\n")


if __name__ == "__main__":
    main()
