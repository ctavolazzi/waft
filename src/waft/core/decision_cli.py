"""
Decision CLI - Standardized command-line interface for decision matrix calculations.

Provides a reusable, standardized way to run decision matrix analysis
using the DecisionMatrixCalculator module.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

from .decision_matrix import (
    DecisionMatrix, DecisionMatrixCalculator,
    Alternative, Criterion, Score
)
from .input_transformer import InputTransformer
from .persistence import DecisionPersistence


class DecisionCLI:
    """Standardized CLI interface for decision matrix calculations."""
    
    def __init__(self, project_path: Path):
        """
        Initialize decision CLI.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.console = Console()
    
    def run_decision_matrix(
        self,
        problem: str,
        alternatives: List[str],
        criteria: Dict[str, float],
        scores: Dict[str, Dict[str, float]],
        methodology: str = "WSM",
        criterion_descriptions: Optional[Dict[str, str]] = None,
        show_details: bool = True,
        show_sensitivity: bool = True
    ) -> Dict[str, Any]:
        """
        Run a standardized decision matrix calculation.
        
        Args:
            problem: Description of the decision problem
            alternatives: List of alternative names
            criteria: Dictionary mapping criterion names to weights (must sum to 1.0)
            scores: Nested dict: {alternative_name: {criterion_name: score}}
            methodology: Calculation method (WSM only - WPM, AHP, BWM removed in Iron Core)
            criterion_descriptions: Optional descriptions for criteria
            show_details: Whether to show detailed breakdown
            show_sensitivity: Whether to run sensitivity analysis
            
        Returns:
            Dictionary with results, rankings, and recommendations
        """
        # Prepare raw input data for transformer
        # Merge criterion_descriptions into criteria dict if provided
        criteria_with_descriptions = {}
        for name, weight in criteria.items():
            if criterion_descriptions and name in criterion_descriptions:
                criteria_with_descriptions[name] = {
                    'weight': weight,
                    'description': criterion_descriptions[name]
                }
            else:
                criteria_with_descriptions[name] = weight
        
        raw_data = {
            'alternatives': alternatives,
            'criteria': criteria_with_descriptions,
            'scores': scores,
            'methodology': methodology
        }
        
        # Transform input using InputTransformer (The Gateway/Airlock)
        try:
            matrix = InputTransformer.transform_input(raw_data)
        except ValueError as e:
            # User-friendly error message
            self.console.print(f"[bold red]Input Error:[/bold red] {str(e)}")
            raise
        
        # Calculate
        calculator = DecisionMatrixCalculator(matrix)
        
        # Only WSM is supported in the hardened Iron Core
        if methodology != "WSM":
            raise ValueError(f"Unsupported methodology: {methodology}. Only 'WSM' is supported.")
        results = calculator.calculate_wsm()
        
        rankings = calculator.rank_alternatives(results)
        
        # Display results
        self._display_results(
            problem, alternatives, criteria, results, rankings,
            calculator, show_details, show_sensitivity
        )
        
        # Offer to save the decision
        self.save_decision_dialog(matrix)
        
        return {
            "problem": problem,
            "alternatives": alternatives,
            "criteria": criteria,
            "methodology": methodology,
            "results": results,
            "rankings": rankings,
            "recommendation": rankings[0][0] if rankings else None,
        }
    
    def _display_results(
        self,
        problem: str,
        alternatives: List[str],
        criteria: Dict[str, float],
        results: Dict[str, float],
        rankings: List[tuple],
        calculator: DecisionMatrixCalculator,
        show_details: bool,
        show_sensitivity: bool
    ):
        """Display decision matrix results with Rich formatting."""
        # Header
        self.console.print()
        self.console.print(Panel(
            f"[bold cyan]{problem}[/bold cyan]",
            title="[bold]Decision Matrix Analysis[/bold]",
            border_style="cyan"
        ))
        self.console.print()
        
        # Feature A: The Summary Table (The Leaderboard)
        self._display_leaderboard(rankings)
        
        # Feature B: The Detailed Matrix (The Analysis)
        if show_details:
            self._display_analysis_matrix(alternatives, criteria, results, calculator)
        
        # Feature C: Sensitivity Analysis (The "What If")
        if show_sensitivity and len(criteria) > 1:
            self._display_sensitivity_analysis(criteria, rankings, calculator)
    
    def _display_leaderboard(self, rankings: List[tuple]):
        """Feature A: Display summary table with winner highlighted."""
        table = Table(
            title="[bold]🏆 Leaderboard[/bold]",
            show_header=True,
            header_style="bold cyan",
            box=box.ROUNDED,
            border_style="cyan"
        )
        table.add_column("Rank", justify="center", style="dim", width=6)
        table.add_column("Alternative", style="cyan", width=40)
        table.add_column("Total Score", justify="right", style="bold", width=12)
        
        for alt_name, score, rank in rankings:
            # Highlight winner (Rank 1) in green/gold
            if rank == 1:
                rank_style = "[bold gold1]🥇[/bold gold1]"
                alt_style = f"[bold green]{alt_name}[/bold green]"
                score_style = f"[bold green]{score:.2f}[/bold green]"
            elif rank == 2:
                rank_style = "[bold]🥈[/bold]"
                alt_style = alt_name
                score_style = f"[bold]{score:.2f}[/bold]"
            elif rank == 3:
                rank_style = "[bold]🥉[/bold]"
                alt_style = alt_name
                score_style = f"{score:.2f}"
            else:
                rank_style = f"{rank}."
                alt_style = alt_name
                score_style = f"{score:.2f}"
            
            table.add_row(rank_style, alt_style, score_style)
        
        self.console.print(table)
        self.console.print()
    
    def _display_analysis_matrix(
        self,
        alternatives: List[str],
        criteria: Dict[str, float],
        results: Dict[str, float],
        calculator: DecisionMatrixCalculator
    ):
        """Feature B: Display detailed matrix showing why each option scored as it did."""
        table = Table(
            title="[bold]📊 Detailed Analysis Matrix[/bold]",
            show_header=True,
            header_style="bold cyan",
            box=box.ROUNDED,
            border_style="cyan"
        )
        
        # Add Alternative column
        table.add_column("Alternative", style="cyan", width=25)
        
        # Add criterion columns with weight in header
        for crit_name, weight in criteria.items():
            header = f"{crit_name}\n[dim]({weight:.0%})[/dim]"
            table.add_column(header, justify="right", width=12)
        
        # Add Total Score column
        table.add_column("Total Score", justify="right", style="bold", width=12)
        
        # Get detailed scores
        all_details = calculator.get_detailed_scores()
        
        # Add rows for each alternative
        for alt_name in alternatives:
            row = [alt_name]
            
            # Add scores for each criterion
            alt_scores = all_details.get(alt_name, {})
            for crit_name in criteria.keys():
                raw_score = alt_scores.get(crit_name, 0.0)
                # Show raw score (user can see why it won)
                row.append(f"{raw_score:.1f}")
            
            # Add total score
            total_score = results.get(alt_name, 0.0)
            # Highlight if this is the winner
            if total_score == max(results.values()):
                row.append(f"[bold green]{total_score:.2f}[/bold green]")
            else:
                row.append(f"{total_score:.2f}")
            
            table.add_row(*row)
        
        self.console.print(table)
        self.console.print()
    
    def _display_sensitivity_analysis(
        self,
        criteria: Dict[str, float],
        rankings: List[tuple],
        calculator: DecisionMatrixCalculator
    ):
        """Feature C: Sensitivity analysis - check if winner changes when highest weight criterion is reduced."""
        # Find criterion with highest weight
        highest_crit = max(criteria.items(), key=lambda x: x[1])
        crit_name, crit_weight = highest_crit
        
        # Original winner
        original_winner = rankings[0][0]
        
        # Calculate what happens if highest weight is reduced by 20%
        reduced_weight = crit_weight * 0.8
        remaining_weight = 1.0 - reduced_weight
        
        # Distribute remaining weight proportionally to other criteria
        other_criteria = {k: v for k, v in criteria.items() if k != crit_name}
        other_total = sum(other_criteria.values())
        
        if other_total > 0:
            adjusted_criteria = {crit_name: reduced_weight}
            for other_name, other_weight in other_criteria.items():
                # Proportional distribution
                adjusted_criteria[other_name] = other_weight * (remaining_weight / other_total)
            
            # Rebuild criteria objects
            crit_objects = []
            for name, weight in adjusted_criteria.items():
                # Find original criterion to preserve description
                original = next(
                    c for c in calculator.matrix.criteria
                    if c.name == name
                )
                crit_objects.append(
                    Criterion(name, weight, original.description)
                )
            
            # Create adjusted matrix and calculate
            adjusted_matrix = DecisionMatrix(
                calculator.matrix.alternatives,
                crit_objects,
                calculator.matrix.scores,
                methodology="WSM"
            )
            adjusted_calc = DecisionMatrixCalculator(adjusted_matrix)
            adjusted_results = adjusted_calc.calculate_wsm()
            adjusted_rankings = adjusted_calc.rank_alternatives(adjusted_results)
            new_winner = adjusted_rankings[0][0]
            
            # Display sensitivity analysis
            self.console.print(Panel(
                "[bold]🔍 Sensitivity Analysis[/bold]",
                border_style="yellow"
            ))
            self.console.print()
            
            self.console.print(f"[dim]Scenario:[/dim] If '{crit_name}' weight reduced by 20% "
                             f"({crit_weight:.0%} → {reduced_weight:.0%})")
            self.console.print()
            
            # Show new rankings
            sens_table = Table(show_header=True, header_style="bold", box=box.SIMPLE)
            sens_table.add_column("Rank", justify="center", width=6)
            sens_table.add_column("Alternative", width=30)
            sens_table.add_column("Score", justify="right", width=12)
            
            for alt_name, score, rank in adjusted_rankings:
                if rank == 1:
                    sens_table.add_row(
                        "[bold]1[/bold]",
                        f"[bold]{alt_name}[/bold]",
                        f"[bold]{score:.2f}[/bold]"
                    )
                else:
                    sens_table.add_row(str(rank), alt_name, f"{score:.2f}")
            
            self.console.print(sens_table)
            self.console.print()
            
            # Warning if winner changed
            if new_winner != original_winner:
                self.console.print(
                    Panel(
                        f"⚠️  [bold yellow]Warning:[/bold yellow] If '{crit_name}' becomes less important, "
                        f"[bold]{new_winner}[/bold] would win instead of [bold]{original_winner}[/bold].",
                        border_style="yellow",
                        title="[bold yellow]Winner Changed[/bold yellow]"
                    )
                )
            else:
                self.console.print(
                    f"[green]✓[/green] Recommendation is [bold]robust[/bold]: "
                    f"[bold]{original_winner}[/bold] remains the winner even with reduced '{crit_name}' weight."
                )
            
            self.console.print()
    
    def save_decision_dialog(self, matrix: DecisionMatrix) -> Optional[Path]:
        """
        Prompt user to save the decision matrix.
        
        Args:
            matrix: The DecisionMatrix to save
        
        Returns:
            Path to saved file if saved, None if user declined
        """
        try:
            # Try to use rich.prompt if available
            from rich.prompt import Confirm, Prompt
            save_it = Confirm.ask("\n💾 Save this analysis?", default=False)
        except ImportError:
            # Fallback to standard input
            response = input("\n💾 Save this analysis? [y/N]: ").strip().lower()
            save_it = response in ('y', 'yes')
        
        if not save_it:
            return None
        
        # Create saved_decisions directory
        saved_dir = self.project_path / "saved_decisions"
        saved_dir.mkdir(exist_ok=True)
        
        # Generate default filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"decision_{timestamp}.json"
        
        try:
            from rich.prompt import Prompt
            filename = Prompt.ask(
                "📝 Filename",
                default=default_filename
            )
        except ImportError:
            filename = input(f"📝 Filename [{default_filename}]: ").strip()
            if not filename:
                filename = default_filename
        
        # Ensure .json extension
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = saved_dir / filename
        
        try:
            DecisionPersistence.save(matrix, filepath)
            self.console.print(f"\n[green]✓[/green] Saved to: [cyan]{filepath}[/cyan]")
            return filepath
        except Exception as e:
            self.console.print(f"[bold red]Error saving file:[/bold red] {str(e)}")
            return None
    
    def load_decision_dialog(self) -> Optional[DecisionMatrix]:
        """
        Prompt user to load a saved decision matrix.
        
        Returns:
            DecisionMatrix if loaded, None if user cancelled
        """
        saved_dir = self.project_path / "saved_decisions"
        
        if not saved_dir.exists():
            self.console.print("[yellow]No saved decisions found.[/yellow]")
            return None
        
        # List available files
        json_files = sorted(saved_dir.glob("*.json"))
        
        if not json_files:
            self.console.print("[yellow]No saved decisions found.[/yellow]")
            return None
        
        # Display list
        self.console.print("\n[bold]📂 Saved Decisions:[/bold]\n")
        table = Table(show_header=True, header_style="bold", box=box.SIMPLE)
        table.add_column("#", justify="right", width=4)
        table.add_column("Filename", width=40)
        table.add_column("Modified", width=20)
        
        for i, filepath in enumerate(json_files, 1):
            mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
            table.add_row(
                str(i),
                filepath.name,
                mtime.strftime("%Y-%m-%d %H:%M")
            )
        
        self.console.print(table)
        self.console.print()
        
        try:
            from rich.prompt import IntPrompt
            choice = IntPrompt.ask(
                "Select decision to load",
                default=1,
                show_default=True
            )
        except ImportError:
            choice_str = input(f"Select decision to load [1-{len(json_files)}]: ").strip()
            try:
                choice = int(choice_str)
            except ValueError:
                self.console.print("[red]Invalid selection.[/red]")
                return None
        
        if choice < 1 or choice > len(json_files):
            self.console.print("[red]Invalid selection.[/red]")
            return None
        
        selected_file = json_files[choice - 1]
        
        try:
            matrix = DecisionPersistence.load(selected_file)
            self.console.print(f"\n[green]✓[/green] Loaded: [cyan]{selected_file.name}[/cyan]")
            return matrix
        except Exception as e:
            self.console.print(f"[bold red]Error loading file:[/bold red] {str(e)}")
            return None
