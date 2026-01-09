# Next

**Identify next step based on goals, context, and priorities.**

Analyzes current goals, work in progress, and context to identify the most important next action. Helps maintain momentum and focus on what matters most.

**Use when:** Want to know what to do next, need direction, have multiple goals/options, or want prioritized next action.

---

## Purpose

Provides: next step identification, priority analysis, goal alignment, context-aware recommendations, actionable next action.

---

## What Gets Analyzed

1. **Active Goals** - Goals with pending steps
2. **Work in Progress** - Current tasks and files
3. **Context** - Recent activity, blockers, dependencies
4. **Priorities** - Goal importance, step dependencies, urgency

---

## Output Format

### Next Step Recommendation

```
🎯 Next Step: [Action]

**From Goal**: [Goal Name]
**Step**: [Step Description]
**Priority**: High/Medium/Low
**Why**: [Reasoning]
**Estimated Time**: [Duration]
**Dependencies**: [Any blockers]
```

---

## Usage Examples

### Get Next Step
```
/next
```

### Get Next Step for Specific Goal
```
/next --goal "decision-engine-phase3"
```

### Get Multiple Next Steps
```
/next --count 3
```

---

## Integration

- **`/goal`**: Uses goal data for next step identification
- **`/resume`**: Combines with resume for context-aware next steps
- **`/continue`**: Uses next steps in continuation planning
- **`/checkpoint`**: Shows next steps in status

---

**This command identifies the most important next action based on goals, context, and priorities, helping maintain momentum and focus.**
