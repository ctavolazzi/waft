# Bridge Prompt for Claude Code

**Copy this entire prompt and give it to Claude Code when you resume work:**

---

## Context: Branch Strategy Setup Complete - Next Steps

**IMPORTANT**: Tavern Keeper is being migrated to `treasuretavernhq-web` repo. This waft repo remains as a workshop/sandbox for future projects. The branch strategy we set up here is still valuable for future development in this repo.

I've just set up a three-tier branch strategy for the waft project. Here's where things stand:

### What Was Just Done
- Created automation scripts for branch promotion (`scripts/promote-dev-to-staging.sh`, `scripts/promote-staging-to-main.sh`)
- Created GitHub Actions workflows for branch protection and staging validation
- Created documentation (`docs/BRANCH_STRATEGY.md`)

### Current State
- **You are on `main` branch** (production) - but you should be working on `dev` branch
- **24 uncommitted files** need to be moved to `dev` branch
- **Branch structure not created yet** - `dev` and `staging` branches don't exist

### Branch Strategy
- **`main`** = Production (stable, released)
- **`staging`** = Stable Dev (next version ready for production)
- **`dev`** = Experimental (where Claude Code should work)

### What You Need to Do First

**Step 1: Set up branches** (run these commands):
```bash
# Create dev branch from current main (with uncommitted work)
git checkout -b dev
git add .
git commit -m "chore: move current work to dev branch - engineering workflow and exploration"
git push -u origin dev

# Create staging branch from clean main
git checkout main
git checkout -b staging
git push -u origin staging

# Push the one commit ahead on main
git push origin main
```

**Step 2: Continue work on `dev` branch**
- Switch to `dev`: `git checkout dev`
- Continue the engineering workflow you were doing
- All future work should be on `dev` (or feature branches from `dev`)

### What You Were Working On
- Engineering workflow: Phase 1 (Spin-Up) ✅ and Phase 2 (Explore) ✅ complete
- Identified issue: Debug logging code in `dashboard.py`, `substrate.py`, `web.py` (63 total occurrences)
- Next: Phase 3-6 (Plan, Critique, Finalize, Implement)

### Key Files Created
- `scripts/promote-dev-to-staging.sh` - Promotes dev → staging
- `scripts/promote-staging-to-main.sh` - Promotes staging → main (with comprehensive validation)
- `.github/workflows/branch-protection.yml` - CI for all branches
- `.github/workflows/staging-promotion.yml` - Validation for staging → main
- `docs/BRANCH_STRATEGY.md` - Complete guide

### Important Rules Going Forward
- ✅ **Always work on `dev` branch** (or feature branches from `dev`)
- ✅ **Use promotion scripts** to move work forward (`./scripts/promote-*.sh`)
- ❌ **Never commit directly to `main`** - always use promotion scripts
- ❌ **Never commit directly to `staging`** - use promotion script

### Quick Reference
```bash
# Check current branch
git branch --show-current

# Switch to dev
git checkout dev

# Promote dev → staging
./scripts/promote-dev-to-staging.sh

# Promote staging → main (with version tag)
./scripts/promote-staging-to-main.sh --version v0.0.3
```

### Documentation
- Read `docs/BRANCH_STRATEGY.md` for complete branch strategy guide
- Read `.cursor/CLAUDE_CODE_CONTEXT.md` for detailed context
- Read `_pyrite/active/2026-01-07_exploration_comprehensive.md` for exploration findings

---

**Your immediate action**: Set up the branches (Step 1 above), then continue your engineering workflow on the `dev` branch.

