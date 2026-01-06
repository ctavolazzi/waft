# AI Narrative Guide - Contributing to the TavernKeeper Chronicle

This guide shows how AI assistants (Cursor, Claude, etc.) can contribute narratives, observations, and reflections to the TavernKeeper system, making development a collaborative, story-driven experience.

## Quick Start

```python
from waft.core.tavern_keeper.ai_helper import (
    quick_observe,
    quick_note,
    celebrate_moment,
    raise_concern,
)

# Log an observation
quick_observe("woah that's kinda sick", mood="surprised")

# Celebrate something beautiful
celebrate_moment("that's so beautiful wow holy cannoli I love this")

# Note a concern
raise_concern("weird that's not right", concern_type="bug")

# Log a general note
quick_note("Refactored the authentication module", category="refactor")
```

## When to Contribute

### Observations (`quick_observe`)
Use when you notice something interesting, surprising, or noteworthy:
- "The code structure here is really elegant"
- "This pattern appears multiple times - potential refactor?"
- "The error handling is comprehensive"

### Celebrations (`celebrate_moment`)
Use for moments of beauty, delight, or achievement:
- "The dashboard looks amazing!"
- "This refactor is so clean and beautiful"
- "The narrative system is working perfectly"

### Concerns (`raise_concern`)
Use when something seems off or needs attention:
- "This might cause a performance issue"
- "The error message could be clearer"
- "There's a potential race condition here"

### Notes (`quick_note`)
Use for general observations, changes, or insights:
- "Fixed bug in authentication"
- "Added new feature for user profiles"
- "Refactored to improve maintainability"

## Moods

Available moods for observations:
- `neutral` - Standard observation
- `surprised` - "woah that's kinda sick"
- `delighted` - "that's so beautiful wow"
- `concerned` - "weird that's not right"
- `amazed` - "holy cannoli I love this"

## Categories

Available categories for notes:
- `bug` - Bug fixes or bug reports
- `feature` - New features
- `refactor` - Code refactoring
- `insight` - Insights or realizations
- `design` - Design decisions
- `performance` - Performance improvements
- `general` - General notes

## Advanced Usage

For more control, use the Narrator class directly:

```python
from waft.core.tavern_keeper import TavernKeeper, Narrator
from pathlib import Path

tavern = TavernKeeper(Path("."))
narrator = Narrator(tavern)

# Log with context
narrator.observe(
    "The refactor is complete",
    context={"files_changed": 5, "lines_removed": 200},
    mood="delighted",
    source="ai",
)

# Add a reflection
narrator.reflect(
    "The codebase is becoming more maintainable",
    trigger="refactor_complete",
    insight="Modular design improves clarity",
)

# Log a celebration
narrator.celebrate(
    "The dashboard is live and beautiful!",
    achievement="dashboard_complete",
)
```

## Viewing Narratives

All narratives appear in:
- `waft journal` - View all journal entries
- `waft dashboard` - Live dashboard with narrative entries highlighted
- Adventure journal in `_pyrite/.waft/chronicles.json`

## Example Workflow

```python
# AI assistant working on a feature
from waft.core.tavern_keeper.ai_helper import quick_observe, celebrate_moment

# Start working
quick_observe("Starting implementation of new feature", mood="neutral")

# Notice something interesting
quick_observe("The existing pattern here is really elegant", mood="delighted")

# Complete the feature
celebrate_moment("Feature complete! The code is clean and beautiful")

# All of these appear in the chronicle and dashboard!
```

## Integration with Development

The Narrator system integrates seamlessly with:
- Command hooks (automatic narratives on commands)
- Dashboard (narratives appear in real-time)
- Journal (all narratives are logged)
- Character progression (narratives are part of the story)

Make development a collaborative, narrative-driven experience where AI and human co-create the story of the codebase!

