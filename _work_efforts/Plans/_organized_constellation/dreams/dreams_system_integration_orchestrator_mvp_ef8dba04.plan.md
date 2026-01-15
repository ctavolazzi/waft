---
name: System Integration Orchestrator MVP
overview: Create a minimal MVP integration orchestrator that provides a simple interface to coordinate between major WAFT systems (Beings, Scints, TavernKeeper, KarmaMerchant, etc.). This will be a lightweight coordinator that enables basic cross-system communication and coordination.
todos:
  - id: orchestrator_class
    content: Create SystemOrchestrator class in src/waft/core/orchestrator.py with lazy system loading and basic accessors
    status: pending
  - id: coordination_method
    content: Implement one coordination method (coordinate_being_quest) to demonstrate cross-system interaction
    status: pending
  - id: example_script
    content: Create example script (examples/test_orchestrator_integration.py) demonstrating orchestrator usage
    status: pending
  - id: documentation
    content: Create basic documentation (docs/SYSTEM_ORCHESTRATOR_GUIDE.md) with usage examples
    status: pending
  - id: devlog_update
    content: Update devlog with orchestrator implementation progress
    status: pending

category: dreams
confidence: 0.57
constellation_date: 2026-01-14
---

# System Integration Orchestrator MVP

## Goal

Create a minimal MVP system that helps coordinate and integrate existing WAFT systems. This orchestrator will provide a simple interface to connect Beings, Scints, TavernKeeper, KarmaMerchant, and other core systems.

## Current State Analysis

### Existing Orchestrators

- **WAFTKernel** (`src/waft/core/kernel.py`) - Lightweight orchestrator for:
  - TheObserver (Flight Recorder)
  - EmpiricaManager (Epistemic State)
  - GamificationManager (Gamification)

- **NowCycleManager** (`src/waft/core/now_cycle.py`) - Manages Being lifecycle cycles

### Systems Needing Integration

1. **BeingSystem** - Entity management in realities
2. **Scint System** - Reality fracture detection and stabilization
3. **TavernKeeper** - RPG narrative and quest system
4. **KarmaMerchant** - Karma economy and Akasha storage
5. **SourceConsciousness** - Knowledge accumulation
6. **Reality System** - Reality management
7. **Decision Engine** - WSM decision analysis
8. **Evolution System** - Genetic evolution tracking

## Architecture

### Core Concept

A lightweight `SystemOrchestrator` class that:

- Provides a single entry point to access all major systems
- Handles initialization and dependency injection
- Provides simple coordination methods for cross-system operations
- Minimal - just enough to connect systems, not replace them

### Design Principles

1. **Composition over replacement** - Orchestrator coordinates, doesn't replace existing systems
2. **Lazy initialization** - Systems initialized only when needed
3. **Simple interface** - Easy to use, minimal complexity
4. **Extensible** - Easy to add new systems later

## Implementation Plan

### Phase 1: Core Orchestrator (MVP)

#### 1.1 Create SystemOrchestrator Class

**File**: `src/waft/core/orchestrator.py`

**Structure**:

```python
class SystemOrchestrator:
    """Lightweight coordinator for WAFT system integration."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self._systems = {}  # Lazy-loaded system cache

    # System accessors (lazy initialization)
    def get_being_system(self) -> BeingSystem
    def get_karma_merchant(self) -> KarmaMerchant
    def get_tavern_keeper(self) -> TavernKeeper
    def get_scint_system(self) -> ScintSystem  # If exists
    def get_source_consciousness(self) -> SourceConsciousness

    # Coordination methods (minimal MVP)
    def coordinate_being_quest(self, being_id: str, quest_id: str) -> Dict
    def coordinate_scint_stabilization(self, being_id: str, scint_data: Dict) -> Dict
    def get_system_status(self) -> Dict
```

#### 1.2 Integration Points

- **BeingSystem** - Access via `get_being_system()`
- **KarmaMerchant** - Access via `get_karma_merchant()`
- **TavernKeeper** - Access via `get_tavern_keeper()`
- **SourceConsciousness** - Access via `get_source_consciousness()`

#### 1.3 Basic Coordination Method

Implement one simple coordination method to demonstrate the concept:

- `coordinate_being_quest()` - Shows how a Being can interact with TavernKeeper for quests

### Phase 2: Simple Example Integration

#### 2.1 Create Example Script

**File**: `examples/test_orchestrator_integration.py`

Demonstrates:

- Initializing orchestrator
- Accessing multiple systems through orchestrator
- Simple cross-system operation (e.g., Being completes quest, earns karma)

#### 2.2 Documentation

**File**: `docs/SYSTEM_ORCHESTRATOR_GUIDE.md`

Basic usage guide:

- How to initialize
- How to access systems
- Simple coordination example

## Files to Create

1. `src/waft/core/orchestrator.py` - Main orchestrator class (~200-300 lines)
2. `examples/test_orchestrator_integration.py` - Simple integration test (~100 lines)
3. `docs/SYSTEM_ORCHESTRATOR_GUIDE.md` - Basic documentation (~100 lines)

## Files to Modify

1. `src/waft/__init__.py` - Export SystemOrchestrator if needed
2. `_work_efforts/devlog.md` - Log development progress

## Success Criteria (MVP)

- [ ] SystemOrchestrator class created with lazy system loading
- [ ] Can access BeingSystem, KarmaMerchant, TavernKeeper through orchestrator
- [ ] One coordination method working (e.g., `coordinate_being_quest`)
- [ ] Example script demonstrates basic integration
- [ ] Basic documentation created

## Future Extensions (Not in MVP)

- More coordination methods
- Event system for cross-system communication
- System health monitoring
- Dependency graph visualization
- Advanced orchestration patterns

## Dependencies

- Existing WAFT systems (BeingSystem, KarmaMerchant, TavernKeeper, etc.)
- No new external dependencies

## Testing Strategy

- Unit test: System accessors return correct instances
- Integration test: Example script runs successfully
- Manual test: Verify systems can be accessed and coordinated

## Notes

- This is intentionally minimal - just enough to prove the concept
- Can be extended later based on actual usage patterns
- Follows existing WAFT patterns (file-based, project_path initialization)
- Integrates with existing systems without modifying them