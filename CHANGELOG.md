# Changelog

All notable changes to Waft will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] / [0.0.3] - 2026-01-06

### Added

#### Tavern Keeper RPG Gamification System
- Complete RPG gamification system with Constructivist Sci-Fi theme
- `waft character` - Display full character sheet with D&D stats
- `waft chronicle` - View adventure journal entries
- `waft roll` - Manual dice roll (d20 system)
- `waft quests` - View active and completed quests
- `waft note` - Add notes to the chronicle
- `waft observe` - Log observations with mood
- `waft dashboard` - Red October Dashboard TUI (real-time updates)
- Character system with ability scores (STR, DEX, CON, INT, WIS, CHA)
- Dice rolling system (d20 with advantage/disadvantage)
- Narrative generation using Tracery grammars
- Status effects (buffs/debuffs) system
- Adventure journal logging
- Command hooks integrated into all major commands:
  - `waft new` - Character creation (CHA check)
  - `waft verify` - Constitution save
  - `waft init` - Ritual casting (WIS check)
  - `waft info` - Perception check
  - `waft sync` - Resource management (INT check)
  - `waft add` - Acquisition (CHA check)
  - `waft finding log` - Discovery (INT check)
  - `waft assess` - Wisdom save
  - `waft check` - Safety gate
  - `waft goal create` - Quest creation
- Git merge driver for semantic merging of `chronicles.json`
- Data migration from `gamification.json` to `chronicles.json`
- Comprehensive test suite (15 tests, all passing)

## [0.0.2] - 2026-01-05

### Added

#### Empirica Beautiful CLI Integration
- `waft session` command group for session management
  - `waft session create` - Create new Empirica session
  - `waft session bootstrap` - Load project context and display dashboard
  - `waft session status` - Show current session state
- `waft finding log` - Log discoveries with impact scores
- `waft unknown log` - Log knowledge gaps
- `waft check` - Run safety gates (PROCEED/HALT/BRANCH/REVISE)
- `waft assess` - Show detailed epistemic assessment with vectors and moon phase
- `waft goal` command group for goal management
  - `waft goal create` - Create goals with epistemic scope
  - `waft goal list` - List active goals
- Moon phase indicators (🌑→🌕) for epistemic health visualization
- Epistemic dashboards with Rich visualizations
- Enhanced existing commands with epistemic state display

#### Epistemic HUD & Gamification System (Constructivist Sci-Fi Theme)
- `waft dashboard` - Epistemic HUD with split-screen layout
  - Header: Project Name | Integrity Bar | Moon Phase
  - Left Panel ("The Build"): Active tasks, file changes (Praxic Stream)
  - Right Panel ("The Mind"): Epistemic vectors, known unknowns (Noetic State)
- Gamification system with Constructivist Sci-Fi terminology:
  - **Integrity** (structural stability, not HP) - Tied to project health
  - **Insight** (verified knowledge, not XP) - Earned from actions and goals
  - **Moon Phase** - "Epistemic Clock" (New Moon = Discovery, Full Moon = Certainty)
  - Leveling system with exponential progression
- `waft stats` - Show current stats (Integrity, Insight, Level, Achievements)
- `waft level` - Show level details and progress to next level
- `waft achievements` - List all achievements (locked/unlocked)
- Achievement badges:
  - 🌱 First Build, 🏗️ Constructor, 🎯 Goal Achiever, 🧠 Knowledge Architect
  - 💎 Perfect Integrity, 🚀 Level 10, 🏆 Master Constructor, 🌙 Epistemic Master

#### Core Commands
- `waft sync` - Sync project dependencies
- `waft add <package>` - Add dependencies to project
- `waft init` - Initialize Waft in existing projects
- `waft info` - Show project information with epistemic state
- `waft serve` - Web dashboard for project visualization

#### Testing Infrastructure
- Comprehensive test suite with pytest
- Test fixtures for various project scenarios (valid/invalid pyproject.toml, with/without _pyrite)
- End-to-end tests for all core commands
- Unit tests for MemoryManager and SubstrateManager

### Changed
- Enhanced CLI with epistemic tracking integration
- Improved error messages with actionable suggestions
- Better validation and error handling
- Commands now show Integrity, Insight, and Moon Phase indicators
- Project creation awards Insight and checks for achievements
- Verification updates Integrity based on results

### Fixed
- Fixed `waft info` duplicate Project Name bug - now shows only one "Project Name" row regardless of pyproject.toml parsing status

## [0.0.1] - 2026-01-05

### Added
- Initial release of Waft framework
- `waft new <name>` command to create new projects with full structure
- `waft verify` command to verify project structure
- Automatic `_pyrite` folder structure creation (active/, backlog/, standards/)
- Template generation for:
  - Justfile with standard recipes
  - GitHub Actions CI workflow
  - CrewAI agents starter template
- Full `uv` integration for Python project management
- SubstrateManager for environment management
- MemoryManager for `_pyrite` structure management
- TemplateWriter for project scaffolding

[0.0.1]: https://github.com/ctavolazzi/waft/releases/tag/v0.0.1


