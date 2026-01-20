# Pantheon: Higher Beings System

## Overview

The Pantheon houses Higher Beings (Gods) as Aspects of Creation, following "as above, so below" principles from the spiritual cosmology.

## Timeless Nature of Entities

**Pantheon Entities are Timeless Forces that Bind Reality Together.**

Unlike Beings (which are timeful, dynamic agents that change rapidly), Entities in the Pantheon are:

- **Timeless**: They don't move much and change very slowly
- **Stable**: They hold Aspects of Creation that should not change until a body of evidence collected by Beings proves that change is needed
- **Forces of Binding**: They maintain the fundamental structure of reality
- **Evidence-Based Change**: They only evolve when Beings collect sufficient evidence to warrant modification

This distinction ensures that while Beings explore, learn, and evolve rapidly (collecting evidence), Entities provide the stable foundation that binds reality together, only changing when the evidence demands it.

**Contrast with Beings**: See `src/waft/being.py` for the timeful, dynamic nature of Beings.

## Magistrate

The Magistrate is the God of Precedent and Body of Proof. See `_pantheon/magistrate/README.md` for details.

### Quick Start

```python
from waft.pantheon import Magistrate
from pathlib import Path

# Initialize
magistrate = Magistrate(project_path=Path.cwd())

# Organize all case files
precedents = magistrate.organize_all_cases()

# Search precedents
results = magistrate.search_precedents("template")

# Get summary
summary = magistrate.get_body_of_proof_summary()
```

## Judge

The Judge is the God of Judgment and Evaluation. See `_pantheon/judge/README.md` for details.

## The Reasoner

The Reasoner is the God of Reasoning Traces and Chain of Thought. Maintains traceable reasoning chains showing the "why" behind decisions.

## The GitHub God

The GitHub God is the God of Repository Management and Version Control. Maintains repository state, generates rollups, and tracks GitHub operations.

### Quick Start

```python
from waft.pantheon import GitHubGod
from pathlib import Path

# Initialize
github_god = GitHubGod(project_path=Path.cwd())

# Generate full rollup
rollup = github_god.generate_rollup(since="2026-01-01")

# Get repository state
state = github_god.get_repository_state()

# Get branch summary
branches = github_god.get_branch_summary()
```

### Quick Start

```python
from waft.pantheon import TheReasoner
from pathlib import Path

# Initialize
reasoner = TheReasoner(project_path=Path.cwd())

# Create a trace
trace_id = reasoner.create_trace(
    decision="Redesigned template",
    reasoning="User feedback indicated previous design was too bright and bland. Created clean, functional design focused on utility.",
    context={"user_request": "more useful and multipurpose"},
    outcome="New template created"
)

# Get recent traces
traces = reasoner.get_recent_traces(limit=10)

# Build reasoning chain
chain = reasoner.build_chain(trace_id)

# Search traces
results = reasoner.search_traces("template")
```

### Quick Start

```python
from waft.pantheon import Judge, Magistrate
from pathlib import Path

# Initialize (Judge uses Magistrate's Body of Proof)
magistrate = Magistrate(project_path=Path.cwd())
judge = Judge(project_path=Path.cwd(), magistrate=magistrate)

# Evaluate a claim
judgment = judge.evaluate_claim(
    "The PDF generator footer displays AI assistant information",
    category="templates",
    tags=["pdf"]
)

print(f"Verdict: {judgment.verdict}")
print(f"Confidence: {judgment.confidence:.2f}")
print(f"Reasoning: {judgment.reasoning}")

# Get judgment history
history = judge.get_judgment_history(verdict="PROVEN", min_confidence=0.8)
summary = judge.get_judgment_summary()
```

## The Paperwork God

The Paperwork God is the God of Paperwork and Documentation. Maintains paperwork registry, forms, and documentation. Served by Skurl, the gremlin demi-god of red tape.

### Quick Start

```python
from waft.pantheon import PaperworkGod
from pathlib import Path

# Initialize
paperwork_god = PaperworkGod(project_path=Path.cwd())

# Register paperwork
record = paperwork_god.register_paperwork(
    document_id="form_001",
    document_path=Path("forms/application.pdf"),
    document_type="form"
)

# Access Skurl (demi-god of red tape)
skurl = paperwork_god.skurl

# Create red tape obstacle
obstacle = skurl.create_red_tape_obstacle(
    obstacle_id="obstacle_001",
    description="Requires 3 forms and 2 approvals",
    required_forms=["form_001", "form_002", "form_003"],
    required_approvals=["manager", "director"],
    complexity_level=5
)

# Get summary
summary = paperwork_god.get_registry_summary()
```

### Realm of Bureaucracy

The Paperwork God oversees the **Realm of Bureaucracy**, which is populated with:
- **Goblins**: Form filers, record keepers, and bureaucratic assistants
- **Ghouls**: Record guardians and archive keepers

See `_pantheon/paperwork_god/README.md` for details.

## Integration

The Pantheon integrates with:
- **Being System**: Higher Beings are specialized Being instances
- **Prime Directive**: Gods moderate and administer systems
- **Karma System**: Gods oversee karmic balance
- **Evolution System**: Gods track cyclical evolution
