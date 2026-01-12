# Status Components Guide

**Reusable PDF components for WAFT Kernel Status Reports**

## Overview

The `status_components` module provides specialized, reusable components for generating PDFs that display WAFT system status information, including epistemic state, gamification metrics, Flight Recorder events, and system health.

## Quick Start

```python
from src.waft.evolution.status_components import (
    StatusComponentBuilder,
    create_status_components_from_status_dict
)
from scripts.waft_status import check_status

# Get status
status = check_status()

# Create components
components = create_status_components_from_status_dict(status)

# Use in PDF generation
# (components are DocumentComponent objects ready for TwoPageGenerator)
```

## Available Components

### 1. Progress Bar Component ⭐ NEW

Displays visual progress bars with percentage and fraction (inspired by AI-DnD quest progress).

```python
component = builder.build_progress_bar_component(
    label="Work Effort Progress",
    current=3,
    total=5,
    show_percentage=True,
    show_fraction=True
)
```

**Features:**
- Visual progress bar with fill animation
- Percentage display (e.g., "60.0%")
- Fraction display (e.g., "3/5")
- Configurable display options
- Automatic percentage calculation

**Use Cases:**
- Work effort completion tracking
- Epistemic knowledge progress
- Gamification level progress
- Any metric with current/total values

### 2. Status Badges Component ⭐ NEW

Displays compact status indicators as badges (inspired by AI-DnD status effects).

```python
badges = [
    {"label": "Pyrite Valid", "status": "good", "icon": "✅"},
    {"label": "No Lock File", "status": "warning", "icon": "⚠️"},
    {"label": "Structure Invalid", "status": "error", "icon": "❌"},
]
component = builder.build_status_badges_component(badges, "System Health")
```

**Features:**
- Color-coded status (good/warning/error/info)
- Icon support (emoji or text)
- Compact display
- Flexible badge configuration

**Status Types:**
- `good` - Green background, positive status
- `warning` - Orange background, caution
- `error` - Red background, problem
- `info` - Neutral background, information

**Use Cases:**
- System health indicators
- Epistemic state badges
- Quick status overview
- Multiple status indicators in one component

### 3. Epistemic State Component

Displays moon phase indicator, knowledge percentage, and uncertainty percentage.

```python
builder = StatusComponentBuilder()
component = builder.build_epistemic_state_component({
    "initialized": True,
    "moon_phase": "🌓",
    "moon_phase_desc": "Moderate (65% coverage)",
    "knowledge_pct": 65.0,
    "uncertainty_pct": 35.0
})
```

**Features:**
- Moon phase emoji and description
- Knowledge percentage display
- Uncertainty percentage display
- Graceful degradation when Empirica not initialized

### 2. Gamification Component

Displays character level, integrity score, insight points, and achievements.

```python
component = builder.build_gamification_component({
    "available": True,
    "level": 3,
    "integrity": 87.5,
    "insight": 450.0,
    "achievements_count": 2
})
```

**Features:**
- Table format for metrics
- Character level display
- Integrity score percentage
- Insight points counter
- Achievements count

### 3. Flight Recorder Component

Displays recent evolutionary events from TheObserver.

```python
component = builder.build_flight_recorder_component([
    {
        "event_type": "spawn",
        "timestamp": "2026-01-09T10:08:46",
        "genome_id": "1411a4c2a275156e..."
    },
    # ... more events
], limit=5)
```

**Features:**
- Event type display
- Timestamp formatting
- Genome ID truncation
- Configurable event limit

### 4. Epistemic Phase Component

Displays the current epistemic phase declaration.

```python
component = builder.build_epistemic_phase_component("Data Gathering")
```

**Features:**
- Badge-style display
- High priority (always shown)
- Centered formatting

### 5. System Health Component

Displays system health metrics in table format.

```python
component = builder.build_system_health_component({
    "pyrite_valid": True,
    "structure_valid": True,
    "lock_exists": True
})
```

**Features:**
- Status indicators (✅/❌)
- Component-by-component breakdown
- Table format

### 6. Generic Metrics Table Component

Build custom metrics tables.

```python
component = builder.build_metrics_table_component(
    title="Work Efforts Summary",
    metrics=[
        {"Category": "Active", "Count": 5},
        {"Category": "Recent", "Count": 10}
    ],
    columns=["Category", "Count"]
)
```

## Complete Example

```python
from pathlib import Path
from src.waft.evolution.status_components import create_status_components_from_status_dict
from src.waft.evolution.document_components import ComponentBuilder, DocumentLayout
from src.waft.evolution.two_page_generator import TwoPageGenerator
from scripts.waft_status import check_status

# Get status
status = check_status(Path.cwd())

# Create all status components
status_components = create_status_components_from_status_dict(status)

# Add title
builder = ComponentBuilder()
title = builder.build_title_component("WAFT Kernel Status Report")

# Combine
all_components = [title] + status_components

# Create layout
layout = DocumentLayout(components=all_components, allowed_pages=10)

# Generate PDF (using TwoPageGenerator)
generator = TwoPageGenerator(weasyprint_available=True)
# ... generate PDF from layout
```

## Component Properties

All status components are `DocumentComponent` objects with:

- **component_type**: `ComponentType.SECTION`
- **metadata.component_subtype**: Status-specific type (e.g., "epistemic_state")
- **size_estimate**: Estimated space (0.0-1.0 of a page)
- **priority**: Importance (0.0-1.0, higher = more likely to include)

## Styling

Status components use CSS classes for styling:

- `.status-section`: Container for status sections
- `.epistemic-state`: Epistemic state display box
- `.moon-phase`: Moon phase indicator container
- `.phase-badge`: Epistemic phase badge
- `.gamification-table`, `.health-table`, `.metrics-table`: Table styles
- `.flight-events`: Flight Recorder event list

Styles are automatically included in the PDF template when using `TwoPageGenerator`.

## Integration with Existing Systems

Status components work seamlessly with:

- **TwoPageGenerator**: Use components in layouts
- **ComponentPDFGenerator**: Add to component lists
- **DocumentEvolutionEngine**: Evolve component combinations
- **OnePager**: Include in one-pager documents

## Files Created

- `src/waft/evolution/status_components.py` - Status component builders
- `scripts/generate_status_pdf.py` - Example script using status components

## Usage in Status Documentation

The status components are designed to be used in the enhanced `waft_status.py` documentation generation, providing consistent formatting across all documentation levels (layman, professional, scientist).
