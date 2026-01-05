# Empirica Integration into Waft

**Created**: 2026-01-04
**Purpose**: Integrate Empirica for epistemic tracking and learning measurement

---

## Sanity Check Results

### ✅ What We Discovered

**TOML Parsing Assumption Test:**
- ✅ 6/8 test cases passed
- ❌ 2 cases failed:
  1. **Escaped quotes** - Regex doesn't handle `\"` correctly
  2. **No quotes** - Regex requires quotes, but TOML allows unquoted strings

**This proves our assumption is incomplete.** We need to either:
- Use a proper TOML parser (`tomllib` in Python 3.11+, or `tomli` for older versions)
- Improve regex to handle these cases
- Document the limitation

---

## Empirica Integration

### What is Empirica?

**Empirica** is a "Cognitive Operating System for AI Agents" that provides:
- **Epistemic Self-Assessment** - Track knowledge across 13 vectors
- **CASCADE Workflow** - Preflight/postflight assessment
- **Session Continuity** - Track learning over time
- **Multi-Agent Coordination** - Coordinate multiple AI agents
- **Git-Native** - Uses git notes for epistemic checkpoints

**Why It's Critical for Waft:**
- Waft tracks **project structure** (_pyrite)
- Empirica tracks **knowledge and learning** (epistemic vectors)
- They complement each other perfectly
- Empirica provides the "self-awareness" layer

---

## Integration Status

### ✅ Completed

1. **Added Empirica as Dependency**
   - Added `empirica>=1.2.3` to `pyproject.toml`
   - Will be installed with `uv sync`

2. **Created EmpiricaManager**
   - `src/waft/core/empirica.py`
   - Methods: `initialize()`, `create_session()`, `submit_preflight()`, `submit_postflight()`
   - Handles git initialization (required for Empirica)

3. **Integrated into Project Creation**
   - `waft new` now initializes Empirica automatically
   - `waft init` also initializes Empirica
   - Gracefully handles if Empirica CLI not available

4. **Added to Project Info**
   - `waft info` now shows Empirica initialization status

5. **Updated Documentation**
   - README mentions Empirica as 4th pillar
   - Main docstring updated

### ⏳ Next Steps

1. **Install Empirica CLI**
   ```bash
   pip install git+https://github.com/Nubaeon/empirica.git@v1.2.3
   ```

2. **Test Integration**
   - Create a test project
   - Verify Empirica initializes
   - Test session creation
   - Test preflight/postflight

3. **Add Empirica Commands**
   - `waft session create` - Create Empirica session
   - `waft session preflight` - Submit preflight assessment
   - `waft session postflight` - Submit postflight assessment
   - `waft session status` - Show current session status

4. **Integrate with _pyrite**
   - Store Empirica session IDs in `_pyrite/active/`
   - Link epistemic assessments to work items
   - Track learning over time

---

## How Empirica Works with Waft

### The Four Pillars

```
┌─────────────────────────────────────┐
│      Agents (CrewAI)                │  ← AI capabilities
│      ───────────────                │
├─────────────────────────────────────┤
│      Epistemic (Empirica)           │  ← Knowledge tracking
│      CASCADE workflow                │
├─────────────────────────────────────┤
│      Memory (_pyrite/)               │  ← Project knowledge
│      active/ backlog/ standards/     │
├─────────────────────────────────────┤
│      Substrate (uv)                 │  ← Package management
│      pyproject.toml uv.lock          │
└─────────────────────────────────────┘
```

### Workflow Integration

**Before Work (Preflight):**
```python
empirica = EmpiricaManager(project_path)
session_id = empirica.create_session(ai_id="waft", session_type="development")
empirica.submit_preflight(session_id, vectors={
    "engagement": 0.8,
    "foundation": {"know": 0.6, "do": 0.7},
    "uncertainty": 0.4
}, reasoning="Starting new feature")
```

**After Work (Postflight):**
```python
empirica.submit_postflight(session_id, vectors={
    "engagement": 0.9,
    "foundation": {"know": 0.85, "do": 0.9},
    "uncertainty": 0.15
}, reasoning="Feature completed, learned X, Y, Z")
```

**Result:** Quantified learning (know: +0.25, uncertainty: -0.25)

---

## EmpiricaManager API

### Methods

```python
from waft.core.empirica import EmpiricaManager

empirica = EmpiricaManager(project_path)

# Check if initialized
if empirica.is_initialized():
    print("Empirica is ready")

# Initialize (runs: empirica project-init)
empirica.initialize()

# Create session
session_id = empirica.create_session(ai_id="waft", session_type="development")

# Submit assessments
empirica.submit_preflight(session_id, vectors={...}, reasoning="...")
empirica.submit_postflight(session_id, vectors={...}, reasoning="...")
```

---

## Installation Requirements

**For Empirica to work:**
1. Git must be installed and initialized
2. Empirica CLI must be installed: `pip install git+https://github.com/Nubaeon/empirica.git@v1.2.3`
3. Project must be a git repository

**Waft handles:**
- ✅ Auto-initializes git if not present
- ✅ Gracefully handles if Empirica CLI not available
- ✅ Shows status in `waft info`

---

## Benefits of Integration

1. **Self-Awareness** - Projects track their own learning
2. **Measurable Progress** - Quantified knowledge growth
3. **Multi-Agent Support** - Coordinate multiple AI agents
4. **Session Continuity** - Track learning across sessions
5. **Transparency** - "Bullshit detector for AI" - keeps everyone honest

---

## Next Steps

1. ✅ **Integration Complete** - EmpiricaManager created and integrated
2. ⏳ **Install Empirica** - `pip install git+https://github.com/Nubaeon/empirica.git@v1.2.3`
3. ⏳ **Test Integration** - Create test project and verify
4. ⏳ **Add CLI Commands** - `waft session` commands for Empirica
5. ⏳ **Document Usage** - How to use Empirica with Waft projects

---

## Status

✅ **Empirica integrated into Waft**
- Manager created
- Integrated into project creation
- Added to project info
- Ready for use once Empirica CLI is installed

