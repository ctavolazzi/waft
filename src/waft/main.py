"""
Waft - Ambient, self-modifying Meta-Framework for Python

The "Operating System" for projects, orchestrating:
- Environment (uv)
- Memory (_pyrite)
- Agents (crewai)
- Epistemic Tracking (Empirica)
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .cli.chief_cli import app as chief_app
from .cli.epistemic_display import (
    create_epistemic_dashboard,
    format_epistemic_summary,
    get_moon_phase,
)
from .cli.hud import render_hud
from .cli.project_commands import app as project_app
from .cli.pyrite_cli import app as pyrite_app
from .core.analytics_cli import app as analytics_app
from .core.empirica import EmpiricaManager
from .core.gamification import GamificationManager
from .core.memory import MemoryManager
from .core.substrate import SubstrateManager
from .core.tavern_keeper import Narrator, TavernKeeper
from .logging import get_logger
from .utils import (
    is_inside_waft_project,
    resolve_project_path,
    validate_package_name,
    validate_project_name,
    validate_waft_project,
)

app = typer.Typer(
    name="waft",
    help="Waft - Ambient Meta-Framework for Python",
    add_completion=False,
)

console = Console()
logger = get_logger(__name__)


def _process_tavern_hook(
    project_path: Path, command: str, success: bool, context: dict | None = None
) -> None:
    """
    Helper function to process TavernKeeper command hooks.

    Args:
        project_path: Path to project
        command: Command name
        success: Whether command succeeded
        context: Optional context dict
    """
    try:
        tavern = TavernKeeper(project_path)
        hook_result = tavern.process_command_hook(command, success, context)

        # Display narrative if available
        if hook_result.get("narrative"):
            console.print(f"\n[dim]# {hook_result['narrative']}[/dim]")

        # Show dice roll result
        dice_result = hook_result.get("dice_result", {})
        if dice_result:
            roll = dice_result.get("roll", 0)
            total = dice_result.get("total", 0)
            dc = dice_result.get("dc", 0)
            classification = dice_result.get("classification", "")

            # Color based on classification
            if classification == "critical_success":
                color = "bold gold1"
            elif classification == "critical_failure":
                color = "bold red"
            elif classification == "superior":
                color = "gold1"
            elif classification == "optimal":
                color = "green"
            else:
                color = "dim"

            ability_map = {
                "new": "CHA",
                "verify": "CON",
                "init": "WIS",
                "info": "WIS",
                "sync": "INT",
                "add": "CHA",
                "finding_log": "INT",
                "assess": "WIS",
                "check": "WIS",
                "goal_create": "CHA",
            }
            ability = ability_map.get(command, "WIS")
            console.print(
                f"[{color}]🎲 {ability} Check: {roll} + {dice_result.get('modifier', 0)} = {total} (DC {dc}) - {classification}[/{color}]"
            )

        # Show rewards
        rewards = hook_result.get("rewards", {})
        if rewards.get("level_up"):
            console.print(
                f"[bold gold1]🎉 LEVEL UP! Level {rewards.get('old_level', 1)} → {rewards.get('new_level', 1)}[/bold gold1]"
            )
        if hook_result.get("xp_gained", 0) > 0:
            credits = hook_result.get("rewards", {}).get("new_credits", 0)
            if credits > 0:
                console.print(
                    f"[dim]✨ +{hook_result['xp_gained']} Insight, +{credits} Credits[/dim]"
                )
            else:
                console.print(f"[dim]✨ +{hook_result['xp_gained']} Insight[/dim]")
    except (ImportError, AttributeError, FileNotFoundError) as e:
        logger.debug(f"TavernKeeper hook failed (not critical): {e}")


@app.command()
def new(
    name: str = typer.Argument(..., help="Project name"),
    path: str | None = typer.Option(
        None, "--path", "-p", help="Target directory (default: current)"
    ),
):
    """
    Create a new project with full Waft structure.

    This command:
    1. Runs `uv init <name>`
    2. Creates the full `_pyrite` directory structure
    3. Writes templates (Justfile, CI, agents.py)
    4. Sets up the project for high-reliability development
    """
    # Validate project name
    is_valid, error_msg = validate_project_name(name)
    if not is_valid:
        console.print(f"[bold red]❌ Invalid project name: {error_msg}[/bold red]")
        raise typer.Exit(1)

    # Resolve and validate target path
    try:
        target_path = Path(path) if path else Path.cwd()
        target_path = target_path.resolve()

        if not target_path.exists():
            console.print(f"[bold red]❌ Target directory does not exist: {target_path}[/bold red]")
            raise typer.Exit(1)

        if not target_path.is_dir():
            console.print(f"[bold red]❌ Target path is not a directory: {target_path}[/bold red]")
            raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]❌ Invalid path: {e}[/bold red]")
        raise typer.Exit(1)

    # Check for nested project creation
    is_inside, waft_project = is_inside_waft_project(target_path)
    if is_inside and waft_project:
        console.print("[bold red]❌ Cannot create project inside existing Waft project[/bold red]")
        console.print(f"[dim]Target directory is inside: {waft_project}[/dim]")
        console.print("[dim]→[/dim] Create the project outside the Waft project directory")
        raise typer.Exit(1)

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

    # Award insight for creating project
    gamification = GamificationManager(project_path)
    insight_result = gamification.award_insight(50.0, reason="Created new project")

    # TavernKeeper: Character creation event
    _process_tavern_hook(project_path, "new", True, {"project_name": name})

    # Check for achievements
    stats = gamification.get_stats()
    newly_unlocked = gamification.check_achievements(stats)

    # Check for First Build achievement
    if gamification.unlock_achievement("first_build", "🌱 First Build"):
        newly_unlocked.append("first_build")
        console.print("[bold green]🏆 Achievement Unlocked: 🌱 First Build[/bold green]")

    # Show level up notification
    if insight_result["level_up"]:
        console.print(
            f"[bold cyan]🎉 Level Up! Level {insight_result['old_level']} → {insight_result['new_level']}[/bold cyan]"
        )

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

    integrity = gamification.integrity
    insight = gamification.insight
    level = gamification.level

    success_panel = Panel(
        Text.from_markup(
            f"[bold green]Project '{name}' created successfully![/bold green]\n\n"
            f"{moon_phase} [dim]Epistemic tracking active[/dim]\n"
            f"💎 Integrity: {integrity:.0f}% | 🧠 Insight: {insight:.0f} | ⭐ Level: {level}\n\n"
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
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """
    Verify the Waft project structure.

    Checks:
    - _pyrite directory exists with required subfolders
    - uv.lock exists
    - Project structure is valid
    """
    project_path = resolve_project_path(path)

    console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Verifying project structure\n")

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

    # Update integrity based on verification result
    gamification = GamificationManager(project_path)
    if all_valid:
        gamification.restore_integrity(2.0, reason="Project verification passed")
    else:
        gamification.damage_integrity(10.0, reason="Project verification failed")

    # TavernKeeper: Process command hook (Constitution Save)
    _process_tavern_hook(
        project_path,
        "verify",
        all_valid,
        {"pyrite_valid": pyrite_status["valid"], "lock_exists": lock_exists},
    )

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

        integrity = gamification.integrity
        console.print(f"\n[bold green]✅ Project structure is valid {moon_phase}[/bold green]")
        console.print(f"[dim]💎 Integrity: {integrity:.0f}%[/dim]")
    else:
        integrity = gamification.integrity
        console.print("\n[bold yellow]⚠️  Project structure has issues[/bold yellow]")
        console.print(f"[dim]💎 Integrity: {integrity:.0f}%[/dim]")
        raise typer.Exit(1)


@app.command()
def sync(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """
    Sync project dependencies using uv sync.
    """
    # Resolve and validate project path
    try:
        project_path = resolve_project_path(path)
    except ValueError as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(1)

    console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Syncing dependencies\n")

    substrate = SubstrateManager()
    console.print("[dim]→[/dim] Running uv sync...")

    success = substrate.sync(project_path)

    if success:
        console.print("[green]✅[/green] Dependencies synced successfully")
        _process_tavern_hook(project_path, "sync", True)
    else:
        console.print("[bold red]❌ Failed to sync dependencies[/bold red]")
        _process_tavern_hook(project_path, "sync", False)
        raise typer.Exit(1)


@app.command()
def add(
    package: str = typer.Argument(..., help="Package name (e.g., 'pytest>=7.0.0')"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    dev: bool = typer.Option(False, "--dev", "-d", help="Add as development dependency"),
):
    """
    Add a dependency to the project using uv add.
    """
    # Validate package name
    is_valid, error_msg = validate_package_name(package)
    if not is_valid:
        console.print(f"[bold red]❌ Invalid package name: {error_msg}[/bold red]")
        raise typer.Exit(1)

    # Resolve and validate project path
    try:
        project_path = resolve_project_path(path)
    except ValueError as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(1)

    console.print(f"\n[bold cyan]🌊 Waft[/bold cyan] - Adding dependency: [bold]{package}[/bold]\n")

    substrate = SubstrateManager()

    if dev:
        console.print("[dim]→[/dim] Adding development dependency...")
        # For dev dependencies, we'd need to use uv add --dev
        # For now, just add normally
        console.print(
            "[yellow]⚠️[/yellow]  Dev flag not yet fully supported, adding as regular dependency"
        )

    console.print(f"[dim]→[/dim] Running uv add {package}...")

    success = substrate.add_dependency(package, project_path)

    if success:
        console.print(f"[green]✅[/green] Dependency '{package}' added successfully")
        _process_tavern_hook(project_path, "add", True, {"package": package})
    else:
        console.print(f"[bold red]❌ Failed to add dependency '{package}'[/bold red]")
        _process_tavern_hook(project_path, "add", False, {"package": package})
        raise typer.Exit(1)


@app.command()
def init(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """
    Initialize Waft structure in an existing project.

    This command:
    1. Creates the _pyrite directory structure
    2. Writes templates (Justfile, CI, agents.py)
    3. Does NOT run uv init (assumes project already exists)
    """
    # Resolve and validate project path
    try:
        project_path = resolve_project_path(path)
    except ValueError as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(1)

    console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Initializing Waft in existing project\n")

    # Check if already initialized
    if is_inside_waft_project(project_path)[0]:
        console.print(
            "[yellow]⚠️[/yellow]  This project already has Waft initialized (_pyrite directory exists)."
        )
        console.print(
            "[dim]→[/dim] Re-initializing will update templates but preserve existing _pyrite content."
        )
        # Continue - allow re-initialization

    # Check if pyproject.toml exists
    if not (project_path / "pyproject.toml").exists():
        console.print(
            "[bold red]❌ No pyproject.toml found. This command is for existing Python projects.[/bold red]"
        )
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

    # TavernKeeper: Ritual casting event
    _process_tavern_hook(project_path, "init", True)


@app.command()
def info(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """
    Show information about the Waft project.
    """
    project_path = resolve_project_path(path)

    console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Project Information\n")

    from rich.table import Table

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Property", style="dim")
    table.add_column("Value")

    # Project path
    table.add_row("Project Path", str(project_path.resolve()))

    # Check pyproject.toml
    substrate = SubstrateManager()
    pyproject_path = project_path / "pyproject.toml"

    if pyproject_path.exists():
        project_info = substrate.get_project_info(project_path)
        if project_info and "name" in project_info:
            project_name = project_info.get("name", "Unknown")
            project_version = project_info.get("version", "Unknown")
            table.add_row("Project Name", project_name)
            table.add_row("Version", project_version)
        else:
            # pyproject.toml exists but couldn't parse name/version
            table.add_row("Project Name", "[yellow]pyproject.toml exists (parse error)[/yellow]")
            table.add_row("Version", "[yellow]N/A[/yellow]")
    else:
        # No pyproject.toml
        table.add_row("Project Name", "[red]Not a Python project[/red]")
        table.add_row("Version", "[red]N/A[/red]")

    # Check _pyrite
    memory = MemoryManager(project_path)
    pyrite_status = memory.verify_structure()
    table.add_row(
        "_pyrite Structure",
        "[green]Valid[/green]" if pyrite_status["valid"] else "[red]Invalid[/red]",
    )

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

    table.add_row(
        "Templates", ", ".join(templates_status) if templates_status else "[yellow]None[/yellow]"
    )

    # Check Empirica
    empirica = EmpiricaManager(project_path)
    empirica_status = (
        "[green]Initialized[/green]"
        if empirica.is_initialized()
        else "[yellow]Not initialized[/yellow]"
    )
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

            table.add_row(
                "Epistemic State", f"{moon_phase} K:{know:.0%} U:{uncertainty:.0%} C:{coverage:.0%}"
            )
            table.add_row("", "[dim]Run 'waft assess' for detailed view[/dim]")

    console.print(table)

    # TavernKeeper: Perception check
    _process_tavern_hook(project_path, "info", True)


@app.command()
def serve(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
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

    # Use new FastAPI + SvelteKit visualizer
    try:
        import uvicorn

        from .api.main import create_app

        # Create FastAPI app
        static_dir = None
        if not dev:
            build_path = project_path / "visualizer" / "build"
            if build_path.exists():
                static_dir = build_path
                console.print("[dim]→[/dim] Serving SvelteKit build from visualizer/build")
            else:
                console.print(
                    "[yellow]⚠️[/yellow]  SvelteKit build not found. Run 'cd visualizer && npm run build' first"
                )
                console.print("[dim]→[/dim] API-only mode (use --dev for development)")

        app = create_app(project_path, static_dir=static_dir)

        console.print("\n[bold cyan]🌊 Waft Visualizer[/bold cyan]")
        if dev:
            console.print(
                "[dim]→[/dim] Development mode - Start SvelteKit dev server: cd visualizer && npm run dev"
            )
            console.print("[dim]→[/dim] SvelteKit will proxy API requests to this server")
        console.print(f"[dim]→[/dim] API server: http://{host}:{port}")
        if static_dir:
            console.print(f"[dim]→[/dim] Dashboard: http://{host}:{port}/")
        else:
            console.print(f"[dim]→[/dim] API docs: http://{host}:{port}/docs")
        console.print(f"[dim]→[/dim] API docs: http://{host}:{port}/docs")
        console.print(f"[dim]→[/dim] Project: {project_path.resolve()}")
        console.print("\nPress Ctrl+C to stop\n")

        uvicorn.run(app, host=host, port=port, log_level="info")

    except ImportError as e:
        console.print(f"[bold red]❌ Missing dependencies: {e}[/bold red]")
        console.print("[dim]→[/dim] Install with: uv sync[/dim]")
        raise typer.Exit(1)
    except Exception as e:
        if "Address already in use" in str(e) or "already in use" in str(e):
            console.print(f"[bold red]❌ Port {port} is already in use[/bold red]")
            console.print("[dim]Try a different port with --port[/dim]")
        else:
            console.print(f"[bold red]❌ Error starting server: {e}[/bold red]")
            import traceback

            if dev:
                console.print(f"[dim]{traceback.format_exc()}[/dim]")
        raise typer.Exit(1)


@app.command()
def evolve(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    agent: str | None = typer.Option(None, "--agent", "-a", help="Agent identifier to evolve"),
    generations: int = typer.Option(1, "--generations", "-g", help="Number of generations to run"),
):
    """
    Run the evolutionary cycle (Spawn -> Gym -> Select) for a target agent.

    This command orchestrates the complete evolutionary process:
    1. Spawn multiple variants with mutations
    2. Evaluate fitness in the Scint Gym
    3. Select the fittest variant
    4. Evolve the agent into the selected genome
    5. Record all events in the Flight Recorder

    Status: Coming Soon

    This is a placeholder for the evolutionary cycle implementation.
    """
    project_path = resolve_project_path(path)

    # Check if this is a Waft project
    is_valid, error = validate_waft_project(project_path)
    if not is_valid:
        console.print("[bold red]❌ Not a Waft project[/bold red]")
        console.print(f"[dim]{error}[/dim]")
        raise typer.Exit(1)

    console.print("\n[bold cyan]🧬 Evolutionary Code Laboratory[/bold cyan]")
    console.print("[yellow]⚠️[/yellow]  Evolutionary cycle coming soon")
    console.print(f"[dim]→[/dim] Project: {project_path.resolve()}")
    if agent:
        console.print(f"[dim]→[/dim] Agent: {agent}")
    console.print(f"[dim]→[/dim] Generations: {generations}")
    console.print("\n[dim]This command will implement the complete evolutionary cycle:[/dim]")
    console.print("[dim]  • Spawn variants with mutations[/dim]")
    console.print("[dim]  • Evaluate fitness in Scint Gym[/dim]")
    console.print("[dim]  • Select fittest variant[/dim]")
    console.print("[dim]  • Evolve agent into selected genome[/dim]")
    console.print("[dim]  • Record events in Flight Recorder[/dim]")


# Empirica command groups
session_app = typer.Typer(help="Session management commands")
finding_app = typer.Typer(help="Finding logging commands")
unknown_app = typer.Typer(help="Unknown logging commands")
goal_app = typer.Typer(help="Goal management commands")
github_app = typer.Typer(help="GitHub integration commands")
journal_app = typer.Typer(help="Development journal commands")
empirica_monitor_app = typer.Typer(help="Empirica monitoring and dashboard commands")

app.add_typer(session_app, name="session")
app.add_typer(finding_app, name="finding")
app.add_typer(unknown_app, name="unknown")
app.add_typer(goal_app, name="goal")
app.add_typer(github_app, name="github")
app.add_typer(journal_app, name="journal")
app.add_typer(project_app, name="project")
app.add_typer(empirica_monitor_app, name="empirica")
app.add_typer(chief_app, name="chief")


@empirica_monitor_app.command("monitor")
def empirica_monitor_cmd(
    dashboard_type: str = typer.Option(
        "snapshot",
        "--type",
        "-t",
        help="Dashboard type: snapshot, cascade, or tui",
    ),
    session_id: str | None = typer.Option(
        None, "--session-id", "-s", help="Session ID to monitor (snapshot only)"
    ),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Launch Empirica TUI dashboard for monitoring epistemic state.

    Dashboard types:
    - snapshot: Monitor epistemic snapshot memory quality (default)
    - cascade: Monitor PREFLIGHT → POSTFLIGHT workflow
    - tui: Full terminal UI dashboard with Textual
    """
    from .core.empirica_dashboard import (
        check_dashboard_dependencies,
        launch_dashboard,
    )

    project_path = resolve_project_path(path)

    console.print(f"\n[bold cyan]🌊 Waft[/bold cyan] - Empirica {dashboard_type.title()} Monitor\n")

    # Check if Empirica is initialized
    empirica = EmpiricaManager(project_path)
    if not empirica.is_initialized():
        console.print("[yellow]⚠️[/yellow]  Empirica not initialized. Run 'waft init' first.")
        raise typer.Exit(1)

    # Check dependencies
    deps = check_dashboard_dependencies(dashboard_type)
    if not deps["available"]:
        console.print(f"[bold red]❌ {deps['message']}[/bold red]")
        if deps.get("missing"):
            console.print(f"[dim]Missing: {', '.join(deps['missing'])}[/dim]")
        raise typer.Exit(1)

    console.print(f"[dim]Launching {dashboard_type} dashboard...[/dim]")
    console.print("[dim]Press 'q' to quit the dashboard[/dim]\n")

    # Launch the dashboard
    success = launch_dashboard(
        dashboard_type=dashboard_type,
        project_path=project_path,
        session_id=session_id,
    )

    if not success:
        console.print(f"\n[bold red]❌ Failed to launch {dashboard_type} dashboard[/bold red]")
        console.print("[dim]Make sure Empirica is installed: pip install empirica[/dim]")
        raise typer.Exit(1)

    console.print("\n[dim]Dashboard closed[/dim]")


@session_app.command("create")
def session_create(
    ai_id: str = typer.Option("waft", "--ai-id", help="AI agent identifier"),
    session_type: str = typer.Option("development", "--type", help="Session type"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Create a new Empirica session."""
    project_path = resolve_project_path(path)

    console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Creating Empirica session\n")

    empirica = EmpiricaManager(project_path)
    if not empirica.is_initialized():
        console.print("[yellow]⚠️[/yellow]  Empirica not initialized. Run 'waft init' first.")
        raise typer.Exit(1)

    session_id = empirica.create_session(ai_id=ai_id, session_type=session_type)
    if session_id:
        console.print(f"[green]✅[/green] Session created: [bold]{session_id}[/bold]")
        console.print(f"[dim]AI ID: {ai_id} | Type: {session_type}[/dim]")
    else:
        console.print("[bold red]❌ Failed to create session[/bold red]")
        raise typer.Exit(1)


@session_app.command("bootstrap")
def session_bootstrap(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Load project context and display epistemic dashboard."""
    project_path = resolve_project_path(path)

    console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Loading project context\n")

    empirica = EmpiricaManager(project_path)
    if not empirica.is_initialized():
        console.print("[yellow]⚠️[/yellow]  Empirica not initialized. Run 'waft init' first.")
        raise typer.Exit(1)

    context = empirica.project_bootstrap()
    if context:
        dashboard = create_epistemic_dashboard(context)
        console.print(dashboard)
    else:
        console.print("[yellow]⚠️[/yellow]  No project context available")


@session_app.command("status")
def session_status(
    session_id: str | None = typer.Option(None, "--session-id", help="Session ID"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Show current session state."""
    project_path = resolve_project_path(path)

    console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Session Status\n")

    empirica = EmpiricaManager(project_path)
    if not empirica.is_initialized():
        console.print("[yellow]⚠️[/yellow]  Empirica not initialized. Run 'waft init' first.")
        raise typer.Exit(1)

    if session_id:
        state = empirica.assess_state(session_id=session_id)
    else:
        state = empirica.assess_state()

    if state:
        from rich.table import Table

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Property", style="dim")
        table.add_column("Value")

        vectors = state.get("vectors", {})
        foundation = vectors.get("foundation", {})
        know = foundation.get("know", 0.0)
        uncertainty = vectors.get("uncertainty", 0.0)
        moon_phase = get_moon_phase(know * (1.0 - uncertainty))

        table.add_row("Moon Phase", moon_phase)
        table.add_row("Know", f"{know:.0%}")
        table.add_row("Uncertainty", f"{uncertainty:.0%}")

        console.print(table)
    else:
        console.print("[yellow]⚠️[/yellow]  No session state available")


@finding_app.command("log")
def finding_log(
    finding: str = typer.Argument(..., help="Finding description"),
    impact: float = typer.Option(0.5, "--impact", help="Impact score (0.0-1.0)"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Log a finding with impact score."""
    project_path = resolve_project_path(path)

    console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Logging Finding\n")

    empirica = EmpiricaManager(project_path)
    if not empirica.is_initialized():
        console.print("[yellow]⚠️[/yellow]  Empirica not initialized. Run 'waft init' first.")
        raise typer.Exit(1)

    success = empirica.log_finding(finding, impact=impact)
    if success:
        # Award insight for logging finding
        gamification = GamificationManager(project_path)
        insight_result = gamification.award_insight(10.0, reason="Logged finding")

        # Check for Knowledge Architect achievement (50 findings)
        gamification.get_stats()
        # Count findings from history
        findings_count = sum(
            1
            for h in gamification._data.get("history", [])
            if h.get("type") == "insight_award" and "finding" in h.get("reason", "").lower()
        )
        if findings_count >= 50:
            if gamification.unlock_achievement("knowledge_architect", "🧠 Knowledge Architect"):
                console.print(
                    "[bold green]🏆 Achievement Unlocked: 🧠 Knowledge Architect[/bold green]"
                )

        if insight_result["level_up"]:
            console.print(
                f"[bold cyan]🎉 Level Up! Level {insight_result['old_level']} → {insight_result['new_level']}[/bold cyan]"
            )

        console.print(f"[green]✅[/green] Finding logged: [bold]{finding}[/bold]")
        console.print(f"[dim]Impact: {impact:.0%} | 🧠 +10 Insight[/dim]")
        _process_tavern_hook(
            project_path, "finding_log", True, {"finding": finding, "impact": impact}
        )
    else:
        console.print("[bold red]❌ Failed to log finding[/bold red]")
        _process_tavern_hook(project_path, "finding_log", False)
        raise typer.Exit(1)


@unknown_app.command("log")
def unknown_log(
    unknown: str = typer.Argument(..., help="Unknown description"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Log a knowledge gap."""
    project_path = resolve_project_path(path)

    console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Logging Unknown\n")

    empirica = EmpiricaManager(project_path)
    if not empirica.is_initialized():
        console.print("[yellow]⚠️[/yellow]  Empirica not initialized. Run 'waft init' first.")
        raise typer.Exit(1)

    success = empirica.log_unknown(unknown)
    if success:
        console.print(f"[green]✅[/green] Unknown logged: [bold]{unknown}[/bold]")
    else:
        console.print("[bold red]❌ Failed to log unknown[/bold red]")
        raise typer.Exit(1)


@app.command()
def check(
    operation: str | None = typer.Option(None, "--operation", help="Operation JSON description"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Run safety gate and display result."""
    project_path = resolve_project_path(path)

    console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Safety Gate Check\n")

    empirica = EmpiricaManager(project_path)
    if not empirica.is_initialized():
        console.print("[yellow]⚠️[/yellow]  Empirica not initialized. Run 'waft init' first.")
        raise typer.Exit(1)

    operation_dict = None
    if operation:
        import json

        try:
            operation_dict = json.loads(operation)
        except json.JSONDecodeError:
            console.print("[red]❌ Invalid JSON in --operation[/red]")
            raise typer.Exit(1)

    gate_result = empirica.check_submit(operation=operation_dict)
    if gate_result:
        from .cli.epistemic_display import format_gate_result

        gate_text = format_gate_result(gate_result)
        console.print(f"Gate Result: {gate_text}")

        if gate_result == "HALT":
            console.print("[red]⚠️  Operation requires human approval[/red]")
            _process_tavern_hook(project_path, "check", False, {"gate_result": gate_result})
            raise typer.Exit(1)
        elif gate_result == "BRANCH":
            console.print("[yellow]⚠️  Need to investigate before proceeding[/yellow]")
            _process_tavern_hook(project_path, "check", True, {"gate_result": gate_result})
        elif gate_result == "REVISE":
            console.print("[yellow]⚠️  Approach needs revision[/yellow]")
            _process_tavern_hook(project_path, "check", True, {"gate_result": gate_result})
        else:
            _process_tavern_hook(project_path, "check", True, {"gate_result": gate_result})
    else:
        console.print("[yellow]⚠️  Gate check unavailable[/yellow]")
        _process_tavern_hook(project_path, "check", False)


@app.command(name="dashboard")
def dashboard_cmd(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Show the Red October Dashboard - TavernKeeper TUI."""
    project_path = resolve_project_path(path)

    try:
        from .ui.dashboard import RedOctoberDashboard

        tavern = TavernKeeper(project_path)
        dashboard = RedOctoberDashboard(tavern)
        dashboard.run()
    except KeyboardInterrupt:
        console.print("\n[dim]Dashboard closed[/dim]")
    except Exception as e:
        console.print(f"[bold red]❌ Error starting dashboard: {e}[/bold red]")
        raise typer.Exit(1)


@app.command(name="hud")
def hud_cmd(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    integrity: float = typer.Option(100.0, "--integrity", help="Integrity value (0.0-100.0)"),
):
    """Show the Epistemic HUD with split-screen layout (legacy)."""
    project_path = resolve_project_path(path)
    render_hud(project_path, integrity=integrity)


@app.command()
def assess(
    session_id: str | None = typer.Option(None, "--session-id", help="Session ID"),
    history: bool = typer.Option(False, "--history", help="Include historical data"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Show detailed epistemic assessment."""
    project_path = resolve_project_path(path)

    console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Epistemic Assessment\n")

    empirica = EmpiricaManager(project_path)
    if not empirica.is_initialized():
        console.print("[yellow]⚠️[/yellow]  Empirica not initialized. Run 'waft init' first.")
        raise typer.Exit(1)

    state = empirica.assess_state(session_id=session_id, include_history=history)
    if state:
        # Award insight for assessment
        gamification = GamificationManager(project_path)
        insight_result = gamification.award_insight(25.0, reason="Epistemic assessment")

        # Update integrity based on epistemic health
        vectors = state.get("vectors", {})
        uncertainty = vectors.get("uncertainty", 0.0)
        if uncertainty > 0.5:  # High uncertainty decreases integrity
            gamification.damage_integrity(5.0, reason="High epistemic uncertainty")
        elif uncertainty < 0.2:  # Low uncertainty restores integrity
            gamification.restore_integrity(2.0, reason="Low epistemic uncertainty")

        if insight_result["level_up"]:
            console.print(
                f"[bold cyan]🎉 Level Up! Level {insight_result['old_level']} → {insight_result['new_level']}[/bold cyan]"
            )

        from .cli.epistemic_display import format_epistemic_state

        panel = format_epistemic_state(state)
        console.print(panel)

        integrity = gamification.integrity
        insight = gamification.insight
        console.print(
            f"\n[dim]💎 Integrity: {integrity:.0f}% | 🧠 Insight: {insight:.0f} | 🧠 +25 Insight[/dim]"
        )

        # TavernKeeper: Wisdom save
        _process_tavern_hook(project_path, "assess", True, {"uncertainty": uncertainty})
    else:
        console.print("[yellow]⚠️  No assessment data available[/yellow]")


@goal_app.command("create")
def goal_create(
    objective: str = typer.Argument(..., help="Goal objective"),
    session_id: str | None = typer.Option(None, "--session-id", help="Session ID"),
    scope: str | None = typer.Option(
        None, "--scope", help="Scope JSON (breadth, duration, coordination)"
    ),
    criteria: str | None = typer.Option(
        None, "--criteria", help="Success criteria (comma-separated)"
    ),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Create a goal with epistemic scope."""
    project_path = resolve_project_path(path)

    console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Creating Goal\n")

    empirica = EmpiricaManager(project_path)
    if not empirica.is_initialized():
        console.print("[yellow]⚠️[/yellow]  Empirica not initialized. Run 'waft init' first.")
        raise typer.Exit(1)

    # Get or create session
    if not session_id:
        session_id = empirica.create_session(ai_id="waft", session_type="development")
        if not session_id:
            console.print("[bold red]❌ Failed to create session[/bold red]")
            raise typer.Exit(1)

    # Parse scope
    scope_dict = None
    if scope:
        import json

        try:
            scope_dict = json.loads(scope)
        except json.JSONDecodeError:
            console.print("[red]❌ Invalid JSON in --scope[/red]")
            raise typer.Exit(1)

    # Parse criteria
    criteria_list = None
    if criteria:
        criteria_list = [c.strip() for c in criteria.split(",")]

    success = empirica.create_goal(
        session_id=session_id,
        objective=objective,
        scope=scope_dict,
        success_criteria=criteria_list,
    )

    if success:
        console.print(f"[green]✅[/green] Goal created: [bold]{objective}[/bold]")
        console.print(f"[dim]Session: {session_id}[/dim]")

        # Create quest from goal
        try:
            tavern = TavernKeeper(project_path)
            quest = {
                "id": f"quest_{session_id}_{len(tavern._data.get('quests', []))}",
                "name": objective,
                "status": "active",
                "reward": "500 Insight",
                "progress": "0%",
                "created_at": datetime.now().isoformat(),
                "goal_id": session_id,
            }
            if tavern.db:
                tavern.db.table("quests").insert(quest)
            else:
                tavern._data.setdefault("quests", []).append(quest)
                tavern._save_json_data()
            console.print(f"[dim]✨ Quest created: {objective}[/dim]")
        except Exception:
            pass  # Silently fail if quest creation doesn't work

        _process_tavern_hook(project_path, "goal_create", True, {"objective": objective})
    else:
        console.print("[bold red]❌ Failed to create goal[/bold red]")
        _process_tavern_hook(project_path, "goal_create", False)
        raise typer.Exit(1)


@goal_app.command("list")
def goal_list(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """List active goals."""
    project_path = resolve_project_path(path)

    console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Active Goals\n")

    empirica = EmpiricaManager(project_path)
    if not empirica.is_initialized():
        console.print("[yellow]⚠️[/yellow]  Empirica not initialized. Run 'waft init' first.")
        raise typer.Exit(1)

    context = empirica.project_bootstrap()
    if context:
        goals = context.get("goals", [])
        if goals:
            from rich.table import Table

            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Objective", width=50)
            table.add_column("Status", width=15)

            for goal in goals:
                objective = goal.get("objective", "Unknown")
                status = goal.get("status", "active")
                table.add_row(objective, status)

            console.print(table)
        else:
            console.print("[dim]No active goals[/dim]")
    else:
        console.print("[yellow]⚠️  No project context available[/yellow]")


@app.command()
def stats(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    session: bool = typer.Option(
        False, "--session", "-s", help="Show session statistics instead of gamification stats"
    ),
    detailed: bool = typer.Option(False, "--detailed", "-d", help="Show detailed breakdown"),
):
    """
    Show statistics.

    By default shows gamification stats (Integrity, Insight, Level).
    Use --session to show session statistics (files created, lines written, etc.).
    """
    project_path = resolve_project_path(path)

    if session:
        # Session statistics
        from .core.session_stats import SessionStats

        console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Session Statistics\n")

        stats_tracker = SessionStats(project_path)
        stats_data = stats_tracker.calculate_session_stats()
        formatted = stats_tracker.format_stats(stats_data, detailed=detailed)

        console.print(Panel(formatted, title="📊 Session Activity", border_style="cyan"))

        if detailed:
            # Save to file
            stats_file = (
                project_path
                / "_pyrite"
                / "phase1"
                / f"session-stats-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}.json"
            )
            stats_file.parent.mkdir(parents=True, exist_ok=True)
            import json

            stats_file.write_text(json.dumps(stats_data, indent=2), encoding="utf-8")
            console.print(
                f"\n[dim]💾 Statistics saved: {stats_file.relative_to(project_path)}[/dim]"
            )
    else:
        # Gamification stats (original behavior)
        console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Stats\n")

        gamification = GamificationManager(project_path)
        stats = gamification.get_stats()

        from rich.table import Table

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Stat", style="dim", width=20)
        table.add_column("Value", width=20)

        table.add_row("💎 Integrity", f"{stats['integrity']:.0f}%")
        table.add_row("🧠 Insight", f"{stats['insight']:.0f}")
        table.add_row("⭐ Level", str(stats["level"]))
        table.add_row("🏆 Achievements", str(stats["achievements_count"]))

        console.print(table)

        # Show insight to next level
        insight_needed = gamification.get_insight_to_next_level()
        if insight_needed > 0:
            console.print(f"\n[dim]🧠 {insight_needed:.0f} Insight needed for next level[/dim]")


@app.command()
def checkout(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    quick: bool = typer.Option(
        False, "--quick", "-q", help="Quick checkout (skip detailed statistics)"
    ),
    silent: bool = typer.Option(False, "--silent", "-s", help="Silent mode (minimal output)"),
):
    """
    End chat session - run all relevant cleanup, documentation, and summary tasks.

    Orchestrates comprehensive end-of-session workflow including statistics,
    checkpoint creation, documentation updates, session summaries, and analytics tracking.
    """
    from .core.checkout import CheckoutManager

    project_path = resolve_project_path(path)

    checkout_manager = CheckoutManager(project_path)
    checkout_manager.run_checkout(quick=quick, silent=silent)


# Add analytics subcommand
app.add_typer(analytics_app, name="analytics")
app.add_typer(pyrite_app, name="pyrite", help="The Steward - The God of Work Efforts")


@app.command()
def decide(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    topic: str | None = typer.Option(
        None, "--topic", "-t", help="Specific decision topic (e.g., 'workflow')"
    ),
):
    """
    Run decision matrix analysis using standardized methodology.

    This command uses DecisionCLI for standardized decision matrix calculations.
    The decision matrix is built from the /consider command's output or can be
    provided directly. Uses the DecisionMatrixCalculator for mathematical rigor.

    Standardized workflow:
    1. Use /consider to identify options and criteria
    2. /decide uses DecisionCLI.run_decision_matrix() for calculations
    3. Results are displayed in consistent format with sensitivity analysis
    """
    project_path = resolve_project_path(path)

    # Check for topic-specific analyzers
    if topic == "workflow":
        from .core.workflow_decision import WorkflowDecisionAnalyzer

        analyzer = WorkflowDecisionAnalyzer(project_path)
        analyzer.analyze_workflow_options()
        return

    # Default: Show usage
    from .core.decision_cli import DecisionCLI

    DecisionCLI(project_path)

    console.print("[bold cyan]🎯 Decision Matrix Analysis[/bold cyan]\n")
    console.print("[dim]The /decide command uses DecisionCLI for standardized calculations.")
    console.print("DecisionCLI.run_decision_matrix() provides a reusable interface.")
    console.print("\n[bold]Standardized Components:[/bold]")
    console.print("  • DecisionCLI - Reusable CLI handler")
    console.print("  • DecisionMatrixCalculator - Mathematical calculations")
    console.print("  • Consistent output format with Rich tables")
    console.print("  • Built-in sensitivity analysis")
    console.print("\n[bold]Available Topics:[/bold]")
    console.print("  • workflow - Analyze workflow implementation options")
    console.print("\n[dim]See .cursor/commands/decide.md for full documentation.[/dim]")
    console.print(
        "[dim]Use /consider first to identify options, then /decide for quantitative analysis.[/dim]"
    )
    console.print("[dim]Example: waft decide --topic workflow[/dim]")


@app.command()
def level(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Show level details and progress to next level."""
    project_path = resolve_project_path(path)

    console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Level Details\n")

    gamification = GamificationManager(project_path)
    current_level = gamification.level
    current_insight = gamification.insight
    next_level = current_level + 1

    # Calculate insight for current and next level
    insight_for_current = (current_level - 1) ** 2 * 100 if current_level > 1 else 0
    insight_for_next = (next_level - 1) ** 2 * 100
    insight_needed = insight_for_next - current_insight
    progress = (
        (current_insight - insight_for_current) / (insight_for_next - insight_for_current)
        if insight_for_next > insight_for_current
        else 1.0
    )

    from rich.progress import BarColumn, Progress, TextColumn

    progress_bar = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )

    task = progress_bar.add_task(f"Level {current_level} → {next_level}", total=100)
    progress_bar.update(task, completed=int(progress * 100))

    console.print(f"[bold]Current Level:[/bold] {current_level}")
    console.print(f"[bold]Current Insight:[/bold] {current_insight:.0f}")
    console.print(f"[bold]Insight for Level {next_level}:[/bold] {insight_for_next:.0f}")
    console.print(f"[bold]Insight Needed:[/bold] {insight_needed:.0f}")
    console.print()
    console.print(progress_bar)


@app.command()
def character(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Display full D&D 5e character sheet."""
    project_path = resolve_project_path(path)

    console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Character Sheet\n")

    try:
        tavern = TavernKeeper(project_path)
        sheet = tavern.get_character_sheet()
        char = sheet["character"]
        ability_scores = sheet["ability_scores"]
        ability_modifiers = sheet["ability_modifiers"]
        hp = sheet["hp"]
        status_effects = sheet["status_effects"]

        from rich.panel import Panel
        from rich.table import Table

        # Character Info with colors
        info_table = Table(show_header=False, box=None)
        info_table.add_column(style="bold cyan")
        info_table.add_column(style="")

        # Color code values
        level = char.get("level", 1)
        level_color = "gold1" if level >= 5 else "cyan" if level >= 3 else "green"

        integrity = char.get("integrity", 100.0)
        integrity_color = "green" if integrity >= 80 else "yellow" if integrity >= 50 else "red"

        insight = char.get("insight", 0.0)
        insight_color = "magenta" if insight >= 500 else "cyan" if insight >= 100 else "dim"

        credits = char.get("credits", 0)
        credits_color = "gold1" if credits >= 100 else "cyan" if credits >= 50 else "dim"

        info_table.add_row("Name:", f"[bold]{char.get('name', 'Unknown')}[/]")
        info_table.add_row("Level:", f"[bold {level_color}]{level}[/]")
        info_table.add_row("Proficiency Bonus:", f"[cyan]+{sheet['proficiency_bonus']}[/]")
        info_table.add_row("Hit Dice:", f"[dim]{char.get('hit_dice', 'd8')}[/]")
        info_table.add_row("HP:", f"[green]{hp['current']}[/]/[dim]{hp['max']}[/]")
        info_table.add_row("Integrity:", f"[{integrity_color}]{integrity:.1f}%[/]")
        info_table.add_row("Insight:", f"[{insight_color}]{insight:.1f}[/]")
        info_table.add_row("Credits:", f"[{credits_color}]{credits}[/]")

        console.print(Panel(info_table, title="[bold]Character Info[/bold]", border_style="cyan"))

        # Ability Scores
        ability_table = Table(show_header=True, header_style="bold cyan")
        ability_table.add_column("Ability", width=15)
        ability_table.add_column("Score", width=8, justify="center")
        ability_table.add_column("Modifier", width=10, justify="center")

        # Color mapping for abilities
        ability_colors = {
            "strength": "red",
            "dexterity": "cyan",
            "constitution": "green",
            "intelligence": "blue",
            "wisdom": "magenta",
            "charisma": "bright_magenta",
        }

        for ability in [
            "strength",
            "dexterity",
            "constitution",
            "intelligence",
            "wisdom",
            "charisma",
        ]:
            score = ability_scores.get(ability, 8)
            modifier = ability_modifiers.get(ability, -1)
            modifier_str = f"+{modifier}" if modifier >= 0 else str(modifier)

            # Color code score
            if score >= 16:
                score_color = "gold1"
            elif score >= 13:
                score_color = "green"
            elif score >= 10:
                score_color = "cyan"
            else:
                score_color = "dim"

            ability_color = ability_colors.get(ability, "white")
            ability_table.add_row(
                f"[{ability_color}]{ability.title()}[/]",
                f"[{score_color}]{score}[/]",
                f"[dim]{modifier_str}[/]",
            )

        console.print("\n")
        console.print(
            Panel(ability_table, title="[bold]Ability Scores[/bold]", border_style="cyan")
        )

        # Status Effects
        if status_effects:
            effects_table = Table(show_header=True, header_style="bold cyan")
            effects_table.add_column("Effect", width=20)
            effects_table.add_column("Type", width=10)
            effects_table.add_column("Description", width=40)

            for effect in status_effects:
                effect_type = effect.get("type", "unknown")
                if effect_type == "buff":
                    effect_color = "gold1"
                    symbol = "▲"
                else:
                    effect_color = "red"
                    symbol = "▼"

                effects_table.add_row(
                    f"[{effect_color}]{symbol}[/] {effect.get('name', 'Unknown')}",
                    f"[{effect_color}]{effect_type}[/]",
                    f"[dim]{effect.get('description', '')}[/]",
                )

            console.print("\n")
            console.print(
                Panel(effects_table, title="[bold]Status Effects[/bold]", border_style="cyan")
            )

    except Exception as e:
        console.print(f"[bold red]❌ Error loading character sheet: {e}[/bold red]")
        console.print("[dim]Make sure you've run 'waft new' or 'waft init' first[/dim]")


@app.command()
def achievements(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """List all achievements (locked/unlocked)."""
    project_path = resolve_project_path(path)

    console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Achievements\n")

    gamification = GamificationManager(project_path)
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

    from rich.table import Table

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Achievement", width=30)
    table.add_column("Status", width=15)

    for achievement_id, unlocked in achievement_status.items():
        name = achievement_names.get(achievement_id, achievement_id)
        status = "[green]✓ Unlocked[/green]" if unlocked else "[dim]🔒 Locked[/dim]"
        table.add_row(name, status)

    console.print(table)


@app.command(name="chronicle")
def chronicle(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    limit: int = typer.Option(20, "--limit", "-n", help="Number of entries to show"),
):
    """View the Adventure Chronicle - Your journey's story."""
    project_path = resolve_project_path(path)

    try:
        tavern = TavernKeeper(project_path)

        # Get journal entries
        if tavern.db:
            journal_entries = tavern.db.table("adventure_journal").all()
        else:
            journal_entries = tavern._data.get("adventure_journal", [])

        # Get last N entries
        recent_entries = (
            journal_entries[-limit:] if len(journal_entries) > limit else journal_entries
        )
        recent_entries.reverse()  # Show newest first

        console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Adventure Journal\n")

        if not recent_entries:
            console.print(
                "[dim]No entries in the chronicle yet. Run some commands to generate adventures![/dim]"
            )
            return

        from rich.table import Table

        journal_table = Table(show_header=True, header_style="bold cyan")
        journal_table.add_column("Time", width=10, style="dim")
        journal_table.add_column("Event", width=12)
        journal_table.add_column("Roll", width=15, justify="center")
        journal_table.add_column("Narrative", ratio=2)
        journal_table.add_column("Reward", width=20, justify="right")

        for entry in recent_entries:
            timestamp = entry.get("timestamp", "")
            event = entry.get("event", "unknown")
            narrative = entry.get("narrative", "")
            dice_result = entry.get("dice_roll", "")
            result = entry.get("result", 0)
            classification = entry.get("classification", "")
            rewards = entry.get("rewards", {})

            # Format timestamp
            try:
                time_part = (
                    timestamp.split("T")[1].split(".")[0] if "T" in timestamp else timestamp[:8]
                )
            except (IndexError, AttributeError) as e:
                logger.debug(f"Could not parse timestamp '{timestamp}': {e}")
                time_part = timestamp[:8] if len(timestamp) >= 8 else timestamp

            # Format roll display
            roll_display = f"{dice_result} = {result}"
            if classification:
                if classification == "critical_success":
                    roll_display = f"[bold gold1]{roll_display} ⭐[/]"
                elif classification == "critical_failure":
                    roll_display = f"[bold red]{roll_display} 💥[/]"
                elif classification == "superior":
                    roll_display = f"[gold1]{roll_display} ▲[/]"

            # Format reward
            insight = rewards.get("insight", 0)
            credits = rewards.get("credits", 0)
            reward_str = ""
            if insight > 0:
                reward_str += f"+{insight} Insight "
            if credits > 0:
                reward_str += f"+{credits} Credits"
            if not reward_str:
                reward_str = "[dim]-[/]"

            journal_table.add_row(
                time_part,
                event,
                roll_display,
                narrative,
                reward_str,
            )

        console.print(journal_table)
        console.print(
            f"\n[dim]Showing {len(recent_entries)} of {len(journal_entries)} entries[/dim]"
        )

    except Exception as e:
        console.print(f"[bold red]❌ Error loading journal: {e}[/bold red]")
        raise typer.Exit(1)


@app.command()
def roll(
    ability: str = typer.Argument(..., help="Ability to use (strength, dexterity, etc.)"),
    dc: int = typer.Option(10, "--dc", help="Difficulty Class (target number)"),
    advantage: bool = typer.Option(False, "--advantage", "-a", help="Roll with advantage"),
    disadvantage: bool = typer.Option(False, "--disadvantage", "-d", help="Roll with disadvantage"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Roll a d20 check manually - Test your luck!"""
    project_path = resolve_project_path(path)

    try:
        tavern = TavernKeeper(project_path)

        console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Dice Roll\n")

        result = tavern.roll_check(ability, dc, advantage=advantage, disadvantage=disadvantage)

        roll = result["roll"]
        modifier = result["modifier"]
        total = result["total"]
        success = result["success"]
        classification = result["classification"]

        # Display roll
        console.print(f"[bold]Ability:[/bold] {ability.title()}")
        console.print(f"[bold]DC:[/bold] {dc}")
        if advantage:
            console.print("[dim]Rolling with advantage[/dim]")
        elif disadvantage:
            console.print("[dim]Rolling with disadvantage[/dim]")

        console.print()

        # Show dice result with color
        if classification == "critical_success":
            console.print(f"[bold gold1]🎲 Roll: {roll} + {modifier} = {total}[/bold gold1]")
            console.print("[bold gold1]⭐ CRITICAL SUCCESS![/bold gold1]")
        elif classification == "critical_failure":
            console.print(f"[bold red]🎲 Roll: {roll} + {modifier} = {total}[/bold red]")
            console.print("[bold red]💥 CRITICAL FAILURE![/bold red]")
        elif classification == "superior":
            console.print(f"[gold1]🎲 Roll: {roll} + {modifier} = {total}[/gold1]")
            console.print("[gold1]▲ Superior Result[/gold1]")
        elif classification == "optimal":
            console.print(f"[green]🎲 Roll: {roll} + {modifier} = {total}[/green]")
            console.print("[green]✓ Optimal Result[/green]")
        else:
            console.print(f"🎲 Roll: {roll} + {modifier} = {total}")

        console.print()

        if success:
            console.print(f"[bold green]✅ Success! (Total {total} >= DC {dc})[/bold green]")
        else:
            console.print(f"[bold red]❌ Failure (Total {total} < DC {dc})[/bold red]")

    except Exception as e:
        console.print(f"[bold red]❌ Error rolling dice: {e}[/bold red]")
        raise typer.Exit(1)


@app.command()
def quests(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """View active and completed quests."""
    project_path = resolve_project_path(path)

    try:
        tavern = TavernKeeper(project_path)

        # Get quests
        if tavern.db:
            quests = tavern.db.table("quests").all()
        else:
            quests = tavern._data.get("quests", [])

        console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Quests\n")

        if not quests:
            console.print(
                "[dim]No quests available. Create goals with 'waft goal create' to generate quests![/dim]"
            )
            return

        from rich.table import Table

        quest_table = Table(show_header=True, header_style="bold cyan")
        quest_table.add_column("Quest", width=30)
        quest_table.add_column("Status", width=12)
        quest_table.add_column("Reward", width=15)
        quest_table.add_column("Progress", width=20)

        for quest in quests:
            name = quest.get("name", "Unknown Quest")
            status = quest.get("status", "active")
            reward = quest.get("reward", "N/A")
            progress = quest.get("progress", "0%")

            status_color = (
                "green" if status == "completed" else "yellow" if status == "active" else "dim"
            )
            quest_table.add_row(
                name,
                f"[{status_color}]{status.title()}[/{status_color}]",
                str(reward),
                progress,
            )

        console.print(quest_table)

    except Exception as e:
        console.print(f"[bold red]❌ Error loading quests: {e}[/bold red]")
        raise typer.Exit(1)


@app.command()
def note(
    text: str = typer.Argument(..., help="Note to add to the chronicle"),
    category: str = typer.Option(
        "general", "--category", "-c", help="Category (bug, feature, refactor, insight, etc.)"
    ),
    source: str = typer.Option("human", "--source", "-s", help="Source (human, ai, system)"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Add a narrative note to the chronicle - Share your thoughts!"""
    project_path = resolve_project_path(path)

    try:
        tavern = TavernKeeper(project_path)
        narrator = Narrator(tavern)

        narrator.note(text, category=category, tags=[source])

        console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Note Added\n")
        console.print(f"[green]✅[/green] Note logged: [bold]{text}[/bold]")
        console.print(f"[dim]Category: {category} | Source: {source}[/dim]")

    except Exception as e:
        console.print(f"[bold red]❌ Error adding note: {e}[/bold red]")
        raise typer.Exit(1)


@app.command()
def observe(
    observation: str = typer.Argument(..., help="Observation to log"),
    mood: str = typer.Option(
        "neutral", "--mood", "-m", help="Mood (neutral, surprised, delighted, concerned, amazed)"
    ),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Log an observation - "woah that's kinda sick" or "weird that's not right"."""
    project_path = resolve_project_path(path)

    try:
        tavern = TavernKeeper(project_path)
        narrator = Narrator(tavern)

        narrator.observe(observation, mood=mood, source="human")

        console.print("\n[bold cyan]🌊 Waft[/bold cyan] - Observation Logged\n")
        console.print(f"[green]✅[/green] Observation: [bold]{observation}[/bold]")
        console.print(f"[dim]Mood: {mood}[/dim]")

    except Exception as e:
        console.print(f"[bold red]❌ Error logging observation: {e}[/bold red]")
        raise typer.Exit(1)


@app.command()
def phase1(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed progress"),
):
    """Run Phase 1: Comprehensive data gathering and visualization."""
    project_path = resolve_project_path(path)

    from .core.visualizer import Visualizer

    visualizer = Visualizer(project_path)
    visualizer.phase1(verbose=verbose)


@app.command()
def analyze(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed progress"),
):
    """Run Analyze: Analysis, insights, and action planning."""
    project_path = resolve_project_path(path)

    from .core.visualizer import Visualizer

    visualizer = Visualizer(project_path)
    visualizer.analyze(verbose=verbose)


@app.command()
def resume(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    session: str | None = typer.Option(
        None, "--session", "-s", help="Specific session file to load"
    ),
    compare: bool = typer.Option(
        True, "--compare/--no-compare", help="Compare current state with last session"
    ),
    full: bool = typer.Option(False, "--full", "-f", help="Load full context (not just summary)"),
):
    """
    Pick up where you left off - restore context and continue work.

    Loads the most recent session summary, compares current state with what was left,
    identifies what was in progress, and provides clear next steps.
    """
    project_path = resolve_project_path(path)

    from .core.resume import ResumeManager

    resume_manager = ResumeManager(project_path)
    resume_manager.run_resume(session_file=session, compare=compare, full_context=full)


@app.command(name="continue")
def continue_work(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    deep: bool = typer.Option(False, "--deep", "-d", help="Perform deep reflection"),
    focus: str | None = typer.Option(
        None, "--focus", "-f", help="Focus area: approach, patterns, quality"
    ),
    save: bool = typer.Option(False, "--save", "-s", help="Save reflection to file"),
):
    """
    Keep doing what you're doing, but take this opportunity to really reflect on what you're doing.

    Pauses to deeply reflect on current work, approach, and progress, then continues
    with improved awareness and potentially adjusted direction.
    """
    project_path = resolve_project_path(path)

    from .core.continue_work import ContinueManager

    continue_manager = ContinueManager(project_path)
    continue_manager.run_continue(deep=deep, focus=focus, save=save)


@app.command()
def reflect(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    prompt: str | None = typer.Option(None, "--prompt", help="Custom reflection prompt"),
    topic: str | None = typer.Option(None, "--topic", "-t", help="Topic to focus reflection on"),
    save: bool = typer.Option(True, "--save/--no-save", help="Save entry to journal"),
):
    """
    Induce the AI to write in its journal - reflect on current work, thoughts, and experiences.

    The AI definitely needs a journal if it doesn't have one. This command ensures it exists
    and prompts the AI to write reflective entries about its work, thoughts, and learnings.
    """
    project_path = resolve_project_path(path)

    from .core.reflect import ReflectManager

    reflect_manager = ReflectManager(project_path)
    reflect_manager.run_reflect(prompt=prompt, topic=topic, save_entry=save)


@app.command(name="journal-search")
def journal_search(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    query: str | None = typer.Option(None, "--query", "-q", help="Text search query"),
    topic: str | None = typer.Option(None, "--topic", "-t", help="Filter by topic"),
    date_from: str | None = typer.Option(None, "--from", help="Start date (YYYY-MM-DD)"),
    date_to: str | None = typer.Option(None, "--to", help="End date (YYYY-MM-DD)"),
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum results"),
):
    """
    Search journal entries by query, topic, or date range.
    """
    project_path = resolve_project_path(path)

    from rich.table import Table

    from .core.reflect import ReflectManager

    reflect_manager = ReflectManager(project_path)
    results = reflect_manager.search_entries(
        query=query, topic=topic, date_from=date_from, date_to=date_to, limit=limit
    )

    if not results:
        reflect_manager.console.print("[yellow]No entries found matching your criteria.[/yellow]\n")
        return

    table = Table(title=f"📔 Journal Search Results ({len(results)} found)", show_header=True)
    table.add_column("Date", style="dim")
    table.add_column("Time", style="dim")
    table.add_column("Preview", style="cyan")

    for entry in results:
        preview = entry.get("content", "")[:100].replace("\n", " ")
        table.add_row(
            entry.get("date", "Unknown"),
            entry.get("time", "Unknown"),
            preview + "..." if len(preview) >= 100 else preview,
        )

    reflect_manager.console.print("\n")
    reflect_manager.console.print(table)
    reflect_manager.console.print("\n")


@app.command(name="journal-stats")
def journal_stats(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    cleanup: bool = typer.Option(False, "--cleanup", help="Clean up old archives"),
):
    """
    Display journal statistics and analytics.
    """
    project_path = resolve_project_path(path)

    from .core.reflect import ReflectManager

    reflect_manager = ReflectManager(project_path)

    if cleanup:
        reflect_manager.cleanup_old_archives()

    reflect_manager.display_statistics()


@app.command()
def help_cmd(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    category: str | None = typer.Option(None, "--category", "-c", help="Filter by category"),
    search: str | None = typer.Option(None, "--search", "-s", help="Search commands by keyword"),
    command: str | None = typer.Option(None, "--command", help="Show details for specific command"),
    count: bool = typer.Option(False, "--count", help="Just show command count"),
):
    """
    Discover and understand available Cursor commands.

    Lists all available commands, organized by category, with brief descriptions
    and usage guidance. Helps you discover commands and understand when to use each one.
    """
    project_path = resolve_project_path(path)

    from .core.help import HelpManager

    help_manager = HelpManager(project_path)
    help_manager.run_help(category=category, search=search, command=command, count=count)


@app.command(name="encapsulated-environments-pdf")
def encapsulated_environments_pdf(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    output: str | None = typer.Option(
        None, "--output", "-o", help="Output PDF path (default: auto-generated)"
    ),
    style: str = typer.Option(
        "clinical_standard",
        "--style",
        "-s",
        help="PDF style (clinical_standard/premium/professional)",
    ),
    open_pdf: bool = typer.Option(True, "--open/--no-open", help="Open PDF after generation"),
):
    """
    Generate research PDF explaining Encapsulated Environments system.

    Creates a multi-section research PDF with simple prose and scientific design elements
    explaining the framework for Being storytelling and information exchange.
    """
    project_path = resolve_project_path(path)
    console.print(
        "\n[bold cyan]📄 Waft[/bold cyan] - Generating Encapsulated Environments Research PDF\n"
    )

    from pathlib import Path

    # Read the research document
    research_file = project_path / "_pyrite" / "research" / "encapsulated-environments-research.md"

    if not research_file.exists():
        console.print(f"[red]❌ Research file not found: {research_file}[/red]")
        raise typer.Exit(1)

    # Use the working example script with uv run to ensure dependencies
    import shutil
    import subprocess

    example_script = project_path / "examples" / "generate_encapsulated_environments_pdf.py"

    if not example_script.exists():
        console.print(f"[red]❌ Example script not found: {example_script}[/red]")
        raise typer.Exit(1)

    # Generate output path
    if output:
        output_path = Path(output)
    else:
        output_path = project_path / "encapsulated_environments_research.pdf"

    console.print("[yellow]→[/yellow] Generating PDF...")

    # Check if uv is available, use it if so
    uv_available = shutil.which("uv") is not None

    try:
        if uv_available:
            # Use uv run to ensure dependencies are available
            console.print("[dim]Using uv run to ensure dependencies...[/dim]")
            result = subprocess.run(
                ["uv", "run", "python3", str(example_script)],
                cwd=project_path,
                capture_output=True,
                text=True,
            )
        else:
            # Fallback to python3 directly
            console.print("[dim]Running with python3 (uv not found)...[/dim]")
            result = subprocess.run(
                ["python3", str(example_script)], cwd=project_path, capture_output=True, text=True
            )

        if result.returncode == 0:
            # Check if PDF was created (script creates it at default location)
            default_pdf = project_path / "encapsulated_environments_research.pdf"
            if default_pdf.exists():
                # Move to requested location if different
                if output_path != default_pdf:
                    default_pdf.rename(output_path)

                console.print(f"[green]✅ PDF generated:[/green] {output_path}")
                console.print(f"[dim]Style: {style} | Pages: Auto[/dim]")

                if open_pdf:
                    import subprocess as sp

                    sp.run(["open", str(output_path)], check=False)

                return output_path
            else:
                console.print("[yellow]⚠️[/yellow]  Script completed but PDF not found")
                if result.stdout:
                    console.print(f"[dim]Output: {result.stdout}[/dim]")
                raise typer.Exit(1)
        else:
            error_msg = result.stderr or result.stdout or "Unknown error"
            console.print("[red]❌ Error generating PDF[/red]")
            if "jinja2" in error_msg or "ModuleNotFoundError" in error_msg:
                console.print("[yellow]💡 Missing dependencies. Try:[/yellow]")
                console.print("   uv pip install jinja2 weasyprint markdown")
                console.print(f"   Or: uv run python3 {example_script}")
            else:
                console.print(f"[dim]{error_msg}[/dim]")
            raise typer.Exit(1)

    except FileNotFoundError:
        console.print("[red]❌ Python not found. Please ensure Python 3 is installed.[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        logger.exception("Error generating encapsulated environments PDF")
        raise typer.Exit(1)


goal_app = typer.Typer(help="Goal management commands")
app.add_typer(goal_app, name="goal")


@goal_app.command()
def create(
    name: str = typer.Argument(..., help="Goal name (slug)"),
    objective: str = typer.Argument(..., help="Goal objective/description"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Create a new goal with objective."""
    project_path = resolve_project_path(path)

    from .core.goal import GoalManager

    goal_manager = GoalManager(project_path)
    goal_manager.create_goal(name, objective)


@goal_app.command("list")
def goal_list(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    status: str | None = typer.Option(
        None, "--status", "-s", help="Filter by status (active, completed, paused)"
    ),
):
    """List all goals."""
    project_path = resolve_project_path(path)

    from rich.table import Table

    from .core.goal import GoalManager

    goal_manager = GoalManager(project_path)
    goals = goal_manager.list_goals(status=status)

    if not goals:
        console.print("[dim]No goals found.[/dim]")
        return

    table = Table(show_header=True)
    table.add_column("Name", style="bold")
    table.add_column("Status", width=12)
    table.add_column("Objective", ratio=2)
    table.add_column("Progress", width=15)

    for goal in goals:
        steps = goal.get("steps", [])
        completed = sum(1 for s in steps if s.get("completed", False))
        total = len(steps)
        progress = f"{completed}/{total}" if total > 0 else "0/0"

        table.add_row(
            goal.get("name", ""),
            goal.get("status", ""),
            goal.get("objective", "")[:60] + "..."
            if len(goal.get("objective", "")) > 60
            else goal.get("objective", ""),
            progress,
        )

    console.print("\n[bold cyan]🎯 Goals[/bold cyan]\n")
    console.print(table)
    console.print()


@goal_app.command()
def show(
    name: str = typer.Argument(..., help="Goal name"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Show goal details."""
    project_path = resolve_project_path(path)

    from .core.goal import GoalManager

    goal_manager = GoalManager(project_path)
    goal_manager.show_goal(name)


@app.command()
def next_cmd(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    goal: str | None = typer.Option(None, "--goal", "-g", help="Specific goal name"),
    count: int = typer.Option(1, "--count", "-c", help="Number of next steps to show"),
):
    """
    Identify next step based on goals, context, and priorities.

    Analyzes current goals, work in progress, and context to identify
    the most important next action.
    """
    project_path = resolve_project_path(path)

    from .core.goal import GoalManager

    goal_manager = GoalManager(project_path)
    next_steps = goal_manager.get_next_step(goal_name=goal, count=count)

    if not next_steps:
        console.print(
            "[dim]No next steps found. Create a goal first with: waft goal create <name> <objective>[/dim]"
        )
        return

    console.print("\n[bold cyan]🎯 Next Steps[/bold cyan]\n")

    for i, step in enumerate(next_steps, 1):
        console.print(f"[bold]{i}. {step.get('step', '')}[/bold]")
        console.print(f"   [dim]From Goal:[/dim] {step.get('goal', '')}")
        console.print(f"   [dim]Priority:[/dim] {step.get('priority', 0)}")
        if step.get("objective"):
            console.print(f"   [dim]Objective:[/dim] {step.get('objective', '')[:80]}...")
        console.print()


@app.command()
def recap(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    output: str | None = typer.Option(None, "--output", "-o", help="Custom output path"),
):
    """
    Create conversation recap and session summary.

    Creates comprehensive recap of current conversation/session, extracting
    key points, decisions, accomplishments, and questions.
    """
    project_path = resolve_project_path(path)

    from .core.recap import RecapManager

    recap_manager = RecapManager(project_path)
    recap_manager.run_recap(output_path=output)


@app.command(name="recap-and-review")
def recap_and_review(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    output: str | None = typer.Option(None, "--output", "-o", help="Custom output path"),
):
    """
    Capture mindspace and generate review PDF.

    Creates comprehensive documentation of the current mindspace - thoughts,
    context, state, decisions, and observations - then generates a PDF document
    and opens it on your desktop.
    """
    project_path = resolve_project_path(path)

    from .core.recap_and_review import RecapAndReviewManager

    manager = RecapAndReviewManager(project_path)
    manager.run_recap_and_review(output_path=output)


@app.command(name="science-bitch")
def science_bitch(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    hypothesis: str | None = typer.Option(None, "--hypothesis", "-h", help="Hypothesis statement"),
    run: bool = typer.Option(False, "--run", "-r", help="Run experiment"),
    report: bool = typer.Option(False, "--report", help="Generate report"),
    field_guide: bool = typer.Option(False, "--field-guide", help="Generate field guide PDF"),
):
    """
    Science-Bitch: Full scientific method workflow.

    Runs the complete scientific method:
    1. Form hypothesis
    2. Design experiment
    3. Capture initial state (A)
    4. Run experiment
    5. Collect data (C)
    6. Capture final state (B)
    7. Analyze results
    8. Generate reports
    """
    project_path = resolve_project_path(path)

    from .core.science_bitch import ScienceBitchManager

    manager = ScienceBitchManager(project_path)

    if field_guide:
        # Generate field guide PDF
        console.print("\n[bold cyan]📖 Generating Field Guide PDF...[/bold cyan]\n")
        guide_path = manager.generate_field_guide()
        if guide_path:
            console.print(f"[green]✅ Field guide generated:[/green] {guide_path}")
        else:
            console.print("[red]❌ Failed to generate field guide[/red]")
            raise typer.Exit(1)
        return

    if report:
        # Generate project status report
        console.print("\n[bold cyan]📊 Generating Project Status Report...[/bold cyan]\n")
        report_path = manager.generate_project_status_report()
        if report_path:
            console.print(f"[green]✅ Report generated:[/green] {report_path}")
        else:
            console.print("[red]❌ Failed to generate report[/red]")
            raise typer.Exit(1)
        return

    # Run interactive workflow
    result = manager.run_interactive()

    if result.get("success"):
        console.print("\n[green]✅ Scientific method workflow complete![/green]")
        if result.get("report_path"):
            console.print(f"[dim]Report: {result['report_path']}[/dim]")
    else:
        console.print(f"\n[red]❌ Workflow failed: {result.get('error', 'Unknown error')}[/red]")
        raise typer.Exit(1)


@app.command(name="work-efforts")
def work_efforts(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    output: str | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Output HTML file path (default: _work_efforts/work_dashboard.html)",
    ),
    limit: int | None = typer.Option(
        None, "--limit", "-l", help="Maximum work efforts to process (default: 100)"
    ),
    no_open: bool = typer.Option(False, "--no-open", help="Don't open browser automatically"),
):
    """
    Generate interactive HTML dashboard with polymorphic action buttons for work efforts.

    Creates a beautiful neumorphic-styled dashboard that intelligently analyzes
    work efforts and projects, then generates context-aware action buttons.
    Click buttons to copy commands to clipboard for execution in Cursor.
    """
    project_path = resolve_project_path(path)

    import subprocess
    import sys

    script_path = project_path / "scripts" / "work_dashboard.py"

    if not script_path.exists():
        console.print(f"[red]❌ Script not found: {script_path}[/red]")
        raise typer.Exit(1)

    # Build command
    cmd = [sys.executable, str(script_path)]
    if output:
        cmd.extend(["--output", output])
    if limit:
        cmd.extend(["--limit", str(limit)])
    if no_open:
        cmd.append("--no-open")

    # Run script
    console.print("\n[bold cyan]📊 Generating Work Dashboard...[/bold cyan]\n")
    result = subprocess.run(cmd, cwd=str(project_path))

    if result.returncode != 0:
        raise typer.Exit(result.returncode)


@app.command(name="auto-work")
def auto_work(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be done without executing"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """
    Think about work efforts, pick the best one, and execute it autonomously.

    Analyzes all work efforts, calculates priorities, selects the best one,
    determines the best action, and executes it. The AI will then execute
    the selected work effort action directly.
    """
    project_path = resolve_project_path(path)

    import json
    import re
    import subprocess
    import sys

    script_path = project_path / "scripts" / "auto_work.py"

    if not script_path.exists():
        console.print(f"[red]❌ Script not found: {script_path}[/red]")
        raise typer.Exit(1)

    # Build command
    cmd = [sys.executable, str(script_path), "--path", str(project_path)]
    if dry_run:
        cmd.append("--dry-run")
    if verbose:
        cmd.append("--verbose")

    # Run script and capture output
    result = subprocess.run(cmd, cwd=str(project_path), capture_output=True, text=True)

    # Print output
    console.print(result.stdout)
    if result.stderr:
        console.print(f"[yellow]{result.stderr}[/yellow]")

    # If not dry-run, try to extract execution instruction for AI
    if not dry_run and result.returncode == 0:
        # Extract JSON from output
        json_match = re.search(
            r"AUTO-WORK RESULT \(JSON\):.*?=+\s*\n(.*?)\n=+", result.stdout, re.DOTALL
        )
        if json_match:
            try:
                output_data = json.loads(json_match.group(1))
                execution_cmd = output_data.get("execution_instruction", "")
                if execution_cmd:
                    console.print(
                        f"\n[bold cyan]🤖 AI: I will now execute:[/bold cyan] {execution_cmd}\n"
                    )
            except json.JSONDecodeError:
                pass

    if result.returncode != 0:
        raise typer.Exit(result.returncode)


@app.command()
def improve(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    focus: str | None = typer.Option(
        None, "--focus", "-f", help="Focus area (file path, work effort, or 'all')"
    ),
    category: str | None = typer.Option(
        None,
        "--category",
        "-c",
        help="Filter by category (code, documentation, architecture, testing, performance, usability)",
    ),
    recent_only: bool = typer.Option(False, "--recent", "-r", help="Only analyze recent changes"),
    output: str | None = typer.Option(
        None, "--output", "-o", help="Save improvement report to file"
    ),
):
    """
    Analyze work and suggest improvements.

    Analyzes code, documentation, architecture, and implementation to identify
    improvement opportunities with prioritized recommendations.
    """
    project_path = resolve_project_path(path)

    from .core.improve import ImproveManager

    improve_manager = ImproveManager(project_path)

    output_path = None
    if output:
        output_path = Path(output)

    result = improve_manager.run_improve(
        focus=focus, category=category, recent_only=recent_only, output_path=output_path
    )

    if result["success"]:
        summary = result["summary"]
        console.print(
            f"\n[green]✅[/green] Analysis complete: {summary['total']} improvements identified"
        )
        if summary["top_3"]:
            console.print(f"[dim]Top priority: {summary['top_3'][0]['title']}[/dim]")
    else:
        console.print("[red]❌ Analysis failed[/red]")
        raise typer.Exit(1)


@app.command()
def celebrate(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    achievement: str | None = typer.Option(
        None, "--achievement", "-a", help="What was accomplished"
    ),
    message: str | None = typer.Option(None, "--message", "-m", help="Custom celebration message"),
    no_print: bool = typer.Option(False, "--no-print", help="Don't print PDF, just generate it"),
):
    """
    Generate and print a celebratory PDF!

    Creates a beautiful ArXiv-style celebration PDF and prints it to the material world.
    Perfect for acknowledging achievements, milestones, and moments of success.
    """
    project_path = resolve_project_path(path)

    from .core.celebrate import CelebrateManager

    celebrate_manager = CelebrateManager(project_path)
    pdf_path = celebrate_manager.celebrate(
        achievement=achievement, message=message, print_pdf=not no_print
    )

    if pdf_path:
        console.print("\n[green]✅ Celebration PDF ready![/green]")
        console.print(f"[dim]Location: {pdf_path.relative_to(project_path)}[/dim]")
    else:
        console.print("[red]❌ Failed to generate celebration PDF[/red]")
        raise typer.Exit(1)


@app.command()
def audit(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    output: str | None = typer.Option(None, "--output", "-o", help="Custom output path"),
):
    """
    Audit the conversation - analyze quality, completeness, issues, and improvements.

    Analyzes current conversation for quality, completeness, potential issues,
    and provides recommendations for improvement.
    """
    project_path = resolve_project_path(path)

    from .core.audit import AuditManager

    audit_manager = AuditManager(project_path)
    audit_manager.run_audit(output_path=output)


@app.command()
def proceed(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    focus: str | None = typer.Option(
        None, "--focus", "-f", help="Focus area: assumptions, ambiguity, context"
    ),
    strict: bool = typer.Option(False, "--strict", "-s", help="Ask questions before proceeding"),
    relaxed: bool = typer.Option(False, "--relaxed", "-r", help="Proceed with best understanding"),
):
    """
    Keep doing what you're doing, but verify context and assumptions first.

    Pauses to check larger context, reflect on assumptions, ask clarifying questions,
    perform a "flight check", then proceeds with verified understanding. Ensures no
    unverified assumptions or unclear ambiguity before taking actions.
    """
    project_path = resolve_project_path(path)

    from .core.proceed import ProceedManager

    proceed_manager = ProceedManager(project_path)
    proceed_manager.run_proceed(
        focus=focus,
        strict=strict,
        relaxed=relaxed,
    )


@app.command()
def check_assumptions(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    focus: str | None = typer.Option(
        None, "--focus", "-f", help="Focus area: code, dependencies, data, system, behavioral"
    ),
    critical_only: bool = typer.Option(
        False, "--critical", "-c", help="Only check critical assumptions"
    ),
    test: bool = typer.Option(
        False, "--test", "-t", help="Run experiments for assumptions needing testing"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed evidence traces"),
):
    """
    View and analyze data traces.

    Actions:
      - list: Show recent traces
      - show: Display detailed trace tree for a specific trace ID

    Examples:
      waft trace list
      waft trace list --limit 20
      waft trace show <trace-id>
    """
    from .core.tracing import TraceViewer

    viewer = TraceViewer()

    if action == "list":
        recent_traces = viewer.list_recent_traces(limit=limit)
        if not recent_traces:
            console.print("[yellow]No traces found.[/yellow]")
            return

        console.print(f"\n[bold]Recent Traces[/bold] (showing {len(recent_traces)}):\n")
        for span in recent_traces:
            summary = viewer.format_trace_summary(span)
            console.print(summary)

@app.command()
def final_report(
    title: str = typer.Option("Final Report", "--title", "-t", help="Report title"),
    subtitle: str | None = typer.Option(None, "--subtitle", "-s", help="Report subtitle"),
    output_name: str | None = typer.Option(
        None, "--output", "-o", help="Output filename (without extension)"
    ),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """
    Generate a comprehensive final report PDF using the Science Textbook LaTeX template.
    """
    console.print("\n[bold cyan]📚 Waft[/bold cyan] - Generating Final Report\n")

    from .core.final_report import FinalReportGenerator

    try:
        generator = FinalReportGenerator(project_path)

        console.print("[yellow]→[/yellow] Gathering session data...")
        pdf_path = generator.generate_report(
            title=title, subtitle=subtitle, output_name=output_name
        )

        console.print("\n[green]✅[/green] Final report generated successfully!")
        console.print(f"   Location: {pdf_path}")
        console.print("   PDF opened in default viewer")

        _process_tavern_hook(project_path, "final_report", True)

    except FileNotFoundError as e:
        console.print(f"[red]❌[/red] Error: {e}")
        console.print(
            f"[dim]Science Textbook template not found. Expected at: {project_path / '_science_textbook' / 'stb-template.tex'}[/dim]"
        )
        _process_tavern_hook(project_path, "final_report", False)
    except RuntimeError as e:
        console.print(f"[red]❌[/red] LaTeX compilation failed: {e}")
        console.print("[dim]Make sure pdflatex is installed:[/dim]")
        console.print("[dim]  macOS: brew install --cask mactex[/dim]")
        console.print("[dim]  Linux: sudo apt-get install texlive-full[/dim]")
        _process_tavern_hook(project_path, "final_report", False)
    except Exception as e:
        console.print(f"[red]❌[/red] Error generating report: {e}")
        _process_tavern_hook(project_path, "final_report", False)


@app.command()
def validate_empirica(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    fix: bool = typer.Option(False, "--fix", "-f", help="Attempt to fix issues automatically"),
):
    """
    Run preflight validation checks on Empirica setup.

    Validates:
    - Git repository initialization
    - Empirica initialization
    - CLI availability
    - Project existence
    - Session creation capability
    """
    project_path = resolve_project_path(path)

    console.print("\n[bold cyan]🔍 Waft[/bold cyan] - Empirica Validation\n")

    from rich.table import Table

    from .core.empirica import EmpiricaManager

    empirica = EmpiricaManager(project_path)

    console.print("[yellow]→[/yellow] Running validation checks...")
    validation = empirica.validate_setup()

    # Create validation table
    table = Table(
        title="Empirica Validation Results", show_header=True, header_style="bold magenta"
    )
    table.add_column("Check", style="cyan")
    table.add_column("Status", style="yellow")
    table.add_column("Details", style="dim")

    # Git check
    git_status = "✅" if validation["git_initialized"] else "❌"
    table.add_row(
        "Git Initialized",
        git_status,
        "Required for Empirica" if validation["git_initialized"] else "Not initialized",
    )

    # Empirica check
    empirica_status = "✅" if validation["empirica_initialized"] else "⚠️"
    table.add_row(
        "Empirica Initialized",
        empirica_status,
        "Ready" if validation["empirica_initialized"] else "Will auto-initialize",
    )

    # CLI check
    cli_status = "✅" if validation["cli_available"] else "❌"
    cli_details = validation["cli_version"] or "Not available"
    table.add_row("CLI Available", cli_status, cli_details)

    # Project check
    project_status = "✅" if validation["project_exists"] else "⚠️"
    project_details = validation["project_id"] or "Will auto-create"
    table.add_row("Project Exists", project_status, project_details)

    # Session check
    session_status = "✅" if validation["session_creatable"] else "⚠️"
    table.add_row(
        "Session Creation",
        session_status,
        "Working" if validation["session_creatable"] else "May fail",
    )

    console.print("\n")
    console.print(table)

    # Show errors
    if validation["errors"]:
        console.print("\n[bold red]❌ Errors:[/bold red]")
        for error in validation["errors"]:
            console.print(f"  • {error}")

    # Show warnings
    if validation["warnings"]:
        console.print("\n[bold yellow]⚠️  Warnings:[/bold yellow]")
        for warning in validation["warnings"]:
            console.print(f"  • {warning}")

    # Overall status
    if validation["ready"]:
        console.print("\n[bold green]✅ Empirica is ready![/bold green]")
        _process_tavern_hook(project_path, "validate_empirica", True)
    else:
        console.print("\n[bold red]❌ Empirica is not ready[/bold red]")
        if fix:
            console.print("\n[yellow]→[/yellow] Attempting to fix issues...")
            try:
                result = empirica.ensure_ready()
                if result.get("ready"):
                    console.print("[green]✅ Fixed! Empirica is now ready.[/green]")
                else:
                    console.print(
                        f"[red]❌ Could not fix: {result.get('message', 'Unknown error')}[/red]"
                    )
            except RuntimeError as e:
                console.print(f"[red]❌ Fix failed: {e}[/red]")
        else:
            console.print("\n[dim]Run with --fix to attempt automatic fixes[/dim]")
        _process_tavern_hook(project_path, "validate_empirica", False)


@app.command()
def oracle(
    question: str | None = typer.Argument(None, help="Question or context for guidance"),
    assess: str | None = typer.Option(
        None, "--assess", "-a", help="Assess a decision (provide description)"
    ),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """
    Consult TheOracle for epistemic insights and guidance.

    TheOracle provides epistemic intelligence based on Empirica state, offering
    insights, recommendations, and decision support.
    """
    project_path = resolve_project_path(path)

    console.print("\n[bold cyan]🔮 Waft[/bold cyan] - Consulting TheOracle\n")

    from rich.table import Table

    from .core.science import TheOracle

    try:
        # TheOracle will FORCE Empirica to be ready - no degraded mode
        # It will raise RuntimeError if Empirica cannot be initialized
        console.print("[yellow]→[/yellow] Ensuring Empirica is ready...")

        # Load personality if available
        from .core.science.oracle_personality_tools import PersonalityManager

        personality_manager = PersonalityManager(project_path)
        personality = personality_manager.load_personality()

        oracle = TheOracle(project_path, ai_id="claude-code", personality=personality)

        # Get epistemic state (Empirica is guaranteed to be ready)
        console.print("[yellow]→[/yellow] Gathering epistemic state...")
        state = oracle.get_epistemic_state()

        # Full context available - display epistemic state
        epistemic_state = state.get("epistemic_state", {})
        vectors = epistemic_state.get("vectors", {})
        foundation = vectors.get("foundation", {})

        know = foundation.get("know", 0.0) if foundation else 0.0
        uncertainty = vectors.get("uncertainty", 1.0)
        engagement = vectors.get("engagement", 0.0)

        console.print("[green]✓[/green] Epistemic state retrieved")

        # Get phase
        phase = oracle.get_epistemic_phase()
        console.print(f"\n[bold]Epistemic Phase:[/bold] [cyan]{phase}[/cyan]")

        # Display vectors table
        table = Table(title="Epistemic Vectors", show_header=True, header_style="bold magenta")
        table.add_column("Vector", style="cyan")
        table.add_column("Value", style="yellow")
        table.add_column("Interpretation", style="dim")

        table.add_row("Knowledge", f"{know:.0%}", "What we know" if know > 0.5 else "Low knowledge")
        table.add_row(
            "Uncertainty",
            f"{uncertainty:.0%}",
            "High uncertainty" if uncertainty > 0.5 else "Low uncertainty",
        )
        table.add_row(
            "Engagement",
            f"{engagement:.0%}",
            "Active engagement" if engagement > 0.5 else "Low engagement",
        )

        console.print("\n")
        console.print(table)

        # Get recent insights
        console.print("\n[yellow]→[/yellow] Retrieving recent insights...")
        insights = oracle.get_insights(limit=5)
        unknowns = oracle.get_unknowns(limit=5)

        console.print(f"[green]✓[/green] Found {len(insights)} insights, {len(unknowns)} unknowns")

        if insights:
            console.print("\n[bold]Recent Insights:[/bold]")
            for i, insight in enumerate(insights[-5:], 1):
                insight_text = str(insight) if isinstance(insight, dict) else insight
                if len(insight_text) > 80:
                    console.print(f"  {i}. [dim]{insight_text[:80]}...[/dim]")
                else:
                    console.print(f"  {i}. {insight_text}")
        else:
            console.print("  [dim]No recent insights recorded[/dim]")

        if unknowns:
            console.print("\n[bold]Open Unknowns:[/bold]")
            for i, unknown in enumerate(unknowns[-5:], 1):
                unknown_text = str(unknown) if isinstance(unknown, dict) else unknown
                if len(unknown_text) > 80:
                    console.print(f"  {i}. [yellow]{unknown_text[:80]}...[/yellow]")
                else:
                    console.print(f"  {i}. {unknown_text}")
        else:
            console.print("\n[bold]Open Unknowns:[/bold]")
            console.print("  [dim]No open unknowns recorded[/dim]")

        # Handle question or assessment
        if assess:
            # Decision assessment
            console.print(f"\n[yellow]→[/yellow] Assessing decision: {assess}")
            assessment = oracle.assess_decision(
                {"description": assess, "scope": "medium", "type": "implementation"}
            )

            gate_result = assessment.get("gate_result", "UNKNOWN")
            if gate_result == "PROCEED":
                gate_color = "green"
            elif gate_result in ["BRANCH", "REVISE"]:
                gate_color = "yellow"
            else:
                gate_color = "red"

            # Apply personality to recommendation display
            recommendation = assessment.get("recommendation", "No recommendation")
            personality_info = oracle.get_personality_info()
            transition = oracle.personality.get_transition()

            console.print("\n[bold]Decision Assessment:[/bold]")
            console.print(f"  Gate Result: [{gate_color}]{gate_result}[/{gate_color}]")

            if transition and transition != "Consider this...":
                console.print(f"  [dim]{transition}[/dim]")

            console.print(
                Panel(
                    recommendation,
                    title=f"Recommendation from {personality_info['name']}",
                    border_style="cyan",
                )
            )

        elif question:
            # Specific question
            personality_info = oracle.get_personality_info()
            greeting = oracle.personality.get_greeting()
            if greeting and greeting != "I see...":
                console.print(f"\n[dim italic]{greeting}[/dim italic]")

            console.print(f"\n[yellow]→[/yellow] Seeking guidance: {question}")
            guidance = oracle.provide_guidance(question)

            console.print("\n[bold cyan]🔮 Oracle Guidance:[/bold cyan]")

            recommendation = guidance.get("recommendation", "No recommendation available")
            transition = oracle.personality.get_transition()
            if transition and transition != "Consider this...":
                console.print(f"[dim]{transition}[/dim]")

            console.print(
                Panel(
                    recommendation,
                    title=f"Guidance from {personality_info['name']}",
                    border_style="cyan",
                )
            )

            console.print(
                f"\n[dim]Knowledge Coverage: {guidance.get('knowledge_coverage', 0):.0%}[/dim]"
            )
            console.print(f"[dim]Phase: {guidance.get('epistemic_phase', 'UNKNOWN')}[/dim]")
        else:
            # General guidance
            personality_info = oracle.get_personality_info()
            greeting = oracle.personality.get_greeting()
            if greeting and greeting != "I see...":
                console.print(f"\n[dim italic]{greeting}[/dim italic]")

            console.print("\n[yellow]→[/yellow] Seeking general guidance...")

            # Show thinking process
            from .core.science.oracle_thinking import (
                display_oracle_thinking,
                display_thinking_step_by_step,
            )

            console.print("\n[bold cyan]🧠 TheOracle is thinking...[/bold cyan]\n")

            # Step-by-step thinking display
            thinking_data = {}

            def thinking_callback(step: str, data: dict[str, Any]) -> None:
                """Callback to capture thinking steps."""
                thinking_data[step] = data
                display_thinking_step_by_step(console, step, data, delay=0.3)

            guidance = oracle.provide_guidance(
                "What should we focus on next?",
                show_thinking=True,
                thinking_callback=thinking_callback,
            )

            # Display full thinking dashboard
            console.print("\n")
            display_oracle_thinking(
                console,
                "What should we focus on next?",
                guidance.get("preflight", {}),
                guidance.get("reflection", {}),
                guidance.get("findings", []),
                guidance.get("unknowns", []),
                guidance.get("check", {}),
                guidance.get("epistemic_state", {}),
                guidance.get("postflight"),
                guidance.get("storage_info"),
            )
            console.print("\n")

            console.print("\n[bold cyan]🔮 Oracle Guidance:[/bold cyan]")

            # Display Empirica workflow results
            preflight = guidance.get("preflight", {})
            if preflight:
                know = preflight.get("know", 0.0)
                uncertainty = preflight.get("uncertainty", 1.0)
                console.print(
                    f"\n[dim]📊 Preflight: KNOW={know:.0%} ({preflight.get('know_level', 'Unknown')}), UNCERTAINTY={uncertainty:.0%} ({preflight.get('uncertainty_level', 'Unknown')})[/dim]"
                )
                if preflight.get("investigate_required"):
                    console.print("[dim]   → INVESTIGATE REQUIRED[/dim]")

            check = guidance.get("check", {})
            if check:
                confidence = check.get("confidence", 0.0)
                decision = check.get("decision", "UNKNOWN")
                console.print(
                    f"[dim]✅ Check: CONFIDENCE={confidence:.0%}, DECISION={decision}[/dim]"
                )

            # Display reflection if available
            reflection = guidance.get("reflection")
            if reflection and reflection.get("reflection_summary"):
                console.print(f"\n[dim]💭 Reflection: {reflection['reflection_summary']}[/dim]")
                if reflection.get("relevant_experiences"):
                    exp_count = len(reflection["relevant_experiences"])
                    console.print(
                        f"[dim]   ({exp_count} relevant past experiences considered)[/dim]"
                    )

            postflight = guidance.get("postflight", {})
            if postflight and postflight.get("guidance_provided"):
                console.print("[dim]📈 Postflight: Guidance provided, learning tracked[/dim]")

            recommendation = guidance.get("recommendation", "No recommendation available")
            transition = oracle.personality.get_transition()
            if transition and transition != "Consider this...":
                console.print(f"[dim]{transition}[/dim]")

            console.print(
                Panel(
                    recommendation,
                    title=f"Guidance from {personality_info['name']}",
                    border_style="cyan",
                )
            )

            console.print(
                f"\n[dim]Knowledge Coverage: {guidance.get('knowledge_coverage', 0):.0%}[/dim]"
            )
            console.print(f"[dim]Phase: {guidance.get('epistemic_phase', 'UNKNOWN')}[/dim]")

        # Show personality conclusion
        conclusion = oracle.personality.get_conclusion()
        if conclusion and conclusion != "The path forward is clear.":
            console.print(f"\n[dim italic]{conclusion}[/dim italic]")

        # Display personality info
        personality_info = oracle.get_personality_info()
        console.print(
            f"\n[dim]Oracle: {personality_info['name']} ({personality_info['type']})[/dim]"
        )

        _process_tavern_hook(project_path, "oracle", True)

    except RuntimeError as e:
        error_msg = str(e)
        console.print(f"[red]❌ Empirica Error: {error_msg}[/red]")
        console.print("\n[dim]The Oracle requires Empirica to be fully functional.[/dim]")

        # Provide specific guidance based on error
        if "Git not available" in error_msg:
            console.print("\n[bold yellow]Fix:[/bold yellow]")
            console.print("[dim]  1. Install git: https://git-scm.com/downloads[/dim]")
            console.print("[dim]  2. Run: git init (if not already done)[/dim]")
            console.print("[dim]  3. Try again: waft oracle[/dim]")
        elif "CLI not found" in error_msg or "not installed" in error_msg:
            console.print("\n[bold yellow]Fix:[/bold yellow]")
            console.print("[dim]  1. Install Empirica: pip install empirica[/dim]")
            console.print("[dim]  2. Verify: empirica --version[/dim]")
            console.print("[dim]  3. Try again: waft oracle[/dim]")
        elif "not working" in error_msg or "failed" in error_msg:
            console.print("\n[bold yellow]Fix:[/bold yellow]")
            console.print("[dim]  1. Check Empirica installation: empirica --version[/dim]")
            console.print("[dim]  2. Reinstall if needed: pip install --upgrade empirica[/dim]")
            console.print("[dim]  3. Try again: waft oracle[/dim]")
        else:
            console.print("\n[bold yellow]Fix:[/bold yellow]")
            console.print("[dim]  1. Run: waft init (to initialize Empirica)[/dim]")
            console.print("[dim]  2. Verify: empirica --version[/dim]")
            console.print("[dim]  3. Try again: waft oracle[/dim]")

        _process_tavern_hook(project_path, "oracle", False)
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]❌ Error consulting Oracle: {e}[/red]")
        _process_tavern_hook(project_path, "oracle", False)
        raise typer.Exit(1)


@app.command()
def oracle_journal(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    show: bool = typer.Option(False, "--show", "-s", help="Show recent journal entries"),
    search: str | None = typer.Option(None, "--search", help="Search journal and memory"),
    memory: bool = typer.Option(False, "--memory", "-m", help="Show memory summary"),
    patterns: bool = typer.Option(False, "--patterns", help="Show learned patterns"),
    limit: int = typer.Option(10, "--limit", "-l", help="Number of entries to show"),
):
    """
    View Oracle journal and memory.

    The Oracle maintains its own journal of consultations, assessments, and learnings.
    """
    project_path = resolve_project_path(path)

    from rich.table import Table

    from .core.science.oracle_journal import OracleJournal

    console.print("\n[bold cyan]📖 Waft[/bold cyan] - Oracle Journal & Memory\n")

    journal = OracleJournal(project_path)

    # Show memory summary
    if memory or (not show and not search and not patterns):
        summary = journal.get_memory_summary()

        console.print("[bold]Memory Summary[/bold]\n")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="yellow")

        table.add_row("Total Consultations", str(summary["total_consultations"]))
        table.add_row("Insights Remembered", str(summary["insights_count"]))
        table.add_row(
            "Successful Recommendations", str(summary["successful_recommendations_count"])
        )
        table.add_row("Epistemic History Points", str(summary["epistemic_history_length"]))

        if summary["first_consultation"]:
            table.add_row("First Consultation", summary["first_consultation"][:10])
        if summary["last_consultation"]:
            table.add_row("Last Consultation", summary["last_consultation"][:10])

        console.print(table)

        # Learned patterns summary
        patterns_info = summary["learned_patterns"]
        console.print("\n[bold]Learned Patterns[/bold]")
        console.print(f"  Question Keywords: {patterns_info['question_keywords']}")
        console.print(f"  Phase Recommendations: {patterns_info['phase_recommendations']}")
        console.print(f"  Gate Outcomes Tracked: {patterns_info['gate_outcomes']}")

    # Show recent consultations
    if show:
        console.print(f"\n[bold]Recent Consultations[/bold] (last {limit})\n")

        consultations = journal.get_recent_consultations(limit=limit)

        if consultations:
            for i, consultation in enumerate(consultations, 1):
                console.print(
                    f"[bold]{i}. {consultation.get('question', 'No question')[:60]}[/bold]"
                )
                console.print(f"   Phase: {consultation.get('epistemic_phase', 'UNKNOWN')}")
                console.print(f"   Coverage: {consultation.get('knowledge_coverage', 0):.0%}")
                console.print(f"   Time: {consultation.get('timestamp', '')[:19]}")
                console.print("")
        else:
            console.print("[dim]No consultations recorded yet.[/dim]")

    # Search memory
    if search:
        console.print(f"\n[bold]Search Results for: '{search}'[/bold]\n")

        results = journal.search_memory(search, limit=limit)

        if results:
            for i, result in enumerate(results, 1):
                result_type = result.get("type", "unknown")
                content = result.get("content", "")

                console.print(f"[bold]{i}. [{result_type.upper()}] {content[:80]}[/bold]")
                if result.get("impact"):
                    console.print(f"   Impact: {result.get('impact'):.2f}")
                if result.get("phase"):
                    console.print(f"   Phase: {result.get('phase')}")
                console.print(f"   Time: {result.get('timestamp', '')[:19]}")
                console.print("")
        else:
            console.print("[dim]No results found.[/dim]")

    # Show patterns
    if patterns:
        console.print("\n[bold]Learned Patterns[/bold]\n")

        # Top keywords
        top_keywords = journal.get_top_keywords(limit=10)
        if top_keywords:
            console.print("[bold]Top Question Keywords:[/bold]")
            for keyword, count in top_keywords:
                console.print(f"  • {keyword}: {count} occurrences")

        # Phase recommendations
        phase_recs = journal.patterns.get("phase_recommendations", {})
        if phase_recs:
            console.print("\n[bold]Recommendations by Phase:[/bold]")
            for phase, recs in phase_recs.items():
                console.print(f"  {phase}: {len(recs)} recommendations")
                if recs:
                    console.print(f"    Example: {recs[-1][:60]}...")

        # Gate outcomes
        gate_outcomes = journal.patterns.get("gate_outcomes", {})
        if gate_outcomes:
            console.print("\n[bold]Gate Outcomes:[/bold]")
            for gate, count in sorted(gate_outcomes.items(), key=lambda x: x[1], reverse=True):
                console.print(f"  {gate}: {count} occurrences")

    _process_tavern_hook(project_path, "oracle_journal", True)


@app.command()
def pantheon(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """
    Summon the ENTIRE PANTHEON to weigh in and pass judgment.

    The Pantheon gathers to review evidence, discuss, and collectively determine
    what should be done next based on current state and context.
    """
    project_path = resolve_project_path(path)

    console.print("\n[bold gold1]⚡ Waft[/bold gold1] - Summoning The Pantheon\n")

    try:
        from .cli.pantheon_command import pantheon_command

        judgment = pantheon_command(project_path)

        # Log to Empirica if available
        try:
            from .core.empirica import EmpiricaManager

            empirica = EmpiricaManager(project_path)
            if empirica.is_initialized():
                primary = judgment.get("primary_focus", {})
                entity = primary.get("entity", "Unknown")
                recommendation = primary.get("recommendation", "")
                empirica.log_finding(
                    f"Pantheon judgment: {entity} recommends {recommendation[:100]}", impact=0.7
                )
        except Exception:
            pass

        _process_tavern_hook(project_path, "pantheon", True, {"judgment": judgment})

    except Exception as e:
        console.print(f"[red]❌ Error summoning Pantheon: {e}[/red]")
        _process_tavern_hook(project_path, "pantheon", False)
        raise typer.Exit(1)


@app.command()
def tell_story(
    story: str = typer.Argument(..., help="Story input (text, can be multi-line)"),
    title: str | None = typer.Option(
        None, "--title", "-t", help="PDF title (default: auto-generated)"
    ),
    style: str = typer.Option(
        "premium", "--style", "-s", help="PDF style (premium/clinical_standard/professional)"
    ),
    narrative_style: str = typer.Option(
        "medium", "--narrative", "-n", help="Narrative style (simple/medium)"
    ),
    structure: str = typer.Option(
        "linear", "--structure", help="Story structure (linear/three_act)"
    ),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    no_oracle: bool = typer.Option(False, "--no-oracle", help="Skip Oracle insights"),
    output: str | None = typer.Option(
        None, "--output", "-o", help="Output PDF path (default: auto-generated)"
    ),
):
    """
    Tell a story using TheOracle, Storyteller, and TavernKeeper.

    Generates a narrative PDF from your story input, enriched with epistemic insights
    from TheOracle and narrative elements from TavernKeeper.
    """
    project_path = resolve_project_path(path)

    console.print("\n[bold cyan]📖 Waft[/bold cyan] - Telling Your Story\n")

    import subprocess
    from pathlib import Path

    from .core.campfire import TheCampfire

    try:
        # Use TheCampfire to gather around the campfire
        console.print("[yellow]→[/yellow] Gathering around the campfire...")
        campfire = TheCampfire(project_path)
        console.print("[green]✓[/green] Campfire ready")

        # Tell the story
        console.print("[yellow]→[/yellow] Telling story...")
        result = campfire.gather_around_the_campfire(
            story_input=story,
            title=title,
            style=style,
            narrative_style=narrative_style,
            structure=structure,
            include_oracle=not no_oracle,
            save_story=True,
        )

        pdf_path = Path(result["pdf_path"])
        story_metadata = result["story"]

        console.print(f"[green]✓[/green] Story told! (ID: {story_metadata['id']})")
        console.print(f"[green]✓[/green] PDF generated: {pdf_path}")

        if result.get("oracle_insights"):
            console.print(
                f"[green]✓[/green] Oracle insights included (Phase: {result['oracle_insights']['phase']})"
            )

        # Open PDF
        console.print("[yellow]→[/yellow] Opening PDF...")
        try:
            subprocess.run(["open", str(pdf_path)], check=True)
            console.print("[green]✓[/green] PDF opened")
        except subprocess.CalledProcessError:
            console.print("[yellow]⚠️[/yellow]  Could not open PDF automatically")
            console.print(f"[dim]PDF saved at: {pdf_path}[/dim]")
        except FileNotFoundError:
            # Try alternative on Linux
            try:
                subprocess.run(["xdg-open", str(pdf_path)], check=True)
                console.print("[green]✓[/green] PDF opened")
            except (subprocess.CalledProcessError, FileNotFoundError):
                console.print("[yellow]⚠️[/yellow]  Could not open PDF automatically")
                console.print(f"[dim]PDF saved at: {pdf_path}[/dim]")

        # Process TavernKeeper hook
        _process_tavern_hook(
            project_path,
            "tell_story",
            True,
            {
                "pdf_path": str(pdf_path),
                "story_id": story_metadata["id"],
                "title": story_metadata["title"],
                "style": style,
            },
        )

        console.print("\n[bold green]✅ Story complete![/bold green]")
        console.print(f"[dim]PDF: {pdf_path}[/dim]")
        console.print("[dim]Story saved to campfire. Start with: waft campfire[/dim]")

    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {e}")
        logger.exception("Error in tell_story command")
        _process_tavern_hook(project_path, "tell_story", False, {"error": str(e)})
        raise typer.Exit(1)


@app.command(name="print-pdf")
def print_pdf(
    force_create: bool = typer.Option(
        False, "--force-create", help="Force creation of new PDF even if relevant one exists"
    ),
    no_print: bool = typer.Option(
        False, "--no-print", help="Generate but don't print (preview only)"
    ),
    style: str = typer.Option(
        "clinical_standard",
        "--style",
        "-s",
        help="PDF style (clinical_standard/premium/professional)",
    ),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """
    Print most relevant PDF or create evolved PDF using WAFT.

    Intelligently finds the most relevant PDF based on conversation context,
    active files, work efforts, and Oracle epistemic state. If no relevant PDF
    exists or relevance is low, creates an evolved PDF using WAFT principles.
    """
    project_path = resolve_project_path(path)

    console.print("\n[bold cyan]🖨️  Waft[/bold cyan] - Print PDF\n")

    import platform
    import subprocess

    from .core.pdf_discovery import PDFDiscovery
    from .core.pdf_evolution import PDFEvolution
    from .core.science import TheOracle

    try:
        # Gather context
        console.print("[yellow]→[/yellow] Gathering context...")

        # Build context dictionary
        # Note: In a real implementation, this would gather from conversation history,
        # active files, etc. For now, we use minimal context.
        context = {
            "conversation": [],  # Would be populated from conversation history
            "active_files": [],  # Would be populated from active files
            "work_efforts": [],  # Would be populated from active work efforts
        }

        # Try to initialize Oracle
        oracle = None
        oracle_state = None
        try:
            oracle = TheOracle(project_path)
            oracle_state = oracle.get_epistemic_state()
            context["oracle_state"] = oracle_state
            console.print("[green]✓[/green] Oracle available")
        except RuntimeError:
            console.print("[dim]Oracle not available (Empirica not initialized)[/dim]")
        except Exception as e:
            console.print(f"[dim]Oracle error: {e}[/dim]")

        # Discover relevant PDF
        console.print("[yellow]→[/yellow] Discovering relevant PDF...")
        discovery = PDFDiscovery(project_path)

        pdf_path = None
        if not force_create:
            pdf_path = discovery.find_relevant_pdf(context)

        # If found and relevant, use it
        if pdf_path and pdf_path.exists():
            # Score it to check relevance
            score = discovery.score_pdf(pdf_path, context)

            if score >= 0.5:  # Threshold for relevance
                console.print(
                    f"[green]✓[/green] Found relevant PDF: {pdf_path.name} (relevance: {score:.0%})"
                )
                console.print(f"[dim]   Path: {pdf_path}[/dim]")
            else:
                console.print(
                    f"[yellow]⚠️[/yellow]  Found PDF but low relevance ({score:.0%}), creating new one..."
                )
                pdf_path = None

        # If no relevant PDF found, create evolved PDF
        if not pdf_path:
            console.print("[yellow]→[/yellow] Creating evolved PDF using WAFT principles...")

            evolution = PDFEvolution(project_path, oracle)
            pdf_path = evolution.evolve_pdf(context, style=style)

            console.print(f"[green]✓[/green] Created evolved PDF: {pdf_path}")

        # Print PDF if requested
        if not no_print:
            console.print("[yellow]→[/yellow] Printing PDF...")

            # Use PDF class print method

            # Create PDF instance to use print method
            # Note: We need to load the existing PDF or recreate it
            # For now, use direct lpr command
            system = platform.system()
            try:
                if system == "Darwin":  # macOS
                    result = subprocess.run(
                        ["lpr", str(pdf_path)], capture_output=True, text=True, check=False
                    )
                elif system == "Windows":
                    result = subprocess.run(
                        ["print", str(pdf_path)],
                        shell=True,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                else:  # Linux
                    result = subprocess.run(
                        ["lpr", str(pdf_path)], capture_output=True, text=True, check=False
                    )

                if result.returncode == 0:
                    console.print("[green]✓[/green] PDF sent to printer!")
                else:
                    console.print(f"[yellow]⚠️[/yellow]  Print command returned: {result.stderr}")
                    console.print(f"[dim]PDF saved at: {pdf_path}[/dim]")
            except FileNotFoundError:
                console.print("[yellow]⚠️[/yellow]  Print command not found. Please print manually:")
                console.print(f"[dim]lpr {pdf_path}[/dim]")
            except Exception as e:
                console.print(f"[yellow]⚠️[/yellow]  Print error: {e}")
                console.print(f"[dim]PDF saved at: {pdf_path}[/dim]")
        else:
            console.print(f"[dim]PDF saved at: {pdf_path} (not printed)[/dim]")

        # Log to Oracle if available
        if oracle:
            try:
                oracle.log_insight(f"Printed PDF: {pdf_path.name}", impact=0.3)
            except Exception:
                pass

        # Process TavernKeeper hook
        _process_tavern_hook(
            project_path,
            "print_pdf",
            True,
            {
                "pdf_path": str(pdf_path),
                "created": not force_create and pdf_path and pdf_path.exists(),
                "style": style,
            },
        )

        console.print("\n[bold green]✅ Complete![/bold green]")
        console.print(f"[dim]PDF: {pdf_path}[/dim]")

    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {e}")
        logger.exception("Error in print_pdf command")
        _process_tavern_hook(project_path, "print_pdf", False, {"error": str(e)})
        raise typer.Exit(1)


@app.command(name="evolve-another-template")
def evolve_another_template(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    template: str | None = typer.Option(
        None, "--template", "-t", help="Template name (academic, field-guide, etc.)"
    ),
    list_templates: bool = typer.Option(False, "--list", "-l", help="List available templates"),
    all_templates: bool = typer.Option(False, "--all", "-a", help="Generate all templates"),
):
    """
    Generate evolution report using alternative template format.

    Creates a new version of the complete evolution report using a different
    template style (academic paper, field guide, lab notes, etc.) instead
    of the default format.

    Requires a previous /evolve run to have evolution data available.
    """
    project_path = resolve_project_path(path)

    import subprocess
    import sys

    script_path = project_path / "scripts" / "evolve_another_template.py"

    if not script_path.exists():
        console.print(f"[red]❌ Script not found: {script_path}[/red]")
        raise typer.Exit(1)

    # Build command
    cmd = [sys.executable, str(script_path)]
    if list_templates:
        cmd.append("--list")
    elif all_templates:
        cmd.append("--all")
    elif template:
        cmd.extend(["--template", template])

    # Run script
    result = subprocess.run(cmd, cwd=str(project_path))

    if result.returncode != 0:
        raise typer.Exit(result.returncode)


@app.command(name="chronicler")
def chronicler_start(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    reset_hour: int = typer.Option(
        5, "--reset-hour", help="Hour to reset daily cycle (default: 5 AM)"
    ),
):
    """
    Start TheChronicler - Self-monitoring system.

    TheChronicler observes, records, and reports on all activity within WAFT:
    - File system changes (genesis, exodus, mutations)
    - Git repository activity
    - Work effort lifecycle

    Generates:
    - Hourly reports on the hour
    - Daily reports at 5 AM (reset cycle)

    Observations stored in: _chronicler/observations/
    Reports stored in: _chronicler/reports/
    """
    project_path = resolve_project_path(path)

    console.print("\n[bold cyan]📜[/bold cyan] [bold]TheChronicler[/bold]")
    console.print(
        "[dim]The Chronicler of All System Activity - Observing Genesis and Exodus[/dim]\n"
    )

    from .core.chronicler import TheChronicler

    try:
        chronicler = TheChronicler(project_path, reset_hour=reset_hour)
        chronicler.start()

        console.print("[green]✅[/green] TheChronicler monitoring active")
        console.print("[dim]Press Ctrl+C to stop[/dim]\n")

        # Keep running until interrupted
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            console.print("\n[dim]Stopping TheChronicler...[/dim]")
            chronicler.stop()
            console.print("[green]✅[/green] TheChronicler stopped")
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        logger.exception("Error starting TheChronicler")
        raise typer.Exit(1)


@app.command(name="chronicler-stats")
def chronicler_stats(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Show TheChronicler statistics."""
    project_path = resolve_project_path(path)

    from .core.chronicler import TheChronicler

    try:
        chronicler = TheChronicler(project_path)
        stats = chronicler.get_stats()

        console.print("\n[bold cyan]📊 TheChronicler Statistics[/bold cyan]\n")
        console.print(f"Date: {stats['date']}")
        console.print(f"Genesis (Created): {stats['genesis_count']}")
        console.print(f"Exodus (Deleted): {stats['exodus_count']}")
        console.print(f"Net Change: {stats['net_change']}")
        console.print(f"Observers Active: {stats['observers_active']}")
        console.print(f"Oracle Available: {stats['oracle_available']}")
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        logger.exception("Error getting TheChronicler stats")
        raise typer.Exit(1)


@app.command(name="chronicler-report")
def chronicler_report(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    hourly: bool = typer.Option(False, "--hourly", help="Generate hourly report for current hour"),
    daily: bool = typer.Option(False, "--daily", help="Generate daily report for today"),
):
    """Generate TheChronicler reports manually."""
    if not hourly and not daily:
        console.print("[red]❌ Error:[/red] Must specify --hourly or --daily")
        raise typer.Exit(1)

    project_path = resolve_project_path(path)

    from .core.chronicler import TheChronicler

    try:
        chronicler = TheChronicler(project_path)

        if hourly:
            console.print("[dim]Generating hourly report...[/dim]")
            chronicler.generate_immediate_hourly_report()
            console.print("[green]✅[/green] Hourly report generated")

        if daily:
            console.print("[dim]Generating daily report...[/dim]")
            chronicler.generate_immediate_daily_report()
            console.print("[green]✅[/green] Daily report generated")
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        logger.exception("Error generating TheChronicler report")
        raise typer.Exit(1)


@app.command()
def campfire(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    port: int = typer.Option(5000, "--port", help="Port to serve on (default: 5000)"),
    host: str = typer.Option("localhost", "--host", help="Host to bind to (default: localhost)"),
):
    """
    Start TheCampfire - Gather around to tell stories.

    TheCampfire is a self-contained full-stack application that embodies
    the essence of sitting around a campfire to tell stories.

    True Name: "Essence of Sitting Around a Campfire to Tell Stories"
    """
    project_path = resolve_project_path(path)

    console.print("\n[bold yellow]🔥[/bold yellow] [bold]TheCampfire[/bold]")
    console.print("[dim]The Essence of Sitting Around a Campfire to Tell Stories[/dim]\n")

    from .core.campfire import TheCampfire

    try:
        campfire = TheCampfire(project_path, port=port, host=host)
        campfire.serve()
    except KeyboardInterrupt:
        console.print("\n[dim]Campfire extinguished.[/dim]")
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        logger.exception("Error starting TheCampfire")
        raise typer.Exit(1)


# RAG Chatbot Commands
rag_app = typer.Typer(name="rag", help="RAG Chatbot - Query PDFs with AI")


@rag_app.command("query")
def rag_query(
    question: str = typer.Argument(..., help="Question to ask"),
    pdfs: str | None = typer.Option(None, "--pdfs", "-p", help="Comma-separated list of PDF paths"),
    path: str | None = typer.Option(None, "--path", help="Project path (default: current)"),
):
    """
    Query RAG chatbot with a question.

    Examples:
        waft rag query "What is WAFT?" --pdfs docs/welcome_packet/WAFT_WELCOME_PACKET.pdf
        waft rag query "How do agents work?" --pdfs docs/**,_work_efforts/**
    """
    project_path = resolve_project_path(path)

    try:
        from .rag import RAGChatbot

        console.print("\n[bold cyan]🤖[/bold cyan] [bold]RAG Chatbot[/bold]\n")

        chatbot = RAGChatbot(project_path=project_path)

        # Parse PDF paths
        pdf_list = []
        if pdfs:
            pdf_list = [p.strip() for p in pdfs.split(",")]

        # Query
        console.print(f"[dim]Question:[/dim] {question}")
        if pdf_list:
            console.print(f"[dim]PDFs:[/dim] {', '.join(pdf_list)}")

        console.print("\n[dim]Querying...[/dim]")
        answer = chatbot.query(question=question, pdfs=pdf_list if pdf_list else None)

        console.print(f"\n[bold]Answer:[/bold]\n{answer}\n")

    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        logger.exception("Error querying RAG")
        raise typer.Exit(1)


@rag_app.command("index")
def rag_index(
    pdfs: str = typer.Argument(..., help="Comma-separated list of PDF paths or directories"),
    path: str | None = typer.Option(None, "--path", help="Project path (default: current)"),
):
    """
    Index PDFs into the vector store.

    Examples:
        waft rag index docs/welcome_packet/WAFT_WELCOME_PACKET.pdf
        waft rag index docs/**,_work_efforts/briefs/**
    """
    project_path = resolve_project_path(path)

    try:
        from pathlib import Path

        from .rag import RAGChatbot

        console.print("\n[bold cyan]📚[/bold cyan] [bold]RAG Indexing[/bold]\n")

        chatbot = RAGChatbot(project_path=project_path)

        # Parse paths
        path_list = [p.strip() for p in pdfs.split(",")]

        # Index
        console.print(f"[dim]Indexing {len(path_list)} path(s)...[/dim]")
        for pdf_path in path_list:
            p = Path(pdf_path)
            if not p.is_absolute():
                p = project_path / p

            if p.is_file() and p.suffix.lower() == ".pdf":
                chatbot.add_pdfs([str(p)])
                console.print(f"[green]✓[/green] Indexed: {p.name}")
            elif p.is_dir():
                chatbot.index_path(p)
                pdf_count = len(list(p.rglob("*.pdf")))
                console.print(f"[green]✓[/green] Indexed {pdf_count} PDF(s) from: {p}")
            else:
                console.print(f"[yellow]⚠[/yellow]  Skipped (not a PDF or directory): {p}")

        indexed = chatbot.get_indexed_files()
        console.print(f"\n[green]✅[/green] Indexing complete. {len(indexed)} file(s) indexed.")

    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        logger.exception("Error indexing PDFs")
        raise typer.Exit(1)


@rag_app.command("ui")
def rag_ui(
    path: str | None = typer.Option(None, "--path", help="Project path (default: current)"),
    port: int = typer.Option(7860, "--port", help="Port to serve on (default: 7860)"),
    host: str = typer.Option("0.0.0.0", "--host", help="Host to bind to (default: 0.0.0.0)"),
):
    """
    Launch RAG Chatbot Gradio UI.

    Opens an interactive web interface for querying PDFs.
    """
    project_path = resolve_project_path(path)

    try:
        import sys

        # Add rag-chatbot to path
        rag_chatbot_path = project_path / "_integrations" / "rag-chatbot"
        if str(rag_chatbot_path) not in sys.path:
            sys.path.insert(0, str(rag_chatbot_path))

        from rag_chatbot import LocalRAGPipeline
        from rag_chatbot.logger import Logger
        from rag_chatbot.ui.ui import LocalChatbotUI

        console.print("\n[bold cyan]🎨[/bold cyan] [bold]RAG Chatbot UI[/bold]\n")
        console.print(f"[dim]Starting Gradio interface on http://{host}:{port}[/dim]\n")

        pipeline = LocalRAGPipeline(host="localhost")
        logger = Logger()
        ui = LocalChatbotUI(
            pipeline=pipeline,
            logger=logger,
            host="localhost",
            data_dir=str(project_path / "_hidden" / ".truth" / "rag" / "data"),
        )

        ui.launch(server_name=host, server_port=port, share=False)

    except KeyboardInterrupt:
        console.print("\n[dim]UI stopped.[/dim]")
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        logger.exception("Error launching RAG UI")
        raise typer.Exit(1)


@rag_app.command("serve")
def rag_serve(
    path: str | None = typer.Option(None, "--path", help="Project path (default: current)"),
    port: int = typer.Option(7860, "--port", help="Port to serve on (default: 7860)"),
    host: str = typer.Option("0.0.0.0", "--host", help="Host to bind to (default: 0.0.0.0)"),
):
    """
    Serve RAG Chatbot API (alias for 'ui' command).

    Serves the RAG chatbot with both UI and API access.
    """
    rag_ui(path=path, port=port, host=host)


# Register rag subcommand
app.add_typer(rag_app)


@app.command()
def dnd_scenario(
    encounter: bool = typer.Option(False, "--encounter", help="Force an encounter scenario"),
    explore: bool = typer.Option(False, "--explore", help="Free exploration mode"),
    lore: bool = typer.Option(False, "--lore", help="Focus on lore building"),
    resume: bool = typer.Option(False, "--resume", help="Resume from last scenario state"),
    party_state: bool = typer.Option(False, "--party-state", help="Show current party state"),
    crystallize: bool = typer.Option(
        False, "--crystallize", help="Freeze current state as new initial state"
    ),
    restore_initial: bool = typer.Option(
        False, "--restore-initial", help="Restore crystallized initial state"
    ),
    experiment: str | None = typer.Option(None, "--experiment", help="Experiment ID"),
    iteration: int | None = typer.Option(None, "--iteration", help="Iteration number"),
    science: bool = typer.Option(False, "--science", help="Run with /science-bitch integration"),
    hypothesis: str | None = typer.Option(
        None, "--hypothesis", help="Hypothesis statement for science mode"
    ),
    iterations: int = typer.Option(5, "--iterations", help="Number of iterations for science mode"),
):
    """
    Run interactive DnD scenarios with experimental iteration support.

    Creates an Original Realm for scenario management and supports:
    - Encounters, exploration, and lore building
    - Party state persistence
    - Experimental iteration with state crystallization
    """
    from pathlib import Path

    from .core.dnd_scenario.realm_state_preserver import RealmStatePreserver
    from .core.dnd_scenario.scenario_orchestrator import ScenarioOrchestrator
    from .core.dnd_scenario.scenario_realm import ScenarioRealm
    from .core.dnd_scenario.security import validate_experiment_id, validate_iteration

    project_path = Path.cwd()

    try:
        # Initialize realm
        realm = ScenarioRealm(project_path=project_path)

        # Create realm if it doesn't exist
        if not (realm.realm_path / "realm_manifest.json").exists():
            console.print("[yellow]Creating DnD Scenario Realm...[/yellow]")
            realm.create_realm()
            console.print("[green]✅ Realm created![/green]")

        # Initialize orchestrator
        orchestrator = ScenarioOrchestrator(realm)

        # Handle special commands first
        if party_state:
            state = orchestrator.get_party_state()
            if state:
                console.print(
                    Panel.fit(
                        f"[bold]Current Party State[/bold]\n\n{json.dumps(state, indent=2)}",
                        style="cyan",
                    )
                )
            else:
                console.print("[yellow]No party state found.[/yellow]")
            return

        if crystallize:
            console.print("[yellow]Crystallizing current state...[/yellow]")
            preserver = RealmStatePreserver(realm.realm_path, project_path)

            # Gather current state
            party_state = orchestrator.get_party_state() or {}
            state_data = {
                "party_state": party_state,
                "realm_state": realm.get_realm_manifest(),
                "timestamp": datetime.now().isoformat(),
            }

            manifest = preserver.crystallize_state(state_data)
            console.print("[green]✅ State crystallized![/green]")
            console.print(f"   Version: {manifest['version']}")
            console.print(f"   Hash: {manifest['hash'][:16]}...")
            return

        if restore_initial:
            console.print("[yellow]Restoring initial state...[/yellow]")
            preserver = RealmStatePreserver(realm.realm_path, project_path)
            state_data = preserver.restore_state()

            # Restore party state
            if "party_state" in state_data:
                orchestrator.party_state_manager.save_party_state(state_data["party_state"])

            console.print("[green]✅ Initial state restored![/green]")
            return

        # Determine mode
        mode = None
        if encounter:
            mode = "encounter"
        elif explore:
            mode = "explore"
        elif lore:
            mode = "lore"
        elif resume:
            mode = "resume"
        else:
            # Default to interactive selection
            console.print(
                "[yellow]No mode specified. Use --encounter, --explore, --lore, or --resume[/yellow]"
            )
            return

        # Validate experiment/iteration if provided
        if experiment:
            is_valid, error = validate_experiment_id(experiment)
            if not is_valid:
                console.print(f"[red]❌ Invalid experiment ID: {error}[/red]")
                raise typer.Exit(1)

        if iteration is not None:
            is_valid, error = validate_iteration(iteration)
            if not is_valid:
                console.print(f"[red]❌ Invalid iteration: {error}[/red]")
                raise typer.Exit(1)

        # Science-bitch integration
        if science:
            try:
                from scientific_method_tool import Hypothesis, Variable, VariableType

                from .core.dnd_scenario.science_integration import DnDScenarioScienceIntegration

                console.print(
                    Panel.fit("[bold cyan]🔬 SCIENCE-BITCH INTEGRATION[/bold cyan]", style="cyan")
                )

                # Create hypothesis
                if hypothesis:
                    # Split hypothesis into statement and prediction if format allows
                    if "|" in hypothesis:
                        parts = hypothesis.split("|", 1)
                        hypothesis_obj = Hypothesis(
                            statement=parts[0].strip(), prediction=parts[1].strip()
                        )
                    else:
                        # Use statement as both, add default prediction
                        hypothesis_obj = Hypothesis(
                            statement=hypothesis, prediction=f"Testing: {hypothesis}"
                        )
                else:
                    # Default hypothesis
                    hypothesis_obj = Hypothesis(
                        statement="Different scenario modes produce different party outcomes",
                        prediction="Encounter mode will result in higher XP gain than exploration mode",
                    )
                    hypothesis_obj.add_variable(
                        Variable(
                            name="scenario_mode",
                            type=VariableType.INDEPENDENT,
                            value=mode,
                            description="Type of scenario to run",
                        )
                    )
                    hypothesis_obj.add_variable(
                        Variable(
                            name="party_xp_gain",
                            type=VariableType.DEPENDENT,
                            value=0.0,
                            description="Total XP gained by party",
                        )
                    )

                # Initialize science integration
                science_integration = DnDScenarioScienceIntegration(realm)

                # Run iterative experiment
                console.print(
                    f"[yellow]Running {iterations} iterations with state restoration...[/yellow]"
                )
                experiment_results = science_integration.run_iterative_experiment(
                    hypothesis=hypothesis_obj,
                    mode=mode,
                    max_iterations=iterations,
                    restore_initial_state=True,
                )

                console.print("[green]✅ Experiment complete![/green]")
                console.print(f"   Experiment ID: {experiment_results['experiment_id']}")
                console.print(f"   Iterations: {len(experiment_results['iterations'])}")
                console.print(f"   Hypothesis: {experiment_results['hypothesis']}")

                # Show analysis if available
                if "analysis" in experiment_results:
                    analysis = experiment_results["analysis"]
                    console.print("\n[bold]Analysis:[/bold]")
                    if "conclusion" in analysis:
                        console.print(f"   Conclusion: {analysis['conclusion']}")
                    if "confidence" in analysis:
                        console.print(f"   Confidence: {analysis['confidence']}")

                return

            except ImportError as e:
                console.print(f"[red]❌ Science integration unavailable: {e}[/red]")
                console.print(
                    "[yellow]Install scientific_method_tool to use --science mode[/yellow]"
                )
                raise typer.Exit(1)
            except Exception as e:
                console.print(f"[red]❌ Science integration error: {e}[/red]")
                logger.exception("Error in science integration")
                raise typer.Exit(1)

        # Run scenario
        result = orchestrator.run_scenario(mode=mode, experiment_id=experiment, iteration=iteration)

        console.print("[green]✅ Scenario complete![/green]")
        console.print(f"   Mode: {result.get('mode')}")
        console.print(f"   Status: {result.get('status')}")

    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        logger.exception("Error running DnD scenario")


@app.command()
def trace(
    action: str = typer.Argument(..., help="Action: 'list' or 'show'"),
    trace_id: Optional[str] = typer.Argument(None, help="Trace ID (required for 'show' action)"),
    limit: int = typer.Option(10, "--limit", "-n", help="Number of traces to show (for 'list')"),
):
    """
    View and analyze data traces.

    Actions:
      - list: Show recent traces
      - show: Display detailed trace tree for a specific trace ID

    Examples:
      waft trace list
      waft trace list --limit 20
      waft trace show <trace-id>
    """
    from .core.tracing import TraceViewer

    viewer = TraceViewer()

    if action == "list":
        recent_traces = viewer.list_recent_traces(limit=limit)
        if not recent_traces:
            console.print("[yellow]No traces found.[/yellow]")
            return

        console.print(f"\n[bold]Recent Traces[/bold] (showing {len(recent_traces)}):\n")
        for span in recent_traces:
            summary = viewer.format_trace_summary(span)
            console.print(summary)

        console.print(f"\n[dim]Use 'waft trace show <trace-id>' to view details[/dim]")

    elif action == "show":
        if not trace_id:
            console.print("[red]Error: trace_id is required for 'show' action[/red]")
            console.print("Usage: waft trace show <trace-id>")
            raise typer.Exit(1)

        trace_tree = viewer.format_trace_tree(trace_id)
        console.print("\n" + trace_tree + "\n")

    else:
        console.print(f"[red]Error: Unknown action '{action}'[/red]")
        console.print("Valid actions: list, show")
        raise typer.Exit(1)


def main():
    """Entry point for the waft CLI."""
    app()


if __name__ == "__main__":
    main()
