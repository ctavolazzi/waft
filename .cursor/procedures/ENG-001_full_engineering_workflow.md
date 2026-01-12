# Procedure: Full Engineering Workflow

**Shortcode**: ENG-001  
**Category**: Engineering  
**Created**: 2026-01-10  
**Updated**: 2026-01-10  
**Status**: Active  
**Aliases**: `/engineering`, `/eng`

---

## Description

Complete engineering workflow from orientation through implementation. Executes all phases: spin-up, explore, draft plan, critique plan, finalize plan, and begin implementation.

---

## Use When

- Starting a new feature or significant change
- Need thorough understanding before implementation
- Want systematic approach with planning
- Need comprehensive workflow

---

## Prerequisites

- Project is a git repository
- Working directory is project root
- MCP servers available (work-efforts, docs-maintainer, etc.)
- Waft framework initialized (if applicable)

---

## Steps

### Phase 1: Spin-Up (Orientation)
**Execute**: `/spin-up`

**Actions**:
1. Date check
2. Disk space check
3. MCP health check
4. Git status check
5. Active work efforts listed
6. Recent history read
7. GitHub state checked
8. Project state checked

**Output**: Orientation summary with current state

**Documentation**: `_pyrite/active/YYYY-MM-DD_engineering_spinup.md`

---

### Phase 2: Explore (Deep Understanding)
**Execute**: `/explore` or manual exploration

**Actions**:
1. Create Empirica session (if initialized)
2. GitHub exploration (commits, issues, PRs, branches, releases, tags, code search)
3. Project structure analysis
4. Architecture analysis
5. Dependency analysis
6. Pattern discovery
7. Functionality mapping
8. Documentation review
9. Testing analysis
10. Integration points identification

**Output**: Comprehensive exploration report

**Documentation**: `_pyrite/active/YYYY-MM-DD_exploration_*.md` files

**Log**: Findings via `waft finding log`, unknowns via `waft unknown log`

---

### Phase 3: Draft Plan
**Actions**:
1. Review exploration findings
2. Identify requirements
3. Break down work into tasks
4. Estimate complexity
5. Identify dependencies
6. Create work effort (if needed)
7. Create tickets
8. Document plan

**Output**: Initial plan with objectives, tasks, dependencies

**Documentation**: `_pyrite/active/YYYY-MM-DD_plan_draft.md` or work effort index

---

### Phase 4: Critique Plan
**Actions**:
1. Review plan for completeness
2. Validate assumptions
3. Identify gaps
4. Check feasibility
5. Review dependencies
6. Consider alternatives
7. Get feedback (if applicable)
8. Refine plan
9. Update documentation

**Output**: Refined plan with addressed gaps

**Documentation**: Update plan document with critique notes

---

### Phase 5: Finalize Plan
**Actions**:
1. Final review
2. Update work effort
3. Update tickets
4. Document final plan
5. Update devlog
6. Commit planning work

**Output**: Finalized plan ready for implementation

**Documentation**: Final plan in `_work_efforts/` or `_pyrite/active/`

---

### Phase 6: Begin (Implementation)
**Actions**:
1. Preflight assessment (if Empirica)
2. Start first ticket
3. Implementation workflow:
   - Make changes incrementally
   - Verify after each change
   - Log findings and unknowns
   - Check stats
   - Commit frequently
   - Update tickets
4. Complete ticket
5. Repeat for each ticket
6. Complete work effort
7. Postflight assessment (if Empirica)
8. Update devlog
9. Final summary

**Output**: Implemented feature with all tickets completed

**Documentation**: All work in `_pyrite/active/` and work effort tickets

---

## Expected Output

After completion:
- ✅ Complete understanding of codebase
- ✅ Comprehensive plan with tasks and dependencies
- ✅ Work effort created with tickets
- ✅ Implementation started or completed
- ✅ All findings documented
- ✅ Devlog updated

---

## Notes

- Use all available tools actively (Empirica, _pyrite, GitHub MCP, work-efforts, waft)
- Document findings throughout each phase
- Log findings and unknowns via waft commands
- Commit frequently during implementation
- Update tickets as work progresses

---

## Related Procedures

- **ORC-001**: Comprehensive Orchestration (similar but includes hypothesis/verification)
- **ANL-001**: Data Analysis Workflow (focused on analysis)
- **CMD-001**: Create New Command (for creating commands)

---

**Procedure Created**: 2026-01-10  
**Last Updated**: 2026-01-10
