# Waft Framework Expansion Summary

**Date**: 2026-01-04
**Status**: Completed

## Overview

Expanded the waft framework with new CLI commands, enhanced managers, and additional templates.

## New Features Added

### 1. New CLI Commands

#### `waft sync`
- Syncs project dependencies using `uv sync`
- Usage: `waft sync [--path PATH]`

#### `waft add <package>`
- Adds a dependency to the project using `uv add`
- Usage: `waft add pytest --dev` (dev flag for future enhancement)
- Usage: `waft add "pytest>=7.0.0"`

#### `waft init`
- Initializes Waft structure in an existing project
- Creates `_pyrite` structure and writes templates
- Does NOT run `uv init` (assumes project already exists)
- Usage: `waft init [--path PATH]`

#### `waft info`
- Shows comprehensive project information
- Displays: project path, name, version, `_pyrite` status, `uv.lock` status, templates
- Usage: `waft info [--path PATH]`

### 2. Enhanced MemoryManager

Added utility methods:
- `get_active_files()` - Get all files in `_pyrite/active/`
- `get_backlog_files()` - Get all files in `_pyrite/backlog/`
- `get_standards_files()` - Get all files in `_pyrite/standards/`

### 3. Enhanced SubstrateManager

Added utility methods:
- `get_project_info()` - Parse and extract project name/version from `pyproject.toml`
  - Uses regex fallback if TOML parsing libraries unavailable
  - Returns dict with `name` and `version` keys

### 4. Additional Templates

#### `.gitignore`
- Comprehensive Python `.gitignore` template
- Includes: `__pycache__`, virtual environments, IDEs, testing artifacts, `uv.lock`

#### `README.md`
- Project README template
- Auto-detects project name from `pyproject.toml`
- Includes Quick Start, Project Structure, Development commands
- References Waft framework

## Files Modified

1. `src/waft/main.py`
   - Added 4 new CLI commands: `sync`, `add`, `init`, `info`
   - Enhanced error handling and user feedback

2. `src/waft/core/memory.py`
   - Added 3 utility methods for file management

3. `src/waft/core/substrate.py`
   - Added `get_project_info()` method

4. `src/waft/templates/__init__.py`
   - Added `write_gitignore()` method
   - Added `write_readme()` method
   - Updated `write_all()` to include new templates

## Testing

- ✅ All new commands appear in `waft --help`
- ✅ `waft info` command works and displays project information
- ✅ No linting errors
- ✅ Tool reinstalled successfully

## Next Steps (Future Enhancements)

1. **Testing Infrastructure**
   - Add pytest test suite
   - Integration tests for CLI commands
   - Unit tests for managers

2. **Additional Commands**
   - `waft migrate` - Migrate existing projects to Waft structure
   - `waft update` - Update Waft templates in existing projects
   - `waft remove <package>` - Remove dependencies

3. **Enhanced Templates**
   - Pre-commit hooks template
   - Dockerfile template
   - More CI/CD workflow options

4. **Better Error Handling**
   - More descriptive error messages
   - Validation of inputs
   - Graceful degradation when dependencies missing

## Command Reference

```bash
# Create new project
waft new my_project

# Initialize in existing project
waft init

# Verify structure
waft verify

# Sync dependencies
waft sync

# Add dependency
waft add pytest

# Show project info
waft info
```

