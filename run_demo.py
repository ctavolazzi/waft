import sys
from waft.core.decision_cli import DecisionCLI
from waft.core.decision_matrix import DecisionMatrixCalculator
from pathlib import Path

def run_porchroot_strategy():
    cli = DecisionCLI(Path('.'))
    
    print("\n🚀 INITIALIZING STRATEGIC ANALYSIS ENGINE...\n")

    # Define the Strategic Decision
    problem = "Primary Business Focus for Q1 2026"
    
    alternatives = [
        "PorchRoot (Maker Goods)", 
        "FogSift (Consulting)", 
        "NovaSystem (AI Agents)"
    ]
    
    # Criteria: What matters most right now?
    # Let's say "Cash Flow" is King (0.5), but "Joy" is essential (0.3).
    criteria = {
        "Cash Flow Velocity": 0.5,
        "Joy & Fulfillment": 0.3,
        "Long-Term Scalability": 0.2
    }
    
    # The Scoring (1-10 Scale)
    scores = {
        "PorchRoot (Maker Goods)": {
            "Cash Flow Velocity": 4.0,  # Slow inventory turnover
            "Joy & Fulfillment": 10.0,  # Pure creative bliss
            "Long-Term Scalability": 3.0 # Hard to scale handmade
        },
        "FogSift (Consulting)": {
            "Cash Flow Velocity": 9.0,  # High hourly rate, immediate
            "Joy & Fulfillment": 6.0,   # It's work, but rewarding
            "Long-Term Scalability": 5.0 # Limited by hours in day
        },
        "NovaSystem (AI Agents)": {
            "Cash Flow Velocity": 2.0,  # R&D phase (money pit)
            "Joy & Fulfillment": 9.0,   # Intellectual thrill
            "Long-Term Scalability": 10.0 # Infinite scale software
        }
    }

    # RUN THE ENGINE
    cli.run_decision_matrix(
        problem=problem,
        alternatives=alternatives,
        criteria=criteria,
        scores=scores,
        methodology="WSM"
    )

def load_and_run():
    """Load a saved decision and run the analysis."""
    cli = DecisionCLI(Path('.'))
    
    print("\n📂 Loading saved decision...\n")
    
    matrix = cli.load_decision_dialog()
    if not matrix:
        print("No decision loaded.")
        return
    
    # Reconstruct problem name from matrix (or use default)
    problem = "Loaded Decision Analysis"
    
    # Extract data for display
    alternatives = [alt.name for alt in matrix.alternatives]
    criteria = {crit.name: crit.weight for crit in matrix.criteria}
    scores = {}
    for score in matrix.scores:
        if score.alternative_name not in scores:
            scores[score.alternative_name] = {}
        scores[score.alternative_name][score.criterion_name] = score.value
    
    # Run the analysis
    calculator = DecisionMatrixCalculator(matrix)
    results = calculator.calculate_wsm()
    rankings = calculator.rank_alternatives(results)
    
    # Display results
    cli._display_results(
        problem, alternatives, criteria, results, rankings,
        calculator, show_details=True, show_sensitivity=True
    )
    
    # Offer to save again (with new name)
    cli.save_decision_dialog(matrix)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--load':
        load_and_run()
    else:
        run_porchroot_strategy()
