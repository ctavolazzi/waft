---
name: Update System E2E Test
overview: Create an end-to-end test suite for the update system (check, install, rollback) using an isolated test root to avoid modifying the real installation.
todos: []
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