# One-Pager Iterative Learning: Using Existing Tools

**Created**: 2026-01-11
**Status**: Refactored Design
**Purpose**: Recontextualize existing WAFT tools for one-pager learning system

---

## Existing Tools We Should Use

### 1. Study Gym (`src/waft/study_gym.py`)
**What it does:**
- Observation tracking with metrics
- Hypothesis formation and testing
- Pattern analysis
- Session management
- JSON storage of sessions

**How to use for one-pagers:**
- Each one-pager generation = a Study Gym session
- Track style composition as "observations"
- Form hypotheses about successful style combinations
- Test hypotheses by generating variations
- Analyze patterns across sessions

### 2. SessionAnalytics (`src/waft/core/session_analytics.py`)
**What it does:**
- Session tracking with metadata
- SQLite database for structured queries
- Pattern analysis (trends, drift, comparisons)
- Iteration chain tracking
- Success indicators

**How to use for one-pagers:**
- Track each one-pager generation as a session
- Store style composition in `metadata` field
- Use `approach_category` for content type (markdown, code, dict, etc.)
- Use `success_indicators` for user ratings/feedback
- Analyze patterns with existing `analyze_productivity_trends()` and `compare_approaches()`

### 3. TheObserver (`src/waft/core/science/observer.py`)
**What it does:**
- Scientific event logging (JSONL)
- Immutable log for research
- Event tracking with context

**How to use for one-pagers:**
- Log one-pager generation events (optional, for scientific tracking)
- Track template evolution events
- Record pattern discovery events

---

## Refactored Architecture

```
One-Pager Generation
        │
        ▼
┌─────────────────────────────────────┐
│   Study Gym Session                 │
│   - Observe: Track style composition│
│   - Hypothesize: What works?        │
│   - Test: Generate variations       │
│   - Analyze: Find patterns          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   SessionAnalytics                  │
│   - Store session with metadata     │
│   - Track style composition         │
│   - Track success indicators        │
│   - Enable pattern queries           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Pattern Analysis                  │
│   - Use existing analytics methods  │
│   - Compare approaches              │
│   - Identify successful patterns    │
└──────────────┬──────────────────────┘
               │
               ▼
        Template Evolution
```

---

## Implementation Plan

### Phase 1: Integrate Study Gym
- Modify `OnePager.generate()` to start a Study Gym session
- Track style composition as observations
- Record generation metadata (iterations, scaling factors)
- Save session at end of generation

### Phase 2: Integrate SessionAnalytics
- Create `SessionRecord` for each one-pager generation
- Store style composition in `metadata` field
- Use `approach_category` for content type
- Use `success_indicators` for user feedback (if provided)

### Phase 3: Pattern Analysis
- Use `SessionAnalytics.analyze_productivity_trends()` to find patterns
- Use `SessionAnalytics.compare_approaches()` to compare style combinations
- Use `SessionAnalytics.analyze_prompt_drift()` to track template evolution

### Phase 4: Template Evolution
- Analyze collected sessions to identify successful patterns
- Update template style rotations based on patterns
- Generate improved base templates

---

## Data Structure

### Study Gym Session
```python
challenge_config = {
    "name": "one_pager_generation",
    "objective": "Create 2-page one-pager",
    "content_type": "markdown",  # or "code", "dict", etc.
    "title": "My One-Pager"
}

# Observations track:
# - Style composition (which styles were used)
# - Generation metadata (iterations, scaling factors)
# - Content metrics (sections, headers, lists, etc.)
```

### SessionAnalytics Record
```python
SessionRecord(
    session_id="one_pager_20260111_105000",
    timestamp="2026-01-11T10:50:00",
    approach_category="one_pager_markdown",  # or "one_pager_code", etc.
    metadata={
        "style_composition": {
            "section_styles": ["story-section", "boxed-section", ...],
            "header_variants": ["", "boxed", ...],
            "list_styles": ["", "checkmarks", ...],
            "paragraph_styles": ["", "indented", ...],
            "code_styles": ["", "boxed", ...]
        },
        "content_metrics": {
            "total_sections": 5,
            "total_headers": 8,
            "total_lists": 3,
            "word_count": 1200
        },
        "generation_metadata": {
            "iterations": 6,
            "font_scale_final": 0.95,
            "margin_scale_final": 0.92,
            "page_count": 2
        },
        "output_path": "_work_efforts/one_pagers/..."
    },
    success_indicators=["perfect_2_pages", "user_approved"]  # if user provides feedback
)
```

---

## Benefits of Using Existing Tools

1. **No Reinvention**: Reuse proven, tested systems
2. **Consistency**: Same patterns across WAFT
3. **Integration**: Works with existing analytics and visualization
4. **Maintenance**: One less system to maintain
5. **Features**: Get all existing features (trends, comparisons, etc.) for free

---

## Next Steps

1. **Modify `OnePager.generate()`** to:
   - Start a Study Gym session
   - Track observations during generation
   - Save session at end

2. **Create SessionAnalytics integration**:
   - Save each generation as a session record
   - Store style composition in metadata
   - Enable pattern queries

3. **Use existing analysis methods**:
   - `analyze_productivity_trends()` for style usage trends
   - `compare_approaches()` for style combination comparisons
   - `analyze_prompt_drift()` for template evolution tracking

---

**Status**: Design refactored to use existing tools
