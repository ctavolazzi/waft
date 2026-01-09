# Resume

**Pick up where you left off - restore context and continue work.**

Loads the most recent session summary, compares current state with what was left, identifies what was in progress, and provides clear next steps to continue work seamlessly.

**Use when:** Starting a new session and want to quickly understand where you left off and what to do next.

---

## Purpose

This command provides:
- **Context Restoration**: Loads last session's state and summary
- **State Comparison**: Shows what's changed since last session
- **Progress Identification**: Identifies what was in progress
- **Next Steps**: Clear actions to continue work
- **Seamless Continuity**: Pick up exactly where you left off

---

## Philosophy

1. **Continuity**: Seamless transition between sessions
2. **Context**: Full understanding of where things were left
3. **Clarity**: Clear next steps, not just information
4. **Comparison**: See what changed since last session
5. **Actionable**: Ready to continue immediately

---

## What Gets Loaded

### 1. Last Session Summary
- Most recent checkout session summary
- Files created/modified in last session
- Decisions made
- Work accomplished
- Next steps that were planned

### 2. Current State
- Current git status
- Current branch
- Uncommitted changes
- Files modified since last session
- Project health status

### 3. Comparison
- What's changed since last session
- New files created
- Files modified
- Git commits made
- Work progress since last session

### 4. In-Progress Items
- Uncommitted work from last session
- Pending tasks
- Open questions
- Blockers that were identified

### 5. Next Steps
- Immediate actions to continue
- Tasks that were pending
- Decisions that need to be made
- Work that was in progress

---

## Execution Steps

1. **Find Last Session**
   - Search `_pyrite/checkout/` for most recent session summary
   - Load session summary markdown
   - Parse key information (files, stats, next steps)

2. **Get Current State**
   - Run `git status` for current state
   - Check current branch
   - Get uncommitted files
   - Check project health

3. **Compare States**
   - Compare git status (committed vs uncommitted)
   - Compare file lists (what's new/changed)
   - Identify progress made
   - Identify what's still pending

4. **Identify In-Progress Work**
   - Uncommitted changes from last session
   - Files that were being worked on
   - Tasks mentioned in "Next Steps"
   - Work efforts that were active

5. **Generate Resume Report**
   - Display last session summary
   - Show current state
   - Highlight what's changed
   - Provide clear next steps

---

## Output Format

### Last Session Summary

**Session**: [Date/Time]
**Status**: ✅ Complete / ⏸️ In Progress

**Accomplishments**:
- Files created: X
- Files modified: Y
- Lines written: Z
- Key work: [Summary]

**Next Steps (from last session)**:
1. [Action 1]
2. [Action 2]
3. [Action 3]

---

### Current State

**Git Status**:
- Branch: [branch name]
- Uncommitted files: X
- Commits ahead: Y
- Status: [Clean / Has changes]

**Project Health**:
- Integrity: X%
- Structure: Valid / Invalid
- Dependencies: Locked / Unlocked

---

### What's Changed

**Since Last Session**:
- ✅ [Completed items]
- 📝 [Modified items]
- 🆕 [New items]
- ⚠️ [Pending items]

**Progress Made**:
- [What was accomplished since last session]

**Still Pending**:
- [What's still in progress]

---

### Continue Work

**Immediate Next Steps**:
1. [Action 1] - [Why]
2. [Action 2] - [Why]
3. [Action 3] - [Why]

**In-Progress Items**:
- [Item 1] - [Status]
- [Item 2] - [Status]

**Suggested Commands**:
- `/phase1` - Get full project overview
- `/analyze` - Analyze current state
- `/checkpoint` - Create new checkpoint
- `git status` - Review uncommitted changes

---

## Use Cases

### 1. Starting New Session
**Scenario**: Coming back to work after a break

**Example**:
```
User: "/resume"

AI: [Loads last session, compares state, shows next steps]

AI: ✅ Resumed from session: 2026-01-07 21:13:03
    Last session: Created 3 files, modified 5 files
    Current state: 2 uncommitted files, branch: main
    Next steps: Review dashboard changes, commit if ready
```

---

### 2. Checking Progress
**Scenario**: Want to see what's changed since last session

**Example**:
```
User: "/resume"

AI: [Shows comparison of states]

AI: 📊 Progress Since Last Session:
    ✅ Committed dashboard improvements
    ✅ Fixed decision engine documentation
    ⏸️ Still working on: Phase 3 persistence
```

---

### 3. Finding Next Steps
**Scenario**: Not sure what to work on next

**Example**:
```
User: "/resume"

AI: [Shows next steps from last session]

AI: 🎯 Next Steps (from last session):
    1. Implement Phase 3 persistence
    2. Test decision engine
    3. Update documentation
```

---

## Integration with Other Commands

- **`/checkout`**: Creates the session summaries that `/resume` loads
- **`/phase1`**: Can run after resume to get full current state
- **`/analyze`**: Can analyze current state after resuming
- **`/checkpoint`**: Can create new checkpoint after resuming
- **`/stats`**: Shows current session stats (different from resume)

---

## When to Use

**Use `/resume` when**:
- ✅ Starting a new work session
- ✅ Want to pick up where you left off
- ✅ Need to understand what was in progress
- ✅ Want to see what's changed since last session
- ✅ Need clear next steps

**Don't use `/resume` when**:
- ❌ Need current state only (use `/phase1`)
- ❌ Need full analysis (use `/analyze`)
- ❌ No previous session exists (use `/phase1` or `/spin-up`)
- ❌ Just want git status (use `git status`)

---

## Technical Details

### Session Summary Format

Session summaries are stored in `_pyrite/checkout/session-YYYY-MM-DD-HHMMSS.md` with:
- Session date/time
- Files created/modified
- Statistics (lines, operations)
- Git status at session end
- Next steps planned

### State Comparison

Compares:
- Git branch (same or changed)
- Uncommitted files (committed or still uncommitted)
- File modifications (new changes or same)
- Project health (improved or same)

### Error Handling

- **No session found**: Suggests running `/phase1` or `/spin-up`
- **Corrupted session file**: Falls back to git status and current state
- **Missing data**: Gracefully handles missing information

---

## Example Output

```
🌊 Resume: Picking Up Where You Left Off

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Last Session: 2026-01-07 21:13:03

Accomplishments:
  • Files Created: 3
  • Files Modified: 5
  • Lines Written: 1,247
  • Net Change: +1,189 lines

Top Files Worked On:
  1. ✨ src/waft/core/decision_cli.py (+249 lines)
  2. ✨ docs/DECISION_ENGINE_ARCHITECTURE.md (+398 lines)
  3. 📝 src/waft/core/decision_matrix.py (+182 lines)

Next Steps (from last session):
  1. Review decision engine documentation
  2. Test Phase 3 persistence design
  3. Consider implementing Phase 3.1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Current State

Git Status:
  • Branch: main
  • Uncommitted Files: 2
  • Commits Ahead: 4
  • Status: Has uncommitted changes

Project Health:
  • Integrity: 100%
  • Structure: Valid
  • Dependencies: Locked

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 What's Changed Since Last Session

✅ Progress Made:
  • Committed decision engine documentation
  • Updated devlog with Phase 3 design

⏸️ Still In Progress:
  • 2 uncommitted files (decision_matrix.py, decision_cli.py)
  • Phase 3 persistence implementation pending

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Continue Work

Immediate Next Steps:
  1. Review uncommitted changes in decision_matrix.py and decision_cli.py
  2. Consider committing if changes are complete
  3. Continue with Phase 3.1 implementation (decision persistence)

In-Progress Items:
  • Decision Engine Phase 3 design - ✅ Design complete, ready for implementation
  • Documentation updates - ⏸️ In progress

Suggested Commands:
  • git status - Review uncommitted changes
  • /phase1 - Get full current project overview
  • /analyze - Analyze current state and generate action plan
  • /checkpoint - Create new checkpoint for current state

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Resume Complete - Ready to continue work
```

---

## Advanced Features

### Resume with Specific Session
```bash
/resume --session session-2026-01-07-211303
```

### Resume with Comparison
```bash
/resume --compare  # Show detailed comparison
```

### Resume with Full Context
```bash
/resume --full  # Load full session context, not just summary
```

---

**This command ensures seamless continuity between sessions, helping you pick up exactly where you left off with full context and clear next steps.**
