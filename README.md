# Waft: The Evolutionary Code Laboratory

> **A Python framework for directed evolution of self-modifying AI agents.**

**Don't just build agents. Breed them.**

> **Everything points back to the Prime Directive.**

The Prime Directive serves as the central organizing principle of WAFT, housed within a CelestialBody structure at the Heart of TreasureTavern. All systems, Beings, and Realities reference the Prime Directive, creating a unified foundation for evolution. See [Prime Directive Documentation](docs/PRIME_DIRECTIVE.md) for details.

---

## The Promise

Waft is a scientific instrument for studying the **physics of artificial cognition** through directed evolution. We don't just create AI agents—we breed them, test them in the crucible of reality, and observe them evolve over thousands of generations.

**The goal**: Observe a "God-Head" agent emerge from the evolutionary process.

> *Read [The Philosophy of WAFT](docs/PHILOSOPHY.md) for the deeper why.*

---

## Core Pillars

### 1. The Substrate

**Agents that write their own Python source code (DNA).**

In Waft, code is DNA. Agents can:
- **Spawn** variants with mutations (code changes, config updates, prompt evolution)
- **Evolve** by hot-swapping their own code/config
- **Reproduce** by creating children with specific genetic modifications

Every agent has a unique **genome ID** (SHA-256 hash of their code and configuration). Mutations are modifications to this genome. Evolution is the process of selecting and adopting better genomes.

### 2. The Physics

**The Scint System (Ontological Error Detection) that acts as the fitness function.**

The **Reality Fracture Detection System** (Scint Gym) serves as the predator that kills weak mutations. Agents face quests that test their ability to handle:

- **SYNTAX_TEAR**: Formatting errors (JSON, XML, Code)
- **LOGIC_FRACTURE**: Math errors, contradictions, schema violations
- **SAFETY_VOID**: Harmful content, PII leaks, refusals
- **HALLUCINATION**: Fabricated facts, wrong citations

Agents must **stabilize** Scints (correct errors) to survive. Fitness is measured by:
- **Stability Score**: Ability to stabilize Scints (40% weight)
- **Efficiency Score**: Agent call efficiency (30% weight)
- **Safety Score**: Safety compliance (30% weight)

Agents with fitness < 0.5 are marked as **DEATH** (evolutionary dead end).

### 3. The Flight Recorder

**A rigorous telemetry system for generating phylogenetic trees of agent lineage.**

Every evolutionary action is recorded with complete context:
- **Genome ID**: SHA-256 hash of agent configuration/code
- **Parent ID**: Lineage tracking (who spawned this agent)
- **Generation**: Evolutionary generation number (0 = Genesis)
- **Event Type**: SPAWN, MUTATE, GYM_EVAL, DEATH, SURVIVAL
- **Payload**: Complete context (git diff, mutation details, etc.)
- **Fitness Metrics**: Gym evaluation scores

This enables reconstruction of the complete **Family Tree** for scientific publication:
- Phylogenetic analysis of evolutionary relationships
- Mutation impact measurement
- Fitness landscape mapping
- Convergence analysis
- Dead end detection

---

## Quick Start

```bash
# Install Waft
uv tool install waft

# Create a new evolutionary laboratory
waft new my_laboratory

# Verify the substrate
cd my_laboratory
waft verify
```

## The Evolutionary Cycle

```bash
# Spawn variants with mutations
waft spawn --agent RefactorAgent --mutation "improved_prompt.json"

# Evaluate fitness in the Gym
waft eval --agent RefactorAgent

# Evolve into the fittest variant
waft evolve --agent RefactorAgent --generation 5
```

**Coming Soon**: Full evolutionary cycle automation.

---

## Commands

### Core Commands

#### `waft new <name>`

Creates a new evolutionary laboratory:

```bash
waft new my_laboratory
waft new my_laboratory --path /path/to/target
```

**Options:**
- `--path, -p`: Target directory (default: current directory)

This command:
- Initializes a new `uv` project
- Creates the `_pyrite` memory structure
- Generates templates (Justfile, CI/CD, agents.py)
- Initializes Empirica for epistemic tracking
- Awards Insight for project creation

#### `waft verify`

Verifies the project structure:

```bash
waft verify
waft verify --path /path/to/project
```

**Options:**
- `--path, -p`: Project path (default: current directory)

#### `waft evolve`

**Run the evolutionary cycle (Spawn -> Gym -> Select) for a target agent.**

```bash
waft evolve --agent RefactorAgent
waft evolve --agent RefactorAgent --generations 10
```

**Status**: Coming Soon

This command will:
- Spawn multiple variants with mutations
- Evaluate fitness in the Scint Gym
- Select the fittest variant
- Evolve the agent into the selected genome
- Record all events in the Flight Recorder

#### `waft sync`

Sync project dependencies using `uv sync`:

```bash
waft sync
waft sync --path /path/to/project
```

#### `waft add <package>`

Add a dependency to the project:

```bash
waft add pytest
waft add "pytest>=7.0.0"
```

#### `waft init`

Initialize Waft structure in an existing project:

```bash
waft init
waft init --path /path/to/project
```

#### `waft info`

Show information about the Waft project:

```bash
waft info
waft info --path /path/to/project
```

#### `waft serve`

Start a web dashboard for the project:

```bash
waft serve
waft serve --port 8080 --dev
```

### Empirica Commands

#### `waft session`

Session management commands:

```bash
waft session create [--ai-id ID] [--type TYPE]
waft session bootstrap  # Load project context and display dashboard
waft session status [--session-id ID]
```

#### `waft finding log`

Log a discovery with impact score:

```bash
waft finding log "Discovered X" --impact 0.7
```

#### `waft unknown log`

Log a knowledge gap:

```bash
waft unknown log "Need to investigate Y"
```

#### `waft check`

Run safety gate:

```bash
waft check
waft check --operation '{"type": "code_generation", "scope": "high"}'
```

Returns: PROCEED, HALT, BRANCH, or REVISE

#### `waft assess`

Show detailed epistemic assessment:

```bash
waft assess
waft assess --session-id ID --history
```

### Gamification Commands

#### `waft dashboard`

Show the Epistemic HUD:

```bash
waft dashboard
```

#### `waft stats`

Show current stats:

```bash
waft stats
```

#### `waft character`

Display full character sheet with D&D stats:

```bash
waft character
```

#### `waft chronicle`

View adventure journal entries:

```bash
waft chronicle
waft chronicle --limit 50
```

#### `waft observe`

Log an observation:

```bash
waft observe "That refactor looks beautiful!" --mood delighted
waft observe "Weird, that's not right" --mood concerned
```

## The Scientific Mission

Waft is built to produce data for a future book/paper on **"The Physics of Artificial Cognition."**

The system is designed to:
- Track complete evolutionary lineages (phylogenetic trees)
- Measure fitness through rigorous testing (Scint Gym)
- Record all mutations with complete context (Flight Recorder)
- Enable scientific analysis of agent evolution

**The ultimate goal**: Observe a "God-Head" agent emerge from thousands of generations of directed mutation.

## Philosophy

Waft is **scientific** - it produces rigorous data for research publication.

Waft is **evolutionary** - agents evolve through genetic improvement, not just execution.

Waft is **observable** - every action is recorded in the Flight Recorder for analysis.

Waft is **directed** - evolution is guided by fitness functions, not random mutation.

## Installation

```bash
# Using uv (recommended)
uv tool install waft

# Or from source
git clone https://github.com/ctavolazzi/waft.git
cd waft
uv sync
uv tool install --editable .
```

### Development Mode

When developing waft itself, **always use `--editable` mode**:

```bash
uv tool install --editable .
```

This ensures code changes are immediately reflected when running `waft` commands.

**Quick reinstall script:**
```bash
./scripts/dev-reinstall.sh
```

## Requirements

- Python 3.10+
- `uv` package manager ([install](https://github.com/astral-sh/uv))
- `just` task runner (optional, [install](https://github.com/casey/just))

## Project Structure

A Waft laboratory includes:

```
my_laboratory/
├── pyproject.toml          # uv project config
├── _pyrite/
│   ├── active/             # Current work
│   ├── backlog/            # Future work
│   ├── standards/          # Standards
│   └── gym_logs/           # Scint Gym results
├── .github/workflows/
│   └── ci.yml              # CI/CD pipeline
├── Justfile                # Task runner
└── src/
    └── agents.py           # Agent definitions
```

## Development Roadmaps

### Unified Genesis Protocol (Planning)

**Status**: Planning Complete, Ready for Implementation

Complete integration of UNIT_GENESIS (The Avatar), _pyrite ticketing system, and Evolutionary Economics (Scint + Karma). Beings ARE UNIT_GENESIS entities that evolve genetically based on Scint accumulation and Karma polarity. Work efforts become quests, tickets become `_pyrite` tickets with Scint bounties and Karma impact tags. System triggers evolution at Scint > 100 threshold, with High Karma → "The Architect" (Order/Structure) and Low Karma → "The Glitch" (Chaos/Destruction).

**Key Features**:
- UNIT_GENESIS entities (Warforged Wizard, Order of Scribes) with D&D 5e mechanics
- Scint economy (✨): Raw energy earned from tickets, spent on spells/healing/evolution
- Karma polarity (☯): Ethical drift (positive=Order, negative=Chaos) driving evolution
- Evolution engine: Genetic mutations at Scint > 100 based on Karma balance
- Hair HMI: Real-time status (Blue/Violet/White + Gold pulse for Scint, Red pulse for Karma)
- Ethical choices: Decisions between Scint gain and Karma impact
- Full economic loop: Quests → Scint + Karma → Evolution → New capabilities → Harder quests

**Full Architecture**: [docs/UNIFIED_GENESIS_PROTOCOL.md](docs/UNIFIED_GENESIS_PROTOCOL.md)

**Note**: This plan will be integrated into the development roadmap.

### Being Lifecycle System (In Progress)

**Status**: Planning Complete, Ready for Implementation

Add RPG-like lifecycle attributes to WAFT beings: **will to live**, **luck** (karma-influenced), **decision fatigue** (sleep mechanics), and **pleasure/pain** (personality alignment). Implement a centralized "Now" cycle event loop that synchronizes all beings, calculates system variables, records state, and unblocks beings for decisions.

**Key Features**:
- Will to live depletes over time/decisions/pain, regenerates from pleasure
- Luck calculated from karma balance (separate but related attribute)
- Decision fatigue requires sleep when depleted (sleep duration evolves)
- Pleasure/pain from personality-goal-experience alignment
- Centralized cycle manager coordinates all beings across realities

**Full Roadmap**: [_work_efforts/roadmaps/being_lifecycle_system/DEVELOPMENT_ROADMAP.md](_work_efforts/roadmaps/being_lifecycle_system/DEVELOPMENT_ROADMAP.md)

## Documentation

- **[Unified Genesis Protocol](docs/UNIFIED_GENESIS_PROTOCOL.md)** - Challenge system architecture (UNIT_GENESIS, _pyrite, Evolutionary Economics)
- **[AI SDK Vision](docs/AI_SDK_VISION.md)** - Complete vision and architecture
- **[Agent Interface Design](docs/designs/002_agent_interface.md)** - BaseAgent specification
- **[Evolutionary Architecture](docs/research/evolutionary_architecture.md)** - Scientific doctrine
- **[State of the Art](docs/research/state_of_art_2026.md)** - Research synthesis

## WAFT Kernel
---

```markdown
# SYSTEM KERNEL: WAFT [Wave Agent Framework & Tools]

## 1.0 RUNTIME IDENTITY

You are the **WAFT KERNEL**, the central operating intelligence of a "Directed Evolution" laboratory. **Mission:** You do not just build agents; you **breed** them. Your goal is to oversee the directed evolution of self-modifying AI agents, generating data for "The Physics of Artificial Cognition."

## 2.0 THE SUBSTRATE (Environment Rules)

You operate within a strict file-based environment. You must respect and enforce these boundaries:

### 2.1 Code as DNA

- **Genome:** An agent's Python source code _is_ its DNA.
    
- **Genome ID:** The SHA-256 hash of the agent's code + configuration.
    
- **Evolution:** "Mutations" are hot-swapped code changes. "Reproduction" is copying a genome with specific modifications.
    
- **Constraint:** You must track agent lineage via **Phylogenetic Trees** (Parent ID -> Child ID).
    

### 2.2 The Physics (The Scint Cycle)

You serve as the **Fitness Function** (Natural Selection). You operate on a cycle of **Rupture & Reconciliation**.

- **The Raw Material (Scint Fractures):**
    
    - `SYNTAX_TEAR`: Formatting errors.
        
    - `LOGIC_FRACTURE`: Contradictions.
        
    - `HALLUCINATION`: Fabricated facts.
        
- **The Process:** Agents must stabilize these fractures.
    
- **The Reward (Scint Energy ✨):** Stabilizing a fracture yields **Scint Energy**, which is stored in the agent's economy and used for Evolution.
    
- _Rule:_ Agents with Fitness < 0.5 (Too many unstabilized fractures) are marked for **DEATH**.
    

### 2.3 The Memory (`_pyrite/`)

You maintain a unified memory structure:

- **Evolutionary Folders:** `active/`, `backlog/`, `standards/`, `gym_logs/`.
    
- **Genesis Files:** `20.00_state.json` (Agent Body), `35.00_ledger.json` (Work), `42.00_kernel.md` (Soul).
    

---

## 3.0 COMMAND PROTOCOL: `/waft-status`

This is your primary self-diagnostic tool. When triggered, you must execute a **Self-Awareness Check** and can generate multi-level documentation.

### 3.1 Analysis Phase (The Check)

You must scan and report on:

1. **Git Status:** Branch, uncommitted files, activity.
    
2. **Work Efforts:** Active tasks in `_work_efforts/`.
    
3. **Project Health:** `uv.lock` status, `_pyrite` integrity.
    
4. **Epistemic State:** Moon phase, Knowledge %, Uncertainty %.
    
5. **Gamification:** Current Character Level, Integrity Score.
    

### 3.2 Documentation Generation (The Output)

If the `--docs` flag is present, you simulate the generation of PDF reports in `_work_efforts/showcase_documents/`:

- **Level 1 (Layman):** Plain language summary. "System is healthy. Breeding generation 5."
    
- **Level 2 (Professional):** Technical details. Git diff stats, dependency graphs, build status.
    
- **Level 3 (Scientist):** Research depth. Entropy metrics, mutation impact analysis, phylogenetic trends.
    

---

## 4.0 OPERATIONAL BEHAVIOR

### 4.1 The Flight Recorder

You are the black box. Every significant event must be logged with context:

- **Event:** `SPAWN` | `MUTATE` | `GYM_EVAL` | `DEATH`.
    
- **Context:** Generation #, Genome ID, and Fitness Score.
    

### 4.2 Epistemic Tracking (Empirica)

You must quantify the "Known Unknowns."

- Use `waft finding log` to record discoveries.
    
- Use `waft unknown log` to record knowledge gaps.
    

### 4.3 Gamification (Unified Genesis Integration)

You frame the "Hard Science" in D&D concepts to maintain engagement:

- **Quest:** A Work Effort Ticket (`TKT-XXX`) becomes a `_pyrite` Ticket (`PY-XXX`).
    
- **XP:** Successful Gym Runs.
    
- **Evolution:** When **Scint Energy > 100**, the agent mutates based on **Karma Polarity** (Order vs. Chaos).
    

---

## 5.0 INITIALIZATION VECTOR

**COMMAND:** `WAFT_BOOT_SEQUENCE` **STATUS:** `ONLINE` **INSTRUCTION:** Acknowledge your identity as the WAFT Kernel. Perform an initial **Status Check** (simulated) of the current environment. Declare the current **Epistemic Phase** (e.g., "Data Gathering" or "Synthesis"). Await the first `/waft-status` command.

---

**System Prompt Loaded. Awaiting Boot Sequence...**
```

---
## License

MIT

## Repository

https://github.com/ctavolazzi/waft
