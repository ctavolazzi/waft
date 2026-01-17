# How to Use the Reasoning Trace System

**The Reasoner** is the God of Reasoning Traces - a Pantheon Entity that maintains traceable chains of thought.

## Quick Start

### 1. Create a Trace

```python
from waft.pantheon import TheReasoner
from pathlib import Path

reasoner = TheReasoner(project_path=Path.cwd())

# Create a trace when you make a decision
trace_id = reasoner.create_trace(
    decision="Chose to use WeasyPrint for PDF generation",
    reasoning="Compared WeasyPrint, ReportLab, and FPDF2. WeasyPrint won because: 1) Template-based approach fits WAFT architecture, 2) Full CSS control, 3) Team has web dev background, 4) Professional typography out of box",
    context={
        "options_considered": ["WeasyPrint", "ReportLab", "FPDF2"],
        "criteria": ["template-based", "CSS control", "team skills", "typography"]
    },
    outcome="WeasyPrint integrated successfully"
)
```

### 2. Build Reasoning Chains

```python
# Create linked traces (shows decision path)
parent_id = reasoner.create_trace(
    decision="User wants template redesign",
    reasoning="User feedback: 'too bright and bland'",
    outcome="Decision to redesign"
)

child_id = reasoner.create_trace(
    decision="Created clean, functional template",
    reasoning="Focused on information-first, utility over aesthetics",
    parent_trace_id=parent_id,
    outcome="New template created"
)

# Build the complete chain
chain = reasoner.build_chain(child_id)
# Shows: [parent_trace, child_trace] - the full reasoning path
```

### 3. View Traces in /show-me

```bash
# See reasoning traces in HTML (opens automatically)
/show-me --output trace.html

# See in markdown
/show-me --format markdown

# See in table format
/show-me --format table
```

### 4. Search Traces

```python
# Search for traces about templates
results = reasoner.search_traces("template")
for trace in results:
    print(f"{trace['decision']}")
    print(f"  Why: {trace['reasoning']}")
```

## Integration Points

### In Your Code

```python
from waft.pantheon import TheReasoner

reasoner = TheReasoner()

# When making a decision
def implement_feature():
    trace_id = reasoner.create_trace(
        decision="Implementing feature X",
        reasoning="User requested X. Analyzed Y and Z approaches. Chose Y because...",
        context={"user_request": "feature X"},
        outcome="Feature X implemented"
    )
    # ... do the work ...
    return trace_id
```

### In Work Efforts

Create `reasoning.md` in your work effort directory:

```markdown
# Reasoning for WE-260116-xxxx

## Decision
Implemented feature X

## Reasoning
User requested X because Y. We considered options A, B, C.
Chose A because:
- Reason 1
- Reason 2
- Reason 3

## Outcome
Feature X implemented successfully
```

The `/show-me` command will automatically extract this!

### Using Scripts

```python
from scripts.reasoning_trace import create_reasoning_trace_entry

# Quick trace creation
trace_file = create_reasoning_trace_entry(
    decision="Fixed bug in template",
    reasoning="Bug was caused by X. Fixed by doing Y.",
    context={"bug_id": "123", "fix_approach": "Y"},
    outcome="Bug fixed, tests passing"
)
```

## What Gets Traced

- **Decisions**: What was decided
- **Reasoning**: WHY it was decided (the chain of thought)
- **Context**: Additional information (user requests, options considered, etc.)
- **Outcome**: What happened as a result
- **Parent Links**: How decisions connect (reasoning chains)

## Storage Locations

- **Pantheon Traces**: `_pantheon/reasoner/traces/trace_*.json`
- **Work Effort Traces**: `_work_efforts/reasoning_traces/trace_*.json`
- **Work Effort Reasoning**: `_work_efforts/WE-*/reasoning.md`

All are automatically discovered by `/show-me`!

## Example Workflow

1. **Make a decision** → Create trace with The Reasoner
2. **Implement** → Create child trace linking to parent
3. **View chain** → Use `/show-me` to see the reasoning path
4. **Search** → Find related decisions and reasoning

This creates a **traceable chain of thought** - you can always see how and why decisions were made!
