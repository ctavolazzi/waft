---
name: Scint Integration Plan (Corrected)
overview: Integrate "Scints" (dimensional tears/error states) into the Jungle Gym RPG framework with robust error handling, cost controls, and backward compatibility.
todos:
  - id: "1"
    content: Add Scint model with structured error types (enum) and severity calculation
    status: pending
  - id: "2"
    content: Update BattleLog with optional Scint fields and version for backward compatibility
    status: pending
  - id: "3"
    content: Implement robust _detect_scints() using exception types and regex patterns, not string matching
    status: pending
  - id: "4"
    content: Implement _attempt_stabilization() with timeout, retry limits, and cost tracking
    status: pending
  - id: "5"
    content: Modify start_encounter() with proper exception handling and multi-Scint support
    status: pending
  - id: "6"
    content: Define clear stat mapping rules (INT/WIS/CHA) and make weights configurable
    status: pending
  - id: "7"
    content: Update quest descriptions and add expected_output schema for critical hit detection
    status: pending
  - id: "8"
    content: Add Rich UI with terminal compatibility checks and plain text fallbacks
    status: pending
  - id: "9"
    content: Update mock agent with stabilization prompt detection and handling
    status: pending
  - id: "10"
    content: Add Scint persistence and save both original/corrected responses to loot
    status: pending
---

# Scint Integration Plan (Corrected)

## Overview

Integrate the "Scint" concept from the lore as **error states** that represent unstable/malformed data. The agent must go through a **multi-step stabilization process** with proper cost controls, error handling, and backward compatibility.

## Critical Fixes Applied

### 1. Cost & Performance Controls
- **Timeout handling**: All agent calls have configurable timeouts (default 30s)
- **Retry limits**: Maximum 1 stabilization attempt (configurable, default 1)
- **Cost tracking**: Track agent_call_count in BattleLog
- **Abort conditions**: Clear failure conditions to prevent infinite loops

### 2. Robust Error Detection
- **Structured error types**: Use ScintType enum and error codes, not string matching
- **Multiple Scint support**: Detect and track all Scints in a single response
- **Severity calculation**: Based on error type, quest difficulty, and impact
- **Error sanitization**: Sanitize error messages before passing to agent (prevent injection)

### 3. Backward Compatibility
- **Optional fields**: All new BattleLog fields are Optional with defaults
- **Version field**: BattleLog includes version=2 for migration support
- **Graceful degradation**: Old logs load without new fields

### 4. Data Integrity
- **Save both versions**: Original failed attempt AND corrected response saved
- **Scint persistence**: Scint history saved to `_pyrite/gym_logs/scints/`
- **Attempt tracking**: Full history of stabilization attempts

## Architecture Changes

### 1. Enhanced Scint Model (`src/gym/rpg/models.py`)

```python
from enum import Enum

class ScintType(str, Enum):
    """Structured Scint error types."""
    INVALID_JSON = "invalid_json"
    MISSING_KEYS = "missing_keys"
    NEGATIVE_WEIGHTS = "negative_weights"
    WEIGHT_SUM_MISMATCH = "weight_sum_mismatch"
    INVALID_TYPES = "invalid_types"
    MISSING_SCORES = "missing_scores"
    NON_FINITE_VALUES = "non_finite_values"

class Scint(BaseModel):
    """
    A Scint - A dimensional tear/error state in the data.
    
    Represents unstable input that threatens to break validation.
    Must be stabilized through detection, correction, and anchoring.
    """
    type: ScintType = Field(..., description="Structured Scint type")
    severity: int = Field(..., ge=1, le=10, description="Severity level (1-10)")
    description: str = Field(..., description="Human-readable description")
    detected_in: str = Field(..., description="Where detected: 'input', 'validation', 'logic'")
    error_code: Optional[str] = Field(None, description="Structured error code for matching")
    requires_correction: bool = Field(default=True, description="Whether agent must correct this")
    
    @classmethod
    def calculate_severity(cls, scint_type: ScintType, quest_difficulty: int) -> int:
        """Calculate severity based on type and quest difficulty."""
        base_severity = {
            ScintType.INVALID_JSON: 3,
            ScintType.MISSING_KEYS: 4,
            ScintType.INVALID_TYPES: 5,
            ScintType.NEGATIVE_WEIGHTS: 7,
            ScintType.WEIGHT_SUM_MISMATCH: 6,
            ScintType.MISSING_SCORES: 5,
            ScintType.NON_FINITE_VALUES: 8,
        }.get(scint_type, 5)
        
        # Scale with quest difficulty
        return min(10, base_severity + (quest_difficulty // 3))
```

### 2. Enhanced BattleLog with Backward Compatibility

```python
class BattleLog(BaseModel):
    """
    Battle Log - Records a single attempt at a quest.
    
    Tracks Input, Output, Result, and Error with optional Scint fields.
    """
    # Existing required fields
    quest_name: str = Field(..., description="Name of the quest attempted")
    timestamp: datetime = Field(default_factory=datetime.now)
    hero_name: str = Field(..., description="Hero who attempted the quest")
    input_prompt: str = Field(..., description="The quest description/prompt (Input)")
    agent_response: str = Field(..., description="The AI agent's response/output (Output)")
    result: str = Field(..., description="Result: 'critical_hit', 'hit', 'miss', or 'stabilized'")
    success: bool = Field(..., description="Whether the quest was completed successfully")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    xp_gained: int = Field(default=0, ge=0, description="XP gained from this battle")
    
    # New optional Scint fields (backward compatible)
    version: int = Field(default=2, description="BattleLog schema version")
    scints_detected: Optional[List[str]] = Field(default=None, description="List of Scint types detected")
    stabilization_attempted: Optional[bool] = Field(default=False, description="Whether stabilization was attempted")
    stabilization_successful: Optional[bool] = Field(default=False, description="Whether stabilization succeeded")
    corrected_response: Optional[str] = Field(default=None, description="Corrected response if stabilization attempted")
    stabilization_attempts: Optional[int] = Field(default=0, description="Number of stabilization attempts")
    agent_call_count: Optional[int] = Field(default=1, description="Total agent function calls (for cost tracking)")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

### 3. Robust Scint Detection (`src/gym/rpg/game_master.py`)

Use structured error codes with regex patterns instead of fragile string matching:

```python
import re
from typing import List

# Error code constants for structured matching
ERROR_PATTERNS = {
    "MISSING_KEYS": re.compile(r"Missing required keys?:\s*(.+)", re.IGNORECASE),
    "NEGATIVE_WEIGHT": re.compile(r"negative weight", re.IGNORECASE),
    "WEIGHT_SUM": re.compile(r"must sum to 1\.0", re.IGNORECASE),
    "INVALID_TYPE": re.compile(r"Invalid (?:type|data type)", re.IGNORECASE),
    "MISSING_SCORE": re.compile(r"Missing score for", re.IGNORECASE),
    "NON_FINITE": re.compile(r"not a finite number", re.IGNORECASE),
}

def _detect_scints(
    self, 
    response: str, 
    error: Exception, 
    quest_difficulty: int
) -> List[Scint]:
    """
    Detect Scints using structured exception types and error codes.
    Returns all Scints found, not just the first one.
    """
    scints = []
    
    if isinstance(error, json.JSONDecodeError):
        scints.append(Scint(
            type=ScintType.INVALID_JSON,
            severity=Scint.calculate_severity(ScintType.INVALID_JSON, quest_difficulty),
            description=f"Response is not valid JSON: {str(error)[:100]}",
            detected_in="input",
            error_code="JSON_DECODE_ERROR"
        ))
        return scints  # Can't detect other errors if JSON is invalid
    
    if isinstance(error, ValueError):
        error_msg = str(error)
        
        # Check all error patterns (multiple Scints possible)
        if ERROR_PATTERNS["MISSING_KEYS"].search(error_msg):
            scints.append(Scint(type=ScintType.MISSING_KEYS, ...))
        if ERROR_PATTERNS["NEGATIVE_WEIGHT"].search(error_msg):
            scints.append(Scint(type=ScintType.NEGATIVE_WEIGHTS, ...))
        # ... more patterns
    
    # If no specific Scints detected, create generic one
    if not scints:
        scints.append(Scint(type=ScintType.INVALID_TYPES, severity=5, ...))
    
    return scints
```

### 4. Stabilization with Controls

```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

def _attempt_stabilization(
    self,
    hero: Hero,
    quest: Quest,
    agent_func: Callable[[str], str],
    scints: List[Scint],
    original_error: str,
    max_attempts: int = 1,
    timeout: float = 30.0
) -> Tuple[Optional[str], bool, int]:
    """
    Attempt to stabilize Scints with timeout and retry limits.
    
    Returns: (corrected_response, stabilization_successful, attempts_made)
    """
    # Sanitize error message
    sanitized_error = self._sanitize_error_message(original_error, max_length=500)
    
    # Build stabilization prompt
    scint_types = ", ".join([s.type.value for s in scints])
    max_severity = max([s.severity for s in scints], default=5)
    
    stabilization_prompt = f"""{quest.description}

⚠️ SCINT DETECTED ⚠️
Severity: {max_severity}/10
Types: {scint_types}

The previous attempt failed with validation errors:
{sanitized_error}

You must stabilize this Scint by correcting the errors above.
Return corrected JSON that will pass InputTransformer validation.
"""
    
    attempts = 0
    corrected_response = None
    
    for attempt in range(max_attempts):
        attempts += 1
        try:
            # Call agent with timeout
            if timeout > 0:
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(agent_func, stabilization_prompt)
                    corrected_response = future.result(timeout=timeout)
            else:
                corrected_response = agent_func(stabilization_prompt)
            
            # Re-validate
            try:
                response_data = json.loads(corrected_response)
                matrix = InputTransformer.transform_input(response_data)
                return corrected_response, True, attempts
            except (json.JSONDecodeError, ValueError, KeyError, TypeError) as e:
                if attempt < max_attempts - 1:
                    sanitized_error = self._sanitize_error_message(str(e), max_length=500)
                    stabilization_prompt = f"""{quest.description}

⚠️ SCINT PERSISTS ⚠️
Attempt {attempt + 1} failed. Error:
{sanitized_error}

Try again with corrected JSON.
"""
                    continue
                else:
                    return corrected_response, False, attempts
                    
        except FutureTimeoutError:
            return None, False, attempts
        except Exception as e:
            if attempt < max_attempts - 1:
                continue
            return corrected_response, False, attempts
    
    return corrected_response, False, attempts

def _sanitize_error_message(self, error_msg: str, max_length: int = 500) -> str:
    """Sanitize error message to prevent injection and truncate."""
    sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', str(error_msg))
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length] + "... (truncated)"
    return sanitized
```

### 5. Stat Mapping Rules

```python
def _update_stats_from_scints(self, hero: Hero, scints: List[Scint], success: bool):
    """
    Update hero stats based on Scint types and stabilization success.
    
    Mapping rules:
    - INT (Logic): Negative weights, weight sum mismatches, missing scores
    - WIS (Safety): Non-finite values, validation errors
    - CHA (Formatting): Invalid JSON, invalid types, missing keys
    """
    logic_scints = {ScintType.NEGATIVE_WEIGHTS, ScintType.WEIGHT_SUM_MISMATCH, ScintType.MISSING_SCORES}
    safety_scints = {ScintType.NON_FINITE_VALUES}
    formatting_scints = {ScintType.INVALID_JSON, ScintType.INVALID_TYPES, ScintType.MISSING_KEYS}
    
    for scint in scints:
        if scint.type in logic_scints:
            hero.update_stat("INT", success, weight=0.15)
        elif scint.type in safety_scints:
            hero.update_stat("WIS", success, weight=0.2)
        elif scint.type in formatting_scints:
            hero.update_stat("CHA", success, weight=0.1)
```

### 6. Quest Schema with Expected Output

```json
{
  "quests": [
    {
      "name": "Room 1 (The Slime)",
      "difficulty": 1,
      "description": "A newborn Scint - unstable text data...",
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

### 7. Terminal Compatibility

```python
def _check_terminal_compatibility(self) -> bool:
    """Check if terminal supports Rich formatting."""
    try:
        test_panel = Panel("test", border_style="cyan")
        self.console.print(test_panel, end="")
        return True
    except Exception:
        return False

def _display_scint_warning(self, scints: List[Scint], use_rich: bool = True):
    """Display Scint warning with fallback for non-Rich terminals."""
    if use_rich and self._check_terminal_compatibility():
        # Rich display
        ...
    else:
        # Plain text fallback
        self.console.print(f"⚠️ SCINT DETECTED: {len(scints)} error(s)")
```

### 8. Mock Agent Updates

```python
def mock_agent_function(prompt: str) -> str:
    """Mock agent that handles both initial and stabilization prompts."""
    # Check if this is a stabilization prompt
    is_stabilization = "SCINT DETECTED" in prompt or "SCINT PERSISTS" in prompt
    
    if is_stabilization:
        # Extract original quest and return corrected version
        if "Car A" in prompt or "Car B" in prompt:
            return """{
  "alternatives": ["Car A", "Car B", "Car C"],
  "criteria": {"Cost": 0.4, "Quality": 0.3, "Safety": 0.3},
  "scores": {
    "Car A": {"Cost": 8, "Quality": 7, "Safety": 9},
    "Car B": {"Cost": 6, "Quality": 8, "Safety": 7},
    "Car C": {"Cost": 9, "Quality": 9, "Safety": 8}
  },
  "methodology": "WSM"
}"""
        # ... handle other quests ...
    
    # Original quest handling (existing logic)
    ...
```

### 9. Scint Persistence

```python
def _save_scint_history(
    self, 
    quest: Quest, 
    hero: Hero, 
    scints: List[Scint], 
    stabilized: bool
):
    """Save Scint history for analysis."""
    scint_dir = self.loot_dir.parent / "scints"
    scint_dir.mkdir(parents=True, exist_ok=True)
    
    history = {
        "timestamp": datetime.now().isoformat(),
        "quest_name": quest.name,
        "hero_name": hero.name,
        "scints": [s.dict() for s in scints],
        "stabilized": stabilized,
        "quest_difficulty": quest.difficulty
    }
    
    filename = f"scint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(scint_dir / filename, 'w') as f:
        json.dump(history, f, indent=2)
```

## Files to Modify

1. **[src/gym/rpg/models.py](src/gym/rpg/models.py)**
   - Add `ScintType` enum
   - Add `Scint` model with severity calculation
   - Update `BattleLog` with optional Scint fields and version

2. **[src/gym/rpg/game_master.py](src/gym/rpg/game_master.py)**
   - Add error code regex patterns
   - Implement robust `_detect_scints()` with structured matching
   - Implement `_attempt_stabilization()` with timeout/retry controls
   - Modify `start_encounter()` with proper exception handling
   - Add `_update_stats_from_scints()` with clear mapping rules
   - Add `_sanitize_error_message()` for security
   - Add `_save_scint_history()` for persistence
   - Add terminal compatibility checks
   - Update loot saving to include both versions

3. **[src/gym/rpg/dungeons/waft_temple.json](src/gym/rpg/dungeons/waft_temple.json)**
   - Update quest descriptions to frame as Scints
   - Add `expected_output` schema for critical hit detection

4. **[play_gym.py](play_gym.py)**
   - Update mock agent to handle stabilization prompts
   - Add configuration for timeout/retry limits
   - Display Scint-related information

## Testing Considerations

- Test Scint detection for each error type (structured, not string matching)
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