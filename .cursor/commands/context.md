# Context

**Get current context for handoff or continuation - summarize where we are.**

Provides a comprehensive context summary of the current working state, recent conversation topics, active work items, key decisions made, and next steps. Perfect for handoffs between sessions, resuming after breaks, or getting a quick understanding of current state.

**Use when:** Handing off to another session, resuming after break, or need context summary.

---

## Purpose

This command provides:
- **Current Working State**: What's happening right now
- **Recent Conversation Topics**: What was discussed
- **Active Work Items**: Current work efforts and tickets
- **Key Decisions Made**: Important choices and rationale
- **Next Steps**: What comes next
- **Context Summary**: Complete picture for continuation

---

## Philosophy

1. **Complete Picture**: Capture everything needed to continue
2. **Structured**: Organize information logically
3. **Actionable**: Include next steps and decisions
4. **Handoff-Ready**: Format perfect for session transitions
5. **Current Focus**: What matters right now

---

## Execution Steps

### Context 1.1: Current Working State
**Purpose**: Capture current working state

**Steps**:
1. Get current date/time
2. Get working directory
3. Get git status (branch, uncommitted changes, commits ahead/behind)
4. Get project status (if applicable)
5. Identify current working directory context

**Output**: Current state summary

---

### Context 1.2: Recent Conversation Topics
**Purpose**: Summarize what was discussed

**Steps**:
1. Review recent conversation history
2. Identify main topics discussed
3. Extract key themes
4. Note important context

**Output**: Conversation topics summary

---

### Context 1.3: Active Work Items
**Purpose**: List what's currently being worked on

**Steps**:
1. Check active work efforts (via MCP or file system)
2. List active work effort names and status
3. Check active tickets and their status
4. Identify current focus area

**Output**: Active work summary

---

### Context 1.4: Key Decisions Made
**Purpose**: Document important decisions

**Steps**:
1. Review conversation for decisions
2. Extract key decisions with context
3. Note rationale for decisions
4. Document alternatives considered

**Output**: Decisions summary

---

### Context 1.5: Next Steps
**Purpose**: Identify what comes next

**Steps**:
1. Review active work for next actions
2. Check for pending tasks
3. Identify immediate next steps
4. Note any blockers or dependencies

**Output**: Next steps summary

---

## Execution Flow

```
Context 1.1: Current Working State
  ↓
Context 1.2: Recent Conversation Topics
  ↓
Context 1.3: Active Work Items
  ↓
Context 1.4: Key Decisions Made
  ↓
Context 1.5: Next Steps
  ↓
✅ Complete - Context document created
```

---

## Output Format

### Context Document

The command creates a context summary document:

```markdown
# Context Summary

**Date**: 2026-01-12 19:40:54 PST
**Working Directory**: /Users/ctavolazzi/Code/active/waft
**Session Type**: Development

## Current Working State

**Git Status**:
- Branch: main
- Uncommitted: 3 files (2 modified, 1 new)
- Commits Ahead: 0
- Commits Behind: 0

**Project Status**:
- Structure: ✅ Valid
- Health: ✅ Good
- Version: v0.0.2

**Current Focus**: Implementing Cursor Development Plan Phase 1

## Recent Conversation Topics

1. **Cursor Development Plan Implementation**
   - Reviewing plan for Phase 1
   - Identifying missing commands
   - Creating work effort

2. **Command Implementation**
   - Planning implementation order
   - Reviewing existing command patterns
   - Setting up work effort tracking

## Active Work Items

**Work Efforts**:
- WE-260112-g0ih: Cursor Development Plan - Phase 1 (active)
  - 6 tickets created
  - Status: In progress

**Tickets**:
- TKT-g0ih-001: Implement /context command (in progress)
- TKT-g0ih-002: Implement /sync command (pending)
- TKT-g0ih-003: Implement /todos command (pending)
- TKT-g0ih-004: Implement /search command (pending)
- TKT-g0ih-005: Implement /cleanup command (pending)
- TKT-g0ih-006: Implement /links command (pending)

## Key Decisions Made

1. **Implementation Order**: Start with Phase 1.1 (core utilities), then Phase 1.2 (management)
2. **Work Effort**: Created WE-260112-g0ih for tracking
3. **Command Pattern**: Follow existing command structure and style

## Next Steps

1. Complete /context command implementation
2. Implement /sync command
3. Implement remaining Phase 1.2 commands
4. Update COMMAND_RECOMMENDATIONS.md

## Files Created/Modified

- `.cursor/commands/context.md` (new)
- `_work_efforts/WE-260112-g0ih_cursor_development_plan_phase_1_complete_missing_commands/` (new)

## Notes

- Following Cursor Development Plan structure
- Commands should be lightweight and focused
- All commands should follow existing patterns
```

---

## What Gets Captured

### Current Working State
- Date and time
- Working directory
- Git status (branch, changes, commits)
- Project status (if applicable)
- Current focus area

### Recent Conversation Topics
- Main topics discussed
- Key themes
- Important context

### Active Work Items
- Active work efforts (names, status)
- Active tickets (status, progress)
- Current focus area

### Key Decisions Made
- Important decisions
- Rationale
- Alternatives considered

### Next Steps
- Immediate actions
- Pending tasks
- Blockers or dependencies

---

## Use Cases

### 1. Session Handoff
**Scenario**: Ending session, need to hand off to next session

**Example**:
```
User: "/context"
```

**Output**: Complete context document for next session

---

### 2. Resume After Break
**Scenario**: Resuming work after break, need to remember where we were

**Example**:
```
User: "/context"
```

**Output**: Context summary to resume work

---

### 3. Quick Context Check
**Scenario**: Need to understand current state quickly

**Example**:
```
User: "/context"
```

**Output**: Context summary for awareness

---

## Integration with Other Commands

- **`/checkpoint`**: Comprehensive status (`/context` is for handoff)
- **`/status`**: Quick status (`/context` is detailed summary)
- **`/recap`**: Conversation recap (`/context` is current state)
- **`/continue`**: Continue work (`/context` provides context for continuation)

---

## When to Use

**Use `/context` when**:
- ✅ Handing off to another session
- ✅ Resuming after break
- ✅ Need context summary
- ✅ Want complete picture of current state
- ✅ Preparing for continuation

**Don't use `/context` when**:
- ❌ Need quick status (use `/status`)
- ❌ Need comprehensive checkpoint (use `/checkpoint`)
- ❌ Need conversation recap (use `/recap`)

---

## Technical Details

### Tools Used

**Git Commands**:
- `git status` - Git status
- `git branch --show-current` - Current branch
- `git log --oneline -5` - Recent commits

**File System**:
- `pwd` - Working directory
- `date` - Current timestamp

**MCP Servers** (if available):
- `mcp_work-efforts_list_work_efforts` - Active work efforts
- `mcp_work-efforts_list_tickets` - Active tickets

### Performance

- **Target Time**: < 10 seconds
- **State Check**: ~2 seconds
- **Conversation Analysis**: ~3 seconds
- **Work Items Check**: ~2 seconds
- **Document Generation**: ~3 seconds

### Error Handling

- **Git Errors**: Show "Git unavailable" and continue
- **File Errors**: Show "Unable to check" and continue
- **MCP Errors**: Fall back to file system checks
- **Always Complete**: Always show what's available

---

## Example Workflow

```
User: "/context"

AI: 📋 Context Summary Created

Location: _work_efforts/CONTEXT_2026-01-12_194054.md

Summary:
- Current: Implementing Cursor Development Plan Phase 1
- Active Work: WE-260112-g0ih (6 tickets)
- Next: Complete /context, then /sync
- Status: ✅ Good progress

User: [Reviews context, continues work]
```

---

## Output Location

Context document is saved to:
- `_work_efforts/CONTEXT_YYYY-MM-DD_HHMMSS.md`

For quick reference:
- Console summary is displayed
- Full document available for review

---

**This command provides complete context for handoffs and continuation - perfect for session transitions and resuming work.**
