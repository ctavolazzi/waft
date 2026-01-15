---
name: Prime Directive Celestial Structure
overview: Create a Prime Directive system with a CelestialBody (Heart, Mind, Body, Spirit) at the center of TreasureTavern, integrated with TheOne Being, featuring MaintenanceStaff, SecurityTeam, and Curator Beings, all recorded in an hourglass/torus evolution structure that cycles generation after generation forevermore.
todos:
  - id: create_prime_directive_module
    content: Create src/waft/prime_directive/ module with __init__.py, directive.py (PrimeDirective class), celestial_body.py (CelestialBody with Heart/Mind/Body/Spirit), hourglass_torus.py (evolution tracking), guardians.py (MaintenanceStaff, SecurityTeam, Curator), and museum.py (Karma Museum)
    status: pending
  - id: implement_prime_directive_class
    content: Implement PrimeDirective class with core principles storage, version tracking, change history, validation methods, and reference tracking
    status: pending
  - id: implement_celestial_body
    content: Implement CelestialBody class with Heart (PrimeDirective), CelestialMind (knowledge/evolution), CelestialBody (physical structure), CelestialSpirit (TheOne connection/karma), and methods for initialization, evolution, cycle recording, and history querying
    status: pending
  - id: implement_hourglass_torus
    content: Implement HourglassTorus class with generation/cycle rotation, evolution event recording, archiving of old cycles, query interface, and torus rotation logic for continuous evolution
    status: pending
  - id: create_guardian_beings
    content: Create MaintenanceStaff, SecurityTeam, and Curator Being classes extending Being class with specialized roles, methods, and Prime Directive references
    status: pending
  - id: implement_curator_swap_power
    content: "Implement Curator's ultimate power: swap_prime_directive() method with SecurityTeam validation, backup creation, reference updates, hourglass/torus recording, and Karma Museum logging"
    status: pending
  - id: integrate_with_the_one
    content: Modify BeingSystem.get_or_create_the_one() to initialize CelestialBody and create guardian Beings when TheOne is created
    status: pending
  - id: create_storage_structure
    content: Create _hidden/.truth/celestial_body/ directory structure with heart/, mind/, body/, spirit/, hourglass_torus/, and karma_museum/ subdirectories
    status: pending
  - id: integrate_with_tavern_keeper
    content: Integrate Heart location into TavernKeeper, make TreasureTavern reference Heart at center, and make Karma Museum accessible through TavernKeeper
    status: pending
  - id: add_reference_tracking
    content: Add Prime Directive reference tracking to BeingSystem, RealitySystem, Evolution System, and all major components so everything points back to Prime Directive
    status: pending
  - id: create_karma_museum
    content: Implement Karma Museum structure with exhibits/, artifacts/, timeline/, and index.json for evolution history documentation
    status: pending
  - id: update_documentation
    content: Update README.md, create docs/PRIME_DIRECTIVE.md, update BeingSystem/TavernKeeper docs, and create architecture diagram showing all relationships
    status: pending

category: dreams
confidence: 0.69
constellation_date: 2026-01-14
---

# Prime Directive & CelestialBody Architecture

## Overview

Create a foundational Prime Directive system that serves as the central organizing principle of WAFT, housed within a CelestialBody structure at the Heart of TreasureTavern. The system includes three specialized Beings (MaintenanceStaff, SecurityTeam, Curator) and uses an hourglass/torus data structure for eternal evolution tracking.

## Core Components

### 1. Prime Directive Structure

**Location**: `src/waft/prime_directive/`

**Files**:

- `__init__.py` - Module initialization
- `directive.py` - PrimeDirective class (core principles)
- `celestial_body.py` - CelestialBody with Heart, Mind, Body, Spirit
- `hourglass_torus.py` - Evolution tracking structure
- `guardians.py` - MaintenanceStaff, SecurityTeam, Curator Beings

**Prime Directive Content** (from user selection: core principles):

- "Don't just build agents. Breed them."
- "Humanity creates reality"
- Core WAFT principles from README.md and system documentation
- Evolutionary principles (Scint system, fitness functions)
- Being lifecycle principles

### 2. CelestialBody Architecture

**Structure**:

```
CelestialBody
├── Heart (Prime Directive - at center)
├── CelestialMind (Knowledge, understanding, evolution tracking)
├── CelestialBody (Physical structure, data storage, persistence)
└── CelestialSpirit (Essence, karma, connection to TheOne)
```

**Integration with TheOne**:

- CelestialBody is created as part of TheOne Being
- All three components (Mind, Body, Spirit) are initialized when TheOne is created
- CelestialBody references TheOne's being_id
- Hourglass/torus structure records all evolution from this point forward

### 3. Hourglass/Torus Evolution Structure

**Concept**: A toroidal (doughnut-shaped) data structure that cycles through generations and cycles, recording evolution forevermore.

**Implementation**:

- **Top Half (Past)**: Completed generations/cycles
- **Narrow Center (Present)**: Current generation/cycle being recorded
- **Bottom Half (Future)**: Space for next generation/cycle

**Data Flow**:

1. New cycle starts → enters bottom of hourglass
2. Cycle progresses → moves through narrow center
3. Cycle completes → moves to top of hourglass
4. Top cycles eventually overflow → oldest cycles archived
5. Structure rotates (torus) → continuous evolution

**Storage**: `_hidden/.truth/celestial_body/hourglass_torus/`

- `generations/` - Each generation as JSON
- `cycles/` - Each cycle within generations
- `current_cycle.json` - Active cycle being recorded
- `torus_index.json` - Metadata about torus structure

### 4. Guardian Beings

**Three Specialized Beings**:

#### MaintenanceStaff Being

- **Role**: Maintains Prime Directive structure
- **Responsibilities**:
  - Validates Prime Directive integrity
  - Updates core principles when needed
  - Ensures all references point back to Prime Directive
  - Maintains hourglass/torus data structure
- **Being ID**: `maintenance_staff_prime_directive`
- **Parent**: TheOne

#### SecurityTeam Being

- **Role**: Protects Prime Directive
- **Responsibilities**:
  - Monitors access to Prime Directive
  - Validates changes to Prime Directive
  - Enforces security around Heart/CelestialBody
  - Logs all access attempts
- **Being ID**: `security_team_prime_directive`
- **Parent**: TheOne

#### Curator Being

- **Role**: Explores and learns about Prime Directive
- **Responsibilities**:
  - Builds Karma Museum around Heart
  - Documents evolution history
  - Provides interface for exploring Prime Directive
  - **ULTIMATE POWER**: Can swap out Prime Directive (with proper authorization)
- **Being ID**: `curator_prime_directive`
- **Parent**: TheOne

### 5. Karma Museum

**Location**: `_hidden/.truth/celestial_body/karma_museum/`

**Structure**:

- `exhibits/` - Evolution exhibits (generations, cycles)
- `artifacts/` - Important moments in evolution
- `timeline/` - Chronological evolution record
- `index.json` - Museum catalog

**Integration**: Built around the Heart, accessible through Curator Being

### 6. Integration Points

**All Systems Reference Prime Directive**:

- BeingSystem: References Prime Directive in Being creation
- RealitySystem: References Prime Directive in Reality creation
- TavernKeeper: Heart at center of TreasureTavern
- Evolution System: All evolution recorded in hourglass/torus
- Karma System: Karma Museum tracks karma evolution
- Documentation: All docs reference Prime Directive

**File Structure**:

```
src/waft/prime_directive/
├── __init__.py
├── directive.py              # PrimeDirective class
├── celestial_body.py         # CelestialBody with Heart/Mind/Body/Spirit
├── hourglass_torus.py        # Evolution tracking structure
├── guardians.py              # MaintenanceStaff, SecurityTeam, Curator
└── museum.py                 # Karma Museum structure

_hidden/.truth/
├── celestial_body/
│   ├── heart/                # Prime Directive storage
│   │   └── directive.json
│   ├── mind/                 # CelestialMind data
│   ├── body/                 # CelestialBody data
│   ├── spirit/                # CelestialSpirit data
│   ├── hourglass_torus/      # Evolution records
│   └── karma_museum/         # Museum exhibits
└── beings/
    ├── the_one.json          # Updated with CelestialBody reference
    ├── maintenance_staff_prime_directive.json
    ├── security_team_prime_directive.json
    └── curator_prime_directive.json
```

## Implementation Details

### PrimeDirective Class

- Stores core principles
- Version tracking
- Change history
- Validation methods
- Reference tracking (what references this directive)

### CelestialBody Class

- Heart: PrimeDirective instance
- Mind: Evolution tracking, knowledge storage
- Body: Physical data structure, persistence
- Spirit: Connection to TheOne, karma integration
- Methods: Initialize, evolve, record_cycle, query_history

### HourglassTorus Class

- Manages generation/cycle rotation
- Records evolution events
- Archives old cycles
- Provides query interface for evolution history
- Torus rotation logic (continuous cycle)

### Guardian Beings

- Extend Being class with specialized roles
- Each has methods specific to their role
- All reference Prime Directive in their purpose
- Can interact with CelestialBody components

### Curator's Ultimate Power

- `swap_prime_directive(new_directive, authorization)` method
- Requires validation from SecurityTeam
- Creates backup of old directive
- Updates all references
- Records change in hourglass/torus
- Logs in Karma Museum

## Integration with Existing Systems

### BeingSystem Integration

- Modify `get_or_create_the_one()` to initialize CelestialBody
- Create guardian Beings when TheOne is created
- All new Beings reference Prime Directive

### TavernKeeper Integration

- Heart location: `src/waft/core/tavern_keeper/heart.py`
- TreasureTavern references Heart at center
- Karma Museum accessible through TavernKeeper

### Evolution System Integration

- All evolution events recorded in hourglass/torus
- Generation tracking through CelestialMind
- Cycle tracking through CelestialBody

## Data Flow

```
TheOne Being Created
  ↓
CelestialBody Initialized (Heart, Mind, Body, Spirit)
  ↓
Guardian Beings Created (MaintenanceStaff, SecurityTeam, Curator)
  ↓
Hourglass/Torus Structure Initialized
  ↓
First Cycle Begins → Recorded in Torus
  ↓
Evolution Events → Recorded in Narrow Center
  ↓
Cycle Completes → Moves to Top of Hourglass
  ↓
Next Cycle Begins → Continuous Evolution
  ↓
All Events Reference Prime Directive
```

## Testing Strategy

1. Test CelestialBody initialization with TheOne
2. Test hourglass/torus cycle recording
3. Test guardian Being creation and roles
4. Test Curator's Prime Directive swap (with authorization)
5. Test reference tracking (everything points back)
6. Test Karma Museum exhibit creation
7. Test torus rotation and archiving

## Documentation Updates

- Update README.md to reference Prime Directive
- Create `docs/PRIME_DIRECTIVE.md` explaining the system
- Update BeingSystem docs to mention CelestialBody
- Update TavernKeeper docs to mention Heart at center
- Create architecture diagram showing relationships