"""
Refinement Detector Demo

Demonstrates detecting polish opportunities without redesign.
Refinement = buffing out cracks while keeping essence intact.
"""

from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from waft.core.self_engineering import RefinementDetector, Severity

console = Console()

def main():
    console.print(Panel.fit(
        "[bold cyan]REFINEMENT DETECTOR DEMO[/bold cyan]\n"
        "[dim]Finding polish opportunities without redesign[/dim]",
        border_style="cyan"
    ))
    
    # Initialize detector
    console.print("\n[yellow]→[/yellow] Initializing refinement detector...")
    detector = RefinementDetector()
    console.print("[green]✓[/green] Refinement detector ready")
    
    # Example code with rough edges
    example_code = '''
def calc(x, y):
    """Calculate something."""
    try:
        return x/y
    except:
        return None

def processData(input_data):
    result = []
    for item in input_data:
        if item > 0:
            result.append(item * 2)
    return result

class MyClass:
    def __init__(self):
        self.value = 0
    
    def _helper_method(self):
        print("Helper")
        return True
'''
    
    console.print("\n[yellow]→[/yellow] Analyzing example code for refinement opportunities...")
    opportunities = detector.detect_rough_edges(example_code)
    console.print(f"[green]✓[/green] Found {len(opportunities)} refinement opportunity/opportunities")
    
    # Display results
    if opportunities:
        table = Table(title="Refinement Opportunities", show_header=True, header_style="bold magenta")
        table.add_column("Type", style="cyan")
        table.add_column("Severity", style="yellow")
        table.add_column("Description", style="white")
        table.add_column("Line", style="dim")
        
        for opp in opportunities:
            table.add_row(
                opp.type,
                opp.severity.value,
                opp.description,
                str(opp.line_number) if opp.line_number else "N/A"
            )
        
        console.print("\n")
        console.print(table)
        
        # Summary by type
        console.print("\n[bold]Summary by Type:[/bold]")
        type_counts = {}
        for opp in opportunities:
            type_counts[opp.type] = type_counts.get(opp.type, 0) + 1
        
        for opp_type, count in sorted(type_counts.items()):
            console.print(f"  [cyan]{opp_type}[/cyan]: {count}")
        
        # Show what refinement would do
        console.print("\n[bold]What Refinement Would Do:[/bold]")
        console.print("  [green]✓[/green] Fix cracks (bare except → specific exception)")
        console.print("  [green]✓[/green] Add polish (type hints, better naming)")
        console.print("  [green]✓[/green] Remove dead code (unused _helper_method)")
        console.print("  [green]✓[/green] Standardize patterns (naming conventions)")
        console.print("\n[bold]What Refinement Would NOT Do:[/bold]")
        console.print("  [red]✗[/red] Change architecture")
        console.print("  [red]✗[/red] Restructure code")
        console.print("  [red]✗[/red] Change APIs")
        console.print("  [red]✗[/red] Break functionality")
    else:
        console.print("[green]✓[/green] No refinement opportunities found - code is polished!")
    
    console.print("\n[bold green]✓ Demo Complete![/bold green]")
    console.print("\n[dim]Refinement = Polish without redesign. Buffing cracks while keeping essence intact.[/dim]")

if __name__ == "__main__":
    main()
