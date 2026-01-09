# Checkpoint

**Create a situation report and status update for the current chat session.**

Captures the current state of the conversation, work, and project in a "good enough" checkpoint document. Updates relevant documentation (devlog, work efforts, etc.) with a rough pass over what's happening right now.

**Use when:** You want to document the current state, create a recovery point, or sync documentation with chat progress.

---

## Purpose

This command provides:
- **Situation Report (SITREP)**: Current state snapshot
- **Chat Recap**: Summary of conversation so far
- **Status Update**: Current work, todos, and progress
- **Documentation Sync**: Updates devlog and relevant files
- **Recovery Point**: Checkpoint file for future reference
- **"Good Enough" Approach**: Rough pass, not perfect

---

## Philosophy

1. **Capture Now**: Document current state, not perfect state
2. **Good Enough**: Rough pass is better than no pass
3. **Incremental**: Builds on previous checkpoints
4. **Contextual**: Focus on what matters right now
5. **Traceable**: Links to related work and documentation

---

## What Gets Captured

### 1. Chat Recap
- **Conversation Summary**: What was discussed
- **Key Decisions**: Important choices made
- **Questions Asked**: Open questions or unknowns
- **Tasks Completed**: What was finished
- **Tasks Started**: What was begun

### 2. Current State
- **Date/Time**: Current timestamp
- **Working Directory**: Current location
- **Git Status**: Branch, uncommitted changes, commits ahead/behind
- **Project Status**: Structure validity, version, integrity
- **Active Work**: Current work efforts and tickets
- **Todos**: Current todo list status

### 3. Work Progress
- **Files Changed**: Modified and new files
- **Work Efforts**: Active or recently completed
- **Tickets**: Status of related tickets
- **Documentation**: What docs were created/updated

### 4. Next Steps
- **Immediate Actions**: What to do next
- **Pending Work**: What's waiting
- **Blockers**: Anything blocking progress
- **Questions**: What needs clarification

---

## Execution Steps

1. **Get Current State**
   - Run `date` for timestamp
   - Run `pwd` for working directory
   - Run `git status` for git state
   - Run `waft verify` for project status (if applicable)
   - Check active work efforts via MCP
   - Check todos (if available)

2. **Recap Conversation**
   - Summarize chat history
   - Identify key topics
   - Extract decisions and actions
   - Note open questions

3. **Create Checkpoint File**
   - Generate filename: `CHECKPOINT_YYYY-MM-DD_[TOPIC].md`
   - Write checkpoint content
   - Include all captured information

4. **Update Devlog**
   - Add entry to `_work_efforts/devlog.md`
   - Include summary and link to checkpoint
   - Update with current date

5. **Update Work Efforts** (if applicable)
   - Update active work effort status
   - Add progress notes
   - Update ticket statuses

6. **Update Related Documentation**
   - Update any docs that were discussed
   - Add links to checkpoint
   - Sync status information

---

## Checkpoint File Format

**Location**: `_work_efforts/CHECKPOINT_YYYY-MM-DD_[TOPIC].md`

**Template**:
```markdown
# Checkpoint: [Topic/Summary]

**Date**: YYYY-MM-DD HH:MM:SS
**Session**: [Brief session description]
**Status**: ✅ Complete | 🚧 In Progress | ⏸️ Paused | ❓ Unknown

---

## Executive Summary

[One paragraph summary of current state]

---

## Chat Recap

### Conversation Summary
[What was discussed in this chat session]

### Key Decisions
- [Decision 1]
- [Decision 2]

### Questions Asked
- [Question 1]
- [Question 2]

### Tasks Completed
- [Task 1]
- [Task 2]

### Tasks Started
- [Task 1]
- [Task 2]

---

## Current State

### Environment
- **Date/Time**: [timestamp]
- **Working Directory**: [path]
- **Project**: [project name/version]

### Git Status
- **Branch**: [branch name]
- **Uncommitted Changes**: [count]
- **Commits Ahead**: [count]
- **Commits Behind**: [count]

### Project Status
- **Structure**: [valid/invalid]
- **Integrity**: [percentage]
- **Version**: [version number]

### Active Work
- **Work Efforts**: [list]
- **Tickets**: [list with status]
- **Todos**: [list]

---

## Work Progress

### Files Changed
- **Modified**: [list]
- **New**: [list]
- **Deleted**: [list]

### Work Efforts
- **Active**: [list]
- **Completed**: [list]
- **Paused**: [list]

### Documentation
- **Created**: [list]
- **Updated**: [list]

---

## Next Steps

### Immediate Actions
1. [Action 1]
2. [Action 2]

### Pending Work
- [Work item 1]
- [Work item 2]

### Blockers
- [Blocker 1] (if any)
- [Blocker 2] (if any)

### Questions
- [Question 1]
- [Question 2]

---

## Related Documentation

- [Link to devlog entry]
- [Link to work effort]
- [Link to other relevant docs]

---

**Checkpoint Created**: YYYY-MM-DD HH:MM:SS
```

---

## Devlog Entry Format

Add to `_work_efforts/devlog.md`:

```markdown
## YYYY-MM-DD - [Topic/Summary]

**Checkpoint**: [Link to checkpoint file]

### Summary
[Brief summary]

### Key Accomplishments
- [Accomplishment 1]
- [Accomplishment 2]

### Current State
- [State item 1]
- [State item 2]

### Next Steps
- [Next step 1]
- [Next step 2]

---
```

---

## Work Effort Updates

If active work effort exists:

1. **Update Status**: Add progress note
2. **Update Tickets**: Mark completed tickets
3. **Add Notes**: Document current progress
4. **Link Checkpoint**: Reference checkpoint file

---

## Topic Extraction

**How to determine checkpoint topic:**

1. **Primary Work**: What was the main focus?
   - Feature name
   - Bug fix
   - Documentation
   - System setup

2. **Session Theme**: What was the session about?
   - Engineering workflow
   - Command creation
   - Exploration
   - Implementation

3. **Key Achievement**: What was accomplished?
   - Feature completed
   - System verified
   - Documentation created

**Examples**:
- `CHECKPOINT_2026-01-07_verify_command_creation.md`
- `CHECKPOINT_2026-01-07_checkpoint_command_creation.md`
- `CHECKPOINT_2026-01-07_engineering_workflow.md`

---

## "Good Enough" Approach

This command prioritizes:
- ✅ **Speed over perfection**: Rough pass is fine
- ✅ **Completeness over polish**: Capture everything, refine later
- ✅ **Usefulness over beauty**: Functional over pretty
- ✅ **Context over detail**: What matters now

**Don't worry about**:
- Perfect formatting
- Complete details
- Exhaustive coverage
- Perfect grammar

**Do focus on**:
- Current state
- Key decisions
- Next steps
- Important context

---

## Best Practices

1. **Run Frequently**: Create checkpoints regularly
2. **Be Honest**: Document actual state, not ideal state
3. **Link Everything**: Connect to related work
4. **Update Devlog**: Always update devlog
5. **Keep It Brief**: Summary, not novel
6. **Focus on Now**: Current state, not history

---

## Example Usage

```markdown
User: "/checkpoint"

AI: Creating checkpoint...
- Recapping conversation
- Capturing current state
- Creating checkpoint file
- Updating devlog
- Updating work efforts

✅ Checkpoint created: CHECKPOINT_2026-01-07_verify_command_creation.md
```

---

## Related Commands

- `verify` - Verify information (may be used before checkpoint)
- `spin-up` - Quick orientation (may inform checkpoint)
- `explore` - Deep exploration (may create checkpoint)
- `engineering` - Full workflow (creates checkpoints at phases)

---

## Output

After execution, provides:
1. **Checkpoint File**: Created in `_work_efforts/`
2. **Devlog Entry**: Added to `devlog.md`
3. **Work Effort Updates**: Updated if applicable
4. **Summary**: Brief summary of what was captured

---

**This command is designed to be fast, useful, and "good enough". Don't overthink it - just capture the current state!**
