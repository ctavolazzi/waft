---
name: Evolve Devlog System and GitHub Feature Branch Evolution
overview: Evolve the devlog system to use categorized, organized, timestamped entry files based on source context, and enhance the /evolve command to use GitHub MCP for feature branch-based evolution workflows.
todos:
  - id: devlog-manager
    content: Create DevlogManager class in src/waft/core/devlog.py with source detection, categorization, and entry management
    status: pending
  - id: devlog-structure
    content: Create _work_efforts/devlog/ directory structure (by_source, by_category, by_date) with index.json
    status: pending
  - id: devlog-migration
    content: Create migration script to parse existing devlog.md and create categorized entry files
    status: pending
  - id: update-visualizer
    content: Update Visualizer._get_recent_devlog() to use DevlogManager
    status: pending
  - id: update-status
    content: Update scripts/waft_status.py to use DevlogManager
    status: pending
  - id: github-mcp-check
    content: Verify GitHub MCP availability and add connection check to evolve workflow
    status: completed
  - id: github-branch-creation
    content: Add feature branch creation to evolve workflow using GitHub MCP
    status: pending
  - id: github-commit-strategy
    content: Implement commit strategy for workflow phases (spawn, version-bake, lineage, evolution)
    status: pending
  - id: github-pr-creation
    content: Add PR creation at end of evolution workflow with evolution summary and genetic lineage
    status: pending
  - id: update-evolve-command
    content: Update .cursor/commands/evolve.md with GitHub workflow documentation
    status: pending
  - id: update-evolve-script
    content: Update scripts/execute_full_evolve.py with GitHub integration
    status: pending
  - id: test-integration
    content: "Test complete workflow: devlog + GitHub feature branch evolution"
    status: pending
---

# Plan: Evolve Devlog System and GitHub Feature Branch Evolution

## Overview

This plan evolves two major systems:

1. **Devlog System**: Transform from single-file to categorized, organized, timestamped entry files based on update source
2. **Evolve Command**: Integrate GitHub MCP to use feature branches for evolution workflows

---

## Part 1: Evolve Devlog System

### Current State

- Single file: `_work_efforts/devlog.md` (4596+ lines)
- Manual entry format: `## YYYY-MM-DD - Title` with content
- Read by `Visualizer._get_recent_devlog()` and `waft_status.py`
- No categorization or source tracking

### Target State

- Categorized entry files in `_work_efforts/devlog/` directory structure
- Timestamped entries: `YYYY-MM-DD_HHMMSS_[source]_[category].md`
- Source-based organization (command, script, manual, api, etc.)
- Category-based organization (feature, bugfix, refactor, documentation, etc.)
- Maintain backward compatibility with existing devlog.md
- Index file for fast lookups

### Implementation

#### 1.1 Create DevlogManager Class

**File**: `src/waft/core/devlog.py` (new file)

**Purpose**: Centralized devlog management with categorization and source tracking

**Key Methods**:

- `write_entry(content, source, category, metadata)` - Write categorized entry
- `get_recent_entries(limit, source, category)` - Query entries
- `migrate_legacy_devlog()` - Migrate existing devlog.md to new structure
- `get_entry_path(source, category, timestamp)` - Generate file paths

**Entry Structure**:

```markdown
# Devlog Entry

**Timestamp**: YYYY-MM-DD HH:MM:SS
**Source**: command|script|api|manual|being|workflow
**Category**: feature|bugfix|refactor|documentation|research|maintenance
**Context**: {git_branch, work_effort, being_id, command_name, etc.}

## Content
[Entry content]
```

#### 1.2 Directory Structure

```
_work_efforts/
├── devlog.md                    # Legacy file (kept for compatibility)
└── devlog/                      # New categorized structure
    ├── index.json               # Fast lookup index
    ├── by_source/               # Organized by update source
    │   ├── command/              # From cursor commands
    │   │   ├── 2026-01-12_201430_evolve_feature.md
    │   │   └── 2026-01-12_201500_checkpoint_maintenance.md
    │   ├── script/               # From Python scripts
    │   ├── api/                  # From API endpoints
    │   ├── manual/               # Manual entries
    │   ├── being/                # From Being system
    │   └── workflow/             # From workflow commands
    ├── by_category/              # Organized by category
    │   ├── feature/
    │   ├── bugfix/
    │   ├── refactor/
    │   ├── documentation/
    │   ├── research/
    │   └── maintenance/
    └── by_date/                  # Organized by date
        └── 2026-01-12/
            └── [all entries for this date]
```

#### 1.3 Source Detection

**Automatic source detection**:

- `command`: When called from `.cursor/commands/` execution
- `script`: When called from `scripts/` directory
- `api`: When called from API routes
- `being`: When called from Being system
- `workflow`: When called from workflow commands (`/version-bake`, `/evolve`, etc.)
- `manual`: Explicit manual entry

**Context capture**:

- Git branch name
- Work effort ID (if active)
- Being ID (if in Being context)
- Command name (if from command)
- File paths modified
- Session statistics

#### 1.4 Update Existing Code

**Files to modify**:

- `src/waft/core/visualizer.py` - Update `_get_recent_devlog()` to use DevlogManager
- `scripts/waft_status.py` - Update to use DevlogManager
- All commands that write to devlog - Use DevlogManager instead of direct file writes

**Backward compatibility**:

- Keep `devlog.md` for reading (legacy support)
- New entries go to categorized structure
- Migration script to move old entries

#### 1.5 Migration Strategy

1. Create `DevlogManager` class
2. Parse existing `devlog.md` to extract entries
3. Categorize entries by content analysis (keywords, patterns)
4. Create categorized entry files
5. Update index.json
6. Keep `devlog.md` as read-only archive

---

## Part 2: Evolve /evolve Command with GitHub Feature Branches

### Current State

- Command documented in `.cursor/commands/evolve.md`
- Executed via `scripts/execute_full_evolve.py`
- Spawns Being, runs version-bake workflow
- No GitHub integration
- No feature branch workflow

### Target State

- Use GitHub MCP to create feature branches for evolution
- Each evolution gets its own feature branch: `evolve/[being_id]` or `evolve/[feature-name]`
- Workflow commits to feature branch
- Create PR at end of evolution
- Merge strategy configurable
- Full GitHub integration for evolution tracking

### Implementation

#### 2.1 GitHub MCP Integration

**Check GitHub MCP availability**:

- ✅ **VERIFIED**: GitHub MCP is available and working
- ✅ Successfully tested: `mcp_github_get_me` returns user info (ctavolazzi)
- ✅ GitHub CLI authenticated and operational
- Handle graceful fallback if GitHub MCP unavailable (for future robustness)

**GitHub MCP Tools to Use**:

- `mcp_github_create_branch` - Create feature branch
- `mcp_github_create_or_update_file` - Commit changes to branch
- `mcp_github_create_pull_request` - Create PR at end
- `mcp_github_list_branches` - Check existing branches
- `mcp_github_get_commit` - Track commit history

#### 2.2 Enhanced Evolve Workflow

**File**: Update `.cursor/commands/evolve.md` and `scripts/execute_full_evolve.py`

**New Workflow Sequence**:

```
1. Check GitHub MCP availability
2. Create feature branch: evolve/[being_id] or evolve/[feature-name]
3. Spawn Being from Source
4. Execute /version-bake workflow (commits to feature branch)
5. Track genetic lineage (commits to feature branch)
6. Document evolution (commits to feature branch)
7. Create Pull Request (optional, configurable)
8. Return learnings to Source
```

#### 2.3 Branch Naming Strategy

**Pattern**: `evolve/[being_id]` or `evolve/[feature-name]`

**Examples**:

- `evolve/being_20260112_201430_a1b2c3d4`
- `evolve/devlog-system-evolution`
- `evolve/github-integration`

**Branch metadata**:

- Being ID in branch name
- PR description includes genetic lineage
- Commits reference Being ID

#### 2.4 Commit Strategy

**Commit points**:

1. After Being spawn (initial commit)
2. After each workflow phase (optional, configurable)
3. After genetic lineage tracking
4. After evolution documentation
5. Final commit with complete evolution record

**Commit messages**:

- Format: `[evolve] [being_id] Phase: Description`
- Include Being ID for traceability
- Reference genetic lineage

#### 2.5 Pull Request Creation

**When to create PR**:

- End of evolution workflow
- Configurable (always, on success, never)
- PR includes:
  - Evolution summary
  - Genetic lineage
  - Being metadata
  - Workflow results
  - Testing status

**PR Template**:

```markdown
# Evolution: [Being ID]

## Being Evolution Summary
- Being ID: `[being_id]`
- Reality: `[reality_id]`
- Fitness: [fitness]

## Genetic Lineage
[Lineage chain from Source → Being → Work → Evolution]

## Workflow Results
[Summary of workflow phases]

## Changes
[List of files changed]

## Testing
[Testing status]
```

#### 2.6 Fallback Strategy

**If GitHub MCP unavailable**:

- Log warning
- Continue with local evolution (current behavior)
- Document in devlog that GitHub integration was skipped
- Suggest manual branch creation

#### 2.7 Integration Points

**Files to modify**:

- `.cursor/commands/evolve.md` - Update documentation
- `scripts/execute_full_evolve.py` - Add GitHub integration
- `src/waft/being.py` - Add GitHub context to Being metadata
- `src/waft/core/devlog.py` - Log GitHub branch operations

**New dependencies**:

- GitHub MCP server (already configured per AGENTS.md)
- Git operations for branch management

---

## Implementation Order

### Phase 1: Devlog System Evolution

1. Create `DevlogManager` class
2. Implement directory structure
3. Implement source detection
4. Update existing code to use DevlogManager
5. Create migration script
6. Test with sample entries

### Phase 2: GitHub Integration

1. ✅ Verify GitHub MCP availability - **COMPLETED**
2. Add branch creation to evolve workflow
3. Add commit strategy
4. Add PR creation
5. Update documentation
6. Test full workflow

### Phase 3: Integration & Testing

1. Integrate both systems
2. Test end-to-end workflow
3. Update all documentation
4. Create migration guide
5. Update devlog with evolution

---

## Files to Create/Modify

### New Files

- `src/waft/core/devlog.py` - DevlogManager class
- `scripts/migrate_devlog.py` - Migration script
- `_work_efforts/devlog/` - New directory structure

### Modified Files

- `.cursor/commands/evolve.md` - Add GitHub workflow
- `scripts/execute_full_evolve.py` - Add GitHub integration
- `src/waft/core/visualizer.py` - Use DevlogManager
- `scripts/waft_status.py` - Use DevlogManager
- All commands that write devlog - Use DevlogManager

### Documentation

- Update `AGENTS.md` with new devlog system
- Create migration guide
- Update command documentation

---

## Success Criteria

### Devlog System

- ✅ Categorized entry files created
- ✅ Source tracking working
- ✅ Backward compatibility maintained
- ✅ Migration completed
- ✅ All existing code updated

### GitHub Integration

- ✅ Feature branches created
- ✅ Commits made during workflow
- ✅ PRs created (if configured)
- ✅ Fallback works if GitHub unavailable
- ✅ Full workflow tested

---

## Notes

- Devlog migration preserves all existing entries
- GitHub integration is optional (graceful fallback)
- Both systems work independently
- Can be implemented incrementally