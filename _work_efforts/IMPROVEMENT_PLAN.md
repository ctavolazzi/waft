# Waft Framework Improvement Plan

**Created**: 2026-01-04
**Status**: Planning → Ready for Execution

## Overview

Comprehensive plan to improve waft framework quality, documentation, and reliability after recent expansion that added 4 new CLI commands.

## Goals

1. ✅ Fix known bugs
2. ✅ Update all documentation
3. ✅ Add test infrastructure
4. ✅ Validate end-to-end functionality
5. ✅ Improve error handling

---

## Phase 1: Critical Fixes (30 minutes)

### 1.1 Fix `waft info` Bug
**Issue**: Duplicate "Project Name" entries in output
**Root Cause**: Logic flow issue in info command
**Fix**: Simplify project info extraction logic
**Files**: `src/waft/main.py`
**Priority**: High
**Estimated Time**: 10 minutes

**Steps**:
1. Review current `info` command implementation
2. Fix duplicate row issue
3. Test with `waft info` command
4. Verify output is clean

---

## Phase 2: Documentation Updates (45 minutes)

### 2.1 Update README.md
**Current State**: Only documents 2 commands (new, verify)
**Target State**: Document all 6 commands with examples
**Priority**: High
**Estimated Time**: 30 minutes

**Content to Add**:
- `waft sync` command documentation
- `waft add <package>` command documentation
- `waft init` command documentation
- `waft info` command documentation
- Update "Commands" section with all 6 commands
- Add usage examples for each command
- Update "What Waft Creates" to mention .gitignore and README templates

**Sections to Update**:
- Commands section (expand from 2 to 6)
- Quick Start (add examples of new commands)
- Project Structure (mention new templates)

### 2.2 Update CHANGELOG.md
**Current State**: Only has 0.0.1 release
**Target State**: Add unreleased section or prepare 0.0.2
**Priority**: Medium
**Estimated Time**: 15 minutes

**Content to Add**:
```markdown
## [Unreleased] or [0.0.2] - 2026-01-04

### Added
- `waft sync` command to sync project dependencies
- `waft add <package>` command to add dependencies
- `waft init` command to initialize Waft in existing projects
- `waft info` command to show project information
- `.gitignore` template generation
- `README.md` template generation
- MemoryManager utility methods (get_active_files, get_backlog_files, get_standards_files)
- SubstrateManager.get_project_info() method

### Changed
- Enhanced CLI with 4 new commands
- Improved project scaffolding with additional templates
```

---

## Phase 3: Testing Infrastructure (2 hours)

### 3.1 Set Up Test Structure
**Priority**: High
**Estimated Time**: 30 minutes

**Tasks**:
1. Create `tests/` directory structure
2. Create `tests/__init__.py`
3. Create `tests/conftest.py` with fixtures
4. Create `tests/test_main.py` for CLI tests
5. Create `tests/test_memory.py` for MemoryManager tests
6. Create `tests/test_substrate.py` for SubstrateManager tests
7. Create `tests/test_templates.py` for TemplateWriter tests
8. Update `pyproject.toml` to include pytest in dev dependencies (already there)

**Directory Structure**:
```
tests/
├── __init__.py
├── conftest.py
├── test_main.py
├── test_memory.py
├── test_substrate.py
└── test_templates.py
```

### 3.2 Write Basic Tests
**Priority**: High
**Estimated Time**: 90 minutes

**Test Coverage Goals**:

#### `tests/test_memory.py`
- ✅ Test `create_structure()` creates all required folders
- ✅ Test `verify_structure()` with valid structure
- ✅ Test `verify_structure()` with missing folders
- ✅ Test `get_active_files()` returns correct files
- ✅ Test `get_backlog_files()` returns correct files
- ✅ Test `get_standards_files()` returns correct files

#### `tests/test_substrate.py`
- ✅ Test `init_project()` creates project
- ✅ Test `sync()` runs successfully
- ✅ Test `add_dependency()` adds package
- ✅ Test `verify_lock()` checks for uv.lock
- ✅ Test `get_project_info()` extracts name and version

#### `tests/test_templates.py`
- ✅ Test `write_justfile()` creates Justfile
- ✅ Test `write_ci_yml()` creates CI workflow
- ✅ Test `write_agents_py()` creates agents.py
- ✅ Test `write_gitignore()` creates .gitignore
- ✅ Test `write_readme()` creates README.md
- ✅ Test `write_all()` creates all templates

#### `tests/test_main.py`
- ✅ Test `waft new` creates project structure
- ✅ Test `waft verify` validates structure
- ✅ Test `waft sync` runs successfully
- ✅ Test `waft add` adds dependency
- ✅ Test `waft init` initializes existing project
- ✅ Test `waft info` shows project information

**Test Utilities Needed**:
- Temporary directory fixture
- Mock subprocess calls for uv commands
- File system assertions

---

## Phase 4: End-to-End Validation (30 minutes)

### 4.1 Test All Commands
**Priority**: High
**Estimated Time**: 30 minutes

**Test Scenarios**:

1. **Fresh Project Creation**
   ```bash
   waft new test_project
   cd test_project
   waft verify
   waft info
   ```

2. **Existing Project Initialization**
   ```bash
   mkdir existing_project
   cd existing_project
   uv init --name existing_project
   waft init
   waft verify
   ```

3. **Dependency Management**
   ```bash
   waft sync
   waft add pytest
   waft verify
   ```

4. **Template Verification**
   - Check all templates are created
   - Verify template content is correct
   - Test that existing files aren't overwritten

**Validation Checklist**:
- [ ] `waft new` creates complete project structure
- [ ] `waft verify` correctly validates structure
- [ ] `waft sync` syncs dependencies
- [ ] `waft add` adds dependencies to pyproject.toml
- [ ] `waft init` works on existing projects
- [ ] `waft info` displays correct information
- [ ] All templates are generated correctly
- [ ] No errors or warnings in output

---

## Phase 5: Error Handling Improvements (1 hour)

### 5.1 Input Validation
**Priority**: Medium
**Estimated Time**: 30 minutes

**Improvements**:
- Validate project names (no special characters, valid Python identifier)
- Validate paths exist before operations
- Better error messages for common failures
- Graceful handling of missing dependencies (uv, just)

**Files to Update**:
- `src/waft/main.py` - Add validation functions
- `src/waft/core/substrate.py` - Better error messages
- `src/waft/core/memory.py` - Path validation

### 5.2 Error Messages
**Priority**: Medium
**Estimated Time**: 30 minutes

**Improvements**:
- More descriptive error messages
- Suggest solutions in error messages
- Use Rich for better error formatting
- Add context to subprocess errors

**Example Improvements**:
- Instead of: "Failed to initialize uv project"
- Show: "Failed to initialize uv project. Is 'uv' installed? Run: curl -LsSf https://astral.sh/uv/install.sh | sh"

---

## Phase 6: Code Quality (1 hour)

### 6.1 Code Review
**Priority**: Low
**Estimated Time**: 30 minutes

**Tasks**:
- Review all new code for consistency
- Check docstrings are complete
- Verify type hints where appropriate
- Look for code duplication

### 6.2 Refactoring Opportunities
**Priority**: Low
**Estimated Time**: 30 minutes

**Potential Improvements**:
- Extract common patterns
- Improve code organization
- Add helper functions where needed
- Ensure consistent error handling patterns

---

## Execution Order

1. **Phase 1** - Fix critical bug (10 min)
2. **Phase 2** - Update documentation (45 min)
3. **Phase 4** - End-to-end validation (30 min) - *Do this before tests to ensure everything works*
4. **Phase 3** - Add test infrastructure (2 hours)
5. **Phase 5** - Improve error handling (1 hour)
6. **Phase 6** - Code quality review (1 hour)

**Total Estimated Time**: ~5.5 hours

---

## Success Criteria

- [ ] All 6 commands documented in README
- [ ] CHANGELOG updated with new features
- [ ] `waft info` bug fixed
- [ ] Test suite exists with >80% coverage
- [ ] All commands work end-to-end
- [ ] Error messages are helpful and actionable
- [ ] Code passes linting and formatting checks

---

## Notes

- Tests should use temporary directories to avoid polluting filesystem
- Mock subprocess calls to avoid requiring actual uv installation in tests
- Keep tests fast and isolated
- Documentation should include examples for each command
- Consider adding a "Troubleshooting" section to README

---

## Next Steps After This Plan

1. Version bump to 0.0.2
2. Create release notes
3. Tag release
4. Consider additional features based on testing feedback

