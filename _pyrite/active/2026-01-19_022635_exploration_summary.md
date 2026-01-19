# Codebase Exploration Summary

**Date**: 2026-01-19 02:28:00 PST  
**Context**: `/another-cycle` - Group 1, Phase 2 (Explore)

---

## Project Structure

### Core Architecture
- **Entry Point**: `src/waft/main.py` (1263+ lines, Typer CLI)
- **Core Systems**: `src/waft/core/` (80+ modules)
- **CLI Components**: `src/waft/cli/`
- **Templates**: `src/waft/templates/` (Typst, LaTeX)
- **API**: `src/waft/api/` (FastAPI)
- **UI**: `src/waft/ui/` (Streamlit, SvelteKit visualizer)

### Key Systems Identified

#### 1. Core Managers
- `MemoryManager` - `_pyrite/` structure management
- `SubstrateManager` - uv environment management
- `EmpiricaManager` - Epistemic tracking
- `GamificationManager` - D&D progression
- `GitHubManager` - GitHub integration
- `TavernKeeper` - RPG narrative system

#### 2. Agent System
- `BaseAgent` - OODA cycle implementation
- `Genome` - Code DNA tracking
- `Inventory` - Agent items/tools
- `Reproduction` - Spawn variants

#### 3. Being System
- `Being` - Timeful entities with lifecycle
- `BeingSystem` - Being management
- `NowCycleManager` - Lifecycle event loop
- `BeingDecisionSystem` - Decision-making

#### 4. Economic Systems
- `CorporationsSystem` - Corporate management
- `FinancialState` - Financial tracking
- `Transaction` - Economic transactions
- `AccountingSystem` - Double-entry accounting
- `SimulationEngine` - Economic simulation

#### 5. Document Generation
- Typst templates (`src/waft/templates/typst/`)
- LaTeX templates (`src/waft/templates/latex/`)
- Template registry system
- PDF generation pipeline

#### 6. D&D Integration
- `DNDScenario` - Scenario orchestration
- `PartyManager` - Party management
- `QuestPDFGenerator` - Quest document generation
- `EncounterGenerator` - Combat encounters

#### 7. Scientific Method
- `ScienceBitch` - Full scientific workflow
- `Observer` - Event logging
- `Oracle` - Epistemic insights
- Experiment tracking

#### 8. Decision Systems
- `DecisionMatrix` - WSM calculations
- `DecisionCLI` - Decision interface
- `WorkflowDecisionAnalyzer` - Workflow analysis

---

## Key Patterns

### Manager Pattern
- Centralized system management
- Project path resolution
- State persistence
- Integration points

### Registry Pattern
- Template registries (Typst, LaTeX)
- Auto-discovery mechanisms
- Metadata extraction

### Lifecycle Pattern
- Being lifecycle (NowCycleManager)
- Agent lifecycle (BaseAgent OODA)
- Corporate lifecycle (CorporationsSystem)

### Document Generation Pattern
- Wrapper functions for templates
- Template registry integration
- PDF/HTML output generation

---

## Integration Points

### Being System ↔ Corporations
- Employees are Beings
- Being lifecycle affects corporations
- Skills map to job performance

### Typst ↔ Economic Systems
- Invoice generation from transactions
- Financial statement generation
- Report generation

### D&D ↔ Being System
- Beings can participate in campaigns
- Quest generation
- Character integration

### Scientific Method ↔ All Systems
- Experiment tracking
- State capture
- Evidence collection

---

## Recent Additions

### Corporations System
- Complete economic simulation framework
- Financial state tracking
- Transaction system
- Typst invoice integration

### Work Efforts System
- MCP integration
- Johnny Decimal organization
- Status tracking

### Typst Templates
- Template registry
- Wrapper pattern
- Auto-discovery

---

## Architecture Insights

1. **Modular Design**: Clear separation of concerns
2. **Manager Pattern**: Centralized system management
3. **Lifecycle Management**: Multiple lifecycle systems (Being, Agent, Corporate)
4. **Document Generation**: Unified template system
5. **Integration**: Systems designed to work together

---

**Status**: Exploration complete, ready for Group 2: Analysis & Planning
