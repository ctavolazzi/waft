# Recap and Review

**Capture the mindspace of this moment and generate a review document PDF.**

Creates comprehensive documentation of the current mindspace - thoughts, context, state, decisions, and observations - then generates a PDF document and opens it on your desktop.

**Use when:** Need to capture current state, document mindspace, create review PDF, or want a snapshot of the moment.

---

## Purpose

This command provides:
- **Mindspace Documentation**: Complete capture of current mental state and context
- **Review PDF Generation**: Beautiful PDF document of the mindspace
- **Desktop Opening**: Automatically opens PDF on your desktop
- **State Snapshot**: Complete picture of this moment in time
- **Context Preservation**: Saves important context for later review

---

## Philosophy

1. **Capture the Moment**: Document the mindspace as it exists right now
2. **Beautiful Documentation**: Create visually appealing PDF review
3. **Immediate Access**: Open PDF on desktop for instant review
4. **Complete Context**: Include everything relevant to current state
5. **Review-Ready**: Format optimized for review and reflection

---

## Execution Steps

### Step 1: Gather Mindspace Data

**Purpose**: Collect all relevant information about current state

**Actions**:
1. Analyze current conversation context
2. Gather session statistics and activity
3. Collect active files and work in progress
4. Extract key decisions and thoughts
5. Capture current goals and objectives
6. Document open questions and unknowns
7. Note current emotional/mental state indicators
8. Collect system state (git, files, etc.)

**Output**: Complete mindspace data structure

---

### Step 2: Generate Mindspace Document

**Purpose**: Create markdown document of mindspace

**Actions**:
1. Structure mindspace into sections:
   - **Moment**: Timestamp and context
   - **Current State**: What's happening now
   - **Thoughts**: Current thinking and observations
   - **Context**: Relevant background information
   - **Decisions**: Recent decisions and rationale
   - **Work in Progress**: Active work and tasks
   - **Questions**: Open questions and unknowns
   - **Next Steps**: Immediate next actions
   - **Reflections**: Observations and insights
2. Format as markdown with clear structure
3. Save to `_work_efforts/` directory

**Output**: Markdown mindspace document

---

### Step 3: Generate Review PDF

**Purpose**: Convert mindspace document to beautiful PDF

**Actions**:
1. Use LaTeX or PDF generation template
2. Apply professional styling
3. Include all mindspace sections
4. Add visual elements (headers, sections, formatting)
5. Generate PDF file
6. Save to output directory

**Output**: PDF document

---

### Step 4: Open PDF on Desktop

**Purpose**: Make PDF immediately accessible

**Actions**:
1. Use system command to open PDF:
   - macOS: `open [pdf_path]`
   - Windows: `start [pdf_path]`
   - Linux: `xdg-open [pdf_path]`
2. Verify PDF opened successfully
3. Display confirmation

**Output**: PDF opened on desktop

---

## What Gets Captured

### Current Moment
- Timestamp and date
- Session duration
- Time of day context
- Current activity

### Mental State
- Current thoughts and observations
- Mental state indicators
- Focus areas
- Energy levels (if available)

### Context
- Current work context
- Active files and projects
- Recent activity
- System state

### Decisions
- Recent decisions made
- Rationale and context
- Alternatives considered
- Impact assessment

### Work in Progress
- Active tasks
- Files being worked on
- Current objectives
- Progress indicators

### Questions
- Open questions
- Unknowns
- Areas needing investigation
- Unresolved issues

### Next Steps
- Immediate actions
- Planned work
- Goals and objectives
- Priorities

### Reflections
- Insights and observations
- Patterns noticed
- Learnings
- Meta-observations

---

## Output Format

### Markdown Document
- Location: `_work_efforts/MINDSPACE_REVIEW_YYYY-MM-DD_HHMM.md`
- Format: Structured markdown with sections
- Content: Complete mindspace documentation

### PDF Document
- Location: `_work_efforts/MINDSPACE_REVIEW_YYYY-MM-DD_HHMM.pdf`
- Format: Professional PDF with styling
- Content: Same as markdown, beautifully formatted
- Status: Automatically opened on desktop

---

## Integration

This command integrates with:
- **RecapManager**: For session data gathering
- **SessionStats**: For activity statistics
- **MemoryManager**: For active files and context
- **PDF Generation**: For PDF creation
- **System Commands**: For desktop opening

---

## Use Cases

### 1. End of Session Review
**Scenario**: Want to capture mindspace at end of work session

**Example**:
```
User: "/recap-and-review"
```

**Output**: PDF document of mindspace opened on desktop

---

### 2. Decision Point Documentation
**Scenario**: Need to document mindspace before making important decision

**Example**:
```
User: "/recap-and-review"
```

**Output**: PDF with current state, thoughts, and context for decision-making

---

### 3. Context Preservation
**Scenario**: Want to save current mindspace for later review

**Example**:
```
User: "/recap-and-review"
```

**Output**: PDF saved and opened, ready for review anytime

---

### 4. Reflection Moment
**Scenario**: Want to capture thoughts and observations

**Example**:
```
User: "/recap-and-review"
```

**Output**: PDF with reflections and insights

---

## Technical Details

### Mindspace Data Sources
- Conversation history
- Session statistics
- Active files
- Git status
- Work effort system
- Memory system
- Current context

### PDF Generation
- Uses LaTeX or PDF template
- Professional styling
- Clear structure
- Visual formatting

### Desktop Opening
- Platform-specific commands
- Automatic detection
- Error handling
- Confirmation display

---

## Example Output

```
📋 Recap and Review: Mindspace Documentation

✅ Mindspace captured
   • Current State: Active development
   • Thoughts: 5 key observations
   • Decisions: 3 recent decisions
   • Work in Progress: 2 active tasks
   • Questions: 2 open questions

✅ PDF Generated
   📄 Saved: _work_efforts/MINDSPACE_REVIEW_2026-01-15_1200.pdf
   🖥️  Opened on desktop

✅ Review ready for viewing
```

---

## When to Use

**Use `/recap-and-review` when**:
- ✅ Want to capture current mindspace
- ✅ Need review document PDF
- ✅ Want PDF opened on desktop
- ✅ End of session review
- ✅ Decision point documentation
- ✅ Context preservation
- ✅ Reflection moment

**Don't use `/recap-and-review` when**:
- ❌ Just need quick recap (use `/recap`)
- ❌ Just need status (use `/checkpoint`)
- ❌ Don't need PDF (use `/recap`)

---

**This command captures the complete mindspace of this moment and presents it as a beautiful PDF document ready for review on your desktop.**

--- End Command ---
