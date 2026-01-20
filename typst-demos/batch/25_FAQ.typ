// WAFT FAQ
// Frequently Asked Questions

#import "@preview/showybox:2.0.4": showybox

#set document(title: "WAFT FAQ", author: "WAFT Documentation Team")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#4299e1")

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(20%)), width: 100%, inset: 2em)[
    #text(fill: white, size: 28pt, weight: "bold")[FAQ]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[WAFT | Frequently Asked Questions]
  ]
]

#v(1em)

= General Questions

== What does WAFT stand for?

WAFT doesn't have an official acronym expansion. It's simply the name of the evolutionary code laboratory. Think of it as code "wafting" through evolutionary generations.

== What is WAFT for?

WAFT is a framework for *directed evolution of AI agents*. Instead of manually engineering agents, you breed them through evolutionary pressure. The fittest agents survive and reproduce.

== Who is WAFT for?

- AI researchers studying artificial cognition
- Developers who want self-improving agents
- Scientists needing rigorous evolution data
- Anyone curious about evolutionary AI

= Technical Questions

== What LLMs does WAFT support?

WAFT supports any LLM with a compatible API:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Local models (via OpenAI-compatible APIs)
- Azure OpenAI
- Any OpenRouter model

== How long does evolution take?

Depends on:
- Population size (10-100 agents typical)
- Generations (5-1000+)
- Gym complexity (simple scenarios: seconds; complex: minutes)

A typical 10-generation run with 20 agents takes 5-15 minutes.

== Can I run WAFT locally?

Yes! Use a local LLM server (like ollama, llama.cpp, or vLLM) with OpenAI-compatible API. Set the base URL in configuration.

#pagebreak()

= Scint Questions

== What is a Scint?

A *Scint* (Semantic Contradiction/Inconsistency/Noise Token) is an ontological error — a point where the AI's output doesn't match reality or logical constraints.

Think of it as a "reality fracture" in the AI's response.

== Why use Scints for fitness?

Scints provide a meaningful fitness signal:
- They measure actual failure modes
- They're automatically detectable
- They span multiple dimensions (syntax, logic, safety, factuality)
- They create genuine evolutionary pressure

== Can I define custom Scint types?

Yes! Extend the `ScintDetector` class:

```python
class MyScintDetector(ScintDetector):
    def detect(self, text: str) -> list[Scint]:
        # Your custom detection logic
        ...
```

= Evolution Questions

== What is a "genome" in WAFT?

An agent's genome includes:
- Source code (the agent class)
- Configuration (parameters, settings)
- System prompts

Changes to any of these are mutations.

== How does breeding work?

Two parent agents combine:
1. Code sections may swap
2. Configurations merge
3. Prompts may blend

The offspring inherits traits from both parents, with possible mutations.

== What prevents degenerate evolution?

Several mechanisms:
- Minimum fitness thresholds
- Diversity maintenance
- Elitism (best agents always survive)
- Multi-objective fitness

#pagebreak()

= Teleport Massive Questions

== Is Teleport Massive real?

Teleport Massive is a *fictional corporation* within the WAFT universe. It provides narrative context for the framework and makes documentation more engaging.

== What is the connection between WAFT and Teleport Massive?

In the fiction, WAFT is a scientific instrument developed by Teleport Massive for AI research. The Scint system emerged from their quantum teleportation research.

== What is the Quantum Incident?

A fictional event where researcher Sarah Chen experienced multi-state existence during a teleportation test, leading to the discovery of Scints.

= Practical Questions

== How do I get started?

```bash
uv tool install waft
waft new my_lab
cd my_lab
waft verify
waft evolve --agent BaseAgent --generations 5
```

== Where can I get help?

- GitHub Issues: https://github.com/ctavolazzi/waft/issues
- Documentation: https://github.com/ctavolazzi/waft
- Discord: [Coming soon]

== How do I contribute?

1. Fork the repository
2. Create a feature branch
3. Submit a pull request
4. Follow the contribution guidelines

#v(1em)

#showybox(
  frame: (border-color: primary, body-color: primary.lighten(95%)),
)[
  #align(center)[
    *Still have questions?*
    
    Open an issue on GitHub or check the documentation.
    
    "Don't just build agents. Breed them."
  ]
]
