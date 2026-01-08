"""
Analytics CLI - Command-line interface for session analytics.

Provides commands to view, analyze, and learn from historical session data.
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .session_analytics import SessionAnalytics

app = typer.Typer(name="analytics", help="Session analytics and historical analysis")
console = Console()


@app.command()
def sessions(
    days: int = typer.Option(30, "--days", "-d", help="Number of days to show"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category"),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum sessions to show"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path"),
):
    """List recent sessions."""
    project_path = Path(path) if path else Path.cwd()
    analytics = SessionAnalytics(project_path)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    sessions = analytics.get_sessions(
        start_date=start_date,
        end_date=end_date,
        category=category,
        limit=limit
    )
    
    if not sessions:
        console.print("[yellow]No sessions found[/yellow]")
        return
    
    table = Table(title=f"Sessions (Last {days} days)")
    table.add_column("Date", style="cyan")
    table.add_column("Category", style="green")
    table.add_column("Files", justify="right")
    table.add_column("Lines", justify="right")
    table.add_column("ID", style="dim")
    
    for session in sessions:
        date_str = session.timestamp[:10] if len(session.timestamp) >= 10 else session.timestamp
        table.add_row(
            date_str,
            session.approach_category or "uncategorized",
            str(session.files_created + session.files_modified),
            f"{session.net_lines:+,}",
            session.session_id[:12],
        )
    
    console.print(table)


@app.command()
def trends(
    days: int = typer.Option(30, "--days", "-d", help="Number of days to analyze"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path"),
):
    """Show productivity trends."""
    project_path = Path(path) if path else Path.cwd()
    analytics = SessionAnalytics(project_path)
    
    trends_data = analytics.analyze_productivity_trends(days=days)
    
    if "error" in trends_data:
        console.print(f"[red]{trends_data['error']}[/red]")
        return
    
    console.print(f"\n[bold cyan]📊 Productivity Trends (Last {days} days)[/bold cyan]\n")
    
    # Summary table
    summary_table = Table(show_header=False, box=None)
    summary_table.add_column("Metric", style="bold")
    summary_table.add_column("Value", style="green")
    
    summary_table.add_row("Total Sessions", str(trends_data["total_sessions"]))
    summary_table.add_row("Total Files", f"{trends_data['total_files']:,}")
    summary_table.add_row("Total Lines", f"{trends_data['total_lines']:+,}")
    summary_table.add_row("Avg Files/Session", f"{trends_data['avg_files_per_session']:.1f}")
    summary_table.add_row("Avg Lines/Session", f"{trends_data['avg_lines_per_session']:.1f}")
    
    console.print(summary_table)
    
    # By category
    if trends_data.get("by_category"):
        console.print("\n[bold]By Category:[/bold]")
        cat_table = Table()
        cat_table.add_column("Category", style="cyan")
        cat_table.add_column("Sessions", justify="right")
        cat_table.add_column("Files", justify="right")
        cat_table.add_column("Lines", justify="right")
        
        for category, data in sorted(trends_data["by_category"].items(), key=lambda x: x[1]["count"], reverse=True):
            cat_table.add_row(
                category,
                str(data["count"]),
                f"{data['files']:,}",
                f"{data['lines']:+,}",
            )
        
        console.print(cat_table)


@app.command()
def drift(
    days: int = typer.Option(30, "--days", "-d", help="Number of days to analyze"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path"),
):
    """Analyze prompt drift over time."""
    project_path = Path(path) if path else Path.cwd()
    analytics = SessionAnalytics(project_path)
    
    drift_data = analytics.analyze_prompt_drift(days=days)
    
    if "error" in drift_data:
        console.print(f"[red]{drift_data['error']}[/red]")
        return
    
    console.print(f"\n[bold cyan]🔄 Prompt Drift Analysis (Last {days} days)[/bold cyan]\n")
    console.print(f"Unique Prompts: {drift_data['unique_prompts']}")
    
    if drift_data.get("by_prompt"):
        table = Table()
        table.add_column("Prompt Signature", style="dim", width=20)
        table.add_column("Sessions", justify="right")
        table.add_column("Avg Files", justify="right")
        table.add_column("Avg Lines", justify="right")
        table.add_column("Success Rate", justify="right")
        
        for prompt, data in sorted(drift_data["by_prompt"].items(), key=lambda x: x[1]["count"], reverse=True)[:10]:
            table.add_row(
                prompt[:16] + "...",
                str(data["count"]),
                f"{data['avg_files']:.1f}",
                f"{data['avg_lines']:.1f}",
                f"{data['success_rate']:.1%}",
            )
        
        console.print(table)


@app.command()
def compare(
    category1: str = typer.Argument(..., help="First category"),
    category2: str = typer.Argument(..., help="Second category"),
    days: int = typer.Option(30, "--days", "-d", help="Number of days to analyze"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path"),
):
    """Compare two approach categories."""
    project_path = Path(path) if path else Path.cwd()
    analytics = SessionAnalytics(project_path)
    
    comparison = analytics.compare_approaches(category1, category2, days=days)
    
    console.print(f"\n[bold cyan]⚖️  Comparison: {category1} vs {category2}[/bold cyan]\n")
    
    table = Table()
    table.add_column("Metric", style="bold")
    table.add_column(category1, style="green", justify="right")
    table.add_column(category2, style="blue", justify="right")
    
    for metric in ["count", "avg_files", "avg_lines", "success_rate"]:
        val1 = comparison.get(category1, {}).get(metric, 0)
        val2 = comparison.get(category2, {}).get(metric, 0)
        
        if metric == "success_rate":
            val1 = f"{val1:.1%}" if val1 else "N/A"
            val2 = f"{val2:.1%}" if val2 else "N/A"
        else:
            val1 = f"{val1:.1f}" if isinstance(val1, float) else str(val1) if val1 else "N/A"
            val2 = f"{val2:.1f}" if isinstance(val2, float) else str(val2) if val2 else "N/A"
        
        table.add_row(metric.replace("_", " ").title(), val1, val2)
    
    console.print(table)


@app.command()
def chains(
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path"),
):
    """Show iteration chains."""
    project_path = Path(path) if path else Path.cwd()
    analytics = SessionAnalytics(project_path)
    
    chains = analytics.get_iteration_chains()
    
    if not chains:
        console.print("[yellow]No iteration chains found[/yellow]")
        return
    
    console.print(f"\n[bold cyan]🔗 Iteration Chains[/bold cyan]\n")
    
    for chain_id, session_ids in chains.items():
        console.print(f"[bold]{chain_id}[/bold]: {len(session_ids)} sessions")
        for sid in session_ids[:5]:
            console.print(f"  • {sid}")
        if len(session_ids) > 5:
            console.print(f"  ... and {len(session_ids) - 5} more")


if __name__ == "__main__":
    app()
