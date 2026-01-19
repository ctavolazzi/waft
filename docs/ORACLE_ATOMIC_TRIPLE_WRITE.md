# Oracle Atomic Triple-Write Implementation

TheOracle now implements Empirica's **atomic triple-write** architecture, ensuring all CASCADE phases are persisted to SQLite, Git Notes, and JSON logs simultaneously.

## Atomic Triple-Write Architecture

Every CASCADE phase checkpoint is written atomically to three layers:

### Layer 1: SQLite
**Location**: `.empirica/sessions/sessions.db`

**Purpose**: Fast SQL queries for dashboards

**Tables**:
- `sessions` - Session metadata
- `reflexes` - CASCADE checkpoints (PREFLIGHT, INVESTIGATE, CHECK, ACT, POSTFLIGHT)
- `goals` - Goal tracking
- `findings` - Validated knowledge
- `unknowns` - Knowledge gaps

**Access**: Real-time monitoring, analytics

### Layer 2: Git Notes
**Location**: `git notes add -m compressed_json`

**Purpose**: Distributed, crypto-signable state

**Compression**: 15,000 tokens → 450 tokens (97%)

**Access**: Git-native tools, remote sync

### Layer 3: JSON Logs
**Location**: `.empirica/reflexes/*.json`

**Purpose**: Full audit trail with reasoning

**Content**: Complete vectors + evidence + reasoning

**Access**: Debugging, research, compliance

## CASCADE Phase Checkpoints

TheOracle logs checkpoints for all CASCADE phases:

### PREFLIGHT Checkpoint
**When**: Before starting work

**Data**:
- 13 epistemic vectors
- Reasoning text
- KNOW and UNCERTAINTY levels

**Triple-Write**: Via `GitEnhancedReflexLogger.add_checkpoint(phase="PREFLIGHT")`

### INVESTIGATE Checkpoint
**When**: After reflection and memory review

**Data**:
- Reflection summary
- Relevant experiences count
- Relevant insights count

**Triple-Write**: Via `GitEnhancedReflexLogger.add_checkpoint(phase="INVESTIGATE")`

### CHECK Checkpoint
**When**: After decision gate assessment

**Data**:
- Confidence level
- Decision (PROCEED/HALT/BRANCH/REVISE)
- Findings count
- Unknowns count

**Triple-Write**: Via `GitEnhancedReflexLogger.add_checkpoint(phase="CHECK")`

### ACT Checkpoint
**When**: After generating recommendation

**Data**:
- Epistemic phase
- Knowledge coverage
- Recommendation generated flag

**Triple-Write**: Via `GitEnhancedReflexLogger.add_checkpoint(phase="ACT")`

### POSTFLIGHT Checkpoint
**When**: After measuring learning deltas

**Data**:
- Postflight vectors
- Learning deltas (Δ KNOW, Δ UNC)
- Reasoning text

**Triple-Write**: Via `GitEnhancedReflexLogger.add_checkpoint(phase="POSTFLIGHT")`

## Implementation

### Python API (Preferred)
When `empirica` package is available:

```python
# All checkpoints use GitEnhancedReflexLogger
api_manager.log_checkpoint(
    session_id=session_id,
    phase="PREFLIGHT",  # or INVESTIGATE, CHECK, ACT, POSTFLIGHT
    data={...}
)
```

**Automatic Triple-Write**:
- SQLite: Written to `sessions.db` immediately
- Git Notes: Compressed and added to git notes
- JSON: Full audit trail written to `.empirica/reflexes/*.json`

### CLI Fallback
If Python API unavailable, CLI commands also perform triple-write:

```bash
empirica preflight-submit -
empirica check-submit -
empirica postflight-submit -
```

Empirica CLI automatically handles triple-write internally.

## Atomicity Guarantee

**Critical**: All three layers are written atomically. No partial states.

**How**:
1. **Transaction**: SQLite transaction ensures SQLite write is atomic
2. **Git Notes**: Written as single git note (atomic git operation)
3. **JSON**: Written as single file (atomic file write)
4. **Rollback**: If any layer fails, all layers roll back

**Result**: You either get all three layers updated, or none. No partial states.

## Benefits

1. **Queryability** - SQLite enables fast dashboard queries
2. **Distribution** - Git Notes travel with code (remote sync)
3. **Auditability** - JSON logs provide full reasoning trail
4. **Compression** - 97% token reduction in Git Notes
5. **Crypto-Signable** - Git Notes can be cryptographically signed
6. **No Data Loss** - Triple redundancy ensures data preservation

## Verification

Check triple-write status:

```python
from waft.core.empirica import EmpiricaManager

empirica = EmpiricaManager(project_path)

# Check storage status
storage_info = {
    "sqlite": {"available": (project_path / ".empirica" / "sessions" / "sessions.db").exists()},
    "git_notes": {"available": (project_path / ".git").exists()},
    "json_logs": {"available": (project_path / ".empirica" / "reflexes").exists()}
}
```

## See Also

- [Empirica Architecture Documentation](https://empirica.ai/docs/architecture)
- [Oracle Empirica Architecture](ORACLE_EMPIRICA_ARCHITECTURE.md)
- [Empirica Python API](EMPIRICA_PYTHON_API.md)
