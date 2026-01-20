"""
Self-Engineering Notebook Demo

Demonstrates how the notebook system journals findings, reflects on them,
and creates actionable work (work efforts, scenarios, quests).
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console

from waft.core.empirica import EmpiricaManager
from waft.core.self_engineering import (
    ActionableCreator,
    NotebookManager,
    ProblemDetector,
)

console = Console()


def demo_notebook_system():
    """Demonstrate the notebook system."""

    console.print(
        "\n[bold bright_blue]╔════════════════════════════════════════╗[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]║[/bold bright_blue]  [bold white]SELF-ENGINEERING NOTEBOOK DEMO[/bold white]  [bold bright_blue]║[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]║[/bold bright_blue]  [dim]Journal → Reflect → Create Actionables[/dim]  [bold bright_blue]║[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]╚════════════════════════════════════════╝[/bold bright_blue]\n"
    )

    project_path = Path(__file__).parent.parent
    notebook_dir = project_path / "_notebook"

    # Initialize Empirica (if available)
    console.print("[yellow]→[/yellow] Checking Empirica...")
    empirica = EmpiricaManager(project_path)
    if empirica.is_initialized():
        console.print("[green]✓[/green] Empirica initialized - epistemic tracking enabled")
        epistemic_context = empirica.project_bootstrap()
        if epistemic_context:
            uncertainty = (
                epistemic_context.get("epistemic_state", {})
                .get("vectors", {})
                .get("uncertainty", 0.5)
            )
            console.print(f"[dim]  Current uncertainty: {uncertainty:.2f}[/dim]")
    else:
        console.print("[yellow]⚠[/yellow]  Empirica not initialized - epistemic tracking disabled")
        empirica = None

    # Initialize notebook with Empirica
    console.print("\n[yellow]→[/yellow] Initializing notebook...")
    notebook = NotebookManager(notebook_dir, empirica_manager=empirica)
    console.print("[green]✓[/green] Notebook initialized at: _notebook/")
    if empirica:
        console.print("[green]✓[/green] Empirica integration enabled")

    # Initialize problem detector with notebook
    console.print("\n[yellow]→[/yellow] Initializing problem detector with notebook...")
    detector = ProblemDetector(notebook_manager=notebook)
    console.print("[green]✓[/green] Problem detector ready (auto-journaling enabled)")

    # Simulate a problem (EOFError from interactive input)
    console.print("\n[yellow]→[/yellow] Simulating problem detection...")
    execution_result = {
        "exception": EOFError("EOF when reading a line"),
        "error_message": "EOF when reading a line",
        "context": {
            "scenario": "tavern_scenario.py",
            "line": 50,
            "function": "create_character",
            "interactive": True,
        },
        "traceback": 'Traceback (most recent call last):\n  File "tavern_scenario.py", line 50...',
    }

    problems = detector.monitor_execution(execution_result, execution_time=0.5)

    console.print(f"[green]✓[/green] Detected {len(problems)} problem(s)")
    for problem in problems:
        console.print(f"  - {problem.type.value}: {problem.description[:60]}...")
        console.print(f"    Severity: {problem.severity.value}")

    # Get journaled entries
    console.print("\n[yellow]→[/yellow] Retrieving journaled entries...")
    entries = notebook.get_entries()
    console.print(f"[green]✓[/green] Found {len(entries)} journaled entry/entries")

    # Show entry details
    if entries:
        entry = entries[0]
        console.print("\n[bold]Entry Details:[/bold]")
        console.print(f"  ID: {entry.entry_id}")
        console.print(f"  Type: {entry.entry_type.value}")
        console.print(f"  Title: {entry.title}")
        console.print(f"  Timestamp: {entry.timestamp}")

    # Create a reflection
    console.print("\n[yellow]→[/yellow] Creating reflection on findings...")
    reflection = notebook.journal_reflection(
        entries=entries,
        insights=[
            "System requires interactive input but runs in non-interactive mode",
            "Need to add non-interactive mode or input simulation",
        ],
        patterns=[
            "EOFError occurs consistently in non-interactive environments",
            "All interactive scenarios fail when run programmatically",
        ],
        questions=[
            "How to handle interactive input in automated scenarios?",
            "Should we add a non-interactive mode or simulate input?",
        ],
    )
    console.print(f"[green]✓[/green] Reflection created: {reflection.reflection_id}")
    console.print(f"  Insights: {len(reflection.insights)}")
    console.print(f"  Patterns: {len(reflection.patterns)}")
    console.print(f"  Actionable Suggestions: {len(reflection.actionable_suggestions)}")

    # Show actionable suggestions
    if reflection.actionable_suggestions:
        console.print("\n[bold]Actionable Suggestions:[/bold]")
        for i, suggestion in enumerate(reflection.actionable_suggestions, 1):
            console.print(f"  {i}. {suggestion['type']}: {suggestion['title']}")

    # Initialize actionable creator with Empirica
    console.print("\n[yellow]→[/yellow] Initializing actionable creator...")
    creator = ActionableCreator(
        project_path=project_path,
        work_efforts_dir=project_path / "_work_efforts",
        scenarios_dir=project_path / "examples",
        quests_dir=project_path / "src/gym/rpg/dungeons",
        empirica_manager=empirica,
    )
    console.print("[green]✓[/green] Actionable creator ready")
    if empirica:
        console.print("[green]✓[/green] Empirica CHECK gates enabled")

    # Create work effort from entry
    if entries:
        console.print("\n[yellow]→[/yellow] Creating work effort from entry...")
        work_effort = creator.create_work_effort_from_entry(entries[0])
        console.print("[green]✓[/green] Work effort data prepared:")
        console.print(f"  ID: {work_effort['id']}")
        console.print(f"  Title: {work_effort['title']}")
        console.print(f"  Priority: {work_effort['priority']}")
        console.print(
            "\n[dim]Note: Use MCP work-efforts server to create actual work effort:[/dim]"
        )
        console.print("[dim]  mcp_work-efforts_create_work_effort(...)[/dim]")

    # Summary
    console.print("\n[bold green]✓ Demo Complete![/bold green]")
    console.print("\n[bold]Summary:[/bold]")
    console.print(f"  Problems Detected: {len(problems)}")
    console.print(f"  Entries Journaled: {len(entries)}")
    console.print("  Reflections Created: 1")
    console.print(f"  Actionable Suggestions: {len(reflection.actionable_suggestions)}")
    console.print(f"\n[dim]Notebook Location: {notebook_dir}[/dim]")
    console.print("[dim]Check _notebook/entries/ and _notebook/reflections/ for details[/dim]\n")


if __name__ == "__main__":
    demo_notebook_system()
