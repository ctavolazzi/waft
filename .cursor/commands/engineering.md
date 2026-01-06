# Engineering

**Complete workflow from orientation to implementation.**

Runs the entire development process from start to finish:
1. `spin-up` → Get oriented
2. `explore` → Understand structure
3. `draft plan` → Create initial plan
4. `critique plan` → Review and refine
5. `finalize plan` → Lock in the plan
6. `begin` → Start implementation

**Use when:** Starting a new feature, bug fix, or significant change that requires full understanding and planning.

---

## Purpose

This command orchestrates the complete development workflow, ensuring:
- **Thorough understanding** before implementation
- **Active tool usage** (Empirica, _pyrite, GitHub MCP, work-efforts)
- **Incremental documentation** throughout the process
- **Quality planning** before coding
- **Continuous tracking** of progress and learning

---

## Workflow Sequence

### Phase 1: Spin-Up (Orientation)

**Goal**: Get oriented to current state

**Steps**:
1. **Date check**: Run `date` - Ensure correct date/time
2. **Disk space**: Check available space
3. **MCP health**: Verify MCP servers are operational
4. **Git status**: Check for uncommitted changes
5. **Active work**: List active work efforts via `mcp_work-efforts_list_work_efforts`
6. **Recent history**: Read last 50 lines of `_work_efforts/devlog.md`
7. **GitHub state**: 
   - `mcp_github_get_me` - Get user context
   - `mcp_github_list_commits` - Recent commits (last 10)
   - `mcp_github_list_issues` - Open issues
   - `mcp_github_list_pull_requests` - Open PRs
8. **Project state**: 
   - `waft info` - Project information
   - `waft verify` - Structure health
   - `waft stats` - Gamification state

**Output**: 
- Environment status
- Active work efforts
- Recent changes
- Recommended next step

**Document**: Create `_pyrite/active/YYYY-MM-DD_engineering_spinup.md`

---

### Phase 2: Explore (Deep Understanding)

**Goal**: Understand codebase structure, architecture, and relationships

**Steps**:
1. **Empirica session**: Create exploration session
   ```bash
   waft session create --ai-id waft --type exploration
   ```

2. **GitHub exploration** (CRITICAL - Do First):
   - `mcp_github_get_me` - User context
   - `mcp_github_list_commits` - Evolution (last 20)
   - `mcp_github_list_issues` - Priorities
   - `mcp_github_list_pull_requests` - Pending work
   - `mcp_github_list_branches` - Branch structure
   - `mcp_github_get_latest_release` - Release history
   - `mcp_github_list_tags` - Version tags
   - `mcp_github_search_code` - Find patterns
   - `mcp_github_get_file_contents` - Read key files

3. **Project structure analysis**:
   - Map directory structure
   - Identify entry points
   - Find configuration files
   - Locate test directories
   - **Use**: `waft info`, `waft verify`, filesystem exploration
   - **Document**: `_pyrite/active/YYYY-MM-DD_exploration_structure.md`

4. **Architecture analysis**:
   - Identify core modules
   - Map component relationships
   - Understand data flow
   - Find integration points
   - **Use**: Semantic search, code reading
   - **Document**: `_pyrite/active/YYYY-MM-DD_exploration_architecture.md`
   - **Log**: `waft finding log "Identified core components: X, Y, Z" --impact 0.7`

5. **Dependency analysis**:
   - List external dependencies
   - Map internal dependencies
   - **Use**: `pyproject.toml`, `mcp_github_search_code`
   - **Log**: `waft finding log "Found X dependencies" --impact 0.6`

6. **Pattern discovery**:
   - Identify coding patterns
   - Find design patterns
   - Understand conventions
   - **Document**: `_pyrite/active/YYYY-MM-DD_exploration_patterns.md`
   - **Use MCP**: `mcp_memory_create_entities` for patterns

7. **Functionality mapping**:
   - Locate main features
   - Find critical paths
   - Map extension points
   - **Use**: `waft --help`, command exploration
   - **Use MCP**: `mcp_work-efforts_list_work_efforts`

8. **Documentation review**:
   - Read key docs
   - Check architecture docs
   - Find design decisions
   - **Use**: `mcp_docs-maintainer_search_docs`, `mcp_github_get_file_contents`

9. **Testing analysis**:
   - Understand test structure
   - Identify coverage areas
   - **Use**: `waft verify`, run tests
   - **Document**: Test findings

10. **Integration points**:
    - Find external integrations
    - Identify API boundaries
    - **Use**: `mcp_github_search_code`
    - **Document**: Integration map

**Output**: Comprehensive exploration report with:
- Project structure
- Architecture overview
- Dependencies
- Patterns & conventions
- Key functionality
- Integration points
- Testing & quality
- Documentation
- Insights & observations
- Questions & unknowns

**Document**: All findings in `_pyrite/active/YYYY-MM-DD_exploration_*.md` files

**Log**: Findings via `waft finding log`, unknowns via `waft unknown log`

---

### Phase 3: Draft Plan

**Goal**: Create initial plan based on understanding

**Steps**:
1. **Review exploration findings**: Consolidate all exploration documents
2. **Identify requirements**: What needs to be done?
3. **Break down work**: Create tasks/subtasks
4. **Estimate complexity**: Assess difficulty
5. **Identify dependencies**: What depends on what?
6. **Create work effort** (if needed):
   - `mcp_work-efforts_create_work_effort` - Create new work effort
   - Or update existing work effort
7. **Create tickets**:
   - `mcp_work-efforts_create_ticket` - Create tickets for each major task
8. **Document plan**: 
   - Create plan document in `_work_efforts/` or `_pyrite/active/`
   - Include: objectives, tasks, dependencies, success criteria

**Output**: Initial plan with:
- Objectives
- Task breakdown
- Dependencies
- Success criteria
- Estimated complexity

**Document**: `_pyrite/active/YYYY-MM-DD_plan_draft.md` or work effort index

**Log**: `waft finding log "Drafted plan: X tasks, Y complexity" --impact 0.7`

---

### Phase 4: Critique Plan

**Goal**: Review and refine the plan

**Steps**:
1. **Review plan**: Read the draft plan carefully
2. **Check completeness**: Are all requirements covered?
3. **Validate assumptions**: Are assumptions correct?
4. **Identify gaps**: What's missing?
5. **Check feasibility**: Is this realistic?
6. **Review dependencies**: Are dependencies correct?
7. **Consider alternatives**: Are there better approaches?
8. **Get feedback** (if applicable): Review with user or team
9. **Refine plan**: Update based on critique
10. **Update documentation**: Update plan document

**Output**: Refined plan with:
- Addressed gaps
- Validated assumptions
- Refined approach
- Updated dependencies

**Document**: Update plan document with critique notes

**Log**: `waft finding log "Critiqued plan: identified X gaps, refined Y approach" --impact 0.6`

---

### Phase 5: Finalize Plan

**Goal**: Lock in the final plan

**Steps**:
1. **Final review**: One last check of the plan
2. **Update work effort**: 
   - `mcp_work-efforts_update_work_effort` - Update status, add progress notes
3. **Update tickets**: Ensure all tickets are created and properly scoped
4. **Document final plan**: 
   - Final plan document
   - Include: final objectives, tasks, dependencies, timeline
5. **Update devlog**: Add entry about plan finalization
6. **Commit planning work**: 
   - `git add` planning documents
   - `git commit -m "docs: finalize plan for [feature]"`

**Output**: Finalized plan ready for implementation

**Document**: Final plan in `_work_efforts/` or `_pyrite/active/`

**Log**: `waft finding log "Finalized plan: ready for implementation" --impact 0.8`

---

### Phase 6: Begin (Implementation)

**Goal**: Start implementation

**Steps**:
1. **Preflight assessment** (if Empirica initialized):
   - Submit preflight with current knowledge state
2. **Start first ticket**:
   - `mcp_work-efforts_update_ticket` - Set status to "in_progress"
   - Create `_pyrite/active/YYYY-MM-DD_ticket_XXX.md`
3. **Implementation workflow**:
   - Make changes incrementally
   - Verify after each change: `waft verify`
   - Log findings: `waft finding log "Discovered X" --impact 0.6`
   - Log unknowns: `waft unknown log "Need to investigate Y"`
   - Check stats: `waft stats`
   - Commit frequently: `git commit -m "feat: [description] (TKT-XXX)"`
   - Update ticket: `mcp_work-efforts_update_ticket` with commit hash
4. **Complete ticket**:
   - Verify: `waft verify`, run tests
   - Update ticket: `mcp_work-efforts_update_ticket` with status="completed"
   - Document: Update `_pyrite/active/` file
   - Commit: Final commit for ticket
5. **Repeat** for each ticket
6. **Complete work effort**:
   - Update work effort: `mcp_work-efforts_update_work_effort` with status="completed"
   - Postflight assessment (if Empirica initialized)
   - Update devlog
   - Final summary

**Output**: Implemented feature with:
- All tickets completed
- Tests passing
- Documentation updated
- Commits linked to tickets

**Document**: All work in `_pyrite/active/` and work effort tickets

**Log**: Final findings via `waft finding log`

---

## Tool Usage Throughout

### Empirica
- **Phase 1**: Optional - Check if initialized
- **Phase 2**: Create session, log findings/unknowns
- **Phase 3-5**: Log planning findings
- **Phase 6**: Preflight, log during work, postflight

### _pyrite
- **Phase 1**: Document spin-up findings
- **Phase 2**: Document all exploration findings
- **Phase 3-5**: Document planning process
- **Phase 6**: Document implementation progress

### GitHub MCP
- **Phase 1**: Check repository state
- **Phase 2**: Extensive exploration (CRITICAL)
- **Phase 3-5**: Search for related work, patterns
- **Phase 6**: Review related code, check for conflicts

### Work Efforts MCP
- **Phase 1**: List active work
- **Phase 2**: Search related work
- **Phase 3**: Create work effort and tickets
- **Phase 4-5**: Update work effort
- **Phase 6**: Update tickets, track progress

### Waft Commands
- **Phase 1**: `waft info`, `waft verify`, `waft stats`
- **Phase 2**: `waft info`, `waft verify`, `waft finding log`, `waft unknown log`
- **Phase 3-5**: `waft finding log`
- **Phase 6**: `waft verify`, `waft stats`, `waft finding log`, `waft unknown log`

### Git
- **Phase 1**: Check status
- **Phase 2**: Review history
- **Phase 3-5**: Commit planning documents
- **Phase 6**: Frequent incremental commits

---

## Execution Checklist

### Phase 1: Spin-Up
- [ ] Date check
- [ ] Disk space check
- [ ] MCP health check
- [ ] Git status check
- [ ] Active work efforts listed
- [ ] Recent history read
- [ ] GitHub state checked (commits, issues, PRs, branches)
- [ ] Project state checked (waft info, verify, stats)
- [ ] Documented in `_pyrite/active/`

### Phase 2: Explore
- [ ] Empirica session created
- [ ] GitHub exploration complete (all tools used)
- [ ] Project structure analyzed
- [ ] Architecture analyzed
- [ ] Dependencies analyzed
- [ ] Patterns discovered
- [ ] Functionality mapped
- [ ] Documentation reviewed
- [ ] Testing analyzed
- [ ] Integration points identified
- [ ] All findings documented in `_pyrite/active/`
- [ ] Findings logged via `waft finding log`
- [ ] Unknowns logged via `waft unknown log`

### Phase 3: Draft Plan
- [ ] Exploration findings reviewed
- [ ] Requirements identified
- [ ] Work broken down into tasks
- [ ] Complexity estimated
- [ ] Dependencies identified
- [ ] Work effort created/updated
- [ ] Tickets created
- [ ] Plan documented

### Phase 4: Critique Plan
- [ ] Plan reviewed for completeness
- [ ] Assumptions validated
- [ ] Gaps identified
- [ ] Feasibility checked
- [ ] Dependencies reviewed
- [ ] Alternatives considered
- [ ] Plan refined
- [ ] Documentation updated

### Phase 5: Finalize Plan
- [ ] Final review complete
- [ ] Work effort updated
- [ ] Tickets finalized
- [ ] Final plan documented
- [ ] Devlog updated
- [ ] Planning work committed

### Phase 6: Begin
- [ ] Preflight assessment (if Empirica)
- [ ] First ticket started
- [ ] Implementation workflow followed:
  - [ ] Incremental changes
  - [ ] Frequent verification
  - [ ] Findings logged
  - [ ] Unknowns logged
  - [ ] Frequent commits
  - [ ] Tickets updated
- [ ] All tickets completed
- [ ] Work effort completed
- [ ] Postflight assessment (if Empirica)
- [ ] Devlog updated
- [ ] Final summary

---

## Output Format

After each phase, provide:
1. **Phase summary**: What was accomplished
2. **Key findings**: Important discoveries
3. **Next steps**: What comes next
4. **Tool usage**: What tools were used
5. **Documentation**: Where findings are documented

---

## Notes

- **Use tools actively** - Don't just read, use Empirica, _pyrite, MCPs, waft
- **Document as you go** - Create `_pyrite/active/` files during each phase
- **Log findings** - Use `waft finding log` for discoveries
- **Track unknowns** - Use `waft unknown log` for gaps
- **Commit frequently** - Make incremental commits, not big batches
- **Update tickets** - Keep work effort tickets updated with progress
- **Verify often** - Run `waft verify` after changes
- **Check stats** - Use `waft stats` to track gamification progress

---

## Related Commands

- `spin-up` - Quick orientation (Phase 1 only)
- `explore` - Deep exploration (Phase 2 only)
- See individual phase commands for detailed procedures

---

**This command runs the complete workflow. Use it when you need thorough understanding and planning before implementation.**

