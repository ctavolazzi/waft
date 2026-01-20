// FLIGHT RECORDER DOCUMENTATION
// The Fossil Record of Artificial Cognition

#import "@preview/showybox:2.0.4": showybox
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *

#set document(title: "Flight Recorder Guide", author: "WAFT Documentation Team")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#show: codly-init.with()
#codly(languages: codly-languages)

#let primary = rgb("#2b6cb0")
#let secondary = rgb("#2c5282")

#align(center)[
  #rect(fill: gradient.linear(primary, secondary), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[FLIGHT RECORDER]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[The Fossil Record of Artificial Cognition]
  ]
]

#v(1em)

= Purpose

The *Flight Recorder* captures every evolutionary event in WAFT. Like a black box on an aircraft, it provides complete telemetry for understanding what happened and why.

#showybox(
  frame: (border-color: primary, body-color: primary.lighten(95%)),
  title: "Why It Matters",
)[
  WAFT produces scientific data. The Flight Recorder ensures that data is complete, traceable, and reproducible. Future researchers can study the phylogenetic history of any agent lineage.
]

= Event Types

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 10pt,
  [*Event*], [*Description*],
  [`SPAWN`], [New agent created (generation 0)],
  [`MUTATE`], [Agent genome modified],
  [`GYM_EVAL`], [Agent evaluated in Scint Gym],
  [`BREED`], [Two agents combined to create offspring],
  [`DEATH`], [Agent removed from population (fitness < threshold)],
  [`CHECKPOINT`], [Periodic state snapshot],
  [`EMERGENCE`], [Potential God-Head behavior detected],
)

= Event Schema

Every event follows a consistent structure:

```json
{
  "event_id": "evt_abc123...",
  "timestamp": "2026-01-20T00:15:30Z",
  "event_type": "GYM_EVAL",
  "genome_id": "sha256:def456...",
  "parent_id": "sha256:ghi789...",
  "generation": 5,
  "fitness": 0.73,
  "metadata": {
    "scints_encountered": 10,
    "scints_stabilized": 7,
    "tokens_used": 4521,
    "duration_ms": 12340
  }
}
```

#pagebreak()

= Querying the Flight Recorder

== List Recent Events

```bash
waft flight list --limit 20
```

== Filter by Event Type

```bash
waft flight query --type GYM_EVAL --since "1 day ago"
```

== Filter by Agent

```bash
waft flight query --genome sha256:abc123...
```

== Show Full Event Details

```bash
waft flight show evt_abc123...
```

= Lineage Tracing

== View Agent Ancestry

```bash
waft flight lineage sha256:abc123... --depth 10
```

Output:
```
Generation 0: sha256:root... (SPAWN)
    └── Generation 1: sha256:mut1... (MUTATE, fitness: 0.52)
        └── Generation 2: sha256:mut2... (MUTATE, fitness: 0.61)
            └── Generation 3: sha256:bred... (BREED, fitness: 0.68)
                └── Generation 4: sha256:mut3... (MUTATE, fitness: 0.71)
                    └── Generation 5: sha256:abc123... (current, fitness: 0.73)
```

== Compare Lineages

```bash
waft flight compare sha256:abc... sha256:def...
```

= Data Export

== JSON Export

```bash
waft flight export --format json --output events.json
```

== CSV Export

```bash
waft flight export --format csv --output events.csv
```

== Phylogenetic Tree

```bash
waft flight tree --format newick --output tree.nwk
```

= Analysis Tools

== Fitness Over Time

```python
from waft.flight import FlightRecorder

recorder = FlightRecorder()
events = recorder.query(
    event_type="GYM_EVAL",
    since="7 days ago",
)

# Plot fitness trajectory
import matplotlib.pyplot as plt
generations = [e.generation for e in events]
fitness = [e.fitness for e in events]
plt.scatter(generations, fitness)
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.show()
```

== Mutation Impact Analysis

```python
# Find which mutations improved fitness
improvements = recorder.find_improvements(
    min_delta=0.05,  # At least 5% improvement
)

for imp in improvements:
    print(f"Mutation at gen {imp.generation}:")
    print(f"  Before: {imp.parent_fitness:.2f}")
    print(f"  After: {imp.child_fitness:.2f}")
    print(f"  Delta: +{imp.delta:.2f}")
```

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white, size: 10pt)[
      FLIGHT RECORDER | Every Evolution, Recorded
    ]
  ]
]
