---
name: Pain Pleasure Alignment Energy System
overview: Implement a comprehensive Pain/Pleasure/Alignment system where Beings feel sensations in response to Harm/Help, learn through Experience and Karma, and Alignment increases Capacity while Misalignment causes Friction. Energy is innate to all Beings with bidirectional Karma relationship, and Stamina modulates both Pain/Pleasure intensity and Action intensity (inverse relationship).
todos:
  - id: harm_help_classes
    content: Create Harm/Help classes in src/waft/core/harm.py with Arrow of Intent integration
    status: completed
  - id: alignment_system
    content: Create Alignment system in src/waft/core/alignment.py with Arrow of Intent cosine similarity
    status: completed
  - id: energy_system
    content: Add Energy system to Being class with bidirectional Karma relationship
    status: completed
  - id: enhance_pain_pleasure
    content: Enhance calculate_pleasure_pain() to use Harm/Help and Alignment with Stamina modulation
    status: completed
  - id: stamina_intensity
    content: Implement Stamina modulation of Action Intensity (inverse relationship) and Pain/Pleasure intensity
    status: completed
  - id: alignment_effects
    content: Add Alignment effects on Capacity (Energy, Stamina) and Misalignment effects on Will to Live
    status: completed
  - id: decision_integration
    content: Integrate Pain/Pleasure, Alignment, and Energy into decision calculus
    status: completed
  - id: learning_system
    content: Implement learning through Experience and Karma with alignment history tracking
    status: completed
---

# Pain/Pleasure/Alignment/Energy System Implementation Plan

## System Overview

Beings experience Pain and Pleasure based on Alignment of Arrow of Intent. Harm/Help are subjective - what one being intends as harm might be felt as pleasure by another. Alignment increases Capacity (Energy, Stamina), while Misalignment causes Friction (decreases Will to Live). Energy is innate to all Beings with bidirectional Karma relationship. Stamina modulates Pain/Pleasure intensity (capacity to feel) and Action intensity (inverse: more stamina = less intensity per action).

## Core Components

### 1. Harm/Help Class (`src/waft/core/harm.py`)

**Purpose**: Track intentional/unintentional Harm and Help with Arrow of Intent.

**Key Features**:

- `Harm` class: severity, intentional/unintentional, source, target, Arrow of Intent
- `Help` class: same structure but for positive outcomes
- Both can be interpreted differently by target (subjective interpretation)
- Arrow of Intent from encapsulated environments work (3D vector)

**Structure**:

```python
class Harm:
 - severity: float (0.0-1.0)
 - intentional: bool
 - source_being_id: str
 - target_being_id: str
 - arrow_of_intent: ArrowOfIntent (3D vector)
 - harm_type: str (physical, emotional, informational, systemic)
 - resolved: bool

class Help:
 - benefit: float (0.0-1.0)
 - intentional: bool
 - source_being_id: str
 - target_being_id: str
 - arrow_of_intent: ArrowOfIntent
 - help_type: str
 - acknowledged: bool
```

### 2. Alignment System (`src/waft/core/alignment.py`)

**Purpose**: Calculate Alignment between Arrow of Intent and outcomes/interpretations.

**Key Features**:

- Calculate alignment between two beings' Arrows of Intent (cosine similarity)
- Calculate alignment with environment/stimulus
- Alignment score (0.0-1.0): 1.0 = perfect alignment, 0.0 = misalignment
- Alignment → Pleasure conversion
- Misalignment → Pain conversion

**Alignment Calculation**:

- Between beings: cosine similarity of Arrow of Intent vectors
- With environment: how well stimulus matches being's goals/personality
- With outcomes: how well intended outcome matches actual outcome

**Integration**:

- Extends existing Scint/Agreement system from encapsulated environments
- Uses Arrow of Intent from Harm/Help classes

### 3. Energy System (Being Enhancement)

**Purpose**: Add innate Energy to all Beings with bidirectional Karma relationship.

**Being Class Changes** (`src/waft/being.py`):

- Add `energy: float` (current energy, 0.0-100.0)
- Add `energy_capacity: float` (max energy, derived from Karma)
- Add `energy_well: float` (Energy Well/Source, related to Karma)
- Add `energy_regeneration_rate: float` (energy restored per cycle)

**Energy ↔ Karma Relationship**:

- **Karma → Energy Capacity**: More karma = larger energy pool
  - Formula: `energy_capacity = base_capacity + (karma_balance / 100.0) * capacity_multiplier`
- **Energy Spent → Karma**: Energy expenditure generates karma
  - Formula: `karma_generated = energy_spent * karma_conversion_rate`

**Energy Consumption**:

- All actions consume energy (in addition to stamina)
- Energy depletion affects capacity to feel pain/pleasure
- Energy depletion affects action effectiveness

### 4. Enhanced Pain/Pleasure System

**Purpose**: Pain/Pleasure respond to Harm/Help and Alignment, modulated by Stamina.

**Current System** (`src/waft/being.py::calculate_pleasure_pain`):

- Currently only uses personality-goal-experience alignment
- Needs to integrate Harm/Help and Alignment system

**New Calculation**:

```python
def calculate_pleasure_pain(
    self,
    harm_events: List[Harm] = None,
    help_events: List[Help] = None,
    alignment_score: float = None,
    personality: Dict = None,
    goals: List = None,
    experience: Dict = None
) -> Tuple[float, float]:
    """
    Calculate pleasure and pain from multiple sources:
 1. Harm/Help events (subjective interpretation)
 2. Alignment score (Arrow of Intent alignment)
 3. Personality-goal-experience alignment (existing)

    Modulated by Stamina (capacity to feel)
    """
```

**Pain Sources**:

- Harm events (interpreted subjectively)
- Misalignment (Arrow of Intent mismatch)
- Personality-goal-experience misalignment (existing)

**Pleasure Sources**:

- Help events (interpreted subjectively)
- Alignment (Arrow of Intent match)
- Personality-goal-experience alignment (existing)

**Stamina Modulation**:

- Stamina affects capacity to feel pain/pleasure
- Formula: `effective_pain = pain * (stamina_ratio * 0.5 + 0.5)`
- Formula: `effective_pleasure = pleasure * (stamina_ratio * 0.5 + 0.5)`
- Low stamina = reduced capacity to feel (numbness)
- High stamina = full capacity to feel

### 5. Stamina Modulations

**Purpose**: Stamina modulates Pain/Pleasure intensity and Action intensity.

**Pain/Pleasure Intensity Modulation** (see above):

- Stamina ratio affects capacity to feel
- Implemented in `calculate_pleasure_pain()`

**Action Intensity Modulation** (`src/waft/core/being_decisions.py`):

- **Inverse Relationship**: More Stamina = Less Intensity per Action
- **Formula**: `action_intensity = base_intensity * (1.0 - stamina_ratio * intensity_modifier)`
- High stamina = more control, less intensity per action (efficient)
- Low stamina = desperate, high intensity per action (inefficient but powerful)

**Implementation**:

- Modify `_execute_decision()` to calculate action intensity from stamina
- Apply intensity to action outcomes (skill learning, goal progress, etc.)

### 6. Alignment Effects on Capacity

**Purpose**: Alignment increases Capacity, Misalignment decreases Will to Live.

**Alignment Effects** (per cycle):

- **Energy**: `energy += alignment_score * energy_regeneration_bonus`
- **Stamina**: `stamina += alignment_score * stamina_regeneration_bonus`
- **Capacity**: Overall capacity increases with alignment

**Misalignment Effects** (per cycle):

- **Will to Live**: `will_to_live -= (1.0 - alignment_score) * friction_rate`
- **Energy**: `energy -= (1.0 - alignment_score) * energy_drain_rate`
- **Stamina**: `stamina -= (1.0 - alignment_score) * stamina_drain_rate`

**Implementation**:

- Add to `NowCycleManager` cycle processing
- Calculate alignment for each being
- Apply alignment/misalignment effects

### 7. Learning Through Experience and Karma

**Purpose**: Beings learn how it feels to be treated, building understanding over lifetimes.

**Mechanism**:

- Track Harm/Help events in `recent_experiences`
- Store alignment history in memories
- Karma accumulates from Energy expenditure and Alignment
- Beings learn which actions create Alignment vs. Misalignment
- Personality/goals evolve based on what creates Pleasure (Alignment)

**Implementation**:

- Enhance `record_memory()` to include Harm/Help events
- Track alignment history in being's memory
- Update personality/goals based on alignment patterns

### 8. Decision Calculus Integration

**Purpose**: Pain/Pleasure, Alignment, Energy, and Stamina inform decisions.

**Current System** (`src/waft/core/being_decisions.py::_calculate_weights`):

- Already uses stamina for energy-based weighting
- Needs to integrate Pain/Pleasure and Alignment

**Enhancements**:

- Add Pain/Pleasure to decision weights (avoid pain, seek pleasure)
- Add Alignment preference (seek alignment, avoid misalignment)
- Add Energy state to decision weights (low energy = prefer rest)
- Combine all factors in weighted decision making

## Implementation Files

### New Files

- `src/waft/core/harm.py` - Harm/Help classes with Arrow of Intent
- `src/waft/core/alignment.py` - Alignment calculation system

### Modified Files

- `src/waft/being.py` - Add Energy system, enhance Pain/Pleasure calculation
- `src/waft/core/being_decisions.py` - Integrate Pain/Pleasure/Alignment into decisions, add action intensity modulation
- `src/waft/core/now_cycle.py` - Add alignment effects on Capacity
- `src/waft/core/personality_alignment.py` - Integrate with new Alignment system

### Integration Points

- Encapsulated Environments work (Arrow of Intent, Scint/Agreement)
- Existing Being lifecycle system (will_to_live, stamina, pleasure, pain)
- Karma system (bidirectional Energy ↔ Karma relationship)

## Implementation Order

1. **Phase 1: Harm/Help Classes**

   - Create `src/waft/core/harm.py` with Harm and Help classes
   - Integrate Arrow of Intent from encapsulated environments work
   - Add to Being class (track harm/help events)

2. **Phase 2: Alignment System**

   - Create `src/waft/core/alignment.py`
   - Calculate alignment between beings' Arrows of Intent
   - Calculate alignment with environment/stimulus
   - Integration with existing Scint/Agreement system

3. **Phase 3: Energy System**

   - Add Energy attributes to Being class
   - Implement Energy ↔ Karma bidirectional relationship
   - Add energy consumption to actions
   - Add energy regeneration per cycle

4. **Phase 4: Enhanced Pain/Pleasure**

   - Enhance `calculate_pleasure_pain()` to use Harm/Help and Alignment
   - Add Stamina modulation of Pain/Pleasure intensity
   - Integrate with existing personality-goal-experience system

5. **Phase 5: Stamina Modulations**

   - Implement action intensity modulation (inverse relationship)
   - Update `_execute_decision()` to use intensity
   - Verify Pain/Pleasure intensity modulation

6. **Phase 6: Alignment Effects**

   - Add alignment effects to NowCycleManager
   - Alignment increases Energy, Stamina, Capacity
   - Misalignment decreases Will to Live, Energy, Stamina

7. **Phase 7: Decision Integration**

   - Integrate Pain/Pleasure into decision weights
   - Integrate Alignment into decision weights
   - Integrate Energy state into decision weights

8. **Phase 8: Learning System**

   - Track Harm/Help in memories
   - Track alignment history
   - Update personality/goals based on alignment patterns

## Key Design Decisions

1. **Subjective Interpretation**: Harm/Help are interpreted by the target being, not determined by source intent alone
2. **Alignment = Pleasure**: Perfect alignment generates maximum pleasure
3. **Inverse Stamina → Intensity**: More stamina = less intensity per action (more control)
4. **Bidirectional Energy ↔ Karma**: Karma affects capacity, Energy spent generates Karma
5. **Stamina Modulates Feeling**: Low stamina = reduced capacity to feel pain/pleasure (numbness)
6. **Alignment Increases Capacity**: Creates positive feedback loop for aligned beings
7. **Misalignment = Friction**: Creates negative feedback, decreases Will to Live

## Testing Considerations

- Test Harm/Help subjective interpretation (same event, different beings)
- Test Alignment calculation (cosine similarity of Arrow of Intent)
- Test Energy ↔ Karma bidirectional relationship
- Test Stamina modulation of Pain/Pleasure intensity
- Test inverse Stamina → Action Intensity relationship
- Test Alignment effects on Capacity
- Test Misalignment effects on Will to Live
- Test decision calculus with all factors integrated