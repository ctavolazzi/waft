# Scientific Method Tool

Implements a rudimentary version of the scientific method for experimental verification and hypothesis testing.

## Purpose

This tool enables the system to:
1. Form hypotheses
2. Design experiments
3. Capture initial state (A)
4. Run experiments
5. Collect data during experiments (C)
6. Capture final state (B)
7. Analyze results
8. Verify or refute hypotheses
9. Iterate with variable changes

## Architecture

```
scientific_method_tool/
├── __init__.py              # Exports
├── hypothesis.py            # Hypothesis and Variable system
├── state_capture.py         # State capture (A and B)
├── data_collection.py       # Data collection (C)
├── experiment.py            # Experiment management
├── experiment_loop.py       # Iterative experiment loop
└── analysis.py              # Result analysis
```

## Core Components

### 1. Hypothesis System (`hypothesis.py`)

Defines testable hypotheses with variables:
- **Independent variables**: Variables we control
- **Dependent variables**: Variables we measure
- **Control variables**: Variables we keep constant

### 2. State Capture (`state_capture.py`)

Captures system states:
- **Initial state (A)**: System state before experiment
- **Final state (B)**: System state after experiment
- **State comparison**: Identifies changes between states

### 3. Data Collection (`data_collection.py`)

Collects data during experiments:
- **Data points**: Individual measurements
- **Data series**: Time series of measurements
- **Metrics**: Fitness, decisions, skills, etc.

### 4. Experiment Management (`experiment.py`)

Manages individual experiments:
- Creates experiments
- Captures states
- Runs experiments
- Stores results

### 5. Experiment Loop (`experiment_loop.py`)

Runs iterative experiments:
- Iterates over variable values
- Runs multiple experiments
- Collects all results
- Enables hypothesis testing

### 6. Analysis (`analysis.py`)

Analyzes experiment results:
- Verifies or refutes hypotheses
- Calculates confidence
- Generates conclusions
- Provides recommendations

## Usage Example

```python
from scientific_method_tool import (
    Hypothesis, Variable, VariableType,
    ExperimentLoop, IterationConfig,
    ExperimentAnalyzer
)
from pathlib import Path

# 1. Form hypothesis
hypothesis = Hypothesis(
    statement="Increasing investigation skill improves decision quality",
    prediction="Higher investigation skill will result in better choices and higher fitness"
)

# Add variables
hypothesis.add_variable(Variable(
    name="investigation_skill",
    type=VariableType.INDEPENDENT,
    value=30.0,
    description="Investigation skill level",
    range=(10.0, 50.0)
))

hypothesis.add_variable(Variable(
    name="fitness_gained",
    type=VariableType.DEPENDENT,
    value=0.0,
    description="Fitness gained during experiment"
))

# 2. Create experiment loop
loop = ExperimentLoop(Path("./experiments"))

# 3. Define experiment function
def run_experiment(experiment):
    # Your experiment logic here
    # Use experiment.data_collector to record data
    experiment.data_collector.record_fitness(50.0)
    return {"fitness_gained": 50.0, "prediction_match": True, "confidence": 0.8}

# 4. Define initial components function
def create_initial_components(var_values):
    return {
        "beings": [{"skills": {"investigation": var_values["investigation_skill"]}}]
    }

# 5. Run iterative experiments
results = loop.run_iterative_experiment(
    hypothesis=hypothesis,
    experiment_function=run_experiment,
    initial_components_function=create_initial_components,
    max_iterations=10
)

# 6. Analyze results
analyzer = ExperimentAnalyzer()
analysis = analyzer.analyze_iteration_results(hypothesis, results)

print(f"Hypothesis verified: {analysis.verified}")
print(f"Confidence: {analysis.confidence:.2%}")
print("Conclusions:", analysis.conclusions)
```

## Storage Structure

```
scientific_method_tool/
├── experiments/          # Experiment definitions
│   └── exp_xxxxx.json
├── states/              # State snapshots (A and B)
│   └── state_initial_xxxxx.json
│   └── state_final_xxxxx.json
├── data/                # Collected data (C)
│   └── data_exp_xxxxx.json
└── results_summary_xxxxx.json
```

## Integration with Self-Engineering

The scientific method tool integrates with the self-engineering system:
- Experiments can test self-engineering improvements
- State capture tracks system evolution
- Data collection monitors self-modification effects
- Analysis verifies if improvements work

## The Scientific Method Cycle

1. **Observe**: System detects problems
2. **Hypothesize**: Form hypothesis about solution
3. **Experiment**: Test hypothesis with controlled variables
4. **Collect Data**: Record all measurements (C)
5. **Capture States**: Save initial (A) and final (B) states
6. **Analyze**: Verify or refute hypothesis
7. **Iterate**: Modify variables and repeat
8. **Conclude**: Draw conclusions from evidence

This enables the system to scientifically verify its own improvements.
