// EXPERIMENT LOGGING
// Recording Scientific Data

#import "@preview/showybox:2.0.4": showybox

#set document(title: "Experiment Logging", author: "WAFT Science Division")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#2c5282")

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(30%)), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[EXPERIMENT LOGGING]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[WAFT | Recording Scientific Data]
  ]
]

#v(1em)

= Why Log Experiments?

WAFT produces scientific data. Proper logging ensures:
- *Reproducibility* — Others can replicate your results
- *Analysis* — You can study what happened
- *Publication* — Data for research papers
- *Learning* — Understand what works

= What Gets Logged

#grid(
  columns: 2,
  gutter: 1em,
  showybox(frame: (border-color: blue, body-color: blue.lighten(95%)), title: "Automatic")[
    - All Flight Recorder events
    - Gym evaluations
    - Mutations applied
    - Fitness scores
  ],
  showybox(frame: (border-color: green, body-color: green.lighten(95%)), title: "Manual")[
    - Experiment hypotheses
    - Observations
    - Configuration changes
    - Conclusions
  ],
)

= Experiment Structure

```python
from waft.experiments import Experiment

exp = Experiment(
    name="mutation_rate_study",
    hypothesis="Higher mutation rates escape local optima faster",
    variables={
        "independent": ["mutation_rate"],
        "dependent": ["fitness", "generations_to_plateau"],
        "controlled": ["population_size", "gym_scenarios"],
    },
)
```

#pagebreak()

= Running Experiments

```python
# Define conditions
conditions = [
    {"mutation_rate": 0.05},
    {"mutation_rate": 0.10},
    {"mutation_rate": 0.15},
    {"mutation_rate": 0.20},
]

# Run each condition
for condition in conditions:
    exp.run_trial(
        config=condition,
        generations=100,
        replicates=3,  # Run 3 times each
    )

# Analyze results
results = exp.analyze()
exp.save_results("results/mutation_study.json")
```

= Logging Observations

```python
# Manual observations
exp.log_observation(
    "Generation 45: Interesting behavior emerged. Agent started "
    "generating self-referential statements.",
    tags=["emergence", "unexpected"],
)

# Structured notes
exp.log_note(
    title="Plateau Detected",
    content="Fitness stuck at 0.73 for 10 generations",
    generation=55,
    action_taken="Increased mutation rate to 0.15",
)
```

= CLI Commands

```bash
# Create experiment
waft experiment create "mutation_study" \
    --hypothesis "Higher mutation escapes optima"

# Log observation
waft experiment log "Interesting behavior at gen 45"

# View experiment
waft experiment show mutation_study

# Export data
waft experiment export mutation_study --format csv
```

= Best Practices

1. *State hypothesis upfront* — What do you expect?
2. *Control variables* — Change one thing at a time
3. *Multiple replicates* — Run each condition 3+ times
4. *Log everything* — Better too much than too little
5. *Analyze promptly* — Review results while context is fresh

= Report Generation

```bash
# Generate experiment report
waft experiment report mutation_study --format pdf

# Include in publication
waft experiment export mutation_study --format latex
```

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white)[EXPERIMENT LOGGING | Science Requires Records]
  ]
]
