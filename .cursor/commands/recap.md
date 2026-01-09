# Recap

**Conversation recap and session summary - capture what happened.**

Creates a comprehensive recap of the current conversation/session, extracting key points, decisions, accomplishments, and questions. Perfect for documenting work sessions, handoffs, or creating conversation summaries.

**Use when:** End of session, handoff preparation, or need detailed conversation summary.

---

## Purpose

This command provides:
- **Conversation Summary**: Complete summary of what was discussed
- **Key Points Extraction**: Important information highlighted
- **Decision Documentation**: Decisions made during conversation
- **Accomplishment Tracking**: What was completed
- **Question Tracking**: Open questions and unknowns
- **Next Steps**: What comes next

---

## Philosophy

1. **Capture Everything**: Don't miss important details
2. **Structure Clearly**: Organize information logically
3. **Actionable**: Include next steps and decisions
4. **Complete**: Full picture of the session
5. **Reusable**: Format that's useful for handoffs

---

## Execution Steps

### Step 1: Conversation Analysis
**Purpose**: Analyze the conversation to extract key information

**Actions**:
1. Review entire conversation history
2. Identify main topics discussed
3. Extract key decisions made
4. Note accomplishments and completions
5. Identify open questions or unknowns
6. Find action items and next steps

**Output**: Structured analysis of conversation

---

### Step 2: Recap Document Generation
**Purpose**: Create comprehensive recap document

**Actions**:
1. Generate markdown document with sections:
   - **Session Overview**: Date, duration, participants
   - **Topics Discussed**: Main subjects covered
   - **Decisions Made**: Key decisions with context
   - **Accomplishments**: Completed work and achievements
   - **Open Questions**: Unanswered questions
   - **Next Steps**: Action items and follow-ups
   - **Key Files**: Important files created/modified
   - **Notes**: Additional context or observations
2. Save to `_work_efforts/` directory
3. Use timestamped filename: `SESSION_RECAP_YYYY-MM-DD.md`

**Output**: Complete recap document

---

### Step 3: Summary Display
**Purpose**: Show recap summary in console

**Actions**:
1. Display key highlights from recap
2. Show file location
3. Provide quick reference

**Output**: Console summary

---

## What Gets Captured

### Session Information
- Date and time
- Duration (if available)
- Participants (AI + user)
- Session type/context

### Topics Discussed
- Main subjects covered
- Technical topics
- Decisions discussed
- Problems addressed

### Decisions Made
- Key decisions with context
- Rationale for decisions
- Alternatives considered
- Impact of decisions

### Accomplishments
- Completed tasks
- Files created/modified
- Features implemented
- Problems solved
- Tests written/passed

### Open Questions
- Unanswered questions
- Unknowns identified
- Areas needing investigation
- Blockers or issues

### Next Steps
- Action items
- Follow-up tasks
- Planned work
- Dependencies

### Key Files
- Important files created
- Significant modifications
- Configuration changes
- Documentation updates

---

## Output Format

### Console Output

```
📋 Recap: Conversation Summary

Session: 2026-01-07 21:30:00
Duration: ~45 minutes

Topics Discussed:
- Implemented /analyze command
- Created recap command
- Synced commands globally

Decisions Made:
- All commands should be global
- Recap command needed for session summaries

Accomplishments:
✅ Implemented analyze() method
✅ Added CLI commands
✅ Created recap command
✅ Synced commands globally

Open Questions:
- None

Next Steps:
1. Test recap command
2. Continue with planned work

📄 Recap saved: _work_efforts/SESSION_RECAP_2026-01-07.md
```

### Recap Document

The document includes:

```markdown
# Session Recap

**Date**: 2026-01-07
**Time**: 21:30:00
**Duration**: ~45 minutes
**Participants**: User, AI Assistant

---

## Topics Discussed

1. **Command Implementation**
   - Implemented `/analyze` command
   - Added `analyze()` method to Visualizer class
   - Created CLI commands in main.py

2. **Global Commands**
   - Discussed making all commands global
   - Created `/recap` command
   - Synced commands to global location

---

## Decisions Made

1. **All Commands Should Be Global**
   - Decision: Make all reusable commands global
   - Rationale: Commands are useful across all projects
   - Impact: Commands available everywhere

2. **Recap Command Needed**
   - Decision: Create `/recap` command for session summaries
   - Rationale: Need way to document conversations
   - Impact: Better session documentation

---

## Accomplishments

✅ **Implemented `/analyze` Command**
   - Added `analyze()` method to Visualizer class
   - Implemented 8 analysis phases
   - Created comprehensive report generation
   - Added CLI command support

✅ **Created `/recap` Command**
   - Defined command specification
   - Created command file
   - Ready for implementation

✅ **Synced Commands Globally**
   - Ran sync script
   - All commands now available globally
   - Updated documentation

---

## Open Questions

None

---

## Next Steps

1. Test `/recap` command implementation
2. Continue with planned work
3. Update documentation as needed

---

## Key Files

### Created
- `src/waft/core/visualizer.py` (analyze method)
- `.cursor/commands/recap.md`
- `_pyrite/analyze/analyze-2026-01-07-212705.md`

### Modified
- `src/waft/main.py` (added analyze and phase1 commands)
- `_work_efforts/devlog.md` (updated with implementation)

---

## Notes

- All commands successfully synced to global location
- Analyze command tested and working
- Recap command ready for use
```

---

## Use Cases

### 1. End of Session
**Scenario**: Finishing a work session, want to document what happened

**Example**:
```
User: "/recap"
```

**Output**: Complete session recap with all details

---

### 2. Handoff Preparation
**Scenario**: Preparing to hand off work to someone else

**Example**:
```
User: "/recap"
```

**Output**: Comprehensive recap for handoff

---

### 3. Decision Documentation
**Scenario**: Need to document important decisions made

**Example**:
```
User: "/recap"
```

**Output**: Decisions clearly documented with context

---

### 4. Progress Tracking
**Scenario**: Want to track what was accomplished

**Example**:
```
User: "/recap"
```

**Output**: Accomplishments clearly listed

---

## Integration with Other Commands

- **`/checkpoint`**: Status snapshot (`/recap` is conversation-focused)
- **`/phase1`**: Data gathering (`/recap` summarizes conversation)
- **`/analyze`**: Data analysis (`/recap` is conversation summary)
- **`/orient`**: Project startup (`/recap` is session end)

---

## When to Use

**Use `/recap` when**:
- ✅ End of work session
- ✅ Preparing for handoff
- ✅ Need conversation summary
- ✅ Want to document decisions
- ✅ Tracking accomplishments
- ✅ Creating session documentation

**Don't use `/recap` when**:
- ❌ Need quick status (use `/checkpoint`)
- ❌ Need data analysis (use `/analyze`)
- ❌ Need project overview (use `/phase1`)
- ❌ Mid-session (use at end)

---

## Technical Details

### Data Sources

Recap analyzes:
- Current conversation history
- Files created/modified in session
- Commands executed
- Decisions mentioned
- Questions asked
- Accomplishments stated

### Output Location

- **Default**: `_work_efforts/SESSION_RECAP_YYYY-MM-DD.md`
- **Custom**: Can specify output path if needed

### Format

- **Markdown**: Easy to read and edit
- **Structured**: Clear sections for easy scanning
- **Timestamped**: Unique filename per session
- **Complete**: All relevant information included

---

## Example Workflow

```
User: [Works on implementing feature]
User: [Makes decisions]
User: [Completes tasks]
User: "/recap"

AI: [Analyzes conversation]
AI: [Generates recap document]
AI: [Displays summary]

AI: 📋 Recap Complete
    📄 Saved: _work_efforts/SESSION_RECAP_2026-01-07.md
    ✅ Topics: 3 discussed
    ✅ Decisions: 2 made
    ✅ Accomplishments: 5 completed
    ✅ Next Steps: 3 identified

User: [Reviews recap document]
```

---

**This command captures the complete picture of your conversation - perfect for documentation, handoffs, and tracking progress.**

--- End Command ---
