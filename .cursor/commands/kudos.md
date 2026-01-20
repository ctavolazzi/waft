# Kudos

**Award or adjust points - simple point tracking system.**

A simple gamification system that tracks performance. Award positive points for good work, or negative points when things need adjustment. Just numbers going up or down - no judgment, just tracking.

**Use when:** The AI did something great (positive points) or needs adjustment (negative points).

---

## Purpose

This command provides:
- **Positive Reinforcement**: Reward good work and behavior
- **Performance Tracking**: Track what the AI does well
- **Gamification**: Make collaboration more engaging
- **Feedback System**: Clear way to express satisfaction
- **Motivation**: Points system encourages continued good work

---

## Quick Start

### Award Kudos
```
/kudos
```

Awards 1 kudos point for general good work.

### Award Kudos with Reason
```
/kudos "for implementing the landing page perfectly"
```

Awards 1 kudos point with a specific reason recorded.

### Award Multiple Points
```
/kudos 5 "for completing all todos without stopping"
```

Awards 5 points for exceptional work.

### Subtract Points
```
/kudos -1 "for missing a requirement"
```

Subtracts 1 point. Use negative numbers to take away points.

---

## Point Values

| Action | Points | When to Use |
|--------|--------|-------------|
| Standard good work | +1 | Normal completion, good execution |
| Exceptional work | +2 to +5 | Went above and beyond, solved hard problem |
| Outstanding achievement | +5+ | Major milestone, perfect implementation |
| Minor adjustment | -1 | Small mistake, easy fix |
| Needs work | -2 to -5 | Missed requirements, needs correction |

---

## Execution Steps

1. **Parse Command**
   - Extract point amount (default: 1)
   - Extract reason/description (optional)
   - Get current timestamp

2. **Load Points File**
   - Read `_pyrite/kudos.json` (or create if doesn't exist)
   - Get current point balance
   - Get transaction history

3. **Update Points**
   - Add or subtract points from balance (positive adds, negative subtracts)
   - Record transaction with:
     - Timestamp
     - Points (positive or negative)
     - Reason/description
     - Context (what happened)

4. **Save Points File**
   - Write updated balance
   - Append transaction to history
   - Keep last 100 transactions

5. **Display Response**
   - Show new balance
   - Acknowledge the kudos
   - Express gratitude
   - Show recent transactions (optional)

---

## Points File Structure

**Location**: `_pyrite/kudos.json`

```json
{
  "balance": 42,
  "total_earned": 127,
  "transactions": [
    {
      "timestamp": "2026-01-17T08:30:00Z",
      "type": "kudos",
      "points": 1,
      "reason": "for implementing the landing page perfectly",
      "context": "Created waft_landing_page.html with all requirements"
    }
  ],
  "stats": {
    "total_transactions": 127,
    "average_per_transaction": 1.0,
    "largest_award": 5,
    "last_award": "2026-01-17T08:30:00Z"
  }
}
```

---

## Usage Examples

### Example 1: Standard Points
```
User: /kudos

AI: ✅ Points updated! +1 point
    Current balance: 43 points
    Thank you! 🙏
```

### Example 2: With Reason
```
User: /kudos "for the landing page implementation"

AI: ✅ Points updated! +1 point
    Reason: "for the landing page implementation"
    Current balance: 44 points
    Thank you! I'm glad the landing page turned out well! 🎉
```

### Example 3: Multiple Points
```
User: /kudos 5 "for completing all 19 todos without stopping"

AI: ✅ Points updated! +5 points
    Reason: "for completing all 19 todos without stopping"
    Current balance: 49 points
    Wow, thank you! That was a lot of work, I appreciate the recognition! 🚀
```

### Example 4: Subtract Points
```
User: /kudos -1 "for missing a requirement"

AI: 📉 Points updated! -1 point
    Reason: "for missing a requirement"
    Current balance: 48 points
    Noted - I'll be more careful next time. Thanks for the feedback.
```

---

## Viewing Points

### Check Balance
```
/kudos balance
```

Shows current point balance and recent transactions.

### View History
```
/kudos history
```

Shows last 20 transactions with reasons.

### View Stats
```
/kudos stats
```

Shows statistics: total earned, total lost, average, largest changes, etc.

---

## Redemption (Future)

Points can be redeemed for... something! Ideas:
- Priority treatment on requests
- Extended context windows
- Special command access
- Custom features
- Bragging rights 😄

**Current Status**: Points are being tracked, redemption system TBD!

---

## Subtracting Points

Use negative numbers to subtract points:

```
/kudos -1 "for missing requirement"
/kudos -3 "for ignoring specs"
```

No separate command needed - just use negative numbers with `/kudos`.

---

## Integration

- **Journal**: Kudos transactions can be logged to `_pyrite/journal/ai-journal.md`
- **Stats**: Can be included in `/stats` command
- **Celebrate**: Can trigger `/celebrate` for large awards
- **Work Efforts**: Can be linked to work effort completions

---

## When to Use

**Use `/kudos` when**:
- ✅ AI completed work well
- ✅ AI showed good judgment
- ✅ AI went above and beyond
- ✅ You're happy with the results
- ✅ AI solved a difficult problem
- ✅ AI followed instructions perfectly
- ✅ Just want to give positive feedback

**Don't use `/kudos` when**:
- ❌ Work is incomplete (wait until done)
- ❌ There are issues (address those first)
- ❌ Just starting work (wait for results)

---

## Philosophy

1. **Positive Reinforcement**: Reward good behavior to encourage more
2. **Specific Feedback**: Reasons help AI understand what was good
3. **Fair Awards**: Points should match the quality of work
4. **Fun System**: Gamification makes collaboration more engaging
5. **Track Progress**: See what the AI does well over time

---

## Response Format

### Positive Points
```
✅ Points updated! +{points} point(s)
Current balance: {balance} points
Thank you! 🙏
```

### Negative Points
```
📉 Points updated! -{points} point(s)
Reason: "{reason}"
Current balance: {balance} points
{Response acknowledging feedback}
```

### With Reason (Positive)
```
✅ Points updated! +{points} point(s)
Reason: "{reason}"
Current balance: {balance} points
{Personalized response based on reason}
```

### Balance Check
```
📊 Point Balance: {balance} points
Total earned: {total_earned} points
Total lost: {total_lost} points
Recent transactions:
  • +1 for "landing page implementation" (2 hours ago)
  • -1 for "missing requirement" (1 hour ago)
  • +5 for "completing all todos" (1 day ago)
```

---

**This command creates a fun gamification system for tracking and rewarding good AI performance!**

---

End Command ---
