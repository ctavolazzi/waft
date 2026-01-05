"""
Epistemic HUD (Heads-Up Display) - Constructivist Sci-Fi interface.

Provides a split-screen view showing:
- Left: "The Build" (Praxic Stream) - Active tasks, file changes
- Right: "The Mind" (Noetic State) - Empirica vectors, known unknowns
- Header: Project Name | Integrity Bar | Moon Phase
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.progress import BarColumn, Progress, TextColumn
from rich.text import Text
from rich.live import Live
from rich.align import Align

from ..core.empirica import EmpiricaManager
from ..core.memory import MemoryManager
from .epistemic_display import get_moon_phase


def create_integrity_bar(integrity: float) -> Text:
    """
    Create an integrity bar with color coding.
    
    Args:
        integrity: Integrity value (0.0-100.0)
        
    Returns:
        Rich Text with integrity bar
    """
    if integrity >= 75:
        color = "green"
    elif integrity >= 50:
        color = "yellow"
    elif integrity >= 25:
        color = "red"
    else:
        color = "bold red"
    
    bar_length = 20
    filled = int((integrity / 100.0) * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    return Text(f"[{color}]{bar}[/{color}] {integrity:.0f}%")


def create_header(project_name: str, integrity: float, moon_phase: str) -> Panel:
    """
    Create the HUD header with project name, integrity bar, and moon phase.
    
    Args:
        project_name: Name of the project
        integrity: Integrity value (0.0-100.0)
        moon_phase: Moon phase emoji
        
    Returns:
        Rich Panel with header
    """
    integrity_bar = create_integrity_bar(integrity)
    header_text = f"[bold cyan]{project_name}[/bold cyan] | {integrity_bar} | {moon_phase}"
    
    return Panel(
        Align.center(header_text),
        border_style="cyan",
        height=3,
    )


def create_build_panel(project_path: Path) -> Panel:
    """
    Create the "Build" panel showing active work (Praxic Stream).
    
    Shows files from _pyrite/active/ directory.
    
    Args:
        project_path: Path to project root
        
    Returns:
        Rich Panel with build information
    """
    memory = MemoryManager(project_path)
    active_files = memory.get_active_files()
    
    content_lines = ["[bold]The Build[/bold] - Praxic Stream\n"]
    
    if active_files:
        content_lines.append(f"[dim]Active files: {len(active_files)}[/dim]\n")
        for i, file_path in enumerate(active_files[:10], 1):  # Show first 10
            file_name = file_path.name
            content_lines.append(f"  {i}. {file_name}")
        if len(active_files) > 10:
            content_lines.append(f"  ... and {len(active_files) - 10} more")
    else:
        content_lines.append("[dim]No active files[/dim]")
    
    content = "\n".join(content_lines)
    
    return Panel(
        content,
        title="[bold cyan]The Build[/bold cyan]",
        border_style="cyan",
    )


def create_mind_panel(project_path: Path, empirica: EmpiricaManager) -> Panel:
    """
    Create the "Mind" panel showing epistemic state (Noetic State).
    
    Shows Empirica vectors, known unknowns, and epistemic summary.
    
    Args:
        project_path: Path to project root
        empirica: EmpiricaManager instance
        
    Returns:
        Rich Panel with mind information
    """
    content_lines = ["[bold]The Mind[/bold] - Noetic State\n"]
    
    if empirica.is_initialized():
        context = empirica.project_bootstrap()
        if context:
            epistemic_state = context.get("epistemic_state", {})
            vectors = epistemic_state.get("vectors", {})
            foundation = vectors.get("foundation", {})
            know = foundation.get("know", 0.0)
            uncertainty = vectors.get("uncertainty", 0.0)
            coverage = know * (1.0 - uncertainty) if know > 0 else 0.0
            moon_phase = get_moon_phase(coverage)
            
            content_lines.append(f"{moon_phase} [bold]Epistemic State[/bold]")
            content_lines.append(f"  Know: {know:.0%}")
            content_lines.append(f"  Uncertainty: {uncertainty:.0%}")
            content_lines.append(f"  Coverage: {coverage:.0%}\n")
            
            # Show unknowns
            unknowns = context.get("unknowns", [])
            if unknowns:
                content_lines.append(f"[bold]Known Unknowns:[/bold] {len(unknowns)}")
                for i, unknown in enumerate(unknowns[:5], 1):  # Show first 5
                    content = unknown.get("content", "Unknown")
                    content_lines.append(f"  {i}. {content[:40]}...")
                if len(unknowns) > 5:
                    content_lines.append(f"  ... and {len(unknowns) - 5} more")
            else:
                content_lines.append("[dim]No known unknowns[/dim]")
        else:
            content_lines.append("[dim]No epistemic context available[/dim]")
    else:
        content_lines.append("[yellow]Empirica not initialized[/yellow]")
        content_lines.append("[dim]Run 'waft init' to enable[/dim]")
    
    content = "\n".join(content_lines)
    
    return Panel(
        content,
        title="[bold cyan]The Mind[/bold cyan]",
        border_style="cyan",
    )


def render_hud(project_path: Path, integrity: float = 100.0) -> None:
    """
    Render the Epistemic HUD with split-screen layout.
    
    Args:
        project_path: Path to project root
        integrity: Current integrity value (default: 100.0)
    """
    console = Console()
    
    # Get project name
    from ..core.substrate import SubstrateManager
    substrate = SubstrateManager()
    project_info = substrate.get_project_info(project_path)
    project_name = project_info.get("name", "Unknown Project") if project_info else "Unknown Project"
    
    # Get moon phase
    empirica = EmpiricaManager(project_path)
    moon_phase = "🌑"  # Default
    if empirica.is_initialized():
        context = empirica.project_bootstrap()
        if context:
            epistemic_state = context.get("epistemic_state", {})
            vectors = epistemic_state.get("vectors", {})
            foundation = vectors.get("foundation", {})
            know = foundation.get("know", 0.0)
            uncertainty = vectors.get("uncertainty", 0.0)
            coverage = know * (1.0 - uncertainty) if know > 0 else 0.0
            moon_phase = get_moon_phase(coverage)
    
    # Create layout
    layout = Layout()
    
    # Header
    header = create_header(project_name, integrity, moon_phase)
    layout.split_column(
        Layout(header, size=3, name="header"),
        Layout(name="body"),
    )
    
    # Split body into left and right
    layout["body"].split_row(
        Layout(name="build"),
        Layout(name="mind"),
    )
    
    # Create panels
    build_panel = create_build_panel(project_path)
    mind_panel = create_mind_panel(project_path, empirica)
    
    layout["build"].update(build_panel)
    layout["mind"].update(mind_panel)
    
    # Render
    console.print(layout)

