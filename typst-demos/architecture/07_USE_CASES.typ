// WAFT USE CASES
// What You Can Build

#import "@preview/showybox:2.0.4": showybox
#import "@preview/fletcher:0.5.7" as fletcher: diagram, node, edge

#set document(title: "WAFT Use Cases", author: "WAFT Team")
#set page(paper: "us-letter", margin: 0.75in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#c53030")

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(20%)), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[USE CASES]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[What You Can Build with WAFT]
  ]
]

#v(1em)

= 1. Evolutionary AI Development

#showybox(
  frame: (border-color: blue, body-color: blue.lighten(95%)),
  title: "Breed Better Agents",
)[
  *Goal:* Develop AI agents that improve through evolution
  
  *How:*
  ```bash
  waft new my_ai_lab
  waft spawn --agent BaseAgent
  waft evolve --generations 100
  waft dashboard  # Monitor progress
  ```
  
  *Output:* Evolved agents with improved Scint handling, tracked lineage, and fitness metrics
]

= 2. Corporate Simulation

#showybox(
  frame: (border-color: green, body-color: green.lighten(95%)),
  title: "Simulate Business Operations",
)[
  *Goal:* Model corporations with economics, employees, and departments
  
  *How:*
  ```python
  from waft.core.corporations import CorporationsSystem
  
  corps = CorporationsSystem()
  corp = corps.create_corporation(
      name="My Startup",
      initial_capital=Decimal("1000000"),
  )
  corp.hire_employee(being_id, role="Engineer")
  simulator.advance(months=12)
  ```
  
  *Output:* Financial projections, runway analysis, organizational structure
]

= 3. Worldbuilding

#showybox(
  frame: (border-color: purple, body-color: purple.lighten(95%)),
  title: "Create Rich Fictional Universes",
)[
  *Goal:* Build detailed worlds with characters, organizations, and lore
  
  *How:*
  - Create Realms with specific physics/rules
  - Spawn Beings with personalities and goals
  - Simulate interactions and history
  - Generate documentation automatically
  
  *Output:* Complete worldbuilding documents, character profiles, timeline
]

#pagebreak()

= 4. Document Generation

#showybox(
  frame: (border-color: orange, body-color: orange.lighten(95%)),
  title: "Professional PDF Production",
)[
  *Goal:* Generate high-quality documents from data
  
  *Templates Available:*
  #grid(
    columns: 3,
    gutter: 1em,
    [- Reports], [- Briefs], [- Memos],
    [- Invoices], [- Papers], [- Manuals],
    [- Guides], [- Storybooks], [- Character Sheets],
  )
  
  *Output:* Professional PDFs via Typst, HTML, or LaTeX
]

= 5. D&D Campaign Management

#showybox(
  frame: (border-color: red, body-color: red.lighten(95%)),
  title: "Run and Track RPG Campaigns",
)[
  *Goal:* Manage D&D 5e campaigns with AI assistance
  
  *Features:*
  - Character sheet generation
  - Encounter creation
  - Lore building
  - Party state tracking
  - Quest management
  
  *Output:* Campaign materials, session notes, character documents
]

= 6. Epistemic Research

#showybox(
  frame: (border-color: teal, body-color: teal.lighten(95%)),
  title: "Track Knowledge and Learning",
)[
  *Goal:* Quantify what AI (and humans) know and learn
  
  *Empirica Features:*
  - 13 epistemic vectors
  - Preflight/Postflight assessment
  - Learning quantification
  - Gamification (XP, Karma)
  
  *Output:* Session data, learning metrics, knowledge graphs
]

#pagebreak()

= 7. Multi-Agent Simulation

#showybox(
  frame: (border-color: purple, body-color: purple.lighten(95%)),
  title: "AI Town & Agent Coordination",
)[
  *Goal:* Simulate multiple agents interacting
  
  *AI Town Features:*
  - Agent spawning and management
  - Conversation system
  - Voting mechanisms
  - Memory sharing
  
  *Output:* Agent interaction logs, emergent behaviors, town state
]

= 8. Self-Improving Systems

#showybox(
  frame: (border-color: blue, body-color: blue.lighten(95%)),
  title: "Build Systems That Fix Themselves",
)[
  *Goal:* Create systems that detect and solve their own problems
  
  *Self-Engineering Modules:*
  - Problem Detector
  - Diagnostician
  - Solution Engineer
  - Self Modification
  - Iteration Loop
  
  *Output:* Self-improving code, diagnostic reports, fix logs
]

= Use Case Decision Tree

#align(center)[
  #diagram(
    node-stroke: 1pt,
    spacing: 1.5em,
    node((2, 0), [*What do you\ want to do?*], fill: gray.lighten(70%)),
    node((0, 1), [Evolve AI], fill: blue.lighten(80%)),
    node((1.5, 1), [Simulate], fill: green.lighten(80%)),
    node((3, 1), [Generate Docs], fill: orange.lighten(80%)),
    node((4.5, 1), [Track Knowledge], fill: purple.lighten(80%)),
    node((0, 2), [Evolution\ Engine], fill: blue.lighten(90%)),
    node((1.5, 2), [Corporation\ System], fill: green.lighten(90%)),
    node((3, 2), [Chronicler], fill: orange.lighten(90%)),
    node((4.5, 2), [Empirica], fill: purple.lighten(90%)),
    edge((2, 0), (0, 1), "->"),
    edge((2, 0), (1.5, 1), "->"),
    edge((2, 0), (3, 1), "->"),
    edge((2, 0), (4.5, 1), "->"),
    edge((0, 1), (0, 2), "->"),
    edge((1.5, 1), (1.5, 2), "->"),
    edge((3, 1), (3, 2), "->"),
    edge((4.5, 1), (4.5, 2), "->"),
  )
]

= Quick Start by Use Case

#table(
  columns: (1fr, 2fr),
  stroke: 0.5pt,
  inset: 8pt,
  fill: (x, y) => if y == 0 { luma(230) } else { white },
  [*Use Case*], [*Command*],
  [Evolve Agents], [`waft new lab && waft evolve`],
  [Create Corporation], [`waft corp create "My Startup"`],
  [Generate Brief], [`waft chronicle brief --data data.json`],
  [Start Session], [`waft session create`],
  [Spawn Being], [`waft being spawn --reality my_reality`],
  [Run D&D], [`waft quest create --scenario dungeon`],
)

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white, size: 10pt)[
      USE CASES | One Framework, Infinite Applications
    ]
  ]
]
