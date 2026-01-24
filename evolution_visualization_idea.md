# Evolution Visualization Integration

## The Idea

Combine the **Evolution Engine** we just built with the **AI Town Visualization** to create a **live evolution simulation**:

### What We Have Now

1. **Evolution Engine** (`src/waft/core/evolution_engine.py`)
   - Spawns variants with mutations
   - Evaluates fitness in Scint Gym
   - Selects fittest variant
   - Records in Flight Recorder

2. **AI Town Visualization** (`src/waft/ui/streamlit/town_integration.py`)
   - Shows beings as particles on a 2D canvas
   - Real-time simulation loop
   - Interactive Plotly scatter plot
   - Conversation lines between agents

### What We Could Build

**"Evolution Arena" - Watch Natural Selection in Real-Time**

```python
# Spawn 10 variant beings into AI Town
# Each has slightly different:
# - Personality (sociability, curiosity, energy)
# - Skills (reasoning, pattern recognition)
# - Lifecycle attributes (will_to_live, luck)

# Run simulation for 100 ticks
# - Beings with better skills make better decisions
# - Beings with higher sociability form more connections
# - Beings with low will_to_live struggle

# Every 20 ticks, evaluate fitness:
# - Conversation success rate
# - Movement efficiency
# - Energy management
# - Scint detection (reality fractures)

# Eliminate bottom 50%, spawn new variants from top 50%
# - Inherit traits from "parents"
# - Add mutations
# - Repeat

# Watch the population evolve!
# - Colors fade/brighten based on fitness
# - Particle size = fitness level
# - Trails show movement history
# - Family trees visualized
```

### Implementation Steps

1. **Add Evolution to AI Town**
   - `TownAgent` already extends `BaseAgent`
   - Connect to `Being` system for full lifecycle
   - Add fitness evaluation based on town behavior

2. **Visual Fitness Indicators**
   - Particle size = fitness score
   - Color intensity = current energy
   - Glow effect = high performers
   - Fade out = low fitness (about to die)

3. **Generation Overlay**
   - Timeline showing generations
   - Family tree view
   - Fitness graph over time
   - Mutation tracker

4. **Interactive Controls**
   - Speed control (ticks per second)
   - Selection pressure slider
   - Mutation rate control
   - Pause/resume/step through

5. **Flight Recorder Integration**
   - Save entire evolutionary run
   - Replay past generations
   - Compare different runs
   - Export phylogenetic tree

### The Meta Magic

- **Use Evolution to Improve Evolution**
  - Run meta-evolution on mutation strategies
  - Evolve the fitness function itself
  - Let the system discover what "fitness" means

- **Emergent Behaviors to Watch For**
  - Social clustering (high-fitness beings grouping)
  - Specialization (different niches emerge)
  - Communication patterns evolving
  - Strategies that we didn't program

### Quick Prototype

Want to see it in action? We could:

1. Add a simple evolution mode to the existing AI Town
2. Run 5 generations with 5 variants each
3. Watch what emerges
4. Document the results

This is literally **"breeding agents, not building them"** - but with a visual interface to watch it happen!
