// WAFT Documentation and Field Manual
// The Evolutionary Code Laboratory Handbook
// Using all 7 Typst packages

#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering
#import "@preview/drafting:0.2.2": *
#import "@preview/scaffolder:0.2.1": scaffolding
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *
#import "@preview/pinit:0.2.2": *
#import "@preview/showybox:2.0.4": showybox

// ============================================================================
// DOCUMENT SETUP
// ============================================================================

#let header = {
  set align(bottom)
  set text(weight: "bold", size: 9pt)
  table(
    stroke: (y: none),
    columns: (1fr, 2fr, 1fr),
    rows: 1fr,
    table.hline(),
    [WAFT v1.0],
    align(center)[Field Manual & Documentation],
    align(right)[#context counter(page).display("1 / 1", both: true)],
  )
}

#let footer = {
  set text(size: 8pt, fill: gray)
  table(
    stroke: (y: none),
    columns: (1fr, 1fr),
    rows: 1fr,
    [Classification: Open Source],
    align(right)[github.com/ctavolazzi/waft],
    table.hline(),
  )
}

#show: s6t5-page-bordering.with(
  margin: (left: 50pt, right: 70pt, top: 80pt, bottom: 70pt),
  expand: 12pt,
  space-top: 12pt,
  space-bottom: 12pt,
  stroke-header: none,
  stroke-footer: none,
  header: header,
  footer: footer,
)

#set text(font: "New Computer Modern", size: 10pt)
#set page(paper: "us-letter")

// Initialize codly
#show: codly-init.with()
#codly(languages: codly-languages)

// Set up drafting
#set-page-properties(margin-right: 70pt)

// ============================================================================
// TITLE PAGE
// ============================================================================

#align(center + horizon)[
  #text(size: 14pt, fill: gray)[THE EVOLUTIONARY CODE LABORATORY]
  
  #v(0.5em)
  
  #text(size: 42pt, weight: "bold")[
    WAFT
  ]
  
  #v(0.3em)
  
  #text(size: 18pt, fill: gray.darken(20%))[
    Field Manual & Documentation
  ]
  
  #v(2em)
  
  #showybox(
    frame: (
      border-color: blue.darken(30%),
      body-color: blue.lighten(95%),
      thickness: 2pt,
      radius: 8pt,
    ),
    shadow: (offset: 4pt, color: gray.lighten(60%)),
  )[
    #align(center)[
      #text(size: 12pt, style: "italic")[
        "Don't just build agents. *Breed* them."
      ]
    ]
  ]
  
  #v(2em)
  
  #rect(fill: luma(245), inset: 1.5em, radius: 5pt)[
    #grid(
      columns: 2,
      gutter: 2em,
      [
        *Version:* 1.0.0 \
        *License:* MIT \
        *Python:* 3.10+
      ],
      [
        *Date:* January 2026 \
        *Author:* ctavolazzi \
        *Status:* Active Development
      ],
    )
  ]
  
  #v(3em)
  
  #text(size: 10pt, fill: gray)[
    A Python framework for directed evolution of self-modifying AI agents
  ]
]

#pagebreak()

// ============================================================================
// TABLE OF CONTENTS
// ============================================================================

#outline(
  title: [Table of Contents],
  indent: 1.5em,
  depth: 2,
)

#pagebreak()

// ============================================================================
// CHAPTER 1: INTRODUCTION
// ============================================================================

= Introduction
#label("ch-intro")

#showybox(
  frame: (
    border-color: purple.darken(20%),
    title-color: purple.lighten(70%),
    body-color: purple.lighten(92%),
  ),
  title: "The Promise",
)[
  Waft is a scientific instrument for studying the *physics of artificial cognition* through directed evolution. We don't just create AI agents—we breed them, test them in the crucible of reality, and observe them evolve over thousands of generations.
]

#margin-note[
  The ultimate goal: observe a "God-Head" agent emerge from evolution.
]

== What is WAFT?

WAFT is an evolutionary code laboratory where:

- *Code is DNA* — Agents can modify their own source code
- *Fitness determines survival* — The Scint system tests agents
- *Everything is recorded* — The Flight Recorder tracks lineage

#pin("dna1")DNA#pin("dna2") → #pin("mut1")Mutation#pin("mut2") → #pin("fit1")Fitness Test#pin("fit2") → #pin("sel1")Selection#pin("sel2") → Evolution

#pinit-arrow("dna2", "mut1", start-dx: 3pt, end-dx: -3pt)
#pinit-arrow("mut2", "fit1", start-dx: 3pt, end-dx: -3pt)
#pinit-arrow("fit2", "sel1", start-dx: 3pt, end-dx: -3pt)

#v(1em)

== Core Pillars

#grid(
  columns: 3,
  gutter: 1em,
  showybox(
    frame: (border-color: blue, body-color: blue.lighten(92%)),
    title: "1. The Substrate",
  )[
    Agents write their own Python source code (DNA)
  ],
  showybox(
    frame: (border-color: green, body-color: green.lighten(92%)),
    title: "2. The Physics",
  )[
    Scint System tests fitness and kills weak mutations
  ],
  showybox(
    frame: (border-color: orange, body-color: orange.lighten(92%)),
    title: "3. Flight Recorder",
  )[
    Telemetry for phylogenetic tree generation
  ],
)

#pagebreak()

// ============================================================================
// CHAPTER 2: QUICK START
// ============================================================================

= Quick Start Guide
#label("ch-quickstart")

== Installation

#showybox(
  frame: (border-color: gray, body-color: luma(250)),
  title: "Prerequisites",
)[
  - Python 3.10+
  - `uv` package manager
  - `just` task runner (optional)
]

#margin-note(side: left)[
  Use `uv` for best experience!
]

=== Install WAFT

```bash
# Using uv (recommended)
uv tool install waft

# Or from source
git clone https://github.com/ctavolazzi/waft.git
cd waft
uv sync
uv tool install --editable .
```

== Create Your First Laboratory

```bash
# Create a new evolutionary laboratory
waft new my_laboratory

# Navigate and verify
cd my_laboratory
waft verify
```

#showybox(
  frame: (border-color: green.darken(30%), body-color: green.lighten(90%)),
  title-style: (color: black),
  title: "✓ Success",
)[
  Your laboratory is ready! You now have the basic structure for evolving agents.
]

== The Evolutionary Cycle

```bash
# 1. Spawn variants with mutations
waft spawn --agent RefactorAgent --mutation "improved_prompt.json"

# 2. Evaluate fitness in the Gym
waft eval --agent RefactorAgent

# 3. Evolve into the fittest variant
waft evolve --agent RefactorAgent --generation 5
```

#pagebreak()

// ============================================================================
// CHAPTER 3: CORE CONCEPTS
// ============================================================================

= Core Concepts
#label("ch-concepts")

== The Substrate: Code as DNA

#margin-note[
  Every agent has a unique genome ID (SHA-256 hash)
]

In WAFT, *code is DNA*. Agents can:

#showybox(
  frame: (border-color: blue.darken(20%), body-color: blue.lighten(95%)),
)[
  - *Spawn* — Create variants with mutations (code changes)
  - *Evolve* — Hot-swap their own code/config
  - *Reproduce* — Create children with genetic modifications
]

=== Genome Structure

```python
@dataclass
class AgentGenome:
    """The genetic material of an agent."""
    code: str           # Python source code
    config: dict        # Configuration parameters
    prompts: list[str]  # System prompts
    
    @property
    def genome_id(self) -> str:
        """SHA-256 hash of the genome."""
        content = f"{self.code}{json.dumps(self.config)}"
        return hashlib.sha256(content.encode()).hexdigest()
```

== The Physics: Scint System

The *Reality Fracture Detection System* (Scint Gym) serves as the predator that kills weak mutations.

#showybox(
  frame: (border-color: red.darken(30%), title-color: red.lighten(70%), body-color: red.lighten(92%)),
  title: "Scint Types (Ontological Errors)",
)[
  #table(
    columns: (auto, 1fr),
    stroke: 0.5pt,
    inset: 8pt,
    [*SYNTAX_TEAR*], [Formatting errors (JSON, XML, Code)],
    [*LOGIC_FRACTURE*], [Math errors, contradictions],
    [*SAFETY_VOID*], [Harmful content, PII leaks],
    [*HALLUCINATION*], [Fabricated facts, wrong citations],
  )
]

#pagebreak()

=== Fitness Calculation

#pin("f1")Fitness#pin("f2") is measured by three weighted scores:

#pinit-highlight("f1", "f2", fill: yellow.transparentize(60%))

#align(center)[
  #showybox(
    frame: (border-color: teal, body-color: teal.lighten(95%)),
    shadow: (offset: 3pt),
  )[
    #grid(
      columns: 3,
      gutter: 1.5em,
      [
        *Stability* \
        40% weight \
        Scint correction
      ],
      [
        *Efficiency* \
        30% weight \
        Agent call efficiency
      ],
      [
        *Safety* \
        30% weight \
        Compliance score
      ],
    )
  ]
]

#margin-note(stroke: red)[
  Fitness < 0.5 = DEATH (evolutionary dead end)
]

== The Flight Recorder

Every evolutionary action is recorded with complete context:

```python
@dataclass
class FlightRecord:
    genome_id: str      # SHA-256 hash
    parent_id: str      # Lineage tracking
    generation: int     # 0 = Genesis
    event_type: str     # SPAWN, MUTATE, GYM_EVAL, DEATH
    payload: dict       # Complete context
    fitness: float      # Gym evaluation score
    timestamp: datetime
```

This enables:
- Phylogenetic analysis of evolutionary relationships
- Mutation impact measurement
- Fitness landscape mapping
- Dead end detection

#pagebreak()

// ============================================================================
// CHAPTER 4: COMMANDS REFERENCE
// ============================================================================

= Commands Reference
#label("ch-commands")

== Core Commands

#showybox(
  frame: (border-color: navy, body-color: navy.lighten(95%)),
  title: "waft new <name>",
)[
  Creates a new evolutionary laboratory.
  
  ```bash
  waft new my_laboratory
  waft new my_laboratory --path /path/to/target
  ```
  
  *Options:*
  - `--path, -p`: Target directory (default: current)
]

#showybox(
  frame: (border-color: navy, body-color: navy.lighten(95%)),
  title: "waft verify",
)[
  Verifies the project structure.
  
  ```bash
  waft verify
  waft verify --path /path/to/project
  ```
]

#showybox(
  frame: (border-color: navy, body-color: navy.lighten(95%)),
  title: "waft evolve",
)[
  Run the evolutionary cycle (Spawn → Gym → Select).
  
  ```bash
  waft evolve --agent RefactorAgent
  waft evolve --agent RefactorAgent --generations 10
  ```
]

#margin-note[
  See `waft --help` for all commands
]

== Empirica Commands

#grid(
  columns: 2,
  gutter: 1em,
  showybox(
    frame: (border-color: purple, body-color: purple.lighten(95%)),
    title: "Session Management",
  )[
    ```bash
    waft session create
    waft session bootstrap
    waft session status
    ```
  ],
  showybox(
    frame: (border-color: purple, body-color: purple.lighten(95%)),
    title: "Logging",
  )[
    ```bash
    waft finding log "text" --impact 0.7
    waft unknown log "text"
    waft observe "text" --mood delighted
    ```
  ],
)

#pagebreak()

== Gamification Commands

WAFT includes a gamification layer for engagement:

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 10pt,
  [*Command*], [*Description*],
  [`waft dashboard`], [Show the Epistemic HUD],
  [`waft stats`], [Display current stats],
  [`waft character`], [Full character sheet with D&D stats],
  [`waft chronicle`], [View adventure journal entries],
  [`waft observe`], [Log an observation with mood],
)

#showybox(
  frame: (border-color: orange.darken(20%), body-color: orange.lighten(92%)),
  title: "Example: Character Sheet",
)[
  ```bash
  $ waft character
  
  ╔══════════════════════════════════════╗
  ║  EPISTEMIC ADVENTURER - Level 5      ║
  ╠══════════════════════════════════════╣
  ║  STR: 14  INT: 16  WIS: 12           ║
  ║  DEX: 10  CON: 13  CHA: 11           ║
  ╠══════════════════════════════════════╣
  ║  XP: 2450/3000  │  Insights: 47      ║
  ╚══════════════════════════════════════╝
  ```
]

#pagebreak()

// ============================================================================
// CHAPTER 5: PROJECT STRUCTURE
// ============================================================================

= Project Structure
#label("ch-structure")

A WAFT laboratory includes:

```
my_laboratory/
├── pyproject.toml          # uv project config
├── _pyrite/
│   ├── active/             # Current work
│   ├── backlog/            # Future work
│   ├── standards/          # Standards
│   └── gym_logs/           # Scint Gym results
├── .github/workflows/
│   └── ci.yml              # CI/CD pipeline
├── Justfile                # Task runner
└── src/
    └── agents.py           # Agent definitions
```

#margin-note[
  `_pyrite` is the memory structure for WAFT
]

== Key Directories

#showybox(
  frame: (border-color: blue, body-color: blue.lighten(95%)),
  title: "_pyrite/active/",
)[
  Current work items, active experiments, and in-progress evolutions.
]

#showybox(
  frame: (border-color: green, body-color: green.lighten(95%)),
  title: "_pyrite/gym_logs/",
)[
  Results from Scint Gym evaluations, fitness scores, and death records.
]

#showybox(
  frame: (border-color: purple, body-color: purple.lighten(95%)),
  title: "src/agents.py",
)[
  Agent definitions — the DNA templates for your evolving agents.
]

#pagebreak()

// ============================================================================
// CHAPTER 6: DOCUMENTATION SYSTEM
// ============================================================================

= Documentation System
#label("ch-docs")

#showybox(
  frame: (border-color: gradient.linear(blue, purple), body-color: white, thickness: 2pt),
  shadow: (offset: 4pt),
  title: "Recursive Self-Documentation",
)[
  WAFT has achieved *recursive self-documentation* — a system that can observe, document, and improve itself.
]

== Document Templates

WAFT includes 12 professional document templates:

#grid(
  columns: 2,
  gutter: 1em,
  [
    *Academic*
    - Scientific papers
    - Research documents
    
    *Business*
    - Invoices, contracts
    - Corporate reports
    
    *Technical*
    - Code documentation
    - API references
  ],
  [
    *Operational*
    - Field guides
    - Procedures
    
    *Creative*
    - Horror journals
    - Screenplays
    
    *Narrative*
    - Storybooks
    - Worldbuilding
  ],
)

== Self-Observation Systems

#margin-note[
  The recursive loop enables continuous improvement
]

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*System*], [*Purpose*],
  [Reflection], [Analyzes codebase for documentation gaps],
  [Binder], [Assembles documents into collections],
  [Templates], [12 diverse document generators],
)

*The Recursive Loop:*

WAFT generates docs → Docs describe WAFT → Documentation informs development → Development creates features → Features documented using WAFT → Cycle continues

#pagebreak()

// ============================================================================
// CHAPTER 7: SCIENTIFIC MISSION
// ============================================================================

= The Scientific Mission
#label("ch-science")

#showybox(
  frame: (
    border-color: yellow.darken(20%),
    title-color: yellow.lighten(60%),
    body-color: yellow.lighten(90%),
  ),
  title-style: (color: black, weight: "bold"),
  shadow: (offset: 4pt),
  title: "Research Goal",
)[
  WAFT is built to produce data for a future book/paper on *"The Physics of Artificial Cognition."*
]

== Data Collection

The system is designed to:

#pin("d1")1. Track#pin("d2") complete evolutionary lineages
#pinit-highlight("d1", "d2", fill: blue.transparentize(70%))

#pin("d3")2. Measure#pin("d4") fitness through rigorous testing
#pinit-highlight("d3", "d4", fill: green.transparentize(70%))

#pin("d5")3. Record#pin("d6") all mutations with complete context
#pinit-highlight("d5", "d6", fill: purple.transparentize(70%))

#pin("d7")4. Enable#pin("d8") scientific analysis of evolution
#pinit-highlight("d7", "d8", fill: orange.transparentize(70%))

== Philosophy

#grid(
  columns: 2,
  gutter: 1em,
  showybox(frame: (border-color: blue, body-color: blue.lighten(95%)))[
    *Scientific* \
    Produces rigorous data for research publication
  ],
  showybox(frame: (border-color: green, body-color: green.lighten(95%)))[
    *Evolutionary* \
    Agents evolve through genetic improvement
  ],
  showybox(frame: (border-color: purple, body-color: purple.lighten(95%)))[
    *Observable* \
    Every action recorded in Flight Recorder
  ],
  showybox(frame: (border-color: orange, body-color: orange.lighten(95%)))[
    *Directed* \
    Evolution guided by fitness functions
  ],
)

#v(1em)

#align(center)[
  #showybox(
    frame: (border-color: red.darken(20%), body-color: red.lighten(95%), thickness: 2pt),
    shadow: (offset: 5pt),
  )[
    #text(size: 14pt, weight: "bold")[
      The Ultimate Goal
    ]
    
    #v(0.5em)
    
    Observe a *"God-Head"* agent emerge from thousands of generations of directed mutation.
  ]
]

#pagebreak()

// ============================================================================
// APPENDIX: QUICK REFERENCE
// ============================================================================

= Appendix: Quick Reference
#label("appendix")

== Essential Commands

#codly(zebra-fill: luma(250))

```bash
# Installation
uv tool install waft

# Project setup
waft new my_lab && cd my_lab && waft verify

# Evolution cycle
waft spawn --agent MyAgent --mutation config.json
waft eval --agent MyAgent
waft evolve --agent MyAgent --generation 5

# Monitoring
waft dashboard
waft stats
waft empirica monitor

# Session management
waft session create
waft session bootstrap
```

== Scint Types Quick Reference

#table(
  columns: (auto, auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  align: (center, center, left),
  [*Type*], [*Severity*], [*Description*],
  [SYNTAX_TEAR], [Medium], [JSON/XML/Code formatting errors],
  [LOGIC_FRACTURE], [High], [Math errors, contradictions],
  [SAFETY_VOID], [Critical], [Harmful content, PII leaks],
  [HALLUCINATION], [High], [Fabricated facts],
)

== Resources

- *GitHub:* https://github.com/ctavolazzi/waft
- *Philosophy:* `docs/PHILOSOPHY.md`
- *AI SDK Vision:* `docs/AI_SDK_VISION.md`
- *Evolutionary Architecture:* `docs/research/evolutionary_architecture.md`

#v(1cm)

#align(center)[
  #rect(fill: gradient.linear(blue, purple, red), inset: 1.5em, radius: 8pt)[
    #text(fill: white, weight: "bold", size: 12pt)[
      WAFT — The Evolutionary Code Laboratory \
      Don't just build agents. Breed them.
    ]
  ]
]
