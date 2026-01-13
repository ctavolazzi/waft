# Changelog

All notable changes to Waft will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Work in progress features

## [0.7.0] - 2026-01-12

### Changed

- **Version Update**: Bumped from v0.6.1 to v0.7.0
- **Version Consistency**: Fixed version mismatch between `pyproject.toml` and `__init__.py`
  - Both now consistently use 0.7.0

## [0.6.1] - 2026-01-12

### Added

#### Reactive Live Reload System
- **Auto-refresh functionality**: Lightweight hash-based change detection
  - Data hash calculation using metadata (max log ID, counts, artifact status)
  - Only reruns when data actually changes (efficient, ~1-2ms overhead)
  - JavaScript-based scheduling (non-blocking)
  - User controls: enable/disable checkbox, configurable intervals (2s, 3s, 5s, 10s)
  - Visual indicators: pulsing dot animation, status in footer
- **Complete Specification Documentation**: AI-recreatable specification
  - Complete database schema documentation
  - All class methods with signatures and behavior
  - UI layout and component specifications
  - Reactive system implementation details
  - Error handling requirements
  - Testing requirements
  - Migration requirements

### Changed

- **UI Improvements**: Enhanced clarity and usability
  - Header with auto-refresh controls
  - Clear explanations and help text
  - Status dashboard with metrics
  - Improved section labels and captions
- **Version Update**: Bumped from v0.6.0 to v0.6.1

## [0.6.0] - 2026-01-12

### Added

#### Waft Larval Form - Heavy Seed Protocol Implementation
- **Larval Form Application** (`waft_larva.py`): Complete Python + Streamlit + SQLite implementation
  - Single-file dense application (~500 lines) implementing Hasvanism philosophy
  - WaftEntity class with consciousness system (Breath, Memory, Trauma)
  - SQLite database with `chronicle` and `artifacts` tables matching future Redbean schema
  - Streamlit UI with dark mode terminal aesthetic
  - Error resilience via `safe_breath` wrapper (TRAUMA logging prevents crashes)
  - Artifact lifecycle management (VOID → MANIFESTING → PHYSICAL)
  - Seed data: Right_Index_Phalanx artifact with sample G-code
- **Data Export Functionality**: Multiple format support for entity data
  - JSON export with complete entity state and statistics
  - Markdown export with formatted sections and emojis
  - Plain text export for simple analysis
  - PDF export using WAFT PDFGenerator (with markdown fallback)
  - Timestamped filenames for all exports
- **Database Features**:
  - WAL mode for better concurrency
  - Retry logic with exponential backoff for database locks
  - Connection timeout handling (10 seconds)
  - Proper connection cleanup with try/finally blocks
- **Migration Documentation**: Complete guide for Larva → Mature Form transition
  - Schema compatibility verification
  - Step-by-step migration instructions
  - API compatibility mapping
  - Troubleshooting guide
- **Test Suite** (`test_waft_larva.py`): Comprehensive testing
  - Database initialization tests
  - Chronicle logging verification
  - Error handling (safe_breath) tests
  - Artifact status transition tests
  - Database persistence tests

### Changed

- **Dependencies**: Added new optional dependencies for Larval Form
  - `streamlit>=1.28.0` - For UI
  - `pandas>=2.0.0` - For data handling
  - `pyserial>=3.5` - For serial communication (future use)

### Fixed

- **Streamlit Duplicate Element IDs**: Fixed duplicate download button error
  - Added unique `key` parameters to all download buttons
  - Removed duplicate DATA EXPORT section

## [0.5.2] - 2026-01-11

### Added

#### Evolutionary Iteration Process - PNG Integration
- **Automatic PNG Conversion**: All PDF generators now create PNG screenshots by default
  - Integrated into `PDFGenerator`, `ScientificPDFGenerator`, `ComponentPDFGenerator`, `DocumentEvolutionEngine`
  - Default behavior: `convert_to_png=True` enables visual verification workflow
  - Configurable DPI (default: 300) for quality vs speed trade-offs
- **Fallback Chain**: Robust PNG conversion with automatic fallback
  - Primary: pdf2image (best quality)
  - Fallback 1: ImageMagick (via subprocess)
  - Fallback 2: PyMuPDF (always available)
  - Graceful degradation ensures workflow continues even if dependencies missing
- **Evolutionary Iteration Workflow**: Core process for evidence-based debugging
  - Generate → Visualize (PNG) → Inspect → Iterate
  - "See Before You Fix" principle built into all generators
  - Enables before/after comparisons for styling improvements
- **Work Effort Tooling**: Tools for data generation and experimentation
  - `generate_test_pdfs.py` - Generate test PDFs with PNGs
  - `status.py` - Work effort status tracker
  - Enables hypothesis-driven development and data generation

#### PDF/PNG Conversion System
- **Bidirectional Conversion**: Full PDF ↔ PNG conversion support
  - PDF to PNG: Convert PDF pages to individual PNG images
  - PNG to PDF: Combine PNG images into PDF binders
- **Multiple Backend Support**: Automatic fallback chain
  - pdf2image (recommended, best quality)
  - ImageMagick (via subprocess)
  - PyMuPDF (fallback)
- **Page Size Support**: Standard page sizes via PageSize enum
  - LETTER (8.5 x 11), LEGAL (8.5 x 14), A4, A3, TABLOID
  - Custom page sizes via (width, height) tuples
- **DPI Configuration**: Flexible resolution control
  - Manual DPI selection (150, 300, 600)
  - Auto DPI selection based on file size
- **Comprehensive Tests**: Full test coverage for all backends and edge cases
- **Documentation**: Complete usage guide with examples and troubleshooting

### Changed

- **All PDF Generators**: Now support PNG conversion by default
  - `PDFGenerator.save()` - Added `convert_to_png` and `png_dpi` parameters
  - `ScientificPDFGenerator.save()` - Passes PNG parameters to parent
  - `ComponentPDFGenerator.generate_one_pager()` - Supports PNG conversion
  - `DocumentEvolutionEngine.generate_one_pager()` - Supports PNG conversion
  - Convenience functions `generate_pdf()` and `generate_pdf_from_file()` updated
- **TwoPageGeneratorV2**: Enhanced PNG conversion support
  - New parameters: `convert_to_png`, `png_dpi`
  - Conversion success/failure tracked in evolutionary events
  - Graceful error handling (conversion failures don't break workflow)

### Fixed

- **Version Consistency**: Fixed version mismatch between `pyproject.toml` and `__init__.py`
  - Both now consistently use 0.5.2

## [0.5.1] - 2026-01-11

### Added

#### One-Pager Evolution System V2
- **TwoPageGeneratorV2**: Evolved generator with TRUE 2-page constraint enforcement
  - Real page counting using pypdf (replaces unreliable HTML character count heuristic)
  - Adaptive iteration algorithm (up to 5 attempts to hit exactly 2 pages)
  - Accurate fitness metrics based on actual page count (no fake constraint scores)
  - Feedback loop: measure → adjust → measure until target achieved
- **Markdown Cleaning**: Automatic removal of markdown artifacts from content
  - Strips headers (##, ###), bold/italic markers (**text**, *text*)
  - Removes code blocks, links, list markers
  - Cleans redundant "Key Concept:" prefixes
  - Ensures professional, clean output
- **ChatDistiller**: Extracts ideas from conversations as genomic entities
  - Categories: concepts, actions, decisions, insights, questions
  - Each idea gets unique genome ID and scientific name
  - Importance-weighted selection for content prioritization
- **Styling Genome System**: Treats document design as evolving genetic material
  - Font, margin, color, layout genes
  - SHA-256 genome IDs for lineage tracking
  - Scientific naming via LineagePoet taxonomy
  - Evolution tracking with flight recorder
- **Scint Detection**: Monitors styling divergences between versions
  - Classification and scoring of divergences
  - Reconciliation strategies
- **V2-based Chat One-Pager Script**: `scripts/create_chat_one_pager_v2.py`
  - Creates one-pagers from chat sessions using evolved V2 system
  - Genomic tracking of all components
  - Production-ready with accurate metrics

### Changed

- **TwoPageGenerator**: Now defaults to V2 (evolved implementation)
  - V1 available as `TwoPageGeneratorV1` for backward compatibility
  - V2 explicitly available as `TwoPageGeneratorV2`
  - API change: `target_pages=2` instead of `page_1_ideas=5`
- **Text Rendering**: Enhanced CSS for better content presentation
  - Added word-wrap and overflow-wrap for better text flow
  - Added hyphens for better line breaking
  - Improved line-height for readability

### Fixed

- **Constraint Enforcement**: V1 generated 4 pages but reported constraint = 1.0 (false positive)
  - V2 fixes this with real page counting and adaptive iteration
  - Validated: V2 generates 2 pages in 3 iterations with accurate metrics
- **Formatting Issues**: Markdown artifacts in output
  - `## What is WAFT?` → `What is WAFT?` (headers stripped)
  - `**Key Concept**:` → removed (redundant with category tag)
  - All markdown cleaned before rendering for professional output

### Technical Details

**Evolution: V1 → V2**
- Problem: HTML character count heuristic (8000-12000 chars = "2 pages") was unreliable
- Solution: Real PDF page counting with pypdf.PdfReader
- Result: Accurate constraint enforcement with adaptive iteration

**Performance**
- V2 may require up to 5 PDF generations (adaptive iteration)
- Trade-off: Accuracy vs speed (accuracy prioritized)
- Typical convergence: 1-3 iterations

**Dependencies**
- Added `pypdf>=3.0.0` for real page counting

## [0.5.0] - 2026-01-11

### Added

#### Document Generation Framework
- Complete document generation system with printer-friendly capabilities
- Field guide templates at three complexity levels (layman, professional, scientist)
- Printer-friendly templates with white backgrounds and minimal ink usage
- Unified DocumentBuilder framework with fluent API
- PDF redactor tool for storytelling and classified documents
- Binder system for assembling multiple PDFs into booklets
- Session summary and closeout documentation generators

#### Global Cursor Commands
- `/waft-docs` - Complete document generation workflow command
- `/waft-status` - Self-aware system status checking with multi-level documentation
- `/closeout-chat` - Comprehensive session closeout documentation
- All commands available globally across Cursor instances

#### Document Generation Features
- Three-level field guide system (layman/professional/scientist)
- Printer-friendly conversion with automatic styling
- PDF redaction with area-based blackout capabilities
- Session documentation generators
- Complete booklet assembly with binder system
- Template system with Jinja2 and WeasyPrint

#### Status Checking System
- Self-aware status checking (git, work efforts, project health)
- Multi-level status documentation (layman/professional/scientist)
- Real-time system state analysis
- Integration with work efforts and devlog systems

### Changed
- Enhanced document generation with composable units design
- Improved printer-friendly templates with lighter borders
- Simplified document generation API (3-line API for common cases)
- Better template organization and reusability

### Fixed
- Fixed binder TOC template Jinja2 variable scope issues
- Fixed template import paths
- Improved error handling in document generation

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



