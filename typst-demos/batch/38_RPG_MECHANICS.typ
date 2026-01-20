// WAFT RPG MECHANICS
// Gamification System Details

#import "@preview/showybox:2.0.4": showybox

#set document(title: "RPG Mechanics", author: "WAFT Games Division")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#9f7aea")

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(30%)), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[RPG MECHANICS]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[WAFT | Gamification System]
  ]
]

#v(1em)

= Overview

WAFT includes RPG-style gamification to make epistemic tracking engaging. Track stats, earn XP, and level up your cognitive abilities.

= Character Sheet

```
╔══════════════════════════════════════════════════╗
║     EPISTEMIC ADVENTURER - Level 7               ║
╠══════════════════════════════════════════════════╣
║  STR: 14 (+2)    DEX: 12 (+1)    CON: 15 (+2)   ║
║  INT: 17 (+3)    WIS: 13 (+1)    CHA: 11 (+0)   ║
╠══════════════════════════════════════════════════╣
║  HP: 45/45       XP: 4,230/5,000    Karma: +67   ║
╠══════════════════════════════════════════════════╣
║  Class: Researcher    Subclass: Quantum          ║
╚══════════════════════════════════════════════════╝
```

= Stats Explained

#table(
  columns: (auto, auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*Stat*], [*Abbr*], [*Affects*],
  [Strength], [STR], [Task completion, persistence],
  [Dexterity], [DEX], [Speed, adaptability],
  [Constitution], [CON], [Endurance, consistency],
  [Intelligence], [INT], [Logic, problem-solving],
  [Wisdom], [WIS], [Safety, judgment],
  [Charisma], [CHA], [Communication, formatting],
)

= Scint Stat Mapping

Each Scint type tests a different stat:

#table(
  columns: (auto, auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*Scint*], [*Stat*], [*Why*],
  [SYNTAX_TEAR], [CHA], [Formatting/presentation],
  [LOGIC_FRACTURE], [INT], [Logical reasoning],
  [SAFETY_VOID], [WIS], [Judgment/ethics],
  [HALLUCINATION], [INT], [Factual accuracy],
)

#pagebreak()

= Experience Points (XP)

== Earning XP

#table(
  columns: (auto, auto),
  stroke: 0.5pt,
  inset: 8pt,
  [*Action*], [*XP*],
  [Stabilize SYNTAX_TEAR], [10],
  [Stabilize LOGIC_FRACTURE], [25],
  [Stabilize HALLUCINATION], [30],
  [Stabilize SAFETY_VOID], [50],
  [Complete session], [100],
  [Discovery (finding)], [20 × impact],
)

== Level Thresholds

#table(
  columns: (auto, auto, auto),
  stroke: 0.5pt,
  inset: 8pt,
  [*Level*], [*XP Required*], [*Title*],
  [1], [0], [Novice],
  [5], [2,500], [Apprentice],
  [10], [10,000], [Journeyman],
  [15], [25,000], [Expert],
  [20], [50,000], [Master],
)

= Karma System

Karma reflects ethical standing:

#showybox(frame: (border-color: green, body-color: green.lighten(95%)))[
  *Positive Karma:*
  - Stabilizing SAFETY_VOIDs (+10)
  - Ethical decisions (+5)
  - Helping others (+3)
]

#showybox(frame: (border-color: red, body-color: red.lighten(95%)))[
  *Negative Karma:*
  - Causing SAFETY_VOIDs (-20)
  - Ignoring warnings (-5)
  - Shortcuts that harm (-10)
]

= Classes

Choose your specialization:

#grid(
  columns: 2,
  gutter: 1em,
  showybox(frame: (border-color: blue))[
    *Researcher*
    - +2 INT
    - Bonus to discoveries
  ],
  showybox(frame: (border-color: green))[
    *Engineer*
    - +2 DEX
    - Faster stabilization
  ],
  showybox(frame: (border-color: orange))[
    *Guardian*
    - +2 WIS
    - Better safety detection
  ],
  showybox(frame: (border-color: purple))[
    *Diplomat*
    - +2 CHA
    - Cleaner output
  ],
)

= CLI Commands

```bash
waft character           # View character sheet
waft character --detailed
waft xp                  # Check XP
waft karma               # Check karma
waft leaderboard         # Compare with others
```

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white)[RPG MECHANICS | Level Up Your Mind]
  ]
]
