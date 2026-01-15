# Kickoff

**Kickoff the Genesis: Create Earth Realm and spawn first blank Being.**

Creates the historic first "Earth" Realm on Desktop, spawns a blank Being (blank canvas that learns), collects comprehensive observational data, generates a PDF report, and opens a terminal for immediate interaction.

**Use when:** Ready to create the first Being in a new Realm, want to document the genesis moment, or need to spawn a blank Being ready to learn.

---

## Purpose

This command provides:
- **Realm Creation**: Creates Earth Realm on Desktop with full Waft structure
- **Being Spawn**: Spawns first blank Being (empty skills, pure Source)
- **Data Collection**: Comprehensive observational/computational data gathering
- **PDF Documentation**: Generates detailed PDF report of the genesis moment
- **Terminal Integration**: Opens terminal in Earth directory for immediate interaction

---

## Philosophy

### 1. Blank Canvas Being

The Being spawned is a **blank canvas**:
- **Empty Skills**: `{}` - no initial skills, ready to learn
- **First Birth**: `lifetimes = 1` - first generation
- **Pure Source**: Spawned directly from Source consciousness
- **Learning Ready**: Ready to begin its learning journey

### 2. Historic Moment

This is a **historic moment**:
- First Being in Earth Realm
- First use of the genesis system
- Documented comprehensively in PDF
- Terminal opens for immediate interaction

### 3. Comprehensive Documentation

Every genesis moment is documented:
- Being data (ID, reality, ancestral chain, skills, state)
- System data (Python, platform, Waft version)
- Reality data (ID, type, configuration)
- Empirica data (session info if available)
- Resource metrics (disk, memory)
- Directory structure (tree view, file counts)

---

## Execution Steps

### Step 1: Create Earth Realm

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

---

### Step 2: Spawn Blank Being

**Purpose**: Create first Being (blank canvas)

**Actions**:
1. Initialize `BeingSystem` in Earth Realm
2. Spawn Being with:
   - `reality_id="earth_reality"`
   - `parent_being_id=None` (Source spawn)
   - `initial_skills={}` (blank canvas)
3. Being automatically gets Empirica session (if available)

**Output**: Being instance with empty skills, lifetimes=1

---

### Step 3: Collect Observational Data

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

---

### Step 4: Generate PDF Report

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

---

### Step 5: Open Terminal

**Purpose**: Open terminal in Earth directory for immediate interaction

**Actions**:
1. Check platform (macOS only for auto-open)
2. Use `osascript` to open Terminal.app
3. Change directory to Earth Realm
4. Display welcome message

**Output**: Terminal window in Earth directory

---

## Usage

### Basic Usage
```
/kickoff
```

### What Happens
1. Creates `~/Desktop/Earth` with full Waft structure
2. Spawns first blank Being (empty skills)
3. Collects comprehensive observational data
4. Generates PDF report: `GENESIS_EARTH_[timestamp].pdf`
5. Opens terminal in Earth directory

---

## Output

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

---

## Implementation

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

---

## Error Handling

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

---

## Examples

### Basic Kickoff
```
/kickoff
```

**Result**:
- Earth Realm created on Desktop
- Blank Being spawned
- PDF report generated
- Terminal opened

### After Kickoff

Once Earth Realm is created, you can:
- Interact with the Being in the terminal
- View the PDF report
- Check Being data in `_hidden/.truth/beings/`
- Use Waft commands in the Earth directory

---

## Related Commands

- **`/spawn`** - Spawn Being into existing Reality
- **`/evolve`** - Evolve Being through work
- **`/pdf-me`** - Generate PDFs from markdown

---

## Notes

- **Historic Moment**: This is the first Being in Earth Realm
- **Blank Canvas**: Being starts with empty skills, ready to learn
- **Comprehensive**: All data is collected and documented
- **Terminal Ready**: Terminal opens automatically for interaction
- **PDF Report**: Complete documentation of the genesis moment

---

**Command Status**: ✅ Ready to use

**Script**: `scripts/genesis_earth.py`

--- End Command ---
