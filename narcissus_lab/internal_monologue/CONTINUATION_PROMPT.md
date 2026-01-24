# Continuation Prompt: TheGuide Dashboard & 3-Body Architecture

## Context: What We've Built

We've successfully implemented **"The 3-Body Problem Solution"** - a unified architecture connecting:

- **🧠 Mind**: `TheOracle` (epistemic reasoning) - `waft.core.science.TheOracle`
- **🤖 Body**: `NarcissusAgent` + `llm_brain` (self-modification + code generation) - `narcissus_lab/internal_monologue/src/agents/narcissus.py`
- **✨ Spirit**: `TheGuide` (meta-cognitive conscience with FVCU) - `waft.pantheon.guide.TheGuide`

## Current State

### ✅ Completed

1. **FULL 3-Body Decision Loop** (NEW - Jan 20, 2026)
   - `_consult_oracle()` now chains: Oracle → LLM Brain → Guide
   - **Mind (Oracle)**: Epistemic assessment - understands WHAT to fix
   - **Body (LLM Brain)**: Code generation - determines HOW to fix
   - **Spirit (Guide)**: FVCU evaluation - decides IF we SHOULD apply
   - Graceful fallback to `DEFAULT_THINK_CODE` when LLM unavailable

2. **FVCU Evaluation System** (NEW)
   - `_evaluate_with_guide()` method implements FVCU scoring for code patches
   - **F**actuality: Does the code address the described bug?
   - **V**alidity: Is the code syntactically correct? (uses `compile()`)
   - **C**oherence: Does the code preserve existing functionality?
   - **U**tility: Does the code fix the identified fracture?
   - **Fa**ithfulness: No hidden behavior? (checks for eval/exec/imports)
   - Threshold: `overall >= 0.7` to approve patch

3. **LLM Brain Integration** (NEW)
   - `_generate_code_with_llm()` method calls `mirage_experiment/llm_brain.py`
   - Auto-detects available LLM (Anthropic, OpenAI, Gemini)
   - Handles diff parsing and code extraction
   - Graceful fallback if `litellm` not installed

4. **Homebase Dashboard** (Console Goblin)
   - **Location**: `narcissus_lab/internal_monologue/theguide_hello.py`
   - **Static HTML**: `narcissus_lab/internal_monologue/guide_dashboard.html`
   - **Server**: `http://localhost:8008` (HOMEBASE)
   - **Features**:
     - 🧙 Console Goblin reactive logging (SSE, no polling)
     - Dark mode Pantheon aesthetic
     - Live 3-Body orbital animation (Mind/Body/Spirit)
     - FVCU Analysis panel with live updates
     - **Fully responsive** (desktop, tablet, mobile)

5. **Browser Testing with Playwright** (NEW)
   - **Test Script**: `test_browser.py`
   - **Pytest Suite**: `tests/test_homebase.py`
   - **Screenshots**: `screenshots/`
   - **Start Script**: `./start.sh` (server) or `./start.sh --test` (with tests)

5. **Main Trunk Unification** (Previous Work)
   - Symlinked `_unified/` directory with `empirica`, `NovaSystem-Codex`, `_pyrite`
   - `EmpiricaManager` and `TheOracle` integrated
   - Work effort: `WE-260120-p7ic_protocol_main_trunk_unification`

### 📁 Key Files

```
narcissus_lab/internal_monologue/
├── start.sh                       # 🏠 Homebase launcher (./start.sh or ./start.sh --test)
├── theguide_hello.py              # Web server with Console Goblin (port 8008)
├── guide_dashboard.html           # Static HTML dashboard
├── test_browser.py                # Playwright browser tests
├── tests/
│   └── test_homebase.py           # Pytest browser test suite
├── screenshots/                   # Test screenshots
├── src/agents/narcissus.py        # NarcissusAgent with FULL 3-Body integration
├── iterate_the_guide.py           # Self-iterative push protocol script
├── test_oracle_wiring.py          # Test script for Oracle integration
└── README_3BODY.md                # Architecture documentation

mirage_experiment/
└── llm_brain.py                   # LLM code generation (used by Body layer)
```

### 🔧 Technical Details

**3-Body Decision Flow:**
```
Fracture Detected
       ↓
🧠 TheOracle.provide_guidance() → Epistemic context
       ↓
🤖 _generate_code_with_llm() → Code diff/patch
       ↓
✨ _evaluate_with_guide() → FVCU scores
       ↓
   FVCU >= 0.7? → Apply patch
       ↓
   Else: Retry (up to 3x) or fallback
```

**New Methods in NarcissusAgent:**
```python
# Code generation with LLM Brain
def _generate_code_with_llm(self, source_code, oracle_guidance, max_retries=2) -> dict

# FVCU evaluation with TheGuide
def _evaluate_with_guide(self, proposed_code, original_code, oracle_guidance, fvcu_threshold=0.7) -> dict

# Helper for diff application
def _apply_diff_to_code(self, original, diff) -> str

# Optional LLM-based FVCU (if Guide has LLM configured)
def _guide_llm_evaluate(self, proposed_code, original_code, oracle_guidance) -> dict | None
```

**Server Configuration:**
- Port: `7072`
- Serves static `guide_dashboard.html` if exists, falls back to embedded template
- Auto-opens browser on start

### ⚠️ Current Limitations

1. **LLM Availability**:
   - Requires `litellm` package and API key (ANTHROPIC_API_KEY, OPENAI_API_KEY, or GEMINI_API_KEY)
   - Falls back to `DEFAULT_THINK_CODE` if unavailable
   - **To enable**: `pip install litellm` + set API key

2. **Empirica API**:
   - Oracle returns `UNKNOWN` phase when Empirica API not fully configured
   - Core functionality works without it

3. **Dashboard Data**:
   - Currently shows mock/static data
   - **Next Step**: Connect to real FVCU scores from decisions

## Next Steps (Suggested)

1. **Install LLM Dependencies** (Quick Win)
   ```bash
   pip install litellm
   export ANTHROPIC_API_KEY=your-key  # or OPENAI_API_KEY
   ```

2. **Real-time Dashboard Data**
   - Connect dashboard to live FVCU scores from `_evaluate_with_guide()`
   - Stream actual agent status and fracture detection
   - Show Oracle epistemic phase

3. **WebSocket Integration**
   - Real-time updates without page refresh
   - Live log streaming from 3-Body loop
   - Interactive console for querying TheOracle

4. **Enhanced Guide LLM Evaluation**
   - Configure TheGuide with its own LLM for sophisticated FVCU
   - Hybrid scoring (60% LLM + 40% heuristic)

## Quick Start Commands

```bash
# === HOMEBASE (localhost:8008) ===
cd narcissus_lab/internal_monologue

# Start homebase server
./start.sh
# OR: uv run python theguide_hello.py

# Run browser tests (starts server, runs Playwright tests, stops server)
./start.sh --test
# OR: uv run python test_browser.py

# Interactive browser session (opens Chrome)
uv run python test_browser.py --interactive

# === 3-Body Architecture Tests ===

# Test component initialization
uv run python -c "
from src.agents.narcissus import NarcissusAgent, LLM_BRAIN_AVAILABLE
from pathlib import Path
agent = NarcissusAgent(Path('../../'))
print(f'🧠 Oracle: {agent.oracle is not None}')
print(f'🤖 LLM Brain: {LLM_BRAIN_AVAILABLE}')
print(f'✨ Guide: {agent.guide is not None}')
"

# Test fracture detection and repair
uv run python -c "
from src.agents.narcissus import NarcissusAgent, FRACTURE_MARKER
from pathlib import Path
agent = NarcissusAgent(Path('../../'))
source = agent.inspect_my_source()
fractured = source.replace('if not', f'# {FRACTURE_MARKER}\nif not')
result = agent._think(fractured)
print(f'Action: {result[\"action\"]}, Note: {result[\"note\"]}')
"

# Run pytest suite (requires server running)
uv run pytest tests/ -v
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    NarcissusAgent                           │
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  🧠 TheOracle   │  │  🤖 LLM Brain   │  │ ✨ TheGuide │ │
│  │     (Mind)      │  │    (Body)       │  │   (Spirit)  │ │
│  │                 │  │                 │  │             │ │
│  │ - Epistemic     │→│ - Code Gen      │→│ - FVCU      │ │
│  │   reasoning     │  │ - Diff parse    │  │   scoring   │ │
│  │ - provide_      │  │ - generate_fix  │  │ - Approval  │ │
│  │   guidance()    │  │                 │  │   gate      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
│           │                    │                   │        │
│           └────────────────────┴───────────────────┘        │
│                            ↓                                │
│               _consult_oracle() chains all 3                │
│                            ↓                                │
│              ┌──────────────────────────┐                   │
│              │  FVCU >= 0.7?            │                   │
│              │  ✅ Apply patch          │                   │
│              │  ❌ Retry or fallback    │                   │
│              └──────────────────────────┘                   │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Web Dashboard (localhost:7072)                             │
│  - 3-Body visualization                                     │
│  - FVCU metrics (F, V, C, U, Fa)                           │
│  - Agent status logs                                        │
└─────────────────────────────────────────────────────────────┘
```

## Important Notes

- **Server Status**: Check if server is running with `ps aux | grep theguide_hello.py`
- **File Locations**: All paths relative to `waft/` root
- **Dependencies**: Requires `uv` environment with `empirica` and `waft` packages
- **LLM Support**: Optional `litellm` + API key for full code generation
- **Git Status**: Changes made to `narcissus.py` (3-Body integration complete)

---

**Status**: ✅ FULL 3-Body Decision Loop operational (Oracle → LLM → Guide)
**Ready for**: LLM API key setup, real-time dashboard data, WebSocket streaming
