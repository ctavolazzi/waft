// MULTI-AGENT COORDINATION
// Running Agent Teams

#import "@preview/showybox:2.0.4": showybox

#set document(title: "Multi-Agent Coordination", author: "WAFT Swarm Division")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#e53e3e")

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(30%)), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[MULTI-AGENT]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[WAFT | Coordination & Swarms]
  ]
]

#v(1em)

= Overview

WAFT supports running multiple agents simultaneously, enabling coordination, competition, and collective problem-solving.

= Coordination Patterns

#grid(
  columns: 2,
  gutter: 1em,
  showybox(frame: (border-color: blue, body-color: blue.lighten(95%)), title: "Pipeline")[
    Agents process sequentially:
    ```
    A → B → C → Output
    ```
    Each agent refines the previous output.
  ],
  showybox(frame: (border-color: green, body-color: green.lighten(95%)), title: "Parallel")[
    Agents process simultaneously:
    ```
    A ─┬─ Output
    B ─┤
    C ─┘
    ```
    Results are aggregated.
  ],
  showybox(frame: (border-color: orange, body-color: orange.lighten(95%)), title: "Debate")[
    Agents argue positions:
    ```
    A ←→ B
      ↓
    Judge → Decision
    ```
    A third agent decides.
  ],
  showybox(frame: (border-color: purple, body-color: purple.lighten(95%)), title: "Hierarchy")[
    Manager delegates to workers:
    ```
    Manager
    ├─ Worker A
    ├─ Worker B
    └─ Worker C
    ```
  ],
)

= Creating a Team

```python
from waft.teams import Team, Pipeline

# Create a pipeline team
team = Team(
    name="review_pipeline",
    pattern="pipeline",
    agents=[
        CodeAgent(name="coder"),
        ReviewAgent(name="reviewer"),
        TestAgent(name="tester"),
    ],
)

# Run the team
result = team.process("Write a sorting algorithm")
```

#pagebreak()

= Parallel Execution

```python
from waft.teams import ParallelTeam

team = ParallelTeam(
    agents=[Agent1(), Agent2(), Agent3()],
    aggregator="vote",  # or "merge", "best"
)

results = team.process("Solve this problem")
# Returns aggregated result from all agents
```

= Debate Pattern

```python
from waft.teams import DebateTeam

team = DebateTeam(
    proponent=Agent(role="argue_for"),
    opponent=Agent(role="argue_against"),
    judge=Agent(role="decide"),
    rounds=3,
)

decision = team.debate("Should we implement feature X?")
```

= Evolution with Teams

Teams can evolve together:

```python
evolution = TeamEvolution(
    team_template=MyTeam,
    population_size=10,
    fitness_fn=team_fitness,
)

# Evolve team composition and coordination
best_team = evolution.run(generations=20)
```

= Communication Protocols

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*Protocol*], [*Description*],
  [`broadcast`], [One agent sends to all],
  [`direct`], [Point-to-point messaging],
  [`publish`], [Agents subscribe to topics],
  [`blackboard`], [Shared memory space],
)

= CLI Commands

```bash
# Create team
waft team create review_pipeline --pattern pipeline

# Add agents to team
waft team add review_pipeline --agent CodeAgent --role coder

# Run team
waft team run review_pipeline --input "task description"

# Evolve team
waft team evolve review_pipeline --generations 10
```

= Best Practices

1. *Start simple* — Pipeline before complex patterns
2. *Define clear roles* — Each agent has one job
3. *Use appropriate aggregation* — Vote for consensus, best for competition
4. *Monitor communication* — Log inter-agent messages
5. *Evolve holistically* — Team fitness > individual fitness

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white)[MULTI-AGENT | Stronger Together]
  ]
]
