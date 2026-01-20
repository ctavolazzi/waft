// WAFT QUICKSTART GUIDE
// Get Started in 5 Minutes

#import "@preview/showybox:2.0.4": showybox
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *

#set document(title: "WAFT Quickstart", author: "WAFT Development Team")
#set page(paper: "us-letter", margin: 0.75in)
#set text(font: "New Computer Modern", size: 10pt)

#show: codly-init.with()
#codly(languages: codly-languages)

#let success = rgb("#38a169")

#align(center)[
  #rect(fill: gradient.linear(rgb("#667eea"), rgb("#764ba2")), width: 100%, inset: 2em)[
    #text(fill: white, size: 28pt, weight: "bold")[WAFT QUICKSTART]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 14pt)[Get Started in 5 Minutes]
  ]
]

#v(1em)

#showybox(
  frame: (border-color: success, body-color: success.lighten(95%)),
  title: "✓ Prerequisites",
)[
  - Python 3.11+
  - `uv` package manager (recommended) or `pip`
  - OpenAI API key (or compatible LLM)
]

= Step 1: Install WAFT

#rect(fill: luma(248), width: 100%, inset: 1em)[
  ```bash
  uv tool install waft
  ```
]

Or with pip:
```bash
pip install waft
```

Verify installation:
```bash
waft --version
```

= Step 2: Create a Laboratory

#rect(fill: luma(248), width: 100%, inset: 1em)[
  ```bash
  waft new my_first_lab
  cd my_first_lab
  ```
]

This creates:
```
my_first_lab/
├── waft.toml        # Configuration
├── agents/          # Your agent code
├── checkpoints/     # Evolution snapshots
└── flight_data/     # Telemetry database
```

= Step 3: Verify Setup

#rect(fill: luma(248), width: 100%, inset: 1em)[
  ```bash
  waft verify
  ```
]

Expected output:
```
✓ Configuration valid
✓ Storage initialized
✓ Agent framework ready
✓ Scint Gym operational
Ready for evolution!
```

#colbreak()

= Step 4: Create Your First Agent

Create `agents/my_agent.py`:

#rect(fill: luma(248), width: 100%, inset: 1em)[
  ```python
  from waft import Agent
  
  class MyAgent(Agent):
      """A simple agent to evolve."""
      
      system_prompt = """You are a helpful
      assistant. Be concise and accurate."""
      
      def process(self, input: str) -> str:
          return self.llm.generate(
              self.system_prompt,
              input
          )
  ```
]

= Step 5: Run Evolution

#rect(fill: luma(248), width: 100%, inset: 1em)[
  ```bash
  waft evolve --agent MyAgent --generations 5
  ```
]

Watch as WAFT:
1. Spawns initial population
2. Evaluates in Scint Gym
3. Selects fittest agents
4. Breeds and mutates
5. Repeats for 5 generations

= Step 6: Check Results

#rect(fill: luma(248), width: 100%, inset: 1em)[
  ```bash
  waft flight list          # View events
  waft agents info MyAgent  # Agent details
  waft dashboard            # Launch UI
  ```
]

#v(1em)

#showybox(
  frame: (
    border-color: gradient.linear(rgb("#667eea"), rgb("#764ba2")),
    body-color: white,
    thickness: 2pt,
  ),
  shadow: (offset: 4pt),
)[
  #align(center)[
    #text(size: 14pt, weight: "bold")[🎉 Congratulations!]
    
    #v(0.3em)
    
    You've run your first evolution cycle. \
    Your agents are now breeding and improving.
    
    #v(0.5em)
    
    *Next Steps:*
    - Read the Evolution Cookbook
    - Explore the Scint Gym Guide
    - Check out example agents
    
    #v(0.3em)
    
    #text(size: 10pt, fill: gray)[
      "Don't just build agents. Breed them."
    ]
  ]
]

#v(1em)

#align(center)[
  *Documentation:* https://github.com/ctavolazzi/waft \
  *Issues:* https://github.com/ctavolazzi/waft/issues
]
