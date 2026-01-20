// SITE-DELTA-9 FACILITY GUIDE
// Teleport Massive Research Installation

#import "@preview/showybox:2.0.4": showybox

#set document(title: "Site-Delta-9 Guide", author: "Teleport Massive Facilities")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let tm-blue = rgb("#1a365d")
#let danger = rgb("#c53030")
#let warning = rgb("#d69e2e")

#align(center)[
  #rect(fill: tm-blue, width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[SITE-DELTA-9]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[Teleport Massive Research Installation]
    #v(0.2em)
    #text(fill: white.darken(20%), size: 10pt)[Facility Guide | Classification: Internal]
  ]
]

#v(1em)

= Overview

*Site-Delta-9* is Teleport Massive's primary research installation, located [REDACTED]. The facility houses the company's most advanced quantum teleportation equipment and serves as the center for Scint research.

#showybox(
  frame: (border-color: warning, body-color: warning.lighten(92%)),
)[
  *NOTE:* This document contains general facility information only. Detailed layouts, security protocols, and research specifics are available on a need-to-know basis.
]

= Facility Levels

== Level 1: Administration (GREEN Clearance)

- Main entrance and reception
- Human Resources offices
- General meeting rooms
- Visitor processing

== Level 2: Research Labs (YELLOW Clearance)

- Standard research laboratories
- Equipment calibration rooms
- Data analysis centers
- Graduate student offices

== Level 3: Advanced Labs (RED Clearance)

- Quantum entanglement chambers
- Teleportation testing facilities
- Scint detection equipment
- Post-incident analysis rooms

#pagebreak()

== Level 4: Quantum Core (BLACK Clearance)

#showybox(
  frame: (border-color: danger, body-color: danger.lighten(95%)),
  title: "⚠ RESTRICTED ACCESS",
)[
  - Quantum Chamber 7 (site of The Incident)
  - Primary teleportation apparatus
  - Scint containment systems
  - [ADDITIONAL INFORMATION REDACTED]
]

== Level 5: The Void Room (SPECIAL Clearance)

#rect(fill: black, width: 100%, inset: 1em)[
  #text(fill: white)[
    *INFORMATION CLASSIFIED* \
    Contact Executive Council for access requirements
  ]
]

= Key Locations

== Quantum Chamber 7

Where the Quantum Incident occurred. Now serves as the primary Scint research facility. Enhanced monitoring and containment systems installed following TM-TX-8472.

== The Cafeteria

Located on Level 1. Open 6 AM - 10 PM. Surprisingly good food. *Do not ask questions about the food.*

== Medical Bay

Level 2. Staffed 24/7. Specialized in quantum exposure treatment and post-Scint psychological support.

== The Archive

Level 3. Contains all research documentation, Flight Recorder backups, and historical records. Temperature and humidity controlled.

= Daily Operations

== Shift Schedule

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*Shift*], [*Hours*],
  [Day], [6:00 AM - 2:00 PM],
  [Swing], [2:00 PM - 10:00 PM],
  [Night], [10:00 PM - 6:00 AM],
)

== Regular Drills

- *Scint Drill:* Monthly (first Monday)
- *Evacuation Drill:* Quarterly
- *Containment Drill:* Bi-annually
- *Full Facility Lockdown:* Annual test

= Emergency Procedures

== Scint Alert

1. Alarm sounds (distinctive warbling tone)
2. Check nearest Scint indicator panel
3. Follow color-coded evacuation routes
4. Report to designated assembly area
5. Await all-clear announcement

== Containment Breach

#showybox(
  frame: (border-color: danger, body-color: danger.lighten(95%)),
)[
  1. *DO NOT PANIC*
  2. Seal all doors (automatic in most areas)
  3. Don protective equipment if available
  4. Avoid looking at any anomalies
  5. Wait for extraction team
]

= Amenities

- On-site gym (Level 1)
- Meditation room (Level 1)
- Library and reading room (Level 2)
- Rooftop garden (access restricted during experiments)
- Sleeping quarters for extended shifts (Level 2)

= Contact Information

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*Emergency*], [Extension 911],
  [*Security*], [Extension 100],
  [*Medical*], [Extension 200],
  [*Facilities*], [Extension 300],
  [*HR*], [Extension 400],
)

#v(1em)

#align(center)[
  #rect(fill: tm-blue, inset: 1em)[
    #text(fill: white, size: 10pt)[
      SITE-DELTA-9 | "Where Reality Meets Research"
    ]
  ]
]
