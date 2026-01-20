= Step-by-Step Walkthrough

This chapter provides a detailed walkthrough of Auto-Work execution from start to finish, with example outputs at each step.

== Prerequisites Check

Before starting, ensure:

- Work efforts exist in `_work_efforts/` directory
- At least one work effort is not `completed`
- (Optional) Empirica is initialized
- (Optional) Pantheon entities are available

== Step 1: Command Execution

Run the Auto-Work command:

```
/auto-work
```

*[Screenshot Placeholder: Terminal showing command execution]*

```
🤔 Thinking about work efforts...
```

== Step 2: System Initialization

The system initializes supporting systems:

=== Empirica Initialization

```
🔬 Empirica: Active and monitoring
```

If Empirica is not initialized:

```
⚠️  Empirica: Not initialized (continuing without epistemic tracking)
```

=== Pantheon Initialization

```
⚡ Pantheon: Summoning entities for guidance...

  ✅ Magistrate (Precedent & Proof)
  ✅ Judge (Judgment & Evaluation)
  ✅ TheReasoner (Reasoning Traces)
  ✅ GitHubGod (Repository State)
  ✅ Fae (Quests & Creativity)
  ✅ MissionControl (Coordination)
  ✅ Librarian (Knowledge & Records)
```

If Pantheon is unavailable:

```
⚠️  Pantheon: Not available (continuing without Pantheon guidance)
```

=== Campfire Initialization

```
🔥 Campfire: Ready for storytelling
```

=== D&D Campaign Initialization

```
⚔️  D&D Campaign: Initializing realm and quest system...

  ✅ Scenario Realm initialized
  ✅ Scenario Orchestrator ready
  ✅ Quest PDF Generator ready (Typst available)
```

*[Screenshot Placeholder: System initialization output]*

== Step 3: Work Effort Collection

The system gathers all work efforts:

```
📋 Found 15 work effort(s)
✅ 8 actionable work effort(s)
```

*[Screenshot Placeholder: Work effort collection output]*

== Step 4: Priority Scoring

For each actionable work effort, the system calculates priority scores:

```
🎯 Selecting best work effort to work on...

Calculating priorities...
  WE-260118-abc1: 230.0 points (active, HIGH, TODO, FIXME, 2 commits)
  WE-260118-def2: 150.0 points (active, MEDIUM, TODO)
  WE-260117-ghi3: 100.0 points (paused, HIGH)
  ...
```

*[Screenshot Placeholder: Priority scoring output]*

== Step 5: Work Effort Selection

The highest scoring work effort is selected:

```
✅ Selected: WE-260118-abc1
   Title: Implement User Authentication
   Status: active
   Priority Score: 230.0
```

*[Screenshot Placeholder: Selected work effort details]*

== Step 6: Action Analysis

The system analyzes available actions for the selected work effort:

```
🔍 Analyzing available actions...

Available actions:
  1. Address TODOs (HIGH priority)
     Reason: Work effort contains TODO items
  2. Review changes (MEDIUM priority)
     Reason: Recent changes detected
  3. Add progress note (LOW priority)
     Reason: Work effort is active
```

*[Screenshot Placeholder: Action analysis output]*

== Step 7: Action Selection

The highest priority action is selected:

```
✅ Best action: Address TODOs
   Reason: Work effort contains TODO items
   Command: Review and address TODOs in work effort WE-260118-abc1
```

*[Screenshot Placeholder: Selected action details]*

== Step 8: Safety Gates

The system runs safety checks:

=== Empirica Gate

```
🔬 Empirica Gate: Checking execution safety...
   Result: PROCEED
```

If gate returns `HALT`:

```
🔬 Empirica Gate: Checking execution safety...
   Result: HALT
   Reason: Operation requires human approval
   
❌ Execution halted by safety gate
```

=== Pantheon Judge

```
⚖️  Judge: Evaluating action safety...
   Verdict: PROVEN (confidence: 0.85)
   Reasoning: Action is safe to execute autonomously
```

*[Screenshot Placeholder: Safety gate results]*

== Step 9: Execution Preparation

The system prepares the execution instruction:

```
🚀 Preparing action...

✅ Work effort and action selected!
```

*[Screenshot Placeholder: Execution preparation output]*

== Step 10: JSON Output

The system outputs structured JSON for Cursor AI:

```
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
```

*[Screenshot Placeholder: JSON output]*

== Step 11: Execution Instruction

The system displays the execution instruction:

```
🚀 EXECUTING NOW...

============================================================
EXECUTION INSTRUCTION:
============================================================
Review and address TODOs in work effort WE-260118-abc1
============================================================

💡 Cursor AI: Execute the command above now.
```

*[Screenshot Placeholder: Execution instruction]*

== Step 12: AI Execution

Cursor AI executes the instruction, performing the actual work.

*[Screenshot Placeholder: AI execution in progress]*

== Step 13: Storytelling (Optional)

If Campfire is available, a story is told:

```
🔥 Campfire: Telling story around the campfire...
   Story ID: story-20260119-102530
   PDF: _pyrite/campfire/stories/story-20260119-102530.pdf
```

*[Screenshot Placeholder: Story generation output]*

== Step 14: Quest Generation (Optional)

If D&D campaign is available, a quest PDF is generated:

```
⚔️  D&D Campaign: Running scenario...
   Scenario Mode: encounter
   Quest PDF: _work_efforts/WE-260118-abc1/quest_20260119_102530.pdf
```

*[Screenshot Placeholder: Quest PDF generation]*

== Complete Example Output

Here's a complete example of Auto-Work execution:

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

🔍 Analyzing available actions...

✅ Best action: Address TODOs
   Reason: Work effort contains TODO items
   Command: Review and address TODOs in work effort WE-260118-abc1

🚀 Preparing action...

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

🚀 EXECUTING NOW...

============================================================
EXECUTION INSTRUCTION:
============================================================
Review and address TODOs in work effort WE-260118-abc1
============================================================

💡 Cursor AI: Execute the command above now.

🔥 Campfire: Story told around the campfire
   Story ID: story-20260119-102530
   PDF: _pyrite/campfire/stories/story-20260119-102530.pdf

⚔️  D&D Campaign: Quest PDF generated
   Quest: Quest: Implement User Authentication
   PDF: _work_efforts/WE-260118-abc1/quest_20260119_102530.pdf
```

*[Screenshot Placeholder: Complete terminal output]*

== Next Steps

Now that you've seen the complete walkthrough, let's explore usage examples in different scenarios.
