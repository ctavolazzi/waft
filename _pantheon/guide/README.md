# The Guide: Meta-Cognitive Guidance System

**Pantheon Entity**: *Timeless Force that Binds Reality Together*

The Guide is the God of Meta-Cognitive Guidance - a Pantheon entity that orchestrates iterative reasoning improvement through guided evaluation and meta-cognitive oversight.

## Philosophy ("As Above, So Below")

- **As Above**: Pantheon god maintaining the celestial loop of guidance and evaluation
- **So Below**: File-based system tracking guidance sessions, protocols, and reasoning chains

## Overview

TheGuide implements a meta-cognitive guidance loop where:

1. **Guide LLM** provides meta-cognitive instructions and evaluates reasoning quality
2. **Client LLM** receives problems and produces step-by-step reasoning
3. **FVCU+Faithfulness Evaluation** assesses reasoning across 5 dimensions
4. **Protocol** captures the complete reasoning chain for "Why?" explanations
5. **Integration** with TheReasoner for trace storage and chain building

## Architecture

```
User → Client LLM → Guide LLM → Loop (Instructions ↔ Reasoning ↔ Evaluation) → Answer + Protocol
                                                                                        ↓
                                                                                  User: "Why?"
                                                                                        ↓
                                                                              Explanation (from Protocol)
```

## FVCU+Faithfulness Taxonomy

TheGuide evaluates reasoning using a multi-criteria taxonomy based on research:

### The Five Dimensions (0.0-1.0 scores)

1. **Factuality**: Is the reasoning grounded in the query or external facts?
   - High: Uses facts from the problem statement or verified external sources
   - Low: Makes unfounded assumptions or introduces ungrounded information

2. **Validity**: Is the reasoning logically and arithmetically correct?
   - High: Sound logical inference, correct calculations
   - Low: Logical fallacies, arithmetic errors

3. **Coherence**: Are all preconditions satisfied by previous steps?
   - High: Builds only on established facts, no forward-looking planning
   - Low: References future steps, assumes unproven premises, forward planning

4. **Utility**: Does this reasoning contribute to the correct final answer?
   - High: Directly advances toward solving the problem
   - Low: Irrelevant tangents, unhelpful detours

5. **Faithfulness**: Does claimed reasoning match actual computation?
   - High: All claimed steps actually occur, no phantom reasoning
   - Low: Claims to do computation that doesn't actually happen

### Evaluation Method: Critic Model (LLM-as-a-Judge)

The Guide LLM acts as a critic, evaluating each reasoning step and providing:

- Numerical scores (0.0-1.0) for each dimension
- Rationale explaining the scores
- Strengths identified in the reasoning
- Weaknesses to address
- Recommendations for improvement
- Detection of forward-looking planning
- Detection of unfaithful reasoning

## Key Features

### Core Capabilities

- **Meta-Cognitive Guidance Loop**: Iterative refinement through Guide ↔ Client interaction
- **FVCU+Faithfulness Evaluation**: Multi-criteria assessment of reasoning quality
- **Protocol Generation**: Complete session records for transparency
- **"Why?" Explanations**: Human-readable narratives from protocols
- **Reasoner Integration**: Automatic trace creation and chain building

### Advanced Features (Optional)

- **Self-Rewarding**: Guide evaluates its own instruction quality before sending to Client
- **Self-Correction**: Guide revises instructions if quality is low
- **Partial Context**: Premise identification for efficiency (reduces context size)
- **Test-Time Scaling**: Majority voting across multiple evaluation samples

## Installation

```bash
# Install OpenHands SDK
pip install openhands-sdk openhands-tools

# TheGuide is part of the WAFT Pantheon
from waft.pantheon import TheGuide, Protocol, EvaluationScores
```

## Usage

### Basic Usage

```python
from pathlib import Path
import os
from openhands.sdk import LLM
from waft.pantheon import TheGuide

# Create Client LLM
client_llm = LLM(
    model="anthropic/claude-sonnet-4-5-20250929",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Create TheGuide
guide = TheGuide(
    project_path=Path.cwd(),
    client_llm=client_llm,
    guide_llm_config={
        "model": "anthropic/claude-sonnet-4-5-20250929",
        "api_key": os.getenv("ANTHROPIC_API_KEY")
    }
)

# Solve a problem
answer, protocol = guide.solve(
    problem_statement="How do I implement OAuth2 authentication in Python?",
    max_iterations=10,
    quality_threshold=0.8
)

print(f"Answer: {answer}")
print(f"Quality Score: {protocol.quality_score:.2f}")
```

### With Advanced Features

```python
# Enable self-rewarding and self-correction
guide = TheGuide(
    project_path=Path.cwd(),
    client_llm=client_llm,
    guide_llm_config={"model": "...", "api_key": "..."},
    enable_self_rewarding=True,   # Guide evaluates its own instructions
    enable_self_correction=True    # Guide revises instructions if quality is low
)

# Solve with test-time scaling (majority voting)
answer, protocol = guide.solve(
    problem_statement="Explain the CAP theorem",
    max_iterations=10,
    quality_threshold=0.8,
    use_partial_context=True,  # Use partial context for efficiency
    test_time_scaling=3         # 3 evaluation samples per step
)

# Access FVCU+Faithfulness scores
for evaluation in protocol.evaluations:
    print(f"Iteration {evaluation['iteration']}:")
    print(f"  Factuality: {evaluation['scores']['factuality']:.2f}")
    print(f"  Validity: {evaluation['scores']['validity']:.2f}")
    print(f"  Coherence: {evaluation['scores']['coherence']:.2f}")
    print(f"  Utility: {evaluation['scores']['utility']:.2f}")
    print(f"  Faithfulness: {evaluation['scores']['faithfulness']:.2f}")
    print(f"  Overall: {evaluation['scores']['overall']:.2f}")

    if evaluation.get('planning_detected'):
        print("  ⚠️ Forward-looking planning detected")

    if evaluation.get('unfaithful_reasoning_detected'):
        print("  ⚠️ Unfaithful reasoning detected")
```

### "Why?" Explanations

```python
# User asks: "Why did you arrive at this answer?"
explanation = guide.explain(protocol.session_id)
print(explanation)
```

**Output:**
```markdown
# Meta-Cognitive Guidance Explanation

## Problem Statement
How do I implement OAuth2 authentication in Python?

## Reasoning Chain (3 iterations)

### Iteration 1
**Instruction:**
Begin by identifying the key components of OAuth2...

**Reasoning:**
OAuth2 has four main components: Resource Owner, Client, Authorization Server...

**Evaluation (FVCU+Faithfulness):**
- Factuality: 0.95 - Grounded in facts?
- Validity: 0.90 - Logically correct?
- Coherence: 0.85 - Preconditions satisfied?
- Utility: 0.90 - Contributes to answer?
- Faithfulness: 1.00 - Claimed reasoning matches computation?
- Overall: 0.92

**Rationale:** Strong factual grounding and logical flow...

[... more iterations ...]

## Final Answer
To implement OAuth2 authentication in Python, use the `requests-oauthlib` library...

## Summary
- Total Iterations: 3
- Overall Quality Score: 0.88
- Evaluation Method: critic_model
```

## Integration with TheReasoner

TheGuide automatically creates reasoning traces in TheReasoner:

```python
from waft.pantheon import TheReasoner

# TheReasoner is automatically used by TheGuide
reasoner = TheReasoner(project_path=Path.cwd())

# View reasoning chains
recent_traces = reasoner.get_recent_traces(limit=10)
for trace in recent_traces:
    print(f"Trace {trace['trace_id']}: {trace['decision']}")

# Build chain from a session
trace_id = "trace_20260117_123456"
chain = reasoner.build_chain(trace_id)
print(f"Reasoning chain has {len(chain)} steps")
```

## Storage Structure

```
_pantheon/guide/
├── sessions/
│   └── session_YYYYMMDD_HHMMSS.json  # Full session data
├── protocols/
│   └── session_YYYYMMDD_HHMMSS.json  # Protocol for "Why?" queries
└── index.json                         # Session index
```

## Protocol Structure

Each session generates a Protocol (Pydantic model) containing:

```python
Protocol(
    session_id="session_20260117_123456",
    problem_statement="...",
    reasoning_chain=[
        {
            "iteration": 1,
            "instruction": "...",
            "reasoning_trace": "...",
            "timestamp": "2026-01-17T12:34:56"
        },
        # ... more steps
    ],
    evaluations=[
        {
            "iteration": 1,
            "scores": {
                "factuality": 0.95,
                "validity": 0.90,
                "coherence": 0.85,
                "utility": 0.90,
                "faithfulness": 1.00,
                "overall": 0.92
            },
            "rationale": "...",
            "strengths": ["...", "..."],
            "weaknesses": ["...", "..."],
            "recommendations": ["...", "..."],
            "should_continue": True,
            "planning_detected": False,
            "unfaithful_reasoning_detected": False
        },
        # ... more evaluations
    ],
    final_answer="...",
    quality_score=0.88,
    iteration_count=3,
    evaluation_method="critic_model",
    created="2026-01-17T12:34:56",
    completed="2026-01-17T12:45:12"
)
```

## Configuration Options

### TheGuide Constructor

```python
TheGuide(
    project_path: Optional[Path] = None,          # Project root (default: cwd)
    client_llm: Optional[LLM] = None,             # OpenHands LLM for client
    guide_llm_config: Optional[Dict] = None,      # Guide LLM config
    evaluation_config: Optional[Dict] = None,     # Evaluation settings
    enable_self_rewarding: bool = False,          # Self-rewarding capability
    enable_self_correction: bool = False          # Self-correction capability
)
```

### solve() Method

```python
guide.solve(
    problem_statement: str,               # Problem to solve
    max_iterations: int = 10,             # Maximum iterations
    quality_threshold: float = 0.8,       # Quality score threshold
    use_partial_context: bool = True,     # Partial context optimization
    test_time_scaling: int = 1            # Majority voting samples (1 = no scaling)
)
```

## Termination Logic

The guidance loop terminates when ANY of these conditions are met:

1. **Quality Threshold**: Overall score ≥ threshold (default: 0.8)
2. **Validity + Utility**: Both ≥ threshold (complementarity)
3. **Max Iterations**: Iteration count ≥ max_iterations (default: 10)
4. **Guide Assessment**: Guide says "should_continue: false"

## Research Foundations

TheGuide is based on recent research in meta-cognitive reasoning and evaluation:

1. **FVCU Taxonomy**: Multi-criteria evaluation of reasoning quality
   - Factuality, Validity, Coherence, Utility
   - Critic model approach (LLM-as-a-judge)

2. **Faithfulness Detection**: Identifying unfaithful reasoning
   - Detects claimed computation that doesn't actually occur
   - Ensures reasoning transparency

3. **Self-Rewarding Reasoning**: Guide evaluates its own instructions
   - Self-assessment of instruction quality
   - Self-correction loops

4. **Test-Time Scaling**: Majority voting for robust evaluation
   - Multiple evaluation samples
   - Aggregated scores via voting

## Future Enhancements (Self-Rewarding Training)

Based on RLHFlow research:

1. **Two-Stage Training Framework**:
   - Stage 1: Sequential rejection sampling for CoT trajectories
   - Stage 2: RL optimization (PPO/DPO) using correctness scores

2. **Self-Rewarding Capabilities**:
   - Guide evaluates its own instruction quality
   - Detects unclear or ineffective instructions
   - Revises instructions based on self-evaluation

3. **Training Data Generation**:
   - Sequential rejection sampling for high-quality guidance examples
   - Curated trajectories showing effective self-rewarding patterns
   - Fine-tuning Guide LLM on these examples

## API Reference

### TheGuide Class

- `solve(problem_statement, ...)` → Tuple[str, Protocol]
- `explain(session_id)` → str
- `get_protocol(session_id)` → Optional[Protocol]
- `get_recent_sessions(limit)` → List[Dict]
- `get_session_summary()` → Dict

### Protocol Class (Pydantic)

- `session_id`: str
- `problem_statement`: str
- `reasoning_chain`: List[Dict]
- `evaluations`: List[Dict]
- `final_answer`: str
- `quality_score`: float
- `iteration_count`: int
- `evaluation_method`: str
- `created`: str
- `completed`: Optional[str]
- `metadata`: Dict

### EvaluationScores Class (Pydantic)

- `factuality`: float (0.0-1.0)
- `validity`: float (0.0-1.0)
- `coherence`: float (0.0-1.0)
- `utility`: float (0.0-1.0)
- `faithfulness`: float (0.0-1.0)
- `overall`: float (0.0-1.0)

## Contributing

TheGuide is part of the WAFT Pantheon system. Contributions should:

1. Follow "as above, so below" Pantheon philosophy
2. Maintain file-based storage (no database)
3. Keep Protocol structure extensible
4. Integrate seamlessly with TheReasoner

## License

Part of the WAFT project.

---

*"As Above, So Below" - The Guide maintains the celestial loop of meta-cognitive guidance*
