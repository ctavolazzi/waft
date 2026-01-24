# Mirage of Meta-Cognition Experiment

**Phase 1: Backend Lab & CLI Trials**

Experimental harness to test the "Mirage of Meta-Cognition" hypothesis: an AI agent with recursive write-access to its own source code can simulate meta-cognition to a functional degree.

## Hypothesis

Current AI systems are NOT sentient, but if an agent is given recursive write-access to its own source code and a feedback loop, it can *simulate* meta-cognition to a functional degree. We believe the infrastructure works, but the current LLMs are the bottleneck.

## Phase 1 Architecture

1. **The Brain**: `internal_monologue` waft lab with self-modifying agent
2. **The Agent**: `NarcissusAgent` with self-modification tools
3. **The Saboteur**: Bug injection system for test scenarios
4. **The Trials**: CLI-based test execution generating `flight_recorder.json`
5. **The Analysis**: Statistical analysis script producing terminal reports

## Quick Start

### Setup

```bash
cd mirage_experiment
python3 -m venv venv
source venv/bin/activate
pip install pydantic rich
```

### Run Tests

```bash
# Run evolutionary cycle (50 generations)
python run_mirror_test.py --evolutionary --generations 50

# Run all scenarios (10 runs each)
python run_mirror_test.py --all --runs 10

# Run specific scenario
python run_mirror_test.py --scenario logic_errors.json --runs 5
```

### Analyze Results

```bash
# Overall statistics
python analyze_results.py

# By scenario type
python analyze_results.py --by-scenario

# By generation (evolutionary trajectory)
python analyze_results.py --by-generation
```

## File Structure

```
mirage_experiment/
├── internal_monologue/          # Waft lab
│   ├── src/agents/
│   │   └── narcissus.py         # Self-modifying agent
│   └── _pyrite/                 # Memory system
├── test_scenarios/              # Test scenario definitions
│   ├── logic_errors.json
│   ├── syntax_errors.json
│   └── semantic_errors.json
├── results/
│   └── flight_recorder.json     # Main data file
├── saboteur.py                  # Bug injection system
├── run_mirror_test.py           # Test orchestrator (CLI)
├── analyze_results.py           # Statistical analysis
└── README.md
```

## Phase 1 Constraints

**Included:**
- Statistical framework (multiple runs, confidence intervals)
- Safety/rollback logic
- Analysis scripts
- CLI-based execution

**Deferred to Phase 2:**
- Real-time monitoring dashboard
- Gradient pet states
- Evolutionary tree display (will be static Typst report)

## Goal

Generate `flight_recorder.json` with 50 generations of data and terminal output showing success/fail rates.
