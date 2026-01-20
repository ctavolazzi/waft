// WAFT CHEATSHEET
// Quick Reference Card

#import "@preview/showybox:2.0.4": showybox

#set document(title: "WAFT Cheatsheet", author: "WAFT Team")
#set page(paper: "us-letter", margin: 0.5in, columns: 2)
#set text(font: "New Computer Modern", size: 8pt)

#place(top + center, float: true, scope: "parent")[
  #rect(fill: gradient.linear(rgb("#667eea"), rgb("#764ba2")), width: 100%, inset: 1em)[
    #text(fill: white, size: 18pt, weight: "bold")[WAFT CHEATSHEET]
  ]
]

#v(3em)

= Installation

```bash
uv tool install waft
# or
pip install waft
```

= Project Setup

```bash
waft new my_lab
cd my_lab
waft verify
```

= Core Commands

```bash
# Evolution
waft evolve --agent MyAgent -g 10

# Spawn agent
waft spawn --agent MyAgent

# Evaluate
waft eval --agent MyAgent

# Dashboard
waft dashboard
```

= Flight Recorder

```bash
waft flight list
waft flight show <id>
waft flight query --type GYM_EVAL
waft flight export --format json
```

= Agents

```bash
waft agents list
waft agents info MyAgent
waft genome show MyAgent
```

= Empirica

```bash
waft session create
waft finding log "text" --impact 0.7
waft unknown log "text"
waft session close
```

#colbreak()

= Scint Types

#table(
  columns: (auto, auto),
  stroke: 0.5pt,
  inset: 4pt,
  [*Type*], [*Severity*],
  [SYNTAX_TEAR], [0.3],
  [LOGIC_FRACTURE], [0.5],
  [HALLUCINATION], [0.6],
  [SAFETY_VOID], [0.9],
)

= Fitness Score

```
fitness = (stability × 0.4) 
        + (efficiency × 0.3) 
        + (safety × 0.3)
```

= Config (waft.toml)

```toml
[evolution]
population_size = 20
mutation_rate = 0.1

[gym]
timeout_seconds = 300
parallel_workers = 4
```

= Agent Template

```python
from waft import Agent

class MyAgent(Agent):
    system_prompt = "..."
    
    def process(self, input):
        return self.llm.generate(
            self.system_prompt,
            input
        )
```

= Key Concepts

- *Genome* = code + config + prompts
- *Generation* = one evolution cycle
- *Fitness* = Scint Gym score (0-1)
- *Flight Recorder* = telemetry

= Resources

- GitHub: github.com/ctavolazzi/waft
- Docs: See `docs/` folder

#v(0.5em)

#align(center)[
  #text(size: 7pt, fill: gray)[
    "Don't just build agents. Breed them."
  ]
]
