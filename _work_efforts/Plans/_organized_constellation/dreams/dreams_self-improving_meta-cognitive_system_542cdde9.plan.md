---
name: Self-Improving Meta-Cognitive System
overview: Create a self-improving AI system that studies itself through /study, runs /engineering cycles, explores to form hypotheses, sets goals, tracks progress across generations, detects stagnation, and prunes unproductive thought chains.
todos:
  - id: create_meta_cognition_structure
    content: Create src/waft/meta_cognition/ directory structure and base classes
    status: pending
  - id: implement_generation_tracker
    content: Implement GenerationTracker class with progress metrics and stagnation detection
    status: pending
  - id: implement_thought_chain_tracker
    content: Implement ThoughtChainTracker class with pattern detection and cycle counting
    status: pending
  - id: implement_self_study
    content: Integrate /study command for self-observation and recording
    status: pending
  - id: implement_goal_discovery
    content: Implement GoalDiscovery system using /explore, /hypothesis, /check-assumptions, /verify
    status: pending
  - id: implement_progress_measurement
    content: Implement composite progress metrics calculation and delta tracking
    status: pending
  - id: implement_stagnation_detector
    content: Implement StagnationDetector with 12-generation threshold
    status: pending
  - id: implement_chain_pruner
    content: Implement ChainPruner with /critique integration and pruning logic
    status: pending
  - id: implement_orchestrator
    content: Create MetaCognitionOrchestrator with generation loop and termination conditions
    status: pending
  - id: create_cli_commands
    content: Add CLI commands for meta-cognition system (/meta-cognition start, status, report, prune)
    status: pending
  - id: create_data_storage
    content: Create _genetics/meta_cognition/ directory structure for persistence
    status: pending
  - id: integrate_with_existing_systems
    content: Integrate with Study Gym, Engineering Workflow, Evolution System, Empirica
    status: pending

category: dreams
confidence: 0.73
constellation_date: 2026-01-14
---

# Self-Improving Meta-Cognitive System

## Overview

A meta-cognitive evolutionary system that studies itself, forms hypotheses about improvement, tests them through engineering cycles, tracks progress across generations, and prunes unproductive thought chains.

## Core Components

### 1. Self-Study System (`src/waft/meta_cognition/self_study.py`)

**Purpose**: Study the system's own behavior and capabilities

**Key Features**:

- Uses `/study` command to observe own behavior
- Records observations about engineering cycles
- Tracks tool usage patterns
- Measures cycle efficiency
- Documents self-discoveries

**Data Structure**:

```python
@dataclass
class SelfStudySession:
    session_id: str
    generation: int
    study_type: str  # "engineering_cycle", "tool_usage", "hypothesis_formation"
    observations: List[Observation]
    findings: List[str]
    timestamp: datetime
```

### 2. Generation Tracker (`src/waft/meta_cognition/generation_tracker.py`)

**Purpose**: Track progress across generations and detect stagnation

**Key Features**:

- Tracks generation number
- Measures progress metrics (composite)
- Detects stagnation (12 generations with no progress)
- Stores generation history
- Links to thought chains

**Progress Metrics** (Composite):

- Goal achievement progress (0.0-1.0)
- Epistemic state improvement (knowledge gained)
- Engineering cycle efficiency (time/quality)
- Hypothesis verification rate
- Tool usage optimization

**Data Structure**:

```python
@dataclass
class Generation:
    generation_id: int
    start_time: datetime
    end_time: Optional[datetime]
    goal: Optional[str]
    progress_metrics: Dict[str, float]
    thought_chain_id: Optional[str]
    engineering_cycles: List[str]  # Cycle IDs
    status: str  # "active", "completed", "stagnant"
```

### 3. Thought Chain Tracker (`src/waft/meta_cognition/thought_chain.py`)

**Purpose**: Track persistent thought patterns across cycles

**Key Features**:

- Identifies thought chains (recurring patterns)
- Tracks chain persistence (cycles count)
- Links chains to generations
- Flags chains for critique/pruning (12 cycles)

**Data Structure**:

```python
@dataclass
class ThoughtChain:
    chain_id: str
    pattern_description: str
    first_seen: datetime
    last_seen: datetime
    cycle_count: int
    generation_span: List[int]
    hypothesis_ids: List[str]
    status: str  # "active", "flagged", "pruned"
```

### 4. Goal Discovery System (`src/waft/meta_cognition/goal_discovery.py`)

**Purpose**: Discover goals through exploration

**Key Features**:

- Analyzes exploration findings
- Identifies improvement opportunities
- Formulates goals from discoveries
- Prioritizes goals by impact
- Updates goals based on progress

**Process**:

1. Run `/explore` to understand system
2. Form `/hypothesis` about improvements
3. `/check-assumptions` about goals
4. `/verify` goal feasibility
5. Set `/goal` with steps

### 5. Stagnation Detector (`src/waft/meta_cognition/stagnation_detector.py`)

**Purpose**: Detect when system is not making progress

**Key Features**:

- Monitors progress metrics across generations
- Calculates progress delta (change)
- Flags stagnation (12 generations no progress)
- Triggers critique/pruning workflow

**Stagnation Criteria**:

- 12 consecutive generations with:
  - Progress delta < threshold (e.g., 0.01)
  - No goal achievement
  - No epistemic gain
  - No efficiency improvement

### 6. Thought Chain Pruner (`src/waft/meta_cognition/chain_pruner.py`)

**Purpose**: Critique and prune unproductive thought chains

**Key Features**:

- Runs `/critique` on thought chain
- Analyzes chain productivity
- Identifies pruning candidates
- Executes pruning (removes chain from active consideration)
- Documents pruning rationale

**Pruning Criteria**:

- Thought chain persists 12 `/another-cycle` repetitions
- Chain shows no progress
- Chain has negative impact on goal achievement
- Critique identifies fundamental flaws

## Main Workflow

### Generation Loop

```
1. GENERATION START
   ├─> /study /yourself
   │   └─> Observe own behavior
   │       └─> Record observations
   │
   ├─> /explore environment
   │   └─> Understand current state
   │       └─> Document findings
   │
   ├─> /hypothesis formation
   │   └─> Form hypotheses about improvements
   │       └─> Based on exploration findings
   │
   ├─> /check-assumptions
   │   └─> Validate hypothesis assumptions
   │       └─> Gather evidence
   │
   ├─> /verify ideas
   │   └─> Verify hypothesis claims
   │       └─> Test predictions
   │
   ├─> /goal selection
   │   └─> Choose goal (discovered or existing)
   │       └─> Break into steps
   │
   ├─> ENGINEERING CYCLE LOOP
   │   ├─> /engineering cycle
   │   │   ├─> spin-up → explore → draft plan
   │   │   ├─> critique plan → finalize plan → begin
   │   │   └─> Track cycle metrics
   │   │
   │   ├─> Update thought chain tracker
   │   │   └─> Identify patterns
   │   │
   │   └─> Check for thought chain persistence
   │       └─> If 12 cycles: flag for critique
   │
   ├─> PROGRESS MEASUREMENT
   │   ├─> Calculate composite metrics
   │   ├─> Compare to previous generation
   │   └─> Update generation tracker
   │
   ├─> STAGNATION CHECK
   │   ├─> Check progress delta
   │   └─> If 12 generations no progress:
   │       └─> Flag for termination
   │
   └─> GENERATION END
       ├─> Save generation data
       ├─> Update thought chains
       └─> Prepare next generation
```

### Thought Chain Critique/Prune Workflow

```
1. THOUGHT CHAIN FLAGGED (12 cycles)
   ├─> /critique thought chain
   │   ├─> Security analysis
   │   ├─> Assumption detection
   │   ├─> Overengineering detection
   │   └─> Oversight detection
   │
   ├─> Analyze chain productivity
   │   ├─> Progress contribution
   │   ├─> Goal alignment
   │   └─> Resource efficiency
   │
   ├─> Decision: Prune or Keep
   │   ├─> If prune:
   │   │   ├─> Remove from active consideration
   │   │   ├─> Document rationale
   │   │   └─> Archive chain data
   │   └─> If keep:
   │       └─> Reset cycle count (give another chance)
   │
   └─> Update thought chain tracker
```

## File Structure

```
src/waft/meta_cognition/
├── __init__.py
├── self_study.py          # Self-study system
├── generation_tracker.py  # Generation tracking
├── thought_chain.py       # Thought chain tracking
├── goal_discovery.py      # Goal discovery system
├── stagnation_detector.py # Stagnation detection
├── chain_pruner.py        # Thought chain pruning
└── orchestrator.py        # Main orchestrator

_genetics/meta_cognition/
├── generations/
│   ├── gen_001.json
│   ├── gen_002.json
│   └── ...
├── thought_chains/
│   ├── chain_001.json
│   ├── chain_002.json
│   └── ...
└── index.json

_work_efforts/meta_cognition/
├── self_study_sessions/
│   └── study_YYYYMMDD_HHMMSS.json
├── generation_reports/
│   └── gen_XXX_report.md
└── pruning_logs/
    └── prune_YYYYMMDD_HHMMSS.md
```

## Key Data Structures

### Generation Record

```json
{
  "generation_id": 1,
  "start_time": "2026-01-12T20:10:23Z",
  "end_time": "2026-01-12T21:30:45Z",
  "goal": "Improve engineering cycle efficiency",
  "goal_achieved": false,
  "progress_metrics": {
    "goal_progress": 0.45,
    "epistemic_gain": 0.32,
    "cycle_efficiency": 0.67,
    "hypothesis_verification_rate": 0.80,
    "tool_optimization": 0.55
  },
  "composite_score": 0.558,
  "thought_chains": ["chain_001"],
  "engineering_cycles": ["cycle_001", "cycle_002"],
  "status": "completed",
  "stagnation_detected": false
}
```

### Thought Chain Record

```json
{
  "chain_id": "chain_001",
  "pattern_description": "Always uses /engineering before /explore",
  "first_seen": "2026-01-12T20:10:23Z",
  "last_seen": "2026-01-12T22:15:30Z",
  "cycle_count": 12,
  "generation_span": [1, 2, 3],
  "hypothesis_ids": ["hyp_001", "hyp_002"],
  "progress_contribution": -0.15,
  "status": "flagged",
  "critique_result": null
}
```

## Implementation Steps

### Phase 1: Core Infrastructure

1. Create `src/waft/meta_cognition/` directory structure
2. Implement `GenerationTracker` class
3. Implement `ThoughtChainTracker` class
4. Create data storage in `_genetics/meta_cognition/`
5. Add CLI command `/meta-cognition` or `/self-improve`

### Phase 2: Self-Study Integration

1. Integrate `/study` command for self-observation
2. Create `SelfStudySession` data structures
3. Implement observation recording
4. Link to generation tracker

### Phase 3: Goal Discovery

1. Implement `GoalDiscovery` system
2. Integrate `/explore`, `/hypothesis`, `/check-assumptions`, `/verify`
3. Create goal formulation logic
4. Link goals to generations

### Phase 4: Progress Measurement

1. Implement composite metrics calculation
2. Create progress delta tracking
3. Implement stagnation detection
4. Add progress visualization

### Phase 5: Thought Chain Management

1. Implement pattern detection
2. Create chain tracking across cycles
3. Implement flagging logic (12 cycles)
4. Integrate `/critique` for chain analysis

### Phase 6: Pruning System

1. Implement pruning decision logic
2. Create pruning execution
3. Add pruning documentation
4. Archive pruned chains

### Phase 7: Main Orchestrator

1. Create `MetaCognitionOrchestrator` class
2. Implement generation loop
3. Integrate all components
4. Add termination conditions (goal achieved OR 12 stagnant generations)

### Phase 8: CLI Integration

1. Add `/meta-cognition start` command
2. Add `/meta-cognition status` command
3. Add `/meta-cognition report` command
4. Add `/meta-cognition prune` command (manual)

## Integration Points

### With Existing Systems

- **Study Gym**: Use for self-study sessions
- **Engineering Workflow**: Track cycle metrics
- **Evolution System**: Link to genome tracking
- **Empirica**: Track epistemic state
- **Work Efforts**: Link to work tracking
- **Genetics System**: Store generation data

### Command Integration

- `/study /yourself` - Self-study
- `/engineering` - Engineering cycles
- `/explore` - Environment exploration
- `/hypothesis` - Hypothesis formation
- `/check-assumptions` - Assumption validation
- `/verify` - Idea verification
- `/goal` - Goal management
- `/another-cycle` - Full cycle execution
- `/critique` - Thought chain critique

## Success Criteria

1. System can study itself and record observations
2. System discovers goals through exploration
3. System tracks progress across generations
4. System detects stagnation (12 generations)
5. System critiques and prunes unproductive thought chains
6. System terminates when goal achieved OR 12 stagnant generations
7. All data is persisted and traceable

## Notes

- System should be self-contained but integrate with existing WAFT systems
- Progress metrics are composite (multiple factors)
- Thought chains are identified by pattern matching across cycles
- Pruning is destructive (removes from active consideration) but archived
- Generation data is preserved for analysis
- System can be manually interrupted and resumed