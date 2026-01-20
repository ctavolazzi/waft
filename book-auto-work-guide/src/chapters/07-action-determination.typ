= Action Determination

This chapter describes how Auto-Work determines the optimal action.

== Available Actions

Common action types:

- `status_transition`: Change work effort status
- `add_progress`: Add progress note
- `review`: Review work effort
- `review_todos`: Review and address TODOs
- `fix_issues`: Fix issues
- `review_changes`: Review recent changes

== Action Priority

Actions are prioritized:

- `high` → Highest priority
- `medium` → Medium priority
- `low` → Lowest priority

== Selection Process

1. Analyze available actions for selected work effort
2. Sort by priority (high > medium > low)
3. Select highest priority action

== Example

```
Available Actions:
  1. Address TODOs (HIGH priority) ✅ Selected
  2. Review changes (MEDIUM priority)
  3. Add progress note (LOW priority)
```

== Next Steps

Now let's explore the execution phase.
