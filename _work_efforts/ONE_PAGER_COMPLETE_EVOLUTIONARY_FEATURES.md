# One-Pager: Complete Evolutionary Features Inventory

**Created**: 2026-01-11
**Status**: Complete Feature Mapping
**Purpose**: Map ALL existing evolutionary features and ensure we're using them ALL

---

## All Evolutionary Features in WAFT

### Event Types (EvolutionaryEventType)
1. ✅ **SPAWN** - Agent reproduction (creates variant)
2. ❌ **MUTATE** - Code/config mutation (hot-swap/evolve) - **NOT YET USED**
3. ❌ **GYM_EVAL** - Fitness evaluation in Gym - **NOT YET USED**
4. ❌ **DEATH** - Agent termination (fitness below threshold) - **NOT YET USED**
5. ❌ **SURVIVAL** - Agent survives generation - **NOT YET USED**
6. ❌ **SESSION_END** - Session completion marker - **NOT YET USED**

### Reproduction Mechanisms
1. ✅ **Spawn** - Parent creates child with mutation - **PLANNED**
2. ❌ **Conjugate** - Two parents create hybrid offspring - **NOT YET USED**
   - Requires proximity (adjacent in PetriDish)
   - Requires metabolic surplus (>70% energy)
   - Creates hybrid genome from both parents
   - Uses LineagePoet.generate_hybrid_name()

### Evolution Mechanisms
1. ❌ **Evolve (Hot-Swap)** - Agent replaces itself with better variant - **NOT YET USED**
   - Spawn multiple variants
   - Evaluate each variant
   - Select best (highest fitness)
   - Hot-swap: agent becomes new genome
   - Old genome preserved in flight recorder

### Fitness Evaluation
1. ❌ **GYM_EVAL** - Fitness evaluation in Scint Gym - **NOT YET USED**
   - Tests agents on Reality Fractures (Scints)
   - Calculates: Stability (40%), Efficiency (30%), Safety (30%)
   - Fitness < 0.5 → DEATH
   - Fitness >= 0.5 → SURVIVAL

### Selection Mechanisms
1. ❌ **Fitness-proportional** - Probability proportional to fitness - **NOT YET USED**
2. ❌ **Tournament** - Random selection from top N agents - **NOT YET USED**
3. ❌ **Elitism** - Always preserve top K agents - **NOT YET USED**
4. ❌ **Diversity** - Penalize similar genomes to maintain diversity - **NOT YET USED**

### Mutation Types
1. ❌ **Point Mutation** - Single code/config change - **NOT YET USED**
2. ❌ **Crossover** - Combine code from two parents - **NOT YET USED**
3. ❌ **Deletion** - Remove code segments - **NOT YET USED**
4. ❌ **Insertion** - Add new code segments - **NOT YET USED**
5. ❌ **Inversion** - Reverse code order - **NOT YET USED**

### Mutation Rate Control
1. ❌ **Population-based** - Larger population = lower mutation rate - **NOT YET USED**
2. ❌ **Generation-based** - Decrease mutation rate over time - **NOT YET USED**
3. ❌ **Fitness landscape** - Increase if stuck in local optimum - **NOT YET USED**
4. ❌ **Diversity-based** - Increase if low diversity - **NOT YET USED**

### Analysis Metrics
1. ❌ **Branching Factor** - Average children per parent - **NOT YET USED**
2. ❌ **Convergence Time** - Generations to fitness plateau - **NOT YET USED**
3. ❌ **Mutation Impact** - Fitness change per mutation - **NOT YET USED**
4. ❌ **Dead End Rate** - Percentage of DEATH events - **NOT YET USED**
5. ❌ **Diversity Index** - Genome uniqueness in population - **NOT YET USED**

---

## What We're Currently Using (Subset)

### ✅ Currently Planned:
- **SPAWN** events for template variants
- **Genome IDs** (hash of style composition)
- **Lineage tracking** (parent_id, generation)
- **Fitness metrics** (aesthetic, efficiency, user rating)
- **Scientific names** (LineagePoet)
- **Pattern analysis** (Study Gym, SessionAnalytics)
- **Event logging** (TheObserver)

### ❌ NOT Yet Using:
- **MUTATE** events (hot-swap/evolve)
- **GYM_EVAL** events (fitness evaluation)
- **DEATH** events (fitness < threshold)
- **SURVIVAL** events (fitness >= threshold)
- **Conjugate** (hybrid templates from two parents)
- **Selection mechanisms** (fitness-proportional, tournament, elitism, diversity)
- **Mutation types** (point, crossover, deletion, insertion, inversion)
- **Mutation rate control** (population, generation, fitness landscape, diversity)
- **Analysis metrics** (branching factor, convergence time, mutation impact, dead end rate, diversity index)

---

## Complete Integration Plan

### Phase 1: Basic Events (Current Plan)
- ✅ SPAWN events for template variants
- ✅ Genome IDs and lineage tracking
- ✅ Fitness metrics
- ✅ Scientific names

### Phase 2: Full Event Types
- ⏳ **MUTATE** events when templates hot-swap
- ⏳ **GYM_EVAL** events for template fitness evaluation
- ⏳ **DEATH** events for templates with fitness < 0.5
- ⏳ **SURVIVAL** events for templates with fitness >= 0.5

### Phase 3: Reproduction Mechanisms
- ⏳ **Conjugate** - Two templates create hybrid
  - Example: "story-section" template + "boxed-section" template → hybrid template
  - Uses LineagePoet.generate_hybrid_name()
  - Recombines style compositions

### Phase 4: Evolution Mechanisms
- ⏳ **Evolve (Hot-Swap)** - Template replaces itself with better variant
  - Spawn multiple template variants
  - Evaluate each (fitness test)
  - Select best (highest fitness)
  - Hot-swap: template becomes new genome

### Phase 5: Selection Mechanisms
- ⏳ **Fitness-proportional** - Templates selected based on fitness probability
- ⏳ **Tournament** - Random selection from top N templates
- ⏳ **Elitism** - Always preserve top K templates
- ⏳ **Diversity** - Penalize similar style compositions

### Phase 6: Mutation Types
- ⏳ **Point Mutation** - Single style change (e.g., change one list style)
- ⏳ **Crossover** - Combine styles from two parent templates
- ⏳ **Deletion** - Remove style from composition
- ⏳ **Insertion** - Add new style to composition
- ⏳ **Inversion** - Reverse style order

### Phase 7: Mutation Rate Control
- ⏳ **Population-based** - More templates = lower mutation rate
- ⏳ **Generation-based** - Decrease mutation rate over time
- ⏳ **Fitness landscape** - Increase if stuck (no improvement)
- ⏳ **Diversity-based** - Increase if low diversity

### Phase 8: Analysis Metrics
- ⏳ **Branching Factor** - Average template variants per parent
- ⏳ **Convergence Time** - Generations to optimal template
- ⏳ **Mutation Impact** - Fitness change per style mutation
- ⏳ **Dead End Rate** - Percentage of templates with fitness < 0.5
- ⏳ **Diversity Index** - Style composition uniqueness

---

## Template as Full Digital Organism

### Complete Lifecycle:
```
Template Genesis (v1.0)
    │
    ├── SPAWN → Template v1.1 (point mutation: added checkmarks)
    │   │
    │   ├── GYM_EVAL → Fitness: 0.75 → SURVIVAL
    │   │
    │   └── SPAWN → Template v1.2 (crossover: combined with another)
    │       │
    │       └── GYM_EVAL → Fitness: 0.45 → DEATH
    │
    ├── CONJUGATE → Hybrid Template (with another template)
    │   │
    │   └── GYM_EVAL → Fitness: 0.82 → SURVIVAL
    │
    └── EVOLVE → Template v2.0 (hot-swap: replaced with better variant)
        │
        └── GYM_EVAL → Fitness: 0.88 → SURVIVAL
```

### Selection Process:
1. **Population**: 50 templates with different style compositions
2. **Evaluation**: Each tested (GYM_EVAL) → fitness scores
3. **Selection**: Fitness-proportional selection (higher fitness = more likely)
4. **Reproduction**: Selected templates spawn variants
5. **Mutation**: Variants mutated (point, crossover, etc.)
6. **Evolution**: Best variants hot-swap (MUTATE event)
7. **Death**: Templates with fitness < 0.5 marked DEATH

---

## Implementation Priority

### High Priority (Core Evolution)
1. **SPAWN** - Already planned ✅
2. **MUTATE** (hot-swap) - Essential for evolution
3. **GYM_EVAL** - Essential for fitness-based selection
4. **DEATH/SURVIVAL** - Essential for selection pressure

### Medium Priority (Advanced Features)
5. **Conjugate** - Hybrid templates (interesting but not essential)
6. **Selection mechanisms** - Improve evolution efficiency
7. **Mutation types** - More sophisticated mutations

### Low Priority (Optimization)
8. **Mutation rate control** - Fine-tuning
9. **Analysis metrics** - Research value

---

## The Answer: We're Using a Subset

**Currently planned**: ~30% of available features
- ✅ SPAWN, genome IDs, lineage, fitness metrics, scientific names
- ❌ MUTATE, GYM_EVAL, DEATH, SURVIVAL, Conjugate, selection mechanisms, mutation types, mutation rate control, analysis metrics

**Should we use ALL of them?** YES! Templates should be full digital organisms with complete evolutionary capabilities.

---

**Status**: Complete inventory created, ready for full integration
