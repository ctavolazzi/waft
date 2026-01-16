# /late-night-report - Late Night Status Report

**Purpose:** Create a comprehensive late-night status report with deep work accomplishments, current state, late-night insights, and tomorrow's priorities

**Usage:** `/late-night-report [options]`

**Script:** `scripts/create_late_night_report.py`

---

## Overview

The Late Night Report creates a comprehensive late-night/deep work session status report:
- **Late-Night Accomplishments**: Commits and work efforts from late-night sessions (10 PM - 6 AM)
- **Current System Status**: Git status, pending changes, active work
- **Active Work Efforts**: Current work in progress
- **Late-Night Insights**: Key learnings and decisions from deep work
- **Tomorrow's Priorities**: Next steps and focus areas
- **TM-ARCH-009 Style Cover**: Professional formatting

**Perfect for:**
- Late-night coding sessions
- Deep work documentation
- Late-night progress tracking
- Session handoff documentation
- Capturing breakthrough insights

---

## Quick Start

### Basic Late Night Report
```
/late-night-report
```

### With Custom Title
```
/late-night-report title:"Late Night Deep Work Session"
```

### With Insights
```
/late-night-report insights:"Discovered pattern in authentication flow, refactored core module"
```

---

## Features

- **Late-Night Tracking**: Identifies commits and work efforts from late-night hours (10 PM - 6 AM)
- **Deep Work Summary**: Highlights accomplishments from focused late-night sessions
- **Git Activity**: Today's commits and pending changes, with late-night commit highlighting
- **Work Effort Progress**: Files created/updated during late-night sessions
- **System Status**: Current git state and pending files
- **Insights Capture**: Space for documenting key learnings and decisions
- **Tomorrow Planning**: Next steps and priorities
- **TM-ARCH-009 Cover**: Professional cover page
- **Binder-Ready**: Perfect for printing

---

## Output

All reports are saved to:
- `_work_efforts/briefs/Late_Night_Report_[date].pdf`

Format:
- **Cover Page**: TM-ARCH-009 style with metadata
- **Late-Night Accomplishments Section**: Deep work summary
- **Status Section**: Current system state
- **Work Section**: Active work efforts
- **Insights Section**: Key learnings and decisions
- **Planning Section**: Tomorrow's priorities

---

## Integration

The Late Night Report integrates with:
- Git status and commit history (with late-night filtering)
- Work efforts system (with late-night activity tracking)
- Devlog tracking
- Project health monitoring

---

## Examples

### Basic Late Night Report
```
/late-night-report
```

### With Insights
```
/late-night-report insights:"Refactored authentication module, discovered performance bottleneck in query layer"
```

### Custom Title
```
/late-night-report title:"Midnight Deep Work Session - Auth Refactor"
```

---

## Related Commands

- **`/evening-report`** - End of day status report
- **`/midday-dossier`** - Midday status report
- **`/dossier`** - Comprehensive mission sitrep
- **`/brief`** - Quick brief document

---

**Created for late-night coding sessions, deep work documentation, and capturing breakthrough insights.**

---

End Command ---
