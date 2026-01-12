# Prior Efforts Tracker

**Tool**: `prior_efforts_tracker.py`  
**Purpose**: Track evolution attempts and prior efforts for work effort reproduction

---

## Overview

The Prior Efforts Tracker logs and tracks all attempts, iterations, and evolution efforts made by Beings to accomplish a work effort. This creates a learning history that future Beings can reference.

---

## Usage

### Python API

```python
from pathlib import Path
from prior_efforts_tracker import PriorEffortsTracker

tracker = PriorEffortsTracker(Path("_work_efforts/WE-260112-l7tt_..."))

# Log an attempt
tracker.log_attempt(
    attempt_id="attempt_001",
    description="Initial implementation of TheCampfire class",
    approach="Created single-file implementation with http.server",
    status="succeeded",
    outcome="Successfully created full-stack application",
    lessons_learned=[
        "Python's http.server is sufficient for simple apps",
        "Observer pattern works well for story events",
        "LRU cache improves performance for story retrieval"
    ],
    files_created=["src/waft/core/campfire.py"],
    being_id="being_001",
    generation=1
)

# Get prior efforts
efforts = tracker.get_prior_efforts(status="succeeded")

# Get statistics
stats = tracker.get_statistics()

# Export markdown report
tracker.export_markdown()
```

### CLI Usage

```bash
# List all prior efforts
python tools/prior_efforts_tracker.py _work_efforts/WE-260112-l7tt_... list

# Show statistics
python tools/prior_efforts_tracker.py _work_efforts/WE-260112-l7tt_... stats

# Show lessons learned
python tools/prior_efforts_tracker.py _work_efforts/WE-260112-l7tt_... lessons

# Show common errors
python tools/prior_efforts_tracker.py _work_efforts/WE-260112-l7tt_... errors

# Export markdown report
python tools/prior_efforts_tracker.py _work_efforts/WE-260112-l7tt_... export
```

---

## Data Structure

Prior efforts are stored in `tools/prior_efforts.json`:

```json
[
  {
    "attempt_id": "attempt_001",
    "timestamp": "2026-01-12T12:00:00",
    "description": "Initial implementation",
    "approach": "Single-file approach",
    "status": "succeeded",
    "outcome": "Successfully created",
    "lessons_learned": ["Lesson 1", "Lesson 2"],
    "files_created": ["file1.py"],
    "files_modified": ["file2.py"],
    "errors_encountered": ["Error 1"],
    "being_id": "being_001",
    "generation": 1
  }
]
```

---

## Integration with Spec Sheet

The spec sheet should include a "Prior Efforts" section that references this tracker and summarizes key learnings from prior attempts.

---

## Benefits

1. **Learning from History**: Beings can see what worked and what didn't
2. **Avoiding Repeated Mistakes**: Common errors are tracked
3. **Building on Success**: Successful approaches are documented
4. **Evolution Tracking**: Generations and Being IDs track evolution
5. **Reproducibility**: Clear record of how work effort was accomplished

---

**This tool helps Beings learn from the past to build better futures.**
