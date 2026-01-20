"""
Pyrite CLI Interface
====================

Command-line interface for interacting with The Steward, the God of Work Efforts.
"""

import asyncio
import json
from pathlib import Path
from typing import Optional

import click
import typer

from ..pyrite import Pyrite, EvolutionaryStrategy, WorkEffortStatus, get_pyrite

# Create typer app for commands that use typer
app = typer.Typer()


@click.group()
@click.option("--work-efforts-path", default="_work_efforts", type=click.Path(exists=False))
@click.option("--pyrite-path", default="_pyrite", type=click.Path(exists=False))
@click.pass_context
def pyrite_cli(ctx, work_efforts_path, pyrite_path):
    """The Steward - The God of Work Efforts."""
    ctx.ensure_object(dict)
    ctx.obj["pyrite"] = get_pyrite(Path(work_efforts_path), Path(pyrite_path))


@app.command()
def think(
    work_efforts_path: str = typer.Option("_work_efforts", "--work-efforts-path"),
    pyrite_path: str = typer.Option("_pyrite", "--pyrite-path")
):
    """Initialize cognitive systems (/think ability)."""
    pyrite = get_pyrite(Path(work_efforts_path), Path(pyrite_path))
    result = pyrite.execute_ability("/think")
    typer.echo(json.dumps(result, indent=2))


@pyrite_cli.command()
@click.argument("we_id")
@click.option("--strategy", default="adaptive", type=click.Choice(["conservative", "aggressive", "adaptive", "exploratory"]))
@click.option("--num-variants", default=5, type=int)
@click.pass_context
def evolve(ctx, we_id, strategy, num_variants):
    """Initiate evolutionary cycle for a work effort (/evolve ability)."""
    pyrite = ctx.obj["pyrite"]
    result = pyrite.execute_ability("/evolve", we_id, strategy, num_variants)
    click.echo(json.dumps(result, indent=2))


@app.command()
def monitor(
    we_id: Optional[str] = typer.Argument(None),
    work_efforts_path: str = typer.Option("_work_efforts", "--work-efforts-path"),
    pyrite_path: str = typer.Option("_pyrite", "--pyrite-path")
):
    """Monitor work efforts (/monitor ability)."""
    pyrite = get_pyrite(Path(work_efforts_path), Path(pyrite_path))
    result = pyrite.execute_ability("/monitor", we_id)
    typer.echo(json.dumps(result, indent=2))


@pyrite_cli.command()
@click.pass_context
def organize(ctx):
    """Organize work efforts (/organize ability)."""
    pyrite = ctx.obj["pyrite"]
    result = pyrite.execute_ability("/organize")
    click.echo(json.dumps(result, indent=2))


@app.command()
def lock(
    we_id: str,
    lock_id: str,
    work_efforts_path: str = typer.Option("_work_efforts", "--work-efforts-path"),
    pyrite_path: str = typer.Option("_pyrite", "--pyrite-path")
):
    """Lock a work effort (/lock ability)."""
    pyrite = get_pyrite(Path(work_efforts_path), Path(pyrite_path))
    result = pyrite.execute_ability("/lock", we_id, lock_id)
    typer.echo(json.dumps(result, indent=2))


@app.command()
def unlock(
    we_id: str,
    lock_id: str,
    work_efforts_path: str = typer.Option("_work_efforts", "--work-efforts-path"),
    pyrite_path: str = typer.Option("_pyrite", "--pyrite-path")
):
    """Unlock a work effort (/unlock ability)."""
    pyrite = get_pyrite(Path(work_efforts_path), Path(pyrite_path))
    result = pyrite.execute_ability("/unlock", we_id, lock_id)
    typer.echo(json.dumps(result, indent=2))


@app.command()
def status(
    work_efforts_path: str = typer.Option("_work_efforts", "--work-efforts-path"),
    pyrite_path: str = typer.Option("_pyrite", "--pyrite-path")
):
    """Get Pyrite status (/status ability)."""
    pyrite = get_pyrite(Path(work_efforts_path), Path(pyrite_path))
    result = pyrite.execute_ability("/status")
    typer.echo(json.dumps(result, indent=2))


@app.command()
def secrets(
    work_efforts_path: str = typer.Option("_work_efforts", "--work-efforts-path"),
    pyrite_path: str = typer.Option("_pyrite", "--pyrite-path")
):
    """List secrets (metadata only) (/secrets ability)."""
    pyrite = get_pyrite_instance(work_efforts_path, pyrite_path)
    result = pyrite.execute_ability("/secrets")
    typer.echo(json.dumps(result, indent=2))


@pyrite_cli.command()
@click.argument("data", type=str)
@click.option("--metadata", type=str, help="JSON metadata")
@click.pass_context
def create_secret(ctx, data, metadata):
    """Create a secret that even Pyrite cannot directly access."""
    pyrite = ctx.obj["pyrite"]
    
    try:
        data_dict = json.loads(data)
    except json.JSONDecodeError:
        data_dict = {"data": data}
    
    metadata_dict = None
    if metadata:
        try:
            metadata_dict = json.loads(metadata)
        except json.JSONDecodeError:
            metadata_dict = {"note": metadata}
    
    secret_id = pyrite.create_secret(data_dict, metadata_dict)
    click.echo(f"Secret created: {secret_id}")
    click.echo(json.dumps(pyrite.get_secret_metadata(secret_id), indent=2))


@app.command()
def get_work_effort(
    we_id: str,
    work_efforts_path: str = typer.Option("_work_efforts", "--work-efforts-path"),
    pyrite_path: str = typer.Option("_pyrite", "--pyrite-path")
):
    """Get work effort details."""
    pyrite = get_pyrite(Path(work_efforts_path), Path(pyrite_path))
    node = pyrite.get_work_effort(we_id)
    
    if node:
        typer.echo(json.dumps({
            "we_id": node.we_id,
            "title": node.title,
            "status": node.status.value,
            "created": node.created.isoformat(),
            "updated": node.updated.isoformat(),
            "parent": node.parent,
            "children": node.children,
            "fitness": node.fitness,
            "generation": node.generation,
            "lineage": node.lineage,
            "metadata": node.metadata
        }, indent=2))
    else:
        typer.echo(f"Work effort not found: {we_id}")


@app.command()
def set_status(
    we_id: str,
    status: str = typer.Argument(..., help="Status: dormant, active, locked, evolving, completed, archived, corrupted"),
    work_efforts_path: str = typer.Option("_work_efforts", "--work-efforts-path"),
    pyrite_path: str = typer.Option("_pyrite", "--pyrite-path")
):
    """Set work effort status."""
    pyrite = get_pyrite_instance(work_efforts_path, pyrite_path)
    new_status = WorkEffortStatus(status)
    success = pyrite.update_work_effort_status(we_id, new_status)
    
    if success:
        typer.echo(f"Status updated: {we_id} -> {status}")
    else:
        typer.echo(f"Failed to update status: {we_id}")


@app.command()
def get_children(
    we_id: str,
    work_efforts_path: str = typer.Option("_work_efforts", "--work-efforts-path"),
    pyrite_path: str = typer.Option("_pyrite", "--pyrite-path")
):
    """Get children of a work effort."""
    pyrite = get_pyrite(Path(work_efforts_path), Path(pyrite_path))
    children = pyrite.get_children(we_id)
    
    result = [
        {
            "we_id": child.we_id,
            "title": child.title,
            "status": child.status.value
        }
        for child in children
    ]
    typer.echo(json.dumps(result, indent=2))


@app.command()
def get_ancestors(
    we_id: str,
    work_efforts_path: str = typer.Option("_work_efforts", "--work-efforts-path"),
    pyrite_path: str = typer.Option("_pyrite", "--pyrite-path")
):
    """Get ancestors of a work effort."""
    pyrite = get_pyrite(Path(work_efforts_path), Path(pyrite_path))
    ancestors = pyrite.get_ancestors(we_id)
    
    result = [
        {
            "we_id": ancestor.we_id,
            "title": ancestor.title,
            "status": ancestor.status.value
        }
        for ancestor in ancestors
    ]
    typer.echo(json.dumps(result, indent=2))


@app.command()
def evolution_history(
    we_id: str,
    work_efforts_path: str = typer.Option("_work_efforts", "--work-efforts-path"),
    pyrite_path: str = typer.Option("_pyrite", "--pyrite-path")
):
    """Get evolutionary history for a work effort."""
    pyrite = get_pyrite(Path(work_efforts_path), Path(pyrite_path))
    history = pyrite.get_evolutionary_history(we_id)
    
    result = [
        {
            "cycle_id": cycle.cycle_id,
            "generation": cycle.generation,
            "strategy": cycle.strategy.value,
            "variants": len(cycle.variants),
            "selected_variant": cycle.selected_variant,
            "fitness": cycle.fitness_scores.get(cycle.selected_variant, 0.0) if cycle.selected_variant else None,
            "started": cycle.started.isoformat(),
            "completed": cycle.completed.isoformat() if cycle.completed else None
        }
        for cycle in history
    ]
    typer.echo(json.dumps(result, indent=2))


@app.command()
def personality(
    work_efforts_path: str = typer.Option("_work_efforts", "--work-efforts-path"),
    pyrite_path: str = typer.Option("_pyrite", "--pyrite-path")
):
    """Get Pyrite's personality summary."""
    pyrite = get_pyrite(Path(work_efforts_path), Path(pyrite_path))
    result = pyrite.get_personality_summary()
    typer.echo(json.dumps(result, indent=2))


if __name__ == "__main__":
    app()
