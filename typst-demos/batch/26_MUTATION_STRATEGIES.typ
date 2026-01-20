// MUTATION STRATEGIES
// Guide to Evolving Agent Genomes

#import "@preview/showybox:2.0.4": showybox

#set document(title: "Mutation Strategies", author: "WAFT Research Division")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#ed8936")

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(30%)), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[MUTATION STRATEGIES]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[Guide to Evolving Agent Genomes]
  ]
]

#v(1em)

= Overview

Mutation is the engine of evolution. This guide covers strategies for mutating agent genomes effectively.

= Mutation Types

#grid(
  columns: 2,
  gutter: 1em,
  showybox(frame: (border-color: blue, body-color: blue.lighten(95%)), title: "Prompt Mutation")[
    Modify system prompts while preserving intent.
    
    *Methods:*
    - Rephrase
    - Elaborate
    - Simplify
    - Specialize
  ],
  showybox(frame: (border-color: green, body-color: green.lighten(95%)), title: "Config Mutation")[
    Adjust parameters and settings.
    
    *Methods:*
    - Temperature ±0.1
    - Max tokens ±100
    - Top-p adjustment
  ],
  showybox(frame: (border-color: orange, body-color: orange.lighten(95%)), title: "Code Mutation")[
    Modify agent source code.
    
    *Methods:*
    - Add conditionals
    - Modify expressions
    - Add error handling
  ],
  showybox(frame: (border-color: purple, body-color: purple.lighten(95%)), title: "Architecture Mutation")[
    Change agent structure.
    
    *Methods:*
    - Add/remove methods
    - Change inheritance
    - Modify interfaces
  ],
)

= Mutation Rates

#table(
  columns: (auto, auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*Rate*], [*Value*], [*Use Case*],
  [Conservative], [0.01-0.05], [Fine-tuning near-optimal agents],
  [Standard], [0.05-0.15], [General exploration],
  [Aggressive], [0.15-0.30], [Escaping local optima],
  [Extreme], [0.30+], [Complete restart/exploration],
)

= Best Practices

1. *Start conservative* — High mutation destroys good genomes
2. *Increase on plateaus* — If fitness stagnates, try higher rates
3. *Use adaptive rates* — Decrease mutation as fitness improves
4. *Preserve champions* — Never mutate your best agents (elitism)
5. *Log everything* — Flight Recorder tracks all mutations

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white)[MUTATION STRATEGIES | The Art of Change]
  ]
]
