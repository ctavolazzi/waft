# Hypothesis: FlightRecorder + Empirica Integration

**Date**: 2026-01-12  
**Status**: Hypothesis  
**Purpose**: Design integration between FlightRecorder (TheObserver) and Empirica

---

## Context

### Current State

**FlightRecorder (TheObserver)**:
- ✅ Passive scientific registry
- ✅ Records evolutionary events to `_pyrite/science/laboratory.jsonl`
- ✅ Immutable JSONL log for phylogenetic tree reconstruction
- ❌ **NO Empirica** - Must remain passive for scientific integrity

**Empirica**:
- ✅ Epistemic state tracking
- ✅ Findings and unknowns logging
- ✅ CHECK gates for decision support
- ✅ Learning measurement

**Gap**: FlightRecorder events contain rich information but aren't analyzed epistemically.

---

## Hypothesis

### Core Principle

**FlightRecorder (TheObserver) remains passive. Analysis happens via adapter/wrapper.**

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FlightRecorder                       │
│                  (Conceptual Layer)                     │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ TheObserver │    │ FlightRecorder│    │ FlightRecorder│
│ (Recording) │    │ Analyzer     │    │ Epistemic    │
│             │    │              │    │ Adapter      │
│ ❌ NO       │    │ ✅ YES       │    │ ✅ YES       │
│ Empirica    │    │ Empirica     │    │ Empirica     │
│             │    │              │    │              │
│ Passive     │    │ Analysis     │    │ Integration  │
│ Recording   │    │ Layer        │    │ Layer        │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        │                   └─────────┬──────────┘
        │                             │
        ▼                             ▼
┌──────────────┐            ┌──────────────┐
│ laboratory   │            │  Empirica     │
│ .jsonl       │            │  Manager      │
│ (immutable)  │            └──────────────┘
└──────────────┘
```

---

## Design: FlightRecorderEpistemicAdapter

### Purpose

Analyze FlightRecorder events and extract epistemic insights without modifying TheObserver.

### Responsibilities

1. **Read Events**: Read from `laboratory.jsonl` (TheObserver's log)
2. **Analyze Patterns**: Extract epistemic patterns from events
3. **Log Insights**: Log findings and unknowns to Empirica
4. **Track Trajectories**: Monitor evolutionary trajectories epistemically
5. **Provide Guidance**: Use Empirica to guide analysis

### Implementation

```python
class FlightRecorderEpistemicAdapter:
    """
    Adapter that analyzes FlightRecorder events and logs insights to Empirica.
    
    Does NOT modify TheObserver - reads events and analyzes them.
    """
    
    def __init__(self, project_path: Path, observer: TheObserver, empirica_manager: EmpiricaManager):
        self.project_path = Path(project_path)
        self.observer = observer
        self.empirica = empirica_manager
    
    def analyze_recent_events(self, limit: int = 100) -> Dict[str, Any]:
        """
        Analyze recent FlightRecorder events for epistemic insights.
        
        Returns:
            Dictionary with insights, patterns, and unknowns
        """
        events = self.observer.get_laboratory_log(limit=limit)
        
        insights = []
        patterns = []
        unknowns = []
        
        # Analyze event patterns
        event_types = [e.get("event_type") for e in events]
        event_counts = Counter(event_types)
        
        # Pattern: High mutation rate
        if event_counts.get("MUTATE", 0) > 10:
            insights.append("High mutation rate detected - system actively evolving")
            self.empirica.log_finding(
                "High mutation rate in FlightRecorder: System actively evolving",
                impact=0.6
            )
        
        # Pattern: Death events
        death_count = event_counts.get("DEATH", 0)
        if death_count > 0:
            insights.append(f"{death_count} agent deaths detected - evolutionary pressure")
            self.empirica.log_finding(
                f"Agent deaths in FlightRecorder: {death_count} evolutionary dead ends",
                impact=0.7
            )
        
        # Pattern: Fitness trends
        fitness_scores = [
            e.get("fitness_metrics", {}).get("fitness", 0)
            for e in events
            if e.get("fitness_metrics")
        ]
        if len(fitness_scores) > 5:
            avg_fitness = sum(fitness_scores) / len(fitness_scores)
            if avg_fitness < 0.5:
                unknowns.append("Why is average fitness below 0.5? Need investigation")
                self.empirica.log_unknown(
                    "Average fitness below 0.5 - why are agents failing?"
                )
        
        # Pattern: Generation progression
        generations = [e.get("generation", 0) for e in events if e.get("generation")]
        if generations:
            max_gen = max(generations)
            if max_gen > 10:
                insights.append(f"System reached generation {max_gen} - significant evolution")
                self.empirica.log_finding(
                    f"Evolutionary depth: {max_gen} generations",
                    impact=0.5
                )
        
        return {
            "insights": insights,
            "patterns": patterns,
            "unknowns": unknowns,
            "event_count": len(events),
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def track_evolutionary_trajectory(self) -> Dict[str, Any]:
        """
        Track evolutionary trajectory using epistemic state.
        
        Returns:
            Trajectory analysis with epistemic context
        """
        # Get epistemic state
        epistemic_context = self.empirica.project_bootstrap()
        epistemic_state = epistemic_context.get("epistemic_state", {})
        vectors = epistemic_state.get("vectors", {})
        
        # Get recent events
        events = self.observer.get_laboratory_log(limit=50)
        
        # Analyze trajectory
        trajectory = {
            "epistemic_phase": self._calculate_phase_from_events(events, vectors),
            "evolutionary_depth": max([e.get("generation", 0) for e in events] or [0]),
            "fitness_trend": self._calculate_fitness_trend(events),
            "mutation_rate": self._calculate_mutation_rate(events),
            "survival_rate": self._calculate_survival_rate(events)
        }
        
        # Log trajectory insights
        if trajectory["fitness_trend"] == "improving":
            self.empirica.log_finding(
                "Evolutionary trajectory: Fitness improving over time",
                impact=0.7
            )
        elif trajectory["fitness_trend"] == "declining":
            self.empirica.log_unknown(
                "Evolutionary trajectory: Fitness declining - why?"
            )
        
        return trajectory
    
    def _calculate_phase_from_events(self, events: List[Dict], vectors: Dict) -> str:
        """Calculate epistemic phase from events and vectors."""
        # Use Empirica phase calculation
        know = vectors.get("foundation", {}).get("know", 0.0)
        uncertainty = vectors.get("uncertainty", 1.0)
        
        # Adjust based on event patterns
        if len(events) < 10:
            return "Data Gathering"  # Not enough events
        elif uncertainty > 0.7:
            return "Exploration"  # High uncertainty
        elif know > 0.6 and uncertainty < 0.3:
            return "Synthesis"  # High knowledge, low uncertainty
        else:
            return "Transition"
    
    def _calculate_fitness_trend(self, events: List[Dict]) -> str:
        """Calculate fitness trend from events."""
        fitness_scores = [
            e.get("fitness_metrics", {}).get("fitness", 0)
            for e in events
            if e.get("fitness_metrics")
        ]
        
        if len(fitness_scores) < 5:
            return "unknown"
        
        # Compare first half to second half
        mid = len(fitness_scores) // 2
        first_half_avg = sum(fitness_scores[:mid]) / mid
        second_half_avg = sum(fitness_scores[mid:]) / (len(fitness_scores) - mid)
        
        if second_half_avg > first_half_avg + 0.1:
            return "improving"
        elif second_half_avg < first_half_avg - 0.1:
            return "declining"
        else:
            return "stable"
    
    def _calculate_mutation_rate(self, events: List[Dict]) -> float:
        """Calculate mutations per event."""
        mutations = sum(1 for e in events if e.get("event_type") == "MUTATE")
        return mutations / len(events) if events else 0.0
    
    def _calculate_survival_rate(self, events: List[Dict]) -> float:
        """Calculate survival rate (survivals / (survivals + deaths))."""
        survivals = sum(1 for e in events if e.get("event_type") == "SURVIVAL")
        deaths = sum(1 for e in events if e.get("event_type") == "DEATH")
        total = survivals + deaths
        return survivals / total if total > 0 else 0.0
```

---

## Key Design Decisions

### 1. Adapter Pattern (Not Modification)

**Decision**: Create adapter that reads from TheObserver, doesn't modify it.

**Rationale**:
- TheObserver must remain passive for scientific integrity
- Analysis can be separate from recording
- Enables multiple analysis layers without coupling

### 2. Read-Only Access

**Decision**: Adapter only reads `laboratory.jsonl`, never writes.

**Rationale**:
- Preserves immutability of FlightRecorder log
- Analysis doesn't corrupt scientific data
- Multiple analyzers can run in parallel

### 3. Epistemic Pattern Extraction

**Decision**: Extract patterns that map to epistemic vectors.

**Rationale**:
- Events contain information about system knowledge
- Patterns indicate learning (or lack thereof)
- Can inform epistemic state

### 4. Real-Time vs Batch Analysis

**Decision**: Support both - real-time for active monitoring, batch for deep analysis.

**Rationale**:
- Real-time: Immediate insights during execution
- Batch: Comprehensive analysis of historical data
- Flexibility for different use cases

---

## Epistemic Insights from Events

### Event → Epistemic Mapping

| Event Pattern | Epistemic Insight | Empirica Action |
|---------------|-------------------|----------------|
| High mutation rate | System actively exploring | Log finding: "Active exploration" |
| Many deaths | High evolutionary pressure | Log finding: "Strong selection pressure" |
| Low fitness | System struggling | Log unknown: "Why is fitness low?" |
| Improving fitness | System learning | Log finding: "Evolutionary improvement" |
| Stagnant generations | System stuck | Log unknown: "Why no progress?" |
| High survival rate | System stable | Log finding: "Stable evolution" |

---

## Integration Points

### 1. Real-Time Analysis

```python
# During agent execution
adapter = FlightRecorderEpistemicAdapter(project_path, observer, empirica)

# Analyze recent events periodically
insights = adapter.analyze_recent_events(limit=20)
```

### 2. Trajectory Tracking

```python
# Track evolutionary trajectory
trajectory = adapter.track_evolutionary_trajectory()

# Use trajectory to inform decisions
if trajectory["fitness_trend"] == "declining":
    # System needs intervention
    pass
```

### 3. Epistemic Phase from Events

```python
# Calculate phase from events + epistemic state
phase = adapter._calculate_phase_from_events(events, vectors)

# Use phase to guide analysis
if phase == "Data Gathering":
    # Need more events
    pass
```

---

## Benefits

1. **Scientific Integrity**: TheObserver remains passive and unmodified
2. **Epistemic Insights**: Events analyzed for knowledge patterns
3. **Separation of Concerns**: Recording separate from analysis
4. **Flexibility**: Multiple analyzers can coexist
5. **Integration**: Empirica gets insights from FlightRecorder

---

## Testing Strategy

1. **Unit Tests**: Test pattern extraction logic
2. **Integration Tests**: Test adapter with real events
3. **Epistemic Tests**: Verify insights map to epistemic vectors
4. **Performance Tests**: Ensure analysis doesn't slow recording

---

## Implementation Plan

1. **Create Adapter Class**: `FlightRecorderEpistemicAdapter`
2. **Implement Pattern Extraction**: Event → Epistemic mapping
3. **Integrate with Empirica**: Log findings and unknowns
4. **Add Trajectory Tracking**: Monitor evolutionary paths
5. **Create Analysis Methods**: Real-time and batch analysis
6. **Test Integration**: Verify with real FlightRecorder events

---

## Hypothesis Validation

**To Validate**:
1. ✅ Adapter can read from TheObserver without modification
2. ✅ Patterns can be extracted from events
3. ✅ Insights map to epistemic vectors
4. ✅ Empirica receives meaningful findings
5. ✅ Trajectory tracking provides actionable insights

**Success Criteria**:
- TheObserver remains passive (no Empirica)
- Adapter successfully analyzes events
- Empirica receives relevant insights
- Trajectory tracking works correctly
- No performance degradation

---

**This hypothesis enables FlightRecorder (concept) to use Empirica while keeping TheObserver (implementation) clean and passive.**
