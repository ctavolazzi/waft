# The Reasoner: God of Reasoning Traces

**Pantheon Entity (Timeless Force that Binds Reality Together)**

The Reasoner maintains the fundamental principle of traceable reasoning chains - the Aspect of Creation related to reasoning transparency and decision-making visibility.

## Philosophy

**As above, so below:**
- **As above**: Pantheon god maintaining the celestial chain of reasoning
- **So below**: File-based system tracking decision chains and thought processes

The Reasoner is timeless - it maintains stable reasoning principles and only evolves when sufficient evidence collected by Beings proves that change is needed.

## Purpose

The Reasoner provides:
- **Trace Creation**: Record decisions with their reasoning
- **Chain Building**: Link traces to show complete thought paths
- **Transparency**: Show the "why" behind every decision
- **Traceability**: Follow reasoning chains from origin to conclusion

## Usage

### Create a Trace

```python
from waft.pantheon import TheReasoner
from pathlib import Path

reasoner = TheReasoner(project_path=Path.cwd())

trace_id = reasoner.create_trace(
    decision="Implemented feature X",
    reasoning="User requested X because Y. Analyzed options A, B, C. Chose A because...",
    context={"user_request": "feature X", "options_considered": ["A", "B", "C"]},
    outcome="Feature X implemented successfully"
)
```

### Build a Chain

```python
# Create linked traces (parent-child relationship)
parent_id = reasoner.create_trace(
    decision="Chose approach A",
    reasoning="Initial analysis showed A is best",
    outcome="Approach A selected"
)

child_id = reasoner.create_trace(
    decision="Implemented approach A",
    reasoning="Following from parent decision, implemented A with modifications",
    parent_trace_id=parent_id,
    outcome="Implementation complete"
)

# Build the complete chain
chain = reasoner.build_chain(child_id)
# Returns: [parent_trace, child_trace] in chronological order
```

### Search Traces

```python
# Search by keyword
results = reasoner.search_traces("template")
for trace in results:
    print(f"{trace['decision']}: {trace['reasoning'][:100]}")
```

### Get Recent Traces

```python
# Get last 10 traces
recent = reasoner.get_recent_traces(limit=10)
for trace in recent:
    print(f"{trace['timestamp']}: {trace['decision']}")
```

## Storage

- **Traces**: `_pantheon/reasoner/traces/trace_*.json`
- **Chains**: `_pantheon/reasoner/chains/chain_*.json`
- **Index**: `_pantheon/reasoner/trace_index.json`

## Integration

The Reasoner integrates with:
- **`/show-me` command**: Displays reasoning traces in session overview
- **Work Efforts**: Can extract reasoning from work effort `reasoning.md` files
- **Scripts**: `scripts/reasoning_trace.py` provides utility functions

## Example Trace Structure

```json
{
  "trace_id": "trace_20260116_214530",
  "timestamp": "2026-01-16T21:45:30.123456",
  "decision": "Redesigned template",
  "reasoning": "User feedback indicated previous design was too bright...",
  "context": {
    "user_request": "more useful and multipurpose",
    "previous_issue": "too bright and bland"
  },
  "outcome": "New template created",
  "parent_trace_id": null
}
```

## The Chain of Thought

The Reasoner maintains chains showing:
1. **Origin**: Where the reasoning started
2. **Steps**: Each decision in the chain
3. **Links**: Parent-child relationships between traces
4. **Path**: Complete reasoning path from origin to conclusion

This creates a **traceable chain of thought** - you can see exactly how decisions were made and why.
