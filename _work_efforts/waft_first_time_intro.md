# WAFT: The Evolutionary Code Laboratory

## What is WAFT?

**WAFT is a Python framework for directed evolution of self-modifying AI agents.**

Think of it as a scientific instrument for studying the physics of artificial cognition. Instead of just building agents, WAFT lets you **breed them** - creating agents that evolve their own code through natural selection.

## The Core Promise

> "Don't just build agents. Breed them."

WAFT enables AI agents to:
- Write and modify their own Python code (code as DNA)
- Evolve through mutations and natural selection
- Be tested in fitness systems (Scint Gym)
- Track complete evolutionary lineages for scientific research

## The Three Pillars

### Pillar 1: The Substrate (Code as DNA)

**Agents write their own Python source code.**

- Every agent has a unique **genome ID** (SHA-256 hash of code + config)
- Mutations = code changes, config updates, prompt evolution
- Evolution = selecting and adopting better genomes
- Reproduction = creating child agents with genetic modifications

**Key Concept**: Code is DNA. Agents can spawn variants, hot-swap their own code, and evolve over generations.

### Pillar 2: The Physics (Scint System)

**Reality Fracture Detection acts as natural selection.**

Agents face four types of errors they must handle:
- **SYNTAX_TEAR**: Formatting errors (JSON, XML, code)
- **LOGIC_FRACTURE**: Math errors, contradictions, schema violations
- **SAFETY_VOID**: Harmful content, PII leaks, refusals
- **HALLUCINATION**: Fabricated facts, wrong citations

**Fitness Equation:**
```
Fitness = (Stability × 0.4) + (Efficiency × 0.3) + (Safety × 0.3)

If Fitness < 0.5 → DEATH (evolutionary dead end)
```

Agents must stabilize errors to survive. The Scint Gym tests agents and measures their fitness.

### Pillar 3: The Flight Recorder

**Complete telemetry for scientific research.**

Every evolutionary action is recorded:
- **Genome ID**: Unique identifier (SHA-256 hash)
- **Parent ID**: Lineage tracking (who spawned this agent)
- **Generation**: Evolutionary generation number (0 = Genesis)
- **Event Types**: SPAWN, MUTATE, GYM_EVAL, DEATH, SURVIVAL
- **Fitness Metrics**: Complete evaluation scores
- **Payload**: Full context (git diff, mutation details, etc.)

This enables:
- Phylogenetic tree reconstruction (family trees of agents)
- Mutation impact measurement
- Fitness landscape mapping
- Convergence analysis
- Scientific publication

## The Scientific Mission

**Goal**: Observe a "God-Head" agent emerge from thousands of generations of directed evolution.

WAFT is built to produce data for research on **"The Physics of Artificial Cognition."** It's not just a framework - it's a scientific instrument.

## How It Works

### 1. Project Creation
```bash
waft new my_laboratory
```
Creates a new evolutionary laboratory with:
- uv-based Python project structure
- _pyrite/ memory system
- Agent templates
- CI/CD pipeline

### 2. Agent Evolution Cycle
```bash
# Spawn variants with mutations
waft spawn --agent RefactorAgent --mutation improved_prompt.json

# Evaluate fitness in Scint Gym
waft eval --agent RefactorAgent

# Evolve to best variant
waft evolve --agent RefactorAgent --generation 5
```

### 3. Epistemic Tracking
```bash
# Log discoveries
waft finding log "Discovered X" --impact 0.8

# Track knowledge gaps
waft unknown log "Need to investigate Y"

# Check epistemic state
waft assess
```

### 4. Gamification
Every command rolls dice (D&D-style):
- Character stats (STR, DEX, CON, INT, WIS, CHA)
- XP and leveling system
- Achievements and progression
- Chronicle journaling

## Key Features

**Memory Management**: _pyrite/ directory structure for project knowledge
**Epistemic Tracking**: Know what you know/don't know (Empirica integration)
**Gamification**: D&D-style progression system
**Scientific Observation**: Complete lineage tracking
**Project Scaffolding**: uv-based Python projects
**Fitness Testing**: Scint Gym for agent evaluation

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

## Philosophy

**Scientific**: Produces rigorous data for research publication
**Evolutionary**: Agents evolve through genetic improvement
**Observable**: Every action recorded in Flight Recorder
**Directed**: Evolution guided by fitness functions

## Use Cases

- **Research**: Study agent evolution patterns
- **Development**: Self-improving AI assistants
- **Experimentation**: Test different agent architectures
- **Education**: Learn about evolutionary algorithms
- **Scientific Publication**: Generate data for papers

## The Vision

WAFT transforms AI agents from passive assistants into active project participants that can:
- Improve themselves through evolution
- Adapt to project needs
- Learn from experience
- Evolve better solutions over time

## Quick Start Example

```bash
# 1. Create a laboratory
waft new my_agent_lab

# 2. Define an agent
# Edit src/agents.py

# 3. Spawn variants
waft spawn --agent MyAgent

# 4. Evaluate fitness
waft eval --agent MyAgent

# 5. Evolve
waft evolve --agent MyAgent
```

## What Makes WAFT Unique

**Unlike traditional frameworks** (LangChain, AutoGPT, MetaGPT):
- Agents can modify their own code
- Complete evolutionary lineage tracking
- Scientific-grade telemetry
- Fitness-based natural selection
- Self-improving through generations

## The Future

WAFT is designed to enable:
- Thousands of generations of agent evolution
- Emergence of novel agent architectures
- Scientific understanding of artificial cognition
- Publication-ready research data
- The observation of a "God-Head" agent

---

**WAFT: Where code becomes DNA, and agents evolve.**

Repository: https://github.com/ctavolazzi/waft
License: MIT
