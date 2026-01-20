= Key Features

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
