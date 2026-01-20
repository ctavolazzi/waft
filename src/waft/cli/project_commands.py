"""
Project Commands - CLI interface for project management.
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..core.projects import Milestone, ProgressEntry, ProjectManager, ProjectStatus
from ..logging import get_logger
from ..utils import resolve_project_path

logger = get_logger(__name__)

app = typer.Typer(
    name="project",
    help="Manage long-term projects",
    add_completion=False,
)

console = Console()


@app.command("create")
def create_project(
    title: str = typer.Argument(..., help="Project title"),
    description: str = typer.Option("", "--description", "-d", help="Project description"),
    tags: str | None = typer.Option(None, "--tags", "-t", help="Comma-separated tags"),
    status: str = typer.Option(
        "planning", "--status", "-s", help="Initial status (planning, active, paused)"
    ),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Create a new project."""
    try:
        project_path = resolve_project_path(path)
    except ValueError as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(1)

    try:
        manager = ProjectManager(project_path)

        # Parse tags
        tag_list = []
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]

        # Parse status
        try:
            project_status = ProjectStatus(status.lower())
        except ValueError:
            console.print(f"[bold red]❌ Invalid status: {status}[/bold red]")
            console.print(
                "[dim]Valid statuses: planning, active, paused, completed, archived[/dim]"
            )
            raise typer.Exit(1)

        # Create project
        project = manager.create_project(
            title=title, description=description, tags=tag_list, status=project_status
        )

        console.print("\n[bold green]✅ Project created[/bold green]")
        console.print(f"[dim]ID:[/dim] {project.project_id}")
        console.print(f"[dim]Title:[/dim] {project.title}")
        console.print(f"[dim]Status:[/dim] {project.status.value}")
        if project.tags:
            console.print(f"[dim]Tags:[/dim] {', '.join(project.tags)}")

    except ValueError as e:
        console.print(f"[bold red]❌ Validation error: {e}[/bold red]")
        raise typer.Exit(1)
    except OSError as e:
        console.print(f"[bold red]❌ File system error: {e}[/bold red]")
        raise typer.Exit(1)
    except Exception as e:
        logger.exception("Failed to create project")
        console.print(f"[bold red]❌ Failed to create project: {e}[/bold red]")
        raise typer.Exit(1)


@app.command("list")
def list_projects(
    status: str | None = typer.Option(None, "--status", "-s", help="Filter by status"),
    tags: str | None = typer.Option(None, "--tags", "-t", help="Comma-separated tags to filter"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """List all projects."""
    try:
        project_path = resolve_project_path(path)
    except ValueError as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(1)

    try:
        manager = ProjectManager(project_path)

        # Parse filters
        status_filter = None
        if status:
            try:
                status_filter = ProjectStatus(status.lower())
            except ValueError:
                console.print(f"[bold red]❌ Invalid status: {status}[/bold red]")
                raise typer.Exit(1)

        tag_list = None
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]

        # List projects
        projects = manager.list_projects(status=status_filter, tags=tag_list)

        if not projects:
            console.print("[yellow]No projects found[/yellow]")
            return

        # Display table
        table = Table(title="Projects", show_header=True, header_style="bold cyan")
        table.add_column("ID", style="dim")
        table.add_column("Title", style="bold")
        table.add_column("Status")
        table.add_column("Progress", justify="right")
        table.add_column("Tags")
        table.add_column("Updated", style="dim")

        for project in projects:
            # Format progress
            progress_str = f"{project.progress_percent:.1f}%"
            if project.progress_percent >= 100.0:
                progress_style = "green"
            elif project.progress_percent >= 50.0:
                progress_style = "yellow"
            else:
                progress_style = "dim"

            # Format status
            status_style = {
                "planning": "dim",
                "active": "green",
                "paused": "yellow",
                "completed": "bold green",
                "archived": "dim",
            }.get(project.status.value, "dim")

            # Format updated date
            try:
                from datetime import datetime

                updated = datetime.fromisoformat(project.updated_at.replace("Z", "+00:00"))
                updated_str = updated.strftime("%Y-%m-%d")
            except:
                updated_str = (
                    project.updated_at[:10] if len(project.updated_at) >= 10 else project.updated_at
                )

            table.add_row(
                project.project_id,
                project.title[:40] + "..." if len(project.title) > 40 else project.title,
                f"[{status_style}]{project.status.value}[/{status_style}]",
                f"[{progress_style}]{progress_str}[/{progress_style}]",
                ", ".join(project.tags[:3]) + ("..." if len(project.tags) > 3 else "")
                if project.tags
                else "",
                updated_str,
            )

        console.print(table)
        console.print(f"\n[dim]Total: {len(projects)} project(s)[/dim]")

    except Exception as e:
        logger.exception("Failed to list projects")
        console.print(f"[bold red]❌ Failed to list projects: {e}[/bold red]")
        raise typer.Exit(1)


@app.command("show")
def show_project(
    project_id: str = typer.Argument(..., help="Project ID"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Show project details."""
    try:
        project_path = resolve_project_path(path)
    except ValueError as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(1)

    try:
        manager = ProjectManager(project_path)
        project = manager.get_project(project_id)

        if not project:
            console.print(f"[bold red]❌ Project not found: {project_id}[/bold red]")
            raise typer.Exit(1)

        # Display project details
        console.print(f"\n[bold cyan]{project.title}[/bold cyan]")
        console.print(f"[dim]ID:[/dim] {project.project_id}")
        console.print(f"[dim]Status:[/dim] {project.status.value}")
        console.print(f"[dim]Progress:[/dim] {project.progress_percent:.1f}%")
        console.print(
            f"[dim]Created:[/dim] {project.created_at[:19] if len(project.created_at) >= 19 else project.created_at}"
        )
        console.print(
            f"[dim]Updated:[/dim] {project.updated_at[:19] if len(project.updated_at) >= 19 else project.updated_at}"
        )

        if project.tags:
            console.print(f"[dim]Tags:[/dim] {', '.join(project.tags)}")

        if project.description:
            console.print("\n[bold]Description:[/bold]")
            console.print(Panel(project.description, border_style="dim"))

        if project.milestones:
            console.print(f"\n[bold]Milestones:[/bold] ({len(project.milestones)})")
            for milestone in project.milestones[:10]:  # Show first 10
                status_icon = "✅" if milestone.completed else "⏳"
                console.print(f"  {status_icon} {milestone.title}")
            if len(project.milestones) > 10:
                console.print(f"  [dim]... and {len(project.milestones) - 10} more[/dim]")

        if project.progress_entries:
            console.print(
                f"\n[bold]Recent Progress:[/bold] ({len(project.progress_entries)} entries)"
            )
            for entry in project.progress_entries[-5:]:  # Show last 5
                delta_str = (
                    f"+{entry.progress_delta:.1f}%"
                    if entry.progress_delta >= 0
                    else f"{entry.progress_delta:.1f}%"
                )
                console.print(
                    f"  {entry.timestamp[:19]}: {delta_str} - {entry.notes[:50] if entry.notes else 'No notes'}"
                )

        if project.related_work_efforts:
            console.print("\n[bold]Related Work Efforts:[/bold]")
            for we_id in project.related_work_efforts:
                console.print(f"  - {we_id}")

        if project.notes:
            console.print("\n[bold]Notes:[/bold]")
            console.print(
                Panel(
                    project.notes[:500] + ("..." if len(project.notes) > 500 else ""),
                    border_style="dim",
                )
            )

    except ValueError as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(1)
    except Exception as e:
        logger.exception("Failed to show project")
        console.print(f"[bold red]❌ Failed to show project: {e}[/bold red]")
        raise typer.Exit(1)


@app.command("update")
def update_project(
    project_id: str = typer.Argument(..., help="Project ID"),
    title: str | None = typer.Option(None, "--title", "-t", help="Update title"),
    description: str | None = typer.Option(None, "--description", "-d", help="Update description"),
    status: str | None = typer.Option(None, "--status", "-s", help="Update status"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Update project."""
    try:
        project_path = resolve_project_path(path)
    except ValueError as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(1)

    try:
        manager = ProjectManager(project_path)
        project = manager.get_project(project_id)

        if not project:
            console.print(f"[bold red]❌ Project not found: {project_id}[/bold red]")
            raise typer.Exit(1)

        # Update fields
        if title is not None:
            project.title = title
        if description is not None:
            project.description = description
        if status is not None:
            try:
                project.status = ProjectStatus(status.lower())
            except ValueError:
                console.print(f"[bold red]❌ Invalid status: {status}[/bold red]")
                raise typer.Exit(1)

        # Save updates
        manager.update_project(project)

        console.print(f"[bold green]✅ Project updated: {project_id}[/bold green]")

    except ValueError as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(1)
    except Exception as e:
        logger.exception("Failed to update project")
        console.print(f"[bold red]❌ Failed to update project: {e}[/bold red]")
        raise typer.Exit(1)


@app.command("progress")
def update_progress(
    project_id: str = typer.Argument(..., help="Project ID"),
    percent: float = typer.Option(..., "--percent", "-p", help="Progress percentage (0.0-100.0)"),
    notes: str = typer.Option("", "--notes", "-n", help="Progress notes"),
    work_effort: str | None = typer.Option(
        None, "--work-effort", "-w", help="Related work effort ID"
    ),
    duration: float | None = typer.Option(None, "--duration", help="Session duration in minutes"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Update project progress."""
    try:
        project_path = resolve_project_path(path)
    except ValueError as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(1)

    try:
        manager = ProjectManager(project_path)
        project = manager.get_project(project_id)

        if not project:
            console.print(f"[bold red]❌ Project not found: {project_id}[/bold red]")
            raise typer.Exit(1)

        # Calculate progress delta
        old_progress = project.progress_percent
        new_progress = percent
        progress_delta = new_progress - old_progress

        # Create progress entry
        from datetime import datetime

        entry = ProgressEntry(
            entry_id=f"entry_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now().isoformat(),
            progress_delta=progress_delta,
            notes=notes,
            work_effort_id=work_effort,
            session_duration=duration,
        )

        # Update project
        project.progress_percent = new_progress
        project.progress_entries.append(entry)

        # Keep only last N entries
        if len(project.progress_entries) > manager.MAX_PROGRESS_ENTRIES:
            project.progress_entries = project.progress_entries[-manager.MAX_PROGRESS_ENTRIES :]

        # Save
        manager.update_project(project)

        console.print(
            f"[bold green]✅ Progress updated: {old_progress:.1f}% → {new_progress:.1f}%[/bold green]"
        )
        if progress_delta != 0:
            delta_str = (
                f"+{progress_delta:.1f}%" if progress_delta > 0 else f"{progress_delta:.1f}%"
            )
            console.print(f"[dim]Change: {delta_str}[/dim]")

    except ValueError as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(1)
    except Exception as e:
        logger.exception("Failed to update progress")
        console.print(f"[bold red]❌ Failed to update progress: {e}[/bold red]")
        raise typer.Exit(1)


@app.command("status")
def project_status(
    project_id: str = typer.Argument(..., help="Project ID"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Quick project status check."""
    try:
        project_path = resolve_project_path(path)
    except ValueError as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(1)

    try:
        manager = ProjectManager(project_path)
        project = manager.get_project(project_id)

        if not project:
            console.print(f"[bold red]❌ Project not found: {project_id}[/bold red]")
            raise typer.Exit(1)

        # Quick status display
        status_icon = {
            "planning": "📋",
            "active": "🚀",
            "paused": "⏸️",
            "completed": "✅",
            "archived": "📦",
        }.get(project.status.value, "❓")

        console.print(f"\n{status_icon} [bold]{project.title}[/bold]")
        console.print(f"[dim]Status:[/dim] {project.status.value}")
        console.print(f"[dim]Progress:[/dim] {project.progress_percent:.1f}%")
        console.print(
            f"[dim]Milestones:[/dim] {len(project.milestones)} ({sum(1 for m in project.milestones if m.completed)} completed)"
        )
        console.print(f"[dim]Progress Entries:[/dim] {len(project.progress_entries)}")

    except Exception as e:
        logger.exception("Failed to get project status")
        console.print(f"[bold red]❌ Failed to get project status: {e}[/bold red]")
        raise typer.Exit(1)


@app.command("milestone")
def milestone_command(
    action: str = typer.Argument(..., help="Action: create, complete, list"),
    project_id: str = typer.Argument(..., help="Project ID"),
    milestone_id: str | None = typer.Argument(None, help="Milestone ID (for complete)"),
    title: str | None = typer.Option(None, "--title", "-t", help="Milestone title (for create)"),
    description: str | None = typer.Option(
        None, "--description", "-d", help="Milestone description (for create)"
    ),
    target_date: str | None = typer.Option(
        None, "--target-date", help="Target date (ISO format, for create)"
    ),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Manage project milestones."""
    try:
        project_path = resolve_project_path(path)
    except ValueError as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(1)

    try:
        manager = ProjectManager(project_path)
        project = manager.get_project(project_id)

        if not project:
            console.print(f"[bold red]❌ Project not found: {project_id}[/bold red]")
            raise typer.Exit(1)

        if action == "create":
            if not title:
                console.print("[bold red]❌ Title required for milestone creation[/bold red]")
                raise typer.Exit(1)

            from datetime import datetime

            milestone = Milestone(
                milestone_id=f"milestone_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                title=title,
                description=description or "",
                target_date=target_date,
                completed=False,
            )

            project.milestones.append(milestone)
            manager.update_project(project)

            console.print(
                f"[bold green]✅ Milestone created: {milestone.milestone_id}[/bold green]"
            )
            console.print(f"[dim]Title:[/dim] {milestone.title}")

        elif action == "complete":
            if not milestone_id:
                console.print("[bold red]❌ Milestone ID required[/bold red]")
                raise typer.Exit(1)

            milestone = next(
                (m for m in project.milestones if m.milestone_id == milestone_id), None
            )
            if not milestone:
                console.print(f"[bold red]❌ Milestone not found: {milestone_id}[/bold red]")
                raise typer.Exit(1)

            if milestone.completed:
                console.print("[yellow]⚠️  Milestone already completed[/yellow]")
            else:
                from datetime import datetime

                milestone.completed = True
                milestone.completed_at = datetime.now().isoformat()
                manager.update_project(project)
                console.print(f"[bold green]✅ Milestone completed: {milestone.title}[/bold green]")

        elif action == "list":
            if not project.milestones:
                console.print("[yellow]No milestones found[/yellow]")
            else:
                table = Table(
                    title=f"Milestones for {project.title}",
                    show_header=True,
                    header_style="bold cyan",
                )
                table.add_column("ID", style="dim")
                table.add_column("Title", style="bold")
                table.add_column("Status")
                table.add_column("Target Date", style="dim")

                for milestone in project.milestones:
                    status = (
                        "[green]✅ Completed[/green]"
                        if milestone.completed
                        else "[yellow]⏳ Pending[/yellow]"
                    )
                    target = milestone.target_date[:10] if milestone.target_date else "—"
                    table.add_row(milestone.milestone_id, milestone.title, status, target)

                console.print(table)
                completed = sum(1 for m in project.milestones if m.completed)
                console.print(
                    f"\n[dim]Progress: {completed}/{len(project.milestones)} completed[/dim]"
                )

        else:
            console.print(f"[bold red]❌ Invalid action: {action}[/bold red]")
            console.print("[dim]Valid actions: create, complete, list[/dim]")
            raise typer.Exit(1)

    except ValueError as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(1)
    except Exception as e:
        logger.exception("Failed to manage milestone")
        console.print(f"[bold red]❌ Failed to manage milestone: {e}[/bold red]")
        raise typer.Exit(1)


@app.command("link")
def link_work_effort(
    project_id: str = typer.Argument(..., help="Project ID"),
    work_effort_id: str = typer.Argument(..., help="Work effort ID to link"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Link a work effort to a project."""
    try:
        project_path = resolve_project_path(path)
    except ValueError as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(1)

    try:
        manager = ProjectManager(project_path)
        project = manager.get_project(project_id)

        if not project:
            console.print(f"[bold red]❌ Project not found: {project_id}[/bold red]")
            raise typer.Exit(1)

        if work_effort_id in project.related_work_efforts:
            console.print(f"[yellow]⚠️  Work effort already linked: {work_effort_id}[/yellow]")
        else:
            project.related_work_efforts.append(work_effort_id)
            manager.update_project(project)
            console.print(f"[bold green]✅ Linked work effort: {work_effort_id}[/bold green]")

    except ValueError as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(1)
    except Exception as e:
        logger.exception("Failed to link work effort")
        console.print(f"[bold red]❌ Failed to link work effort: {e}[/bold red]")
        raise typer.Exit(1)


@app.command("unlink")
def unlink_work_effort(
    project_id: str = typer.Argument(..., help="Project ID"),
    work_effort_id: str = typer.Argument(..., help="Work effort ID to unlink"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Unlink a work effort from a project."""
    try:
        project_path = resolve_project_path(path)
    except ValueError as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(1)

    try:
        manager = ProjectManager(project_path)
        project = manager.get_project(project_id)

        if not project:
            console.print(f"[bold red]❌ Project not found: {project_id}[/bold red]")
            raise typer.Exit(1)

        if work_effort_id not in project.related_work_efforts:
            console.print(f"[yellow]⚠️  Work effort not linked: {work_effort_id}[/yellow]")
        else:
            project.related_work_efforts.remove(work_effort_id)
            manager.update_project(project)
            console.print(f"[bold green]✅ Unlinked work effort: {work_effort_id}[/bold green]")

    except ValueError as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(1)
    except Exception as e:
        logger.exception("Failed to unlink work effort")
        console.print(f"[bold red]❌ Failed to unlink work effort: {e}[/bold red]")
        raise typer.Exit(1)
