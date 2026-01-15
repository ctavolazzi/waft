# /dossier - Mission Sitrep Dossier

**Purpose:** Create comprehensive binder-ready mission sitrep dossier with cover, section dividers, and complete status briefing.

**Usage:** `/dossier [options]`

**Script:** `scripts/create_dossier.py`

---

## Overview

The Dossier command creates a complete mission sitrep document perfect for getting someone up to speed. It includes:
- **TM-ARCH-009 Style Cover Page**: Professional cover with metadata, warnings, signatures
- **Section Dividers**: Color-coded dividers for each major section
- **Mission Sitrep**: Current situation and status
- **Work Efforts**: Active work and progress
- **Recent Activity**: What's been happening
- **System Status**: Complete system health
- **Key Findings**: Important discoveries
- **Next Steps**: Actionable recommendations
- **Binder-Ready**: Perfect for printing and physical binders

**Perfect for:**
- Mission briefings
- Handoff documents
- Status reports
- Onboarding new team members
- Situation reports
- Binder documentation

---

## Quick Start

### Basic Dossier
```
/dossier
```

### With Custom Title
```
/dossier title:"Mission Sitrep - January 2026"
```

### With Custom Classification
```
/dossier classification:"CLASSIFIED" cover-header:"FOUNDATION"
```

---

## Features

- **TM-ARCH-009 Cover Page**: Professional cover with all Foundation elements
- **Section Dividers**: Color-coded dividers for each section
- **Mission Sitrep**: Current situation, status, and context
- **Work Efforts Summary**: Active work, progress, priorities
- **Recent Activity**: Recent commits, changes, activity
- **System Status**: Complete system health and status
- **Key Findings**: Important discoveries and insights
- **Next Steps**: Actionable recommendations
- **Binder-Ready**: Perfect for printing and physical binders

---

## Output

All dossiers are saved to:
- `_work_efforts/briefs/Dossier_[title]_[date].pdf`

Format:
- **Cover Page**: TM-ARCH-009 style with metadata, warnings, signatures
- **Section Dividers**: Color-coded dividers for each section
- **Content Sections**: Mission sitrep, work efforts, status, findings, next steps
- **Multiple Pages**: Full document, binder-ready
- **Professional Formatting**: Foundation + Field Guide hybrid

---

## Integration

The Dossier integrates with:
- System status checker
- Work efforts system
- Git status
- Project health monitoring
- Recent activity tracking

---

**Created for mission briefings, handoffs, and comprehensive situation reports.**

--- End Command ---
