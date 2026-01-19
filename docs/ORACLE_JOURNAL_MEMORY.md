# Oracle Journal & Memory System

The Oracle maintains its own journal and memory system to track consultations, learn patterns, and build persistent knowledge.

## Overview

The Oracle Journal system:
- **Tracks all consultations** - Every question asked and guidance given
- **Remembers insights** - Stores important discoveries with impact scores
- **Learns patterns** - Identifies what works in different epistemic phases
- **Builds memory** - Creates a knowledge base of successful recommendations
- **Tracks evolution** - Monitors epistemic state over time

## Storage Location

All Oracle journal and memory data is stored in:
```
.empirica/oracle_journal/
├── journal.jsonl          # All consultations and assessments (JSONL format)
├── memory.json            # Oracle's memory (insights, recommendations, history)
└── patterns.json          # Learned patterns (keywords, phase recommendations, gate outcomes)
```

## Journal Structure

### Journal Entries (journal.jsonl)

Each line is a JSON object representing one interaction:

**Consultation Entry:**
```json
{
  "type": "consultation",
  "timestamp": "2026-01-17T07:30:00",
  "question": "What should we focus on next?",
  "epistemic_phase": "Data Gathering",
  "knowledge_coverage": 0.25,
  "uncertainty": 0.75,
  "recommendation": "...",
  "personality": {...},
  "epistemic_state": {...}
}
```

**Assessment Entry:**
```json
{
  "type": "assessment",
  "timestamp": "2026-01-17T07:35:00",
  "decision": "Implement feature X",
  "gate_result": "PROCEED",
  "recommendation": "...",
  "epistemic_phase": "Exploration",
  "unknowns_count": 2
}
```

### Memory (memory.json)

Structured memory of Oracle's experiences:

```json
{
  "insights": [
    {
      "insight": "Pattern X works well in Synthesis phase",
      "impact": 0.8,
      "timestamp": "...",
      "context": {...}
    }
  ],
  "successful_recommendations": [
    {
      "recommendation": "...",
      "outcome": "Feature implemented successfully",
      "epistemic_phase": "Synthesis",
      "timestamp": "..."
    }
  ],
  "learned_patterns": [...],
  "epistemic_history": [
    {
      "timestamp": "...",
      "phase": "Data Gathering",
      "coverage": 0.2,
      "uncertainty": 0.8
    }
  ],
  "consultation_count": 42,
  "first_consultation": "2026-01-10T...",
  "last_consultation": "2026-01-17T..."
}
```

### Patterns (patterns.json)

Learned patterns from experience:

```json
{
  "question_patterns": {
    "architecture": 5,
    "implementation": 8,
    "testing": 3
  },
  "phase_recommendations": {
    "Data Gathering": [
      "Focus on collecting data...",
      "Gather observations..."
    ],
    "Synthesis": [
      "Synthesize findings...",
      "Identify patterns..."
    ]
  },
  "gate_outcomes": {
    "PROCEED": 15,
    "HALT": 3,
    "BRANCH": 5,
    "REVISE": 2
  }
}
```

## Usage

### View Memory Summary

```bash
waft oracle-journal --memory
```

Shows:
- Total consultations
- Insights remembered
- Successful recommendations
- Epistemic history length
- Learned patterns summary

### View Recent Consultations

```bash
waft oracle-journal --show --limit 20
```

Shows last N consultations with:
- Question asked
- Epistemic phase
- Knowledge coverage
- Timestamp

### Search Memory

```bash
waft oracle-journal --search "architecture" --limit 10
```

Searches:
- Insights
- Successful recommendations
- Returns matching entries

### View Learned Patterns

```bash
waft oracle-journal --patterns
```

Shows:
- Top question keywords
- Recommendations by phase
- Gate outcome statistics

## Reflection System

Before providing guidance, The Oracle **reflects** on:
- **Past similar consultations** - Searches memory for relevant experiences
- **Relevant insights** - Finds insights related to the question
- **Learned patterns** - Reviews patterns for the current epistemic phase
- **Epistemic trajectory** - Analyzes how knowledge has evolved recently

The reflection happens automatically before every `provide_guidance()` call, ensuring recommendations are informed by past experiences.

### Reflection Process

1. **Search Memory** - Finds relevant past experiences matching the question
2. **Extract Insights** - Identifies relevant insights from memory
3. **Review Patterns** - Checks learned patterns for the current phase
4. **Analyze Trajectory** - Examines epistemic state trends (improving/declining/clarifying)
5. **Generate Summary** - Creates a reflection summary for display

The reflection is included in the guidance response and displayed in the CLI output.

## Automatic Logging

The Oracle automatically logs:
- **Every consultation** - When `provide_guidance()` is called (includes reflection)
- **Every assessment** - When `assess_decision()` is called
- **Every insight** - When `log_insight()` is called
- **Successful recommendations** - When explicitly remembered

## Memory Integration

The Oracle uses its memory when providing guidance:
- **Learned patterns** - Uses successful recommendations from similar phases
- **Question patterns** - Identifies common question types
- **Epistemic history** - Tracks how knowledge evolves over time
- **Gate outcomes** - Learns which decisions are typically safe

## Memory Methods

### Programmatic Access

```python
from waft.core.science import TheOracle

oracle = TheOracle(project_path)

# Get memory summary
summary = oracle.get_memory_summary()

# Search memory
results = oracle.search_memory("architecture", limit=10)

# Remember successful recommendation
oracle.remember_successful_recommendation(
    recommendation="Focus on testing first",
    outcome="Tests caught bugs early",
    epistemic_phase="Exploration"
)
```

## Memory Limits

To prevent unbounded growth:
- **Insights**: Top 50 by impact
- **Successful recommendations**: Last 100
- **Epistemic history**: Last 100 points
- **Phase recommendations**: Last 20 per phase
- **Question patterns**: All keywords (can be pruned manually)

## Integration with Empirica

Oracle journal complements Empirica:
- **Empirica**: Tracks epistemic state, findings, unknowns (project-level)
- **Oracle Journal**: Tracks Oracle-specific interactions and learnings (Oracle-level)

Both systems work together to provide comprehensive epistemic tracking.
