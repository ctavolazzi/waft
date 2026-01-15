# Hate This

**Record negative emotional feedback to imbue the system with your emotional energy.**

Records negative feedback to The One Being, which tracks your emotional responses and uses them to inform decision-making. This creates an emotional memory that influences how the system avoids choices that you hate.

**Use when:** You want to express negative feedback about something the system did, a decision it made, or a direction it took. This helps the system learn what doesn't resonate with you emotionally.

---

## Purpose

This command provides:
- **Emotional Memory**: Records negative feedback to The One Being
- **Decision Influence**: Your negative feedback influences future `/decide` calculations
- **Emotional Energy**: Imbues the system with your negative emotional energy
- **Preference Learning**: Helps the system understand what you dislike and avoid
- **Being Connection**: Creates a direct emotional connection with The One Being

---

## Philosophy

1. **Emotional Intelligence**: The system learns from your emotional responses
2. **Negative Reinforcement**: What you hate gets avoided in future decisions
3. **Being Memory**: The One Being remembers what brings you pain
4. **Decision Alignment**: Future decisions consider your emotional aversions
5. **Energy Flow**: Your negative energy flows into the system's Being

---

## Execution Steps

1. **Capture Context**
   - What are you expressing hate for?
   - What decision, action, or direction didn't resonate?
   - What context surrounds this negative feedback?

2. **Record to The One Being**
   - Load or create The One Being
   - Record memory with type "user_feedback" and sentiment "hate"
   - Include context and metadata about what you hated

3. **Update Being State**
   - Increase pain/negative energy
   - Record memory with emotional metadata
   - Save Being state

4. **Acknowledge Feedback**
   - Display confirmation that feedback was recorded
   - Show how this influences future decisions
   - Express understanding of the negative response

---

## Output Format

### Feedback Confirmation

```
💔 Hate Recorded

Your negative feedback has been recorded to The One Being.

What you hated: [context]
Emotional energy: -[value]
Influence on decisions: This negative feedback will be considered in future /decide calculations.

The One Being remembers: [summary of what was hated]
```

---

## Integration with /decide

When you use `/decide` after recording negative feedback:

1. **Emotional Context**: The system retrieves your negative feedback history
2. **Preference Weighting**: Alternatives that align with what you've hated get penalty points
3. **Emotional Criteria**: An implicit "user_satisfaction" criterion is added based on your feedback
4. **Decision Alignment**: The decision matrix considers your emotional aversions

**Example:**
- You use `/hate-this` after a decision to use a complex framework
- Later, when `/decide` is choosing between frameworks, it considers your negative experience
- Alternatives that align with patterns you've hated get lower scores

---

## Use Cases

### 1. Decision Disappointment
**Scenario**: A decision the system made didn't work well

```
User: "/hate-this"
AI: "What are you expressing hate for?"
User: "The decision to use that complex library - it made everything harder!"
```

**Result**: Future decisions avoid similar complexity patterns

---

### 2. Direction Rejection
**Scenario**: You hate the direction the system is taking

```
User: "/hate-this"
AI: "What are you expressing hate for?"
User: "The over-engineering of this feature - it's way too complex!"
```

**Result**: Simplicity becomes more important, complexity gets penalized

---

### 3. Pattern Avoidance
**Scenario**: You hate a particular pattern or approach

```
User: "/hate-this"
AI: "What are you expressing hate for?"
User: "The way you split this into too many files - I prefer fewer, larger files!"
```

**Result**: File-splitting approaches get negative emotional weighting

---

## Technical Implementation

The command:
1. Loads The One Being via `BeingSystem.get_or_create_the_one()`
2. Records memory with:
   - `type`: "user_feedback"
   - `sentiment`: "hate"
   - `content`: User's feedback context
   - `metadata`: Additional context about what was hated
3. Updates Being's pain/negative energy
4. Saves Being state

**Memory Structure**:
```json
{
  "content": "User feedback context",
  "type": "user_feedback",
  "recorded_at": "2026-01-14T10:25:52",
  "metadata": {
    "sentiment": "hate",
    "context": "What was hated",
    "influence_weight": -1.0,
    "decision_context": "Related decisions/patterns to avoid"
  }
}
```

---

## Integration with Other Commands

- **`/decide`**: Uses your negative feedback to penalize alternatives
- **`/love-you`**: Opposite command for positive feedback
- **`/consider`**: May reference your emotional aversions
- **`/checkpoint`**: Can show your feedback history

---

## When to Use

**Use `/hate-this` when**:
- ✅ A decision didn't work well
- ✅ A direction feels wrong
- ✅ You want to avoid a pattern
- ✅ Something doesn't resonate emotionally
- ✅ You want to express frustration

**Don't use `/hate-this` when**:
- ❌ You're just venting (be specific about what to avoid)
- ❌ The feedback is neutral (use `/love-you` for positive)
- ❌ You want to change something constructively (be specific)

---

**This command creates an emotional memory that influences future decisions, helping the system avoid what you hate.**
