# Help

**Discover and understand available Cursor commands.**

Lists all available commands, organized by category, with brief descriptions and usage guidance. Helps you discover commands and understand when to use each one.

**Use when:** Want to see available commands, understand what each does, or find the right command for a task.

---

## Purpose

Provides: command discovery, categorization by purpose, brief descriptions, usage guidance, command count.

---

## Command Categories

### Core Workflow Commands
Essential commands for daily development workflow.

1. **`/execute`** - Gather all relevant context, then execute the following order. Use when need context-aware execution of commands or instructions.

2. **`/phase1`** - Gather all project data, create interactive dashboard. Use when starting work, need full overview.

3. **`/analyze`** - Analyze Phase 1 data, generate insights and action plans. Use after Phase 1, need recommendations.

4. **`/resume`** - Load last session summary, compare current state, continue previous work. Use when starting new session.

5. **`/continue`** - Reflect on current work, then continue with awareness. Use mid-work, want reflection without stopping.

6. **`/proceed`** - Verify context and assumptions before continuing. Use when need to check understanding before acting.

7. **`/reflect`** - Prompt AI to write reflective journal entries. Use when want AI to document thoughts, learnings, experiences.

8. **`/checkpoint`** - Document current state, progress, todos. Use when need snapshot of current situation.

9. **`/verify`** - Verify project state with traceable evidence. Use when need to verify project is in good state.

10. **`/checkout`** - Run cleanup, documentation, summary tasks. Use when ending session, want comprehensive wrap-up.

---

### Analysis & Planning Commands
Commands for analysis, decision-making, and planning.

9. **`/consider`** - Analyze situation, present options with recommendations. Use when facing decision, need options evaluated.

10. **`/decide`** - Run decision matrix calculations (WSM, AHP, WPM, BWM). Use when need quantitative decision analysis.

11. **`/explore`** - Deep codebase exploration and analysis. Use when need to understand codebase deeply.

---

### Project Management Commands
Commands for project setup, orientation, and management.

12. **`/rampup`** - Progressive project orientation through phases. Use when starting new repo, want incremental understanding (proceed → spin-up → analyze → phase1 → prepare phase2 → recap).

13. **`/orient`** - Complete project orientation and startup workflow. Use when starting work on project, need full orientation.

14. **`/spin-up`** - Quick project overview and status check. Use when need quick orientation, not full deep dive.

15. **`/engineer`** - Full engineering workflow from start to finish. Use when need comprehensive engineering workflow.

---

### Utility Commands
Utility commands for visualization, stats, and analytics.

15. **`/visualize`** - Generate interactive dashboard in browser. Use when want visual representation of project state.

16. **`/stats`** - Show session statistics (files created, lines written, etc.). Use when want to see what was accomplished in session.

17. **`/analytics`** - Analyze session history, patterns, trends. Use when want to understand work patterns over time.

18. **`/recap`** - Create conversation recap and session summary. Use when want summary of conversation/session.

### Goal Management Commands
Commands for tracking larger goals and identifying next steps.

19. **`/goal`** - Track larger goals, break into steps. Use when have larger objective, want to track progress.

20. **`/next`** - Identify next step based on goals. Use when want to know what to do next, need direction.

---

## Command Discovery

### By Task

**Starting Work:**
- `/spin-up` - Quick orientation
- `/orient` - Full orientation
- `/resume` - Continue from last session
- `/phase1` - Full data gathering

**During Work:**
- `/execute` - Execute command/instruction with full context
- `/continue` - Reflect and continue
- `/reflect` - Write in journal
- `/checkpoint` - Document current state
- `/verify` - Verify project state

**Decision Making:**
- `/consider` - Analyze options
- `/decide` - Quantitative decision matrix

**Analysis:**
- `/analyze` - Analyze Phase 1 data
- `/explore` - Deep exploration
- `/analytics` - Historical analysis

**Ending Work:**
- `/checkout` - End session workflow
- `/recap` - Session summary
- `/stats` - Session statistics

---

## Command Count

**Total Commands**: 20+

**By Category:**
- Core Workflow: 9 commands
- Analysis & Planning: 3 commands
- Project Management: 4 commands
- Utility: 4 commands

**Are we getting out of hand?**
- Maybe! But each command serves a specific purpose
- Commands are well-organized and discoverable
- This `/help` command helps with discovery

---

## Usage Examples

### Starting Work
- `/rampup` - Progressive orientation: proceed → spin-up → analyze → phase1 → prepare phase2 → recap
- `/orient` - Get project orientation and context
- `/phase1` - Gather all project data and create dashboard
- `/resume` - Continue from last session
- `/goal create feature-auth "Implement authentication system"` - Create new goal

### During Work
- `/execute /phase1` - Execute command with full context awareness
- `/execute a thorough cleanup on the current feature branch` - Execute natural language instruction
- `/continue` - Reflect on current work and continue
- `/proceed` - Verify context and assumptions before continuing
- `/checkpoint` - Take snapshot of current state
- `/next` - Get next step recommendation
- `/goal show feature-auth` - View goal progress
- `/reflect` - Write in journal about current work

### Making Decisions
- `/consider` - Get analysis and recommendations
- `/decide` - Use decision matrix for choices
- `/explore` - Deep dive into topic before deciding

### Ending Work
- `/checkout` - Comprehensive end-of-session workflow
- `/recap` - Create conversation summary
- `/stats` - View session statistics
- `/goal update feature-auth --step 3 --complete` - Mark step complete

### Discovery & Learning
- `/help` - Discover all available commands
- `/help --category Goal` - Show goal management commands
- `/help --search reflect` - Find reflection-related commands
- `/analytics` - Analyze work patterns over time

### Goal Workflow
- `/goal create api-v2 "Build REST API v2"` - Create goal
- `/goal list` - List all goals
- `/goal show api-v2` - View goal details
- `/next` - Get next step from active goals
- `/next --goal api-v2` - Get next step for specific goal
- `/next --count 3` - Get top 3 next steps

### Help Command Usage
- `/help` - List all commands
- `/help --category workflow` - Show workflow commands
- `/help --search "reflect"` - Search for commands
- `/help --command resume` - Show command details
- `/help --count` - Show command count

---

## Integration

This command helps discover other commands. It's a meta-command that supports the command ecosystem.

**Related:**
- `COMMAND_RECOMMENDATIONS.md` - Detailed command recommendations
- `GLOBAL_COMMANDS_SETUP.md` - How to sync commands globally

---

## When to Use

**Use `/help` when:**
- ✅ Want to see all available commands
- ✅ Need to find the right command for a task
- ✅ Want to understand command categories
- ✅ Need quick reference for commands
- ✅ Want to discover new commands

**Don't use `/help` when:**
- ❌ Need detailed command documentation (read command file directly)
- ❌ Need to execute a command (use the command directly)
- ❌ Need command implementation details (read source code)

---

**This command helps you discover and understand available commands, making the command ecosystem more accessible and manageable.**
