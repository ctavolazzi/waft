---
name: Delete Stale Git Branches
overview: Delete the two stale feature branches (local and remote) that have been superseded by main.
todos:
  - id: delete-local
    content: Delete local feature branches
    status: in_progress
  - id: delete-remote
    content: Delete remote feature branches from origin
    status: pending
  - id: verify
    content: Verify branch cleanup
    status: pending

category: dreads
confidence: 0.83
constellation_date: 2026-01-14
---

# Delete Stale Git Branches

## Summary

Your main branch is fully up to date. Two stale feature branches can be safely deleted for cleanup:

- `feat/component-styles` (local + remote)
- `feat/utils-and-components` (local + remote)

## Actions

1. **Delete local branches**
   ```bash
   git branch -d feat/component-styles
   git branch -d feat/utils-and-components
   ```

2. **Delete remote branches on origin**
   ```bash
   git push origin --delete feat/component-styles
   git push origin --delete feat/utils-and-components
   ```

3. **Verify cleanup**
   ```bash
   git branch -a
   ```


## Expected Result

Only `main` branch will remain locally, with `remotes/origin/main` and `remotes/upstream/main` as the only remote refs.