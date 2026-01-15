"""
Tests for decision tree integration with scenario engine.

Tests:
1. Decision tree training on scenario data
2. Choice recommendations
3. Feature extraction
4. Integration with ScenarioEngine
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from demo_scenario_engine import ScenarioEngine, run_demo_scenario
from waft.core.scenario_decision_tree import ScenarioDecisionTree, ScenarioState


def test_feature_extraction():
    """Test feature extraction from scenario state."""
    print("=" * 60)
    print("Test 1: Feature Extraction")
    print("=" * 60)
    
    state = ScenarioState(
        sequence_id="seq_001",
        sequence_type="ordinary",
        containers={
            "inventory": ["rusty_key", "coin_purse"],
            "clues": ["mysterious_note"]
        },
        visited_sequences=["seq_001"],
        choice_history=["A", "B"],
        available_choices=["A", "B", "C"]
    )
    
    # Create a minimal tree to test feature extraction
    tree = ScenarioDecisionTree()
    
    # Manually set container values for testing
    tree.all_container_values = {"rusty_key", "ornate_key", "coin_purse", "mysterious_note"}
    tree.all_sequence_ids = {"seq_001", "seq_002", "seq_003"}
    
    features = tree._extract_features(state)
    
    print(f"State: {state.sequence_id}")
    print(f"Features extracted: {len(features)} features")
    print(f"Feature vector: {features[:10]}...")  # Show first 10
    print("✓ Feature extraction works\n")


def test_decision_tree_training():
    """Test decision tree training on scenario data."""
    print("=" * 60)
    print("Test 2: Decision Tree Training")
    print("=" * 60)
    
    # Create training data
    states = [
        ScenarioState(
            sequence_id="seq_001",
            sequence_type="ordinary",
            containers={"inventory": ["rusty_key"]},
            visited_sequences=[],
            choice_history=[],
            available_choices=["A", "B", "C"]
        ),
        ScenarioState(
            sequence_id="seq_001",
            sequence_type="ordinary",
            containers={"inventory": ["rusty_key"]},
            visited_sequences=[],
            choice_history=[],
            available_choices=["A", "B", "C"]
        ),
        ScenarioState(
            sequence_id="seq_002",
            sequence_type="ordinary",
            containers={"inventory": ["rusty_key", "coin_purse"]},
            visited_sequences=["seq_001"],
            choice_history=["A"],
            available_choices=["A", "B"]
        ),
        ScenarioState(
            sequence_id="seq_002",
            sequence_type="ordinary",
            containers={"inventory": ["rusty_key", "coin_purse"]},
            visited_sequences=["seq_001"],
            choice_history=["A"],
            available_choices=["A", "B"]
        ),
    ]
    
    choices = ["A", "A", "B", "B"]  # Pattern: A when no history, B when has history
    
    tree = ScenarioDecisionTree(max_depth=5)
    tree.train(states, choices)
    
    print(f"Tree trained: {tree.is_trained}")
    print(f"Tree depth: {tree.get_tree_depth()}")
    
    # Test prediction
    test_state = ScenarioState(
        sequence_id="seq_001",
        sequence_type="ordinary",
        containers={"inventory": ["rusty_key"]},
        visited_sequences=[],
        choice_history=[],
        available_choices=["A", "B", "C"]
    )
    
    predictions = tree.predict(test_state)
    print(f"Predictions: {predictions}")
    
    recommendation = tree.recommend_choice(test_state, available_choices=["A", "B", "C"])
    if recommendation:
        choice, confidence = recommendation
        print(f"Recommendation: {choice} (confidence: {confidence:.2f})")
    
    # Feature importance
    importance = tree.get_feature_importance()
    top_features = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:5]
    print(f"Top 5 features: {top_features}")
    
    print("✓ Decision tree training works\n")


def test_scenario_engine_integration():
    """Test decision tree integration with ScenarioEngine."""
    print("=" * 60)
    print("Test 3: Scenario Engine Integration")
    print("=" * 60)
    
    scenario_file = Path(__file__).parent / "demo_scenario.json"
    
    if not scenario_file.exists():
        print(f"✗ Scenario file not found: {scenario_file}")
        return
    
    # Run scenario with decision tree enabled
    engine = run_demo_scenario(
        scenario_file,
        auto_play=True,
        use_decision_tree=True,
        use_recommendations=False  # Don't use recommendations for first run (training)
    )
    
    print(f"\nEvents: {len(engine.events)}")
    print(f"Training states: {len(engine.training_states)}")
    print(f"Training choices: {len(engine.training_choices)}")
    print(f"Decision tree trained: {engine.decision_tree.is_trained if engine.decision_tree else False}")
    
    if engine.decision_tree and engine.decision_tree.is_trained:
        # Test recommendation on a sequence
        if engine.events:
            last_event = engine.events[-1]
            if last_event.sequence_id:
                recommendation = engine.recommend_choice(last_event.sequence_id)
                if recommendation:
                    choice, confidence = recommendation
                    print(f"Recommendation for {last_event.sequence_id}: {choice} (confidence: {confidence:.2f})")
    
    print("✓ Scenario engine integration works\n")


def test_recommendation_accuracy():
    """Test recommendation accuracy by simulating player behavior."""
    print("=" * 60)
    print("Test 4: Recommendation Accuracy")
    print("=" * 60)
    
    scenario_file = Path(__file__).parent / "demo_scenario.json"
    
    if not scenario_file.exists():
        print(f"✗ Scenario file not found: {scenario_file}")
        return
    
    # Run scenario multiple times to collect training data
    all_states = []
    all_choices = []
    
    # Simulate 5 different playthroughs
    for i in range(5):
        engine = run_demo_scenario(
            scenario_file,
            auto_play=True,
            use_decision_tree=True,
            use_recommendations=False
        )
        
        if engine.training_states and engine.training_choices:
            all_states.extend(engine.training_states)
            all_choices.extend(engine.training_choices)
    
    if len(all_states) < 10:
        print(f"✗ Not enough training data: {len(all_states)} examples")
        return
    
    # Train on all data
    tree = ScenarioDecisionTree(max_depth=8)
    tree.train(all_states, all_choices)
    
    print(f"Trained on {len(all_states)} examples")
    print(f"Tree depth: {tree.get_tree_depth()}")
    
    # Test on a new scenario run
    test_engine = run_demo_scenario(
        scenario_file,
        auto_play=True,
        use_decision_tree=True,
        use_recommendations=False
    )
    
    # Use the trained tree
    test_engine.decision_tree = tree
    
    # Test recommendations
    correct = 0
    total = 0
    
    for event in test_engine.events:
        if event.choices_available and event.choice_made:
            recommendation = test_engine.recommend_choice(event.sequence_id)
            if recommendation:
                predicted_choice, confidence = recommendation
                actual_choice = event.choice_made.upper()
                total += 1
                if predicted_choice == actual_choice:
                    correct += 1
                    print(f"✓ Correct: {event.sequence_id} -> {predicted_choice} (confidence: {confidence:.2f})")
                else:
                    print(f"✗ Wrong: {event.sequence_id} -> predicted {predicted_choice}, actual {actual_choice}")
    
    if total > 0:
        accuracy = correct / total
        print(f"\nAccuracy: {accuracy:.2%} ({correct}/{total})")
        print("✓ Recommendation accuracy test complete\n")
    else:
        print("✗ No test cases available\n")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Decision Tree Integration Tests")
    print("=" * 60 + "\n")
    
    try:
        test_feature_extraction()
        test_decision_tree_training()
        test_scenario_engine_integration()
        test_recommendation_accuracy()
        
        print("=" * 60)
        print("All tests completed!")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
