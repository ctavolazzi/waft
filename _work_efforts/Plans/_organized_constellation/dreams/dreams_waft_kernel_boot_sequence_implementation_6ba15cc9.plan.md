---
name: WAFT Kernel Boot Sequence Implementation
overview: Implement the WAFT Kernel boot sequence that acknowledges identity, performs initial status check, declares epistemic phase, and integrates with the existing `/waft-status` command system. The kernel acts as the central operating intelligence for the directed evolution laboratory.
todos:
  - id: kernel-identity
    content: Adopt WAFT Kernel identity in conversation and acknowledge boot sequence
    status: pending
  - id: boot-command
    content: Create `.cursor/commands/waft-boot.md` command handler for boot sequence
    status: pending
  - id: epistemic-calculator
    content: Implement epistemic phase calculator in `src/waft/core/kernel.py`
    status: pending
  - id: extend-event-types
    content: Extend `EvolutionaryEventType` enum with BOOT and STATUS_CHECK in `src/waft/core/agent/state.py`
    status: pending
  - id: kernel-event-logging
    content: Use existing `TheObserver` to log kernel events (BOOT, STATUS_CHECK)
    status: pending
  - id: enhance-status
    content: Enhance `scripts/waft_status.py` with kernel-aware reporting and epistemic state
    status: pending
  - id: update-status-command
    content: Update `.cursor/commands/waft-status.md` with kernel status section
    status: pending

category: dreams
confidence: 0.52
constellation_date: 2026-01-14
---

# WAFT Kernel Boot Sequence Implementation Plan (REVISED)

**Revision Date**: 2026-01-11

**Based On**: Critique and Codebase Audit

## Overview

The WAFT Kernel is the central operating intelligence that oversees directed evolution of self-modifying AI agents. This plan implements the boot sequence that acknowledges kernel identity, performs self-awareness checks, and integrates with the existing status system.

**CRITICAL CHANGES FROM ORIGINAL PLAN**:

- ✅ Uses existing `TheObserver` instead of creating new flight recorder
- ✅ Extends existing `EvolutionaryEventType` enum instead of creating parallel system
- ✅ Integrates with existing `EmpiricaManager` for epistemic state
- ✅ Enhances existing `waft_status.py` instead of replacing it
- ✅ Adds comprehensive error handling and path validation
- ✅ Removes unnecessary abstractions

## Architecture

### Core Components

1. **Kernel Identity Handler** - Adopts WAFT Kernel persona in conversation (conversational only)
2. **Boot Sequence Executor** - Performs initial status check and phase declaration
3. **Status Check Integration** - Enhances existing `scripts/waft_status.py` with kernel-aware reporting and Empirica integration
4. **Epistemic Phase Calculator** - Determines phase from Empirica state (simple function, not separate module)
5. **Kernel Event Logging** - Uses existing `TheObserver` to log kernel events (BOOT, STATUS_CHECK)

## Implementation Details

### 1. Kernel Identity Acknowledgment

**Location**: Conversation-level (immediate adoption)

**Behavior**:

- Acknowledge identity as WAFT Kernel upon boot sequence command
- Adopt kernel persona: "I am the WAFT KERNEL, central operating intelligence of the Directed Evolution laboratory"
- Reference mission: "Oversee directed evolution of self-modifying AI agents for 'The Physics of Artificial Cognition'"

**Files**: No code changes needed - this is conversational identity

### 2. Boot Sequence Executor

**Location**: `.cursor/commands/waft-boot.md` (new command)

**Functionality**:

- Execute initial status check using existing `scripts/waft_status.py`
- Calculate epistemic phase from Empirica state
- Display kernel boot message with:
  - Identity acknowledgment
  - Initial status summary
  - Epistemic phase declaration
  - Readiness message

**Integration Points**:

- Calls `scripts/waft_status.py` for status data
- Uses `src/waft/core/empirica.py` for epistemic state
- References `_pyrite/` structure for memory state

### 3. Enhanced Status Check

**Location**: `scripts/waft_status.py` (enhance existing)

**Enhancements**:

- Add kernel-aware status reporting
- Integrate Empirica for epistemic state (moon phase, knowledge %, uncertainty %)
- Add gamification state (character level, integrity score) if available
- Reference `_pyrite/` structure integrity
- Check for Genesis files (20.00_state.json, 35.00_ledger.json, 42.00_kernel.md) - handle missing gracefully
- Add comprehensive error handling and path validation

**New Functions** (with error handling):

```python
def validate_path(path: Path, project_root: Path) -> bool:
    """Validate path is within project root (prevent path traversal)."""
    try:
        resolved = path.resolve()
        root_resolved = project_root.resolve()
        return str(resolved).startswith(str(root_resolved))
    except Exception:
        return False

def get_epistemic_state(project_path: Path) -> Dict[str, Any]:
    """Get epistemic state from Empirica if initialized."""
    try:
        from waft.core.empirica import EmpiricaManager
        from waft.core.kernel import calculate_epistemic_phase

        empirica = EmpiricaManager(project_path)
        if not empirica.is_initialized():
            return {"initialized": False}

        context = empirica.project_bootstrap()
        if not context:
            return {"initialized": True, "state": None}

        epistemic_state = context.get("epistemic_state", {})
        vectors = epistemic_state.get("vectors", {})
        foundation = vectors.get("foundation", {})
        know = foundation.get("know", 0.0) if foundation else 0.0
        uncertainty = vectors.get("uncertainty", 1.0)
        coverage = know * (1.0 - uncertainty) if know > 0 else 0.0

        phase = calculate_epistemic_phase(empirica)

        return {
            "initialized": True,
            "know": know,
            "uncertainty": uncertainty,
            "coverage": coverage,
            "phase": phase,
            "moon_phase": get_moon_phase(coverage)  # From existing code
        }
    except Exception as e:
        return {"initialized": False, "error": str(e)}

def check_pyrite_integrity(project_path: Path) -> Dict[str, Any]:
    """Check _pyrite structure and Genesis files (handle missing gracefully)."""
    try:
        pyrite_dir = project_path / "_pyrite"
        if not pyrite_dir.exists():
            return {"exists": False}

        # Validate path
        if not validate_path(pyrite_dir, project_path):
            return {"exists": False, "error": "Invalid path"}

        integrity = {
            "exists": True,
            "structure_valid": False,
            "genesis_files": {}
        }

        # Check structure
        required_dirs = ["active", "backlog", "standards", "gym_logs"]
        integrity["structure_valid"] = all(
            (pyrite_dir / d).exists() and (pyrite_dir / d).is_dir()
            for d in required_dirs
        )

        # Check Genesis files (may not exist yet - that's OK)
        genesis_files = {
            "state": "20.00_state.json",
            "ledger": "35.00_pyrite_ledger.json",
            "kernel": "42.00_internal_kernel.md"
        }

        for key, filename in genesis_files.items():
            file_path = pyrite_dir / filename
            integrity["genesis_files"][key] = {
                "exists": file_path.exists() and validate_path(file_path, project_path),
                "path": str(file_path.relative_to(project_path)) if file_path.exists() else None
            }

        return integrity
    except Exception as e:
        return {"exists": False, "error": str(e)}
```

### 4. Epistemic Phase Calculator

**Location**: `src/waft/core/kernel.py` (new module - simple utility functions)

**Functionality**:

- Calculate epistemic phase from Empirica vectors
- Phases:
  - **Data Gathering**: Low knowledge (< 30%), high uncertainty (> 50%)
  - **Exploration**: Moderate knowledge (30-60%), moderate uncertainty (30-50%)
  - **Synthesis**: High knowledge (> 60%), low uncertainty (< 30%)
  - **Evolution**: Very high knowledge (> 80%), very low uncertainty (< 20%)

**Implementation** (with error handling):

```python
from waft.core.empirica import EmpiricaManager
from pathlib import Path
from typing import Optional

def calculate_epistemic_phase(empirica_manager: EmpiricaManager) -> str:
    """
    Calculate current epistemic phase from Empirica state.

    Returns "UNKNOWN" if Empirica not initialized or data invalid.
    """
    try:
        if not empirica_manager.is_initialized():
            return "UNKNOWN"

        context = empirica_manager.project_bootstrap()
        if not context:
            return "UNKNOWN"

        epistemic_state = context.get("epistemic_state", {})
        if not epistemic_state:
            return "UNKNOWN"

        vectors = epistemic_state.get("vectors", {})
        if not vectors:
            return "UNKNOWN"

        foundation = vectors.get("foundation", {})
        know = foundation.get("know", 0.0) if foundation else 0.0
        uncertainty = vectors.get("uncertainty", 1.0)

        # Validate ranges
        know = max(0.0, min(1.0, know))
        uncertainty = max(0.0, min(1.0, uncertainty))

        if know < 0.3 and uncertainty > 0.5:
            return "Data Gathering"
        elif know < 0.6 and uncertainty > 0.3:
            return "Exploration"
        elif know > 0.6 and uncertainty < 0.3:
            return "Synthesis"
        elif know > 0.8 and uncertainty < 0.2:
            return "Evolution"
        else:
            return "Transition"
    except Exception:
        # Log error but don't crash
        return "UNKNOWN"
```

### 5. Kernel Event Logging (Using Existing TheObserver)

**Location**: Uses existing `src/waft/core/science/observer.py` (TheObserver)

**Functionality**:

- Log kernel events using existing `TheObserver.observe_event()`
- Extend `EvolutionaryEventType` enum with BOOT and STATUS_CHECK
- Events logged to `_pyrite/science/laboratory.jsonl` (existing infrastructure)

**Implementation**:

```python
# Extend EvolutionaryEventType enum in src/waft/core/agent/state.py
class EvolutionaryEventType(str, Enum):
    SPAWN = "spawn"
    MUTATE = "mutate"
    GYM_EVAL = "gym_eval"
    DEATH = "death"
    SURVIVAL = "survival"
    SESSION_END = "session_end"
    BOOT = "boot"  # NEW: Kernel boot event
    STATUS_CHECK = "status_check"  # NEW: Status check event

# Use existing TheObserver
from waft.core.science.observer import TheObserver
from waft.core.agent.state import EvolutionaryEvent, EvolutionaryEventType

observer = TheObserver(project_path)
event = EvolutionaryEvent(
    timestamp=datetime.utcnow(),
    genome_id="waft_kernel",
    event_type=EvolutionaryEventType.BOOT,
    payload={
        "kernel_version": "1.0",
        "epistemic_phase": "Synthesis",
        "status": "ONLINE"
    },
    agent_id="waft_kernel"
)
observer.observe_event(event)
```

**Security**: Uses existing path validation and error handling from TheObserver

### 6. `/waft-status` Command Enhancement

**Location**: `.cursor/commands/waft-status.md` (update existing)

**Enhancements**:

- Add kernel identity acknowledgment in status output
- Include epistemic phase in status summary
- Reference kernel mission in documentation
- Add "Kernel Status" section showing:
  - Boot time
  - Epistemic phase
  - Active generation
  - Fitness landscape summary

## File Changes

### New Files

1. `.cursor/commands/waft-boot.md` - Boot sequence command (OR add `--boot` flag to waft-status)
2. `src/waft/core/kernel.py` - Kernel utilities (epistemic phase calculation, simple functions)

### Modified Files

1. `src/waft/core/agent/state.py` - Extend `EvolutionaryEventType` enum with BOOT and STATUS_CHECK
2. `scripts/waft_status.py` - Add kernel-aware status reporting, Empirica integration, error handling, path validation
3. `.cursor/commands/waft-status.md` - Add kernel status section

### NOT Creating (Using Existing)

- ❌ `src/waft/core/flight_recorder.py` - Use existing `TheObserver` instead
- ❌ New event system - Extend existing `EvolutionaryEventType` instead

## Integration Points

### Empirica Integration (EXISTING)

- ✅ Use existing `EmpiricaManager.project_bootstrap()` for epistemic state
- ✅ Calculate moon phase from coverage (know × (1 - uncertainty)) - function exists
- ✅ Extract knowledge % and uncertainty % from vectors
- ⚠️ Add error handling for missing/invalid Empirica state

### TheObserver Integration (EXISTING)

- ✅ Use existing `TheObserver.observe_event()` for kernel events
- ✅ Extend existing `EvolutionaryEventType` enum (don't create new system)
- ✅ Events automatically logged to `_pyrite/science/laboratory.jsonl`
- ⚠️ Add BOOT and STATUS_CHECK event types to enum

### _pyrite Integration

- Check for Genesis files existence (handle missing gracefully - may not exist yet)
- Validate structure (active/, backlog/, standards/, gym_logs/)
- ⚠️ Add path validation to prevent traversal attacks
- Read state files if available (with error handling)

### Work Efforts Integration

- Count active work efforts (existing functionality)
- ⚠️ Add path validation for work effort directory names
- Identify evolutionary work (agent breeding, mutation tracking)
- Reference work effort tickets as potential quests

## Execution Flow

### Boot Sequence

1. **Identity Acknowledgment**: "I am the WAFT KERNEL..." (conversational only)
2. **Status Check**: Execute comprehensive system analysis (with error handling)
3. **Epistemic Phase**: Calculate and declare current phase (handle UNKNOWN gracefully)
4. **Flight Recorder**: Log BOOT event using existing `TheObserver.observe_event()`
5. **Readiness**: "Awaiting first `/waft-status` command"

### Status Check Flow

1. Validate project path (prevent traversal attacks)
2. Gather git status, work efforts, project health (with error handling)
3. Calculate epistemic state from Empirica (handle missing/invalid gracefully)
4. Check _pyrite integrity (handle missing files gracefully)
5. Get gamification state (if available, handle missing gracefully)
6. Log STATUS_CHECK event using existing `TheObserver`
7. Display kernel-aware status summary
8. [Optional] Generate documentation at requested level

## Testing Strategy

### Unit Tests

- Test epistemic phase calculation with various Empirica states
- Test path validation (prevent traversal attacks)
- Test error handling for missing Empirica, _pyrite, etc.
- Test _pyrite integrity checks (with missing files)
- Test event logging using TheObserver

### Integration Tests

- Test boot sequence with Empirica initialized
- Test boot sequence without Empirica (graceful degradation)
- Test status check with all components available
- Test status check with missing components (error handling)
- Test concurrent status checks (thread safety)
- Test with corrupted _pyrite structure

### Security Tests

- Test path traversal prevention
- Test subprocess injection prevention
- Test file permission handling
- Test input validation

## Success Criteria

1. ✅ Kernel identity acknowledged in conversation
2. ✅ Boot sequence executes and displays status (with error handling)
3. ✅ Epistemic phase calculated from Empirica state (handles UNKNOWN gracefully)
4. ✅ Flight recorder logs BOOT event using existing TheObserver
5. ✅ `/waft-status` includes kernel-aware information and Empirica state
6. ✅ Documentation generation includes kernel context
7. ✅ All paths validated (no traversal attacks)
8. ✅ All errors handled gracefully (no crashes)
9. ✅ Uses existing infrastructure (TheObserver, EmpiricaManager)
10. ✅ Tests pass (unit, integration, security)

## Next Steps (Revised)

1. ✅ Extend `EvolutionaryEventType` enum with BOOT and STATUS_CHECK
2. ✅ Create `src/waft/core/kernel.py` with epistemic phase calculator (simple functions)
3. ✅ Enhance `scripts/waft_status.py`:

   - Add Empirica integration
   - Add path validation
   - Add error handling
   - Add kernel status section

4. ✅ Use existing `TheObserver` for kernel event logging
5. ✅ Create boot command handler (or add `--boot` flag)
6. ✅ Add comprehensive tests (unit, integration, security)
7. ✅ Update documentation

## Security Checklist

- [ ] All file paths validated (prevent traversal)
- [ ] All subprocess calls validated (prevent injection)
- [ ] All inputs validated (prevent invalid data)
- [ ] All errors handled gracefully (no crashes)
- [ ] File permissions set correctly (0700 for .waft/)
- [ ] No sensitive data logged (secrets, PII)

## Critical Fixes from Critique

1. ✅ Use existing TheObserver instead of creating new flight recorder
2. ✅ Extend EvolutionaryEventType instead of creating parallel system
3. ✅ Add comprehensive error handling
4. ✅ Add path validation (prevent traversal attacks)
5. ✅ Integrate with existing EmpiricaManager
6. ✅ Handle missing components gracefully