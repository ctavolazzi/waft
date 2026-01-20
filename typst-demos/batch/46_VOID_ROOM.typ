// THE VOID ROOM
// Classified Facility Documentation

#import "@preview/showybox:2.0.4": showybox

#set document(title: "The Void Room", author: "Teleport Massive [REDACTED]")
#set page(paper: "us-letter", margin: 1in, fill: rgb("#0a0a0a"))
#set text(font: "New Computer Modern", size: 10pt, fill: rgb("#00ff00"))

#let danger = rgb("#ff0000")
#let void-green = rgb("#00ff00")

#align(center)[
  #rect(fill: danger, width: 100%, inset: 1em)[
    #text(fill: white, size: 12pt, weight: "bold")[
      CLASSIFICATION: [REDACTED] \
      CLEARANCE REQUIRED: BLACK \
      UNAUTHORIZED ACCESS: TERMINATION
    ]
  ]
  
  #v(0.5em)
  
  #rect(fill: rgb("#111"), stroke: 1pt + void-green, width: 100%, inset: 2em)[
    #text(fill: void-green, size: 24pt, weight: "bold")[THE VOID ROOM]
    #v(0.3em)
    #text(fill: void-green.darken(30%), size: 12pt)[Site-Delta-9 | Level 5 | Section [REDACTED]]
  ]
]

#v(1em)

= NOTICE

#showybox(
  frame: (border-color: danger, body-color: rgb("#1a0000")),
)[
  #text(fill: danger)[
    If you are reading this document without BLACK clearance, report immediately to Security. Failure to comply will result in [REDACTED].
  ]
]

= Location

The Void Room is located on Level 5 of Site-Delta-9. Access requires:

- BLACK clearance authorization
- Biometric verification
- Quantum signature scan
- Executive Council approval
- [REDACTED]

= Description

The Void Room is a [REDACTED] measuring approximately [REDACTED] meters. The walls are constructed of [REDACTED] and maintained at a temperature of [REDACTED].

#showybox(
  frame: (border-color: void-green, body-color: rgb("#001100")),
)[
  *Physical Characteristics:*
  - Dimensions: [REDACTED]
  - Temperature: [REDACTED]
  - Lighting: [REDACTED]
  - Atmosphere: [REDACTED]
]

#pagebreak()

= Purpose

The Void Room serves as [REDACTED] for Teleport Massive's [REDACTED] research. Following the Quantum Incident, it was repurposed to [REDACTED].

Current uses include:
- [REDACTED]
- [REDACTED]
- Scint containment (limited)
- [REDACTED]

= Safety Protocols

#showybox(
  frame: (border-color: danger, body-color: rgb("#1a0000")),
  title-style: (color: danger),
  title: "⚠ CRITICAL",
)[
  #text(fill: danger)[
    DO NOT look directly at [REDACTED]. \
    DO NOT speak aloud while inside. \
    DO NOT acknowledge the [REDACTED]. \
    DO NOT [REDACTED].
  ]
]

= Incident Log (Partial)

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt + void-green,
  inset: 8pt,
  fill: rgb("#0a0a0a"),
  [*Date*], [*Event*],
  [2026-02-03], [[REDACTED]],
  [2026-02-17], [Researcher [REDACTED] reported seeing [REDACTED]],
  [2026-03-01], [[REDACTED] contained successfully],
  [2026-03-15], [The [REDACTED] spoke. Contents classified.],
)

= Current Status

#text(fill: void-green)[
  The Void Room is currently: *ACTIVE*
  
  Occupant status: [REDACTED]
  
  Last inspection: [REDACTED]
  
  Next scheduled [REDACTED]: [REDACTED]
]

= Related Documents

- TM-VR-001: Void Room Construction (CLASSIFIED)
- TM-VR-002: [REDACTED] Protocols (CLASSIFIED)
- TM-VR-003: The [REDACTED] Incident (CLASSIFIED)
- TM-VR-004: What Lives in the Void (CLASSIFIED)

#v(1em)

#align(center)[
  #rect(fill: rgb("#111"), stroke: 1pt + void-green, inset: 1em)[
    #text(fill: void-green, size: 9pt)[
      TELEPORT MASSIVE | THE VOID ROOM \
      "Some doors should not be opened." \
      — Dr. [REDACTED], 2026
    ]
  ]
]
