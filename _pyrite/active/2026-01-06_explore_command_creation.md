# Explore Command Creation

**Date**: 2026-01-06
**File**: `.cursor/commands/explore.md`

## Purpose

Created the `explore` command to complement `spin-up` in the development workflow sequence:
1. `spin-up` → Get oriented (status, active work, recent changes)
2. `explore` → Understand structure and architecture ← **NEW**
3. `draft plan` → Create initial plan
4. `critique plan` → Review and refine
5. `finalize plan` → Lock in plan
6. `begin` → Start implementation

## What Explore Does

While `spin-up` answers "what's the current state?", `explore` answers "how does this work?":

- **Project Structure Analysis** - Map directories, entry points, configs
- **Codebase Architecture** - Understand components and relationships
- **Dependency Analysis** - Map dependencies (external and internal)
- **Pattern Discovery** - Identify conventions and patterns
- **Key Functionality Mapping** - Locate main features and critical paths
- **Documentation & Knowledge** - Find and review key docs
- **Testing & Quality** - Understand test structure and coverage
- **Integration Points** - Find external integrations and boundaries

## Key Features

1. **Structured Exploration** - 10-step process covering all aspects
2. **Command Reference** - Ready-to-use commands for exploration
3. **Semantic Search Queries** - Questions to ask for understanding
4. **Output Format** - Structured report template
5. **Workflow Integration** - Clear position in development sequence

## Output Sections

The explore command produces a structured report with:
1. Project Structure
2. Architecture Overview
3. Dependencies
4. Patterns & Conventions
5. Key Functionality
6. Integration Points
7. Testing & Quality
8. Documentation
9. Insights & Observations
10. Questions & Unknowns

## Integration

- Complements `spin-up.md` (orientation vs. exploration)
- Prepares for `draft plan` (understanding before planning)
- Uses semantic search for deep understanding
- Creates diagrams when helpful (mermaid)

## Files Changed

- `.cursor/commands/explore.md` - NEW (5.7KB, comprehensive exploration guide)

