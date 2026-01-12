# One-Pager Full Ecosystem Integration

**Created**: 2026-01-11
**Status**: Deep Integration Design
**Purpose**: Map ALL existing WAFT systems that can be leveraged for one-pager iterative learning

---

## The Rich Ecosystem We Have

### 1. **Study Gym** (`src/waft/study_gym.py`)
**What it does:**
- Observation tracking with metrics
- Hypothesis formation and testing
- Pattern analysis (`_analyze_results()`, `_form_conclusions()`)
- Session management with JSON storage
- Challenge templates via `ChallengeGenerator`

**For one-pagers:**
- Each generation = Study Gym session
- Track style composition as observations
- Form hypotheses about successful combinations
- Test hypotheses by generating variations
- Analyze patterns across sessions
- Use `ChallengeGenerator` to create style exploration challenges

### 2. **SessionAnalytics** (`src/waft/core/session_analytics.py`)
**What it does:**
- Session tracking with SQLite database
- Pattern analysis: `analyze_productivity_trends()`, `analyze_prompt_drift()`, `compare_approaches()`
- Iteration chain tracking
- Success indicators and metadata

**For one-pagers:**
- Track each generation as a session
- Store style composition in `metadata`
- Use `approach_category` for content type
- Use `success_indicators` for user ratings
- Analyze trends: `analyze_productivity_trends()` for style usage over time
- Track evolution: `analyze_prompt_drift()` for template changes
- Compare variants: `compare_approaches()` for style combinations

### 3. **TheObserver** (`src/waft/core/science/observer.py`)
**What it does:**
- Scientific JSONL logging (immutable log)
- Event tracking with complete context
- Research-grade data collection

**For one-pagers:**
- Log template generation events
- Track template evolution events
- Record pattern discovery events
- Scientific-grade data for analysis

### 4. **EvolutionaryEvent System** (`src/waft/core/agent/state.py`)
**What it does:**
- Complete lineage tracking (genome_id, parent_id, generation)
- Fitness metrics tracking
- Event classification (SPAWN, MUTATE, GYM_EVAL, etc.)
- Lineage path reconstruction

**For one-pagers:**
- Templates have "genome IDs" (hash of style composition)
- Track template evolution lineage
- Parent-child relationships between template versions
- Generation tracking (template v1.0 → v1.1 → v2.0)
- Fitness metrics for template performance

### 5. **LineagePoet** (`src/waft/core/science/taxonomy.py`)
**What it does:**
- Generates scientific names from genome IDs
- Multilingual naming (Sanskrit, Norse, Latin, Cyber)
- Deterministic naming (same hash = same name)
- Culture detection and hybrid names

**For one-pagers:**
- Give templates scientific names based on style composition hash
- Example: "Cognis Novus, the Fragile" (Latin template)
- Example: "Prana Adi, the Swift" (Sanskrit template)
- Makes templates feel like living organisms!

### 6. **SessionReportGenerator** (`src/waft/core/science/report.py`)
**What it does:**
- Generates scientific reports from laboratory.jsonl
- Analyzes biodiversity (different types)
- Builds phylogenetic trees (evolution lineages)
- Tracks metabolic health (performance metrics)
- Reports breach incidents (failures)

**For one-pagers:**
- Generate pattern analysis reports
- Analyze template biodiversity (different style combinations)
- Build template phylogenetic trees (evolution history)
- Track template "metabolic health" (performance metrics)
- Report template "breaches" (failed generations)

### 7. **TamPsyche** (`src/waft/core/science/tam_psyche.py`)
**What it does:**
- Psychological state tracking (coherence, chaos, energy)
- Realization progress (threshold-based)
- Forgetfulness decay
- State persistence

**For one-pagers:**
- Track template "coherence" (style consistency)
- Track template "chaos" (style diversity/confusion)
- Track template "energy" (generation efficiency)
- Realization: when template reaches "optimal" state
- Forgetfulness: templates can "forget" bad patterns

### 8. **ChallengeGenerator** (`src/waft/study_gym.py`)
**What it does:**
- "Mad lib" style challenge templates
- Variable filling system
- Challenge types: `page_constraint`, `content_fitting`, `style_exploration`, etc.

**For one-pagers:**
- Create style exploration challenges
- Test specific style combinations
- Explore content type → style mappings
- Generate systematic test cases

### 9. **Fitness Metrics System** (Agent system)
**What it does:**
- Fitness scoring: `(Stability × 0.4) + (Efficiency × 0.3) + (Safety × 0.3)`
- Fitness thresholds (fitness < 0.5 = DEATH)
- Performance tracking

**For one-pagers:**
- Score templates: `(Aesthetic × 0.4) + (Efficiency × 0.3) + (UserRating × 0.3)`
- Templates with fitness < 0.5 are "dead" (not used)
- Track template performance over time

### 10. **Agent Spawn/Mutation System** (`src/waft/core/agent/base.py`)
**What it does:**
- Agents can spawn variants with mutations
- Code/config/prompt mutations
- Hot-swapping better genomes
- Lineage tracking

**For one-pagers:**
- Templates can "spawn" variants with style mutations
- Mutate style composition (add/remove styles)
- Hot-swap better template versions
- Track template evolution lineage

---

## Integrated Architecture

```
One-Pager Generation
        │
        ▼
┌─────────────────────────────────────┐
│   Study Gym Session                  │
│   - Observe: Track style composition│
│   - ChallengeGenerator: Style tests  │
│   - Hypothesize: What works?        │
│   - Test: Generate variations        │
│   - Analyze: Find patterns           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Template "Genome"                  │
│   - Hash style composition → ID      │
│   - LineagePoet → Scientific name    │
│   - EvolutionaryEvent → Lineage      │
│   - Fitness metrics → Performance    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   SessionAnalytics                   │
│   - Store session with metadata      │
│   - Track style composition          │
│   - Analyze trends & drift          │
│   - Compare approaches               │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   TheObserver                        │
│   - Log generation events            │
│   - Track evolution events           │
│   - Scientific JSONL log              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   SessionReportGenerator                 │
│   - Generate pattern reports         │
│   - Analyze biodiversity             │
│   - Build phylogenetic trees         │
│   - Track metabolic health           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   TamPsyche                          │
│   - Track template coherence         │
│   - Track template chaos             │
│   - Realization progress             │
└──────────────┬──────────────────────┘
               │
               ▼
        Template Evolution
        (Spawn variants, track fitness)
```

---

## Template as "Living Organism"

### Template Genome
```python
# Style composition hash = genome ID
style_composition = {
    "section_styles": ["story-section", "boxed-section"],
    "header_variants": ["", "boxed"],
    "list_styles": ["checkmarks"],
    ...
}
genome_id = hashlib.sha256(json.dumps(style_composition, sort_keys=True)).hexdigest()

# Scientific name from genome
scientific_name = LineagePoet.generate_name(genome_id)
# Example: "Cognis Novus, the Fragile" (Latin template)
# Example: "Prana Adi, the Swift" (Sanskrit template)
```

### Template Evolution
```python
# Template spawns variant (mutation)
parent_template = Template(genome_id="abc123...")
child_template = parent_template.spawn(mutation={
    "type": "style",
    "change": {"list_styles": ["checkmarks"] → ["boxed"]}
})
# Child has new genome_id, parent_id = "abc123..."
```

### Template Fitness
```python
fitness = (
    (aesthetic_score * 0.4) +      # Visual quality
    (efficiency_score * 0.3) +    # Generation speed
    (user_rating * 0.3)            # User feedback
)

if fitness < 0.5:
    template.status = "DEATH"  # Don't use this template
```

### Template Phylogenetic Tree
```
Template v1.0 (Prana Adi, the Swift)
    ├── Template v1.1 (Prana Dvitiya, the Great) [mutation: added boxed sections]
    │   ├── Template v1.2 (Prana Tritiya, the Wise) [mutation: added checkmarks]
    │   └── Template v1.3 (Prana Chaturtha, the Bold) [mutation: removed indented]
    └── Template v2.0 (Cognis Novus, the Fragile) [major mutation: new style system]
```

---

## Implementation Strategy

### Phase 1: Basic Integration
1. **Study Gym Integration**
   - Each one-pager generation = Study Gym session
   - Track style composition as observations
   - Use ChallengeGenerator for style exploration

2. **SessionAnalytics Integration**
   - Store each generation as session
   - Style composition in metadata
   - Use existing analysis methods

### Phase 2: Template Genome System
1. **Genome ID Generation**
   - Hash style composition → genome_id
   - Use LineagePoet for scientific names
   - Track template identity

2. **EvolutionaryEvent Integration**
   - Log template generation events
   - Track template evolution lineage
   - Parent-child relationships

### Phase 3: Advanced Analysis
1. **SessionReportGenerator Reports**
   - Generate pattern analysis reports
   - Template biodiversity analysis
   - Phylogenetic tree visualization

2. **TamPsyche Integration**
   - Track template coherence/chaos
   - Realization progress (optimal state)
   - Template "health" metrics

### Phase 4: Template Evolution
1. **Template Spawn System**
   - Templates spawn variants (mutations)
   - Style composition mutations
   - Hot-swap better templates

2. **Fitness System**
   - Score templates (aesthetic, efficiency, user rating)
   - Fitness < 0.5 = DEATH (don't use)
   - Track performance over time

---

## Example: Full Integration Flow

```python
# 1. Generate one-pager
pager = OnePager.from_markdown(content, title="My Doc")
output = pager.generate()

# 2. Create Study Gym session
gym = StudyGym()
session = gym.start_session({
    "name": "one_pager_generation",
    "content_type": "markdown",
    "title": "My Doc"
})

# 3. Track observations
gym.observe(
    action="style_composition",
    result={
        "section_styles": ["story-section", "boxed-section"],
        "header_variants": ["", "boxed"],
        "list_styles": ["checkmarks"],
        ...
    },
    metrics={"iterations": 6, "page_count": 2}
)

# 4. Generate template genome
style_composition = extract_style_composition(pager)
genome_id = hashlib.sha256(json.dumps(style_composition, sort_keys=True)).hexdigest()
scientific_name = LineagePoet.generate_name(genome_id)
# "Cognis Novus, the Fragile"

# 5. Create EvolutionaryEvent
event = EvolutionaryEvent(
    genome_id=genome_id,
    parent_id=parent_template_genome_id,  # If evolved
    generation=template_generation,
    event_type=EvolutionaryEventType.SPAWN,
    payload={
        "template_name": scientific_name,
        "style_composition": style_composition,
        "output_path": str(output)
    },
    fitness_metrics={
        "aesthetic": 0.8,
        "efficiency": 0.9,
        "user_rating": 0.85,
        "total": 0.85
    }
)

# 6. Log to TheObserver
observer.observe_event(event)

# 7. Save to SessionAnalytics
session = SessionRecord(
    session_id=f"one_pager_{genome_id[:8]}",
    approach_category="one_pager_markdown",
    metadata={
        "genome_id": genome_id,
        "scientific_name": scientific_name,
        "style_composition": style_composition,
        "fitness": event.fitness_metrics
    },
    success_indicators=["perfect_2_pages", "user_approved"]
)
analytics.save_session(session)

# 8. Update TamPsyche (template health)
psyche.update_coherence(0.1)  # Good style consistency
psyche.update_chaos(-0.05)     # Low confusion
psyche.increment_realization_progress(0.02)  # Moving toward optimal

# 9. End Study Gym session
gym.end_session()

# 10. Periodically: Generate SessionReportGenerator report
report_gen = SessionReportGenerator(project_path)
report = report_gen.generate_session_report()
# Includes: template biodiversity, phylogenetic tree, metabolic health
```

---

## Benefits of Full Integration

1. **Scientific Names**: Templates get beautiful names like "Prana Adi, the Swift"
2. **Lineage Tracking**: Complete evolution history of templates
3. **Fitness Scoring**: Templates scored and selected based on performance
4. **Pattern Reports**: Automatic scientific reports on template patterns
5. **Template Health**: Track coherence, chaos, realization progress
6. **Evolution**: Templates can spawn variants and evolve
7. **Research-Grade Data**: All data suitable for scientific analysis

---

## The Vision: Templates as Digital Organisms

Templates become **living digital organisms** that:
- Have scientific names (LineagePoet)
- Evolve through mutations (spawn system)
- Have fitness scores (performance metrics)
- Build phylogenetic trees (evolution history)
- Have psychological states (TamPsyche)
- Generate scientific reports (SessionReportGenerator)

Each one-pager generation is a **data point** in the evolution of template organisms. Over time, we observe which "species" of templates thrive and which go extinct.

---

**Status**: Full ecosystem mapped, ready for integration
