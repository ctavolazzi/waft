# /chronicle - TheChronicler Command

**Purpose:** Interact with TheChronicler - WAFT's self-monitoring system that observes, records, and reports on all system activity

**Usage:** `/chronicle [action] [options]`

**Script:** `waft chronicler` (CLI)

---

## Overview

TheChronicler is WAFT's passive observer - a journalist and historian of system activity. It monitors genesis (creation) and exodus (deletion) of all system components, generating hourly and daily reports.

**Perfect for:**
- Starting continuous monitoring
- Viewing system activity statistics
- Generating activity reports
- Understanding system evolution

---

## Quick Start

### Start Monitoring
```
/chronicle start
```

### View Statistics
```
/chronicle stats
```

### Generate Reports
```
/chronicle report hourly
/chronicle report daily
```

---

## Actions

### Start Monitoring

**Usage:** `/chronicle start [--reset-hour HOUR]`

Starts TheChronicler monitoring service. Runs continuously until stopped.

**Options:**
- `--reset-hour HOUR`: Hour to reset daily cycle (default: 5 AM)

**Example:**
```
/chronicle start
/chronicle start --reset-hour 6
```

**What it does:**
- Starts file system observer (watchdog)
- Starts git observer (polling)
- Starts work effort observer (polling)
- Starts scheduler for hourly/daily reports
- Begins recording observations

**Output:**
- Observations stored in: `_chronicler/observations/YYYY-MM-DD/`
- Reports stored in: `_chronicler/reports/`

---

### View Statistics

**Usage:** `/chronicle stats`

Shows current day's activity statistics.

**Example:**
```
/chronicle stats
```

**Output:**
- Date
- Genesis count (creations)
- Exodus count (deletions)
- Net change
- Observers active
- Oracle availability

---

### Generate Reports

**Usage:** `/chronicle report [hourly|daily]`

Manually generate reports.

**Options:**
- `hourly`: Generate hourly report for current hour
- `daily`: Generate daily report for today

**Examples:**
```
/chronicle report hourly
/chronicle report daily
```

**Output:**
- Hourly reports: `_chronicler/reports/hourly_YYYYMMDD_HH00.pdf`
- Daily reports: `_chronicler/reports/daily_YYYYMMDD.pdf`

---

## What TheChronicler Observes

### File System Observer
- **Genesis**: File/directory creation
- **Exodus**: File/directory deletion
- **Mutations**: File modifications
- **Moves**: File renames/moves

**Ignores:**
- `.git/`, `__pycache__/`, `node_modules/`, `.venv/`, etc.

### Git Observer
- **Genesis**: New commits
- **Mutations**: Status changes (modified, added, deleted files)

### Work Effort Observer
- **Genesis**: New work efforts created
- **Exodus**: Work efforts deleted
- **Tickets**: New tickets in work efforts

---

## Automatic Reporting

### Hourly Reports
- Generated automatically on the hour (00:00, 01:00, ..., 23:00)
- Contains activity summary for that hour
- Categorized by genesis, exodus, mutations
- Grouped by observer

### Daily Reports
- Generated automatically at 5 AM (reset cycle)
- Contains 24-hour activity summary
- Hourly breakdown table
- Activity by observer
- Professional PDF format

---

## Storage Structure

```
_chronicler/
├── observations/
│   └── YYYY-MM-DD/
│       ├── observations_00.jsonl
│       ├── observations_01.jsonl
│       └── ...
└── reports/
    ├── hourly_YYYYMMDD_HH00.pdf
    └── daily_YYYYMMDD.pdf
```

---

## Integration

TheChronicler integrates with:
- **Oracle**: Logs significant observations for epistemic tracking
- **Brief System**: Uses BriefDocument for report generation
- **Work Efforts**: Monitors work effort lifecycle
- **Git**: Tracks repository activity

---

## Philosophy

TheChronicler is a **passive observer**:
- ✅ Observes and records (journalist)
- ✅ Chronicles history (historian)
- ✅ Generates reports (monitor)
- ❌ Does NOT defend or guard
- ❌ Does NOT hold the line
- ❌ Does NOT make decisions

It is the chronicler of all system activity, not a guardian.

---

## Use Cases

### Daily Monitoring
```
/chronicle start
# Let it run all day
# Check stats periodically
/chronicle stats
```

### Generate Morning Brief
```
/chronicle report daily
# Review yesterday's activity
```

### Check Current Activity
```
/chronicle stats
# See what's happening right now
```

### Manual Report Generation
```
/chronicle report hourly
# Generate report for current hour
```

---

## Examples

### Example 1: Start Monitoring
```
/chronicle start
```

**Output:**
- Starts all observers
- Begins recording observations
- Scheduler starts for automatic reports

### Example 2: View Today's Activity
```
/chronicle stats
```

**Output:**
```
📊 TheChronicler Statistics

Date: 2026-01-13
Genesis (Created): 42
Exodus (Deleted): 3
Net Change: 39
Observers Active: 3
Oracle Available: True
```

### Example 3: Generate Reports
```
/chronicle report daily
```

**Output:**
- Generates daily PDF report
- Shows path to generated report

---

## CLI Alternative

All functionality is also available via CLI:

```bash
# Start monitoring
waft chronicler

# View statistics
waft chronicler-stats

# Generate reports
waft chronicler-report --hourly
waft chronicler-report --daily
```

---

## Notes

- **5 AM Reset**: Daily cycle resets at 5 AM (configurable)
- **Non-Blocking**: Observations don't interfere with operations
- **Thread-Safe**: All observers run independently
- **Oracle Integration**: Significant events logged to Oracle
- **Watchdog Optional**: Falls back gracefully if not installed

---

**Created for self-monitoring, activity tracking, and system awareness.**

---

End Command ---
