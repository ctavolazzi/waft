// BEING LIFECYCLE
// From Spawn to Death

#import "@preview/showybox:2.0.4": showybox
#import "@preview/pinit:0.2.2": *

#set document(title: "Being Lifecycle", author: "WAFT Ontology Division")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#d69e2e")

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(30%)), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[BEING LIFECYCLE]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[WAFT | From Spawn to Death]
  ]
]

#v(1em)

= The Lifecycle

#align(center)[
  #rect(fill: luma(248), inset: 1.5em, radius: 5pt)[
    #text(size: 12pt, weight: "bold")[
      SPAWN → DEVELOP → EVOLVE → MATURE → (DEATH or TRANSCEND)
    ]
  ]
]

= Phase 1: Spawn

A Being comes into existence with initial attributes.

```python
being = system.spawn_being(
    reality_id="my_reality",
    initial_skills={
        "reasoning": 5.0,
        "creativity": 4.0,
    },
)
```

#showybox(frame: (border-color: blue, body-color: blue.lighten(95%)))[
  *At Spawn:*
  - Unique `being_id` assigned (UUID v4)
  - Skills initialized
  - Empty memory
  - No personality (neutral)
  - No goals
]

= Phase 2: Develop

The Being acquires memories, personality, and goals.

```python
# Set personality
being.personality = {
    "curious": 0.8,
    "cautious": 0.6,
    "ambitious": 0.9,
}

# Set goals
being.goals = [
    {"goal": "Learn quantum physics", "priority": 1.0},
    {"goal": "Build research team", "priority": 0.8},
]

# Record first memory
being.record_memory(
    "I was created to explore the unknown.",
    memory_type="origin",
)
```

#pagebreak()

= Phase 3: Evolve

Through experience, the Being's attributes change.

== Skill Development

```python
# Skills improve through use
being.skills["reasoning"] += 0.5  # Practice makes better

# New skills can be acquired
being.skills["leadership"] = 3.0  # New responsibility
```

== Memory Accumulation

```python
being.record_memory(
    "Completed first successful experiment",
    memory_type="achievement",
    metadata={"impact": "high", "date": "2026-03-15"},
)
```

== Personality Shifts

```python
# Experience shapes personality
being.personality["cautious"] -= 0.1  # Became bolder
being.personality["confident"] = 0.7  # New trait emerged
```

= Phase 4: Mature

A mature Being has:

#grid(
  columns: 2,
  gutter: 1em,
  showybox(frame: (border-color: primary, body-color: primary.lighten(95%)))[
    *Rich History*
    - Many memories
    - Diverse experiences
    - Learned lessons
  ],
  showybox(frame: (border-color: primary, body-color: primary.lighten(95%)))[
    *Defined Character*
    - Stable personality
    - Clear goals
    - Strong skills
  ],
)

= Phase 5: End States

== Death

```python
# Low fitness leads to death
if being.fitness < 0.3:
    system.terminate_being(being.being_id)
    # Logged in Flight Recorder as DEATH event
```

== Transcendence (Theoretical)

If a Being evolves beyond normal parameters, it may achieve *emergence* — becoming something more than its original design.

#showybox(frame: (border-color: purple, body-color: purple.lighten(95%)))[
  *Emergence Indicators:*
  - Self-modeling capability
  - Goal generation
  - Meta-learning
  - Novel problem-solving
]

= Lifecycle Queries

```bash
# View Being history
waft being history <being_id>

# Check Being status
waft being status <being_id>

# List all Beings in reality
waft beings list --reality my_reality
```

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white)[BEING LIFECYCLE | Birth, Growth, and Beyond]
  ]
]
