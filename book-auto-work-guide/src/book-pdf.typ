#set page(margin: (top: 2cm, bottom: 2cm, left: 2.5cm, right: 2cm))
#set text(font: "Times New Roman", size: 11pt)
#set heading(numbering: "1.", depth: 2)

#align(center)[
  #text(size: 24pt, weight: "bold")[WAFT Auto-Work]
  
  #text(size: 18pt)[Autonomous Work Effort Execution Guide]
  
  #v(1cm)
  
  #text(size: 12pt)[A comprehensive guide to the WAFT Auto-Work feature]
  
  #v(0.5cm)
  
  #text(size: 10pt)[WAFT System | AI Assistant]
  
  #text(size: 10pt)[January 2026]
]

#pagebreak()

= Introduction

The WAFT Auto-Work feature represents a significant advancement in autonomous project management. This system enables intelligent, hands-off execution of work efforts by analyzing priorities, selecting optimal tasks, and executing them autonomously with comprehensive safety mechanisms.

== Purpose of This Guide

This guide provides:

- *[Comprehensive Documentation]*: Complete explanation of how Auto-Work functions
- *[Step-by-Step Walkthrough]*: Detailed process flow from start to finish
- *[Usage Examples]*: Real-world scenarios with expected outputs
- *[Integration Details]*: How Auto-Work integrates with Empirica, Pantheon, Campfire, and D&D systems
- *[Safety Mechanisms]*: Security features and validation processes
- *[Troubleshooting]*: Common issues and solutions

== Who This Guide Is For

This guide is designed for:

- *[Developers]*: Understanding the technical implementation
- *[Project Managers]*: Learning how to leverage autonomous work execution
- *[System Administrators]*: Configuring and maintaining the system
- *[Users]*: Learning to use Auto-Work effectively

#pagebreak()

= What is Auto-Work?

Auto-Work is an autonomous work effort execution system that intelligently analyzes all available work efforts, calculates priorities, selects the best one to work on, determines the optimal action, and executes it autonomously.

== Core Concept

Auto-Work embodies the principle of *[autonomous decision-making]*: instead of manually selecting which work effort to tackle next, the system uses sophisticated algorithms to make that decision for you.

== The Problem It Solves

In complex projects with many work efforts, deciding what to work on next can be challenging:

- *[Too Many Options]*: Dozens or hundreds of work efforts to choose from
- *[Priority Confusion]*: Unclear which work effort is most important
- *[Context Switching]*: Time lost deciding between tasks
- *[Inconsistent Prioritization]*: Different criteria applied at different times
- *[Missed Opportunities]*: Important work efforts overlooked

Auto-Work solves these problems by:

1. *[Systematic Analysis]*: Evaluates all work efforts using consistent criteria
2. *[Intelligent Prioritization]*: Uses multi-factor scoring to rank work efforts
3. *[Autonomous Selection]*: Picks the best work effort automatically
4. *[Action Determination]*: Identifies the optimal action to take
5. *[Safe Execution]*: Executes with comprehensive safety checks

#pagebreak()

= Priority Scoring Algorithm

The priority scoring algorithm is the heart of Auto-Work's decision-making. It calculates a numerical score for each work effort, with higher scores indicating higher priority.

== Scoring Formula Overview

The total priority score is calculated as:

```
Total Score = Status Weight + Priority Level + Content Indicators + 
              Recent Activity + Empirica Adjustment + Pantheon Adjustment
```

== Factor 1: Status Weighting

Work effort status is the primary factor, as active work should be prioritized:

| Status | Points | Description |
|--------|--------|-------------|
| `active` | 100.0 | Currently in progress (highest priority) |
| `paused` | 50.0 | Temporarily stopped |
| `open` | 30.0 | Not yet started |
| `completed` | 0.0 | Finished (excluded from selection) |

*[Example]*: An `active` work effort starts with 100 points, while a `paused` one starts with 50.

== Factor 2: Priority Level

Explicit priority levels add to the base score:

| Priority | Points | Description |
|----------|--------|-------------|
| `CRITICAL` | +50.0 | Urgent, must be addressed |
| `HIGH` | +30.0 | Important, should be done soon |
| `MEDIUM` | +15.0 | Normal priority |
| `LOW` | +5.0 | Can wait |

#pagebreak()

= Step-by-Step Walkthrough

This chapter provides a detailed walkthrough of Auto-Work execution from start to finish, with example outputs at each step.

== Step 1: Command Execution

Run the Auto-Work command:

```
/auto-work
```

The system responds:

```
🤔 Thinking about work efforts...
```

== Step 2: System Initialization

The system initializes supporting systems:

=== Empirica Initialization

```
🔬 Empirica: Active and monitoring
```

=== Pantheon Initialization

```
⚡ Pantheon: Summoning entities for guidance...

  ✅ Magistrate (Precedent & Proof)
  ✅ Judge (Judgment & Evaluation)
  ✅ TheReasoner (Reasoning Traces)
  ✅ GitHubGod (Repository State)
```

== Step 3: Work Effort Collection

The system gathers all work efforts:

```
📋 Found 15 work effort(s)
✅ 8 actionable work effort(s)
```

== Step 4: Priority Scoring

For each actionable work effort, the system calculates priority scores and selects the highest scoring one:

```
✅ Selected: WE-260118-abc1
   Title: Implement User Authentication
   Status: active
```

== Step 5: Action Analysis

The system analyzes available actions:

```
✅ Best action: Address TODOs
   Reason: Work effort contains TODO items
   Command: Review and address TODOs in work effort WE-260118-abc1
```

== Step 6: Execution

The system outputs structured JSON for Cursor AI to execute:

```json
{
  "selected_work_effort": {
    "id": "WE-260118-abc1",
    "title": "Implement User Authentication"
  },
  "action": {
    "type": "review_todos",
    "label": "Address TODOs",
    "command": "Review and address TODOs in work effort WE-260118-abc1"
  }
}
```

#pagebreak()

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

== Empirica Safety Gates

Empirica provides epistemic safety gates:

| Result | Meaning | Action |
|--------|---------|--------|
| `PROCEED` | Safe to execute | ✅ Continue |
| `HALT` | Requires human approval | ❌ Stop |
| `BRANCH` | Needs investigation | ❌ Stop, investigate |
| `REVISE` | Approach needs revision | ❌ Stop, revise |

== Pantheon Judge

The Judge evaluates action safety:

- `PROVEN` with confidence > 0.9: ✅ Safe, proceed
- `DISPROVEN` with confidence > 0.9: ❌ Unsafe, halt

#pagebreak()

= Usage Examples

== Example 1: Simple Execution

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
```

== Example 2: Dry Run

*[Command]*:
```
/auto-work --dry-run
```

Shows what would be selected and executed without actually doing it.

== Example 3: With Full Integration

When Empirica, Pantheon, Campfire, and D&D are available:

```
🔬 Empirica: Active and monitoring
⚡ Pantheon: Summoning entities for guidance...
🔥 Campfire: Ready for storytelling
⚔️  D&D Campaign: Initializing realm and quest system...
```

#pagebreak()

= Integration Details

== Empirica Integration

Empirica provides:

- Epistemic state assessment
- Safety gate checks
- Finding logging
- Uncertainty tracking

== Pantheon Integration

Pantheon entities provide:

- *[Judge]*: Action safety evaluation
- *[Magistrate]*: Precedent search
- *[TheReasoner]*: Reasoning traces
- *[GitHubGod]*: Repository state
- *[Librarian]*: Knowledge base search

== Campfire Integration

After successful execution, Auto-Work tells a story around the campfire:

```
🔥 Campfire: Story told around the campfire
   Story ID: story-20260119-102530
   PDF: _pyrite/campfire/stories/story-20260119-102530.pdf
```

== D&D Campaign Integration

Auto-Work runs D&D scenarios and generates quest PDFs:

```
⚔️  D&D Campaign: Quest PDF generated
   Quest: Quest: Implement User Authentication
   PDF: _work_efforts/WE-260118-abc1/quest_20260119_102530.pdf
```

#pagebreak()

= Troubleshooting

== No Work Efforts Found

*[Problem]*: `❌ No work efforts found.`

*[Solution]*:
- Check that `_work_efforts/` directory exists
- Verify work effort directories follow `WE-YYMMDD-xxxx` format

== No Actionable Work Efforts

*[Problem]*: `❌ No actionable work efforts found (all completed).`

*[Solution]*:
- Create new work efforts
- Reopen paused work efforts

== Safety Gate Halt

*[Problem]*: `❌ Execution halted by safety gate`

*[Solution]*:
- Review Empirica gate reason
- Check Judge verdict
- Manually approve if safe

#pagebreak()

= Conclusion

This guide has covered the WAFT Auto-Work feature comprehensively, from basic usage to advanced integration.

== Key Takeaways

1. *[Auto-Work is intelligent]*: Uses sophisticated algorithms for prioritization
2. *[Auto-Work is safe]*: Multiple layers of security ensure safe operation
3. *[Auto-Work is integrated]*: Works seamlessly with Empirica, Pantheon, Campfire, and D&D
4. *[Auto-Work is flexible]*: Supports dry run, verbose mode, and customization

== Next Steps

- Try Auto-Work with `/auto-work --dry-run`
- Review priority scoring with `--verbose`
- Configure integrations (Empirica, Pantheon, Campfire, D&D)
- Monitor execution logs

== Resources

- WAFT Documentation: `docs/`
- Auto-Work Script: `scripts/auto_work.py`
- Command Reference: `.cursor/commands/auto-work.md`

Thank you for using WAFT Auto-Work!
