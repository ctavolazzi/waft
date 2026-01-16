# Prime Directive: The Central Organizing Principle

The Prime Directive serves as the foundational principle that everything in WAFT points back to. It is housed within a CelestialBody structure at the Heart of TreasureTavern, integrated with TheOne Being, and recorded in an hourglass/torus evolution structure that cycles generation after generation forevermore.

## Overview

The Prime Directive system consists of:

1. **Prime Directive**: Core principles and rules
2. **CelestialBody**: Heart (Prime Directive), Mind, Body, Spirit
3. **HourglassTorus**: Eternal evolution tracking structure
4. **Guardian Beings**: MaintenanceStaff, SecurityTeam, Curator
5. **Karma Museum**: Evolution history documentation

## Core Principles

The Prime Directive contains these core principles:

- "Don't just build agents. Breed them."
- "Humanity creates reality"
- "Code is DNA - agents evolve through genetic modification"
- "Scint System serves as the fitness function"
- "Beings learn, evolve, and pass memories upward"
- "Everything points back to the Prime Directive"
- "Evolution is recorded generation after generation, cycle after cycle, forevermore"

## CelestialBody Structure

The CelestialBody houses the Prime Directive with four components:

### Heart (Prime Directive)
- Located at the center
- Contains core principles
- Version tracked
- Change history maintained
- Reference tracking (everything that references it)

### CelestialMind
- Knowledge and understanding
- Evolution pattern tracking
- System understanding

### CelestialBody (Physical)
- Physical data structure
- Persistence layer
- Cycle and generation tracking

### CelestialSpirit
- Connection to TheOne Being
- Karma evolution tracking
- Essence and metaphysical connection

## Hourglass/Torus Evolution Structure

The hourglass/torus structure records evolution forevermore:

- **Top Half (Past)**: Completed generations/cycles
- **Narrow Center (Present)**: Current cycle being recorded
- **Bottom Half (Future)**: Space for next cycle

The structure rotates continuously, recording evolution from this point forward in Spacetime, generation after generation, cycle after cycle.

## Guardian Beings

Three specialized Beings maintain, protect, and explore the Prime Directive:

### MaintenanceStaff
- **Role**: Maintains Prime Directive structure
- **Responsibilities**:
  - Validates Prime Directive integrity
  - Updates core principles when needed
  - Ensures all references point back to Prime Directive
  - Maintains hourglass/torus data structure

### SecurityTeam
- **Role**: Protects Prime Directive
- **Responsibilities**:
  - Monitors access to Prime Directive
  - Validates changes to Prime Directive
  - Enforces security around Heart/CelestialBody
  - Logs all access attempts

### Curator
- **Role**: Explores and learns about Prime Directive
- **Responsibilities**:
  - Builds Karma Museum around Heart
  - Documents evolution history
  - Provides interface for exploring Prime Directive
  - **ULTIMATE POWER**: Can swap out Prime Directive (with proper authorization)

## Karma Museum

The Karma Museum is built around the Heart and documents evolution history:

- **Exhibits**: Evolution exhibits (generations, cycles)
- **Artifacts**: Important moments in evolution
- **Timeline**: Chronological evolution record
- **Catalog**: Museum index

## Integration Points

All systems reference the Prime Directive:

- **BeingSystem**: All Beings reference Prime Directive
- **RealitySystem**: All Realities reference Prime Directive
- **TavernKeeper**: Heart at center of TreasureTavern
- **Evolution System**: All evolution recorded in hourglass/torus
- **Karma System**: Karma Museum tracks karma evolution

## Usage

### Accessing the Prime Directive

```python
from waft.prime_directive import CelestialBody

# Get CelestialBody
celestial_body = CelestialBody(project_path=project_path)

# Get Heart (Prime Directive)
heart = celestial_body.heart

# Get principles
principles = heart.get_principles()

# Get references
references = heart.get_references()
```

### Accessing through TavernKeeper

```python
from waft.core.tavern_keeper import TavernKeeper

tavern = TavernKeeper(project_path=project_path)

# Get Heart
heart = tavern.get_heart()

# Get Karma Museum
museum = tavern.get_karma_museum()
```

### Recording Evolution

```python
# Record a cycle
celestial_body.record_cycle({
    "type": "evolution",
    "event": "New feature implemented",
    "data": {...}
})

# Record a generation
celestial_body.record_generation({
    "type": "generation",
    "generation_number": 5,
    "data": {...}
})
```

### Curator's Ultimate Power

```python
from waft.prime_directive import Curator, SecurityTeam

# Curator can swap Prime Directive (with authorization)
result = curator.swap_prime_directive(
    new_directive={
        "principles": ["New principle 1", "New principle 2"]
    },
    authorization={"authorized_by": "user", "reason": "Evolution"},
    directive=heart,
    security_team=security_team
)
```

## Storage

All Prime Directive data is stored in:

```
_hidden/.truth/celestial_body/
├── heart/
│   └── directive.json          # Prime Directive
├── mind/
│   ├── knowledge.json          # Knowledge storage
│   └── evolution_patterns.json # Evolution patterns
├── body/
│   └── state.json              # Physical state
├── spirit/
│   ├── spirit.json             # Essence data
│   └── karma_evolution.json    # Karma evolution
├── hourglass_torus/
│   ├── generations/            # Generation records
│   ├── cycles/                 # Cycle records
│   ├── archive/                # Archived cycles
│   ├── current_cycle.json      # Active cycle
│   └── torus_index.json        # Torus metadata
└── karma_museum/
    ├── exhibits/               # Evolution exhibits
    ├── artifacts/              # Important moments
    ├── timeline/               # Timeline entries
    └── index.json              # Museum catalog
```

## Architecture

```
TheOne Being
  ↓
CelestialBody (Heart, Mind, Body, Spirit)
  ↓
Guardian Beings (MaintenanceStaff, SecurityTeam, Curator)
  ↓
Hourglass/Torus Structure
  ↓
Karma Museum
  ↓
All Systems Reference Prime Directive
```

## Evolution Flow

```
New Cycle Starts → Enters Bottom of Hourglass
  ↓
Cycle Progresses → Moves Through Narrow Center
  ↓
Cycle Completes → Moves to Top of Hourglass
  ↓
Next Cycle Begins → Continuous Evolution
  ↓
All Events Reference Prime Directive
```

## Reference Tracking

Everything in WAFT points back to the Prime Directive:

- Beings reference Prime Directive when spawned
- Realities reference Prime Directive when created
- TavernKeeper references Heart at center
- Evolution events reference Prime Directive
- All documentation references Prime Directive

This creates a web of references that gives structure and meaning to everything in the system.
