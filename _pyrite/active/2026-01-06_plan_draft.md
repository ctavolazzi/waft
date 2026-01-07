# Draft Plan: Complete Tavern Keeper System

**Date**: 2026-01-06
**Status**: Draft
**Objective**: Complete remaining Tavern Keeper work and prepare for merge to main

## Executive Summary

The Tavern Keeper system is **95% complete**. All core functionality is implemented, tested, and integrated. Remaining work is primarily documentation updates, testing, and polish.

## Current State Assessment

### ✅ Complete (95%)

1. **Core Implementation**
   - TavernKeeper class (725 lines) - Complete
   - Character system - Complete
   - Dice rolling - Complete
   - Narrative generation - Complete (with fallback)
   - Status effects - Complete
   - Adventure journal - Complete
   - Command hooks - Complete (10/10 commands)

2. **Supporting Systems**
   - Narrator class - Complete
   - Grammar definitions - Complete
   - AI helper utilities - Complete
   - Dashboard UI - Complete (432 lines)

3. **CLI Integration**
   - All command hooks integrated - Complete
   - All Tavern Keeper commands exist - Complete (7/7)

4. **Testing**
   - Comprehensive test suite - Complete (15 tests)
   - All tests passing - Complete

5. **Data Management**
   - TinyDB integration - Complete
   - JSON fallback - Complete
   - Migration from gamification.json - Complete
   - Git merge driver - Complete

### 🚧 Remaining Work (5%)

1. **Documentation**
   - Update SPEC document to reflect actual status
   - Verify all checkboxes match reality

2. **Testing & Verification**
   - Test dashboard in real terminal environment
   - Verify all command hooks work correctly
   - Test narrative generation with/without Tracery

3. **Polish & Refinement**
   - Review narrative grammars for quality
   - Verify XP balance is appropriate
   - Check for any edge cases

4. **Merge Preparation**
   - Ensure all tests pass
   - Update CHANGELOG
   - Prepare merge commit message

## Task Breakdown

### Task 1: Update SPEC Document (30 min)

**Objective**: Align SPEC with actual implementation status

**Steps**:
1. Review SPEC-TAVERNKEEPER.md
2. Update all checkboxes to reflect completed work
3. Update "Implementation Status" section
4. Update "Next Steps" section
5. Verify accuracy

**Acceptance Criteria**:
- [ ] All completed items marked as ✅
- [ ] Implementation Status section accurate
- [ ] Next Steps section updated
- [ ] No false "incomplete" claims

**Files**:
- `SPEC-TAVERNKEEPER.md`

---

### Task 2: Test Dashboard (15 min)

**Objective**: Verify dashboard works in real terminal

**Steps**:
1. Run `waft dashboard` command
2. Verify layout renders correctly
3. Verify real-time updates work
4. Test keyboard interrupt (Q to quit)
5. Check for any rendering issues

**Acceptance Criteria**:
- [ ] Dashboard launches without errors
- [ ] Layout renders correctly
- [ ] Real-time updates work (4Hz refresh)
- [ ] Keyboard interrupt works
- [ ] No rendering artifacts

**Commands**:
- `waft dashboard`

---

### Task 3: Test Command Hooks (20 min)

**Objective**: Verify all command hooks work correctly

**Steps**:
1. Test each command with TavernKeeper hook
2. Verify dice rolls occur
3. Verify narratives generate
4. Verify rewards are awarded
5. Verify adventure journal entries created

**Commands to Test**:
- `waft new` (character creation)
- `waft verify` (constitution save)
- `waft init` (ritual casting)
- `waft info` (perception check)
- `waft sync` (resource management)
- `waft add <package>` (acquisition)
- `waft finding log` (discovery)
- `waft assess` (wisdom save)
- `waft check` (safety gate)
- `waft goal create` (quest creation)

**Acceptance Criteria**:
- [ ] All commands trigger hooks
- [ ] Dice rolls work correctly
- [ ] Narratives generate
- [ ] Rewards awarded correctly
- [ ] Journal entries created

---

### Task 4: Review Narrative Grammars (20 min)

**Objective**: Ensure narrative quality and theme consistency

**Steps**:
1. Review all grammar definitions
2. Generate sample narratives
3. Check for theme consistency
4. Verify placeholder replacement works
5. Check for any awkward phrasing

**Files**:
- `src/waft/core/tavern_keeper/grammars.py`

**Acceptance Criteria**:
- [ ] All grammars generate valid narratives
- [ ] Theme is consistent (Constructivist Sci-Fi)
- [ ] Placeholders replaced correctly
- [ ] No awkward phrasing
- [ ] Narratives are engaging

---

### Task 5: Verify XP Balance (15 min)

**Objective**: Ensure XP rewards are balanced

**Steps**:
1. Review XP values in command_map
2. Calculate level progression rates
3. Verify multipliers are appropriate
4. Check for any imbalances

**Files**:
- `src/waft/core/tavern_keeper/keeper.py` (command_map)

**Acceptance Criteria**:
- [ ] XP values are reasonable
- [ ] Level progression is balanced
- [ ] Multipliers are appropriate
- [ ] No obvious imbalances

---

### Task 6: Run Full Test Suite (10 min)

**Objective**: Ensure all tests pass

**Steps**:
1. Run pytest on test_tavern_keeper.py
2. Verify all tests pass
3. Check for any warnings
4. Verify coverage is adequate

**Commands**:
- `pytest tests/test_tavern_keeper.py -v`

**Acceptance Criteria**:
- [ ] All tests pass
- [ ] No warnings
- [ ] Coverage is adequate

---

### Task 7: Update CHANGELOG (15 min)

**Objective**: Document Tavern Keeper feature

**Steps**:
1. Add Tavern Keeper section to CHANGELOG
2. List all features
3. Document breaking changes (if any)
4. Add migration notes

**Files**:
- `CHANGELOG.md`

**Acceptance Criteria**:
- [ ] Tavern Keeper features documented
- [ ] Breaking changes noted
- [ ] Migration notes included

---

### Task 8: Prepare for Merge (10 min)

**Objective**: Prepare branch for merge to main

**Steps**:
1. Verify all changes committed
2. Create merge commit message
3. Review diff summary
4. Ensure branch is up to date

**Acceptance Criteria**:
- [ ] All changes committed
- [ ] Merge message prepared
- [ ] Branch ready for merge

---

## Dependencies

- Task 1 (Update SPEC) → Can be done independently
- Task 2 (Test Dashboard) → Can be done independently
- Task 3 (Test Hooks) → Can be done independently
- Task 4 (Review Grammars) → Can be done independently
- Task 5 (Verify XP) → Can be done independently
- Task 6 (Run Tests) → Should be done after Tasks 2-5
- Task 7 (Update CHANGELOG) → Should be done after all testing
- Task 8 (Prepare Merge) → Should be done last

## Success Criteria

1. ✅ SPEC document accurately reflects implementation
2. ✅ Dashboard works correctly in terminal
3. ✅ All command hooks verified working
4. ✅ Narrative grammars reviewed and refined
5. ✅ XP balance verified
6. ✅ All tests pass
7. ✅ CHANGELOG updated
8. ✅ Branch ready for merge

## Risks & Mitigation

1. **Dashboard rendering issues**
   - Risk: Terminal compatibility issues
   - Mitigation: Test in multiple terminals

2. **Command hook failures**
   - Risk: Some hooks may not work correctly
   - Mitigation: Test each command individually

3. **XP imbalance**
   - Risk: Progression too fast/slow
   - Mitigation: Review and adjust if needed

## Next Steps After Completion

1. Merge to main branch
2. Create release tag (v0.0.3?)
3. Update README with Tavern Keeper docs
4. Consider user feedback

