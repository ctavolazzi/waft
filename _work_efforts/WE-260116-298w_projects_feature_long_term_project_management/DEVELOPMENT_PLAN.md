# Projects Feature - Development Plan

**Work Effort**: WE-260116-298w
**Status**: Planning
**Created**: 2026-01-16 11:28:41 PST

---

## Overview

Build a comprehensive Projects feature that enables long-term project management with incremental work support. This system will provide the foundation for managing complex, multi-session work like the campaign book generation system.

---

## Architecture

### Core Components

```
Projects System
├── ProjectManager (core/projects.py)
│   ├── Project (dataclass) - Project metadata and state
│   ├── Milestone (dataclass) - Project milestones
│   ├── ProgressEntry (dataclass) - Work session progress
│   └── ProjectManager (class) - CRUD and persistence
├── CLI Commands (cli/project_commands.py)
│   ├── project create
│   ├── project list
│   ├── project show
│   ├── project update
│   ├── project progress
│   └── project status
└── Storage (_pyrite/.waft/projects/)
    └── {project_id}.json - Project data files
```

### Data Model

```python
@dataclass
class Project:
    project_id: str  # Validated: safe filename characters only, no path traversal
    title: str  # Validated: max 200 chars, no control characters
    description: str  # Validated: max 10,000 chars, no control characters
    status: ProjectStatus  # planning, active, paused, completed, archived
    created_at: str  # ISO format timestamp
    updated_at: str  # ISO format timestamp
    progress_percent: float  # 0.0 to 100.0, validated
    tags: List[str]  # Max 20 tags, each max 50 chars
    milestones: List[Milestone]  # Max 100 milestones
    progress_entries: List[ProgressEntry]  # Max 1000 entries (keep last N)
    related_work_efforts: List[str]  # Work effort IDs, validated format
    notes: str  # Max 10,000 chars
    version: int = 1  # Schema version for migrations

@dataclass
class Milestone:
    milestone_id: str
    title: str
    description: str
    target_date: Optional[str]
    completed: bool
    completed_at: Optional[str]

@dataclass
class ProgressEntry:
    entry_id: str
    timestamp: str
    progress_delta: float  # Change in progress percentage
    notes: str
    work_effort_id: Optional[str]  # Link to work effort
    session_duration: Optional[float]  # Minutes spent
```

---

## Implementation Phases

### Phase 1: Foundation (Tickets 001-003)

**Goal**: Core data models and storage

**Tasks**:
1. Design project data structures with security considerations
2. Create Project, Milestone, ProgressEntry dataclasses with validation
3. Implement ProjectManager class with file-based persistence
4. **CRITICAL**: Add path validation using `_validate_path_in_project()` pattern
5. **CRITICAL**: Set file permissions (`chmod(0o600)` files, `chmod(0o700)` directories)
6. **CRITICAL**: Add input validation (project_id, title, description, progress_percent)
7. **CRITICAL**: Implement file locking and atomic writes for concurrent access
8. **HIGH**: Add comprehensive error handling (IOError, OSError, PermissionError, json.JSONDecodeError)
9. **HIGH**: Add JSON validation on load
10. **HIGH**: Add disk space checks before writes
11. **HIGH**: Add backup/rollback mechanism
12. **HIGH**: Add input size limits (description, tags, milestones, progress entries)
13. Create storage directory structure (`_pyrite/.waft/projects/`)
14. Implement CRUD operations (create, read, update, delete, list)
15. Add logging for operations and errors

**Deliverable**: Working ProjectManager with file-based storage

**Files**:
- `src/waft/core/projects.py` - Core project management with security measures

**Security Requirements**:
- Path validation using `_validate_path_in_project()` from `src/waft/utils.py`
- File permissions: `chmod(0o600)` on files, `chmod(0o700)` on directories
- Input validation: project_id (safe filename), title (max 200 chars), description (max 10,000 chars)
- Progress validation: 0.0 to 100.0, reject NaN/infinity
- File locking: Use `threading.Lock()` for concurrent access
- Atomic writes: Write to temp file, then rename (see `src/waft/utils.py:1622`)
- Error handling: Handle IOError, OSError, PermissionError, json.JSONDecodeError
- Disk space checks: Check before writes, warn if low
- Backup/rollback: Create backup before updates

---

### Phase 2: CLI Interface (Ticket 004)

**Goal**: Command-line interface for project management

**Tasks**:
1. Create `project_commands.py` CLI module
2. Implement `project create` command
3. Implement `project list` command
4. Implement `project show` command
5. Implement `project update` command
6. Integrate with main `waft` CLI

**Deliverable**: Full CLI interface for project management

**Files**:
- `src/waft/cli/project_commands.py` - CLI commands
- Update `src/waft/main.py` - Add project app to main CLI

---

### Phase 3: Progress Tracking (Ticket 005)

**Goal**: Progress tracking and milestones

**Tasks**:
1. Implement progress percentage calculation
2. Add milestone management (create, complete, list)
3. Implement progress entry logging
4. Add session duration tracking
5. Create progress summary views

**Deliverable**: Complete progress tracking system

---

### Phase 4: Integration (Tickets 006-007)

**Goal**: Integrate with existing systems

**Tasks**:
1. Link projects to work efforts
2. Add project status filtering
3. Create project search functionality
4. Add project tags and categorization
5. Integrate with campaign book generation system

**Deliverable**: Fully integrated project system

---

### Phase 5: Polish (Ticket 008)

**Goal**: Dashboard and summary views

**Tasks**:
1. Create project dashboard view
2. Add progress visualization
3. Implement project summary reports
4. Add export functionality
5. Create usage documentation

**Deliverable**: Complete, polished Projects feature

---

## File Structure

```
src/waft/
├── core/
│   └── projects.py              # ProjectManager and data models
├── cli/
│   └── project_commands.py     # CLI commands
└── main.py                      # Updated with project app

_pyrite/
└── .waft/
    └── projects/                # Project storage
        ├── {project_id}.json    # Project data files
        └── .gitkeep

examples/
└── test_projects.py             # Test suite

docs/
└── projects_feature.md          # User documentation
```

---

## Storage Format

Projects stored as JSON files in `_pyrite/.waft/projects/{project_id}.json`:

```json
{
  "project_id": "proj_20260116_112841",
  "title": "Campaign Book Generation System",
  "description": "Build comprehensive campaign book generation...",
  "status": "active",
  "created_at": "2026-01-16T19:28:41.000Z",
  "updated_at": "2026-01-16T19:28:41.000Z",
  "progress_percent": 15.5,
  "tags": ["campaign", "pdf", "dnd"],
  "milestones": [...],
  "progress_entries": [...],
  "related_work_efforts": ["WE-260116-298w"],
  "notes": "Starting implementation..."
}
```

---

## CLI Usage Examples

```bash
# Create a new project
waft project create "Campaign Book Generation" \
  --description "Build campaign book generation system" \
  --tags campaign,pdf,dnd

# List all projects
waft project list
waft project list --status active
waft project list --tag campaign

# Show project details
waft project show proj_20260116_112841

# Update project
waft project update proj_20260116_112841 --status active

# Update progress
waft project progress proj_20260116_112841 --percent 25.0 --notes "Phase 1 complete"

# Quick status check
waft project status proj_20260116_112841
```

---

## Integration Points

### With Work Efforts
- Projects can link to work efforts via `related_work_efforts` field
- Progress entries can reference work effort IDs
- Projects can track completion of related work efforts

### With Campaign Book Generation
- Campaign book generation will be created as a project
- Progress tracked as implementation phases complete
- Milestones align with campaign book generation phases

### With CLI
- Projects accessible via `waft project` commands
- Integrated into main CLI help system
- Follows existing WAFT CLI patterns

---

## Testing Strategy

1. **Unit Tests**: Test ProjectManager CRUD operations
2. **Integration Tests**: Test CLI commands end-to-end
3. **Data Tests**: Verify JSON serialization/deserialization
4. **Storage Tests**: Verify file-based persistence

---

## Success Criteria

- ✅ Create, read, update, delete projects via CLI
- ✅ Track progress percentage and milestones
- ✅ Log progress entries with timestamps
- ✅ Link projects to work efforts
- ✅ Filter and search projects
- ✅ File-based storage in `_pyrite/.waft/projects/`
- ✅ CLI commands integrated into main `waft` CLI
- ✅ Foundation ready for campaign book generation system

---

## Timeline

- **Phase 1**: 1-2 days (Foundation)
- **Phase 2**: 1 day (CLI Interface)
- **Phase 3**: 1 day (Progress Tracking)
- **Phase 4**: 1 day (Integration)
- **Phase 5**: 1 day (Polish)

**Total**: ~5-7 days for complete implementation

---

## Next Steps

1. ✅ Create work effort (Done)
2. ⏳ Start Phase 1: Design and implement core data models
3. ⏳ Implement ProjectManager class
4. ⏳ Create CLI commands
5. ⏳ Add progress tracking
6. ⏳ Integrate with existing systems
