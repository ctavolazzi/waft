---
name: Full Repository Cleanup
overview: Comprehensive cleanup of work efforts, git branches, outdated docs, and tech debt tracking. This will archive completed work efforts, delete merged branches, update stale documentation, and reconcile the TECH_DEBT.md file with current state.
todos:
  - id: create-archive
    content: Create _work_efforts/_archive/2025-12/ and legacy/ directories
    status: completed
  - id: archive-v030-wes
    content: Move 4 completed WE-251227-* work efforts to archive
    status: completed
    dependencies:
      - create-archive
  - id: archive-legacy-wes
    content: Move 00-09_* legacy work effort directories to archive
    status: completed
    dependencies:
      - create-archive
  - id: delete-branches
    content: Delete merged remote branches (theme-switcher-ux, theme-system-enhancements)
    status: completed
  - id: update-tech-debt
    content: Update TECH_DEBT.md with current state and resolve TD-010
    status: completed
  - id: review-continuation
    content: Review CONTINUATION.md for staleness
    status: completed
  - id: commit-cleanup
    content: Commit all cleanup changes with descriptive message
    status: completed
    dependencies:
      - archive-v030-wes
      - archive-legacy-wes
      - delete-branches
      - update-tech-debt
  - id: update-devlog
    content: Add cleanup summary to devlog
    status: completed
    dependencies:
      - commit-cleanup
---

# Full Repository Cleanup Plan

## Audit Summary

| Category | Finding | Action |
|----------|---------|--------|
| Work Efforts | 4 completed WEs from Dec 27 | Archive to `_work_efforts/_archive/` |
| Git Branches | 2 stale remote branches | Delete merged feature branches |
| Documentation | TECH_DEBT.md outdated | Update with current state |
| Legacy Work Efforts | 17+ old format WEs in `00-09_*` | Archive or migrate |
| Devlog | Contains plan reference | Clean up completed entries |

---

## 1. Archive Completed Work Efforts

All 4 v0.3.0 format WEs are marked **completed**:

| ID | Title | Tickets |
|----|-------|---------|
| WE-251227-fmhx | MCP System Dashboard | 4 |
| WE-251227-giok | MCP Integration Test Task | 2 |
| WE-251227-uzo7 | Work Effort System Rules Setup | 5 |
| WE-251227-x7k9 | API Architecture | 8 |

**Action:** Move to `_work_efforts/_archive/2025-12/`

---

## 2. Archive Legacy Work Efforts

17 old-format work efforts exist in `_work_efforts/00-09_*` directories:

```
00-09_category/00_subcategory/  (8 files)
00-09_category/01_subcategory/  (1 file)
00-09_category/02_features/     (3 files)
00-09_site_improvements/00_ui_ux/ (9 files)
```

**Action:** Move entire `00-09_*` directories to `_work_efforts/_archive/legacy/`

---

## 3. Delete Merged Git Branches

Remote branches that are merged and can be deleted:

- `origin/feature/theme-switcher-ux-improvements`
- `origin/feature/theme-system-enhancements`

**Action:** `git push origin --delete <branch>`

---

## 4. Update TECH_DEBT.md

Current file is outdated (last updated 2025-12-28). Updates needed:

| Section | Update |
|---------|--------|
| TD-010 | Theme logic is now DRY (single `app.js`) - mark resolved |
| File sizes | Update line counts (e.g., `sleep.js` is 596 lines, not 548) |
| Version | Bump to 0.0.5 |
| Phase 2: Build | Still accurate, no minification yet |
| New items | Consider adding wiki.css (1,135 lines) as TD candidate |

---

## 5. Clean Up Documentation

### Files to Review

| File | Issue |
|------|-------|
| [`FEATURE_VOID_AUDIT.md`](FEATURE_VOID_AUDIT.md) | Dec 27 audit - still valid, keep |
| [`CONTINUATION.md`](CONTINUATION.md) | May be stale, review |
| [`PULL_REQUEST.md`](PULL_REQUEST.md) | Template, keep |
| [`RELEASE_TEMPLATE.md`](RELEASE_TEMPLATE.md) | Template, keep |

---

## 6. Final Directory Structure

```
_work_efforts/
  _archive/
    2025-12/
      WE-251227-fmhx_mcp_system_dashboard/
      WE-251227-giok_mcp_integration_test_task/
      WE-251227-uzo7_work_effort_system_rules_setup/
      WE-251227-x7k9_api_architecture/
    legacy/
      00-09_category/
      00-09_site_improvements/
  devlog.md  (keep, trim old entries)
```

---

## Execution Order

1. Create archive directories
2. Move completed v0.3.0 work efforts to archive
3. Move legacy work efforts to archive
4. Delete merged git branches
5. Update TECH_DEBT.md
6. Review and update CONTINUATION.md
7. Commit cleanup changes
8. Update devlog with cleanup summary