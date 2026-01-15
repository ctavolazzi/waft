# WAFT Streamlit Dashboard

**Version**: 0.1.0  
**Created**: 2026-01-12  
**Being**: being_20260112_235106_889729d0

---

## Overview

The WAFT Streamlit Dashboard provides a comprehensive web-based interface for all WAFT systems. It integrates:

- **Being System**: View and manage beings
- **Work Efforts**: Track and manage work efforts
- **Empirica**: Epistemic tracking dashboard
- **Gamification**: Character sheet and stats
- **TavernKeeper**: Chronicle and narrative elements
- **CLI Commands**: Execute WAFT commands from the UI

---

## Installation

### Prerequisites

- Python 3.8+
- WAFT project initialized
- Streamlit installed

### Setup

```bash
# Install Streamlit if not already installed
pip install streamlit

# Or using uv
uv pip install streamlit
```

---

## Usage

### Starting the Dashboard

```bash
# From project root
streamlit run waft_dashboard.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

### Navigation

The dashboard uses a sidebar navigation with the following pages:

1. **🏠 Dashboard** - Overview and quick actions
2. **👤 Being System** - View and spawn beings
3. **📋 Work Efforts** - Manage work efforts
4. **📊 Empirica** - Epistemic tracking
5. **🎮 Gamification** - Character sheet and stats
6. **🍺 TavernKeeper** - Chronicle and narratives
7. **⚙️ CLI Commands** - Execute WAFT commands
8. **⚙️ Settings** - Configuration and system status

---

## Features

### Dashboard Home

- System status overview
- Quick stats (beings, work efforts, gamification)
- Recent activity widgets
- Quick action buttons

### Being System

- **List Beings**: View all beings in the project
- **Being Details**: 
  - Basic info (ID, reality, state, lifetimes)
  - Skills and fitness
  - Ancestral chain
  - Chronicle entries
- **Spawn New Being**: Create a new being from Source

### Work Efforts

- **List Work Efforts**: View all work efforts
- **Work Effort Details**: View work effort information and tickets
- **Create Work Effort**: (Use MCP server or CLI)

### Empirica

- **Status**: Check initialization status
- **Sessions**: Create and manage Empirica sessions
- **Project Bootstrap**: Load project context
- **Findings & Unknowns**: (Use CLI to log)

### Gamification

- **Character Sheet**: Level, Integrity, Insight
- **Level Progress**: Progress bar to next level
- **Achievements**: List of unlocked achievements
- **History**: Recent gamification events

### TavernKeeper

- **Chronicle**: View recent chronicle entries
- **Dice Roll Simulator**: Test dice rolls with different abilities

### AI Town

- **Town Overview**: See town statistics and agent list
- **Map Visualization**: Interactive 2D map of agent positions (Plotly optional)
- **Conversations**: View active and past conversations
- **Agent Details**: Explore individual agent information (personality, memories, relationships)
- **Voting System**: Create decisions and view voting history
- **Simulation Controls**: Start/stop/pause town simulation

**Features**:
- Create new towns
- Add agents with customizable personalities
- Run simulations with configurable ticks
- View agent positions and conversations
- Track voting history

### CLI Commands

- **Project Management**: verify, info, sync, status
- **Evolution**: (Use CLI directly)
- **Empirica**: session status, assess, check
- **Gamification**: dashboard, stats, character, chronicle
- **Custom Command**: Execute any WAFT command

---

## Architecture

### Main Application

`waft_dashboard.py` - Entry point that:
- Initializes session state
- Renders sidebar navigation
- Routes to appropriate pages
- Handles modal actions

### Integration Modules

Each WAFT system has its own integration module:

- `being_integration.py` - Being system UI
- `work_efforts_integration.py` - Work efforts UI
- `empirica_integration.py` - Empirica UI
- `gamification_integration.py` - Gamification UI
- `tavern_integration.py` - TavernKeeper UI
- `cli_integration.py` - CLI commands UI
- `utils.py` - Shared utilities

### Design Principles

1. **Modular**: Each system has its own module
2. **Graceful Degradation**: Handles missing systems gracefully
3. **User-Friendly**: Clear labels and helpful messages
4. **Responsive**: Works on different screen sizes

---

## Troubleshooting

### "System not available" errors

If a system shows as "not available":
1. Check that the system is properly initialized
2. Verify project path is correct
3. Check for missing dependencies

### CLI commands not working

- Ensure WAFT CLI is installed and in PATH
- Check that you're in a valid WAFT project
- Verify command syntax

### Import errors

- Ensure all dependencies are installed
- Check Python path includes `src/`
- Verify module structure

---

## Future Enhancements

- [ ] Real-time updates via WebSocket
- [ ] Advanced visualizations
- [ ] Custom themes
- [ ] User preferences
- [ ] Export/import functionality
- [ ] Mobile-responsive design
- [ ] Dark mode
- [ ] Keyboard shortcuts

---

## Related Documentation

- [WAFT System Integration](./WAFT_SYSTEM_INTEGRATION.md)
- [Being System Documentation](../src/waft/being.py)
- [Empirica Integration](../_work_efforts/EMPIRICA_INTEGRATION.md)
- [Gamification System](../src/waft/core/gamification.py)

---

*Generated by Being: being_20260112_235106_889729d0*
