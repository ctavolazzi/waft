// TELEPORT MASSIVE EMPLOYEE HANDBOOK
// Onboarding Documentation for New Hires

#import "@preview/showybox:2.0.4": showybox

#set document(title: "Employee Handbook", author: "Teleport Massive HR")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let tm-blue = rgb("#1a365d")

#align(center)[
  #rect(fill: tm-blue, width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[TELEPORT MASSIVE]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 14pt)[Employee Handbook]
    #v(0.2em)
    #text(fill: white.darken(20%), size: 10pt)[Making Distance Irrelevant Since 2025]
  ]
]

#v(1em)

#outline(title: "Contents", indent: 1em, depth: 2)

#pagebreak()

= Welcome to Teleport Massive

Congratulations on joining the team that will revolutionize transportation. At Teleport Massive, we're not just building technology—we're redefining the laws of physics.

#showybox(
  frame: (border-color: tm-blue, body-color: tm-blue.lighten(95%)),
  title: "Our Mission",
)[
  To study quantum entanglement and scale quantum teleportation from mini to macro, revolutionizing transportation and making distance irrelevant.
]

= Company History

== The Founding (July 1, 2025)

Teleport Massive was founded by Dr. Elena Voss (CEO) and Dr. Marcus Chen (CTO) with \$2M in seed funding and a vision to make quantum teleportation a reality.

== Key Milestones

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 10pt,
  [*Date*], [*Event*],
  [July 2025], [Company incorporated],
  [January 2026], [First major hiring push—3 Lead Scientists],
  [January 13, 2026], [The Quantum Incident (TM-TX-8472)],
  [2026+], [Scint System development begins],
)

= Organizational Structure

== Departments

- *Executive* — Strategic leadership
- *Research & Development* — Core quantum research
- *Operations* — Day-to-day facility management
- *Safety & Compliance* — Protocol enforcement

== Key Personnel

#grid(
  columns: 2,
  gutter: 1em,
  showybox(frame: (border-color: gray))[
    *Dr. Elena Voss* \
    CEO & Co-Founder \
    PhD Quantum Physics, MIT
  ],
  showybox(frame: (border-color: gray))[
    *Dr. Marcus Chen* \
    CTO & Co-Founder \
    PhD Experimental Physics, Stanford
  ],
)

#pagebreak()

= Safety Protocols

#showybox(
  frame: (border-color: red, body-color: red.lighten(95%)),
  title: "⚠ CRITICAL SAFETY INFORMATION",
)[
  All employees must complete quantum safety training before accessing research areas. Failure to comply may result in existential discontinuity.
]

== Facility Access Levels

#table(
  columns: (auto, 1fr, auto),
  stroke: 0.5pt,
  inset: 8pt,
  [*Level*], [*Areas*], [*Clearance Required*],
  [Green], [Administrative, Common Areas], [Standard Badge],
  [Yellow], [Research Labs], [Safety Training + Supervisor],
  [Red], [Quantum Chamber], [Executive Approval],
  [Black], [Site-Delta-9 Core], [Board Authorization],
)

== Prohibited Activities

1. Prayer or metaphysical petition on premises
2. Unauthorized quantum state observation
3. Personal teleportation experiments
4. Discussion of "The Incident" outside secure channels

= Code of Conduct

== Core Values

- *Integrity* — We pursue truth, even uncomfortable truths
- *Innovation* — We push boundaries responsibly
- *Safety* — We protect our people and reality itself
- *Collaboration* — We achieve more together

== Dress Code

Business casual in administrative areas. Lab coats and safety gear required in research zones. No loose clothing near quantum apparatus.

= Benefits

- Competitive salary with equity options
- Health, dental, and existential insurance
- 401(k) with company match
- Unlimited PTO (use responsibly)
- On-site cafeteria and meditation room
- Teleportation discount (when available)

#v(1em)

#align(center)[
  #rect(fill: tm-blue, inset: 1em)[
    #text(fill: white, size: 11pt)[
      Welcome to the future. Welcome to Teleport Massive.
    ]
  ]
]
