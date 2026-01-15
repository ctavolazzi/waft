# Genesis Kickoff - Complete Documentation

**Historic moment: Create Earth Realm and spawn the first blank Being.**

This document contains all assets for using the Genesis Kickoff system: command definition, plain text prompts, and script documentation.

---

## Table of Contents

1. [Command Definition (`/kickoff`)](#command-definition-kickoff)
2. [Plain Text Prompts](#plain-text-prompts)
3. [Script Documentation](#script-documentation)
4. [Quick Reference](#quick-reference)

---

## Command Definition (`/kickoff`)

### Overview

**Kickoff the Genesis: Create Earth Realm and spawn first blank Being.**

Creates the historic first "Earth" Realm on Desktop, spawns a blank Being (blank canvas that learns), collects comprehensive observational data, generates a PDF report, and opens a terminal for immediate interaction.

**Use when:** Ready to create the first Being in a new Realm, want to document the genesis moment, or need to spawn a blank Being ready to learn.

### Purpose

This command provides:
- **Realm Creation**: Creates Earth Realm on Desktop with full Waft structure
- **Being Spawn**: Spawns first blank Being (empty skills, pure Source)
- **Data Collection**: Comprehensive observational/computational data gathering
- **PDF Documentation**: Generates detailed PDF report of the genesis moment
- **Terminal Integration**: Opens terminal in Earth directory for immediate interaction

### Philosophy

#### 1. Blank Canvas Being

The Being spawned is a **blank canvas**:
- **Empty Skills**: `{}` - no initial skills, ready to learn
- **First Birth**: `lifetimes = 1` - first generation
- **Pure Source**: Spawned directly from Source consciousness
- **Learning Ready**: Ready to begin its learning journey

#### 2. Historic Moment

This is a **historic moment**:
- First Being in Earth Realm
- First use of the genesis system
- Documented comprehensively in PDF
- Terminal opens for immediate interaction

#### 3. Comprehensive Documentation

Every genesis moment is documented:
- Being data (ID, reality, ancestral chain, skills, state)
- System data (Python, platform, Waft version)
- Reality data (ID, type, configuration)
- Empirica data (session info if available)
- Resource metrics (disk, memory)
- Directory structure (tree view, file counts)

### Execution Steps

#### Step 1: Create Earth Realm

**Purpose**: Create new Waft project on Desktop

**Actions**:
1. Check Desktop directory exists
2. Verify `waft` CLI is available
3. Run: `waft new Earth --path ~/Desktop`
4. Verify structure created:
   - `pyproject.toml`
   - `_pyrite/` structure
   - `_hidden/.truth/beings/` directory

**Output**: Earth Realm directory at `~/Desktop/Earth`

#### Step 2: Spawn Blank Being

**Purpose**: Create first Being (blank canvas)

**Actions**:
1. Initialize `BeingSystem` in Earth Realm
2. Spawn Being with:
   - `reality_id="earth_reality"`
   - `parent_being_id=None` (Source spawn)
   - `initial_skills={}` (blank canvas)
3. Being automatically gets Empirica session (if available)

**Output**: Being instance with empty skills, lifetimes=1

#### Step 3: Collect Observational Data

**Purpose**: Gather comprehensive data about the genesis moment

**Data Categories**:

1. **Being Data**:
   - Being ID, Reality ID, Ancestral Chain
   - Lifetimes, Initial Skills, State, Stamina
   - Empirica session ID (if available)

2. **System Data**:
   - Timestamp (ISO format)
   - Python version, Platform, Architecture
   - Waft version, Project path

3. **Reality Data**:
   - Reality ID, Type, Configuration
   - Active status

4. **Empirica Data** (if available):
   - Session ID, AI ID, Session type
   - Initialization status

5. **Resource Metrics**:
   - Disk space (total, used, free)
   - Memory (available, total)
   - CPU count
   - Directory size

6. **Directory Structure**:
   - Tree view of created structure
   - File and directory counts
   - Key files created

**Output**: Dictionary of all collected data

#### Step 4: Generate PDF Report

**Purpose**: Create comprehensive PDF documenting genesis moment

**Actions**:
1. Generate markdown report from collected data
2. Create PDF using `PDFGenerator`:
   - Title: "Genesis: Earth Realm Creation"
   - Style: `clinical_standard`
   - Content: All observational data
3. Save to: `GENESIS_EARTH_[timestamp].pdf` in Earth directory
4. Open PDF automatically

**Output**: PDF report with all genesis data

#### Step 5: Open Terminal

**Purpose**: Open terminal in Earth directory for immediate interaction

**Actions**:
1. Check platform (macOS only for auto-open)
2. Use `osascript` to open Terminal.app
3. Change directory to Earth Realm
4. Display welcome message

**Output**: Terminal window in Earth directory

### Usage

#### Basic Usage
```
/kickoff
```

#### What Happens
1. Creates `~/Desktop/Earth` with full Waft structure
2. Spawns first blank Being (empty skills)
3. Collects comprehensive observational data
4. Generates PDF report: `GENESIS_EARTH_[timestamp].pdf`
5. Opens terminal in Earth directory

### Output

**Created Files**:
- `~/Desktop/Earth/` - Full Waft project structure
- `~/Desktop/Earth/GENESIS_EARTH_[timestamp].pdf` - Genesis report
- `~/Desktop/Earth/_hidden/.truth/beings/[being_id].json` - Being data

**Terminal**:
- Opens in `~/Desktop/Earth` directory
- Ready for immediate Being interaction

**PDF Report Contains**:
- Being Information (ID, reality, ancestral chain, skills, state)
- System Information (Python, platform, Waft version)
- Reality Information (ID, type, configuration)
- Empirica Session (if available)
- Directory Structure (tree view, file counts)
- Resource Metrics (disk, memory, CPU)
- Observational Notes

### Implementation

The command runs `scripts/genesis_earth.py`:

```python
python scripts/genesis_earth.py
```

**Script Location**: `scripts/genesis_earth.py`

**Dependencies**:
- `waft` CLI (must be installed and in PATH)
- `BeingSystem` from `waft.being`
- `RealitySystem` from `waft.reality`
- `PDFGenerator` from `waft.evolution.pdf_generator`
- `EmpiricaManager` (optional, for epistemic tracking)
- `psutil` (optional, for resource metrics)
- `rich` (for console output)

### Error Handling

**Validation**:
- Checks Desktop directory exists
- Verifies `waft` CLI is available
- Handles Being spawn failures gracefully
- Verifies directory structure after creation
- Handles Empirica initialization failures (optional)

**Error Messages**:
- Clear error messages for each failure point
- Suggests fixes for common issues
- Logs errors to console with Rich formatting

### Examples

#### Basic Kickoff
```
/kickoff
```

**Result**:
- Earth Realm created on Desktop
- Blank Being spawned
- PDF report generated
- Terminal opened

#### After Kickoff

Once Earth Realm is created, you can:
- Interact with the Being in the terminal
- View the PDF report
- Check Being data in `_hidden/.truth/beings/`
- Use Waft commands in the Earth directory

### Related Commands

- **`/spawn`** - Spawn Being into existing Reality
- **`/evolve`** - Evolve Being through work
- **`/pdf-me`** - Generate PDFs from markdown

### Notes

- **Historic Moment**: This is the first Being in Earth Realm
- **Blank Canvas**: Being starts with empty skills, ready to learn
- **Comprehensive**: All data is collected and documented
- **Terminal Ready**: Terminal opens automatically for interaction
- **PDF Report**: Complete documentation of the genesis moment

**Command Status**: ✅ Ready to use

**Script**: `scripts/genesis_earth.py`

---

## Plain Text Prompts

### Full Version (Detailed)

Copy and paste this into any chat:

```
I'm ready to run the genesis entry point. I'm ready to run the beginning of the script to try and test it out to see what's happening. This is the first time we're gonna do it together so I want to document this moment in a PDF with a bunch of data on a bunch of observers looking at this. I'd like to get as much observational computational data as possible and then I'd like to move on.

What I am expecting to happen is that we will create a new being and that will be the first one that uses this system that we've designed where essentially it's a blank canvas Being that Learns.

I'm expecting to see a terminal open that uses Waft on a NEW directory on the DESKTOP please.

That NEW directory on the Desktop should be a "Realm" and should be called "Earth".

Please run the genesis script to:
1. Create Earth Realm on Desktop using Waft
2. Spawn first blank Being (empty skills, pure Source)
3. Collect comprehensive observational/computational data
4. Generate PDF documenting this historic moment
5. Open terminal in Earth directory

Run: python scripts/genesis_earth.py
```

### Short Version (Quick)

```
Run the genesis script to create Earth Realm on Desktop, spawn the first blank Being, collect observational data, generate a PDF report, and open a terminal. Execute: python scripts/genesis_earth.py
```

### What It Does

1. **Creates Earth Realm** - Full Waft project structure at `~/Desktop/Earth`
2. **Spawns Blank Being** - First Being with empty skills (blank canvas)
3. **Collects Data** - Comprehensive observational/computational metrics
4. **Generates PDF** - Detailed report: `GENESIS_EARTH_[timestamp].pdf`
5. **Opens Terminal** - Terminal window in Earth directory for interaction

### Expected Output

- ✅ Earth Realm created on Desktop
- ✅ Blank Being spawned (empty skills, lifetimes=1)
- ✅ PDF report generated with all data
- ✅ Terminal opened in Earth directory
- ✅ All observational data documented

---

## Script Documentation

### Script Location

`scripts/genesis_earth.py`

### Script Purpose

Historic moment: Creates the first "Earth" Realm on Desktop and spawns the first blank Being (blank canvas that learns) into it.

### What the Script Does

1. Creates Earth Realm on Desktop using Waft
2. Spawns first blank Being (empty skills, pure Source)
3. Collects comprehensive observational/computational data
4. Generates PDF documenting this historic moment
5. Opens terminal in Earth directory

### Running the Script

#### Direct Execution
```bash
python scripts/genesis_earth.py
```

#### From Project Root
```bash
cd /Users/ctavolazzi/Code/active/waft
python scripts/genesis_earth.py
```

#### As Executable
```bash
chmod +x scripts/genesis_earth.py
./scripts/genesis_earth.py
```

### Script Structure

The script is organized into the following functions:

1. **`get_waft_version()`** - Get Waft version from pyproject.toml
2. **`check_waft_cli()`** - Check if waft CLI is available
3. **`create_earth_realm(desktop_path)`** - Create Earth Realm using Waft CLI
4. **`spawn_blank_being(earth_path)`** - Spawn blank Being (empty skills)
5. **`collect_observational_data(being, earth_path, timestamp)`** - Collect comprehensive data
6. **`generate_markdown_report(data)`** - Generate markdown from data
7. **`generate_pdf(data, earth_path)`** - Create PDF report
8. **`open_terminal(earth_path)`** - Open terminal in Earth directory
9. **`main()`** - Main execution function

### Data Collection

The script collects data in 6 categories:

1. **Being Data**: ID, reality, ancestral chain, skills, state, stamina, Empirica session
2. **System Data**: Timestamp, Python version, platform, architecture, Waft version
3. **Reality Data**: Reality ID, type, configuration, active status
4. **Empirica Data**: Session ID, AI ID, session type, initialization status
5. **Resource Metrics**: Disk space, memory, CPU count, directory size
6. **Directory Structure**: Tree view, file counts, key files

### PDF Report Contents

The generated PDF includes:

- **Being Information**: ID, reality, ancestral chain, lifetimes, skills, state, stamina
- **System Information**: Python version, platform, architecture, Waft version, project path
- **Reality Information**: Reality ID, type, configuration, active status
- **Empirica Session**: Session details (if available)
- **Directory Structure**: Tree view and file counts
- **Resource Metrics**: Disk, memory, CPU information
- **Observational Notes**: Key observations and next steps

### Error Handling

The script includes comprehensive error handling:

- Validates Desktop directory exists
- Verifies `waft` CLI is available
- Handles Being spawn failures gracefully
- Verifies directory structure after creation
- Handles optional dependencies (Empirica, psutil)
- Provides clear error messages with suggestions

### Dependencies

**Required**:
- `waft` CLI (must be installed and in PATH)
- `BeingSystem` from `waft.being`
- `RealitySystem` from `waft.reality`
- `PDFGenerator` from `waft.evolution.pdf_generator`
- `rich` (for console output)

**Optional**:
- `EmpiricaManager` (for epistemic tracking)
- `psutil` (for resource metrics)

---

## Quick Reference

### Command
```
/kickoff
```

### Plain Text Prompt (Short)
```
Run the genesis script to create Earth Realm on Desktop, spawn the first blank Being, collect observational data, generate a PDF report, and open a terminal. Execute: python scripts/genesis_earth.py
```

### Script Execution
```bash
python scripts/genesis_earth.py
```

### Output Location
- **Earth Realm**: `~/Desktop/Earth`
- **PDF Report**: `~/Desktop/Earth/GENESIS_EARTH_[timestamp].pdf`
- **Being Data**: `~/Desktop/Earth/_hidden/.truth/beings/[being_id].json`

### What You Get

1. ✅ Earth Realm with full Waft structure
2. ✅ Blank Being (empty skills, ready to learn)
3. ✅ Comprehensive PDF report
4. ✅ Terminal opened in Earth directory
5. ✅ All observational data documented

---

## Files

- **Command Definition**: `.cursor/commands/kickoff.md`
- **Plain Text Prompts**: `docs/KICKOFF_PROMPT.md`
- **Script**: `scripts/genesis_earth.py`
- **This README**: `scripts/GENESIS_KICKOFF_README.md`

---

**Status**: ✅ Ready to use

**Last Updated**: 2026-01-14
