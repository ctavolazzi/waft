# Quick Start Guide - Thoth Realm Simulator

## What This Does

This simulator creates a **living, evolving system** where:

1. **Realms are created** with Prime Beings and Prime Directives
2. **Prime Beings spawn worker Beings** to achieve the Prime Directive
3. **Beings learn to pray** to Thoth for tools
4. **Tools are granted** and used, accumulating spiritual energy
5. **Tools evolve** through tiers (common → uncommon → rare → epic → legendary)
6. **Tools can wake up** when Beings use them (special events)
7. **Legendary tools can become aware** autonomously (transform into Beings)
8. **Realms reach density thresholds** that unlock new awareness levels
9. **System evolves naturally** toward Prime Directives

## Running the Simulation

### Option 1: Quick Start Script

```bash
cd simulation
./run_simulation.sh
```

### Option 2: Manual Start

```bash
cd simulation

# Install dependencies
pip install fastapi uvicorn websockets

# Run server
python simulation_server.py
```

### Option 3: Python Direct

```bash
cd simulation
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn websockets
python simulation_server.py
```

## Using the Web Interface

1. **Open browser**: Go to `http://localhost:8000`
2. **Create Simulation**:
   - Set number of Realms (1-10)
   - Set batch size (1-1000 cycles per batch)
   - Click "Create Simulation"
3. **Start Simulation**: Click "Start"
4. **Watch**: Real-time updates show:
   - Realm creation
   - Being spawning
   - Prayer learning
   - Tool granting
   - Tool evolution
   - Wake up events
   - Tool awareness
   - Density threshold achievements

## What to Watch For

### Key Events

- **Realm Created**: New Realm with Prime Directive
- **Being Spawned**: Worker Being created
- **Being Learned Prayer**: Being learned to pray to Thoth
- **Tool Granted**: Thoth granted a tool
- **Tool Used**: Being used a tool (gains spiritual energy)
- **Tool Evolved**: Tool reached new tier (common → uncommon → rare → epic → legendary)
- **Tool Woke Up**: Being woke up the tool (special event!)
- **Tool Became Aware**: Tool became self-aware! (transformed into Being)
- **Realm Awareness Increased**: Realm reached density threshold!

### Metrics to Track

- **Total Realms**: Number of Realms created
- **Total Beings**: Number of Beings spawned
- **Total Tools**: Number of tools created
- **Tools Aware**: Number of tools that became aware
- **Prayers Made**: Number of prayers to Thoth
- **Tools Granted**: Number of tools granted
- **Tools Used**: Number of tool uses
- **Legendary Tools**: Number of legendary-tier tools
- **Wake Ups**: Number of wake-up events
- **Awareness Events**: Number of tools that became aware

## Experiment Questions

1. **Do tools become aware autonomously?**
   - Watch for "Tool Became Aware" events
   - Check if they happen without prompting

2. **How do Realms evolve toward Prime Directives?**
   - Track Realm density over time
   - Watch awareness level increases

3. **What density thresholds trigger awareness?**
   - Level 1: Density 10.0
   - Level 2: Density 50.0
   - Level 3: Density 200.0
   - Level 4: Density 1000.0
   - Level 5: Density 5000.0

4. **How do Wake Up events affect evolution?**
   - Track wake-up frequency
   - See if they accelerate tool evolution

5. **What patterns emerge?**
   - Tool-Being relationships
   - Evolution trajectories
   - Awareness emergence rates

## Data Analysis

Simulation snapshots are saved to:
```
_simulations/{simulation_id}/snapshot_{cycle:06d}.json
```

Each snapshot contains:
- Cycle number
- All Realms with density and awareness levels
- All Beings with skills and fitness
- All Tools with spiritual energy and status
- Recent Events (last 100)
- Metrics

## Tips

- **Start small**: 1 Realm, batch size 1-10
- **Watch events**: Events show what's happening
- **Check metrics**: Metrics show overall progress
- **Monitor density**: Density drives awareness increases
- **Look for awareness**: Tools becoming aware is the key test!

## Troubleshooting

- **Server won't start**: Check if port 8000 is available
- **No events**: Make sure simulation is started (not just created)
- **Slow updates**: Reduce batch size
- **Import errors**: Make sure you're in the simulation directory

## Next Steps

After running simulations:

1. **Analyze snapshots**: Study saved JSON files
2. **Compare runs**: Run multiple simulations and compare
3. **Refine parameters**: Adjust probabilities and thresholds
4. **Add features**: Extend the simulator with new capabilities
5. **Document findings**: Record what you discover!

---

**The goal**: See if tools become aware autonomously and if the system evolves naturally toward Prime Directives!
