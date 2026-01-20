// WAFT DATA FLOW
// How Information Moves Through the System

#import "@preview/showybox:2.0.4": showybox
#import "@preview/fletcher:0.5.7" as fletcher: diagram, node, edge

#set document(title: "WAFT Data Flow", author: "WAFT Architecture Team")
#set page(paper: "us-letter", margin: 0.75in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#2c5282")

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(20%)), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[DATA FLOW ARCHITECTURE]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[How Information Moves Through WAFT]
  ]
]

#v(1em)

= Evolution Data Flow

#align(center)[
  #diagram(
    node-stroke: 1pt,
    edge-stroke: 1pt,
    spacing: 2em,
    // Top row - input
    node((0, 0), [*User Command*], shape: rect, fill: blue.lighten(80%)),
    // Second row - processing
    node((0, 1), [*CLI Parser*], shape: rect, fill: green.lighten(80%)),
    // Third row - core
    node((-1, 2), [*Evolution\ Engine*], shape: rect, fill: orange.lighten(80%)),
    node((1, 2), [*Scint Gym*], shape: rect, fill: orange.lighten(80%)),
    // Fourth row - data
    node((-1, 3), [*Genome\ Manager*], shape: rect, fill: purple.lighten(80%)),
    node((0, 3), [*Flight\ Recorder*], shape: rect, fill: purple.lighten(80%)),
    node((1, 3), [*Fitness\ Scorer*], shape: rect, fill: purple.lighten(80%)),
    // Bottom - storage
    node((0, 4), [*Storage Layer*], shape: rect, fill: gray.lighten(50%)),
    // Edges
    edge((0, 0), (0, 1), "->"),
    edge((0, 1), (-1, 2), "->"),
    edge((0, 1), (1, 2), "->"),
    edge((-1, 2), (-1, 3), "<->"),
    edge((-1, 2), (0, 3), "->"),
    edge((1, 2), (1, 3), "<->"),
    edge((1, 2), (0, 3), "->"),
    edge((-1, 3), (0, 4), "<->"),
    edge((0, 3), (0, 4), "<->"),
    edge((1, 3), (0, 4), "<->"),
    // Cross connections
    edge((-1, 2), (1, 2), "<->", label: [evaluate]),
  )
]

= Being Lifecycle Data Flow

#align(center)[
  #diagram(
    node-stroke: 1pt,
    spacing: 1.5em,
    // Row 1
    node((0, 0), [*Spawn\ Request*], fill: blue.lighten(80%)),
    node((2, 0), [*Being\ System*], fill: green.lighten(80%)),
    // Row 2
    node((0, 1), [*Reality\ Context*], fill: orange.lighten(80%)),
    node((2, 1), [*New Being*], fill: purple.lighten(80%)),
    // Row 3
    node((1, 2), [*Skills*], fill: yellow.lighten(80%)),
    node((2, 2), [*Memories*], fill: yellow.lighten(80%)),
    node((3, 2), [*Goals*], fill: yellow.lighten(80%)),
    // Row 4
    node((2, 3), [*Persistence*], fill: gray.lighten(50%)),
    // Edges
    edge((0, 0), (2, 0), "->"),
    edge((0, 1), (2, 0), "->"),
    edge((2, 0), (2, 1), "->"),
    edge((2, 1), (1, 2), "->"),
    edge((2, 1), (2, 2), "->"),
    edge((2, 1), (3, 2), "->"),
    edge((1, 2), (2, 3), "->"),
    edge((2, 2), (2, 3), "->"),
    edge((3, 2), (2, 3), "->"),
  )
]

#pagebreak()

= Corporation Simulation Flow

#showybox(
  frame: (border-color: primary, body-color: primary.lighten(95%)),
  title: "Economic Simulation Cycle",
)[
  #align(center)[
    #diagram(
      node-stroke: 1pt,
      spacing: 1.8em,
      node((0, 0), [*Time\ Advance*], fill: blue.lighten(80%)),
      node((1, 0), [*Process\ Expenses*], fill: red.lighten(80%)),
      node((2, 0), [*Add\ Revenue*], fill: green.lighten(80%)),
      node((3, 0), [*Update\ Balance*], fill: purple.lighten(80%)),
      node((4, 0), [*Log\ Transaction*], fill: orange.lighten(80%)),
      edge((0, 0), (1, 0), "->"),
      edge((1, 0), (2, 0), "->"),
      edge((2, 0), (3, 0), "->"),
      edge((3, 0), (4, 0), "->"),
    )
  ]
]

= Document Generation Flow

#align(center)[
  #diagram(
    node-stroke: 1pt,
    spacing: 2em,
    node((0, 0), [*Data Source*], fill: blue.lighten(80%)),
    node((1, 0), [*Template*], fill: green.lighten(80%)),
    node((2, 0), [*Chronicler*], fill: orange.lighten(80%)),
    node((3, 0), [*Typst/HTML*], fill: purple.lighten(80%)),
    node((4, 0), [*PDF Output*], fill: red.lighten(80%)),
    edge((0, 0), (2, 0), "->"),
    edge((1, 0), (2, 0), "->"),
    edge((2, 0), (3, 0), "->"),
    edge((3, 0), (4, 0), "->"),
  )
]

= Scint Detection Flow

#grid(
  columns: 2,
  gutter: 2em,
  [
    #align(center)[
      #diagram(
        node-stroke: 1pt,
        spacing: 1.5em,
        node((0, 0), [*Agent Output*], fill: blue.lighten(80%)),
        node((0, 1), [*Pattern\ Matcher*], fill: green.lighten(80%)),
        node((0, 2), [*Scint\ Classifier*], fill: orange.lighten(80%)),
        node((0, 3), [*Severity\ Calculator*], fill: red.lighten(80%)),
        node((0, 4), [*Fitness\ Impact*], fill: purple.lighten(80%)),
        edge((0, 0), (0, 1), "->"),
        edge((0, 1), (0, 2), "->"),
        edge((0, 2), (0, 3), "->"),
        edge((0, 3), (0, 4), "->"),
      )
    ]
  ],
  [
    == Detection Steps
    
    1. *Agent Output* — Raw response from agent
    
    2. *Pattern Matcher* — Regex patterns identify issues
    
    3. *Scint Classifier* — Categorize into types:
       - SYNTAX_TEAR
       - LOGIC_FRACTURE
       - SAFETY_VOID
       - HALLUCINATION
    
    4. *Severity Calculator* — Compute impact score
    
    5. *Fitness Impact* — Adjust agent fitness
  ],
)

= Empirica Session Flow

#showybox(
  frame: (border-color: green, body-color: green.lighten(95%)),
)[
  #align(center)[
    #diagram(
      node-stroke: 1pt,
      spacing: 1.5em,
      node((0, 0), [*Session\ Create*], fill: blue.lighten(80%)),
      node((1, 0), [*Preflight*], fill: green.lighten(80%)),
      node((2, 0), [*Work*], fill: orange.lighten(80%)),
      node((3, 0), [*Postflight*], fill: purple.lighten(80%)),
      node((4, 0), [*Analysis*], fill: red.lighten(80%)),
      edge((0, 0), (1, 0), "->"),
      edge((1, 0), (2, 0), "->"),
      edge((2, 0), (3, 0), "->"),
      edge((3, 0), (4, 0), "->"),
    )
    
    #v(0.5em)
    
    *Vectors measured:* engagement, know, do, context, clarity, coherence, signal, density, state, change, completion, impact, uncertainty
  ]
]

#pagebreak()

= API Request Flow

#align(center)[
  #diagram(
    node-stroke: 1pt,
    spacing: 2em,
    // Client
    node((0, 0), [*HTTP\ Request*], fill: blue.lighten(80%)),
    // API Layer
    node((1, 0), [*FastAPI\ Router*], fill: green.lighten(80%)),
    node((1, 1), [*Auth\ Middleware*], fill: orange.lighten(80%)),
    // Service Layer
    node((2, 0), [*Service\ Layer*], fill: purple.lighten(80%)),
    // Core
    node((3, 0), [*Core\ Module*], fill: red.lighten(80%)),
    // Storage
    node((4, 0), [*Storage*], fill: gray.lighten(50%)),
    // Response
    node((5, 0), [*JSON\ Response*], fill: blue.lighten(80%)),
    // Edges
    edge((0, 0), (1, 0), "->"),
    edge((1, 0), (1, 1), "<->"),
    edge((1, 0), (2, 0), "->"),
    edge((2, 0), (3, 0), "->"),
    edge((3, 0), (4, 0), "<->"),
    edge((3, 0), (2, 0), "<-"),
    edge((2, 0), (5, 0), "->"),
  )
]

= Flight Recorder Event Flow

#table(
  columns: (auto, auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  fill: (x, y) => if y == 0 { luma(230) } else { white },
  [*Source*], [*Event Type*], [*Data Captured*],
  [Evolution Engine], [SPAWN], [genome_id, generation, parent_id],
  [Evolution Engine], [MUTATE], [genome_id, mutation_type, changes],
  [Scint Gym], [GYM_EVAL], [genome_id, fitness, scints_detected],
  [Selection], [BREED], [parent_ids, offspring_id],
  [Selection], [DEATH], [genome_id, reason, final_fitness],
  [Checkpoint], [CHECKPOINT], [generation, population_state],
  [Detection], [EMERGENCE], [genome_id, signals, criteria_met],
)

= Data Persistence Flow

#align(center)[
  #diagram(
    node-stroke: 1pt,
    spacing: 2em,
    node((0, 0), [*In-Memory\ State*], fill: blue.lighten(80%)),
    node((1, 0), [*Serializer*], fill: green.lighten(80%)),
    node((2, -0.5), [*JSON Files*], fill: orange.lighten(80%)),
    node((2, 0.5), [*SQLite DB*], fill: purple.lighten(80%)),
    node((3, 0), [*File System*], fill: gray.lighten(50%)),
    edge((0, 0), (1, 0), "->"),
    edge((1, 0), (2, -0.5), "->"),
    edge((1, 0), (2, 0.5), "->"),
    edge((2, -0.5), (3, 0), "->"),
    edge((2, 0.5), (3, 0), "->"),
  )
]

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white, size: 10pt)[
      DATA FLOW ARCHITECTURE | Every Path, Every Transaction
    ]
  ]
]
