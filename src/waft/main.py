"""
Waft - Ambient, self-modifying Meta-Framework for Python

The "Operating System" for projects, orchestrating:
- Environment (uv)
- Memory (_pyrite)
- Agents (crewai)
- Epistemic Tracking (Empirica)
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .core.memory import MemoryManager
from .core.substrate import SubstrateManager
from .core.empirica import EmpiricaManager
from .utils import resolve_project_path, validate_waft_project
from .cli.epistemic_display import (
    get_moon_phase,
    format_epistemic_summary,
    create_epistemic_dashboard,
)

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

    # Step 4: Initialize Empirica (if git is available)
    console.print("[dim]→[/dim] Initializing Empirica for epistemic tracking...")
    empirica = EmpiricaManager(project_path)
    empirica_initialized = empirica.initialize()
    if empirica_initialized:
        console.print("[green]✅[/green] Empirica initialized")
        
        # Load project-bootstrap context and show epistemic state
        context = empirica.project_bootstrap()
        if context:
            epistemic_summary = format_epistemic_summary(context.get("epistemic_state"))
            console.print(f"[dim]📊 {epistemic_summary}[/dim]")
    else:
        console.print("[yellow]⚠️[/yellow]  Empirica not initialized (git may not be available)")

    # Success message with epistemic indicator
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
    
    success_panel = Panel(
        Text.from_markup(
            f"[bold green]Project '{name}' created successfully![/bold green]\n\n"
            f"{moon_phase} [dim]Epistemic tracking active[/dim]\n\n"
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
    project_path = resolve_project_path(path)

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

    # Check epistemic health if Empirica is initialized
    empirica = EmpiricaManager(project_path)
    if empirica.is_initialized():
        console.print("\n[dim]→[/dim] Checking epistemic health...")
        context = empirica.project_bootstrap()
        if context:
            epistemic_state = context.get("epistemic_state", {})
            epistemic_summary = format_epistemic_summary(epistemic_state)
            console.print(f"[dim]📊 {epistemic_summary}[/dim]")
        else:
            console.print("[dim]📊 Epistemic state not available[/dim]")

    # Summary
    all_valid = pyrite_status["valid"] and lock_exists

    if all_valid:
        # Show moon phase in summary
        moon_phase = "🌑"
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
        console.print(f"\n[bold green]✅ Project structure is valid {moon_phase}[/bold green]")
    else:
        console.print("\n[bold yellow]⚠️  Project structure has issues[/bold yellow]")
        raise typer.Exit(1)


@app.command()
def sync(
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """
    Sync project dependencies using uv sync.
    """
    project_path = Path(path) if path else Path.cwd()

    console.print(f"\n[bold cyan]🌊 Waft[/bold cyan] - Syncing dependencies\n")

    substrate = SubstrateManager()
    console.print("[dim]→[/dim] Running uv sync...")

    success = substrate.sync(project_path)

    if success:
        console.print("[green]✅[/green] Dependencies synced successfully")
    else:
        console.print("[bold red]❌ Failed to sync dependencies[/bold red]")
        raise typer.Exit(1)


@app.command()
def add(
    package: str = typer.Argument(..., help="Package name (e.g., 'pytest>=7.0.0')"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    dev: bool = typer.Option(False, "--dev", "-d", help="Add as development dependency"),
):
    """
    Add a dependency to the project using uv add.
    """
    project_path = Path(path) if path else Path.cwd()

    console.print(f"\n[bold cyan]🌊 Waft[/bold cyan] - Adding dependency: [bold]{package}[/bold]\n")

    substrate = SubstrateManager()

    if dev:
        console.print("[dim]→[/dim] Adding development dependency...")
        # For dev dependencies, we'd need to use uv add --dev
        # For now, just add normally
        console.print("[yellow]⚠️[/yellow]  Dev flag not yet fully supported, adding as regular dependency")

    console.print(f"[dim]→[/dim] Running uv add {package}...")

    success = substrate.add_dependency(package, project_path)

    if success:
        console.print(f"[green]✅[/green] Dependency '{package}' added successfully")
    else:
        console.print(f"[bold red]❌ Failed to add dependency '{package}'[/bold red]")
        raise typer.Exit(1)


@app.command()
def init(
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """
    Initialize Waft structure in an existing project.

    This command:
    1. Creates the _pyrite directory structure
    2. Writes templates (Justfile, CI, agents.py)
    3. Does NOT run uv init (assumes project already exists)
    """
    project_path = Path(path) if path else Path.cwd()

    console.print(f"\n[bold cyan]🌊 Waft[/bold cyan] - Initializing Waft in existing project\n")

    # Check if pyproject.toml exists
    if not (project_path / "pyproject.toml").exists():
        console.print("[yellow]⚠️[/yellow]  No pyproject.toml found. This command is for existing projects.")
        console.print("[dim]→[/dim] Use 'waft new <name>' to create a new project instead.")
        raise typer.Exit(1)

    # Step 1: Create _pyrite structure
    memory = MemoryManager(project_path)
    console.print("[dim]→[/dim] Creating _pyrite memory structure...")
    memory.create_structure()
    console.print("[green]✅[/green] _pyrite structure created")

    # Step 2: Write templates
    console.print("[dim]→[/dim] Writing templates...")
    from .templates import TemplateWriter

    template_writer = TemplateWriter(project_path)
    template_writer.write_all()
    console.print("[green]✅[/green] Templates written")

    # Step 3: Initialize Empirica (if git is available)
    console.print("[dim]→[/dim] Initializing Empirica for epistemic tracking...")
    empirica = EmpiricaManager(project_path)
    empirica_initialized = empirica.initialize()
    if empirica_initialized:
        console.print("[green]✅[/green] Empirica initialized")
        
        # Show epistemic state after initialization
        context = empirica.project_bootstrap()
        if context:
            epistemic_summary = format_epistemic_summary(context.get("epistemic_state"))
            console.print(f"[dim]📊 {epistemic_summary}[/dim]")
    else:
        console.print("[yellow]⚠️[/yellow]  Empirica not initialized (git may not be available)")

    # Success message with epistemic indicator
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
    
    success_panel = Panel(
        Text.from_markup(
            f"[bold green]Waft initialized successfully![/bold green]\n\n"
            f"{moon_phase} [dim]Epistemic tracking active[/dim]\n\n"
            "[dim]Next steps:[/dim]\n"
            "  waft verify   # Verify structure\n"
            "  waft sync     # Sync dependencies (if needed)\n"
        ),
        title="🌊 Waft",
        border_style="green",
    )
    console.print(success_panel)


@app.command()
def info(
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """
    Show information about the Waft project.
    """
    project_path = resolve_project_path(path)

    console.print(f"\n[bold cyan]🌊 Waft[/bold cyan] - Project Information\n")

    from rich.table import Table

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Property", style="dim")
    table.add_column("Value")

    # Project path
    table.add_row("Project Path", str(project_path.resolve()))

    # Check pyproject.toml
    substrate = SubstrateManager()
    project_info = substrate.get_project_info(project_path)

    if project_info:
        table.add_row("Project Name", project_info.get("name", "Unknown"))
        table.add_row("Version", project_info.get("version", "Unknown"))
    else:
        pyproject_path = project_path / "pyproject.toml"
        if pyproject_path.exists():
            table.add_row("Project Name", "[yellow]pyproject.toml exists (parse error)[/yellow]")
            table.add_row("Version", "[yellow]N/A[/yellow]")
        else:
            table.add_row("Project Name", "[red]Not a Python project[/red]")
            table.add_row("Version", "[red]N/A[/red]")

    # Check _pyrite
    memory = MemoryManager(project_path)
    pyrite_status = memory.verify_structure()
    table.add_row("_pyrite Structure", "[green]Valid[/green]" if pyrite_status["valid"] else "[red]Invalid[/red]")

    # Check uv.lock
    substrate = SubstrateManager()
    lock_exists = substrate.verify_lock(project_path)
    table.add_row("uv.lock", "[green]Exists[/green]" if lock_exists else "[yellow]Missing[/yellow]")

    # Check templates
    justfile_exists = (project_path / "Justfile").exists()
    ci_exists = (project_path / ".github" / "workflows" / "ci.yml").exists()
    agents_exists = (project_path / "src" / "agents.py").exists()

    templates_status = []
    if justfile_exists:
        templates_status.append("[green]Justfile[/green]")
    if ci_exists:
        templates_status.append("[green]CI[/green]")
    if agents_exists:
        templates_status.append("[green]agents.py[/green]")

    table.add_row("Templates", ", ".join(templates_status) if templates_status else "[yellow]None[/yellow]")

    # Check Empirica
    empirica = EmpiricaManager(project_path)
    empirica_status = "[green]Initialized[/green]" if empirica.is_initialized() else "[yellow]Not initialized[/yellow]"
    table.add_row("Empirica", empirica_status)

    # Add Epistemic State section if Empirica is initialized
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
            
            table.add_row("Epistemic State", f"{moon_phase} K:{know:.0%} U:{uncertainty:.0%} C:{coverage:.0%}")
            table.add_row("", "[dim]Run 'waft assess' for detailed view[/dim]")

    console.print(table)


@app.command()
def serve(
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    port: int = typer.Option(8000, "--port", help="Port to serve on"),
    host: str = typer.Option("localhost", "--host", help="Host to bind to"),
    dev: bool = typer.Option(False, "--dev", help="Enable development mode with live reloading"),
):
    """
    Start a web dashboard for the Waft project.

    Opens a web interface at http://localhost:8000 (default) to view
    project information, structure, and _pyrite contents.

    Use --dev to enable live reloading when code changes are saved.
    """
    project_path = resolve_project_path(path)

    # Check if this is a Waft project
    is_valid, error = validate_waft_project(project_path)
    if not is_valid:
        console.print("[bold red]❌ Not a Waft project[/bold red]")
        console.print(f"[dim]{error}[/dim]")
        raise typer.Exit(1)

    from .web import serve as serve_web

    try:
        serve_web(project_path, port=port, host=host, dev=dev)
    except OSError as e:
        if "Address already in use" in str(e):
            console.print(f"[bold red]❌ Port {port} is already in use[/bold red]")
            console.print(f"[dim]Try a different port with --port[/dim]")
        else:
            console.print(f"[bold red]❌ Error starting server: {e}[/bold red]")
        raise typer.Exit(1)


def main():
    """Entry point for the waft CLI."""
    app()


if __name__ == "__main__":
    main()

