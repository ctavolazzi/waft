# Oracle Empirica Architecture Integration

TheOracle now fully integrates with Empirica's three-layer storage architecture and CASCADE workflow, providing a complete epistemic intelligence system.

## Architecture Overview

TheOracle follows Empirica's core architectural principles:

### 🗄️ Triple Storage
- **SQLite** - Fast queries for real-time monitoring
- **Git Notes** - Distributed, compressed (97% token reduction)
- **JSON Logs** - Full audit trail with reasoning

### 🔄 CASCADE Workflow
- **PREFLIGHT** - Assess what you know before starting
- **INVESTIGATE** - Reduce uncertainty (branch-based)
- **CHECK** - Decision gate (0-N times, confidence ≥ 0.7 → proceed)
- **ACT** - Execute with precision
- **POSTFLIGHT** - Measure learning deltas

### 📊 13 Epistemic Vectors
Structured confidence measurement across:
- **Tier 0 (Foundation)**: engagement, know, do, context
- **Tier 1 (Comprehension)**: clarity, coherence, signal, density
- **Tier 2 (Execution)**: state, change, completion, impact
- **Meta**: uncertainty

## Thinking Visualization

When you run `waft oracle`, TheOracle displays its complete cognitive process:

```
┌─ TheOracle - Epistemic Intelligence System ─────────────┐
│                                                          │
├─ CASCADE Workflow ────────────┬─ 13 Epistemic Vectors ─┤
│                               │                          │
│ 📊 PREFLIGHT                  │ Tier 0: Foundation      │
│   KNOW: 45%, UNCERT: 70%      │   Engagement: ████░░░░  │
│   → INVESTIGATE REQUIRED      │   Know: ███░░░░░░░░░░   │
│                               │   Do: ██████░░░░░░░░    │
│ 🔍 INVESTIGATE                │   Context: ████████░░   │
│   Found 3 relevant experiences│                          │
│                               │ Tier 1: Comprehension   │
│ ✅ CHECK                      │   Clarity: ██████░░░░   │
│   Confidence: 85%             │   Coherence: ███████░░   │
│   Gate: ≥ 0.7 → PROCEED      │   Signal: ████████░░    │
│   Decision: PROCEED           │   Density: █████░░░░░   │
│                               │                          │
│ 🎯 ACT                        │ Tier 2: Execution       │
│   Generating recommendation...│   State: ████████░░     │
│                               │   Change: ██████░░░░     │
│ 📈 POSTFLIGHT                 │   Completion: ████░░░░  │
│   ✓ Guidance provided        │   Impact: ████████░░     │
│   Δ KNOW: +0.25, Δ UNC: -0.30│                          │
│                               │ Uncertainty: ░░░░░░░░░░ │
│                               │ Confidence: ██████████   │
│                               │                          │
│                               │ Findings Stream:         │
│                               │   ✓ Pattern X works...   │
│                               │   ✓ Feature implemented │
│                               │                          │
│                               │ Unknowns:                │
│                               │   ? Edge case Y...       │
└───────────────────────────────┴──────────────────────────┘
┌─ Three-Layer Storage ────────────────────────────────────┐
│ Layer 1: SQLite                                           │
│   ✓ .empirica/sessions/sessions.db                        │
│   Fast queries, real-time monitoring                      │
│                                                            │
│ Layer 2: Git Notes                                        │
│   ✓ git notes (compressed)                                │
│   97% compression: 97% token reduction                    │
│   Distributed, crypto-signable                            │
│                                                            │
│ Layer 3: JSON Logs                                        │
│   ✓ .empirica/reflexes/*.json                             │
│   Full audit trail with reasoning                         │
└────────────────────────────────────────────────────────────┘
```

## Storage Architecture

### Layer 1: SQLite
**Location**: `.empirica/sessions/sessions.db`

**Purpose**: Fast SQL queries for dashboards

**Tables**:
- `sessions` - Session metadata
- `reflexes` - CASCADE checkpoints
- `goals` - Goal tracking
- `findings` - Validated knowledge
- `unknowns` - Knowledge gaps

**Access**: Real-time monitoring, analytics

### Layer 2: Git Notes
**Location**: `git notes add -m compressed_json`

**Purpose**: Distributed, crypto-signable state

**Compression**: 15,000 tokens → 450 tokens (97%)

**Access**: Git-native tools, remote sync

### Layer 3: JSON Logs
**Location**: `.empirica/reflexes/*.json`

**Purpose**: Full audit trail with reasoning

**Content**: Complete vectors + evidence + reasoning

**Access**: Debugging, research, compliance

## CASCADE Workflow Details

### PREFLIGHT
**Before starting work**: Assess what you actually know right now.

**13 Vectors Assessed**:
- engagement, know, do, context
- clarity, coherence, signal, density
- state, change, completion, impact
- uncertainty

**Decision**: High uncertainty → INVESTIGATE REQUIRED

### INVESTIGATE
**Reduce uncertainty** by:
- Reviewing past experiences (Oracle journal)
- Logging findings (`empirica finding-log`)
- Logging unknowns (`empirica unknown-log`)
- Branch-based investigation tree

### CHECK
**Decision gate** (0-N times during work):
- Confidence ≥ 0.7 → PROCEED
- Confidence < 0.7 → INVESTIGATE MORE
- Uses findings vs unknowns to calculate confidence

**Gate Logic**:
```python
confidence = (findings_count * 0.1) * (1.0 - uncertainty)

if confidence >= 0.7 and uncertainty < 0.3:
    decision = "PROCEED"
elif confidence < 0.3 or uncertainty > 0.7:
    decision = "HALT"
elif unknowns_count > findings_count:
    decision = "BRANCH"  # Need investigation
else:
    decision = "REVISE"  # Need refinement
```

### ACT
**Execute with precision**: Generate recommendation based on:
- Epistemic phase
- Knowledge coverage
- Findings and unknowns
- Reflection insights
- Check decision
- Learned patterns

### POSTFLIGHT
**Measure learning deltas**:
- Compare PREFLIGHT → POSTFLIGHT vectors
- Quantify learning: `Δ KNOW: +0.25, Δ UNC: -0.30`
- Verify calibration quality

## Epistemic State vs Git Diff

**Critical Distinction**:
- **Git Diff**: Tracks WHAT changed (code content)
- **Epistemic Vectors**: Track WHY and HOW CONFIDENT (reasoning quality)

**Example**:
- Large git diff (100 lines) + minimal epistemic change = Agent already knew solution
- Small git diff (5 lines) + massive epistemic change = Breakthrough understanding

Traditional metrics can't capture this distinction. Empirica does.

## Integration Points

### Python API (Preferred)
When `empirica` package is available:
- Direct `SessionDatabase` access
- `EpistemicAssessor` for 13-vector assessment
- `GitEnhancedReflexLogger` for atomic logging
- `HandoffGenerator` for AI-to-AI continuity

### CLI Fallback
If Python API unavailable:
- All operations use CLI commands
- Same interface, graceful degradation

### Oracle Journal
Oracle's own memory system complements Empirica:
- **Empirica**: Project-level epistemic tracking
- **Oracle Journal**: Oracle-specific interactions and learnings

Both systems work together for comprehensive tracking.

## Benefits

1. **Eliminates Confabulation** - Every recommendation based on verified epistemic state
2. **Maximizes Learning** - Explicit tracking of knowledge changes
3. **Decision Transparency** - Clear PROCEED/HALT/BRANCH/REVISE decisions
4. **97% Token Compression** - While preserving full epistemic state
5. **Triple-Layer Safety** - SQLite + Git Notes + JSON (atomic writes)
6. **Git-Native** - Epistemic state travels with code
7. **Real-Time Monitoring** - SQLite enables fast dashboards

## See Also

- [Empirica Architecture Documentation](https://empirica.ai/docs/architecture)
- [Oracle Empirica Workflow](ORACLE_EMPIRICA_WORKFLOW.md)
- [Oracle Journal & Memory](ORACLE_JOURNAL_MEMORY.md)
- [Empirica Python API](EMPIRICA_PYTHON_API.md)
