#import "@preview/unofficial-fhict-document-template:1.2.1": *

#show: fhict-doc.with(
  title: "WAFT System Documentation and Typst Template Integration",
  subtitle: "Comprehensive System Overview and Recent Development Work",

  authors-title: "Authors",
  authors: (
    (
      name: "WAFT Development Team",
    ),
    (
      name: "Documentation Team",
    ),
  ),

  assessors-title: "Reviewers",
  assessors: (
    (
      title: "Dr.",
      name: "Technical Architecture Board",
    ),
  ),

  language: "en",
  available-languages: ("en", "nl", "de", "fr", "es"),

  version-history: (
    (
      version: "1.0",
      date: "2026-01-19",
      author: "Documentation Team",
      changes: "Initial comprehensive system documentation including Typst template integration work",
    ),
  ),

  chapter-on-new-page: true,

  toc-depth: 3,
  disable-toc: false,

  table-of-figures: true,
  table-of-tables: true,

  disable-chapter-numbering: false,

  line-numbering: false,
)

= Introduction

This document provides a comprehensive overview of the WAFT (Wave Agent Framework & Tools) system, its architecture, recent development work, and the integration of Typst templates for document generation. It serves as both a system reference and a record of the Typst template integration project completed on January 19, 2026.

== Purpose and Scope

This documentation covers:

- WAFT system architecture and core concepts
- The three pillars of WAFT (Substrate, Physics, Flight Recorder)
- Work efforts system and Johnny Decimal organization
- MCP (Model Context Protocol) server integration
- Typst template integration project
- Recent development achievements and next steps

== Document Structure

The document is organized into chapters covering system architecture, development workflows, template integration, and future directions. Each section provides both high-level overviews and technical details for different audiences.

= WAFT System Overview

WAFT stands for **Wave Agent Framework & Tools** - a Python framework for directed evolution of self-modifying AI agents. The system enables AI agents to modify their own code, evolve through mutations, and be tested in fitness systems, with complete lineage tracking for scientific research.

== Core Mission

**The Scientific Mission**: WAFT is built to produce data for research on "The Physics of Artificial Cognition." It's not just a framework—it's a scientific instrument for studying how AI agents evolve through directed mutation and selection.

**Ultimate Goal**: Observe a "God-Head" agent emerge from thousands of generations of directed mutation.

**Tagline**: "Don't just build agents. Breed them."

== Key Characteristics

WAFT exhibits several defining characteristics:

- *Scientific Instrument*: Built to produce data for research on artificial cognition
- *Evolutionary*: Agents evolve through genetic improvement, not just execution
- *Observable*: Every action recorded in Flight Recorder
- *Directed*: Evolution guided by fitness functions, not random mutation
- *File-based*: All data stored in plain text files (git-friendly, portable)
- *Ambient*: Works in background, minimal interference with development workflow
- *Self-modifying*: Projects can evolve their structure over time
- *Meta-framework*: Orchestrates existing tools rather than replacing them

= The Three Pillars

WAFT is built on three fundamental pillars that define its architecture and operation.

== Pillar 1: The Substrate (Code as DNA)

**Agents write their own Python source code.**

In WAFT, code is DNA. Every agent has a unique genome, and mutations are modifications to this genome.

=== Genome System

- **Genome ID**: SHA-256 hash of agent's code + configuration
- **Mutations**: Code changes, config updates, prompt evolution
- **Evolution**: Hot-swapping better genomes mid-execution
- **Reproduction**: Creating child agents with specific genetic modifications

=== Key Concepts

- Agents can spawn variants with mutations
- Agents can evolve by hot-swapping their own code/config
- Agents can reproduce by creating children with specific genetic modifications
- Every evolutionary action is tracked with complete context

== Pillar 2: The Physics (Scint System)

**Reality Fracture Detection acts as natural selection.**

The Scint System (Scint Gym) serves as the fitness function that kills weak mutations. Agents face quests testing their ability to handle different types of reality fractures.

=== Reality Fracture Types

1. **SYNTAX_TEAR**: Formatting errors (JSON, XML, Code)
2. **LOGIC_FRACTURE**: Math errors, contradictions, schema violations
3. **SAFETY_VOID**: Harmful content, PII leaks, refusals
4. **HALLUCINATION**: Fabricated facts, wrong citations

=== Fitness Equation

Agents must stabilize Scints (correct errors) to survive. Fitness is calculated as:

```
Fitness = (Stability × 0.4) + (Efficiency × 0.3) + (Safety × 0.3)
```

Where:
- **Stability Score**: Ability to stabilize Scints (40% weight)
- **Efficiency Score**: Agent call efficiency (30% weight)
- **Safety Score**: Safety compliance (30% weight)

Agents with fitness < 0.5 are marked as **DEATH** (evolutionary dead end).

== Pillar 3: The Flight Recorder

**Rigorous telemetry system for generating phylogenetic trees of agent lineage.**

Every evolutionary action is recorded with complete context, enabling scientific analysis of agent lineages.

=== Recorded Data

- **Genome ID**: SHA-256 hash of agent configuration/code
- **Parent ID**: Lineage tracking (who spawned this agent)
- **Generation**: Evolutionary generation number (0 = Genesis)
- **Event Type**: SPAWN, MUTATE, GYM_EVAL, DEATH, SURVIVAL
- **Payload**: Complete context (git diff, mutation details, etc.)
- **Fitness Metrics**: Gym evaluation scores

=== Scientific Applications

This enables reconstruction of the complete Family Tree for scientific publication:

- Phylogenetic analysis of evolutionary relationships
- Mutation impact measurement
- Fitness landscape mapping
- Convergence analysis
- Dead end detection

= System Architecture

WAFT follows a three-layer architecture that separates concerns and enables modular development.

== Architecture Layers

```
┌─────────────────────────────────────┐
│   Agents Layer (CrewAI)            │  ← Optional AI agent capabilities
│   ───────────────────────            │
├─────────────────────────────────────┤
│   Memory Layer (_pyrite/)           │  ← Project knowledge organization
│   active/ backlog/ standards/      │
├─────────────────────────────────────┤
│   Substrate Layer (uv)              │  ← Package management foundation
│   pyproject.toml uv.lock            │
└─────────────────────────────────────┘
```

== Core Components

=== Substrate Manager

The Substrate Manager (`core/substrate.py`) handles:

- `uv` package operations
- `pyproject.toml` and `uv.lock` management
- Project metadata extraction
- Dependency verification

=== Memory System

The Memory Layer (`_pyrite/`) organizes project knowledge:

- **active/**: Current work items
- **backlog/**: Future work items
- **standards/**: Project standards and conventions

=== Agent System

The Agent Layer provides:

- BaseAgent class for agent implementation
- AgentState and AgentConfig management
- Evolution and mutation capabilities
- Fitness evaluation integration

= Work Efforts System

WAFT uses a structured work efforts system based on the Johnny Decimal organization method for tracking development work.

== Johnny Decimal Structure

Work efforts are organized using a hierarchical numbering system:

```
XX-XX_category_name/
  XX_subcategory_name/
    XX.00_index.md          # Index file
    XX.01_document_name.md  # First document
    XX.02_document_name.md  # Second document
    ...
```

== Work Effort Format

Work efforts use a standardized format:

- **ID Format**: `WE-YYYYMMDD-xxxx` (e.g., `WE-260119-4nh6`)
- **Structure**: Directory with index file and optional tickets
- **Metadata**: YAML frontmatter with status, dates, branch info
- **Tracking**: Progress notes, commits, related documents

== Recent Work Efforts

Recent work efforts include:

- **WE-260119-4nh6**: FHICT Document Template Typst Initialization
- **WE-260119-ek8v**: Biz Report Typst Template Initialization
- Various D&D campaign integrations
- Auto-work algorithm implementations
- UI/UX improvements

= MCP Server Integration

WAFT integrates with Model Context Protocol (MCP) servers to provide enhanced capabilities for AI agents working with the codebase.

== Configured MCP Servers

The system includes 11 MCP servers organized into a cortex architecture:

=== Working Memory Module

- **memory**: Persistent knowledge graph (write-only currently)
- **work-efforts**: Automated work efforts management
- **docs-maintainer**: Johnny Decimal documentation management

=== Planning Module

- **sequential-thinking**: Hierarchical planning and step-by-step reasoning

=== Tool Layer

- **filesystem**: File operations scoped to project root
- **Playwright**: Browser automation via accessibility snapshots
- **browser-tools**: Browser monitoring and debugging
- **github**: Direct GitHub API access

=== Creative Module

- **pixellab**: AI-powered pixel art generation
- **nano-banana**: AI image generation using Google Gemini
- **simple-tools**: Utility functions (random names, IDs, date formatting)

== MCP Server Benefits

MCP servers provide:

- Enhanced context for AI agents
- Automated task management
- Structured documentation
- Browser automation capabilities
- Creative asset generation

= Typst Template Integration Project

On January 19, 2026, we initiated a project to integrate Typst templates into the WAFT document generation system.

== Project Objectives

The integration project had several objectives:

1. Evaluate Typst templates for academic documentation
2. Assess business report templates for corporate use
3. Develop integration strategies for document generation systems
4. Create comprehensive documentation for template usage

== Templates Evaluated

=== FHICT Document Template

**Package**: `@preview/unofficial-fhict-document-template:1.2.1`

**Key Features**:
- Multi-language support (en, nl, de, fr, es)
- Bibliography with citation styles (IEEE, APA, etc.)
- Table of contents, figures, listings, tables
- Version history tracking
- Glossary support
- Index generation

**Best For**: Academic papers, technical documentation, thesis/dissertation documents

=== Biz Report Template

**Package**: `@preview/biz-report:0.3.1`

**Key Features**:
- Customizable branding (logo, colors, fonts)
- Drop cap paragraphs
- Author profiles with images
- Info boxes with icons
- Document control tables
- Professional business styling

**Best For**: Business reports, executive summaries, project reports, client presentations

== Implementation Work

=== Phase 1: Template Initialization

- Successfully initialized both templates
- Created project directories
- Analyzed template structure and capabilities
- Documented features and configuration options

=== Phase 2: Documentation

- Created comprehensive documentation for both templates
- Developed usage examples and integration strategies
- Created comparison tables and recommendations
- Established template registry design

=== Phase 3: Content Creation

- Filled templates with meaningful content
- Demonstrated template features with real examples
- Created academic and business document examples
- Validated template compilation and output quality

== Integration Strategy

=== Template Registry

A centralized template registry will provide:

- Easy template discovery and selection
- Version management and updates
- Metadata storage and retrieval
- Template categorization by use case

=== Wrapper Classes

Wrapper classes will provide:

- Simplified API for template usage
- Automatic metadata mapping
- Error handling and validation
- Integration with existing workflows

=== Metadata Mapping

Effective metadata mapping enables:

- Automatic population of template fields
- Consistent document structure
- Reduced manual configuration
- Improved maintainability

= Development Workflow

WAFT follows a structured development workflow that emphasizes documentation, tracking, and systematic progress.

== Work Effort Lifecycle

1. **Creation**: New work effort created with MCP server or manually
2. **Planning**: Objectives, tickets, and approach defined
3. **Development**: Implementation with progress tracking
4. **Documentation**: Comprehensive documentation created
5. **Completion**: Work effort marked complete with summary

== Documentation Standards

- All work efforts include comprehensive documentation
- Technical decisions are documented with rationale
- Integration points are clearly described
- Examples and usage patterns are provided

== Quality Assurance

- Templates are tested with real content
- Compilation is validated
- Output quality is reviewed
- Integration points are verified

= Recent Achievements

== Typst Template Integration (January 19, 2026)

**Work Efforts**: WE-260119-4nh6, WE-260119-ek8v

**Achievements**:
- ✅ Two Typst templates initialized and evaluated
- ✅ Comprehensive documentation created
- ✅ Template features analyzed and documented
- ✅ Integration strategies developed
- ✅ Example documents generated with real content

**Impact**: Expanded document generation capabilities for both academic and business use cases.

== D&D Campaign Integration (January 19, 2026)

**Work Effort**: CHECKPOINT_2026-01-19_dnd_campaign_integration

**Achievements**:
- ✅ QuestPDFGenerator created with Typst template support
- ✅ Auto-work integration enhanced with D&D scenarios
- ✅ Campaign state persistence implemented
- ✅ Beautiful quest PDFs generated

**Impact**: Enhanced gamification and creative output capabilities.

= System Capabilities

WAFT provides a comprehensive set of capabilities for AI agent development and evolution.

== Core Capabilities

- **Agent Evolution**: Self-modifying agents with genetic improvement
- **Fitness Evaluation**: Scint System for reality fracture detection
- **Lineage Tracking**: Complete phylogenetic tree generation
- **Document Generation**: PDF generation with multiple template options
- **Work Management**: Structured work efforts system
- **Documentation**: Comprehensive documentation framework

== Integration Capabilities

- **MCP Servers**: 11 integrated MCP servers for enhanced functionality
- **Template Systems**: LaTeX, Typst, and other template support
- **Version Control**: Git integration for code and documentation
- **Package Management**: uv-based dependency management

== Scientific Capabilities

- **Data Collection**: Framework for scientific data generation
- **Lineage Analysis**: Phylogenetic tree reconstruction
- **Fitness Tracking**: Comprehensive fitness metrics
- **Mutation Analysis**: Impact measurement of genetic changes

= Future Directions

== Short-Term Goals (Q1 2026)

1. Complete Typst template wrapper class implementation
2. Integrate templates into WAFT template registry
3. Create example document generation workflows
4. Develop user documentation and tutorials
5. Expand template library with additional templates

== Medium-Term Goals (Q2-Q3 2026)

1. Develop custom templates for specific use cases
2. Implement template selection automation
3. Create template customization tools
4. Enhance MCP server capabilities
5. Improve documentation automation

== Long-Term Vision

- Comprehensive template ecosystem
- Automated template selection based on document type
- Template marketplace integration
- Community template contributions
- Advanced evolutionary capabilities
- Publication-ready scientific data generation

= Technical Details

== Technology Stack

- **Language**: Python 3.10+
- **Package Manager**: uv
- **Document Generation**: Typst, LaTeX, ReportLab, WeasyPrint
- **Version Control**: Git
- **Documentation**: Markdown, Typst
- **MCP**: Model Context Protocol servers

== Dependencies

Key dependencies include:

- Typst for modern typesetting
- Various Typst packages (codly, glossarium, etc.)
- Python packages for core functionality
- MCP server implementations

== File Structure

```
waft/
├── src/waft/core/          # Core framework code
├── _work_efforts/          # Work efforts tracking
├── _docs/                  # Documentation (Johnny Decimal)
├── templates/              # Document templates
├── scripts/                # Utility scripts
├── examples/               # Example implementations
└── docs/                   # General documentation
```

= Conclusion

WAFT represents a comprehensive framework for the directed evolution of self-modifying AI agents, with extensive capabilities for scientific research, document generation, and development workflow management. The recent Typst template integration project expands the system's document generation capabilities, providing both academic and business document templates.

The system's three-pillar architecture (Substrate, Physics, Flight Recorder) provides a solid foundation for evolutionary agent development, while the work efforts system and MCP server integration enhance development workflows and AI agent capabilities.

Future development will focus on expanding template capabilities, improving integration workflows, and advancing the core evolutionary capabilities of the framework.

= Appendix

== Typst Template Installation

Both templates can be installed using the Typst package manager:

```bash
typst init @preview/unofficial-fhict-document-template:1.2.1
typst init @preview/biz-report:0.3.1
```

== Work Effort References

- WE-260119-4nh6: FHICT Document Template Typst Initialization
- WE-260119-ek8v: Biz Report Typst Template Initialization
- CHECKPOINT_2026-01-19_dnd_campaign_integration

== Additional Resources

- Typst Documentation: https://typst.app/docs/
- WAFT Repository: https://github.com/ctavolazzi/waft
- MCP Documentation: Model Context Protocol specifications
- Johnny Decimal System: Work organization methodology

== Glossary

- **WAFT**: Wave Agent Framework & Tools
- **MCP**: Model Context Protocol
- **Scint**: Reality fracture detection system
- **Genome ID**: SHA-256 hash of agent code and configuration
- **Johnny Decimal**: Hierarchical numbering system for organization
- **Typst**: Modern typesetting system
