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


# Color Palette (Mandatory)
CRISIS_RED = "#D32F2F"
VOID_BLACK = "#121212"
PAPER_CREAM = "#FFF8E1"
CONCRETE_GREY = "#757575"
GLORY_GOLD = "#FFD700"
BORDER_GREY = "#424242"


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
        
        # Level Display
        level = character.get("level", 1)
        level_text = Text(f"LVL {level:02d}", style=f"bold {GLORY_GOLD}")
        
        # Attribute Matrix
        ability_scores = sheet["ability_scores"]
        ability_modifiers = sheet["ability_modifiers"]
        
        attributes_text = Text()
        for ability in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
            score = ability_scores.get(ability, 8)
            modifier = ability_modifiers.get(ability, -1)
            modifier_str = f"+{modifier}" if modifier >= 0 else str(modifier)
            
            # Create bar visualization (score out of 20, so 20 blocks max)
            bar_length = 20
            filled = int((score / 20.0) * bar_length)
            bar = "▰" * filled + "▱" * (bar_length - filled)
            
            abbr = ability[:3].upper()
            attributes_text.append(f"{abbr} [{score:2d}] {bar}\n", style=PAPER_CREAM)
        
        # Status Effects
        status_effects = sheet["status_effects"]
        status_text = Text()
        
        if status_effects:
            for effect in status_effects[-5:]:  # Show last 5
                effect_type = effect.get("type", "unknown")
                effect_name = effect.get("name", "Unknown")
                duration = effect.get("duration")
                
                if effect_type == "buff":
                    symbol = "▲"
                    color = GLORY_GOLD
                else:
                    symbol = "▼"
                    color = CRISIS_RED
                
                duration_str = f" ({duration}s)" if duration else " (Perm)"
                status_text.append(f"[{color}]{symbol} {effect_name}{duration_str}[/]\n")
        else:
            status_text.append("[dim]No active effects[/]\n", style=CONCRETE_GREY)
        
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
                
                # Format timestamp (extract time part)
                try:
                    time_part = timestamp.split("T")[1].split(".")[0] if "T" in timestamp else timestamp[:8]
                except:
                    time_part = timestamp[:8] if len(timestamp) >= 8 else timestamp
                
                # Determine row style based on outcome/classification
                if classification == "critical_success" or outcome == "critical_success":
                    row_style = f"bold {VOID_BLACK} on {GLORY_GOLD}"
                elif classification == "critical_failure" or outcome == "critical_failure":
                    row_style = f"bold {PAPER_CREAM} on {CRISIS_RED}"
                else:
                    row_style = PAPER_CREAM
                
                log_text = f"[{CONCRETE_GREY}]{time_part}[/] │ {narrative}"
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
        
        # Combine content
        content = Align.left(
            Text.assemble(
                "[bold]ACTIVE OPERATION[/]\n",
                op_text, "\n\n",
                "[bold]RESOURCE FUND[/]\n",
                credits_text, "\n\n",
                "[bold]INVENTORY[/]\n",
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

