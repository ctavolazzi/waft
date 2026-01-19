# /dnd-scenario - Run DnD Scenarios with Experimental Iteration

**Purpose:** Run interactive DnD scenarios in your campaign, create an Original Realm for scenario management, and support experimental iteration with state crystallization.

**Use when:** Want to run DnD scenarios, build campaign lore, test different scenario outcomes, or run controlled experiments with the same starting conditions.

---

## Overview

The `/dnd-scenario` command runs interactive DnD scenarios within your existing campaign system. It creates an Original Realm (`_realms/dnd_scenario_realm/`) for scenario management and supports:

- **Flexible Scenario Types**: Encounters, exploration, lore building
- **Party State Persistence**: Party state saved/loaded from realm
- **Experimental Iteration**: Crystallize initial state for repeated experiments
- **State Preservation**: Encrypted/frozen starting conditions
- **Scientific Method Integration**: Hypothesis testing through controlled iterations

---

## Quick Start

### Run an Encounter
```
/dnd-scenario --encounter
```

### Explore Freely
```
/dnd-scenario --explore
```

### Build Lore
```
/dnd-scenario --lore
```

### Resume Last Scenario
```
/dnd-scenario --resume
```

### Check Party State
```
/dnd-scenario --party-state
```

### Crystallize Current State (for experiments)
```
/dnd-scenario --crystallize
```

### Restore Initial State (start fresh iteration)
```
/dnd-scenario --restore-initial
```

### Run Experiment Iteration
```
/dnd-scenario --experiment exp_001 --iteration 1 --encounter
/dnd-scenario --experiment exp_001 --iteration 2 --encounter
/dnd-scenario --experiment exp_001 --iteration 3 --encounter
```

---

## Command Options

### Scenario Modes

- `--encounter` - Force an encounter scenario (combat or challenge)
- `--explore` - Free exploration mode (discover locations, NPCs, events)
- `--lore` - Focus on lore building (NPC interactions, historical events)
- `--resume` - Resume from last scenario state

### State Management

- `--party-state` - Show current party state
- `--crystallize` - Freeze current state as new initial state (for experiments)
- `--restore-initial` - Restore crystallized initial state (start fresh iteration)

### Experimental Iteration

- `--experiment [id]` - Run scenario as part of experiment iteration (validated: alphanumeric + underscore/hyphen, max 64 chars)
- `--iteration [n]` - Specify iteration number (validated: int, 1-10000)

---

## How It Works

### Original Realm

The command creates an Original Realm at `_realms/dnd_scenario_realm/` with:

- **PrimeBeing**: Realm governance and scenario coordination
- **Reality**: Scenario realm reality for Being system
- **State Persistence**: All scenario data saved to realm
- **Lore Accumulation**: Organized lore storage (locations, NPCs, events)
- **Crystallized State**: Encrypted initial states for experiments

### Scenario Execution

1. **Initialize Realm**: Creates realm structure if it doesn't exist
2. **Load Party State**: Loads party state from realm (or creates new)
3. **Run Scenario**: Executes scenario in specified mode
4. **Save Results**: Saves party state, encounter logs, lore entries
5. **Update History**: Tracks scenario history and progression

### Experimental Iteration

**Crystallization Process**:
1. Capture complete realm state (party, lore, world)
2. Encrypt using Pyrite's Fernet encryption
3. Generate SHA-256 hash + HMAC for verification
4. Store in `crystallized_state/` directory
5. Mark with version number (prevents replay attacks)

**Restoration Process**:
1. Load encrypted initial state
2. Verify hash + HMAC before decryption
3. Verify version number (prevent replay)
4. Backup current state
5. Decrypt and restore realm to initial conditions
6. Ready for new iteration

---

## Security Features

### Encryption
- **Algorithm**: Fernet (symmetric encryption via Pyrite)
- **Key Management**: Pyrite's existing key system
- **Key Storage**: `_pyrite/.secret_key` with 0o600 permissions

### Path Validation
- All paths validated using `_validate_realm_path()` pattern
- Prevents path traversal attacks
- Blocks symlinks
- Validates within realm directory

### Input Validation
- Experiment IDs: Alphanumeric + underscore/hyphen only, max 64 chars
- Iteration numbers: Integer, 1-10000 range
- All parameters validated before use

### State Integrity
- SHA-256 hashing for verification
- HMAC for additional integrity checks
- Version numbers prevent replay attacks
- File locking during operations
- Atomic operations (write to temp, verify, move)

---

## Example Usage

### Basic Scenario Run
```bash
# Run an encounter
waft dnd-scenario --encounter

# Explore the world
waft dnd-scenario --explore

# Build lore
waft dnd-scenario --lore
```

### Experimental Iteration
```bash
# Crystallize current state
waft dnd-scenario --crystallize

# Run first iteration
waft dnd-scenario --experiment exp_001 --iteration 1 --encounter

# Restore initial state
waft dnd-scenario --restore-initial

# Run second iteration (same starting conditions)
waft dnd-scenario --experiment exp_001 --iteration 2 --encounter
```

### State Management
```bash
# Check party state
waft dnd-scenario --party-state

# Resume from last scenario
waft dnd-scenario --resume
```

---

## Integration

### With Existing Systems
- **BeingSystem**: Party members are Beings
- **ExtendedCampaign**: Uses encounter mechanics from `long_dnd_campaign.py`
- **RealmColonizationSystem**: Creates and manages realm
- **RealitySystem**: Creates reality for scenario realm
- **Pyrite**: Uses encryption for state crystallization

### With Scientific Method
- **`/science-bitch`**: Integrates with scientific method workflow
- **Hypothesis Testing**: Run multiple iterations from same starting state
- **Data Collection**: Track outcomes per iteration
- **Analysis**: Compare results across iterations

---

## Realm Structure

```
_realms/dnd_scenario_realm/
├── realm_manifest.json          # Realm metadata
├── crystallized_state/          # Frozen initial states (encrypted)
│   ├── initial_realm_state_*.json.encrypted
│   ├── state_hash_*.txt         # SHA-256 hash
│   ├── state_hmac_*.txt         # HMAC
│   └── state_version_*.txt      # Version number
├── party_state.json             # Current party state
├── scenario_history.json        # All scenarios run
├── experiments/                 # Experimental iterations
│   └── [experiment_id]/
│       ├── iteration_[n]/
│       └── experiment_manifest.json
├── lore/                        # Accumulated lore
│   ├── locations/
│   ├── npcs/
│   ├── events/
│   └── world_history.md
├── encounters/                   # Encounter logs
└── campaigns/                    # Campaign sessions
```

---

## When to Use

**Use `/dnd-scenario` when**:
- ✅ Want to run DnD scenarios in your campaign
- ✅ Need to build campaign lore
- ✅ Want to test different scenario outcomes
- ✅ Need experimental iteration with same starting conditions
- ✅ Want to integrate with scientific method workflow
- ✅ Need party state persistence across scenarios

**Don't use `/dnd-scenario` when**:
- ❌ Just want to run a one-off campaign (use `long_dnd_campaign.py` directly)
- ❌ Don't need state persistence
- ❌ Don't need experimental iteration

---

## Security Considerations

- **Encryption**: All crystallized states are encrypted
- **Path Validation**: All paths validated to prevent traversal
- **Input Validation**: All parameters validated before use
- **State Integrity**: Hash + HMAC verification
- **File Permissions**: Proper permissions set (0o700/0o600)
- **Atomic Operations**: Safe state restoration with backups

---

## Troubleshooting

**Error: "Realm not found"**
- Solution: Realm is created automatically on first run
- Check: `_realms/dnd_scenario_realm/` directory exists

**Error: "Invalid experiment ID"**
- Solution: Use alphanumeric characters, underscores, and hyphens only
- Max length: 64 characters

**Error: "Invalid iteration"**
- Solution: Use integer between 1 and 10000

**Error: "State hash mismatch"**
- Solution: Crystallized state may be corrupted
- Check: Verify crystallized state files are intact

---

**This command provides a complete DnD scenario system with experimental iteration support, perfect for testing different scenario outcomes and building campaign lore.**

--- End Command ---
