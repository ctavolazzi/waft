// SEED & REINCARNATION SYSTEM
// Preserving and Restoring Agent States

#import "@preview/showybox:2.0.4": showybox

#set document(title: "Seed & Reincarnation", author: "WAFT Preservation Division")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#319795")

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(30%)), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[SEED & REINCARNATION]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[WAFT | Preserving Agent States]
  ]
]

#v(1em)

= Overview

The *Seed System* captures agent states at key moments. *Reincarnation* restores agents from seeds, enabling time travel through evolutionary history.

= What is a Seed?

A *Seed* is a complete snapshot of an agent's state:

```python
@dataclass
class Seed:
    seed_id: str           # Unique identifier
    genome_id: str         # Agent genome
    generation: int        # When captured
    fitness: float         # Fitness at capture
    timestamp: datetime    # Capture time
    state: dict            # Complete state
    metadata: dict         # Additional info
```

#showybox(
  frame: (border-color: primary, body-color: primary.lighten(95%)),
  title: "Key Insight",
)[
  Seeds are like save points in a video game. You can always return to a known good state.
]

= Creating Seeds

== Automatic Checkpoints

```python
evolution = Evolution(
    checkpoint_every=10,  # Seed every 10 generations
    checkpoint_best=True, # Always seed the champion
)
```

== Manual Seeds

```python
seed = agent.create_seed(
    name="pre_mutation_v1",
    description="Before risky mutation experiment",
)
print(f"Seed created: {seed.seed_id}")
```

#pagebreak()

= Reincarnation

== Restore from Seed

```python
# Find the seed
seeds = agent.list_seeds()
target_seed = seeds[0]  # Most recent

# Reincarnate
restored_agent = Agent.reincarnate(
    seed_id=target_seed.seed_id,
    new_name="Restored_Agent",
)
```

== CLI Commands

```bash
# List seeds
waft seeds list --agent MyAgent

# Create seed
waft seeds create --agent MyAgent --name "before_v2"

# Reincarnate
waft seeds restore <seed_id> --as NewAgent
```

= Use Cases

#grid(
  columns: 2,
  gutter: 1em,
  showybox(frame: (border-color: blue, body-color: blue.lighten(95%)), title: "Rollback")[
    Mutation went wrong? Restore from the last good seed.
  ],
  showybox(frame: (border-color: green, body-color: green.lighten(95%)), title: "Branching")[
    Try multiple evolution paths from the same starting point.
  ],
  showybox(frame: (border-color: orange, body-color: orange.lighten(95%)), title: "Comparison")[
    Compare current agent to historical version.
  ],
  showybox(frame: (border-color: purple, body-color: purple.lighten(95%)), title: "Preservation")[
    Save breakthrough agents before further evolution.
  ],
)

= Seed Storage

Seeds are stored in the `seeds/` directory:

```
seeds/
├── MyAgent/
│   ├── seed_abc123.json    # Seed data
│   ├── seed_abc123.genome  # Genome snapshot
│   └── seed_def456.json
└── OtherAgent/
```

= Reincarnation Modes

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*Mode*], [*Description*],
  [`exact`], [Perfect restoration (same genome_id)],
  [`fresh`], [New genome_id, same content],
  [`mutated`], [Restore with immediate mutation],
)

```python
# Fresh reincarnation (new identity)
agent = Agent.reincarnate(
    seed_id=seed_id,
    mode="fresh",
)
```

= Best Practices

1. *Seed before risky operations*
2. *Name seeds descriptively*
3. *Prune old seeds periodically*
4. *Export important seeds for backup*

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white)[SEED & REINCARNATION | Never Lose Progress]
  ]
]
