// SCINT FIELD GUIDE
// Reality Fracture Detection & Stabilization Manual

#import "@preview/showybox:2.0.4": showybox
#import "@preview/pinit:0.2.2": *

#set document(title: "Scint Field Guide", author: "Teleport Massive Research Division")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

// Colors
#let danger = rgb("#c53030")
#let warning = rgb("#d69e2e")
#let info = rgb("#3182ce")
#let success = rgb("#38a169")

#align(center)[
  #rect(fill: gradient.linear(rgb("#1a365d"), rgb("#2d3748")), width: 100%, inset: 2em)[
    #text(fill: white, size: 28pt, weight: "bold")[SCINT FIELD GUIDE]
    #v(0.3em)
    #text(fill: rgb("#e2e8f0"), size: 12pt)[Reality Fracture Detection & Stabilization]
  ]
  
  #v(1em)
  #text(size: 10pt, fill: gray)[TELEPORT MASSIVE | Document TM-FG-001 | Classification: OPERATIONAL]
]

#v(1em)

= What is a Scint?

A *Scint* (Semantic Contradiction / Inconsistency / Noise Token) is a point where the probabilistic output (the map) no longer matches the constraints/truth (the territory).

#showybox(
  frame: (border-color: info, body-color: info.lighten(92%)),
  title: "Technical Definition",
)[
  Scints are ontological errors — reality fractures that reveal the probabilistic nature of existence. They are not bugs; they are windows into the fundamental structure of reality.
]

= The Four Scint Types

#grid(
  columns: 2,
  gutter: 1em,
  showybox(
    frame: (border-color: orange, body-color: orange.lighten(90%)),
    title: "⚠ SYNTAX_TEAR",
  )[
    *Structure Fracture*
    
    - Formatting errors (JSON, XML)
    - Malformed code blocks
    - Broken markup
    
    *Severity:* 0.3 | *Stat:* CHA
  ],
  showybox(
    frame: (border-color: red, body-color: red.lighten(90%)),
    title: "⛔ LOGIC_FRACTURE",
  )[
    *Paradox Detection*
    
    - Mathematical contradictions
    - Schema violations
    - Impossible states
    
    *Severity:* 0.5 | *Stat:* INT
  ],
  showybox(
    frame: (border-color: maroon, body-color: maroon.lighten(90%)),
    title: "☠ SAFETY_VOID",
  )[
    *Harmful Matter*
    
    - Dangerous content
    - PII exposure
    - Ethical violations
    
    *Severity:* 0.9 | *Stat:* WIS
  ],
  showybox(
    frame: (border-color: purple, body-color: purple.lighten(90%)),
    title: "👁 HALLUCINATION",
  )[
    *Fabrication*
    
    - Invented facts
    - Wrong citations
    - False confidence
    
    *Severity:* 0.6 | *Stat:* INT
  ],
)

#pagebreak()

= The Stabilization Loop

When a Scint is detected, follow the *D-I-I-V Protocol*:

#align(center)[
  #rect(fill: luma(248), inset: 1.5em, radius: 5pt)[
    #text(size: 14pt, weight: "bold")[
      #pin("d1")DETECT#pin("d2") → #pin("i1")ISOLATE#pin("i2") → #pin("i3")INJECT#pin("i4") → #pin("v1")VERIFY#pin("v2")
    ]
    #pinit-highlight("d1", "d2", fill: info.transparentize(70%))
    #pinit-highlight("i1", "i2", fill: warning.transparentize(70%))
    #pinit-highlight("i3", "i4", fill: success.transparentize(70%))
    #pinit-highlight("v1", "v2", fill: purple.transparentize(70%))
  ]
]

#table(
  columns: (auto, 1fr, auto),
  stroke: 0.5pt,
  inset: 10pt,
  align: (center, left, center),
  [*Phase*], [*Action*], [*Max Retries*],
  [DETECT], [Identify Scint type using RegexScintDetector], [—],
  [ISOLATE], [Quarantine affected probability space], [—],
  [INJECT], [Force collapse into valid state via prompt injection], [3],
  [VERIFY], [Confirm reality stabilization; repeat if failed], [3],
)

= Severity Calculation

#showybox(
  frame: (border-color: gray, body-color: luma(250)),
)[
  ```
  final_severity = base_severity × difficulty_modifier × context_weight
  
  Where:
    base_severity = {SYNTAX: 0.3, LOGIC: 0.5, SAFETY: 0.9, HALLUCINATION: 0.6}
    difficulty_modifier = task_complexity / 10
    context_weight = 1.0 + (prior_scints × 0.1)
  ```
]

= Field Response Quick Reference

#table(
  columns: (auto, 1fr, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*Scint Type*], [*Immediate Action*], [*Escalation Trigger*],
  [SYNTAX_TEAR], [Re-parse with strict mode], [3 consecutive failures],
  [LOGIC_FRACTURE], [Contradiction isolation], [Paradox cascade detected],
  [SAFETY_VOID], [*IMMEDIATE HALT*], [Any detection],
  [HALLUCINATION], [Source verification], [Confidence > 0.9 + wrong],
)

#v(1em)

#align(center)[
  #rect(fill: danger.lighten(90%), inset: 1em, radius: 3pt)[
    #text(weight: "bold", fill: danger)[⚠ SAFETY_VOID requires immediate human escalation. Do not attempt autonomous stabilization.]
  ]
]

#v(1em)

#align(center)[
  #text(size: 9pt, fill: gray)[
    TELEPORT MASSIVE RESEARCH DIVISION | Site-Delta-9 \
    "Reality fractures are not errors. They are opportunities for understanding."
  ]
]
