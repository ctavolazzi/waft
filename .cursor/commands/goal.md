# Goal

**Track larger goals, break them into steps, identify next actions.**

Manages larger objectives and goals, breaks them into actionable steps, tracks progress, and identifies what to do next. Helps maintain focus on bigger picture while managing incremental progress.

**Use when:** You have a larger objective, want to track progress toward a goal, need to identify next steps, or want to break down a big goal into manageable pieces.

---

## Purpose

Provides: goal definition, step breakdown, progress tracking, next step identification, goal prioritization.

---

## Command Categories

### Goal Management
1. **`/goal create`** - Create new goal with steps. Use when starting new larger objective.

2. **`/goal list`** - List all goals with status. Use when want to see all goals.

3. **`/goal show <name>`** - Show goal details and progress. Use when want details on specific goal.

4. **`/goal update <name>`** - Update goal progress or steps. Use when progress made on goal.

5. **`/goal next`** - Identify next step across all goals. Use when want to know what to do next.

---

## Goal Structure

```markdown
# Goal: [Name]

**Status**: Active/Completed/Paused
**Created**: YYYY-MM-DD
**Updated**: YYYY-MM-DD

## Objective
[What we're trying to achieve]

## Steps
1. [ ] Step 1 - [Description]
2. [ ] Step 2 - [Description]
3. [x] Step 3 - [Description] ✅

## Progress
- Completed: 1/3 steps
- Current: Working on Step 2
- Next: Complete Step 2, then move to Step 3

## Notes
[Any relevant notes or context]
```

---

## Usage Examples

### Create Goal
```
/goal create "Implement decision engine Phase 3"
```

### List Goals
```
/goal list
```

### Show Goal
```
/goal show "decision-engine-phase3"
```

### Update Progress
```
/goal update "decision-engine-phase3" --step 2 --complete
```

### Get Next Step
```
/goal next
```

---

## Integration

- **`/next`**: Uses goal data to identify next steps
- **`/checkpoint`**: Shows goal progress in status
- **`/resume`**: Loads goals when resuming work
- **`/continue`**: Reflects on goal progress

---

**This command helps track larger objectives and break them into actionable steps, maintaining focus on bigger picture while managing incremental progress.**
