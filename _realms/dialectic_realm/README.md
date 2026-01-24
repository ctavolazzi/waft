# DIALECTIC Realm

> "The truth is the whole." - G.W.F. Hegel

## The God: DIALECTIC

**True Name:** The Dialectical Analysis Engine  
**Port:** 2112  
**Philosophy:** Hegelian Dialectics

DIALECTIC is a God that orchestrates three-phase analysis workflows, implementing the Hegelian dialectical method to systematically evaluate project state and generate actionable documentation.

## The Three Phases

### 1. THESIS (Assembly Phase)
*Color: Blue (#1f6feb)*

Gathers context and establishes initial propositions:
- Project context and state
- Git repository analysis
- Work effort discovery
- AI Town analysis (distributed Being analysis)
- Comprehensive orchestration

**Output:** Assembly Report PDF

### 2. ANTITHESIS (Sanity Check Phase)
*Color: Red (#da3633)*

Challenges assumptions and validates evidence:
- Extract assumptions from thesis
- Validate each assumption with evidence
- Create checkout documentation
- Generate recommendations

**Output:** Sanity Check Report PDF

### 3. SYNTHESIS (Problem Description Phase)
*Color: Purple (#a371f7)*

Resolves contradictions and generates conclusions:
- Analyze previous phase outputs
- Create structured problem description
- Generate MVP documents
- Produce scientific-quality report

**Output:** Scientific Report PDF

## Final Output: SITREP

The SITREP (Situation Report) combines all three phases into a comprehensive status document that can be used to seed a Work Effort.

## Usage

### Start the Server
```bash
waft dialectic
```
Opens web dashboard at http://localhost:2112

### Run Individual Phases
```bash
waft dialectic --assembly      # Run Thesis phase only
waft dialectic --antithesis    # Run Antithesis phase only
waft dialectic --synthesis     # Run Synthesis phase only
```

### Generate SITREP
```bash
waft dialectic --sitrep
```

### Full Workflow
```bash
waft dialectic --full
```

## Directory Structure

```
_realms/dialectic_realm/
├── realm_manifest.json    # Realm configuration
├── README.md              # This file
├── sessions/              # Analysis session data
├── outputs/               # Generated PDFs
│   ├── assembly/          # Thesis phase outputs
│   ├── sanity/            # Antithesis phase outputs
│   └── synthesis/         # Synthesis phase outputs
└── templates/             # Custom Typst templates
```

## Tools

Reusable Typst tools are available at `tools/typst/`:
- `scientific_base.typ` - Scientific report template
- `phase_report.typ` - Phase-specific templates
- `sitrep_template.typ` - SITREP formatting
- `dialectic_components.typ` - Shared components

## Philosophy

The DIALECTIC Engine implements the Hegelian dialectical method:

1. **Thesis**: An initial proposition or state
2. **Antithesis**: The negation or opposition to the thesis
3. **Synthesis**: The resolution that preserves truth from both

This method enables systematic, evidence-based analysis that:
- Gathers comprehensive context
- Challenges assumptions rigorously
- Produces actionable conclusions

## Integration

- **Observatory (Port 2077)**: Can monitor DIALECTIC as a mesh node
- **PortRegistry**: Port 2112 registered for dialectic_realm
- **Work Efforts**: SITREP can seed new work efforts
- **Oracle**: Provides epistemic state for analysis
- **Being System**: AI Town spawns Beings for distributed analysis

## Related Links

- [Hegel's Dialectical Process](https://en.wikipedia.org/wiki/Dialectic#Hegelian_dialectic)
- [WAFT Documentation](../../README.md)
- [Typst Tools](../../tools/typst/README.md)
