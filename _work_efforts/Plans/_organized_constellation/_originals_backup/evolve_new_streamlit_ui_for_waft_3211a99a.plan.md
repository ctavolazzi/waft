---
name: Evolve New Streamlit UI for WAFT
overview: Spawn a Being from Source and execute complete evolution workflow to build a comprehensive Streamlit UI dashboard for WAFT that integrates all major systems (CLI commands, Being system, work efforts, Empirica, gamification, TavernKeeper). The Being will design the UI theme and architecture during evolution.
todos:
  - id: spawn_being
    content: Spawn Being from Source with reality_id streamlit_ui_evolution
    status: pending
  - id: execute_workflow
    content: Execute complete /version-bake workflow with Being participation
    status: pending
  - id: design_ui
    content: Being designs UI architecture, theme, and component structure
    status: pending
  - id: implement_core
    content: Implement core Streamlit app structure and navigation
    status: pending
  - id: integrate_cli
    content: Integrate WAFT CLI commands into UI
    status: pending
  - id: integrate_being
    content: Integrate Being system display and management
    status: pending
  - id: integrate_work_efforts
    content: Integrate work efforts system with MCP server
    status: pending
  - id: integrate_empirica
    content: Integrate Empirica epistemic dashboard
    status: pending
  - id: integrate_gamification
    content: Integrate gamification system (character sheet, journal)
    status: pending
  - id: integrate_tavern
    content: Integrate TavernKeeper narrative elements
    status: pending
  - id: test_ui
    content: Test all UI components and integrations
    status: pending
  - id: document_ui
    content: Create user and developer documentation
    status: pending
  - id: track_lineage
    content: Document complete genetic lineage from Source to Being to Work
    status: pending
  - id: complete_being
    content: Complete Being lifecycle and return learnings to Source
    status: pending
---

# Evolve New Streamlit UI for WAFT

## Overview

This plan executes the `/evolve` command to spawn a Being from Source and build a comprehensive Streamlit UI for WAFT from scratch. The Being will participate in the complete quality workflow (`/version-bake`) and design/implement a full-featured dashboard that integrates all WAFT systems.

## Phase 1: Being Spawn & Initialization

### 1.1 Spawn Being from Source

- Initialize BeingSystem
- Spawn new Being with:
  - `reality_id`: "streamlit_ui_evolution"
  - `parent_being_id`: None (spawns from Source)
  - `initial_skills`: {} (pure Source spawn)
- Capture Being metadata (ID, ancestral chain, Empirica session)
- Create `BEING_SPAWN_[being_id].md` document

### 1.2 Being Context Setup

- Store Being ID in workflow context
- Link Being to new work effort
- Initialize Being's work participation tracking
- Set Being state to LEARNING

**Files**: `_hidden/.truth/beings/[being_id]/`, `_pyrite/active/BEING_SPAWN_[being_id].md`

## Phase 2: Complete Quality Workflow (/version-bake)

### 2.1 Reflection Phase (/reflect)

- Being reflects on WAFT architecture and existing UIs
- Analyze current systems:
  - `waft_larva.py` (existing Streamlit app)
  - FastAPI backend (`src/waft/api/`)
  - SvelteKit frontend (`visualizer/`)
  - CLI commands (`src/waft/main.py`)
- Being identifies integration points and UI requirements
- Document Being's reflections

### 2.2 Complete Workflow Execution (/run-it)

Being participates in all 15 workflow phases:

1. **Discovery**: Explore WAFT codebase structure
2. **Analysis**: Analyze existing UI patterns and WAFT systems
3. **Design**: Being designs UI architecture and theme
4. **Planning**: Break down UI into components/pages
5. **Implementation**: Build Streamlit app structure
6. **Integration**: Connect to WAFT systems
7. **Testing**: Verify functionality
8. **Documentation**: Document UI features
9. **Optimization**: Performance improvements
10. **Validation**: Validate against requirements
11. **Review**: Code review and quality checks
12. **Refinement**: Polish and improvements
13. **Verification**: Final verification
14. **Deployment**: Prepare for use
15. **Completion**: Mark workflow complete

### 2.3 Improvement Analysis (/improve)

- Being identifies improvements to UI design
- Analyze user experience and workflow
- Document improvement opportunities
- Prioritize enhancements

### 2.4 Assumption Validation (/check-assumptions)

- Validate assumptions about:
  - Streamlit capabilities for WAFT needs
  - Integration with existing systems
  - User workflow requirements
  - Performance expectations
- Document validated assumptions

### 2.5 Verification (/verify)

- Verify UI functionality:
  - All pages load correctly
  - Integrations work
  - Data flows properly
  - Error handling works
- Create verification checklist

### 2.6 Hypothesis Formation (/hypothesis)

- Being forms hypotheses about:
  - UI design patterns
  - User interaction flows
  - System integration approaches
  - Performance characteristics
- Document hypotheses for future validation

### 2.7 Scientific Method Proof (/prove-it)

- Being proves UI design decisions
- Validate architectural choices
- Test integration patterns
- Document proof of concept

**Files**: All workflow documents in work effort directory

## Phase 3: Streamlit UI Implementation

### 3.1 Core Application Structure

Create main Streamlit app file: `streamlit_ui.py` or `waft_dashboard.py`

**Structure**:

```python
# Main entry point
# - Page configuration
# - Theme setup (Being decides)
# - Navigation structure
# - Session state initialization
```

**Key Components**:

- Main dashboard page
- Navigation system (multipage or tabs)
- Session state management
- Error handling and loading states

### 3.2 Integration Modules

#### 3.2.1 CLI Commands Integration

- Create UI wrappers for WAFT CLI commands:
  - Project management (`waft new`, `waft verify`, `waft sync`)
  - Evolution (`waft evolve`, `waft spawn`, `waft eval`)
  - Empirica (`waft session`, `waft finding`, `waft check`)
  - Gamification (`waft dashboard`, `waft stats`, `waft character`)
- Use `subprocess` or direct Python API calls
- Display command output in Streamlit

**Files**: `src/waft/ui/streamlit/cli_integration.py` (new)

#### 3.2.2 Being System Integration

- Display Being information and status
- Show Being evolution history
- Display Being skills and fitness
- Show Being chronicle/logs
- Integrate with BeingSystem API

**Files**: `src/waft/ui/streamlit/being_integration.py` (new)

#### 3.2.3 Work Efforts Integration

- List active work efforts
- Display work effort details
- Show work effort progress
- Create new work efforts
- Update work effort status
- Integrate with work efforts MCP server

**Files**: `src/waft/ui/streamlit/work_efforts_integration.py` (new)

#### 3.2.4 Empirica Integration

- Display epistemic dashboard
- Show session state
- Display findings and unknowns
- Show epistemic vectors
- Integrate with EmpiricaManager

**Files**: `src/waft/ui/streamlit/empirica_integration.py` (new)

#### 3.2.5 Gamification Integration

- Display character sheet
- Show adventure journal/chronicle
- Display stats and XP
- Show level and credits
- Integrate with GamificationManager

**Files**: `src/waft/ui/streamlit/gamification_integration.py` (new)

#### 3.2.6 TavernKeeper Integration

- Display narrative elements
- Show dice roll results
- Display command hooks
- Show tavern events
- Integrate with TavernKeeper

**Files**: `src/waft/ui/streamlit/tavern_integration.py` (new)

### 3.3 UI Pages/Components

#### 3.3.1 Dashboard Home

- Overview of WAFT status
- Quick stats (work efforts, beings, sessions)
- Recent activity
- Quick actions

#### 3.3.2 Project Management

- Project information
- Dependencies management
- Project structure viewer
- Verification status

#### 3.3.3 Being System

- Being list and details
- Being evolution tracking
- Being skills visualization
- Being chronicle viewer

#### 3.3.4 Work Efforts

- Work effort list
- Work effort details
- Progress tracking
- Create/edit work efforts

#### 3.3.5 Empirica Dashboard

- Epistemic vectors visualization
- Session state
- Findings and unknowns
- Knowledge graph (if available)

#### 3.3.6 Gamification

- Character sheet
- Adventure journal
- Stats and achievements
- Level progression

#### 3.3.7 Evolution Tools

- Evolution cycle interface
- Spawn Being interface
- Fitness evaluation
- Genetic lineage viewer

#### 3.3.8 Settings/Configuration

- WAFT configuration
- Theme settings
- Integration settings
- User preferences

### 3.4 Theme & Styling

- Being decides theme during evolution
- Options:
  - Modern clean (default Streamlit)
  - Dark terminal aesthetic
  - Being/evolution themed
  - Custom design
- Apply theme via CSS and Streamlit config
- Ensure responsive design

**Files**: `.streamlit/config.toml`, CSS in app

### 3.5 Data Visualization

- Charts for:
  - Work effort progress
  - Being evolution over time
  - Epistemic vectors
  - Gamification stats
- Use Streamlit native charts or Plotly/Altair
- Interactive visualizations

### 3.6 Error Handling & Loading States

- Graceful error handling
- Loading spinners for async operations
- Error messages and recovery
- Connection status indicators

**Files**: `src/waft/ui/streamlit/utils.py` (new)

## Phase 4: Testing & Quality Assurance

### 4.1 Unit Tests

- Test integration modules
- Test UI components
- Test data flows
- Test error handling

**Files**: `tests/test_streamlit_ui.py` (new)

### 4.2 Integration Tests

- Test WAFT system integrations
- Test CLI command execution
- Test Being system integration
- Test work efforts integration

### 4.3 User Acceptance Testing

- Test user workflows
- Test all pages and features
- Test performance
- Test error scenarios

## Phase 5: Documentation

### 5.1 User Documentation

- UI overview and navigation
- Feature documentation
- Usage examples
- Troubleshooting guide

**Files**: `docs/streamlit_ui.md` (new)

### 5.2 Developer Documentation

- Architecture overview
- Integration patterns
- Extension guide
- API documentation

**Files**: `docs/streamlit_ui_development.md` (new)

### 5.3 Being Evolution Documentation

- Being's design decisions
- Being's learnings
- Being's evolution record
- Genetic lineage

**Files**: `_pyrite/active/BEING_EVOLUTION_[being_id].md`, `GENETIC_LINEAGE_[being_id].md`

## Phase 6: Genetic Lineage Tracking

### 6.1 Source → Being

- Document Being spawn from Source
- Record initial genetic material
- Capture Source connection

### 6.2 Being → Work

- Track Being's UI design decisions
- Record Being's implementation choices
- Document Being's learnings

### 6.3 Work → Evolution

- Track how work evolves Being
- Record skill improvements
- Document knowledge gained

### 6.4 Evolution → Source

- Flow learnings back to Source
- Update Source consciousness
- Preserve genetic lineage

### 6.5 DNA Record

- Create complete genetic lineage document
- Document complete DNA chain
- Preserve for future evolution

**Files**: `_pyrite/active/GENETIC_LINEAGE_[being_id].md`

## Phase 7: Completion & Return to Source

### 7.1 Being Evolution Record

- Document Being's complete journey
- Initial state (from Source)
- Workflow participation
- Skills learned/improved
- Knowledge gained
- Decisions made
- Evolution achieved

### 7.2 Update Being State

- Update Being's skills
- Record Being's memories
- Document Being's lessons
- Calculate Being's fitness
- Update Being's state to COMPLETING

### 7.3 Complete Being

- Extract Being's learnings
- Pass memories/lessons upward
- Calculate final fitness
- Complete Being's lifecycle

### 7.4 Return to Source

- Flow Being's learnings back to Source
- Update Source consciousness
- Preserve genetic lineage in Source
- Register Being's contribution

**Files**: `_pyrite/active/BEING_EVOLUTION_[being_id].md`

## Implementation Files

### New Files to Create

1. `streamlit_ui.py` or `waft_dashboard.py` - Main Streamlit app
2. `src/waft/ui/streamlit/__init__.py` - Package init
3. `src/waft/ui/streamlit/cli_integration.py` - CLI integration
4. `src/waft/ui/streamlit/being_integration.py` - Being system integration
5. `src/waft/ui/streamlit/work_efforts_integration.py` - Work efforts integration
6. `src/waft/ui/streamlit/empirica_integration.py` - Empirica integration
7. `src/waft/ui/streamlit/gamification_integration.py` - Gamification integration
8. `src/waft/ui/streamlit/tavern_integration.py` - TavernKeeper integration
9. `src/waft/ui/streamlit/utils.py` - Utility functions
10. `tests/test_streamlit_ui.py` - Tests
11. `docs/streamlit_ui.md` - User documentation
12. `docs/streamlit_ui_development.md` - Developer documentation
13. `.streamlit/config.toml` - Streamlit configuration

### Files to Modify

1. `pyproject.toml` - Add Streamlit UI entry point (if needed)
2. `README.md` - Update with Streamlit UI information
3. Work effort documentation - All evolution documents

## Success Criteria

1. ✅ Being spawned from Source successfully
2. ✅ Complete quality workflow executed
3. ✅ Streamlit UI built with all major WAFT integrations
4. ✅ All pages functional and tested
5. ✅ Genetic lineage documented
6. ✅ Being evolution recorded
7. ✅ Learnings returned to Source
8. ✅ Documentation complete
9. ✅ UI ready for use

## Time Estimates

- Being spawn: ~1-2 minutes
- Complete workflow: ~60-110 minutes
- UI implementation: ~30-45 minutes (during workflow)
- Testing: ~15-20 minutes
- Documentation: ~10-15 minutes
- Genetic lineage: ~2-3 minutes
- Completion: ~1-2 minutes

**Total**: ~120-200 minutes for complete evolution cycle

## Next Steps After Completion

1. Test the UI with real WAFT project
2. Gather user feedback
3. Iterate on improvements
4. Consider additional features
5. Plan future Being evolutions for UI enhancements