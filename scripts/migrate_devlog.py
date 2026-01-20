#!/usr/bin/env python3
"""
Migrate Legacy Devlog to Categorized Structure

Migrates existing devlog.md to the new categorized devlog structure.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console

from waft.core.devlog import DevlogManager

console = Console()


def main():
    """Migrate legacy devlog to new structure."""
    console.print("\n[bold cyan]📦 Migrating Legacy Devlog[/bold cyan]\n")

    project_path = Path(__file__).parent.parent
    devlog_manager = DevlogManager(project_path)

    console.print("[yellow]→[/yellow] Starting migration...")
    result = devlog_manager.migrate_legacy_devlog()

    console.print("[green]✓[/green] Migration complete!")
    console.print(f"[dim]Entries migrated: {result['migrated']}[/dim]")

    if result.get("errors"):
        console.print(f"[yellow]⚠[/yellow]  Errors: {len(result['errors'])}")
        for error in result["errors"]:
            console.print(f"[dim]  - {error['entry']}: {error['error']}[/dim]")

    console.print("\n[bold green]✅ Migration complete![/bold green]\n")
    console.print("[dim]Legacy devlog.md is preserved for backward compatibility.[/dim]")
    console.print("[dim]New entries will be written to categorized structure.[/dim]\n")


if __name__ == "__main__":
    main()
