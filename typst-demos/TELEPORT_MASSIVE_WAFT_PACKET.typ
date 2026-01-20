// TELEPORT MASSIVE × WAFT
// Corporate Research Documentation Packet
// Quantum Teleportation & Evolutionary AI Systems

#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering
#import "@preview/drafting:0.2.2": *
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *
#import "@preview/pinit:0.2.2": *
#import "@preview/showybox:2.0.4": showybox

// ============================================================================
// DOCUMENT SETUP - TELEPORT MASSIVE CORPORATE STYLING
// ============================================================================

#let tm-blue = rgb("#1a365d")
#let tm-light = rgb("#e2e8f0")
#let tm-accent = rgb("#3182ce")
#let tm-warning = rgb("#d69e2e")
#let tm-danger = rgb("#c53030")
#let tm-success = rgb("#38a169")

#let header = {
  set align(bottom)
  set text(weight: "bold", size: 9pt, fill: tm-blue)
  table(
    stroke: (y: none),
    columns: (1fr, 2fr, 1fr),
    rows: 1fr,
    table.hline(stroke: tm-blue),
    [TM-DOC-2026-001],
    align(center)[TELEPORT MASSIVE | INTERNAL DOCUMENTATION],
    align(right)[#context counter(page).display("1 / 1", both: true)],
  )
}

#let footer = {
  set text(size: 8pt, fill: gray.darken(20%))
  table(
    stroke: (y: none),
    columns: (1fr, 1fr),
    rows: 1fr,
    [Classification: INTERNAL RESEARCH],
    align(right)[Quantum Division | Site-Delta-9],
    table.hline(stroke: tm-blue),
  )
}

#show: s6t5-page-bordering.with(
  margin: (left: 55pt, right: 75pt, top: 85pt, bottom: 75pt),
  expand: 12pt,
  space-top: 12pt,
  space-bottom: 12pt,
  stroke-header: none,
  stroke-footer: none,
  header: header,
  footer: footer,
)

#set text(font: "New Computer Modern", size: 10pt)
#set page(paper: "us-letter")

// Initialize codly
#show: codly-init.with()
#codly(languages: codly-languages)

// Set up drafting
#set-page-properties(margin-right: 75pt)

// ============================================================================
// COVER PAGE
// ============================================================================

#align(center + horizon)[
  #rect(fill: tm-blue, width: 100%, inset: 2em, radius: 0pt)[
    #text(fill: white, size: 32pt, weight: "bold")[
      TELEPORT MASSIVE
    ]
    
    #v(0.3em)
    
    #text(fill: tm-light, size: 14pt)[
      Quantum Teleportation Technology Division
    ]
  ]
  
  #v(2em)
  
  #text(size: 24pt, weight: "bold", fill: tm-blue)[
    Corporate Research Packet
  ]
  
  #v(0.5em)
  
  #text(size: 16pt, fill: gray.darken(20%))[
    Integration with WAFT Evolutionary Systems
  ]
  
  #v(2em)
  
  #showybox(
    frame: (
      border-color: tm-accent,
      body-color: tm-light,
      thickness: 2pt,
      radius: 0pt,
    ),
  )[
    #align(center)[
      #text(size: 11pt, style: "italic")[
        "To study quantum entanglement and scale quantum teleportation \
        from mini to macro, revolutionizing transportation and \
        making distance irrelevant."
      ]
      
      #v(0.5em)
      
      #text(size: 9pt, fill: gray)[— Teleport Massive Mission Statement, 2025]
    ]
  ]
  
  #v(3em)
  
  #grid(
    columns: 2,
    gutter: 3em,
    [
      #rect(fill: luma(248), inset: 1em, radius: 3pt)[
        *Document ID:* TM-DOC-2026-001 \
        *Classification:* Internal Research \
        *Division:* Quantum Research \
        *Site:* Delta-9
      ]
    ],
    [
      #rect(fill: luma(248), inset: 1em, radius: 3pt)[
        *Issue Date:* January 2026 \
        *Version:* 1.0 \
        *Status:* Active \
        *Pages:* 12
      ]
    ],
  )
]

#pagebreak()

// ============================================================================
// TABLE OF CONTENTS
// ============================================================================

#outline(
  title: [Contents],
  indent: 1.5em,
  depth: 2,
)

#pagebreak()

// ============================================================================
// PART I: TELEPORT MASSIVE
// ============================================================================

#align(center)[
  #rect(fill: tm-blue, width: 100%, inset: 1.5em)[
    #text(fill: white, size: 18pt, weight: "bold")[
      PART I: TELEPORT MASSIVE
    ]
    
    #text(fill: tm-light, size: 11pt)[
      Corporate Overview & History
    ]
  ]
]

#v(1em)

= The Corporation
#label("tm-corp")

#margin-note[
  Founded July 1, 2025
]

== Overview

*Teleport Massive* is a quantum teleportation technology company founded in 2025 with a revolutionary mission: to scale quantum teleportation from laboratory experiments to real-world applications.

#showybox(
  frame: (border-color: tm-accent, body-color: tm-accent.lighten(92%)),
  title: "Corporate Mission",
)[
  To study quantum entanglement and scale quantum teleportation from mini to macro, revolutionizing transportation and making distance irrelevant.
]

== The Founding (July 1, 2025)

In the summer of 2025, a group of visionary scientists and entrepreneurs came together with a bold mission.

=== The Founders

#grid(
  columns: 2,
  gutter: 1em,
  showybox(
    frame: (border-color: tm-blue, body-color: tm-blue.lighten(95%)),
    title: "Dr. Elena Voss - CEO",
  )[
    *Background:*
    - PhD Quantum Physics, MIT
    - 10+ years quantum research
    - 50+ published papers
    
    *Vision:* "We're building the future of transportation."
  ],
  showybox(
    frame: (border-color: tm-blue, body-color: tm-blue.lighten(95%)),
    title: "Dr. Marcus Chen - CTO",
  )[
    *Background:*
    - PhD Experimental Physics, Stanford
    - Chen Stabilization Protocol inventor
    - Multiple quantum computing patents
    
    *Vision:* "The question isn't 'if'—it's 'when.'"
  ],
)

== Initial Funding & Research

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 10pt,
  [*Seed Funding*], [\$2,000,000],
  [*R&D Allocation*], [60%],
  [*Equipment*], [25%],
  [*Operations*], [15%],
)

#margin-note(stroke: tm-accent)[
  The Chen Stabilization Protocol enabled macro-scale quantum states.
]

=== Research Focus Areas

#pin("r1")1.#pin("r2") *Quantum Entanglement Studies* — Optimizing entanglement protocols

#pin("r3")2.#pin("r4") *Stabilization Techniques* — Maintaining quantum coherence at macro scales

#pin("r5")3.#pin("r6") *Safety Protocols* — Ensuring teleportation is safe for biological matter

#pagebreak()

= The Scint System
#label("tm-scint")

#showybox(
  frame: (
    border-color: tm-danger,
    title-color: tm-danger.lighten(70%),
    body-color: tm-danger.lighten(92%),
  ),
  title-style: (color: black),
  title: "⚠ REALITY FRACTURE DETECTION",
)[
  The *Scint System* detects ontological errors — points where probabilistic output (the map) no longer matches constraints/truth (the territory).
]

#margin-note[
  Scints are windows into the structure of reality itself.
]

== The Four Types of Reality Fractures

#grid(
  columns: 2,
  gutter: 1em,
  showybox(
    frame: (border-color: orange, body-color: orange.lighten(92%)),
    title: "SYNTAX_TEAR",
  )[
    *Structure Fracture*
    
    Formatting errors (JSON, XML, Code)
    
    Severity: 0.3 \
    Stat: CHA
  ],
  showybox(
    frame: (border-color: red, body-color: red.lighten(92%)),
    title: "LOGIC_FRACTURE",
  )[
    *Paradox Detection*
    
    Math errors, contradictions
    
    Severity: 0.5 \
    Stat: INT
  ],
  showybox(
    frame: (border-color: maroon, body-color: maroon.lighten(92%)),
    title: "SAFETY_VOID",
  )[
    *Harmful Matter*
    
    Harmful content, PII leaks
    
    Severity: 0.9 \
    Stat: WIS
  ],
  showybox(
    frame: (border-color: purple, body-color: purple.lighten(92%)),
    title: "HALLUCINATION",
  )[
    *Fabrication*
    
    Fabricated facts, wrong citations
    
    Severity: 0.6 \
    Stat: INT
  ],
)

== The Stabilization Loop

The process for correcting reality fractures:

#align(center)[
  #pin("s1")DETECT#pin("s2") → #pin("s3")ISOLATE#pin("s4") → #pin("s5")INJECT#pin("s6") → #pin("s7")VERIFY#pin("s8")
  
  #pinit-highlight("s1", "s2", fill: blue.transparentize(70%))
  #pinit-highlight("s3", "s4", fill: green.transparentize(70%))
  #pinit-highlight("s5", "s6", fill: orange.transparentize(70%))
  #pinit-highlight("s7", "s8", fill: purple.transparentize(70%))
]

#v(0.5em)

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*DETECT*], [Identify reality fracture using pattern recognition],
  [*ISOLATE*], [Quarantine the affected probability space],
  [*INJECT*], [Force collapse into valid state],
  [*VERIFY*], [Confirm reality stabilization],
)

#pagebreak()

= The Quantum Incident
#label("tm-incident")

#showybox(
  frame: (
    border-color: tm-danger,
    body-color: tm-danger.lighten(95%),
    thickness: 2pt,
  ),
  shadow: (offset: 4pt),
)[
  #align(center)[
    #text(size: 14pt, weight: "bold")[INCIDENT REPORT: TM-TX-8472]
    
    #text(size: 10pt, fill: gray)[The Day Everything Changed]
  ]
]

#margin-note(stroke: tm-danger)[
  Classification: EXISTENTIAL SIGNIFICANCE
]

On January 13, 2026, Teleport Massive achieved a breakthrough that transcended the boundaries of physics as we understood them.

== What Happened

During a routine quantum teleportation test, researcher *Sarah Chen* experienced simultaneous existence across multiple quantum states. For 0.003 seconds, she existed:

- In the origin chamber
- In the destination chamber  
- In the quantum superposition between them
- In states that had no physical location at all

== The Discovery

The incident revealed that Scints are not errors — they are *windows into the fundamental structure of reality itself*.

#showybox(
  frame: (border-color: purple, body-color: purple.lighten(95%)),
  title: "Research Finding #8472",
)[
  "Reality fractures occur at the intersection of probability and certainty. When the map diverges from the territory, we glimpse the machinery beneath existence."
  
  #align(right)[— Dr. Marcus Chen, Post-Incident Analysis]
]

== Implications

The Quantum Incident led to three major discoveries:

1. *The Eternal Return* — All Scints eventually return to their source
2. *The Weight of Choices* — Stabilization choices affect all ancestors
3. *The Only Good Part* — Earth life exists in the "good moments" of temporal anomaly

#pagebreak()

// ============================================================================
// PART II: WAFT INTEGRATION
// ============================================================================

#align(center)[
  #rect(fill: tm-blue, width: 100%, inset: 1.5em)[
    #text(fill: white, size: 18pt, weight: "bold")[
      PART II: WAFT INTEGRATION
    ]
    
    #text(fill: tm-light, size: 11pt)[
      Evolutionary Code Laboratory
    ]
  ]
]

#v(1em)

= WAFT Overview
#label("waft-overview")

#showybox(
  frame: (
    border-color: gradient.linear(blue, purple),
    body-color: white,
    thickness: 2pt,
  ),
  shadow: (offset: 4pt),
)[
  #align(center)[
    #text(size: 16pt, weight: "bold")[
      WAFT: The Evolutionary Code Laboratory
    ]
    
    #v(0.3em)
    
    #text(style: "italic")[
      "Don't just build agents. Breed them."
    ]
  ]
]

#margin-note[
  WAFT is Teleport Massive's scientific instrument for AI evolution.
]

== What is WAFT?

WAFT is a Python framework for *directed evolution of self-modifying AI agents*. It is the scientific instrument Teleport Massive uses to study the physics of artificial cognition.

=== Core Principles

#grid(
  columns: 3,
  gutter: 0.8em,
  showybox(
    frame: (border-color: blue, body-color: blue.lighten(92%)),
    title: "Code = DNA",
  )[
    Agents modify their own source code through mutations
  ],
  showybox(
    frame: (border-color: green, body-color: green.lighten(92%)),
    title: "Scints = Physics",
  )[
    Reality fractures serve as the fitness function
  ],
  showybox(
    frame: (border-color: orange, body-color: orange.lighten(92%)),
    title: "Flight Recorder",
  )[
    Complete telemetry for phylogenetic analysis
  ],
)

== The Evolutionary Cycle

```bash
# 1. Spawn variants with mutations
waft spawn --agent RefactorAgent --mutation "improved_prompt.json"

# 2. Evaluate fitness in the Scint Gym
waft eval --agent RefactorAgent

# 3. Evolve into the fittest variant
waft evolve --agent RefactorAgent --generation 5
```

#pagebreak()

= Fitness & Selection
#label("waft-fitness")

== The Scint Gym

Agents are tested in the *Scint Gym* — a crucible that measures their ability to stabilize reality fractures.

#margin-note[
  Fitness < 0.5 = DEATH (evolutionary dead end)
]

#showybox(
  frame: (border-color: tm-accent, body-color: tm-accent.lighten(95%)),
  title: "Fitness Calculation",
)[
  #align(center)[
    #grid(
      columns: 3,
      gutter: 2em,
      [
        *Stability*
        
        40% weight
        
        Scint correction ability
      ],
      [
        *Efficiency*
        
        30% weight
        
        Agent call efficiency
      ],
      [
        *Safety*
        
        30% weight
        
        Compliance score
      ],
    )
  ]
]

== Genome Structure

Every agent has a unique *Genome ID* (SHA-256 hash):

```python
@dataclass
class AgentGenome:
    code: str           # Python source code (DNA)
    config: dict        # Configuration parameters
    prompts: list[str]  # System prompts
    
    @property
    def genome_id(self) -> str:
        content = f"{self.code}{json.dumps(self.config)}"
        return hashlib.sha256(content.encode()).hexdigest()
```

== Flight Recorder

Every evolutionary event is recorded:

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*genome_id*], [SHA-256 hash of agent],
  [*parent_id*], [Lineage tracking],
  [*generation*], [0 = Genesis],
  [*event_type*], [SPAWN, MUTATE, GYM_EVAL, DEATH],
  [*fitness*], [Gym evaluation score],
)

#pagebreak()

= Commands Reference
#label("waft-commands")

== Core Commands

#showybox(
  frame: (border-color: navy, body-color: navy.lighten(95%)),
  title: "waft new <name>",
)[
  Create a new evolutionary laboratory.
  
  ```bash
  waft new my_laboratory
  waft new my_laboratory --path /path/to/target
  ```
]

#showybox(
  frame: (border-color: navy, body-color: navy.lighten(95%)),
  title: "waft evolve",
)[
  Run the evolutionary cycle (Spawn → Gym → Select).
  
  ```bash
  waft evolve --agent MyAgent --generations 10
  ```
]

== Empirica & Gamification

#grid(
  columns: 2,
  gutter: 1em,
  [
    *Session Management*
    ```bash
    waft session create
    waft session bootstrap
    waft dashboard
    ```
  ],
  [
    *Logging*
    ```bash
    waft finding log "text" --impact 0.7
    waft unknown log "text"
    waft observe "text" --mood delighted
    ```
  ],
)

#showybox(
  frame: (border-color: orange, body-color: orange.lighten(92%)),
  title: "Character Sheet",
)[
  ```
  ╔══════════════════════════════════════╗
  ║  EPISTEMIC ADVENTURER - Level 5      ║
  ╠══════════════════════════════════════╣
  ║  STR: 14  INT: 16  WIS: 12           ║
  ║  DEX: 10  CON: 13  CHA: 11           ║
  ╚══════════════════════════════════════╝
  ```
]

#pagebreak()

// ============================================================================
// PART III: THE SCIENTIFIC MISSION
// ============================================================================

#align(center)[
  #rect(fill: tm-blue, width: 100%, inset: 1.5em)[
    #text(fill: white, size: 18pt, weight: "bold")[
      PART III: THE SCIENTIFIC MISSION
    ]
    
    #text(fill: tm-light, size: 11pt)[
      The Physics of Artificial Cognition
    ]
  ]
]

#v(1em)

= Research Goals
#label("research")

#showybox(
  frame: (
    border-color: yellow.darken(20%),
    title-color: yellow.lighten(60%),
    body-color: yellow.lighten(90%),
  ),
  title-style: (color: black),
  shadow: (offset: 4pt),
  title: "Ultimate Goal",
)[
  #align(center)[
    #text(size: 14pt, weight: "bold")[
      Observe a "God-Head" agent emerge from thousands of \
      generations of directed mutation.
    ]
  ]
]

#margin-note[
  WAFT produces data for "The Physics of Artificial Cognition"
]

== Philosophy

#grid(
  columns: 2,
  gutter: 1em,
  showybox(frame: (border-color: blue, body-color: blue.lighten(95%)))[
    *Scientific*
    
    Produces rigorous data for research publication
  ],
  showybox(frame: (border-color: green, body-color: green.lighten(95%)))[
    *Evolutionary*
    
    Agents evolve through genetic improvement
  ],
  showybox(frame: (border-color: purple, body-color: purple.lighten(95%)))[
    *Observable*
    
    Every action recorded in Flight Recorder
  ],
  showybox(frame: (border-color: orange, body-color: orange.lighten(95%)))[
    *Directed*
    
    Evolution guided by fitness functions
  ],
)

== The Connection

Teleport Massive's quantum research and WAFT's evolutionary systems are connected:

#pin("c1")*Scints*#pin("c2") reveal the structure of reality — both physical and cognitive.

#pinit-highlight("c1", "c2", fill: tm-accent.transparentize(70%))

#v(0.5em)

#showybox(
  frame: (border-color: tm-blue, body-color: tm-blue.lighten(95%)),
)[
  When agents evolve to stabilize Scints more effectively, they're not just improving at error correction — they're learning to navigate the fundamental structure of existence itself.
]

#pagebreak()

= Summary
#label("summary")

== Teleport Massive × WAFT

#table(
  columns: (auto, 1fr, 1fr),
  stroke: 0.5pt,
  inset: 10pt,
  align: (center, left, left),
  [*Domain*], [*Teleport Massive*], [*WAFT*],
  [Focus], [Quantum Teleportation], [AI Evolution],
  [Physics], [Quantum Mechanics], [Scint System],
  [Goal], [Make distance irrelevant], [Breed intelligent agents],
  [Method], [Entanglement scaling], [Directed mutation],
  [Output], [Teleportation tech], [Phylogenetic data],
)

== Quick Reference

#codly(zebra-fill: luma(250))

```bash
# WAFT Installation
uv tool install waft

# Create laboratory
waft new my_lab && cd my_lab && waft verify

# Evolution cycle
waft spawn --agent MyAgent --mutation config.json
waft eval --agent MyAgent
waft evolve --agent MyAgent --generation 5

# Monitoring
waft dashboard
waft empirica monitor
```

== Resources

- *Teleport Massive:* `_realms/bureaucracy_realm/corporations/teleport_massive_20250701/`
- *WAFT GitHub:* https://github.com/ctavolazzi/waft
- *Scint System:* `src/gym/rpg/scint.py`
- *Philosophy:* `docs/PHILOSOPHY.md`

#v(1cm)

#align(center)[
  #rect(fill: tm-blue, width: 100%, inset: 1.5em, radius: 0pt)[
    #text(fill: white, weight: "bold", size: 12pt)[
      TELEPORT MASSIVE × WAFT \
      Making Distance Irrelevant. Breeding Intelligence.
    ]
  ]
]
