# Waft

> **Ambient, self-modifying Meta-Framework for Python**

Waft is the "Operating System" for your projects, gently orchestrating:
- **Environment** (`uv`) - Python package management
- **Memory** (`_pyrite`) - Persistent project structure
- **Agents** (`crewai`) - AI agent capabilities (optional)
- **Epistemic Tracking** (`Empirica`) - Knowledge and learning measurement

## Quick Start

```bash
# Install Waft
uv tool install waft

# Create a new project
waft new my_awesome_project

# Verify project structure
cd my_awesome_project
waft verify
```

## What Waft Creates

When you run `waft new <name>`, it creates:

- ✅ **uv project** - Fully configured Python project
- ✅ **_pyrite structure** - Memory folders (active/, backlog/, standards/)
- ✅ **Justfile** - Modern task runner with standard recipes
- ✅ **CI/CD** - GitHub Actions workflow for validation
- ✅ **CrewAI template** - Starter template for AI agents

## Commands

### Core Commands

#### `waft new <name>`

Creates a new project with full Waft structure:

```bash
waft new my_project
waft new my_project --path /path/to/target
```

**Options:**
- `--path, -p`: Target directory (default: current directory)

This command:
- Initializes a new `uv` project
- Creates the `_pyrite` memory structure
- Generates templates (Justfile, CI/CD, agents.py)
- Initializes Empirica for epistemic tracking
- Awards Insight for project creation

#### `waft verify`

Verifies the project structure:

```bash
waft verify
waft verify --path /path/to/project
```

**Options:**
- `--path, -p`: Project path (default: current directory)

Checks:
- `_pyrite` directory structure
- `uv.lock` existence
- Project configuration
- Epistemic health (if Empirica initialized)
- Updates Integrity based on verification results

#### `waft sync`

Sync project dependencies using `uv sync`:

```bash
waft sync
waft sync --path /path/to/project
```

**Options:**
- `--path, -p`: Project path (default: current directory)

#### `waft add <package>`

Add a dependency to the project:

```bash
waft add pytest
waft add "pytest>=7.0.0"
waft add pytest --path /path/to/project
```

**Options:**
- `--path, -p`: Project path (default: current directory)
- `--dev, -d`: Add as development dependency (note: currently adds as regular dependency)

**Note:** The `--dev` flag is recognized but currently adds dependencies as regular dependencies. Full dev dependency support coming soon.

#### `waft init`

Initialize Waft structure in an existing project:

```bash
waft init
waft init --path /path/to/project
```

**Options:**
- `--path, -p`: Project path (default: current directory)

**Requirements:**
- Project must have `pyproject.toml` (command will fail if missing)

This command:
- Creates `_pyrite` structure
- Writes templates
- Initializes Empirica

#### `waft info`

Show information about the Waft project:

```bash
waft info
waft info --path /path/to/project
```

**Options:**
- `--path, -p`: Project path (default: current directory)

Displays:
- Project path, name, version
- `_pyrite` structure status
- `uv.lock` status
- Template status (Justfile, CI, agents.py)
- Empirica initialization status
- Epistemic state (if available)

#### `waft serve`

Start a web dashboard for the project:

```bash
waft serve
waft serve --port 8080 --dev
```

### Empirica Commands

#### `waft session`

Session management commands:

```bash
waft session create [--ai-id ID] [--type TYPE]
waft session bootstrap  # Load project context and display dashboard
waft session status [--session-id ID]
```

#### `waft finding log`

Log a discovery with impact score:

```bash
waft finding log "Discovered X" --impact 0.7
```

Awards +10 Insight per finding.

#### `waft unknown log`

Log a knowledge gap:

```bash
waft unknown log "Need to investigate Y"
```

#### `waft check`

Run safety gate:

```bash
waft check
waft check --operation '{"type": "code_generation", "scope": "high"}'
```

Returns: PROCEED, HALT, BRANCH, or REVISE

#### `waft assess`

Show detailed epistemic assessment:

```bash
waft assess
waft assess --session-id ID --history
```

Displays epistemic vectors, moon phase, and learning trajectory.

#### `waft goal`

Goal management commands:

```bash
waft goal create "Implement OAuth2" --scope '{"breadth": 0.6}' --criteria "Auth works,Tests pass"
waft goal list
```

### Gamification Commands

#### `waft dashboard`

Show the Epistemic HUD with split-screen layout:

```bash
waft dashboard
```

Displays:
- **Header**: Project Name | Integrity Bar | Moon Phase
- **Left Panel ("The Build")**: Active tasks, file changes
- **Right Panel ("The Mind")**: Epistemic vectors, known unknowns

#### `waft stats`

Show current stats:

```bash
waft stats
```

Displays Integrity, Insight, Level, and Achievements.

#### `waft level`

Show level details and progress:

```bash
waft level
```

#### `waft achievements`

List all achievements:

```bash
waft achievements
```

### Tavern Keeper Commands

The Tavern Keeper transforms your repository into a "Living Repository" with RPG gamification mechanics.

#### `waft character`

Display full character sheet with D&D stats:

```bash
waft character
```

Shows ability scores, modifiers, HP, level, insight, credits, and status effects.

#### `waft chronicle`

View adventure journal entries:

```bash
waft chronicle
waft chronicle --limit 50
```

Displays recent events, narratives, dice rolls, and outcomes.

#### `waft roll`

Manual dice roll:

```bash
waft roll strength --dc 15
waft roll dexterity --dc 12 --advantage
waft roll wisdom --dc 10 --disadvantage
```

Roll a d20 check with optional advantage/disadvantage.

#### `waft quests`

View active and completed quests:

```bash
waft quests
```

#### `waft note`

Add a note to the chronicle:

```bash
waft note "Fixed authentication bug" --category bug
waft note "Added new feature" --category feature
```

#### `waft observe`

Log an observation:

```bash
waft observe "That refactor looks beautiful!" --mood delighted
waft observe "Weird, that's not right" --mood concerned
```

#### `waft dashboard`

Red October Dashboard - Real-time TUI:

```bash
waft dashboard
```

Displays:
- **Header**: Integrity monitor with health bar
- **Left Panel**: Character biometrics (level, ability scores, status effects)
- **Center Panel**: System log (adventure journal feed)
- **Right Panel**: Directives (active operation, credits, insight)

Press `Q` to quit.

**See [SPEC-TAVERNKEEPER.md](SPEC-TAVERNKEEPER.md) for complete documentation.**

## Epistemic Tracking

Waft integrates with [Empirica](https://github.com/Nubaeon/empirica) to provide epistemic tracking:

- **Moon Phase Indicators** (🌑→🌕): Visual representation of epistemic health
  - 🌑 New Moon: Discovery/Uncertainty phase
  - 🌒→🌔 Waxing: Building knowledge
  - 🌕 Full Moon: Execution/Certainty phase

- **Epistemic Vectors**: Track 13 dimensions of knowledge
- **Project Bootstrap**: Load compressed context (~800 tokens)
- **Safety Gates**: CHECK gates for risky operations

## Gamification System

Waft includes a Constructivist Sci-Fi themed gamification system:

- **💎 Integrity**: Structural stability of the project (100% = Perfect)
  - Decreases with errors (-10 per failed test)
  - Increases with successful operations (+2 per success)

- **🧠 Insight**: Accumulation of verified knowledge
  - Earned from: creating projects (+50), logging findings (+10), assessments (+25)
  - Level calculation: `Level = sqrt(Insight / 100)`

- **🌙 Moon Phase**: "Epistemic Clock" reflecting certainty level

- **🏆 Achievements**: Unlock badges for milestones
  - 🌱 First Build, 🏗️ Constructor, 🎯 Goal Achiever, 🧠 Knowledge Architect, etc.

### Tavern Keeper RPG System

The **Tavern Keeper** adds full RPG mechanics to your repository:

- **Character System**: D&D 5e style ability scores (STR, DEX, CON, INT, WIS, CHA)
- **Dice Rolling**: d20 system with advantage/disadvantage
- **Narrative Generation**: Procedural narratives using Tracery grammars
- **Status Effects**: Buffs and debuffs from critical successes/failures
- **Adventure Journal**: Chronicle of all events, rolls, and outcomes
- **Command Hooks**: All major commands trigger RPG checks and award rewards

Every command you run becomes part of your repository's story. The Tavern Keeper narrates your journey, tracks your progress, and celebrates your achievements.

**See [SPEC-TAVERNKEEPER.md](SPEC-TAVERNKEEPER.md) for complete documentation.**

## Philosophy

Waft is **ambient** - it works quietly in the background, setting up the infrastructure so you can focus on building.

Waft is **self-modifying** - projects created with Waft can evolve and adapt.

Waft is a **meta-framework** - it doesn't replace your tools, it orchestrates them.

## Installation

```bash
# Using uv (recommended)
uv tool install waft

# Or from source
git clone https://github.com/ctavolazzi/waft.git
cd waft
uv sync
uv tool install --editable .
```

### Development Mode

When developing waft itself, **always use `--editable` mode**:

```bash
uv tool install --editable .
```

This ensures code changes are immediately reflected when running `waft` commands.
Without `--editable`, you must reinstall after each code change.

**Quick reinstall script:**
```bash
./scripts/dev-reinstall.sh
```

## Requirements

- Python 3.10+
- `uv` package manager ([install](https://github.com/astral-sh/uv))
- `just` task runner (optional, [install](https://github.com/casey/just))

### Optional Dependencies

- **CrewAI**: For AI agent capabilities. Install with `uv sync --extra crewai` in projects that need it.
  - Note: Requires macOS 13.0+ due to onnxruntime dependency

## Project Structure

A Waft project includes:

```
my_project/
├── pyproject.toml          # uv project config
├── _pyrite/
│   ├── active/             # Current work
│   ├── backlog/            # Future work
│   └── standards/          # Standards
├── .github/workflows/
│   └── ci.yml              # CI/CD pipeline
├── Justfile                # Task runner
└── src/
    └── agents.py           # CrewAI template
```

## License

MIT

## Repository

https://github.com/ctavolazzi/waft

