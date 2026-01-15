# Another Cycle Exploration - 2026-01-14

**Date**: 2026-01-14 16:11:49 PST  
**Phase**: Group 1 - Phase 2: Exploration  
**Cycle**: Another Cycle Awakening

---

## Architecture Overview

### Five-Layer System

1. **Substrate Layer (uv)**: Package management foundation
   - `pyproject.toml`, `uv.lock`
   - SubstrateManager handles package operations

2. **Memory Layer (_pyrite)**: Project knowledge organization
   - `active/`, `backlog/`, `standards/`
   - MemoryManager manages structure

3. **Agents Layer (CrewAI)**: Optional AI agent capabilities
   - BaseAgent with OODA loop
   - AgentState with memory, journal, short_term_memory

4. **Epistemic Layer (Empirica)**: Knowledge tracking
   - 11 methods for epistemic self-assessment
   - CASCADE workflow (PREFLIGHT → WORK → POSTFLIGHT)

5. **Gamification Layer (TavernKeeper)**: RPG mechanics
   - 15+ methods for D&D integration
   - Karma system, Being lifecycle

---

## Key Systems

### Probe System
- **Purpose**: "Pokey stick" for testing - probes HTTP endpoints, files, services
- **Components**:
  - `HTTPProbe`: Probe HTTP endpoints
  - `FileSystemProbe`: Probe file system
  - `ServiceProbe`: Check if ports are open
  - `ProbeCollector`: Manages multiple probes and stores results
- **Prime Being Probe**: Integrates Being system, Probe system, and Scientific Method tool
  - Observes, reflects, learns, adapts
  - Uses evolutionary loop: External Pressure → Internal Response → External Response

### Pantheon System
- **Purpose**: Higher Beings (Gods) as Aspects of Creation
- **Components**:
  - **Magistrate**: God of Precedent and Body of Proof
    - Organizes case files into Precedents
    - Builds Body of Proof
    - Searches precedents by category, tags, claim similarity
  - **Judge**: God of Judgment and Evaluation
    - Evaluates claims against Body of Proof
    - Renders judgments (PROVEN/DISPROVEN/INCONCLUSIVE)
    - Uses precedent and evidence for decisions
- **Integration**: Works together as legal system (Magistrate organizes, Judge evaluates)

### RAG Integration
- **Location**: `src/waft/rag/`
- **Components**: `chatbot.py`, `agent_integration.py`, `config.py`
- **Status**: Recently added, integration in progress

### Evolution System
- **Location**: `src/waft/evolution/`
- **Components**: PDF generators, document evolution, character sheets, campaign tracking
- **Flow**: Content → ChatDistiller → StylingGenome → Generators → Output → Analysis

---

## Integration Points

### External Dependencies
- `uv`: Package management
- `Empirica`: Epistemic tracking
- `git`: Version control
- `TinyDB`: File-based database
- `d20`: D&D dice rolling
- `FastAPI`: Web API
- `Streamlit`: UI components
- `llama-index`: RAG capabilities

### Internal Patterns
- **Manager Pattern**: Each domain has dedicated manager (MemoryManager, SubstrateManager, etc.)
- **Command Pattern**: CLI commands use managers
- **Template Pattern**: Templates separate from logic
- **Graceful Degradation**: Optional deps with fallbacks
- **Hook Pattern**: TavernKeeper hooks into commands

---

## Key Files & Directories

### Core Modules
- `src/waft/core/`: 65 files - Core functionality
- `src/waft/being.py`: Being class (personality, skills, memories, fitness)
- `src/waft/main.py`: Main CLI entry point (Typer app)

### Templates
- `src/waft/templates/`: Multiple PDF/document templates
  - `brief.py`, `academic_paper.py`, `tm_report.py`, etc.

### Work Efforts
- `_work_efforts/`: Extensive work tracking system
- Johnny Decimal organization
- Multiple active work efforts

### Data Storage
- `_pyrite/`: Project knowledge (active, backlog, standards)
- `_genetics/`: Genetic lineage tracking
- `_pantheon/`: Higher Beings data (judge, magistrate)
- `_probe_data/`: Probe results

---

## Recent Additions

1. **Probe System**: Comprehensive analysis tool
2. **Pantheon System**: Judge and Magistrate for legal evaluation
3. **RAG Integration**: Local RAG chatbot integration
4. **Midday Dossier**: Status reporting command
5. **Multiple Cursor Commands**: case-file, deep-think, evolve-a-ui, etc.

---

## Next Steps

Proceeding to Group 2: Analysis & Planning
- Phase 3: `/check-assumptions`
- Phase 4: `/hypothesis`
- Phase 5: `/critique`
- Phase 6: `/comprehensive-orchestration`
- Phase 7: `/analyze`
