#!/usr/bin/env python3
"""
Waft Framework - Interactive Demo

This demo showcases all of waft's capabilities:
- Memory Manager (_pyrite structure)
- Substrate Manager (uv/environment)
- Gamification Manager (integrity, insight, achievements)
- CLI integration
- Project lifecycle

Run with: python3 demo.py
"""

import tempfile
import shutil
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

from waft.core.memory import MemoryManager
from waft.core.substrate import SubstrateManager
from waft.core.gamification import GamificationManager

console = Console()


def print_header(text: str):
    """Print a section header."""
    console.print(f"\n[bold cyan]🌊 {text}[/bold cyan]\n")


def demo_memory_manager(project_path: Path):
    """Demonstrate Memory Manager capabilities."""
    print_header("Memory Manager - _pyrite Structure")

    memory = MemoryManager(project_path)

    # Create structure
    console.print("[dim]→[/dim] Creating _pyrite structure...")
    memory.create_structure()
    console.print("[green]✅[/green] Structure created")

    # Add files to active
    console.print("\n[dim]→[/dim] Adding files to active/...")
    (project_path / "_pyrite" / "active" / "current_work.md").write_text(
        "# Current Work\n\nWorking on demo features."
    )
    (project_path / "_pyrite" / "active" / "ideas.md").write_text(
        "# Ideas\n\n- Feature A\n- Feature B"
    )
    console.print("[green]✅[/green] Added 2 files to active/")

    # Add files to backlog
    console.print("\n[dim]→[/dim] Adding files to backlog/...")
    (project_path / "_pyrite" / "backlog" / "future_feature.md").write_text(
        "# Future Feature\n\nTo be implemented later."
    )
    console.print("[green]✅[/green] Added 1 file to backlog/")

    # List files
    console.print("\n[bold]File Organization:[/bold]")
    table = Table(show_header=True, header_style="bold")
    table.add_column("Location", style="cyan")
    table.add_column("Files", style="green")

    active_files = memory.get_active_files()
    backlog_files = memory.get_backlog_files()
    standards_files = memory.get_standards_files()

    table.add_row("active/", ", ".join([f.name for f in active_files]))
    table.add_row("backlog/", ", ".join([f.name for f in backlog_files]))
    table.add_row("standards/", ", ".join([f.name for f in standards_files]) if standards_files else "(empty)")

    console.print(table)

    # Verify structure
    result = memory.verify_structure()
    status = "[green]Valid[/green]" if result["valid"] else "[red]Invalid[/red]"
    console.print(f"\n[bold]Structure Status:[/bold] {status}")


def demo_substrate_manager(project_path: Path):
    """Demonstrate Substrate Manager capabilities."""
    print_header("Substrate Manager - Environment & Dependencies")

    substrate = SubstrateManager(project_path)

    # Get project info
    console.print("[dim]→[/dim] Reading project information...")
    info = substrate.get_project_info()

    table = Table(show_header=True, header_style="bold")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Project Name", info.get("name", "Unknown"))
    table.add_row("Version", info.get("version", "Unknown"))
    table.add_row("uv.lock", "[green]Exists[/green]" if substrate.verify_lock() else "[yellow]Missing[/yellow]")

    console.print(table)

    # Show dependency management
    console.print("\n[bold]Dependency Management:[/bold]")
    console.print("[dim]→[/dim] Use 'waft add <package>' to add dependencies")
    console.print("[dim]→[/dim] Use 'waft sync' to sync dependencies")
    console.print("[dim]→[/dim] Use 'waft verify' to check project health")


def demo_gamification(project_path: Path):
    """Demonstrate Gamification Manager capabilities."""
    print_header("Gamification Manager - Integrity & Insight")

    gamification = GamificationManager(project_path)

    # Show initial stats
    console.print("[bold]Initial Stats:[/bold]")
    stats = gamification.get_stats()

    table = Table(show_header=True, header_style="bold")
    table.add_column("Stat", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("💎 Integrity", f"{stats['integrity']:.0f}%")
    table.add_row("🧠 Insight", f"{stats['insight']:.0f}")
    table.add_row("⭐ Level", str(stats['level']))
    table.add_row("🏆 Achievements", str(stats['achievements_count']))

    console.print(table)

    # Award insight
    console.print("\n[dim]→[/dim] Awarding 100 insight for completing demo...")
    result = gamification.award_insight(100.0, reason="Completed demo exploration")

    if result["level_up"]:
        console.print(f"[bold green]🎉 Level Up![/bold green] Level {result['old_level']} → {result['new_level']}")

    # Show updated stats
    console.print("\n[bold]Updated Stats:[/bold]")
    stats = gamification.get_stats()

    table = Table(show_header=True, header_style="bold")
    table.add_column("Stat", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("💎 Integrity", f"{stats['integrity']:.0f}%")
    table.add_row("🧠 Insight", f"{stats['insight']:.0f}")
    table.add_row("⭐ Level", str(stats['level']))

    console.print(table)

    # Show achievements
    console.print("\n[bold]Achievements:[/bold]")
    achievement_status = gamification.get_achievement_status()

    achievement_names = {
        "first_build": "🌱 First Build",
        "constructor": "🏗️ Constructor",
        "goal_achiever": "🎯 Goal Achiever",
        "knowledge_architect": "🧠 Knowledge Architect",
        "perfect_integrity": "💎 Perfect Integrity",
        "level_10": "🚀 Level 10",
        "master_constructor": "🏆 Master Constructor",
        "epistemic_master": "🌙 Epistemic Master",
    }

    table = Table(show_header=True, header_style="bold")
    table.add_column("Achievement", style="cyan")
    table.add_column("Status", style="green")

    for achievement_id, unlocked in achievement_status.items():
        name = achievement_names.get(achievement_id, achievement_id)
        status = "[green]✓ Unlocked[/green]" if unlocked else "[dim]🔒 Locked[/dim]"
        table.add_row(name, status)

    console.print(table)

    # Demonstrate integrity changes
    console.print("\n[bold]Integrity System:[/bold]")
    console.print("[dim]→[/dim] Integrity decreases with errors/issues")
    console.print("[dim]→[/dim] Integrity increases with successful operations")
    console.print(f"[dim]→[/dim] Current integrity: [bold]{gamification.integrity:.0f}%[/bold]")


def demo_project_lifecycle():
    """Demonstrate full project lifecycle."""
    print_header("Project Lifecycle Demo")

    # Create temporary project
    temp_dir = Path(tempfile.mkdtemp())
    project_path = temp_dir / "demo_project"
    project_path.mkdir()

    try:
        # Create pyproject.toml
        pyproject = project_path / "pyproject.toml"
        pyproject.write_text(
            """[project]
name = "demo-project"
version = "0.1.0"
description = "Waft demo project"
"""
        )

        console.print(f"[green]✅[/green] Created demo project at: {project_path}")

        # Run all demos
        demo_memory_manager(project_path)
        demo_substrate_manager(project_path)
        demo_gamification(project_path)

        # Summary
        console.print("\n" + "="*60)
        console.print("[bold green]Demo Complete![/bold green]")
        console.print("="*60)

        console.print("\n[bold]What we demonstrated:[/bold]")
        console.print("  • Memory Manager - _pyrite structure and file organization")
        console.print("  • Substrate Manager - Project info and dependency management")
        console.print("  • Gamification Manager - Integrity, insight, leveling, achievements")
        console.print("  • Full project lifecycle")

        console.print(f"\n[dim]Demo project location: {project_path}[/dim]")
        console.print("[dim]Project will be cleaned up automatically[/dim]")

    finally:
        # Cleanup
        shutil.rmtree(temp_dir)


def main():
    """Run the interactive demo."""
    console.print(Panel.fit(
        "[bold cyan]🌊 Waft Framework - Interactive Demo[/bold cyan]\n\n"
        "This demo showcases all of waft's core capabilities:\n"
        "• Memory Manager (_pyrite structure)\n"
        "• Substrate Manager (uv/environment)\n"
        "• Gamification Manager (integrity, insight, achievements)\n"
        "• Full project lifecycle",
        title="Welcome",
        border_style="cyan"
    ))

    with console.status("[bold green]Running demo...", spinner="dots"):
        time.sleep(1)
        demo_project_lifecycle()

    console.print("\n[bold cyan]✨ Thanks for exploring waft![/bold cyan]\n")


if __name__ == "__main__":
    main()


