---
name: Update System E2E Test
overview: Create an end-to-end test suite for the update system (check, install, rollback) using an isolated test root to avoid modifying the real installation.
todos:
  - id: create-test-file
    content: Create tests/update-system.test.js with test harness and fixtures setup
    status: completed
  - id: test-check
    content: Implement update check tests (API fetch, caching, refresh flag)
    status: completed
  - id: test-install
    content: Implement update install tests (backup creation, file update, version bump)
    status: completed
  - id: test-rollback
    content: Implement rollback tests (restore files, revert version, list backups)
    status: completed
  - id: run-tests
    content: Execute test suite and verify all tests pass
    status: completed

category: dreads
confidence: 0.40
constellation_date: 2026-01-14
---

# Update System End-to-End Test Plan

## Approach

Test the full update lifecycle in an **isolated sandbox** (`tests/fixtures/update-test/`) to avoid modifying the real installation.

```mermaid
flowchart LR
    subgraph setup [Setup]
        A[Create test root] --> B[Copy minimal files]
        B --> C[Initialize version tracking]
    end
    
    subgraph tests [Test Commands]
        D[update check] --> E[update install]
        E --> F[update rollback]
    end
    
    subgraph cleanup [Cleanup]
        G[Remove test fixtures]
    end
    
    setup --> tests --> cleanup
```



## File to Create

[tests/update-system.test.js](tests/update-system.test.js) - New test file

## Test Cases

### 1. Update Check (Network Test)

- Verify `checkForUpdates()` fetches from GitHub API
- Verify cache is created at `.update-cache.json`
- Verify `--refresh` bypasses cache
- Verify offline fallback uses stale cache

### 2. Update Install (Sandboxed)

- Create minimal test installation with `package.json` version set to `1.0.0`
- Run install targeting a known older tag (e.g., `v2.0.0`)
- Verify backup is created in `.backups/`
- Verify files are updated
- Verify version tracking is updated

### 3. Update Rollback

- After install, run `manualRollback()`
- Verify files restored from backup
- Verify version tracking reverted
- Test `--list` shows available backups

## Key Code Pattern

```javascript
const TEST_ROOT = path.join(__dirname, 'fixtures', 'update-test');
const UpdateChecker = require('../scripts/update-checker');
const UpdateInstaller = require('../scripts/update-installer');

// Use rootDir option to sandbox
const checker = new UpdateChecker({ rootDir: TEST_ROOT });
const installer = new UpdateInstaller({ rootDir: TEST_ROOT });
```



## Dependencies

- Requires network access for `update check` test
- Requires GitHub releases to exist for `update install` test
- No external dependencies to install

## Estimated Time