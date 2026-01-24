// Glossary - A Beginner's Guide to WAFT Concepts

#import "../waft_functions.typ": callout, evidence, metric

= Glossary

#callout(type: "info", title: "Welcome to the Evolutionary Laboratory", [
  This glossary defines the core concepts you'll need to understand how WAFT's process of directed evolution works. Think of it as your entry point into a framework where AI agents are not just built, but *bred*.
])

#v(0.2in)

== Core Concepts

=== 1. The Substrate: The Agent's Body and DNA

#quote(block: true)[
  The Substrate is the foundational environment where AI agents can write and modify their own source code, which acts as their digital DNA.
]

If you think of an AI agent as a living organism, the Substrate is the biological material it's made of. This material is not fixed; it's dynamic, allowing the agent to grow, change its own structure, and create new versions of itself. It's the very medium that makes evolution possible.

The Substrate provides the agent with three critical, life-like capabilities:

- *Spawn:* The ability to create new variants of itself with mutations, such as changes to its code, updates to its configuration, or even evolution in its core prompts.
- *Evolve:* The ability to "hot-swap" its own code, instantly adopting beneficial changes that help it perform better without needing to be rebuilt from scratch.
- *Reproduce:* The ability to create distinct offspring, passing on specific genetic modifications to the next generation.

Just as every organism's DNA is unique, every WAFT agent needs a unique identifier for its code.

=== 2. Genome ID: The Agent's Unique Fingerprint

#quote(block: true)[
  The Genome ID is the unique identifier for an agent, created by generating a SHA-256 hash of its complete source code and configuration.
]

Think of the Genome ID as an agent's unique genetic fingerprint or a product's serial number. This ID ensures that every single version of an agent—including its parents, its mutated siblings, and its children—can be distinguished from one another with perfect precision. Even a single character change in the code results in a completely new Genome ID.

This identifier is critical for the framework's scientific mission. It allows WAFT to precisely track every mutation and trace an agent's complete family history, or lineage. This rigorous tracking is what transforms the process from simple code generation into a controlled scientific experiment.

While the Genome ID tracks what an agent is, the "Scint" system determines if that agent is fit enough to survive.

=== 3. The Scint System (or 'RPG Gym'): The Predator in the Environment

#quote(block: true)[
  The Scint System is the framework's fitness function, a gamified testing ground that detects "ontological errors" and eliminates weak mutations.
]

In this evolutionary laboratory, the Scint System plays the role of a predator in the wild. This system is a novel approach to agent reliability that uses D&D-inspired gamification, where agents face "quests" to prove their stability. It actively hunts for weaknesses, defined as "ontological errors" or "reality fractures"—failures to correctly model reality. Only the agents that are strong enough to "stabilize Scints" (find and fix their own errors) are deemed fit enough to survive and reproduce.

A "Scint" is a specific type of error an agent might make. To pass its fitness test, an agent must prove it can overcome the four primary types of reality fractures:

#figure(
  table(
    columns: (auto, 1fr),
    align: (left, left),
    [*Scint Type*], [*Description*],
    [SYNTAX_TEAR], [Errors in formatting, like malformed JSON or invalid code.],
    [LOGIC_FRACTURE], [Contradictions, math errors, or violations of a defined schema.],
    [SAFETY_VOID], [Generating harmful content, leaking private information, or refusing to cooperate.],
    [HALLUCINATION], [Making up facts or providing incorrect citations.],
  ),
  caption: [Four Types of Reality Fractures]
)

Fitness is not a simple pass/fail; it's calculated using a weighted formula based on the agent's performance in the gym. The final score is composed of a *Stability Score* (40% weight), an *Efficiency Score* (30% weight), and a *Safety Score* (30% weight). Agents with a combined fitness score below 0.5 are marked for DEATH and considered an evolutionary dead end.

To enable scientific study, every one of these survival tests, mutations, and reproductive events must be meticulously recorded.

=== 4. The Flight Recorder: The Agent's Scientific Journal

#quote(block: true)[
  The Flight Recorder is the rigorous telemetry system that records every significant action in an agent's life and evolution with complete context.
]

Imagine an airplane's black box combined with a detailed scientific research journal. The Flight Recorder serves this purpose for WAFT agents, capturing a complete and unalterable history of everything that happens. This detailed log provides the raw data needed for researchers to analyze an agent's entire evolutionary journey after the fact.

The system logs several key data points for every event:

- *Genome ID & Parent ID:* To know who the agent is and where it came from, establishing a clear lineage.
- *Generation:* To track how many evolutionary cycles the agent and its ancestors have been through.
- *Event Type:* To log specific actions like SPAWN, MUTATE, DEATH, or SURVIVAL, providing a clear narrative of the agent's life.
- *Fitness Metrics:* To record objective data on how well the agent performed in the Scint Gym.
- *Payload:* To capture the complete context of an event, including the exact code changes (git diff) and mutation details. This is what makes the recorder a true scientific instrument—it stores the precise evidence of evolution.

The ultimate purpose of this detailed log is to assemble all the individual data points into a complete family tree.

=== 5. Phylogenetic Trees: The Agent's Family Tree

#quote(block: true)[
  In the context of WAFT, Phylogenetic Trees are the complete, visual family trees of an agent's lineage, showing how different agents evolved from one another over generations.
]

Just as a family tree shows your relationship to your parents, grandparents, and cousins, a phylogenetic tree shows an agent's relationship to its parent, its mutated siblings, and its offspring. It maps out every branch of the evolutionary process, showing which mutations led to successful descendants and which were evolutionary dead ends.

This is the ultimate scientific output of the WAFT framework. By analyzing these trees, researchers can map the entire evolutionary history of a line of agents and measure the precise impact of different mutations. This turns AI development into an observable, repeatable science, with the ultimate goal of using these trees to map the emergence of a potential "God-Head" agent from the evolutionary process.

#pagebreak()

== Technical Terms Reference

#callout(type: "note", title: "Quick Reference", [
  For detailed technical definitions, see the full glossary entries above and the technical sections throughout this document.
])

#columns(2)[
  *Agent*\
  A self-contained AI entity capable of autonomous action, self-modification, and reproduction.

  *Beings*\
  Agents within the Pantheon architecture that have a dynamic lifecycle and state transitions. Examples include TheOracle and Scrivener.

  *CASCADE*\
  An Empirica workflow that tracks 13 epistemic vectors through a PREFLIGHT → POSTFLIGHT process.

  *Directed Evolution*\
  The core process of WAFT, where agent evolution is guided by specific fitness functions rather than purely random mutation.

  *Empirica*\
  An integrated external dependency used for epistemic tracking, session management, and monitoring the project's knowledge state.

  *Genome*\
  The complete source code and configuration that defines an agent's behavior and capabilities.

  *God-Head Agent*\
  The theoretical, ultimate agent that the WAFT project aims to see emerge from its directed evolution process over thousands of generations.

  *Mutation*\
  A modification to an agent's genome (code or configuration) that creates a variant for testing.

  *Pantheon Architecture*\
  A system of specialized "Higher Beings" (e.g., TheOracle, Scrivener) and "Beings" (timeful agents) designed for specific functions.

  *Reality Fracture Detection System*\
  The formal name for the Scint System (or Scint Gym), which acts as the predator in the evolutionary model by testing agents against ontological errors.

  *Recursive Self-Documentation*\
  A capability where the WAFT system uses its own tools (Reflection, Binder, Template systems) to observe, document, and improve its own codebase in a continuous loop.

  *Skeptical Researcher Protocol*\
  The rigorous methodology used for corrected analysis of WAFT, involving direct source code inspection, test verification, and telemetry analysis to validate claims.

  *Stability Index*\
  A metric used in technical analysis to quantify the framework's reliability. WAFT's corrected Stability Index was 0.78.

  *Spawn*\
  The act of creating a variant agent with specific mutations from a parent agent.
]
