# /evolve-template - Evolve a WAFT Typst Template into a Living Artifact

**Comprehensive workflow to evolve any WAFT Typst template from static document into a living, queryable artifact integrated with the WAFT ecosystem.**

---

## Purpose

This command provides a **repeatable process** for evolving WAFT templates:

1. **Understand Current State** - Read and analyze the existing template
2. **System Context** - Understand how the template fits in WAFT's ecosystem
3. **Design Evolution** - Create comprehensive design for machine-readable format
4. **Create Work Effort** - Track the evolution with tickets
5. **Generate Artifacts** - Schema, examples, documentation
6. **Identify God** - Determine which Pantheon entity needs this tool
7. **Update Devlog** - Document the evolution

**Use when:**
- You have a Typst template that needs to evolve
- Template should integrate with Flight Recorder, Empirica, Realms, Beings
- Template needs machine-readable format (YAML frontmatter)
- Template should be queryable by AI agents
- Template should support versioning and validation

---

## Execution Workflow

### Phase 1: Understand Current State

**Actions:**
1. Read the target template file
2. Identify the template's purpose and domain
3. List current metadata fields
4. Note any existing integrations

**AI Prompt:**
```
I'm looking at [template_name].typ

Current template analysis:
- Purpose: [what does this template do?]
- Domain: [architecture, testing, security, process, etc.]
- Metadata Fields: [list current fields]
- Integrations: [any existing connections?]
```

### Phase 2: System Context Analysis

**Actions:**
1. Read WAFT README and architecture docs
2. Check existing templates in `templates/typst/`
3. Search for related work efforts
4. Identify integration points (Flight Recorder, Empirica, Realms, Beings)

**Key Integration Points:**
- **Flight Recorder**: How can this become an evolutionary event?
- **Empirica**: What epistemic claims does this track?
- **Realms/Beings**: Which entities would use this?
- **Work Efforts**: How does this connect to ongoing work?
- **API**: How should AI agents query this?

### Phase 3: Create Work Effort

**Actions:**
1. Create work effort with MCP tool
2. Generate 10 standard tickets:
   - Design machine-readable schema with YAML frontmatter
   - Implement registry and indexing system
   - Create Flight Recorder integration
   - Build Empirica integration
   - Develop cross-reference and dependency graph
   - Implement confidence calibration
   - Create automated validation hooks
   - Design versioning and evolution timeline
   - Build queryable API
   - Create template variants

**Naming Convention:**
```
WE-[YYMMDD]-[id]_[template_name]_evolution_living_artifacts
```

### Phase 4: Design Document

**Actions:**
Create comprehensive design document with these sections:

```markdown
# [Template Name] Evolution: Living [Type] Artifacts

## Executive Summary
[Vision for evolution]

## Part 1: Machine-Readable Schema
- Current State
- Evolved State: YAML Frontmatter + Typst Body
- Benefits

## Part 2: Registry & Indexing
- Architecture
- Index Schema
- CLI Commands

## Part 3: Flight Recorder Integration
- Event Types
- Entry Format
- Phylogenetic Analysis

## Part 4: Empirica Integration
- Epistemic Tracking
- CASCADE Workflow
- Learning Delta

## Part 5: Cross-Reference & Dependency Graph
- Link Types
- Visualization

## Part 6: Confidence Calibration
- Prediction Tracking
- Calibration Reports

## Part 7: Automated Validation
- Evidence Spec
- Validation Report
- Scheduled Validation

## Part 8: Versioning & Evolution Timeline
- Version History
- Timeline Command

## Part 9: Queryable API
- REST Endpoints
- Python SDK
- AI Agent Integration

## Part 10: Template Variants
- Type-specific templates
- Template selection

## Implementation Roadmap
[Phases with timeline]

## Success Metrics
[Measurable outcomes]
```

### Phase 5: Create Schema

**Actions:**
Create JSON Schema for validation at:
```
_work_efforts/WE-[id]/schemas/[template_name].schema.yaml
```

**Standard Schema Structure:**
```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "WAFT [Template Name] v2.0"
type: object

required:
  - [primary_entity]
  - [claim_or_content]
  - [verdict_or_status]

properties:
  [primary_entity]:
    # ID, type, version, timestamps
  [claim_or_content]:
    # Main content of the template
  [verdict_or_status]:
    # Outcome or current state
  evidence:
    # Files, tests, commands
  links:
    # Cross-references
  flight_recorder:
    # Event metadata
  empirica:
    # Epistemic vectors
  calibration:
    # Prediction tracking
  validation:
    # Auto-validation config
  history:
    # Version history
  tags:
    # Searchable tags
```

### Phase 6: Create Example

**Actions:**
Create example of evolved format at:
```
_work_efforts/WE-[id]/examples/[example_name].typ
```

**Example Structure:**
```typst
// WAFT [Template Name] v2.0 - Living [Type] Artifact
// YAML frontmatter in comment block

/*
---
[primary_entity]:
  id: [template_id]
  type: [template_type]
  version: 1
  created: [ISO timestamp]

[claim_or_content]:
  statement: "[main content]"
  domain: [domain]

[verdict_or_status]:
  status: [status]
  confidence: [0.0-1.0]

# ... rest of schema fields
---
*/

// Regular Typst document follows
#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering
// ... template content
```

### Phase 7: Identify the God

**Actions:**
Determine which Pantheon entity needs this template as a tool.

**Pantheon Candidates:**
| God | Domain | Would Use For |
|-----|--------|---------------|
| **The Archivist** | Knowledge & Memory | Case files, retrospectives, analyses |
| **The Scientist** | Hypothesis & Proof | Scientific method, experiments, proofs |
| **The Dealer** | Transactions & Contracts | Invoices, contracts, agreements |
| **The Storyteller** | Narrative & Worldbuilding | Storybooks, scenarios, worldbuilding |
| **The Librarian** | Organization & Retrieval | Catalogs, indexes, references |
| **The Inspector** | Verification & Audit | Checklists, audits, security reviews |
| **The Chronicler** | History & Timeline | Timelines, changelogs, evolution |
| **The Paperwork God** | Forms & Bureaucracy | Forms, reports, filings |

**Question to Answer:**
> "Which God in the WAFT Pantheon would wield this template as their primary tool? What does this template enable them to do?"

### Phase 8: Update Devlog

**Actions:**
Add entry to `_work_efforts/devlog.md`:

```markdown
## [DATE] - [Template Name] Evolution: Living [Type] Artifacts (Design Complete)

**Time**: [TIME]  
**Status**: ✅ **DESIGN COMPLETE** - WE-[id]

### Summary
[Brief description of evolution]

### Key Design Decisions
[Numbered list of major decisions]

### Why This Matters
[Bullet points on impact]

### Outputs
[List of files created]

### Pantheon Integration
**God**: [Which God]
**Tool Purpose**: [What this enables]

### Next Steps
[Implementation priorities]
```

---

## Quick Start

### Standard Usage
```
/evolve-template [path/to/template.typ]
```

### With Specific Domain
```
/evolve-template templates/typst/case_brief.typ --domain proof
```

### List Candidate Templates
```
/evolve-template --list
```

---

## Template Evolution Checklist

Use this checklist for every template evolution:

- [ ] **Read**: Understand current template
- [ ] **Context**: Identify system integration points
- [ ] **Work Effort**: Create WE with standard tickets
- [ ] **Design Doc**: Write 10-section design document
- [ ] **Schema**: Create JSON Schema for validation
- [ ] **Example**: Create evolved format example
- [ ] **God**: Identify Pantheon owner
- [ ] **Devlog**: Update development log
- [ ] **NO VERSION SUFFIXES**: Never use `_v1`, `_v2` in filenames

---

## Naming Conventions

### Files - NO VERSION SUFFIXES
❌ BAD: `case_brief_v2.typ`, `template_v1.schema.yaml`
✅ GOOD: `case_brief.typ`, `template.schema.yaml`

### Work Efforts
```
WE-[YYMMDD]-[id]_[template_name]_evolution_living_artifacts
```

### Design Documents
```
[TEMPLATE_NAME]_EVOLUTION_DESIGN.md
```

### Schemas
```
[template_name].schema.yaml
```

### Examples
```
[descriptive_example_name].typ
```

---

## Templates Eligible for Evolution

Current WAFT Typst templates that can be evolved:

| Template | Location | Domain | Status |
|----------|----------|--------|--------|
| Case Brief | `templates/typst/case_brief.typ` | Proof | ✅ Evolved (WE-260121-oxzc) |
| Aero-Check | `aero-check/examples/*.typ` | Checklists | Candidate |
| FHICT | `templates/typst/fhict/` | Academic | Candidate |
| Flow-Way | `templates/typst/templates/flow-way/` | Flow | Candidate |
| Umbra | `templates/typst/umbra/` | Shadow/Style | Candidate |

---

## Integration Points Reference

### Flight Recorder Events
```python
class TemplateEventType(Enum):
    TEMPLATE_CREATED = "template_created"
    TEMPLATE_PROVEN = "template_proven"
    TEMPLATE_REVISED = "template_revised"
    TEMPLATE_VALIDATED = "template_validated"
    TEMPLATE_INVALIDATED = "template_invalidated"
```

### Empirica Vectors
```yaml
empirica:
  preflight:
    engagement: [0.0-1.0]
    foundation:
      know: [0.0-1.0]
      do: [0.0-1.0]
      context: [0.0-1.0]
    uncertainty: [0.0-1.0]
  postflight:
    # Same structure
  learning_delta:
    total: [calculated]
    most_improved: [vector_name]
```

### Cross-Reference Types
```yaml
links:
  depends_on: []     # Prerequisites
  enables: []        # What this enables
  related_to: []     # Related templates
  revises: []        # Superseded templates
  work_efforts: []   # Connected work
  realms: []         # Connected realms
  beings: []         # Connected beings
  code: []           # Code artifacts
```

---

## Best Practices

1. **Start with Understanding**: Read the template thoroughly before designing
2. **System Thinking**: Consider all integration points
3. **Machine-First**: Design YAML schema before visual format
4. **No Version Suffixes**: Never `_v1`, `_v2` in filenames - use version field in schema
5. **Calibration**: Every template with confidence should track calibration
6. **Validation**: Every template with evidence should auto-validate
7. **God Assignment**: Every template belongs to a Pantheon entity
8. **Documentation**: Always update devlog

---

## Output Summary

After running `/evolve-template`, you should have:

1. **Work Effort** - WE-[id] with 10 standard tickets
2. **Design Document** - Comprehensive 10-section design
3. **Schema** - JSON Schema for validation
4. **Example** - Evolved format example
5. **God Assignment** - Pantheon entity identified
6. **Devlog Entry** - Development documented

---

## Related Commands

- **`/case-file`** - Generate case file from proof evidence
- **`/prove-it`** - Scientific method proof workflow
- **`/evolve`** - Complete Being evolution cycle
- **`/version-bake`** - Complete quality workflow
- **`/chronicle`** - View adventure journal

---

**Evolve any WAFT Typst template into a living artifact integrated with the WAFT ecosystem.**

--- End Command ---
