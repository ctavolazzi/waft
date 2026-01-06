# Engineering Command Creation

**Date**: 2026-01-06
**File**: `.cursor/commands/engineering.md`

## Purpose

Created a comprehensive command that orchestrates the entire development workflow from start to finish:
1. Spin-up (orientation)
2. Explore (deep understanding)
3. Draft plan (initial planning)
4. Critique plan (review and refine)
5. Finalize plan (lock in)
6. Begin (implementation)

## Key Features

### Complete Workflow Orchestration
- Runs all 6 phases sequentially
- Each phase has clear goals, steps, and outputs
- Tool usage specified for each phase

### Active Tool Integration
- **Empirica**: Sessions, findings, unknowns, preflight/postflight
- **_pyrite**: Documentation throughout all phases
- **GitHub MCP**: Extensive usage, especially in Phase 2
- **Work Efforts MCP**: Create/update work efforts and tickets
- **Waft Commands**: info, verify, stats, finding log, unknown log
- **Git**: Status checks, history review, frequent commits

### Phase Details

**Phase 1: Spin-Up**
- Environment checks (date, disk, MCP health)
- Git status
- Active work efforts
- GitHub state (commits, issues, PRs, branches)
- Project state (waft commands)

**Phase 2: Explore**
- Empirica session creation
- GitHub exploration (CRITICAL - do first)
- 10 exploration areas (structure, architecture, dependencies, patterns, etc.)
- Comprehensive documentation in `_pyrite/active/`
- Finding/unknown logging

**Phase 3: Draft Plan**
- Review exploration findings
- Break down work into tasks
- Create work effort and tickets
- Document plan

**Phase 4: Critique Plan**
- Review for completeness
- Validate assumptions
- Identify gaps
- Refine approach

**Phase 5: Finalize Plan**
- Final review
- Update work effort
- Finalize tickets
- Commit planning work

**Phase 6: Begin**
- Preflight assessment
- Implementation workflow:
  - Incremental changes
  - Frequent verification
  - Finding/unknown logging
  - Frequent commits
  - Ticket updates
- Postflight assessment
- Final summary

### Execution Checklist
- Comprehensive checklist for each phase
- Ensures nothing is missed
- Tool usage verification

### Output Format
- Phase summaries
- Key findings
- Next steps
- Tool usage tracking
- Documentation locations

## Result

A complete orchestration command that:
- Ensures thorough understanding before implementation
- Uses all available tools actively
- Documents everything incrementally
- Plans carefully before coding
- Tracks progress continuously

This makes the entire development workflow systematic, tool-using, and well-documented.

