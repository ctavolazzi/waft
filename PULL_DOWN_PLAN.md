# Pull Down Cloud Code - Preparation Plan

**Created**: 2026-01-25
**Status**: ⏳ Waiting for cloud merges to complete
**Purpose**: Prepare for pulling merged code from origin/main

---

## Current State

### Local Branch Status
- **Current Branch**: `main`
- **Status**: Diverged from `origin/main`
  - Local has **2 commits** not on remote
  - Remote has **3 commits** not on local
- **Remote**: `https://github.com/ctavolazzi/waft.git`

### Uncommitted Changes
**Modified Files** (18 files):
- Work effort updates (WE-260116-65m0 integration)
- Devlog updates
- Visualizer components (BeingRenderer, DataTable, etc.)
- Model files (Being.ts, Evolution.ts, Village.ts, etc.)

**Untracked Files** (New):
- `Character.ts` (D&D character model)
- New services directory
- New test directory
- New utils directory
- Campaign planner components
- Character panel components
- Documentation files

---

## Waiting For

**Claude Code Browser** is currently:
- Working on code in cloud/remote
- Merging branches into `main`
- Need to wait until all branches are merged and available on `origin/main`

---

## When Ready to Pull

### Step 1: Save Current Work
Before pulling, decide what to do with local changes:

**Option A: Commit Local Changes**
```bash
# Review changes
git status
git diff

# Stage and commit
git add .
git commit -m "Local work: WAFT-FogSift integration + Character system"
```

**Option B: Stash Local Changes**
```bash
# Stash uncommitted changes
git stash push -m "WAFT-FogSift integration work"

# Stash untracked files too
git stash push -u -m "New Character system files"
```

**Option C: Create Backup Branch**
```bash
# Create backup of current state
git branch backup/local-work-$(date +%Y%m%d)
```

### Step 2: Fetch Latest from Remote
```bash
# Fetch all updates from remote
git fetch origin

# Check what's new
git log HEAD..origin/main --oneline
```

### Step 3: Merge or Rebase
**Option A: Merge (Recommended)**
```bash
# Merge remote changes into local
git pull origin main

# Resolve any conflicts if they occur
# Then commit the merge
```

**Option B: Rebase (Cleaner history)**
```bash
# Rebase local commits on top of remote
git pull --rebase origin main

# Resolve conflicts as they appear
# Continue with: git rebase --continue
```

### Step 4: Verify Integration
```bash
# Check status
git status

# Verify no conflicts
git log --oneline -10

# Test that everything still works
# (run tests, check visualizer, etc.)
```

---

## Pre-Pull Checklist

Before pulling, ensure:

- [ ] All important local work is committed or stashed
- [ ] You understand what changes are local vs remote
- [ ] You have a backup/restore plan if needed
- [ ] You're ready to resolve potential conflicts
- [ ] Cloud merges are complete (check GitHub)

---

## Post-Pull Actions

After successfully pulling:

1. **Verify Integration**
   - Check that WAFT-FogSift integration still works
   - Verify Character.ts is present (if merged)
   - Test visualizer components

2. **Resolve Conflicts** (if any)
   - Review conflict markers
   - Resolve manually
   - Test after resolution

3. **Update Documentation**
   - Update devlog if needed
   - Update work efforts if status changed

4. **Push Local Changes** (if committed)
   ```bash
   git push origin main
   ```

---

## Current Local Commits (Not on Remote)

Check what's local-only:
```bash
git log origin/main..main --oneline
```

## Remote Commits (Not on Local)

Check what's coming from cloud:
```bash
git log main..origin/main --oneline
```

---

## Notes

- **Character.ts**: New file created locally - may need to merge with cloud version
- **WAFT-FogSift Integration**: Completed locally - should be preserved
- **Visualizer Changes**: Multiple component updates - may conflict with cloud changes
- **Work Efforts**: Updated locally - should merge cleanly

---

## When Cloud Work is Complete

1. Check GitHub to confirm all branches merged
2. Run `git fetch origin` to get latest
3. Review `git log origin/main` to see what's new
4. Follow Step 1-4 above to pull and integrate

---

**Status**: ⏳ Waiting for cloud merges
**Next Action**: Monitor GitHub, then execute pull plan when ready
