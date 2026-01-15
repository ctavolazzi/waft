# /good-morning - Morning Briefing Dashboard

**Purpose:** Launch the WAFT morning briefing dashboard - your entry point to the ecosystem

**Usage:** `/good-morning`

**Script:** `scripts/start_good_morning.py` (launches Streamlit app on port 8507)

---

## Overview

The Good Morning dashboard is your daily entry point to the WAFT ecosystem. It provides:

- **Activity Since 5 AM**: What happened since the previous day's reset
- **TheChronicler Observations**: Genesis, exodus, and mutations
- **Work Efforts Status**: Active work efforts and recent activity
- **System Health**: Status of all WAFT systems
- **Quick Actions**: Generate briefs, start services, navigate
- **External Data**: Integration with external data sources

**Perfect for:**
- Starting your day
- Understanding what happened overnight
- Planning your work session
- System health check

---

## Quick Start

```
/good-morning
```

This will:
1. Start Streamlit server on port 8507
2. Open browser automatically at http://localhost:8507
3. Display morning briefing dashboard with activity since 5 AM

---

## Features

### Activity Since 5 AM

Shows all activity recorded by TheChronicler since 5 AM the previous day:
- **Genesis Events**: Files, commits, work efforts created
- **Exodus Events**: Files, work efforts deleted
- **Mutations**: Files modified
- **By Observer**: Breakdown by filesystem, git, work_effort

### Work Efforts Summary

- Active work efforts count
- Recent work efforts list
- Quick navigation to work effort details

### System Health

Status indicators for:
- ✅ TheChronicler (monitoring active)
- ✅ Empirica (epistemic tracking)
- ✅ Oracle (decision support)
- ✅ Gamification (character system)

### Quick Actions

- **Generate Morning Brief PDF**: Create a full morning brief document
- **Start TheChronicler**: Instructions to start monitoring
- **View Full Dashboard**: Link to complete WAFT dashboard

### External Data

Placeholder for external data integration (coming soon):
- Weather
- Calendar
- News/updates
- Other external sources

---

## Dashboard Layout

```
┌─────────────────────────────────────────┐
│         🌅 Good Morning                 │
│  Activity Since 5 AM: [time range]     │
├─────────────────────────────────────────┤
│ [Metrics: Genesis | Exodus | Mutations] │
├──────────────┬──────────────────────────┤
│ Activity     │ System Health             │
│ Summary      │ Quick Actions             │
│ Work Efforts │ External Data             │
└──────────────┴──────────────────────────┘
```

---

## Integration

The dashboard integrates with:
- **TheChronicler**: Activity observations
- **Work Efforts**: Status and recent activity
- **Brief System**: PDF generation
- **Empirica**: Epistemic state
- **Oracle**: Decision context
- **Gamification**: Character stats

---

## Technical Details

**Port**: 8507 (separate from main dashboard on 8501)

**Dependencies**:
- Streamlit
- TheChronicler
- Brief system
- Work efforts system

**File**: `good_morning.py` in project root

---

## Usage Examples

### Example 1: Start Morning Dashboard

```
/good-morning
```

**Output**:
- Streamlit server starts on port 8507
- Browser opens automatically
- Dashboard displays with current activity

### Example 2: Generate Morning Brief

From the dashboard, click "Generate Morning Brief PDF"

**Output**:
- PDF brief generated in `_work_efforts/briefs/`
- Includes system status and activity summary

---

## Philosophy

The Good Morning dashboard is:
- **Entry Point**: First thing you see each day
- **Context Provider**: Shows what happened since you last worked
- **Health Check**: Verifies all systems are operational
- **Action Hub**: Quick access to common tasks

It's designed to give you immediate context and help you start your day productively.

---

## Future Enhancements

- External data integration (weather, calendar, news)
- Personalized recommendations
- Work effort prioritization
- Daily goals and planning
- Integration with calendar systems
- Notification system

---

**Created as the entry point to the WAFT ecosystem - your morning companion.**

---

End Command ---
