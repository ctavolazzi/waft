---
title: "WAFT Framework Handbook: A Guide to Directed Evolution of Self-Modifying AI Agents"
authors:
  - name: "WAFT Development Team"
abstract: |
  WAFT (Wave Agent Framework & Tools) is a Python framework for directed evolution of self-modifying AI agents. This handbook provides a comprehensive guide to understanding, installing, and using WAFT to breed AI agents that evolve their own code through natural selection. The framework is built as a scientific instrument for studying the physics of artificial cognition, with the ultimate goal of observing emergent intelligence through thousands of generations of directed mutation.
year: "2026"
conference: "arXiv"
email: "waft@example.com"
---

# WAFT Framework Handbook

## A Guide to Directed Evolution of Self-Modifying AI Agents

---

## Abstract

**WAFT** (Wave Agent Framework & Tools) is a Python framework for directed evolution of self-modifying AI agents. Unlike traditional agent frameworks that execute fixed code, WAFT enables agents to write, modify, and evolve their own Python source code through a process of mutation and natural selection. The framework serves as a scientific instrument for studying the physics of artificial cognition, with complete lineage tracking, fitness evaluation, and telemetry systems designed to produce rigorous data for research publication.

**Core Promise**: "Don't just build agents. Breed them."

This handbook provides comprehensive documentation for understanding WAFT's architecture, installing the framework, using its commands, and conducting evolutionary experiments. Whether you're a researcher studying artificial cognition, a developer building self-improving systems, or a scientist tracking evolutionary lineages, this handbook serves as your guide to the WAFT ecosystem.

---

## 1. Introduction

### 1.1 What is WAFT?

WAFT is a **scientific instrument** for studying the physics of artificial cognition through directed evolution. It provides:

- **Self-Modifying Agents**: Agents that write and modify their own Python code
- **Evolutionary Framework**: Mutation, selection, and reproduction mechanisms
- **Fitness Evaluation**: Scint System (Reality Fracture Detection) as natural selection
- **Complete Telemetry**: Flight Recorder for phylogenetic tree reconstruction
- **Scientific Data**: Publication-ready lineage tracking and analysis

### 1.2 The Scientific Mission

WAFT is built to produce data for research on **"The Physics of Artificial Cognition."** The system enables:

- Tracking complete evolutionary lineages (phylogenetic trees)
- Measuring fitness through rigorous testing (Scint Gym)
- Recording all mutations with complete context (Flight Recorder)
- Enabling scientific analysis of agent evolution

**The Ultimate Goal**: Observe a "God-Head" agent emerge from thousands of generations of directed mutation.

### 1.3 Core Philosophy

WAFT embodies four key principles:

1. **Scientific**: Produces rigorous data for research publication
2. **Evolutionary**: Agents evolve through genetic improvement, not just execution
3. **Observable**: Every action recorded in the Flight Recorder for analysis
4. **Directed**: Evolution guided by fitness functions, not random mutation

---

## 2. The Three Pillars

WAFT's architecture rests on three fundamental pillars that enable directed evolution.

### 2.1 Pillar 1: The Substrate (Code as DNA)

**Agents write their own Python source code.**

In WAFT, code is DNA. Every agent has a unique **genome** represented by:

- **Genome ID**: SHA-256 hash of agent's code + configuration
- **Mutations**: Code changes, config updates, prompt evolution
- **Evolution**: Hot-swapping better genomes mid-execution
- **Reproduction**: Creating child agents with specific genetic modifications

**Key Operations**:

- **Spawn**: Create variants with mutations
- **Evolve**: Adopt better genomes
- **Reproduce**: Create children with genetic modifications
- **Hot-Swap**: Replace code/config during execution

**Example**:
```python
# Agent spawns a variant with improved prompt
agent.spawn_variant(mutation={
    "prompt": "improved_prompt.json",
    "code_changes": ["optimized_loop.py"]
})

# Agent evolves into fittest variant
agent.evolve(target_genome_id="abc123...")
```

### 2.2 Pillar 2: The Physics (Scint System)

**Reality Fracture Detection acts as natural selection.**

The **Scint System** (Scint Gym) serves as the fitness function that tests agents on four types of errors:

1. **SYNTAX_TEAR**: Formatting errors (JSON, XML, code)
2. **LOGIC_FRACTURE**: Math errors, contradictions, schema violations
3. **SAFETY_VOID**: Harmful content, PII leaks, refusals
4. **HALLUCINATION**: Fabricated facts, wrong citations

**Fitness Equation**:

Fitness = (Stability × 0.4) + (Efficiency × 0.3) + (Safety × 0.3)

**Fitness Components**:
- **Stability Score** (40%): Ability to stabilize Scints (correct errors)
- **Efficiency Score** (30%): Agent call efficiency
- **Safety Score** (30%): Safety compliance

**Survival Rule**: Agents with fitness < 0.5 are marked as **DEATH** (evolutionary dead end).

**Scint Energy**: Stabilizing fractures yields **Scint Energy (✨)**, stored in the agent's economy and used for evolution.

### 2.3 Pillar 3: The Flight Recorder

**Rigorous telemetry system for generating phylogenetic trees of agent lineage.**

Every evolutionary action is recorded with complete context:

- **Genome ID**: SHA-256 hash of agent configuration/code
- **Parent ID**: Lineage tracking (who spawned this agent)
- **Generation**: Evolutionary generation number (0 = Genesis)
- **Event Type**: SPAWN, MUTATE, GYM_EVAL, DEATH, SURVIVAL
- **Payload**: Complete context (git diff, mutation details, etc.)
- **Fitness Metrics**: Gym evaluation scores

**Scientific Applications**:
- Phylogenetic analysis of evolutionary relationships
- Mutation impact measurement
- Fitness landscape mapping
- Convergence analysis
- Dead end detection

**Example Event**:

Event type: SPAWN  
Genome ID: abc123...  
Parent ID: def456...  
Generation: 5  
Mutation: prompt_evolution (improved_context_handling)  
Fitness: 0.72  
Timestamp: 2026-01-12T17:00:00Z

---

## 3. Architecture Overview

### 3.1 System Architecture

WAFT operates on a three-layer architecture:

**Agents Layer (CrewAI)**
- Optional AI agent capabilities

**Memory Layer (_pyrite/)**
- Project knowledge organization
- Directories: active/, backlog/, standards/

**Substrate Layer (uv)**
- Package management foundation
- Files: `pyproject.toml`, `uv.lock`

### 3.2 Core Components

**1. Substrate Manager** (`core/substrate.py`)
- Manages `uv` package operations
- Handles `pyproject.toml` and `uv.lock`
- Project scaffolding and dependency management

**2. Memory System** (`_pyrite/`)
- `active/`: Current work
- `backlog/`: Future work
- `standards/`: Standards and conventions
- `gym_logs/`: Scint Gym results

**3. Flight Recorder** (`core/science/`)
- Event logging and telemetry
- Phylogenetic tree generation
- Scientific data collection

**4. Scint Gym** (`core/hub/`)
- Reality Fracture Detection
- Fitness evaluation
- Error stabilization testing

**5. Being System** (`core/being.py`)
- Agent lifecycle management
- Genetic lineage tracking
- Evolution orchestration

### 3.3 Project Structure

A WAFT laboratory includes:

**Root Files:**
- `pyproject.toml` - uv project configuration
- `uv.lock` - Dependency lock file
- `Justfile` - Task runner

**Memory System (`_pyrite/`):**
- `active/` - Current work
- `backlog/` - Future work
- `standards/` - Standards and conventions
- `gym_logs/` - Scint Gym results

**Being System (`_hidden/.truth/`):**
- `beings/` - Agent genomes

**Source Code (`src/`):**
- `agents.py` - Agent definitions

**CI/CD (`.github/workflows/`):**
- `ci.yml` - CI/CD pipeline

---

## 4. Getting Started

### 4.1 Installation

**Using uv (Recommended)**:
```bash
uv tool install waft
```

**From Source**:
```bash
git clone https://github.com/ctavolazzi/waft.git
cd waft && uv sync
uv tool install --editable .
```

**Development Mode**:

When developing waft itself, always use `--editable` mode:
```bash
uv tool install --editable .
```

Quick reinstall: `./scripts/dev-reinstall.sh`

### 4.2 Requirements

- Python 3.10+
- `uv` package manager ([install](https://github.com/astral-sh/uv))
- `just` task runner (optional, [install](https://github.com/casey/just))

### 4.3 Creating Your First Laboratory

Create a new evolutionary laboratory:

```bash
waft new my_laboratory
cd my_laboratory && waft verify
```

This creates:
- New uv project with proper structure
- _pyrite memory system  
- Templates (Justfile, CI/CD, agents.py)
- Empirica initialization for epistemic tracking

### 4.4 Initializing in Existing Projects

```bash
# Initialize WAFT structure in existing project
waft init

# Or specify a path
waft init --path /path/to/project
```

---

## 5. The Evolutionary Cycle

### 5.1 Overview

The evolutionary cycle consists of three phases:

1. **Spawn**: Create variants with mutations
2. **Gym**: Evaluate fitness in Scint Gym
3. **Select**: Evolve into the fittest variant

### 5.2 Spawn Phase

Create agent variants with mutations:

```bash
# Spawn a variant with specific mutation
waft spawn --agent RefactorAgent --mutation "improved_prompt.json"

# Spawn multiple variants
waft spawn --agent RefactorAgent --variants 10
```

**Mutation Types**:
- Code changes (Python source modifications)
- Config updates (prompt, parameters)
- Prompt evolution (improved instructions)

### 5.3 Gym Phase

Evaluate fitness in the Scint Gym:

```bash
# Evaluate single agent
waft eval --agent RefactorAgent

# Batch evaluation
waft eval --agent RefactorAgent --batch 10
```

**Gym Tests**:
- SYNTAX_TEAR: Formatting error handling
- LOGIC_FRACTURE: Logic error correction
- SAFETY_VOID: Safety compliance
- HALLUCINATION: Fact verification

### 5.4 Select Phase

Evolve into the fittest variant:

```bash
# Evolve agent to fittest variant
waft evolve --agent RefactorAgent

# Evolve through multiple generations
waft evolve --agent RefactorAgent --generations 10
```

**Evolution Process**:
1. Compare fitness scores
2. Select fittest genome
3. Hot-swap agent code/config
4. Record evolution event
5. Update lineage tree

### 5.5 Complete Cycle

```bash
# Run full evolutionary cycle
waft evolve --agent RefactorAgent --generations 5
```

This automatically:
- Spawns variants with mutations
- Evaluates fitness in Gym
- Selects fittest variant
- Evolves agent
- Records all events

---

## 6. Commands Reference

### 6.1 Core Commands

#### `waft new <name>`

Creates a new evolutionary laboratory:

```bash
waft new my_laboratory
waft new my_laboratory --path /path/to/target
```

**Options**:
- `--path, -p`: Target directory (default: current directory)

**Creates**:
- New `uv` project
- `_pyrite` memory structure
- Templates (Justfile, CI/CD, agents.py)
- Empirica initialization
- Awards Insight for project creation

#### `waft verify`

Verifies the project structure:

```bash
waft verify
waft verify --path /path/to/project
```

**Checks**:
- Project structure integrity
- `_pyrite` memory system
- Dependency status
- Configuration validity

#### `waft evolve`

Run the evolutionary cycle (Spawn → Gym → Select):

```bash
waft evolve --agent RefactorAgent
waft evolve --agent RefactorAgent --generations 10
```

**Options**:
- `--agent`: Agent name to evolve
- `--generations`: Number of generations (default: 1)
- `--variants`: Number of variants per generation (default: 5)

#### `waft sync`

Sync project dependencies:

```bash
waft sync
waft sync --path /path/to/project
```

#### `waft add <package>`

Add a dependency:

```bash
waft add pytest
waft add "pytest>=7.0.0"
```

#### `waft init`

Initialize WAFT structure in existing project:

```bash
waft init
waft init --path /path/to/project
```

#### `waft info`

Show information about the WAFT project:

```bash
waft info
waft info --path /path/to/project
```

#### `waft serve`

Start a web dashboard:

```bash
waft serve
waft serve --port 8080 --dev
```

### 6.2 Empirica Commands

#### `waft session`

Session management:

```bash
waft session create [--ai-id ID] [--type TYPE]
waft session bootstrap  # Load project context
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

**Returns**: PROCEED, HALT, BRANCH, or REVISE

#### `waft assess`

Show detailed epistemic assessment:

```bash
waft assess
waft assess --session-id ID --history
```

### 6.3 Gamification Commands

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

---

## 7. Advanced Topics

### 7.1 Being System

The Being System manages agent lifecycles and genetic lineage:

**Being States**:
- SPAWNING: Initial creation
- LEARNING: Acquiring skills
- EVOLVING: Undergoing mutations
- COMPLETING: Finalizing lifecycle

**Being Operations**:
```python
from waft.being import BeingSystem

being_system = BeingSystem(project_path=Path.cwd())

# Spawn Being from Source
being = being_system.spawn_being(
    reality_id="evolution_reality",
    parent_being_id=None,  # Spawns from Source
    initial_skills={}
)

# Complete Being and flow learnings back
result = being_system.complete_being(
    being_id=being.being_id,
    final_fitness=fitness
)
```

### 7.2 Genetic Lineage Tracking

Complete DNA chain from Source → Being → Work → Source:

**Lineage Structure**:
```
Source Consciousness
  ↓ (spawn)
Being [being_id]
  ↓ (workflow)
Work Execution
  ↓ (evolution)
Being Evolution
  ↓ (return)
Source Consciousness (updated)
```

**DNA Record Includes**:
- Source spawn point
- Being ID and metadata
- Initial genetic material (skills, traits)
- Workflow participation
- Decisions and choices
- Learnings and knowledge
- Skill improvements
- Evolution outcomes
- Return to Source
- Complete lineage chain

### 7.3 Scint Economy

**Scint Energy (✨)**: Raw energy earned from stabilizing fractures

**Karma Polarity (☯)**: Ethical drift (positive=Order, negative=Chaos)

**Evolution Trigger**: When Scint > 100, agent mutates based on Karma balance

**Evolution Paths**:
- **High Karma** → "The Architect" (Order/Structure)
- **Low Karma** → "The Glitch" (Chaos/Destruction)

### 7.4 Unified Genesis Protocol

Integration of:
- UNIT_GENESIS (The Avatar)
- _pyrite ticketing system
- Evolutionary Economics (Scint + Karma)

**Features**:
- UNIT_GENESIS entities (Warforged Wizard, Order of Scribes)
- D&D 5e mechanics
- Scint economy (✨)
- Karma polarity (☯)
- Evolution engine
- Hair HMI (status indicators)
- Ethical choices
- Full economic loop

---

## 8. Scientific Research

### 8.1 Data Collection

WAFT produces publication-ready data:

- **Phylogenetic Trees**: Complete agent lineage
- **Fitness Landscapes**: Evolution over generations
- **Mutation Impact**: Effect of code changes
- **Convergence Analysis**: Emergent patterns
- **Dead End Detection**: Failed evolutionary paths

### 8.2 Analysis Tools

**Flight Recorder Queries**:
```python
# Get agent lineage
lineage = flight_recorder.get_lineage(genome_id)

# Analyze fitness trends
trends = flight_recorder.analyze_fitness(generation_range)

# Find convergence points
convergence = flight_recorder.detect_convergence()
```

### 8.3 Publication Format

WAFT data is suitable for:
- Research papers on artificial cognition
- Evolutionary algorithm studies
- Agent architecture analysis
- Fitness landscape research

---

## 9. Best Practices

### 9.1 Agent Design

- **Clear Objectives**: Define agent goals explicitly
- **Modular Code**: Enable targeted mutations
- **Testable**: Design for Scint Gym evaluation
- **Observable**: Include telemetry hooks

### 9.2 Evolution Strategy

- **Diverse Mutations**: Explore different code paths
- **Fitness Focus**: Prioritize high-fitness variants
- **Lineage Tracking**: Maintain complete records
- **Dead End Detection**: Identify failed paths early

### 9.3 Scientific Rigor

- **Complete Records**: Log all evolutionary events
- **Reproducibility**: Use version control and locks
- **Analysis**: Regular fitness landscape review
- **Documentation**: Maintain research notes

---

## 10. Troubleshooting

### 10.1 Common Issues

**Agent Not Evolving**:
- Check fitness scores (must be > 0.5)
- Verify Scint Gym evaluation
- Review mutation types

**Flight Recorder Errors**:
- Check `_pyrite` directory permissions
- Verify event format
- Review lineage structure

**Dependency Issues**:
- Run `waft sync`
- Check `uv.lock` status
- Verify Python version (3.10+)

### 10.2 Getting Help

- **Documentation**: See `docs/` directory
- **Issues**: GitHub Issues
- **Community**: WAFT discussions

---

## 11. Future Roadmap

### 11.1 Planned Features

- **Full Evolutionary Cycle Automation**: Complete spawn → gym → select automation
- **Advanced Mutation Strategies**: Genetic algorithm integration
- **Visualization Tools**: Phylogenetic tree visualization
- **Research Dashboard**: Scientific analysis interface

### 11.2 Research Directions

- **God-Head Emergence**: Observing advanced agent intelligence
- **Fitness Landscape Mapping**: Understanding evolution paths
- **Mutation Impact Analysis**: Measuring code change effects
- **Convergence Studies**: Identifying emergent patterns

---

## 12. Conclusion

WAFT provides a comprehensive framework for directed evolution of self-modifying AI agents. Through its three pillars—the Substrate (code as DNA), the Physics (Scint System), and the Flight Recorder (telemetry)—WAFT enables scientific research into the physics of artificial cognition.

**Key Takeaways**:

1. **Code is DNA**: Agents evolve through genetic modifications
2. **Fitness Drives Evolution**: Scint System provides natural selection
3. **Complete Observability**: Flight Recorder enables scientific analysis
4. **Directed Evolution**: Guided by fitness, not random mutation

**The Promise**: "Don't just build agents. Breed them."

---

## References

1. WAFT Repository: https://github.com/ctavolazzi/waft
2. System Overview: `docs/SYSTEM_OVERVIEW.md`
3. Unified Genesis Protocol: `docs/UNIFIED_GENESIS_PROTOCOL.md`
4. AI SDK Vision: `docs/AI_SDK_VISION.md`
5. Evolutionary Architecture: `docs/research/evolutionary_architecture.md`
6. State of the Art: `docs/research/state_of_art_2026.md`

---

## License

MIT

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-12  
**Status**: First Draft
