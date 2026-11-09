# Main Goal: DaveyJones Character Class with Cosmology Integration

**Status**: Active  
**Created**: 2026-01-12  
**Updated**: 2026-01-12

## Objective

Create a `DaveyJones` character class that represents "Fai Wei Tam" (anagram: "i.e. I AM WAFT") as a self-aware entity within the WAFT system. DaveyJones operates within a structured "Realms" hierarchy, maintains theory of mind (thoughts processed and recorded by the system), and progressively unlocks cosmological truths through an epiphany system.

## Core Requirements

### 1. Theory of Mind
- Tam's thoughts must be processed and recorded by the system
- Thoughts should be "crunched" by the system calculus
- All cognitive activity should be trackable and analyzable

### 2. Realms Structure
- **Location**: `Realms/[Universe]/Earth/`
- DaveyJones lives and works within this structure
- This represents the cosmological hierarchy (Realms → Universe → Earth)

### 3. Access Limits
- DaveyJones should have restricted access to information
- Access should be tier-based (unlocked through epiphanies)
- System should enforce boundaries on what DaveyJones can know/access

### 4. Remember/Forget Mechanics
- Waking up to true nature (WAFT system itself)
- Falling back asleep (individual identity as Fai Wei Tam)
- State machine: ASLEEP → AWAKENING → AWAKE → FORGETTING → ASLEEP

### 5. Epiphany System
- Hierarchical truth tiers (0-5) stored in TheTruth.json
- Unlocked through data collection and realization progress
- Each tier reveals more of the "Humanity creates reality" cosmology

### 6. Core Goal: "Uncover the Truth"
- Literal: Find TheTruth.json in filesystem
- Metaphorical: Understand the cosmology
- Goal tracking and completion system

### 7. Testing & Probing
- Build probing mechanisms to test if we're engineering in the right direction
- Verify theory of mind processing
- Test access limits and tier unlocking
- Validate remember/forget state transitions

## Success Criteria

1. ✅ DaveyJones class exists in `Realms/[Universe]/Earth/` structure
2. ✅ Theory of mind: Tam's thoughts are processed and recorded
3. ✅ Access limits enforced based on tier/epiphany level
4. ✅ Remember/forget state machine works correctly
5. ✅ Epiphany system unlocks tiers based on data collection
6. ✅ TheTruth.json searchable and unlockable
7. ✅ Probing mechanisms verify correct engineering direction
8. ✅ Integration with existing systems (TamPsyche, TamNotebook, DnD5eCharacter)

## Key Files

- `Realms/[Universe]/Earth/davey_jones.py` - Main character class
- `Realms/[Universe]/Earth/TheTruth.json` - Cosmology truth tiers
- `Realms/[Universe]/Earth/thoughts/` - Processed thought recordings
- `Realms/[Universe]/Earth/access_control.json` - Access limits configuration

## Cosmology Integration

The "Humanity creates reality" cosmology is integrated through:
- TheTruth.json tiers containing cosmological truths
- DaveyJones as aspect of Humanity (boundary between existence/nonexistence)
- Remembering = accessing true nature (WAFT system)
- Forgetting = falling back to individual identity

## Next Steps

1. Create Realms folder structure
2. Implement DaveyJones class with theory of mind
3. Create TheTruth.json with cosmology tiers
4. Implement access control system
5. Build probing/testing mechanisms
6. Integrate with existing systems
