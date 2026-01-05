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
from .core.gamification import GamificationManager
from .core.github import GitHubManager
from .utils import resolve_project_path, validate_waft_project
from .cli.epistemic_display import (
    get_moon_phase,
    format_epistemic_summary,
    create_epistemic_dashboard,
)
from .cli.hud import render_hud

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

    # Award insight for creating project
    gamification = GamificationManager(project_path)
    insight_result = gamification.award_insight(50.0, reason="Created new project")
    
    # Check for achievements
    stats = gamification.get_stats()
    newly_unlocked = gamification.check_achievements(stats)
    
    # Check for First Build achievement
    if gamification.unlock_achievement("first_build", "🌱 First Build"):
        newly_unlocked.append("first_build")
        console.print("[bold green]🏆 Achievement Unlocked: 🌱 First Build[/bold green]")
    
    # Show level up notification
    if insight_result["level_up"]:
        console.print(f"[bold cyan]🎉 Level Up! Level {insight_result['old_level']} → {insight_result['new_level']}[/bold cyan]")
    
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

    # Update integrity based on verification result
    gamification = GamificationManager(project_path)
    if all_valid:
        gamification.restore_integrity(2.0, reason="Project verification passed")
    else:
        gamification.damage_integrity(10.0, reason="Project verification failed")

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
        project_name = project_info.get("name", "Unknown")
        project_version = project_info.get("version", "Unknown")
        table.add_row("Project Name", project_name)
        table.add_row("Version", project_version)
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


# Empirica command groups
session_app = typer.Typer(help="Session management commands")
finding_app = typer.Typer(help="Finding logging commands")
unknown_app = typer.Typer(help="Unknown logging commands")
goal_app = typer.Typer(help="Goal management commands")
github_app = typer.Typer(help="GitHub integration commands")
journal_app = typer.Typer(help="Development journal commands")

app.add_typer(session_app, name="session")
app.add_typer(finding_app, name="finding")
app.add_typer(unknown_app, name="unknown")
app.add_typer(goal_app, name="goal")
app.add_typer(github_app, name="github")
app.add_typer(journal_app, name="journal")


@session_app.command("create")
def session_create(
    ai_id: str = typer.Option("waft", "--ai-id", help="AI agent identifier"),
    session_type: str = typer.Option("development", "--type", help="Session type"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Create a new Empirica session."""
    project_path = resolve_project_path(path)
    
    console.print(f"\n[bold cyan]🌊 Waft[/bold cyan] - Creating Empirica session\n")
    
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
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Load project context and display epistemic dashboard."""
    project_path = resolve_project_path(path)
    
    console.print(f"\n[bold cyan]🌊 Waft[/bold cyan] - Loading project context\n")
    
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
    session_id: Optional[str] = typer.Option(None, "--session-id", help="Session ID"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Show current session state."""
    project_path = resolve_project_path(path)
    
    console.print(f"\n[bold cyan]🌊 Waft[/bold cyan] - Session Status\n")
    
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
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Log a finding with impact score."""
    project_path = resolve_project_path(path)
    
    console.print(f"\n[bold cyan]🌊 Waft[/bold cyan] - Logging Finding\n")
    
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
        stats = gamification.get_stats()
        # Count findings from history
        findings_count = sum(1 for h in gamification._data.get("history", []) if h.get("type") == "insight_award" and "finding" in h.get("reason", "").lower())
        if findings_count >= 50:
            if gamification.unlock_achievement("knowledge_architect", "🧠 Knowledge Architect"):
                console.print("[bold green]🏆 Achievement Unlocked: 🧠 Knowledge Architect[/bold green]")
        
        if insight_result["level_up"]:
            console.print(f"[bold cyan]🎉 Level Up! Level {insight_result['old_level']} → {insight_result['new_level']}[/bold cyan]")
        
        console.print(f"[green]✅[/green] Finding logged: [bold]{finding}[/bold]")
        console.print(f"[dim]Impact: {impact:.0%} | 🧠 +10 Insight[/dim]")
    else:
        console.print("[bold red]❌ Failed to log finding[/bold red]")
        raise typer.Exit(1)


@unknown_app.command("log")
def unknown_log(
    unknown: str = typer.Argument(..., help="Unknown description"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Log a knowledge gap."""
    project_path = resolve_project_path(path)
    
    console.print(f"\n[bold cyan]🌊 Waft[/bold cyan] - Logging Unknown\n")
    
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
    operation: Optional[str] = typer.Option(None, "--operation", help="Operation JSON description"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Run safety gate and display result."""
    project_path = resolve_project_path(path)
    
    console.print(f"\n[bold cyan]🌊 Waft[/bold cyan] - Safety Gate Check\n")
    
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
            raise typer.Exit(1)
        elif gate_result == "BRANCH":
            console.print("[yellow]⚠️  Need to investigate before proceeding[/yellow]")
        elif gate_result == "REVISE":
            console.print("[yellow]⚠️  Approach needs revision[/yellow]")
    else:
        console.print("[yellow]⚠️  Gate check unavailable[/yellow]")


@app.command()
def dashboard(
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
    integrity: float = typer.Option(100.0, "--integrity", help="Integrity value (0.0-100.0)"),
):
    """Show the Epistemic HUD with split-screen layout."""
    project_path = resolve_project_path(path)
    
    render_hud(project_path, integrity=integrity)


@app.command()
def assess(
    session_id: Optional[str] = typer.Option(None, "--session-id", help="Session ID"),
    history: bool = typer.Option(False, "--history", help="Include historical data"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Show detailed epistemic assessment."""
    project_path = resolve_project_path(path)
    
    console.print(f"\n[bold cyan]🌊 Waft[/bold cyan] - Epistemic Assessment\n")
    
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
            console.print(f"[bold cyan]🎉 Level Up! Level {insight_result['old_level']} → {insight_result['new_level']}[/bold cyan]")
        
        from .cli.epistemic_display import format_epistemic_state
        panel = format_epistemic_state(state)
        console.print(panel)
        
        integrity = gamification.integrity
        insight = gamification.insight
        console.print(f"\n[dim]💎 Integrity: {integrity:.0f}% | 🧠 Insight: {insight:.0f} | 🧠 +25 Insight[/dim]")
    else:
        console.print("[yellow]⚠️  No assessment data available[/yellow]")


@goal_app.command("create")
def goal_create(
    objective: str = typer.Argument(..., help="Goal objective"),
    session_id: Optional[str] = typer.Option(None, "--session-id", help="Session ID"),
    scope: Optional[str] = typer.Option(None, "--scope", help="Scope JSON (breadth, duration, coordination)"),
    criteria: Optional[str] = typer.Option(None, "--criteria", help="Success criteria (comma-separated)"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Create a goal with epistemic scope."""
    project_path = resolve_project_path(path)
    
    console.print(f"\n[bold cyan]🌊 Waft[/bold cyan] - Creating Goal\n")
    
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
    else:
        console.print("[bold red]❌ Failed to create goal[/bold red]")
        raise typer.Exit(1)


@goal_app.command("list")
def goal_list(
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """List active goals."""
    project_path = resolve_project_path(path)
    
    console.print(f"\n[bold cyan]🌊 Waft[/bold cyan] - Active Goals\n")
    
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
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Show current stats (Integrity, Insight, Level, Achievements)."""
    project_path = resolve_project_path(path)
    
    console.print(f"\n[bold cyan]🌊 Waft[/bold cyan] - Stats\n")
    
    gamification = GamificationManager(project_path)
    stats = gamification.get_stats()
    
    from rich.table import Table
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Stat", style="dim", width=20)
    table.add_column("Value", width=20)
    
    table.add_row("💎 Integrity", f"{stats['integrity']:.0f}%")
    table.add_row("🧠 Insight", f"{stats['insight']:.0f}")
    table.add_row("⭐ Level", str(stats['level']))
    table.add_row("🏆 Achievements", str(stats['achievements_count']))
    
    console.print(table)
    
    # Show insight to next level
    insight_needed = gamification.get_insight_to_next_level()
    if insight_needed > 0:
        console.print(f"\n[dim]🧠 {insight_needed:.0f} Insight needed for next level[/dim]")


@app.command()
def level(
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Show level details and progress to next level."""
    project_path = resolve_project_path(path)
    
    console.print(f"\n[bold cyan]🌊 Waft[/bold cyan] - Level Details\n")
    
    gamification = GamificationManager(project_path)
    current_level = gamification.level
    current_insight = gamification.insight
    next_level = current_level + 1
    
    # Calculate insight for current and next level
    insight_for_current = (current_level - 1) ** 2 * 100 if current_level > 1 else 0
    insight_for_next = (next_level - 1) ** 2 * 100
    insight_needed = insight_for_next - current_insight
    progress = (current_insight - insight_for_current) / (insight_for_next - insight_for_current) if insight_for_next > insight_for_current else 1.0
    
    from rich.progress import Progress, BarColumn, TextColumn
    from rich.console import Group
    
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
def achievements(
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """List all achievements (locked/unlocked)."""
    project_path = resolve_project_path(path)
    
    console.print(f"\n[bold cyan]🌊 Waft[/bold cyan] - Achievements\n")
    
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


def main():
    """Entry point for the waft CLI."""
    app()


if __name__ == "__main__":
    main()

