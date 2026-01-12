#!/usr/bin/env python3
"""
Generate Scientific PDF from Larval Form Specification

Transforms the technical specification into a scientific research document
and generates a professionally formatted PDF.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path for imports
# File is at: _work_efforts/WE-260112-.../generate_scientific_pdf.py
# Need to go up 3 levels to reach project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Read the specification
spec_path = Path(__file__).parent / "LARVAL_FORM_COMPLETE_SPECIFICATION.md"
with open(spec_path, 'r', encoding='utf-8') as f:
    spec_content = f.read()

# Transform into scientific research paper format
scientific_content = f"""# Waft Larval Form: Complete Technical Specification v0.6.0

**A Comprehensive Research Document on the Developmental Stage Architecture**

**Version**: v0.6.0  
**Date**: 2026-01-12  
**Status**: Complete Implementation  
**Document Type**: Technical Specification & Research Documentation

---

## Abstract

This document presents a complete technical specification for the Waft Larval Form, a Python-based application serving as the developmental stage preceding the Redbean "Mature Form" implementation. The system implements a 3D printing workflow manager that tracks G-code files and print jobs, built on a philosophical foundation termed "Hasvanism" (Breath, Memory, Trauma). The architecture demonstrates a novel approach to error resilience, where errors are not ignored but rather etched into persistent memory as "TRAUMA" events, allowing the system to continue operating while maintaining a complete historical record. The implementation utilizes Python 3.x with Streamlit for the user interface, SQLite 3 for persistent storage, and Pandas for data processing. The system features a reactive live reload mechanism, comprehensive data export capabilities, and a migration-ready database schema designed for seamless transition to the mature Redbean form. This specification provides complete implementation details including database schema, core classes, user interface components, error handling strategies, and testing requirements.

**Keywords**: Waft Larval Form, Hasvanism, Error Resilience, SQLite, Streamlit, 3D Printing Workflow, Database Migration

---

## 1. Introduction

### 1.1 Background and Purpose

The Waft Larval Form represents a transitional stage in the evolution of the Waft system architecture, designed as a developmental precursor to the Redbean "Mature Form". This application serves as a 3D printing workflow manager that tracks G-code files and print jobs, implementing a unique philosophical framework that guides both its design and operational behavior.

### 1.2 Core Philosophy: Hasvanism

The system is built upon three fundamental principles:

1. **Breath**: Runtime logic that executes upon interaction
2. **Memory**: Persistent storage of state and history (SQLite)
3. **Trauma**: Refusal to ignore errors; they are etched into memory

This philosophical foundation creates an entity that "breathes" (executes logic), "remembers" (persists to database), and "feels pain" (logs errors as TRAUMA). Unlike traditional error handling approaches that may suppress or ignore errors, this system maintains a complete chronicle of all events, including failures, ensuring that the system's history is preserved and can be analyzed.

### 1.3 Key Design Principles

- **Error Resilience**: Errors are logged, not ignored - the system continues running
- **Migration-Ready**: Database schema matches future Redbean version exactly
- **Complete Observability**: All system events, thoughts, and errors are recorded
- **Reactive Updates**: Automatic UI updates when database changes occur

---

## 2. Methodology

### 2.1 Technology Stack

The application is built using:

- **Language**: Python 3.x
- **UI Framework**: Streamlit
- **Database**: SQLite 3 with WAL (Write-Ahead Logging) mode
- **Data Processing**: Pandas
- **Serial Communication**: PySerial (for future printer integration)

### 2.2 Application Architecture

The system follows a single-file application structure:

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

### 2.3 Database Schema Design

The database schema consists of two primary tables designed to support the Hasvanism philosophy:

#### 2.3.1 Chronicle Table

The `chronicle` table serves as the "stream of consciousness" - recording all events, thoughts, and errors:

```sql
CREATE TABLE IF NOT EXISTS chronicle (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    severity TEXT,
    message TEXT,
    context TEXT
)
```

**Severity Levels**:
- `THOUGHT`: Normal system activity (startup, successful operations)
- `STRAIN`: Warnings or non-critical issues
- `TRAUMA`: Errors that were caught and logged (system continues running)

#### 2.3.2 Artifacts Table

The `artifacts` table represents the "physical body" - G-code files and print jobs:

```sql
CREATE TABLE IF NOT EXISTS artifacts (
    id INTEGER PRIMARY KEY,
    name TEXT,
    gcode TEXT,
    status TEXT DEFAULT 'VOID',
    birth_time TEXT
)
```

**Status Flow**:
- `VOID`: Pending print job (not yet printed)
- `MANIFESTING`: Currently being printed (future state)
- `PHYSICAL`: Successfully printed (complete)

---

## 3. Implementation Details

### 3.1 Core Classes and Functions

#### 3.1.1 Configuration Constants

```python
DB_NAME = "waft_memory.db"
DB_TIMEOUT = 10.0  # Seconds to wait for database lock
MAX_RETRIES = 3
RETRY_DELAY = 0.1  # Initial delay between retries (seconds)
```

#### 3.1.2 Severity Enumeration

```python
class Severity(Enum):
    THOUGHT = "THOUGHT"   # Routine internal monologue
    STRAIN = "STRAIN"     # Non-critical resistance
    TRAUMA = "TRAUMA"     # Critical failure / Severance
```

#### 3.1.3 Database Connection Management

The `get_db_connection()` function implements robust connection handling:

- Attempts connection with timeout (10.0 seconds)
- Sets WAL mode (ignores if already set or locked)
- Retries on lock with exponential backoff (0.1s, 0.2s, 0.4s)
- Raises error after max retries

#### 3.1.4 WaftEntity Class

The `WaftEntity` class serves as the central consciousness, wrapping all actions in error handling:

**Key Methods**:
- `__init__()`: Initializes database and seeds initial artifact
- `chronicle()`: Logs events to the chronicle
- `safe_breath()`: Protective wrapper that executes functions and logs TRAUMA on failure
- `pulse()`: Checks vitals - returns current state as DataFrames
- `get_next_manifestation()`: Finds next artifact that needs to be printed
- `confirm_birth()`: Marks artifact as PHYSICAL (successfully printed)
- `get_data_hash()`: Returns MD5 hash of current data state for change detection

**Export Methods**:
- `export_json()`: Returns JSON string with complete entity data
- `export_markdown()`: Returns formatted markdown string
- `export_txt()`: Returns plain ASCII text
- `export_pdf_bytes()`: Attempts PDF generation using PDFGenerator

### 3.2 User Interface Components

#### 3.2.1 Page Configuration

```python
st.set_page_config(
    page_title="WAFT: LARVAL STAGE",
    page_icon="🌑",
    layout="wide"
)
```

#### 3.2.2 Visual Design

The interface employs a dark mode terminal aesthetic with:
- Background: `#050505`
- Text color: `#00ff41` (terminal green)
- Font: `'Courier New', monospace`
- Visual indicators for severity levels (emojis: 💭 THOUGHT, ⚠️ STRAIN, 🔴 TRAUMA)

#### 3.2.3 Dashboard Layout

**Header Section**: Two columns (3:1 ratio)
- Left: Title and description
- Right: Auto-refresh controls and live indicator

**Quick Status Summary**: Four metrics
- Total Events
- Errors (TRAUMA count)
- Total Artifacts
- Pending Jobs

**Main Dashboard**: Two columns (2:1 ratio)
- Left: Activity Log (chronicle entries)
- Right: Print Job Management

**Data Export Section**: Four download buttons (JSON, Markdown, TXT, PDF)

### 3.3 Reactive Live Reload System

The system implements automatic UI updates through:

1. **State Tracking**: MD5 hash of data state stored in session state
2. **Change Detection**: Compares current hash with last known hash
3. **Update Mechanism**: JavaScript-based scheduling for non-blocking updates
4. **Performance**: Hash calculation ~1-2ms (queries metadata only)

**Session State Variables**:
- `last_data_hash`: MD5 hash of last known data state
- `auto_refresh_enabled`: Boolean (default: True)
- `refresh_interval`: Integer seconds (default: 3)

---

## 4. Results and Features

### 4.1 Data Export Capabilities

The system provides comprehensive data export in multiple formats:

1. **JSON Export**: Pretty-printed JSON with complete entity data, statistics, and timestamps
2. **Markdown Export**: Formatted markdown with emojis, code blocks, and structured sections
3. **TXT Export**: Plain ASCII text for simple text processing
4. **PDF Export**: Professional PDF generation using PDFGenerator with "clinical_standard" style

### 4.2 Error Handling Strategy

#### 4.2.1 Database Connection Resilience

- **Retry Logic**: 3 attempts with exponential backoff
- **WAL Mode**: Write-Ahead Logging for concurrency support
- **Connection Cleanup**: All operations use try/finally blocks
- **Timeout**: 10.0 seconds per connection attempt

#### 4.2.2 Application Error Management

- **Safe Breath Wrapper**: All critical operations wrapped in `safe_breath()`
- **Trauma Logging**: Errors logged as TRAUMA with full traceback
- **Graceful Degradation**: Application continues running after errors
- **User Feedback**: Clear error messages displayed in UI

### 4.3 Reactive Update System

The reactive system provides:
- **Efficient Change Detection**: MD5 hash comparison (~1-2ms)
- **Non-Blocking Updates**: JavaScript-based scheduling
- **User Control**: Configurable auto-refresh with interval selection
- **Visual Indicators**: Live status indicator when auto-refresh enabled

---

## 5. Discussion

### 5.1 Testing Requirements

#### 5.1.1 Unit Tests

Test cases cover:
- Database initialization and table creation
- Seed data insertion on first run
- Chronicle logging for all severity levels
- Artifact creation and status updates
- Export methods format validation
- Data hash change detection

#### 5.1.2 Manual Testing Scenarios

- First run verification (seed data appearance)
- Status update verification (marking artifacts as printed)
- Data export functionality (all formats)
- Auto-refresh behavior (UI updates on data changes)
- Error handling verification (TRAUMA logging, app continuation)

#### 5.1.3 Integration Testing

- Database persistence across restarts
- Concurrent access (multiple Streamlit instances)
- Large datasets (100+ artifacts, 1000+ chronicle entries)
- PDF generation with/without PDFGenerator module

### 5.2 Migration Requirements

#### 5.2.1 Future Redbean Migration

The database schema is designed for seamless migration:

1. Stop Larval Form application
2. Copy `waft_memory.db` to Redbean directory
3. Redbean reads same database file
4. Memory transfers seamlessly

**Schema Compatibility Requirements**:
- Table names: `chronicle`, `artifacts` (must match exactly)
- Column names: Must match exactly
- Data types: TEXT, INTEGER (SQLite compatible)
- Seed data: Compatible format

#### 5.2.2 Version History

- **v0.1**: Initial implementation
- **v0.5.2**: Database lock fixes
- **v0.6.0**: UI improvements, reactive system, data export

### 5.3 Implementation Considerations

#### 5.3.1 Critical Requirements

1. **Database Schema**: Must match exactly for migration compatibility
2. **Error Handling**: All operations must use safe_breath or try/finally
3. **Connection Management**: Always close connections in finally blocks
4. **State Tracking**: Use session_state for reactive system
5. **UI Clarity**: Use clear labels, explanations, and help text

#### 5.3.2 Common Pitfalls

1. **Database Locks**: Always use retry logic and WAL mode
2. **Connection Leaks**: Always close connections in finally blocks
3. **Duplicate Widget IDs**: Use unique `key` parameters for all Streamlit widgets
4. **Blocking Operations**: Use JavaScript for non-blocking auto-refresh
5. **Data Serialization**: Use `default=str` for JSON datetime serialization

---

## 6. Conclusions

### 6.1 Implementation Status

The Waft Larval Form specification is complete and ready for implementation. All core functionality, user interface components, reactive systems, data export capabilities, error handling, and testing requirements have been fully specified.

### 6.2 Key Achievements

- **Complete Specification**: All aspects of the system documented
- **Migration-Ready Design**: Database schema compatible with future Redbean form
- **Error Resilience**: Novel approach to error handling through TRAUMA logging
- **Reactive Architecture**: Efficient change detection and automatic UI updates
- **Comprehensive Export**: Multiple format support for data analysis and backup

### 6.3 Future Work

The system is designed as a developmental stage, with the following future considerations:

- Migration to Redbean "Mature Form"
- Enhanced printer integration capabilities
- Extended artifact management features
- Advanced analytics and reporting

---

## 7. Appendices

### Appendix A: Dependencies

#### Required Packages

```python
streamlit>=1.28.0
pandas>=2.0.0
pyserial>=3.5
```

#### Standard Library Imports

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

#### Optional Dependencies

- `src.waft.evolution.pdf_generator`: For PDF export (fallback to markdown if unavailable)

### Appendix B: File Structure

#### Main Application

**File**: `waft_larva.py` (~650 lines)

**Structure**:
1. Imports
2. Configuration constants
3. `get_db_connection()` function
4. `Severity` enum
5. `WaftEntity` class
6. `main()` function (Streamlit UI)

#### Test File

**File**: `test_waft_larva.py`

**Purpose**: Unit tests for `WaftEntity` class

#### Documentation Files

- `docs/LARVA_TO_MATURE_MIGRATION.md`: Migration guide
- `WAFT_LARVA_IMPLEMENTATION_SUMMARY.md`: Implementation summary
- `CHANGELOG.md`: Version history

### Appendix C: Example Usage

#### Running the Application

```bash
pip install streamlit pandas pyserial
streamlit run waft_larva.py
```

#### Adding Artifacts via SQL

```sql
sqlite3 waft_memory.db

INSERT INTO artifacts (name, gcode, status) 
VALUES ('New_Artifact_Name', 'G28\nG1 X10 Y10', 'VOID');
```

#### Exporting Data

1. Click download button for desired format
2. File downloads with timestamp in filename
3. Open file in appropriate application

### Appendix D: Implementation Checklist

#### Core Functionality

- [x] Database schema (chronicle, artifacts)
- [x] WaftEntity class with all methods
- [x] Chronicle logging system
- [x] Artifact management
- [x] Safe breath error handling
- [x] Database connection with retry logic
- [x] WAL mode for concurrency

#### User Interface

- [x] Streamlit UI with dark mode
- [x] Header with auto-refresh controls
- [x] Status summary dashboard
- [x] Activity log panel
- [x] Print job management panel
- [x] Data export section
- [x] Help section
- [x] Footer with status

#### Reactive System

- [x] Data hash calculation
- [x] State tracking (session state)
- [x] Auto-refresh controls
- [x] JavaScript-based scheduling
- [x] Change detection logic
- [x] Visual indicators

#### Data Export

- [x] JSON export
- [x] Markdown export
- [x] TXT export
- [x] PDF export (with fallback)

#### Error Handling

- [x] Database retry logic
- [x] Connection cleanup
- [x] Safe breath wrapper
- [x] UI error display
- [x] Trauma logging

#### Testing

- [x] Unit tests
- [x] Manual testing scenarios
- [x] Integration testing

#### Documentation

- [x] Implementation summary
- [x] Migration guide
- [x] Complete specification (this document)

---

## References

1. Waft Larval Form Implementation Summary (2026-01-12)
2. Larva to Mature Migration Guide
3. Waft System Architecture Documentation
4. SQLite WAL Mode Documentation
5. Streamlit Framework Documentation

---

**Document Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Specification Version**: v0.6.0  
**Status**: Complete Implementation  
**Document Type**: Scientific Research & Technical Specification
"""

# Generate PDF using ScientificPDFGenerator
try:
    from src.waft.evolution.scientific_pdf_generator import ScientificPDFGenerator
    use_scientific = True
except ImportError:
    try:
        from src.waft.evolution.pdf_generator import PDFGenerator
        use_scientific = False
        print("⚠️  ScientificPDFGenerator not available, using PDFGenerator instead")
    except ImportError as e:
        print(f"❌ Error: Required dependencies not installed: {e}")
        print("   Please install: pip install jinja2 weasyprint")
        sys.exit(1)

print("🔬 Generating scientific PDF from specification...")
print(f"📄 Source: {spec_path}")
print(f"📊 Content length: {len(scientific_content)} characters")

# Generate PDF with clinical_standard style (academic formatting)
output_path = spec_path.parent / "LARVAL_FORM_COMPLETE_SPECIFICATION.pdf"

if use_scientific:
    pdf_path = ScientificPDFGenerator.from_content(
        content=scientific_content,
        title="Waft Larval Form: Complete Technical Specification v0.6.0",
        style="clinical_standard",  # Academic style: Times New Roman, 1-inch margins
        scientific_mode=True
    ).save(
        output_path=output_path,
        open_pdf=False,
        collect_metrics=True,
        convert_to_png=True,
        png_dpi=300
    )
else:
    pdf_path = PDFGenerator.from_content(
        content=scientific_content,
        title="Waft Larval Form: Complete Technical Specification v0.6.0",
        style="clinical_standard"  # Academic style: Times New Roman, 1-inch margins
    ).save(
        output_path=output_path,
        open_pdf=False,
        convert_to_png=True,
        png_dpi=300
    )

print(f"✅ PDF generated: {pdf_path}")
print(f"📄 File size: {pdf_path.stat().st_size / 1024:.2f} KB")

# Check for analysis file
analysis_path = pdf_path.with_suffix('.analysis.json')
if analysis_path.exists():
    import json
    with open(analysis_path) as f:
        analysis = json.load(f)
    print(f"\n🔬 Quality Analysis:")
    print(f"   Completeness: {analysis.get('scores', {}).get('completeness', 0):.2f}")
    print(f"   Structure: {analysis.get('scores', {}).get('structure', 0):.2f}")
    print(f"   Gaps: {len(analysis.get('gaps', []))}")
    print(f"   Suggestions: {len(analysis.get('suggestions', []))}")

print("\n✅ Scientific PDF generation complete!")
