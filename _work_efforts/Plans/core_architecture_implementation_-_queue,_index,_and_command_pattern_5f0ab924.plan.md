---
name: Core Architecture Implementation - Queue, Index, and Command Pattern
overview: "Implement the foundational architecture for Pyrite's work effort system: FIFO write queue for concurrency safety, sidecar SQLite index for O(1) lookups at scale, and Command Pattern job system for testable, sequential processing."
todos: []
---

# Core Architecture Implementation Plan

## Context

Building on the core data structure analysis, this plan implements three critical architectural components:

1. **FIFO Write Queue** - Required for mixed human/AI concurrency (prevents git lock contention)
2. **Sidecar SQLite Index** - Required for 5,000+ item performance (O(1) lookups vs O(n) scans)
3. **Command Pattern Job System** - Testable, sequential processing architecture

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer (Future)                     │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              FIFO Write Queue (JobQueue)                 │
│  - Sequential processing (single worker)                  │
│  - Transaction boundary (all-or-nothing)                 │
│  - Error isolation (failed jobs don't crash queue)        │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Job Execution (Command Pattern)              │
│  - File I/O operations                                  │
│  - Sidecar Index updates                                 │
│  - Git operations (branch/commit/merge)                  │
│  - Event emission                                        │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Sidecar Index (SQLite)                      │
│  - O(1) ID → file_path lookups                           │
│  - ETag validation (detect external changes)             │
│  - Performance: 400-1000x faster at scale                │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              File System (_work_efforts/)                │
│  - Markdown files with YAML frontmatter                 │
│  - Flat directory structure                              │
│  - Atomic writes (temp + rename)                         │
└─────────────────────────────────────────────────────────┘
```

## Implementation Phases

### Phase 1: Command Pattern Foundation (Job & JobQueue)

**Files to Create:**
- `core/QueueSystem.js` - Job and JobQueue classes
- `test-queue.js` - Validation script

**Job Class:**
- Properties: `id`, `type`, `payload`, `status`, `logs`, `createdAt`
- Method: `log(message)` for audit trail
- Status transitions: `pending` → `processing` → `completed`/`failed`

**JobQueue Class:**
- Properties: `queue[]`, `isProcessing` flag
- Methods:
  - `add(type, payload)` - Enqueue job, trigger processing
  - `processNext()` - Sequential processing loop (with lock)
  - `executeJob(job)` - Mock worker (500-1500ms simulation)
  - `getPending()` - Helper to inspect queue

**Key Features:**
- Sequential processing (only one job at a time)
- Error isolation (try/catch/finally)
- Auto-continuation (recursive `processNext()`)
- Mock implementation (setTimeout simulation)

**Validation:**
- Test script creates 3 jobs (normal, failing, normal)
- Verify sequential processing
- Verify error recovery
- Verify queue doesn't crash on failure

### Phase 2: Sidecar Index Schema & Operations

**Files to Create:**
- `core/SidecarIndex.js` - SQLite index operations
- `core/index-schema.sql` - Database schema

**SQLite Schema:**
```sql
CREATE TABLE work_efforts_index (
  id TEXT PRIMARY KEY,              -- WE-YYMMDD-xxxx
  file_path TEXT NOT NULL,           -- Absolute path to index.md
  etag TEXT NOT NULL,                -- File hash for validation
  last_modified INTEGER NOT NULL,    -- Unix timestamp
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);

CREATE INDEX idx_work_efforts_updated ON work_efforts_index(updated_at DESC);
```

**Operations:**
- `initialize()` - Create database, run migrations
- `get(id)` - O(1) lookup by ID → returns file_path, etag
- `set(id, file_path, etag)` - Insert/update index entry
- `delete(id)` - Remove index entry
- `validate(id, file_path)` - Check etag matches file hash
- `rebuild()` - Scan file system, rebuild entire index

**Integration Points:**
- Write queue updates index after successful file write
- Read operations query index first (O(1)), fallback to scan if not found
- Index validation on read (etag check)

### Phase 3: Write Queue Processor (Real Operations)

**Files to Modify:**
- `core/QueueSystem.js` - Replace mock `executeJob` with real operations

**Job Types:**
- `CREATE_WORK_EFFORT` - Create directory, files, git branch, index entry
- `UPDATE_WORK_EFFORT` - Update file, git commit, index entry
- `DELETE_WORK_EFFORT` - Delete directory, git branch, index entry
- `CREATE_TICKET` - Create ticket file, git commit, index entry
- `UPDATE_TICKET` - Update ticket file, git commit, index entry

**Transaction Flow:**
1. Acquire git lock (`.git/index.lock`)
2. Execute file operations (atomic writes)
3. Update sidecar index
4. Execute git operations (checkout, commit, merge)
5. Release git lock
6. Emit EventBus event
7. Return result

**Error Handling:**
- If any step fails, rollback previous steps
- Mark job as `failed` with error message
- Queue continues processing next job

### Phase 4: Path Generator & ID Collision Detection

**Files to Create:**
- `core/PathGenerator.js` - Generate canonical paths
- `core/IDGenerator.js` - Generate IDs with collision detection

**PathGenerator:**
- `getWorkEffortPath(we_id, title)` → `_work_efforts/WE-YYMMDD-xxxx_{slug}/`
- `getIndexFilePath(we_path)` → `WE-YYMMDD-xxxx_index.md`
- `getTicketsDir(we_path)` → `tickets/`
- `getTicketPath(we_path, ticket_id, title)` → `tickets/TKT-xxxx-NNN_{slug}.md`

**IDGenerator:**
- `generateWorkEffortId()` - Date + random suffix
- `checkCollision(id)` - Query sidecar index
- `generateUniqueId()` - Generate with collision retry (max 10 attempts)

### Phase 5: Integration & Testing

**Files to Create:**
- `tests/queue-system.test.js` - Unit tests for Job/JobQueue
- `tests/sidecar-index.test.js` - Unit tests for index operations
- `tests/integration.test.js` - End-to-end tests

**Test Coverage:**
- Queue sequential processing
- Queue error recovery
- Index O(1) lookups
- Index etag validation
- ID collision detection
- Path generation
- Transaction rollback
- Git lock contention prevention

## File Structure

```
_pyrite/
├── core/
│   ├── QueueSystem.js          # Job & JobQueue classes
│   ├── SidecarIndex.js         # SQLite index operations
│   ├── PathGenerator.js        # Path generation utilities
│   ├── IDGenerator.js          # ID generation with collision detection
│   └── index-schema.sql        # SQLite schema
├── tests/
│   ├── queue-system.test.js
│   ├── sidecar-index.test.js
│   └── integration.test.js
└── test-queue.js               # Validation script (Phase 1)
```

## Success Criteria

**Phase 1 Complete:**
- ✅ Job and JobQueue classes implemented
- ✅ Test script validates sequential processing
- ✅ Test script validates error recovery
- ✅ No external dependencies (pure Node.js)

**Phase 2 Complete:**
- ✅ SQLite index created and initialized
- ✅ O(1) lookup operations working
- ✅ ETag validation working
- ✅ Index rebuild functionality

**Phase 3 Complete:**
- ✅ Real file operations integrated
- ✅ Git operations integrated
- ✅ Transaction rollback working
- ✅ EventBus integration

**Phase 4 Complete:**
- ✅ Path generation working
- ✅ ID collision detection working
- ✅ All utilities tested

**Phase 5 Complete:**
- ✅ Unit tests passing
- ✅ Integration tests passing
- ✅ Performance validated (O(1) lookups)

## Risk Mitigation

**Git Lock Contention:**
- ✅ FIFO queue ensures sequential git operations
- ✅ Single worker pattern prevents concurrent commits

**Index Desync:**
- ✅ Queue as transaction boundary
- ✅ Index rebuild on startup if corruption detected
- ✅ ETag validation on read

**ID Collision:**
- ✅ Check index before create
- ✅ Retry with new suffix (max 10 attempts)

**Performance at Scale:**
- ✅ Sidecar index enables O(1) lookups
- ✅ Index required for 5,000+ items

**Queue Overflow:**
- ✅ Bounded queue (max 1000 items)
- ✅ Backpressure (reject when full)

## Dependencies

- `better-sqlite3` or `sqlite3` - SQLite database
- `gray-matter` - YAML frontmatter parsing (already in use)
- `fs/promises` - File system operations
- `child_process` - Git command execution

## Out of Scope (Future Phases)

- API layer implementation
- Authentication/authorization
- Multi-repository coordination
- Performance benchmarking
- Search/filtering logic
- Binary asset storage