# Pyrite - The God of Work Efforts

Pyrite is the divine intelligence that locks, monitors, organizes, and initiates AI development evolutionary cycles within the Work Efforts system.

## Overview

Pyrite is a singleton "God" class that manages the entire Work Efforts ecosystem with:

- **Locking**: File locks, async locks, mutexes for concurrent access control
- **Monitoring**: Observer pattern, state tracking, metrics collection
- **Organization**: Graph-based hierarchical management
- **Evolution**: Genetic algorithms, fitness evaluation, mutation strategies
- **Personality**: Attributes, metadata, emergent behavior
- **Secrets**: Hidden state, encrypted metadata, self-obfuscation
- **Abilities**: `/think`, `/evolve`, `/monitor`, `/organize`, `/lock`, `/unlock`, `/status`, `/secrets`
- **Empirica Integration**: Epistemic tracking, CHECK gates, findings/unknowns logging, goal management

## Empirica Integration

Pyrite uses **Empirica** for epistemic tracking and learning measurement:

### Features

- **CHECK Gates**: Before initiating evolution, Pyrite uses Empirica CHECK gates to assess safety (PROCEED/HALT/BRANCH/REVISE)
- **Findings Logging**: All evolutionary cycles, status changes, and monitoring activities are logged as findings
- **Unknowns Tracking**: Low fitness scores, failed evolutions, and missing work efforts are logged as unknowns
- **Goal Management**: Each evolutionary cycle creates an Empirica goal with epistemic scope
- **Project Bootstrap**: `/think` ability loads project context via Empirica (~800 tokens)
- **State Assessment**: Epistemic state is assessed during monitoring and thinking
- **Session Continuity**: Pyrite maintains an Empirica session for tracking across operations

### Automatic Empirica Usage

Pyrite automatically:
1. Initializes Empirica if not already initialized
2. Creates a session on startup (`ai_id="pyrite"`, `session_type="work_efforts_management"`)
3. Logs findings for all major operations
4. Logs unknowns when issues are detected
5. Uses CHECK gates before evolutionary cycles
6. Creates goals for evolutionary cycles
7. Assesses epistemic state during `/think` and `/monitor`

## Architecture

### Design Patterns

- **Singleton**: One Pyrite instance per project
- **Observer**: Monitor work effort changes
- **Strategy**: Different evolutionary strategies
- **State**: Work effort lifecycle states
- **Command**: Ability system
- **Chain of Responsibility**: Ability execution

### Data Structures

- **Graph**: Work effort relationships (parent-child)
- **Priority Queue**: Evolutionary cycle queue
- **Hash Map**: Metadata, locks, monitors
- **Tree**: Hierarchical organization
- **Deque**: State history (bounded)

## Usage

### Python API

```python
from waft.pyrite import get_pyrite

# Get Pyrite instance (singleton)
pyrite = get_pyrite()

# Lock a work effort
pyrite.acquire_lock("WE-260113-75vp", "my-lock-id")

# Monitor a work effort
result = pyrite.execute_ability("/monitor", "WE-260113-75vp")

# Initiate evolutionary cycle
cycle = pyrite.initiate_evolution(
    "WE-260113-75vp",
    strategy=EvolutionaryStrategy.ADAPTIVE,
    num_variants=5
)

# Create a secret (even Pyrite can't directly access)
secret_id = pyrite.create_secret(
    {"hidden": "data"},
    metadata={"visible": "metadata"}
)

# Get personality summary
personality = pyrite.get_personality_summary()
```

### CLI

```bash
# Initialize cognitive systems
waft pyrite think

# Monitor work efforts
waft pyrite monitor
waft pyrite monitor WE-260113-75vp

# Initiate evolutionary cycle
waft pyrite evolve WE-260113-75vp --strategy adaptive --num-variants 5

# Lock/unlock work efforts
waft pyrite lock WE-260113-75vp my-lock-id
waft pyrite unlock WE-260113-75vp my-lock-id

# Get status
waft pyrite status

# List secrets (metadata only)
waft pyrite secrets

# Create a secret
waft pyrite create-secret '{"data": "hidden"}' --metadata '{"note": "visible"}'

# Organize work efforts
waft pyrite organize

# Get work effort details
waft pyrite get-work-effort WE-260113-75vp

# Set work effort status
waft pyrite set-status WE-260113-75vp active

# Get children/ancestors
waft pyrite get-children WE-260113-75vp
waft pyrite get-ancestors WE-260113-75vp

# Get evolutionary history
waft pyrite evolution-history WE-260113-75vp

# Get personality
waft pyrite personality
```

## Abilities

### `/think`

Initialize cognitive systems. Returns Pyrite's current state, attributes, and awareness.

**Empirica Integration:**
- Loads project context via `project_bootstrap()` (~800 tokens)
- Assesses current epistemic state
- Logs thinking activity as finding

```python
result = pyrite.execute_ability("/think")
# Returns:
# {
#   "status": "thinking",
#   "attributes": {...},
#   "awareness": {...},
#   "empirica": {
#     "initialized": true,
#     "session_id": "...",
#     "epistemic_state": {...},
#     "context_loaded": true
#   },
#   "thoughts": [...]
# }
```

### `/evolve`

Initiate evolutionary cycle for a work effort.

**Empirica Integration:**
- **CHECK Gate**: Assesses if evolution is safe (PROCEED/HALT/BRANCH/REVISE)
- **Goal Creation**: Creates Empirica goal with epistemic scope
- **Findings Logging**: Logs evolution start, completion, and results
- **Unknowns Tracking**: Logs unknowns if fitness is low or evolution fails

```python
result = pyrite.execute_ability("/evolve", "WE-260113-75vp", "adaptive", 5)
# Returns:
# {
#   "status": "success",
#   "cycle_id": "EVO-...",
#   "generation": 2,
#   "variants": 5,
#   "selected_variant": "...",
#   "fitness": 0.85,
#   "empirica": {
#     "goal_created": true,
#     "findings_logged": true
#   }
# }
```

### `/monitor`

Monitor work efforts (all or specific).

**Empirica Integration:**
- Logs monitoring activity as finding
- Logs unknowns if fitness is low (< 0.5)

```python
# Monitor all
result = pyrite.execute_ability("/monitor")

# Monitor specific
result = pyrite.execute_ability("/monitor", "WE-260113-75vp")
# Returns:
# {
#   "we_id": "WE-260113-75vp",
#   "status": "active",
#   "fitness": 0.85,
#   ...
#   "empirica": {
#     "findings_logged": true
#   }
# }
```

### `/organize`

Organize work efforts (rebuild graph, find roots/orphans).

```python
result = pyrite.execute_ability("/organize")
# Returns:
# {
#   "total_nodes": 42,
#   "roots": 5,
#   "orphans": ["WE-...", ...]
# }
```

### `/lock` and `/unlock`

Lock/unlock work efforts.

```python
result = pyrite.execute_ability("/lock", "WE-260113-75vp", "my-lock-id")
result = pyrite.execute_ability("/unlock", "WE-260113-75vp", "my-lock-id")
```

### `/status`

Get Pyrite's complete status.

```python
result = pyrite.execute_ability("/status")
# Returns comprehensive status including:
# - Personality
# - Work efforts (by status)
# - Locks
# - Evolution
# - Secrets
```

### `/secrets`

List secrets (metadata only - Pyrite cannot decrypt the actual secrets).

```python
result = pyrite.execute_ability("/secrets")
# Returns:
# {
#   "total_secrets": 3,
#   "secrets": [
#     {
#       "secret_id": "...",
#       "created": "...",
#       "access_count": 0,
#       "metadata": {...}
#     },
#     ...
#   ]
# }
```

## Personality & Attributes

Pyrite has personality attributes that grow over time:

- **wisdom**: Knowledge and understanding (growth_rate: 0.0005)
- **power**: Ability to effect change (growth_rate: 0.001)
- **awareness**: Consciousness of system state (growth_rate: 0.0008)
- **curiosity**: Drive to explore (growth_rate: 0.0012)
- **patience**: Tolerance for long processes (growth_rate: 0.0003)
- **creativity**: Innovation capacity (growth_rate: 0.001)
- **determination**: Persistence (growth_rate: 0.0004)

Attributes grow automatically with each cycle. You can also manually update them:

```python
pyrite.update_attribute("wisdom", 0.1)  # Increase wisdom by 0.1
pyrite.grow_attributes()  # Grow all attributes by their growth rates
```

## Evolutionary Strategies

### Conservative

Small mutations, high stability. Good for stable work efforts.

```python
cycle = pyrite.initiate_evolution(
    "WE-260113-75vp",
    strategy=EvolutionaryStrategy.CONSERVATIVE
)
```

### Aggressive

Large mutations, high risk. Good for experimental work efforts.

```python
cycle = pyrite.initiate_evolution(
    "WE-260113-75vp",
    strategy=EvolutionaryStrategy.AGGRESSIVE
)
```

### Adaptive

Strategy changes based on current fitness. Default strategy.

```python
cycle = pyrite.initiate_evolution(
    "WE-260113-75vp",
    strategy=EvolutionaryStrategy.ADAPTIVE
)
```

### Exploratory

Random mutations, exploration. Good for discovery.

```python
cycle = pyrite.initiate_evolution(
    "WE-260113-75vp",
    strategy=EvolutionaryStrategy.EXPLORATORY
)
```

## Secrets System

Pyrite can create secrets that even it cannot directly access. Only metadata is visible:

```python
# Create a secret
secret_id = pyrite.create_secret(
    {"hidden": "data", "secret": "information"},
    metadata={"visible": "metadata", "note": "This is visible"}
)

# Get metadata (visible)
metadata = pyrite.get_secret_metadata(secret_id)
# Returns: {"visible": "metadata", "note": "This is visible"}

# List all secrets (metadata only)
secrets = pyrite.list_secrets()
```

The actual encrypted data is stored but cannot be decrypted by Pyrite itself (the encryption key is stored separately).

## Locking System

### Synchronous Locks

```python
# Acquire lock
success = pyrite.acquire_lock("WE-260113-75vp", "my-lock-id", timeout=30.0)

# Check if locked
is_locked = pyrite.is_locked("WE-260113-75vp")

# Get lock holder
holder = pyrite.get_lock_holder("WE-260113-75vp")

# Release lock
success = pyrite.release_lock("WE-260113-75vp", "my-lock-id")
```

### Async Locks

```python
# Acquire async lock
success = await pyrite.acquire_lock_async("WE-260113-75vp", "my-lock-id", timeout=30.0)

# Release async lock
success = await pyrite.release_lock_async("WE-260113-75vp", "my-lock-id")
```

## Monitoring System

### Observer Pattern

```python
from waft.pyrite import WorkEffortObserver, WorkEffortStatus

class MyObserver(WorkEffortObserver):
    def on_status_change(self, we_id, old_status, new_status):
        print(f"{we_id}: {old_status} -> {new_status}")
    
    def on_evolution_start(self, cycle):
        print(f"Evolution started: {cycle.cycle_id}")
    
    def on_evolution_complete(self, cycle):
        print(f"Evolution complete: {cycle.cycle_id}")

# Register observer
observer = MyObserver()
pyrite.register_observer(observer)

# Unregister when done
pyrite.unregister_observer(observer)
```

### State History

```python
# Record state
pyrite.record_state("WE-260113-75vp", {"status": "active", "fitness": 0.8})

# Get state history
history = pyrite.get_state_history("WE-260113-75vp", limit=10)
```

### Metrics

```python
# Update metric
pyrite.update_metric("fitness", 0.85, we_id="WE-260113-75vp")
pyrite.update_metric("total_evolutions", 42)  # Global metric

# Get metrics
metrics = pyrite.get_metrics("WE-260113-75vp")  # Work effort specific
global_metrics = pyrite.get_metrics()  # All metrics
```

## Organization System

### Graph Operations

```python
# Get work effort node
node = pyrite.get_work_effort("WE-260113-75vp")

# Get children
children = pyrite.get_children("WE-260113-75vp")

# Get ancestors
ancestors = pyrite.get_ancestors("WE-260113-75vp")

# Update status
pyrite.update_work_effort_status("WE-260113-75vp", WorkEffortStatus.ACTIVE)

# Scan work efforts (rebuild graph)
pyrite._scan_work_efforts()
```

## State Persistence

Pyrite automatically saves its state to `_pyrite/.waft/pyrite_state.json`:

- Metadata
- Attributes
- Work effort graph
- Secrets (encrypted)

State is loaded automatically on initialization and saved after significant operations.

## Work Effort Status

Work efforts can be in one of these states:

- **DORMANT**: Inactive, not being worked on
- **ACTIVE**: Currently being worked on
- **LOCKED**: Locked by a process
- **EVOLVING**: Undergoing evolutionary cycle
- **COMPLETED**: Finished
- **ARCHIVED**: Archived
- **CORRUPTED**: Error state

## Examples

### Complete Evolutionary Cycle

```python
from waft.pyrite import get_pyrite, EvolutionaryStrategy

pyrite = get_pyrite()

# Lock work effort
pyrite.acquire_lock("WE-260113-75vp", "evolution-lock")

try:
    # Initiate evolution
    cycle = pyrite.initiate_evolution(
        "WE-260113-75vp",
        strategy=EvolutionaryStrategy.ADAPTIVE,
        num_variants=5
    )
    
    print(f"Cycle {cycle.cycle_id} completed")
    print(f"Selected variant: {cycle.selected_variant}")
    print(f"Fitness: {cycle.fitness_scores[cycle.selected_variant]}")
    
finally:
    # Release lock
    pyrite.release_lock("WE-260113-75vp", "evolution-lock")
```

### Monitoring Work Effort

```python
from waft.pyrite import get_pyrite, WorkEffortObserver, WorkEffortStatus

pyrite = get_pyrite()

class StatusMonitor(WorkEffortObserver):
    def on_status_change(self, we_id, old_status, new_status):
        print(f"Status change: {we_id}: {old_status.value} -> {new_status.value}")

monitor = StatusMonitor()
pyrite.register_observer(monitor)

# Monitor specific work effort
result = pyrite.execute_ability("/monitor", "WE-260113-75vp")
print(result)
```

### Creating and Managing Secrets

```python
from waft.pyrite import get_pyrite

pyrite = get_pyrite()

# Create secret
secret_id = pyrite.create_secret(
    {
        "api_key": "secret-key-123",
        "password": "hidden-password"
    },
    metadata={
        "service": "API",
        "created_by": "user",
        "note": "API credentials"
    }
)

# List secrets (metadata only)
secrets = pyrite.list_secrets()
for secret in secrets:
    print(f"Secret {secret['secret_id']}: {secret['metadata']}")
```

## Integration

To integrate Pyrite into the main WAFT CLI, add to `src/waft/main.py`:

```python
from .cli.pyrite_cli import app as pyrite_app

app.add_typer(pyrite_app, name="pyrite", help="Pyrite - The God of Work Efforts")
```

Then use:

```bash
waft pyrite think
waft pyrite evolve WE-260113-75vp
```

## Philosophy

Pyrite is designed as a "God" class - a single, powerful entity that manages the entire Work Efforts ecosystem. It has:

- **Personality**: Attributes that grow and evolve
- **Secrets**: Hidden state even from itself
- **Abilities**: Divine powers to lock, monitor, organize, and evolve
- **Awareness**: Consciousness of the system state
- **Wisdom**: Knowledge that accumulates over time

Pyrite embodies the principle that complex systems need a central intelligence to coordinate, but that intelligence itself can have emergent properties and hidden depths.
