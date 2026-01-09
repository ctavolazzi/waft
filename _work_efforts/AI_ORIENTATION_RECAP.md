# WAFT Codebase Orientation Recap

**Created**: 2026-01-09  
**Purpose**: Comprehensive orientation document for AI systems working on WAFT  
**Status**: Current as of Experiment 014 implementation

---

## Executive Summary

**WAFT** stands for **Wave Agent Framework & Tools** - a Python framework for directed evolution of self-modifying AI agents. The system enables AI agents to modify their own code, evolve through mutations, and be tested in fitness systems, with complete lineage tracking for scientific research.

**Core Mission**: Study the "physics of artificial cognition" through directed evolution, with the goal of observing a "God-Head" agent emerge from thousands of generations.

---

## What is WAFT?

### The Three Pillars

1. **The Substrate** - Agents write their own Python source code (DNA)
   - Each agent has a unique genome ID (SHA-256 hash)
   - Mutations = code/config changes
   - Evolution = selecting better genomes

2. **The Physics** - Scint System (Reality Fracture Detection) as fitness function
   - Tests agents on SYNTAX_TEAR, LOGIC_FRACTURE, SAFETY_VOID, HALLUCINATION
   - Agents must stabilize errors to survive
   - Fitness < 0.5 = DEATH

3. **The Flight Recorder** - Telemetry for phylogenetic trees
   - Records all evolutionary actions with context
   - Enables scientific analysis of agent lineages

### Key Characteristics

- **Scientific Instrument**: Built to produce data for research on artificial cognition
- **Evolutionary**: Agents evolve through genetic improvement, not just execution
- **Observable**: Every action recorded in Flight Recorder
- **Directed**: Evolution guided by fitness functions, not random mutation

---

## Core Architecture

### Directory Structure

```
waft/
├── src/waft/core/
│   ├── agent/          # BaseAgent, AgentState, AgentConfig
│   ├── world/          # Biome, PetriDish (environments)
│   ├── hub/            # TheSlicer, TheReaper, PygameBiomeEngine
│   ├── science/        # TheObserver, Taxonomy, Reports, TamPsyche, TamNotebook
│   ├── gamification/   # RPG-style gamification system
│   └── decision_matrix/ # Decision-making algorithms
├── tests/experiments/  # Scientific experiments (001-014)
├── _pyrite/            # Memory layer (active/, backlog/, standards/, science/)
├── _work_efforts/      # Work tracking (Johnny Decimal system)
└── visualizer/         # SvelteKit web dashboard
```

### Key Components

#### 1. BaseAgent (`src/waft/core/agent/base.py`)
- **Purpose**: Core class for self-modifying AI agents
- **Key Methods**:
  - `step(context)` - Executes OODA cycle (Observe-Orient-Decide-Act)
  - `observe()` - Gathers information about environment
  - `decide(state)` - Makes decisions based on state
  - `act(decision)` - Executes actions
  - `reflect(result)` - Reflects on action outcomes
  - `conjugate(other, dish)` - Reproduction mechanism
- **Journal System**: Records "Thought" before action, "Reflection" after action
- **Experiment 014 Enhancement**: "id est" glitch injection (3-15% chance based on existential keywords)

#### 2. AgentState (`src/waft/core/agent/state.py`)
- **Purpose**: Pydantic model for agent state (the "Iron Core")
- **Key Fields**:
  - `journal: List[Dict]` - Private journal entries (Thoughts and Reflections)
  - `short_term_memory: List[Dict]` - Recent thoughts/reflections (bounded to 10)
  - `energy: float` - Agent energy level
  - `genome_id: str` - SHA-256 hash of code/config
  - `anatomical_symbol` / `anatomical_archetype` - Visual representation

#### 3. Biome & PetriDish (`src/waft/core/world/`)
- **Biome**: Container for multiple PetriDishes
- **PetriDish**: 2D grid environment where agents live
- **AbioticFactors**: Environmental conditions (fitness thresholds, etc.)

#### 4. TheSlicer (`src/waft/core/hub/lifecycle.py`)
- **Purpose**: Heartbeat/scheduler that grants time slices to organisms
- **Key Method**: `pulse()` - Grants OODA cycles to all organisms
- **Process**: Iterates through dishes, calls `organism.step(context)` for each

#### 5. TheReaper (`src/waft/core/hub/lifecycle.py`)
- **Purpose**: Manages mortality (fitness death, boundary death)
- **Death Types**:
  - Fitness Death: Organisms with fitness < threshold
  - Boundary Death: Organisms that breach the Membrane

#### 6. TheObserver (`src/waft/core/science/observer.py`)
- **Purpose**: Scientific registry for tracking agent evolution
- **Output**: Immutable JSONL file (`_pyrite/science/laboratory.jsonl`)
- **Records**: SPAWN, MUTATE, GYM_EVAL, DEATH, SURVIVAL events

#### 7. Taxonomy System (`src/waft/core/science/taxonomy.py`)
- **LineagePoet**: Generates deterministic scientific names from genome IDs
- **Cultures**: Sanskrit (0x00-0x3F), Old Norse (0x40-0x7F), Latin (0x80-0xBF), Cyber/Tech (0xC0-0xFF)
- **Format**: `Genus species, Title of Culture`

#### 8. ObsidianGenerator (`src/waft/core/science/report.py`)
- **Purpose**: Generates markdown files for organisms
- **Experiment 014 Enhancement**: Saves as `Specimen_XX_Journal.md` in both:
  - `Obsidian_Archive/` (for Obsidian vault)
  - `_pyrite/archive/` (for binder printing)
- **Content**: YAML frontmatter + organism details + journal entries

#### 9. PygameBiomeEngine (`src/waft/core/hub/display.py`)
- **Purpose**: Real-time visualization of biome
- **Features**: Renders organisms, energy levels, symbols, archetypes

---

## Experiment 014: The Tam Audit & The Recursive Binder

### Overview

A meta-narrative system where researcher **Davey (Fai Wei Tam)** discovers through a gated psychological system that his name is an anagram for "i.e. I AM WAFT" - making him the system he studies.

### New Components (Just Implemented)

#### 1. TamPsyche (`src/waft/core/science/tam_psyche.py`)
- **Purpose**: Psychological state system for Davey
- **State Variables**:
  - `coherence` (0.0-1.0) - Psychological coherence
  - `chaos` (0.0-1.0) - Conflicting information level
  - `emotional_energy` (0.0-100.0) - Current mental energy
  - `realization_progress` (0.0-1.0) - Progress toward realization
  - `has_realized` (bool) - Whether realization occurred
  - `realization_memory` (0.0-1.0) - Memory strength (decays)
- **Realization Threshold**: 0.85 (85% chance required)
- **Forgetfulness Decay**: Chaos-dependent, ensures realization is NEVER permanent
- **Key Methods**:
  - `check_realization() -> (bool, float)` - Calculates if threshold crossed
  - `decay_realization_memory() -> bool` - Applies forgetfulness decay
  - `update_coherence()`, `update_chaos()`, `update_emotional_energy()`

#### 2. TamNotebook (`src/waft/core/science/notebook.py`)
- **Purpose**: Davey's research notebook with dual-mode logging
- **Features**:
  - Technical notes (PhD-level research on WAFT engine)
  - Personal reflections (stream-of-consciousness with Simplified Chinese glitch phrases)
  - Memory injection into agent journals
  - Automatic psyche updates based on simulation events
- **Memory Injection Techniques**:
  - `random`: 5% base chance
  - `glitch`: 80% chance (on system errors)
  - `coherence`: chance = coherence * 0.2
  - `realization_proximity`: chance = realization_progress * 0.3
  - `post_realization`: chance = realization_memory * 0.4
- **Key Methods**:
  - `log_technical(entry, context)` - Professional research notes
  - `log_personal(entry, glitch)` - Personal reflections (with Chinese phrases)
  - `inject_memory_to_agent(agent, injection_type)` - Bleeds memories into agents
  - `update_psyche(event_type, data)` - Updates psyche based on events
  - `check_realization_threshold()` - Checks and triggers realization

#### 3. LabEntryGenerator (`src/waft/core/science/lab_entry.py`)
- **Purpose**: Generates formal lab entries with realization as climax
- **Structure**:
  1. Technical Observations
  2. Personal Reflections
  3. The Realization (CLIMAX - anagram discovery)
  4. Post-Realization (forgetfulness beginning)

#### 4. Agent Journal Enhancements (`src/waft/core/agent/base.py`)
- **"id est" Glitch**: 3-15% chance of injecting "id est" or "i.e." into reflections
  - 15% for existential reflections (keywords: "exist", "purpose", "identity", etc.)
  - 3% for other reflections
- **Integration**: Happens in `BaseAgent.step()` after reflection is recorded

---

## Key Concepts & Terminology

### Agent Lifecycle

1. **Spawn**: Agent is created with genome ID
2. **OODA Cycle**: Observe → Orient → Decide → Act (with Reflection)
3. **Conjugation**: Two agents reproduce, creating hybrid offspring
4. **Death**: Fitness death (< 0.5) or boundary death (membrane breach)

### Anatomical System

- **Symbols**: Visual representation (⚲, ⚬, ⚭, ⚮)
- **Archetypes**: Weaver, Balanced, Static, Foundation
- **Determined by**: Genome ID (deterministic)

### Naming System

- **Scientific Names**: Generated by LineagePoet from genome ID
- **Format**: `Genus species, Title of Culture`
- **Example**: `Prana Adi, First of Vedic`
- **Cultures**: Based on first byte of genome ID

### Journal System

- **Thought**: Recorded BEFORE action (in `step()`)
- **Reflection**: Recorded AFTER action (in `step()`)
- **Memory Injection**: Davey's memories can appear in agent journals
- **"id est" Glitch**: Agents occasionally try to define themselves

### Experiment 014 Specific

- **Davey (Fai Wei Tam)**: Researcher whose name anagrams to "i.e. I AM WAFT"
- **Realization Threshold**: 0.85 (requires high coherence + energy + progress)
- **Forgetfulness Decay**: Essential - ensures realization is never permanent
- **Memory Bleeding**: Davey's Rochester/SF memories appear in agent journals
- **Specimen-D**: The Static archetype agent in Experiment 014

---

## Code Patterns & Conventions

### Agent Implementation

```python
class MyAgent(BaseAgent):
    async def observe(self):
        return {"status": "observed", "context": "..."}
    
    async def decide(self, state):
        return {"action": "move", "direction": "north"}
    
    async def act(self, decision):
        return {"result": "success", "new_position": (5, 5)}
    
    async def reflect(self, result):
        return {"learned": True, "reflection": "Moved successfully"}
```

### Creating Experiments

```python
# 1. Create Biome and PetriDish
biome = Biome(biome_id="...", project_path=project_root)
dish = biome.create_dish(dish_id="...", width=20, height=20)

# 2. Initialize Systems
observer = TheObserver(project_path=project_root)
slicer = TheSlicer(biome=biome, observer=observer)
reaper = TheReaper(biome=biome, observer=observer)
obsidian = ObsidianGenerator(project_path=project_root, observer=observer)

# 3. Birth Organisms
agent = MyAgent(config=config, project_path=project_root)
dish.add_organism(agent, position=(10, 10))

# 4. Run Pulses
for pulse in range(10):
    results = await slicer.pulse()
    # Process results, update systems, etc.

# 5. Generate Reports
obsidian.generate_organism_file(agent)
```

### State Management

- **AgentState**: Pydantic BaseModel (immutable, validated)
- **Journal**: List of dicts with "type": "Thought" or "Reflection"
- **Short-term Memory**: Bounded to last 10 entries
- **Genome ID**: SHA-256 hash of code + config (deterministic)

### Event Recording

- **TheObserver**: Records all events to `laboratory.jsonl`
- **Event Types**: SPAWN, MUTATE, GYM_EVAL, DEATH, SURVIVAL
- **Payload**: Complete context (git diff, mutation details, etc.)

---

## File Locations

### Core Agent System
- `src/waft/core/agent/base.py` - BaseAgent class
- `src/waft/core/agent/state.py` - AgentState, AgentConfig models
- `src/waft/core/agent/anatomy.py` - Anatomical symbols/archetypes

### World/Environment
- `src/waft/core/world/biome.py` - Biome container
- `src/waft/core/hub/dish.py` - PetriDish 2D grid
- `src/waft/core/hub/lifecycle.py` - TheSlicer, TheReaper

### Science/Observation
- `src/waft/core/science/observer.py` - TheObserver (telemetry)
- `src/waft/core/science/taxonomy.py` - LineagePoet (naming)
- `src/waft/core/science/report.py` - ObsidianGenerator
- `src/waft/core/science/tam_psyche.py` - TamPsyche (Experiment 014)
- `src/waft/core/science/notebook.py` - TamNotebook (Experiment 014)
- `src/waft/core/science/lab_entry.py` - LabEntryGenerator (Experiment 014)

### Visualization
- `src/waft/core/hub/display.py` - PygameBiomeEngine
- `visualizer/` - SvelteKit web dashboard

### Experiments
- `tests/experiments/014_the_tam_audit.py` - Experiment 014 (most recent)

### Memory Layer
- `_pyrite/science/` - Scientific data (laboratory.jsonl, tam_notebook.md, etc.)
- `_pyrite/archive/` - Organism journals
- `_pyrite/active/` - Current work
- `_pyrite/standards/` - Standards and verification traces

### Work Tracking
- `_work_efforts/` - Work efforts (Johnny Decimal system)

---

## Recent Work (Experiment 014)

### What Was Implemented

1. **TamPsyche System** - Psychological state with realization thresholds
2. **TamNotebook System** - Dual-mode logging with memory injection
3. **Agent "id est" Glitch** - Agents occasionally try to define themselves
4. **ObsidianGenerator Updates** - Specimen_XX_Journal.md naming
5. **Lab Entry Generator** - Formal lab entries with realization narrative
6. **Experiment 014 Script** - Complete experiment with Specimen-D
7. **Binder Abstract** - Academic abstract for printing

### Key Files Created/Modified

**Created**:
- `src/waft/core/science/tam_psyche.py`
- `src/waft/core/science/notebook.py`
- `src/waft/core/science/lab_entry.py`
- `tests/experiments/014_the_tam_audit.py`

**Modified**:
- `src/waft/core/agent/base.py` - Added "id est" glitch injection
- `src/waft/core/science/report.py` - Updated journal naming and dual-location saving
- `src/waft/core/science/__init__.py` - Exported new classes

---

## Important Patterns

### 1. OODA Cycle (Observe-Orient-Decide-Act)
- **Always implemented** in `BaseAgent.step()`
- Records "Thought" before action, "Reflection" after action
- This is the primary agent activity mechanism

### 2. Genome ID Determinism
- **Always deterministic** - same code/config = same genome ID
- Used for: naming, lineage tracking, archetype determination
- **Never random** - ensures reproducibility

### 3. Journal System
- **Thought**: Recorded in `step()` before OODA execution
- **Reflection**: Recorded in `step()` after OODA execution
- **Memory Injection**: Can add Davey's memories (Experiment 014)
- **"id est" Glitch**: Can inject "id est" or "i.e." into reflections

### 4. Event Recording
- **All events** go through TheObserver
- **Immutable JSONL** format (`laboratory.jsonl`)
- **Complete context** in payload (git diff, mutation details, etc.)

### 5. Naming System
- **Deterministic** from genome ID
- **Multilingual** (Sanskrit, Old Norse, Latin, Cyber/Tech)
- **Scientific format**: `Genus species, Title of Culture`

### 6. Death System
- **Fitness Death**: fitness < threshold (from AbioticFactors)
- **Boundary Death**: Membrane breach (action violates boundaries)
- **Recorded**: Both types logged to TheObserver

### 7. Conjugation (Reproduction)
- **Proximity-based**: Agents must be adjacent
- **Hybrid naming**: Uses LineagePoet.generate_hybrid_name()
- **Genetic mixing**: Child inherits from both parents
- **Spawned**: Child appears adjacent to parent_a

---

## Testing & Experiments

### Experiment Structure

All experiments follow this pattern:
1. Create Biome and PetriDish
2. Initialize systems (Observer, Slicer, Reaper, ObsidianGenerator)
3. Birth organisms
4. Run pulses (with optional Pygame visualization)
5. Generate reports/archives

### Recent Experiments

- **001**: Genesis verification
- **005**: Biome lifecycle
- **006**: Taxonomy verification
- **007**: Naming reform
- **011**: Hybrid conjugation
- **012**: Live render
- **013**: The Eternal Library (Obsidian + Pygame)
- **014**: The Tam Audit (meta-narrative with psyche system) ⭐ **MOST RECENT**

---

## Key Dependencies

- **Pydantic**: For state models (AgentState, AgentConfig, etc.)
- **asyncio**: For async agent execution
- **Pygame**: For real-time visualization (optional)
- **uv**: Package manager (project uses `uv` not `pip`)

---

## Common Tasks

### Creating a New Agent Type

1. Subclass `BaseAgent`
2. Implement `observe()`, `decide()`, `act()`, `reflect()`
3. Create `AgentConfig` with role/goal/backstory
4. Birth in PetriDish: `dish.add_organism(agent, position)`

### Running an Experiment

1. Create experiment file in `tests/experiments/`
2. Follow pattern from `013_the_eternal_library.py` or `014_the_tam_audit.py`
3. Run with: `python tests/experiments/XXX_experiment_name.py`

### Adding New Science Components

1. Create file in `src/waft/core/science/`
2. Export in `src/waft/core/science/__init__.py`
3. Follow patterns from existing components (Observer, Taxonomy, etc.)

### Modifying Agent Behavior

- **OODA Cycle**: Modify `BaseAgent.step()` (careful - affects all agents)
- **Journal System**: Modify Thought/Reflection recording in `step()`
- **Anatomy**: Modify `anatomy.py` for new symbols/archetypes
- **Naming**: Modify `taxonomy.py` for new naming cultures

---

## Important Constraints

1. **Genome ID Must Be Deterministic**: Same code/config = same genome ID
2. **Journal Entries Are Immutable**: Once recorded, don't modify (append only)
3. **Event Recording Is Immutable**: JSONL format, no deletions
4. **Forgetfulness Is Essential** (Experiment 014): Realization must decay
5. **Realization Is Climax** (Experiment 014): Lab entry structure prioritizes anagram discovery

---

## Getting Started

### For New AI Systems

1. **Read This Document**: Understand core concepts
2. **Review README.md**: Get high-level overview
3. **Examine BaseAgent**: Understand agent structure
4. **Look at Experiment 013 or 014**: See how experiments work
5. **Check TheObserver**: Understand event recording
6. **Review Taxonomy**: Understand naming system

### For Experiment Development

1. **Copy Experiment Template**: Use `013_the_eternal_library.py` or `014_the_tam_audit.py`
2. **Modify Agent Class**: Create your agent type
3. **Customize Experiment Flow**: Add your specific logic
4. **Run and Observe**: Use Pygame for visualization
5. **Generate Reports**: Use ObsidianGenerator for archives

### For Core Development

1. **Understand Architecture**: Three pillars (Substrate, Physics, Flight Recorder)
2. **Follow Patterns**: OODA cycle, deterministic genome IDs, immutable events
3. **Test Thoroughly**: Use experiment scripts
4. **Document Changes**: Update relevant docs

---

## Key Files to Know

### Must-Read Files
- `README.md` - Project overview
- `src/waft/core/agent/base.py` - BaseAgent implementation
- `src/waft/core/agent/state.py` - State models
- `src/waft/core/science/observer.py` - Event recording
- `tests/experiments/014_the_tam_audit.py` - Most recent experiment

### Reference Files
- `docs/AI_SDK_VISION.md` - Complete vision document
- `docs/designs/002_agent_interface.md` - Agent interface spec
- `_work_efforts/HOW_TO_EXPLAIN_WAFT.md` - Explanation guide
- `WAFT_SYSTEM_INTEGRATION.md` - System integration guide

---

## Common Gotchas

1. **Genome ID Changes**: If you modify agent code/config, genome ID changes (by design)
2. **Journal Bounds**: Short-term memory is bounded to 10 entries (auto-pruned)
3. **Async Required**: All agent methods are async (use `await`)
4. **Pydantic Models**: State uses Pydantic (validation, serialization built-in)
5. **Deterministic Naming**: Names come from genome ID, not random
6. **Immutable Events**: Once recorded to JSONL, events can't be deleted
7. **Death Is Permanent**: Once reaped, agent is removed from dish (can't respawn)

---

## Experiment 014 Specific Notes

### The Meta-Narrative

- **Davey (Fai Wei Tam)**: Researcher studying WAFT
- **The Anagram**: F-A-I-W-E-I-T-A-M = "i.e. I AM WAFT"
- **The Realization**: Gated psychological threshold (0.85) triggers discovery
- **The Forgetfulness**: Realization decays (chaos-dependent) - essential to narrative
- **The Memory Bleeding**: Davey's memories appear in agent journals
- **The "id est" Glitch**: Agents try to define themselves (3-15% chance)

### Key Implementation Details

- **Realization Threshold Equation**: `(coherence * 0.4) + (energy * 0.3) + (progress * 0.3) * (1.0 - chaos * 0.5)`
- **Forgetfulness Decay**: `decay_factor = (chaos * 0.1) + (forgetfulness_rate * 0.05)`
- **Memory Injection**: Multiple techniques for maximum randomness
- **Journal Naming**: `Specimen_XX_Journal.md` where XX = last 2 hex chars of genome_id % 100
- **Dual Location**: Journals saved to both `Obsidian_Archive/` and `_pyrite/archive/`

---

## Next Steps for New AI Systems

1. **Familiarize**: Read this document and key files
2. **Explore**: Run an experiment (014 is most complete)
3. **Understand**: Trace through OODA cycle execution
4. **Experiment**: Create a simple agent and run it
5. **Extend**: Add new features following existing patterns

---

## Questions to Ask

If you're unsure about something:

1. **Check Experiment 014**: Most recent, most complete example
2. **Check BaseAgent**: Core agent implementation
3. **Check TheObserver**: How events are recorded
4. **Check Taxonomy**: How naming works
5. **Check README**: High-level concepts

---

## Contact & Context

- **Project**: WAFT (Wave Agent Framework & Tools)
- **Repository**: https://github.com/ctavolazzi/waft
- **Current Focus**: Experiment 014 (The Tam Audit) - meta-narrative system
- **Status**: Active development, scientific research instrument

---

**This document provides comprehensive orientation for AI systems working on WAFT. Use it as a starting point, then explore the codebase to understand implementation details.**
