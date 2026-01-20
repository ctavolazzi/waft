// WAFT SUMMARY POSTER
// One-Page Overview

#import "@preview/showybox:2.0.4": showybox
#import "@preview/fletcher:0.5.7" as fletcher: diagram, node, edge

#set document(title: "WAFT Summary", author: "WAFT Team")
#set page(paper: "us-letter", margin: 0.5in)
#set text(font: "New Computer Modern", size: 8pt)

#let primary = rgb("#1a365d")

#align(center)[
  #rect(fill: gradient.linear(rgb("#667eea"), rgb("#764ba2")), width: 100%, inset: 1.5em)[
    #text(fill: white, size: 28pt, weight: "bold")[WAFT]
    #h(0.5em)
    #text(fill: white.darken(10%), size: 14pt)[Worldbuilding & AI Framework for Teleport]
    #v(0.2em)
    #text(fill: white.darken(20%), size: 10pt, style: "italic")["Don't just build agents. Breed them."]
  ]
]

#v(0.3em)

#grid(
  columns: 3,
  gutter: 0.8em,
  // Column 1
  [
    == What is WAFT?
    
    A Python framework for:
    - *Evolutionary AI* — Breed agents
    - *Worldbuilding* — Simulate realities
    - *Documents* — Generate PDFs
    - *Research* — Track knowledge
    
    == Core Architecture
    
    #align(center)[
      #diagram(
        node-stroke: 0.8pt,
        spacing: 1em,
        node((0, 0), [CLI], fill: blue.lighten(85%)),
        node((0, 1), [Core], fill: green.lighten(85%)),
        node((0, 2), [Storage], fill: purple.lighten(85%)),
        edge((0, 0), (0, 1), "->"),
        edge((0, 1), (0, 2), "->"),
      )
    ]
    
    == Key Numbers
    
    #table(
      columns: (1fr, auto),
      stroke: 0.5pt,
      inset: 4pt,
      [Python Modules], [443+],
      [Classes], [285],
      [Templates], [80+],
      [CLI Commands], [20+],
    )
    
    == Storage
    
    - *JSON* — Beings, Corporations
    - *SQLite* — Flight Recorder
    - *Files* — Checkpoints, Seeds
  ],
  // Column 2
  [
    == Beings System
    
    Timeful agents with:
    - Skills (0-10)
    - Memories
    - Personality
    - Goals
    - Fitness
    
    States: SPAWNING → LEARNING → EVOLVING → COMPLETING
    
    == Evolution Engine
    
    #align(center)[
      #diagram(
        node-stroke: 0.8pt,
        spacing: 0.8em,
        node((0, 0), [Spawn], fill: blue.lighten(85%)),
        node((1, 0), [Eval], fill: green.lighten(85%)),
        node((2, 0), [Select], fill: orange.lighten(85%)),
        node((1, 1), [Mutate], fill: red.lighten(85%)),
        edge((0, 0), (1, 0), "->"),
        edge((1, 0), (2, 0), "->"),
        edge((2, 0), (1, 1), "->"),
        edge((1, 1), (1, 0), "->"),
      )
    ]
    
    == Scint Types
    
    #table(
      columns: (1fr, auto),
      stroke: 0.5pt,
      inset: 3pt,
      [SYNTAX_TEAR], [0.3],
      [LOGIC_FRACTURE], [0.5],
      [HALLUCINATION], [0.6],
      [SAFETY_VOID], [0.9],
    )
    
    == Corporation Sim
    
    - Departments
    - Employees (Beings)
    - Financial tracking
    - Time simulation
  ],
  // Column 3
  [
    == Templates
    
    #grid(
      columns: 2,
      gutter: 0.3em,
      [- Typst (50+)], [- HTML (20+)],
      [- Reports], [- Briefs],
      [- Memos], [- Invoices],
    )
    
    == Empirica
    
    13 epistemic vectors:
    - Foundation (4)
    - Comprehension (4)
    - Execution (4)
    - Uncertainty (1)
    
    == Gamification
    
    - XP & Levels
    - Karma system
    - Character stats
    - Achievement tracking
    
    == Quick Start
    
    ```bash
    uv tool install waft
    waft new my_lab
    waft evolve --gen 10
    waft dashboard
    ```
    
    == Links
    
    GitHub: github.com/ctavolazzi/waft
  ],
)

#v(0.3em)

#line(length: 100%, stroke: 0.5pt)

#v(0.3em)

#grid(
  columns: 4,
  gutter: 1em,
  showybox(frame: (border-color: blue, body-color: blue.lighten(92%)), title: "Evolve")[
    Breed AI through selection + mutation
  ],
  showybox(frame: (border-color: green, body-color: green.lighten(92%)), title: "Simulate")[
    Corporations, economies, realities
  ],
  showybox(frame: (border-color: orange, body-color: orange.lighten(92%)), title: "Document")[
    PDFs, reports, briefs automatically
  ],
  showybox(frame: (border-color: purple, body-color: purple.lighten(92%)), title: "Research")[
    Track knowledge with Empirica
  ],
)

#v(0.3em)

#align(center)[
  #rect(fill: primary, width: 100%, inset: 0.8em)[
    #grid(
      columns: 5,
      gutter: 2em,
      [
        #text(fill: white, weight: "bold")[Beings]
        
        #text(fill: white.darken(20%), size: 7pt)[Timeful agents]
      ],
      [
        #text(fill: white, weight: "bold")[Corporations]
        
        #text(fill: white.darken(20%), size: 7pt)[Economic sim]
      ],
      [
        #text(fill: white, weight: "bold")[Evolution]
        
        #text(fill: white.darken(20%), size: 7pt)[Agent breeding]
      ],
      [
        #text(fill: white, weight: "bold")[Chronicler]
        
        #text(fill: white.darken(20%), size: 7pt)[Auto-docs]
      ],
      [
        #text(fill: white, weight: "bold")[Flight Recorder]
        
        #text(fill: white.darken(20%), size: 7pt)[Telemetry]
      ],
    )
  ]
]
