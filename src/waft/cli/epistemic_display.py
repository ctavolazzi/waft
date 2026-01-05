"""
Epistemic Display Module - Beautiful visualizations for epistemic state.

Provides moon phase indicators, state formatting, gate styling, and dashboard creation
using the Rich library for beautiful terminal output.
"""

from typing import Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn
from rich.layout import Layout


def get_moon_phase(coverage: float) -> str:
    """
    Returns moon phase emoji based on epistemic coverage.
    
    Args:
        coverage: Epistemic coverage value (0.0-1.0)
        
    Returns:
        Moon phase emoji string
    """
    if coverage < 0.25:
        return "🌑"  # Critical - New Moon (Discovery/Uncertainty)
    elif coverage < 0.50:
        return "🌒"  # Low - Waxing Crescent
    elif coverage < 0.75:
        return "🌓"  # Moderate - First Quarter
    elif coverage < 0.90:
        return "🌔"  # Good - Waxing Gibbous
    else:
        return "🌕"  # Excellent - Full Moon (Execution/Certainty)


def format_gate_result(gate: str) -> Text:
    """
    Styles gate results with appropriate colors.
    
    Args:
        gate: Gate result string (PROCEED, HALT, BRANCH, REVISE)
        
    Returns:
        Styled Rich Text object
    """
    gate_text = Text(gate)
    
    if gate == "PROCEED":
        gate_text.stylize("bold green")
    elif gate == "HALT":
        gate_text.stylize("bold red")
    elif gate == "BRANCH":
        gate_text.stylize("bold yellow")
    elif gate == "REVISE":
        gate_text.stylize("bold yellow")
    else:
        gate_text.stylize("dim")
    
    return gate_text


def format_epistemic_state(state: Dict[str, Any]) -> Panel:
    """
    Creates Rich Panel with epistemic state visualization.
    
    Shows all 13 vectors in organized table with color-coding by health level.
    Includes moon phase indicator.
    
    Args:
        state: Epistemic state dictionary with vectors
        
    Returns:
        Rich Panel with epistemic state table
    """
    table = Table(show_header=True, header_style="bold cyan", box=None)
    table.add_column("Vector", style="dim", width=20)
    table.add_column("Value", justify="right", width=10)
    table.add_column("Status", width=15)
    
    # Extract vectors from state
    vectors = state.get("vectors", {})
    foundation = vectors.get("foundation", {})
    comprehension = vectors.get("comprehension", {})
    execution = vectors.get("execution", {})
    
    # Foundation vectors
    know = foundation.get("know", 0.0)
    do = foundation.get("do", 0.0)
    context = foundation.get("context", 0.0)
    engagement = vectors.get("engagement", 0.0)
    
    # Comprehension vectors
    clarity = comprehension.get("clarity", 0.0)
    coherence = comprehension.get("coherence", 0.0)
    signal = comprehension.get("signal", 0.0)
    density = comprehension.get("density", 0.0)
    
    # Execution vectors
    exec_state = execution.get("state", 0.0)
    change = execution.get("change", 0.0)
    completion = execution.get("completion", 0.0)
    impact = execution.get("impact", 0.0)
    
    # Meta vector
    uncertainty = vectors.get("uncertainty", 0.0)
    
    # Calculate average coverage for moon phase
    all_values = [
        know, do, context, engagement,
        clarity, coherence, signal, density,
        exec_state, change, completion, impact
    ]
    avg_coverage = sum(all_values) / len(all_values) if all_values else 0.0
    moon_phase = get_moon_phase(avg_coverage)
    
    # Helper to get status color
    def get_status_color(value: float) -> str:
        if value >= 0.75:
            return "green"
        elif value >= 0.50:
            return "yellow"
        else:
            return "red"
    
    # Add rows
    table.add_row("Engagement", f"{engagement:.0%}", f"[{get_status_color(engagement)}]●[/]")
    table.add_row("Know", f"{know:.0%}", f"[{get_status_color(know)}]●[/]")
    table.add_row("Do", f"{do:.0%}", f"[{get_status_color(do)}]●[/]")
    table.add_row("Context", f"{context:.0%}", f"[{get_status_color(context)}]●[/]")
    table.add_row("Clarity", f"{clarity:.0%}", f"[{get_status_color(clarity)}]●[/]")
    table.add_row("Coherence", f"{coherence:.0%}", f"[{get_status_color(coherence)}]●[/]")
    table.add_row("Signal", f"{signal:.0%}", f"[{get_status_color(signal)}]●[/]")
    table.add_row("Density", f"{density:.0%}", f"[{get_status_color(density)}]●[/]")
    table.add_row("State", f"{exec_state:.0%}", f"[{get_status_color(exec_state)}]●[/]")
    table.add_row("Change", f"{change:.0%}", f"[{get_status_color(change)}]●[/]")
    table.add_row("Completion", f"{completion:.0%}", f"[{get_status_color(completion)}]●[/]")
    table.add_row("Impact", f"{impact:.0%}", f"[{get_status_color(impact)}]●[/]")
    table.add_row("Uncertainty", f"{uncertainty:.0%}", f"[{get_status_color(1.0 - uncertainty)}]●[/]")
    
    # Create panel with moon phase in title
    panel_content = f"{moon_phase} Epistemic State\n\n{table}"
    
    return Panel(
        panel_content,
        title="[bold cyan]Epistemic Vectors[/bold cyan]",
        border_style="cyan"
    )


def create_epistemic_dashboard(context: Dict[str, Any]) -> Panel:
    """
    Creates comprehensive epistemic dashboard.
    
    Shows epistemic state summary, active goals, recent findings,
    open unknowns, and learning trajectory.
    
    Args:
        context: Project bootstrap context from Empirica
        
    Returns:
        Rich Panel with comprehensive dashboard
    """
    console = Console()
    
    # Extract data
    epistemic_state = context.get("epistemic_state", {})
    goals = context.get("goals", [])
    findings = context.get("findings", [])
    unknowns = context.get("unknowns", [])
    
    # Calculate moon phase from epistemic state
    vectors = epistemic_state.get("vectors", {})
    foundation = vectors.get("foundation", {})
    know = foundation.get("know", 0.0)
    uncertainty = vectors.get("uncertainty", 0.0)
    coverage = know * (1.0 - uncertainty)
    moon_phase = get_moon_phase(coverage)
    
    # Build dashboard content
    dashboard_lines = []
    
    # Header with moon phase
    dashboard_lines.append(f"{moon_phase} [bold cyan]Epistemic Dashboard[/bold cyan]\n")
    
    # Epistemic state summary
    dashboard_lines.append("[bold]Epistemic State:[/bold]")
    dashboard_lines.append(f"  Know: {know:.0%} | Uncertainty: {uncertainty:.0%} | Coverage: {coverage:.0%}")
    dashboard_lines.append("")
    
    # Active goals
    dashboard_lines.append(f"[bold]Active Goals:[/bold] {len(goals)}")
    for i, goal in enumerate(goals[:3], 1):  # Show first 3
        objective = goal.get("objective", "Unknown")
        dashboard_lines.append(f"  {i}. {objective[:50]}...")
    if len(goals) > 3:
        dashboard_lines.append(f"  ... and {len(goals) - 3} more")
    dashboard_lines.append("")
    
    # Recent findings
    dashboard_lines.append(f"[bold]Recent Findings:[/bold] {len(findings)}")
    for i, finding in enumerate(findings[:3], 1):  # Show first 3
        content = finding.get("content", "Unknown")
        dashboard_lines.append(f"  {i}. {content[:50]}...")
    if len(findings) > 3:
        dashboard_lines.append(f"  ... and {len(findings) - 3} more")
    dashboard_lines.append("")
    
    # Open unknowns
    dashboard_lines.append(f"[bold]Open Unknowns:[/bold] {len(unknowns)}")
    for i, unknown in enumerate(unknowns[:3], 1):  # Show first 3
        content = unknown.get("content", "Unknown")
        dashboard_lines.append(f"  {i}. {content[:50]}...")
    if len(unknowns) > 3:
        dashboard_lines.append(f"  ... and {len(unknowns) - 3} more")
    
    dashboard_content = "\n".join(dashboard_lines)
    
    return Panel(
        dashboard_content,
        title="[bold cyan]Epistemic Dashboard[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    )


def format_epistemic_summary(state: Optional[Dict[str, Any]] = None) -> str:
    """
    Creates a brief summary string of epistemic state.
    
    Args:
        state: Optional epistemic state dictionary
        
    Returns:
        Formatted summary string
    """
    if not state:
        return "🌑 Epistemic state unavailable"
    
    vectors = state.get("vectors", {})
    foundation = vectors.get("foundation", {})
    know = foundation.get("know", 0.0)
    uncertainty = vectors.get("uncertainty", 0.0)
    coverage = know * (1.0 - uncertainty)
    moon_phase = get_moon_phase(coverage)
    
    return f"{moon_phase} K:{know:.0%} U:{uncertainty:.0%}"

