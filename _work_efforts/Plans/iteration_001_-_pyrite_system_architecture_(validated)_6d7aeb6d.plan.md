---
name: Iteration 001 - Pyrite System Architecture (Validated)
overview: "Rigorous architecture design with validated assumptions: Custom API program (Node.js/Python), 5,000+ items scale (index required), mixed human/AI concurrency (queue required). Focused design for write queue, sidecar index, and git integration."
todos:
  - id: workeffort_interface
    content: Define WorkEffortInterface TypeScript type enforcing YAML frontmatter schema (id, title, status, created, branch, repository)
    status: pending
  - id: path_generator
    content: "Design PathGenerator utility function that generates canonical file paths from WorkEffort entities: _work_efforts/WE-YYMMDD-xxxx_{slug}/WE-YYMMDD-xxxx_index.md"
    status: pending
    dependencies:
      - workeffort_interface
  - id: write_queue_structure
    content: Design FIFO write queue data structure (in-memory + optional persistence) with single worker processor - REQUIRED for concurrency safety
    status: pending
  - id: sidecar_index_schema
    content: "Design Sidecar Index SQLite schema: work_efforts_index(id TEXT PRIMARY KEY, file_path TEXT, etag TEXT, last_modified INTEGER) - REQUIRED for 5,000+ item performance"
    status: pending
  - id: queue_processor_algorithm
    content: Design Write Queue Processor algorithm coordinating File I/O → Index Update → Git Operations → Events within transaction boundary
    status: pending
    dependencies:
      - write_queue_structure
      - sidecar_index_schema
---

# ITERATION REPORT 0

01

## 1. Executive Summary

- **Current Focus:** Defining the physical "WorkEffort" storage layout and the atomic data schema to ensure file system performance, Git compatibility, and support for 5,000+ items with programmatic API access.
- **The Roadmap:**

    - *Immediate:* Establish the directory structure, strict YAML Frontmatter template, and FIFO write queue design to prevent Git lock contention during concurrent operations (human + AI agents).

    - *Medium:* Build the "Sidecar Index" (SQLite) to map WorkEffort IDs to file paths for O(1) lookups, eliminating O(n) directory scans that become prohibitively slow at scale (5,000+ items).

    - *Long:* Enable automated Git operations (branch/commit/merge) integrated with work effort lifecycle, with full transaction support and API layer for programmatic access.

**Validated Assumptions:**

- ✅ **Custom Program**: Building Node.js/Python API to manage work efforts programmatically

- ✅ **Large Scale**: 5,000+ items expected - sidecar index is **essential** (not optional)

- ✅ **Mixed Concurrency**: Both human and AI agents will write simultaneously - FIFO queue is **critical** (not optional)

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

We use a **Flat Directory Structure** with ID-based folder names. At 5,000+ items, we need the sidecar index for performance.

```text
_work_efforts/
  /.git/                              # Version Control Root (if repo-level)
  /_system/                           # System Configs
     pyrite_index.db                  # Sidecar Index (SQLite) - CRITICAL for scale
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



**Why Flat (Not Time-Partitioned):**

- Simpler path generation

- Git-friendly (fewer directory changes)

- Index handles performance (O(1) lookup regardless of directory structure)

- Easier to move/rename work efforts

### Algorithm Logic (IPO)

**Operation:** `Create Work Effort` (via API)

- **Input:** JSON Payload `{ title, objective, tickets: string[] }`.
- **Process:**

1. **Generate Work Effort ID**: `WE-YYMMDD-xxxx` (date + random 4-char suffix)

2. **Check Collision**: Query sidecar index `SELECT id FROM work_efforts_index WHERE id = ?` (O(1))

3. **If Collision**: Retry with new random suffix

4. **Generate Timestamp**: ISO 8601 (now)

5. **Sanitize Title**: Create `slug` (e.g., "Dashboard Data Flow" -> `dashboard_data_flow`)

6. **Construct Path**: `_work_efforts/WE-YYMMDD-xxxx_{slug}/`

7. **Push to Write Queue** (CRITICAL - prevents git lock contention):

- Enqueue operation: `{ type: 'create', we_id, path, files: [...] }`

- Queue processor (single worker, sequential):

a. Acquire git lock (file-based: `.git/index.lock`)

b. `WRITE` directory structure (create folder, tickets/ subfolder)

c. `WRITE` index.md file (atomic: temp + rename)

d. `WRITE` ticket files (if provided)

e. `UPDATE` Sidecar Index (SQLite: `INSERT INTO work_efforts_index ...`)

f. `GIT CHECKOUT` develop (if git enabled)

g. `GIT CHECKOUT -b` feature/WE-XXXX-xxxx-slug

h. `GIT ADD` _work_efforts/WE-XXXX-xxxx_slug/

i. `GIT COMMIT` -m "WE-XXXX-xxxx: {title}"

j. Release git lock

k. Emit event: `workeffort:created` via EventBus

8. **Return Promise**: Resolves when queue processor completes

- **Output:** JSON `{ id: "WE-260103-abc1", path: "...", branch: "feature/WE-260103-abc1-slug", commit_hash: "a1b2c3d" }`.

**Operation:** `Read Work Effort by ID` (via API)

- **Input:** Work Effort ID `"WE-260102-t2z2"`.

- **Process:**

1. **Query Sidecar Index** (O(1) - CRITICAL for 5,000+ items):
   ```sql
      SELECT file_path, etag, last_modified 
      FROM work_efforts_index 
      WHERE id = 'WE-260102-t2z2'
   ```


2. **If Found**:

- Read file at `file_path`

- Calculate current file hash (etag)

- If hash matches index → return parsed entity

- If hash mismatch → file modified externally, update index, return entity

3. **If Not Found**:

- Fallback: Scan `_work_efforts/` directory (O(n) - slow but works)

- Rebuild index entry for this work effort

- Return entity

4. **Parse**: gray-matter.parse(content) → WorkEffort entity

5. **Parse Tickets**: Scan tickets/ subdirectory, parse each ticket file

- **Output:** WorkEffort entity with tickets array.

**Performance Comparison (5,000 work efforts):**

- **Without Index**: Scan 5,000 directories, read 5,000 files = ~2-5 seconds

- **With Index**: Single SQL query = ~0.005 seconds (400-1000x faster)

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

- `POST /api/v1/work-efforts` - Creates work effort (queued)

- `GET /api/v1/work-efforts/:id` - Reads work effort (uses index for O(1) lookup)

- `PATCH /api/v1/work-efforts/:id` - Updates work effort (queued)

- `DELETE /api/v1/work-efforts/:id` - Deletes work effort (queued, removes branch)

## 3. Scope & Risk Audit

- **Hard Scope:**

- **IN:** YAML Frontmatter definition, Directory structure logic, Filename convention (WE-YYMMDD-xxxx_slug), **FIFO Write Queue design (REQUIRED for concurrency)**, **Sidecar Index SQLite schema (REQUIRED for scale)**, Git workflow patterns, API endpoint specifications.

- **OUT:** The actual implementation code for the Queue, Binary asset storage, Search/filtering logic, Authentication/authorization, Multi-repository coordination, Performance benchmarking.

- **The "Break" Test:**

1. **Git Lock Contention (CRITICAL - VALIDATED):** Two operations (human + AI) try to create work efforts simultaneously → both try `git commit` → second fails with "index.lock" error. **Mitigation: FIFO Write Queue (REQUIRED, not optional).**

2. **Index Desync:** File write succeeds, index update fails (process crash) → system cannot find work effort by ID on next boot. **Mitigation: Queue as transaction boundary, index rebuild on startup if corruption detected.**

3. **ID Collision:** Two work efforts generated with same ID (same day, random suffix collision) → second overwrites first. **Mitigation: Check index before create, retry with new suffix if collision.**

4. **Partial Write Failure:** Directory created, index.md written, but git commit fails → file system and git state diverge. **Mitigation: Queue processor rolls back file changes if git fails.**

5. **Index Staleness:** File modified externally (human editor) → index points to old file, returns stale data. **Mitigation: Index stores etag (file hash), validate on read, update index if mismatch.**

6. **Performance at Scale (CRITICAL - VALIDATED):** 5,000 work efforts, query "all active" → without index: 2-5 seconds (unacceptable), with index: <0.01 seconds. **Mitigation: Sidecar Index (REQUIRED, not optional).**

7. **Queue Overflow:** 1,000 write operations queued rapidly → memory exhaustion. **Mitigation: Bounded queue (max 1000 items), backpressure (reject when full).**

- **Mitigation Strategy:**

1. **FIFO Write Queue (REQUIRED):** All write operations (file + git + index) pass through single queue, processed sequentially by single worker. Prevents git lock contention. **Validated: Mixed human/AI concurrency makes this essential.**

2. **Queue as Transaction Boundary:** Write queue ensures atomicity - if git commit fails, rollback file changes. All-or-nothing guarantee.

3. **Sidecar Index (REQUIRED):** SQLite database with `work_efforts_index(id, file_path, etag, last_modified)`. Enables O(1) lookups. **Validated: 5,000+ items makes this essential.**

4. **Index Validation:** Index stores file_path + etag (file hash). On read, validate etag matches file. If mismatch, rebuild index entry.

5. **ID Collision Detection:** Before creating work effort, check sidecar index for existing ID. If collision, retry with new random suffix.

6. **Atomic File Writes:** Use temp file + rename pattern (already implemented). Readers see old OR new content, never partial.

7. **Index Invalidation on Write:** When write queue completes, invalidate index entry (mark for refresh) before next read.

8. **Queue Bounds:** Maximum 1000 items in queue, reject new operations when full (backpressure).

## 4. Final Plan of Action

- **Step 1:** Define the `WorkEffortInterface` TypeScript/JavaScript type that enforces the YAML frontmatter schema (id, title, status, created, branch, repository).

- **Step 2:** Design the `PathGenerator` utility that accepts a WorkEffort and returns its canonical file path: `_work_efforts/WE-YYMMDD-xxxx_{slug}/WE-YYMMDD-xxxx_index.md`.

- **Step 3:** Design the FIFO Write Queue data structure (in-memory queue + optional persistence) with single worker processor. **REQUIRED for concurrency safety.**

- **Step 4:** Design the Sidecar Index SQLite schema: `work_efforts_index(id TEXT PRIMARY KEY, file_path TEXT, etag TEXT, last_modified INTEGER)`. **REQUIRED for 5,000+ item performance.**

- **Step 5:** Design the Write Queue Processor algorithm that coordinates: File I/O → Index Update → Git Operations → Event Emission (all within transaction boundary).

## 5. Verification

- **Logic Check:**

- **Git-Queue:** We validated that mixed human/AI concurrency requires a FIFO write queue. All git operations (commit, branch, merge) must pass through the queue to prevent lock contention. The queue worker is the single point of git access. **CONFIRMED: Queue is required, not optional.**

- **Sidecar Index:** We validated that 5,000+ items requires a sidecar index. The Index is the Source of Truth for location (ID → file_path), while the File is the Source of Truth for content. Index must be kept in sync via write queue. **CONFIRMED: Index is required, not optional.**

- **Constraint Met:** "WorkEfforts" are strictly typed Markdown files with YAML frontmatter, stored in predictable directory structure, accessible via O(1) index lookup. **API layer enables programmatic access.**

- **Transaction Boundary:** Write queue ensures atomicity - file operations, index updates, and git operations succeed together or fail together (with rollback). **CONFIRMED: Required for reliability.**

**Architecture Validated:**

- ✅ Custom Program: Node.js/Python API confirmed

- ✅ Large Scale: 5,000+ items confirmed → Index required

- ✅ Mixed Concurrency: Human + AI confirmed → Queue required