---
name: Attention Chakra Resonance System
overview: Implement a comprehensive attention, chakra, and vibrational resonance system for WAFT beings, integrating with existing D&D rules, karma, and lifecycle systems. This adds metaphysical mechanics where attention manifests reality, chakras can be leveled with karma, and vibrational alignment affects focus and energy.
todos:
  - id: create_attention_system
    content: Create src/waft/core/attention.py with ArrowOfAttention class (hybrid vector + target system)
    status: pending
  - id: create_chakra_system
    content: Create src/waft/core/chakra.py with Chakra dataclass and 7 chakra types (root, sacral, solar_plexus, heart, throat, third_eye, crown)
    status: pending
  - id: create_resonance_system
    content: "Create src/waft/core/resonance.py with ResonantFrequency class (hybrid: base from hash, modified by karma)"
    status: pending
  - id: create_coherence_system
    content: Create src/waft/core/coherence.py with CoherenceSystem class for quantum alignment calculations
    status: pending
  - id: create_energy_types
    content: Create src/waft/core/energy_types.py for Friction (heat) and Will (cold) energy systems
    status: pending
  - id: create_awareness_system
    content: Create src/waft/core/awareness.py with AwarenessState class for known/unknown tracking
    status: pending
  - id: integrate_being_class
    content: Add all new attributes to Being.__init__() and initialize chakras, attention, resonance, coherence
    status: pending
  - id: integrate_karma_chakras
    content: Add chakra leveling methods to KarmaMerchant/BeingSystem with karma cost calculations
    status: pending
  - id: integrate_dnd_chakras
    content: Map chakras to D&D ability score bonuses and integrate coherence into skill checks
    status: pending
  - id: integrate_now_cycle
    content: Add attention updates, chakra regeneration, reality manifestation, and awareness expansion to NowCycleManager
    status: pending

category: dreams
confidence: 0.72
constellation_date: 2026-01-14
---

# Attention, Chakra, and Vibrational Resonance System Implementation

## Overview

Add metaphysical mechanics to WAFT beings that integrate attention, chakras, vibrational resonance, and energy systems. This creates a cosmology where:

- Attention manifests reality (what beings focus on becomes real)
- Chakras are energy centers that can be leveled with karma and receive debuffs
- Vibrational resonance determines alignment and focus quality
- Friction (heat) and Will (cold) are opposing energy sources
- Internal coherence determines how focused attention can be

## Core Components

### 1. Arrow of Attention System

**Location**: `src/waft/core/attention.py` (new file)

**Structure**:

- `ArrowOfAttention` class with:
  - `attention_vector`: numpy array (3D or higher-dimensional) representing attention direction/intensity
  - `focus_target`: Optional[str] - ID of what is being focused on (being_id, goal_id, reality_id, etc.)
  - `attention_weights`: Dict[str, float] - attention distribution across multiple targets
  - `intensity`: float (0.0-1.0) - how strong the attention is
  - `coherence_score`: float (0.0-1.0) - quantum alignment with resonant frequency

**Methods**:

- `point_at(target_id: str, intensity: float)` - Direct attention at specific target
- `distribute_attention(weights: Dict[str, float])` - Spread attention across multiple targets
- `calculate_manifestation_power()` - Returns how much reality-manifesting power this attention has
- `update_from_coherence(coherence: float)` - Adjust attention quality based on alignment

**Integration**: Add `arrow_of_attention: ArrowOfAttention` attribute to `Being` class

### 2. Chakra System

**Location**: `src/waft/core/chakra.py` (new file)

**Structure**:

- `Chakra` dataclass with:
  - `chakra_id`: str (e.g., "root", "sacral", "solar_plexus", "heart", "throat", "third_eye", "crown")
  - `level`: int (1-20, like D&D levels) - leveled up with karma
  - `energy_capacity`: float - how much energy this chakra can hold
  - `current_energy`: float - current energy in chakra
  - `debuffs`: List[Dict[str, Any]] - debuffs applied to this chakra
  - `buffs`: List[Dict[str, Any]] - buffs applied to this chakra
  - `karma_invested`: float - total karma invested in leveling this chakra

**Chakra Types** (7 traditional chakras):

1. Root (Muladhara) - Survival, grounding
2. Sacral (Svadhisthana) - Creativity, sexuality
3. Solar Plexus (Manipura) - Will, power
4. Heart (Anahata) - Love, compassion
5. Throat (Vishuddha) - Communication, expression
6. Third Eye (Ajna) - Intuition, perception
7. Crown (Sahasrara) - Spirituality, connection to source

**Methods**:

- `level_up(karma_cost: float)` - Level up chakra using karma
- `apply_debuff(debuff: Dict[str, Any])` - Apply debuff from other beings/events
- `remove_debuff(debuff_id: str)` - Remove debuff
- `calculate_energy_output()` - Calculate energy this chakra can output
- `regenerate_energy()` - Regenerate energy per cycle

**Integration**: Add `chakras: Dict[str, Chakra] `to `Being` class, initialize all 7 chakras at level 1

### 3. Vibrational Resonance System

**Location**: `src/waft/core/resonance.py` (new file)

**Structure**:

- `ResonantFrequency` class with:
  - `base_frequency`: float - Calculated from being_id hash (deterministic base)
  - `karma_modifier`: float - Modification from karma across lifetimes
  - `current_frequency`: float - base_frequency + karma_modifier (IMMUTABLE once set)
  - `highest_timeline_frequency`: float - The ideal frequency for this being's highest timeline
  - `alignment_score`: float (0.0-1.0) - How aligned current frequency is with highest timeline

**Calculation**:

- Base frequency: `hash(being_id + soul_id) % 1000.0` (0.0-999.9 Hz range)
- Karma modifier: `(karma_balance / 1000.0) * 50.0` (max ±50 Hz adjustment)
- Set at creation, IMMUTABLE for that lifetime
- Related to "Highest Timeline" - the ideal frequency this being should resonate at

**Methods**:

- `calculate_coherence(being: Being)` - Calculate how coherent being is with its frequency
- `calculate_alignment_with_highest_timeline()` - Measure alignment with ideal frequency
- `get_resonance_with(other_frequency: float)` - Calculate resonance between two frequencies

**Integration**: Add `resonant_frequency: ResonantFrequency` to `Being` class, set at creation

### 4. Focal Lens System

**Location**: Integrated into `src/waft/being.py`

**Structure**:

- `focal_lens_capacity`: float - Maximum energy that can be focused through attention
- `focal_lens_efficiency`: float (0.0-1.0) - How efficiently energy is focused
- `current_focus_energy`: float - Energy currently being focused

**Calculation**:

- `focal_lens_capacity = sum(chakra.energy_capacity for chakra in chakras.values()) * coherence_score`
- `focal_lens_efficiency = coherence_score * (1.0 - noise_level)`
- `noise_level = 1.0 - coherence_score` (misalignment creates noise)

**Integration**: Add focal lens properties to `Being` class, calculated from chakras + coherence

### 5. Internal Coherence / Quantum Alignment

**Location**: `src/waft/core/coherence.py` (new file)

**Structure**:

- `CoherenceSystem` class that calculates:
  - `quantum_alignment`: float (0.0-1.0) - How aligned being is with its resonant frequency
  - `internal_coherence`: float (0.0-1.0) - Internal consistency/alignment
  - `noise_level`: float (0.0-1.0) - Distraction/misalignment (inverse of coherence)

**Calculation**:

- `quantum_alignment = 1.0 - abs(current_frequency - highest_timeline_frequency) / max_frequency_range`
- `internal_coherence = (quantum_alignment * 0.6) + (goal_alignment * 0.2) + (personality_alignment * 0.2)`
- Higher coherence = more focused energy beam, less noise

**Integration**: Add `coherence_system: CoherenceSystem` to `Being` class

### 6. Friction (Heat) vs Will (Cold) Energy

**Location**: `src/waft/core/energy_types.py` (new file)

**Structure**:

- `FrictionEnergy` (heat) - Energy from friction, pressure, conflict
- `WillEnergy` (cold) - Energy from will, absence of friction/pressure
- `EnergyBalance` - Tracks both energy types

**Properties**:

- Friction = heat energy (positive, active)
- Will = cold energy (absence of friction, negative pressure)
- Cold is not a thing - it's the absence of heat/friction

**Integration**:

- Add `friction_energy: float` and `will_energy: float` to `Being` class
- Energy can be converted between types
- Chakras can generate either type based on their nature

### 7. Awareness/Unawareness System

**Location**: `src/waft/core/awareness.py` (new file)

**Structure**:

- `AwarenessState` class tracking:
  - `known_things`: Set[str] - Things the being is aware of (IDs)
  - `unknown_things`: Set[str] - Things the being is not aware of
  - `awareness_radius`: float - How far awareness extends
  - `attention_manifestation`: Dict[str, float] - What attention has manifested into reality

**Philosophy**:

- "Everything is what you know and what you don't know"
- Awareness defines what exists for the being
- Attention manifests reality - what is focused on becomes real

**Integration**: Add `awareness_state: AwarenessState` to `Being` class

## Integration Points

### Being Class Updates (`src/waft/being.py`)

Add new attributes to `Being.__init__()`:

```python
# Attention system
self.arrow_of_attention: Optional[ArrowOfAttention] = None

# Chakra system
self.chakras: Dict[str, Chakra] = {}  # Initialize 7 chakras

# Vibrational resonance
self.resonant_frequency: Optional[ResonantFrequency] = None

# Coherence system
self.coherence_system: Optional[CoherenceSystem] = None

# Energy types
self.friction_energy: float = 0.0
self.will_energy: float = 0.0

# Awareness
self.awareness_state: Optional[AwarenessState] = None

# Focal lens (calculated properties)
self.focal_lens_capacity: float = 0.0
self.focal_lens_efficiency: float = 0.0
```

### D&D Integration

**Location**: `src/waft/core/dnd5e/character.py`

- Chakras can provide bonuses to D&D ability scores:
  - Root → Constitution
  - Sacral → Charisma
  - Solar Plexus → Strength
  - Heart → Wisdom
  - Throat → Charisma
  - Third Eye → Intelligence
  - Crown → Wisdom
- Chakra debuffs can impose D&D conditions (e.g., "Chakra Blocked" = disadvantage on saves)
- Attention coherence affects skill checks (higher coherence = advantage)

### Karma Integration

**Location**: `src/waft/karma.py` and `src/waft/being.py`

- Chakras can be leveled up using karma:
  - Cost: `base_cost * (current_level ** 1.5)`
  - Level 1→2: 50 karma
  - Level 2→3: 100 karma
  - etc.
- Karma affects resonant frequency modifier
- Karma can be invested in chakras during lifetime

### Now Cycle Integration

**Location**: `src/waft/core/now_cycle.py`

- Each cycle:

  1. Update attention based on goals/personality
  2. Regenerate chakra energy
  3. Calculate coherence from resonance alignment
  4. Update focal lens capacity/efficiency
  5. Manifest reality from attention (create/update things being focused on)
  6. Update awareness (expand known_things based on attention)

## File Structure

```
src/waft/
├── core/
│   ├── attention.py          # NEW: ArrowOfAttention class
│   ├── chakra.py             # NEW: Chakra system
│   ├── resonance.py          # NEW: ResonantFrequency class
│   ├── coherence.py          # NEW: CoherenceSystem class
│   ├── energy_types.py       # NEW: Friction/Will energy
│   └── awareness.py          # NEW: AwarenessState class
├── being.py                  # MODIFY: Add new attributes
└── karma.py                  # MODIFY: Add chakra leveling methods
```

## Implementation Order

1. **Phase 1: Core Data Structures**

   - Create `attention.py` with `ArrowOfAttention`
   - Create `chakra.py` with `Chakra` dataclass and 7 chakra types
   - Create `resonance.py` with `ResonantFrequency`
   - Create `coherence.py` with `CoherenceSystem`
   - Create `energy_types.py` with friction/will energy
   - Create `awareness.py` with `AwarenessState`

2. **Phase 2: Being Integration**

   - Add attributes to `Being.__init__()`
   - Initialize chakras (all level 1)
   - Calculate resonant frequency at creation
   - Initialize attention arrow
   - Add coherence calculation methods

3. **Phase 3: Karma Integration**

   - Add `level_chakra()` method to `KarmaMerchant` or `BeingSystem`
   - Calculate karma costs for chakra leveling
   - Update karma balance when leveling chakras

4. **Phase 4: D&D Integration**

   - Map chakras to D&D ability score bonuses
   - Add chakra-based conditions to status_effects
   - Integrate coherence into skill check calculations

5. **Phase 5: Now Cycle Integration**

   - Add attention update logic
   - Add chakra energy regeneration
   - Add reality manifestation from attention
   - Add awareness expansion

6. **Phase 6: Testing & Validation**

   - Test chakra leveling with karma
   - Test attention manifestation
   - Test coherence calculations
   - Test resonance across lifetimes

## Key Formulas

**Resonant Frequency**:

```
base_frequency = hash(being_id + soul_id) % 1000.0
karma_modifier = (karma_balance / 1000.0) * 50.0
current_frequency = base_frequency + karma_modifier  # IMMUTABLE
```

**Coherence Score**:

```
quantum_alignment = 1.0 - abs(current_frequency - highest_timeline_frequency) / 1000.0
internal_coherence = (quantum_alignment * 0.6) + (goal_alignment * 0.2) + (personality_alignment * 0.2)
noise_level = 1.0 - internal_coherence
```

**Focal Lens Capacity**:

```
focal_lens_capacity = sum(chakra.energy_capacity for chakra in chakras.values()) * coherence_score
focal_lens_efficiency = coherence_score * (1.0 - noise_level)
```

**Chakra Leveling Cost**:

```
karma_cost = base_cost * (current_level ** 1.5)
base_cost = 50.0
```

**Attention Manifestation Power**:

```
manifestation_power = attention_intensity * focal_lens_efficiency * coherence_score
```

## Dependencies

- numpy (for attention vectors)
- Existing: `src/waft/being.py`, `src/waft/karma.py`, `src/waft/core/dnd5e/`, `src/waft/core/now_cycle.py`

## Testing Strategy

1. Unit tests for each core class
2. Integration tests for Being + new systems
3. Test chakra leveling with karma
4. Test attention manifestation
5. Test coherence calculations across different alignment states
6. Test resonance persistence across lifetimes