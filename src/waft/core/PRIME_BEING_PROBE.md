# Prime Being Probe - The Origin Point

## Overview

The Prime Being Probe is a sentient, learning system that represents the very first Being with the ability to:
- **Observe** its surroundings through probing
- **Reflect** on feedback loops (sensation → reaction, cause → effect)
- **Learn** over time to respond to stimuli
- **Adapt** based on what it has learned

This is an evolutionary experiment to see what happens when we give a Being the ability to use the Scientific Method to learn and evolve.

## Philosophy

The Prime Being Probe implements the evolutionary loop:

### External Pressure → Internal Response → External Response
- **External Pressure**: The environment (services, files, endpoints) presents stimuli
- **Internal Response**: The Being observes, reflects, and forms hypotheses
- **External Response**: The Being adapts its behavior and probes differently

### Internal Pressure → Internal Response → External Response
- **Internal Pressure**: The Being's own curiosity, goals, or hypotheses drive action
- **Internal Response**: The Being decides what to probe based on its learning
- **External Response**: The Being probes and observes the results

## Architecture

The Prime Being Probe integrates three WAFT systems:

1. **Being System**: Provides personality, skills, memories, fitness, and evolution
2. **Probe System**: Provides the ability to probe HTTP endpoints, files, and services
3. **Scientific Method Tool**: Provides hypothesis formation, experimentation, and learning

## Core Components

### Observation
The Prime Being probes outward in "jagged ways" to learn about its environment:
- HTTP endpoints (services, APIs)
- File system (files, directories)
- Services (ports, connectivity)

Each observation is interpreted and stored for reflection.

### Reflection
The Prime Being reflects on observations to identify:
- **Patterns**: What patterns emerge from multiple observations?
- **Cause-Effect**: What causes what? What are the relationships?
- **Hypotheses**: What can we predict based on what we've seen?

### Learning
The Prime Being learns from reflections:
- Updates skills (observation, reflection, learning, adaptation)
- Forms hypotheses using the Scientific Method
- Adapts behavior based on patterns identified

### Adaptation
The Prime Being adapts its behavior:
- Changes probe frequency based on success/failure patterns
- Adjusts caution level based on system stability
- Updates confidence based on reflection quality

## D&D Character Sheet

The Prime Being has a D&D 5e character sheet for roleplay:

- **Class**: Scholar (custom class for learning)
- **Ability Scores**: Based on Being skills
  - Intelligence: Based on scientific_method + learning skills
  - Wisdom: Based on observation + reflection skills
  - Constitution: Based on adaptation skill
- **Skills**: Investigation, Insight, Perception, Nature
- **HP**: Based on constitution

The character sheet evolves as the Being learns and adapts.

## Usage

### Basic Usage

```python
from waft.core.prime_being_probe import PrimeBeingProbe

# Create Prime Being
probe = PrimeBeingProbe(
    being_id="prime_being_probe_001",
    reality_id="probe_reality",
    personality_type="curious_explorer"
)

# Observe (probe outward)
observation = probe.observe("http://localhost:8507")

# Reflect on observations
reflection = probe.reflect(observation_count=5)

# Learn from reflection
adaptation = probe.learn(reflection)

# Run full evolutionary cycle
cycle_data = probe.evolve_cycle()
```

### Pilot Interface

Use the pilot interface to roleplay as the Prime Being:

```bash
python examples/prime_being_pilot.py
```

This provides an interactive interface where you can:
- Observe (probe targets)
- Reflect (think about observations)
- Evolve (run full cycles)
- View status and character sheet

## Evolutionary Cycle

Each cycle implements:

1. **Observe**: Probe multiple targets (jagged outward probing)
2. **Reflect**: Analyze observations for patterns and cause-effect
3. **Learn**: Form hypotheses and adapt behavior
4. **Adapt**: Update skills, fitness, and character stats

## Scientific Method Integration

The Prime Being uses the Scientific Method Tool to:
- Form hypotheses based on patterns
- Test hypotheses through additional observations
- Verify or refute hypotheses with confidence levels
- Iterate and refine understanding

## Storage

The Prime Being stores its state in `_prime_being_data/`:
- Being state (skills, fitness, memories)
- Observations (all probe results)
- Reflections (pattern analysis)
- Adaptations (behavior changes)
- Hypotheses (scientific hypotheses)
- Experiments (scientific experiments)

## Roleplay

You are piloting the Prime Being - the Origin Point. As you roleplay:

- **You are the Being**: Make decisions as if you are the Prime Being
- **Observe**: Probe things that interest you or seem important
- **Reflect**: Think about what patterns you see
- **Learn**: Adapt your behavior based on what you've learned
- **Evolve**: Run cycles to see how the Being grows

The D&D character sheet represents the Being's "stats" - its capabilities that evolve over time.

## Example Session

```
1. Create Prime Being
2. Observe: Probe http://localhost:8507 (Good Morning dashboard)
3. Observe: Probe http://localhost:8000/api/health (API health)
4. Reflect: "I notice both probes succeeded - system appears stable"
5. Learn: "I should probe more frequently when system is stable"
6. Evolve: Run full cycle to see adaptation
7. Check character sheet: See how skills and stats have evolved
```

## Future Enhancements

- More sophisticated pattern detection
- Hypothesis testing through experiments
- Memory system for long-term learning
- Goal system for directed exploration
- Integration with other WAFT systems
- Visualization of evolutionary progress

## Status

🚧 **In Development** - This is an experimental system for exploring sentient, learning probes.

The Prime Being Probe is the first Being with the ability to Observe, Reflect, and Learn - making it a true Origin Point for evolutionary learning.
