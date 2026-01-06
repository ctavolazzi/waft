"""
Red October Dashboard - Constructivist Sci-Fi TUI for TavernKeeper

Implements the "Red October" aesthetic with high contrast, block geometry,
and industrial design inspired by Russian Constructivism.
"""

import time
from typing import Optional
from pathlib import Path

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live
from rich.align import Align

from ..core.tavern_keeper import TavernKeeper


# Color Palette (Mandatory + Enhanced)
CRISIS_RED = "#D32F2F"
VOID_BLACK = "#121212"
PAPER_CREAM = "#FFF8E1"
CONCRETE_GREY = "#757575"
GLORY_GOLD = "#FFD700"
BORDER_GREY = "#424242"

# Enhanced Color Palette
CYAN_ENERGY = "#00FFFF"
GREEN_SUCCESS = "#4CAF50"
ORANGE_WARNING = "#FF9800"
PURPLE_MAGIC = "#9C27B0"
BLUE_INFO = "#2196F3"
PINK_DELIGHT = "#E91E63"


class RedOctoberDashboard:
    """
    The Red October Dashboard - Terminal User Interface for TavernKeeper.

    Displays real-time game state with Constructivist Sci-Fi aesthetic.
    """

    def __init__(self, tavern_keeper: TavernKeeper):
        """
        Initialize the dashboard.

        Args:
            tavern_keeper: TavernKeeper instance to read data from
        """
        self.tavern = tavern_keeper
        self.console = Console()
        self.running = True

    def generate_layout(self) -> Layout:
        """
        Build the grid system as specified in Article II.

        Returns:
            Configured Layout object
        """
        layout = Layout()

        # Root: Split Column
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=1),
        )

        # Body: Split Row
        layout["body"].split_row(
            Layout(name="left", ratio=1),
            Layout(name="center", ratio=2),
            Layout(name="right", ratio=1),
        )

        return layout

    def render_header(self) -> Panel:
        """
        Render the Header (Integrity Monitor) as per Section 3.01.

        Returns:
            Panel with header content
        """
        character = self.tavern.get_character()
        integrity = character.get("integrity", 100.0)
        project_name = character.get("name", "UNKNOWN")

        # Calculate health bar
        bar_length = 10
        filled = int((integrity / 100.0) * bar_length)
        empty = bar_length - filled

        # Create health bar string with blocks
        health_bar = "█" * filled + "░" * empty
        health_percent = f"{integrity:.0f}%"

        # Create 3-column grid
        header_table = Table.grid(expand=True, padding=(0, 1))
        header_table.add_column("left", justify="left", style=f"bold {PAPER_CREAM} on {CRISIS_RED}")
        header_table.add_column("center", justify="center", style=f"bold {PAPER_CREAM} on {CRISIS_RED}")
        header_table.add_column("right", justify="right", style=f"bold {PAPER_CREAM} on {CRISIS_RED}")

        header_table.add_row(
            "TAVERNKEEPER OS [bold]v2.1[/]",
            project_name.upper(),
            f"INTEGRITY [{health_bar}] {health_percent}",
        )

        return Panel(
            header_table,
            style=f"bold {PAPER_CREAM} on {CRISIS_RED}",
            border_style=CRISIS_RED,
        )

    def render_left_panel(self) -> Panel:
        """
        Render the Left Panel (Biometrics) as per Section 3.02.

        Returns:
            Panel with biometrics content
        """
        character = self.tavern.get_character()
        sheet = self.tavern.get_character_sheet()

        # Level Display with enhanced styling
        level = character.get("level", 1)
        insight = character.get("insight", 0.0)
        next_level_insight = self.tavern._calculate_insight_for_level(level + 1)
        insight_needed = next_level_insight - insight
        
        level_color = GLORY_GOLD if level >= 5 else CYAN_ENERGY if level >= 3 else GREEN_SUCCESS
        level_text = Text.assemble(
            (f"LVL {level:02d}", f"bold {level_color}"),
            f"\n[{CONCRETE_GREY}]Insight: {insight:.0f}/{next_level_insight:.0f}[/]",
            f"\n[{CYAN_ENERGY}]{insight_needed:.0f} to next[/]",
        )
        
        # Attribute Matrix with color coding
        ability_scores = sheet["ability_scores"]
        ability_modifiers = sheet["ability_modifiers"]
        
        # Color mapping for abilities
        ability_colors = {
            "strength": CRISIS_RED,
            "dexterity": CYAN_ENERGY,
            "constitution": GREEN_SUCCESS,
            "intelligence": BLUE_INFO,
            "wisdom": PURPLE_MAGIC,
            "charisma": PINK_DELIGHT,
        }
        
        attributes_text = Text()
        for ability in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
            score = ability_scores.get(ability, 8)
            modifier = ability_modifiers.get(ability, -1)
            modifier_str = f"+{modifier}" if modifier >= 0 else str(modifier)
            ability_color = ability_colors.get(ability, PAPER_CREAM)
            
            # Color code based on score
            if score >= 16:
                score_color = GLORY_GOLD
            elif score >= 13:
                score_color = GREEN_SUCCESS
            elif score >= 10:
                score_color = CYAN_ENERGY
            else:
                score_color = CONCRETE_GREY
            
            # Create bar visualization with color
            bar_length = 15
            filled = int((score / 20.0) * bar_length)
            bar_filled = f"[{ability_color}]" + "▰" * filled + "[/]"
            bar_empty = "[dim]" + "▱" * (bar_length - filled) + "[/]"
            
            abbr = ability[:3].upper()
            attributes_text.append(f"[{ability_color}]{abbr}[/] ", style=PAPER_CREAM)
            attributes_text.append(f"[{score_color}][{score:2d}][/] ", style=PAPER_CREAM)
            attributes_text.append(f"[dim]({modifier_str})[/] ", style=PAPER_CREAM)
            attributes_text.append(f"{bar_filled}{bar_empty}\n", style=PAPER_CREAM)

        # Status Effects with enhanced styling
        status_effects = sheet["status_effects"]
        status_text = Text()
        
        if status_effects:
            for effect in status_effects[-5:]:  # Show last 5
                effect_type = effect.get("type", "unknown")
                effect_name = effect.get("name", "Unknown")
                duration = effect.get("duration")
                
                if effect_type == "buff":
                    symbol = f"[{GLORY_GOLD}]▲[/]"
                    color = GLORY_GOLD
                    bg_color = f"on {GLORY_GOLD}"
                else:
                    symbol = f"[{CRISIS_RED}]▼[/]"
                    color = CRISIS_RED
                    bg_color = f"on {CRISIS_RED}"
                
                duration_str = f" [{CONCRETE_GREY}]{duration}s[/]" if duration else f" [{PURPLE_MAGIC}]Perm[/]"
                status_text.append(f"{symbol} [{color}]{effect_name}[/]{duration_str}\n")
        else:
            status_text.append(f"[{CONCRETE_GREY}]No active effects[/]\n", style=CONCRETE_GREY)

        # Combine all content
        content = Align.left(
            Text.assemble(
                level_text, "\n\n",
                "[bold]ATTRIBUTES[/]\n", attributes_text, "\n",
                "[bold]STATUS EFFECTS[/]\n", status_text,
            ),
            vertical="top",
        )

        return Panel(
            content,
            title=f"[bold {CRISIS_RED}]BIOMETRICS[/]",
            border_style=BORDER_GREY,
            style=f"{PAPER_CREAM} on {VOID_BLACK}",
        )

    def render_center_panel(self) -> Panel:
        """
        Render the Center Panel (The Chronicle) as per Section 3.03.

        Returns:
            Panel with system log content
        """
        # Get adventure journal entries
        if self.tavern.db:
            journal_entries = self.tavern.db.table("adventure_journal").all()
        else:
            journal_entries = self.tavern._data.get("adventure_journal", [])

        # Get last 15 entries
        recent_entries = journal_entries[-15:] if len(journal_entries) > 15 else journal_entries
        recent_entries.reverse()  # Show newest first

        # Create table
        log_table = Table(box=None, padding=(0, 1), expand=True, show_header=False)
        log_table.add_column("content", style=PAPER_CREAM)

        if recent_entries:
            for entry in recent_entries:
                timestamp = entry.get("timestamp", "")
                narrative = entry.get("narrative", "")
                outcome = entry.get("outcome", "")
                classification = entry.get("classification", "")
                entry_type = entry.get("type", "event")
                mood = entry.get("mood", "")
                source = entry.get("source", "")

                # Format timestamp (extract time part)
                try:
                    time_part = timestamp.split("T")[1].split(".")[0] if "T" in timestamp else timestamp[:8]
                except:
                    time_part = timestamp[:8] if len(timestamp) >= 8 else timestamp

                # Determine row style with enhanced color coding
                if classification == "critical_success" or outcome == "critical_success":
                    row_style = f"bold {VOID_BLACK} on {GLORY_GOLD}"
                    icon = f"[{VOID_BLACK}]⭐[/] "
                elif classification == "critical_failure" or outcome == "critical_failure":
                    row_style = f"bold {PAPER_CREAM} on {CRISIS_RED}"
                    icon = f"[{PAPER_CREAM}]💥[/] "
                elif classification == "superior":
                    row_style = f"{GLORY_GOLD}"
                    icon = f"[{GLORY_GOLD}]▲[/] "
                elif classification == "optimal":
                    row_style = f"{GREEN_SUCCESS}"
                    icon = f"[{GREEN_SUCCESS}]✓[/] "
                elif entry_type == "narrative":
                    # Narrative entries get special styling
                    if mood == "delighted" or entry.get("event") == "celebration":
                        row_style = f"{GLORY_GOLD}"
                        icon = f"[{GLORY_GOLD}]✨[/] "
                    elif mood == "concerned" or entry.get("event") == "question":
                        row_style = f"{ORANGE_WARNING}"
                        icon = f"[{ORANGE_WARNING}]?[/] "
                    elif mood == "surprised" or mood == "amazed":
                        row_style = f"{CYAN_ENERGY}"
                        icon = f"[{CYAN_ENERGY}]⚡[/] "
                    else:
                        row_style = PAPER_CREAM
                        icon = f"[{CONCRETE_GREY}]•[/] "
                else:
                    row_style = PAPER_CREAM
                    icon = f"[{CONCRETE_GREY}]•[/] "
                
                # Add source indicator for narrative entries
                source_indicator = ""
                if entry_type == "narrative" and source:
                    if source == "ai":
                        source_indicator = f"[{PURPLE_MAGIC}][AI][/] "
                    elif source == "human":
                        source_indicator = f"[{BLUE_INFO}][YOU][/] "
                
                log_text = f"[{CONCRETE_GREY}]{time_part}[/] │ {icon}{source_indicator}{narrative}"
                log_table.add_row(Text(log_text, style=row_style))
        else:
            log_table.add_row(Text("[dim]No entries in the chronicle yet...[/]", style=CONCRETE_GREY))

        return Panel(
            log_table,
            title=f"[bold {CRISIS_RED}]SYSTEM LOG[/]",
            border_style=CRISIS_RED,
            style=f"{PAPER_CREAM} on {VOID_BLACK}",
        )

    def render_right_panel(self) -> Panel:
        """
        Render the Right Panel (Directives) as per Section 3.04.

        Returns:
            Panel with directives content
        """
        character = self.tavern.get_character()
        credits = character.get("credits", 0)

        # Get current git branch
        import subprocess
        git_branch = "unknown"
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                cwd=self.tavern.project_path,
                timeout=1,
            )
            if result.returncode == 0:
                git_branch = result.stdout.strip()
        except:
            pass

        # Active Operation
        op_text = Text.assemble(
            "OP: ", (f"[bold {GLORY_GOLD}]{git_branch}[/]", ""),
        )

        # Resource Fund
        credits_text = Text()
        credits_text.append("CREDITS: ", style=PAPER_CREAM)
        credits_text.append(f"¤ {credits}", style=GLORY_GOLD)

        # Inventory (placeholder - would come from inventory system)
        inventory_text = Text("[dim]No items[/]", style=CONCRETE_GREY)

        # Combine content with enhanced layout
        content = Align.left(
            Text.assemble(
                f"[bold {CYAN_ENERGY}]ACTIVE OPERATION[/]\n",
                op_text, "\n\n",
                f"[bold {GLORY_GOLD}]RESOURCE FUND[/]\n",
                credits_text, "\n",
                insight_text, "\n\n",
                f"[bold {CONCRETE_GREY}]INVENTORY[/]\n",
                inventory_text, "\n",
            ),
            vertical="top",
        )

        return Panel(
            content,
            title=f"[bold {CRISIS_RED}]DIRECTIVES[/]",
            border_style=BORDER_GREY,
            style=f"{PAPER_CREAM} on {VOID_BLACK}",
        )

    def render_footer(self) -> Text:
        """
        Render the Footer as per Section 3.05.

        Returns:
            Footer text
        """
        footer_text = Text(
            "TERMINAL ACTIVE // ENTROPY IS WATCHING // PRESS [Q] TO ABORT",
            style=f"italic {CONCRETE_GREY} on {VOID_BLACK}",
        )
        return Align.center(footer_text)

    def render(self) -> Layout:
        """
        Populate the layout with live data from TavernKeeper.

        Returns:
            Fully rendered layout
        """
        layout = self.generate_layout()

        # Populate each section
        layout["header"].update(self.render_header())
        layout["left"].update(self.render_left_panel())
        layout["center"].update(self.render_center_panel())
        layout["right"].update(self.render_right_panel())
        layout["footer"].update(self.render_footer())

        return layout

    def run(self):
        """
        Start the dashboard with Live context manager, refreshing at 4Hz.
        """
        with Live(
            self.render(),
            console=self.console,
            refresh_per_second=4,
            screen=True,
        ) as live:
            try:
                while self.running:
                    live.update(self.render())
                    time.sleep(0.25)  # 4Hz = 0.25s interval
            except KeyboardInterrupt:
                self.running = False

