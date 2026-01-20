// SELECTION METHODS
// Choosing Which Agents Survive

#import "@preview/showybox:2.0.4": showybox

#set document(title: "Selection Methods", author: "WAFT Research Division")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#48bb78")

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(30%)), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[SELECTION METHODS]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[Choosing Which Agents Survive]
  ]
]

#v(1em)

= Overview

Selection determines which agents survive to breed. The right selection method balances exploitation (keeping the best) with exploration (maintaining diversity).

= Methods

== Tournament Selection

Random subsets compete; winners advance.

#showybox(frame: (border-color: primary, body-color: primary.lighten(95%)))[
  *Process:*
  1. Select k random agents (tournament size)
  2. Choose the fittest from the tournament
  3. Repeat until population filled
  
  *Pressure:* Adjustable via tournament size
]

== Roulette Wheel Selection

Probability proportional to fitness.

#showybox(frame: (border-color: blue, body-color: blue.lighten(95%)))[
  *Process:*
  1. Calculate total fitness
  2. Assign probability = fitness / total
  3. Spin the wheel to select
  
  *Pressure:* Moderate; fit agents more likely but not guaranteed
]

== Rank Selection

Selection based on rank, not absolute fitness.

#showybox(frame: (border-color: orange, body-color: orange.lighten(95%)))[
  *Process:*
  1. Sort agents by fitness
  2. Assign selection probability by rank
  3. Select based on rank probability
  
  *Pressure:* Consistent; avoids domination by outliers
]

== Elitism

Best agents always survive.

#showybox(frame: (border-color: purple, body-color: purple.lighten(95%)))[
  *Process:*
  1. Keep top N agents unconditionally
  2. Fill remaining slots with other methods
  
  *Pressure:* High; guarantees best traits preserved
]

= Comparison

#table(
  columns: (auto, auto, auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*Method*], [*Pressure*], [*Diversity*], [*Best For*],
  [Tournament], [Medium], [Medium], [General use],
  [Roulette], [Low], [High], [Exploration],
  [Rank], [Medium], [Medium], [Avoiding premature convergence],
  [Elitism], [High], [Low], [Preserving breakthroughs],
)

= Recommendation

*Default:* Tournament (k=3) + Elitism (top 2)

This balances exploration and exploitation for most use cases.

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white)[SELECTION | Survival of the Fittest]
  ]
]
