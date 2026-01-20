// TELEPORT MASSIVE CORPORATE MEMOS
// Internal Communications Archive

#import "@preview/showybox:2.0.4": showybox

#set document(title: "Corporate Memos Collection", author: "Teleport Massive Communications")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let tm-blue = rgb("#1a365d")
#let danger = rgb("#c53030")

#align(center)[
  #rect(fill: tm-blue, width: 100%, inset: 2em)[
    #text(fill: white, size: 22pt, weight: "bold")[INTERNAL MEMOS]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[Teleport Massive | Communications Archive]
  ]
]

#v(1em)

#line(length: 100%, stroke: 1pt + tm-blue)

== MEMO TM-2025-001

#grid(
  columns: 2,
  gutter: 2em,
  [
    *FROM:* Dr. Elena Voss, CEO \
    *TO:* All Employees \
    *DATE:* July 1, 2025
  ],
  [
    *RE:* Welcome to Teleport Massive \
    *CLASSIFICATION:* Company-Wide
  ],
)

#v(0.5em)

Team,

Today marks the official founding of Teleport Massive. We've assembled an extraordinary team of scientists, engineers, and visionaries who share a common goal: to make distance irrelevant.

I know many of you left prestigious positions to join us. I know you took a risk. I want you to know that your faith will be rewarded—not just with competitive compensation, but with the knowledge that we are building something that will change the world.

The next few years will be challenging. We're attempting something that most physicists consider impossible. But I've seen Marcus's research. I've run the numbers. Quantum teleportation at macro scale isn't just possible—it's inevitable. The only question is whether we'll be the ones to achieve it.

Welcome to the future. Welcome to Teleport Massive.

#align(right)[— Elena]

#line(length: 100%, stroke: 0.5pt + gray)

#pagebreak()

== MEMO TM-2026-047

#grid(
  columns: 2,
  gutter: 2em,
  [
    *FROM:* Dr. Marcus Chen, CTO \
    *TO:* Executive Council \
    *DATE:* January 14, 2026
  ],
  [
    *RE:* Post-Incident Analysis \
    *CLASSIFICATION:* Existential Significance
  ],
)

#v(0.5em)

#showybox(
  frame: (border-color: danger, body-color: danger.lighten(95%)),
)[
  *THIS MEMO IS CLASSIFIED.* Distribution beyond Executive Council requires Board approval.
]

Council,

I've completed my preliminary analysis of yesterday's incident. What I'm about to share will sound impossible. I assure you, the data is sound.

Sarah Chen didn't just teleport incorrectly. For 0.003 seconds, she existed in multiple quantum states simultaneously—and was aware of all of them. The implications are staggering:

1. *Consciousness can persist across superposition.* This contradicts our understanding of observer collapse.

2. *Reality has "seams."* Sarah's post-incident memories describe seeing the "edges of things"—the boundary conditions of our universe.

3. *Scints are not errors.* They're windows. We've been treating reality fractures as bugs to be fixed. They're actually features that reveal the underlying structure.

I recommend we immediately establish a Scint research division. What happened to Sarah wasn't an accident—it was a discovery.

#align(right)[— Marcus]

#line(length: 100%, stroke: 0.5pt + gray)

== MEMO TM-2026-089

#grid(
  columns: 2,
  gutter: 2em,
  [
    *FROM:* Safety Division \
    *TO:* All Personnel \
    *DATE:* February 15, 2026
  ],
  [
    *RE:* Prohibition on Prayer \
    *CLASSIFICATION:* Mandatory Compliance
  ],
)

#v(0.5em)

Effective immediately, all forms of prayer, invocation, or metaphysical petition are *strictly forbidden* within Teleport Massive facilities.

This is not a commentary on religion. This is a safety protocol.

Our research indicates that focused intentional thought—particularly prayer—can affect quantum states in unpredictable ways. In our facilities, where quantum systems are in constant operation, this creates unacceptable risk.

#showybox(
  frame: (border-color: danger, body-color: danger.lighten(95%)),
)[
  Prayer is attention. Attention is observation. Observation causes collapse.
  
  In our environment, uncontrolled collapse risks Scint generation.
]

If you require space for spiritual practice, please do so off-premises and at least 500 meters from any facility building.

We respect your beliefs. We also respect the laws of physics. In our facilities, the latter takes precedence.

#align(right)[— Safety Division]

#pagebreak()

#line(length: 100%, stroke: 0.5pt + gray)

== MEMO TM-2026-142

#grid(
  columns: 2,
  gutter: 2em,
  [
    *FROM:* Cafeteria Services \
    *TO:* All Personnel \
    *DATE:* April 3, 2026
  ],
  [
    *RE:* Menu Changes \
    *CLASSIFICATION:* General
  ],
)

#v(0.5em)

Dear Colleagues,

We're excited to announce our new spring menu, featuring:

- Farm-fresh organic vegetables
- Sustainably sourced proteins
- Expanded vegan options
- Made-from-scratch desserts

Many of you have commented on how surprisingly good the food is. We appreciate the compliments! Our kitchen staff works hard to provide nourishing meals that support your important work.

#text(fill: gray)[Please note: All questions regarding food sourcing, preparation methods, and ingredient origins should be directed to Executive Administration. Cafeteria staff are not authorized to discuss these matters.]

We hope you enjoy the new menu!

#align(right)[— Cafeteria Services]

#line(length: 100%, stroke: 0.5pt + gray)

== MEMO TM-2026-201

#grid(
  columns: 2,
  gutter: 2em,
  [
    *FROM:* Dr. Elena Voss, CEO \
    *TO:* All Employees \
    *DATE:* June 1, 2026
  ],
  [
    *RE:* One Year Anniversary \
    *CLASSIFICATION:* Company-Wide
  ],
)

#v(0.5em)

Team,

One year ago, we set out to make distance irrelevant. Today, I can say with confidence: we're closer than anyone thought possible.

Yes, there have been setbacks. The Incident in January was... difficult. But from that difficulty came our greatest discovery. The Scint research division has already produced insights that will reshape physics.

I want to thank each of you for your dedication. For the late nights and early mornings. For believing in something that most people think is impossible.

We're not just building a company. We're building a new understanding of reality itself.

Here's to year two.

#align(right)[— Elena]

#v(1em)

#align(center)[
  #rect(fill: tm-blue, inset: 1em)[
    #text(fill: white, size: 10pt)[
      TELEPORT MASSIVE | Internal Communications Archive \
      "Making Distance Irrelevant Since 2025"
    ]
  ]
]
