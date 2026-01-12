"""
Self-Engineering Demo

Demonstrates the self-engineering system:
1. System tries to play itself
2. Detects when it can't
3. Diagnoses why
4. Engineers solutions
5. Iterates on itself
"""

from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.core.self_engineering import SelfEngineeringLoop
from waft.being import Being
from waft.core.dnd5e import DnD5eCharacter, DnD5eStats, DnDRoller, ArmorType
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from datetime import datetime

console = Console()


def run_tavern_scenario() -> dict:
    """
    Run tavern scenario and return execution result.
    
    This simulates trying to run the scenario - it will fail if
    interactive input is required.
    """
    try:
        # Try to import and run the evolved scenario
        from examples.tavern_scenario_evolved import (
            create_character,
            tavern_scenario_evolved,
            main as evolved_main
        )
        
        # Create a Being
        being = Being(
            being_id=f"self_eng_being_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            reality_id="self_engineering_demo",
            personality_type="analytical",
            skills={
                "perception": 30.0,
                "investigation": 40.0,
                "persuasion": 25.0,
                "intelligence": 35.0,
            }
        )
        
        # Create character
        character = create_character(being)
        
        # Run scenario
        results = tavern_scenario_evolved(being, character)
        
        return {
            "success": True,
            "fitness_gained": results.get("fitness_gained", 0.0),
            "being_id": being.being_id,
            "character_name": character.name,
            "choices_made": ["auto"],  # Being made choices automatically
            "context": {
                "being_personality": being.personality_type,
                "character_level": character.level
            }
        }
        
    except Exception as e:
        # This will catch EOFError if interactive input is required
        return {
            "success": False,
            "exception": e,
            "error": str(e),
            "error_message": str(e),
            "context": {
                "exception_type": type(e).__name__
            }
        }


def main():
    """Run self-engineering demo."""
    console.print("\n[bold bright_blue]╔════════════════════════════════════════╗[/bold bright_blue]")
    console.print("[bold bright_blue]║[/bold bright_blue]  [bold white]SELF-ENGINEERING DEMO[/bold white]  [bold bright_blue]║[/bold bright_blue]")
    console.print("[bold bright_blue]║[/bold bright_blue]  [dim]The Meta-Game: System Engineering Itself[/dim]  [bold bright_blue]║[/bold bright_blue]")
    console.print("[bold bright_blue]╚════════════════════════════════════════╝[/bold bright_blue]\n")
    
    # Create self-engineering loop
    loop = SelfEngineeringLoop(
        scenario_runner=run_tavern_scenario,
        project_path=Path(__file__).parent.parent
    )
    
    console.print("[bold]Starting Self-Engineering Iteration Loop...[/bold]\n")
    
    # Run iteration
    result = loop.run_iteration(max_iterations=3)
    
    # Display results
    console.print(f"\n[bold]Iteration Results:[/bold]")
    console.print(f"  Success: {result.success}")
    console.print(f"  Iterations: {result.iterations}")
    console.print(f"  Improvements: {len(result.improvements)}")
    console.print(f"  Message: {result.message}\n")
    
    # Display problems detected
    problems = loop.problem_detector.get_recent_problems(10)
    if problems:
        console.print("[bold]Problems Detected:[/bold]")
        table = Table()
        table.add_column("Type", style="cyan")
        table.add_column("Severity", style="yellow")
        table.add_column("Description")
        
        for problem in problems:
            table.add_row(
                problem.type.value,
                problem.severity.value,
                problem.description[:60] + "..." if len(problem.description) > 60 else problem.description
            )
        console.print(table)
        console.print()
    
    # Display diagnoses
    diagnoses = loop.diagnostician.get_diagnosis_history(10)
    if diagnoses:
        console.print("[bold]Diagnoses:[/bold]")
        table = Table()
        table.add_column("Cause", style="cyan")
        table.add_column("Confidence", style="green")
        table.add_column("Explanation")
        
        for diagnosis in diagnoses:
            table.add_row(
                diagnosis.cause,
                f"{diagnosis.confidence:.2f}",
                diagnosis.explanation[:50] + "..." if len(diagnosis.explanation) > 50 else diagnosis.explanation
            )
        console.print(table)
        console.print()
    
    # Display solutions
    solutions = loop.solution_engineer.get_solution_history(10)
    if solutions:
        console.print("[bold]Solutions Proposed:[/bold]")
        table = Table()
        table.add_column("Type", style="cyan")
        table.add_column("Risk", style="yellow")
        table.add_column("Description")
        
        for solution in solutions:
            table.add_row(
                solution.type.value,
                solution.risk.value,
                solution.description[:50] + "..." if len(solution.description) > 50 else solution.description
            )
        console.print(table)
        console.print()
    
    # Display improvements
    if result.improvements:
        console.print("[bold]Improvements Made:[/bold]")
        table = Table()
        table.add_column("Iteration", style="cyan")
        table.add_column("Problem", style="yellow")
        table.add_column("Solution", style="green")
        table.add_column("Status")
        
        for improvement in result.improvements:
            table.add_row(
                str(improvement.iteration),
                improvement.problem.type.value,
                improvement.solution.description[:40] + "..." if len(improvement.solution.description) > 40 else improvement.solution.description,
                "✓ Success" if improvement.implementation.success else "✗ Failed"
            )
        console.print(table)
        console.print()
    
    console.print("[bold green]✓ Self-Engineering Demo Complete![/bold green]\n")
    
    # Summary
    console.print("[bold]Summary:[/bold]")
    console.print(f"  The system tried to play itself")
    console.print(f"  Detected {len(problems)} problem(s)")
    console.print(f"  Diagnosed {len(diagnoses)} cause(s)")
    console.print(f"  Proposed {len(solutions)} solution(s)")
    console.print(f"  Made {len(result.improvements)} improvement(s)")
    console.print()
    console.print("[dim]This demonstrates the self-engineering meta-game:[/dim]")
    console.print("[dim]  The system engineering itself to play itself better[/dim]\n")


if __name__ == "__main__":
    main()
