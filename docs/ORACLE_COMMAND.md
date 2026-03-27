# Oracle Command

**Date**: 2026-01-12  
**Status**: ✅ Implemented  
**Command**: `/oracle` or `waft oracle`

---

## Overview

The `/oracle` command consults TheOracle for epistemic insights and guidance based on Empirica state.

---

## Usage

### Basic Consultation

```bash
waft oracle
```

or in Cursor:

```
/oracle
```

### With Question

```bash
waft oracle "How should we proceed with FlightRecorder integration?"
```

or in Cursor:

```
/oracle "How should we proceed with FlightRecorder integration?"
```

### Decision Assessment

```bash
waft oracle --assess "Implement FlightRecorderEpistemicAdapter"
```

or in Cursor:

```
/oracle assess "Implement FlightRecorderEpistemicAdapter"
```

---

## What It Does

1. **Gets Epistemic State**: Retrieves current knowledge, uncertainty, engagement from Empirica
2. **Displays Vectors**: Shows epistemic vectors in a table
3. **Shows Insights**: Lists recent findings logged to Empirica
4. **Shows Unknowns**: Lists open knowledge gaps
5. **Provides Guidance**: Generates recommendations based on epistemic state
6. **Assesses Decisions**: Uses Empirica CHECK gates for decision support (`PROCEED | INVESTIGATE | HALT | BRANCH | REVISE`)

---

## Output

### Epistemic State Display

```
Epistemic Phase: Exploration

┏━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Vector        ┃ Value   ┃ Interpretation              ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Knowledge     │ 45%     │ Low knowledge               │
│ Uncertainty   │ 65%     │ High uncertainty            │
│ Engagement    │ 30%     │ Low engagement              │
└───────────────┴─────────┴────────────────────────────┘
```

### Recent Insights

```
Recent Insights:
  1. TheObserver verified clean - no Empirica usage
  2. TheOracle created with full Empirica integration
  3. FlightRecorderEpistemicAdapter hypothesis created
```

### Open Unknowns

```
Open Unknowns:
  1. How to implement FlightRecorderEpistemicAdapter pattern extraction?
  2. What event patterns best map to epistemic vectors?
```

### Guidance Panel

```
🔮 Oracle Guidance:
╭──────────────────────────── Recommendation ────────────────────────────╮
│ Low knowledge coverage (0%). Focus on addressing unknowns: 2 open      │
│ questions.                                                              │
╰─────────────────────────────────────────────────────────────────────────╯
```

### Decision Assessment

```
Decision Assessment:
  Gate Result: PROCEED
  Recommendation: Safe to proceed. Epistemic state supports this operation.
```

---

## Integration

- **Uses**: TheOracle (epistemic intelligence)
- **Requires**: Empirica initialized
- **Integrates**: TavernKeeper (for command hooks)

---

## Examples

### Example 1: General Consultation

```bash
$ waft oracle

🔮 Waft - Consulting TheOracle

→ Gathering epistemic state...
✓ Epistemic state retrieved

Epistemic Phase: Exploration

[Vectors table displayed]

Recent Insights:
  1. TheObserver verified clean - no Empirica usage
  2. TheOracle created with full Empirica integration

🔮 Oracle Guidance:
[Recommendation panel]
```

### Example 2: Specific Question

```bash
$ waft oracle "What should we focus on next?"

🔮 Waft - Consulting TheOracle

→ Seeking guidance: What should we focus on next?

🔮 Oracle Guidance:
╭──────────────────────────── Recommendation ────────────────────────────╮
│ Focus on addressing unknowns: 2 open questions should be investigated. │
╰─────────────────────────────────────────────────────────────────────────╯
```

### Example 3: Decision Assessment

```bash
$ waft oracle --assess "Implement FlightRecorderEpistemicAdapter"

🔮 Waft - Consulting TheOracle

→ Assessing decision: Implement FlightRecorderEpistemicAdapter

Decision Assessment:
  Gate Result: PROCEED
  Recommendation: Safe to proceed. Epistemic state supports this operation.
```

---

## Error Handling

If Empirica is not initialized:

```
⚠️  Empirica not fully initialized
  Message: Empirica not initialized or no context available

🔮 Oracle Basic Guidance:
[Basic recommendation panel]
```

The command still provides basic guidance even without full Empirica context.

---

**The `/oracle` command is now available for epistemic intelligence and guidance.**
