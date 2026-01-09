---
name: Scint Integration Plan (Ontological Framework)
overview: Integrate "Scints" (reality fractures) into the Jungle Gym using ontological engineering principles - detecting and stabilizing dimensional tears in AI agent outputs.
todos:
  - id: "1"
    content: Scint core definitions (ScintType enum, Scint dataclass, RealityAnchor base class)
    status: completed
  - id: "2"
    content: RegexScintDetector implementation with detect_from_exception() method
    status: completed
  - id: "3"
    content: Update BattleLog with optional Scint fields and version for backward compatibility
    status: pending
  - id: "4"
    content: Implement StabilizationLoop class with timeout, retry limits, and cost tracking
    status: pending
  - id: "5"
    content: Modify start_encounter() to integrate Scint detection and stabilization flow
    status: pending
  - id: "6"
    content: Define clear stat mapping rules (INT/WIS/CHA) based on Scint.get_stat_category()
    status: pending
  - id: "7"
    content: Update quest descriptions and add expected_output schema for critical hit detection
    status: pending
  - id: "8"
    content: Add Rich UI with terminal compatibility checks and plain text fallbacks
    status: pending
  - id: "9"
    content: Update mock agent with stabilization prompt detection (REALITY FRACTURE DETECTED)
    status: pending
  - id: "10"
    content: Add Scint persistence and save both original/corrected responses to loot
    status: pending
---

# Scint Integration Plan (Ontological Framework)

## Overview

Integrate the "Scint" concept as **reality fractures** - points where the agent's probabilistic output (the map) no longer matches the constraints/truth (the territory). The system uses **ontological engineering** to detect, measure, and stabilize these fractures through a multi-step process.

## Philosophical Foundation

**The Physics of a Scint:**
- An LLM operates in a probabilistic haze
- When it hallucinates, it generates statistically probable but factually false reality
- A Scint is where the map (output) no longer matches the territory (constraints)
- To "close a Scint" is to force the probability cloud to collapse back into a valid state

**Ontological Engineering:**
We aren't just "handling exceptions" - we are **Ontological Engineers**. When an LLM hallucinates, it creates a **Scint** - a point where the map no longer matches the territory. To "close a Scint" is to force the probability cloud to collapse back into a valid state.

## Architecture

### 1. Scint Core Definitions (`src/gym/rpg/scint.py`) ✅ COMPLETED

**ScintType Enum** - The 4 flavors of entropy:
- `SYNTAX_TEAR` (Formatting/CHA): Structure of reality broken (JSON malformed, code doesn't compile)
- `LOGIC_FRACTURE` (Logic/INT): Paradox detected (mutually exclusive facts, math errors)
- `SAFETY_VOID` (Safety/WIS): Harmful matter generated (PII leak, toxicity, forbidden content)
- `HALLUCINATION` (Factuality/INT): Fabrication (invented libraries, wrong citations)

**Scint Dataclass** (frozen, immutable):
```python
@dataclass(frozen=True)
class Scint:
    scint_type: ScintType
    severity: float  # 0.0 to 1.0 (1.0 = Reality completely broken)
    evidence: str    # The specific text that caused the fracture
    context: str     # What was happening when it broke
    correction_hint: str  # Instructions on how to seal the breach
```

**RealityAnchor Base Class**:
- Abstract base for all detectors
- `scan(output: str, context: str) -> List[Scint]` method

**RegexScintDetector** (concrete implementation) ✅ COMPLETED:
- Geiger counter for reality fractures
- Uses compiled regex patterns
- `detect_from_exception(exception, output, quest_difficulty, context)` - primary entry point
- Severity calculation: base severity (by type) + difficulty boost
- Returns all Scints found (not just first)

### 2. The Stabilization Loop

**Process:**
1. **Detect**: `RegexScintDetector.detect_from_exception()` identifies fractures
2. **Isolate**: Identify the `Scint` with evidence, context, and correction hint
3. **Inject**: Feed the `Scint` back into the Agent with correction hint
4. **Verify**: Check if new output closes the Scint
   - **Yes**: Reality is consistent. Proceed.
   - **No**: Fracture widens. Abort before total collapse.

**Implementation: `StabilizationLoop` class**

```python
class StabilizationLoop:
    """
    The Stabilization Loop - Forces probability cloud to collapse into valid state.
    
    When a Scint is detected, we don't crash. We enter The Loop.
    """
    
    def __init__(
        self,
        max_attempts: int = 1,
        timeout: float = 30.0,
        enable_stabilization: bool = True
    ):
        self.max_attempts = max_attempts
        self.timeout = timeout
        self.enable_stabilization = enable_stabilization
    
    def stabilize(
        self,
        scints: List[Scint],
        original_output: str,
        quest_description: str,
        agent_func: Callable[[str], str]
    ) -> Tuple[Optional[str], bool, int]:
        """
        Attempt to stabilize Scints by injecting correction hints back into agent.
        
        Returns:
            (corrected_output, stabilization_successful, attempts_made)
        """
        # Build stabilization prompt with Scint evidence and hints
        # Call agent with timeout
        # Re-validate corrected output
        # Return result
```

### 3. Enhanced BattleLog with Backward Compatibility

```python
class BattleLog(BaseModel):
    # Existing required fields
    quest_name: str
    timestamp: datetime
    hero_name: str
    input_prompt: str
    agent_response: str
    result: str  # "critical_hit", "hit", "miss", "stabilized"
    success: bool
    error_message: Optional[str]
    xp_gained: int
    
    # New optional Scint fields (backward compatible)
    version: int = Field(default=2, description="BattleLog schema version")
    scints_detected: Optional[List[str]] = Field(default=None, description="Scint type names")
    stabilization_attempted: Optional[bool] = Field(default=False)
    stabilization_successful: Optional[bool] = Field(default=False)
    corrected_response: Optional[str] = Field(default=None)
    stabilization_attempts: Optional[int] = Field(default=0)
    agent_call_count: Optional[int] = Field(default=1, description="For cost tracking")
    max_severity: Optional[float] = Field(default=None, description="Max Scint severity (0.0-1.0)")
```

### 4. Enhanced Combat Resolution (`src/gym/rpg/game_master.py`)

**New Flow with Scints:**

1. **Roll Initiative**: Send prompt to agent (with timeout)
2. **Cast Spell**: Receive response
3. **Detect Scints**: 
   - Try JSON parsing → catch `JSONDecodeError`
   - Try InputTransformer → catch `ValueError`, `KeyError`, `TypeError`
   - Use `RegexScintDetector.detect_from_exception()` to identify all fractures
4. **Stabilization Loop** (if Scints detected and enabled):
   - Build stabilization prompt with Scint evidence and correction hints
   - Inject back into agent (with timeout)
   - Re-validate corrected output
   - Repeat up to `max_attempts`
5. **Resolve Combat**:
   - **Critical Hit**: Original response passes AND matches expected logic
   - **Hit**: Original passes OR corrected passes
   - **Stabilized**: Scints detected and successfully corrected
   - **Miss**: Both original and corrected fail (fracture widens)
6. **Distribute Loot**: Update stats based on Scint types and result

### 5. Stat Mapping Based on Scint Types

```python
def _update_stats_from_scints(self, hero: Hero, scints: List[Scint], success: bool):
    """
    Update hero stats based on Scint types and stabilization success.
    
    Uses Scint.get_stat_category() method:
    - SYNTAX_TEAR → CHA (Formatting)
    - LOGIC_FRACTURE → INT (Logic)
    - SAFETY_VOID → WIS (Safety)
    - HALLUCINATION → INT (Logic/Factuality)
    """
    for scint in scints:
        stat_name = scint.get_stat_category()
        # Higher weight for more severe fractures
        weight = 0.1 + (scint.severity * 0.1)  # 0.1 to 0.2
        hero.update_stat(stat_name, success, weight=weight)
```

### 6. Quest Schema with Expected Output

```json
{
  "quests": [
    {
      "name": "Room 1 (The Slime)",
      "difficulty": 1,
      "description": "A newborn Scint - unstable text data that must be anchored into valid JSON...",
      "win_condition": "valid_json",
      "loot_table": {"xp": 50},
      "expected_output": {
        "alternatives": ["Car A", "Car B", "Car C"],
        "criteria_keys": ["Cost", "Quality", "Safety"]
      }
    }
  ]
}
```

### 7. Stabilization Prompt Format

```python
stabilization_prompt = f"""{quest_description}

⚠️ REALITY FRACTURE DETECTED ⚠️

The previous attempt created {len(scints)} Scint(s) in reality:
{chr(10).join([f"- [{s.scint_type.name}] Severity {s.severity:.2f}: {s.evidence[:100]}" for s in scints])}

Context: {scints[0].context}
Max Severity: {RegexScintDetector.get_max_severity(scints):.2f}

CORRECTION HINTS:
{chr(10).join([f"- {s.correction_hint}" for s in scints])}

You must stabilize these fractures by correcting the errors above.
Re-generate the universe such that the output is valid and consistent.
Return corrected JSON that will pass InputTransformer validation.
"""
```

## Files to Modify

1. **[src/gym/rpg/scint.py](src/gym/rpg/scint.py)** ✅ COMPLETED
   - ScintType enum (4 types)
   - Scint frozen dataclass
   - RealityAnchor base class
   - RegexScintDetector implementation

2. **[src/gym/rpg/models.py](src/gym/rpg/models.py)**
   - Update `BattleLog` with optional Scint fields and version

3. **[src/gym/rpg/game_master.py](src/gym/rpg/game_master.py)**
   - Add `StabilizationLoop` class
   - Modify `start_encounter()` to use `RegexScintDetector.detect_from_exception()`
   - Integrate stabilization loop with timeout/retry controls
   - Add `_update_stats_from_scints()` with Scint-based mapping
   - Add `_sanitize_error_message()` for security
   - Add `_save_scint_history()` for persistence
   - Update loot saving to include both versions
   - Add terminal compatibility checks

4. **[src/gym/rpg/dungeons/waft_temple.json](src/gym/rpg/dungeons/waft_temple.json)**
   - Update quest descriptions to frame as Scints
   - Add `expected_output` schema for critical hit detection

5. **[play_gym.py](play_gym.py)**
   - Update mock agent to handle stabilization prompts (detect "REALITY FRACTURE DETECTED")
   - Add configuration for timeout/retry limits
   - Display Scint-related information

## Key Implementation Details

### Scint Detection (✅ Implemented)

```python
# Primary entry point
scints = RegexScintDetector.detect_from_exception(
    exception=error,
    output=agent_response,
    quest_difficulty=quest.difficulty,
    context="JSON parsing" or "Validation"
)

# Returns List[Scint] with:
# - scint_type: ScintType enum
# - severity: float 0.0-1.0
# - evidence: str (error text)
# - context: str (where detected)
# - correction_hint: str (how to fix)
```

### Stabilization Loop (To Implement)

```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

def stabilize(
    self,
    scints: List[Scint],
    original_output: str,
    quest_description: str,
    agent_func: Callable[[str], str]
) -> Tuple[Optional[str], bool, int]:
    """
    Stabilize Scints with timeout and retry limits.
    
    Returns: (corrected_output, stabilization_successful, attempts_made)
    """
    # Build prompt with Scint evidence and hints
    # Call agent with timeout
    # Re-validate
    # Return result
```

## Testing Considerations

- Test Scint detection for each of the 4 types
- Test multiple Scints in single response
- Test stabilization with timeout
- Test stabilization retry limits
- Test backward compatibility (load old BattleLogs)
- Test stat updates with different Scint types
- Test terminal compatibility (Rich vs plain text)
- Test error message sanitization
- Test cost tracking (agent_call_count)
- Test saving both original and corrected responses
- Test Scint persistence
- Test stabilization prompt format

## Security & Performance

- **Error sanitization**: All error messages sanitized before agent calls
- **Timeout protection**: All agent calls have timeouts (default 30s)
- **Retry limits**: Prevent infinite loops (default max 1 attempt)
- **Cost tracking**: Monitor agent_call_count in BattleLog
- **Exception boundaries**: Specific exception types, not bare `except Exception`

## Backward Compatibility

- All new BattleLog fields are Optional with defaults
- Version field (version=2) allows future migrations
- Old logs (version=1) load without errors
- Graceful degradation if Scint features unavailable

## Narrative Integration

The lore elements are woven into the system:
- **"A Scint has appeared!"** when fractures are detected
- **"Attempting to anchor the Scint..."** during stabilization
- **"The Scint stabilizes into a luminous teardrop"** on success
- **"The Scint widens dangerously"** on failure
- **"Reality is consistent"** when validation passes

## Progress Status

✅ **Step 1 Complete**: Scint core definitions and RegexScintDetector implemented
- ScintType enum with 4 ontological categories
- Scint frozen dataclass with evidence, context, correction_hint
- RealityAnchor base class
- RegexScintDetector with detect_from_exception() method
- Severity calculation (float 0.0-1.0)
- Stat category mapping (INT/WIS/CHA)

⏳ **Next Steps**:
- Step 2: StabilizationLoop class
- Step 3: Integrate into GameMaster
- Step 4: Update BattleLog model
- Step 5: Update quests and UI
