= Execution Phase

This chapter describes the execution phase of Auto-Work.

== Execution Steps

1. Validate action safety
2. Run Empirica gate check
3. Run Pantheon Judge evaluation
4. Prepare execution instruction
5. Output JSON for Cursor AI
6. (Optional) Generate story
7. (Optional) Generate quest PDF

== Safety Validation

Before execution:

- Validate work effort ID format
- Check action type whitelist
- Sanitize command
- Run Empirica gate
- Run Judge evaluation

== JSON Output

Structured JSON output for Cursor AI:

```json
{
  "selected_work_effort": {
    "id": "WE-260118-abc1",
    "title": "Implement User Authentication",
    "path": "_work_efforts/WE-260118-abc1_implement_user_authentication"
  },
  "action": {
    "type": "review_todos",
    "label": "Address TODOs",
    "command": "Review and address TODOs in work effort WE-260118-abc1",
    "context": {
      "reason": "Work effort contains TODO items",
      "priority": "high"
    }
  },
  "execution_instruction": "Review and address TODOs in work effort WE-260118-abc1"
}
```

== AI Execution

Cursor AI reads the JSON and executes the command autonomously.

== Next Steps

Now let's explore Empirica integration.
