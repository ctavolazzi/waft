// BEINGS & REALITIES GUIDE
// Understanding the WAFT Ontology System

#import "@preview/showybox:2.0.4": showybox
#import "@preview/pinit:0.2.2": *

#set document(title: "Beings & Realities Guide", author: "WAFT Documentation Team")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#3182ce")
#let secondary = rgb("#805ad5")

#align(center)[
  #rect(fill: gradient.linear(primary, secondary), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[BEINGS & REALITIES]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[WAFT Ontology System Guide]
  ]
]

#v(1em)

= Introduction

WAFT's ontology system models *Beings* (autonomous entities) existing within *Realities* (simulation contexts). This guide explains the core concepts.

= What is a Being?

A *Being* is an autonomous entity with:

#grid(
  columns: 3,
  gutter: 1em,
  showybox(frame: (border-color: primary, body-color: primary.lighten(92%)))[
    *Identity*
    
    Unique ID, name, and persistent state
  ],
  showybox(frame: (border-color: primary, body-color: primary.lighten(92%)))[
    *Cognition*
    
    Skills, memories, goals, and personality
  ],
  showybox(frame: (border-color: primary, body-color: primary.lighten(92%)))[
    *Agency*
    
    Ability to act, learn, and evolve
  ],
)

== Being Attributes

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 10pt,
  [*Attribute*], [*Description*],
  [`being_id`], [UUID v4 unique identifier],
  [`reality_id`], [Which reality the Being exists in],
  [`custom_name`], [Optional human-readable name],
  [`skills`], [Dictionary of skill → proficiency (0-10)],
  [`personality`], [Dictionary of trait → intensity (0-1)],
  [`goals`], [List of objectives with priorities],
  [`memories`], [Recorded experiences and knowledge],
)

= What is a Reality?

A *Reality* is a simulation context where Beings exist. Think of it as a "universe" with its own rules, history, and inhabitants.

#showybox(
  frame: (border-color: secondary, body-color: secondary.lighten(92%)),
  title: "Reality Structure",
)[
  ```
  _realms/
  └── bureaucracy_realm/
      └── corporations/
          └── teleport_massive_20250701/
              ├── manifest.json      # Reality metadata
              ├── founders.json      # Being references
              ├── departments/       # Organizational structure
              └── history/           # Event log
  ```
]

#pagebreak()

= The Being System

== Spawning Beings

```python
from waft.being import BeingSystem

system = BeingSystem(project_path=Path("."))

# Spawn a new Being
being = system.spawn_being(
    reality_id="teleport_massive_20250701",
    initial_skills={
        "quantum_physics": 8.5,
        "leadership": 7.0,
    }
)

# Customize the Being
being.custom_name = "Dr. Elena Voss"
being.personality = {"visionary": 0.9, "determined": 0.85}
being.goals = [{"goal": "Scale quantum teleportation", "priority": 1.0}]
```

== Recording Memories

Beings accumulate memories that shape their behavior:

```python
being.record_memory(
    "Achieved breakthrough in quantum stabilization",
    memory_type="achievement",
    metadata={
        "date": "2026-01-15",
        "impact": "high",
        "witnesses": ["Marcus Chen", "Sarah Kim"]
    }
)
```

== Skill Development

Skills improve through experience:

```python
# Skills range from 0 (novice) to 10 (master)
being.skills["quantum_physics"] = 9.5  # Expertise gained
being.skills["management"] = 6.0       # New skill acquired
```

= Reality Management

== Creating Realities

```python
from waft.core.corporations_system import CorporationsSystem

corps = CorporationsSystem(project_path=Path("."))

# Create a new corporate reality
corp = corps.create_corporation(
    name="Teleport Massive",
    sector="Quantum Teleportation Technology",
    mission="Make distance irrelevant",
    founded_date=datetime(2025, 7, 1),
    initial_capital=Decimal("2000000"),
)
```

== Assigning Beings to Realities

```python
# Hire Being into corporation
corp.hire_employee(
    being_id=being.being_id,
    role="CEO",
    department="Executive",
    title="Chief Executive Officer",
    level=10,
    salary=Decimal("180000"),
)
```

= Key Concepts

#grid(
  columns: 2,
  gutter: 1em,
  showybox(frame: (border-color: blue))[
    *Persistence*
    
    Beings and Realities are saved to disk as JSON. State survives across sessions.
  ],
  showybox(frame: (border-color: green))[
    *Autonomy*
    
    Beings can make decisions based on their goals, skills, and memories.
  ],
  showybox(frame: (border-color: orange))[
    *Evolution*
    
    Through the Scint Gym, Beings can evolve and improve over time.
  ],
  showybox(frame: (border-color: purple))[
    *Relationships*
    
    Beings can interact, collaborate, and form organizational structures.
  ],
)

#v(1em)

#align(center)[
  #text(size: 9pt, fill: gray)[
    WAFT Beings System | "Don't just build agents. Breed them."
  ]
]
