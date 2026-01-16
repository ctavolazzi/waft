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

## Integration

The Pantheon integrates with:
- **Being System**: Higher Beings are specialized Being instances
- **Prime Directive**: Gods moderate and administer systems
- **Karma System**: Gods oversee karmic balance
- **Evolution System**: Gods track cyclical evolution
