= System Architecture

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
