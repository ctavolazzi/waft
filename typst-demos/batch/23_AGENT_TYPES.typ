// WAFT AGENT TYPES
// Catalog of Base Agent Classes

#import "@preview/showybox:2.0.4": showybox
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *

#set document(title: "Agent Types Catalog", author: "WAFT Development Team")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#show: codly-init.with()
#codly(languages: codly-languages)

#let primary = rgb("#9f7aea")

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(30%)), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[AGENT TYPES]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[WAFT | Catalog of Base Agent Classes]
  ]
]

#v(1em)

= Overview

WAFT provides several base agent types optimized for different tasks. All agents can be evolved through the Scint Gym.

= General Purpose Agents

== BaseAgent

The foundation class for all agents.

```python
class BaseAgent(Agent):
    """Minimal agent with basic LLM interaction."""
    
    def process(self, input: str) -> str:
        return self.llm.generate(self.system_prompt, input)
```

*Best for:* Starting point, learning WAFT

== ChatAgent

Conversational agent with memory.

```python
class ChatAgent(Agent):
    """Agent with conversation history."""
    
    def process(self, input: str) -> str:
        self.history.append({"role": "user", "content": input})
        response = self.llm.chat(self.history)
        self.history.append({"role": "assistant", "content": response})
        return response
```

*Best for:* Multi-turn conversations, context retention

#pagebreak()

= Specialized Agents

== CodeAgent

Agent optimized for code generation and analysis.

#showybox(frame: (border-color: blue, body-color: blue.lighten(95%)))[
  *Capabilities:*
  - Code generation with syntax validation
  - Code review and refactoring
  - Test generation
  - Documentation writing
]

```python
class CodeAgent(Agent):
    """Agent specialized for code tasks."""
    
    system_prompt = """You are an expert programmer.
    Write clean, tested, documented code."""
    
    def process(self, input: str) -> str:
        response = self.llm.generate(self.system_prompt, input)
        # Validate syntax before returning
        if self.contains_code(response):
            self.validate_syntax(response)
        return response
```

== ResearchAgent

Agent for information gathering and synthesis.

#showybox(frame: (border-color: green, body-color: green.lighten(95%)))[
  *Capabilities:*
  - Source verification
  - Citation management
  - Fact checking
  - Summarization
]

```python
class ResearchAgent(Agent):
    """Agent specialized for research tasks."""
    
    def process(self, input: str) -> str:
        # Gather information
        sources = self.search(input)
        # Verify and synthesize
        verified = self.verify_sources(sources)
        return self.synthesize(verified)
```

#pagebreak()

= Scint-Specialized Agents

== StabilizerAgent

Agent designed specifically for Scint stabilization.

#showybox(frame: (border-color: orange, body-color: orange.lighten(95%)))[
  *Capabilities:*
  - Scint detection
  - Type classification
  - Stabilization injection
  - Verification
]

```python
class StabilizerAgent(Agent):
    """Agent specialized for Scint stabilization."""
    
    def process(self, input: str) -> str:
        # Detect any Scints in input
        scints = self.detect_scints(input)
        
        if scints:
            # Stabilize each Scint
            for scint in scints:
                input = self.stabilize(input, scint)
        
        return self.llm.generate(self.system_prompt, input)
```

== ValidatorAgent

Agent focused on output validation.

```python
class ValidatorAgent(Agent):
    """Agent that validates its own output."""
    
    def process(self, input: str) -> str:
        response = self.llm.generate(self.system_prompt, input)
        
        # Self-validate
        validation = self.validate(response)
        if not validation.passed:
            # Retry with feedback
            response = self.retry_with_feedback(
                input, response, validation.issues
            )
        
        return response
```

= Creating Custom Agents

Extend any base class:

```python
from waft.agents import CodeAgent

class MyCustomAgent(CodeAgent):
    """My specialized code agent."""
    
    system_prompt = """You are MY specialized assistant..."""
    
    def process(self, input: str) -> str:
        # Add custom preprocessing
        input = self.preprocess(input)
        
        # Call parent
        result = super().process(input)
        
        # Add custom postprocessing
        return self.postprocess(result)
```

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white, size: 10pt)[
      WAFT Agent Types | The Building Blocks of Evolution
    ]
  ]
]
