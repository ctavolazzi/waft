# Oracle

**Consult TheOracle for epistemic insights and guidance.**

This is the source-of-truth command spec for Oracle behavior.

---

## Purpose

Provides epistemic intelligence from WAFT's Empirica brain realm:
- CASCADE-aware guidance
- CHECK gate decision support
- Knowledge/unknown tracking
- Brain realm transport visibility (`mcp -> cli -> degraded`)

---

## Usage

### Basic Consultation

```
/oracle
```

### Specific Question

```
/oracle "How should we proceed with FlightRecorder integration?"
```

### Decision Assessment

```
/oracle assess "Implement FlightRecorderEpistemicAdapter"
```

---

## Runtime Integration

TheOracle now integrates with:
- **Empirica**: Epistemic state, findings/unknowns, CASCADE submissions
- **ThePonderingOne**: Brain realm governance and transport posture
- **MCP-first Policy**: Prefer `empirica-mcp`, fallback to CLI, then degraded mode

---

## What Oracle Outputs

1. **Epistemic State**: Knowledge, uncertainty, engagement and phase
2. **Decision Assessment**: `PROCEED | INVESTIGATE | HALT | BRANCH | REVISE`
3. **Guidance**: Recommendation grounded in current epistemic state
4. **Brain Realm Status**: Active transport + fallback reason (if any)
5. **Learning Signal**: Preflight/check/postflight deltas from consultation cycle

---

## Drift Prevention

- `/consult-the-oracle` is an alias and should remain lightweight.
- If this file changes, update alias docs and run:

```bash
python3 scripts/verify_oracle_command_docs.py
```

