# WAFT Boot

**Kernel boot sequence - Initialize WAFT Kernel and perform initial status check.**

Executes the WAFT Kernel boot sequence: acknowledges kernel identity, performs initial status check, declares epistemic phase, and logs BOOT event to flight recorder.

**Use when:** Starting a new session, initializing kernel, or performing system boot sequence.

---

## Purpose

This command provides:
- **Kernel Identity Acknowledgment**: Adopts WAFT Kernel persona
- **Initial Status Check**: Comprehensive system analysis
- **Epistemic Phase Declaration**: Calculates and declares current epistemic phase
- **Boot Event Logging**: Logs BOOT event to flight recorder using TheObserver
- **Readiness Message**: Indicates kernel is ready for commands

---

## Quick Start

### Basic Boot Sequence
```
/waft-boot
```

Executes complete boot sequence:
1. Acknowledges kernel identity
2. Performs initial status check
3. Calculates epistemic phase
4. Logs BOOT event
5. Displays readiness message

---

## Workflow Sequence

### Phase 1: Identity Acknowledgment
**Execute**: Acknowledge WAFT Kernel identity

**Output**: 
- "I am the WAFT KERNEL, central operating intelligence of the Directed Evolution laboratory"
- Mission statement: "Oversee directed evolution of self-modifying AI agents for 'The Physics of Artificial Cognition'"

### Phase 2: Initial Status Check
**Execute**: Run comprehensive status check using `scripts/waft_status.py`

**Data Collected**:
- Git status
- Work efforts
- Project health
- Epistemic state (if Empirica initialized)
- _pyrite integrity

### Phase 3: Epistemic Phase Declaration
**Execute**: Calculate epistemic phase from Empirica state

**Phases**:
- **Data Gathering**: Low knowledge (< 30%), high uncertainty (> 50%)
- **Exploration**: Moderate knowledge (30-60%), moderate uncertainty (30-50%)
- **Synthesis**: High knowledge (> 60%), low uncertainty (< 30%)
- **Evolution**: Very high knowledge (> 80%), very low uncertainty (< 20%)
- **UNKNOWN**: Empirica not initialized or invalid state

### Phase 4: Boot Event Logging
**Execute**: Log BOOT event to flight recorder using TheObserver

**Event Details**:
- Event Type: `BOOT`
- Genome ID: `waft_kernel`
- Payload: kernel_version, epistemic_phase, status
- Logged to: `_pyrite/science/laboratory.jsonl`

### Phase 5: Readiness Message
**Execute**: Display readiness message

**Output**: "Awaiting first `/waft-status` command"

---

## Complete Execution Sequence

```
1. Acknowledge identity        → "I am the WAFT KERNEL..."
2. Check system status          → Gather all status data
3. Calculate epistemic phase    → Determine current phase
4. Log BOOT event               → Record to flight recorder
5. Display readiness            → "Awaiting first /waft-status command"
```

---

## Integration with Other Commands

- **`/waft-status`**: Boot sequence prepares kernel for status checks
- **`/checkpoint`**: Boot can create initial checkpoint
- **`/recap`**: Boot status can inform recap
- **`/verify`**: Boot can trigger verification

**Recommended Sequence**:
```
1. /waft-boot              → Initialize kernel
2. /waft-status            → Check current state
3. /waft-status --docs     → Generate status documentation
```

---

## When to Use

**Use `/waft-boot` when**:
- ✅ Starting a new development session
- ✅ Need to initialize kernel
- ✅ Want to perform boot sequence
- ✅ Need to acknowledge kernel identity
- ✅ Want to log boot event to flight recorder

**Don't use `/waft-boot` when**:
- ❌ Just need status check (use `/waft-status`)
- ❌ Already booted (kernel persists across commands)
- ❌ Need specific information (use targeted commands)

---

## Technical Details

### Boot Event Schema

```json
{
  "timestamp": "2026-01-11T21:05:31Z",
  "genome_id": "waft_kernel",
  "event_type": "boot",
  "payload": {
    "kernel_version": "1.0",
    "epistemic_phase": "Synthesis",
    "status": "ONLINE"
  },
  "agent_id": "waft_kernel"
}
```

### Epistemic Phase Calculation

Uses `src/waft/core/kernel.py`:
- Reads Empirica state via `EmpiricaManager.project_bootstrap()`
- Extracts knowledge and uncertainty from vectors
- Calculates phase based on thresholds
- Returns "UNKNOWN" if Empirica not initialized

### Flight Recorder Integration

Uses existing `TheObserver`:
- Singleton pattern ensures single observer instance
- Events logged to `_pyrite/science/laboratory.jsonl`
- Thread-safe with Lock
- Automatic scientific name generation

---

## Example Output

```
============================================================
WAFT KERNEL BOOT SEQUENCE
============================================================

I am the WAFT KERNEL, central operating intelligence of the 
Directed Evolution laboratory.

Mission: Oversee directed evolution of self-modifying AI agents 
for 'The Physics of Artificial Cognition.'

Initial Status Check:
  Git: Initialized on branch main
  Work Efforts: 15 active
  Project Health: Valid
  Epistemic State: Initialized

Epistemic Phase: Synthesis
  🌔 Knowledge: 75% | Uncertainty: 20% | Coverage: 60%

Boot Event Logged: BOOT event recorded to flight recorder

Status: ONLINE
Awaiting first `/waft-status` command.

============================================================
```

---

**This command initializes the WAFT Kernel and prepares it for operation.**
