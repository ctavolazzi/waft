# Checkout

**End chat session - run all relevant cleanup, documentation, and summary tasks.**

Orchestrates a comprehensive "end of session" workflow that captures session statistics, creates checkpoints, updates documentation, and prepares for the next session. Designed to be run at the end of a chat session to ensure nothing is lost and everything is properly documented.

**Use when:** You're ending a chat session and want to ensure all work is captured, documented, and ready for the next session.

---

## Purpose

This command provides:
- **Session Statistics**: Capture what was accomplished (files, lines, activity)
- **Checkpoint Creation**: Document current state and progress
- **Devlog Update**: Log session activity and accomplishments
- **Session Summary**: Create a comprehensive session recap
- **Work Effort Sync**: Update any active work efforts
- **Git Status Check**: Review uncommitted changes (suggest commit if needed)
- **Next Session Prep**: Prepare context for future sessions

---

## Philosophy

1. **Complete**: Capture everything relevant to the session
2. **Non-Destructive**: Never auto-commit or delete anything
3. **Comprehensive**: Run all relevant end-of-session tasks
4. **Contextual**: Focus on what matters for this session
5. **Prepared**: Set up for smooth next session start

---

## What Gets Executed

### 1. Session Statistics
- Run `/stats --session --detailed`
- Capture files created/modified
- Calculate lines written/changed
- Identify top files by changes
- Save statistics to `_pyrite/phase1/`

### 2. Checkpoint Creation
- Run `/checkpoint` workflow
- Create checkpoint file in `_work_efforts/`
- Document current state
- Capture conversation recap
- Note next steps

### 3. Devlog Update
- Add session entry to `_work_efforts/devlog.md`
- Include session summary
- Link to checkpoint and statistics
- Document key accomplishments

### 4. Session Summary
- Create comprehensive session recap
- Include statistics summary
- List files created/modified
- Document decisions made
- Note open questions

### 5. Work Effort Sync
- Update active work efforts (if any)
- Add progress notes
- Update ticket statuses
- Link to checkpoint

### 6. Git Status Review
- Check git status
- List uncommitted changes
- Suggest commit (but don't auto-commit)
- Show commits ahead/behind

### 7. Next Session Prep
- Create session summary file
- Save to `_pyrite/checkout/` or similar
- Include quick reference for next session
- Document any pending work

---

## Execution Steps

1. **Capture Session Statistics**
   ```
   Phase 1: Statistics
   - Gathering file changes
   - Calculating line counts
   - Identifying top files
   - Saving statistics
   ```

2. **Create Checkpoint**
   ```
   Phase 2: Checkpoint
   - Recapping conversation
   - Capturing current state
   - Creating checkpoint file
   - Updating devlog
   ```

3. **Generate Session Summary**
   ```
   Phase 3: Summary
   - Compiling session recap
   - Documenting accomplishments
   - Listing files changed
   - Noting decisions made
   ```

4. **Update Documentation**
   ```
   Phase 4: Documentation
   - Updating devlog
   - Syncing work efforts
   - Creating summary file
   ```

5. **Review Git Status**
   ```
   Phase 5: Git Review
   - Checking git status
   - Listing uncommitted files
   - Suggesting next steps
   ```

6. **Save Analytics**
   ```
   Phase 6: Analytics
   - Saving session data
   - Generating prompt signature
   - Categorizing approach
   - Linking iteration chains
   ```

7. **Final Summary**
   ```
   Phase 7: Completion
   - Displaying final summary
   - Listing created files
   - Providing next steps
   ```

---

## Output Format

### Console Output

```
🚪 Checkout: Ending Chat Session

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1: Session Statistics
  📊 Gathering statistics...
  ✓ Files created: 5
  ✓ Files modified: 8
  ✓ Lines written: 1,247
  ✓ Net change: +1,577 lines
  ✓ Statistics saved: _pyrite/phase1/session-stats-2026-01-07-203045.json

Phase 2: Checkpoint Creation
  📋 Creating checkpoint...
  ✓ Checkpoint created: CHECKPOINT_2026-01-07_command_creation.md
  ✓ Devlog updated

Phase 3: Session Summary
  📝 Generating summary...
  ✓ Summary created: _pyrite/checkout/session-2026-01-07-203045.md

Phase 4: Documentation Sync
  📚 Updating documentation...
  ✓ Devlog entry added
  ✓ Work efforts synced (if applicable)

Phase 5: Git Status Review
  🔍 Checking git status...
  ⚠️  13 uncommitted files
  💡 Suggestion: Consider committing changes
     git add .
     git commit -m "Session: Command creation and enhancements"

Phase 6: Analytics & Tracking
  📊 Saving session data...
  ✓ Session saved: session-2026-01-07-203045
  ✓ Category: command_creation
  ✓ Analytics database updated

Phase 7: Completion
  ✅ Checkout complete!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Session Summary:
  • Files: 13 operations (5 created, 8 modified)
  • Code: +1,577 lines net change
  • Commands: 3 executed
  • Duration: ~45 minutes

📁 Files Created:
  • .cursor/commands/decide.md
  • .cursor/commands/visualize.md
  • .cursor/commands/phase1.md
  • src/waft/core/decision_matrix.py
  • src/waft/core/visualizer.py

📋 Documentation:
  • Checkpoint: _work_efforts/CHECKPOINT_2026-01-07_command_creation.md
  • Statistics: _pyrite/phase1/session-stats-2026-01-07-203045.json
  • Summary: _pyrite/checkout/session-2026-01-07-203045.md

💡 Next Steps:
  1. Review checkpoint and summary
  2. Commit changes if ready
  3. Push to remote if needed
  4. Start next session with /spin-up or /phase1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Session checkout complete. Ready for next session!
```

---

## Session Summary File Format

**Location**: `_pyrite/checkout/session-YYYY-MM-DD-HHMMSS.md`

**Template**:
```markdown
# Session Summary: [Date]

**Session End**: YYYY-MM-DD HH:MM:SS
**Duration**: [if available]
**Status**: ✅ Complete | 🚧 In Progress | ⏸️ Paused

---

## Quick Stats

- **Files Created**: X
- **Files Modified**: Y
- **Lines Written**: Z
- **Net Change**: +N lines
- **Commands Executed**: N

---

## Key Accomplishments

1. [Accomplishment 1]
2. [Accomplishment 2]
3. [Accomplishment 3]

---

## Files Changed

### Created
- [File 1]
- [File 2]

### Modified
- [File 1]
- [File 2]

---

## Decisions Made

- [Decision 1]
- [Decision 2]

---

## Open Questions

- [Question 1]
- [Question 2]

---

## Next Steps

1. [Next step 1]
2. [Next step 2]

---

## Related Files

- **Checkpoint**: [Link to checkpoint]
- **Statistics**: [Link to stats JSON]
- **Devlog**: [Link to devlog entry]

---

**Checkout Complete**: YYYY-MM-DD HH:MM:SS
```

---

## Integration with Other Commands

### Commands Used by Checkout

- **`/stats --session --detailed`**: Captures session statistics
- **`/checkpoint`**: Creates checkpoint document
- **`git status`**: Reviews git state
- **Work Efforts MCP**: Updates work efforts if applicable

### Commands That May Use Checkout

- **`/spin-up`**: May reference last checkout summary
- **`/phase1`**: May include checkout summary in visualization
- **`/orient`**: May use checkout for context

---

## Options

### Standard Checkout (Default)
```bash
/checkout
```
- Runs all phases
- Creates all documentation
- Reviews git status
- Provides suggestions

### Quick Checkout
```bash
/checkout --quick
```
- Skips detailed statistics
- Minimal documentation
- Fast execution
- Basic summary only

### Silent Checkout
```bash
/checkout --silent
```
- Minimal console output
- Creates all files
- No suggestions
- Just does the work

---

## What Checkout Does NOT Do

**Checkout is non-destructive and will NOT**:
- ❌ Auto-commit changes (only suggests)
- ❌ Delete any files
- ❌ Modify code
- ❌ Push to remote
- ❌ Close work efforts
- ❌ Change project state

**Checkout WILL**:
- ✅ Create documentation files
- ✅ Update devlog
- ✅ Generate summaries
- ✅ Review and report status
- ✅ Suggest next steps

---

## Best Practices

1. **Run at Session End**: Use `/checkout` when ending a session
2. **Review Output**: Check the summary and suggestions
3. **Commit if Ready**: Follow git suggestions if appropriate
4. **Start Next Session**: Use `/spin-up` or `/phase1` next time
5. **Reference Summaries**: Use checkout summaries for context

---

## Example Usage

### Standard End of Session
```
User: "/checkout"

AI: [Runs all phases, creates documentation, shows summary]

✅ Checkout complete!
```

### After Major Work
```
User: "We've done a lot. Let's checkout."

AI: [Comprehensive checkout with detailed statistics]

✅ Checkout complete! Consider committing these changes.
```

---

## Technical Details

### Files Created

1. **Session Statistics**: `_pyrite/phase1/session-stats-*.json`
2. **Checkpoint**: `_work_efforts/CHECKPOINT_*.md`
3. **Session Summary**: `_pyrite/checkout/session-*.md`
4. **Devlog Entry**: Updated in `_work_efforts/devlog.md`

### Dependencies

- Git (for status review)
- Session Stats module (for statistics)
- Checkpoint command (for checkpoint creation)
- Work Efforts MCP (for work effort updates)

### Execution Order

1. Statistics (needed for summary)
2. Checkpoint (needed for summary)
3. Summary (uses stats and checkpoint)
4. Documentation (updates devlog, work efforts)
5. Git review (final status check)
6. Completion (final summary)

---

## Error Handling

If any phase fails:
- Continue with remaining phases
- Report errors clearly
- Still create what's possible
- Don't fail entire checkout

---

## Related Commands

- **`/checkpoint`**: Creates checkpoint (used by checkout)
- **`/stats`**: Shows statistics (used by checkout)
- **`/spin-up`**: Quick orientation (use after checkout)
- **`/phase1`**: Comprehensive data gathering (use after checkout)

---

**This command ensures nothing is lost when ending a session and prepares everything for the next session.**
