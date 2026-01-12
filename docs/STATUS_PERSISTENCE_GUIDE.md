# Status Persistence Guide

**Save and track status snapshots with checksum integrity**

## Overview

The `StatusPersistence` system provides status snapshot saving, history tracking, and comparison utilities. Inspired by AI-DnD's save system pattern with checksum verification for data integrity.

## Quick Start

```python
from src.waft.core.status_persistence import save_status_snapshot, load_status_snapshot
from scripts.waft_status import check_status

# Get status and save snapshot
status = check_status()
snapshot = save_status_snapshot(status)

# Load snapshot later
loaded_status = load_status_snapshot(snapshot["snapshot_id"])
```

## Features

### 1. Snapshot Saving with Checksums

**Purpose**: Save status snapshots with MD5 checksums for integrity verification.

```python
from src.waft.core.status_persistence import StatusPersistence

persistence = StatusPersistence(Path.cwd())
snapshot = persistence.save_status_snapshot(status)

print(f"Snapshot ID: {snapshot['snapshot_id']}")
print(f"Checksum: {snapshot['checksum']}")
```

**Storage Location**: `_pyrite/.waft/status_snapshots/`

**Format**: JSON files with version, timestamp, status data, metadata, and checksum.

### 2. Integrity Verification

**Purpose**: Verify snapshot data hasn't been corrupted.

```python
# Load with integrity verification (default)
status = load_status_snapshot(snapshot_id, verify_integrity=True)

# Returns None if checksum doesn't match
if status is None:
    print("Snapshot integrity check failed!")
```

**How It Works**:
1. Calculate MD5 checksum of snapshot data (excluding checksum field)
2. Store checksum in snapshot
3. On load, recalculate and compare
4. Return `None` if mismatch detected

### 3. Snapshot Listing

**Purpose**: List all available snapshots.

```python
persistence = StatusPersistence(Path.cwd())

# List all snapshots
snapshots = persistence.list_snapshots()
for snapshot in snapshots:
    print(f"{snapshot['snapshot_id']}: {snapshot['timestamp']}")

# Get latest snapshot
latest_status = persistence.get_latest_snapshot()
```

### 4. Snapshot Comparison

**Purpose**: Compare two snapshots to see what changed.

```python
comparison = persistence.compare_snapshots("snapshot_1", "snapshot_2")

print(f"Differences: {len(comparison['differences'])}")
for path, diff in comparison['differences'].items():
    print(f"  {path}: {diff['old']} → {diff['new']}")
```

**Output Structure**:
```python
{
    "snapshot_1": "status_20260111_120000",
    "snapshot_2": "status_20260111_130000",
    "differences": {
        "epistemic_state.knowledge_pct": {
            "old": 50.0,
            "new": 65.0
        }
    },
    "unchanged": ["epistemic_state.moon_phase", ...]
}
```

### 5. Status History Tracking

**Purpose**: Track a specific metric over time.

```python
# Get history of epistemic knowledge percentage
history = persistence.get_status_history("epistemic_state.knowledge_pct", limit=10)

for entry in history:
    print(f"{entry['timestamp']}: {entry['value']}%")
```

**Metric Path Format**: Dot-separated path to metric (e.g., `"epistemic_state.knowledge_pct"`)

### 6. Cleanup Old Snapshots

**Purpose**: Keep only the most recent N snapshots.

```python
# Keep only the 100 most recent snapshots
deleted_count = persistence.cleanup_old_snapshots(keep_count=100)
print(f"Deleted {deleted_count} old snapshots")
```

## Integration with check_status()

### Command Line

```bash
# Save snapshot automatically
python scripts/waft_status.py --save-snapshot

# Check status and save snapshot
python scripts/waft_status.py --save-snapshot --generate-docs
```

### Programmatic

```python
from scripts.waft_status import check_status

# Save snapshot during status check
status = check_status(save_snapshot=True)
```

## Usage Examples

### Example 1: Basic Save and Load

```python
from src.waft.core.status_persistence import save_status_snapshot, load_status_snapshot
from scripts.waft_status import check_status

# Save snapshot
status = check_status(log_event=False)
snapshot = save_status_snapshot(status)
snapshot_id = snapshot["snapshot_id"]

# Load later
loaded_status = load_status_snapshot(snapshot_id)
assert loaded_status is not None
```

### Example 2: Track Status Over Time

```python
from src.waft.core.status_persistence import StatusPersistence

persistence = StatusPersistence(Path.cwd())

# Save daily snapshots
status = check_status(log_event=False)
persistence.save_status_snapshot(status, snapshot_id=f"daily_{datetime.now().strftime('%Y%m%d')}")

# Get history of overall health
history = persistence.get_status_history("overall_health_score", limit=30)
for entry in history:
    print(f"{entry['timestamp']}: {entry['value']}")
```

### Example 3: Compare Before/After Changes

```python
from src.waft.core.status_persistence import StatusPersistence

persistence = StatusPersistence(Path.cwd())

# Save "before" snapshot
status_before = check_status(log_event=False)
persistence.save_status_snapshot(status_before, snapshot_id="before_changes")

# ... make changes ...

# Save "after" snapshot
status_after = check_status(log_event=False)
persistence.save_status_snapshot(status_after, snapshot_id="after_changes")

# Compare
comparison = persistence.compare_snapshots("before_changes", "after_changes")
print(f"Changes detected: {len(comparison['differences'])}")
```

### Example 4: Integration with Typed State

```python
from src.waft.core.status_state import StatusState
from src.waft.core.status_persistence import save_status_snapshot

# Get typed state
status_dict = check_status(log_event=False)
typed_state = StatusState.from_dict(status_dict)

# Save snapshot (can use typed state's to_dict())
snapshot = save_status_snapshot(typed_state.to_dict())
```

## API Reference

### StatusPersistence Class

#### `__init__(project_path: Path)`
Initialize persistence manager.

#### `save_status_snapshot(status: Dict[str, Any], snapshot_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]`
Save status snapshot with checksum.

#### `load_status_snapshot(snapshot_id: str, verify_integrity: bool = True) -> Optional[Dict[str, Any]]`
Load and verify snapshot.

#### `list_snapshots(limit: Optional[int] = None) -> List[Dict[str, Any]]`
List all snapshots.

#### `get_latest_snapshot() -> Optional[Dict[str, Any]]`
Get most recent snapshot.

#### `compare_snapshots(snapshot_id_1: str, snapshot_id_2: str) -> Optional[Dict[str, Any]]`
Compare two snapshots.

#### `get_status_history(metric_path: str, limit: Optional[int] = None) -> List[Dict[str, Any]]`
Get history of a specific metric.

#### `delete_snapshot(snapshot_id: str) -> bool`
Delete a snapshot.

#### `cleanup_old_snapshots(keep_count: int = 100) -> int`
Clean up old snapshots.

### Convenience Functions

#### `save_status_snapshot(status: Dict[str, Any], project_path: Optional[Path] = None, snapshot_id: Optional[str] = None) -> Dict[str, Any]`
Convenience function to save snapshot.

#### `load_status_snapshot(snapshot_id: str, project_path: Optional[Path] = None, verify_integrity: bool = True) -> Optional[Dict[str, Any]]`
Convenience function to load snapshot.

## Snapshot Format

```json
{
  "version": "1.0",
  "snapshot_id": "status_20260111_120000",
  "timestamp": "2026-01-11T12:00:00",
  "status": {
    "epistemic_state": {...},
    "gamification_state": {...},
    "project_health": {...},
    ...
  },
  "metadata": {
    "source": "waft-status",
    "project_path": "/path/to/project"
  },
  "checksum": "ae5c8c3dda2d8461..."
}
```

## Best Practices

1. **Regular Snapshots**: Save snapshots regularly (e.g., daily, before major changes)
2. **Cleanup**: Use `cleanup_old_snapshots()` to prevent disk space issues
3. **Integrity Checks**: Always verify integrity when loading (default behavior)
4. **Meaningful IDs**: Use descriptive snapshot IDs for important snapshots
5. **History Tracking**: Use `get_status_history()` to track metrics over time

## Storage Location

**Directory**: `_pyrite/.waft/status_snapshots/`

**Files**: `{snapshot_id}.json`

**Permissions**: Standard file permissions (no special restrictions)

## Benefits

- ✅ **Data Integrity**: Checksum verification ensures data hasn't been corrupted
- ✅ **History Tracking**: Track status changes over time
- ✅ **Comparison**: Compare snapshots to see what changed
- ✅ **Debugging**: Historical snapshots help debug status issues
- ✅ **Audit Trail**: Complete record of system state over time

---

**This persistence system provides reliable status snapshot management with integrity verification - perfect for tracking system health over time.**
