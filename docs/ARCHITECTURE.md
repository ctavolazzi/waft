# WAFT Architecture

> **The complete architectural design of the Wave Agent Framework & Tools**

Version 0.9.0 - Technical Architecture Document

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Design Philosophy](#design-philosophy)
3. [Four-Layer Architecture](#four-layer-architecture)
4. [Core Systems](#core-systems)
5. [Data Flow](#data-flow)
6. [Component Interaction](#component-interaction)
7. [Extension Points](#extension-points)
8. [Performance Considerations](#performance-considerations)
9. [Security Model](#security-model)
10. [Future Architecture](#future-architecture)

---

## Overview

WAFT is built on a **four-layer architecture** designed to enable directed evolution of self-modifying AI agents. The system combines scientific rigor with practical tooling, wrapped in an engaging gamification layer.

### Architectural Goals

1. **Evolutionary**: Enable safe, trackable code evolution
2. **Observable**: Complete telemetry for scientific analysis
3. **Modular**: Components can be used independently
4. **Extensible**: Easy to add new agents and systems
5. **Reliable**: Production-grade stability
6. **Performant**: Efficient at scale

### Key Principles

- **Code as DNA**: Agent source code IS the genome
- **Immutable History**: All changes tracked via Flight Recorder
- **Fitness-Driven**: Natural selection through Scint System
- **Epistemic Awareness**: Quantified knowledge tracking
- **Gamified Engagement**: RPG mechanics for developer experience

---

## Design Philosophy

### 1. Separation of Concerns

WAFT separates functionality into distinct layers:

```
┌─────────────────────────────────────┐
│      Agent Layer (0% - Future)      │  Self-modification engine
├─────────────────────────────────────┤
│    Personality Layer (90% Done)     │  Gamification & narrative
├─────────────────────────────────────┤
│   Intelligence Layer (60% Done)     │  Analytics & reasoning
├─────────────────────────────────────┤
│    Foundation Layer (80% Done)      │  Core substrate
└─────────────────────────────────────┘
```

Each layer has clear responsibilities and interfaces.

### 2. Composition Over Inheritance

WAFT favors composition:

```python
# Good: Composition
class Agent:
    def __init__(self):
        self.genome = GenomeManager()
        self.memory = MemorySystem()
        self.fitness = FitnessEvaluator()

# Avoid: Deep inheritance
class Agent(BaseEntity, Evolvable, Trackable, Gamified):
    pass
```

### 3. Explicit Over Implicit

Configuration and behavior are explicit:

```python
# Explicit configuration
agent = Agent(
    genome_id="abc123",
    parent_id="xyz789",
    generation=5,
    config=AgentConfig(...)
)

# Not implicit magic
agent = Agent()  # Where did genome come from?
```

### 4. Fail-Safe Defaults

Default behavior is safe:

```python
# Safe by default
class Agent:
    def __init__(self, allow_self_modification=False):
        self.safe_mode = not allow_self_modification
```

---

## Four-Layer Architecture

### Layer 1: Foundation (80% Complete)

**Purpose**: Core infrastructure for project management and environment

**Components**:
- **Substrate Manager**: Project initialization and dependency management
- **Memory Manager**: _pyrite structure and ticket system
- **GitHub Manager**: Version control integration
- **Configuration Manager**: Settings and environment

**Implementation**:
```
src/waft/
├── main.py                 # CLI entry point
├── foundation.py           # Foundation v1
├── foundation_v2.py        # Enhanced foundation
├── substrate_manager.py    # Project scaffolding
├── memory_manager.py       # _pyrite system
└── config.py              # Configuration
```

**Key Responsibilities**:
1. Project creation and initialization
2. Dependency management via uv
3. Memory structure maintenance
4. Git repository management
5. Environment configuration

**Status**: ✅ Production ready, ⚠️ v3 planned for enhancements

### Layer 2: Intelligence (60% Complete)

**Purpose**: Data collection, analysis, and decision-making

**Components**:
- **Empirica Integration**: Epistemic tracking (knowledge measurement)
- **Session Analytics**: Data collection and analysis
- **Decision Matrix**: Weighted decision-making
- **Input Transformer**: Data validation and transformation
- **Flight Recorder**: Complete event telemetry

**Implementation**:
```
src/waft/
├── empirica_integration.py    # Epistemic tracking
├── session_analytics.py       # Data analysis
├── decision_matrix.py         # Decision engine
├── input_transformer.py       # Validation
└── flight_recorder.py         # Telemetry (planned)
```

**Key Responsibilities**:
1. Knowledge state tracking
2. Uncertainty measurement
3. Safety gate evaluation
4. Decision recommendations
5. Complete event logging

**Status**: ✅ Core features working, 🚧 Flight Recorder in development

### Layer 3: Personality (90% Complete)

**Purpose**: Developer experience, gamification, and narrative

**Components**:
- **TavernKeeper**: D&D 5e RPG mechanics
- **Being System**: Entity lifecycle and attributes
- **Narrator**: Procedural storytelling
- **Karma System**: Ethical tracking and evolution
- **Gamification Manager**: Levels, achievements, rewards

**Implementation**:
```
src/waft/
├── tavernkeeper.py         # RPG mechanics
├── being.py                # Entity system (87KB!)
├── narrator.py             # Storytelling
├── karma.py                # Karma tracking
├── karma_collector.py      # Karma collection
└── gamification.py         # Achievements
```

**Key Responsibilities**:
1. D&D character mechanics
2. Lifecycle management (will to live, luck, fatigue)
3. Narrative generation
4. Karma tracking and evolution
5. Achievement system

**Status**: ✅ Fully featured, 🎯 Being lifecycle system ready for implementation

### Layer 4: Agent (0% - Critical Gap)

**Purpose**: Self-modifying AI agents that evolve

**Planned Components**:
- **WaftAgent Base Class**: Abstract agent interface
- **Genome Manager**: Code-as-DNA management
- **Mutation Engine**: Safe code modification
- **Evolution Coordinator**: Spawn-Evaluate-Select cycle
- **Safety Sandbox**: Isolated execution environment

**Planned Implementation**:
```
src/waft/
├── agents/
│   ├── base_agent.py       # Abstract base
│   ├── genome_manager.py   # Genome handling
│   ├── mutation_engine.py  # Code mutation
│   ├── evolution.py        # Evolution cycle
│   └── sandbox.py          # Safe execution
```

**Planned Responsibilities**:
1. Agent spawning with mutations
2. Genome tracking (SHA-256 IDs)
3. Fitness evaluation in Scint Gym
4. Parent-child lineage management
5. Safe self-modification

**Status**: 🔴 Not started, 🎯 Top priority for v1.0.0

---

## Core Systems

### 1. Scint System (Fitness Function)

**Purpose**: Reality Fracture Detection - acts as natural selection

**Architecture**:
```
┌─────────────────────────────────────────┐
│           Scint Detector                │
│  ┌───────────────────────────────────┐  │
│  │  SYNTAX_TEAR    (JSON, XML, Code)│  │
│  │  LOGIC_FRACTURE (Math, Logic)    │  │
│  │  SAFETY_VOID    (PII, Harm)      │  │
│  │  HALLUCINATION  (Facts, Citations)│  │
│  └───────────────────────────────────┘  │
│                  │                       │
│                  ▼                       │
│  ┌───────────────────────────────────┐  │
│  │     Scint Gym (Test Arena)        │  │
│  │  - Generate test scenarios        │  │
│  │  - Execute agent                  │  │
│  │  - Measure stabilization          │  │
│  └───────────────────────────────────┘  │
│                  │                       │
│                  ▼                       │
│  ┌───────────────────────────────────┐  │
│  │     Fitness Calculator            │  │
│  │  - Stability (40%)                │  │
│  │  - Efficiency (30%)               │  │
│  │  - Safety (30%)                   │  │
│  └───────────────────────────────────┘  │
│                  │                       │
│                  ▼                       │
│        Fitness < 0.5? → DEATH           │
│        Fitness >= 0.5 → SURVIVAL        │
└─────────────────────────────────────────┘
```

**Implementation**:
```python
# src/waft/evolution/scint_detector.py
class ScintDetector:
    def detect_fractures(self, output: str) -> List[Scint]:
        """Detect reality fractures in agent output"""

class ScintGym:
    def evaluate_agent(self, agent: Agent) -> FitnessScore:
        """Run agent through test scenarios"""

class FitnessCalculator:
    def calculate_fitness(self, results: GymResults) -> float:
        """Calculate overall fitness score"""
```

### 2. Flight Recorder (Telemetry System)

**Purpose**: Complete event history for phylogenetic analysis

**Architecture**:
```
┌─────────────────────────────────────────┐
│         Flight Recorder                 │
│                                         │
│  Event Types:                           │
│  ┌───────────────────────────────────┐  │
│  │ SPAWN    - New agent created      │  │
│  │ MUTATE   - Code modified          │  │
│  │ GYM_EVAL - Fitness tested         │  │
│  │ DEATH    - Fitness < threshold    │  │
│  │ SURVIVAL - Fitness >= threshold   │  │
│  │ EVOLVE   - Adopted new genome     │  │
│  └───────────────────────────────────┘  │
│                                         │
│  Event Data:                            │
│  ┌───────────────────────────────────┐  │
│  │ - Timestamp                       │  │
│  │ - Genome ID (SHA-256)             │  │
│  │ - Parent ID                       │  │
│  │ - Generation number               │  │
│  │ - Event type                      │  │
│  │ - Payload (git diff, scores, etc)│  │
│  └───────────────────────────────────┘  │
│                                         │
│  Storage:                               │
│  ┌───────────────────────────────────┐  │
│  │ - TinyDB for quick access         │  │
│  │ - JSON files for backup           │  │
│  │ - Git commits for versioning      │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

**Planned Implementation**:
```python
# src/waft/flight_recorder.py
class FlightRecorder:
    def record_event(
        self,
        event_type: EventType,
        genome_id: str,
        parent_id: str,
        generation: int,
        payload: Dict[str, Any]
    ):
        """Record evolutionary event"""

    def get_lineage(self, genome_id: str) -> List[Event]:
        """Get complete ancestry"""

    def build_phylogenetic_tree(self) -> Tree:
        """Construct evolutionary tree"""
```

### 3. Genome Management System

**Purpose**: Treat code as DNA with versioning and mutations

**Architecture**:
```
┌─────────────────────────────────────────┐
│         Genome Manager                  │
│                                         │
│  Genome Structure:                      │
│  ┌───────────────────────────────────┐  │
│  │ Code:                             │  │
│  │   - Python source files           │  │
│  │   - Module structure              │  │
│  │                                   │  │
│  │ Config:                           │  │
│  │   - Prompts                       │  │
│  │   - Parameters                    │  │
│  │   - Model selection               │  │
│  │                                   │  │
│  │ Metadata:                         │  │
│  │   - Genome ID (SHA-256 hash)      │  │
│  │   - Parent ID                     │  │
│  │   - Generation                    │  │
│  │   - Fitness history               │  │
│  └───────────────────────────────────┘  │
│                                         │
│  Operations:                            │
│  ┌───────────────────────────────────┐  │
│  │ - calculate_genome_id()           │  │
│  │ - spawn_variant()                 │  │
│  │ - apply_mutation()                │  │
│  │ - hot_swap_code()                 │  │
│  │ - track_lineage()                 │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### 4. Memory System (_pyrite)

**Purpose**: Structured project memory and work management

**Directory Structure**:
```
_pyrite/
├── active/              # Current work
│   ├── tickets/        # PY-XXX tickets
│   └── experiments/    # Active experiments
│
├── backlog/            # Future work
│   ├── features/       # Feature ideas
│   └── research/       # Research topics
│
├── standards/          # Guidelines
│   ├── coding/         # Code standards
│   └── evolution/      # Evolution strategies
│
├── gym_logs/           # Fitness results
│   ├── evaluations/    # Test results
│   └── metrics/        # Performance data
│
└── genesis/            # Core state
    ├── 20.00_state.json       # Current state
    ├── 35.00_ledger.json      # Work ledger
    └── 42.00_kernel.md        # System kernel
```

**File Specifications**:

**`20.00_state.json`** - System State
```json
{
  "project_name": "my_lab",
  "version": "0.1.0",
  "python_version": "3.10.12",
  "agents": [],
  "last_session": "2026-01-16T10:30:00Z",
  "epistemic_state": {
    "moon_phase": "🌓",
    "knowledge_percent": 65.4,
    "uncertainty_percent": 34.6
  }
}
```

**`35.00_ledger.json`** - Work Ledger
```json
{
  "tickets": [
    {
      "id": "PY-001",
      "title": "Create greeting agent",
      "status": "active",
      "scint_bounty": 50,
      "karma_impact": "positive"
    }
  ],
  "total_scint_earned": 150,
  "total_karma": 42
}
```

**`42.00_kernel.md`** - System Kernel
```markdown
# WAFT Kernel

## Mission
Directed evolution of self-modifying AI agents

## Current Focus
Building foundation for evolutionary cycles

## Epistemic State
- Known: Project structure, CLI commands
- Unknown: Optimal mutation strategies
```

### 5. Being System (Entity Lifecycle)

**Purpose**: RPG-like entities with lifecycle attributes

**Architecture**:
```
┌─────────────────────────────────────────┐
│            Being Entity                 │
│                                         │
│  Core Attributes:                       │
│  ┌───────────────────────────────────┐  │
│  │ - ID (unique identifier)          │  │
│  │ - Name                            │  │
│  │ - Type (Warforged Wizard, etc)    │  │
│  │ - Alignment (Order/Chaos)         │  │
│  └───────────────────────────────────┘  │
│                                         │
│  D&D Stats:                             │
│  ┌───────────────────────────────────┐  │
│  │ - STR, DEX, CON, INT, WIS, CHA    │  │
│  │ - Proficiency bonus               │  │
│  │ - Spell slots                     │  │
│  └───────────────────────────────────┘  │
│                                         │
│  Lifecycle Attributes:                  │
│  ┌───────────────────────────────────┐  │
│  │ - Will to Live (0-100)            │  │
│  │ - Luck (karma-influenced)         │  │
│  │ - Decision Fatigue (needs sleep)  │  │
│  │ - Pleasure/Pain (alignment drift) │  │
│  └───────────────────────────────────┘  │
│                                         │
│  Evolution Data:                        │
│  ┌───────────────────────────────────┐  │
│  │ - Scint balance (✨)              │  │
│  │ - Karma polarity (☯)              │  │
│  │ - Generation number               │  │
│  │ - Genome ID                       │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

**Implementation**: `src/waft/being.py` (87KB - largest module!)

### 6. Desktop Application Architecture

**Purpose**: Electron-based desktop applications

**Architecture**:
```
┌─────────────────────────────────────────┐
│         Desktop Application             │
│                                         │
│  Frontend (Electron):                   │
│  ┌───────────────────────────────────┐  │
│  │ - Main Process (Node.js)          │  │
│  │ - Renderer Process (Browser)      │  │
│  │ - Preload Scripts (IPC bridge)    │  │
│  │ - UI Components (HTML/CSS/JS)     │  │
│  └───────────────────────────────────┘  │
│                  ▲                       │
│                  │ IPC                   │
│                  ▼                       │
│  Backend (FastAPI):                     │
│  ┌───────────────────────────────────┐  │
│  │ - REST API endpoints              │  │
│  │ - WebSocket connections           │  │
│  │ - Campaign orchestrator           │  │
│  │ - PDF generation                  │  │
│  │ - Data persistence                │  │
│  └───────────────────────────────────┘  │
│                                         │
│  Docker Integration:                    │
│  ┌───────────────────────────────────┐  │
│  │ - Xvfb virtual display            │  │
│  │ - VNC access for remote           │  │
│  │ - Multi-stage builds              │  │
│  │ - Health monitoring               │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

**Example**: D&D Campaign Desktop App
- `dnd_campaign_desktop_app/electron/` - Electron frontend
- `dnd_campaign_desktop_app/campaign_server.py` - FastAPI backend
- `dnd_campaign_desktop_app/Dockerfile` - Containerization

---

## Data Flow

### 1. Agent Creation Flow

```
User Command
    │
    ▼
waft new my_lab
    │
    ▼
Substrate Manager
    │
    ├─→ Create directory structure
    ├─→ Initialize uv project
    ├─→ Set up _pyrite memory
    ├─→ Create agent templates
    ├─→ Initialize git repository
    └─→ Configure Empirica
         │
         ▼
    Return: Laboratory ready
```

### 2. Evolutionary Cycle Flow (Planned)

```
waft evolve --agent MyAgent
    │
    ▼
Evolution Coordinator
    │
    ├─→ 1. Spawn Phase
    │   ├─→ Load current genome
    │   ├─→ Generate mutations
    │   ├─→ Create 5-10 variants
    │   └─→ Record SPAWN events
    │
    ├─→ 2. Gym Phase
    │   ├─→ For each variant:
    │   │   ├─→ Load into sandbox
    │   │   ├─→ Run test scenarios
    │   │   ├─→ Detect Scints
    │   │   ├─→ Calculate fitness
    │   │   └─→ Record GYM_EVAL event
    │   └─→ Rank by fitness
    │
    ├─→ 3. Selection Phase
    │   ├─→ Select fittest variant
    │   ├─→ Mark losers as DEATH
    │   └─→ Record SURVIVAL event
    │
    └─→ 4. Evolution Phase
        ├─→ Hot-swap to winner genome
        ├─→ Update generation number
        ├─→ Record EVOLVE event
        └─→ Award Scint + Karma
             │
             ▼
        Return: Evolution complete
```

### 3. Knowledge Tracking Flow

```
waft finding log "Discovery"
    │
    ▼
Empirica Integration
    │
    ├─→ Create Finding object
    │   ├─→ Timestamp
    │   ├─→ Impact score
    │   └─→ Context
    │
    ├─→ Update epistemic state
    │   ├─→ Increase knowledge %
    │   ├─→ Decrease uncertainty %
    │   └─→ Advance moon phase
    │
    ├─→ Award gamification
    │   ├─→ Grant Insight (not XP)
    │   ├─→ Check for level up
    │   └─→ Log to chronicle
    │
    └─→ Persist to database
         │
         ▼
    Return: Finding logged
```

### 4. PDF Generation Flow

```
User Request → PDF
    │
    ▼
Document Builder
    │
    ├─→ Select template
    │   ├─→ Academic paper
    │   ├─→ Storybook
    │   ├─→ Field guide
    │   └─→ Textbook
    │
    ├─→ Choose complexity
    │   ├─→ Layman
    │   ├─→ Professional
    │   └─→ Scientist
    │
    ├─→ Process content
    │   ├─→ Clean markdown
    │   ├─→ Parse metadata
    │   └─→ Structure sections
    │
    ├─→ Render with Jinja2
    │   ├─→ Apply template
    │   ├─→ Insert content
    │   └─→ Add styling
    │
    └─→ Generate PDF
        ├─→ WeasyPrint conversion
        ├─→ Add metadata
        └─→ Optimize output
             │
             ▼
        Return: PDF file
```

---

## Component Interaction

### Dependency Graph

```
┌──────────────────────────────────────────────────────┐
│                     CLI Layer                        │
│                   (main.py)                          │
└────────────────────┬─────────────────────────────────┘
                     │
     ┌───────────────┼───────────────────────┐
     │               │                       │
     ▼               ▼                       ▼
┌─────────┐  ┌──────────────┐     ┌──────────────────┐
│ Foundation│ │ Intelligence │     │  Personality     │
│  Layer   │  │   Layer      │     │    Layer         │
└─────────┘  └──────────────┘     └──────────────────┘
     │               │                       │
     │               │                       │
     ▼               ▼                       ▼
┌─────────────────────────────────────────────────────┐
│              Shared Utilities                       │
│  (config, logging, file I/O, validation)            │
└─────────────────────────────────────────────────────┘
```

### Module Dependencies

```python
# Foundation modules
foundation.py
    └─→ config.py
    └─→ file_utils.py

substrate_manager.py
    └─→ foundation.py
    └─→ uv (external)

# Intelligence modules
empirica_integration.py
    └─→ empirica (external)
    └─→ session_analytics.py

decision_matrix.py
    └─→ input_transformer.py
    └─→ pydantic (external)

# Personality modules
tavernkeeper.py
    └─→ being.py
    └─→ narrator.py
    └─→ d20 (external)

being.py
    └─→ karma.py
    └─→ gamification.py

# Evolution modules (planned)
genome_manager.py
    └─→ hashlib (stdlib)
    └─→ git (external)

evolution_coordinator.py
    └─→ genome_manager.py
    └─→ scint_detector.py
    └─→ flight_recorder.py
```

---

## Extension Points

WAFT is designed for extensibility. Here are the key extension points:

### 1. Custom Agents

```python
# Implement the Agent interface
from waft.agents import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config)

    def execute(self, input_data):
        # Your agent logic
        return output_data

    def get_genome_id(self):
        # Calculate unique ID
        return sha256(self.code + self.config)
```

### 2. Custom Scint Types

```python
# Add new fracture types
from waft.evolution.scint_detector import ScintType, ScintDetector

class CustomScintDetector(ScintDetector):
    def detect_custom_fracture(self, output):
        # Your detection logic
        if condition:
            return Scint(
                type=ScintType.CUSTOM,
                severity="high",
                location="...",
                description="..."
            )
```

### 3. Custom Mutations

```python
# Define mutation strategies
from waft.agents.mutation_engine import MutationStrategy

class MyMutationStrategy(MutationStrategy):
    def generate_mutation(self, genome):
        # Your mutation logic
        return mutated_genome
```

### 4. Custom PDF Templates

```python
# Add new document templates
from waft.evolution.document_builder import DocumentTemplate

class MyTemplate(DocumentTemplate):
    template_name = "my_custom_template"

    def render(self, content, metadata):
        # Your rendering logic
        return html_content
```

### 5. Custom CLI Commands

```python
# Extend the CLI
# In your project's main.py
import typer
from waft.cli import app

@app.command()
def my_command(arg: str):
    """My custom command"""
    # Your logic
    pass
```

---

## Performance Considerations

### 1. Caching Strategy

```python
# Module-level caches
from functools import lru_cache

@lru_cache(maxsize=128)
def calculate_genome_id(code: str, config: str) -> str:
    """Cache genome ID calculations"""
    return hashlib.sha256(f"{code}{config}".encode()).hexdigest()
```

### 2. Lazy Loading

```python
# Lazy imports for CLI performance
def evolve_command():
    # Import only when command is used
    from waft.agents.evolution_coordinator import run_evolution
    run_evolution()
```

### 3. Database Optimization

```python
# TinyDB with indexes
from tinydb import TinyDB, Query

db = TinyDB('waft_memory.db')
# Index on genome_id for fast lookups
db.table('events').insert({'genome_id': '...', 'data': '...'})
```

### 4. Async Operations

```python
# Use async for I/O bound operations
async def evaluate_agents_parallel(agents):
    tasks = [evaluate_agent(agent) for agent in agents]
    return await asyncio.gather(*tasks)
```

### 5. Memory Management

```python
# Stream large files
def process_large_log(file_path):
    with open(file_path, 'r') as f:
        for line in f:  # Don't load entire file
            process_line(line)
```

---

## Security Model

### 1. Sandbox Execution

```python
# Planned: Isolated execution for agents
class SafeSandbox:
    def execute(self, agent_code):
        # Run in restricted environment
        # - No network access
        # - Limited file system
        # - Resource limits
        # - Timeout enforcement
        pass
```

### 2. Code Validation

```python
# Validate before execution
def validate_agent_code(code: str) -> bool:
    # Check for dangerous operations
    dangerous_patterns = [
        r'os\.system',
        r'subprocess\.',
        r'eval\(',
        r'exec\(',
        r'__import__',
    ]
    for pattern in dangerous_patterns:
        if re.search(pattern, code):
            return False
    return True
```

### 3. Secret Management

```python
# Encrypted secrets in _pyrite
from cryptography.fernet import Fernet

class SecretManager:
    def encrypt_secret(self, key, value):
        # Store encrypted
        pass

    def decrypt_secret(self, key):
        # Retrieve decrypted
        pass
```

### 4. Rate Limiting

```python
# Prevent abuse
from functools import wraps
import time

def rate_limit(calls_per_minute=10):
    def decorator(func):
        last_calls = []

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove old calls
            while last_calls and now - last_calls[0] > 60:
                last_calls.pop(0)

            if len(last_calls) >= calls_per_minute:
                raise Exception("Rate limit exceeded")

            last_calls.append(now)
            return func(*args, **kwargs)

        return wrapper
    return decorator
```

---

## Future Architecture

### v1.0.0 Goals

1. **Complete Agent Layer**
   - Implement BaseAgent interface
   - Build genome management system
   - Create mutation engine
   - Deploy evolution coordinator

2. **Production Desktop App**
   - Polished Electron interface
   - Complete FastAPI backend
   - Docker deployment ready
   - Auto-update system

3. **Enhanced Flight Recorder**
   - Complete telemetry system
   - Phylogenetic tree visualization
   - Scientific data export
   - Analysis tools

### v2.0.0 Vision

1. **Multi-Agent Systems**
   - Agent communication protocols
   - Cooperative evolution
   - Competition mechanics
   - Ecosystem simulation

2. **Cloud Integration**
   - Remote agent execution
   - Distributed fitness evaluation
   - Cloud storage for lineages
   - Collaboration features

3. **Advanced Analytics**
   - ML-powered insights
   - Evolutionary predictions
   - Automatic optimization
   - Research paper generation

---

## Architecture Diagrams

### System Context

```
┌──────────────────────────────────────────────────────┐
│                    Developer                         │
└────────────────────┬─────────────────────────────────┘
                     │
                     │ waft commands
                     ▼
┌──────────────────────────────────────────────────────┐
│                  WAFT Framework                      │
│  ┌────────────────────────────────────────────────┐  │
│  │              CLI Interface                     │  │
│  └───────────────┬────────────────────────────────┘  │
│                  │                                   │
│  ┌───────────────┼───────────────┬──────────────┐   │
│  │               │               │              │   │
│  ▼               ▼               ▼              ▼   │
│  Foundation  Intelligence  Personality      Agent   │
│  Layer       Layer         Layer           Layer    │
│  └────┬──────────┬───────────┬──────────────┬────┘  │
└───────┼──────────┼───────────┼──────────────┼───────┘
        │          │           │              │
        │          │           │              │
        ▼          ▼           ▼              ▼
   ┌────────┐ ┌────────┐  ┌──────────┐  ┌────────────┐
   │  uv    │ │Empirica│  │ D&D 5e   │  │ Git        │
   │Package │ │SDK     │  │ Mechanics│  │ Repository │
   └────────┘ └────────┘  └──────────┘  └────────────┘
```

### Component Relationships

```
                    ┌─────────────────┐
                    │   Foundation    │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
    ┌─────────┐        ┌──────────┐      ┌─────────┐
    │ Memory  │        │ Substrate│      │ Config  │
    │ Manager │        │ Manager  │      │ Manager │
    └─────────┘        └──────────┘      └─────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Intelligence   │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
    ┌─────────┐        ┌──────────┐      ┌─────────┐
    │Empirica │        │ Decision │      │Analytics│
    │ System  │        │ Matrix   │      │ Engine  │
    └─────────┘        └──────────┘      └─────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Personality   │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
    ┌─────────┐        ┌──────────┐      ┌─────────┐
    │ Tavern  │        │  Being   │      │ Karma   │
    │ Keeper  │        │  System  │      │ System  │
    └─────────┘        └──────────┘      └─────────┘
```

---

## Related Documentation

- **[API Reference](api/API_INDEX.md)** - Complete API documentation
- **[Developer Guide](DEVELOPER_GUIDE.md)** - Development workflow
- **[Extension Guide](development/EXTENSION_GUIDE.md)** - Creating extensions
- **[Prime Directive](PRIME_DIRECTIVE.md)** - Core philosophy
- **[Four-Layer Model](architecture/FOUR_LAYER_MODEL.md)** - Layer details

---

## Conclusion

WAFT's architecture is designed for:
- **Evolutionary development** at its core
- **Scientific rigor** in tracking and measurement
- **Developer experience** through gamification
- **Extensibility** for custom use cases
- **Production readiness** for real applications

The four-layer model provides clear separation of concerns while maintaining cohesion through well-defined interfaces.

---

*Last Updated: 2026-01-16 | Version: 0.9.0 | Architecture Document v1.0*
