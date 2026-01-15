---
name: Comprehensive Waft Enhancement & Release
overview: Complete enhancement package including Empirica Beautiful CLI with "Constructivist Sci-Fi" theme, bug fixes, documentation updates, testing infrastructure, and GitHub release preparation. Implementing "Living Repository" workflow with feature branches and atomic commits.
todos:
  - id: create-display-module
    content: Create src/waft/cli/epistemic_display.py with moon phase indicators, state formatting, gate styling, and dashboard creation functions
    status: completed
  - id: enhance-new-command
    content: Enhance waft new command to show epistemic state and moon phase indicator in success panel
    status: completed
    dependencies:
      - create-display-module
  - id: enhance-verify-command
    content: Enhance waft verify command to include epistemic health check and state display
    status: completed
    dependencies:
      - create-display-module
  - id: enhance-info-command
    content: Enhance waft info command to add Epistemic State section with moon phase and confidence levels
    status: completed
    dependencies:
      - create-display-module
  - id: enhance-init-command
    content: Enhance waft init command to show epistemic initialization status and state
    status: completed
    dependencies:
      - create-display-module
  - id: add-session-commands
    content: Add waft session command group with create, bootstrap, and status subcommands
    status: completed
    dependencies:
      - create-display-module
  - id: add-finding-command
    content: Add waft finding log command for logging discoveries with impact scores
    status: completed
    dependencies:
      - create-display-module
  - id: add-unknown-command
    content: Add waft unknown log command for logging knowledge gaps
    status: completed
    dependencies:
      - create-display-module
  - id: add-check-command
    content: Add waft check command for safety gates with styled gate result display
    status: completed
    dependencies:
      - create-display-module
  - id: add-assess-command
    content: Add waft assess command with detailed epistemic assessment dashboard including vectors, moon phase, trajectory, and drift detection
    status: completed
    dependencies:
      - create-display-module
  - id: add-goal-commands
    content: Add waft goal command group with create and list subcommands
    status: completed
    dependencies:
      - create-display-module
  - id: fix-info-bug
    content: Fix waft info duplicate Project Name bug by simplifying project info extraction logic
    status: pending
  - id: improve-error-handling
    content: Improve error handling with validation, better messages, and Rich formatting
    status: pending
  - id: update-readme
    content: Update README.md to document all 7+ commands including new Empirica commands with examples
    status: pending
  - id: update-changelog
    content: Update CHANGELOG.md with all new features, bug fixes, and changes for v0.0.2
    status: pending
  - id: setup-test-infrastructure
    content: Create tests/ directory structure with conftest.py and test files for all modules
    status: pending
  - id: write-tests
    content: Write basic tests for CLI commands, epistemic display, Empirica integration, and error handling
    status: pending
    dependencies:
      - setup-test-infrastructure
  - id: end-to-end-validation
    content: Test all commands end-to-end including new Empirica features and error scenarios
    status: pending
    dependencies:
      - write-tests
  - id: version-bump
    content: Update pyproject.toml version to 0.0.2 and ensure CHANGELOG is complete
    status: pending
    dependencies:
      - update-changelog
  - id: create-epistemic-hud
    content: Create src/waft/cli/hud.py with Rich split-screen layout (The Build / The Mind) and header with Integrity bar and Moon Phase
    status: pending
  - id: create-gamification-manager
    content: Create src/waft/core/gamification.py with GamificationManager class using Constructivist Sci-Fi theme (Integrity/Insight, not HP/XP)
    status: pending
  - id: integrate-gamification-commands
    content: Add waft dashboard, waft stats, waft level, and waft achievements commands with Rich visualizations
    status: pending
    dependencies:
      - create-gamification-manager
      - create-epistemic-hud
  - id: integrate-gamification-into-commands
    content: Integrate gamification rewards into existing commands (Insight for actions, Integrity for health, Moon Phase for epistemic state)
    status: pending
    dependencies:
      - create-gamification-manager
  - id: create-achievements-system
    content: Implement achievements system with Constructivist Sci-Fi badges and milestone tracking
    status: pending
    dependencies:
      - create-gamification-manager
  - id: setup-github-repo-structure
    content: Create .github/ISSUE_TEMPLATE/, .github/PULL_REQUEST_TEMPLATE.md, and repository configuration
    status: pending
  - id: enhance-github-actions
    content: Enhance .github/workflows/ci.yml and create .github/workflows/release.yml with comprehensive CI/CD
    status: pending
  - id: create-github-integration
    content: Create src/waft/core/github.py and add waft github commands (init, status, create-pr, sync)
    status: pending
  - id: setup-github-projects
    content: Set up GitHub Project board, milestones, labels, and issue templates
    status: pending
  - id: create-github-journal
    content: Create .github/JOURNAL.md and waft journal commands for development introspection and decision tracking
    status: pending
  - id: version-bump
    content: Update pyproject.toml version to 0.0.2 and ensure CHANGELOG is complete with all features
    status: pending
    dependencies:
      - update-changelog
  - id: github-release
    content: Create GitHub release v0.0.2 with release notes, tag, and push all changes
    status: pending
    dependencies:
      - version-bump
      - end-to-end-validation

category: hopes
confidence: 0.66
constellation_date: 2026-01-14
---

#Empirica Beautiful CLI Enhancement Plan

## Overview

Enhance the Waft CLI to leverage Empirica's epistemic tracking capabilities, making the CLI more informative and beautiful through:

1. **Enhanced existing commands** - Add epistemic state visualization to current commands
2. **New Empirica commands** - Create dedicated commands for epistemic tracking
3. **Rich visualizations** - Use Rich library + Empirica data for beautiful epistemic dashboards

## Architecture

### Components

1. **Epistemic Display Module** (`src/waft/cli/epistemic_display.py`)

- Moon phase indicators (🌑→🌕) based on epistemic coverage
- Confidence level visualization
- Epistemic state panels and tables
- Gate result styling (PROCEED/HALT/BRANCH/REVISE)

2. **Enhanced Main CLI** (`src/waft/main.py`)

- Integrate epistemic indicators into existing commands
- Add project-bootstrap context loading
- Show epistemic health in command outputs

3. **New Empirica Commands** (`src/waft/main.py` - new command groups)

- `waft session` - Session management
- `waft finding` - Finding logging
- `waft unknown` - Unknown logging
- `waft check` - Safety gates
- `waft assess` - State assessment
- `waft goal` - Goal management

## Implementation Details

### Phase 1: Epistemic Display Module

Create `src/waft/cli/epistemic_display.py` with:

- `get_moon_phase(coverage: float) -> str` - Returns moon phase emoji based on epistemic coverage
- 🌑 Critical (< 25%)
- 🌒 Low (25-50%)
- 🌓 Moderate (50-75%)
- 🌔 Good (75-90%)
- 🌕 Excellent (90%+)
- `format_epistemic_state(state: dict) -> Panel` - Creates Rich Panel with epistemic state
- Shows all 13 vectors in organized table
- Color-coded by health level
- Includes moon phase indicator
- `format_gate_result(gate: str) -> Text` - Styles gate results
- PROCEED: green
- HALT: red
- BRANCH: yellow
- REVISE: yellow
- `create_epistemic_dashboard(context: dict) -> Panel` - Comprehensive dashboard
- Epistemic state summary
- Active goals
- Recent findings
- Open unknowns
- Learning trajectory

### Phase 2: Enhance Existing Commands

**`waft new`**:

- Load project-bootstrap context if Empirica initialized
- Show epistemic state in success panel
- Display moon phase indicator

**`waft verify`**:

- Add epistemic health check
- Show epistemic state if available
- Display moon phase in verification summary

**`waft info`**:

- Add "Epistemic State" section to table
- Show moon phase indicator
- Display confidence levels
- Link to `waft assess` for detailed view

**`waft init`**:

- Show epistemic initialization status
- Display epistemic state after initialization

### Phase 3: New Empirica Commands

**`waft session`** (subcommands):

- `waft session create [--ai-id ID] [--type TYPE]` - Create new session
- `waft session bootstrap` - Load project context and display dashboard
- `waft session status [--session-id ID]` - Show current session state

**`waft finding`**:

- `waft finding log "discovery" [--impact 0.7]` - Log finding with impact

**`waft unknown`**:

- `waft unknown log "gap"` - Log knowledge gap

**`waft check`**:

- `waft check [--operation JSON]` - Run safety gate, display result with styling

**`waft assess`**:

- `waft assess [--session-id ID] [--history]` - Show detailed epistemic assessment
- Epistemic vectors table
- Moon phase indicator
- Learning trajectory
- Drift detection

**`waft goal`**:

- `waft goal create "objective" [--scope JSON] [--criteria LIST]` - Create goal
- `waft goal list` - List active goals

## Files to Create/Modify

### New Files

1. `src/waft/cli/epistemic_display.py` - Epistemic visualization utilities
2. `src/waft/core/gamification.py` - Gamification manager (HP, XP, Gold, Leveling)
3. `src/waft/core/github.py` - GitHub integration
4. `.github/ISSUE_TEMPLATE/bug_report.md` - Bug report template
5. `.github/ISSUE_TEMPLATE/feature_request.md` - Feature request template
6. `.github/PULL_REQUEST_TEMPLATE.md` - PR template
7. `.github/workflows/release.yml` - Release automation workflow
8. `tests/test_gamification.py` - Gamification tests
9. `tests/test_github.py` - GitHub integration tests

### Modified Files

1. `src/waft/main.py` - Add new commands and enhance existing ones
2. `src/waft/core/empirica.py` - Minor enhancements for display data
3. `.github/workflows/ci.yml` - Enhanced CI/CD
4. `README.md` - Document all new features
5. `CHANGELOG.md` - Update with all changes
6. `pyproject.toml` - Version bump, add dependencies (PyGithub if needed)

## Visual Design

- **Moon Phases**: Use as primary epistemic health indicator
- **Color Coding**:
- Green: Healthy/Proceed
- Yellow: Warning/Revise
- Red: Critical/Halt
- **Rich Tables**: For vector displays and state summaries
- **Panels**: For dashboards and important information
- **Progress Bars**: For confidence levels and coverage

## Integration Points

- Use `EmpiricaManager.project_bootstrap()` at command start when available
- Use `EmpiricaManager.assess_state()` for detailed assessments
- Use `EmpiricaManager.is_initialized()` to check if Empirica is available
- Gracefully degrade if Empirica not initialized (show basic output)

## Phase 4: Bug Fixes & Quality Improvements

### 4.1 Fix `waft info` Bug

**Issue**: Duplicate "Project Name" entries in output

**Fix**: Simplify project info extraction logic in `src/waft/main.py`

**Priority**: High

### 4.2 Error Handling Improvements

- Validate project names and paths
- Better error messages with suggestions
- Graceful handling of missing dependencies
- Use Rich for better error formatting

**Files**: `src/waft/main.py`, `src/waft/core/substrate.py`, `src/waft/core/memory.py`

## Phase 5: Documentation Updates

### 5.1 Update README.md

**Current**: Only documents 2 commands (new, verify)

**Target**: Document all 7 commands + new Empirica commands**Content to Add**:

- `waft sync` command documentation
- `waft add <package>` command documentation
- `waft init` command documentation
- `waft info` command documentation
- `waft serve` command documentation
- All new Empirica commands (session, finding, unknown, check, assess, goal)
- Epistemic tracking features explanation
- Moon phase indicators explanation

### 5.2 Update CHANGELOG.md

**Content to Add**:

```markdown
## [Unreleased] or [0.0.2] - 2026-01-05

### Added
- **Empirica Beautiful CLI** integration with epistemic tracking
    - `waft session` command group for session management
    - `waft finding` command for logging discoveries
    - `waft unknown` command for logging knowledge gaps
    - `waft check` command for safety gates
    - `waft assess` command for epistemic assessment
    - `waft goal` command group for goal management
    - Moon phase indicators (🌑→🌕) for epistemic health
    - Epistemic dashboards with Rich visualizations
    - Enhanced existing commands with epistemic state display
- **Epistemic HUD & Gamification System** 🎮 (Constructivist Sci-Fi Theme)
    - Epistemic HUD with split-screen layout (The Build / The Mind)
    - Integrity system (structural stability, not HP) tied to project health
    - Insight system (verified knowledge, not XP) for completing actions and goals
    - Moon Phase "Epistemic Clock" (New Moon = Discovery, Full Moon = Certainty)
    - Leveling system with exponential progression
    - Achievement badges (First Build, Constructor, Knowledge Architect, etc.)
    - `waft dashboard` command to view the HUD
    - `waft stats` command to view current stats
    - `waft level` command to view level details
    - `waft achievements` command to list achievements
- **GitHub Integration**
    - `waft github init` - Initialize GitHub repository
    - `waft github status` - Show repository status
    - `waft github create-pr` - Create pull requests
    - `waft github sync` - Sync with GitHub
    - Enhanced GitHub Actions CI/CD workflows
    - Release automation workflow
    - `waft journal entry "text"` - Add introspection entry to development journal
    - `waft journal view [--date DATE]` - View journal entries
- Core commands:
    - `waft sync` command to sync project dependencies
    - `waft add <package>` command to add dependencies
    - `waft init` command to initialize Waft in existing projects
    - `waft info` command to show project information
    - `waft serve` command for web dashboard

### Changed
- Enhanced CLI with epistemic tracking integration
- Improved error messages with actionable suggestions
- Better validation and error handling
- GitHub Actions CI/CD enhanced with test matrix and coverage

### Fixed
- Fixed `waft info` duplicate Project Name bug
```



## Phase 6: Testing Infrastructure

### 6.1 Set Up Test Structure

Create `tests/` directory with:

- `tests/__init__.py`
- `tests/conftest.py` with fixtures
- `tests/test_main.py` for CLI tests
- `tests/test_memory.py` for MemoryManager tests
- `tests/test_substrate.py` for SubstrateManager tests
- `tests/test_templates.py` for TemplateWriter tests
- `tests/test_empirica.py` for EmpiricaManager tests
- `tests/test_epistemic_display.py` for display module tests

### 6.2 Write Basic Tests

- Test all CLI commands
- Test epistemic display functions
- Test Empirica integration
- Test error handling
- Test validation logic

## Phase 7: End-to-End Validation

### 7.1 Test All Commands

- Fresh project creation with epistemic tracking
- Existing project initialization
- Dependency management
- All new Empirica commands
- Epistemic state visualization
- Error scenarios

## Phase 8: Epistemic HUD & Gamification System (Constructivist Sci-Fi Theme)

### 8.1 The "Epistemic HUD" (The View)

**Branch**: `feat/epistemic-hud`
**File**: `src/waft/cli/hud.py` (NEW)

**Design**: Rich library layout rendering:
1. **The Header**: Project Name | Integrity Bar (Green/Yellow/Red) | Moon Phase
2. **Split Screen**:
   - **Left ("The Build")**: Active tasks, file changes (Praxic Stream)
   - **Right ("The Mind")**: Empirica vectors, known unknowns (Noetic State)

**Implementation**:
- Use `rich.layout` for split-screen layout
- Header with project info, integrity bar, moon phase indicator
- Left panel: Active work stream (from `_pyrite/active/`)
- Right panel: Epistemic state (from Empirica)
- Real-time updates when commands run

### 8.2 Gamification Core (The Model)

**Branch**: `feat/gamification`
**File**: `src/waft/core/gamification.py` (NEW)

**Theme**: "Constructivist Sci-Fi" terminology:
- **Integrity** (not HP): Structural stability of the project (100% = Perfect)
  - Starts at 100
  - Decreases with errors (-10 per failed test, -5 per epistemic drift)
  - Increases with successful operations (+2 per success)
  - Critical at < 25 Integrity
- **Insight** (not XP): Accumulation of verified knowledge
  - Earned from: `waft finding log` (+10), `waft assess` (+25), goal completion (+25)
  - Level calculation: `Level = sqrt(Insight / 100)`
- **Moon Phase**: "Epistemic Clock"
  - New Moon (🌑): Discovery/Uncertainty phase
  - Waxing (🌒→🌔): Building knowledge
  - Full Moon (🌕): Execution/Certainty phase
- **Achievements**: Construction milestones (First Build, Master Builder, etc.)

**Storage**: File-based in `_pyrite/.waft/gamification.json`

### 8.3 GamificationManager Implementation

**Features**:
- `GamificationManager` class with Constructivist Sci-Fi terminology
- File-based storage in `_pyrite/.waft/gamification.json`
- **Insight rewards**:
  - Creating projects (+50 Insight)
  - Completing goals (+25 Insight per goal)
  - Logging findings (+10 Insight per finding)
  - Reaching epistemic milestones (+100 Insight)
  - Fixing bugs (+30 Insight)
- **Integrity system**:
  - Starts at 100
  - Decreases with errors (-10 per failed test, -5 per epistemic drift)
  - Increases with successful operations (+2 per success)
  - Critical at < 25 Integrity
- **Level calculation**: `Level = sqrt(Insight / 100)`
  - Level 1: 0-99 Insight
  - Level 2: 100-399 Insight
  - Level 3: 400-899 Insight
  - Level 4: 900-1599 Insight
  - etc. (exponential)

### 8.4 Integration Points

- **Empirica Integration**:
  - Insight from epistemic gains (know vector increases)
  - Integrity tied to epistemic health (uncertainty decreases Integrity)
  - Moon phase reflects epistemic state (uncertainty = New Moon, certainty = Full Moon)
- **Command Integration**:
  - Show Integrity/Insight in command outputs
  - Display level-up notifications
  - Achievement announcements
  - Integrity bar in HUD header
- **Visual Display**:
  - Use Rich for beautiful stat displays
  - Progress bars for Insight to next level
  - Integrity bar with color coding (green/yellow/red)
  - Moon phase indicator in header

### 8.5 Commands

- `waft dashboard` - Show the Epistemic HUD (split-screen view)
- `waft stats` - Show current stats (Integrity, Insight, Level, Achievements)
- `waft level` - Show level details and progress to next level
- `waft achievements` - List all achievements (locked/unlocked)

### 8.6 Achievements System

**Achievements** (Constructivist Sci-Fi theme):

- 🌱 **First Build**: Create your first project
- 🏗️ **Constructor**: Create 10 projects
- 🎯 **Goal Achiever**: Complete 10 goals
- 🧠 **Knowledge Architect**: Log 50 findings
- 💎 **Perfect Integrity**: Maintain 100 Integrity for 7 days
- 🚀 **Level 10**: Reach level 10
- 🏆 **Master Constructor**: Create 100 projects
- 🌙 **Epistemic Master**: Achieve Full Moon (100% certainty) on 5 projects

## Phase 9: GitHub Integration & Repository Setup

### 9.1 GitHub Repository Configuration

- Verify git remote configuration
- Set up proper repository structure
- Create `.github/ISSUE_TEMPLATE/` for bug reports and feature requests
- Create `.github/PULL_REQUEST_TEMPLATE.md` for PR standardization
- Set up branch protection rules (via GitHub UI)

### 9.2 GitHub Actions CI/CD Enhancement

**File**: `.github/workflows/ci.yml`

- Add comprehensive test matrix (Python 3.10, 3.11, 3.12)
- Add linting with ruff
- Add type checking (optional mypy)
- Add security scanning
- Add code coverage reporting
- Add gamification stats to CI output

**File**: `.github/workflows/release.yml` (NEW)

- Automated version bumping
- Automated changelog generation
- Automated release creation
- Automated package publishing

### 9.3 GitHub Integration Commands

**File**: `src/waft/core/github.py` (NEW)**New Commands**:

- `waft github init` - Initialize GitHub repository for project
- `waft github status` - Show GitHub repository status
- `waft github create-pr` - Create a pull request (interactive)
- `waft github sync` - Sync local changes with GitHub
- `waft github achievements` - Show GitHub contribution achievements

**Implementation**: Use PyGithub or GitHub CLI integration

### 9.4 GitHub Projects & Organization

- Create GitHub Project board
- Link issues and PRs to project
- Use automation for status updates
- Create milestones for phases
- Use labels for categorization

### 9.5 Documentation & Wiki

- Initialize GitHub Wiki
- Architecture documentation
- Command reference
- Development guide
- Contributing guide
- Gamification guide

### 9.6 GitHub Journal/Diary for Introspection

**File**: `.github/JOURNAL.md` or GitHub Wiki page "Development Journal"

**Purpose**: Track development journey, decisions, insights, and introspection

**Content Structure**:
- Daily/Weekly entries with timestamps
- Decision logs (why we chose certain approaches)
- Epistemic insights (what we learned)
- Challenges and solutions
- Repository growth patterns
- Living repository observations

**Integration**:
- `waft journal entry "text"` - Add entry to journal
- `waft journal view [--date DATE]` - View journal entries
- Auto-commit journal entries to git
- Sync with GitHub Wiki or maintain as `.github/JOURNAL.md`

**Format**:
```markdown
## 2026-01-05 - Epistemic HUD Implementation

**Context**: Starting Phase 8.1 - The Epistemic HUD

**Decisions**:
- Chose Rich library for split-screen layout
- Left panel: "The Build" (Praxic Stream)
- Right panel: "The Mind" (Noetic State)

**Insights**:
- The HUD makes epistemic state visible in real-time
- Split-screen metaphor aligns with Constructivist Sci-Fi theme

**Challenges**:
- Real-time updates require careful state management

**Next Steps**:
- Implement GamificationManager
- Integrate with commands
```

## Phase 10: GitHub Release Preparation

### 10.1 Version Bump

- Update `pyproject.toml` version to 0.0.2
- Ensure CHANGELOG.md is complete
- Include gamification features in changelog

### 10.2 Release Notes

- Create comprehensive release notes
- Include all new features (Empirica, Gamification, GitHub)
- Document breaking changes (if any)
- Include upgrade instructions
- Highlight gamification as fun new feature

### 10.3 Git Operations

- Commit all changes with conventional commits
- Create release branch (if needed)
- Tag release (v0.0.2)
- Push to GitHub

### 10.4 GitHub Release

- Use `create_release.py` or GitHub CLI
- Create release with tag v0.0.2
- Include release notes
- Mark as latest release
- Celebrate with achievement! 🎉

## Execution Order (Living Repository Workflow)

**Workflow**: Act as Lead Developer, create feature branches, make atomic commits, merge branches.

1. **Phase 1** - Create Epistemic Display Module
   - Branch: `feat/epistemic-display`
   - Commit: `feat(cli): add epistemic display module with moon phases`

2. **Phase 2** - Enhance Existing Commands
   - Branch: `feat/enhance-commands`
   - Commit: `feat(cli): enhance commands with epistemic indicators`

3. **Phase 3** - Add New Empirica Commands
   - Branch: `feat/empirica-commands`
   - Commit: `feat(cli): add empirica command groups`

4. **Phase 4** - Fix Bugs & Improve Quality
   - Branch: `fix/info-bug`
   - Commit: `fix(cli): resolve duplicate project name in info command`

5. **Phase 8.1** - Epistemic HUD (The View)
   - Branch: `feat/epistemic-hud`
   - Commit: `feat(cli): add constructive sci-fi HUD layout`

6. **Phase 8.2** - Gamification Core (The Model)
   - Branch: `feat/gamification`
   - Commit: `feat(core): add gamification manager with integrity/insight system`

7. **Phase 8.7** - Integration (The Controller)
   - Branch: `feat/cli-integration`
   - Commit: `feat(cli): integrate gamification into commands`

8. **Phase 5** - Update Documentation
   - Branch: `docs/update-readme-changelog`
   - Commit: `docs: update README and CHANGELOG with new features`

9. **Phase 6** - Add Testing Infrastructure
   - Branch: `test/add-test-suite`
   - Commit: `test: add comprehensive test suite`

10. **Phase 7** - End-to-End Validation
    - Branch: `test/e2e-validation`
    - Commit: `test: add end-to-end validation tests`

11. **Phase 9** - GitHub Integration & Repository Setup
    - Branch: `feat/github-integration`
    - Commit: `feat(github): add GitHub integration commands and workflows`

12. **Phase 10** - GitHub Release Preparation & Push
    - Branch: `release/v0.0.2`
    - Commit: `chore: prepare v0.0.2 release`

## Success Criteria

- All existing commands show epistemic indicators when Empirica is initialized
- New Empirica commands provide beautiful, informative output
- Moon phase indicators accurately reflect epistemic health
- Epistemic dashboards are clear and actionable
- Epistemic HUD working with split-screen layout
- Gamification system working (Integrity, Insight, Moon Phase, Leveling)
- Achievements unlock correctly
- Stats display beautifully with Rich
- `waft info` bug fixed
- All 10+ commands documented in README
- CHANGELOG updated with all features (Empirica, Gamification, GitHub)
- Test suite exists with good coverage
- All commands work end-to-end
- Error messages are helpful and actionable
- GitHub integration working (init, status, create-pr, sync)
- GitHub Actions CI/CD enhanced and working
- Version bumped to 0.0.2
- GitHub release created successfully
- All changes committed and pushed