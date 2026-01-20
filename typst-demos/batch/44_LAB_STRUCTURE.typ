// LABORATORY STRUCTURE
// Organizing Your Evolution Workspace

#import "@preview/showybox:2.0.4": showybox

#set document(title: "Laboratory Structure", author: "WAFT Organization")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#4a5568")

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(30%)), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[LABORATORY STRUCTURE]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[WAFT | Workspace Organization]
  ]
]

#v(1em)

= Overview

A WAFT *Laboratory* is a directory containing everything needed for agent evolution. Understanding the structure helps you work effectively.

= Directory Layout

```
my_lab/
├── waft.toml              # Configuration
├── agents/                # Agent source code
│   ├── __init__.py
│   ├── base_agent.py
│   └── custom_agents/
├── prompts/               # System prompts
│   ├── default.txt
│   └── specialized/
├── mutations/             # Mutation configs
│   └── standard.json
├── checkpoints/           # Evolution snapshots
│   └── gen_050/
├── seeds/                 # Agent state saves
│   └── MyAgent/
├── flight_data/           # Telemetry database
│   └── flight.db
├── results/               # Output files
│   ├── reports/
│   └── exports/
└── logs/                  # Application logs
```

= Key Files

== waft.toml

Main configuration:

```toml
[project]
name = "my_lab"
version = "0.1.0"

[evolution]
population_size = 20
mutation_rate = 0.1

[gym]
timeout_seconds = 300

[storage]
database = "flight_data/flight.db"
```

#pagebreak()

== agents/

Your agent source code:

```python
# agents/my_agent.py
from waft import Agent

class MyAgent(Agent):
    system_prompt = "..."
    
    def process(self, input: str) -> str:
        return self.llm.generate(...)
```

== prompts/

Reusable system prompts:

```
prompts/
├── default.txt        # Standard prompt
├── code_review.txt    # For code agents
├── research.txt       # For research agents
└── safety_focused.txt # High safety emphasis
```

= Working with Laboratories

== Create

```bash
waft new my_lab
cd my_lab
```

== Verify

```bash
waft verify
waft verify --fix  # Auto-fix issues
```

== Status

```bash
waft status
```

Output:
```
Laboratory: my_lab
Agents: 3
Generations: 47
Best Fitness: 0.823
Last Run: 2 hours ago
```

= Multiple Laboratories

You can have multiple labs for different experiments:

```bash
waft new experiment_a
waft new experiment_b

# Work in specific lab
cd experiment_a
waft evolve ...

# Or specify lab
waft --lab experiment_b evolve ...
```

= Backup & Export

```bash
# Backup entire lab
waft lab backup --output my_lab_backup.zip

# Export just results
waft lab export --results-only

# Clone lab
waft lab clone my_lab my_lab_copy
```

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white)[LABORATORY STRUCTURE | Organization Matters]
  ]
]
