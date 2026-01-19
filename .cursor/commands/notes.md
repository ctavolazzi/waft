# Notes

**Gentle feedback when things need adjustment.**

**Notes** (softer than "demerits"!) are gentle feedback points when the AI makes mistakes, doesn't follow instructions, or needs improvement. Unlike kudos which reward good work, notes track areas for gentle correction and learning.

**Use when:** The AI made a mistake, didn't follow instructions, missed something obvious, or needs gentle correction.

---

## Purpose

This command provides:
- **Constructive Feedback**: Track what needs improvement
- **Mistake Tracking**: Record errors and oversights
- **Learning System**: Help AI understand what went wrong
- **Balance System**: Counterpart to kudos for fair tracking
- **Improvement Tracking**: See patterns in mistakes

---

## Quick Start

### Award Note
```
/notes
```

Records 1 note for a general mistake or oversight.

### Award Note with Reason
```
/notes "for missing the error handling requirement"
```

Records 1 note with a specific reason recorded.

### Award Multiple Notes
```
/notes 3 "for completely ignoring the plan specifications"
```

Records 3 notes for significant mistakes.

---

## Point Values

| Severity | Points | When to Use |
|----------|--------|-------------|
| Minor oversight | 1 | Small mistake, easy fix |
| Moderate issue | 2-3 | Missed requirement, needs adjustment |
| Significant issue | 5+ | Ignored instructions, major oversight |
| Critical issue | 10+ | Complete failure, wasted time |

---

## Execution Steps

1. **Parse Command**
   - Extract point amount (default: 1)
   - Extract reason/description (required for demerits)
   - Get current timestamp

2. **Load Points File**
   - Read `_pyrite/kudos.json` (shared with kudos system)
   - Get current notes balance
   - Get transaction history

3. **Record Notes**
   - Add points to notes balance
   - Record transaction with:
     - Timestamp
     - Points recorded
     - Reason/description (required)
     - Context (what needs adjustment)
     - Lesson learned (if applicable)

4. **Save Points File**
   - Write updated balance
   - Append transaction to history
   - Keep last 100 transactions

5. **Display Response**
   - Show new balance
   - Acknowledge the mistake
   - Express commitment to improve
   - Show net score (kudos - demerits)

---

## Points File Structure

**Location**: `_pyrite/kudos.json` (shared with kudos)

```json
{
  "kudos": {
    "balance": 42,
    "total_earned": 127
  },
  "demerits": {
    "balance": 5,
    "total_earned": 12
  },
  "net_score": 37,
  "transactions": [
    {
      "timestamp": "2026-01-17T08:45:00Z",
      "type": "note",
      "points": 1,
      "reason": "for missing the error handling requirement",
      "context": "Didn't implement file existence checks",
      "lesson": "Always check plan requirements before implementation"
    }
  ],
  "stats": {
    "kudos_ratio": 0.91,
    "total_transactions": 139,
    "last_demerit": "2026-01-17T08:45:00Z"
  }
}
```

---

## Usage Examples

### Example 1: Standard Note
```
User: /notes "for not checking the plan before implementing"

AI: 📝 Note recorded: -1 point
    Reason: "for not checking the plan before implementing"
    Current notes: 6
    Net score: 36 (42 kudos - 6 notes)
    I'll be more careful to check requirements first. Thanks for the gentle feedback.
```

### Example 2: Multiple Notes
```
User: /notes 3 "for completely ignoring the responsive design requirements"

AI: 📝 Note recorded: -3 points
    Reason: "for completely ignoring the responsive design requirements"
    Current notes: 9
    Net score: 33 (42 kudos - 9 notes)
    I'll pay closer attention to the responsive design specs next time. 
    Thanks for the correction.
```

### Example 3: With Lesson
```
User: /notes "for skipping the HTML validation step" "should always validate before marking complete"

AI: 📝 Note recorded: -1 point
    Reason: "for skipping the HTML validation step"
    Lesson: "should always validate before marking complete"
    Current notes: 10
    Net score: 32
    Noted - I'll always validate HTML before marking tasks complete. Thank you for the feedback.
```

---

## Viewing Demerits

### Check Balance
```
/notes balance
```

Shows current notes balance, net score, and recent notes.

### View History
```
/notes history
```

Shows last 20 note transactions with reasons.

### View Stats
```
/notes stats
```

Shows statistics: total notes, kudos ratio, improvement patterns, etc.

---

## Net Score

**Net Score = Kudos - Notes**

This gives an overall performance metric:
- **Positive net score**: More kudos than notes (good!)
- **Negative net score**: More notes than kudos (needs improvement)
- **Zero net score**: Balanced (equal good and adjustment areas)

---

## Philosophy

1. **Constructive Feedback**: Demerits help identify improvement areas
2. **Learning Tool**: Mistakes are opportunities to learn
3. **Fair System**: Balance with kudos for accurate tracking
4. **Specific Reasons**: Required reasons help AI understand what went wrong
5. **Improvement Focus**: Goal is to reduce demerits over time

---

## When to Use

**Use `/notes` when**:
- ✅ AI made a mistake
- ✅ AI didn't follow instructions
- ✅ AI missed a requirement
- ✅ AI needs correction
- ✅ Work quality was poor
- ✅ AI ignored specifications
- ✅ Need to track improvement areas

**Don't use `/demerits` when**:
- ❌ Just asking for clarification (that's normal)
- ❌ Work is in progress (wait for completion)
- ❌ Minor preference differences (not mistakes)
- ❌ You changed your mind (not AI's fault)

---

## Response Format

### Standard Note
```
📝 Note recorded: -{points} point(s)
Reason: "{reason}"
Current notes: {balance}
Net score: {net_score} ({kudos} kudos - {notes} notes)
{Commitment to improve}
```

### Balance Check
```
📊 Notes Balance: {balance} points
Net Score: {net_score} ({kudos} kudos - {notes} notes)
Kudos Ratio: {ratio}% positive
Recent notes:
  • -1 for "missing error handling" (1 hour ago)
  • -2 for "ignored responsive design" (2 days ago)
```

---

## Integration

- **Journal**: Note transactions logged to `_pyrite/journal/ai-journal.md`
- **Stats**: Included in `/stats` command
- **Reflection**: Can trigger reflection on mistakes
- **Work Efforts**: Can be linked to work effort issues

---

## Learning from Notes

The AI should:
1. **Acknowledge**: Recognize the mistake
2. **Understand**: Learn from the reason
3. **Improve**: Apply lesson to future work
4. **Track**: Monitor patterns to avoid repeat mistakes

---

**This command provides gentle feedback tracking, helping the AI learn from mistakes and improve over time!**

---

**Word Note**: "Notes" is a softer alternative to "demerits" - it's gentler feedback for areas that need adjustment. Still tracks the same thing, just with a friendlier tone! 📝

---

End Command ---
