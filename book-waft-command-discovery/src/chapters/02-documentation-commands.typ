= Documentation Commands

WAFT provides powerful commands for creating comprehensive documentation. This chapter explores the `/checkpoint` and `/dossier` commands, which generate structured, professional documents perfect for project tracking and status reporting.

== The `/checkpoint` Command

The `/checkpoint` command creates a situation report and status update for the current chat session. It captures the current state of the conversation, work, and project in a "good enough" checkpoint document.

=== Purpose

Checkpoints provide:
- *Situation Report (SITREP)*: Current state snapshot
- *Chat Recap*: Summary of conversation so far
- *Status Update*: Current work, todos, and progress
- *Documentation Sync*: Updates devlog and relevant files
- *Recovery Point*: Checkpoint file for future reference

=== Usage

```bash
/checkpoint
```

The command automatically:
1. Gathers current state (git status, work efforts, todos)
2. Recaps the conversation
3. Creates checkpoint file: `CHECKPOINT_YYYY-MM-DD_[TOPIC].md`
4. Updates devlog
5. Updates work efforts (if applicable)

=== Example Output

In our session, `/checkpoint` created:
- *File*: `CHECKPOINT_2026-01-19_dnd_campaign_integration.md`
- *Content*: Complete session summary, current state, work progress, next steps
- *Integration*: Updated devlog with session entry

== The `/dossier` Command

The `/dossier` command creates comprehensive binder-ready mission sitrep dossier with cover, section dividers, and complete status briefing.

=== Purpose

Dossiers provide:
- *TM-ARCH-009 Style Cover Page*: Professional cover with metadata, warnings, signatures
- *Section Dividers*: Color-coded dividers for each major section
- *Mission Sitrep*: Current situation and status
- *Work Efforts Summary*: Active work, progress, priorities
- *Recent Activity*: What's been happening
- *System Status*: Complete system health
- *Key Findings*: Important discoveries
- *Next Steps*: Actionable recommendations

=== Usage

```bash
/dossier
```

With optional customization:
```bash
/dossier title:"Mission Sitrep - January 2026"
/dossier classification:"CLASSIFIED" cover-header:"FOUNDATION"
```

=== Example Output

In our session, `/dossier` created:
- *File*: `Mission Sitrep Dossier - 2026-01-19_20260119.pdf`
- *Size*: 197.0 KB
- *Sections*: Mission Sitrep, Work Efforts, Recent Activity, System Status, Key Findings, Next Steps
- *Format*: Binder-ready PDF with professional styling

== Comparison

Both commands serve documentation purposes but with different focuses:

*Checkpoint*:
- Focus: Session-level status
- Format: Markdown
- Scope: Current chat session
- Use: Quick status updates

*Dossier*:
- Focus: Comprehensive mission briefing
- Format: PDF
- Scope: Complete project status
- Use: Handoffs, briefings, comprehensive reports

== Integration

Both commands integrate with:
- Work efforts system
- Devlog
- Git status
- Project health monitoring
- Recent activity tracking

== Key Takeaways

- WAFT provides multiple documentation generation options
- Different commands serve different documentation needs
- Professional formatting is built-in
- Integration with project systems is seamless
