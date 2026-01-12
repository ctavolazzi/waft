# AI-DnD Integration Opportunities for WAFT

**Date**: 2026-01-11  
**Source**: `ctavolazzi/AI-DnD` repository analysis  
**Purpose**: Identify patterns and ideas from AI-DnD that could enhance WAFT's status components and PDF generation

---

## Executive Summary

The AI-DnD repository contains several patterns that could significantly enhance WAFT's status components system, particularly around:
1. **Progress visualization** (quest objectives → status progress)
2. **State management** (dataclass patterns → status state)
3. **UI component patterns** (game UI → PDF components)
4. **Data integrity** (save system → status persistence)

---

## 1. Progress Tracking Patterns

### 1.1 Quest Objective Progress Display

**From AI-DnD**: `pygame_mvp/game/quests.py`

**Pattern**:
```python
@property
def progress_text(self) -> str:
    if self.required_count > 1:
        return f"{self.description} ({self.current_count}/{self.required_count})"
    return self.description
```

**WAFT Integration Opportunity**:
- **Status Component Enhancement**: Add progress bars/text to status components
- **Use Cases**:
  - Work effort completion: "Active Development (3/5 tickets)"
  - Epistemic progress: "Knowledge Growth (65/100%)"
  - Gamification: "Level Progress (450/1000 XP)"

**Implementation**:
```python
# In status_components.py
def build_progress_component(
    label: str,
    current: int,
    total: int,
    show_percentage: bool = True
) -> DocumentComponent:
    """Build progress display component."""
    percentage = (current / total * 100) if total > 0 else 0
    progress_text = f"{label} ({current}/{total})"
    if show_percentage:
        progress_text += f" - {percentage:.1f}%"
    
    # HTML with progress bar
    body = f"""
    <div class="progress-container">
        <div class="progress-label">{html.escape(label)}</div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {percentage}%"></div>
        </div>
        <div class="progress-text">{progress_text}</div>
    </div>
    """
    return DocumentComponent(...)
```

**CSS Addition**:
```css
.progress-container {
    margin: 8pt 0;
}
.progress-bar {
    width: 100%;
    height: 8pt;
    background: #e0e0e0;
    border-radius: 4pt;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    background: {{ color.accent }};
    transition: width 0.3s;
}
```

---

## 2. State Management Patterns

### 2.1 Dataclass-Based State with Computed Properties

**From AI-DnD**: `pygame_mvp/game/game_state.py`

**Pattern**:
```python
@dataclass
class CharacterState:
    hp: int
    max_hp: int
    
    @property
    def hp_percent(self) -> float:
        if self.max_hp <= 0:
            return 0.0
        return self.hp / self.max_hp
```

**WAFT Integration Opportunity**:
- **Status State Class**: Create `StatusState` dataclass for type safety
- **Computed Properties**: Calculate percentages, ratios, health indicators
- **Type Safety**: Replace dict-based status with typed state

**Implementation**:
```python
# New file: src/waft/core/status_state.py
from dataclasses import dataclass
from typing import Optional, Dict, List

@dataclass
class EpistemicState:
    initialized: bool = False
    knowledge_pct: float = 0.0
    uncertainty_pct: float = 0.0
    moon_phase: str = "🌑"
    moon_phase_desc: str = "Unknown"
    
    @property
    def coverage_pct(self) -> float:
        """Total epistemic coverage."""
        return self.knowledge_pct + (100 - self.uncertainty_pct) / 2
    
    @property
    def health_status(self) -> str:
        """Health indicator based on coverage."""
        if self.coverage_pct >= 90:
            return "Excellent"
        elif self.coverage_pct >= 75:
            return "Good"
        elif self.coverage_pct >= 50:
            return "Moderate"
        else:
            return "Low"

@dataclass
class GamificationState:
    available: bool = False
    level: int = 1
    integrity: float = 100.0
    insight: float = 0.0
    achievements_count: int = 0
    
    @property
    def integrity_status(self) -> str:
        """Integrity status indicator."""
        if self.integrity >= 90:
            return "Excellent"
        elif self.integrity >= 75:
            return "Good"
        elif self.integrity >= 50:
            return "Fair"
        else:
            return "Poor"
    
    @property
    def next_level_xp(self) -> float:
        """XP needed for next level (example formula)."""
        return 1000 * (self.level ** 1.5)

@dataclass
class StatusState:
    """Complete typed status state."""
    epistemic: EpistemicState
    gamification: GamificationState
    flight_events: List[Dict]
    project_health: Dict
    git_status: Dict
    
    @classmethod
    def from_dict(cls, status_dict: Dict) -> 'StatusState':
        """Create from status dictionary."""
        return cls(
            epistemic=EpistemicState(**status_dict.get("epistemic_state", {})),
            gamification=GamificationState(**status_dict.get("gamification_state", {})),
            flight_events=status_dict.get("flight_recorder_events", []),
            project_health=status_dict.get("project_health", {}),
            git_status=status_dict.get("git_status", {})
        )
```

**Benefits**:
- Type safety and IDE autocomplete
- Computed properties for derived metrics
- Clear data structure
- Easier testing

---

## 3. UI Component Patterns

### 3.1 Status Effect Display

**From AI-DnD**: Character status effects list

**Pattern**: Display multiple status indicators in compact format

**WAFT Integration Opportunity**:
- **Status Badges**: Display multiple status indicators (like status effects)
- **Use Cases**:
  - System health badges: "✅ Pyrite Valid", "⚠️ Lock Missing"
  - Epistemic badges: "🌓 Moderate", "📊 65% Knowledge"
  - Gamification badges: "⭐ Level 3", "💎 87% Integrity"

**Implementation**:
```python
def build_status_badges_component(
    badges: List[Dict[str, str]]
) -> DocumentComponent:
    """Build status badges component.
    
    Args:
        badges: List of {label, status, icon} dicts
    """
    badge_html = "".join([
        f'<span class="status-badge status-{badge["status"]}">'
        f'{badge.get("icon", "")} {html.escape(badge["label"])}'
        f'</span>'
        for badge in badges
    ])
    
    body = f'<div class="status-badges">{badge_html}</div>'
    return DocumentComponent(...)
```

**CSS**:
```css
.status-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 4pt;
    margin: 8pt 0;
}
.status-badge {
    padding: 2pt 6pt;
    border-radius: 4pt;
    font-size: 9pt;
    display: inline-block;
}
.status-badge.status-good {
    background: #e8f5e9;
    color: #2e7d32;
}
.status-badge.status-warning {
    background: #fff3e0;
    color: #e65100;
}
.status-badge.status-error {
    background: #ffebee;
    color: #c62828;
}
```

---

## 4. Data Integrity Patterns

### 4.1 Save System with Checksums

**From AI-DnD**: `pygame_mvp/game/save_system.py`

**Pattern**: JSON serialization with integrity checking

**WAFT Integration Opportunity**:
- **Status Persistence**: Save status snapshots with checksums
- **Version Tracking**: Track status changes over time
- **Integrity Verification**: Verify status data hasn't been corrupted

**Implementation**:
```python
# New file: src/waft/core/status_persistence.py
import hashlib
import json
from pathlib import Path
from datetime import datetime

class StatusPersistence:
    """Persist and verify status snapshots."""
    
    def save_status_snapshot(
        self,
        status: Dict[str, Any],
        output_path: Path
    ) -> Dict[str, Any]:
        """Save status with checksum."""
        snapshot = {
            "version": "1.0",
            "timestamp": datetime.utcnow().isoformat(),
            "status": status,
            "metadata": {
                "source": "waft-status",
                "project_path": str(status.get("project_path", ""))
            }
        }
        
        # Calculate checksum
        json_str = json.dumps(snapshot, sort_keys=True)
        checksum = hashlib.md5(json_str.encode()).hexdigest()
        snapshot["checksum"] = checksum
        
        # Save
        output_path.write_text(json.dumps(snapshot, indent=2))
        return snapshot
    
    def load_status_snapshot(
        self,
        snapshot_path: Path
    ) -> Optional[Dict[str, Any]]:
        """Load and verify status snapshot."""
        try:
            data = json.loads(snapshot_path.read_text())
            stored_checksum = data.pop("checksum", None)
            
            # Verify checksum
            json_str = json.dumps(data, sort_keys=True)
            calculated_checksum = hashlib.md5(json_str.encode()).hexdigest()
            
            if stored_checksum != calculated_checksum:
                return None  # Integrity check failed
            
            return data.get("status")
        except Exception:
            return None
```

**Use Cases**:
- Historical status tracking
- Status comparison over time
- Debugging status issues
- Status audit trail

---

## 5. Inventory/Item Display Patterns

### 5.1 Stackable Items Display

**From AI-DnD**: Inventory system with stacking

**Pattern**: Display items with quantities in compact format

**WAFT Integration Opportunity**:
- **Metrics Aggregation**: Display related metrics together
- **Grouped Status**: Group status items by category
- **Compact Display**: Show multiple related values efficiently

**Implementation**:
```python
def build_metrics_group_component(
    group_name: str,
    metrics: List[Dict[str, Any]]
) -> DocumentComponent:
    """Build grouped metrics component.
    
    Args:
        group_name: Group label
        metrics: List of {label, value, unit, icon} dicts
    """
    rows = "".join([
        f'<tr>'
        f'<td>{metric.get("icon", "")} {html.escape(metric["label"])}</td>'
        f'<td class="metric-value">{metric["value"]} {metric.get("unit", "")}</td>'
        f'</tr>'
        for metric in metrics
    ])
    
    body = f"""
    <div class="metrics-group">
        <h4>{html.escape(group_name)}</h4>
        <table class="metrics-table">
            {rows}
        </table>
    </div>
    """
    return DocumentComponent(...)
```

---

## 6. Recommended Integration Plan

### Phase 1: Quick Wins (Low Effort, High Value)

1. **Progress Bars** (2-3 hours)
   - Add progress bar component to status_components.py
   - Use for work effort completion, epistemic progress
   - Add CSS styling

2. **Status Badges** (1-2 hours)
   - Add badge component for compact status indicators
   - Use for system health, epistemic phase
   - Add CSS styling

### Phase 2: Type Safety (Medium Effort, High Value)

3. **StatusState Dataclass** (4-6 hours)
   - Create typed status state classes
   - Migrate status_components.py to use typed state
   - Add computed properties for derived metrics
   - Update check_status() to return StatusState

### Phase 3: Persistence (Medium Effort, Medium Value)

4. **Status Persistence** (3-4 hours)
   - Implement status snapshot saving
   - Add checksum verification
   - Create status history tracking
   - Add comparison utilities

### Phase 4: Enhanced Display (High Effort, High Value)

5. **Grouped Metrics** (2-3 hours)
   - Add metrics grouping component
   - Organize related metrics together
   - Improve visual hierarchy

---

## 7. Code Examples

### Example 1: Enhanced Status Component with Progress

```python
# In status_components.py
def build_work_effort_progress_component(
    active_count: int,
    total_count: int,
    completed_count: int
) -> DocumentComponent:
    """Build work effort progress component."""
    progress_pct = (completed_count / total_count * 100) if total_count > 0 else 0
    
    body = f"""
    <div class="progress-section">
        <h4>Work Effort Progress</h4>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress_pct}%"></div>
        </div>
        <div class="progress-stats">
            <span>Active: {active_count}</span>
            <span>Completed: {completed_count}/{total_count}</span>
            <span>{progress_pct:.1f}%</span>
        </div>
    </div>
    """
    return DocumentComponent(
        component_type=ComponentType.SECTION,
        content={"title": "Work Effort Progress", "body": body},
        metadata={"level": 3, "component_subtype": "progress"},
        size_estimate=0.1,
        priority=0.8
    )
```

### Example 2: Status Badges Component

```python
def build_system_health_badges_component(
    health: Dict[str, bool]
) -> DocumentComponent:
    """Build system health badges."""
    badges = []
    
    if health.get("pyrite_valid"):
        badges.append({"label": "Pyrite Valid", "status": "good", "icon": "✅"})
    else:
        badges.append({"label": "Pyrite Invalid", "status": "error", "icon": "❌"})
    
    if health.get("lock_exists"):
        badges.append({"label": "Lock File", "status": "good", "icon": "🔒"})
    else:
        badges.append({"label": "No Lock File", "status": "warning", "icon": "⚠️"})
    
    badge_html = "".join([
        f'<span class="status-badge status-{b["status"]}">'
        f'{b["icon"]} {html.escape(b["label"])}'
        f'</span>'
        for b in badges
    ])
    
    body = f'<div class="status-badges">{badge_html}</div>'
    return DocumentComponent(...)
```

---

## 8. Benefits Summary

| Pattern | Benefit | Effort | Priority |
|---------|---------|--------|----------|
| Progress Bars | Visual progress tracking | Low | High |
| Status Badges | Compact status indicators | Low | High |
| Typed State | Type safety, computed properties | Medium | High |
| Status Persistence | Historical tracking, integrity | Medium | Medium |
| Grouped Metrics | Better organization | Low | Medium |

---

## 9. Next Steps

1. **Review this document** with team
2. **Prioritize patterns** based on current needs
3. **Start with Phase 1** (progress bars, badges)
4. **Iterate** based on usage feedback
5. **Migrate to typed state** when ready

---

**These patterns from AI-DnD can significantly enhance WAFT's status components, making them more visual, type-safe, and feature-rich.**
