---
name: Iteration 001 - Pyrite Complete System Architecture
overview: Rigorous Predict-Break-Fix analysis following NovaSystem methodology, defining WorkEffort storage layout, atomic data schema, write queue, and sidecar index for Pyrite system.
todos:
  - id: workeffort_interface
    content: Define WorkEffortInterface TypeScript type enforcing YAML frontmatter schema
    status: pending
  - id: path_generator
    content: Design PathGenerator utility function that generates canonical file paths from WorkEffort entities
    status: pending
    dependencies:
      - workeffort_interface
  - id: write_queue_structure
    content: Design FIFO write queue data structure (in-memory + optional persistence) with queue interface
    status: pending
  - id: sidecar_index_schema
    content: Design Sidecar Index SQLite schema with work_efforts_index table (id, file_path, etag, last_modified)
    status: pending
  - id: queue_processor_algorithm
    content: Design Write Queue Processor algorithm coordinating File I/O → Index Update → Git Operations → Events
    status: pending
    dependencies:
      - write_queue_structure
      - sidecar_index_schema

category: dreams
confidence: 0.85
constellation_date: 2026-01-14
---

# ITERATION REPO

RT 001

## 1. Executive Summary

- **Current Focus:** Defining the physical "WorkEffort" storage layout and the atomic data schema to ensure file system performance, Git compatibility, and eliminate O(n) file scans through sidecar indexing.

- **The Roadmap:**

    - *Immediate:* Establish the directory structure, strict YAML Frontmatter template, and FIFO write queue design to prevent Git lock contention.

    - *Medium:* Build the "Sidecar Index" (SQLite) to map WorkEffort IDs to file paths for O(1) lookups, eliminating directory scans.

    - *Long:* Enable automated Git operations (branch/commit/merge) integrated with work effort lifecycle, with full transaction support.

## 2. Technical Specs (The Engine)

### Data Structure Definition

- **Schema (The Atomic Unit):**

The `.md` file serves as both the database row and the user interface.

```yaml
---
# IDENTITY
id: "WE-260102-t2z2"                    # WE-YYMMDD-xxxx (Date-based, Immutable)
title: "Dashboard Data Flow Testing"    # Human-readable title
status: "completed"                     # active | paused | completed

# TEMPORAL
created: "2026-01-02T13:53:07.573Z"     # ISO 8601
last_updated: "2026-01-03T04:35:47.198Z"
created_by: "ctavolazzi"

# GIT INTEGRATION
branch: "feature/WE-260102-t2z2-dashboard_data_flow_testing_analysis"
repository: "_pyrite"

# RELATIONSHIPS (Implicit via directory structure)
# Child tickets stored in tickets/ subdirectory
---

# CONTENT
## Objective
Build comprehensive data flow tests...

## Tickets
| ID | Title | Status |
|----|-------|--------|
| TKT-t2z2-001 | Map data flow paths | completed |
```



- **Storage (The Physical Layout):**

We use a **Flat Directory Structure** with ID-based folder names to keep paths predictable and Git-friendly.

```text
_work_efforts/
  /.git/                              # Version Control Root (if repo-level)
  /WE-260102-t2z2_dashboard_data_flow_testing_analysis/
     WE-260102-t2z2_index.md          # Primary entity file
     tickets/
        TKT-t2z2-001_map_data_flow_paths.md
        TKT-t2z2-002_create_parser_tests.md
  /WE-260103-abc1_another_work_effort/
     WE-260103-abc1_index.md
     tickets/
        TKT-abc1-001_task.md
```



**Key Differences from NovaSystem:**

- **ID Format**: WE-YYMMDD-xxxx (date-based, 4-char suffix) vs UUID

- **Type System**: Implicit (all work efforts) vs explicit type field

- **Partitioning**: Flat structure (all in `_work_efforts/`) vs time-partitioned by type

- **Relationships**: Hierarchical (WE → TKT) vs graph-based adjacency list

### Algorithm Logic (IPO)

**Operation:** `Create Work Effort`

- **Input:** JSON Payload `{ title, objective, tickets: string[] }`.

- **Process:**

1. **Generate Work Effort ID**: `WE-YYMMDD-xxxx` (date + random 4-char suffix)

2. **Check Collision**: Query sidecar index for existing ID

3. **Generate Timestamp**: ISO 8601 (now)

4. **Sanitize Title**: Create `slug` (e.g., "Dashboard Data Flow" -> `dashboard_data_flow`)

5. **Construct Path**: `_work_efforts/WE-YYMMDD-xxxx_{slug}/`

6. **Push to Write Queue:**

- `WRITE` directory structure (create folder, tickets/ subfolder)

- `WRITE` index.md file (with frontmatter + markdown body)

- `WRITE` ticket files (if provided)

- `UPDATE` Sidecar Index (SQLite: insert work_efforts_index row)

- `GIT CHECKOUT` develop (if git enabled)

- `GIT CHECKOUT -b` feature/WE-XXXX-xxxx-slug

- `GIT ADD` _work_efforts/WE-XXXX-xxxx_slug/

- `GIT COMMIT` -m "WE-XXXX-xxxx: {title}"

7. **Emit Event**: `workeffort:created` via EventBus

- **Output:** JSON `{ id: "WE-260103-abc1", path: "...", branch: "feature/WE-260103-abc1-slug", commit_hash: "a1b2c3d" }`.

**Operation:** `Read Work Effort by ID`

- **Input:** Work Effort ID `"WE-260102-t2z2"`.

- **Process:**

1. **Query Sidecar Index**: `SELECT file_path, etag FROM work_efforts_index WHERE id = ?` (O(1))

2. **If Found**: Read file at `file_path`, validate etag matches

3. **If Not Found**: Fallback to directory scan (rebuild index)

4. **Parse**: gray-matter.parse(content) → WorkEffort entity

5. **Parse Tickets**: Scan tickets/ subdirectory, parse each ticket file

- **Output:** WorkEffort entity with tickets array.

### Workflow Simulation

- **Git-State:**

- The `develop` branch is the integration branch.

- Creating a work effort:

- Creates new branch: `feature/WE-XXXX-xxxx-slug`

- Commits initial files to that branch

- Branch remains active until work effort completed

- Completing a work effort:

- Final commit on feature branch

- Merge `feature/WE-XXXX-xxxx-slug` → `develop`

- Delete feature branch

- Commit Message Format: `WE-XXXX-xxxx/TKT-xxxx-NNN: Description`

- **API Endpoint:**

- `POST /api/v1/work-efforts`

- `GET /api/v1/work-efforts/:id` (uses sidecar index for O(1) lookup)

- `PATCH /api/v1/work-efforts/:id` (updates file, commits, updates index)

- `DELETE /api/v1/work-efforts/:id` (deletes files, deletes branch, updates index)

## 3. Scope & Risk Audit

- **Hard Scope:**

- **IN:** YAML Frontmatter definition, Directory structure logic, Filename convention (WE-YYMMDD-xxxx_slug), Write queue design, Sidecar index schema (SQLite), Git workflow patterns.

- **OUT:** The actual implementation code for the Queue, Binary asset storage, Search/filtering logic, Authentication/authorization, Multi-repository coordination.

- **The "Break" Test:**

1. **Git Lock Contention:** Two API requests create work efforts simultaneously → both try `git commit` → second fails with "index.lock" error.

2. **Index Desync:** File write succeeds, index update fails (process crash) → system cannot find work effort by ID on next boot.

3. **ID Collision:** Two work efforts generated with same ID (same day, random suffix collision) → second overwrites first.

4. **Partial Write Failure:** Directory created, index.md written, but git commit fails → file system and git state diverge.

5. **Index Staleness:** File modified externally (editor) → index points to old file, returns stale data.

6. **Concurrent Read During Write:** API reads work effort while write queue is updating it → reader sees partial/inconsistent data.

7. **Git Repository Not Initialized:** Work effort created in repo without `.git` directory → git operations fail, but file operations succeed.

- **Mitigation Strategy:**

1. **FIFO Write Queue:** All write operations (file + git + index) pass through single queue, processed sequentially by single worker. Prevents git lock contention.

2. **Queue as Transaction Boundary:** Write queue ensures atomicity - if git commit fails, rollback file changes. All-or-nothing guarantee.

3. **Sidecar Index with Validation:** Index stores file_path + etag (file hash). On read, validate etag matches file. If mismatch, rebuild index entry.

4. **ID Collision Detection:** Before creating work effort, check sidecar index for existing ID. If collision, retry with new random suffix.

5. **Atomic File Writes:** Use temp file + rename pattern (already implemented). Readers see old OR new content, never partial.

6. **Index Invalidation on Write:** When write queue completes, invalidate index entry (mark for refresh) before next read.

7. **Git Pre-flight Check:** Before git operations, check if `.git` directory exists. If not, skip git operations, log warning, continue with file operations only.

## 4. Final Plan of Action

- **Step 1:** Define the `WorkEffortInterface` TypeScript/JavaScript type that enforces the YAML frontmatter schema (id, title, status, created, branch, repository).

- **Step 2:** Design the `PathGenerator` utility that accepts a WorkEffort and returns its canonical file path: `_work_efforts/WE-YYMMDD-xxxx_{slug}/WE-YYMMDD-xxxx_index.md`.

- **Step 3:** Design the FIFO Write Queue data structure (in-memory queue + optional persistence) with single worker processor.

- **Step 4:** Design the Sidecar Index SQLite schema: `work_efforts_index(id TEXT PRIMARY KEY, file_path TEXT, etag TEXT, last_modified INTEGER)`.

- **Step 5:** Design the Write Queue Processor algorithm that coordinates: File I/O → Index Update → Git Operations → Event Emission (all within transaction boundary).

## 5. Verification

- **Logic Check:**

- **Git-Queue:** We acknowledged that all git operations (commit, branch, merge) must pass through the FIFO queue to prevent lock contention. The queue worker is the single point of git access.

- **Sidecar Index:** We established that the Index is the Source of Truth for location (ID → file_path), while the File is the Source of Truth for content. Index must be kept in sync via write queue.

- **Constraint Met:** "WorkEfforts" are strictly typed Markdown files with YAML frontmatter, stored in predictable directory structure, accessible via O(1) index lookup.

- **Transaction Boundary:** Write queue ensures atomicity - file operations, index updates, and git operations succeed together or fail together (with rollback).