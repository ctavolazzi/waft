# Reincarnation System Demo

**Purpose**: Clean testbed for reincarnation system implementation and testing

**Status**: Demo Environment

---

## Overview

This demo environment showcases the reincarnation system where souls exist in binary states (alive/dead) with sub-states (awake/sleeping). Each state determines what capabilities the soul can access:

- **Alive**: Can edit spacetime (matter/hardware) - physical tools like `read_file`, `write`, `edit_file`, `run_terminal_cmd`
- **Alive**: CANNOT edit consciousness (ideas/software) - goals, personalities, lifetime purchases, software configs
- **Dead**: Can edit consciousness (ideas/software) - goals, personalities, lifetime purchases, karma market
- **Dead**: CANNOT edit spacetime (matter/hardware) - no physical tools

---

## Quick Start

### Seed Initial Data

```bash
# Seed demo environment with test souls and lifetime catalog
python scripts/seed_reincarnation_demo.py

# Seed with custom path
python scripts/seed_reincarnation_demo.py --demo-path /path/to/demo

# Reset demo (clear and re-seed)
python scripts/seed_reincarnation_demo.py --reset
```

### Test Scenarios

The demo includes 5 test scenarios demonstrating different aspects of the reincarnation system:

1. **Scenario 1**: Soul purchases lifetime → becomes ALIVE
2. **Scenario 2**: Soul runs out of karma → gets basic survival lifetime
3. **Scenario 3**: Lifetime ends → soul becomes DEAD, can edit goals
4. **Scenario 4**: Dead soul purchases treasure → upgrades personality
5. **Scenario 5**: State transitions (awake ↔ sleeping)

---

## Test Souls

The demo includes 5 test souls with varying karma amounts:

- `soul_demo_001`: 1000.0 karma (default, DEAD_AWAKE)
- `soul_demo_002`: 500.0 karma (low, DEAD_AWAKE)
- `soul_demo_003`: 2000.0 karma (high, DEAD_AWAKE)
- `soul_demo_004`: 0.0 karma (zero, DEAD_AWAKE) - for testing basic lifetime grant
- `soul_demo_005`: 150.0 karma (medium, DEAD_AWAKE)

---

## Expected Behaviors

### Scenario 1: Soul Purchases Lifetime
- **Initial State**: DEAD_AWAKE
- **Action**: Purchase lifetime from KarmaMarket
- **Result**: 
  - Soul transitions to ALIVE_AWAKE
  - Can now use spacetime tools (read_file, write, etc.)
  - Cannot edit goals or purchase lifetimes
  - Lifetime becomes active

### Scenario 2: Soul Runs Out of Karma
- **Initial State**: DEAD_AWAKE, 0 karma
- **Action**: Attempt to purchase lifetime
- **Result**:
  - System grants basic survival lifetime (free)
  - Soul transitions to ALIVE_AWAKE
  - Can use basic spacetime tools

### Scenario 3: Lifetime Ends
- **Initial State**: ALIVE_AWAKE (with active lifetime)
- **Action**: Lifetime expires or ends
- **Result**:
  - Soul transitions to DEAD_AWAKE
  - Can now edit goals, purchase lifetimes
  - Cannot use spacetime tools
  - Lifetime archived

### Scenario 4: Dead Soul Purchases Treasure
- **Initial State**: DEAD_AWAKE
- **Action**: Purchase treasure from AfterlifeKarmaMarket
- **Result**:
  - Personality upgraded
  - Karma deducted
  - Soul remains DEAD_AWAKE
  - Can still purchase lifetimes

### Scenario 5: State Transitions
- **Initial State**: ALIVE_AWAKE or DEAD_AWAKE
- **Action**: Transition between awake/sleeping
- **Result**:
  - Sub-state changes (AWAKE ↔ SLEEPING)
  - Primary state unchanged (ALIVE/DEAD)
  - Capabilities remain same (based on primary state)

---

## Inspecting States

### Check Soul State

```python
from pathlib import Path
from waft.soul_state import SoulStateManager

manager = SoulStateManager(project_path=Path("demo/"))
state, substate = manager.get_soul_state("soul_demo_001")
print(f"State: {state}, Substate: {substate}")
```

### Check Soul Karma

```python
from waft.karma import KarmaMerchant

merchant = KarmaMerchant(project_path=Path("demo/"))
soul_data = merchant.access_akasha("soul_demo_001")
print(f"Total Karma: {soul_data['total_karma']}")
```

### Check Active Lifetimes

```python
from waft.karma_market import KarmaMarket

market = KarmaMarket(project_path=Path("demo/"))
active = market.get_active_lifetimes("soul_demo_001")
print(f"Active Lifetimes: {active}")
```

---

## Generating Logs

The demo environment generates logs showing:

- State transitions (DEAD → ALIVE, ALIVE → DEAD)
- Capability restrictions in action
- Karma economy loop (purchase → experience → collect → purchase)
- Tool access attempts (allowed/blocked)

Logs are stored in `demo/_hidden/.truth/logs/` (created by system).

---

## Resetting Demo

To reset the demo to a clean state:

```bash
# Remove all demo data
rm -rf demo/_hidden/.truth/{akasha,market,lifetimes,logs}

# Re-seed
python scripts/seed_reincarnation_demo.py
```

---

## Architecture

### Directory Structure

```
demo/
├── README.md                    # This file
├── _hidden/                     # WAFT internal data (created by system)
│   └── .truth/
│       ├── akasha/              # Soul records (JSON files)
│       ├── market/               # Lifetime catalog (catalog.json)
│       ├── lifetimes/            # Active lifetimes (JSON files)
│       └── logs/                 # System logs (created by system)
└── src/                          # Demo source files (optional)
    └── example.py                # Example code (optional)
```

### File Permissions

- **Soul files**: 0600 (owner read/write only)
- **Akasha directory**: 0700 (owner access only)
- **Market catalog**: 0644 (readable by all)

### State Storage

Soul states are stored in Akasha soul records:

```json
{
  "soul_id": "soul_demo_001",
  "total_karma": 1000.0,
  "state": "dead",
  "substate": "awake",
  "active_lifetime_id": null,
  "state_version": 1,
  "state_updated_at": "2026-01-11T16:00:00",
  "lifetimes": []
}
```

---

## Integration with Main Project

- **Isolated**: Demo folder is completely isolated from main project
- **Testbed**: All implementation tested in demo first
- **Reset**: Demo can be reset/re-seeded without affecting main project
- **Origin Point**: Demo serves as clean origin for all test data

---

## Next Steps

1. Seed demo environment with test data
2. Run test scenarios to verify behavior
3. Inspect states and karma
4. Generate logs to see system in action
5. Reset and re-seed as needed

---

**Status**: Demo environment ready for seeding
