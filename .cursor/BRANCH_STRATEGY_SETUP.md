# Branch Strategy Setup - Context for Claude Code

**Date**: 2026-01-07
**Status**: ✅ Automation Created, Branches Need Setup

---

## What Just Happened

We've set up a three-tier branch strategy for the waft project:

- **`main`** = Production (stable, released versions)
- **`staging`** = Stable Dev (next version ready for production, tested and polished)
- **`dev`** = Experimental (active development, where Claude Code should work)

## Current State

### Branch Status
- **Current branch**: `main`
- **Uncommitted changes**: 24 files (20 modified, 3 untracked, 1 untracked)
- **Local commits ahead**: 1 commit (`cdf54fe` - "fix: add Tavern Keeper hook to info command")
- **Remote status**: `origin/main` is at `fec665d` (Tavern Keeper merge)

### Files Changed
- Documentation updates (CHANGELOG, CONTRIBUTING, RELEASE_NOTES)
- `_pyrite/active/` files (work documentation)
- `src/waft/ui/dashboard.py` (contains debug logging code)
- Test files
- New exploration documents from engineering workflow

### What Was Created
1. **Promotion Scripts**:
   - `scripts/promote-dev-to-staging.sh` - Promotes dev → staging
   - `scripts/promote-staging-to-main.sh` - Promotes staging → main (with comprehensive validation)

2. **GitHub Actions Workflows**:
   - `.github/workflows/branch-protection.yml` - CI for all branches
   - `.github/workflows/staging-promotion.yml` - Validation for staging → main

3. **Documentation**:
   - `docs/BRANCH_STRATEGY.md` - Complete branch strategy guide

## What Needs to Happen Next

### Immediate Actions Required

1. **Set up branch structure**:
   ```bash
   # Create dev branch from current main (with uncommitted changes)
   git checkout -b dev
   git add .
   git commit -m "chore: move current work to dev branch"
   git push -u origin dev

   # Create staging branch from main (clean, production-ready)
   git checkout main
   git checkout -b staging
   git push -u origin staging
   ```

2. **Move uncommitted work to dev**:
   - All current uncommitted changes should go to `dev` branch
   - This includes the debug logging code cleanup work
   - This includes the engineering workflow exploration documents

3. **Sync main with origin**:
   ```bash
   git checkout main
   git push origin main  # Push the one commit ahead
   ```

## Where Claude Code Should Work

**Claude Code should work on the `dev` branch**, not `main`.

### Workflow for Claude Code

1. **Always start by checking out dev**:
   ```bash
   git checkout dev
   git pull origin dev
   ```

2. **Create feature branches from dev**:
   ```bash
   git checkout -b feature/my-feature
   # ... do work ...
   git checkout dev
   git merge --no-ff feature/my-feature
   git push origin dev
   ```

3. **For experimental work**: Work directly on `dev` branch

4. **Never work directly on `main`** - Always use promotion scripts

## Automation Available

### Promotion Scripts

**Dev → Staging**:
```bash
./scripts/promote-dev-to-staging.sh
```
- Runs basic validation (tests, structure verification)
- Interactive confirmation
- Use when features are stable and tested

**Staging → Main**:
```bash
./scripts/promote-staging-to-main.sh [--version VERSION]
```
- Comprehensive validation (tests, linting, formatting, debug code checks)
- Optional version tagging
- Interactive confirmation
- Use when ready for production release

**Dry Run** (preview without making changes):
```bash
./scripts/promote-staging-to-main.sh --dry-run
```

## Key Points for Claude Code

1. **You are currently on `main` branch** - This is production, not where you should work
2. **You have 24 uncommitted files** - These should be moved to `dev` branch
3. **Debug logging code exists** - Should be cleaned up before promoting to main
4. **New automation is ready** - Use promotion scripts, don't merge manually
5. **Work on `dev` branch** - That's where experimental/development work happens

## Next Steps for Claude Code

When you resume work:

1. **Check current branch**: `git branch --show-current`
2. **If on `main`**: Switch to `dev` (or create it if it doesn't exist)
3. **If uncommitted changes exist**: Commit them to `dev` branch
4. **Continue your work on `dev` branch**
5. **Use feature branches** for discrete features
6. **Promote to staging** when features are stable
7. **Promote to main** when ready for production

## Branch Protection

- **Main**: Protected, requires PR from staging, all CI must pass
- **Staging**: Protected, requires CI to pass, direct pushes allowed via promotion script
- **Dev**: Not protected, direct pushes allowed, CI runs on all pushes

## Important Notes

- **Never commit directly to `main`** - Always use promotion scripts
- **Test before promoting** - Run validation locally first
- **Use `--dry-run`** to preview promotion changes
- **Update CHANGELOG** before promoting to main
- **Tag releases** when promoting to main

## Current Work Context

Based on the exploration, the main work items identified were:
1. **Debug logging code cleanup** (57 occurrences in dashboard.py, 1 in substrate.py, 5 in web.py)
2. **Review and commit uncommitted changes** (24 files)
3. **Engineering workflow continuation** (exploration phase complete, ready for planning)

## Quick Reference Commands

```bash
# Check current branch
git branch --show-current

# Switch to dev
git checkout dev

# Create feature branch
git checkout -b feature/my-feature

# Promote dev → staging
./scripts/promote-dev-to-staging.sh

# Promote staging → main
./scripts/promote-staging-to-main.sh --version v0.0.3

# Dry run
./scripts/promote-staging-to-main.sh --dry-run
```

---

**Status**: Automation ready, branches need to be created and current work moved to `dev`

**Action Required**: Set up branches and move current work to `dev` branch before continuing development work

