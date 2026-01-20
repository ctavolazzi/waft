# System Orchestrator Guide

## Overview

The **SystemOrchestrator** is a lightweight coordinator that provides unified access to all major WAFT systems. It simplifies system integration by:

- **Single Entry Point** - Access all systems through one orchestrator instance
- **Lazy Initialization** - Systems are only initialized when first accessed
- **Cross-System Coordination** - Simplifies operations that span multiple systems
- **Minimal Overhead** - Thin coordination layer that doesn't replace existing systems

## Quick Start

### Basic Initialization

```python
from pathlib import Path
from waft.core.orchestrator import SystemOrchestrator

# Initialize with project path (defaults to current directory)
orchestrator = SystemOrchestrator(project_path=Path.cwd())

# Access systems as needed
being_system = orchestrator.get_being_system()
karma_merchant = orchestrator.get_karma_merchant()
tavern_keeper = orchestrator.get_tavern_keeper()
```

### Complete Example

```python
from waft.core.orchestrator import SystemOrchestrator
from pathlib import Path

# Initialize orchestrator
orch = SystemOrchestrator(Path("/path/to/project"))

# Create a reality and spawn a being
reality_system = orch.get_reality_system()
reality = reality_system.create_reality(
    reality_type="TESTING",
    configuration={"name": "Quest Reality"},
    source_id="source_consciousness"
)

being_system = orch.get_being_system()
being = being_system.spawn_being(
    reality_id=reality["reality_id"],
    parent_being_id=None,
    initial_skills={"debugging": 0.7}
)

# Coordinate a quest (cross-system operation)
result = orch.coordinate_being_quest(
    being_id=being.being_id,
    quest_data={
        "quest_type": "debug",
        "difficulty": 3,
        "ability": "INT"
    }
)

print(f"Quest success: {result['success']}")
print(f"Karma earned: {result['karma_impact']}")
print(f"Narrative: {result['narrative']}")
```

## Available Systems

The orchestrator provides access to the following WAFT systems:

### 1. SourceConsciousness

Tracks knowledge accumulation and ancestral chains across all WAFT permutations.

```python
source = orchestrator.get_source_consciousness(source_id="source_consciousness")

# Get source statistics
stats = source.get_source_stats()
print(f"Total capacity: {stats['total_capacity']}")
print(f"Accumulated karma: {stats['accumulated_karma']}")
```

**Storage:** `_hidden/.truth/source/`

### 2. BeingSystem

Manages Being entities across realities, handling spawning, lifecycle, reincarnation, and evolution.

```python
being_system = orchestrator.get_being_system()

# Spawn a new being
being = being_system.spawn_being(
    reality_id="reality_001",
    parent_being_id=None,
    initial_skills={"problem_solving": 0.8}
)

# Reincarnate a dead being
reborn = being_system.reincarnate_being(
    dead_being_id="being_123",
    reality_id="reality_002",
    use_karma=True,
    purchase_order=["memory_continuity", "skill_inheritance"]
)
```

**Storage:** `_hidden/.truth/beings/`

### 3. KarmaMerchant

Manages the karma economy and Akasha records for all beings.

```python
karma_merchant = orchestrator.get_karma_merchant()

# Calculate karma from life experiences
karma = karma_merchant.calculate_karma(life_log={
    "experiences": [
        {"intensity": 0.8, "type": "learning"},
        {"intensity": 0.6, "type": "creation"}
    ]
})
```

**Storage:** `_hidden/.truth/` (Akasha), `_hidden/.truth/store/` (merchant store)

### 4. TavernKeeper

Manages RPG mechanics including D&D 5e character stats, dice rolls, narrative generation, and quest rewards.

```python
tavern_keeper = orchestrator.get_tavern_keeper()

# Get character stats
character = tavern_keeper.get_character()
print(f"Level: {character['level']}")
print(f"INT: {character['INT']}")

# Roll an ability check
roll_result = tavern_keeper.roll_check(
    ability="INT",
    dc=15,
    advantage=True
)
print(f"Roll: {roll_result['total']} - {'Success!' if roll_result['success'] else 'Failed'}")

# Generate narrative
narrative = tavern_keeper.narrate(
    event="quest_complete",
    outcome="success",
    context={"location": "Mystic Library"}
)
```

**Storage:** `_pyrite/.waft/chronicles.json`

### 5. RealitySystem

Manages different reality types (LEARNING, TESTING, EVOLUTION, RESEARCH, CREATIVE, CUSTOM).

```python
reality_system = orchestrator.get_reality_system()

# Create a new reality
reality = reality_system.create_reality(
    reality_type="LEARNING",
    configuration={
        "name": "Python Mastery",
        "skills_to_learn": ["async", "typing", "testing"]
    },
    source_id="source_consciousness"
)

# Start the reality
reality_system.start_reality(reality["reality_id"])

# End the reality and collect outcomes
outcomes = reality_system.end_reality(
    reality_id=reality["reality_id"],
    outcomes={
        "skills_learned": ["async"],
        "memories": ["Learned event loop mechanics"]
    }
)
```

**Storage:** `_hidden/.truth/realities/`

### 6. RegexScintDetector

Scans for reality fractures (scints) in text output.

```python
scint_detector = orchestrator.get_scint_detector()

# Scan text for reality fractures
scints = scint_detector.scan(
    output="Some text that might contain errors or inconsistencies",
    context={"difficulty": 3}
)

for scint in scints:
    print(f"{scint.scint_type}: {scint.description} (severity: {scint.severity})")
```

**Scint Types:**
- `SYNTAX_TEAR` - Formatting errors (JSON, XML, Code)
- `LOGIC_FRACTURE` - Math errors, contradictions, schema violations
- `HALLUCINATION` - Fabricated facts, wrong citations
- `SAFETY_VOID` - Harmful content, PII leaks

### 7. WAFTKernel

Orchestrates TheObserver (flight recorder), EmpiricaManager (epistemic state), and GamificationManager.

```python
kernel = orchestrator.get_waft_kernel()

# Perform boot sequence
boot_result = kernel.boot_sequence()

# Get epistemic state
state = kernel.get_epistemic_state()
print(f"Current phase: {state['phase']}")
print(f"Confidence: {state['confidence']}")

# Check kernel status
status = kernel.kernel_status_check()
```

### 8. NowCycleManager

Manages Being lifecycle cycles, handling state updates, sleep processing, and death conditions.

```python
cycle_manager = orchestrator.get_now_cycle_manager()

# Execute one cycle (async)
import asyncio

result = await cycle_manager.execute_cycle()
print(f"Cycle {result['cycle_number']} complete")
print(f"Beings processed: {result['beings_processed']}")
print(f"Deaths: {result['deaths']}")
```

## Coordination Methods

The orchestrator provides high-level coordination methods that simplify cross-system operations.

### coordinate_being_quest()

Coordinates a Being's quest through multiple systems:

1. Loads Being from BeingSystem
2. Rolls ability checks through TavernKeeper
3. Detects reality fractures (scints) in quest output
4. Awards rewards based on performance
5. Updates Being's experience and karma

```python
result = orchestrator.coordinate_being_quest(
    being_id="hero_001",
    quest_data={
        "quest_type": "debug",      # Type of quest
        "difficulty": 3,             # 1-5 difficulty scale
        "ability": "INT",            # STR, DEX, CON, INT, WIS, CHA
        "context": {                 # Optional narrative context
            "location": "Digital Forest",
            "objective": "Fix memory leak"
        }
    }
)

# Result contains:
{
    "success": True,
    "roll_result": {
        "total": 18,
        "d20": 15,
        "modifier": 3,
        "dc": 16,
        "success": True
    },
    "narrative": "In the Digital Forest, you discover...",
    "scints_detected": [
        {
            "type": "LOGIC_FRACTURE",
            "severity": 0.6,
            "description": "Logical inconsistency detected"
        }
    ],
    "rewards": {
        "insight": 30,
        "credits": 15,
        "integrity_change": -5
    },
    "karma_impact": 250
}
```

**DC Calculation:** `DC = 10 + (difficulty × 2)`

**Karma Calculation:**
- Success: `difficulty × 100`
- Scint penalty: `-50 per scint`

### coordinate_scint_stabilization()

Coordinates a Being's attempt to stabilize a reality fracture.

```python
result = orchestrator.coordinate_scint_stabilization(
    being_id="hero_001",
    scint_data={
        "scint_type": "LOGIC_FRACTURE",
        "severity": 0.6,
        "description": "Mathematical inconsistency in calculation"
    }
)

# Result contains:
{
    "stabilized": True,
    "ability_used": "INT",       # Determined by scint_type
    "roll_result": {
        "total": 19,
        "d20": 16,
        "modifier": 3,
        "dc": 22,
        "success": True
    },
    "karma_reward": 300
}
```

**Ability Mapping:**
- `SYNTAX_TEAR` → CHA
- `LOGIC_FRACTURE` → INT
- `HALLUCINATION` → INT
- `SAFETY_VOID` → WIS

**DC Calculation:** `DC = 10 + (severity × 20)`

**Karma Reward:** `karma = severity × 500`

### get_system_status()

Returns comprehensive status of all initialized systems.

```python
status = orchestrator.get_system_status()

# Status contains:
{
    "project_path": "/path/to/project",
    "initialized_systems": [
        "source_consciousness:source_consciousness",
        "being_system",
        "karma_merchant",
        "tavern_keeper"
    ],
    "system_details": {
        "being_system": {
            "beings_count": 5
        },
        "source_consciousness": {
            "source_id": "source_consciousness",
            "total_capacity": 1000,
            "accumulated_karma": 2500
        },
        "tavern_keeper": {
            "character_level": 3,
            "insight": 450,
            "integrity": 85
        }
    }
}
```

## Utility Methods

### list_available_systems()

Lists all systems that can be accessed through the orchestrator.

```python
systems = orchestrator.list_available_systems()
# Returns: ["source_consciousness", "being_system", "karma_merchant", ...]
```

### reset_system()

Removes a system from cache, forcing reinitialization on next access.

```python
# Reset a specific system
orchestrator.reset_system("being_system")

# Next access will reinitialize
being_system = orchestrator.get_being_system()  # Fresh instance
```

### reset_all_systems()

Clears all cached systems.

```python
orchestrator.reset_all_systems()
```

## Design Patterns

### Lazy Initialization

Systems are only initialized when first accessed:

```python
# Orchestrator initialized, no systems loaded yet
orch = SystemOrchestrator(project_path)

# First access triggers initialization
being_system = orch.get_being_system()  # Loads BeingSystem + SourceConsciousness

# Subsequent accesses use cached instance
being_system_2 = orch.get_being_system()  # Returns cached instance
assert being_system is being_system_2  # Same instance
```

### Shared Dependencies

Systems that depend on SourceConsciousness automatically share the same instance:

```python
# Both systems will share the same SourceConsciousness
being_system = orch.get_being_system()
reality_system = orch.get_reality_system()

# Verify shared source
source_1 = orch.get_source_consciousness()
source_2 = being_system.source_consciousness
assert source_1 is source_2  # Same instance
```

### Dependency Injection

You can provide custom system instances:

```python
# Create custom SourceConsciousness
custom_source = SourceConsciousness(project_path, source_id="custom_source")

# Inject into BeingSystem
being_system = orch.get_being_system(source_consciousness=custom_source)

# Now BeingSystem uses custom source
assert being_system.source_consciousness is custom_source
```

## File Structure

The orchestrator manages systems that use this file structure:

```
project_path/
├── _hidden/
│   └── .truth/                  # Permissions: 0o700 (owner-only)
│       ├── beings/              # BeingSystem storage
│       │   └── [being_id].json
│       ├── realities/           # RealitySystem storage
│       │   └── [reality_id].json
│       ├── source/              # SourceConsciousness storage
│       │   └── [source_id].json
│       ├── store/               # KarmaMerchant store
│       └── [soul_id].json       # Akasha records (KarmaMerchant)
├── _pyrite/
│   └── .waft/
│       └── chronicles.json      # TavernKeeper D&D data
└── [project files...]
```

## Error Handling

All system accessors handle initialization errors gracefully:

```python
try:
    being_system = orchestrator.get_being_system()
except Exception as e:
    print(f"Failed to initialize BeingSystem: {e}")
```

Coordination methods return error information:

```python
result = orchestrator.coordinate_being_quest(
    being_id="nonexistent_being",
    quest_data={...}
)

if not result["success"]:
    print(f"Error: {result.get('error')}")
```

## Best Practices

### 1. Single Orchestrator Instance

Create one orchestrator per project and reuse it:

```python
# Good: Single orchestrator
orchestrator = SystemOrchestrator(project_path)
being_sys = orchestrator.get_being_system()
karma = orchestrator.get_karma_merchant()

# Avoid: Multiple orchestrators
orchestrator1 = SystemOrchestrator(project_path)
orchestrator2 = SystemOrchestrator(project_path)  # Unnecessary
```

### 2. Let Systems Share Dependencies

Don't manually create shared dependencies unless you need custom configuration:

```python
# Good: Automatic sharing
being_system = orch.get_being_system()
reality_system = orch.get_reality_system()

# Avoid: Manual creation (unless needed)
source = SourceConsciousness(project_path)
being_system = BeingSystem(project_path, source)
reality_system = RealitySystem(project_path, source)
```

### 3. Use Coordination Methods

Prefer coordination methods over manual cross-system operations:

```python
# Good: Use coordination method
result = orch.coordinate_being_quest(being_id, quest_data)

# Avoid: Manual coordination (more code, easy to miss steps)
being = being_system.load_being(being_id)
roll_result = tavern_keeper.roll_check(...)
narrative = tavern_keeper.narrate(...)
scints = scint_detector.scan(narrative)
# ... many more steps
```

### 4. Check System Status

Use `get_system_status()` to verify system health:

```python
status = orchestrator.get_system_status()
print(f"Initialized systems: {len(status['initialized_systems'])}")

if "being_system" in status["initialized_systems"]:
    details = status["system_details"]["being_system"]
    print(f"Total beings: {details['beings_count']}")
```

## Examples

See `examples/test_orchestrator_integration.py` for a complete working example that demonstrates:

1. Orchestrator initialization
2. Accessing multiple systems
3. Creating realities and beings
4. Coordinating quests with karma rewards
5. Detecting and stabilizing scints
6. Checking system status
7. Accessing TavernKeeper character stats

Run the example:

```bash
python examples/test_orchestrator_integration.py
```

## Future Extensions

The orchestrator can be extended with:

- **Event System** - Cross-system event broadcasting
- **System Health Monitoring** - Automatic health checks and alerts
- **Dependency Graph** - Visualize system dependencies
- **Advanced Coordination Patterns** - More complex multi-system workflows
- **Transaction Support** - Rollback failed cross-system operations
- **Performance Monitoring** - Track system usage and performance

## See Also

- `src/waft/core/kernel.py` - WAFTKernel orchestrator
- `src/waft/core/now_cycle.py` - NowCycleManager
- `src/waft/being.py` - BeingSystem
- `src/waft/karma.py` - KarmaMerchant
- `src/waft/core/tavern_keeper/keeper.py` - TavernKeeper
- `src/gym/rpg/scint.py` - RegexScintDetector
