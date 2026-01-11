# Cursor Development Plan

**Created**: 2026-01-11
**Branch**: `claude/cursor-plan-epI5z`
**Status**: Draft - Ready for Review

---

## Executive Summary

This plan outlines the comprehensive development of cursor tooling, workflows, and integration for the Waft project. It builds on the existing extensive cursor command system and aims to create a complete, production-ready cursor development environment.

---

## Current State Analysis

### ✅ Existing Infrastructure

**Context Files** (7 total):
- `REPO_PURPOSE.md` - Repository role and philosophy
- `CONTINUATION_PROMPT.md` - Complete handoff instructions
- `MIGRATION_CONTEXT.md` - Migration context for projects
- `CLAUDE_CODE_CONTEXT.md` - Detailed context for Claude Code
- `BRIDGE_PROMPT.md` - Quick bridge prompt
- `BRANCH_STRATEGY_SETUP.md` - Branch strategy context
- `RECAP_AND_REVIEW.md` - Comprehensive review

**Cursor Commands** (20+ implemented):
- Data gathering: `/phase1`, `/visualize`, `/analyze`
- Decision support: `/consider`, `/decide`
- Orientation: `/orient`, `/spin-up`, `/explore`, `/engineer`
- Session management: `/checkout`, `/stats`, `/recap`, `/continue`
- Project management: `/verify`, `/checkpoint`, `/goal`, `/next`
- Analysis: `/analytics`, `/audit`
- Execution: `/execute`, `/compose`

**Plans**:
- `scint_integration_plan_corrected.md` (10 todos, pending implementation)
- `scint_integration_plan_revised.md` (legacy, superseded)

### 🔍 Identified Gaps

**Missing Commands** (from COMMAND_RECOMMENDATIONS.md):
1. `/status` - Quick status check
2. `/context` - Get current context
3. `/sync` - Sync documentation
4. `/todos` - Todo management
5. `/search` - Search documentation
6. `/cleanup` - Cleanup and maintenance
7. `/links` - Create documentation links

**Missing IDE Integration**:
1. `.cursorrules` file (cursor IDE rules)
2. Cursor composer integration
3. Cursor tab completion
4. MCP (Model Context Protocol) integration
5. Custom cursor keybindings

**Missing Documentation**:
1. Cursor workflow guide
2. Command usage examples
3. Best practices guide
4. Cursor automation guide

**Pending Implementation**:
1. Scint integration (10 todos pending)
2. Command testing framework
3. Command versioning system

---

## Development Objectives

### Primary Objectives

1. **Complete Command Suite**
   - Implement all recommended commands
   - Ensure consistent command interface
   - Add comprehensive error handling

2. **IDE Integration**
   - Set up .cursorrules for IDE
   - Configure cursor composer
   - Enable tab completion
   - Integrate MCP servers

3. **Scint Integration**
   - Implement scint detection system
   - Create stabilization workflows
   - Add scint persistence and tracking

4. **Documentation Excellence**
   - Create comprehensive workflow guide
   - Document all commands with examples
   - Establish best practices
   - Add troubleshooting guide

5. **Automation & Testing**
   - Build command testing framework
   - Create automation scripts
   - Set up CI/CD for cursor commands

### Secondary Objectives

1. **Performance Optimization**
   - Optimize command execution speed
   - Reduce context overhead
   - Implement caching strategies

2. **User Experience**
   - Add interactive command helpers
   - Create command discovery system
   - Implement command suggestions

3. **Extensibility**
   - Design plugin architecture
   - Enable custom command creation
   - Support command composition

---

## Phase 1: Complete Missing Commands

**Timeline**: Week 1-2
**Priority**: High

### Phase 1.1: Core Utility Commands

#### Task 1.1.1: Implement `/status`
- **Purpose**: Lightweight status check
- **Output**: One-line summary (date, git, health, active work)
- **Location**: `.cursor/commands/status.md`
- **Estimated Effort**: 2 hours

#### Task 1.1.2: Implement `/context`
- **Purpose**: Current context for handoff
- **Output**: Context summary document
- **Location**: `.cursor/commands/context.md`
- **Estimated Effort**: 3 hours

#### Task 1.1.3: Implement `/sync`
- **Purpose**: Sync documentation across files
- **Output**: List of updated files
- **Location**: `.cursor/commands/sync.md`
- **Estimated Effort**: 4 hours

### Phase 1.2: Management Commands

#### Task 1.2.1: Implement `/todos`
- **Purpose**: Todo management and tracking
- **Output**: Todo list with status
- **Location**: `.cursor/commands/todos.md`
- **Estimated Effort**: 3 hours

#### Task 1.2.2: Implement `/search`
- **Purpose**: Search across documentation
- **Output**: Search results with context
- **Location**: `.cursor/commands/search.md`
- **Estimated Effort**: 4 hours

#### Task 1.2.3: Implement `/cleanup`
- **Purpose**: Cleanup and maintenance
- **Output**: List of cleanup actions
- **Location**: `.cursor/commands/cleanup.md`
- **Estimated Effort**: 3 hours

#### Task 1.2.4: Implement `/links`
- **Purpose**: Create bidirectional documentation links
- **Output**: Updated documents with links
- **Location**: `.cursor/commands/links.md`
- **Estimated Effort**: 4 hours

### Phase 1 Deliverables
- [ ] 7 new command files created
- [ ] Commands documented with examples
- [ ] Commands tested and validated
- [ ] COMMAND_RECOMMENDATIONS.md updated

---

## Phase 2: IDE Integration

**Timeline**: Week 2-3
**Priority**: High

### Phase 2.1: Cursor Rules Setup

#### Task 2.1.1: Create `.cursorrules`
- **Purpose**: Configure cursor IDE behavior
- **Content**:
  - Project-specific rules
  - Code style preferences
  - AI assistant guidelines
  - Context loading strategies
- **Location**: `.cursorrules`
- **Estimated Effort**: 3 hours

#### Task 2.1.2: Configure Cursor Composer
- **Purpose**: Enable multi-file editing workflows
- **Actions**:
  - Define composer templates
  - Set up file groupings
  - Configure auto-completion
- **Estimated Effort**: 2 hours

### Phase 2.2: Advanced Integration

#### Task 2.2.1: Set Up Tab Completion
- **Purpose**: Enable cursor command tab completion
- **Actions**:
  - Create completion spec
  - Configure shell integration
  - Test completion behavior
- **Estimated Effort**: 3 hours

#### Task 2.2.2: MCP Integration
- **Purpose**: Integrate Model Context Protocol servers
- **Actions**:
  - Identify useful MCP servers
  - Configure MCP integration
  - Test server connectivity
- **Estimated Effort**: 4 hours

#### Task 2.2.3: Custom Keybindings
- **Purpose**: Quick access to common commands
- **Actions**:
  - Define keybinding mappings
  - Document keybindings
  - Test in cursor IDE
- **Estimated Effort**: 2 hours

### Phase 2 Deliverables
- [ ] `.cursorrules` file created
- [ ] Cursor composer configured
- [ ] Tab completion enabled
- [ ] MCP servers integrated
- [ ] Custom keybindings documented

---

## Phase 3: Scint Integration Implementation

**Timeline**: Week 3-4
**Priority**: Medium

### Phase 3.1: Scint Detection System

#### Task 3.1.1: Implement Scint Model
- **Reference**: `scint_integration_plan_corrected.md` - Task 1
- **Actions**:
  - Add ScintType enum with structured error types
  - Create Scint model with severity calculation
  - Add error code mapping
- **Location**: `src/gym/rpg/models.py`
- **Estimated Effort**: 4 hours

#### Task 3.1.2: Update BattleLog Model
- **Reference**: `scint_integration_plan_corrected.md` - Task 2
- **Actions**:
  - Add optional Scint fields
  - Add version field for backward compatibility
  - Ensure graceful degradation
- **Location**: `src/gym/rpg/models.py`
- **Estimated Effort**: 3 hours

#### Task 3.1.3: Implement Scint Detection
- **Reference**: `scint_integration_plan_corrected.md` - Task 3
- **Actions**:
  - Create `_detect_scints()` with robust error detection
  - Use exception types and regex patterns
  - Support multiple Scint detection
- **Location**: `src/gym/rpg/engine.py`
- **Estimated Effort**: 6 hours

### Phase 3.2: Scint Stabilization System

#### Task 3.2.1: Implement Stabilization Logic
- **Reference**: `scint_integration_plan_corrected.md` - Task 4
- **Actions**:
  - Create `_attempt_stabilization()` with timeout
  - Add retry limits and cost tracking
  - Implement abort conditions
- **Location**: `src/gym/rpg/engine.py`
- **Estimated Effort**: 6 hours

#### Task 3.2.2: Update Encounter Flow
- **Reference**: `scint_integration_plan_corrected.md` - Task 5
- **Actions**:
  - Modify `start_encounter()` with exception handling
  - Support multi-Scint stabilization
  - Add comprehensive error handling
- **Location**: `src/gym/rpg/engine.py`
- **Estimated Effort**: 4 hours

### Phase 3.3: Scint Configuration & UI

#### Task 3.3.1: Define Stat Mapping
- **Reference**: `scint_integration_plan_corrected.md` - Task 6
- **Actions**:
  - Create clear INT/WIS/CHA mapping rules
  - Make weights configurable
  - Document stat influence
- **Location**: `src/gym/rpg/config.py`
- **Estimated Effort**: 3 hours

#### Task 3.3.2: Update Quest System
- **Reference**: `scint_integration_plan_corrected.md` - Task 7
- **Actions**:
  - Update quest descriptions
  - Add expected_output schema
  - Enable critical hit detection
- **Location**: `src/gym/rpg/quests.py`
- **Estimated Effort**: 4 hours

#### Task 3.3.3: Add Rich UI
- **Reference**: `scint_integration_plan_corrected.md` - Task 8
- **Actions**:
  - Add Rich terminal compatibility checks
  - Create plain text fallbacks
  - Implement Scint visualization
- **Location**: `src/gym/rpg/ui.py`
- **Estimated Effort**: 5 hours

### Phase 3.4: Testing & Persistence

#### Task 3.4.1: Update Mock Agent
- **Reference**: `scint_integration_plan_corrected.md` - Task 9
- **Actions**:
  - Add stabilization prompt detection
  - Implement Scint handling
  - Test stabilization flows
- **Location**: `tests/gym/test_rpg.py`
- **Estimated Effort**: 3 hours

#### Task 3.4.2: Implement Scint Persistence
- **Reference**: `scint_integration_plan_corrected.md` - Task 10
- **Actions**:
  - Save original and corrected responses
  - Create Scint history tracking
  - Add loot system integration
- **Location**: `src/gym/rpg/persistence.py`
- **Estimated Effort**: 4 hours

### Phase 3 Deliverables
- [ ] Scint model implemented (10/10 tasks complete)
- [ ] All tests passing
- [ ] Scint documentation updated
- [ ] Integration tested end-to-end

---

## Phase 4: Documentation & Workflows

**Timeline**: Week 4-5
**Priority**: Medium

### Phase 4.1: Workflow Documentation

#### Task 4.1.1: Create Cursor Workflow Guide
- **Purpose**: Comprehensive guide to cursor workflows
- **Content**:
  - Common workflows (orientation, development, checkout)
  - Command sequences
  - Best practices
  - Troubleshooting
- **Location**: `docs/CURSOR_WORKFLOWS.md`
- **Estimated Effort**: 6 hours

#### Task 4.1.2: Document All Commands with Examples
- **Purpose**: Reference documentation for all commands
- **Content**:
  - Command syntax
  - Use cases
  - Examples
  - Output formats
- **Location**: `docs/CURSOR_COMMANDS.md`
- **Estimated Effort**: 8 hours

#### Task 4.1.3: Create Best Practices Guide
- **Purpose**: Guidelines for cursor usage
- **Content**:
  - When to use which command
  - Command composition patterns
  - Performance tips
  - Anti-patterns to avoid
- **Location**: `docs/CURSOR_BEST_PRACTICES.md`
- **Estimated Effort**: 4 hours

### Phase 4.2: Advanced Documentation

#### Task 4.2.1: Create Troubleshooting Guide
- **Purpose**: Common issues and solutions
- **Content**:
  - Common errors
  - Debug procedures
  - Performance issues
  - FAQ
- **Location**: `docs/CURSOR_TROUBLESHOOTING.md`
- **Estimated Effort**: 4 hours

#### Task 4.2.2: Create Automation Guide
- **Purpose**: Guide to cursor automation
- **Content**:
  - Automation patterns
  - Script examples
  - CI/CD integration
  - Custom workflows
- **Location**: `docs/CURSOR_AUTOMATION.md`
- **Estimated Effort**: 5 hours

### Phase 4 Deliverables
- [ ] 5 comprehensive documentation files
- [ ] All commands documented with examples
- [ ] Workflow patterns documented
- [ ] Troubleshooting guide complete

---

## Phase 5: Testing & Automation

**Timeline**: Week 5-6
**Priority**: Low

### Phase 5.1: Command Testing Framework

#### Task 5.1.1: Create Test Framework
- **Purpose**: Automated testing for cursor commands
- **Actions**:
  - Define test structure
  - Create test utilities
  - Set up test fixtures
- **Location**: `tests/cursor/`
- **Estimated Effort**: 6 hours

#### Task 5.1.2: Write Command Tests
- **Purpose**: Test all cursor commands
- **Actions**:
  - Test each command
  - Test error conditions
  - Test edge cases
- **Location**: `tests/cursor/test_commands.py`
- **Estimated Effort**: 8 hours

### Phase 5.2: Automation Scripts

#### Task 5.2.1: Create Command Runner
- **Purpose**: Run cursor commands programmatically
- **Actions**:
  - Create command executor
  - Add error handling
  - Support dry-run mode
- **Location**: `scripts/cursor-run.sh`
- **Estimated Effort**: 4 hours

#### Task 5.2.2: Set Up CI/CD Integration
- **Purpose**: Test cursor commands in CI
- **Actions**:
  - Add GitHub Actions workflow
  - Test command execution
  - Validate command outputs
- **Location**: `.github/workflows/cursor-tests.yml`
- **Estimated Effort**: 4 hours

### Phase 5 Deliverables
- [ ] Command testing framework complete
- [ ] All commands have tests
- [ ] Automation scripts created
- [ ] CI/CD integration working

---

## Phase 6: Performance & Extensibility

**Timeline**: Week 6-7
**Priority**: Low

### Phase 6.1: Performance Optimization

#### Task 6.1.1: Optimize Command Execution
- **Purpose**: Reduce command execution time
- **Actions**:
  - Profile command performance
  - Identify bottlenecks
  - Implement optimizations
- **Estimated Effort**: 6 hours

#### Task 6.1.2: Implement Caching
- **Purpose**: Cache command outputs
- **Actions**:
  - Design cache strategy
  - Implement cache system
  - Add cache invalidation
- **Estimated Effort**: 6 hours

### Phase 6.2: Extensibility

#### Task 6.2.1: Design Plugin Architecture
- **Purpose**: Enable custom commands
- **Actions**:
  - Define plugin interface
  - Create plugin loader
  - Document plugin API
- **Estimated Effort**: 8 hours

#### Task 6.2.2: Add Command Composition
- **Purpose**: Combine multiple commands
- **Actions**:
  - Create composition syntax
  - Implement command chaining
  - Add parallel execution
- **Estimated Effort**: 6 hours

### Phase 6 Deliverables
- [ ] Performance optimizations complete
- [ ] Caching system implemented
- [ ] Plugin architecture designed
- [ ] Command composition enabled

---

## Success Metrics

### Completion Metrics
- [ ] All 7 missing commands implemented (100%)
- [ ] All 10 scint integration tasks complete (100%)
- [ ] 5 documentation files created
- [ ] Testing framework with >80% coverage
- [ ] IDE integration fully functional

### Quality Metrics
- [ ] All tests passing
- [ ] Command execution <2s (avg)
- [ ] Zero critical bugs
- [ ] Documentation coverage 100%

### User Experience Metrics
- [ ] Command discovery time <30s
- [ ] Error messages clear and actionable
- [ ] Tab completion working
- [ ] Keybindings documented

---

## Risk Assessment

### High Risk
1. **Scint Integration Complexity**
   - Risk: Complex error detection and stabilization logic
   - Mitigation: Break into small tasks, comprehensive testing
   - Impact: Medium (can be deferred)

2. **Performance Degradation**
   - Risk: Commands become too slow
   - Mitigation: Profile early, optimize critical paths
   - Impact: High (affects UX)

### Medium Risk
1. **IDE Integration Issues**
   - Risk: Cursor IDE changes break integration
   - Mitigation: Version pin, maintain compatibility layer
   - Impact: Medium (IDE-specific)

2. **Documentation Drift**
   - Risk: Docs become outdated
   - Mitigation: Automated doc generation, CI checks
   - Impact: Medium (maintainability)

### Low Risk
1. **Plugin Architecture Adoption**
   - Risk: No one uses plugin system
   - Mitigation: Create example plugins, good docs
   - Impact: Low (nice to have)

---

## Next Steps

### Immediate Actions (This Week)
1. Review and approve this plan
2. Start Phase 1.1: Implement core utility commands
3. Create `/status` command (quick win)
4. Set up Phase 1 tracking in _work_efforts

### Next Week
1. Complete Phase 1.1 and 1.2
2. Begin Phase 2: IDE integration
3. Create .cursorrules file
4. Start scint integration planning session

### This Month
1. Complete Phases 1-3 (commands, IDE, scint)
2. Begin Phase 4 (documentation)
3. Review progress and adjust timeline

---

## Resources Required

### Time Investment
- **Phase 1**: 23 hours (commands)
- **Phase 2**: 14 hours (IDE integration)
- **Phase 3**: 42 hours (scint integration)
- **Phase 4**: 27 hours (documentation)
- **Phase 5**: 22 hours (testing & automation)
- **Phase 6**: 26 hours (performance & extensibility)
- **Total**: ~154 hours (~4 weeks full-time)

### Tools & Dependencies
- Cursor IDE (latest version)
- Python 3.10+ with uv
- Rich library (for UI)
- pytest (for testing)
- MCP servers (TBD)

### Knowledge Required
- Cursor IDE workflows
- MCP protocol
- Command design patterns
- Error detection strategies
- Testing frameworks

---

## Appendix

### A. Command Priority Matrix

| Command | Priority | Effort | Impact | Status |
|---------|----------|--------|--------|--------|
| /status | High | Low | High | Pending |
| /context | High | Medium | High | Pending |
| /sync | Medium | Medium | Medium | Pending |
| /todos | Medium | Medium | Medium | Pending |
| /search | Medium | Medium | High | Pending |
| /cleanup | Low | Medium | Low | Pending |
| /links | Low | Medium | Low | Pending |

### B. Scint Integration Timeline

| Task | Dependencies | Estimated Hours | Critical Path |
|------|--------------|-----------------|---------------|
| Scint Model | None | 4 | Yes |
| BattleLog Update | Scint Model | 3 | Yes |
| Scint Detection | BattleLog Update | 6 | Yes |
| Stabilization | Scint Detection | 6 | Yes |
| Encounter Flow | Stabilization | 4 | Yes |
| Stat Mapping | None | 3 | No |
| Quest Update | Stat Mapping | 4 | No |
| Rich UI | None | 5 | No |
| Mock Agent | Stabilization | 3 | No |
| Persistence | Stabilization | 4 | No |

### C. Reference Documents

1. **Existing Context**:
   - `.cursor/CONTINUATION_PROMPT.md` - Full handoff context
   - `.cursor/COMMAND_RECOMMENDATIONS.md` - Command recommendations
   - `.cursor/plans/scint_integration_plan_corrected.md` - Scint plan

2. **Documentation to Create**:
   - `docs/CURSOR_WORKFLOWS.md` - Workflow guide
   - `docs/CURSOR_COMMANDS.md` - Command reference
   - `docs/CURSOR_BEST_PRACTICES.md` - Best practices
   - `docs/CURSOR_TROUBLESHOOTING.md` - Troubleshooting
   - `docs/CURSOR_AUTOMATION.md` - Automation guide

3. **Integration Files**:
   - `.cursorrules` - IDE rules
   - `tests/cursor/` - Test suite
   - `scripts/cursor-run.sh` - Command runner

---

**Plan Status**: Draft - Ready for Review
**Next Review**: After Phase 1 completion
**Last Updated**: 2026-01-11
