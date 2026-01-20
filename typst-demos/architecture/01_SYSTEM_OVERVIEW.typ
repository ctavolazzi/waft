// WAFT SYSTEM OVERVIEW
// Complete Architecture Documentation

#import "@preview/showybox:2.0.4": showybox
#import "@preview/fletcher:0.5.7" as fletcher: diagram, node, edge

#set document(title: "WAFT System Overview", author: "WAFT Architecture Team")
#set page(paper: "us-letter", margin: 0.75in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#1a365d")
#let accent = rgb("#3182ce")

#align(center)[
  #rect(fill: gradient.linear(primary, accent), width: 100%, inset: 2em)[
    #text(fill: white, size: 28pt, weight: "bold")[WAFT SYSTEM OVERVIEW]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 14pt)[Complete Architecture Documentation]
  ]
]

#v(1em)

= What is WAFT?

*WAFT* (Worldbuilding & AI Framework for Teleport) is a comprehensive Python framework for:

#grid(
  columns: 3,
  gutter: 1em,
  showybox(frame: (border-color: blue, body-color: blue.lighten(95%)), title: "Evolutionary AI")[
    Breed AI agents through directed mutation and selection
  ],
  showybox(frame: (border-color: green, body-color: green.lighten(95%)), title: "Worldbuilding")[
    Create and simulate corporations, beings, and realities
  ],
  showybox(frame: (border-color: purple, body-color: purple.lighten(95%)), title: "Documentation")[
    Generate professional PDFs, reports, and templates
  ],
)

= High-Level Architecture

#align(center)[
  #diagram(
    node-stroke: 1pt,
    edge-stroke: 1pt,
    spacing: 2em,
    node((0, 0), [*CLI Layer*], shape: rect, fill: blue.lighten(80%)),
    node((0, 1), [*Core Services*], shape: rect, fill: green.lighten(80%)),
    node((-1, 2), [*Beings*], shape: rect, fill: orange.lighten(80%)),
    node((0, 2), [*Corporations*], shape: rect, fill: orange.lighten(80%)),
    node((1, 2), [*Evolution*], shape: rect, fill: orange.lighten(80%)),
    node((0, 3), [*Storage Layer*], shape: rect, fill: purple.lighten(80%)),
    edge((0, 0), (0, 1), "->"),
    edge((0, 1), (-1, 2), "->"),
    edge((0, 1), (0, 2), "->"),
    edge((0, 1), (1, 2), "->"),
    edge((-1, 2), (0, 3), "->"),
    edge((0, 2), (0, 3), "->"),
    edge((1, 2), (0, 3), "->"),
  )
]

= Core Components

== 1. CLI Layer (`src/waft/cli/`)

Command-line interface for all WAFT operations:
- `waft new` — Create laboratories
- `waft evolve` — Run evolution cycles
- `waft spawn` — Create beings/agents
- `waft status` — Check system state

== 2. Core Services (`src/waft/core/`)

The heart of WAFT with 169 Python modules:

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*Module*], [*Purpose*],
  [`being.py`], [Timeful agents with skills, memories, goals],
  [`corporations/`], [Corporate simulation (Teleport Massive)],
  [`evolution/`], [Agent breeding and mutation],
  [`chronicler/`], [Automated documentation generation],
  [`empirica.py`], [Epistemic self-assessment],
  [`science/`], [Research and observation framework],
)

#pagebreak()

== 3. Beings System (`src/waft/being.py`)

Beings are *timeful, dynamic entities* that exist in realities:

#showybox(
  frame: (border-color: orange, body-color: orange.lighten(95%)),
)[
  ```python
  class Being:
      being_id: str           # Unique identifier
      reality_id: str         # Which reality they exist in
      skills: dict[str, float] # Learned abilities (0-10)
      memories: list          # Experiences
      lessons: list           # What worked/didn't work
      fitness: float          # Evolutionary success
      personality: dict       # Traits
      goals: list             # Objectives
      state: BeingState       # SPAWNING, LEARNING, EVOLVING, etc.
  ```
]

=== Being States

#align(center)[
  #diagram(
    node-stroke: 1pt,
    spacing: 1.5em,
    node((0, 0), [SPAWNING], fill: blue.lighten(80%)),
    node((1, 0), [LEARNING], fill: green.lighten(80%)),
    node((2, 0), [EVOLVING], fill: orange.lighten(80%)),
    node((3, 0), [COMPLETING], fill: purple.lighten(80%)),
    node((2, 1), [DEAD], fill: red.lighten(80%)),
    node((3, 1), [ARCHIVED], fill: gray.lighten(50%)),
    edge((0, 0), (1, 0), "->"),
    edge((1, 0), (2, 0), "->"),
    edge((2, 0), (3, 0), "->"),
    edge((2, 0), (2, 1), "->", label: [fitness < 0.3]),
    edge((3, 0), (3, 1), "->"),
  )
]

== 4. Corporations System (`src/waft/core/corporations/`)

Full economic simulation:

#grid(
  columns: 2,
  gutter: 1em,
  showybox(frame: (border-color: blue))[
    *Corporation*
    - Financial state tracking
    - Department management
    - Employee (Being) roster
    - Economic transactions
  ],
  showybox(frame: (border-color: green))[
    *Simulation*
    - Time advancement
    - Monthly expenses
    - Revenue tracking
    - Runway calculation
  ],
)

== 5. Evolution System (`src/waft/evolution/`)

Directed evolution of agents:

#align(center)[
  #diagram(
    node-stroke: 1pt,
    spacing: 2em,
    node((0, 0), [*SPAWN*], fill: blue.lighten(80%)),
    node((1, 0), [*EVALUATE*], fill: green.lighten(80%)),
    node((2, 0), [*SELECT*], fill: orange.lighten(80%)),
    node((3, 0), [*BREED*], fill: purple.lighten(80%)),
    node((4, 0), [*MUTATE*], fill: red.lighten(80%)),
    edge((0, 0), (1, 0), "->"),
    edge((1, 0), (2, 0), "->"),
    edge((2, 0), (3, 0), "->"),
    edge((3, 0), (4, 0), "->"),
    edge((4, 0), (1, 0), "->", bend: 40deg),
  )
]

#pagebreak()

= Module Count by Area

#table(
  columns: (auto, auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  fill: (x, y) => if y == 0 { luma(230) } else { white },
  [*Area*], [*Files*], [*Description*],
  [`core/`], [169], [Core business logic],
  [`templates/`], [182], [Document templates + fonts],
  [`evolution/`], [30], [Evolution engine],
  [`pantheon/`], [20], [Entity gods system],
  [`api/`], [22], [REST API routes],
  [`ui/`], [13], [Dashboard and UI],
  [`ai_town/`], [7], [Multi-agent town simulation],
  [*Total*], [*443+*], [*Complete framework*],
)

= Key Integrations

#grid(
  columns: 2,
  gutter: 1em,
  showybox(frame: (border-color: blue, body-color: blue.lighten(95%)), title: "Empirica")[
    Epistemic self-assessment:
    - 13 knowledge vectors
    - Preflight/Postflight assessments
    - Gamification (XP, Karma, Levels)
  ],
  showybox(frame: (border-color: green, body-color: green.lighten(95%)), title: "Typst")[
    Document generation:
    - Professional PDFs
    - Multiple template systems
    - Automatic compilation
  ],
  showybox(frame: (border-color: orange, body-color: orange.lighten(95%)), title: "LLM")[
    AI integration:
    - OpenAI compatible
    - Local model support
    - Prompt engineering
  ],
  showybox(frame: (border-color: purple, body-color: purple.lighten(95%)), title: "D&D 5e")[
    RPG mechanics:
    - Character sheets
    - Combat system
    - Scenario generation
  ],
)

= Summary Statistics

#align(center)[
  #rect(fill: luma(248), inset: 2em, radius: 5pt)[
    #grid(
      columns: 4,
      gutter: 3em,
      [
        #text(size: 24pt, weight: "bold")[443+]
        
        Python modules
      ],
      [
        #text(size: 24pt, weight: "bold")[285]
        
        Classes defined
      ],
      [
        #text(size: 24pt, weight: "bold")[50+]
        
        Templates
      ],
      [
        #text(size: 24pt, weight: "bold")[20+]
        
        CLI commands
      ],
    )
  ]
]

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white, size: 11pt)[
      *WAFT* | Evolutionary Code Laboratory | "Don't just build agents. Breed them."
    ]
  ]
]
