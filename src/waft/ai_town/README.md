# AI Town - Basic Implementation

A virtual town where AI characters live, chat, and socialize.

Built using WAFT's tools and inspired by:
- **Generative Agents paper** (arXiv:2304.03442)
- **ai-town repository** (a16z-infra/ai-town)

## Overview

AI Town is a basic implementation of the Generative Agents concept, where AI agents:
- Live in a virtual 2D town
- Move around and explore
- Have conversations with each other
- Remember past conversations
- Form relationships
- Make decisions based on personality

## Architecture

### Core Components

1. **TownAgent** (`town_agent.py`)
   - Extends WAFT's BaseAgent
   - Has position, personality, memories
   - Can move, seek conversations, explore

2. **TownWorld** (`town_world.py`)
   - Game engine managing the simulation
   - Handles agent interactions
   - Manages conversations
   - Runs tick-based simulation

3. **Conversation** (`conversation.py`)
   - Conversation between agents
   - Message history
   - Conversation lifecycle

4. **TownMemory** (`memory.py`)
   - Stores conversation memories
   - Retrieves relevant memories (simplified vector similarity)
   - Memory summarization

## Usage

### Simple Demo

Run the standalone demo:

```bash
python3 examples/ai_town_simple_demo.py
```

### Using WAFT Integration

```python
from waft.ai_town import TownAgent, TownWorld
from waft.core.agent.state import AgentConfig

# Create town
town = TownWorld(name="My AI Town")

# Create agent
config = AgentConfig(
    role="Explorer",
    goal="Explore and meet people",
    tools=[],
)
agent = TownAgent(
    config=config,
    project_path=Path("."),
    name="Alice",
)

# Add to town
town.add_agent(agent)

# Run simulation
await town.run_simulation(ticks=100)
```

## Features

### Current Implementation

✅ **Basic Agents**
- Position in 2D space
- Personality traits (curiosity, sociability, energy)
- Decision-making based on personality
- Movement and exploration

✅ **Conversation System**
- Agents can start conversations
- Message exchange
- Conversation lifecycle (start, continue, end)
- Memory creation from conversations

✅ **Memory System**
- Conversation summaries
- Memory storage and retrieval
- Simplified similarity search (placeholder for vector embeddings)

✅ **Simulation Loop**
- Tick-based simulation
- Agent updates each tick
- Conversation management
- State tracking

### Future Enhancements

🔲 **LLM Integration**
- Generate actual conversation messages using LLM
- Personality-aware responses
- Context-aware memory retrieval

🔲 **Vector Embeddings**
- Real vector embeddings for memory retrieval
- Semantic similarity search
- Better memory relevance

🔲 **Advanced Behaviors**
- Goal setting and planning
- Activity scheduling
- Relationship tracking
- Social dynamics

🔲 **Visualization**
- 2D visualization of town
- Agent positions
- Conversation visualization
- Real-time updates

🔲 **Persistence**
- Save/load town state
- Persistent memory storage
- Conversation history

## Design Decisions

### Simplified for Basic Implementation

1. **No LLM Integration**: Uses simple rule-based conversations (greetings)
2. **Simplified Memory**: Hash-based similarity instead of vector embeddings
3. **Basic Movement**: Random wandering instead of pathfinding
4. **Simple Decisions**: Probability-based instead of planning

### WAFT Integration Points

- **BaseAgent**: Extends WAFT's agent system
- **AgentState**: Uses WAFT's state management
- **Memory System**: Can integrate with WAFT's memory flow
- **Evolution**: Could add evolutionary selection for agent behaviors

## Files

- `town_agent.py` - Agent implementation
- `town_world.py` - World/game engine
- `conversation.py` - Conversation system
- `memory.py` - Memory system
- `__init__.py` - Package exports

## Examples

See `examples/ai_town_simple_demo.py` for a working demo.

## References

- Generative Agents Paper: https://arxiv.org/abs/2304.03442
- ai-town Repository: https://github.com/a16z-infra/ai-town
- WAFT Documentation: `docs/` directory
