# Probe System - Standalone Extraction Plan

## Overview

The Probe system is designed to grow within WAFT and eventually be extracted into its own standalone GitHub repository. This document outlines the plan and current status.

## Current Status

✅ **Standalone Structure Created**: The probe system exists in `_standalone_tools/probe/` with all necessary files for a standalone package.

✅ **Self-Contained**: No dependencies on WAFT-specific code - only uses standard library and `requests`.

✅ **Package Ready**: Includes `pyproject.toml`, `README.md`, `LICENSE`, and proper package structure.

## Directory Structure

```
_standalone_tools/probe/
├── README.md                 # Main documentation
├── LICENSE                   # MIT License
├── pyproject.toml           # Package configuration
├── .gitignore              # Git ignore rules
├── EXTRACTION_GUIDE.md     # Step-by-step extraction guide
├── STANDALONE_PLAN.md      # This file
├── src/
│   └── probe/
│       ├── __init__.py     # Package exports
│       └── probe.py         # Main probe code
└── examples/
    └── example.py           # Usage example
```

## Design Principles

### 1. Minimal Dependencies
- Only requires `requests` (standard HTTP library)
- No WAFT-specific imports
- Uses only Python standard library otherwise

### 2. Clean API
- Simple, intuitive interface
- Well-documented
- Easy to extend

### 3. Self-Contained
- All code in one package
- No external configuration needed
- Works out of the box

### 4. Extensible
- Base `Probe` class for custom probes
- `ProbeCollector` for managing multiple probes
- Easy to add new probe types

## Growth Path

### Phase 1: Current (Within WAFT)
- ✅ Core functionality implemented
- ✅ Used within WAFT project
- ✅ Standalone structure prepared
- ⏳ Tests to be added

### Phase 2: Extraction Ready
- [ ] Add comprehensive tests
- [ ] Add CLI interface (optional)
- [ ] Add more probe types (DatabaseProbe, etc.)
- [ ] Improve documentation
- [ ] Add CI/CD setup

### Phase 3: Standalone Release
- [ ] Extract to GitHub repo
- [ ] Publish to PyPI
- [ ] Add version tags
- [ ] Set up release process

### Phase 4: Independent Development
- [ ] Accept contributions
- [ ] Add features independently
- [ ] Maintain separate from WAFT
- [ ] WAFT can use as dependency

## Integration with WAFT

Currently, WAFT uses the probe system from `src/waft/core/probe.py`. This is fine for now, but when ready to extract:

### Option A: Keep Both
- Maintain probe in WAFT for internal use
- Also maintain standalone version
- Sync changes as needed

### Option B: Use as Dependency
- Extract to standalone repo
- Publish to PyPI
- WAFT imports from `probe` package instead of `waft.core.probe`

### Option C: Submodule
- Extract to standalone repo
- Add as git submodule in WAFT
- WAFT references the submodule

## Next Steps

1. **Add Tests** (Priority)
   - Create `tests/` directory
   - Add `test_probe.py` with unit tests
   - Add `test_integration.py` for integration tests

2. **Enhance Documentation**
   - Add API reference
   - Add more examples
   - Add contributing guide

3. **Add Features** (As needed)
   - More probe types
   - CLI interface
   - Web dashboard
   - Export formats (CSV, etc.)

4. **Prepare for Extraction**
   - Review EXTRACTION_GUIDE.md
   - Test standalone installation
   - Verify all dependencies

## File Locations

| Purpose | WAFT Location | Standalone Location |
|---------|--------------|---------------------|
| Main Code | `src/waft/core/probe.py` | `src/probe/probe.py` |
| Package Config | N/A | `pyproject.toml` |
| Documentation | `src/waft/core/PROBE_README.md` | `README.md` |
| Examples | `examples/probe_example.py` | `examples/example.py` |
| Extraction Guide | N/A | `EXTRACTION_GUIDE.md` |

## Version History

- **0.1.0** (Current): Initial standalone-ready version
  - Core probe functionality
  - HTTP, FileSystem, Service probes
  - Data collection and storage
  - Standalone structure

## Questions?

- See `EXTRACTION_GUIDE.md` for step-by-step extraction instructions
- See `README.md` for usage documentation
- See `examples/example.py` for code examples
