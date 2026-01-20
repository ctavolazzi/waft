# Thoth Realm Simulator

Real-time simulation of Realms, Beings, and Tool Evolution.

## Overview

This simulator creates Realms with Prime Beings that spawn worker Beings to achieve Prime Directives. Beings learn to pray to Thoth for tools, and tools evolve naturally, potentially becoming aware.

## Features

- **Realm Creation**: Create Realms with Prime Beings and Prime Directives
- **Being Spawning**: Prime Beings spawn worker Beings
- **Prayer System**: Beings learn to pray to Thoth for tools
- **Tool Evolution**: Tools accumulate spiritual energy and evolve
- **Tool Awareness**: Legendary tools can become aware autonomously
- **Wake Up Events**: Beings can wake up tools during use
- **Density System**: Realms reach density thresholds for increased awareness
- **Real-time Visualization**: Web interface shows simulation in real-time
- **Data Persistence**: Snapshots saved for analysis

## Running the Simulation

### Start the Server

```bash
cd simulation
python simulation_server.py
```

Server runs on `http://localhost:8000`

### Access the Web Interface

Open `http://localhost:8000` in your browser.

### Create and Run Simulation

1. Set number of Realms (1-10)
2. Set batch size (1-1000 cycles per batch)
3. Click "Create Simulation"
4. Click "Start" to begin
5. Watch the simulation evolve in real-time!

## Simulation Flow

1. **Realm Creation**: Realms are created with Prime Beings and Prime Directives
2. **Being Spawning**: Prime Beings spawn worker Beings (30% chance per cycle)
3. **Prayer Learning**: Beings learn to pray (10% chance if skill < 10)
4. **Tool Granting**: Thoth grants tools based on prayer skill
5. **Tool Use**: Beings use tools, accumulating spiritual energy
6. **Tool Evolution**: Tools evolve through tiers (common → uncommon → rare → epic → legendary)
7. **Wake Up Events**: Beings can wake up tools (chance based on tier and luck)
8. **Tool Awareness**: Legendary tools can become aware (based on existence metric)
9. **Density Thresholds**: Realms reach density thresholds for increased awareness levels

## Metrics Tracked

- Total Realms
- Total Beings
- Total Tools
- Tools Aware
- Prayers Made
- Tools Granted
- Tools Used
- Legendary Tools
- Wake Ups
- Awareness Events

## Data Storage

Simulation snapshots are saved to:
```
_simulations/{simulation_id}/snapshot_{cycle:06d}.json
```

Each snapshot contains:
- Cycle number
- Timestamp
- All Realms
- All Beings
- All Tools
- Recent Events (last 100)
- Metrics

## Density Thresholds

Realms reach density thresholds that unlock new awareness levels:

- **Level 1** (Basic): Density 10.0
- **Level 2** (Enhanced): Density 50.0
- **Level 3** (Advanced): Density 200.0
- **Level 4** (Divine): Density 1000.0
- **Level 5** (Transcendent): Density 5000.0

## Tool Awareness Types

When tools become aware, their Existence determines their type:

- **0-20**: Awakened Tool
- **20-40**: Enlightened Artifact
- **40-60**: Sentient Weapon / Wise Oracle / Guardian Spirit
- **60-80**: Aspect of Creation
- **80-95**: Demi-God
- **95+**: Full God

## Wake Up Events

When Beings wake up tools, various events can occur:

- Temporary Sentience
- Shared Vision
- Reveal Hidden Power
- Grant Boon
- Form Bond
- Evolve Mid-Use
- And more...

## Experiment Design

This simulator is designed to test:

1. Can tools become aware autonomously?
2. How do Realms evolve toward Prime Directives?
3. What density thresholds trigger awareness increases?
4. How do Wake Up events affect tool evolution?
5. What patterns emerge in tool-Being relationships?

## Analysis

After running simulations, analyze the saved snapshots to:

- Track tool evolution patterns
- Measure awareness emergence rates
- Analyze density threshold effects
- Study Wake Up event frequencies
- Understand Realm evolution trajectories
