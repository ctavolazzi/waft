# Goal: Implement Run-It Workflow Findings

**Status**: Active  
**Created**: 2026-01-14  
**Updated**: 2026-01-14

---

## Objective

Implement the HIGH priority findings from the Run-It workflow execution:
1. Centralize debug logging (create utility)
2. Add debug log configuration
3. Audit subprocess calls (MEDIUM priority)

**Focus**: Effort cost and will to act, not time estimates

---

## Steps

1. [ ] Create `src/waft/utils/debug_log.py` utility
   - Centralize debug logging functionality
   - Use relative paths (not hardcoded absolute paths)
   - Support configuration (enable/disable)

2. [ ] Replace hardcoded debug logging in `document_builder.py`
   - Use new debug_log utility
   - Remove hardcoded path: `/Users/ctavolazzi/Code/active/waft/.cursor/debug.log`

3. [ ] Replace hardcoded debug logging in `golden_triangle.py`
   - Use new debug_log utility
   - Remove hardcoded path

4. [ ] Add debug log configuration
   - Add configuration option to enable/disable debug logging
   - Add log rotation support
   - Document configuration

5. [ ] Audit subprocess calls (MEDIUM priority)
   - Search codebase for all `subprocess` calls
   - Verify all use `shell=False`
   - Validate all inputs are sanitized
   - Document findings

---

## Progress

- **Completed**: 0/5 steps
- **Current**: Not started
- **Next**: Create `src/waft/utils/debug_log.py` utility

---

## Notes

**From Run-It Workflow**:
- **Security**: Strong overall, debug logging is main issue
- **Effort Cost**: Moderate (create utility, refactor 2 files)
- **Will to Act**: High (clear benefit, actionable)
- **Value**: High (reduces technical debt, improves portability)

**Decision**: Option A from Phase 13 - Implement HIGH priority items now

**Effort/Will Framing**: 
- Knowledge (knowing) requires effort
- Acting on knowledge requires will
- Being system tracks energy (effort capacity) and will_to_live (will to act)
- This is the real currency, not time

---

## Related Work

- **Workflow**: Run-It workflow execution (15/15 phases complete)
- **Critique**: `_work_efforts/CRITIQUE_2026-01-14_161149_run-it_workflow.md`
- **Decision**: `_pyrite/active/2026-01-14_run-it_decide_phase.md`

---

**Goal Created**: Run-It workflow findings implementation
