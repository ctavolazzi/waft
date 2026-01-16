# PDF Tracing Guide

## Overview

The PDF tracing system tracks where PDFs are stored, where they've been moved, and provides full audit history. This allows you to always find where PDFs are located, even if they've been moved or renamed.

## Features

- **Location Tracking**: Know where every PDF is currently stored
- **Movement History**: Track when PDFs are moved or renamed
- **Audit Log**: Complete history of all file operations
- **Query Capabilities**: Search PDFs by pattern, location, date, etc.
- **Automatic Registration**: PDFs are automatically registered when saved

## Usage

### Command Line Tool

Use the `trace_pdf.py` script for quick PDF tracing:

```bash
# Show storage statistics
python scripts/trace_pdf.py --stats

# List all PDFs
python scripts/trace_pdf.py --list

# Trace a specific PDF
python scripts/trace_pdf.py session_recap_20260115.pdf

# Search for PDFs
python scripts/trace_pdf.py --search session

# Show only PDFs on external drive
python scripts/trace_pdf.py --external-only

# View audit log
python scripts/trace_pdf.py --audit
```

### Python API

#### Find PDF Location

```python
from src.waft.utils import find_pdf_location

# Find where a PDF is stored
location = find_pdf_location("session_recap_20260115.pdf")
print(location)
# Output: /Volumes/Easystore/waft/active-waft/_work_efforts/session_recaps/session_recap_20260115.pdf
```

#### Trace PDF (Full History)

```python
from src.waft.utils import trace_pdf

# Get full trace information
trace = trace_pdf("session_recap_20260115.pdf")

print(f"Current Location: {trace['current_location']}")
print(f"Content Type: {trace['content_type']}")
print(f"Move Count: {trace['move_count']}")
print(f"All Locations: {trace['all_locations']}")
print(f"History: {trace['history']}")
```

#### Search PDFs

```python
from src.waft.utils import StorageRegistry

registry = StorageRegistry()

# Find all PDFs matching pattern
pdfs = registry.find_pdfs(pattern="session", limit=10)

# Find PDFs on external drive
external_pdfs = registry.find_pdfs(content_type="augmented")

# Find PDFs by date range
recent_pdfs = registry.find_pdfs(
    date_from="2026-01-01",
    date_to="2026-01-31"
)
```

#### Track File Moves

```python
from src.waft.utils import track_pdf_move
from pathlib import Path

# Track when a PDF is moved/renamed
track_pdf_move(
    old_path=Path("_work_efforts/old_name.pdf"),
    new_path=Path("_work_efforts/new_name.pdf")
)
```

#### Query Audit Log

```python
from src.waft.utils import StorageRegistry

registry = StorageRegistry()

# Get recent operations
recent_ops = registry.query_audit_log(limit=50)

# Filter by operation type
moves = registry.query_audit_log(operation="moved")

# Filter by date
today_ops = registry.query_audit_log(
    date_from="2026-01-15T00:00:00",
    date_to="2026-01-15T23:59:59"
)
```

## How It Works

### Automatic Registration

When PDFs are saved using the storage system, they're automatically registered:

1. **PDF Generation**: When a PDF is created (via `PDFGenerator.save()`, `DocumentBuilder.generate()`, etc.)
2. **Path Resolution**: The storage path resolver determines where to save it (local or external drive)
3. **Registration**: The PDF is registered in the storage registry with:
   - Relative path
   - Absolute storage location
   - Content type (core/augmented)
   - Timestamp
   - Operation type

### Movement Tracking

When PDFs are moved or renamed:

1. **Detect Move**: Use `track_pdf_move()` to register the move
2. **Update Registry**: Old entry is updated, new entry is created
3. **Audit Log**: Operation is logged to audit log file
4. **History Preserved**: Full history of moves is maintained

### Storage Registry

The registry is stored at:
- **Registry File**: `_pyrite/.storage_registry.json`
- **Audit Log**: `_pyrite/.storage_audit_log.jsonl`

Both files are:
- Protected with restrictive permissions (0o600)
- Updated atomically (temp file + rename)
- Locked for concurrent access

## Examples

### Example 1: Find a PDF

```python
from src.waft.utils import find_pdf_location

# Find by filename
location = find_pdf_location("session_recap_20260115.pdf")
if location:
    print(f"Found at: {location}")
else:
    print("PDF not found in registry")
```

### Example 2: Trace PDF History

```python
from src.waft.utils import trace_pdf

trace = trace_pdf("session_recap_20260115.pdf")

if trace['found']:
    print(f"Current: {trace['current_location']}")
    print(f"Moved {trace['move_count']} times")
    print("\nAll Locations:")
    for loc in trace['all_locations']:
        print(f"  - {loc}")
    print("\nHistory:")
    for entry in trace['history']:
        print(f"  {entry['timestamp']}: {entry['operation']}")
```

### Example 3: Search for PDFs

```python
from src.waft.utils import StorageRegistry

registry = StorageRegistry()

# Find all session recaps
session_pdfs = registry.find_pdfs(pattern="session_recap")

# Find PDFs created today
from datetime import datetime
today = datetime.now().strftime("%Y-%m-%d")
today_pdfs = registry.find_pdfs(
    date_from=f"{today}T00:00:00",
    date_to=f"{today}T23:59:59"
)

# Find PDFs on external drive
external_pdfs = registry.find_pdfs(content_type="augmented")
```

### Example 4: Get Storage Statistics

```python
from src.waft.utils import StorageRegistry

registry = StorageRegistry()
stats = registry.get_storage_stats()

print(f"Total PDFs: {stats['total_pdfs']}")
print(f"On External: {stats['pdfs_on_external']}")
print(f"Local: {stats['pdfs_local']}")
print(f"External Available: {stats['external_drive_available']}")
```

## Registry Structure

### Registry Entry

```json
{
  "_work_efforts/session_recaps/report.pdf": {
    "storage_location": "/Volumes/Easystore/waft/active-waft/_work_efforts/session_recaps/report.pdf",
    "content_type": "augmented",
    "timestamp": "2026-01-15T07:48:56",
    "last_operation": "created",
    "history": [
      {
        "operation": "created",
        "location": "/Volumes/Easystore/waft/active-waft/_work_efforts/session_recaps/report.pdf",
        "timestamp": "2026-01-15T07:48:56"
      }
    ]
  }
}
```

### Audit Log Entry

```json
{
  "timestamp": "2026-01-15T07:48:56",
  "content_path": "_work_efforts/session_recaps/report.pdf",
  "operation": "created",
  "location": "/Volumes/Easystore/waft/active-waft/_work_efforts/session_recaps/report.pdf",
  "content_type": "augmented"
}
```

## Integration

The tracing system is automatically integrated into:

- `PDFGenerator.save()` - Registers PDFs when saved
- `DocumentBuilder.generate()` - Registers PDFs when generated
- `PDFEvolution.evolve_pdf()` - Registers evolved PDFs
- All PDF generators route through `resolve_output_path()` which registers content

## Manual Tracking

If you move PDFs outside the system, use `track_pdf_move()`:

```python
from src.waft.utils import track_pdf_move
from pathlib import Path

# Track a manual move
track_pdf_move(
    old_path=Path("_work_efforts/old.pdf"),
    new_path=Path("_archive/2026/old.pdf")
)
```

## Troubleshooting

### PDF Not Found

If a PDF isn't found in the registry:

1. Check if it was saved using the storage system
2. Try searching by filename only: `find_pdf_location("filename.pdf")`
3. Use `--list` to see all registered PDFs
4. Check if PDF was created before tracing system was implemented

### Missing History

If history is missing:

1. Check audit log: `python scripts/trace_pdf.py --audit`
2. Verify registry file exists: `_pyrite/.storage_registry.json`
3. Check file permissions (should be 0o600)

### External Drive Not Detected

If external drive isn't detected:

1. Check drive is mounted: `ls /Volumes/Easystore`
2. Check drive is writable: `touch /Volumes/Easystore/test && rm /Volumes/Easystore/test`
3. Verify drive name matches (default: "Easystore")

## Best Practices

1. **Always use storage resolver**: Use `resolve_output_path()` or `get_storage_path()` when saving PDFs
2. **Track manual moves**: Use `track_pdf_move()` when moving files outside the system
3. **Regular queries**: Use `find_pdfs()` to discover PDFs, don't rely on filesystem searches
4. **Check registry**: Use `--stats` to monitor storage distribution
5. **Audit regularly**: Review audit log to understand file operations

## Security

- Registry files have restrictive permissions (0o600)
- Path validation prevents path traversal attacks
- Symlink detection prevents security issues
- All operations are logged for audit

---

**The tracing system ensures you always know where your PDFs are, where they've been, and where they're going.**
