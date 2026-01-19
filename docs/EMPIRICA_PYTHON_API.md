# Empirica Python API Integration

WAFT now uses the **Empirica Python API** when available, providing direct programmatic access to Empirica's core modules with better performance and advanced features.

## Overview

The Empirica Python API provides:
- **Direct database access** (no subprocess overhead)
- **13-vector epistemic assessment** via `EpistemicAssessor`
- **Atomic logging** via `GitEnhancedReflexLogger`
- **AI-to-AI continuity** via `HandoffGenerator`
- **Bayesian belief tracking** for real-time updates
- **Project management** with goal aggregation

## Architecture

```
EmpiricaManager
├── EmpiricaAPIManager (Python API - preferred)
│   ├── SessionDatabase
│   ├── EpistemicAssessor
│   ├── ProjectManager
│   ├── GitEnhancedReflexLogger
│   └── HandoffGenerator
└── CLI Fallback (subprocess calls)
```

## Usage

### Automatic Detection

`EmpiricaManager` automatically:
1. **Tries Python API first** - If `empirica` package is available
2. **Falls back to CLI** - If API not available or initialization fails
3. **Transparent interface** - Same methods work with both

### Check API Availability

```python
from waft.core.empirica import EmpiricaManager

empirica = EmpiricaManager(project_path)

if empirica.api_available:
    print("Using Python API (fast, typed, advanced features)")
    api = empirica.api_manager
    # Access advanced features:
    # - api.assessor.assess_vectors()
    # - api.logger.add_checkpoint()
    # - api.handoff.create_handoff()
else:
    print("Using CLI (slower, but works)")
```

## Available Modules

### SessionDatabase
**Direct SQLite access for session management.**

```python
# Create session
session_id = api.db.create_session(
    ai_id="waft",
    bootstrap_level=2,
    subject="development"
)

# Get session
session = api.db.get_session(session_id)

# Bootstrap breadcrumbs (findings, unknowns, dead ends)
breadcrumbs = api.db.bootstrap_project_breadcrumbs(session_id)
```

### EpistemicAssessor
**13-vector epistemic assessment with Bayesian updates.**

```python
# Assess vectors
assessment = api.assessor.assess_vectors(
    session_id=session_id,
    vectors={
        "engagement": 0.8,
        "foundation": {"know": 0.6, "do": 0.7},
        "uncertainty": 0.4
    },
    reasoning="Starting new feature"
)

# Update beliefs
updated = api.assessor.update_beliefs(
    session_id=session_id,
    evidence={"finding": "Discovered pattern X", "impact": 0.7}
)
```

### GitEnhancedReflexLogger
**Atomic 3-layer logging (SQLite + Git Notes + JSON).**

```python
# Log checkpoint
api.logger.add_checkpoint(
    session_id=session_id,
    phase="PREFLIGHT",
    data={"vectors": {...}, "reasoning": "..."}
)

# Get checkpoints
checkpoints = api.logger.get_checkpoints(session_id)
```

### HandoffGenerator
**AI-to-AI continuity with 98% token reduction.**

```python
# Create handoff
handoff = api.handoff.create_handoff(
    session_id=session_id,
    target_ai_id="other-ai"
)

# Load handoff
context = api.handoff.load_handoff(handoff)
```

### ProjectManager
**Multi-session project tracking.**

```python
# Get project summary
summary = api.project_manager.get_project_summary(project_id)

# Track progress across sessions
progress = api.project_manager.track_progress(project_id)
```

## Benefits

### Performance
- **No subprocess overhead** - Direct function calls
- **Faster queries** - Direct SQLite access
- **Reduced latency** - No JSON serialization/parsing

### Features
- **13-vector assessment** - Full epistemic vector math
- **Bayesian updates** - Real-time belief tracking
- **Atomic logging** - Triple-layer storage guarantee
- **Handoff support** - AI-to-AI continuity
- **Type safety** - Typed Python API

### Reliability
- **Transactional integrity** - Database guarantees
- **Git integration** - Atomic git notes
- **Error handling** - Better exception information

## TheOracle Integration

TheOracle automatically uses the Python API when available:

```python
oracle = TheOracle(project_path)

# Preflight uses EpistemicAssessor if available
preflight = oracle._empirica_preflight(question)
# → Uses api.assessor.assess_vectors() if API available
# → Falls back to CLI otherwise

# Check API availability
if oracle.empirica.api_available:
    # Access advanced features
    assessment = oracle.empirica.api_manager.assess_vectors(...)
```

## Installation

The Python API is included with the `empirica` package:

```bash
pip install empirica>=1.2.3
```

WAFT already includes `empirica>=1.2.3` in `pyproject.toml`, so the API should be available if Empirica is installed.

## Fallback Behavior

If the Python API is not available:
- ✅ **CLI fallback** - All operations use CLI commands
- ✅ **Same interface** - No code changes needed
- ✅ **Graceful degradation** - Works with or without API

## See Also

- [Empirica Python API Documentation](https://empirica.ai/docs/python-api)
- [Oracle Empirica Workflow](ORACLE_EMPIRICA_WORKFLOW.md)
- [Empirica Integration](../_work_efforts/EMPIRICA_INTEGRATION.md)
