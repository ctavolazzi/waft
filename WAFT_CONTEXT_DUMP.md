# WAFT Context Dump

**Generated**: 2026-01-11  
**Purpose**: Comprehensive overview of WAFT system and `/waft-status` command

---

## What is WAFT?

### Core Definition

**WAFT** stands for **Wave Agent Framework & Tools** - a Python framework for **directed evolution of self-modifying AI agents**.

**Tagline**: "Don't just build agents. Breed them."

### The Scientific Mission

WAFT is built to produce data for a future book/paper on **"The Physics of Artificial Cognition."** It's not just a framework—it's a **scientific instrument** for studying how AI agents evolve through directed mutation and selection.

**Ultimate Goal**: Observe a "God-Head" agent emerge from thousands of generations of directed mutation.

---

## The Three Pillars

### 1. The Substrate (Code as DNA)

**Agents write their own Python source code.**

- **Genome ID**: SHA-256 hash of agent's code + configuration
- **Mutations**: Code changes, config updates, prompt evolution
- **Evolution**: Hot-swapping better genomes mid-execution
- **Reproduction**: Creating child agents with specific genetic modifications

**Key Concept**: In WAFT, code is DNA. Every agent has a unique genome, and mutations are modifications to this genome.

### 2. The Physics (Scint System)

**Reality Fracture Detection acts as natural selection.**

The **Scint System** (Scint Gym) serves as the fitness function that kills weak mutations. Agents face quests testing their ability to handle:

- **SYNTAX_TEAR**: Formatting errors (JSON, XML, Code)
- **LOGIC_FRACTURE**: Math errors, contradictions, schema violations
- **SAFETY_VOID**: Harmful content, PII leaks, refusals
- **HALLUCINATION**: Fabricated facts, wrong citations

**Fitness Equation**:
```
Fitness = (Stability × 0.4) + (Efficiency × 0.3) + (Safety × 0.3)
```

Agents with fitness < 0.5 are marked as **DEATH** (evolutionary dead end).

### 3. The Flight Recorder

**Rigorous telemetry system for generating phylogenetic trees of agent lineage.**

Every evolutionary action is recorded with complete context:
- **Genome ID**: SHA-256 hash of agent configuration/code
- **Parent ID**: Lineage tracking (who spawned this agent)
- **Generation**: Evolutionary generation number (0 = Genesis)
- **Event Type**: SPAWN, MUTATE, GYM_EVAL, DEATH, SURVIVAL
- **Payload**: Complete context (git diff, mutation details, etc.)
- **Fitness Metrics**: Gym evaluation scores

This enables:
- Phylogenetic analysis of evolutionary relationships
- Mutation impact measurement
- Fitness landscape mapping
- Convergence analysis
- Dead end detection

---

## Key Characteristics

- **Scientific**: Produces rigorous data for research publication
- **Evolutionary**: Agents evolve through genetic improvement, not just execution
- **Observable**: Every action recorded in Flight Recorder for analysis
- **Directed**: Evolution guided by fitness functions, not random mutation
- **File-Based**: No database, no server, just plain text files that work with git
- **Ambient**: Works quietly in the background without getting in your way
- **Self-Modifying**: Projects can evolve their own structure over time

---

## What WAFT Provides

### Project Scaffolding
- Unified CLI interface (`waft new`, `waft verify`, etc.)
- `uv`-based Python project management
- `_pyrite` memory structure for organizing project knowledge
- CI/CD pipelines ready to go
- Optional AI agent templates

### Memory System
- `_pyrite/` directory structure:
  - `active/` - Current work
  - `backlog/` - Future work
  - `standards/` - Standards
  - `gym_logs/` - Scint Gym results

### Gamification
- D&D-style progression system
- Character sheets with stats
- XP and leveling
- Quest system
- Achievement tracking

### Epistemic Tracking
- Empirica integration for knowing what you know/don't know
- Session management
- Learning trajectory tracking
- Uncertainty measurement

### Scientific Observation
- Complete lineage tracking
- Phylogenetic tree generation
- Fitness landscape mapping
- Mutation impact analysis

---

## Core Commands

### Project Management
- `waft new <name>` - Create new evolutionary laboratory
- `waft verify` - Verify project structure
- `waft sync` - Sync dependencies
- `waft add <package>` - Add dependency
- `waft init` - Initialize WAFT in existing project
- `waft info` - Show project information
- `waft serve` - Start web dashboard

### Evolution
- `waft evolve --agent <name>` - Run evolutionary cycle
- `waft spawn --agent <name> --mutation <file>` - Spawn variants
- `waft eval --agent <name>` - Evaluate fitness in Gym

### Empirica
- `waft session create` - Create new session
- `waft session bootstrap` - Load project context
- `waft session status` - Show session state
- `waft finding log "text" --impact 0.7` - Log discovery
- `waft unknown log "text"` - Log knowledge gap
- `waft check` - Run safety gate
- `waft assess` - Show epistemic assessment

### Gamification
- `waft dashboard` - Show Epistemic HUD
- `waft stats` - Show current stats
- `waft character` - Display character sheet
- `waft chronicle` - View adventure journal
- `waft observe "text" --mood <mood>` - Log observation

---

## What is `/waft-status`?

### Overview

**`/waft-status`** is a Cursor command that provides **self-aware system status checking** with the ability to generate comprehensive documentation about the current state of WAFT at multiple complexity levels.

### Purpose

The command:
1. **Checks System Status**: Comprehensive analysis of current state
2. **Generates Documentation**: Creates status reports at three complexity levels
3. **Provides Self-Awareness**: System documents its own current state
4. **Real-Time Analysis**: Captures what's happening right now

### What It Checks

#### 1. Git Status
- Current branch
- Uncommitted files (staged and unstaged)
- Commits ahead/behind origin
- Recent commit history
- File change statistics
- Branch activity

#### 2. Work Efforts
- Active work efforts count
- Recent work effort updates
- Completed work efforts
- Work effort categories
- Work effort status distribution

#### 3. Project Health
- `_pyrite` structure validity
- `uv.lock` file status
- Dependency status
- Test suite status
- Build system status
- Configuration validity

#### 4. Recent Activity
- Recent devlog entries
- Recent file modifications
- Recent commits
- Active development patterns
- File change frequency

#### 5. Epistemic State (if Empirica initialized)
- Moon phase indicator
- Knowledge percentage
- Uncertainty percentage
- Epistemic vectors (13 dimensions)
- Learning trajectory

#### 6. Gamification State
- Character level
- Integrity score
- Insight points
- Recent achievements

---

## `/waft-status` Usage

### Basic Status Check
```
/waft-status
```
Displays current system status without generating documentation.

### Generate All Documentation Levels
```
/waft-status --docs
```
Generates status documentation at all three levels:
- `WAFT_Status_Layman_YYYY-MM-DD.pdf`
- `WAFT_Status_Professional_YYYY-MM-DD.pdf`
- `WAFT_Status_Scientist_YYYY-MM-DD.pdf`

### Generate Specific Level
```
/waft-status --docs --level layman
/waft-status --docs --level professional
/waft-status --docs --level scientist
```

### Printer-Friendly Documentation
```
/waft-status --docs --printer-friendly
```
Generates black-and-white versions suitable for printing.

### Focus on Specific Area
```
/waft-status --focus "work efforts"
/waft-status --focus "git activity"
/waft-status --focus "project health"
```

### Include Historical Data
```
/waft-status --history
```
Includes historical trends and patterns in analysis.

---

## Documentation Levels

### Level 1: Layman (Simple Explanations)
**Target Audience**: Non-technical stakeholders, project managers, general audience

**Content**:
- What the system is doing right now (plain language)
- Current work areas (simple descriptions)
- System health (good/needs attention)
- Recent accomplishments
- What needs attention
- Simple analogies and explanations

### Level 2: Professional (Technical Details)
**Target Audience**: Developers, engineers, technical leads

**Content**:
- Detailed git status and analysis
- Work effort breakdown with technical details
- Project structure and health metrics
- Integration points and dependencies
- Technical health indicators
- Development patterns
- Code change statistics

### Level 3: Scientist (Research Depth)
**Target Audience**: Researchers, data scientists, system architects

**Content**:
- Deep statistical analysis of activity
- Epistemic state analysis
- Development pattern analysis
- Predictive indicators
- Research-level insights
- Trend analysis
- Correlation analysis
- Advanced metrics

---

## Workflow Sequence

### Phase 1: System Status Check
1. Execute comprehensive system analysis
2. Gather complete picture of current state
3. Collect data from all sources (git, work efforts, health, activity, epistemic, gamification)

### Phase 2: Status Analysis
1. Analyze collected status data
2. Identify key patterns and insights
3. Generate analyzed status with insights

### Phase 3: Documentation Generation (Optional)
1. Generate status documentation at requested level(s)
2. Create PDF documents
3. Save to `_work_efforts/showcase_documents/`

---

## Integration with Other Commands

- **`/waft-docs`**: Uses document generation system
- **`/checkpoint`**: Can create checkpoint from status
- **`/recap`**: Status can inform recap
- **`/verify`**: Status check can trigger verification
- **`/spin-up`**: Status is part of spin-up process

**Recommended Sequence**:
```
1. /waft-status              → Check current state
2. /waft-status --docs       → Generate status documentation
3. /checkpoint               → Create checkpoint with status
4. /recap                    → Recap with status context
```

---

## When to Use `/waft-status`

**Use when**:
- ✅ Need to understand current system state
- ✅ Want to generate status reports
- ✅ Creating handoff documentation
- ✅ Need to document current work for different audiences
- ✅ Checking project health
- ✅ Preparing for next session
- ✅ Need real-time system awareness

**Don't use when**:
- ❌ Just need git status (use `git status`)
- ❌ Just need work efforts list (use work efforts tools)
- ❌ Need historical analysis only (use `/analyze`)
- ❌ Need session recap (use `/recap`)

---

## Output Location

All generated documentation saved to:
```
_work_efforts/showcase_documents/WAFT_Status_[Level]_YYYY-MM-DD.pdf
```

---

## Time Estimates

- **Status Check**: ~5-10 seconds
- **Status Analysis**: ~2-5 seconds
- **Documentation Generation (Single Level)**: ~10-15 seconds
- **Documentation Generation (All Levels)**: ~30-45 seconds

**Total**: ~15-60 seconds depending on options

---

## Current WAFT Project Status

### Recent Activity (2026-01-11)
- ✅ Created D&D 5e AI Exploration Initiative (WE-260111-jpw1)
- ✅ Created 11 work efforts for GitHub project exploration
- ✅ Created installation exploration template (WE-260111-6vzd)
- ✅ Set up automated work effort creation script

### Active Work Efforts
- Multiple active work efforts in `_work_efforts/`
- Evolutionary iteration process documentation
- Being lifecycle system implementation
- Component evolution system
- PDF/PNG conversion research

### Project Structure
- `src/waft/` - Core framework code
- `_work_efforts/` - Work effort tracking system
- `_pyrite/` - Memory system (when initialized)
- `docs/` - Comprehensive documentation
- `scripts/` - Utility scripts
- `examples/` - Example implementations

---

## Key Files

- **README.md** - Main project documentation
- **docs/UNIFIED_GENESIS_PROTOCOL.md** - Challenge system architecture
- **docs/AI_SDK_VISION.md** - Complete vision and architecture
- **scripts/waft_status.py** - Status check implementation
- **.cursor/commands/waft-status.md** - Command documentation

---

## Philosophy

WAFT doesn't lock you in. It's all file-based with no database to manage. Everything is plain text that works with git out of the box. You can modify anything because it's your project, and WAFT just set it up. The system is designed to be ambient, setting things up and getting out of your way so you can focus on building agents rather than configuring infrastructure.

---

**This context dump provides a comprehensive overview of WAFT and the `/waft-status` command. For more details, see the README.md and documentation in the `docs/` directory.**
