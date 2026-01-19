= The Need for a Dashboard

As we explored WAFT's command ecosystem, a clear pattern emerged: while the system has powerful capabilities, accessing and discovering these commands requires knowledge of command syntax and scattered documentation. This chapter documents the problem identification that led to the dashboard design.

== The Problem

=== Scattered Commands

WAFT commands are accessed through:
- Cursor slash commands (`/command-name`)
- CLI commands (`waft command-name`)
- Python API calls
- Various entry points

This fragmentation makes discovery difficult.

=== Knowledge Requirements

To use commands effectively, users need to:
- Know command names
- Understand command syntax
- Know available options
- Understand output locations
- Navigate documentation

=== Output Fragmentation

Generated artifacts are saved to various locations:
- `_work_efforts/` - Checkpoints, dossiers, briefs
- `_pyrite/.waft/` - Visualizations, dashboards
- `_genetics/` - Evolution outputs
- `_science/` - Scientific method results
- `_realms/` - D&D campaign quests

Finding generated files requires knowledge of each command's output location.

=== Lack of Unified Interface

No single interface provides:
- Command discovery
- Quick execution
- Artifact viewing
- Status monitoring
- Activity tracking

== The Solution Vision

A unified command dashboard that provides:

1. *Command Discovery* - All commands visible and searchable
2. *Quick Execution* - Execute commands with proper options
3. *Artifact Management* - View and access generated files
4. *Status Monitoring* - Real-time project and system status
5. *Activity Tracking* - Recent commands and results

== Design Principles

The dashboard design follows these principles:

- *Discoverability* - All commands visible and accessible
- *Efficiency* - Quick access to common actions
- *Clarity* - Clear visual hierarchy and status indicators
- *Integration* - Links to generated artifacts and work efforts
- *Evidence-Based* - Show proof of execution and results

== User Experience Goals

The dashboard should enable users to:

- Discover commands without reading documentation
- Execute commands with proper options
- View generated artifacts immediately
- Monitor system status at a glance
- Track work and progress visually

== Next Steps

With the problem clearly identified, we proceed to the methodical design process documented in the next chapter.
