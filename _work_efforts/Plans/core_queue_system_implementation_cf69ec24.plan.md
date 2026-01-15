---
name: Core Queue System Implementation
overview: Implement the foundational Job Queue system (`core/QueueSystem.js`) with sequential processing and error handling, plus a test script (`test-queue.js`) to validate the implementation.
todos:
  - id: create_core_directory
    content: Create core/ directory at repository root
    status: pending
  - id: create_queue_system_file
    content: Create core/QueueSystem.js with Job and JobQueue classes as specified
    status: pending
    dependencies:
      - create_core_directory
  - id: create_test_script
    content: Create test-queue.js at repository root with three test jobs (normal, failing, normal)
    status: pending
    dependencies:
      - create_queue_system_file
  - id: run_test_validation
    content: Run node test-queue.js and verify sequential processing and error recovery
    status: pending
    dependencies:
      - create_test_script
---

# Core Queue System

Implementation

## Overview

This implements the foundational **Job Queue System** for Pyrite's "Safe Mode" architecture. The queue ensures sequential processing of operations (like Git commits, file writes) to prevent concurrency conflicts and provides robust error handling.

## Files to Create

### 1. `core/QueueSystem.js`

**Purpose**: Core queue logic with `Job` and `JobQueue` classes.

**Key Components**:

- **`Job` class**: Represents a single queued operation

- Properties: `id`, `type`, `payload`, `status`, `logs`, `createdAt`

- Method: `log(message)` for operation logging

- **`JobQueue` class**: Manages the FIFO queue

- Properties: `queue[]`, `isProcessing` flag

- Methods:

    - `add(type, payload)` - Enqueue a job and trigger processing

    - `processNext()` - Sequential processing loop (with lock)

    - `executeJob(job)` - Mock worker (simulates 500-1500ms I/O)

    - `getPending()` - Helper to inspect queue

**Architecture**:

- Sequential processing: Only one job runs at a time (`isProcessing` lock)

- Error isolation: Failed jobs don't crash the queue (try/catch/finally)

- Auto-continuation: `processNext()` recurses after each job completes

- Mock implementation: Uses `setTimeout` to simulate async work (will be replaced with real Git/file operations later)

### 2. `test-queue.js`

**Purpose**: Validation script proving sequential processing and error recovery.

**Test Cases**:

1. Normal job (should succeed)

2. Failing job (with `shouldFail: true` payload) - tests error handling

3. Another normal job (proves queue recovers after failure)

**Expected Behavior**:

- Jobs process one at a time (sequential)

- Job 2 fails but doesn't crash the system

- Job 3 still executes successfully

- Console logs show job lifecycle (STARTED → COMPLETED/FAILED)

## Implementation Details

### Directory Structure

- Create `core/` directory at repository root
- Place `QueueSystem.js` in `core/`

- Place `test-queue.js` at repository root

### Code Specifications

The exact code is provided in the iteration report:

- `Job` class with unique ID generation (`job_${timestamp}_${random}`)

- `JobQueue` class with async/await processing loop

- Mock `executeJob` that simulates 500-1500ms work duration

- Error simulation via `payload.shouldFail` flag

### Testing

Run: `node test-queue.js`

**Expected Output**:

```javascript
=== STARTING QUEUE TEST ===
[Queue] Added Job job_... (CREATE_WORK_EFFORT)
[Job job_...] STARTED processing: CREATE_WORK_EFFORT
[Job job_...] COMPLETED successfully
[Queue] Added Job job_... (CREATE_WORK_EFFORT)
[Job job_...] STARTED processing: CREATE_WORK_EFFORT
[Job job_...] FAILED: Simulated random failure!
[Queue] Added Job job_... (CREATE_WORK_EFFORT)
[Job job_...] STARTED processing: CREATE_WORK_EFFORT
[Job job_...] COMPLETED successfully
Pending Jobs: 0
```



## Integration Points (Future)

This foundation will later integrate with:

- **File I/O operations**: Replace mock `executeJob` with real file writes

- **Git operations**: Add Git commit/push to job execution

- **Event Bus**: Emit events when jobs complete/fail

- **Sidecar Index**: Update SQLite index after successful writes

## Risk Assessment

**Low Risk**:

- Isolated implementation (no dependencies on existing code)

- Mock implementation (no file system changes)

- Simple test script (console output only)

**Validation**:

- The `finally` block ensures `isProcessing` is always reset

- Recursive `processNext()` ensures queue continues after errors

- Job status tracking allows UI to monitor progress (future)

## Next Steps (Post-Implementation)

After validation:

1. Replace mock `executeJob` with real file write operations

2. Add Git commit logic to job execution

3. Integrate with Event Bus for job lifecycle events

4. Add persistence layer (save queue state to disk)