// FITNESS LANDSCAPE ANALYSIS
// Understanding Evolutionary Terrain

#import "@preview/showybox:2.0.4": showybox

#set document(title: "Fitness Landscape", author: "WAFT Research Division")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#38a169")

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(30%)), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[FITNESS LANDSCAPE]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[WAFT | Evolutionary Terrain Analysis]
  ]
]

#v(1em)

= What is a Fitness Landscape?

A *fitness landscape* is a visualization of how fitness varies across the space of possible genomes. Think of it as a terrain where:
- Height = Fitness
- Position = Genome configuration
- Peaks = High fitness (goals)
- Valleys = Low fitness (avoid)

= Landscape Features

#grid(
  columns: 2,
  gutter: 1em,
  showybox(frame: (border-color: green, body-color: green.lighten(95%)), title: "Peaks")[
    High fitness regions. Evolution climbs toward these.
  ],
  showybox(frame: (border-color: red, body-color: red.lighten(95%)), title: "Valleys")[
    Low fitness regions. Agents here die or mutate away.
  ],
  showybox(frame: (border-color: orange, body-color: orange.lighten(95%)), title: "Plateaus")[
    Flat regions where mutation doesn't change fitness.
  ],
  showybox(frame: (border-color: blue, body-color: blue.lighten(95%)), title: "Ridges")[
    Narrow paths connecting peaks. Hard to navigate.
  ],
)

= Local vs Global Optima

#showybox(
  frame: (border-color: primary, body-color: primary.lighten(95%)),
)[
  *Local Optimum:* A peak that's higher than neighbors but not the highest overall. Evolution can get stuck here.
  
  *Global Optimum:* The highest peak. The ultimate goal of evolution.
]

= Escaping Local Optima

When stuck on a local optimum:

1. *Increase mutation rate* — Jump to new regions
2. *Use diversity maintenance* — Keep exploring different areas
3. *Add noise* — Random perturbations
4. *Change fitness function* — Reshape the landscape

#pagebreak()

= Analyzing Your Landscape

```python
from waft.analysis import FitnessLandscape

landscape = FitnessLandscape(flight_recorder)

# Plot fitness over generations
landscape.plot_trajectory()

# Identify plateaus
plateaus = landscape.find_plateaus(min_length=5)

# Estimate landscape roughness
roughness = landscape.calculate_roughness()
```

= Landscape Metrics

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*Metric*], [*Meaning*],
  [Roughness], [How much fitness varies with small changes],
  [Correlation length], [Distance over which fitness is predictable],
  [Peak density], [How many local optima exist],
  [Basin size], [How large attraction regions are],
)

= Visualization

```bash
# Generate landscape plot
waft analyze landscape --output landscape.png

# 3D surface (if 2D genome)
waft analyze landscape --3d

# Trajectory overlay
waft analyze landscape --trajectory
```

= Multi-Objective Landscapes

When optimizing multiple fitness dimensions:

```python
landscape = MultiObjectiveLandscape(
    dimensions=["stability", "efficiency", "safety"],
)

# Find Pareto frontier
frontier = landscape.pareto_frontier()
```

= Implications for Evolution

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*Landscape*], [*Strategy*],
  [Smooth], [Low mutation, hill climbing],
  [Rugged], [High mutation, exploration],
  [Plateaued], [Diversity, patience],
  [Multi-modal], [Population diversity],
)

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white)[FITNESS LANDSCAPE | Know Your Terrain]
  ]
]
