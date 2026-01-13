#!/usr/bin/env python3
"""
Run Multiple Proof Experiments

Spawns multiple versions of the proof to demonstrate reproducibility.
"""

from pathlib import Path
import sys
import json
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from scientific_method_tool import (
    Hypothesis,
    Variable,
    VariableType,
    ExperimentManager,
    ExperimentAnalyzer
)

def simple_experiment(experiment):
    """Simple experiment that increments a counter."""
    initial_value = 10
    experiment.data_collector.record("counter", initial_value)
    
    final_value = initial_value + 5
    
    experiment.data_collector.record("counter", final_value)
    experiment.data_collector.record("change", final_value - initial_value)
    
    return {
        "initial": initial_value,
        "final": final_value,
        "change": final_value - initial_value,
        "prediction_match": True,
        "confidence": 0.9
    }

def create_components(var_values):
    """Create initial components."""
    return {
        "counter": 10,
        "test_var": var_values.get("test_variable", 1)
    }

def run_single_proof(proof_id: int, storage_path: Path) -> dict:
    """Run a single proof experiment."""
    print(f"\n{'='*60}")
    print(f"PROOF #{proof_id}")
    print(f"{'='*60}")
    
    # Create hypothesis
    hypothesis = Hypothesis(
        statement="Incrementing a counter increases its value",
        prediction="Counter will increase by 5"
    )
    hypothesis.add_variable(Variable(
        name="test_variable",
        type=VariableType.INDEPENDENT,
        value=1,
        description="Test variable"
    ))
    
    # Create manager
    manager = ExperimentManager(storage_path)
    experiment = manager.create_experiment(hypothesis)
    
    # Capture initial state (A)
    initial_components = create_components({"test_variable": 1})
    initial_state = manager.capture_initial_state(experiment, initial_components)
    
    # Run experiment
    results = manager.run_experiment(
        experiment,
        simple_experiment,
        initial_components
    )
    
    # Get data
    data_series = experiment.data_collector.get_all_series()
    
    # Analyze
    analyzer = ExperimentAnalyzer()
    analysis = analyzer.analyze_experiment(experiment, results)
    
    # Collect summary
    summary = {
        "proof_id": proof_id,
        "experiment_id": experiment.experiment_id,
        "timestamp": datetime.now().isoformat(),
        "initial_state_hash": initial_state.state_hash[:8] if initial_state else None,
        "final_state_hash": experiment.final_state.state_hash[:8] if experiment.final_state else None,
        "results": results,
        "data_series": {
            name: {
                "count": len(series.data_points),
                "values": series.get_values()
            }
            for name, series in data_series.items()
        },
        "analysis": {
            "verified": analysis.verified,
            "confidence": analysis.confidence,
            "conclusions_count": len(analysis.conclusions)
        },
        "files": {
            "experiments": len(list((storage_path / "experiments").glob("*.json"))),
            "states": len(list((storage_path / "states").glob("*.json"))),
            "data": len(list((storage_path / "data").glob("*.json")))
        }
    }
    
    print(f"✅ Proof #{proof_id} complete")
    print(f"   Experiment ID: {experiment.experiment_id}")
    print(f"   Verified: {analysis.verified}")
    print(f"   Confidence: {analysis.confidence:.2%}")
    
    return summary

def main():
    """Run multiple proof experiments."""
    print("=" * 60)
    print("MULTIPLE PROOF EXPERIMENTS")
    print("=" * 60)
    print()
    
    # Use persistent storage
    storage_path = Path("scientific_method_tool/proof_experiments")
    storage_path.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories
    (storage_path / "experiments").mkdir(exist_ok=True)
    (storage_path / "states").mkdir(exist_ok=True)
    (storage_path / "data").mkdir(exist_ok=True)
    
    print(f"📁 Storage: {storage_path.absolute()}")
    print()
    
    # Run multiple proofs
    num_proofs = 5
    print(f"Running {num_proofs} proof experiments...")
    print()
    
    all_summaries = []
    for i in range(1, num_proofs + 1):
        summary = run_single_proof(i, storage_path)
        all_summaries.append(summary)
    
    # Save summary
    summary_file = storage_path / "proof_summary.json"
    with open(summary_file, 'w') as f:
        json.dump({
            "total_proofs": num_proofs,
            "timestamp": datetime.now().isoformat(),
            "proofs": all_summaries
        }, f, indent=2)
    
    print()
    print("=" * 60)
    print("✅ ALL PROOFS COMPLETE")
    print("=" * 60)
    print()
    print(f"📊 Summary saved to: {summary_file}")
    print()
    print("Results:")
    for summary in all_summaries:
        print(f"  Proof #{summary['proof_id']}: "
              f"Verified={summary['analysis']['verified']}, "
              f"Confidence={summary['analysis']['confidence']:.2%}")
    print()
    print("All experiments saved to:")
    print(f"  - Experiments: {storage_path / 'experiments'}")
    print(f"  - States: {storage_path / 'states'}")
    print(f"  - Data: {storage_path / 'data'}")
    print()
    print("Run Streamlit app to visualize:")
    print("  streamlit run scientific_method_tool/proof_visualizer.py")

if __name__ == "__main__":
    main()
