# Entity/Being Timeless/Timeful Distinction

**Date**: 2026-01-15  
**Status**: Design Document  
**Related Work**: [WE-260115-enti](../_work_efforts/WE-260115-enti_entity_being_timeless_timeful_distinction/WE-260115-enti_index.md)

---

## Overview

The WAFT system distinguishes between two fundamental types of entities:

1. **Entities (Pantheon)**: Timeless Forces that Bind Reality Together
2. **Beings**: Timeful, dynamic agents that explore, learn, and evolve

This distinction is fundamental to the system's architecture and philosophy.

---

## Philosophy

### The Balance of Stability and Change

The system maintains a balance between:
- **Stability** (Entities): Fundamental aspects of creation that should not change without evidence
- **Change** (Beings): Dynamic exploration and evolution that collects evidence

Entities provide the stable foundation that binds reality together, while Beings explore and collect evidence that may prove Entities need to evolve.

### Evidence-Based Evolution

Entities only change when Beings collect sufficient evidence to prove that change is warranted. This ensures that:
- Fundamental aspects of creation remain stable
- Change only occurs when justified by evidence
- The system maintains coherence while allowing evolution

---

## Entities (Pantheon) - Timeless

### Nature

**Entities are Forces that Bind Reality Together.**

They are timeless, stable aspects of creation that maintain the fundamental structure of reality.

### Characteristics

- **Timeless**: They don't move much and change very slowly
- **Stable**: They hold Aspects of Creation that should not change until evidence proves change is needed
- **Forces of Binding**: They maintain the fundamental structure of reality
- **Evidence-Based Change**: They only evolve when Beings collect sufficient evidence to warrant modification

### Examples

- **Magistrate**: God of Precedent and Body of Proof - maintains legal precedents
- **Judge**: God of Judgment and Evaluation - maintains judgment standards
- **Fae**: Entity of Whimsy, Creativity, and Open-Ended Discovery - maintains creative principles
- **Storyteller**: Entity of Narrative and Story - maintains narrative structures
- **Librarian**: Entity of Knowledge Organization - maintains knowledge structures
- **TestRunner**: Entity of Testing and Verification - maintains testing standards
- **MilitaryBrass**: Entity of Mission Planning - maintains mission structures
- **MissionControl**: Entity of Coordination and Monitoring - maintains operational structures
- **TheVillage**: Entity of Community and Connection - maintains community structures

### Change Mechanism

Entities change only when:
1. Beings collect evidence that proves an Aspect of Creation needs modification
2. The body of evidence reaches a threshold that warrants change
3. The change is implemented while maintaining the Entity's fundamental nature

### Implementation

Entities are implemented as Python classes in `src/waft/pantheon/`:
- They manage file-based systems following "as above, so below" principles
- They maintain stable data structures
- They provide interfaces for Beings to interact with them
- They evolve slowly based on evidence collected by Beings

---

## Beings - Timeful

### Nature

**Beings are timeful, dynamic agents that explore, learn, and evolve.**

They are constantly changing, moving, and collecting evidence that may influence Entities.

### Characteristics

- **Timeful**: They move a lot and change things rapidly
- **Dynamic**: Constantly learning, evolving, and adapting
- **Evidence Collectors**: They gather evidence that may prove Entities need to change
- **Explorers**: They spawn into realities, learn through experience, evolve through natural selection

### Examples

- All Being instances spawned into realities
- Beings that learn skills, make decisions, and evolve
- Beings that collect memories and lessons
- Beings that pass knowledge upward through ancestral chains

### Change Mechanism

Beings change constantly:
- Skills evolve through experience
- Memories accumulate
- Lessons are learned
- Fitness changes based on evolutionary success
- States change (spawning → learning → evolving → completing → archived)

### Evidence Collection

Beings collect evidence through:
- Experiences in realities
- Skills learned and tested
- Memories and lessons
- Evolutionary success/failure
- Interactions with Entities

This evidence may eventually prove that Entities need to change.

### Implementation

Beings are implemented in `src/waft/being.py`:
- They have lifecycle attributes (will_to_live, luck, decision_fatigue, etc.)
- They learn skills and accumulate memories
- They evolve through natural selection
- They spawn into realities and interact with Entities

---

## Interaction Between Entities and Beings

### How Beings Influence Entities

1. **Evidence Collection**: Beings explore realities and collect evidence
2. **Evidence Accumulation**: Evidence accumulates over time
3. **Threshold Reached**: When evidence reaches a threshold, it may prove an Entity needs to change
4. **Entity Evolution**: The Entity evolves based on the evidence, while maintaining its fundamental nature

### Example Flow

1. A Being spawns into a reality and learns a new skill
2. The Being tests the skill and collects evidence about its effectiveness
3. Multiple Beings collect similar evidence over time
4. The evidence accumulates in the Entity's domain (e.g., Magistrate's Body of Proof)
5. When sufficient evidence is collected, the Entity may evolve its Aspect of Creation
6. The Entity maintains its fundamental nature while incorporating the new evidence

### Maintaining the Distinction

- **Entities remain timeless**: They don't change unless evidence demands it
- **Beings remain timeful**: They constantly change and explore
- **Evidence flows from Beings to Entities**: Beings collect, Entities evaluate
- **Balance is maintained**: Stability (Entities) and change (Beings) coexist

---

## Implementation Guidance

### For Entity Classes

1. **Document timeless nature**: Class docstrings should mention "Force that Binds Reality Together"
2. **Evidence-based change**: Methods that change Entity state should require evidence
3. **Stable interfaces**: Provide stable interfaces for Beings to interact with
4. **Slow evolution**: Design for slow, evidence-based evolution

### For Being Classes

1. **Document timeful nature**: Class docstrings should mention dynamic, timeful nature
2. **Rapid change**: Design for constant change and evolution
3. **Evidence collection**: Methods should collect evidence that may influence Entities
4. **Exploration focus**: Design for exploration and discovery

### For System Design

1. **Clear separation**: Maintain clear separation between Entities and Beings
2. **Evidence flow**: Design mechanisms for evidence to flow from Beings to Entities
3. **Balance**: Ensure the system maintains balance between stability and change
4. **Documentation**: Document the distinction clearly in all relevant files

---

## Related Documentation

- [Pantheon README](../src/waft/pantheon/README.md)
- [Being System](../src/waft/being.py)
- [System Overview](./SYSTEM_OVERVIEW.md)
- [Pantheon Spiritual Architecture](../_work_efforts/CHECKPOINT_2026-01-14_pantheon_spiritual_architecture.md)

---

**Last Updated**: 2026-01-15
