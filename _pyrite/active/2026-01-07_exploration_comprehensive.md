# Comprehensive Codebase Exploration: 2026-01-07

**Created**: 2026-01-07 20:00:00 PST
**Purpose**: Deep dive into codebase structure, architecture, and relationships
**Status**: ✅ COMPLETE

---

## Executive Summary

**Codebase Overview**: Waft is a well-structured Python meta-framework with 21 Python files (~6,182 lines), organized into 5 core layers, with comprehensive test coverage (55 tests) and multiple integration points.

**Key Metrics**:
- **Source Files**: 21 Python files
- **Total Lines**: ~6,182 lines
- **Test Files**: 8 test files, 55 tests
- **Core Managers**: 6 manager classes
- **CLI Commands**: 20+ commands across multiple groups
- **Architecture Layers**: 5 layers (Substrate, Memory, Agents, Epistemic, Gamification)

---

## 1. Project Structure

### Directory Organization

```
waft/
├── src/waft/              # Main source code
│   ├── core/              # Core managers (6 classes)
│   │   ├── substrate.py   # SubstrateManager (uv operations)
│   │   ├── memory.py      # MemoryManager (_pyrite structure)
│   │   ├── empirica.py    # EmpiricaManager (epistemic tracking)
│   │   ├── gamification.py # GamificationManager (stats/achievements)
│   │   ├── github.py      # GitHubManager (git operations)
│   │   └── tavern_keeper/ # TavernKeeper RPG system (4 files)
│   ├── cli/               # CLI display components
│   │   ├── epistemic_display.py # Epistemic visualizations
│   │   └── hud.py         # Legacy HUD renderer
│   ├── templates/         # Project templates
│   │   └── __init__.py    # TemplateWriter class
│   ├── ui/                # User interface
│   │   └── dashboard.py   # Red October Dashboard TUI
│   ├── main.py            # CLI entry point (1,537 lines)
│   ├── utils.py           # Utility functions (14 functions)
│   └── web.py             # Web dashboard server
├── tests/                 # Test suite
│   ├── conftest.py       # Pytest fixtures
│   ├── test_commands.py  # CLI command tests
│   ├── test_memory.py     # MemoryManager tests
│   ├── test_substrate.py  # SubstrateManager tests
│   ├── test_gamification.py # Gamification tests
│   ├── test_epistemic_display.py # Display tests
│   └── test_tavern_keeper.py # TavernKeeper tests (15 tests)
├── _pyrite/              # Memory layer
│   ├── active/           # Current work
│   ├── backlog/          # Future work
│   └── standards/        # Standards and protocols
├── _work_efforts/        # Work effort tracking
└── docs/                 # Documentation
```

### Main Entry Points

1. **CLI Entry**: `src/waft/main.py` - Typer-based CLI with 20+ commands
2. **Web Dashboard**: `src/waft/web.py` - HTTP server for web interface
3. **TUI Dashboard**: `src/waft/ui/dashboard.py` - Red October Dashboard

### Configuration Files

- `pyproject.toml` - Project configuration, dependencies, build system
- `uv.lock` - Dependency lock file
- `.cursor/commands/` - Cursor command definitions (9 commands)
- `.github/workflows/` - CI/CD workflows

---

## 2. Architecture Overview

### Five-Layer Architecture

```
┌─────────────────────────────────────────────┐
│   Gamification Layer (TavernKeeper)         │  ← RPG mechanics, character system
│   ───────────────────────────────            │
├─────────────────────────────────────────────┤
│   Epistemic Layer (Empirica)                │  ← Knowledge tracking, learning
│   ───────────────────────                    │
├─────────────────────────────────────────────┤
│   Agents Layer (CrewAI) - Optional          │  ← AI agent capabilities
│   ───────────────────────                    │
├─────────────────────────────────────────────┤
│   Memory Layer (_pyrite/)                   │  ← Project knowledge organization
│   active/ backlog/ standards/              │
├─────────────────────────────────────────────┤
│   Substrate Layer (uv)                      │  ← Package management foundation
│   pyproject.toml uv.lock                    │
└─────────────────────────────────────────────┘
```

### Core Components

#### 1. SubstrateManager (`core/substrate.py`)
**Purpose**: Manages `uv` package operations
**Key Methods**:
- `init_project(name, target_path)` - Initialize uv project
- `sync(project_path)` - Sync dependencies
- `add_dependency(package, project_path)` - Add dependency
- `verify_lock(project_path)` - Check uv.lock exists
- `get_project_info(project_path)` - Extract project metadata

**Dependencies**: `subprocess`, `pathlib`, `utils.parse_toml_field`
**Pattern**: Manager pattern with subprocess delegation

#### 2. MemoryManager (`core/memory.py`)
**Purpose**: Manages `_pyrite/` file-based structure
**Key Methods**:
- `create_structure()` - Create _pyrite folders
- `verify_structure()` - Validate structure
- `get_active_files()` - List active work
- `get_backlog_files()` - List backlog items
- `get_standards_files()` - List standards
- `get_all_files(recursive)` - Get all files
- `get_files_by_extension(extension, recursive)` - Filter by extension

**Dependencies**: `pathlib` only
**Pattern**: Manager pattern with file system operations

#### 3. EmpiricaManager (`core/empirica.py`)
**Purpose**: Epistemic tracking via Empirica CLI
**Key Methods** (11 total):
- `initialize()` - Initialize Empirica in project
- `is_initialized()` - Check initialization status
- `create_session(ai_id, session_type)` - Create session
- `submit_preflight(session_id, vectors, reasoning)` - Preflight assessment
- `submit_postflight(session_id, vectors, reasoning)` - Postflight assessment
- `project_bootstrap()` - Load project context (~800 tokens)
- `log_finding(finding, impact)` - Log discovery
- `log_unknown(unknown)` - Log knowledge gap
- `check_submit(operation)` - Safety gate (PROCEED/HALT/BRANCH/REVISE)
- `create_goal(session_id, objective, scope, criteria)` - Create goal
- `assess_state(session_id, include_history)` - Epistemic assessment

**Dependencies**: `subprocess`, `json`, `shutil`, `os`
**Pattern**: Manager pattern with CLI subprocess calls
**Special Feature**: Auto-detects Python 3.12/3.11 empirica binary

#### 4. GamificationManager (`core/gamification.py`)
**Purpose**: Constructivist Sci-Fi themed gamification
**Key Methods**:
- `damage_integrity(amount, reason)` - Decrease integrity
- `restore_integrity(amount, reason)` - Increase integrity
- `award_insight(amount, reason)` - Award insight (with level-up detection)
- `unlock_achievement(achievement_id, name)` - Unlock achievement
- `get_stats()` - Get current stats
- `get_insight_to_next_level()` - Calculate progress
- `check_achievements(stats)` - Auto-check achievements

**Data Storage**: `_pyrite/.waft/gamification.json`
**Pattern**: Manager pattern with JSON persistence

#### 5. TavernKeeper (`core/tavern_keeper/keeper.py`)
**Purpose**: RPG gamification system (D&D 5e style)
**Key Methods**:
- `roll_check(ability, dc, advantage, disadvantage)` - d20 dice rolling
- `narrate(event, outcome, context)` - Narrative generation (Tracery)
- `process_command_hook(command, success, context)` - Command integration
- `award_rewards(rewards)` - XP, credits, integrity
- `apply_status_effect(effect)` - Buffs/debuffs
- `get_character_sheet()` - Full character data
- `log_adventure(event)` - Adventure journal

**Dependencies**: `tinydb` (optional), `d20` (optional), `pytracery` (optional)
**Pattern**: Manager pattern with graceful degradation (fallbacks if deps missing)
**Data Storage**: `_pyrite/.waft/chronicles.json` (TinyDB or JSON fallback)

#### 6. GitHubManager (`core/github.py`)
**Purpose**: Git/GitHub operations
**Key Methods**:
- `is_initialized()` - Check if git repo exists
- `get_remote_url()` - Get GitHub remote URL
- `init_repository()` - Initialize git repo
- `get_status()` - Get repository status

**Dependencies**: `subprocess`
**Pattern**: Manager pattern with subprocess delegation

### Component Relationships

```
main.py (CLI)
  ├── SubstrateManager ──→ uv commands
  ├── MemoryManager ──→ _pyrite/ operations
  ├── EmpiricaManager ──→ empirica CLI
  ├── GamificationManager ──→ gamification.json
  ├── TavernKeeper ──→ chronicles.json
  ├── GitHubManager ──→ git commands
  ├── TemplateWriter ──→ File generation
  └── Web Handler ──→ HTTP server

TavernKeeper
  ├── Narrator ──→ Narrative generation
  ├── Grammars ──→ Tracery grammars
  └── AI Helper ──→ Quick narrative functions

CLI Display
  ├── epistemic_display.py ──→ Rich visualizations
  └── hud.py ──→ Legacy HUD (deprecated)

UI
  └── dashboard.py ──→ Red October Dashboard TUI
```

---

## 3. Dependencies

### External Dependencies (Core)

```toml
dependencies = [
    "typer>=0.9.0",        # CLI framework
    "rich>=13.0.0",         # Terminal formatting
    "pydantic>=2.0.0",      # Data validation
    "empirica>=1.2.3",      # Epistemic tracking
    "tinydb>=4.8.0",        # File-based database
    "d20>=1.0.0",           # Dice rolling
]
```

### Optional Dependencies

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",       # Testing
    "ruff>=0.1.0",         # Linting/formatting
    "watchdog>=3.0.0",     # File watching (dev mode)
]
crewai = [
    "crewai>=0.1.0",       # AI agents (requires macOS 13.0+)
]
tavern-keeper = [
    "pytracery>=0.1.1",    # Narrative generation
]
```

### Internal Dependencies

**Import Graph**:
- `main.py` imports all managers
- Managers are independent (no circular dependencies)
- `utils.py` used by multiple managers
- `cli/` modules used by `main.py` for display
- `templates/` used by `main.py` for scaffolding

**Dependency Flow**:
```
main.py
  → core/* (managers)
  → utils.py (helpers)
  → cli/* (display)
  → templates/ (scaffolding)
  → ui/ (dashboard)
  → web.py (server)
```

---

## 4. Patterns & Conventions

### Design Patterns

1. **Manager Pattern** (Primary)
   - All core functionality in Manager classes
   - Each manager handles one domain (Substrate, Memory, Empirica, etc.)
   - Managers are independent and composable
   - Example: `SubstrateManager`, `MemoryManager`, `EmpiricaManager`

2. **Command Pattern** (CLI)
   - Each CLI command is a separate function
   - Commands use managers to perform operations
   - Commands share common utilities (`resolve_project_path`, etc.)
   - Example: `@app.command()` decorators in `main.py`

3. **Template Pattern** (Scaffolding)
   - Templates are separate from logic
   - `TemplateWriter` class handles all template generation
   - Templates can be conditionally written (check if exists)
   - Example: `write_justfile()`, `write_ci_yml()`, etc.

4. **Graceful Degradation Pattern**
   - Optional dependencies handled with try/except
   - Fallbacks when dependencies unavailable
   - Example: TavernKeeper uses JSON if TinyDB unavailable, simple random if d20 unavailable

5. **Hook Pattern** (TavernKeeper)
   - Commands call `_process_tavern_hook()` after execution
   - Hooks process dice rolls, narratives, rewards
   - Non-blocking (silently fails if TavernKeeper unavailable)
   - Example: `_process_tavern_hook(project_path, "verify", success)`

### Naming Conventions

- **Classes**: PascalCase (`SubstrateManager`, `TavernKeeper`)
- **Functions**: snake_case (`create_structure`, `roll_check`)
- **Constants**: UPPER_SNAKE_CASE (`REQUIRED_FOLDERS`, `CRISIS_RED`)
- **Files**: snake_case (`epistemic_display.py`, `tavern_keeper/`)
- **Directories**: snake_case (`_pyrite/`, `_work_efforts/`)

### Code Organization

- **Single Responsibility**: Each manager handles one domain
- **Separation of Concerns**: CLI, core logic, display, templates separated
- **Utility Functions**: Common operations in `utils.py`
- **Type Hints**: Used throughout (Optional, Dict, Path, etc.)
- **Docstrings**: All classes and methods documented

### Error Handling Patterns

1. **Try/Except with Graceful Degradation**
   ```python
   try:
       result = subprocess.run(...)
       return True
   except (subprocess.CalledProcessError, FileNotFoundError):
       return False
   ```

2. **Validation Before Operations**
   ```python
   is_valid, error_msg = validate_project_name(name)
   if not is_valid:
       console.print(f"[bold red]❌ {error_msg}[/bold red]")
       raise typer.Exit(1)
   ```

3. **Silent Failures for Optional Features**
   ```python
   try:
       tavern = TavernKeeper(project_path)
       hook_result = tavern.process_command_hook(...)
   except Exception:
       pass  # Silently fail if TavernKeeper not available
   ```

4. **User-Friendly Error Messages**
   ```python
   console.print(f"[bold red]❌ Failed to initialize uv project[/bold red]")
   console.print(f"[dim]→[/dim] Is 'uv' installed? Run: curl -LsSf https://astral.sh/uv/install.sh | sh")
   ```

---

## 5. Key Functionality Mapping

### Core Commands (7 commands)

1. **`waft new <name>`** - Project creation
   - Uses: SubstrateManager, MemoryManager, TemplateWriter, EmpiricaManager, GamificationManager, TavernKeeper
   - Flow: uv init → _pyrite creation → templates → Empirica init → rewards

2. **`waft verify`** - Structure validation
   - Uses: MemoryManager, SubstrateManager, EmpiricaManager, GamificationManager, TavernKeeper
   - Flow: Check _pyrite → Check uv.lock → Check Empirica → Update integrity → RPG hook

3. **`waft sync`** - Dependency sync
   - Uses: SubstrateManager, TavernKeeper
   - Flow: uv sync → RPG hook

4. **`waft add <package>`** - Add dependency
   - Uses: SubstrateManager, TavernKeeper
   - Flow: uv add → RPG hook

5. **`waft init`** - Initialize in existing project
   - Uses: MemoryManager, TemplateWriter, EmpiricaManager, TavernKeeper
   - Flow: _pyrite creation → templates → Empirica init → RPG hook

6. **`waft info`** - Project information
   - Uses: SubstrateManager, MemoryManager, EmpiricaManager, TavernKeeper
   - Flow: Gather info → Display table → RPG hook

7. **`waft serve`** - Web dashboard
   - Uses: WebHandler, MemoryManager, SubstrateManager
   - Flow: Start HTTP server → Serve dashboard → File watching (dev mode)

### Empirica Commands (5 command groups)

1. **`waft session`** - Session management
   - `create` - Create new session
   - `bootstrap` - Load project context
   - `status` - Show session state

2. **`waft finding log`** - Log discoveries
   - Uses: EmpiricaManager, GamificationManager, TavernKeeper
   - Awards: +10 Insight

3. **`waft unknown log`** - Log knowledge gaps
   - Uses: EmpiricaManager

4. **`waft check`** - Safety gate
   - Uses: EmpiricaManager, TavernKeeper
   - Returns: PROCEED/HALT/BRANCH/REVISE

5. **`waft assess`** - Epistemic assessment
   - Uses: EmpiricaManager, GamificationManager, TavernKeeper
   - Awards: +25 Insight

6. **`waft goal`** - Goal management
   - `create` - Create goal with epistemic scope
   - `list` - List active goals

### Gamification Commands (4 commands)

1. **`waft stats`** - Show stats
   - Uses: GamificationManager
   - Displays: Integrity, Insight, Level, Achievements

2. **`waft level`** - Level details
   - Uses: GamificationManager
   - Shows: Progress bar, insight needed

3. **`waft achievements`** - List achievements
   - Uses: GamificationManager

4. **`waft dashboard`** - Epistemic HUD (legacy)
   - Uses: HUD renderer

### Tavern Keeper Commands (7 commands)

1. **`waft character`** - Character sheet
   - Uses: TavernKeeper
   - Displays: D&D stats, ability scores, HP, status effects

2. **`waft chronicle`** - Adventure journal
   - Uses: TavernKeeper
   - Shows: Recent events, narratives, dice rolls

3. **`waft roll <ability> --dc N`** - Manual dice roll
   - Uses: TavernKeeper
   - Supports: Advantage, disadvantage

4. **`waft quests`** - View quests
   - Uses: TavernKeeper
   - Shows: Active and completed quests

5. **`waft note <text>`** - Add narrative note
   - Uses: TavernKeeper, Narrator

6. **`waft observe <text>`** - Log observation
   - Uses: TavernKeeper, Narrator

7. **`waft dashboard`** - Red October Dashboard TUI
   - Uses: TavernKeeper, RedOctoberDashboard
   - Real-time updates at 4Hz

### Extension Points

1. **Command Hooks** - TavernKeeper hooks into all major commands
2. **Template System** - Easy to add new templates
3. **Manager Pattern** - Easy to add new managers
4. **CLI Groups** - Typer supports command groups for organization

---

## 6. Integration Points

### External Integrations

1. **uv (Substrate)**
   - **Integration**: Subprocess calls to `uv` CLI
   - **Operations**: `init`, `sync`, `add`
   - **Data**: `pyproject.toml`, `uv.lock`
   - **Error Handling**: Graceful failure if uv not installed

2. **Empirica (Epistemic)**
   - **Integration**: Subprocess calls to `empirica` CLI
   - **Operations**: Session management, assessments, logging
   - **Data**: `.empirica-project/` directory
   - **Error Handling**: Graceful degradation if CLI unavailable
   - **Special**: Auto-detects Python 3.12/3.11 binary

3. **Git (GitHubManager)**
   - **Integration**: Subprocess calls to `git` CLI
   - **Operations**: Init, status, remote URL
   - **Data**: `.git/` directory
   - **Error Handling**: Returns None if git unavailable

4. **TinyDB (TavernKeeper)**
   - **Integration**: Optional dependency
   - **Operations**: Character data, journal entries, quests
   - **Data**: `chronicles.json`
   - **Error Handling**: Falls back to JSON file operations

5. **d20 (TavernKeeper)**
   - **Integration**: Optional dependency
   - **Operations**: Dice rolling
   - **Error Handling**: Falls back to `random.randint()`

6. **pytracery (TavernKeeper)**
   - **Integration**: Optional dependency
   - **Operations**: Narrative generation
   - **Error Handling**: Falls back to simple random selection

7. **watchdog (Web Dashboard)**
   - **Integration**: Optional dev dependency
   - **Operations**: File watching for live reload
   - **Error Handling**: Falls back to polling

### Internal Integration Points

1. **Command → Manager Flow**
   ```
   CLI Command → Manager → Subprocess/File Operations → Results → Display
   ```

2. **TavernKeeper Hook Integration**
   ```
   Command Success/Failure → _process_tavern_hook() → TavernKeeper.process_command_hook()
   → Dice Roll → Narrative → Rewards → Display
   ```

3. **Gamification Integration**
   ```
   Command → GamificationManager → Update Stats → Check Achievements → Display
   ```

4. **Empirica Integration**
   ```
   Command → EmpiricaManager → CLI Call → JSON Response → Display
   ```

### Configuration Mechanisms

1. **Project Configuration**: `pyproject.toml` (TOML parsing with regex fallback)
2. **Gamification State**: `_pyrite/.waft/gamification.json`
3. **TavernKeeper State**: `_pyrite/.waft/chronicles.json`
4. **Empirica State**: `.empirica-project/` directory

---

## 7. Testing & Quality

### Test Structure

**Test Files** (8 files):
- `conftest.py` - Pytest fixtures (temp directories, projects)
- `test_commands.py` - CLI command end-to-end tests
- `test_memory.py` - MemoryManager tests
- `test_substrate.py` - SubstrateManager tests
- `test_gamification.py` - GamificationManager tests
- `test_epistemic_display.py` - Display function tests
- `test_tavern_keeper.py` - TavernKeeper tests (15 tests)

**Test Coverage**: 55 tests total, all passing

### Test Patterns

1. **Fixture-Based Testing**
   - `temp_project_path` - Temporary project directory
   - `project_with_pyproject` - Project with valid pyproject.toml
   - `project_with_pyrite` - Project with _pyrite structure
   - `full_waft_project` - Complete project setup

2. **End-to-End Testing**
   - Tests actual command execution
   - Validates file system changes
   - Checks output formatting

3. **Unit Testing**
   - Manager methods tested independently
   - Edge cases covered
   - Error handling validated

### Quality Tools

- **Linting**: `ruff` (configured in `pyproject.toml`)
- **Formatting**: `ruff format` (configured)
- **Testing**: `pytest` (comprehensive suite)
- **Type Checking**: Type hints throughout (no mypy yet)

### Test Results

- **Status**: ✅ 55/55 tests passing
- **Execution Time**: ~20.22s
- **Coverage Areas**: All managers, commands, display, gamification, TavernKeeper

---

## 8. Documentation & Knowledge

### Key Documentation Files

1. **README.md** - Main project documentation
2. **CHANGELOG.md** - Version history
3. **SPEC-TAVERNKEEPER.md** - TavernKeeper specification
4. **WAFT_SYSTEM_INTEGRATION.md** - System integration guide
5. **PROJECT_STARTUP_PROCESS.md** - AI assistant orientation guide
6. **Multiple orientation/assessment documents** in `_work_efforts/`

### Architecture Decisions

1. **File-Based Storage**: All data in plain text files (git-friendly)
2. **Manager Pattern**: Each domain has dedicated manager class
3. **Graceful Degradation**: Optional dependencies with fallbacks
4. **CLI-First**: Primary interface is CLI, web/TUI are secondary
5. **Epistemic Integration**: Empirica for knowledge tracking
6. **RPG Gamification**: TavernKeeper adds fun and engagement

### Design Rationale

- **Why Manager Pattern**: Separation of concerns, testability, composability
- **Why File-Based**: Portability, git-friendly, no database setup
- **Why Graceful Degradation**: Works even if optional deps missing
- **Why Subprocess for Integrations**: Leverages existing CLI tools, no API dependencies

---

## 9. Insights & Observations

### Interesting Patterns

1. **Hook-Based Integration**: TavernKeeper hooks into commands non-intrusively
2. **Dual Storage**: TinyDB with JSON fallback for TavernKeeper
3. **Auto-Detection**: EmpiricaManager finds correct Python version binary
4. **Rich Visualizations**: Extensive use of Rich library for beautiful CLI output
5. **Command Mapping**: RPG ability scores mapped to command types

### Areas of Complexity

1. **Main.py Size**: 1,537 lines - could benefit from command grouping
2. **TavernKeeper Integration**: Complex hook system with multiple fallbacks
3. **Empirica CLI Detection**: Multiple fallback paths for finding correct binary
4. **Web Dashboard**: File watching with multiple fallback strategies

### Opportunities for Improvement

1. **Command Organization**: Split `main.py` into command modules
2. **Error Messages**: More actionable suggestions in error messages
3. **TOML Parsing**: Consider proper TOML library for full compliance
4. **Test Coverage**: Add integration tests for web dashboard
5. **Documentation**: Consolidate duplicate documentation files

### Strengths

1. **Clean Architecture**: Well-organized layers and managers
2. **Comprehensive Testing**: 55 tests covering all major functionality
3. **Graceful Degradation**: Works even with missing optional dependencies
4. **Rich CLI**: Beautiful terminal output with Rich library
5. **Extensibility**: Easy to add new commands, managers, templates

---

## 10. Questions & Unknowns

### What Needs Clarification

1. **TOML Parsing Limitations**: 71% success rate documented, but edge cases not fully tested
2. **Empirica CLI Availability**: How often does Python version mismatch occur?
3. **TavernKeeper Performance**: How does TinyDB vs JSON fallback perform at scale?
4. **Web Dashboard Usage**: How often is web dashboard used vs CLI?

### Areas Requiring Deeper Investigation

1. **Command Performance**: No performance benchmarks for commands
2. **Memory Usage**: No analysis of memory footprint
3. **Concurrent Operations**: How does framework handle concurrent command execution?
4. **Error Recovery**: How well does framework recover from partial failures?

### Assumptions That Need Validation

1. **uv Availability**: Assumes uv is installed (tested, but not validated in all environments)
2. **File System Permissions**: Assumes writable filesystem (not tested)
3. **Git Availability**: Empirica requires git, but not always validated
4. **Terminal Capabilities**: TUI dashboard assumes terminal supports Rich features

---

## Component Details

### Manager Classes Summary

| Manager | File | Lines | Methods | Purpose |
|---------|------|-------|---------|---------|
| SubstrateManager | `core/substrate.py` | 164 | 5 | uv operations |
| MemoryManager | `core/memory.py` | 160 | 7 | _pyrite structure |
| EmpiricaManager | `core/empirica.py` | 411 | 11 | Epistemic tracking |
| GamificationManager | `core/gamification.py` | 303 | 8 | Stats/achievements |
| TavernKeeper | `core/tavern_keeper/keeper.py` | 725 | 15+ | RPG system |
| GitHubManager | `core/github.py` | 91 | 4 | Git operations |
| TemplateWriter | `templates/__init__.py` | 434 | 5 | File generation |

### CLI Command Summary

| Command Group | Commands | Purpose |
|---------------|----------|---------|
| Core | 7 commands | Project management |
| Empirica | 5 groups | Epistemic tracking |
| Gamification | 4 commands | Stats/achievements |
| TavernKeeper | 7 commands | RPG gamification |
| Web | 1 command | Web dashboard |

### Data Storage Summary

| Storage | Location | Format | Purpose |
|---------|----------|--------|---------|
| Gamification | `_pyrite/.waft/gamification.json` | JSON | Stats, achievements |
| Chronicles | `_pyrite/.waft/chronicles.json` | TinyDB/JSON | RPG state |
| Empirica | `.empirica-project/` | Directory | Epistemic data |
| Memory | `_pyrite/active|backlog|standards/` | Files | Project knowledge |

---

## Code Quality Observations

### Strengths

1. **Type Hints**: Used throughout codebase
2. **Docstrings**: All classes and methods documented
3. **Error Handling**: Comprehensive try/except blocks
4. **Validation**: Input validation before operations
5. **Testing**: Comprehensive test coverage

### Areas for Improvement

1. **Code Organization**: `main.py` is large (1,537 lines) - could be split
2. **Error Messages**: Some could be more actionable
3. **TOML Parsing**: Regex-based parsing has limitations
4. **Performance**: No performance benchmarks
5. **Documentation**: Some duplicate documentation files

---

## Integration Flow Examples

### Example 1: Project Creation Flow

```
waft new my_project
  ↓
SubstrateManager.init_project()
  → uv init my_project
  ↓
MemoryManager.create_structure()
  → Create _pyrite/active, backlog, standards
  ↓
TemplateWriter.write_all()
  → Write Justfile, CI, agents.py, .gitignore, README
  ↓
EmpiricaManager.initialize()
  → empirica project-init
  → git init (if needed)
  ↓
GamificationManager.award_insight(50, "Created new project")
  → Update gamification.json
  ↓
TavernKeeper.process_command_hook("new", True, {...})
  → Roll CHA check (DC 10)
  → Generate narrative
  → Award rewards
  → Log adventure
  ↓
Display success message with epistemic state
```

### Example 2: Verification Flow

```
waft verify
  ↓
MemoryManager.verify_structure()
  → Check _pyrite folders exist
  ↓
SubstrateManager.verify_lock()
  → Check uv.lock exists
  ↓
EmpiricaManager.project_bootstrap()
  → Get epistemic state
  ↓
GamificationManager.restore_integrity(2.0, "Verification passed")
  → Update integrity
  ↓
TavernKeeper.process_command_hook("verify", True, {...})
  → Roll CON save (DC 12)
  → Generate narrative
  → Award/penalize based on result
  ↓
Display verification results with moon phase
```

---

## Key Discoveries

1. **Architecture Evolution**: Framework evolved from 3-layer to 5-layer architecture
2. **RPG Integration**: TavernKeeper deeply integrated into all commands via hooks
3. **Graceful Degradation**: Extensive fallback mechanisms for optional dependencies
4. **Epistemic Integration**: Empirica fully integrated with 11 methods
5. **Test Coverage**: Comprehensive test suite (55 tests) covering all major functionality
6. **Code Quality**: Clean codebase with no TODO/FIXME markers
7. **Documentation**: Extensive documentation, though some duplication exists

---

## Additional Component Details

### TavernKeeper Subsystem

**Files** (4 files):
- `keeper.py` (725 lines) - Core RPG system
- `narrator.py` (156 lines) - Narrative contribution system
- `grammars.py` (133 lines) - Tracery grammar definitions
- `ai_helper.py` (120 lines) - AI assistant integration helpers

**Key Classes**:
- `TavernKeeper` - Main RPG manager (15+ methods)
- `Narrator` - Narrative contribution (5 methods: observe, reflect, celebrate, question, note)

**Helper Functions**:
- `get_narrator()` - Get Narrator instance
- `quick_observe()` - Quick observation logging
- `quick_note()` - Quick note logging
- `celebrate_moment()` - Celebration logging
- `raise_concern()` - Concern/question logging

**Grammar Types**:
- `SUCCESS_GRAMMAR` - Success narratives
- `FAILURE_GRAMMAR` - Failure narratives
- `LEVEL_UP_GRAMMAR` - Level up celebrations
- `COMMIT_GRAMMAR` - Commit narratives
- `CRITICAL_SUCCESS_GRAMMAR` - Critical success
- `CRITICAL_FAILURE_GRAMMAR` - Critical failure

### Web Dashboard Details

**File Watching Strategy**:
1. **Primary**: `watchdog` library (if available)
   - Uses `Observer` and `FileSystemEventHandler`
   - Watches `web.py` and `main.py`
   - Debounced to prevent multiple reloads

2. **Fallback**: Simple polling (2-second intervals)
   - Thread-based polling
   - Checks file modification times
   - Same debouncing logic

**Features**:
- Dark mode theme (navy blue gradient)
- Navigation bar with links
- Dev mode badge indicator
- Auto-refresh (2s dev, 30s production)
- JSON API endpoints (`/api/info`, `/api/structure`)

### CLI Display Components

**epistemic_display.py** (252 lines):
- `get_moon_phase(coverage)` - Moon phase calculation
- `format_gate_result(gate)` - Gate styling
- `format_epistemic_state(state)` - State visualization
- `create_epistemic_dashboard(context)` - Dashboard creation
- `format_epistemic_summary(state)` - Brief summary

**hud.py** (167 lines):
- `render_hud()` - Legacy HUD renderer
- `create_integrity_bar()` - Integrity visualization
- `create_header()` - Header panel
- `create_build_panel()` - Build panel
- `create_mind_panel()` - Mind panel

### Recent Evolution (Git History)

**Recent Commits** (Last 15):
1. Debug code cleanup (63 occurrences removed)
2. Tavern Keeper merge (complete RPG system)
3. Engineering workflow documentation
4. Gamification state updates
5. UI enhancements (colors, dashboard)

**Pattern**: Active development with frequent commits, comprehensive documentation, systematic cleanup

---

## Status

✅ **Exploration Complete** - Comprehensive understanding of codebase structure, architecture, patterns, and functionality achieved.

**Key Findings**:
- 5-layer architecture with clear separation of concerns
- 6 manager classes handling different domains
- 20+ CLI commands across 4 groups
- Comprehensive test coverage (55 tests)
- Graceful degradation patterns throughout
- Rich visualizations and RPG gamification
- Multiple integration points (uv, Empirica, git, optional deps)

**Next Steps**: Ready to draft plans, implement features, or continue development with full context.
