# Release Plan: v0.8.1

**Date**: 2026-01-14 20:19:00  
**Current Version**: 0.7.1  
**Target Version**: 0.8.1  
**Release Type**: Minor Version Bump (+0.1.0)

---

## Pre-Release Checklist

### ✅ Phase 1: Preparation (CRITICAL)

- [ ] **1.1 Review Uncommitted Changes**
  - Review 35+ uncommitted files
  - Commit relevant changes
  - Stash or discard irrelevant changes
  - Clean working directory

- [ ] **1.2 Verify Version Consistency**
  - Current: pyproject.toml = 0.7.1
  - Latest tag: v0.6.1 (behind)
  - Target: 0.8.1
  - Action: Update to 0.8.1, create tag

- [ ] **1.3 Review All Branches**
  - List all 30+ branches
  - Categorize: merge, skip, archive
  - Review branch contents
  - Check for conflicts

- [ ] **1.4 Create Release Branch**
  - Branch: `release/v0.8.1`
  - From: `main` (or current branch)
  - Purpose: Safe testing environment

- [ ] **1.5 Scan for Secrets**
  - Check for API keys
  - Check for passwords
  - Check for tokens
  - Remove any secrets

---

### ✅ Phase 2: Branch Merging (HIGH)

- [ ] **2.1 Merge Validated Branches**
  - Merge one branch at a time
  - Resolve conflicts immediately
  - Test after each merge
  - Document conflict resolutions

- [ ] **2.2 Skip Problematic Branches**
  - Experimental branches
  - Broken branches
  - Superseded branches
  - Document skipped branches

- [ ] **2.3 Verify Merge Results**
  - Check for merge conflicts
  - Verify code compiles
  - Check for obvious errors

---

### ✅ Phase 3: Testing (HIGH)

- [ ] **3.1 Run Test Suite**
  - Execute all tests
  - Fix any failures
  - Verify test coverage

- [ ] **3.2 Test Critical Paths**
  - Test core functionality
  - Test CLI commands
  - Test integrations

- [ ] **3.3 Verify Dependencies**
  - Check dependency versions
  - Resolve conflicts
  - Update if needed

- [ ] **3.4 Check for Breaking Changes**
  - Review API changes
  - Check configuration changes
  - Document breaking changes

---

### ✅ Phase 4: Release Preparation (MEDIUM)

- [ ] **4.1 Update Version**
  - Update `pyproject.toml`: 0.7.1 → 0.8.1
  - Update `src/waft/__init__.py` if exists
  - Verify version consistency

- [ ] **4.2 Update CHANGELOG.md**
  - Add v0.8.1 entry
  - Document all changes
  - List new features
  - Note breaking changes

- [ ] **4.3 Create Release Notes**
  - File: `RELEASE_NOTES_v0.8.1.md`
  - Comprehensive change list
  - Migration guide if needed
  - Known issues

- [ ] **4.4 Update Documentation**
  - Update README if needed
  - Update API docs if needed
  - Update examples if needed

---

### ✅ Phase 5: Release Execution (MEDIUM)

- [ ] **5.1 Final Testing**
  - Run full test suite one more time
  - Verify installation
  - Test critical workflows

- [ ] **5.2 Commit Release**
  - Commit all release changes
  - Message: "Release v0.8.1"
  - Tag: `v0.8.1`

- [ ] **5.3 Merge to Main**
  - Merge `release/v0.8.1` → `main`
  - Push to GitHub
  - Verify merge success

- [ ] **5.4 Create GitHub Release**
  - Create release on GitHub
  - Upload release notes
  - Tag: `v0.8.1`
  - Mark as latest release

---

### ✅ Phase 6: Post-Release (MEDIUM)

- [ ] **6.1 Verify Release**
  - Check GitHub release page
  - Verify tag exists
  - Test installation from PyPI (if applicable)

- [ ] **6.2 Update Documentation**
  - Update website/docs
  - Announce release
  - Update examples

- [ ] **6.3 Monitor**
  - Watch for issues
  - Respond to feedback
  - Plan hotfix if needed

---

## Branch Review Strategy

### Branches to Merge (Validated)
- Review each branch
- Test before merging
- Only merge if:
  - Code is tested
  - No breaking changes (or documented)
  - No conflicts
  - Adds value

### Branches to Skip
- Experimental branches
- Broken branches
- Superseded branches
- Feature flags (conditional)

### Branches to Archive
- Old feature branches
- Deprecated implementations
- Proof of concepts

---

## Version Update Locations

1. `pyproject.toml` - Line 7: `version = "0.8.1"`
2. `src/waft/__init__.py` - If exists, update `__version__`
3. `CHANGELOG.md` - Add v0.8.1 entry
4. Create `RELEASE_NOTES_v0.8.1.md`

---

## Rollback Plan

If release fails:
1. Revert merge to main
2. Delete tag `v0.8.1`
3. Restore previous state
4. Document failure
5. Fix issues
6. Retry release

---

## Success Criteria

✅ All tests pass  
✅ No merge conflicts  
✅ Version updated correctly  
✅ CHANGELOG updated  
✅ Release notes created  
✅ GitHub release created  
✅ Tag pushed to GitHub  
✅ Release verified working

---

**This plan addresses all CRITICAL and HIGH issues from the critique.**
