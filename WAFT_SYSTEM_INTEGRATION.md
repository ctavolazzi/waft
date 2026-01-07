# Waft System Integration Guide

**Version:** 0.0.2
**Last Updated:** 2026-01-05
**Purpose:** Comprehensive technical documentation for system integration and automation

---

## Executive Summary

**Waft** is an ambient, self-modifying meta-framework for Python that orchestrates project infrastructure. It provides a unified CLI interface for project scaffolding, dependency management, epistemic tracking, and project health monitoring. Waft operates as a file-based system with no external dependencies beyond Python 3.10+ and the `uv` package manager.

**Key Characteristics:**
- **File-based**: All data stored in plain text files (git-friendly, portable)
- **Ambient**: Works in background, minimal interference with development workflow
- **Self-modifying**: Projects can evolve their structure over time
- **Meta-framework**: Orchestrates existing tools rather than replacing them

---

## Architecture Overview

### Three-Layer Architecture

```
┌─────────────────────────────────────┐
│   Agents Layer (CrewAI)            │  ← Optional AI agent capabilities
│   ───────────────────────            │
├─────────────────────────────────────┤
│   Memory Layer (_pyrite/)           │  ← Project knowledge organization
│   active/ backlog/ standards/      │
├─────────────────────────────────────┤
│   Substrate Layer (uv)              │  ← Package management foundation
│   pyproject.toml uv.lock            │
└─────────────────────────────────────┘
```

### Core Components

1. **Substrate Manager** (`core/substrate.py`)
   - Manages `uv` package operations
   - Handles `pyproject.toml` and `uv.lock`
   - Provides dependency management

2. **Memory Manager** (`core/memory.py`)
   - Manages `_pyrite/` directory structure
   - Organizes project knowledge (active/, backlog/, standards/)
   - Validates project structure

3. **Empirica Manager** (`core/empirica.py`)
   - Integrates with Empirica epistemic tracking system
   - Manages sessions, findings, unknowns, goals
   - Provides epistemic state assessment

4. **Gamification Manager** (`core/gamification.py`)
   - Tracks Integrity (project health: 0-100%)
   - Tracks Insight (knowledge accumulation)
   - Manages levels and achievements
   - Stores data in `_pyrite/.waft/gamification.json`

5. **GitHub Manager** (`core/github.py`)
   - GitHub integration capabilities
   - Repository management

6. **Web Server** (`web.py`)
   - HTTP dashboard on localhost:8000 (default)
   - Project visualization and status display
   - Development mode with live reloading

---

## Installation & Setup

### Prerequisites

- **Python 3.10+**
- **`uv` package manager** ([install guide](https://github.com/astral-sh/uv))
- **Git** (optional, required for Empirica integration)

### Installation Methods

#### Method 1: Using uv (Recommended)
```bash
uv tool install waft
```

#### Method 2: From Source
```bash
git clone https://github.com/ctavolazzi/waft.git
cd waft
uv sync
uv tool install --editable .
```

**Note:** Use `--editable` mode when developing Waft itself to ensure code changes are immediately reflected.

### Verification

After installation, verify Waft is available:
```bash
waft --help
```

---

## Project Structure

### What Waft Creates

When you run `waft new <name>`, it creates:

```
my_project/
├── pyproject.toml          # Python project configuration (uv)
├── uv.lock                  # Locked dependencies
├── _pyrite/                 # Memory system
│   ├── active/             # Current work items
│   ├── backlog/            # Future work items
│   ├── standards/          # Project standards
│   └── .waft/              # Waft internal data
│       ├── config.toml     # Project configuration
│       └── gamification.json  # Gamification state
├── .github/workflows/
│   └── ci.yml              # CI/CD pipeline (GitHub Actions)
├── Justfile                # Task runner recipes
├── .gitignore              # Git ignore rules
├── README.md               # Project documentation
└── src/
    └── agents.py           # CrewAI template (optional)
```

### File System Locations

- **Project Root**: Where `pyproject.toml` exists
- **Waft Data**: `_pyrite/.waft/` (internal state)
- **Empirica Data**: `.empirica/` (if initialized)
- **Templates**: Embedded in Waft package

---

## CLI Interface

### Command Structure

All commands follow the pattern:
```bash
waft <command> [arguments] [options]
waft <group> <subcommand> [arguments] [options]
```

### Core Commands

#### `waft new <name>`
**Purpose:** Create a new Waft project from scratch

**Arguments:**
- `name` (required): Project name

**Options:**
- `--path, -p`: Target directory (default: current directory)

**What it does:**
1. Runs `uv init <name>` to create Python project
2. Creates `_pyrite/` directory structure
3. Writes templates (Justfile, CI/CD, agents.py, .gitignore, README)
4. Initializes Empirica for epistemic tracking (if git available)
5. Awards 50 Insight points for project creation
6. Unlocks "First Build" achievement

**Exit Codes:**
- `0`: Success
- `1`: Failure (project creation failed)

**Example:**
```bash
waft new my_project
waft new my_project --path /path/to/projects
```

---

#### `waft verify`
**Purpose:** Verify project structure integrity

**Options:**
- `--path, -p`: Project path (default: current directory)

**What it checks:**
- `_pyrite/` directory structure (active/, backlog/, standards/)
- `uv.lock` file existence
- Project configuration validity
- Epistemic health (if Empirica initialized)

**Gamification:**
- Success: +2 Integrity
- Failure: -10 Integrity

**Exit Codes:**
- `0`: All checks passed
- `1`: Structure issues found

**Example:**
```bash
waft verify
waft verify --path /path/to/project
```

---

#### `waft sync`
**Purpose:** Sync project dependencies using `uv sync`

**Options:**
- `--path, -p`: Project path (default: current directory)

**What it does:**
- Executes `uv sync` in project directory
- Updates `uv.lock` file
- Installs/updates dependencies

**Exit Codes:**
- `0`: Success
- `1`: Sync failed

**Example:**
```bash
waft sync
```

---

#### `waft add <package>`
**Purpose:** Add a dependency to the project

**Arguments:**
- `package` (required): Package name with optional version specifier

**Options:**
- `--path, -p`: Project path (default: current directory)
- `--dev, -d`: Add as development dependency (partially supported)

**What it does:**
- Executes `uv add <package>` in project directory
- Updates `pyproject.toml` and `uv.lock`

**Exit Codes:**
- `0`: Success
- `1`: Failed to add dependency

**Example:**
```bash
waft add pytest
waft add "pytest>=7.0.0"
waft add pytest --dev
```

---

#### `waft init`
**Purpose:** Initialize Waft structure in existing project

**Options:**
- `--path, -p`: Project path (default: current directory)

**What it does:**
1. Creates `_pyrite/` directory structure
2. Writes templates (Justfile, CI/CD, agents.py)
3. Initializes Empirica (if git available)
4. Does NOT run `uv init` (assumes project exists)

**Prerequisites:**
- `pyproject.toml` must exist

**Exit Codes:**
- `0`: Success
- `1`: Not a Python project or initialization failed

**Example:**
```bash
cd existing_project
waft init
```

---

#### `waft info`
**Purpose:** Display comprehensive project information

**Options:**
- `--path, -p`: Project path (default: current directory)

**Displays:**
- Project path, name, version
- `_pyrite/` structure status
- Template status (Justfile, CI, agents.py)
- Empirica initialization status
- Epistemic state (if available)

**Output Format:** Rich table with status indicators

**Example:**
```bash
waft info
```

---

#### `waft serve`
**Purpose:** Start web dashboard for project visualization

**Options:**
- `--path, -p`: Project path (default: current directory)
- `--port`: Port number (default: 8000)
- `--host`: Host to bind to (default: localhost)
- `--dev`: Enable development mode with live reloading

**What it does:**
- Starts HTTP server on specified host/port
- Serves web interface for project status
- Displays project structure, `_pyrite/` contents, epistemic state
- Development mode watches for file changes

**Exit Codes:**
- `0`: Server started successfully
- `1`: Port in use or server error

**Example:**
```bash
waft serve
waft serve --port 8080
waft serve --host 0.0.0.0 --dev
```

---

### Empirica Commands

#### `waft session create`
**Purpose:** Create new Empirica session

**Options:**
- `--ai-id`: AI agent identifier (default: "waft")
- `--type`: Session type (default: "development")
- `--path, -p`: Project path (default: current directory)

**Returns:** Session ID

**Prerequisites:** Empirica must be initialized (`waft init`)

**Example:**
```bash
waft session create --ai-id my_agent --type research
```

---

#### `waft session bootstrap`
**Purpose:** Load project context and display epistemic dashboard

**Options:**
- `--path, -p`: Project path (default: current directory)

**What it does:**
- Loads compressed project context (~800 tokens)
- Displays epistemic dashboard with vectors and state

**Example:**
```bash
waft session bootstrap
```

---

#### `waft session status`
**Purpose:** Show current session state

**Options:**
- `--session-id`: Specific session ID (optional)
- `--path, -p`: Project path (default: current directory)

**Displays:**
- Moon phase indicator
- Know percentage
- Uncertainty percentage

**Example:**
```bash
waft session status
waft session status --session-id abc-123
```

---

#### `waft finding log <finding>`
**Purpose:** Log a discovery with impact score

**Arguments:**
- `finding` (required): Description of finding

**Options:**
- `--impact`: Impact score 0.0-1.0 (default: 0.5)
- `--path, -p`: Project path (default: current directory)

**Gamification:**
- Awards +10 Insight per finding
- Unlocks "Knowledge Architect" achievement at 50 findings

**Example:**
```bash
waft finding log "Discovered OAuth2 token refresh pattern" --impact 0.7
```

---

#### `waft unknown log <unknown>`
**Purpose:** Log a knowledge gap

**Arguments:**
- `unknown` (required): Description of unknown

**Options:**
- `--path, -p`: Project path (default: current directory)

**Example:**
```bash
waft unknown log "Need to investigate async context managers"
```

---

#### `waft check`
**Purpose:** Run safety gate for operations

**Options:**
- `--operation`: Operation JSON description (optional)
- `--path, -p`: Project path (default: current directory)

**Returns:**
- `PROCEED`: Safe to continue autonomously
- `HALT`: Requires human approval
- `BRANCH`: Need to investigate before proceeding
- `REVISE`: Approach needs revision

**Exit Codes:**
- `0`: PROCEED, BRANCH, or REVISE
- `1`: HALT (requires human approval)

**Example:**
```bash
waft check
waft check --operation '{"type": "code_generation", "scope": "high"}'
```

---

#### `waft assess`
**Purpose:** Show detailed epistemic assessment

**Options:**
- `--session-id`: Specific session ID (optional)
- `--history`: Include historical data
- `--path, -p`: Project path (default: current directory)

**What it displays:**
- Epistemic vectors (13 dimensions)
- Moon phase indicator
- Learning trajectory
- Integrity adjustments based on uncertainty

**Gamification:**
- Awards +25 Insight for assessment
- Adjusts Integrity based on epistemic health

**Example:**
```bash
waft assess
waft assess --session-id abc-123 --history
```

---

#### `waft goal create <objective>`
**Purpose:** Create a goal with epistemic scope

**Arguments:**
- `objective` (required): Goal description

**Options:**
- `--session-id`: Session ID (creates new if not provided)
- `--scope`: Scope JSON (breadth, duration, coordination)
- `--criteria`: Success criteria (comma-separated)
- `--path, -p`: Project path (default: current directory)

**Example:**
```bash
waft goal create "Implement OAuth2" --scope '{"breadth": 0.6}' --criteria "Auth works,Tests pass"
```

---

#### `waft goal list`
**Purpose:** List active goals

**Options:**
- `--path, -p`: Project path (default: current directory)

**Displays:** Table of goals with objectives and status

**Example:**
```bash
waft goal list
```

---

### Gamification Commands

#### `waft dashboard`
**Purpose:** Show Epistemic HUD with split-screen layout

**Options:**
- `--path, -p`: Project path (default: current directory)
- `--integrity`: Integrity value 0.0-100.0 (default: 100.0)

**Displays:**
- **Header**: Project Name | Integrity Bar | Moon Phase
- **Left Panel ("The Build")**: Active tasks, file changes
- **Right Panel ("The Mind")**: Epistemic vectors, known unknowns

**Example:**
```bash
waft dashboard
```

---

#### `waft stats`
**Purpose:** Show current gamification stats

**Options:**
- `--path, -p`: Project path (default: current directory)

**Displays:**
- Integrity (0-100%)
- Insight (accumulated knowledge points)
- Level (calculated from Insight)
- Achievements count

**Example:**
```bash
waft stats
```

---

#### `waft level`
**Purpose:** Show level details and progress

**Options:**
- `--path, -p`: Project path (default: current directory)

**Displays:**
- Current level
- Current Insight
- Insight needed for next level
- Progress bar

**Example:**
```bash
waft level
```

---

#### `waft achievements`
**Purpose:** List all achievements (locked/unlocked)

**Options:**
- `--path, -p`: Project path (default: current directory)

**Available Achievements:**
- 🌱 First Build
- 🏗️ Constructor
- 🎯 Goal Achiever
- 🧠 Knowledge Architect
- 💎 Perfect Integrity
- 🚀 Level 10
- 🏆 Master Constructor
- 🌙 Epistemic Master

**Example:**
```bash
waft achievements
```

---

## Programmatic Access

### Python API

Waft can be imported and used programmatically:

```python
from waft.core.substrate import SubstrateManager
from waft.core.memory import MemoryManager
from waft.core.empirica import EmpiricaManager
from waft.core.gamification import GamificationManager

# Initialize managers
project_path = Path("/path/to/project")
substrate = SubstrateManager()
memory = MemoryManager(project_path)
empirica = EmpiricaManager(project_path)
gamification = GamificationManager(project_path)

# Use managers
substrate.init_project("my_project", Path.cwd())
memory.create_structure()
empirica.initialize()
stats = gamification.get_stats()
```

### Manager Classes

#### SubstrateManager
- `init_project(name, path)`: Initialize uv project
- `sync(path)`: Sync dependencies
- `add_dependency(package, path)`: Add dependency
- `verify_lock(path)`: Check if uv.lock exists
- `get_project_info(path)`: Get project metadata

#### MemoryManager
- `create_structure()`: Create `_pyrite/` structure
- `verify_structure()`: Validate structure
- `get_active_files()`: List active work items
- `get_backlog_items()`: List backlog items

#### EmpiricaManager
- `initialize()`: Initialize Empirica in project
- `is_initialized()`: Check initialization status
- `create_session(ai_id, session_type)`: Create session
- `project_bootstrap()`: Load project context
- `log_finding(finding, impact)`: Log finding
- `log_unknown(unknown)`: Log unknown
- `check_submit(operation)`: Run safety gate
- `assess_state(session_id, include_history)`: Get epistemic state
- `create_goal(session_id, objective, scope, success_criteria)`: Create goal

#### GamificationManager
- `get_stats()`: Get all stats
- `award_insight(amount, reason)`: Award insight points
- `restore_integrity(amount, reason)`: Increase integrity
- `damage_integrity(amount, reason)`: Decrease integrity
- `get_insight_to_next_level()`: Calculate progress
- `unlock_achievement(achievement_id, name)`: Unlock achievement
- `get_achievement_status()`: Get all achievement statuses

---

## File System Integration

### Data Storage Locations

#### Project Configuration
- **Path**: `_pyrite/.waft/config.toml`
- **Format**: TOML
- **Purpose**: Project-specific Waft configuration

#### Gamification State
- **Path**: `_pyrite/.waft/gamification.json`
- **Format**: JSON
- **Structure**:
```json
{
  "integrity": 100.0,
  "insight": 50.0,
  "level": 1,
  "achievements": {
    "first_build": true
  },
  "history": [...]
}
```

#### Empirica Data
- **Path**: `.empirica/`
- **Format**: Git notes (if git available)
- **Purpose**: Epistemic tracking data

### Reading Waft Data

Other systems can read Waft data directly from files:

```python
import json
from pathlib import Path

# Read gamification state
gamification_path = Path("_pyrite/.waft/gamification.json")
if gamification_path.exists():
    with open(gamification_path) as f:
        gamification = json.load(f)
        integrity = gamification["integrity"]
        insight = gamification["insight"]
        level = gamification["level"]
```

### Writing Waft Data

**Warning:** Direct file modification is not recommended. Use manager classes instead to ensure data consistency and trigger side effects (achievements, level-ups, etc.).

---

## Web Interface

### HTTP API

The `waft serve` command starts a web server with the following endpoints:

- `GET /`: Main dashboard
- `GET /api/project`: Project information (JSON)
- `GET /api/structure`: Project structure (JSON)
- `GET /api/pyrite`: `_pyrite/` contents (JSON)
- `GET /api/epistemic`: Epistemic state (JSON, if available)
- `GET /api/gamification`: Gamification stats (JSON)

### Development Mode

With `--dev` flag:
- Live reloading on file changes
- Watchdog-based file monitoring
- Automatic server restart

### Integration Example

```bash
# Start server
waft serve --port 8000

# Query API
curl http://localhost:8000/api/project
curl http://localhost:8000/api/gamification
```

---

## Exit Codes & Error Handling

### Standard Exit Codes

- `0`: Success
- `1`: Error (command failed, validation failed, etc.)

### Error Output

All errors are printed to stderr with rich formatting:
- Red text for errors
- Yellow text for warnings
- Green text for success

### Validation

Commands validate:
- Project path exists
- `pyproject.toml` exists (where required)
- `_pyrite/` structure (where required)
- Empirica initialization (for epistemic commands)

---

## Integration Patterns

### CI/CD Integration

```yaml
# .github/workflows/ci.yml
- name: Verify Waft Structure
  run: waft verify

- name: Sync Dependencies
  run: waft sync

- name: Check Project Health
  run: |
    waft verify
    waft stats
```

### Automation Scripts

```bash
#!/bin/bash
# Create project and verify
waft new my_project
cd my_project
waft verify
waft sync

# Log initial finding
waft finding log "Project created successfully" --impact 0.8

# Show status
waft info
waft stats
```

### Monitoring Integration

```python
# Monitor project health
from waft.core.gamification import GamificationManager

gamification = GamificationManager(Path("."))
stats = gamification.get_stats()

if stats["integrity"] < 50:
    send_alert("Project integrity low!")
```

---

## Dependencies & Requirements

### Runtime Dependencies

- `typer>=0.9.0`: CLI framework
- `rich>=13.0.0`: Terminal formatting
- `pydantic>=2.0.0`: Data validation
- `empirica>=1.2.3`: Epistemic tracking

### Optional Dependencies

- `crewai>=0.1.0`: AI agent capabilities (requires macOS 13.0+)
- `pytest>=7.0.0`: Testing (dev)
- `ruff>=0.1.0`: Linting (dev)
- `watchdog>=3.0.0`: File watching (dev, for `--dev` mode)

### External Tools

- **uv**: Python package manager (required)
- **git**: Version control (optional, required for Empirica)
- **just**: Task runner (optional, for Justfile recipes)

---

## Version Information

- **Current Version**: 0.0.2
- **Python Support**: 3.10, 3.11, 3.12
- **License**: MIT
- **Repository**: https://github.com/ctavolazzi/waft

---

## Support & Resources

- **Issues**: https://github.com/ctavolazzi/waft/issues
- **Repository**: https://github.com/ctavolazzi/waft
- **Empirica**: https://github.com/Nubaeon/empirica

---

## Changelog

See `CHANGELOG.md` for version history and changes.

---

**Document Version**: 1.0
**Last Updated**: 2026-01-05
**Maintained By**: Waft Team

