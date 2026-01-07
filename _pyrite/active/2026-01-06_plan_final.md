# Final Plan: Complete Tavern Keeper System

**Date**: 2026-01-06
**Status**: Final - Ready for Execution
**Objective**: Complete remaining Tavern Keeper work and prepare for merge to main

## Executive Summary

The Tavern Keeper system is **95% complete**. All core functionality is implemented, tested, and integrated. Remaining work is primarily documentation updates, testing, verification, and polish.

**Priority**: High (feature branch ready for merge)

## Task Breakdown

### Task 1: Update SPEC Document

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

### Task 2: Test Dashboard

**Objective**: Verify dashboard works in real terminal

**Steps**:
1. Run `waft dashboard` command
2. Verify layout renders correctly
3. Verify real-time updates work (4Hz refresh)
4. Test keyboard interrupt (Q to quit)
5. Check for any rendering issues

**Acceptance Criteria**:
- [ ] Dashboard launches without errors
- [ ] Layout renders correctly
- [ ] Real-time updates work
- [ ] Keyboard interrupt works
- [ ] No rendering artifacts

**Commands**:
- `waft dashboard`

---

### Task 3: Test Command Hooks

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

### Task 3a: Test CLI Integration

**Objective**: Verify end-to-end CLI command integration

**Steps**:
1. Test commands in real project context
2. Verify output includes narratives
3. Check adventure journal updates
4. Verify character stats update correctly
5. Test with/without Tracery library

**Acceptance Criteria**:
- [ ] Commands work in real project
- [ ] Narratives appear in output
- [ ] Journal updates correctly
- [ ] Stats update correctly
- [ ] Fallback works without Tracery

---

### Task 4: Review Narrative Grammars

**Objective**: Ensure narrative quality and theme consistency

**Steps**:
1. Review all grammar definitions
2. Generate sample narratives
3. Check for theme consistency (Constructivist Sci-Fi)
4. Verify placeholder replacement works
5. Check for any awkward phrasing

**Files**:
- `src/waft/core/tavern_keeper/grammars.py`

**Acceptance Criteria**:
- [ ] All grammars generate valid narratives
- [ ] Theme is consistent
- [ ] Placeholders replaced correctly
- [ ] No awkward phrasing
- [ ] Narratives are engaging

---

### Task 5: Verify XP Balance

**Objective**: Ensure XP rewards are balanced

**Steps**:
1. Review XP values in command_map
2. Calculate level progression rates
3. Verify multipliers are appropriate
4. Check for any imbalances

**Balance Criteria**:
- Level 2 achievable in ~10-15 commands
- Level 5 achievable in ~50-75 commands
- Critical successes provide meaningful boost
- Failures don't feel punitive

**Files**:
- `src/waft/core/tavern_keeper/keeper.py` (command_map)

**Acceptance Criteria**:
- [ ] XP values are reasonable
- [ ] Level progression is balanced
- [ ] Multipliers are appropriate
- [ ] No obvious imbalances

---

### Task 5a: Verify Git Merge Driver

**Objective**: Ensure git merge driver works correctly

**Steps**:
1. Check if `.gitattributes` exists
2. Verify merge driver script exists
3. Test merge scenario (if possible)
4. Verify configuration

**Acceptance Criteria**:
- [ ] `.gitattributes` configured
- [ ] Merge driver script exists
- [ ] Configuration verified

**Files**:
- `.gitattributes`
- `scripts/json_merge_driver.py`

---

### Task 5b: Verify Backward Compatibility

**Objective**: Ensure no breaking changes

**Steps**:
1. Review public API changes
2. Check for removed/changed functions
3. Verify migration path exists
4. Document any breaking changes

**Acceptance Criteria**:
- [ ] No breaking changes (or documented)
- [ ] Migration path exists
- [ ] Public API stable

---

### Task 6: Run Full Test Suite

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

### Task 7: Update CHANGELOG

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

### Task 7a: Update README

**Objective**: Document Tavern Keeper in README

**Steps**:
1. Add Tavern Keeper section
2. Document key commands
3. Add examples
4. Link to SPEC document

**Acceptance Criteria**:
- [ ] Tavern Keeper section added
- [ ] Key commands documented
- [ ] Examples included
- [ ] Links to SPEC

**Files**:
- `README.md`

---

### Task 8: Prepare for Merge

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

## Task Order & Dependencies

1. **Task 1** (Update SPEC) - Independent
2. **Task 2** (Test Dashboard) - Independent
3. **Task 3** (Test Hooks) - Independent
4. **Task 3a** (Test CLI Integration) - After Task 3
5. **Task 4** (Review Grammars) - Independent
6. **Task 5** (Verify XP) - Independent
7. **Task 5a** (Verify Merge Driver) - Independent
8. **Task 5b** (Verify Compatibility) - Independent
9. **Task 6** (Run Tests) - After Tasks 2-5b
10. **Task 7** (Update CHANGELOG) - After all testing
11. **Task 7a** (Update README) - After Task 7
12. **Task 8** (Prepare Merge) - Last

## Success Criteria

1. ✅ SPEC document accurately reflects implementation
2. ✅ Dashboard works correctly in terminal
3. ✅ All command hooks verified working
4. ✅ CLI integration verified end-to-end
5. ✅ Narrative grammars reviewed and refined
6. ✅ XP balance verified with specific criteria
7. ✅ Git merge driver verified
8. ✅ Backward compatibility verified
9. ✅ All tests pass
10. ✅ CHANGELOG updated
11. ✅ README updated
12. ✅ Branch ready for merge

## Risks & Mitigation

1. **Dashboard rendering issues**
   - Risk: Terminal compatibility issues
   - Mitigation: Test in multiple terminals

2. **Command hook failures**
   - Risk: Some hooks may not work correctly
   - Mitigation: Test each command individually, batch similar commands

3. **XP imbalance**
   - Risk: Progression too fast/slow
   - Mitigation: Use specific criteria, adjust if needed

4. **Breaking changes**
   - Risk: May have introduced breaking changes
   - Mitigation: Explicit compatibility check (Task 5b)

## Next Steps After Completion

1. Merge to main branch
2. Create release tag (v0.0.3?)
3. Gather user feedback
4. Iterate based on feedback

---

**Status**: ✅ **FINAL - READY FOR EXECUTION**

This plan has been critiqued, refined, and finalized. All tasks are clearly defined with acceptance criteria. Ready to begin implementation.

