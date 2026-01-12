# Complete Cycle Exploration

**Date**: 2026-01-12 15:34 PST  
**Phase**: Group 1 - Phase 2: `/explore`  
**Status**: In Progress

---

## Project Architecture Overview

### Core Structure

**Three-Layer System**:
1. **Substrate Layer** (`src/waft/core/substrate.py`): uv environment management
2. **Memory Layer** (`_pyrite/`): Persistent memory system
3. **Agents Layer** (`src/waft/core/agent/`): Self-modifying AI agents

### Key Components

**Core Managers**:
- `MemoryManager`: Manages `_pyrite/` structure (active/, backlog/, standards/)
- `SubstrateManager`: Manages uv environment and dependencies
- `EmpiricaManager`: Epistemic state tracking
- `GamificationManager`: D&D-style progression system
- `GitHubManager`: GitHub integration
- `TavernKeeper`: RPG game master system
- `DecisionEngine`: Weighted decision matrix calculations

**Evolution System**:
- `ChatDistiller`: Extracts ideas from conversations
- `StylingGenome`: Styling configuration
- `PDFGenerator`: PDF generation
- `ComponentEvolution`: Document component evolution
- `ScintDetector`: Reality fracture detection

**Agent System**:
- `BaseAgent`: Self-modifying agent with OODA cycle
- `Genome`: DNA-like code tracking
- `Inventory`: Agent items/tools
- `Reproduction`: Spawn variants

**Scientific Tracking**:
- `TheObserver`: Immutable JSONL logging
- `ScienceBitchManager`: Scientific method tool
- `Notebook`: Self-engineering notebook system

### Directory Structure

```
src/waft/
├── main.py              # CLI entry point (Typer)
├── core/                # Core systems
│   ├── memory.py
│   ├── substrate.py
│   ├── empirica.py
│   ├── gamification.py
│   ├── agent/          # Agent system
│   ├── science/        # Scientific tracking
│   ├── tavern_keeper/  # RPG system
│   └── ...
├── evolution/          # Evolution system
├── api/                # FastAPI server
├── cli/                # CLI display
└── templates/          # Document templates
```

### Patterns Identified

1. **Manager Pattern**: Core functionality organized in manager classes
2. **Generator Pattern**: Evolution system uses generators
3. **Observer Pattern**: Scientific tracking uses observer pattern
4. **Template Pattern**: Document generation uses templates

### Dependencies

- **Typer**: CLI framework
- **FastAPI**: Web API
- **uv**: Python package manager
- **Empirica**: Epistemic tracking
- **CrewAI**: Agent framework (mentioned in docs)

---

## Key Findings

1. **Architecture**: Well-organized three-layer system
2. **Evolution Focus**: System designed for agent evolution
3. **Scientific Rigor**: Complete telemetry and tracking
4. **Gamification**: D&D-style progression system
5. **Active Development**: Multiple work efforts in progress

---

**Next**: Continue with Group 2 - Analysis & Planning phases
