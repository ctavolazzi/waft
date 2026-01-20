= Basic Usage

This chapter covers the fundamental usage of Auto-Work, including command syntax and basic examples.

== Command Syntax

The basic command is:

```
/auto-work
```

This command:

1. Analyzes all work efforts
2. Selects the best one
3. Determines the optimal action
4. Prepares execution instruction
5. Outputs JSON for Cursor AI to execute

== Command Options

=== Dry Run

To see what would be done without executing:

```
/auto-work --dry-run
```

*[Screenshot Placeholder: Dry run output]*

This is useful for:

- Understanding what Auto-Work would select
- Verifying priority scoring
- Testing without making changes
- Learning how the system works

=== Verbose Output

For detailed logging:

```
/auto-work --verbose
```

*[Screenshot Placeholder: Verbose output showing detailed logs]*

Verbose mode shows:

- Detailed priority calculations
- Empirica gate details
- Pantheon entity interactions
- Action analysis details
- Safety gate results

=== Project Path

To specify a different project path:

```
/auto-work --path /path/to/project
```

== Basic Example

Here's a simple example:

```
$ /auto-work

🤔 Thinking about work efforts...

🔬 Empirica: Active and monitoring

⚡ Pantheon: Summoning entities for guidance...

  ✅ Magistrate (Precedent & Proof)
  ✅ Judge (Judgment & Evaluation)
  ✅ TheReasoner (Reasoning Traces)
  ✅ GitHubGod (Repository State)

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
```

*[Screenshot Placeholder: Complete basic example output]*

== Dry Run Example

Here's what a dry run looks like:

```
$ /auto-work --dry-run

🤔 Thinking about work efforts...

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

🔍 DRY RUN - Would execute:
   Review and address TODOs in work effort WE-260118-abc1
```

*[Screenshot Placeholder: Dry run example]*

== What Happens After Execution

After Auto-Work outputs the execution instruction:

1. *[Cursor AI reads the JSON]*: Parses the structured output
2. *[AI executes the command]*: Performs the actual work
3. *[Work effort is updated]*: Progress is recorded
4. *[Story is told]*: (Optional) Campfire generates a story
5. *[Quest PDF is generated]*: (Optional) D&D campaign creates a quest

== Common Use Cases

=== Daily Work Session

Start your day with Auto-Work:

```
$ /auto-work
```

This automatically selects and starts work on the highest priority item.

=== Before Committing

Use dry run to see what would be worked on:

```
$ /auto-work --dry-run
```

=== Debugging Priority

Use verbose mode to understand priority scoring:

```
$ /auto-work --verbose
```

== Next Steps

Now that you understand basic usage, let's explore command options in detail.
