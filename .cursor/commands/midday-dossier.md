# /midday-dossier - Midday Status Dossier

**Purpose:** Create a comprehensive midday status dossier with current system state, work progress, and afternoon planning

**Usage:** `/midday-dossier [options]`

**Script:** `scripts/create_midday_dossier.py`

---

## Overview

The Midday Dossier creates a comprehensive status report for midday review:
- **Current System Status**: Git, work efforts, project health
- **Morning Progress**: What was accomplished since morning
- **Active Work**: Current work efforts and tickets
- **Afternoon Planning**: Next steps and priorities
- **TM-ARCH-009 Style Cover**: Professional formatting

**Perfect for:**
- Midday status reviews
- Afternoon planning
- Progress tracking
- Handoff documentation

---

## Quick Start

### Basic Midday Dossier
```
/midday-dossier
```

### With Custom Title
```
/midday-dossier title:"Midday Status Report"
```

### With Afternoon Focus
```
/midday-dossier afternoon-focus:"Prime Directive Implementation"
```

---

## Features

- **Comprehensive Status**: Full system status snapshot
- **Progress Tracking**: Morning accomplishments
- **Work Effort Summary**: Active work efforts and tickets
- **Afternoon Planning**: Next steps and priorities
- **TM-ARCH-009 Cover**: Professional cover page
- **Binder-Ready**: Perfect for printing

---

## Output

All dossiers are saved to:
- `_work_efforts/briefs/Midday_Dossier_[date].pdf`

Format:
- **Cover Page**: TM-ARCH-009 style with metadata
- **Status Section**: Current system state
- **Progress Section**: Morning accomplishments
- **Work Section**: Active work efforts
- **Planning Section**: Afternoon priorities

---

## Integration

The Midday Dossier integrates with:
- System status checker
- Work efforts system
- Git status
- Project health monitoring

---

**Created for midday status reviews and afternoon planning.**

--- End Command ---
