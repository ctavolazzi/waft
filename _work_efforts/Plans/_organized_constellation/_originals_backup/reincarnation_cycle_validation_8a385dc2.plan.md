---
name: Reincarnation Cycle Validation
overview: Create a gamified validation system where Claude (The Mutator) can discover and test the reincarnation cycle through game commands, earning Scint points for successful validation of the soul_id continuity, lifetimes increment, and memory inheritance mechanics.
todos: []
---

# Reincarnation Cycle Validation Plan

## Objective
Validate the newly implemented `reincarnate_being()` function by having Claude (The Mutator) discover and test it through gamified commands, earning Scint points for successful validation.

## Core Mechanics to Validate

### 1. Soul ID Continuity
- **Test**: Verify that `soul_id` persists across reincarnations
- **Expected**: New Being has same `soul_id` as archived parent
- **Scint Value**: 5 points

### 2. Lifetimes Increment
- **Test**: Verify that `lifetimes` increments correctly (parent + 1)
- **Expected**: If parent had `lifetimes=1`, new Being has `lifetimes=2`
- **Scint Value**: 5 points

### 3. Ancestral Chain Inheritance
- **Test**: Verify that ancestral chain includes parent's lifetimes
- **Expected**: Ancestral chain properly tracks lineage
- **Scint Value**: 3 points

### 4. Memory Continuity (Optional)
- **Test**: Verify memory inheritance when `memory_continuity` is specified
- **Expected**: Percentage of memories carried over based on continuity value
- **Scint Value**: 2 points

## Implementation Strategy

### Phase 1: Game Command Structure
Create a validation script that provides game-like commands for Claude to use:

**File**: `examples/test_reincarnation_cycle.py`

**Commands Available**:
1. `spawn_being` - Create a new Being (lifetime 1)
2. `run_tavern` - Run Being through tavern scenario to generate memories
3. `archive_being` - Archive (kill) the Being
4. `reincarnate` - Reincarnate the archived Being
5. `verify_soul` - Verify soul_id continuity
6. `verify_lifetimes` - Verify lifetimes increment
7. `verify_memories` - Verify memory inheritance (if applicable)

### Phase 2: Integration with Tavern Scenario
Modify `examples/tavern_scenario_evolved.py` to support:
- Being state persistence (save after scenario)
- Being loading (load for reincarnation test)
- Memory tracking (count memories before/after)

### Phase 3: Validation Report
Create a validation report that logs:
- Test results (pass/fail)
- Scint points earned
- Findings and observations
- Any "Reality Fractures" discovered

## File Structure

```
examples/
├── test_reincarnation_cycle.py          # NEW: Game command interface
├── tavern_scenario_evolved.py           # MODIFY: Add save/load support
└── reincarnation_validation_report.md   # NEW: Validation results
```

## Validation Workflow

1. **Spawn Phase**: Create Being with `lifetimes=1`, record `soul_id`
2. **Experience Phase**: Run through tavern scenario, generate memories/skills
3. **Death Phase**: Archive Being, verify state is ARCHIVED
4. **Rebirth Phase**: Call `reincarnate_being()`, create new Being
5. **Verification Phase**: 
   - Check `soul_id` matches parent
   - Check `lifetimes == 2` (parent + 1)
   - Check ancestral chain includes parent
   - Check memory inheritance (if continuity specified)

## Success Criteria

- ✅ `soul_id` persists across reincarnations
- ✅ `lifetimes` increments correctly (parent + 1)
- ✅ Ancestral chain properly tracks lineage
- ✅ Memory continuity works when specified
- ✅ Being can be archived and reincarnated multiple times
- ✅ Validation report generated with Scint points

## Integration Points

- **BeingSystem**: Uses `reincarnate_being()` method
- **Tavern Scenario**: Provides experience/memories for Being
- **Gamified Laboratory**: Claude earns Scint for discoveries
- **Work Efforts**: Log findings in appropriate work effort

## Next Steps After Validation

1. Document findings in work effort
2. Create integration test suite based on validation
3. Update RFC_002_REINCARNATION.md with validation results
4. Consider multi-lifetime scenarios (Being with 10+ lifetimes)