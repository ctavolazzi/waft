---
name: Git Full Cleanup
overview: Sync local main with origin/main and clean up stale remote branches from merged PRs.
todos:
  - id: sync-main
    content: Pull latest changes to sync local main with origin/main
    status: completed
  - id: delete-remote-branches
    content: Attempt to delete remote branches via git push --delete
    status: completed
  - id: manual-cleanup
    content: If push fails, provide GitHub UI guidance for branch deletion
    status: cancelled
    dependencies:
      - delete-remote-branches
  - id: prune-refs
    content: Run git fetch --prune to clean up local tracking refs
    status: completed
    dependencies:
      - delete-remote-branches

category: dreads
confidence: 1.00
constellation_date: 2026-01-14
---

# Git Repository Full Cleanup

## Current State
- Local `main` is 1 commit behind `origin/main`
- Remote branches still exist on GitHub:
  - `claude/explore-repo-findings-bI3VB` (from merged PR #8)
  - `claude/v0-0-2-baseline-and-workflows-bI3VB` (may have open PR)
- No stale local tracking refs to prune

## Plan

### Step 1: Sync Local Main
```bash
git pull origin main
```
This will fast-forward your local main to match origin/main (commit `facdf08`).

### Step 2: Attempt Remote Branch Cleanup
```bash
git push origin --delete claude/explore-repo-findings-bI3VB
git push origin --delete claude/v0-0-2-baseline-and-workflows-bI3VB
```

**Note:** Based on the previous 403 error, this may fail due to GitHub branch protection or permission settings.

### Step 3: Manual Cleanup (if Step 2 fails)
If the git push delete commands fail, delete branches via GitHub UI:
1. Go to your repository on GitHub
2. Click "Branches" (or go to `/{owner}/{repo}/branches`)
3. Find each stale branch and click the trash icon

### Step 4: Prune Local Tracking References
After remote branches are deleted:
```bash
git fetch --prune
```
This removes local references to branches that no longer exist on the remote.

## Expected Final State
- Local `main` synced with `origin/main`
- No stale remote branches
- Clean `git branch -a` output showing only `main` and `remotes/origin/main`