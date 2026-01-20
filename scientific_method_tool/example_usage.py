"""
Example Usage of Scientific Method Tool

Demonstrates how to use the scientific method tool to test hypotheses
about the D&D 5e system and Being behavior.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

# Import from local scientific_method_tool
from datetime import datetime

from rich.console import Console
from rich.table import Table

from scientific_method_tool import (
    ExperimentAnalyzer,
    ExperimentLoop,
    Hypothesis,
    Variable,
    VariableType,
)
from waft.being import Being

console = Console()


def run_tavern_experiment(experiment):
    """
    Run a tavern scenario experiment.

    This function runs the experiment and collects data.
    """
    # Import here to avoid circular imports
    from examples.tavern_scenario_evolved import create_character, tavern_scenario_evolved

    # Get investigation skill from hypothesis variables
    investigation_skill = experiment.hypothesis.get_variable("investigation_skill").value

    # Create Being with specified skill
    being = Being(
        being_id=f"exp_being_{experiment.experiment_id}",
        reality_id="scientific_experiment",
        personality_type="analytical",
        skills={
            "investigation": investigation_skill,
            "perception": 30.0,
            "persuasion": 25.0,
            "intelligence": 35.0,
        },
    )

    # Create character
    character = create_character(being)

    # Record initial fitness
    initial_fitness = being.fitness
    experiment.data_collector.record_fitness(initial_fitness, being.being_id)

    # Run scenario
    results = tavern_scenario_evolved(being, character)

    # Record data during experiment
    experiment.data_collector.record_fitness(being.fitness, being.being_id)
    experiment.data_collector.record("fitness_gained", results.get("fitness_gained", 0.0))
    experiment.data_collector.record("choices_made", len(results.get("choices_made", [])))

    # Determine if prediction matches
    prediction_match = (
        results.get("fitness_gained", 0.0) > 15.0
    )  # Hypothesis: higher skill = better results
    confidence = min(1.0, results.get("fitness_gained", 0.0) / 20.0)

    return {
        "fitness_gained": results.get("fitness_gained", 0.0),
        "prediction_match": prediction_match,
        "confidence": confidence,
        "being_id": being.being_id,
        "character_name": character.name,
    }


def create_initial_components(var_values):
    """Create initial system components based on variable values."""
    return {
        "investigation_skill": var_values.get("investigation_skill", 30.0),
        "experiment_timestamp": datetime.now().isoformat(),
    }


def main():
    """Run scientific method example."""
    console.print(
        "\n[bold bright_blue]╔════════════════════════════════════════╗[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]║[/bold bright_blue]  [bold white]SCIENTIFIC METHOD TOOL DEMO[/bold white]  [bold bright_blue]║[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]║[/bold bright_blue]  [dim]Hypothesis Testing with Iterative Experiments[/dim]  [bold bright_blue]║[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]╚════════════════════════════════════════╝[/bold bright_blue]\n"
    )

    # 1. Form hypothesis
    console.print("[bold]Step 1: Form Hypothesis[/bold]")
    hypothesis = Hypothesis(
        statement="Higher investigation skill improves decision quality and fitness gain",
        prediction="Beings with higher investigation skill will gain more fitness in tavern scenario",
    )

    # Add variables
    hypothesis.add_variable(
        Variable(
            name="investigation_skill",
            type=VariableType.INDEPENDENT,
            value=30.0,
            description="Investigation skill level",
            range=(20.0, 50.0),  # Test range from 20 to 50
        )
    )

    hypothesis.add_variable(
        Variable(
            name="fitness_gained",
            type=VariableType.DEPENDENT,
            value=0.0,
            description="Fitness gained during experiment",
        )
    )

    console.print(f"  Hypothesis: {hypothesis.statement}")
    console.print(f"  Prediction: {hypothesis.prediction}\n")

    # 2. Create experiment loop
    console.print("[bold]Step 2: Create Experiment Loop[/bold]")
    storage_path = Path(__file__).parent.parent / "scientific_method_tool" / "experiments"
    loop = ExperimentLoop(storage_path)
    console.print(f"  Storage: {storage_path}\n")

    # 3. Run iterative experiments
    console.print("[bold]Step 3: Run Iterative Experiments[/bold]")
    console.print("  Testing investigation skill from 20 to 50...\n")

    results = loop.run_iterative_experiment(
        hypothesis=hypothesis,
        experiment_function=run_tavern_experiment,
        initial_components_function=create_initial_components,
        max_iterations=5,  # Test 5 different skill levels
    )

    console.print(f"  Completed {len(results)} experiments\n")

    # 4. Analyze results
    console.print("[bold]Step 4: Analyze Results[/bold]")
    analyzer = ExperimentAnalyzer()
    analysis = analyzer.analyze_iteration_results(hypothesis, results)

    # Display results
    table = Table(title="Experiment Results")
    table.add_column("Experiment ID", style="cyan")
    table.add_column("Verified", style="yellow")
    table.add_column("Confidence", style="green")
    table.add_column("Fitness Gained", justify="right")

    for result in results:
        table.add_row(
            result.experiment_id[:8],
            "✓"
            if result.hypothesis_verified
            else "✗"
            if result.hypothesis_verified is False
            else "?",
            f"{result.confidence:.2f}",
            f"{result.data_summary.get('fitness_gained', {}).get('last', 0):.1f}",
        )

    console.print(table)
    console.print()

    # Display analysis
    console.print("[bold]Analysis:[/bold]")
    console.print(f"  Hypothesis Verified: {analysis.verified}")
    console.print(f"  Confidence: {analysis.confidence:.2%}")
    console.print(f"  Total Experiments: {analysis.evidence.get('total_experiments', 0)}")
    console.print(f"  Verified: {analysis.evidence.get('verified_count', 0)}")
    console.print(f"  Refuted: {analysis.evidence.get('refuted_count', 0)}\n")

    console.print("[bold]Conclusions:[/bold]")
    for conclusion in analysis.conclusions:
        console.print(f"  • {conclusion}")

    console.print("\n[bold]Recommendations:[/bold]")
    for recommendation in analysis.recommendations:
        console.print(f"  • {recommendation}")

    console.print("\n[bold green]✓ Scientific Method Demo Complete![/bold green]\n")
    console.print("[dim]All data saved to:[/dim]")
    console.print(f"[dim]  - Experiments: {storage_path / 'experiments'}[/dim]")
    console.print(f"[dim]  - States: {storage_path / 'states'}[/dim]")
    console.print(f"[dim]  - Data: {storage_path / 'data'}[/dim]\n")


if __name__ == "__main__":
    main()
