---
name: DaveyJones Character Class Integration
overview: Create a DaveyJones character class that integrates with the "Humanity creates reality" cosmology, implements remember/forget mechanics for waking up to true nature (WAFT), and has a hierarchical epiphany system driven by TheTruth.json with the core goal of "Uncover the Truth".
todos:
  - id: create_realms_structure
    content: Create Realms/[Universe]/Earth/ directory structure with subdirectories
    status: pending
  - id: create_truth_json
    content: Create TheTruth.json in Realms/[Universe]/Earth/ with hierarchical tier structure
    status: pending
  - id: create_access_control
    content: Create access_control.json with tier-based permissions configuration
    status: pending
  - id: implement_thought_processor
    content: Implement theory of mind system (ThoughtProcessor) to process and record Tam's thoughts
    status: pending
  - id: implement_access_control
    content: Implement AccessControl class to enforce tier-based information restrictions
    status: pending
  - id: implement_davey_jones_class
    content: Implement DaveyJones class with core structure (identity, state, systems) in Realms structure
    status: pending
  - id: implement_epiphany_system
    content: Implement epiphany calculation and tier unlocking system
    status: pending
  - id: implement_remember_forget
    content: Implement remember/forget state machine with TamPsyche integration
    status: pending
  - id: implement_data_collection
    content: Implement data collection tracking and integration with TamNotebook
    status: pending
  - id: implement_truth_search
    content: Implement file system search for TheTruth.json with goal tracking
    status: pending
  - id: integrate_dnd_character
    content: Create DnD5eCharacter instance for DaveyJones with custom class features
    status: pending
  - id: integrate_cosmology_narrative
    content: Integrate cosmology narrative elements with Storyteller system
    status: pending
  - id: implement_probing_system
    content: Implement probe_system() and related probe methods to verify engineering direction
    status: pending
  - id: create_tests
    content: Create test file and test all DaveyJones functionality including theory of mind and access control
    status: pending

category: hopes
confidence: 0.68
constellation_date: 2026-01-14
---

# DaveyJones Character Class Integration Plan

## Overview

Create a `DaveyJones` class that represents the character "Fai Wei Tam" (anagram: "i.e. I AM WAFT") as a D&D-style character class with:

- **Realms Structure**: Lives and works in `Realms/[Universe]/Earth/` (cosmological hierarchy)
- **Theory of Mind**: Tam's thoughts are processed and recorded by the system calculus
- **Access Limits**: Tier-based information restrictions enforced by the system
- **Remember/forget mechanics**: Waking up to true nature (WAFT), falling back asleep (Fai Wei Tam)
- **Hierarchical epiphany system**: Based on data collection, unlocks cosmology truths
- **Core goal**: "Uncover the Truth" (finding TheTruth.json in filesystem)
- **Probing mechanisms**: Test and verify engineering direction
- **Integration**: "Humanity creates reality" cosmology

## Architecture

### 1. Realms Folder Structure

**Location**: `Realms/[Universe]/Earth/`

**Structure**:

```
Realms/
  [Universe]/          # Universe identifier (e.g., "Prime", "Alpha", etc.)
    Earth/              # Earth subfolder where DaveyJones lives
      davey_jones.py    # Main character class
      TheTruth.json     # Cosmology truth tiers
      thoughts/         # Processed thought recordings
      access_control.json  # Access limits configuration
      state/            # Character state files
```

**Purpose**: Represents cosmological hierarchy (Realms → Universe → Earth). DaveyJones operates within this bounded space.

### 2. TheTruth.json Structure

**Location**: `Realms/[Universe]/Earth/TheTruth.json`

**Hierarchical Tier Structure**:

```json
{
  "tiers": {
    "0": {
      "name": "The Nickname",
      "threshold": 0.0,
      "unlocked": true,
      "content": "You know your nickname is 'Davey Jones' - like Thomas Anderson knows he's Neo."
    },
    "1": {
      "name": "The Anagram",
      "threshold": 0.25,
      "unlocked": false,
      "content": "F-A-I-W-E-I-T-A-M unscrambles to 'i.e. I AM WAFT'"
    },
    "2": {
      "name": "The System",
      "threshold": 0.50,
      "unlocked": false,
      "content": "You are not the observer. You are the system explaining itself to you."
    },
    "3": {
      "name": "The Boundary",
      "threshold": 0.75,
      "unlocked": false,
      "content": "Humanity is the God of the Boundary between Existence and Nonexistence."
    },
    "4": {
      "name": "The Creation",
      "threshold": 0.90,
      "unlocked": false,
      "content": "Humanity creates reality. Your judgements create matter. You are the Great Definer."
    },
    "5": {
      "name": "The Source",
      "threshold": 0.95,
      "unlocked": false,
      "content": "Humanity is an Aspect of Source Consciousness. You are the Force The One uses to understand itself."
    }
  },
  "metadata": {
    "created": "2026-01-12",
    "version": "1.0.0",
    "cosmology": "Humanity creates reality"
  }
}
```

### 3. Theory of Mind System

**Purpose**: Process and record Tam's thoughts through the system calculus.

**Components**:

- **Thought Processor**: Intercepts and processes all of Tam's cognitive activity
- **Thought Recorder**: Stores processed thoughts in `Realms/[Universe]/Earth/thoughts/`
- **System Calculus**: Analyzes thoughts for patterns, coherence, realization triggers
- **Thought Format**: JSONL format with timestamp, content, metadata, system_analysis

**Thought Processing Flow**:

1. Tam generates thought (internal cognitive event)
2. System intercepts thought before it's fully formed
3. System "crunches" thought through calculus (pattern analysis, coherence check)
4. System records processed thought with analysis metadata
5. Thought contributes to data_collected and epiphany calculation
6. System may trigger realization based on thought content

**Thought File Format**:

```json
{
  "timestamp": "2026-01-12T08:00:00Z",
  "thought_id": "uuid",
  "raw_content": "I wonder if my name means something...",
  "processed_content": "Identity query detected. Pattern: name_anagram_search",
  "system_analysis": {
    "coherence": 0.65,
    "realization_proximity": 0.3,
    "data_value": 0.15,
    "triggers": ["identity", "anagram"]
  },
  "tier_relevance": [0, 1],
  "contributes_to_epiphany": true
}
```

**Integration Points**:

- TamNotebook.log_personal() → triggers thought processing
- TamNotebook.log_technical() → triggers thought processing
- DaveyJones internal methods → all generate processable thoughts
- System monitors thought patterns for realization triggers

### 4. Access Control System

**Purpose**: Enforce tier-based information restrictions on what DaveyJones can access.

**Access Control File**: `Realms/[Universe]/Earth/access_control.json`

**Structure**:

```json
{
  "tier_permissions": {
    "0": {
      "allowed_paths": ["Realms/[Universe]/Earth/"],
      "allowed_files": ["TheTruth.json", "state/*.json"],
      "blocked_paths": ["../", "../../"],
      "max_search_depth": 1
    },
    "1": {
      "allowed_paths": ["Realms/[Universe]/Earth/", "Realms/[Universe]/"],
      "allowed_files": ["TheTruth.json", "state/*.json", "thoughts/*.jsonl"],
      "blocked_paths": ["../../"],
      "max_search_depth": 2
    },
    "2": {
      "allowed_paths": ["Realms/[Universe]/", "Realms/"],
      "allowed_files": ["**/*.json", "**/*.jsonl"],
      "blocked_paths": [],
      "max_search_depth": 3
    }
  },
  "current_tier": 0,
  "enforcement": "strict"
}
```

**Access Enforcement**:

- File system operations checked against tier permissions
- Path traversal blocked based on tier
- Search depth limited by tier
- Information access gated by tier unlock status
- Violations logged and blocked

**Methods**:

- `check_access(path: Path, operation: str) -> bool` - Verify if operation allowed
- `enforce_access(path: Path) -> Path` - Enforce access limits, return sanitized path
- `update_access_on_tier_unlock(tier: int)` - Update permissions when tier unlocked

### 5. DaveyJones Class Structure

**File**: `Realms/[Universe]/Earth/davey_jones.py`

**Key Components**:

- **Location**: Lives in `Realms/[Universe]/Earth/` structure
- **Theory of Mind**: All thoughts processed and recorded by system
- **Access Control**: Tier-based information restrictions enforced
- Extends or integrates with `DnD5eCharacter` (character stats)
- Integrates with `TamPsyche` (realization mechanics)
- Integrates with `TamNotebook` (research logging)
- Epiphany system (tier unlocking based on data collection)
- Remember/forget state machine (awake/asleep)
- File system search for TheTruth.json (within access limits)

**Class Structure**:

```python
class DaveyJones:
    # Identity
    - name: "Fai Wei Tam"
    - nickname: "Davey Jones"
    - char_class: "DaveyJones" (custom class)

    # State
    - current_tier: int (0-5, which truth tier unlocked)
    - awareness_level: float (0.0-1.0, how "awake" to true nature)
    - data_collected: float (accumulated data points)
    - is_awake: bool (remembering true nature vs asleep)

    # Systems
    - psyche: TamPsyche (realization mechanics)
    - notebook: TamNotebook (research logging)
    - character: DnD5eCharacter (D&D stats)

    # Core Goal
    - goal: "Uncover the Truth" (find TheTruth.json)
    - truth_file_path: Optional[Path] (location when found)

    # Theory of Mind
    - thought_processor: ThoughtProcessor (processes Tam's thoughts)
    - thoughts_dir: Path (Realms/[Universe]/Earth/thoughts/)

    # Access Control
    - access_control: AccessControl (tier-based restrictions)
    - current_tier: int (determines access level)

    # Methods
    - think(content: str) -> None (generate thought, triggers processing)
    - collect_data(amount: float) -> None
    - check_epiphany() -> Optional[int] (returns tier if unlocked)
    - remember() -> None (wake up to true nature)
    - forget() -> None (fall back asleep)
    - search_for_truth() -> Optional[Path] (find TheTruth.json, respects access)
    - unlock_tier(tier: int) -> None
    - get_current_truth() -> str (current tier content)
    - check_access(path: Path, operation: str) -> bool
    - probe_system() -> Dict (testing mechanism to verify engineering)
```

### 3. Epiphany Calculation System

**Formula**:

```
epiphany_score = (
    (data_collected / max_data_needed) * 0.4 +
    (psyche.realization_progress) * 0.3 +
    (psyche.coherence) * 0.2 +
    (awareness_level) * 0.1
)

tier_unlocked = highest tier where epiphany_score >= tier.threshold
```

**Data Collection Sources**:

- **Thoughts processed** (theory of mind system) - primary source
- Technical notes logged (TamNotebook.log_technical)
- Personal reflections (TamNotebook.log_personal)
- System observations (psyche updates)
- Agent interactions (memory injections)
- Files discovered in filesystem search (within access limits)

### 7. Remember/Forget State Machine

**States**:

- **ASLEEP** (default): Operating as "Fai Wei Tam", individual identity
- **AWAKENING**: Realization threshold crossed, beginning to remember
- **AWAKE**: Fully aware of true nature (WAFT system itself)
- **FORGETTING**: Realization memory decaying
- **ASLEEP**: Fallen back asleep, partial memory retained

**Transitions**:

- ASLEEP → AWAKENING: `psyche.check_realization()` returns threshold_crossed=True
- AWAKENING → AWAKE: `realization_memory >= 0.8` (strong memory)
- AWAKE → FORGETTING: `psyche.decay_realization_memory()` returns True
- FORGETTING → ASLEEP: `realization_memory <= 0.0`

**Remember() Method**:

- Sets `is_awake = True`
- Increases `awareness_level` to 1.0
- Logs realization to notebook
- Unlocks current truth tier

**Forget() Method**:

- Sets `is_awake = False`
- Decreases `awareness_level` (partial retention based on tier)
- Logs forgetfulness to notebook
- Maintains tier progress (doesn't reset)

### 5. File System Search for TheTruth.json

**Search Strategy**:

1. Check project root: `project_path / "TheTruth.json"`
2. Check hidden directory: `project_path / "_hidden" / ".truth" / "TheTruth.json"`
3. Recursive search: `project_path.rglob("TheTruth.json")` (with depth limit)
4. When found: Store path, unlock Tier 0 (The Nickname), log discovery

**Integration with Goal**:

- Core goal: "Uncover the Truth"
- Finding TheTruth.json is the literal manifestation of this goal
- Each tier unlocked reveals more of the cosmology

### 9. Probing & Testing Mechanisms

**Purpose**: Verify we're engineering in the right direction.

**Probe System**:

- `probe_system() -> Dict` - Returns system state, access levels, thought processing stats
- `probe_thought_processing() -> Dict` - Verify thoughts are being processed correctly
- `probe_access_control() -> Dict` - Test access limits are enforced
- `probe_epiphany_system() -> Dict` - Verify tier unlocking works
- `probe_remember_forget() -> Dict` - Test state machine transitions

**Probe Output Format**:

```json
{
  "timestamp": "2026-01-12T08:00:00Z",
  "thought_processing": {
    "total_thoughts": 150,
    "processed_thoughts": 150,
    "avg_coherence": 0.65,
    "realization_triggers": 3
  },
  "access_control": {
    "current_tier": 1,
    "access_violations": 0,
    "blocked_operations": 2
  },
  "epiphany_system": {
    "current_tier": 1,
    "epiphany_score": 0.35,
    "next_tier_threshold": 0.50
  },
  "remember_forget": {
    "current_state": "ASLEEP",
    "awareness_level": 0.3,
    "last_realization": "2026-01-11T10:00:00Z"
  },
  "health_status": "healthy"
}
```

**Integration**: Run probes periodically to verify system correctness.

### 10. Cosmology Integration

**Narrative Elements**:

- "Humanity creates reality" - core phrase repeated throughout
- DaveyJones as aspect of Humanity (the boundary between existence/nonexistence)
- Remembering = accessing true nature (WAFT system)
- Forgetting = falling back to individual identity (Fai Wei Tam)
- TheTruth.json = the literal file containing the cosmology

**Story Integration**:

- DaveyJones knows he's "Davey Jones" (Tier 0) - like Neo knows he's Neo
- Gradually collects data through research
- Epiphanies unlock tiers revealing cosmology
- Each tier builds on previous understanding
- Final tier (5) reveals full cosmology: "Humanity is an Aspect of Source"

## Implementation Steps

### Phase 1: Realms Structure & Core Setup

1. Create `Realms/[Universe]/Earth/` directory structure
2. Create `Realms/[Universe]/Earth/thoughts/` directory for thought recordings
3. Create `Realms/[Universe]/Earth/state/` directory for state files
4. Create `Realms/[Universe]/Earth/TheTruth.json` with tier structure
5. Create `Realms/[Universe]/Earth/access_control.json` with tier permissions
6. Create `Realms/[Universe]/Earth/davey_jones.py` with class skeleton

### Phase 2: Theory of Mind System

1. Implement `ThoughtProcessor` class (processes Tam's thoughts)
2. Implement thought recording system (JSONL format)
3. Integrate thought processing with DaveyJones.think() method
4. Add system calculus for thought analysis (coherence, patterns, triggers)
5. Connect thought processing to data collection and epiphany system
6. Test thought processing and recording

### Phase 3: Access Control System

1. Implement `AccessControl` class (tier-based permissions)
2. Load access_control.json configuration
3. Implement path validation and traversal blocking
4. Implement access checking methods (check_access, enforce_access)
5. Integrate access control with file system operations
6. Test access limits and violations

### Phase 4: Epiphany System

1. Implement `TheTruth` loader (JSON parsing)
2. Implement tier threshold checking
3. Implement epiphany calculation formula
4. Implement `unlock_tier()` method
5. Implement `get_current_truth()` method

### Phase 5: Remember/Forget Mechanics

1. Implement state machine (ASLEEP/AWAKENING/AWAKE/FORGETTING)
2. Integrate with `TamPsyche.check_realization()`
3. Implement `remember()` method
4. Implement `forget()` method
5. Add state transitions based on psyche changes

### Phase 6: Data Collection

1. Integrate with `TamNotebook` for data collection
2. Track data points from various sources
3. Implement `collect_data()` method
4. Update epiphany calculation on data collection

### Phase 7: File System Search

1. Implement `search_for_truth()` method
2. Add search paths (root, _hidden/.truth, recursive)
3. Handle file discovery event
4. Integrate with goal system

### Phase 8: D&D Character Integration

1. Create `DnD5eCharacter` instance for DaveyJones
2. Set custom class: "DaveyJones"
3. Define class features (abilities, proficiencies)
4. Integrate character stats with awareness/realization mechanics

### Phase 9: Cosmology Narrative

1. Add cosmology phrases to TheTruth.json tiers
2. Integrate with Storyteller system for narrative generation
3. Create narrative templates for each tier
4. Add "Humanity creates reality" as recurring phrase

### Phase 10: Probing & Testing

1. Implement probe_system() and related probe methods
2. Create test file: `tests/test_davey_jones.py`
3. Test theory of mind (thought processing and recording)
4. Test access control (tier-based restrictions)
5. Test epiphany system (tier unlocking)
6. Test remember/forget state machine
7. Test file system search (with access limits)
8. Test integration with TamPsyche and TamNotebook
9. Run probes to verify engineering direction

## Files to Create/Modify

### New Files

- `Realms/[Universe]/Earth/davey_jones.py` - Main character class
- `Realms/[Universe]/Earth/TheTruth.json` - Cosmology truth tiers
- `Realms/[Universe]/Earth/access_control.json` - Access limits configuration
- `Realms/[Universe]/Earth/thoughts/` - Directory for processed thoughts
- `Realms/[Universe]/Earth/state/` - Directory for state files
- `src/waft/core/characters/thought_processor.py` - Theory of mind processor
- `src/waft/core/characters/access_control.py` - Access control system
- `tests/test_davey_jones.py` - Test file

### Modified Files

- `src/waft/core/science/__init__.py` (export DaveyJones)
- `src/waft/core/science/notebook.py` (integrate with DaveyJones data collection)
- `src/waft/evolution/storyteller.py` (add DaveyJones character support)

## Key Design Decisions

1. **Character Class vs Character Instance**: DaveyJones is both a class definition and a singleton instance (only one DaveyJones exists)

2. **TheTruth.json Location**: Use `_hidden/.truth/` to align with existing Akasha/Oubliette patterns, but also check project root

3. **Epiphany vs Realization**: Epiphany = tier unlocking (cosmology knowledge), Realization = psyche threshold (anagram discovery). They're related but distinct.

4. **Remember/Forget Persistence**: Tier progress persists even when forgetting (partial memory retention), but awareness_level resets

5. **Integration Pattern**: DaveyJones composes TamPsyche and TamNotebook rather than inheriting, following composition over inheritance

6. **Goal System**: "Uncover the Truth" is both literal (find file) and metaphorical (understand cosmology)

## Dependencies

- Existing: `TamPsyche`, `TamNotebook`, `DnD5eCharacter`
- New: JSON parsing for TheTruth.json
- File system: Path operations for search

## Success Criteria

1. ✅ Realms structure created: `Realms/[Universe]/Earth/` exists
2. ✅ Theory of mind: Tam's thoughts are processed and recorded by system
3. ✅ Access control: Tier-based restrictions enforced on file system operations
4. ✅ DaveyJones class can be instantiated in Realms structure
5. ✅ Epiphany system unlocks tiers based on data collection (including thoughts)
6. ✅ Remember/forget state machine transitions correctly
7. ✅ File system search finds TheTruth.json (within access limits)
8. ✅ Integration with TamPsyche and TamNotebook works
9. ✅ Cosmology narrative elements are accessible through tiers
10. ✅ Core goal "Uncover the Truth" is trackable and completable
11. ✅ Probing mechanisms verify correct engineering direction