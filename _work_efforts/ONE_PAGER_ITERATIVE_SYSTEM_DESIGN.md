# One-Pager Iterative Learning System Design

**Created**: 2026-01-11
**Status**: Design Phase
**Purpose**: Design a system for collecting, analyzing, and evolving one-pager templates based on usage patterns

---

## Vision

The one-pager tool should be an **iterative learning system** that:
1. **Collects** metadata about each generated one-pager
2. **Learns** from successful patterns in collected data
3. **Evolves** base templates based on identified patterns
4. **Improves** continuously through natural usage

---

## Core Concept: The One-Pager Genome

Each generated one-pager has a "genome" - a complete description of:
- **Style Composition**: Which styles were used (sections, headers, lists, etc.)
- **Content Metrics**: Structure of the content (sections, headers, lists, paragraphs, code)
- **Generation Metadata**: How it was generated (iterations, scaling factors, etc.)
- **Lineage**: Which template version was used, parent genome (if evolved)

This genome is collected automatically and stored in a registry for analysis.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    One-Pager Generation                      │
│  (User creates one-pager via /one-pager command)            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Genome Collection (Automatic)                  │
│  - Extract style composition                                │
│  - Measure content metrics                                  │
│  - Record generation metadata                                │
│  - Create genome object                                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Genome Registry (Persistent Storage)            │
│  - Store genomes in JSON registry                           │
│  - Track lineage and versions                               │
│  - Enable querying and analysis                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Pattern Analysis (Periodic)                     │
│  - Identify successful style combinations                    │
│  - Analyze content type patterns                            │
│  - Detect generation efficiency patterns                    │
│  - Find user preference patterns (if ratings available)     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Template Evolution (Manual/Auto)                │
│  - Generate improved base templates from patterns           │
│  - Create template variants for A/B testing                │
│  - Update default style rotations                           │
│  - Refine CSS based on successful combinations              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       └──────────────────────────────────────┐
                                                              │
                       ┌──────────────────────────────────────┘
                       │
                       ▼
              (Feedback Loop: Improved templates
               lead to better outputs, which
               provide more data for evolution)
```

---

## Implementation Plan

### Phase 1: Genome Collection (Current)
- ✅ Create `OnePagerGenome` dataclass
- ✅ Create `GenomeCollector` class
- ⏳ Integrate genome collection into `OnePager.generate()`
- ⏳ Track style composition during generation
- ⏳ Record content metrics
- ⏳ Save generation metadata

### Phase 2: Pattern Analysis
- ⏳ Implement pattern analysis in `GenomeCollector.analyze_patterns()`
- ⏳ Identify successful style combinations
- ⏳ Analyze content type → style mappings
- ⏳ Detect generation efficiency patterns
- ⏳ Create analysis reports

### Phase 3: Template Evolution
- ⏳ Design template evolution algorithm
- ⏳ Generate improved base templates
- ⏳ Create template variant system
- ⏳ Implement A/B testing framework
- ⏳ Update default style rotations based on patterns

### Phase 4: User Feedback Integration
- ⏳ Add user rating system (optional)
- ⏳ Collect user notes/feedback
- ⏳ Weight analysis by user preferences
- ⏳ Prioritize highly-rated patterns

---

## Genome Data Structure

```python
@dataclass
class OnePagerGenome:
    # Identity
    id: str
    title: str
    output_path: Path
    created_at: datetime
    
    # Composition
    style_composition: StyleComposition
    content_metrics: ContentMetrics
    generation_metadata: GenerationMetadata
    
    # Lineage
    template_version: str
    parent_genome_id: Optional[str]
    
    # User feedback (optional)
    user_rating: Optional[float]
    user_notes: Optional[str]
```

---

## Style Composition Tracking

Track which styles were actually used:
- **Section Styles**: `['story-section', 'boxed-section', 'highlight-section', ...]`
- **Header Variants**: `['', 'boxed', 'highlight', 'underlined', ...]`
- **List Styles**: `['', 'custom-bullets', 'checkmarks', 'dashed', 'boxed']`
- **Paragraph Styles**: `['', 'indented', 'highlight', 'compact']`
- **Code Styles**: `['', 'boxed', 'minimal']`

This enables analysis like:
- "Boxed sections work well with markdown content"
- "Checkmark lists are preferred for action items"
- "Highlighted paragraphs improve readability in dense content"

---

## Content Metrics Tracking

Track content structure:
- Total sections, headers, lists, paragraphs, code blocks
- Content type (markdown, text, code, dict, etc.)
- Word count, character count

This enables analysis like:
- "Long-form content (2000+ words) benefits from indented paragraphs"
- "Code-heavy content works best with minimal code block style"
- "Structured data (dicts) prefers boxed sections"

---

## Generation Metadata Tracking

Track how generation worked:
- Number of CSS adjustment iterations needed
- Final font/margin/spacing scales
- Actual page count (should be 2)
- Generation time
- Whether content was condensed or expanded

This enables analysis like:
- "Content type X requires more iterations on average"
- "Certain style combinations converge faster"
- "Expanded content patterns indicate template needs adjustment"

---

## Pattern Analysis Examples

### Example 1: Style Combination Success
```
Analysis: "One-pagers with boxed-section + checkmark lists + highlighted paragraphs
          have average user rating of 0.85 (vs 0.65 for other combinations)"
Action: Increase probability of this combination in style rotation
```

### Example 2: Content Type Patterns
```
Analysis: "Markdown content with 5+ sections works best with story-section style"
Action: Add content-aware style selection logic
```

### Example 3: Generation Efficiency
```
Analysis: "Code-heavy content requires 12 iterations on average (vs 6 for text)"
Action: Optimize code block CSS to reduce iterations needed
```

---

## Template Evolution Strategy

### Automatic Evolution
- Analyze patterns every N genomes (e.g., every 50)
- Identify top-performing style combinations
- Update default style rotation probabilities
- Generate template variants for testing

### Manual Evolution
- Review analysis reports
- Manually adjust template based on insights
- Create new template versions
- A/B test new templates

### Versioning
- Track template versions (e.g., "1.0", "1.1", "2.0")
- Link genomes to template versions
- Compare performance across versions
- Roll back if new version performs worse

---

## Registry Structure

```
_work_efforts/one_pagers/
├── genome_registry.json          # Main registry (all genomes)
├── analysis_reports/              # Periodic analysis reports
│   ├── 2026-01-11_patterns.json
│   └── 2026-01-15_evolution.json
├── template_versions/             # Template version history
│   ├── v1.0_base.html
│   ├── v1.1_improved.html
│   └── v2.0_evolved.html
└── [generated PDFs]              # Actual one-pager PDFs
```

---

## Next Steps

1. **Integrate Genome Collection** into `OnePager.generate()`
   - Track style composition during generation
   - Measure content metrics
   - Record generation metadata
   - Create and register genome

2. **Test Collection System**
   - Generate several one-pagers
   - Verify genomes are collected
   - Check registry structure

3. **Implement Basic Analysis**
   - Style distribution analysis
   - Content type patterns
   - Generation efficiency metrics

4. **Design Evolution Algorithm**
   - How to identify successful patterns
   - How to generate improved templates
   - How to test new templates

---

## Questions to Explore

- How do we identify "successful" patterns? (user ratings? usage frequency? aesthetic analysis?)
- How do we balance diversity with consistency?
- What's the right frequency for analysis and evolution?
- How do we handle template versioning and rollback?
- Should evolution be automatic or manual?
- How do we test new templates without breaking existing functionality?

---

## Philosophy

> "Each one-pager is a data point. Each variation teaches us something
> about what works, what doesn't, and how information can be presented
> differently."

The one-pager tool becomes a **living system** that learns and evolves
through use. Knowledge crystallized in paper, and the tool that creates
it learns from each crystallization.

---

**Status**: Design complete, ready for implementation
