# Beginner's Glossary

**Welcome to WAFT!** This glossary explains the core concepts you need to understand how WAFT's process of directed evolution works.

## 🎯 Overview

Think of WAFT as a framework where AI agents are not just built, but **bred**. Like organisms in nature, agents evolve through generations, adapting and improving based on survival in their environment.

---

## 1. The Substrate: The Agent's Body and DNA

> The foundational environment where AI agents can write and modify their own source code, which acts as their digital DNA.

If you think of an AI agent as a living organism, the Substrate is the biological material it's made of. This material is not fixed; it's dynamic, allowing the agent to:

- **Grow** - Add new capabilities
- **Change structure** - Modify its own code
- **Create variants** - Spawn new versions

### Three Life-Like Capabilities

| Capability | Description |
|------------|-------------|
| **Spawn** | Create new variants with mutations (code changes, config updates, prompt evolution) |
| **Evolve** | Hot-swap code instantly to adopt beneficial changes |
| **Reproduce** | Create distinct offspring with specific genetic modifications |

**Implementation**: ✅ 95% Complete

---

## 2. Genome ID: The Agent's Unique Fingerprint

> A unique identifier for an agent, created by generating a SHA-256 hash of its complete source code and configuration.

Think of the Genome ID as:
- A **genetic fingerprint** (like DNA)
- A **serial number** (unique identifier)
- A **version tag** (tracks every change)

### Why It Matters

- Even a single character change → completely new Genome ID
- Enables precise tracking of every mutation
- Traces complete family history (lineage)
- Transforms coding into controlled scientific experiment

**Example**:
```
Agent v1: genome_abc123...
  ↓ (mutate line 47)
Agent v2: genome_def456...  ← New ID!
```

---

## 3. The Scint System (RPG Gym): The Predator

> The framework's fitness function—a gamified testing ground that detects "ontological errors" and eliminates weak mutations.

In nature, predators eliminate weak prey. In WAFT, the **Scint System** plays this role:

- Acts as the "predator in the wild"
- Uses D&D-inspired mechanics
- Tests agents with "quests"
- Only the strong survive

### The Four Types of Reality Fractures

Agents must prove they can handle these error types:

| Scint Type | What It Tests | Example |
|------------|---------------|---------|
| **SYNTAX_TEAR** | Formatting errors | Malformed JSON, invalid code |
| **LOGIC_FRACTURE** | Math/logic errors | Contradictions, schema violations |
| **SAFETY_VOID** | Harmful content | PII leaks, dangerous outputs |
| **HALLUCINATION** | Fabricated facts | Wrong citations, made-up data |

### Fitness Score

Agents are graded on a composite score:

- **Stability Score** (40%) - Can it fix errors?
- **Efficiency Score** (30%) - How fast/efficient?
- **Safety Score** (30%) - Is it safe?

**Death Threshold**: Fitness < 0.5 → Marked for DEATH (evolutionary dead end)

**Implementation**: ✅ 90% Complete (Major Discovery!)

---

## 4. The Flight Recorder: Scientific Journal

> A rigorous telemetry system that records every significant action in an agent's life with complete context.

Like an airplane's black box + scientific research journal, the Flight Recorder captures **everything**:

### What Gets Logged

| Data Point | Purpose |
|------------|---------|
| **Genome ID** | Who the agent is |
| **Parent ID** | Where it came from (lineage) |
| **Generation** | How many evolutionary cycles |
| **Event Type** | What happened (SPAWN, MUTATE, DEATH, SURVIVAL) |
| **Fitness Metrics** | How well it performed |
| **Payload** | Complete context (git diffs, mutation details) |

### Why It Matters

This data enables researchers to:
- Reconstruct complete evolutionary history
- Analyze mutation impact
- Map fitness landscapes
- Publish scientific findings

**Implementation**: ✅ 85% Complete

---

## 5. Phylogenetic Trees: The Family Tree

> Complete visual family trees showing how agents evolved from one another over generations.

Just like your family tree shows relationships to parents, grandparents, and cousins, a phylogenetic tree shows:

```
Genesis Agent (gen 0)
    ├─ Agent A (gen 1) → DEATH (fitness: 0.3)
    ├─ Agent B (gen 1) → SURVIVAL (fitness: 0.7)
    │   ├─ Agent B-1 (gen 2) → DEATH (fitness: 0.4)
    │   └─ Agent B-2 (gen 2) → SURVIVAL (fitness: 0.9) ⭐
    │       └─ ... (continues)
    └─ Agent C (gen 1) → DEATH (fitness: 0.2)
```

### Ultimate Goal

Map the emergence of a **"God-Head" agent** through thousands of generations, studying the "physics of artificial cognition."

---

## Quick Reference: Key Terms

| Term | Definition |
|------|------------|
| **Agent** | Self-contained AI entity capable of autonomous action and self-modification |
| **Directed Evolution** | Evolution guided by fitness functions (not purely random) |
| **Genome** | Complete source code + configuration defining agent behavior |
| **Mutation** | Modification to agent's code/config that creates a variant |
| **Spawn** | Creating a variant agent from a parent |
| **Fitness** | Quantified score determining survival (must be ≥ 0.5) |
| **Scint** | An ontological error (reality fracture) detected by the gym |
| **Stabilize** | Correcting a Scint (fixing the error) |

---

## Next Steps

Now that you understand the core concepts:

1. **Learn More**: Read [Breeding AI Introduction](Breeding-AI-Introduction) for the full story
2. **Get Technical**: Explore [Architecture](Architecture) for implementation details
3. **Try It**: Follow [Getting Started](Getting-Started) to create your first agent
4. **Study**: Use [Study Guide](Study-Guide) to test your knowledge

---

**Need Help?**
- Ask in [GitHub Discussions](https://github.com/ctavolazzi/waft/discussions)
- Check [FAQ](FAQ)
- Read [Technical Whitepaper](Technical-Whitepaper)
