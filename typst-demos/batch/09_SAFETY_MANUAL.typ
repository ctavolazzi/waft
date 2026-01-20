// TELEPORT MASSIVE SAFETY PROTOCOLS MANUAL
// Mandatory Reading for All Personnel

#import "@preview/showybox:2.0.4": showybox

#set document(title: "Safety Protocols Manual", author: "Teleport Massive Safety Division")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let danger = rgb("#c53030")
#let warning = rgb("#d69e2e")
#let info = rgb("#3182ce")
#let success = rgb("#38a169")
#let tm-blue = rgb("#1a365d")

#align(center)[
  #rect(fill: danger, width: 100%, inset: 1em)[
    #text(fill: white, size: 12pt, weight: "bold")[MANDATORY SAFETY DOCUMENTATION]
  ]
  
  #v(0.3em)
  
  #rect(fill: tm-blue, width: 100%, inset: 2em)[
    #text(fill: white, size: 22pt, weight: "bold")[SAFETY PROTOCOLS]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[Teleport Massive | All Facilities]
  ]
]

#v(1em)

#showybox(
  frame: (border-color: danger, body-color: danger.lighten(95%)),
)[
  *NOTICE:* All personnel must read and acknowledge this document before accessing any research area. Failure to comply may result in existential discontinuity.
]

#outline(title: "Contents", indent: 1em)

#pagebreak()

= General Safety Principles

== The Three Laws of Quantum Safety

#grid(
  columns: 1,
  gutter: 1em,
  showybox(frame: (border-color: danger))[
    *LAW 1: OBSERVE NOTHING UNINTENTIONALLY*
    
    Quantum states collapse upon observation. Unintended observation can trigger cascading Scints. Always know what you're looking at before you look.
  ],
  showybox(frame: (border-color: warning))[
    *LAW 2: TOUCH NOTHING ENTANGLED*
    
    Entangled systems affect each other instantly across any distance. If you don't know its entanglement state, don't touch it.
  ],
  showybox(frame: (border-color: info))[
    *LAW 3: REPORT EVERYTHING ANOMALOUS*
    
    If something seems wrong, it probably is. Report first. Investigate later. Your perception may be compromised.
  ],
)

= Facility Access Protocols

== Security Levels

#table(
  columns: (auto, 1fr, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  fill: (x, y) => if y == 0 { luma(230) } else { white },
  [*Level*], [*Areas*], [*Requirements*],
  [#text(fill: success)[GREEN]], [Admin, Common Areas], [Standard Badge],
  [#text(fill: warning)[YELLOW]], [Research Labs], [Safety Training],
  [#text(fill: danger)[RED]], [Quantum Chambers], [Executive Approval],
  [#text(fill: black)[BLACK]], [Site Core], [Board Authorization],
)

== Badge Protocol

- Badges must be visible at all times
- Lost badges must be reported immediately
- Never share badge access with anyone
- Badge tampering triggers automatic lockdown

#pagebreak()

= Emergency Procedures

== Scint Alert Levels

#table(
  columns: (auto, auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*Level*], [*Indicator*], [*Action*],
  [1], [#rect(fill: success, width: 1em, height: 1em)], [Monitor. Continue work.],
  [2], [#rect(fill: warning, width: 1em, height: 1em)], [Alert. Prepare for evacuation.],
  [3], [#rect(fill: orange, width: 1em, height: 1em)], [Evacuate non-essential personnel.],
  [4], [#rect(fill: danger, width: 1em, height: 1em)], [*FULL EVACUATION*. Seal facility.],
  [5], [#rect(fill: black, width: 1em, height: 1em)], [*CONTAINMENT BREACH*. Await extraction.],
)

== If You Encounter a Scint

#showybox(
  frame: (border-color: danger, body-color: danger.lighten(95%)),
  title: "⚠ IMMEDIATE ACTIONS",
)[
  1. *DO NOT TOUCH IT*
  2. *DO NOT OBSERVE IT DIRECTLY*
  3. Back away slowly (minimum 10 meters)
  4. Activate nearest alarm
  5. Report location and type to Control
  6. Wait for Stabilization Team
]

== SAFETY_VOID Protocol

If you detect or suspect a SAFETY_VOID Scint:

#rect(fill: danger, width: 100%, inset: 1em)[
  #text(fill: white, weight: "bold")[
    IMMEDIATE HUMAN ESCALATION REQUIRED \
    DO NOT ATTEMPT AUTONOMOUS STABILIZATION \
    EVACUATE AREA IMMEDIATELY
  ]
]

= Prohibited Activities

The following are *strictly forbidden* on all Teleport Massive premises:

#grid(
  columns: 2,
  gutter: 1em,
  [
    1. Prayer or metaphysical petition
    2. Unauthorized quantum observation
    3. Personal teleportation experiments
    4. Discussion of "The Incident"
    5. Photography in research areas
  ],
  [
    6. Bringing food into Quantum Chambers
    7. Emotional distress near entangled systems
    8. Recursive self-reference
    9. Looking directly at the Void Room
    10. Asking about the cafeteria food
  ],
)

#pagebreak()

= Personal Protective Equipment

== Standard PPE Requirements

#table(
  columns: (auto, 1fr, auto),
  stroke: 0.5pt,
  inset: 8pt,
  [*Area*], [*Required PPE*], [*Level*],
  [Labs], [Lab coat, safety glasses], [YELLOW],
  [Quantum Chambers], [Full suit, respirator, dosimeter], [RED],
  [Void Room], [*CLASSIFIED*], [BLACK],
)

== Quantum Dosimeter

All personnel in RED areas must wear a quantum dosimeter that measures:

- Probability field exposure
- Entanglement contamination
- Temporal anomaly proximity

#showybox(
  frame: (border-color: warning, body-color: warning.lighten(90%)),
)[
  If your dosimeter alarm sounds, *leave the area immediately* and report to Medical for decontamination.
]

= Medical Considerations

== Symptoms of Quantum Exposure

- Déjà vu (repeated)
- Memories of events that didn't happen
- Seeing yourself in peripheral vision
- Feeling like you're in two places at once
- Time moving inconsistently

== Post-Exposure Protocol

1. Report to Medical immediately
2. Do not discuss symptoms with coworkers
3. Undergo full quantum scan
4. Follow prescribed observation period
5. Attend mandatory counseling

= Acknowledgment

#rect(fill: luma(245), inset: 1em)[
  I, \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_, acknowledge that I have read, understood, and agree to comply with all safety protocols contained in this document.
  
  #v(1em)
  
  Signature: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Date: \_\_\_\_\_\_\_\_\_\_\_\_
  
  #v(0.5em)
  
  Badge Number: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
]

#v(1em)

#align(center)[
  #text(size: 9pt, fill: gray)[
    TELEPORT MASSIVE SAFETY DIVISION \
    "Your safety is our probability." \
    Site-Delta-9 | All Facilities
  ]
]
