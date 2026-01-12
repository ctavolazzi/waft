# Typed StatusState Guide

**Type-safe status state management with computed properties**

## Overview

The `StatusState` system provides typed dataclasses for WAFT status data, inspired by AI-DnD's CharacterState pattern. It offers type safety, IDE autocomplete, and computed properties for derived metrics.

## Quick Start

```python
from src.waft.core.status_state import StatusState
from scripts.waft_status import check_status

# Get status dict
status_dict = check_status()

# Create typed state
typed_state = StatusState.from_dict(status_dict)

# Use computed properties
print(f"Coverage: {typed_state.epistemic.coverage_pct}%")
print(f"Health: {typed_state.overall_health_status}")
```

## Available Classes

### EpistemicState

**Properties**:
- `initialized: bool` - Whether Empirica is initialized
- `knowledge_pct: float` - Knowledge percentage (0-100)
- `uncertainty_pct: float` - Uncertainty percentage (0-100)
- `moon_phase: str` - Moon phase emoji
- `moon_phase_desc: str` - Moon phase description

**Computed Properties**:
- `coverage_pct: float` - Total epistemic coverage (average of knowledge and certainty)
- `health_status: str` - Health indicator ("Excellent", "Good", "Moderate", "Low")
- `knowledge_ratio: float` - Knowledge as ratio (0.0-1.0)
- `uncertainty_ratio: float` - Uncertainty as ratio (0.0-1.0)

**Methods**:
- `to_dict() -> Dict[str, Any]` - Convert to dictionary

### GamificationState

**Properties**:
- `available: bool` - Whether gamification is available
- `level: int` - Character level
- `integrity: float` - Integrity score (0-100)
- `insight: float` - Insight points
- `achievements_count: int` - Number of achievements
- `achievements: List[str]` - List of achievement names

**Computed Properties**:
- `integrity_status: str` - Integrity indicator ("Excellent", "Good", "Fair", "Poor")
- `integrity_ratio: float` - Integrity as ratio (0.0-1.0)
- `next_level_xp: float` - XP needed for next level
- `level_progress_pct: float` - Progress toward next level (0-100%)

**Methods**:
- `to_dict() -> Dict[str, Any]` - Convert to dictionary

### ProjectHealthState

**Properties**:
- `pyrite_valid: bool` - _pyrite structure validity
- `structure_valid: bool` - Directory structure validity
- `lock_exists: bool` - Dependency lock file presence
- `genesis_files_count: int` - Number of genesis files present
- `genesis_files_total: int` - Total expected genesis files

**Computed Properties**:
- `health_score: float` - Overall health score (0.0-100.0)
- `health_status: str` - Health indicator ("Excellent", "Good", "Fair", "Poor")

**Methods**:
- `to_dict() -> Dict[str, Any]` - Convert to dictionary

### StatusState

**Properties**:
- `epistemic: EpistemicState` - Epistemic state
- `gamification: GamificationState` - Gamification state
- `project_health: ProjectHealthState` - Project health state
- `flight_events: List[Dict[str, Any]]` - Flight recorder events
- `git_status: Dict[str, Any]` - Git status
- `epistemic_phase: str` - Current epistemic phase
- `work_efforts: Dict[str, Any]` - Work efforts data
- `recent_activity: Dict[str, Any]` - Recent activity data
- `timestamp: datetime` - Status timestamp

**Computed Properties**:
- `overall_health_score: float` - Overall system health (weighted average)
- `overall_health_status: str` - Overall health indicator

**Methods**:
- `from_dict(status_dict: Dict[str, Any]) -> StatusState` - Create from status dict
- `to_dict() -> Dict[str, Any]` - Convert to dictionary

## Usage Examples

### Example 1: Basic Usage

```python
from src.waft.core.status_state import StatusState
from scripts.waft_status import check_status

# Get status and create typed state
status_dict = check_status()
typed_state = StatusState.from_dict(status_dict)

# Access computed properties
print(f"Epistemic coverage: {typed_state.epistemic.coverage_pct}%")
print(f"Gamification integrity: {typed_state.gamification.integrity_status}")
print(f"Overall health: {typed_state.overall_health_status}")
```

### Example 2: Using with Status Components

```python
from src.waft.evolution.status_components import create_status_components_from_status_dict
from scripts.waft_status import check_status
from src.waft.core.status_state import StatusState

# Get status
status_dict = check_status()
typed_state = StatusState.from_dict(status_dict)

# Create components (will use computed properties from typed state)
components = create_status_components_from_status_dict(
    status_dict,
    typed_state=typed_state  # Optional: provides computed properties
)
```

### Example 3: Direct Property Access

```python
from src.waft.core.status_state import EpistemicState

# Create epistemic state
epistemic = EpistemicState(
    initialized=True,
    knowledge_pct=75.0,
    uncertainty_pct=25.0,
    moon_phase="🌔",
    moon_phase_desc="Good (75% coverage)"
)

# Use computed properties
print(f"Coverage: {epistemic.coverage_pct}%")  # 75.0%
print(f"Health: {epistemic.health_status}")    # "Good"
print(f"Knowledge ratio: {epistemic.knowledge_ratio}")  # 0.75
```

### Example 4: Backward Compatibility

```python
from src.waft.core.status_state import StatusState

# Create typed state
typed_state = StatusState.from_dict(status_dict)

# Convert back to dict (for existing code)
status_dict_again = typed_state.to_dict()

# Use with existing functions
components = create_status_components_from_status_dict(status_dict_again)
```

## Integration Points

### check_status() Function

```python
from scripts.waft_status import check_status
from src.waft.core.status_state import StatusState

# Option 1: Get dict, then create typed state
status_dict = check_status()
typed_state = StatusState.from_dict(status_dict)

# Option 2: Use return_typed parameter (future enhancement)
# typed_state = check_status(return_typed=True)
```

### Status Components

```python
from src.waft.evolution.status_components import create_status_components_from_status_dict

# With typed state (uses computed properties)
components = create_status_components_from_status_dict(status_dict, typed_state=typed_state)

# Without typed state (backward compatible)
components = create_status_components_from_status_dict(status_dict)
```

## Computed Properties Reference

### EpistemicState

| Property | Type | Description | Formula |
|----------|------|-------------|---------|
| `coverage_pct` | `float` | Total epistemic coverage | `(knowledge_pct + (100 - uncertainty_pct)) / 2` |
| `health_status` | `str` | Health indicator | Based on coverage_pct thresholds |
| `knowledge_ratio` | `float` | Knowledge as ratio | `knowledge_pct / 100.0` |
| `uncertainty_ratio` | `float` | Uncertainty as ratio | `uncertainty_pct / 100.0` |

### GamificationState

| Property | Type | Description | Formula |
|----------|------|-------------|---------|
| `integrity_status` | `str` | Integrity indicator | Based on integrity thresholds |
| `integrity_ratio` | `float` | Integrity as ratio | `integrity / 100.0` |
| `next_level_xp` | `float` | XP for next level | `1000 * (level ** 1.5)` |
| `level_progress_pct` | `float` | Level progress | `(insight / next_level_xp) * 100` |

### ProjectHealthState

| Property | Type | Description | Formula |
|----------|------|-------------|---------|
| `health_score` | `float` | Overall health | Average of all indicators |
| `health_status` | `str` | Health indicator | Based on health_score thresholds |

### StatusState

| Property | Type | Description | Formula |
|----------|------|-------------|---------|
| `overall_health_score` | `float` | Overall system health | Weighted average (epistemic 30%, gamification 30%, project 40%) |
| `overall_health_status` | `str` | Overall health indicator | Based on overall_health_score thresholds |

## Benefits

### Type Safety
- IDE autocomplete for all properties
- Type checking at development time
- Clear data structure

### Computed Properties
- Derived metrics calculated automatically
- No manual calculation needed
- Consistent formulas across codebase

### Backward Compatibility
- `to_dict()` method for existing code
- Optional typed_state parameter
- Existing code continues to work

### Testing
- Easy to create test instances
- Computed properties testable
- Clear data structure

## Migration Guide

### From Dict to Typed State

**Before**:
```python
status = check_status()
coverage = status["epistemic_state"]["knowledge_pct"] + (100 - status["epistemic_state"]["uncertainty_pct"]) / 2
```

**After**:
```python
status = check_status()
typed_state = StatusState.from_dict(status)
coverage = typed_state.epistemic.coverage_pct  # Computed automatically
```

### Using with Components

**Before**:
```python
components = create_status_components_from_status_dict(status)
```

**After** (optional enhancement):
```python
typed_state = StatusState.from_dict(status)
components = create_status_components_from_status_dict(status, typed_state=typed_state)
```

## Best Practices

1. **Use Typed State for New Code**: Prefer typed state for new code
2. **Keep Dict for Compatibility**: Use dict when integrating with existing code
3. **Leverage Computed Properties**: Use computed properties instead of manual calculations
4. **Test with Typed State**: Create test instances for unit testing

---

**This typed state system provides type safety, computed properties, and backward compatibility - perfect for improving code quality while maintaining existing functionality.**
