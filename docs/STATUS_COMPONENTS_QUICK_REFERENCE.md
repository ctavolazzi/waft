# Status Components Quick Reference

**One-page reference for using status components in PDFs**

## Import

```python
from src.waft.evolution.status_components import (
    StatusComponentBuilder,
    create_status_components_from_status_dict
)
from scripts.waft_status import check_status
```

## Quick Usage

```python
# Get status and create all components
status = check_status()
components = create_status_components_from_status_dict(status)

# Use in PDF generation (TwoPageGenerator, ComponentPDFGenerator, etc.)
```

## Individual Components

```python
builder = StatusComponentBuilder()

# Progress Bar (NEW)
progress_comp = builder.build_progress_bar_component(
    label="Work Progress",
    current=3,
    total=5,
    show_percentage=True,
    show_fraction=True
)

# Status Badges (NEW)
badges_comp = builder.build_status_badges_component([
    {"label": "Valid", "status": "good", "icon": "✅"},
    {"label": "Warning", "status": "warning", "icon": "⚠️"},
], "System Status")

# Grouped Metrics (NEW - Phase 4)
grouped_comp = builder.build_grouped_metrics_component(
    "Epistemic Metrics",
    [
        {"label": "Knowledge", "value": "75.0", "unit": "%", "icon": "📊"},
        {"label": "Uncertainty", "value": "25.0", "unit": "%", "icon": "❓", "status": "warning"},
    ],
    description="Knowledge measurement indicators"
)

# Git Summary (NEW - Phase 4)
git_comp = builder.build_git_summary_component({
    "initialized": True,
    "branch": "main",
    "uncommitted_files": ["file1.py"],
    "recent_commits": ["abc123"]
})

# Work Efforts Summary (NEW - Phase 4)
we_comp = builder.build_work_efforts_summary_component({
    "count": 10,
    "active": ["WE-001", "WE-002"],
    "completed": ["WE-003", "WE-004"],
    "recent": ["WE-001"]
})

# Epistemic State
epistemic_comp = builder.build_epistemic_state_component({
    "initialized": True,
    "moon_phase": "🌓",
    "moon_phase_desc": "Moderate (65% coverage)",
    "knowledge_pct": 65.0,
    "uncertainty_pct": 35.0
})

# Gamification
gamification_comp = builder.build_gamification_component({
    "available": True,
    "level": 3,
    "integrity": 87.5,
    "insight": 450.0,
    "achievements_count": 2
})

# Flight Recorder
flight_comp = builder.build_flight_recorder_component(events, limit=5)

# Epistemic Phase
phase_comp = builder.build_epistemic_phase_component("Data Gathering")

# System Health
health_comp = builder.build_system_health_component({
    "pyrite_valid": True,
    "structure_valid": True,
    "lock_exists": True
})
```

## Component Properties

- `component_type`: `ComponentType.SECTION`
- `metadata.component_subtype`: Status-specific type
- `size_estimate`: 0.0-1.0 (page space estimate)
- `priority`: 0.0-1.0 (higher = more likely included)

## CSS Classes

- `.status-section` - Container
- `.epistemic-state` - Epistemic display box
- `.moon-phase` - Moon phase indicator
- `.phase-badge` - Phase badge
- `.gamification-table`, `.health-table`, `.metrics-table`, `.grouped-metrics-table` - Tables
- `.flight-events` - Event list
- `.progress-container`, `.progress-bar`, `.progress-fill` - Progress bars
- `.status-badges`, `.status-badge` - Status badges
- `.metrics-group` - Grouped metrics container
- `.git-summary`, `.work-efforts-summary` - Summary sections

## Integration

Works with:
- `TwoPageGenerator`
- `ComponentPDFGenerator`
- `DocumentEvolutionEngine`
- `OnePager`
