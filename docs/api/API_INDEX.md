# WAFT API Reference

> **Complete API documentation for the Wave Agent Framework & Tools**

Version 0.9.0 - API Reference Documentation

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [API Organization](#api-organization)
3. [Core APIs](#core-apis)
4. [Module Reference](#module-reference)
5. [Usage Examples](#usage-examples)
6. [Type Definitions](#type-definitions)
7. [Error Handling](#error-handling)

---

## Overview

This document provides comprehensive API documentation for WAFT. Whether you're building agents, extending WAFT, or integrating with your projects, you'll find the API specifications here.

### API Stability

| API Category | Stability | Version |
|--------------|-----------|---------|
| Foundation API | **Stable** | 0.9.0 |
| CLI API | **Stable** | 0.9.0 |
| Intelligence API | **Beta** | 0.9.0 |
| Personality API | **Stable** | 0.9.0 |
| Evolution API | **Alpha** | 0.9.0 (Planned) |
| Agent API | **Planning** | 1.0.0 (Future) |

**Legend:**
- **Stable**: Production-ready, backward compatible
- **Beta**: Feature complete, API may change slightly
- **Alpha**: Early development, breaking changes expected
- **Planning**: Design phase, not implemented

---

## API Organization

WAFT APIs are organized by layer:

```
waft/
├── core/           # Foundation layer
│   ├── foundation
│   ├── substrate_manager
│   ├── memory_manager
│   └── config
│
├── cli/            # Command-line interface
│   ├── commands
│   ├── validators
│   └── formatters
│
├── intelligence/   # Intelligence layer
│   ├── empirica_integration
│   ├── session_analytics
│   ├── decision_matrix
│   └── input_transformer
│
├── personality/    # Personality layer
│   ├── tavernkeeper
│   ├── being
│   ├── narrator
│   └── karma
│
└── evolution/      # Evolution layer (planned)
    ├── genome_manager
    ├── mutation_engine
    ├── scint_detector
    └── flight_recorder
```

---

## Core APIs

### Foundation API

**Purpose**: Core infrastructure for project management

**Modules**:
- [Foundation](FOUNDATION_API.md) - Project initialization and structure
- [Substrate Manager](SUBSTRATE_API.md) - Project scaffolding
- [Memory Manager](MEMORY_API.md) - _pyrite system
- [Config](CONFIG_API.md) - Configuration management

**Quick Example**:
```python
from waft.foundation import Foundation

# Initialize a foundation
foundation = Foundation(project_name="my_lab")
foundation.initialize()

# Verify structure
is_valid = foundation.verify()
```

### CLI API

**Purpose**: Command-line interface operations

**Modules**:
- [Commands](CLI_COMMANDS_API.md) - All CLI commands
- [Validators](CLI_VALIDATORS_API.md) - Input validation
- [Formatters](CLI_FORMATTERS_API.md) - Output formatting

**Quick Example**:
```python
from waft.cli import create_project, verify_project

# Programmatic CLI usage
create_project(name="my_lab", path="/tmp/labs")
verify_project(path="/tmp/labs/my_lab")
```

### Intelligence API

**Purpose**: Data analysis and decision-making

**Modules**:
- [Empirica Integration](EMPIRICA_API.md) - Epistemic tracking
- [Session Analytics](ANALYTICS_API.md) - Data analysis
- [Decision Matrix](DECISION_API.md) - Decision engine
- [Input Transformer](TRANSFORMER_API.md) - Data validation

**Quick Example**:
```python
from waft.empirica_integration import EmpericaClient

# Track findings
client = EmpericaClient()
client.log_finding(
    content="Discovered optimization",
    impact=0.8
)

# Check safety gate
result = client.safety_gate_check()
# Returns: "PROCEED", "HALT", "BRANCH", or "REVISE"
```

### Personality API

**Purpose**: Gamification and engagement

**Modules**:
- [TavernKeeper](TAVERNKEEPER_API.md) - D&D mechanics
- [Being](BEING_API.md) - Entity lifecycle
- [Narrator](NARRATOR_API.md) - Storytelling
- [Karma](KARMA_API.md) - Ethical tracking

**Quick Example**:
```python
from waft.tavernkeeper import TavernKeeper
from waft.being import Being

# Create a being
being = Being(
    name="CodeWizard",
    being_type="Warforged Wizard"
)

# Initialize tavern
tavern = TavernKeeper(being=being)

# Roll for action
result = tavern.roll_check(
    ability="Intelligence",
    difficulty=15
)
```

### Evolution API (Planned)

**Purpose**: Agent evolution and genetic operations

**Modules**:
- [Genome Manager](GENOME_API.md) - DNA management (Planned)
- [Mutation Engine](MUTATION_API.md) - Code mutations (Planned)
- [Scint Detector](SCINT_API.md) - Fitness evaluation (Planned)
- [Flight Recorder](FLIGHT_RECORDER_API.md) - Event logging (Planned)

**Planned Example**:
```python
from waft.evolution import GenomeManager, MutationEngine

# Load agent genome
genome = GenomeManager.load("agent_v1.py")

# Create mutation
mutation = MutationEngine.mutate(
    genome=genome,
    strategy="prompt_optimization"
)

# Spawn variant
variant = genome.spawn_variant(mutation)
```

---

## Module Reference

### Core Modules

#### `waft.foundation`

**Main Class**: `Foundation`

```python
class Foundation:
    """Core project foundation management"""

    def __init__(
        self,
        project_name: str,
        project_path: Optional[Path] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize foundation"""

    def initialize(self) -> bool:
        """Initialize project structure"""

    def verify(self) -> bool:
        """Verify project structure is valid"""

    def get_info(self) -> Dict[str, Any]:
        """Get project information"""

    def sync_dependencies(self) -> bool:
        """Sync uv dependencies"""

    def add_dependency(self, package: str) -> bool:
        """Add a new dependency"""
```

**Usage**:
```python
from waft.foundation import Foundation

foundation = Foundation("my_lab")
foundation.initialize()

if foundation.verify():
    print("Project valid!")

info = foundation.get_info()
print(f"Python: {info['python_version']}")
```

#### `waft.substrate_manager`

**Main Class**: `SubstrateManager`

```python
class SubstrateManager:
    """Manages project scaffolding and structure"""

    def create_project(
        self,
        name: str,
        path: Path,
        template: Optional[str] = None
    ) -> bool:
        """Create new project from template"""

    def create_pyrite_structure(self, path: Path) -> bool:
        """Create _pyrite memory structure"""

    def create_github_workflows(self, path: Path) -> bool:
        """Create CI/CD workflows"""

    def create_justfile(self, path: Path) -> bool:
        """Create task runner configuration"""
```

**Usage**:
```python
from waft.substrate_manager import SubstrateManager
from pathlib import Path

manager = SubstrateManager()
manager.create_project(
    name="my_lab",
    path=Path("/tmp/labs"),
    template="basic"
)
```

#### `waft.memory_manager`

**Main Class**: `MemoryManager`

```python
class MemoryManager:
    """Manages _pyrite memory structure"""

    def __init__(self, project_path: Path):
        """Initialize memory manager"""

    def create_ticket(
        self,
        title: str,
        scint_bounty: int,
        karma_impact: str
    ) -> str:
        """Create new _pyrite ticket"""

    def list_tickets(
        self,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List tickets, optionally filtered by status"""

    def update_ticket(
        self,
        ticket_id: str,
        updates: Dict[str, Any]
    ) -> bool:
        """Update ticket information"""

    def get_state(self) -> Dict[str, Any]:
        """Get current system state"""

    def update_ledger(
        self,
        scint_earned: int,
        karma_change: int
    ) -> bool:
        """Update work ledger"""
```

**Usage**:
```python
from waft.memory_manager import MemoryManager
from pathlib import Path

memory = MemoryManager(Path("./my_lab"))

# Create ticket
ticket_id = memory.create_ticket(
    title="Build greeting agent",
    scint_bounty=50,
    karma_impact="positive"
)

# List active tickets
active = memory.list_tickets(status="active")
```

### Intelligence Modules

#### `waft.empirica_integration`

**Main Class**: `EmpericaClient`

```python
class EmpericaClient:
    """Epistemic tracking integration"""

    def __init__(
        self,
        project_path: Optional[Path] = None,
        ai_id: Optional[str] = None
    ):
        """Initialize Empirica client"""

    def create_session(
        self,
        session_type: str = "waft_session"
    ) -> str:
        """Create new tracking session"""

    def log_finding(
        self,
        content: str,
        impact: float,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Log a discovery/finding"""

    def log_unknown(
        self,
        content: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Log knowledge gap"""

    def safety_gate_check(
        self,
        operation: Optional[Dict[str, Any]] = None
    ) -> str:
        """Check safety gate"""

    def get_assessment(
        self,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get epistemic assessment"""

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get data for epistemic HUD"""
```

**Usage**:
```python
from waft.empirica_integration import EmpericaClient

client = EmpericaClient()

# Start session
session_id = client.create_session()

# Log discovery
client.log_finding(
    content="Found better prompt structure",
    impact=0.7,
    context={"agent": "RefactorAgent"}
)

# Check if operation is safe
gate = client.safety_gate_check(
    operation={"type": "code_generation", "scope": "high"}
)

if gate == "PROCEED":
    # Safe to proceed
    pass
```

#### `waft.decision_matrix`

**Main Class**: `DecisionMatrix`

```python
class DecisionMatrix:
    """Weighted decision-making system"""

    def __init__(
        self,
        weights: Optional[Dict[str, float]] = None
    ):
        """Initialize with decision weights"""

    def evaluate_options(
        self,
        options: List[Dict[str, Any]],
        criteria: List[str]
    ) -> List[Tuple[Any, float]]:
        """Evaluate and rank options"""

    def calculate_score(
        self,
        option: Dict[str, Any],
        criteria: List[str]
    ) -> float:
        """Calculate weighted score"""
```

**Usage**:
```python
from waft.decision_matrix import DecisionMatrix

matrix = DecisionMatrix(weights={
    "performance": 0.4,
    "maintainability": 0.3,
    "safety": 0.3
})

options = [
    {"name": "A", "performance": 8, "maintainability": 6, "safety": 9},
    {"name": "B", "performance": 9, "maintainability": 5, "safety": 7},
]

ranked = matrix.evaluate_options(
    options=options,
    criteria=["performance", "maintainability", "safety"]
)

best = ranked[0]  # Highest scored option
```

### Personality Modules

#### `waft.tavernkeeper`

**Main Class**: `TavernKeeper`

```python
class TavernKeeper:
    """D&D 5e RPG mechanics manager"""

    def __init__(
        self,
        being: "Being",
        rules_variant: str = "standard"
    ):
        """Initialize with a being"""

    def roll_check(
        self,
        ability: str,
        difficulty: int,
        advantage: bool = False,
        disadvantage: bool = False
    ) -> Dict[str, Any]:
        """Roll ability check"""

    def roll_saving_throw(
        self,
        ability: str,
        difficulty: int
    ) -> Dict[str, Any]:
        """Roll saving throw"""

    def cast_spell(
        self,
        spell_name: str,
        spell_level: int
    ) -> Dict[str, Any]:
        """Cast a spell"""

    def take_damage(
        self,
        amount: int,
        damage_type: str = "bludgeoning"
    ) -> Dict[str, Any]:
        """Apply damage to being"""

    def heal(
        self,
        amount: int
    ) -> Dict[str, Any]:
        """Heal being"""

    def level_up(self) -> bool:
        """Advance being level"""

    def award_insight(
        self,
        amount: int,
        reason: str
    ) -> Dict[str, Any]:
        """Award Insight (epistemic XP)"""
```

**Usage**:
```python
from waft.tavernkeeper import TavernKeeper
from waft.being import Being

# Create being
wizard = Being(
    name="Codex",
    being_type="Warforged Wizard"
)

# Initialize tavern
tavern = TavernKeeper(wizard)

# Roll intelligence check
result = tavern.roll_check(
    ability="Intelligence",
    difficulty=15,
    advantage=True
)

if result["success"]:
    print(f"Success! Rolled {result['total']}")

# Cast a spell
spell_result = tavern.cast_spell(
    spell_name="Identify",
    spell_level=1
)
```

#### `waft.being`

**Main Class**: `Being`

```python
class Being:
    """Entity with lifecycle and D&D attributes"""

    def __init__(
        self,
        name: str,
        being_type: str,
        alignment: Optional[str] = None,
        ability_scores: Optional[Dict[str, int]] = None
    ):
        """Initialize being"""

    # D&D Attributes
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int

    # Lifecycle Attributes
    will_to_live: float  # 0-100
    luck: float          # Karma-influenced
    decision_fatigue: float  # Requires sleep
    pleasure: float      # Positive experiences
    pain: float          # Negative experiences

    # Evolution Attributes
    scint_balance: int   # ✨ Energy
    karma: int           # ☯ Polarity
    genome_id: Optional[str]
    generation: int

    def get_modifier(self, ability: str) -> int:
        """Get ability modifier"""

    def update_lifecycle(
        self,
        time_passed: float
    ) -> Dict[str, Any]:
        """Update lifecycle attributes"""

    def needs_sleep(self) -> bool:
        """Check if being needs rest"""

    def sleep(self, duration: float) -> Dict[str, Any]:
        """Rest to recover decision fatigue"""

    def experience_pleasure(
        self,
        amount: float,
        reason: str
    ) -> None:
        """Record positive experience"""

    def experience_pain(
        self,
        amount: float,
        reason: str
    ) -> None:
        """Record negative experience"""

    def earn_scint(
        self,
        amount: int,
        source: str
    ) -> None:
        """Earn Scint energy"""

    def spend_scint(
        self,
        amount: int,
        purpose: str
    ) -> bool:
        """Spend Scint energy"""

    def update_karma(
        self,
        change: int,
        reason: str
    ) -> None:
        """Update karma polarity"""
```

**Usage**:
```python
from waft.being import Being

# Create being
being = Being(
    name="Nexus",
    being_type="Warforged Wizard",
    alignment="Lawful Neutral",
    ability_scores={
        "strength": 10,
        "dexterity": 12,
        "constitution": 14,
        "intelligence": 18,
        "wisdom": 15,
        "charisma": 8
    }
)

# Check intelligence modifier
int_mod = being.get_modifier("intelligence")  # +4

# Earn Scint from completing work
being.earn_scint(50, "Completed PY-001 ticket")

# Update karma
being.update_karma(5, "Helped another developer")

# Check if needs rest
if being.needs_sleep():
    result = being.sleep(8.0)  # 8 hours of rest
```

#### `waft.karma`

**Main Class**: `KarmaTracker`

```python
class KarmaTracker:
    """Ethical polarity tracking"""

    def __init__(
        self,
        being: "Being"
    ):
        """Initialize with being"""

    def record_action(
        self,
        action: str,
        impact: int,
        category: str
    ) -> Dict[str, Any]:
        """Record action with karma impact"""

    def get_polarity(self) -> str:
        """Get karma polarity (Order/Neutral/Chaos)"""

    def get_balance(self) -> int:
        """Get current karma balance"""

    def get_history(
        self,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get karma history"""

    def should_evolve(self) -> bool:
        """Check if being should evolve based on karma"""
```

**Usage**:
```python
from waft.karma import KarmaTracker
from waft.being import Being

being = Being(name="Atlas", being_type="Warforged Wizard")
karma = KarmaTracker(being)

# Record actions
karma.record_action(
    action="Refactored legacy code",
    impact=10,
    category="order"
)

karma.record_action(
    action="Broke production",
    impact=-15,
    category="chaos"
)

# Check polarity
polarity = karma.get_polarity()  # "Chaos", "Neutral", or "Order"

# Check if should evolve
if karma.should_evolve():
    print("Ready for evolution!")
```

### Evolution Modules (Planned)

#### `waft.evolution.genome_manager` (Planned)

**Main Class**: `GenomeManager`

```python
class GenomeManager:
    """Manages agent genomes (code as DNA)"""

    def __init__(
        self,
        agent_path: Path
    ):
        """Initialize with agent directory"""

    def calculate_genome_id(self) -> str:
        """Calculate SHA-256 genome ID"""

    def spawn_variant(
        self,
        mutation: Dict[str, Any],
        variant_name: str
    ) -> "GenomeManager":
        """Create variant with mutation"""

    def get_lineage(self) -> List[str]:
        """Get ancestry (parent genome IDs)"""

    def hot_swap(
        self,
        new_genome_id: str
    ) -> bool:
        """Swap to new genome"""

    def export_genome(
        self,
        output_path: Path
    ) -> bool:
        """Export genome for sharing"""
```

---

## Usage Examples

### Example 1: Complete Project Setup

```python
from pathlib import Path
from waft.foundation import Foundation
from waft.empirica_integration import EmpericaClient

# Create project
foundation = Foundation(
    project_name="my_research_lab",
    project_path=Path("~/projects/labs")
)

# Initialize structure
if foundation.initialize():
    print("✅ Lab created!")

    # Verify
    if foundation.verify():
        print("✅ Structure valid!")

        # Start tracking
        client = EmpericaClient(
            project_path=foundation.project_path
        )

        session = client.create_session()
        print(f"📊 Session started: {session}")

        # Log initial finding
        client.log_finding(
            content="Lab initialized successfully",
            impact=0.5
        )
```

### Example 2: Agent with D&D Mechanics

```python
from waft.being import Being
from waft.tavernkeeper import TavernKeeper
from waft.karma import KarmaTracker

# Create wizard agent
wizard = Being(
    name="Algorithmus",
    being_type="Warforged Wizard",
    alignment="Lawful Good",
    ability_scores={
        "intelligence": 18,
        "wisdom": 14,
        "charisma": 10
    }
)

# Initialize systems
tavern = TavernKeeper(wizard)
karma = KarmaTracker(wizard)

# Agent performs task
task_result = tavern.roll_check(
    ability="Intelligence",
    difficulty=15
)

if task_result["success"]:
    # Award Scint and Insight
    wizard.earn_scint(50, "Completed refactoring")
    tavern.award_insight(100, "Successful task")

    # Record karma
    karma.record_action(
        action="Clean refactor",
        impact=5,
        category="order"
    )

    print(f"✨ Scint: {wizard.scint_balance}")
    print(f"☯️ Karma: {wizard.karma}")
```

### Example 3: Decision Making

```python
from waft.decision_matrix import DecisionMatrix
from waft.empirica_integration import EmpericaClient

# Define options
algorithms = [
    {
        "name": "QuickSort",
        "performance": 9,
        "memory": 7,
        "maintainability": 8,
        "safety": 9
    },
    {
        "name": "BubbleSort",
        "performance": 3,
        "memory": 10,
        "maintainability": 10,
        "safety": 10
    }
]

# Create decision matrix
matrix = DecisionMatrix(weights={
    "performance": 0.4,
    "memory": 0.2,
    "maintainability": 0.2,
    "safety": 0.2
})

# Evaluate
ranked = matrix.evaluate_options(
    options=algorithms,
    criteria=["performance", "memory", "maintainability", "safety"]
)

# Check safety gate
client = EmpericaClient()
gate = client.safety_gate_check(
    operation={
        "type": "algorithm_selection",
        "choice": ranked[0][0]["name"]
    }
)

if gate == "PROCEED":
    selected = ranked[0][0]
    print(f"Selected: {selected['name']}")

    # Log finding
    client.log_finding(
        content=f"Selected {selected['name']} algorithm",
        impact=0.7,
        context={"score": ranked[0][1]}
    )
```

---

## Type Definitions

### Common Types

```python
from typing import TypedDict, Literal, Optional, List, Dict, Any
from pathlib import Path

# Project types
class ProjectInfo(TypedDict):
    name: str
    path: Path
    version: str
    python_version: str
    dependencies: List[str]

# Ticket types
class Ticket(TypedDict):
    id: str
    title: str
    status: Literal["active", "backlog", "completed"]
    scint_bounty: int
    karma_impact: Literal["positive", "neutral", "negative"]
    created_at: str

# Ability check result
class CheckResult(TypedDict):
    success: bool
    roll: int
    modifier: int
    total: int
    critical: bool

# Finding types
class Finding(TypedDict):
    id: str
    content: str
    impact: float
    timestamp: str
    context: Optional[Dict[str, Any]]

# Genome types (planned)
class Genome(TypedDict):
    id: str
    parent_id: Optional[str]
    generation: int
    code_hash: str
    config_hash: str
    fitness_score: Optional[float]
```

---

## Error Handling

### Exception Hierarchy

```python
class WaftError(Exception):
    """Base exception for all WAFT errors"""

class ProjectError(WaftError):
    """Project-related errors"""

class ValidationError(WaftError):
    """Input validation errors"""

class GenomeError(WaftError):
    """Genome management errors"""

class EvolutionError(WaftError):
    """Evolution cycle errors"""

class EmpericaError(WaftError):
    """Epistemic tracking errors"""
```

### Error Handling Example

```python
from waft.foundation import Foundation, ProjectError
from waft.exceptions import ValidationError, WaftError

try:
    foundation = Foundation("my_lab")
    foundation.initialize()

except ValidationError as e:
    print(f"Invalid input: {e}")

except ProjectError as e:
    print(f"Project error: {e}")

except WaftError as e:
    print(f"WAFT error: {e}")

except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## API Best Practices

### 1. Always validate inputs

```python
from waft.validators import validate_project_name

def create_project(name: str):
    if not validate_project_name(name):
        raise ValidationError("Invalid project name")
    # Proceed
```

### 2. Use type hints

```python
from typing import Optional, Dict, Any
from pathlib import Path

def initialize(
    path: Path,
    config: Optional[Dict[str, Any]] = None
) -> bool:
    """Initialize with proper types"""
```

### 3. Handle errors gracefully

```python
def safe_operation():
    try:
        return perform_operation()
    except WaftError as e:
        log_error(e)
        return default_value()
```

### 4. Use context managers

```python
from waft.session import Session

with Session.create() as session:
    # Session automatically closed
    session.log_finding("Discovery")
```

---

## Related Documentation

- **[Architecture](../ARCHITECTURE.md)** - System design
- **[Developer Guide](../DEVELOPER_GUIDE.md)** - Development workflow
- **[Getting Started](../GETTING_STARTED.md)** - Quick start
- **[Troubleshooting](../TROUBLESHOOTING.md)** - Common issues

---

## API Versioning

WAFT follows semantic versioning (SemVer):

- **Major version**: Breaking API changes
- **Minor version**: New features, backward compatible
- **Patch version**: Bug fixes, backward compatible

Current version: **0.9.0**

Next stable: **1.0.0** (API freeze, production ready)

---

*Last Updated: 2026-01-16 | Version: 0.9.0 | API Reference v1.0*
