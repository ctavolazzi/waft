// EMPIRICA INTEGRATION GUIDE
// Epistemic Self-Assessment for AI Agents

#import "@preview/showybox:2.0.4": showybox
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *

#set document(title: "Empirica Guide", author: "WAFT Documentation Team")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#show: codly-init.with()
#codly(languages: codly-languages)

#let primary = rgb("#319795")
#let secondary = rgb("#2c7a7b")

#align(center)[
  #rect(fill: gradient.linear(primary, secondary), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[EMPIRICA]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[Epistemic Self-Assessment for AI Agents]
  ]
]

#v(1em)

= What is Empirica?

*Empirica* is an epistemic self-assessment system that helps AI agents (and humans) track what they know and learn. It quantifies knowledge across 13 vectors organized into 3 tiers.

#showybox(
  frame: (border-color: primary, body-color: primary.lighten(95%)),
  title: "Core Concept",
)[
  Before work: *What do I know?* (Preflight) \
  After work: *What did I learn?* (Postflight) \
  The difference = Quantified learning
]

= The 13 Epistemic Vectors

== Tier 0: Foundation

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*engagement*], [How focused/committed to the task],
  [*know*], [Factual knowledge about the domain],
  [*do*], [Procedural knowledge (how to)],
  [*context*], [Understanding of surrounding situation],
)

== Tier 1: Comprehension

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*clarity*], [How clear the understanding is],
  [*coherence*], [How well pieces fit together],
  [*signal*], [Signal-to-noise ratio],
  [*density*], [Information richness],
)

== Tier 2: Execution

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*state*], [Current system state awareness],
  [*change*], [Understanding of what changed],
  [*completion*], [Task completion level],
  [*impact*], [Effect of actions taken],
)

== Meta

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*uncertainty*], [Explicit tracking of unknowns],
)

#pagebreak()

= The CASCADE Workflow

#align(center)[
  #rect(fill: luma(248), inset: 1.5em, radius: 5pt)[
    #text(size: 12pt, weight: "bold")[
      PREFLIGHT → WORK → CHECK → POSTFLIGHT
    ]
  ]
]

== 1. Preflight (Before Work)

Assess what you know before starting:

```bash
echo '{
  "session_id": "abc-123",
  "vectors": {
    "engagement": 0.8,
    "foundation": {"know": 0.6, "do": 0.7, "context": 0.5},
    "comprehension": {"clarity": 0.7, "coherence": 0.8},
    "uncertainty": 0.4
  },
  "reasoning": "Starting with moderate OAuth2 knowledge..."
}' | empirica preflight-submit -
```

== 2. Work (Do the Task)

Log findings and unknowns as you work:

```bash
empirica finding-log --finding "Discovered token refresh" --impact 0.7
empirica unknown-log --unknown "Need to investigate scopes"
```

== 3. Check (Decision Points)

At critical junctures, run a check gate:

```bash
empirica check-submit -
```

Returns: `PROCEED` | `HALT` | `BRANCH` | `REVISE`

== 4. Postflight (After Work)

Measure what you actually learned:

```bash
echo '{
  "session_id": "abc-123",
  "vectors": {
    "foundation": {"know": 0.85, "do": 0.9},
    "uncertainty": 0.15
  },
  "reasoning": "Successfully implemented OAuth2"
}' | empirica postflight-submit -
```

*Result:* know: +0.25, uncertainty: -0.25 (quantified learning!)

#pagebreak()

= WAFT Integration

== Session Management

```bash
waft session create       # Start Empirica session
waft session bootstrap    # Load project context
waft session close        # End and summarize
```

== Logging Commands

```bash
waft finding log "text" --impact 0.7
waft unknown log "text"
waft observe "text" --mood delighted
```

== Dashboard

```bash
waft dashboard   # Launch monitoring UI
```

= Gamification

Empirica includes RPG elements to make epistemic tracking engaging:

== Character Sheet

```
╔══════════════════════════════════════╗
║  EPISTEMIC ADVENTURER - Level 5      ║
╠══════════════════════════════════════╣
║  STR: 14  INT: 16  WIS: 12           ║
║  DEX: 10  CON: 13  CHA: 11           ║
╠══════════════════════════════════════╣
║  XP: 2340/3000  Karma: +42           ║
╚══════════════════════════════════════╝
```

== Moon Phase Health Indicators

- 🌑 Critical (coverage < 25%)
- 🌒 Low (25-50%)
- 🌓 Moderate (50-75%)
- 🌔 Good (75-90%)
- 🌕 Excellent (90%+)

= Why This Matters

Traditional AI development doesn't track *what the AI knows*. Empirica changes that:

#showybox(frame: (border-color: primary, body-color: primary.lighten(95%)))[
  - *Accountability:* Know what was known when decisions were made
  - *Learning:* Quantify actual knowledge gain
  - *Safety:* Explicit uncertainty tracking prevents overconfidence
  - *Science:* Rigorous data for AI cognition research
]

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white, size: 10pt)[
      EMPIRICA | Know What You Know
    ]
  ]
]
