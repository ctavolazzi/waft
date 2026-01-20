// SARAH CHEN - PERSONNEL FILE
// Subject of Incident TM-TX-8472

#import "@preview/showybox:2.0.4": showybox

#set document(title: "Sarah Chen Personnel File", author: "Teleport Massive HR")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let tm-blue = rgb("#1a365d")
#let danger = rgb("#c53030")

#align(center)[
  #rect(fill: danger, width: 100%, inset: 0.8em)[
    #text(fill: white, size: 10pt, weight: "bold")[CLASSIFICATION: EXISTENTIAL SIGNIFICANCE]
  ]
  
  #v(0.3em)
  
  #rect(fill: tm-blue, width: 100%, inset: 2em)[
    #text(fill: white, size: 22pt, weight: "bold")[PERSONNEL FILE]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 14pt)[CHEN, Sarah | ID: TM-2025-0847]
  ]
]

#v(1em)

#grid(
  columns: (1fr, 2fr),
  gutter: 2em,
  [
    #rect(fill: luma(240), width: 100%, height: 10em, inset: 1em)[
      #align(center + horizon)[
        #text(fill: gray, size: 9pt)[PHOTO \\ REDACTED \\ (Security Protocol)]
      ]
    ]
    
    #v(1em)
    
    *Status:* Active \
    *Clearance:* RED \
    *Department:* R&D \
    *Reports To:* Dr. Marcus Chen
  ],
  [
    = Basic Information
    
    #table(
      columns: (auto, 1fr),
      stroke: 0.5pt,
      inset: 8pt,
      [*Full Name*], [Sarah Chen],
      [*Employee ID*], [TM-2025-0847],
      [*Position*], [Research Associate],
      [*Start Date*], [March 15, 2025],
      [*Location*], [Site-Delta-9],
      [*Incident Status*], [Subject of TM-TX-8472],
    )
  ],
)

= Background

== Education

- MS in Physics, Stanford University (2024)
- BS in Physics, UC Berkeley (2022)

== Prior Experience

- Research Intern, Lawrence Berkeley National Laboratory (2023-2024)
- Teaching Assistant, Stanford Physics Department (2022-2023)

== Specialization

Quantum state measurement and observation protocols. Recruited specifically for teleportation testing program.

#pagebreak()

= Incident TM-TX-8472

#showybox(
  frame: (border-color: danger, body-color: danger.lighten(95%)),
  title: "⚠ CRITICAL INCIDENT",
)[
  On January 13, 2026, Sarah Chen was the test subject in a routine quantum teleportation trial that resulted in anomalous multi-state existence.
]

== Timeline

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*14:45*], [Pre-teleportation checks completed; subject cleared],
  [*14:46*], [Subject entered origin chamber],
  [*14:47:22*], [Anomalous quantum readings detected],
  [*14:47:23*], [*INCIDENT* — Multi-state existence begins],
  [*14:47:23.003*], [Spontaneous wave function collapse],
  [*14:47:24*], [Subject materialized in destination chamber],
  [*14:47:30*], [Emergency protocols activated],
)

== Post-Incident Assessment

Subject reported:
- Simultaneous awareness of multiple locations
- Memories of "seeing the edges of things"
- Perception of "seams" in reality
- Persistent déjà vu (ongoing)

== Medical Status

- Physical health: Normal (all metrics within baseline)
- Psychological status: Under observation
- Quantum contamination: Elevated but stable
- Recommended monitoring: Indefinite

= Post-Incident Role

Following the incident, Sarah Chen was reassigned to the newly created Scint Research Division. Her unique perspective—having directly experienced a reality fracture—makes her invaluable to ongoing research.

#showybox(
  frame: (border-color: tm-blue, body-color: tm-blue.lighten(95%)),
)[
  *Current Assignment:* Lead researcher for Scint phenomenology. Provides first-person accounts of reality fracture experience to inform detection and stabilization protocols.
]

= Subject Statement (Excerpt)

#rect(fill: luma(250), inset: 1em)[
  #text(style: "italic")[
    "I was everywhere. Not sequentially—simultaneously. I remember being in the origin chamber, watching myself fade. I remember being in the destination chamber, watching myself appear. And I remember being... nowhere. Or everywhere. A place that wasn't a place.
    
    I saw how it all fits together. The seams. The edges. Reality isn't solid—it's stitched. And sometimes the stitches show.
    
    I'm not the same person I was before. I'm not sure I'm one person anymore. But I'm still here. And I remember everything."
  ]
  
  #align(right)[— Sarah Chen, Post-Incident Debriefing]
]

= Supervisor Notes

#showybox(frame: (border-color: gray))[
  *Dr. Marcus Chen (no relation):* "Sarah's experience has given us insights we couldn't have obtained any other way. She's handling it remarkably well, all things considered. We're monitoring closely."
  
  *Dr. Elena Voss:* "What happened to Sarah was a tragedy and a breakthrough. We're committed to her wellbeing while learning everything we can from her experience."
]

#v(1em)

#align(center)[
  #text(size: 9pt, fill: gray)[
    TELEPORT MASSIVE | Personnel Division \
    File Last Updated: January 2026
  ]
]
