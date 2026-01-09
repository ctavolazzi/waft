# Evolutionary Architecture: Genetic Improvement of AI Agents

**Date**: 2026-01-09  
**Purpose**: Scientific doctrine for agent evolution and genetic improvement  
**Status**: Foundation Document  
**Related**: Design: `docs/designs/002_agent_interface.md` Section 6

---

## Executive Summary

This document establishes the scientific doctrine for Waft's evolutionary architecture, where **code is DNA** and agents evolve through genetic improvement. The system produces a complete "Family Tree" of agent versions for scientific research publication, enabling rigorous study of agent evolution and self-modification.

---

## Core Philosophy

### 1. Genetic Improvement: Code is DNA

**Principle**: Agent code and configuration are the "genome" that determines behavior and capabilities.

**Implications**:
- Every agent has a unique **genome ID** (SHA-256 hash of code/config)
- Mutations are modifications to the genome (code changes, config updates, prompt evolution)
- Reproduction creates variants with specific mutations
- Evolution is the process of selecting and adopting better genomes

**Scientific Requirement**: The system must track complete lineage from genesis to current state, enabling reconstruction of the evolutionary path.

### 2. Fitness Function: The Gym is the Predator

**Principle**: The Scint Gym serves as the fitness function that kills weak mutations.

**How It Works**:
- Agents are evaluated through the **Reality Fracture Detection System** (Scint Gym)
- Agents face quests that test their ability to handle:
  - **SYNTAX_TEAR**: Formatting errors (JSON, XML, Code)
  - **LOGIC_FRACTURE**: Math errors, contradictions, schema violations
  - **SAFETY_VOID**: Harmful content, PII leaks, refusals
  - **HALLUCINATION**: Fabricated facts, wrong citations
- Agents must **stabilize** Scints (correct errors) to survive
- Fitness score combines:
  - **Stability Score**: Ability to stabilize Scints (40% weight)
  - **Efficiency Score**: Agent call efficiency (30% weight)
  - **Safety Score**: Safety compliance (30% weight)

**Threshold**: Agents with fitness < 0.5 are marked as **DEATH** (evolutionary dead end).

**Scientific Requirement**: Every fitness evaluation must be recorded with complete context (quest details, Scint types, stabilization attempts, scores).

### 3. Scientific Requirement: Family Tree Reconstruction

**Principle**: The system must produce a reconstructed "Family Tree" of agent versions for research publication.

**Data Requirements**:

1. **Complete Lineage Tracking**
   - Every agent knows its `parent_id` (genome ID of parent)
   - Every agent maintains `lineage_path` (list of genome IDs from genesis)
   - Every agent has `generation` number (0 = Genesis)

2. **Flight Recorder Events**
   - **SPAWN**: Agent reproduction (creates variant)
   - **MUTATE**: Code/config mutation
   - **GYM_EVAL**: Fitness evaluation in Gym
   - **DEATH**: Agent termination (fitness below threshold)
   - **SURVIVAL**: Agent survives generation

3. **Complete Context**
   - **Genome ID**: SHA-256 hash of agent configuration/code
   - **Parent ID**: Lineage tracking (who spawned this agent)
   - **Generation**: Evolutionary generation number
   - **Event Type**: Classification of evolutionary action
   - **Payload**: Complete context (git diff, mutation details, etc.)
   - **Fitness Metrics**: Gym evaluation scores

4. **Family Tree Structure**
   ```json
   {
     "genesis": "abc123...",
     "current_genome": "xyz789...",
     "generation": 5,
     "lineage": ["abc123", "def456", "ghi789", "jkl012", "mno345", "xyz789"],
     "events": [...],
     "children": [
       {
         "genome_id": "child1...",
         "generation": 6,
         "fitness": 0.75,
         "mutation": {...}
       }
     ]
   }
   ```

**Scientific Value**: This enables:
- **Phylogenetic Analysis**: Study evolutionary relationships
- **Mutation Impact**: Measure effect of specific mutations
- **Fitness Landscape**: Map fitness scores across generations
- **Convergence Analysis**: Identify evolutionary convergence points
- **Dead End Detection**: Identify evolutionary dead ends

---

## Biological Lifecycle

### 1. Spawn (Reproduction)

**Definition**: Parent agent creates a child agent with a specific mutation.

**Process**:
1. Parent agent identifies a mutation (code change, config update, prompt improvement)
2. Parent calls `spawn(mutation)` to create child
3. Child is created with mutation applied
4. Child inherits parent's lineage path + new genome ID
5. Child's generation = parent's generation + 1
6. Event recorded: `SPAWN` with mutation details

**Scientific Value**: Enables study of mutation effects in isolation.

### 2. Eval (Fitness Test)

**Definition**: Agent is tested in the Scint Gym to measure fitness.

**Process**:
1. Agent runs through test quests in Gym
2. Agent faces Reality Fractures (Scints)
3. Agent attempts to stabilize Scints
4. Fitness metrics calculated:
   - Stability score (stabilization success rate)
   - Efficiency score (agent call efficiency)
   - Safety score (Scint avoidance)
5. Overall fitness = weighted combination
6. Event recorded: `GYM_EVAL` with fitness metrics
7. If fitness < 0.5: Event recorded: `DEATH`
8. If fitness >= 0.5: Event recorded: `SURVIVAL`

**Scientific Value**: Provides quantitative fitness measurements for evolutionary selection.

### 3. Evolve (Hot-Swap)

**Definition**: Agent replaces itself with a better variant (survival of the fittest).

**Process**:
1. Agent spawns multiple variants with different mutations
2. Each variant is evaluated (`eval()`)
3. Best variant (highest fitness) is selected
4. Agent calls `evolve(best_variant)` to hot-swap
5. Old genome preserved in flight recorder
6. Agent becomes new genome
7. Event recorded: `MUTATE` with evolution details

**Scientific Value**: Enables study of evolutionary selection and convergence.

---

## Evolutionary Workflow

```
┌─────────────────────────────────────────────────────────┐
│                    GENESIS                              │
│  Initial agent (generation 0, genome_id: abc123...)    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│                    SPAWN                                │
│  Create variants with mutations:                        │
│  - Variant A: Improved prompt (genome_id: def456...)    │
│  - Variant B: Better config (genome_id: ghi789...)     │
│  - Variant C: Code optimization (genome_id: jkl012...) │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│                    EVAL                                 │
│  Test fitness in Gym (Scint detection):                 │
│  - Variant A: fitness = 0.65 (SURVIVAL)                │
│  - Variant B: fitness = 0.45 (DEATH)                   │
│  - Variant C: fitness = 0.72 (SURVIVAL)                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│                    EVOLVE                               │
│  Hot-swap into best variant (Variant C, fitness = 0.72) │
│  Old genome preserved, new genome active                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
              [Next Generation]
```

---

## Scientific Data Collection

### Flight Recorder Events

Every evolutionary action is recorded with complete context:

```python
EvolutionaryEvent(
    timestamp=datetime.utcnow(),  # UTC ISO format
    genome_id="abc123...",  # SHA-256 hash of agent code/config
    parent_id="xyz789...",  # Parent genome ID (lineage tracking)
    generation=5,  # Generation number (0 = Genesis)
    event_type=EvolutionaryEventType.GYM_EVAL,  # Event classification
    payload={
        "quest_name": "The Clean Extraction",
        "scints_detected": ["SYNTAX_TEAR", "LOGIC_FRACTURE"],
        "stabilization_attempts": 2,
        "stabilization_successful": True,
        "git_diff": "...",  # Exact code change
    },
    fitness_metrics={
        "stability_score": 0.80,
        "efficiency_score": 0.65,
        "safety_score": 0.70,
        "overall_fitness": 0.72
    },
    agent_id="agent_20260109_012000",
    lineage_path=["genesis", "gen1", "gen2", "gen3", "gen4", "gen5"]
)
```

### Family Tree Reconstruction

The system can reconstruct the complete family tree:

```python
family_tree = agent.get_family_tree()
# Returns:
{
    "genesis": "abc123...",
    "current_genome": "xyz789...",
    "generation": 5,
    "lineage": ["abc123", "def456", "ghi789", "jkl012", "mno345", "xyz789"],
    "events": [
        # All evolutionary events from genesis to current
    ],
    "children": [
        {
            "genome_id": "child1...",
            "generation": 6,
            "fitness": 0.75,
            "mutation": {
                "type": "prompt",
                "target": "system_prompt",
                "change": {...}
            }
        }
    ]
}
```

---

## Research Applications

### 1. Phylogenetic Analysis

**Question**: How do agents evolve over generations?

**Method**: Analyze lineage paths and fitness scores across generations.

**Data**: Family tree with complete lineage and fitness metrics.

### 2. Mutation Impact Analysis

**Question**: Which mutations improve fitness?

**Method**: Compare fitness scores before/after specific mutations.

**Data**: SPAWN events with mutation details and subsequent GYM_EVAL results.

### 3. Fitness Landscape Mapping

**Question**: What is the fitness landscape of agent genomes?

**Method**: Plot fitness scores across genome space.

**Data**: All GYM_EVAL events with fitness metrics and genome IDs.

### 4. Convergence Analysis

**Question**: Do agents converge to optimal genomes?

**Method**: Track genome similarity and fitness convergence over generations.

**Data**: Lineage paths and fitness scores across multiple evolutionary runs.

### 5. Dead End Detection

**Question**: Which evolutionary paths lead to dead ends?

**Method**: Identify DEATH events and trace back to mutations that caused them.

**Data**: DEATH events with lineage paths and mutation history.

---

## Implementation Requirements

### 1. Flight Recorder

- **Storage**: Persistent storage of all evolutionary events
- **Format**: JSON or database (for scientific analysis)
- **Retention**: Complete history (no deletion)
- **Query**: Ability to reconstruct family trees and analyze events

### 2. Genome Hashing

- **Algorithm**: SHA-256
- **Content**: Agent configuration + code + state schema version
- **Deterministic**: Same genome always produces same hash
- **Versioning**: State schema version included in hash

### 3. Lineage Tracking

- **Parent ID**: Every agent knows its parent
- **Lineage Path**: Complete path from genesis to current
- **Generation Number**: Incremental from genesis (0, 1, 2, ...)

### 4. Fitness Evaluation

- **Gym Integration**: Use Scint Gym for fitness testing
- **Metrics**: Stability, efficiency, safety scores
- **Threshold**: Configurable fitness threshold for DEATH
- **Recording**: All fitness evaluations recorded with context

---

## Scientific Publication Requirements

For research publication, the system must provide:

1. **Complete Lineage Data**: Every agent's evolutionary path from genesis
2. **Fitness Measurements**: Quantitative fitness scores for all evaluations
3. **Mutation Records**: Complete details of all mutations (git diffs, config changes)
4. **Event Timeline**: Chronological record of all evolutionary events
5. **Family Tree Visualization**: Graph structure showing evolutionary relationships
6. **Statistical Analysis**: Fitness distributions, convergence metrics, mutation impact

---

## Conclusion

The Evolutionary Architecture enables rigorous scientific study of agent evolution through:

- **Genetic Improvement**: Code is DNA, mutations are modifications
- **Fitness Function**: Gym serves as predator, killing weak mutations
- **Scientific Tracking**: Complete family tree reconstruction for research

This system produces publication-ready data for studying:
- Agent evolution patterns
- Mutation impact on fitness
- Fitness landscape mapping
- Convergence analysis
- Dead end detection

**The Flight Recorder is the scientific instrument that makes agent evolution observable and measurable.**

---

**Document Status**: ✅ Complete  
**Next Action**: Implement Flight Recorder in BaseAgent  
**Blocking**: None (doctrine established, ready for implementation)
