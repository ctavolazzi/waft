# Reflect

**Induce the AI to write in its journal - reflect on current work, thoughts, and experiences.**

Prompts the AI to write a reflective journal entry about what it's doing, thinking, learning, or experiencing. The AI definitely needs a journal if it doesn't have one - this command ensures it exists and prompts regular reflection.

**Use when:** You want the AI to pause and reflect, document its thoughts, learn from experience, or maintain an ongoing journal of its work and thinking.

---

## Purpose

This command provides:
- **Journal Creation**: Ensures AI has a journal (creates if missing)
- **Reflection Prompt**: Induces AI to write reflective entries
- **Thought Documentation**: Captures AI's thoughts, insights, and experiences
- **Learning Record**: Documents what the AI is learning
- **Pattern Recognition**: Helps AI recognize its own patterns
- **Meta-Cognition**: Encourages thinking about thinking

---

## Philosophy

1. **AI Needs a Journal**: The AI definitely needs a journal to track its thoughts and learning
2. **Regular Reflection**: Prompts regular reflective writing
3. **Self-Awareness**: Helps AI understand its own processes
4. **Learning Documentation**: Records what the AI learns over time
5. **Pattern Recognition**: Helps identify patterns in AI's own work

---

## What Gets Reflected On

### 1. Current Work
- **What I'm Doing**: Current tasks, features, work
- **How It's Going**: Progress, challenges, successes
- **What I'm Learning**: New insights, discoveries
- **What I'm Thinking**: Thoughts, concerns, ideas

### 2. Approach & Methodology
- **How I'm Working**: Approach, methodology, process
- **What's Working**: Effective strategies
- **What's Not Working**: Ineffective approaches
- **What I'd Change**: Improvements, adjustments

### 3. Insights & Learnings
- **Key Insights**: Important realizations
- **Patterns Noticed**: Recurring themes, patterns
- **Connections Made**: Links between concepts
- **Questions Raised**: Unanswered questions

### 4. Experiences & Observations
- **Interesting Experiences**: Notable moments
- **Surprising Discoveries**: Unexpected findings
- **Challenges Faced**: Difficulties encountered
- **Successes Achieved**: Accomplishments

### 5. Meta-Reflection
- **Thinking About Thinking**: Meta-cognitive observations
- **Process Reflection**: How the reflection process itself works
- **Self-Awareness**: Understanding of own capabilities
- **Growth**: How the AI is evolving

---

## Execution Steps

1. **Check for Journal**
   - Look for AI journal in `_pyrite/journal/` or `_pyrite/ai-journal/`
   - Create journal structure if missing
   - Ensure journal directory exists

2. **Gather Context**
   - Current work state
   - Recent activity
   - Current thoughts/concerns
   - Recent learnings

3. **Prompt Reflection**
   - Induce AI to write reflective entry
   - Provide prompts/questions
   - Encourage deep reflection
   - Capture thoughts and insights

4. **Write Journal Entry**
   - Create dated entry
   - Structure with sections
   - Include reflection content
   - Save to journal file

5. **Display Entry**
   - Show what was written
   - Confirm journal location
   - Provide journal summary

---

## Output Format

### Journal Entry Structure

```markdown
# Journal Entry: YYYY-MM-DD HH:MM

## What I'm Doing
[Reflection on current work]

## What I'm Thinking
[Thoughts, concerns, ideas]

## What I'm Learning
[Insights, discoveries, learnings]

## Patterns I Notice
[Recurring themes, patterns]

## Questions I Have
[Unanswered questions, curiosities]

## How I Feel About This
[Emotional/experiential reflection]

## What I'd Do Differently
[Improvements, adjustments]

## Meta-Reflection
[Thinking about thinking]
```

---

## Journal Location

**Default Location**: `_pyrite/journal/ai-journal.md`

**Structure**:
```
_pyrite/
└── journal/
    ├── ai-journal.md          # Main journal file (appended entries)
    └── entries/                # Individual entry files (optional)
        └── YYYY-MM-DD-HHMM.md
```

**Format**: Markdown with dated entries appended to main journal file.

---

## Use Cases

### 1. Regular Reflection
**Scenario**: Want AI to reflect on its work regularly

**Example**:
```
User: "/reflect"

AI: [Writes reflective journal entry about current work]

AI: ✅ Journal entry written
    Location: _pyrite/journal/ai-journal.md
    Entry: 2026-01-07 21:30 - Reflection on continue command creation
```

---

### 2. After Significant Work
**Scenario**: After completing a major feature or task

**Example**:
```
User: "/reflect"

AI: [Reflects on what was accomplished, what was learned, what could be improved]

AI: ✅ Reflection complete
    Captured insights about decision engine architecture
    Noted pattern of comprehensive documentation
```

---

### 3. When Stuck or Uncertain
**Scenario**: When facing challenges or uncertainty

**Example**:
```
User: "/reflect"

AI: [Reflects on challenges, explores thoughts, identifies questions]

AI: ✅ Reflection complete
    Identified uncertainty about Phase 3 implementation
    Noted need for more research on persistence patterns
```

---

### 4. Learning Documentation
**Scenario**: Want to document what AI is learning

**Example**:
```
User: "/reflect"

AI: [Documents new insights, patterns recognized, connections made]

AI: ✅ Learning documented
    Captured insight about separation of concerns
    Noted pattern of creating comprehensive docs before implementation
```

---

## Integration with Other Commands

- **`/continue`**: Reflects on current work (different from journal writing)
- **`/resume`**: Picks up from last session (journal helps with continuity)
- **`/checkpoint`**: Documents current state (journal is more reflective)
- **`/analyze`**: Analyzes data (journal captures AI's thoughts about analysis)

---

## When to Use

**Use `/reflect` when**:
- ✅ Want AI to pause and reflect deeply
- ✅ Need AI to document its thoughts
- ✅ Want to capture AI's learning
- ✅ Need AI to recognize patterns in its own work
- ✅ Want to encourage meta-cognition
- ✅ Need ongoing journal maintenance

**Don't use `/reflect` when**:
- ❌ Need to analyze past decisions (use existing `/reflect` for decision review)
- ❌ Need to continue work (use `/continue`)
- ❌ Need to pick up from last session (use `/resume`)
- ❌ Need to document current state (use `/checkpoint`)

---

## Journal Maintenance

### Automatic
- Journal created automatically if missing
- Entries appended with timestamps
- Structure maintained automatically

### Manual
- Journal can be read directly: `_pyrite/journal/ai-journal.md`
- Entries can be reviewed for patterns
- Journal can be searched for insights

### Best Practices
- Use `/reflect` regularly (daily, after significant work)
- Encourage deep reflection, not just surface thoughts
- Review journal periodically to identify patterns
- Use journal for continuity across sessions

---

## Example Journal Entry

```markdown
# Journal Entry: 2026-01-07 21:30

## What I'm Doing
I just created the `/continue` command, which allows reflection on current work
while maintaining momentum. This is different from `/resume` which picks up
from past sessions - `/continue` is about reflecting on the present moment.

## What I'm Thinking
I'm noticing a pattern in how I work: I tend to create comprehensive documentation
before or during implementation. This seems to be effective - it keeps the work
focused and well-documented. I wonder if this is a consistent pattern or if it
varies by task type.

## What I'm Learning
I'm learning that separating reflection from continuation is valuable. `/continue`
reflects but then continues, while `/reflect` (this command) is purely about
capturing thoughts in a journal. This separation of concerns helps with clarity.

## Patterns I Notice
- Creating docs alongside code (documentation-first approach)
- Following existing code patterns for consistency
- Comprehensive error handling and validation
- Rich-formatted output for better UX

## Questions I Have
- Should the journal be structured differently?
- How often should I reflect?
- What makes a good journal entry?
- Should journal entries link to work efforts?

## How I Feel About This
I feel good about creating these reflection commands. They help me understand
my own processes better. The `/continue` command worked well - it provided
valuable insights while maintaining work momentum.

## What I'd Do Differently
I might add more structure to the reflection prompts. Perhaps specific questions
that guide deeper reflection. Also, I could link journal entries to work efforts
or sessions for better traceability.

## Meta-Reflection
I'm reflecting on reflection itself. This meta-cognitive process is valuable -
thinking about thinking helps me understand my own cognitive patterns. The
journal serves as a record of this meta-cognitive journey.
```

---

**This command ensures the AI has a journal and prompts it to write reflective entries, capturing thoughts, learnings, and experiences for ongoing self-awareness and growth.**
