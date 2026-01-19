"""
Oracle Thinking Visualization

Shows TheOracle's cognitive process in real-time, similar to Empirica dashboard.
"""

from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
import time


def display_oracle_thinking(
    console: Console,
    question: str,
    preflight: Dict[str, Any],
    reflection: Dict[str, Any],
    findings: List[Dict[str, Any]],
    unknowns: List[Dict[str, Any]],
    check: Dict[str, Any],
    epistemic_state: Dict[str, Any],
    postflight: Optional[Dict[str, Any]] = None,
    storage_info: Optional[Dict[str, Any]] = None
) -> None:
    """
    Display TheOracle's thinking process in a dashboard-like format.
    
    Shows:
    - CASCADE Workflow (PREFLIGHT → INVESTIGATE → CHECK → ACT → POSTFLIGHT)
    - 13 Epistemic Vectors (engagement, foundation, comprehension, execution)
    - Three-Layer Storage status (SQLite + Git Notes + JSON)
    - Recent findings stream
    - Reflection insights
    - Decision gates
    """
    
    # Create layout
    layout = Layout()
    
    # Split into header, body, and footer
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=4)
    )
    
    # Split body into left (workflow) and right (state)
    layout["body"].split_row(
        Layout(name="workflow", ratio=1),
        Layout(name="state", ratio=1)
    )
    
    # Header
    header_text = Text("🔮 TheOracle - Epistemic Intelligence System", style="bold cyan")
    layout["header"].update(Panel(header_text, border_style="cyan"))
    
    # Left panel: CASCADE Workflow
    workflow_content = _build_cascade_workflow_panel(preflight, reflection, check, postflight)
    layout["workflow"].update(Panel(workflow_content, title="CASCADE Workflow", border_style="blue"))
    
    # Right panel: 13 Epistemic Vectors & Findings
    state_content = _build_epistemic_vectors_panel(
        preflight, findings, unknowns, check, epistemic_state
    )
    layout["state"].update(Panel(state_content, title="13 Epistemic Vectors (LIVE)", border_style="magenta"))
    
    # Footer: Three-Layer Storage Status
    if storage_info:
        storage_content = _build_storage_status_panel(storage_info)
        layout["footer"].update(Panel(storage_content, title="Three-Layer Storage", border_style="green"))
    else:
        layout["footer"].update(Panel("[dim]Storage: SQLite + Git Notes + JSON[/dim]", border_style="green"))
    
    # Display
    console.print(layout)


def _build_cascade_workflow_panel(
    preflight: Dict[str, Any],
    reflection: Dict[str, Any],
    check: Dict[str, Any],
    postflight: Optional[Dict[str, Any]]
) -> str:
    """Build CASCADE workflow panel."""
    lines = []
    
    # PREFLIGHT
    know = preflight.get("know", 0.0)
    uncertainty = preflight.get("uncertainty", 1.0)
    investigate = preflight.get("investigate_required", False)
    
    lines.append("[bold cyan]📊 PREFLIGHT[/bold cyan]")
    lines.append(f"   Assess: KNOW={know:.0%}, UNCERT={uncertainty:.0%}")
    if investigate:
        lines.append("   [yellow]→ INVESTIGATE REQUIRED[/yellow]")
    lines.append("")
    
    # INVESTIGATE (Investigation Tree)
    lines.append("[bold cyan]🔍 INVESTIGATE[/bold cyan]")
    if reflection:
        summary = reflection.get("reflection_summary", "")
        if summary:
            lines.append(f"   {summary[:55]}...")
        exp_count = len(reflection.get("relevant_experiences", []))
        if exp_count > 0:
            lines.append(f"   [dim]Branch: {exp_count} experiences[/dim]")
    lines.append("")
    
    # CHECK (Gate - 0-N times)
    lines.append("[bold cyan]✅ CHECK[/bold cyan]")
    confidence = check.get("confidence", 0.0)
    decision = check.get("decision", "UNKNOWN")
    decision_color = {
        "PROCEED": "green",
        "HALT": "red",
        "BRANCH": "yellow",
        "REVISE": "yellow"
    }.get(decision, "white")
    
    # Gate logic
    if confidence >= 0.7:
        gate_status = "[green]≥ 0.7 → PROCEED[/green]"
    else:
        gate_status = "[yellow]< 0.7 → INVESTIGATE[/yellow]"
    
    lines.append(f"   Confidence: {confidence:.0%}")
    lines.append(f"   Gate: {gate_status}")
    lines.append(f"   Decision: [{decision_color}]{decision}[/{decision_color}]")
    lines.append("")
    
    # ACT
    lines.append("[bold cyan]🎯 ACT[/bold cyan]")
    lines.append("   [dim]Generating recommendation...[/dim]")
    lines.append("")
    
    # POSTFLIGHT
    lines.append("[bold cyan]📈 POSTFLIGHT[/bold cyan]")
    if postflight:
        if postflight.get("guidance_provided"):
            know_delta = postflight.get("knowledge_delta", 0.0)
            unc_delta = postflight.get("uncertainty_delta", 0.0)
            lines.append("   [green]✓ Guidance provided[/green]")
            if know_delta != 0.0 or unc_delta != 0.0:
                lines.append(f"   [dim]Δ KNOW: {know_delta:+.2f}, Δ UNC: {unc_delta:+.2f}[/dim]")
            lines.append("   [dim]Learning tracked[/dim]")
    else:
        lines.append("   [dim]Pending...[/dim]")
    
    return "\n".join(lines)


def _build_epistemic_vectors_panel(
    preflight: Dict[str, Any],
    findings: List[Dict[str, Any]],
    unknowns: List[Dict[str, Any]],
    check: Dict[str, Any],
    epistemic_state: Dict[str, Any]
) -> str:
    """Build 13 epistemic vectors panel."""
    lines = []
    
    # Extract vectors
    if isinstance(epistemic_state, dict):
        if "epistemic_state" in epistemic_state:
            vectors = epistemic_state.get("epistemic_state", {}).get("vectors", {})
        else:
            vectors = epistemic_state.get("vectors", {})
    else:
        vectors = {}
    
    foundation = vectors.get("foundation", {})
    comprehension = vectors.get("comprehension", {})
    execution = vectors.get("execution", {})
    
    # Tier 0: Foundation
    lines.append("[bold]Tier 0: Foundation[/bold]")
    engagement = vectors.get("engagement", 0.0)
    know = foundation.get("know", 0.0) if foundation else 0.0
    do = foundation.get("do", 0.0) if foundation else 0.0
    context = foundation.get("context", 0.0) if foundation else 0.0
    
    lines.append(_create_progress_bar(engagement, "  Engagement", "cyan"))
    lines.append(_create_progress_bar(know, "  Know", "blue"))
    lines.append(_create_progress_bar(do, "  Do", "green"))
    lines.append(_create_progress_bar(context, "  Context", "magenta"))
    lines.append("")
    
    # Tier 1: Comprehension
    lines.append("[bold]Tier 1: Comprehension[/bold]")
    clarity = comprehension.get("clarity", 0.0) if comprehension else 0.0
    coherence = comprehension.get("coherence", 0.0) if comprehension else 0.0
    signal = comprehension.get("signal", 0.0) if comprehension else 0.0
    density = comprehension.get("density", 0.0) if comprehension else 0.0
    
    lines.append(_create_progress_bar(clarity, "  Clarity", "blue"))
    lines.append(_create_progress_bar(coherence, "  Coherence", "cyan"))
    lines.append(_create_progress_bar(signal, "  Signal", "green"))
    lines.append(_create_progress_bar(density, "  Density", "yellow"))
    lines.append("")
    
    # Tier 2: Execution
    lines.append("[bold]Tier 2: Execution[/bold]")
    exec_state = execution.get("state", 0.0) if execution else 0.0
    change = execution.get("change", 0.0) if execution else 0.0
    completion = execution.get("completion", 0.0) if execution else 0.0
    impact = execution.get("impact", 0.0) if execution else 0.0
    
    lines.append(_create_progress_bar(exec_state, "  State", "green"))
    lines.append(_create_progress_bar(change, "  Change", "yellow"))
    lines.append(_create_progress_bar(completion, "  Completion", "blue"))
    lines.append(_create_progress_bar(impact, "  Impact", "magenta"))
    lines.append("")
    
    # Meta: Uncertainty
    uncertainty = vectors.get("uncertainty", 1.0)
    uncertainty_bar = _create_progress_bar(uncertainty, "Uncertainty", "red", reverse=True)
    lines.append(uncertainty_bar)
    lines.append("")
    
    # Confidence (from CHECK gate)
    confidence = check.get("confidence", 0.0)
    confidence_bar = _create_progress_bar(confidence, "Confidence", "green")
    lines.append(confidence_bar)
    lines.append("")
    
    # Findings Stream (JSON-like)
    lines.append("[bold]Findings Stream:[/bold]")
    if findings:
        for finding in findings[:3]:  # Show last 3
            finding_text = finding.get("finding", finding.get("content", ""))[:45]
            impact = finding.get("impact", 0.5)
            color = "green" if impact > 0.7 else "yellow" if impact > 0.4 else "dim"
            lines.append(f"   [{color}]✓ {finding_text}...[/{color}]")
    else:
        lines.append("   [dim]No findings yet[/dim]")
    lines.append("")
    
    # Unknowns
    lines.append("[bold]Unknowns:[/bold]")
    if unknowns:
        for unknown in unknowns[:2]:  # Show last 2
            unknown_text = unknown.get("unknown", unknown.get("content", ""))[:45]
            lines.append(f"   [yellow]? {unknown_text}...[/yellow]")
    else:
        lines.append("   [dim]No unknowns[/dim]")
    
    return "\n".join(lines)


def _build_storage_status_panel(storage_info: Dict[str, Any]) -> str:
    """Build three-layer storage status panel."""
    lines = []
    
    lines.append("[bold]Layer 1: SQLite[/bold]")
    sqlite_status = storage_info.get("sqlite", {})
    if sqlite_status.get("available"):
        lines.append("   [green]✓ .empirica/sessions/sessions.db[/green]")
        lines.append(f"   [dim]Fast queries, real-time monitoring[/dim]")
    else:
        lines.append("   [dim]Not available[/dim]")
    lines.append("")
    
    lines.append("[bold]Layer 2: Git Notes[/bold]")
    git_status = storage_info.get("git_notes", {})
    if git_status.get("available"):
        lines.append("   [green]✓ git notes (compressed)[/green]")
        compression = git_status.get("compression", 0.0)
        if compression > 0:
            lines.append(f"   [dim]97% compression: {compression:.0%} token reduction[/dim]")
        lines.append(f"   [dim]Distributed, crypto-signable[/dim]")
    else:
        lines.append("   [dim]Not available[/dim]")
    lines.append("")
    
    lines.append("[bold]Layer 3: JSON Logs[/bold]")
    json_status = storage_info.get("json_logs", {})
    if json_status.get("available"):
        lines.append("   [green]✓ .empirica/reflexes/*.json[/green]")
        lines.append(f"   [dim]Full audit trail with reasoning[/dim]")
    else:
        lines.append("   [dim]Not available[/dim]")
    
    return "\n".join(lines)


def _create_progress_bar(value: float, label: str, color: str, reverse: bool = False) -> str:
    """Create a text-based progress bar."""
    bar_length = 20
    filled = int(value * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    if reverse:
        # For uncertainty, show as "remaining" (inverse)
        filled = bar_length - filled
        bar = "░" * (bar_length - filled) + "█" * filled
    
    return f"[{color}]{label}: {bar} {value:.0%}[/{color}]"


def display_thinking_step_by_step(
    console: Console,
    step: str,
    data: Dict[str, Any],
    delay: float = 0.5
) -> None:
    """
    Display a single thinking step with animation.
    
    Args:
        console: Rich console
        step: Step name (PREFLIGHT, INVESTIGATE, CHECK, ACT, POSTFLIGHT)
        data: Step data
        delay: Animation delay
    """
    step_icons = {
        "PREFLIGHT": "📊",
        "INVESTIGATE": "🔍",
        "CHECK": "✅",
        "ACT": "🎯",
        "POSTFLIGHT": "📈"
    }
    
    icon = step_icons.get(step, "•")
    
    with console.status(f"[bold cyan]{icon} {step}...[/bold cyan]"):
        time.sleep(delay)
    
    # Display step result
    if step == "PREFLIGHT":
        know = data.get("know", 0.0)
        uncertainty = data.get("uncertainty", 1.0)
        console.print(f"   [dim]KNOW: {know:.0%}, UNCERTAINTY: {uncertainty:.0%}[/dim]")
        if data.get("investigate_required"):
            console.print(f"   [yellow]→ INVESTIGATE REQUIRED[/yellow]")
    
    elif step == "INVESTIGATE":
        reflection = data.get("reflection", {})
        if reflection.get("reflection_summary"):
            console.print(f"   [dim]{reflection['reflection_summary'][:60]}...[/dim]")
    
    elif step == "CHECK":
        confidence = data.get("confidence", 0.0)
        decision = data.get("decision", "UNKNOWN")
        decision_color = {
            "PROCEED": "green",
            "HALT": "red",
            "BRANCH": "yellow",
            "REVISE": "yellow"
        }.get(decision, "white")
        console.print(f"   [dim]CONFIDENCE: {confidence:.0%}[/dim]")
        console.print(f"   [{decision_color}]→ DECISION: {decision}[/{decision_color}]")
    
    elif step == "ACT":
        console.print(f"   [dim]Generating recommendation...[/dim]")
    
    elif step == "POSTFLIGHT":
        if data.get("guidance_provided"):
            console.print(f"   [green]✓ Learning tracked[/green]")
