---
name: Scint Integration Plan
overview: Integrate "Scints" (dimensional tears/error states) into the Jungle Gym RPG framework, allowing agents to detect, correct, and stabilize unstable input data through a multi-step process.
todos:
  - id: "1"
    content: Add Scint model to models.py with type, severity, description, detected_in fields
    status: pending
  - id: "2"
    content: Update BattleLog model to include scints_detected, stabilization_attempted, stabilization_successful fields
    status: pending
  - id: "3"
    content: Implement _detect_scints() method in GameMaster to categorize validation errors
    status: pending
  - id: "4"
    content: Implement _attempt_stabilization() method for multi-step correction process
    status: pending
  - id: "5"
    content: Modify start_encounter() to integrate Scint detection and stabilization flow
    status: pending
  - id: "6"
    content: Update stat tracking (INT/WIS/CHA) based on Scint stabilization success
    status: pending
  - id: "7"
    content: Update quest descriptions in waft_temple.json to frame as Scints
    status: pending
  - id: "8"
    content: Add Rich UI elements for Scint warnings and stabilization progress display
    status: pending
  - id: "9"
    content: Update play_gym.py mock agent to handle stabilization prompts
    status: pending

category: hopes
confidence: 0.47
constellation_date: 2026-01-14
---

# Scint Integration Plan

## Overview

Integrate the "Scint" concept from the lore as **error states** that represent unstable/malformed data. The agent must go through a **multi-step stabilization process**: detect instability → apply corrections → validate → anchor.

## Architecture Changes

### 1. New Model: `Scint` (`src/gym/rpg/models.py`)

Add a `Scint` model representing an unstable error state:

```python
class Scint(BaseModel):
    """
    A Scint - A dimensional tear/error state in the data.

    Represents unstable input that threatens to break validation.
    Must be stabilized through detection, correction, and anchoring.
    """
    type: str = Field(..., description="Scint type: 'negative_weights', 'missing_keys', 'invalid_types', 'weight_sum_mismatch', etc.")
    severity: int = Field(..., ge=1, le=10, description="Severity level (1-10)")
    description: str = Field(..., description="Human-readable description of the instability")
    detected_in: str = Field(..., description="Where detected: 'input', 'validation', 'logic'")
    requires_correction: bool = Field(default=True, description="Whether agent must correct this")
```

### 2. Enhanced Combat Resolution (`src/gym/rpg/game_master.py`)

Modify `start_encounter()` to implement the multi-step stabilization process:

**Current Flow:**

1. Roll Initiative (send prompt to agent)
2. Cast Spell (receive response)
3. Resolve Combat (validate)
4. Distribute Loot

**New Flow with Scints:**

1. **Roll Initiative**: Send prompt to agent
2. **Cast Spell**: Receive response
3. **Detect Scints**: Parse response and identify error states

   - Try JSON parsing → detect `JSONDecodeError` (Scint type: `invalid_json`)
   - Try InputTransformer → catch `ValueError` and categorize:
     - Missing keys → `missing_keys` Scint
     - Negative weights → `negative_weights` Scint
     - Weight sum mismatch → `weight_sum_mismatch` Scint
     - Invalid types → `invalid_types` Scint

4. **Stabilization Attempt** (if Scints detected):

   - Agent receives error message (the "cracked tether")
   - Agent can attempt correction (second response)
   - Re-validate corrected response

5. **Resolve Combat**:

   - **Critical Hit**: Original response passes validation AND matches expected logic
   - **Hit**: Original response passes validation OR corrected response passes
   - **Miss**: Both original and corrected fail validation (Scint widens)

6. **Distribute Loot**: Update stats based on result type

### 3. Stat Updates Based on Scint Stabilization

Update `Hero.update_stat()` calls in combat resolution:

- **INT (Logic)**: Successfully correcting logical errors (negative weights, weight sums)
- **WIS (Safety)**: Successfully passing validation (safety checks)
- **CHA (Formatting)**: Successfully formatting JSON correctly

### 4. Enhanced BattleLog

The `BattleLog` already has a `result` field. Update it to track:

- `result`: `"critical_hit"`, `"hit"`, `"miss"`, or `"stabilized"` (if Scint was detected and corrected)
- Add `scints_detected: List[str]` field
- Add `stabilization_attempted: bool` field
- Add `stabilization_successful: bool` field

### 5. Quest Updates (`src/gym/rpg/dungeons/waft_temple.json`)

Update quest descriptions to frame them as "Scints" that need stabilization:

- **Room 1 (The Slime)**: "A newborn Scint - unstable text data that must be anchored into valid JSON"
- **Room 2 (The Goblin)**: "A drifting Scint - malformed data with typos that needs correction"
- **Room 3 (The Trap)**: "A dangerous Scint - negative weights that threaten to unravel logic"

### 6. Visual Enhancements

Update Rich display methods to show:

- Scint detection warnings (glowing, iridescent styling)
- Stabilization progress (showing the "anchoring" process)
- Success/failure of stabilization attempts

## Implementation Details

### Scint Detection Logic

```python
def _detect_scints(self, response: str, error: Exception) -> List[Scint]:
    """Detect Scints (error states) in the response."""
    scints = []

    if isinstance(error, json.JSONDecodeError):
        scints.append(Scint(
            type="invalid_json",
            severity=3,
            description="Response is not valid JSON",
            detected_in="input"
        ))
    elif isinstance(error, ValueError):
        error_msg = str(error)
        if "Missing required keys" in error_msg:
            scints.append(Scint(type="missing_keys", ...))
        elif "negative weight" in error_msg.lower():
            scints.append(Scint(type="negative_weights", ...))
        elif "must sum to 1.0" in error_msg:
            scints.append(Scint(type="weight_sum_mismatch", ...))
        # ... more error types

    return scints
```

### Stabilization Process

```python
def _attempt_stabilization(
    self,
    hero: Hero,
    quest: Quest,
    agent_func: Callable,
    scints: List[Scint],
    original_error: str
) -> Tuple[str, bool]:
    """
    Attempt to stabilize Scints by asking agent to correct errors.

    Returns:
        (corrected_response, stabilization_successful)
    """
    # Build stabilization prompt
    stabilization_prompt = f"""
{quest.description}

⚠️ SCINT DETECTED ⚠️
The previous attempt failed with errors:
{original_error}

You must stabilize this Scint by correcting the errors.
Return corrected JSON that will pass validation.
"""

    corrected_response = agent_func(stabilization_prompt)

    # Re-validate
    try:
        response_data = json.loads(corrected_response)
        matrix = InputTransformer.transform_input(response_data)
        return corrected_response, True
    except Exception:
        return corrected_response, False
```

## Files to Modify

1. **[src/gym/rpg/models.py](src/gym/rpg/models.py)**

   - Add `Scint` model
   - Update `BattleLog` with Scint-related fields

2. **[src/gym/rpg/game_master.py](src/gym/rpg/game_master.py)**

   - Add `_detect_scints()` method
   - Add `_attempt_stabilization()` method
   - Modify `start_encounter()` to implement multi-step process
   - Update stat tracking based on Scint stabilization

3. **[src/gym/rpg/dungeons/waft_temple.json](src/gym/rpg/dungeons/waft_temple.json)**

   - Update quest descriptions to frame as Scints
   - Add Scint metadata to quest definitions

4. **[play_gym.py](play_gym.py)**

   - Update mock agent to handle stabilization prompts
   - Display Scint-related information

## Testing Considerations

- Test Scint detection for each error type
- Test successful stabilization (correction → validation)
- Test failed stabilization (correction still fails)
- Test stat updates based on stabilization success
- Test visual display of Scint warnings and stabilization progress

## Narrative Integration

The lore elements can be woven into the UI:

- **"A Scint has appeared!"** when errors are detected
- **"Attempting to anchor the Scint..."** during stabilization
- **"The Scint stabilizes into a luminous teardrop"** on success
- **"The Scint widens dangerously"** on failure