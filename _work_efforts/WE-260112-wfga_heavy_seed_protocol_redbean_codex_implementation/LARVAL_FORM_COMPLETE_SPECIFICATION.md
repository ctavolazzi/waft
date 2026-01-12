# Waft Larval Form - Complete Specification

**Version**: v0.6.0
**Date**: 2026-01-12
**Status**: ✅ Complete Implementation
**Purpose**: Complete specification for recreating the Waft Larval Form application

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Database Schema](#database-schema)
4. [Core Classes & Functions](#core-classes--functions)
5. [User Interface](#user-interface)
6. [Reactive Live Reload System](#reactive-live-reload-system)
7. [Data Export](#data-export)
8. [Error Handling](#error-handling)
9. [Dependencies](#dependencies)
10. [File Structure](#file-structure)
11. [Testing Requirements](#testing-requirements)
12. [Migration Requirements](#migration-requirements)

---

## Overview

### Purpose

The Waft Larval Form is a **Python + Streamlit + SQLite** application that serves as the developmental stage before the Redbean "Mature Form". It implements a 3D printing workflow manager that tracks G-code files and print jobs, with a philosophical foundation based on "Hasvanism" (Breath, Memory, Trauma).

### Key Principles

1. **Breath**: Runtime logic that executes upon interaction
2. **Memory**: Persistent storage of state and history (SQLite)
3. **Trauma**: Refusal to ignore errors; they are etched into memory

### Core Philosophy

- **Hasvanism**: The entity "breathes" (executes logic), "remembers" (persists to database), and "feels pain" (logs errors as TRAUMA)
- **Error Resilience**: Errors are logged, not ignored - the system continues running
- **Migration-Ready**: Database schema matches future Redbean version exactly

---

## Architecture

### Technology Stack

- **Language**: Python 3.x
- **UI Framework**: Streamlit
- **Database**: SQLite 3
- **Data Processing**: Pandas
- **Serial Communication**: PySerial (for future printer integration)

### Application Structure

```
waft_larva.py (Single-file application)
├── Configuration (Constants, Enums)
├── Database Connection (get_db_connection with retry logic)
├── WaftEntity Class (Core consciousness)
│   ├── Database initialization
│   ├── Chronicle logging
│   ├── Artifact management
│   ├── Data export methods
│   └── Data hash for change detection
└── Streamlit UI (main function)
    ├── Header with auto-refresh controls
    ├── Status summary dashboard
    ├── Activity log panel
    ├── Print job management panel
    ├── Data export section
    └── Reactive update system
```

---

## Database Schema

### Database File

- **Name**: `waft_memory.db`
- **Location**: Same directory as `waft_larva.py`
- **Mode**: WAL (Write-Ahead Logging) for concurrency
- **Timeout**: 10.0 seconds
- **Retry Logic**: 3 attempts with exponential backoff

### Table: `chronicle`

**Purpose**: Stream of consciousness - all events, thoughts, and errors

**Schema**:
```sql
CREATE TABLE IF NOT EXISTS chronicle (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    severity TEXT,
    message TEXT,
    context TEXT
)
```

**Columns**:
- `id`: Auto-incrementing primary key
- `timestamp`: ISO format datetime string (YYYY-MM-DD HH:MM:SS)
- `severity`: One of `THOUGHT`, `STRAIN`, `TRAUMA`
- `message`: Human-readable message describing the event
- `context`: Optional additional context (often traceback for TRAUMA)

**Severity Levels**:
- `THOUGHT`: Normal system activity (startup, successful operations)
- `STRAIN`: Warnings or non-critical issues
- `TRAUMA`: Errors that were caught and logged (system continues running)

### Table: `artifacts`

**Purpose**: Physical body - G-code files and print jobs

**Schema**:
```sql
CREATE TABLE IF NOT EXISTS artifacts (
    id INTEGER PRIMARY KEY,
    name TEXT,
    gcode TEXT,
    status TEXT DEFAULT 'VOID',
    birth_time TEXT
)
```

**Columns**:
- `id`: Auto-incrementing primary key
- `name`: Human-readable name for the artifact (e.g., "Right_Index_Phalanx")
- `gcode`: G-code content (3D printer instructions)
- `status`: One of `VOID`, `MANIFESTING`, `PHYSICAL`
- `birth_time`: ISO format datetime when artifact became PHYSICAL (nullable)

**Status Flow**:
- `VOID`: Pending print job (not yet printed)
- `MANIFESTING`: Currently being printed (future state)
- `PHYSICAL`: Successfully printed (complete)

### Seed Data

**Initial Artifact**: `Right_Index_Phalanx`
- **Name**: "Right_Index_Phalanx"
- **G-code**: "G28\nG1 Z10\nM117 HELLO WORLD"
- **Status**: "VOID"
- **Chronicle Entry**: "Genesis Seed implanted: Right_Index_Phalanx" (THOUGHT severity)

---

## Core Classes & Functions

### Configuration Constants

```python
DB_NAME = "waft_memory.db"
DB_TIMEOUT = 10.0  # Seconds to wait for database lock
MAX_RETRIES = 3
RETRY_DELAY = 0.1  # Initial delay between retries (seconds)
```

### Enum: `Severity`

```python
class Severity(Enum):
    THOUGHT = "THOUGHT"   # Routine internal monologue
    STRAIN = "STRAIN"     # Non-critical resistance
    TRAUMA = "TRAUMA"     # Critical failure / Severance
```

### Function: `get_db_connection()`

**Purpose**: Get database connection with retry logic and WAL mode

**Behavior**:
1. Attempt connection with timeout
2. Set WAL mode (ignore if already set or locked)
3. Retry on lock with exponential backoff (0.1s, 0.2s, 0.4s)
4. Raise error after max retries

**Returns**: `sqlite3.Connection`

**Error Handling**: Catches `sqlite3.OperationalError` for locks, retries up to MAX_RETRIES

### Class: `WaftEntity`

**Purpose**: Central consciousness - wraps all actions in error handling

#### `__init__(self)`

**Behavior**:
- Calls `_init_memory()` to set up database
- Creates tables if they don't exist
- Seeds initial artifact if database is empty
- Logs seed chronicle entry in same transaction

#### `_init_memory(self)`

**Behavior**:
- Creates `chronicle` and `artifacts` tables
- Checks if artifacts table is empty
- If empty, inserts seed artifact and logs chronicle entry
- Commits transaction
- Closes connection

**Error Handling**: Uses `get_db_connection()` with try/finally

#### `chronicle(self, level: Severity, message: str, context: str = "")`

**Purpose**: Log an event to the chronicle

**Parameters**:
- `level`: Severity enum (THOUGHT, STRAIN, TRAUMA)
- `message`: Human-readable message
- `context`: Optional additional context (default: "")

**Behavior**:
- Gets current timestamp
- Inserts into chronicle table
- Commits transaction
- Closes connection

#### `safe_breath(self, ritual_func, *args)`

**Purpose**: Protective wrapper - executes function and logs TRAUMA on failure

**Parameters**:
- `ritual_func`: Function to execute
- `*args`: Arguments to pass to function

**Returns**: Dictionary with:
- `success`: Boolean
- `data`: Function result (if successful) or `error`: Error message (if failed)
- `duration`: Execution time in milliseconds

**Behavior**:
- Records start time
- Executes function in try/except
- On success: returns result with duration
- On failure: logs TRAUMA with traceback, returns error dict

#### `pulse(self)`

**Purpose**: Check vitals - get current state

**Returns**: Tuple of (logs DataFrame, artifacts DataFrame)

**Behavior**:
- Queries last 50 chronicle entries (ordered by id DESC)
- Queries all artifacts
- Returns as pandas DataFrames

#### `get_next_manifestation(self)`

**Purpose**: Find next artifact that needs to be printed

**Returns**: Tuple of artifact row data or None

**Behavior**:
- Queries artifacts with status='VOID'
- Returns first match (LIMIT 1)
- Returns None if no pending artifacts

#### `confirm_birth(self, artifact_id)`

**Purpose**: Mark artifact as PHYSICAL (successfully printed)

**Parameters**:
- `artifact_id`: Integer ID of artifact

**Behavior**:
- Updates artifact status to 'PHYSICAL'
- Sets birth_time to current timestamp
- Commits transaction
- Closes connection
- Logs chronicle entry (THOUGHT) after connection closed

#### `get_data_hash(self)`

**Purpose**: Get hash of current data state for change detection

**Returns**: MD5 hash string (hexdigest)

**Behavior**:
- Queries MAX(id) and COUNT(*) from chronicle
- Queries COUNT(*) and COUNT(CASE WHEN status='VOID') from artifacts
- Creates state string: `"{max_id}_{count}_{total}_{void_count}"`
- Returns MD5 hash of state string

**Purpose**: Lightweight change detection without reading all data

#### Export Methods

##### `export_json(self)`

**Returns**: JSON string with:
- `entity`: "WAFT_ENTITY_LARVAL"
- `export_timestamp`: ISO datetime
- `chronicle`: Array of log records
- `artifacts`: Array of artifact records
- `statistics`: Object with counts (thoughts, strains, traumas, artifacts, void, physical)

**Note**: Uses `json.dumps(data, indent=2, default=str)` for datetime serialization

##### `export_markdown(self)`

**Returns**: Markdown string with:
- Title and export date
- Statistics section
- Chronicle section (formatted with emojis)
- Artifacts section (with G-code blocks)

**Formatting**:
- Severity emojis: THOUGHT=💭, STRAIN=⚠️, TRAUMA=🔴
- G-code blocks: ```gcode ... ```
- Sections separated by `---`

##### `export_txt(self)`

**Returns**: Plain text string with:
- Header with export date
- Statistics section
- Chronicle entries (one per line)
- Artifacts with details

**Format**: Plain ASCII, no markdown formatting

##### `export_pdf_bytes(self)`

**Returns**: PDF bytes or None

**Behavior**:
- Attempts to use `src.waft.evolution.pdf_generator.PDFGenerator`
- Converts markdown export to PDF
- Uses "clinical_standard" style
- Returns None if PDF generation fails (fallback to markdown)

**Dependencies**: Requires `src.waft.evolution.pdf_generator` module

---

## User Interface

### Page Configuration

```python
st.set_page_config(
    page_title="WAFT: LARVAL STAGE",
    page_icon="🌑",
    layout="wide"
)
```

### CSS Styling

**Theme**: Dark mode terminal aesthetic

```css
.stApp {
    background-color: #050505;
    color: #00ff41;
    font-family: 'Courier New', monospace;
}
.stDataFrame {
    border: 1px solid #333;
}
h1, h2, h3 {
    border-bottom: 1px solid #333;
    padding-bottom: 10px;
}
.trauma-alert {
    border: 1px solid red;
    background-color: #300;
    color: red;
    padding: 10px;
}
.auto-refresh-indicator {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #00ff41;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
```

### Header Section

**Layout**: Two columns (3:1 ratio)

**Left Column**:
- Title: "🌑 Waft Larval Form"
- Description: "What is this?" explanation

**Right Column**:
- Auto-refresh checkbox (🔄 Auto-refresh)
- Interval selector (2s, 3s, 5s, 10s) - shown when auto-refresh enabled
- Live indicator (pulsing dot + "Live" text) when auto-refresh enabled

### Quick Status Summary

**Layout**: Four columns with metrics

**Metrics**:
1. **Total Events**: Count of all chronicle entries
2. **Errors**: Count of TRAUMA entries (red delta if > 0)
3. **Total Artifacts**: Count of all artifacts
4. **Pending Jobs**: Count of artifacts with status='VOID'

**Component**: `st.metric()` with appropriate delta colors

### Dashboard Columns

**Layout**: Two columns (2:1 ratio)

#### Left Column: Activity Log

**Title**: "📋 Activity Log"
**Caption**: "All system events, actions, and errors are recorded here. This is the complete history of what the system has done."

**Content**:
- Trauma alert (if latest entry is TRAUMA)
- Dataframe with columns: timestamp, severity (with emojis), message
- Expander: "ℹ️ About Severity Levels" with explanations

**Severity Display**:
- THOUGHT → "💭 THOUGHT"
- STRAIN → "⚠️ STRAIN"
- TRAUMA → "🔴 TRAUMA"

#### Right Column: Print Job Management

**Title**: "🖨️ Print Job Management"
**Caption**: "Manage G-code files and track print job status. Artifacts start as VOID (pending) and become PHYSICAL (printed)."

**Content** (if pending artifact exists):
- Info box: "**Next Job**: {name}"
- Status: {status}
- Artifact ID: {part_id}
- Expander: "📄 View G-code" with code block
- Button: "🔌 Connect to Printer" (simulates connection)
- Button: "✅ Mark as Printed" (marks as PHYSICAL)

**Content** (if no pending artifacts):
- Success message: "✅ All Artifacts Complete"
- Info box with explanation
- Expander: "➕ How to Add More Artifacts"
  - Option 1: "🗑️ Delete Database & Restart" button
  - Option 2: SQL instructions

### Data Export Section

**Title**: "📥 Export Data"
**Caption**: "Download all data (activity logs, artifacts, statistics) in various formats for analysis or backup."

**Layout**: Four columns with download buttons

**Formats**:
1. **JSON**: `waft_entity_export_{timestamp}.json`
2. **Markdown**: `waft_entity_export_{timestamp}.md`
3. **TXT**: `waft_entity_export_{timestamp}.txt`
4. **PDF**: `waft_entity_export_{timestamp}.pdf` (or markdown fallback)

**Timestamp Format**: `YYYYMMDD_HHMMSS`

**Note**: All buttons have unique `key` parameters to prevent duplicate widget errors

### Footer

**Content**: Status line with:
- Database filename
- Event count
- Refresh status (🔄 Auto or ⏸️ Manual)
- System status (✅ System operational)

### Help Section

**Expander**: "❓ Help & Information"

**Content**:
- What is Waft Larval Form?
- How It Works (artifacts, activity log, database)
- Key Features (error resilience, data export, status tracking, activity history)
- Terminology (artifact, chronicle, trauma, VOID/PHYSICAL)

---

## Reactive Live Reload System

### Purpose

Automatically update UI when database changes occur, with minimal overhead and user control.

### State Tracking

**Session State Variables**:
- `last_data_hash`: MD5 hash of last known data state
- `auto_refresh_enabled`: Boolean (default: True)
- `refresh_interval`: Integer seconds (default: 3)

### Initialization

```python
if 'last_data_hash' not in st.session_state:
    st.session_state.last_data_hash = entity.get_data_hash()
if 'auto_refresh_enabled' not in st.session_state:
    st.session_state.auto_refresh_enabled = True
if 'refresh_interval' not in st.session_state:
    st.session_state.refresh_interval = 3
```

### Update Logic

**Location**: End of `main()` function, after all UI rendering

**Behavior**:
1. If auto-refresh enabled:
   - Get current data hash
   - Compare with `last_data_hash`
   - If changed:
     - Update `last_data_hash`
     - Sleep 0.1s (prevent rapid reruns)
     - Call `st.rerun()`
   - If unchanged:
     - Inject JavaScript to schedule next check
     - JavaScript triggers rerun after interval

**JavaScript Code**:
```javascript
setTimeout(function() {
    if (window.parent && window.parent.postMessage) {
        window.parent.postMessage({
            type: 'streamlit:rerun',
            isStreamlitMessage: true
        }, '*');
    }
}, {refresh_interval * 1000});
```

**Injection**: `st.markdown(refresh_js, unsafe_allow_html=True)`

### Performance

- **Hash Calculation**: ~1-2ms (queries metadata only)
- **JavaScript Injection**: ~0ms (just markup)
- **No Blocking**: Non-blocking JavaScript scheduling
- **Efficient**: Only reruns when data actually changes

---

## Data Export

### Export Methods

All export methods call `self.pulse()` to get current data.

### JSON Export

**Format**: Pretty-printed JSON with 2-space indentation

**Structure**:
```json
{
  "entity": "WAFT_ENTITY_LARVAL",
  "export_timestamp": "2026-01-12 15:30:45",
  "chronicle": [...],
  "artifacts": [...],
  "statistics": {
    "total_thoughts": 10,
    "total_strains": 2,
    "total_traumas": 1,
    "total_artifacts": 5,
    "void_artifacts": 2,
    "physical_artifacts": 3
  }
}
```

**Note**: Uses `default=str` for datetime serialization

### Markdown Export

**Sections**:
1. Title and export date
2. Statistics (bulleted list)
3. Chronicle entries (formatted with emojis, timestamps, code blocks for context)
4. Artifacts (with G-code blocks)

**Formatting**: Uses markdown headers, code blocks, horizontal rules

### TXT Export

**Format**: Plain ASCII text

**Sections**:
1. Header with export date
2. Statistics (plain text)
3. Chronicle entries (one per line)
4. Artifacts (with details)

### PDF Export

**Method**: Attempts to use `PDFGenerator.from_content()`

**Parameters**:
- `content`: Markdown export string
- `title`: "WAFT Entity - Larval Stage Export"
- `style`: "clinical_standard"

**Fallback**: If PDF generation fails, returns None (UI shows markdown download button)

---

## Error Handling

### Database Connection

**Retry Logic**:
- Max retries: 3
- Initial delay: 0.1s
- Exponential backoff: 0.1s, 0.2s, 0.4s
- Timeout: 10.0 seconds

**WAL Mode**:
- Attempts to set WAL mode on connection
- Ignores errors if already set or locked

**Connection Cleanup**:
- All database operations use `try...finally` blocks
- Connections always closed in finally block

### Application Errors

**Safe Breath Wrapper**:
- All critical operations wrapped in `safe_breath()`
- Errors logged as TRAUMA with full traceback
- Application continues running

**UI Error Display**:
- Database lock errors: User-friendly message with refresh instruction
- Other database errors: Error message displayed
- Trauma alerts: Red alert box in Activity Log

### Initialization Errors

**Entity Creation**:
- If database locked: Error message, stop execution
- If other error: Error message, stop execution
- Graceful failure with user feedback

---

## Dependencies

### Required Packages

```python
streamlit>=1.28.0
pandas>=2.0.0
pyserial>=3.5
```

### Standard Library

```python
import sqlite3
import time
import traceback
import random
import json
import hashlib
from datetime import datetime
from enum import Enum
import serial.tools.list_ports
```

### Optional Dependencies

- `src.waft.evolution.pdf_generator`: For PDF export (fallback to markdown if unavailable)

---

## File Structure

### Main Application

**File**: `waft_larva.py`

**Structure**:
1. Imports
2. Configuration constants
3. `get_db_connection()` function
4. `Severity` enum
5. `WaftEntity` class
6. `main()` function (Streamlit UI)

**Size**: ~650 lines

### Test File

**File**: `test_waft_larva.py`

**Purpose**: Unit tests for `WaftEntity` class

**Tests**:
- Database initialization
- Chronicle logging
- Artifact management
- Export functionality

### Documentation Files

- `docs/LARVA_TO_MATURE_MIGRATION.md`: Migration guide
- `WAFT_LARVA_IMPLEMENTATION_SUMMARY.md`: Implementation summary
- `CHANGELOG.md`: Version history

---

## Testing Requirements

### Unit Tests

**Test File**: `test_waft_larva.py`

**Test Cases**:
1. Database initialization creates tables
2. Seed data inserted on first run
3. Chronicle logging works for all severity levels
4. Artifact creation and status updates
5. Export methods return correct formats
6. Data hash changes when data changes

### Manual Testing

**Test Scenarios**:
1. First run: Verify seed data appears
2. Mark artifact as printed: Verify status updates
3. Add artifact via SQL: Verify appears in UI
4. Export data: Verify all formats work
5. Auto-refresh: Verify UI updates when data changes
6. Error handling: Verify TRAUMA logged, app continues

### Integration Testing

**Test Scenarios**:
1. Database persistence across restarts
2. Concurrent access (multiple Streamlit instances)
3. Large datasets (100+ artifacts, 1000+ chronicle entries)
4. PDF generation with/without PDFGenerator module

---

## Migration Requirements

### Future Redbean Migration

**Requirement**: Database schema must match exactly

**Migration Steps**:
1. Stop Larval Form application
2. Copy `waft_memory.db` to Redbean directory
3. Redbean reads same database file
4. Memory transfers seamlessly

**Schema Compatibility**:
- Table names: `chronicle`, `artifacts`
- Column names: Must match exactly
- Data types: TEXT, INTEGER (SQLite compatible)
- Seed data: Compatible format

### Version Compatibility

**Current Version**: v0.6.0

**Version History**:
- v0.1: Initial implementation
- v0.5.2: Database lock fixes
- v0.6.0: UI improvements, reactive system, data export

---

## Implementation Checklist

### Core Functionality

- [x] Database schema (chronicle, artifacts)
- [x] WaftEntity class with all methods
- [x] Chronicle logging system
- [x] Artifact management
- [x] Safe breath error handling
- [x] Database connection with retry logic
- [x] WAL mode for concurrency

### User Interface

- [x] Streamlit UI with dark mode
- [x] Header with auto-refresh controls
- [x] Status summary dashboard
- [x] Activity log panel
- [x] Print job management panel
- [x] Data export section
- [x] Help section
- [x] Footer with status

### Reactive System

- [x] Data hash calculation
- [x] State tracking (session state)
- [x] Auto-refresh controls
- [x] JavaScript-based scheduling
- [x] Change detection logic
- [x] Visual indicators

### Data Export

- [x] JSON export
- [x] Markdown export
- [x] TXT export
- [x] PDF export (with fallback)

### Error Handling

- [x] Database retry logic
- [x] Connection cleanup
- [x] Safe breath wrapper
- [x] UI error display
- [x] Trauma logging

### Testing

- [x] Unit tests
- [x] Manual testing scenarios
- [x] Integration testing

### Documentation

- [x] Implementation summary
- [x] Migration guide
- [x] Complete specification (this document)

---

## Example Usage

### Running the Application

```bash
pip install streamlit pandas pyserial
streamlit run waft_larva.py
```

### Adding Artifacts via SQL

```sql
sqlite3 waft_memory.db

INSERT INTO artifacts (name, gcode, status)
VALUES ('New_Artifact_Name', 'G28\nG1 X10 Y10', 'VOID');
```

### Exporting Data

1. Click download button for desired format
2. File downloads with timestamp in filename
3. Open file in appropriate application

---

## Notes for AI Implementation

### Critical Requirements

1. **Database Schema**: Must match exactly for migration compatibility
2. **Error Handling**: All operations must use safe_breath or try/finally
3. **Connection Management**: Always close connections in finally blocks
4. **State Tracking**: Use session_state for reactive system
5. **UI Clarity**: Use clear labels, explanations, and help text

### Implementation Order

1. Database schema and connection logic
2. WaftEntity class (core methods)
3. Basic Streamlit UI
4. Export functionality
5. Reactive system
6. Error handling improvements
7. UI polish and help sections

### Common Pitfalls

1. **Database Locks**: Always use retry logic and WAL mode
2. **Connection Leaks**: Always close connections in finally blocks
3. **Duplicate Widget IDs**: Use unique `key` parameters for all Streamlit widgets
4. **Blocking Operations**: Use JavaScript for non-blocking auto-refresh
5. **Data Serialization**: Use `default=str` for JSON datetime serialization

---

**Specification Complete**: 2026-01-12 15:30
**Status**: ✅ Ready for implementation
**Version**: v0.6.0
