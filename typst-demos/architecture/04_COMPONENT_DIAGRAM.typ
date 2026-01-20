// WAFT COMPONENT DIAGRAM
// Module Relationships

#import "@preview/showybox:2.0.4": showybox
#import "@preview/fletcher:0.5.7" as fletcher: diagram, node, edge

#set document(title: "WAFT Components", author: "WAFT Architecture Team")
#set page(paper: "us-letter", margin: 0.5in)
#set text(font: "New Computer Modern", size: 9pt)

#let primary = rgb("#2f855a")

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(20%)), width: 100%, inset: 1.5em)[
    #text(fill: white, size: 22pt, weight: "bold")[COMPONENT DIAGRAM]
    #v(0.2em)
    #text(fill: white.darken(10%), size: 11pt)[Module Relationships & Dependencies]
  ]
]

#v(0.5em)

= Core Module Relationships

#align(center)[
  #diagram(
    node-stroke: 1pt,
    edge-stroke: 0.8pt,
    spacing: 1.5em,
    // Top level - Entry points
    node((2, 0), [*CLI*\ `main.py`], shape: rect, fill: blue.lighten(80%)),
    node((4, 0), [*API*\ `api/`], shape: rect, fill: blue.lighten(80%)),
    
    // Second level - Core services
    node((0, 1), [*Being*\ System], shape: rect, fill: green.lighten(80%)),
    node((2, 1), [*Evolution*\ Engine], shape: rect, fill: green.lighten(80%)),
    node((4, 1), [*Chronicler*], shape: rect, fill: green.lighten(80%)),
    node((6, 1), [*Empirica*], shape: rect, fill: green.lighten(80%)),
    
    // Third level - Domain modules
    node((0, 2), [*Reality*], shape: rect, fill: orange.lighten(80%)),
    node((1.5, 2), [*Corporation*], shape: rect, fill: orange.lighten(80%)),
    node((3, 2), [*Scint*\ Detector], shape: rect, fill: orange.lighten(80%)),
    node((4.5, 2), [*Templates*], shape: rect, fill: orange.lighten(80%)),
    node((6, 2), [*Gamification*], shape: rect, fill: orange.lighten(80%)),
    
    // Fourth level - Infrastructure
    node((1, 3), [*Memory*], shape: rect, fill: purple.lighten(80%)),
    node((2.5, 3), [*Flight\ Recorder*], shape: rect, fill: purple.lighten(80%)),
    node((4, 3), [*Persistence*], shape: rect, fill: purple.lighten(80%)),
    node((5.5, 3), [*Karma*], shape: rect, fill: purple.lighten(80%)),
    
    // Bottom - Storage
    node((3, 4), [*Storage Layer*\ JSON + SQLite], shape: rect, fill: gray.lighten(50%)),
    
    // Edges - CLI connections
    edge((2, 0), (0, 1), "->"),
    edge((2, 0), (2, 1), "->"),
    edge((2, 0), (4, 1), "->"),
    edge((2, 0), (6, 1), "->"),
    
    // Edges - API connections
    edge((4, 0), (0, 1), "->"),
    edge((4, 0), (2, 1), "->"),
    edge((4, 0), (4, 1), "->"),
    
    // Edges - Service to domain
    edge((0, 1), (0, 2), "->"),
    edge((0, 1), (1.5, 2), "->"),
    edge((2, 1), (3, 2), "->"),
    edge((4, 1), (4.5, 2), "->"),
    edge((6, 1), (6, 2), "->"),
    
    // Edges - Domain to infra
    edge((0, 2), (1, 3), "->"),
    edge((1.5, 2), (4, 3), "->"),
    edge((3, 2), (2.5, 3), "->"),
    edge((6, 2), (5.5, 3), "->"),
    
    // Edges - Infra to storage
    edge((1, 3), (3, 4), "->"),
    edge((2.5, 3), (3, 4), "->"),
    edge((4, 3), (3, 4), "->"),
    edge((5.5, 3), (3, 4), "->"),
    
    // Cross connections
    edge((2, 1), (0, 1), "<->", bend: 20deg),
    edge((4, 1), (4.5, 2), "->"),
    edge((6, 1), (5.5, 3), "->"),
  )
]

#pagebreak()

= Module Dependency Matrix

#table(
  columns: (auto, 1fr, 1fr, 1fr, 1fr, 1fr),
  stroke: 0.5pt,
  inset: 6pt,
  fill: (x, y) => if y == 0 or x == 0 { luma(230) } else { white },
  [], [*Being*], [*Corp*], [*Evol*], [*Chron*], [*Empirica*],
  [*Being*], [—], [uses], [uses], [], [],
  [*Corporation*], [refs], [—], [], [uses], [],
  [*Evolution*], [evals], [], [—], [logs], [tracks],
  [*Chronicler*], [reads], [reads], [reads], [—], [],
  [*Empirica*], [], [], [informs], [], [—],
)

= Pantheon (Entity Gods)

#grid(
  columns: 3,
  gutter: 0.8em,
  showybox(frame: (border-color: blue, body-color: blue.lighten(92%)), title: "Bureaucracy God")[
    Corporate documentation, forms, procedures
  ],
  showybox(frame: (border-color: green, body-color: green.lighten(92%)), title: "GitHub God")[
    Repository management, version control
  ],
  showybox(frame: (border-color: orange, body-color: orange.lighten(92%)), title: "Paperwork God")[
    Document generation, templates
  ],
  showybox(frame: (border-color: purple, body-color: purple.lighten(92%)), title: "Storyteller")[
    Narrative generation, lore
  ],
  showybox(frame: (border-color: red, body-color: red.lighten(92%)), title: "Judge")[
    Evaluation, assessment
  ],
  showybox(frame: (border-color: teal, body-color: teal.lighten(92%)), title: "Librarian")[
    Knowledge organization, retrieval
  ],
)

= Template System

#align(center)[
  #diagram(
    node-stroke: 1pt,
    spacing: 1.5em,
    node((0, 0), [*Template\ Registry*], fill: blue.lighten(80%)),
    node((-1, 1), [*Typst*], fill: green.lighten(80%)),
    node((0, 1), [*HTML*], fill: orange.lighten(80%)),
    node((1, 1), [*LaTeX*], fill: purple.lighten(80%)),
    node((-1, 2), [*50+ templates*], fill: green.lighten(90%)),
    node((0, 2), [*20+ templates*], fill: orange.lighten(90%)),
    node((1, 2), [*10+ templates*], fill: purple.lighten(90%)),
    edge((0, 0), (-1, 1), "->"),
    edge((0, 0), (0, 1), "->"),
    edge((0, 0), (1, 1), "->"),
    edge((-1, 1), (-1, 2), "->"),
    edge((0, 1), (0, 2), "->"),
    edge((1, 1), (1, 2), "->"),
  )
]

= Science Module

#align(center)[
  #diagram(
    node-stroke: 1pt,
    spacing: 1.5em,
    node((0, 0), [*Science\ System*], fill: blue.lighten(80%)),
    node((-1.5, 1), [*Oracle*], fill: orange.lighten(80%)),
    node((-0.5, 1), [*Observer*], fill: orange.lighten(80%)),
    node((0.5, 1), [*Notebook*], fill: orange.lighten(80%)),
    node((1.5, 1), [*Report*], fill: orange.lighten(80%)),
    node((0, 2), [*Lab Entry*], fill: purple.lighten(80%)),
    edge((0, 0), (-1.5, 1), "->"),
    edge((0, 0), (-0.5, 1), "->"),
    edge((0, 0), (0.5, 1), "->"),
    edge((0, 0), (1.5, 1), "->"),
    edge((-1.5, 1), (0, 2), "->"),
    edge((-0.5, 1), (0, 2), "->"),
    edge((0.5, 1), (0, 2), "->"),
    edge((1.5, 1), (0, 2), "->"),
  )
]

= Self-Engineering Module

The self-modification system for continuous improvement:

#align(center)[
  #diagram(
    node-stroke: 1pt,
    spacing: 1.5em,
    node((0, 0), [*Problem\ Detector*], fill: red.lighten(80%)),
    node((1, 0), [*Diagnostician*], fill: orange.lighten(80%)),
    node((2, 0), [*Solution\ Engineer*], fill: green.lighten(80%)),
    node((3, 0), [*Self\ Modification*], fill: blue.lighten(80%)),
    node((1.5, 1), [*Iteration Loop*], fill: purple.lighten(80%)),
    edge((0, 0), (1, 0), "->"),
    edge((1, 0), (2, 0), "->"),
    edge((2, 0), (3, 0), "->"),
    edge((3, 0), (1.5, 1), "->"),
    edge((1.5, 1), (0, 0), "->", bend: -30deg),
  )
]

#pagebreak()

= Full Module Map

#table(
  columns: (auto, auto, 1fr),
  stroke: 0.5pt,
  inset: 6pt,
  fill: (x, y) => if y == 0 { luma(230) } else { white },
  [*Package*], [*Modules*], [*Purpose*],
  [`core/`], [169], [Business logic, domain models],
  [`core/agent/`], [6], [Agent anatomy and state],
  [`core/chronicler/`], [6], [Documentation generation],
  [`core/corporations/`], [12], [Economic simulation],
  [`core/dnd_scenario/`], [11], [RPG scenario generation],
  [`core/dnd5e/`], [6], [D&D 5e mechanics],
  [`core/hub/`], [5], [Central coordination],
  [`core/science/`], [12], [Research framework],
  [`core/self_engineering/`], [9], [Self-modification],
  [`core/tavern_keeper/`], [5], [NPC management],
  [`core/tracing/`], [7], [Observability],
  [`evolution/`], [28], [Evolutionary algorithms],
  [`pantheon/`], [18], [Entity gods],
  [`templates/`], [51], [Document templates],
  [`api/`], [22], [REST endpoints],
  [`ui/`], [13], [Dashboards and visualizations],
)

= Interface Contracts

#showybox(
  frame: (border-color: primary, body-color: primary.lighten(95%)),
  title: "Key Interfaces",
)[
  ```python
  # Every major component implements these patterns:
  
  class Persistable(Protocol):
      def to_dict(self) -> dict: ...
      def from_dict(cls, data: dict) -> Self: ...
      def save(self, path: Path) -> None: ...
      def load(cls, path: Path) -> Self: ...
  
  class Evolvable(Protocol):
      def fitness(self) -> float: ...
      def mutate(self) -> Self: ...
      def crossover(self, other: Self) -> Self: ...
  
  class Observable(Protocol):
      def subscribe(self, observer: Observer) -> None: ...
      def notify(self, event: Event) -> None: ...
  ```
]

#v(0.5em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white, size: 10pt)[
      COMPONENT DIAGRAM | 443+ Modules, One Vision
    ]
  ]
]
