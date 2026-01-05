"""
Waft - Ambient, self-modifying Meta-Framework for Python

The "Operating System" for projects, orchestrating:
- Environment (uv)
- Memory (_pyrite)
- Agents (crewai)
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .core.memory import MemoryManager
from .core.substrate import SubstrateManager

app = typer.Typer(
    name="waft",
    help="Waft - Ambient Meta-Framework for Python",
    add_completion=False,
)

console = Console()


@app.command()
def new(
    name: str = typer.Argument(..., help="Project name"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Target directory (default: current)"),
):
    """
    Create a new project with full Waft structure.
    
    This command:
    1. Runs `uv init <name>`
    2. Creates the full `_pyrite` directory structure
    3. Writes templates (Justfile, CI, agents.py)
    4. Sets up the project for high-reliability development
    """
    target_path = Path(path) if path else Path.cwd()
    project_path = target_path / name
    
    console.print(f"\n[bold cyan]🌊 Waft[/bold cyan] - Creating project: [bold]{name}[/bold]\n")
    
    # Ensure project directory exists
    project_path.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Initialize uv project
    substrate = SubstrateManager()
    console.print("[dim]→[/dim] Initializing uv project...")
    success = substrate.init_project(name, target_path)
    
    if not success:
        console.print("[bold red]❌ Failed to initialize uv project[/bold red]")
        raise typer.Exit(1)
    
    console.print("[green]✅[/green] uv project initialized")
    
    # Verify project was created
    if not project_path.exists():
        console.print(f"[bold red]❌ Project directory not created: {project_path}[/bold red]")
        raise typer.Exit(1)
    
    # Step 2: Create _pyrite structure
    memory = MemoryManager(project_path)
    console.print("[dim]→[/dim] Creating _pyrite memory structure...")
    memory.create_structure()
    console.print("[green]✅[/green] _pyrite structure created")
    
    # Step 3: Write templates
    console.print("[dim]→[/dim] Writing templates...")
    from .templates import TemplateWriter
    
    template_writer = TemplateWriter(project_path)
    template_writer.write_all()
    console.print("[green]✅[/green] Templates written")
    
    # Success message
    success_panel = Panel(
        Text.from_markup(
            f"[bold green]Project '{name}' created successfully![/bold green]\n\n"
            f"[dim]Next steps:[/dim]\n"
            f"  cd {name}\n"
            f"  just setup    # Install dependencies\n"
            f"  just verify   # Run validation\n"
            f"  waft verify   # Verify structure\n"
        ),
        title="🌊 Waft",
        border_style="green",
    )
    console.print(success_panel)


@app.command()
def verify(
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """
    Verify the Waft project structure.
    
    Checks:
    - _pyrite directory exists with required subfolders
    - uv.lock exists
    - Project structure is valid
    """
    project_path = Path(path) if path else Path.cwd()
    
    console.print(f"\n[bold cyan]🌊 Waft[/bold cyan] - Verifying project structure\n")
    
    memory = MemoryManager(project_path)
    substrate = SubstrateManager()
    
    # Check _pyrite structure
    console.print("[dim]→[/dim] Checking _pyrite structure...")
    pyrite_status = memory.verify_structure()
    
    if pyrite_status["valid"]:
        console.print("[green]✅[/green] _pyrite structure is valid")
        for folder, exists in pyrite_status["folders"].items():
            status = "[green]✓[/green]" if exists else "[red]✗[/red]"
            console.print(f"  {status} {folder}")
    else:
        console.print("[red]❌[/red] _pyrite structure is invalid")
        for folder, exists in pyrite_status["folders"].items():
            if not exists:
                console.print(f"  [red]✗ Missing:[/red] {folder}")
    
    # Check uv.lock
    console.print("\n[dim]→[/dim] Checking uv.lock...")
    lock_exists = substrate.verify_lock(project_path)
    
    if lock_exists:
        console.print("[green]✅[/green] uv.lock exists")
    else:
        console.print("[yellow]⚠️[/yellow]  uv.lock not found (run 'uv sync' to create)")
    
    # Summary
    all_valid = pyrite_status["valid"] and lock_exists
    
    if all_valid:
        console.print("\n[bold green]✅ Project structure is valid[/bold green]")
    else:
        console.print("\n[bold yellow]⚠️  Project structure has issues[/bold yellow]")
        raise typer.Exit(1)


def main():
    """Entry point for the waft CLI."""
    app()


if __name__ == "__main__":
    main()
