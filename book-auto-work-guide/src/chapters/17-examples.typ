= Usage Examples

This chapter provides real-world examples of Auto-Work in different scenarios.

== Example 1: Simple Execution

*[Scenario]*: You have multiple work efforts and want Auto-Work to select and execute the best one.

*[Command]*:
```
/auto-work
```

*[Output]*:
```
🤔 Thinking about work efforts...

📋 Found 5 work effort(s)
✅ 3 actionable work effort(s)

🎯 Selecting best work effort to work on...

✅ Selected: WE-260118-abc1
   Title: Fix Critical Bug in Authentication
   Status: active

🔍 Analyzing available actions...

✅ Best action: Fix Issues
   Reason: Work effort contains bug references
   Command: Review and fix issues in work effort WE-260118-abc1

🚀 Preparing action...

✅ Work effort and action selected!

============================================================
AUTO-WORK RESULT (JSON):
============================================================
{
  "selected_work_effort": {
    "id": "WE-260118-abc1",
    "title": "Fix Critical Bug in Authentication",
    "path": "_work_efforts/WE-260118-abc1_fix_critical_bug"
  },
  "action": {
    "type": "fix_issues",
    "label": "Fix Issues",
    "command": "Review and fix issues in work effort WE-260118-abc1",
    "context": {
      "reason": "Work effort contains bug references",
      "priority": "high"
    }
  },
  "execution_instruction": "Review and fix issues in work effort WE-260118-abc1"
}
============================================================
```

*[Screenshot Placeholder: Example 1 output]*

== Example 2: Dry Run Before Execution

*[Scenario]*: You want to see what Auto-Work would select before actually executing.

*[Command]*:
```
/auto-work --dry-run
```

*[Output]*:
```
🤔 Thinking about work efforts...

📋 Found 5 work effort(s)
✅ 3 actionable work effort(s)

🎯 Selecting best work effort to work on...

✅ Selected: WE-260118-abc1
   Title: Fix Critical Bug in Authentication
   Status: active

🔍 Analyzing available actions...

✅ Best action: Fix Issues
   Reason: Work effort contains bug references
   Command: Review and fix issues in work effort WE-260118-abc1

🔍 DRY RUN - Would execute:
   Review and fix issues in work effort WE-260118-abc1
```

*[Screenshot Placeholder: Example 2 dry run output]*

== Example 3: With Empirica and Pantheon

*[Scenario]*: Auto-Work with full integration (Empirica, Pantheon, Campfire, D&D).

*[Command]*:
```
/auto-work
```

*[Output]*:
```
🤔 Thinking about work efforts...

🔬 Empirica: Active and monitoring

⚡ Pantheon: Summoning entities for guidance...

  ✅ Magistrate (Precedent & Proof)
  ✅ Judge (Judgment & Evaluation)
  ✅ TheReasoner (Reasoning Traces)
  ✅ GitHubGod (Repository State)
  ✅ Librarian (Knowledge & Records)

🔥 Campfire: Ready for storytelling

⚔️  D&D Campaign: Initializing realm and quest system...

  ✅ Scenario Realm initialized
  ✅ Scenario Orchestrator ready
  ✅ Quest PDF Generator ready (Typst available)

📋 Found 15 work effort(s)
✅ 8 actionable work effort(s)

🎯 Selecting best work effort to work on...

✅ Selected: WE-260118-abc1
   Title: Implement User Authentication
   Status: active
   Priority Score: 230.0

🔍 Analyzing available actions...

✅ Best action: Address TODOs
   Reason: Work effort contains TODO items
   Command: Review and address TODOs in work effort WE-260118-abc1

🚀 Preparing action...

🔬 Empirica Gate: PROCEED
⚖️  Judge: PROVEN (confidence: 0.85)

✅ Work effort and action selected!

============================================================
AUTO-WORK RESULT (JSON):
============================================================
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
============================================================

🔥 Campfire: Story told around the campfire
   Story ID: story-20260119-102530
   PDF: _pyrite/campfire/stories/story-20260119-102530.pdf

⚔️  D&D Campaign: Quest PDF generated
   Quest: Quest: Implement User Authentication
   PDF: _work_efforts/WE-260118-abc1/quest_20260119_102530.pdf
```

*[Screenshot Placeholder: Example 3 full integration output]*

== Example 4: Safety Gate Halt

*[Scenario]*: Empirica safety gate halts execution due to high risk.

*[Command]*:
```
/auto-work
```

*[Output]*:
```
🤔 Thinking about work efforts...

🔬 Empirica: Active and monitoring

📋 Found 5 work effort(s)
✅ 3 actionable work effort(s)

🎯 Selecting best work effort to work on...

✅ Selected: WE-260118-xyz9
   Title: Delete Production Database
   Status: active

🔍 Analyzing available actions...

✅ Best action: Execute Deletion
   Reason: Work effort is ready for execution
   Command: Execute deletion in work effort WE-260118-xyz9

🚀 Preparing action...

🔬 Empirica Gate: HALT
   Reason: Operation requires human approval

❌ Execution halted by safety gate
   Error: Empirica gate: Operation requires human approval
   Gate Result: HALT
```

*[Screenshot Placeholder: Example 4 safety halt]*

== Example 5: No Actionable Work Efforts

*[Scenario]*: All work efforts are completed.

*[Command]*:
```
/auto-work
```

*[Output]*:
```
🤔 Thinking about work efforts...

📋 Found 5 work effort(s)
✅ 0 actionable work effort(s)

❌ No actionable work efforts found (all completed).
```

*[Screenshot Placeholder: Example 5 no actionable work efforts]*

== Example 6: Verbose Mode

*[Scenario]*: You want detailed logging to understand priority scoring.

*[Command]*:
```
/auto-work --verbose
```

*[Output]* (excerpt):
```
🤔 Thinking about work efforts...

📋 Found 5 work effort(s)
✅ 3 actionable work effort(s)

🎯 Selecting best work effort to work on...

Calculating priority for WE-260118-abc1:
  Status: active → 100.0 points
  Priority: HIGH → +30.0 points
  Content: TODO found → +20.0 points
  Content: FIXME found → +25.0 points
  Git activity: 2 commits → +10.0 points
  Empirica: PROCEED → +10.0 points
  Judge: PROVEN (0.85) → +15.0 points
  Total: 230.0 points

Calculating priority for WE-260118-def2:
  Status: active → 100.0 points
  Priority: MEDIUM → +15.0 points
  Content: TODO found → +20.0 points
  Git activity: 1 commit → +5.0 points
  Total: 140.0 points

✅ Selected: WE-260118-abc1 (230.0 points)
```

*[Screenshot Placeholder: Example 6 verbose output]*

== Example 7: Multiple Work Efforts with Different Priorities

*[Scenario]*: You have work efforts with varying priorities and statuses.

*[Work Efforts]*:
- WE-260118-abc1: active, CRITICAL, TODO, FIXME
- WE-260118-def2: active, HIGH, TODO
- WE-260117-ghi3: paused, HIGH
- WE-260116-jkl4: open, MEDIUM

*[Command]*:
```
/auto-work --dry-run
```

*[Expected Selection]*: WE-260118-abc1 (highest score due to CRITICAL priority and multiple content indicators)

*[Screenshot Placeholder: Example 7 priority comparison]*

== Best Practices from Examples

1. *[Use dry run first]*: Always test with `--dry-run` before actual execution
2. *[Check safety gates]*: Review Empirica and Judge results
3. *[Monitor verbose output]*: Use `--verbose` to understand decisions
4. *[Review JSON output]*: Check the structured output for accuracy
5. *[Verify execution]*: Confirm the AI executed the intended action

== Next Steps

Now that you've seen various examples, let's explore troubleshooting common issues.
