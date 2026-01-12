# Self-Engineering + Empirica Integration

**Date**: 2026-01-12  
**Status**: ✅ Implemented  
**Purpose**: Integrate Empirica epistemic tracking with self-engineering notebook system

---

## Overview

The self-engineering notebook system now integrates with Empirica to:
1. **Track epistemic state** - What the system knows about problems
2. **Log findings and unknowns** - Discoveries and knowledge gaps
3. **Decision support** - CHECK gates before creating actionables
4. **Learning measurement** - Track what the system learns from self-engineering

---

## Integration Points

### 1. Problem Journaling → Empirica Logging

**When**: Problem is detected and journaled

**What Happens**:
```python
# Problem detected → Auto-journaled
entry = notebook.journal_problem(problem)

# Automatically logs to Empirica:
# - Finding: "Problem detected: execution_failure - EOFError..."
# - Impact: Based on severity (critical=0.9, high=0.7, etc.)
# - Unknown: "Why does execution_failure occur? Root cause unknown."
```

**Benefits**:
- Problems tracked in Empirica's epistemic state
- Knowledge gaps automatically logged
- Impact scores help prioritize

---

### 2. Diagnosis Journaling → Empirica Findings

**When**: Diagnosis is made and journaled

**What Happens**:
```python
# Diagnosis made → Journaled
entry = notebook.journal_diagnosis(problem, diagnosis)

# Automatically logs to Empirica:
# - Finding: "Diagnosed: INTERACTIVE_INPUT_REQUIRED (confidence: 0.9)"
# - Impact: Based on confidence (0.5 + confidence * 0.4)
```

**Benefits**:
- Diagnoses tracked as discoveries
- Confidence scores inform impact
- Learning measured over time

---

### 3. Reflection → Empirica Insights

**When**: Reflection is created on findings

**What Happens**:
```python
# Reflection created
reflection = notebook.journal_reflection(
    entries=entries,
    insights=["System needs non-interactive mode"],
    patterns=["EOFError occurs in all non-interactive runs"],
    questions=["How to handle interactive input?"]
)

# Automatically logs to Empirica:
# - Findings: Each insight and pattern logged
# - Unknowns: Each question logged
```

**Benefits**:
- Insights tracked as findings
- Patterns recognized as discoveries
- Questions tracked as knowledge gaps

---

### 4. Actionable Creation → Empirica CHECK Gates

**When**: Creating work effort/scenario/quest from entry

**What Happens**:
```python
# Before creating work effort
work_effort = creator.create_work_effort_from_entry(entry)

# Empirica CHECK gate assesses:
# - Is this safe to proceed?
# - Do we need investigation first?
# - Should approach be revised?

# Gate results:
# - PROCEED: Safe to create work effort
# - HALT: Requires human approval
# - BRANCH: Need investigation first
# - REVISE: Approach needs revision
```

**Benefits**:
- Safety gates prevent dangerous operations
- Epistemic state informs decisions
- Uncertainty tracked and considered

---

## Epistemic State Integration

### Using Epistemic State for Decisions

```python
# Get epistemic state before making decisions
if empirica_manager.is_initialized():
    context = empirica_manager.project_bootstrap()
    epistemic_state = context.get("epistemic_state", {})
    vectors = epistemic_state.get("vectors", {})
    
    uncertainty = vectors.get("uncertainty", 0.5)
    know = vectors.get("foundation", {}).get("know", 0.0)
    
    # High uncertainty → Higher priority for learning
    if uncertainty > 0.7:
        priority = "HIGH"  # Need to learn more
    
    # Low knowledge → More investigation needed
    if know < 0.3:
        gate_result = "BRANCH"  # Need investigation
```

---

## Example: Full Flow with Empirica

```python
from waft.core.self_engineering import (
    ProblemDetector,
    NotebookManager,
    ActionableCreator
)
from waft.core.empirica import EmpiricaManager

# Initialize with Empirica
empirica = EmpiricaManager(project_path)
notebook = NotebookManager(project_path / "_notebook", empirica_manager=empirica)
detector = ProblemDetector(notebook_manager=notebook)
creator = ActionableCreator(
    project_path=project_path,
    work_efforts_dir=project_path / "_work_efforts",
    scenarios_dir=project_path / "examples",
    quests_dir=project_path / "src/gym/rpg/dungeons",
    empirica_manager=empirica
)

# 1. Problem detected → Auto-journaled + Empirica logged
problems = detector.monitor_execution(execution_result)
# ✓ Journaled in notebook
# ✓ Logged as finding in Empirica
# ✓ Unknown logged in Empirica

# 2. Diagnosis made → Journaled + Empirica logged
diagnosis_entry = notebook.journal_diagnosis(problem, diagnosis)
# ✓ Journaled in notebook
# ✓ Logged as finding in Empirica (with confidence)

# 3. Reflection created → Insights logged to Empirica
reflection = notebook.journal_reflection(entries, insights, patterns, questions)
# ✓ Journaled in notebook
# ✓ Insights logged as findings
# ✓ Questions logged as unknowns

# 4. Create work effort → Empirica CHECK gate
work_effort = creator.create_work_effort_from_entry(entry)
# ✓ Empirica CHECK gate assesses safety
# ✓ Epistemic state informs priority
# ✓ Work effort created if PROCEED
```

---

## Benefits

1. **Epistemic Tracking**: System knows what it knows about problems
2. **Learning Measurement**: Track what the system learns from self-engineering
3. **Decision Support**: CHECK gates prevent dangerous operations
4. **Knowledge Gaps**: Unknowns automatically tracked
5. **Priority Adjustment**: Epistemic state informs priority decisions

---

## Future Enhancements

1. **Preflight/Postflight**: Submit epistemic assessments before/after self-engineering iterations
2. **Goal Management**: Create Empirica goals for self-engineering objectives
3. **Trajectory Projection**: Project epistemic trajectory of self-engineering
4. **Drift Detection**: Detect when self-engineering approach drifts

---

**The notebook system now uses Empirica to track epistemic state and make better decisions about self-engineering.**
