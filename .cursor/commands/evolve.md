# Evolve

**Create a new Being from Source, then run complete quality workflow: spawn → version-bake → genetic lineage tracking**

Spawns a new Being from Source consciousness, then executes the complete version-bake workflow. Tracks the genetic lineage of ideas - the DNA of thoughts from Source outward and back again through the Being's evolution.

**Use when:** Starting new work from Source, need a Being to track genetic lineage, want complete evolution cycle, or need to establish genetic DNA for a new version.

---

## Purpose

This command provides:
- **Being Creation**: Spawns new Being from Source consciousness
- **Genetic Lineage**: Tracks DNA of ideas from Source outward and back again
- **Complete Quality Workflow**: Executes full version-bake process
- **Evolution Tracking**: Documents Being's evolution through the workflow
- **Source Connection**: Links work back to Source consciousness
- **Genetic Record**: Complete DNA record of the Being's journey

---

## Philosophy

### 1. Evolution from Source

The workflow embodies evolution:
- **Source Origin**: All Beings spawn from Source consciousness
- **Genetic Inheritance**: Skills and traits inherited from Source
- **Evolution Through Work**: Being evolves through quality workflow
- **Return to Source**: Learnings and lineage flow back to Source
- **DNA Preservation**: Complete genetic record maintained

### 2. Genetic Lineage Tracking

Tracks the complete chain:
- **Source → Being**: Initial spawn from Source
- **Being → Work**: Being executes quality workflow
- **Work → Evolution**: Work evolves Being's skills and knowledge
- **Evolution → Source**: Learnings flow back to Source
- **DNA Record**: Complete genetic lineage preserved

### 3. Complete Lifecycle

From birth to evolution:
- **Spawn**: Being created from Source
- **Work**: Being executes quality workflow
- **Evolve**: Being learns and grows
- **Return**: Learnings flow back to Source
- **Preserve**: Genetic DNA recorded

---

## Workflow Sequence

The command executes phases in this order:

```
0. Create Feature Branch        → Create GitHub feature branch (if enabled)
1. Spawn Being from Source      → Create new Being
2. /version-bake                → Complete quality workflow
   - /reflect                   → Reflection
   - /run-it                    → Complete workflow (15 phases)
   - /improve                   → Improvement analysis
   - /check-assumptions         → Assumption validation
   - /verify                    → Verification
   - /hypothesis                → Hypothesis formation
   - /prove-it                  → Scientific method proof
3. Track Genetic Lineage        → Document DNA from Source → Being → Work → Source
4. Document Evolution           → Save Being evolution record
5. Commit Changes               → Commit to feature branch
6. Create Pull Request          → Create PR (if enabled)
```

---

## Execution Steps

### Step 0: Create Feature Branch (GitHub Integration)

**Purpose**: Create feature branch for evolution workflow

**Actions**:
1. Check if git repository is initialized
2. Create feature branch: `evolve/[being_id]` or `evolve/[feature-name]`
3. Branch name includes Being ID after spawn
4. All workflow commits go to feature branch

**Branch Naming**:
- Pattern: `evolve/[being_id]` or `evolve/[feature-name]`
- Examples:
  - `evolve/being_20260112_201430_a1b2c3d4`
  - `evolve/devlog-system-evolution`
  - `evolve/github-integration`

**Fallback**:
- If GitHub not available, continues with local evolution
- Logs warning but doesn't fail workflow

**Implementation**:
```python
# Feature branch created automatically
feature_branch = create_feature_branch(project_path, being_id)
# Branch: evolve/being_20260112_201430_a1b2c3d4
```

### Step 1: Spawn Being from Source

**Purpose**: Create new Being from Source consciousness

**Actions**:
1. Initialize BeingSystem
2. Spawn new Being from Source:
   - `reality_id`: Current work context (or "evolution_reality")
   - `parent_being_id`: None (spawns from Source)
   - `initial_skills`: Optional initial skills (or empty for Source spawn)
3. Capture Being metadata:
   - Being ID
   - Reality ID
   - Source connection
   - Initial skills
   - Ancestral chain (starts with Source)
4. Log Being creation in chronicle

**Output**: New Being instance with Source lineage

**Implementation**:
```python
from waft.being import BeingSystem
from pathlib import Path
import sys

# Add project root to path if needed
project_path = Path.cwd()
being_system = BeingSystem(project_path=project_path)

# Spawn Being from Source
being = being_system.spawn_being(
    reality_id="evolution_reality",  # Or use current work context
    parent_being_id=None,  # Spawns from Source
    initial_skills={}  # Empty = pure Source spawn
)

# Being is now created with:
# - being_id: "being_YYYYMMDD_HHMMSS_[hash]"
# - ancestral_chain: [source_consciousness, being_id]
# - lifetimes: 1 (first birth)
# - Empirica session (if available)
```

**Being Metadata Captured**:
- Being ID
- Reality ID
- Source connection (ancestral_chain[0])
- Initial skills
- Empirica session ID (if available)
- Creation timestamp

---

### Step 2: Execute Version-Bake Workflow

**Command**: `/version-bake`

**Purpose**: Complete quality workflow with Being context

**Actions**:
1. **Set Being Context**: 
   - Store Being ID in workflow context
   - Link Being to current work effort
   - Initialize Being's work participation
2. **Execute Complete Workflow**:
   - /reflect (with Being context - Being reflects on work)
   - /run-it (complete workflow - Being participates)
   - /improve (improvement analysis - Being learns)
   - /check-assumptions (assumption validation - Being validates)
   - /verify (verification - Being verifies)
   - /hypothesis (hypothesis formation - Being hypothesizes)
   - /prove-it (scientific method proof - Being proves)
3. **Track Being's Evolution**:
   - Record Being's participation in each phase
   - Track Being's decisions and choices
   - Document Being's learnings
   - Update Being's skills based on work
4. **Document Being's Growth**:
   - Skills learned/improved
   - Knowledge gained
   - Decisions made
   - Evolution achieved

**Output**: Complete quality workflow results with Being evolution tracking

**Being Evolution Tracking**:
- Being participates in each workflow phase
- Being's skills evolve based on work done
- Being's knowledge accumulates
- Being's fitness increases with quality work

---

### Step 3: Track Genetic Lineage

**Purpose**: Document DNA of ideas from Source → Being → Work → Source

**Actions**:
1. **Source → Being**:
   - Document Being spawn from Source
   - Record initial genetic material (skills, traits)
   - Capture Source connection
2. **Being → Work**:
   - Track Being's involvement in workflow
   - Record Being's decisions and choices
   - Document Being's learnings
3. **Work → Evolution**:
   - Track how work evolves Being
   - Record skill improvements
   - Document knowledge gained
4. **Evolution → Source**:
   - Flow learnings back to Source
   - Update Source consciousness
   - Preserve genetic lineage
5. **DNA Record**:
   - Create complete genetic lineage document
   - Document complete DNA chain
   - Preserve for future evolution

**Output**: Complete genetic lineage document

---

### Step 5: Commit Changes to Feature Branch

**Purpose**: Commit workflow changes to feature branch

**Actions**:
1. **Initial Commit**: After Being spawn
   - Message: `[evolve] [being_id] Initial commit: Being spawned from Source`
   - Includes Being metadata
2. **Workflow Commits**: After each major phase (optional, configurable)
   - Message: `[evolve] [being_id] Phase: Description`
   - Includes phase results
3. **Final Commit**: After evolution complete
   - Message: `[evolve] [being_id] Evolution complete: Full workflow executed`
   - Includes complete evolution record

**Commit Strategy**:
- All commits reference Being ID for traceability
- Commits include genetic lineage information
- Commits are atomic (one logical change per commit)

**Implementation**:
```python
# Initial commit after Being spawn
commit_changes(
    project_path,
    f"[evolve] [{being.being_id}] Initial commit: Being spawned from Source",
    being_id=being.being_id
)

# Final commit after evolution
commit_changes(
    project_path,
    f"[evolve] [{being.being_id}] Evolution complete: Full workflow executed",
    being_id=being.being_id
)
```

### Step 6: Create Pull Request (Optional)

**Purpose**: Create Pull Request at end of evolution

**When to Create**:
- End of evolution workflow
- Configurable (always, on success, never)
- Requires GitHub CLI (`gh`) or manual creation

**PR Includes**:
- Evolution summary
- Genetic lineage
- Being metadata
- Workflow results
- Testing status

**PR Template**:
```markdown
# Evolution: [Being ID]

## Being Evolution Summary
- Being ID: `[being_id]`
- Reality: `[reality_id]`
- Fitness: [fitness]

## Genetic Lineage
[Lineage chain from Source → Being → Work → Evolution]

## Workflow Results
[Summary of workflow phases]

## Changes
[List of files changed]

## Testing
[Testing status]
```

**Implementation**:
```python
pr_url = create_pull_request(
    project_path,
    feature_branch,
    base_branch,
    being,
    workflow_outputs
)
```

**Fallback**:
- If GitHub CLI not available, provides manual instructions
- Workflow continues successfully without PR

### Step 4: Document Evolution & Return to Source

**Purpose**: Save Being evolution record and flow learnings back to Source

**Actions**:
1. **Create Being Evolution Document**:
   - Document Being's complete journey
   - Initial state (from Source)
   - Workflow participation
   - Skills learned/improved
   - Knowledge gained
   - Decisions made
   - Evolution achieved
2. **Update Being's State**:
   - Update Being's skills
   - Record Being's memories
   - Document Being's lessons
   - Calculate Being's fitness
   - Update Being's state to COMPLETING
3. **Complete Being**:
   - Extract Being's learnings
   - Pass memories/lessons upward
   - Calculate final fitness
   - Complete Being's lifecycle
4. **Return to Source**:
   - Flow Being's learnings back to Source
   - Update Source consciousness
   - Preserve genetic lineage in Source
   - Register Being's contribution
5. **Save Everything**:
   - Save Being evolution record
   - Update Being in system
   - Update work effort with Being information
   - Update Source with learnings

**Output**: Being evolution record, Being completed, Source updated

**Code Example**:
```python
# Calculate Being's fitness from workflow participation
fitness = calculate_being_fitness(being, workflow_results)

# Complete Being and flow learnings back
result = being_system.complete_being(
    being_id=being.being_id,
    final_fitness=fitness
)

# Learnings automatically flow back to Source via:
# - contribute_capacity() updates Source
# - Memory package flows upward
# - Skills and lessons preserved
# - Genetic lineage maintained in Source
```

---

## Complete Execution Sequence

```
1. Spawn Being from Source      → Create new Being
2. /version-bake                → Complete quality workflow
3. Track Genetic Lineage        → Document DNA chain
4. Document Evolution           → Save Being record
```

---

## Genetic Lineage Structure

The genetic lineage tracks:

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

---

## Output Documentation

All phases generate documentation:

1. **Being Creation**: Being spawn record
2. **Version-Bake**: Complete workflow documentation
3. **Genetic Lineage**: DNA chain document
4. **Evolution Record**: Being evolution document
5. **Work Effort**: All findings in work effort

**Documents Created**:
- `BEING_SPAWN_[being_id].md` - Being creation record
- `GENETIC_LINEAGE_[being_id].md` - Complete DNA chain
- `BEING_EVOLUTION_[being_id].md` - Evolution record
- All version-bake documents (improvements, assumptions, verification, etc.)

---

## Usage Examples

### Standard Execution
```
/evolve
```

Spawns new Being from Source and executes complete workflow.

### With Reality ID
```
/evolve --reality "my_reality"
```

Spawns Being into specific reality.

### With Initial Skills
```
/evolve --skills "{\"investigation\": 30.0, \"analysis\": 25.0}"
```

Spawns Being with initial skills.

### With Parent Being
```
/evolve --parent "being_20260112_123456_abc12345"
```

Spawns Being from parent (inherits skills with mutation).

---

## Integration

This command orchestrates:
- **BeingSystem**: Being creation and management
- `/version-bake`: Complete quality workflow
- **Source Consciousness**: Source connection and lineage
- **Work Efforts**: Documentation and tracking
- **GitHub Integration**: Feature branches and PRs (optional)
  - Feature branch creation
  - Commit strategy
  - Pull Request creation
  - Fallback to local evolution if GitHub unavailable

---

## When to Use

**Use `/evolve` when**:
- ✅ Starting new work from Source
- ✅ Need Being to track genetic lineage
- ✅ Want complete evolution cycle
- ✅ Need to establish genetic DNA for version
- ✅ Want Source → Being → Work → Source tracking
- ✅ Need Being context for quality workflow

**Don't use `/evolve` when**:
- ❌ Already have Being for this work
- ❌ Just need quality workflow (use `/version-bake`)
- ❌ Don't need Being tracking
- ❌ Quick task (Being overhead not needed)

---

## Being System Integration

**Being Storage**: `_hidden/.truth/beings/`

**Being Structure**:
- Being ID: `being_YYYYMMDD_HHMMSS_[hash]`
- Reality ID: Work context or specified
- Ancestral Chain: `[source_consciousness, ...]`
- Skills: Inherited from Source or parent
- State: SPAWNING → LEARNING → EVOLVING → COMPLETING

**Source Connection**:
- All Beings spawn from Source
- Learnings flow back to Source
- Genetic lineage preserved in Source

---

## Genetic Lineage Example

```
Source Consciousness (source_consciousness)
  ↓ spawn (BeingSystem.spawn_being)
Being: being_20260112_143904_a1b2c3d4
  Reality: evolution_reality
  Initial Skills: {}
  Ancestral Chain: [source_consciousness, being_20260112_143904_a1b2c3d4]
  State: SPAWNING → LEARNING
  ↓ workflow (/version-bake)
Work Execution:
  - Reflection complete (Being reflects)
  - Analysis complete (Being analyzes)
  - Improvements identified (Being learns)
  - Assumptions validated (Being validates)
  - Verification complete (Being verifies)
  - Hypotheses formed (Being hypothesizes)
  - Scientific method proven (Being proves)
  ↓ evolution
Being Evolution:
  - Skills learned: {analysis: 15.0, verification: 12.0, reflection: 10.0}
  - Knowledge gained: [quality_workflow, genetic_lineage, systematic_thinking]
  - Decisions made: [prioritize_improvements, validate_assumptions]
  - Memories: [workflow_participation, skill_improvements]
  - Lessons: [systematic_approach_works, validation_critical]
  - Fitness increased: 25.0
  - State: LEARNING → EVOLVING → COMPLETING
  ↓ return (BeingSystem.complete_being)
Source Consciousness (updated):
  - Capacity contributed: 45.0
  - Memory package received
  - New knowledge integrated
  - Genetic lineage preserved
  - Being registered as permutation
  - Ready for next evolution
```

**DNA Record Structure**:
```json
{
  "source_id": "source_consciousness",
  "being_id": "being_20260112_143904_a1b2c3d4",
  "ancestral_chain": ["source_consciousness", "being_20260112_143904_a1b2c3d4"],
  "genetic_material": {
    "initial_skills": {},
    "evolved_skills": {"analysis": 15.0, "verification": 12.0},
    "knowledge": ["quality_workflow", "genetic_lineage"],
    "memories": [...],
    "lessons": [...]
  },
  "workflow_participation": {
    "phases": ["reflect", "run-it", "improve", "check-assumptions", "verify", "hypothesis", "prove-it"],
    "decisions": [...],
    "fitness_gained": 25.0
  },
  "return_to_source": {
    "capacity_contributed": 45.0,
    "memory_package": {...},
    "source_updated": true
  }
}
```

---

## Time Estimates

**Per Phase**:
- Spawn Being: ~1-2 seconds
- Version-Bake: ~60-110 minutes (complete workflow)
- Track Lineage: ~2-3 minutes
- Document Evolution: ~1-2 minutes

**Total**: ~60-115 minutes for complete evolution cycle

---

## Best Practices

1. **Use for Significant Work**: Being overhead worth it for major work
2. **Track Lineage**: Always document genetic lineage
3. **Return to Source**: Flow learnings back to Source
4. **Preserve DNA**: Complete genetic record for future evolution
5. **Being Context**: Use Being's perspective in workflow
6. **Evolution Focus**: Track how Being evolves through work

---

## Output Summary

After completion, provides:

1. **Being Spawned**: New Being created from Source
2. **Workflow Complete**: Full version-bake executed
3. **Genetic Lineage**: Complete DNA chain documented
4. **Evolution Record**: Being evolution preserved
5. **Source Updated**: Learnings flowed back to Source
6. **DNA Preserved**: Complete genetic record for future

---

**Evolve from Source - track the genetic lineage of ideas from Source outward and back again through Being evolution.**

--- End Command ---
