# Cursor Documentation Index

**Last Updated**: 2026-01-11
**Purpose**: Navigate the cursor documentation ecosystem

---

## Quick Start

### For First-Time Users
1. Start here: [REPO_PURPOSE.md](REPO_PURPOSE.md) - Understand what Waft is
2. Then read: [CURSOR_DEVELOPMENT_PLAN.md](CURSOR_DEVELOPMENT_PLAN.md) - See the full cursor plan
3. Try commands: [commands/help.md](commands/help.md) - Discover available commands

### For Returning Users
1. Quick status: Use `/status` command (coming soon)
2. Resume work: [CONTINUATION_PROMPT.md](CONTINUATION_PROMPT.md)
3. Check context: [CLAUDE_CODE_CONTEXT.md](CLAUDE_CODE_CONTEXT.md)

---

## Core Documentation

### Context Files

| File | Purpose | When to Use |
|------|---------|-------------|
| [REPO_PURPOSE.md](REPO_PURPOSE.md) | Repository role and philosophy | Understanding Waft's nature as a workshop |
| [CONTINUATION_PROMPT.md](CONTINUATION_PROMPT.md) | Complete handoff instructions | Starting a new session or handoff |
| [CLAUDE_CODE_CONTEXT.md](CLAUDE_CODE_CONTEXT.md) | Detailed context for Claude Code | Working with Claude Code CLI |
| [MIGRATION_CONTEXT.md](MIGRATION_CONTEXT.md) | Migration context for projects | Understanding project migrations |
| [BRANCH_STRATEGY_SETUP.md](BRANCH_STRATEGY_SETUP.md) | Branch strategy context | Working with git branches |
| [BRIDGE_PROMPT.md](BRIDGE_PROMPT.md) | Quick bridge prompt | Quick context refresh |
| [RECAP_AND_REVIEW.md](RECAP_AND_REVIEW.md) | Comprehensive review | End-of-session review |

### Planning Documents

| File | Purpose | Status |
|------|---------|--------|
| [CURSOR_DEVELOPMENT_PLAN.md](CURSOR_DEVELOPMENT_PLAN.md) | Master plan for cursor development | ✅ Complete - 6 phases defined |
| [plans/scint_integration_plan_corrected.md](plans/scint_integration_plan_corrected.md) | Scint system integration plan | 📋 Pending - 10 tasks defined |
| [plans/scint_integration_plan_revised.md](plans/scint_integration_plan_revised.md) | Legacy scint plan | 🗄️ Archived - superseded by corrected version |

---

## Command Reference

### Available Commands (20+)

#### Data Gathering & Analysis
- `/phase1` - Comprehensive data gathering & visualization
- `/analyze` - Analysis, insights & action planning
- `/visualize` - Quick interactive browser dashboard
- `/verify` - Verification with traceable evidence
- `/analytics` - Analytics and metrics
- `/audit` - Comprehensive audit

#### Decision Support
- `/consider` - Qualitative analysis and recommendations
- `/decide` - Quantitative decision matrix calculations
- `/deep-think` - Comprehensive cognitive workflow: critique → reflect → think → check-assumptions → verify → consider → decide → synthesize

#### Orientation & Exploration
- `/orient` - Complete project startup process
- `/spin-up` - Quick orientation
- `/explore` - Deep exploration
- `/engineer` - Complete engineering workflow
- `/rampup` - Get up to speed

#### Session Management
- `/checkout` - End chat session workflow
- `/continue` - Reflect and continue work
- `/recap` - Conversation recap and summary
- `/stats` - Session statistics

#### Project Management
- `/checkpoint` - Situation report and status update
- `/goal` - Track larger goals, break into steps
- `/next` - Identify next step based on goals

#### Utilities
- `/help` - Discover and understand commands

### Coming Soon (7 commands)

Based on [CURSOR_DEVELOPMENT_PLAN.md](CURSOR_DEVELOPMENT_PLAN.md) - Phase 1:

- `/status` - Quick status check (High Priority)
- `/context` - Get current context (High Priority)
- `/sync` - Sync documentation (Medium Priority)
- `/todos` - Todo management (Medium Priority)
- `/search` - Search documentation (Medium Priority)
- `/cleanup` - Cleanup and maintenance (Low Priority)
- `/links` - Create documentation links (Low Priority)

---

## Development Plan Overview

### Phase 1: Complete Missing Commands (Week 1-2)
- 7 new commands to implement
- Focus on core utilities and management
- Est. 23 hours

### Phase 2: IDE Integration (Week 2-3)
- Create .cursorrules file
- Set up cursor composer
- Enable tab completion
- MCP integration
- Est. 14 hours

### Phase 3: Scint Integration (Week 3-4)
- Implement 10 scint integration tasks
- Error detection and stabilization
- Testing and persistence
- Est. 42 hours

### Phase 4: Documentation (Week 4-5)
- Workflow guides
- Command references
- Best practices
- Troubleshooting
- Est. 27 hours

### Phase 5: Testing & Automation (Week 5-6)
- Test framework
- Command tests
- Automation scripts
- CI/CD integration
- Est. 22 hours

### Phase 6: Performance & Extensibility (Week 6-7)
- Performance optimization
- Caching system
- Plugin architecture
- Command composition
- Est. 26 hours

**Total Estimated Time**: ~154 hours (~4 weeks)

---

## Workflows

### Common Workflows

#### Starting a New Session
```
1. Read CONTINUATION_PROMPT.md (or use /continue)
2. Check git status
3. Use /orient or /spin-up
4. Begin work
```

#### Development Workflow
```
1. /explore - Understand codebase
2. /analyze - Analyze findings
3. /consider or /decide - Make decisions
4. /engineer - Implement changes
5. /verify - Verify implementation
6. /checkpoint - Create checkpoint
```

#### Ending a Session
```
1. /stats - Review session stats
2. /recap - Create session summary
3. /checkpoint - Save checkpoint
4. /checkout - Complete checkout workflow
```

#### Making Decisions
```
Qualitative: /consider → recommendations
Quantitative: /decide → decision matrix
```

---

## File Organization

```
.cursor/
├── INDEX.md                          # This file
├── CURSOR_DEVELOPMENT_PLAN.md        # Master development plan
│
├── Context Files/
│   ├── REPO_PURPOSE.md               # Repository philosophy
│   ├── CONTINUATION_PROMPT.md        # Handoff instructions
│   ├── CLAUDE_CODE_CONTEXT.md        # Claude Code context
│   ├── MIGRATION_CONTEXT.md          # Migration context
│   ├── BRANCH_STRATEGY_SETUP.md      # Branch strategy
│   ├── BRIDGE_PROMPT.md              # Quick context
│   └── RECAP_AND_REVIEW.md           # Session review
│
├── commands/                         # Command definitions (20+ files)
│   ├── COMMAND_RECOMMENDATIONS.md    # Recommended commands
│   ├── help.md                       # Help command
│   ├── analyze.md                    # Analysis command
│   ├── decide.md                     # Decision command
│   └── ... (20+ more)
│
└── plans/                            # Implementation plans
    ├── scint_integration_plan_corrected.md
    └── scint_integration_plan_revised.md
```

---

## Quick Reference

### Most Useful Commands
1. `/help` - Discover all commands
2. `/orient` - Get oriented in project
3. `/analyze` - Analyze current state
4. `/consider` - Get recommendations
5. `/decide` - Make quantitative decisions
6. `/checkpoint` - Save current state
7. `/checkout` - End session properly

### Key Files to Read
1. `CURSOR_DEVELOPMENT_PLAN.md` - The master plan
2. `CONTINUATION_PROMPT.md` - How to resume work
3. `COMMAND_RECOMMENDATIONS.md` - Command overview
4. `REPO_PURPOSE.md` - Repository philosophy

### Development Priorities (from plan)
1. **High**: Implement /status, /context, /sync
2. **Medium**: Implement /todos, /search
3. **High**: Create .cursorrules, IDE integration
4. **Medium**: Scint integration implementation
5. **Medium**: Documentation (workflows, best practices)

---

## Next Steps

### Immediate (This Week)
1. ✅ Review CURSOR_DEVELOPMENT_PLAN.md
2. ⏭️ Start Phase 1.1: Implement /status command
3. ⏭️ Create .cursorrules file (Phase 2.1.1)

### Short Term (Next 2 Weeks)
1. Complete Phase 1: All 7 missing commands
2. Complete Phase 2: IDE integration
3. Begin Phase 3: Scint integration

### Medium Term (Next Month)
1. Complete Phases 1-3
2. Begin Phase 4: Documentation
3. Review progress and adjust

---

## Resources

### Internal Documentation
- Main README: `/home/user/waft/README.md`
- Branch Strategy: `docs/BRANCH_STRATEGY.md`
- Work Efforts: `_work_efforts/`
- Active Work: `_pyrite/active/`

### External Resources
- Cursor IDE: https://cursor.sh
- Model Context Protocol: https://modelcontextprotocol.io
- Waft Repository: https://github.com/ctavolazzi/waft

---

## Contributing

When adding new commands or documentation:

1. Follow existing patterns in `commands/` directory
2. Update COMMAND_RECOMMENDATIONS.md
3. Update this INDEX.md
4. Add examples and use cases
5. Test thoroughly
6. Document in CURSOR_DEVELOPMENT_PLAN.md

---

## Questions?

- Start with `/help` command
- Read CURSOR_DEVELOPMENT_PLAN.md for the full picture
- Check CONTINUATION_PROMPT.md for handoff context
- Review command definitions in `commands/` directory

---

**Last Updated**: 2026-01-11
**Maintainer**: Claude (AI Assistant)
**Status**: Living Document - Updated as cursor system evolves
