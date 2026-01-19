= Command Registry

This chapter explores how WAFT commands are discovered, registered, and made available through the dashboard.

== Command Discovery

WAFT commands are defined in `.cursor/commands/*.md` files. Each command file contains:
- Command name and description
- Usage examples
- Purpose and philosophy
- Execution phases
- Integration details

== Command Structure

=== Command File Format

Each command file follows a standard structure:

```markdown
# Command Name

**Brief description**

**Use when:** When to use this command

---

## Purpose

What this command provides

---

## Usage

How to invoke the command

---

## Execution Phases

Step-by-step execution flow

---

## Integration

How it integrates with other systems
```

== Command Categories

=== Documentation Commands
- `/checkpoint` - Create status checkpoints
- `/dossier` - Generate mission sitrep dossiers
- `/one-pager` - Create 2-page documents

=== Learning & Research
- `/study` - Scientific method learning
- `/science-bitch` - Full scientific workflow

=== Document Generation
- `/worldbuild` - Worldbuilding documents
- `/tell-story` - Narrative PDFs

=== Status & Visualization
- `/show-me` - Comprehensive overview
- `/visualize` - Interactive dashboard

=== UI Evolution
- `/evolve-a-ui` - Methodical UI development

== Registry Implementation

=== Scanning Commands

The dashboard scans `.cursor/commands/` directory:
1. Find all `.md` files
2. Parse frontmatter/metadata
3. Extract command name from filename
4. Read command description
5. Build command registry

=== Command Metadata

Each command has:
- **Name**: Command identifier
- **Description**: What it does
- **Category**: Command type
- **Usage**: How to invoke
- **File Path**: Location of command file

== Integration with Dashboard

The command registry powers:
- Command launcher component
- Search functionality
- Category filtering
- Command execution
- Documentation links

== Future Enhancements

- Command aliases
- Command dependencies
- Command parameters UI
- Command history
- Favorite commands
