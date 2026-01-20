// WAFT SYSTEM ARCHITECTURE
// Technical Overview for Developers

#import "@preview/showybox:2.0.4": showybox
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *

#set document(title: "WAFT Architecture", author: "WAFT Development Team")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#show: codly-init.with()
#codly(languages: codly-languages)

#let primary = rgb("#4a5568")
#let secondary = rgb("#2d3748")

#align(center)[
  #rect(fill: gradient.linear(primary, secondary), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[WAFT ARCHITECTURE]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[Technical Overview for Developers]
  ]
]

#v(1em)

= System Overview

WAFT is built on a modular architecture designed for extensibility and scientific rigor.

#align(center)[
  #showybox(frame: (border-color: primary))[
    ```
    ┌─────────────────────────────────────────────┐
    │                   CLI Layer                 │
    │  (waft new, waft evolve, waft gym, etc.)    │
    ├─────────────────────────────────────────────┤
    │               Core Services                 │
    │  ┌─────────┐ ┌─────────┐ ┌─────────┐       │
    │  │Evolution│ │Scint Gym│ │ Flight  │       │
    │  │ Engine  │ │         │ │Recorder │       │
    │  └─────────┘ └─────────┘ └─────────┘       │
    ├─────────────────────────────────────────────┤
    │              Agent Framework                │
    │  ┌─────────┐ ┌─────────┐ ┌─────────┐       │
    │  │ Genome  │ │Mutation │ │ Fitness │       │
    │  │ Manager │ │ Engine  │ │ Scorer  │       │
    │  └─────────┘ └─────────┘ └─────────┘       │
    ├─────────────────────────────────────────────┤
    │             Storage Layer                   │
    │     (SQLite, JSON, File System)             │
    └─────────────────────────────────────────────┘
    ```
  ]
]

= Core Components

== Evolution Engine

The heart of WAFT. Manages populations, runs selection, and coordinates breeding.

```python
class EvolutionEngine:
    def __init__(self, config: EvolutionConfig):
        self.population: list[Agent] = []
        self.generation: int = 0
        self.flight_recorder = FlightRecorder()
    
    def run_generation(self) -> GenerationResult:
        # 1. Evaluate all agents
        scores = self.evaluate_population()
        
        # 2. Select survivors
        survivors = self.select(scores)
        
        # 3. Breed next generation
        offspring = self.breed(survivors)
        
        # 4. Apply mutations
        mutated = self.mutate(offspring)
        
        # 5. Record and return
        self.flight_recorder.log_generation(...)
        return GenerationResult(...)
```

#pagebreak()

== Scint Gym

The fitness evaluation environment.

```python
class ScintGym:
    def __init__(self):
        self.scenarios: list[Scenario] = []
        self.detector = RegexScintDetector()
    
    def evaluate(self, agent: Agent) -> FitnessScore:
        results = []
        for scenario in self.scenarios:
            # Run agent against scenario
            response = agent.process(scenario.prompt)
            
            # Detect any Scints
            scints = self.detector.detect(response)
            
            # Score the result
            score = self.score(scenario, response, scints)
            results.append(score)
        
        return FitnessScore.aggregate(results)
```

== Flight Recorder

Complete telemetry for all evolutionary events.

```python
class FlightRecorder:
    def __init__(self, db_path: Path):
        self.db = sqlite3.connect(db_path)
    
    def log_event(self, event: Event) -> str:
        event_id = generate_event_id()
        self.db.execute("""
            INSERT INTO events 
            (id, timestamp, type, genome_id, metadata)
            VALUES (?, ?, ?, ?, ?)
        """, (event_id, event.timestamp, ...))
        return event_id
    
    def query(self, **filters) -> list[Event]:
        # Flexible querying by type, time, genome, etc.
        ...
```

= Directory Structure

```
waft/
├── src/waft/
│   ├── cli/           # Command-line interface
│   ├── core/          # Core business logic
│   │   ├── evolution/ # Evolution engine
│   │   ├── gym/       # Scint Gym
│   │   └── agents/    # Agent framework
│   ├── storage/       # Persistence layer
│   └── utils/         # Shared utilities
├── tests/             # Test suite
├── docs/              # Documentation
└── examples/          # Example usage
```

= Data Flow

#showybox(frame: (border-color: primary, body-color: luma(250)))[
  ```
  User Command
       │
       ▼
  ┌─────────┐     ┌─────────┐     ┌─────────┐
  │   CLI   │────▶│  Core   │────▶│ Storage │
  └─────────┘     └─────────┘     └─────────┘
       │               │               │
       │               ▼               │
       │         ┌─────────┐          │
       │         │  Agent  │          │
       │         │Framework│          │
       │         └─────────┘          │
       │               │               │
       │               ▼               │
       │         ┌─────────┐          │
       └────────▶│ Flight  │◀─────────┘
                 │Recorder │
                 └─────────┘
  ```
]

= Configuration

== waft.toml

```toml
[project]
name = "my_evolution_lab"
version = "0.1.0"

[evolution]
population_size = 20
mutation_rate = 0.1
selection_pressure = 0.5

[gym]
timeout_seconds = 300
parallel_workers = 4
scenarios = ["syntax", "logic", "safety", "hallucination"]

[storage]
database = "waft.db"
checkpoints_dir = "checkpoints/"
```

= Extension Points

== Custom Agents

```python
from waft import Agent

class MyAgent(Agent):
    def process(self, input: str) -> str:
        # Your implementation
        return result
```

== Custom Mutations

```python
from waft.mutations import Mutator

class MyMutator(Mutator):
    def mutate(self, genome: Genome) -> Genome:
        # Your mutation logic
        return mutated_genome
```

== Custom Fitness Functions

```python
from waft.gym import FitnessFunction

class MyFitness(FitnessFunction):
    def score(self, agent: Agent, scenario: Scenario) -> float:
        # Your scoring logic
        return score
```

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white, size: 10pt)[
      WAFT Architecture | Modular. Extensible. Scientific.
    ]
  ]
]
