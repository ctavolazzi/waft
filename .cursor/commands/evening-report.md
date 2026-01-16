# /evening-report - Evening Status Report

**Purpose:** Create a comprehensive evening status report with daily accomplishments, current state, and tomorrow's priorities

**Usage:** `/evening-report [options]`

**Script:** `scripts/create_evening_report.py`

---

## Overview

The Evening Report creates a comprehensive end-of-day status report:
- **Today's Accomplishments**: Git commits, work efforts, progress made
- **Current System Status**: Git status, pending changes, active work
- **Active Work Efforts**: Current work in progress
- **Tomorrow's Priorities**: Next steps and focus areas
- **TM-ARCH-009 Style Cover**: Professional formatting

**Perfect for:**
- End of day reviews
- Tomorrow planning
- Daily progress tracking
- Session handoff documentation

---

## Quick Start

### Basic Evening Report
```
/evening-report
```

### With Custom Title
```
/evening-report title:"Evening Status Report"
```

### With Tomorrow Focus
```
/evening-report tomorrow-focus:"Feature Implementation"
```

---

## Features

- **Daily Accomplishments**: Summary of today's work
- **Git Activity**: Today's commits and pending changes
- **Work Effort Progress**: Files created/updated today
- **System Status**: Current git state and pending files
- **Tomorrow Planning**: Next steps and priorities
- **TM-ARCH-009 Cover**: Professional cover page
- **Binder-Ready**: Perfect for printing

---

## Output

All reports are saved to:
- `_work_efforts/briefs/Evening_Report_[date].pdf`

Format:
- **Cover Page**: TM-ARCH-009 style with metadata
- **Accomplishments Section**: Today's work summary
- **Status Section**: Current system state
- **Work Section**: Active work efforts
- **Planning Section**: Tomorrow's priorities

---

## Integration

The Evening Report integrates with:
- Git status and commit history
- Work efforts system
- Devlog tracking
- Project health monitoring

---

## Examples

### Basic Evening Report
```
/evening-report
```

### With Tomorrow Focus
```
/evening-report tomorrow-focus:"Complete PDF generator refactor"
```

### Custom Title
```
/evening-report title:"Friday Evening Summary"
```

---

## Related Commands

- **`/late-night-report`** - Late-night/deep work status report
- **`/midday-dossier`** - Midday status report
- **`/dossier`** - Comprehensive mission sitrep
- **`/brief`** - Quick brief document

---

**Created for end-of-day reviews and tomorrow planning.**

--- End Command ---
