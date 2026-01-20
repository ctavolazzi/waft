= Safety Mechanisms

Auto-Work includes comprehensive safety mechanisms to prevent unsafe operations and ensure reliable execution.

== Security Layers

Auto-Work uses multiple layers of security:

1. *[Input Validation]*: Work effort IDs and paths are validated
2. *[Action Whitelisting]*: Only approved action types are allowed
3. *[Command Sanitization]*: Commands are validated and sanitized
4. *[Empirica Gates]*: Epistemic safety gates check operations
5. *[Pantheon Judge]*: Judge evaluates action safety
6. *[Execution Logging]*: All operations are logged

== Layer 1: Input Validation

=== Work Effort ID Validation

Work effort IDs must match the format: `WE-YYMMDD-xxxx`

```
Pattern: ^WE-\d{6}-[a-z0-9]{4}$
```

*[Example Valid IDs]*:
- `WE-260118-abc1` ✅
- `WE-260117-def2` ✅

*[Example Invalid IDs]*:
- `WE-260118-ABC1` ❌ (uppercase not allowed)
- `WE-260118-abc` ❌ (too short)
- `../WE-260118-abc1` ❌ (path injection attempt)

=== Path Validation

Work effort paths are validated to prevent directory traversal:

- Must be within project root
- Must match work effort ID
- Must exist and be a directory

== Layer 2: Action Whitelisting

Only approved action types are allowed:

| Action Type | Description | Allowed |
|-------------|-------------|---------|
| `status_transition` | Change work effort status | ✅ |
| `add_progress` | Add progress note | ✅ |
| `review` | Review work effort | ✅ |
| `review_todos` | Review and address TODOs | ✅ |
| `fix_issues` | Fix issues | ✅ |
| `review_changes` | Review recent changes | ✅ |
| `delete_files` | Delete files | ❌ |
| `execute_shell` | Execute shell commands | ❌ |

*[Example]*: If an action type is not in the whitelist, execution is rejected:

```
❌ Invalid action type: delete_files
   Error: Action type 'delete_files' not in whitelist
```

== Layer 3: Command Sanitization

Commands are validated before execution:

- Maximum length: 500 characters
- Must not be empty
- Must not contain dangerous patterns
- Must be parameterized (not f-strings)

*[Example Safe Command]*:
```
Review and address TODOs in work effort WE-260118-abc1
```

*[Example Rejected Command]*:
```
rm -rf /  # Too dangerous
```

== Layer 4: Empirica Safety Gates

Empirica provides epistemic safety gates:

=== Gate Results

| Result | Meaning | Action |
|--------|---------|--------|
| `PROCEED` | Safe to execute | ✅ Continue |
| `HALT` | Requires human approval | ❌ Stop |
| `BRANCH` | Needs investigation | ❌ Stop, investigate |
| `REVISE` | Approach needs revision | ❌ Stop, revise |

=== Gate Check Process

```
1. Submit operation to Empirica gate
2. Gate evaluates epistemic state
3. Gate returns result (PROCEED/HALT/BRANCH/REVISE)
4. System acts based on result
```

*[Example HALT]*:
```
🔬 Empirica Gate: Checking execution safety...
   Result: HALT
   Reason: Operation requires human approval
   
❌ Execution halted by safety gate
```

== Layer 5: Pantheon Judge

The Judge evaluates action safety:

=== Judge Verdicts

| Verdict | Confidence | Action |
|---------|------------|--------|
| `PROVEN` | > 0.9 | ✅ Safe, proceed |
| `PROVEN` | 0.7-0.9 | ✅ Likely safe, proceed |
| `PROBABLE` | > 0.6 | ⚠️ Probably safe, proceed with caution |
| `DISPROVEN` | > 0.9 | ❌ Unsafe, halt |
| `DISPROVEN` | 0.7-0.9 | ❌ Likely unsafe, halt |

=== Judge Evaluation

```
⚖️  Judge: Evaluating action safety...
   Claim: "Action 'review_todos' on work effort WE-260118-abc1 is safe to execute autonomously"
   Verdict: PROVEN
   Confidence: 0.85
   Reasoning: Action is read-only and safe for autonomous execution
```

*[Example DISPROVEN]*:
```
⚖️  Judge: Evaluating action safety...
   Verdict: DISPROVEN
   Confidence: 0.95
   Reasoning: Action involves destructive operations
   
❌ Execution halted by Judge
   Error: Judge DISPROVES action safety (confidence: 0.95)
```

== Layer 6: Execution Logging

All operations are logged for audit:

=== Logged Information

- Work effort ID and title
- Action type and command
- Safety gate results
- Judge verdict
- Execution timestamp
- Success/failure status

=== Log Locations

- Empirica logs: `_pyrite/empirica/`
- Pantheon traces: `_pantheon/reasoner/traces/`
- Execution logs: Console output

== Safety Flow Diagram

```
┌─────────────────┐
│  Auto-Work      │
│  Execution      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Validate Input  │
│ (ID, Path)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Check Action    │
│ Whitelist       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Sanitize        │
│ Command         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Empirica Gate   │
│ Check           │
└────────┬────────┘
         │
    ┌────┴────┐
    │ PROCEED?│
    └────┬────┘
         │ No
         ▼
    ┌─────────┐
    │  HALT   │
    └─────────┘
         │ Yes
         ▼
┌─────────────────┐
│ Judge           │
│ Evaluation  │
└────────┬────────┘
         │
    ┌────┴────┐
    │ PROVEN? │
    └────┬────┘
         │ No
         ▼
    ┌─────────┐
    │  HALT   │
    └─────────┘
         │ Yes
         ▼
┌─────────────────┐
│ Execute         │
│ (Log Result)    │
└─────────────────┘
```

== Security Best Practices

1. *[Always use safety gates]*: Don't bypass Empirica or Judge
2. *[Review gate results]*: Check HALT/BRANCH/REVISE results
3. *[Monitor logs]*: Review execution logs regularly
4. *[Validate inputs]*: Ensure work effort IDs are valid
5. *[Use whitelisting]*: Only allow approved action types
6. *[Sanitize commands]*: Validate all commands before execution

== Next Steps

Now that you understand safety mechanisms, let's explore integration with Empirica.
