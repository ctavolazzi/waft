---
name: Adaptive Core Architecture - Simple to Complex Scaling
overview: Implement an adaptive architecture that starts simple (file-based only) and automatically scales to complex mode (queue + sidecar index) when needed. Threshold-based switching ensures we only add complexity when performance requires it.
todos: []

category: dreams
confidence: 0.65
constellation_date: 2026-01-14
---

# Adapti

ve Core Architecture Implementation Plan

## Context

Building on the core data structure analysis, this plan implements an **adaptive architecture** that:

- Starts **simple** (file-based only) for small scale (< 100 work efforts)
- Automatically switches to **complex** (queue + sidecar index) when scale requires it (>= 100 work efforts)
- Provides seamless transition between modes

## Architecture Modes

### Tiny Mode (< 10 work efforts, no concurrency)

- **Storage**: File system only
- **Lookups**: O(n) directory scan (~0.01-0.05s)
- **Writes**: Direct file I/O
- **Git**: Direct git commands
- **Use Case**: Initial setup, tiny personal projects

### Simple Mode (10-20 work efforts, no concurrency)

- **Storage**: File system only
- **Lookups**: O(n) directory scan (~0.05-0.1s)
- **Writes**: Direct file I/O (no queue)
- **Git**: Direct git commands (no queue)
- **Use Case**: Small projects, sequential access only

### Standard Mode (>= 20 work efforts OR concurrency detected)

- **Storage**: File system + Sidecar SQLite index (if >= 20 items)
- **Lookups**: O(1) index queries (~0.005s) OR O(n) scan if index disabled
- **Writes**: FIFO queue (always enabled if concurrency)
- **Git**: Queued git operations (sequential processing)
- **Use Case**: Most real-world usage (your case: medium scale + always concurrent)

### Performance Mode (>= 50 work efforts)

- **Storage**: File system + Sidecar SQLite index (required)
- **Lookups**: O(1) index queries only (~0.005s)
- **Writes**: FIFO queue (required)
- **Git**: Queued git operations (required)
- **Use Case**: Medium to large scale, performance critical

## Threshold Configuration

```javascript
const SCALE_THRESHOLDS = {
  // Queue: Enabled based on concurrency, not scale
  QUEUE_ENABLED_ALWAYS: true,   // Always enabled (concurrent writes expected)

  // Index: Enabled based on performance requirements
  INDEX_ENABLED_MIN: 20,        // Enable index at 20 items for instant lookups
  INDEX_REQUIRED_MIN: 50,       // Index required at 50 items (performance critical)

  // Simple Mode: Only for tiny scale with no concurrency
  SIMPLE_MODE_MAX: 20,          // Simple mode only < 20 items (rare case)
  TINY_MODE_MAX: 10             // No queue/index needed < 10 items
};
```



### Rationale

**Queue (Concurrency Safety):**

- **Why always enabled**: You have "always concurrent" writes (human + AI)
- **Not scale-based**: Queue prevents git lock contention, which happens at any scale with concurrency
- **Decision**: Enable queue from day 1 if concurrent writes detected, or always if configured

**Index (Performance):**

- **Why 20 items**: For "instant" performance (< 0.01s), directory scans become too slow
- 20 items: ~0.05-0.1s scan (not instant)
- 50 items: ~0.1-0.2s scan (not instant)
- Index lookup: ~0.005s (instant)
- **Why 50 required**: At 50+ items, scans are consistently > 0.1s, index becomes essential
- **Decision**: Enable index at 20 items, require at 50 items

**Simple Mode:**

- **Why < 20 items**: Only makes sense if:
- No concurrency (but you have "always concurrent")
- Small scale (< 20 items)
- Performance tolerance is higher (but you want "instant")
- **Decision**: Simple mode is rare, mostly for initial setup or tiny projects

## Adaptive Detection

**On System Startup:**

1. Count work efforts in `_work_efforts/` directory
2. Detect concurrency pattern (check config or detect concurrent writes)
3. Determine mode:

- **Tiny Mode**: count < 10 AND no concurrency
- **Simple Mode**: count < 20 AND no concurrency
- **Standard Mode**: count >= 20 OR concurrency detected
- **Performance Mode**: count >= 50 (index required)

4. Enable features:

- **Queue**: Always if concurrency detected, or if count >= 20
- **Index**: If count >= 20 (enabled), required if count >= 50

5. Store mode in config file (`.pyrite/config.json`)

**On Work Effort Creation:**

1. Check current count and concurrency status
2. If transitioning to new mode:

- **10 → 20 items**: Enable index (if not already)
- **20 → 50 items**: Index becomes required
- **Any count + concurrency detected**: Enable queue immediately

3. Migrate if needed:

- Initialize sidecar index (if count >= 20)
- Enable write queue (if concurrency or count >= 20)
- Populate index from existing work efforts

## Implementation Phases

### Phase 1: Simple Mode Foundation

**Files to Create:**

- `core/SimpleMode.js` - Simple file-based operations
- `core/ModeDetector.js` - Detect and switch modes

**SimpleMode Class:**

- `countWorkEfforts()` - Scan directory, return count
- `getWorkEffort(id)` - O(n) scan to find by ID
- `createWorkEffort(data)` - Direct file write
- `updateWorkEffort(id, data)` - Direct file write
- `deleteWorkEffort(id)` - Direct file deletion

**ModeDetector:**

- `detectMode()` - Count work efforts, return 'simple' or 'complex'
- `shouldMigrate()` - Check if migration needed
- `migrateToComplex()` - Initialize index, enable queue

**Key Features:**

- No dependencies (pure file system)
- Fast for small scale
- Easy to test
- No database required

### Phase 2: Command Pattern Foundation (Job & JobQueue)

**Files to Create:**

- `core/QueueSystem.js` - Job and JobQueue classes
- `test-queue.js` - Validation script

**Job Class:**

- Properties: `id`, `type`, `payload`, `status`, `logs`, `createdAt`
- Method: `log(message)` for audit trail

**JobQueue Class:**

- Properties: `queue[]`, `isProcessing` flag, `enabled` flag
- Methods:
- `add(type, payload)` - Enqueue if enabled, else execute directly
- `processNext()` - Sequential processing (only if enabled)
- `enable()` - Switch queue on
- `disable()` - Switch queue off, process remaining jobs

**Adaptive Behavior:**

- If queue disabled: Execute operations directly (Simple Mode)
- If queue enabled: Enqueue and process sequentially (Complex Mode)

### Phase 3: Sidecar Index (Conditional)

**Files to Create:**

- `core/SidecarIndex.js` - SQLite index operations (conditional)
- `core/index-schema.sql` - Database schema

**SidecarIndex Class:**

- `isEnabled()` - Check if index should be used
- `initialize()` - Create database if needed
- `get(id)` - O(1) lookup (if enabled), fallback to scan
- `set(id, file_path, etag)` - Update index (if enabled)
- `rebuild()` - Rebuild from file system

**Adaptive Behavior:**

- If Simple Mode: Index methods return null/fallback to scan
- If Complex Mode: Index methods execute normally

### Phase 4: Adaptive Write Operations

**Files to Create:**

- `core/WorkEffortManager.js` - Unified interface for both modes

**WorkEffortManager Class:**

- `mode` - Current mode ('simple' or 'complex')
- `create(data)` - Adaptive: Simple = direct write, Complex = queue
- `get(id)` - Adaptive: Simple = scan, Complex = index lookup
- `update(id, data)` - Adaptive: Simple = direct write, Complex = queue
- `delete(id)` - Adaptive: Simple = direct delete, Complex = queue

**Mode Switching:**

```javascript
async create(data) {
  const count = await this.countWorkEfforts();
  const hasConcurrency = await this.detectConcurrency();

  // Check if we need to migrate
  if (hasConcurrency && !this.queue.isEnabled()) {
    await this.enableQueue();
  }

  if (count >= 20 && !this.index.isEnabled()) {
    await this.enableIndex();
  }

  if (count >= 50 && !this.index.isRequired()) {
    await this.requireIndex();
  }

  // Execute in current mode
  if (this.queue.isEnabled()) {
    return await this.queue.add('CREATE_WORK_EFFORT', data);
  } else {
    return await this.simpleMode.create(data);
  }
}
```



### Phase 5: Migration Logic

**Files to Create:**

- `core/Migration.js` - Handle mode transitions

**Migration Process:**

1. **Detect Need**: Count work efforts, check threshold
2. **Backup**: Create backup of current state
3. **Initialize Complex Mode**:

- Create sidecar index database
- Enable write queue
- Scan all work efforts
- Populate index

4. **Verify**: Validate index matches file system
5. **Switch Mode**: Update config, enable complex features

**Rollback:**

- If migration fails, restore from backup
- Continue in Simple Mode
- Log error for user review

## File Structure

```javascript
_pyrite/
├── core/
│   ├── SimpleMode.js           # Simple file-based operations
│   ├── QueueSystem.js          # Job & JobQueue (conditional)
│   ├── SidecarIndex.js         # SQLite index (conditional)
│   ├── WorkEffortManager.js    # Unified interface
│   ├── ModeDetector.js         # Mode detection & switching
│   ├── Migration.js            # Mode migration logic
│   ├── PathGenerator.js        # Path generation utilities
│   ├── IDGenerator.js          # ID generation
│   └── index-schema.sql        # SQLite schema
├── .pyrite/
│   └── config.json             # Mode configuration
└── test-queue.js               # Validation script
```



## Configuration File

`.pyrite/config.json`:

```json
{
  "mode": "standard",
  "workEffortCount": 45,
  "concurrencyDetected": true,
  "queueEnabled": true,
  "indexEnabled": true,
  "indexRequired": false,
  "lastMigration": "2026-01-02T12:00:00Z"
}
```



## Success Criteria

**Phase 1 Complete:**

- ✅ Simple Mode working for < 100 work efforts
- ✅ Mode detection working
- ✅ No dependencies (pure file system)

**Phase 2 Complete:**

- ✅ Queue system working (when enabled)
- ✅ Adaptive queue (enabled/disabled based on mode)
- ✅ Test script validates behavior

**Phase 3 Complete:**

- ✅ Sidecar index working (when enabled)
- ✅ Adaptive index (enabled/disabled based on mode)
- ✅ Fallback to scan when index disabled

**Phase 4 Complete:**

- ✅ Unified WorkEffortManager interface
- ✅ Automatic mode switching
- ✅ Seamless transition between modes

**Phase 5 Complete:**

- ✅ Migration logic working
- ✅ Rollback on failure
- ✅ Index population from file system

## Performance Characteristics

**Tiny Mode (< 10 work efforts):**

- Full scan: ~0.01-0.05 seconds
- Single lookup: ~0.01-0.05 seconds
- Write: ~0.01 seconds (direct)

**Simple Mode (10-20 work efforts):**

- Full scan: ~0.05-0.1 seconds
- Single lookup: ~0.05-0.1 seconds
- Write: ~0.01 seconds (direct)

**Standard Mode (>= 20 work efforts):**

- Index lookup: ~0.005 seconds (O(1)) ✅ Instant
- Full scan: ~0.1-0.5 seconds (fallback only)
- Write: ~0.5-1.5 seconds (queued, but safe)

**Performance Mode (>= 50 work efforts):**

- Index lookup: ~0.005 seconds (O(1)) ✅ Instant (required)
- Full scan: Not used (index required)
- Write: ~0.5-1.5 seconds (queued, required)

## Risk Mitigation

**Mode Switching:**

- ✅ Automatic detection on startup
- ✅ Migration only when needed
- ✅ Rollback on failure
- ✅ Config file tracks current mode

**Performance:**

- ✅ Simple Mode fast for small scale
- ✅ Complex Mode fast for large scale
- ✅ No unnecessary complexity

**Backwards Compatibility:**

- ✅ Simple Mode works without database
- ✅ Can disable complex features
- ✅ Migration is one-way (can't go back, but can disable)

## Dependencies (Conditional)

**Simple Mode:**

- No dependencies (pure Node.js)

**Complex Mode:**

- `better-sqlite3` or `sqlite3` - SQLite database (only if enabled)
- `gray-matter` - YAML frontmatter parsing
- `fs/promises` - File system operations
- `child_process` - Git command execution

## Out of Scope (Future Phases)

- API layer implementation
- Authentication/authorization
- Multi-repository coordination
- Performance benchmarking