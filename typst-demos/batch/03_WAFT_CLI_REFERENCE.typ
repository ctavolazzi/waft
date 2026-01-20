// WAFT CLI REFERENCE CARD
// Quick Reference for Command Line Operations

#import "@preview/showybox:2.0.4": showybox
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *

#set document(title: "WAFT CLI Reference", author: "WAFT Development Team")
#set page(paper: "us-letter", margin: 0.75in, columns: 2)
#set text(font: "New Computer Modern", size: 9pt)

#show: codly-init.with()
#codly(languages: codly-languages)

#place(top + center, float: true, scope: "parent")[
  #rect(fill: gradient.linear(blue, purple), width: 100%, inset: 1.5em)[
    #text(fill: white, size: 20pt, weight: "bold")[WAFT CLI REFERENCE]
    #v(0.2em)
    #text(fill: white.darken(10%), size: 10pt)[Evolutionary Code Laboratory | Quick Reference Card]
  ]
]

#v(4em)

= Installation

```bash
uv tool install waft
```

Or from source:
```bash
git clone https://github.com/ctavolazzi/waft
cd waft && uv sync
```

= Core Commands

== waft new

Create a new evolutionary laboratory.

```bash
waft new my_lab
waft new my_lab --path /custom/path
```

== waft verify

Verify laboratory structure and dependencies.

```bash
waft verify
waft verify --fix  # Auto-fix issues
```

== waft spawn

Create agent variants with mutations.

```bash
waft spawn --agent MyAgent
waft spawn --agent MyAgent \
  --mutation config.json
```

== waft eval

Evaluate agent in Scint Gym.

```bash
waft eval --agent MyAgent
waft eval --agent MyAgent --verbose
```

== waft evolve

Run full evolutionary cycle.

```bash
waft evolve --agent MyAgent
waft evolve --agent MyAgent \
  --generations 10
```

= Session Management

== waft session

```bash
waft session create
waft session bootstrap
waft session list
waft session close
```

== waft dashboard

Launch monitoring dashboard.

```bash
waft dashboard
waft dashboard --port 8080
```

= Empirica Integration

== Logging Commands

```bash
waft finding log "Discovery" \
  --impact 0.7

waft unknown log "Question"

waft observe "Note" \
  --mood delighted
```

== Assessment

```bash
waft preflight   # Before work
waft postflight  # After work
waft check       # Mid-work gate
```

= Gamification

== Character Sheet

```bash
waft character    # View stats
waft character --detailed
```

== Karma & XP

```bash
waft karma        # View karma
waft karma add 10 "Good deed"
waft xp           # View XP
```

#colbreak()

= Agent Commands

== List & Info

```bash
waft agents list
waft agents info MyAgent
waft agents history MyAgent
```

== Genome Operations

```bash
waft genome show MyAgent
waft genome diff Agent1 Agent2
waft genome export MyAgent \
  --output genome.json
```

= Flight Recorder

== Query Events

```bash
waft flight list
waft flight show <event_id>
waft flight query \
  --type GYM_EVAL \
  --since "1 hour ago"
```

== Export

```bash
waft flight export \
  --format json \
  --output events.json
```

= Scint Gym

== Run Tests

```bash
waft gym run MyAgent
waft gym run MyAgent \
  --scenario "complex_task"
```

== View Results

```bash
waft gym results
waft gym results --agent MyAgent
```

= Configuration

== Config File

Located at `~/.waft/config.toml` or `./waft.toml`

```toml
[defaults]
model = "gpt-4"
max_retries = 3

[gym]
timeout = 300
parallel = 4

[evolution]
mutation_rate = 0.1
population_size = 10
```

== Environment Variables

```bash
WAFT_HOME=/path/to/waft
WAFT_MODEL=gpt-4
WAFT_DEBUG=1
```

= Useful Patterns

== Full Evolution Cycle

```bash
waft new my_lab && cd my_lab
waft verify --fix
waft spawn --agent BaseAgent
waft evolve --generations 5
waft dashboard
```

== Quick Debug

```bash
WAFT_DEBUG=1 waft eval \
  --agent MyAgent --verbose
```

#v(1em)

#showybox(
  frame: (border-color: blue, body-color: blue.lighten(95%)),
)[
  #align(center)[
    *Help:* `waft --help` | `waft <cmd> --help`
    
    *Docs:* https://github.com/ctavolazzi/waft
  ]
]
