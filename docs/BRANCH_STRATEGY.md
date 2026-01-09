# Branch Strategy

**Last Updated**: 2026-01-07

## Overview

Waft uses a three-tier branch strategy for managing development, testing, and production releases:

- **`main`** = Production (stable, released versions)
- **`staging`** = Stable Dev (next version ready for production, tested and polished)
- **`dev`** = Experimental (active development, where Claude Code works)

## Branch Hierarchy

```
main (production)
  ↑
staging (stable dev)
  ↑
dev (experimental)
  ↑
feature/* branches
```

## Workflow

### 1. Feature Development

1. Create feature branch from `dev`:
   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b feature/my-feature
   ```

2. Work on feature, commit frequently

3. Merge feature back to `dev`:
   ```bash
   git checkout dev
   git merge --no-ff feature/my-feature
   git push origin dev
   ```

### 2. Dev → Staging Promotion

When features in `dev` are stable and tested:

```bash
./scripts/promote-dev-to-staging.sh
```

**What it does:**
- Validates `dev` branch (tests, linting, structure verification)
- Shows commits to be merged
- Merges `dev` into `staging` (no-ff merge)
- Optionally pushes to remote

**When to promote:**
- Features are complete and tested
- All tests passing
- Code is ready for final polish and testing

### 3. Staging → Main Promotion (Production Release)

When `staging` is ready for production:

```bash
./scripts/promote-staging-to-main.sh [--version VERSION]
```

**What it does:**
- Comprehensive validation (tests, linting, formatting, structure)
- Checks for debug code
- Shows commits to be merged
- Merges `staging` into `main` (no-ff merge)
- Creates release tag (if version provided)
- Optionally pushes to remote

**When to promote:**
- All features tested and polished
- No known bugs
- Documentation updated
- CHANGELOG updated
- Ready for production release

## Automation

### GitHub Actions

1. **Branch Protection CI** (`.github/workflows/branch-protection.yml`)
   - Runs on all pushes to `main`, `staging`, `dev`
   - Validates: tests, linting, formatting, project structure

2. **Staging Promotion Validation** (`.github/workflows/staging-promotion.yml`)
   - Runs on pushes to `staging` and PRs from `staging` → `main`
   - Comprehensive validation including debug code checks
   - Creates promotion report

### Scripts

1. **`scripts/promote-dev-to-staging.sh`**
   - Promotes `dev` → `staging`
   - Basic validation
   - Interactive confirmation

2. **`scripts/promote-staging-to-main.sh`**
   - Promotes `staging` → `main`
   - Comprehensive validation
   - Optional version tagging
   - Interactive confirmation

## Branch Protection Rules

### Main Branch
- **Protected**: Yes
- **Requires PR**: Yes (from `staging`)
- **Requires CI**: Yes (all checks must pass)
- **Requires Review**: Recommended
- **No direct pushes**: Yes (use promotion script)

### Staging Branch
- **Protected**: Yes
- **Requires PR**: Optional (from `dev`)
- **Requires CI**: Yes (all checks must pass)
- **Direct pushes**: Allowed (via promotion script)

### Dev Branch
- **Protected**: No
- **Direct pushes**: Allowed
- **CI**: Runs on all pushes

## Best Practices

1. **Always work on feature branches**, not directly on `dev`
2. **Test before promoting** - Run validation locally before using promotion scripts
3. **Use `--dry-run`** to preview promotion changes
4. **Update CHANGELOG** before promoting to `main`
5. **Tag releases** when promoting to `main`
6. **Keep `staging` stable** - Only promote from `dev` when features are complete
7. **Keep `main` production-ready** - Only promote from `staging` when ready for release

## Quick Reference

```bash
# Create feature branch
git checkout dev && git pull && git checkout -b feature/my-feature

# Promote dev → staging
./scripts/promote-dev-to-staging.sh

# Promote staging → main (with version tag)
./scripts/promote-staging-to-main.sh --version v0.0.3

# Dry run (preview without making changes)
./scripts/promote-staging-to-main.sh --dry-run
```

## Troubleshooting

### Promotion fails validation
- Fix issues in the source branch
- Re-run validation locally: `uv run pytest && uv run ruff check . && waft verify`
- Try promotion again

### Merge conflicts
- Resolve conflicts manually
- Test after resolving
- Continue promotion

### Need to rollback
- Use git revert or reset (carefully!)
- Document in CHANGELOG
- Consider hotfix branch if needed

