# Being Lifecycle Attributes and Now Cycle Event Loop - Development Roadmap

**Status**: Planning Complete, Ready for Implementation  
**Work Effort**: [WE-260111-roo0](../WE-260111-roo0_being_lifecycle_attributes_and_now_cycle_event_loop_system/WE-260111-roo0_index.md)  
**Last Updated**: 2026-01-11

---

## Overview

Extend WAFT beings with four new lifecycle attributes and implement a centralized "Now" cycle event loop that synchronizes all beings and system state. This creates a unified temporal framework where all variables are calculated per cycle before beings can make decisions.

**Key Design Decision**: Beings are separate from BaseAgent organisms. The Now cycle coordinates beings across all realities, not agents in PetriDishes.

---

## New Attributes

### 1. Will to Live
- **Type**: `float` (0.0-100.0, death at 0.0)
- **Depletion**: Time-based (-0.1/cycle) + Decision-based (-0.5/decision) + Pain-based (-pain × 10.0)
- **Regeneration**: Pleasure-based (+pleasure × 5.0, capped at 100.0)
- **Death**: Being dies when will_to_live reaches 0.0

### 2. Luck
- **Type**: `float` (0.0-100.0, represents luck range)
- **Relationship to Karma**: Separate but related
  - Base luck: 50.0
  - Karma modifier: `(karma_balance / 1000.0) × 20.0` (max +20.0)
  - Luck range: `base_luck + karma_modifier + random_variance(-10.0 to +10.0)`
- **Usage**: Affects outcomes of decisions, events, and experiences

### 3. Decision Fatigue
- **Type**: `int` (current decisions remaining before sleep)
- **Initial Quota**: Varies per being (base: 10 + personality_modifier + skill_bonus)
- **Depletion**: Decreases by 1 per decision made
- **Sleep Requirement**: When quota reaches 0, being MUST sleep
- **Sleep Duration**: Evolves over time (starts random 3-10 cycles)

### 4. Pleasure and Pain
- **Type**: `float` (pleasure: 0.0-1.0, pain: 0.0-1.0)
- **Calculation**: Based on alignment of personality, goals, and "Now" experience
- **Formula**:
  - Pleasure = `alignment_score × goal_progress × positive_experience_intensity`
  - Pain = `(1 - alignment_score) × (1 - goal_progress) × negative_experience_intensity`
- **Effects**: Pleasure increases will_to_live, Pain decreases it

---

## Now Cycle Event Loop

The "Now" cycle is a centralized event loop that:

1. **Locks all beings** (async-safe using `asyncio.Event`)
2. **Calculates system state** (will_to_live, luck, pleasure/pain, sleep)
3. **Processes sleeping beings** (check duration, reset quota if awake)
4. **Checks death conditions** (will_to_live = 0 → death)
5. **Records state** (Akasha, flight recorder, being files)
6. **Time marches forward** (+1 cycle)
7. **Unblocks beings** (allow decisions)
8. **Beings make decisions** (consume fatigue, generate experiences)

---

## Implementation Phases

### Phase 1: Extend Being Class
**File**: `src/waft/being.py`

- Add lifecycle attributes:
  - `will_to_live: float = 100.0` (0.0-100.0, death at 0.0)
  - `luck: float = 50.0` (0.0-100.0, luck range)
  - `decision_fatigue: int = 10` (decisions remaining)
  - `decision_quota_max: int = 10` (max decisions before sleep)
  - `pleasure: float = 0.0` (0.0-1.0)
  - `pain: float = 0.0` (0.0-1.0)
- Add personality and goals (NEW - Being doesn't have AgentState):
  - `personality: Dict[str, Any] = {}` (personality traits)
  - `goals: List[Dict[str, Any]] = []` (lifetime goals)
  - `personality_type: str = "balanced"` (analytical, creative, balanced)
- Add karma connection:
  - `soul_id: Optional[str] = None` (link to karma system)
- Add sleep state:
  - `is_sleeping: bool = False`
  - `sleep_duration: int = 0` (cycles to sleep)
  - `sleep_duration_base: int = 3` (base sleep duration, evolves)
  - `cycles_slept: int = 0` (current sleep counter)
- Add cycle tracking:
  - `last_cycle_number: int = 0`
  - `cycles_alive: int = 0`
- Add experience tracking:
  - `recent_experiences: List[Dict[str, Any]] = []` (last cycle's experiences)
- Add methods:
  - `calculate_will_to_live_change(cycle_data: dict) -> float`
  - `calculate_luck(karma_balance: float) -> float`
  - `calculate_pleasure_pain(personality: dict, goals: dict, experience: dict) -> tuple`
  - `check_death() -> bool`
  - `enter_sleep() -> None`
  - `process_sleep() -> bool` (returns True if awake)
  - `make_decision(decision_type: str) -> Dict[str, Any]` (decrements fatigue, returns experience)
  - `record_experience(experience: Dict[str, Any]) -> None`
- **CRITICAL**: Update `_save_being()` to set file permissions (0o600)
- **CRITICAL**: Update `_load_being()` to handle missing attributes (backward compatibility)

### Phase 2: Add Being Decision System
- Create `BeingDecisionSystem` class
- Define decision types (learn_skill, record_memory, pursue_goal, rest, explore)
- Implement decision-making algorithm

### Phase 3: Create Now Cycle Manager
**New File**: `src/waft/core/now_cycle.py`

- Create `NowCycleManager` class with:
  - `cycle_number: int = 0` (current cycle number)
  - `cycle_lock: asyncio.Lock` (prevent concurrent cycles)
  - `beings_locked: asyncio.Event` (async-safe locking for beings)
  - `cycle_history: List[Dict[str, Any]]` (cycle history)
- Implement `execute_cycle()` method:
  1. Lock all beings (`beings_locked.clear()`)
  2. Calculate system state (for all beings)
  3. Process sleeping beings
  4. Check death conditions
  5. Record state to storage
  6. Increment cycle_number
  7. Unblock beings (`beings_locked.set()`)
- Implement helper methods:
  - `calculate_system_state() -> Dict[str, Any]` (calculate all variables)
  - `process_sleeping_beings() -> List[str]` (return newly awake being IDs)
  - `check_death_conditions() -> List[str]` (return dead being IDs)
  - `record_cycle_state(cycle_data: Dict[str, Any]) -> None` (record to storage)
- **CRITICAL**: Use `asyncio.Lock` to prevent concurrent cycle execution
- **CRITICAL**: Add error handling for all file I/O operations
- Integrate with:
  - `BeingSystem` for being management
  - `KarmaMerchant` for karma balance lookups (via soul_id)
  - `TheObserver` for flight recorder events
  - Akasha storage for soul records

### Phase 4: Personality Alignment System
- Create `PersonalityAlignment` class
- Implement alignment calculation (cosine similarity or simpler scoring)
- Calculate pleasure/pain from personality-goal-experience alignment

### Phase 5: Karma Integration
**Files**: `src/waft/karma.py`, `src/waft/being.py`

- **CRITICAL**: Implement `KarmaMerchant.access_akasha()` (currently TODO/returns None):
  - Load soul record from `_hidden/.truth/{soul_id}.json`
  - Return dict with `karma_balance` key (required!)
  - Handle missing souls (return default: `{"soul_id": soul_id, "karma_balance": 0.0, "total_karma": 0.0}`)
  - Handle malformed JSON (fallback to default)
  - **CRITICAL**: Set file permissions (0o600) when creating new soul files
- Add `get_karma_balance()` method to `BeingSystem`:
  - Get karma balance for a being via soul_id
  - Create soul_id from being_id if missing: `f"soul_{being.being_id}"`
  - Handle missing karma_merchant (return 0.0)
  - **CRITICAL**: Validate soul_id before use (prevent path traversal)
- Add `get_soul_karma()` method to `KarmaMerchant`:
  - Wrapper around `access_akasha()` that returns just karma balance
  - Convenience method for luck calculation

### Phase 6: Storage and Recording
**Files**: `src/waft/core/now_cycle.py`, `src/waft/being.py`

- Akasha Integration:
  - Store being state after each cycle (via soul_id)
  - Record cycle history
  - Track sleep patterns
  - Track pleasure/pain history
  - **CRITICAL**: Set file permissions (0o600) on all soul files
- Flight Recorder Integration:
  - Record cycle events (via TheObserver)
  - Record death events (will to live = 0)
  - Record sleep events
  - Record pleasure/pain events
  - Use `EvolutionaryEvent` structure for consistency
- Being State Files:
  - Update being JSON files with new attributes
  - Maintain backward compatibility (load with defaults if missing)
  - **CRITICAL**: Set file permissions (0o600) in `_save_being()`
  - **CRITICAL**: Add error handling for file I/O (try/except blocks)
  - **CRITICAL**: Validate file paths (prevent path traversal)

### Phase 7: Sleep Evolution
- Implement sleep duration adaptation algorithm
- Track evolution history
- Pass evolved duration to offspring

---

## Critical Security Fixes Required

**BEFORE IMPLEMENTATION** - These must be addressed first:

1. **Set File Permissions**: Add `chmod(0o600)` to all file write operations
   ```python
   being_file.chmod(0o600)  # Owner read/write only
   self.beings_path.chmod(0o700)  # Owner read/write/execute only
   ```

2. **Validate Input IDs**: Reject path traversal, control characters in being_id/soul_id
   - Reject IDs with `..`, `/`, `\`, null bytes, control characters
   - Limit ID length (max 255 characters)
   - Sanitize IDs (alphanumeric + underscore + hyphen only)

3. **Implement access_akasha()**: MUST implement `KarmaMerchant.access_akasha()` before using
   - Currently returns `None` (TODO)
   - Must return dict with `karma_balance` key
   - Handle missing souls (return default with `karma_balance: 0.0`)

4. **Add Path Traversal Protection**: Validate all file paths resolve within project root
   - Use `Path.resolve()` and check `path.is_relative_to(project_root)`
   - Reject any path that escapes project directory

5. **Add Error Handling**: Try/except blocks for all file I/O operations
   - Handle `IOError`, `PermissionError`, `OSError`
   - Handle `json.JSONDecodeError` when loading
   - Don't crash entire cycle if one being's file fails

6. **Prevent Concurrent Cycles**: Use `asyncio.Lock` to prevent multiple cycles running simultaneously
   ```python
   self.cycle_lock = asyncio.Lock()  # Prevent concurrent cycles
   async with self.cycle_lock:  # Only one cycle at a time
       # ... cycle logic ...
   ```

See [CRITIQUE_2026-01-11_185314_BEING_LIFECYCLE_PLAN.md](../../CRITIQUE_2026-01-11_185314_BEING_LIFECYCLE_PLAN.md) for full security analysis.

---

## File Structure

```
src/waft/
├── being.py                    # Extended with new attributes + personality/goals
├── core/
│   ├── now_cycle.py           # NEW: NowCycleManager
│   ├── personality_alignment.py  # NEW: PersonalityAlignment
│   ├── being_decisions.py      # NEW: BeingDecisionSystem
│   └── hub/
│       └── lifecycle.py       # NOT modified (works with BaseAgent, not Being)
└── karma.py                   # Modified: Implement access_akasha(), add get_karma_balance()
```

---

## Success Criteria

1. Beings have will_to_live, luck, decision_fatigue, pleasure, pain
2. Beings have personality and goals (new attributes)
3. Beings have soul_id for karma access
4. Will to live depletes based on time + decisions + pain
5. Luck calculated from karma (separate but related, via soul_id)
6. Decision fatigue varies per being, requires sleep when depleted
7. Sleep duration evolves over time
8. Pleasure/pain calculated from personality-goal-experience alignment
9. Now cycle event loop executes: calculate → record → unblock
10. All state recorded to proper locations (Akasha, flight recorder)
11. Beings blocked during cycle calculation (async-safe), unblocked after
12. Being decision system works (separate from BaseAgent OODA cycles)
13. Karma access works via soul_id mapping
14. **All security vulnerabilities fixed** (file permissions, input validation, etc.)

---

## Related Documents

- **Work Effort**: [WE-260111-roo0](../WE-260111-roo0_being_lifecycle_attributes_and_now_cycle_event_loop_system/WE-260111-roo0_index.md)
- **Security Critique**: [CRITIQUE_2026-01-11_185314_BEING_LIFECYCLE_PLAN.md](../../CRITIQUE_2026-01-11_185314_BEING_LIFECYCLE_PLAN.md)
- **Plan File**: `~/.cursor/plans/being_lifecycle_attributes_and_now_cycle_event_loop_9b808ead.plan.md`

---

## Notes

- This system creates a full RPG-like experience for beings with stats, decision-making, and lifecycle management
- The "Now" cycle acts as the game loop, synchronizing all beings each cycle
- Beings evolve their sleep patterns over time, creating emergent behavior
- Karma influences luck, creating a karmic luck system
- Pleasure/pain from personality alignment creates authentic experiences
