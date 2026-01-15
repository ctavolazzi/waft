---
name: Reincarnation Validation Framework
overview: Create a gamified validation framework (interactive + automated) to validate the reincarnation cycle functionality, including Soul ID continuity, lifetimes increment, ancestral chain inheritance, and memory continuity.
todos:
  - id: create_work_effort
    content: Create new work effort in _work_efforts/ for reincarnation validation using Johnny Decimal system
    status: pending
  - id: interactive_framework
    content: Create examples/test_reincarnation_cycle.py with gamified command interface and Scint point tracking
    status: pending
  - id: automated_tests
    content: Create tests/test_reincarnation_cycle.py with pytest-based test suite for all 4 core mechanics
    status: pending
  - id: enhance_tavern
    content: Add save_being_state() and load_being_state() functions to examples/tavern_scenario_evolved.py
    status: pending
  - id: report_generator
    content: Implement validation report generation (markdown + console output) in test_reincarnation_cycle.py
    status: pending
  - id: update_devlog
    content: Update _work_efforts/devlog.md with validation progress and results
    status: pending
---

# Reincarnation Cycle Validation Framework

## Overview

Create a comprehensive validation framework to test the `reincarnate_being()` functionality in the WAFT Being system. The framework will include both an interactive command-line game for exploration and automated tests for CI/CD.

## Core Mechanics to Validate

1. **Soul ID Continuity** (5 Scint points)

- Verify `soul_id` persists across reincarnations
- Dead Being and Reincarnated Being share the same `soul_id`

2. **Lifetimes Increment** (5 Scint points)

- Verify `lifetimes` increments correctly (parent + 1)
- Dead Being: lifetime 1 → Reincarnated Being: lifetime 2

3. **Ancestral Chain Inheritance** (3 Scint points)

- Verify `ancestral_chain` includes parent's lifetimes
- Parent Being ID included in new Being's chain

4. **Memory Continuity** (2 Scint points)

- Verify memory inheritance with `memory_continuity` parameter
- Percentage-based memory carryover works correctly

## Implementation Plan

### 1. Create Work Effort

- Create new work effort in `_work_efforts/` using Johnny Decimal system
- Document validation objectives and success criteria
- Link to RFC_002_REINCARNATION.md

### 2. Interactive Validation Framework (`examples/test_reincarnation_cycle.py`)

Create a gamified command-line interface with:

**Core Commands:**

- `spawn_being` - Create a new Being (lifetime 1)
- `run_tavern` - Run Being through tavern scenario to generate memories
- `save_being` - Save Being state to disk
- `load_being` - Load Being state from disk
- `archive_being` - Archive (kill) the Being
- `reincarnate` - Reincarnate the archived Being
- `verify_soul` - Verify soul_id continuity
- `verify_lifetimes` - Verify lifetimes increment
- `verify_ancestral_chain` - Verify ancestral chain inheritance
- `verify_memories` - Verify memory inheritance

**Features:**

- Rich console output with styled panels
- Scint point tracking system (15 total points)
- Detailed validation logging
- Automatic report generation (`reincarnation_validation_report.md`)
- Reality Fracture detection (for unexpected discoveries)

**Implementation Details:**

- Use `rich` library (already in dependencies)
- Integrate with `BeingSystem` for proper initialization
- Support `memory_continuity` parameter testing (0.0, 0.5, 1.0)
- Track validation results with timestamps

### 3. Automated Test Suite (`tests/test_reincarnation_cycle.py`)

Create pytest-based tests for CI/CD:

**Test Cases:**

- `test_soul_id_continuity` - Verify soul_id persists
- `test_lifetimes_increment` - Verify lifetimes increment
- `test_ancestral_chain_inheritance` - Verify chain extends
- `test_memory_continuity_50_percent` - Verify 50% memory carryover
- `test_memory_continuity_0_percent` - Verify no memory carryover
- `test_memory_continuity_100_percent` - Verify full memory carryover
- `test_reincarnate_archived_only` - Verify only ARCHIVED beings can reincarnate
- `test_multi_lifetime_reincarnation` - Test 3+ lifetimes

**Test Structure:**

- Use pytest fixtures for BeingSystem setup
- Create temporary test beings
- Clean up after tests
- Assert on all validation criteria

### 4. Enhance Tavern Scenario (`examples/tavern_scenario_evolved.py`)

Add save/load functionality:

**New Functions:**

- `save_being_state(being, filepath)` - Save Being to disk
- `load_being_state(filepath, being_system)` - Load Being from disk

**Integration:**

- Use `BeingSystem._save_being()` and `BeingSystem._load_being()`
- Support reincarnation testing workflows
- Maintain compatibility with existing tavern scenario

### 5. Validation Report Generator

Create report generation functionality:

**Report Contents:**

- Test results summary (passed/failed)
- Detailed validation data for each test
- Timestamps for all validations
- Scint points earned
- Summary and conclusions
- Recommendations for improvements

**Format:**

- Markdown format (`reincarnation_validation_report.md`)
- Rich console output during execution
- JSON export option for programmatic access

## Files to Create/Modify

### New Files:

1. `examples/test_reincarnation_cycle.py` - Interactive validation framework
2. `tests/test_reincarnation_cycle.py` - Automated test suite
3. `examples/reincarnation_validation_report.md` - Generated validation report

### Modified Files:

1. `examples/tavern_scenario_evolved.py` - Add save/load functions
2. `_work_efforts/devlog.md` - Update with validation progress

## Technical Considerations

### Dependencies

- `rich` - Already in `pyproject.toml` (>=13.0.0)
- `pytest` - Already in dev dependencies
- No new dependencies required

### BeingSystem Integration

- Use `BeingSystem.reincarnate_being()` method
- Properly handle `ARCHIVED` state requirement
- Support `purchase_order` with `memory_continuity` parameter
- Handle `soul_id` creation and inheritance

### Error Handling

- Validate Being state before reincarnation
- Handle missing KarmaMerchant gracefully
- Provide clear error messages for validation failures

### Test Data Management

- Use temporary test beings (clean up after)
- Avoid polluting production Being storage
- Support multiple concurrent test runs

## Success Criteria

- [ ] All 4 core mechanics validated (15 Scint points)
- [ ] Interactive framework fully functional
- [ ] Automated tests pass (100% success rate)
- [ ] Validation report generated
- [ ] Tavern scenario supports save/load
- [ ] Work effort documented
- [ ] Devlog updated

## Next Steps After Validation

1. Integration with KarmaMerchant (if available)
2. Multi-lifetime scenario testing (10+ lifetimes)
3. Karma-based reincarnation testing
4. RFC documentation updates
5. CI/CD integration for automated tests