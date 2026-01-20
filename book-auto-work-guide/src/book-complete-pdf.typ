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

#set heading(numbering: "1.")

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

== What You'll Learn

By the end of this guide, you will understand:

1. How Auto-Work analyzes and prioritizes work efforts
2. The priority scoring algorithm and its factors
3. How safety gates prevent unsafe operations
4. Integration with epistemic tracking (Empirica)
5. Integration with decision support (Pantheon)
6. Storytelling integration (Campfire)
7. D&D campaign integration for quest generation
8. How to use Auto-Work effectively in your workflow

== Prerequisites

Before using Auto-Work, ensure you have:

- WAFT installed and configured
- Work efforts in `_work_efforts/` directory
- (Optional) Empirica initialized for epistemic tracking
- (Optional) Pantheon entities configured for decision support
- (Optional) Campfire configured for storytelling
- (Optional) D&D campaign system configured for quest generation

== Document Structure

This guide is organized into five parts:

*[Part I: Introduction & Overview]* - What Auto-Work is and its key features

*[Part II: How It Works]* - Deep dive into the architecture and algorithms

*[Part III: Integration & Safety]* - Empirica, Pantheon, Campfire, D&D, and safety mechanisms

*[Part IV: Usage Guide]* - How to use Auto-Work with examples and walkthroughs

*[Part V: Advanced Topics]* - Customization, best practices, and future enhancements

== Getting Started

To get started with Auto-Work, run:

```
/auto-work
```

Or to see what would be done without executing:

```
/auto-work --dry-run
```

For detailed output:

```
/auto-work --verbose
```

Let's begin by understanding what Auto-Work is and how it can transform your workflow.


#pagebreak()


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

== Key Characteristics

=== Autonomous

Auto-Work operates independently, making decisions without human intervention. It analyzes, selects, and prepares execution instructions autonomously.

=== Intelligent

The system uses sophisticated algorithms considering:

- Work effort status (active, paused, open, completed)
- Priority levels (CRITICAL, HIGH, MEDIUM, LOW)
- Content indicators (TODOs, FIXMEs, bugs)
- Recent activity (git commits)
- Epistemic state (Empirica)
- Precedent analysis (Pantheon)
- Repository context (GitHubGod)

=== Safe

Multiple safety mechanisms ensure safe operation:

- Empirica safety gates (PROCEED/HALT/BRANCH/REVISE)
- Pantheon Judge evaluation
- Action type whitelisting
- Work effort ID validation
- Command sanitization
- Execution logging

=== Integrated

Auto-Work integrates seamlessly with:

- *[Empirica]*: Epistemic tracking and safety gates
- *[Pantheon]*: Decision support entities (Judge, Magistrate, TheReasoner, GitHubGod, Librarian, MissionControl, Fae)
- *[Campfire]*: Storytelling around the campfire
- *[D&D Campaign]*: Quest PDF generation from scenarios

== How It Differs from Manual Work

=== Manual Work Flow

```
1. Review all work efforts
2. Manually assess priorities
3. Select a work effort
4. Determine what action to take
5. Execute the action
```

=== Auto-Work Flow

```
1. System analyzes all work efforts
2. Calculates priority scores automatically
3. Selects best work effort automatically
4. Determines optimal action automatically
5. Prepares execution instruction
6. AI executes the action
```

== Use Cases

Auto-Work is ideal for:

- *[Hands-Off Execution]*: Let the system work autonomously
- *[Intelligent Prioritization]*: Need consistent, multi-factor prioritization
- *[Large Projects]*: Many work efforts to manage
- *[Continuous Progress]*: Keep work moving forward automatically
- *[Learning Systems]*: Systems that learn from execution patterns

== What Auto-Work Does NOT Do

Auto-Work does not:

- Execute destructive operations without safety checks
- Bypass security validations
- Work on completed work efforts
- Execute actions outside the whitelist
- Ignore Empirica safety gates

== Next Steps

Now that you understand what Auto-Work is, let's explore its key features in detail.


#pagebreak()


Auto-Work includes several key features that make it powerful and reliable.

== Intelligent Prioritization

Auto-Work uses a sophisticated multi-factor scoring algorithm to prioritize work efforts:

- Status weighting (active > paused > open)
- Priority levels (CRITICAL > HIGH > MEDIUM > LOW)
- Content indicators (TODOs, FIXMEs, bugs)
- Recent activity (git commits)
- Epistemic state (Empirica)
- Precedent analysis (Pantheon)

== Autonomous Selection

The system automatically selects the best work effort without human intervention:

- Analyzes all available work efforts
- Calculates priority scores
- Selects highest scoring work effort
- Determines optimal action
- Prepares execution instruction

== Safety Mechanisms

Multiple layers of security ensure safe operation:

- Input validation (work effort IDs, paths)
- Action whitelisting (only approved actions)
- Command sanitization (validate commands)
- Empirica safety gates (PROCEED/HALT/BRANCH/REVISE)
- Pantheon Judge evaluation
- Execution logging

== Integration Support

Auto-Work integrates with multiple WAFT systems:

- *[Empirica]*: Epistemic tracking and safety gates
- *[Pantheon]*: Decision support entities
- *[Campfire]*: Storytelling around the campfire
- *[D&D Campaign]*: Quest PDF generation

== Flexible Execution

Multiple execution modes:

- *[Normal]*: Execute immediately
- *[Dry Run]*: Preview without executing
- *[Verbose]*: Detailed logging output

== Graceful Degradation

System continues to work even if optional components are unavailable:

- Empirica unavailable: Continues without epistemic tracking
- Pantheon unavailable: Continues without decision support
- Campfire unavailable: Continues without storytelling
- D&D unavailable: Continues without quest generation

== Comprehensive Logging

All operations are logged for audit and debugging:

- Work effort selection
- Priority calculations
- Safety gate results
- Execution outcomes
- Story generation
- Quest creation

== Next Steps

Now that you understand the key features, let's explore the system architecture.


#pagebreak()


This chapter describes the architecture of the Auto-Work system.

== Component Overview

Auto-Work consists of several components:

1. *[Work Effort Collector]*: Gathers all work efforts
2. *[Priority Scorer]*: Calculates priority scores
3. *[Work Effort Selector]*: Selects best work effort
4. *[Action Analyzer]*: Analyzes available actions
5. *[Action Selector]*: Selects optimal action
6. *[Safety Validator]*: Validates safety
7. *[Execution Preparer]*: Prepares execution instruction
8. *[Integration Manager]*: Manages integrations

== Data Flow

```
┌──────────────────┐
│  Work Efforts    │
│  Directory       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Work Effort     │
│  Collector       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Priority        │
│  Scorer          │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Work Effort     │
│  Selector        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Action          │
│  Analyzer        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Action          │
│  Selector        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Safety          │
│  Validator       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Execution       │
│  Preparer        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  JSON Output     │
│  (Cursor AI)     │
└──────────────────┘
```

== Integration Points

=== Empirica Integration

- Epistemic state assessment
- Safety gate checks
- Finding logging
- Uncertainty tracking

=== Pantheon Integration

- Judge: Action safety evaluation
- Magistrate: Precedent search
- TheReasoner: Reasoning traces
- GitHubGod: Repository state
- Librarian: Knowledge base search
- MissionControl: Mission coordination

=== Campfire Integration

- Story generation
- Narrative creation
- PDF output

=== D&D Campaign Integration

- Scenario execution
- Quest markdown generation
- Quest PDF generation

== File Structure

```
scripts/
  auto_work.py          # Main script
  show_me.py            # Work effort collection
  work_dashboard.py     # Action analysis

src/waft/
  core/
    empirica.py         # Empirica integration
    science/
      oracle.py         # Oracle integration
  pantheon.py           # Pantheon entities
  core/
    campfire.py         # Campfire integration
    dnd_scenario/       # D&D campaign
```

== Next Steps

Now that you understand the architecture, let's dive into the priority scoring algorithm.


#pagebreak()


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

*[Example]*: A `CRITICAL` work effort gets +50 points, while `MEDIUM` gets +15.

== Factor 3: Content Indicators

The system analyzes work effort content for indicators of work needed:

| Indicator | Points | Description |
|-----------|--------|-------------|
| Contains `TODO` | +20.0 | Tasks to be done |
| Contains `FIXME` | +25.0 | Issues to be fixed |
| Contains `bug`/`error` | +15.0 | Bugs or errors mentioned |

*[Example]*: A work effort with both `TODO` and `FIXME` gets +45 points.

== Factor 4: Recent Activity

Recent git commits indicate active work:

- +5.0 points per commit in last 7 days
- Maximum: 20.0 points (capped at 4 commits)

*[Example]*: A work effort with 3 commits in the last week gets +15 points.

== Factor 5: Empirica Adjustment

When Empirica is available, the system uses epistemic gates to adjust priority:

| Gate Result | Adjustment | Description |
|-------------|------------|-------------|
| `PROCEED` | +10.0 | High confidence, ready to proceed |
| `HALT` | +20.0 | Requires attention, boost priority |
| `BRANCH` | +15.0 | Needs investigation, moderate boost |
| `REVISE` | 0.0 | No adjustment |
| `None` | 0.0 | Empirica unavailable |

*[Example]*: If Empirica gate returns `HALT`, the work effort gets +20 points.

== Factor 6: Pantheon Adjustments

Pantheon entities provide additional context:

=== Judge Evaluation

The Judge evaluates work effort readiness:

- `PROVEN` with confidence > 0.7: +15.0 points
- `DISPROVEN` with confidence > 0.7: -10.0 points
- `PROBABLE` with confidence > 0.6: +8.0 points

=== Magistrate Precedents

Similar work efforts found:

- +5.0 points per proven precedent (max 3 precedents)

=== Librarian Knowledge Base

Work effort referenced in knowledge base:

- +3.0 points per related record (max 3 records)

=== GitHubGod Repository State

Work effort branch matches current branch:

- +10.0 points if branch matches

== Complete Example Calculation

Let's calculate the score for a work effort:

*[Work Effort Details]*:
- Status: `active` → 100.0 points
- Priority: `HIGH` → +30.0 points
- Contains `TODO` → +20.0 points
- Contains `FIXME` → +25.0 points
- 2 commits in last 7 days → +10.0 points
- Empirica gate: `PROCEED` → +10.0 points
- Judge: `PROVEN` (confidence 0.8) → +15.0 points
- Magistrate: 2 proven precedents → +10.0 points
- GitHubGod: Branch matches → +10.0 points

*[Total Score]*: 100 + 30 + 20 + 25 + 10 + 10 + 15 + 10 + 10 = *[230.0 points]*

== Score Comparison

Work efforts are sorted by total score, with the highest scoring work effort selected.

== Score Visualization

```
Work Effort A: ████████████████████ 230.0 (Selected)
Work Effort B: ████████████ 150.0
Work Effort C: ████████ 100.0
Work Effort D: ████ 50.0
```

== Important Notes

- Completed work efforts always score 0.0 and are excluded
- Scores are calculated dynamically on each run
- Empirica and Pantheon adjustments are optional (graceful degradation)
- Content analysis is case-insensitive
- Git activity is limited to the last 7 days

== Next Steps

Now that you understand priority scoring, let's see how work efforts are selected.


#pagebreak()


This chapter describes how Auto-Work selects the best work effort.

== Selection Process

1. Collect all work efforts
2. Filter out completed work efforts
3. Calculate priority scores
4. Sort by score (highest first)
5. Select highest scoring work effort

== Filtering

Completed work efforts are excluded:

- Status: `completed` → Score: 0.0 → Excluded

== Sorting

Work efforts are sorted by total priority score:

```
Highest Score → Selected
Second Highest → Not selected
Third Highest → Not selected
...
```

== Selection Example

```
Work Effort Scores:
  WE-260118-abc1: 230.0 points ✅ Selected
  WE-260118-def2: 150.0 points
  WE-260117-ghi3: 100.0 points
  WE-260116-jkl4: 50.0 points
```

== Next Steps

Now let's explore action determination.


#pagebreak()


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


#pagebreak()


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


#pagebreak()


Auto-Work integrates with Empirica for epistemic tracking and safety gates.

== What is Empirica?

Empirica is an epistemic self-assessment system that tracks:

- Knowledge state (what you know)
- Uncertainty levels
- Engagement metrics
- Execution state
- Learning progress

== Integration Points

=== Priority Adjustment

Empirica gates inform priority scoring:

- `PROCEED`: +10.0 points (high confidence)
- `HALT`: +20.0 points (requires attention)
- `BRANCH`: +15.0 points (needs investigation)
- `REVISE`: 0.0 points (no adjustment)

=== Safety Gates

Empirica provides safety gates before execution:

```
Gate Check → PROCEED/HALT/BRANCH/REVISE → Action
```

=== Finding Logging

Auto-Work logs findings to Empirica:

- Work effort selection
- Action execution
- Safety gate results
- Story generation
- Quest creation

== Example Integration

```
🔬 Empirica: Active and monitoring

🔬 Empirica Gate: Checking execution safety...
   Result: PROCEED
   
✅ Execution approved by Empirica gate
```

== Next Steps

Now let's explore Pantheon integration.


#pagebreak()


Auto-Work integrates with Pantheon entities for decision support.

== Pantheon Entities

=== Judge

Evaluates action safety:

- Verdict: PROVEN/DISPROVEN/PROBABLE
- Confidence: 0.0-1.0
- Reasoning: Explanation

=== Magistrate

Searches for precedents:

- Similar work efforts
- Proven patterns
- Historical outcomes

=== TheReasoner

Creates reasoning traces:

- Decision reasoning
- Context capture
- Outcome tracking

=== GitHubGod

Provides repository context:

- Current branch
- Repository state
- Branch matching

=== Librarian

Searches knowledge base:

- Related records
- Knowledge base presence
- Context enrichment

=== MissionControl

Coordinates missions:

- Mission monitoring
- Work effort tracking
- Coordination patterns

== Integration Example

```
⚡ Pantheon: Summoning entities for guidance...

  ✅ Magistrate (Precedent & Proof)
  ✅ Judge (Judgment & Evaluation)
  ✅ TheReasoner (Reasoning Traces)
  ✅ GitHubGod (Repository State)
  ✅ Librarian (Knowledge & Records)

⚖️  Judge: Evaluating action safety...
   Verdict: PROVEN
   Confidence: 0.85
   Reasoning: Action is safe for autonomous execution
```

== Next Steps

Now let's explore Campfire integration.


#pagebreak()


Auto-Work integrates with Campfire to tell stories around the campfire.

== What is Campfire?

Campfire is a storytelling system that creates narratives about work efforts and actions.

== Integration

After successful execution, Auto-Work:

1. Creates story input from work effort and action
2. Calls Campfire to tell the story
3. Generates story PDF
4. Logs story metadata

== Story Content

Stories include:

- Work effort details (ID, title, status, priority)
- Action taken (type, label, reason)
- Execution instruction
- Context (Empirica, Pantheon, safety gates)

== Example Output

```
🔥 Campfire: Telling story around the campfire...
   Story ID: story-20260119-102530
   PDF: _pyrite/campfire/stories/story-20260119-102530.pdf
```

== Next Steps

Now let's explore D&D campaign integration.


#pagebreak()


Auto-Work integrates with the D&D campaign system to generate quest PDFs.

== What is D&D Campaign?

The D&D campaign system runs scenarios and generates quest PDFs using Typst templates.

== Integration

After successful execution, Auto-Work:

1. Runs a D&D scenario (encounter, explore, or lore)
2. Generates quest markdown from scenario
3. Creates quest PDF using Typst
4. Saves quest PDF to work effort directory

== Scenario Types

- *[Encounter]*: Combat scenarios
- *[Explore]*: Location discovery
- *[Lore]*: World building

== Example Output

```
⚔️  D&D Campaign: Running scenario...
   Scenario Mode: encounter
   Quest PDF: _work_efforts/WE-260118-abc1/quest_20260119_102530.pdf
```

== Next Steps

Now let's explore safety mechanisms in detail.


#pagebreak()


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


#pagebreak()


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


#pagebreak()


This chapter details all command-line options for Auto-Work.

== Basic Command

```
/auto-work
```

Executes Auto-Work with default settings.

== Options

=== --dry-run

Preview what would be done without executing:

```
/auto-work --dry-run
```

=== --verbose

Enable detailed logging:

```
/auto-work --verbose
```

=== --path

Specify project path:

```
/auto-work --path /path/to/project
```

== Option Combinations

=== Dry Run with Verbose

```
/auto-work --dry-run --verbose
```

=== Custom Path with Verbose

```
/auto-work --path /path/to/project --verbose
```

== Next Steps

Now let's explore troubleshooting.


#pagebreak()


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


#pagebreak()


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


#pagebreak()


This chapter covers common issues and solutions.

== No Work Efforts Found

*[Problem]*: `❌ No work efforts found.`

*[Solution]*:
- Check that `_work_efforts/` directory exists
- Verify work effort directories follow `WE-YYMMDD-xxxx` format
- Ensure work efforts are in the correct location

== No Actionable Work Efforts

*[Problem]*: `❌ No actionable work efforts found (all completed).`

*[Solution]*:
- Create new work efforts
- Reopen paused work efforts
- Change status from `completed` to `active` or `paused`

== Action Not Available

*[Problem]*: `❌ No actions available for this work effort.`

*[Solution]*:
- Check work effort has index file
- Verify work effort structure
- Ensure work effort is not empty

== Safety Gate Halt

*[Problem]*: `❌ Execution halted by safety gate`

*[Solution]*:
- Review Empirica gate reason
- Check Judge verdict
- Manually approve if safe
- Revise approach if needed

== Integration Unavailable

*[Problem]*: `⚠️  Empirica: Not initialized`

*[Solution]*:
- Initialize Empirica (optional)
- System continues without it
- Check initialization logs

== Next Steps

Now let's explore customization options.


#pagebreak()


This chapter covers customization options for Auto-Work.

== Priority Scoring Customization

You can adjust priority scoring by modifying:

- Status weights
- Priority level weights
- Content indicator weights
- Activity weights
- Empirica adjustments
- Pantheon adjustments

== Action Types

Add custom action types by:

1. Extending action analyzer
2. Adding to whitelist
3. Implementing action handler

== Integration Configuration

Configure integrations:

- Empirica: Initialize in project
- Pantheon: Configure entities
- Campfire: Set up storytelling
- D&D: Configure campaign system

== Next Steps

Now let's explore best practices.


#pagebreak()


This chapter covers best practices for using Auto-Work.

== Work Effort Management

- Keep work efforts organized
- Use clear, descriptive titles
- Set appropriate priorities
- Update status regularly
- Add TODOs and FIXMEs for tracking

== Safety

- Always review safety gate results
- Use dry run before execution
- Monitor execution logs
- Verify work effort IDs
- Check action types

== Integration

- Initialize Empirica for epistemic tracking
- Configure Pantheon for decision support
- Set up Campfire for storytelling
- Enable D&D campaign for quest generation

== Execution

- Use dry run to preview
- Review JSON output
- Verify execution results
- Monitor logs
- Update work efforts after execution

== Next Steps

Now let's explore future enhancements.


#pagebreak()


This chapter covers planned future enhancements.

== Planned Features

- Multi-work-effort execution (batch mode)
- Learning from execution results
- Adaptive priority scoring
- Execution history and analytics
- Custom action types
- Work effort templates
- Integration with more systems

== Enhancement Ideas

- Machine learning for priority prediction
- Collaborative filtering for work effort selection
- Real-time priority updates
- Work effort dependencies
- Execution scheduling
- Resource monitoring

== Next Steps

Now let's conclude the guide.


#pagebreak()


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
- Explore customization options
- Monitor execution logs

== Resources

- WAFT Documentation: `docs/`
- Auto-Work Script: `scripts/auto_work.py`
- Command Reference: `.cursor/commands/auto-work.md`
- Work Effort System: `_work_efforts/`

== Feedback

For feedback or questions:

- GitHub Issues: https://github.com/ctavolazzi/waft/issues
- Documentation: `docs/`
- Work Efforts: Create a work effort for enhancements

Thank you for using WAFT Auto-Work!


#pagebreak()

