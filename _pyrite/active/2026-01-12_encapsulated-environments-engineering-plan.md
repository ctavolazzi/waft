# Engineering Plan: Encapsulated Environments for Being Storytelling & Information Exchange

**Date**: 2026-01-12 11:40:00 PST  
**Status**: Draft  
**Work Effort**: WE-260112-z87p  
**Hypothesis**: [2026-01-12_being-storytelling-information-exchange.md](../hypothesis/2026-01-12_being-storytelling-information-exchange.md)

---

## Objective

Create encapsulated environments where evolving Beings tell each other Stories to relay Information about "How To Do Things" and "How To Understand What Things Are". Implement Scint as measurable Agreement between Beings, Arrow of Intent for harm tracking, and multi-layered environment simulation.

---

## Core Concepts

### 1. Scint as Agreement
- **Current**: Scint is energy (UNIFIED_GENESIS_PROTOCOL) or reality fracture (gym/rpg/scint.py)
- **New**: Scint measures Agreement between two Beings (0.0-1.0)
- **Calculation**: Based on aligned Intent, shared understanding, successful information exchange
- **Threshold**: High Scint (>0.7) = safe information exchange

### 2. Arrow of Intent
- **Direction**: Points from source Being to target destination
- **Purpose**: Tracks where harm/intent is directed
- **Alignment**: When two Beings' Arrows point the same way = Agreement
- **Misalignment**: Different directions = need to resolve

### 3. Harm Class
- **Intentional Harm**: Being knowingly causes harm (Arrow points at target)
- **Unintentional Harm**: Being causes harm accidentally (Arrow misdirected)
- **No Harm**: Arrow doesn't cause harm, or harm is acceptable
- **Tracking**: Source Being, target, intent type, severity, direction

### 4. Story as Information Medium
- **Encoding**: Stories encode "How To Do Things" and "How To Understand"
- **Decoding**: Beings extract actionable information from stories
- **Agreement Required**: High Scint needed for successful decoding
- **Format**: Structured story with information payload

### 5. Encapsulated Environments
- **Isolation**: Each environment is self-contained
- **Stacking**: Environments can be layered (cosmic soup/foam/pond/puddle/ocean)
- **Interaction**: Internal (within environment) and external (between environments)
- **Simulation**: Run Being interactions, story exchanges, evolution

---

## Architecture

### Component 1: Harm Class (`src/waft/core/harm.py`)

```python
class ArrowOfIntent:
    """Direction of intent/harm from source to destination."""
    source_being_id: str
    destination: str  # Being ID, environment, or abstract target
    direction: Tuple[float, float, float]  # 3D vector
    intent_type: IntentType  # INTENTIONAL, UNINTENTIONAL, NEUTRAL
    severity: float  # 0.0-1.0
    timestamp: datetime

class Harm:
    """Tracks harm caused by Beings."""
    harm_id: str
    source_being_id: str
    target_being_id: Optional[str]
    arrow_of_intent: ArrowOfIntent
    harm_type: HarmType  # PHYSICAL, EMOTIONAL, INFORMATIONAL, SYSTEMIC
    severity: float
    intentional: bool
    resolved: bool
    timestamp: datetime
```

### Component 2: Scint as Agreement (`src/waft/core/agreement.py`)

```python
class Agreement:
    """Agreement measurement between two Beings using Scint."""
    being_a_id: str
    being_b_id: str
    scint_value: float  # 0.0-1.0 (Agreement level)
    intent_alignment: float  # Arrow alignment (0.0-1.0)
    shared_understanding: float  # Common knowledge (0.0-1.0)
    successful_exchanges: int  # Count of successful info exchanges
    last_updated: datetime

def calculate_agreement(being_a: Being, being_b: Being, 
                        harm_history: List[Harm]) -> float:
    """Calculate Scint/Agreement between two Beings."""
    # 1. Check Arrow of Intent alignment
    # 2. Measure shared understanding (common memories/lessons)
    # 3. Count successful information exchanges
    # 4. Factor in harm history (intentional harm reduces Agreement)
    # Return: 0.0-1.0 Scint value
```

### Component 3: Story Information Schema (`src/waft/core/story_information.py`)

```python
class StoryInformation:
    """Information encoded in a story."""
    story_id: str
    being_id: str  # Storyteller
    information_type: InformationType  # HOW_TO_DO, HOW_TO_UNDERSTAND
    payload: Dict[str, Any]  # Structured information
    encoding_method: str  # How information is encoded
    decoding_requirements: Dict[str, Any]  # What's needed to decode
    agreement_threshold: float  # Minimum Scint to decode

class InformationType(Enum):
    HOW_TO_DO = "how_to_do"  # Actionable instructions
    HOW_TO_UNDERSTAND = "how_to_understand"  # Conceptual knowledge
    META = "meta"  # Information about information
```

### Component 4: Encapsulated Environment (`src/waft/core/encapsulated_environment.py`)

```python
class EncapsulatedEnvironment:
    """Isolated environment for Being simulation."""
    environment_id: str
    beings: List[Being]
    stories: List[StoryInformation]
    agreement_matrix: Dict[Tuple[str, str], Agreement]  # Being pairs
    harm_history: List[Harm]
    layers: List['EncapsulatedEnvironment']  # Stacked environments
    simulation_state: Dict[str, Any]
    
    def run_simulation(self, cycles: int):
        """Run Being interactions for N cycles."""
        # 1. Beings tell stories
        # 2. Calculate Agreement (Scint) between pairs
        # 3. Exchange information if Agreement > threshold
        # 4. Track harm and Arrow of Intent
        # 5. Evolve Beings based on success/failure
        # 6. Handle misalignment reactions
```

### Component 5: Being Communication Protocol (`src/waft/core/being_communication.py`)

```python
class BeingCommunication:
    """Protocol for Being-to-Being information exchange."""
    
    def tell_story(self, storyteller: Being, story: str, 
                   information: StoryInformation) -> StoryEvent:
        """Being tells a story with encoded information."""
        
    def receive_story(self, receiver: Being, story: StoryInformation,
                     storyteller: Being) -> Dict[str, Any]:
        """Being receives and decodes story."""
        # 1. Check Agreement (Scint) with storyteller
        # 2. If Agreement > threshold: decode information
        # 3. If Agreement < threshold: information loss/misunderstanding
        # 4. Update Agreement based on success/failure
        # 5. Track harm if misunderstanding causes issues
        
    def exchange_information(self, being_a: Being, being_b: Being,
                            story: StoryInformation) -> ExchangeResult:
        """Attempt information exchange between two Beings."""
        # 1. Calculate current Agreement
        # 2. Check Arrow of Intent alignment
        # 3. Attempt exchange
        # 4. Update Agreement based on result
```

---

## Implementation Phases

### Phase 1: Foundation (Tickets 1-3)
**Goal**: Core classes and data structures

1. **Create Harm Class** (TKT-z87p-001)
   - Implement `ArrowOfIntent` class
   - Implement `Harm` class
   - Track intentional vs unintentional
   - Store in `_pyrite/harm/` directory

2. **Implement Scint as Agreement** (TKT-z87p-002)
   - Create `Agreement` class
   - Implement `calculate_agreement()` function
   - Integrate with existing Scint system
   - Store Agreement matrix

3. **Create Arrow of Intent System** (TKT-z87p-003)
   - Track intent direction
   - Calculate alignment between Beings
   - Visualize Arrow directions
   - Store in Being state

### Phase 2: Story Information System (Tickets 4-5)
**Goal**: Encode/decode information in stories

4. **Build Story Information Schema** (TKT-z87p-004)
   - Define `StoryInformation` class
   - Create encoding methods
   - Create decoding methods
   - Define information types

5. **Implement Information Encoding/Decoding** (TKT-z87p-005)
   - Encode "How To Do Things" in stories
   - Encode "How To Understand" in stories
   - Decode with Agreement threshold
   - Test encoding/decoding accuracy

### Phase 3: Environment Framework (Tickets 6-7)
**Goal**: Encapsulated environment simulation

6. **Build Encapsulated Environment Framework** (TKT-z87p-006)
   - Create `EncapsulatedEnvironment` class
   - Implement Being management
   - Implement story exchange protocols
   - Create simulation loop

7. **Implement Multi-Layered Environments** (TKT-z87p-007)
   - Support environment stacking
   - Handle internal/external interactions
   - Manage environment boundaries
   - Test stacked interactions

### Phase 4: Being Communication (Tickets 8-9)
**Goal**: Being-to-Being protocols

8. **Create Being Communication Protocol** (TKT-z87p-008)
   - Implement `tell_story()` method
   - Implement `receive_story()` method
   - Implement `exchange_information()` method
   - Handle Agreement checks

9. **Implement Misalignment Reactions** (TKT-z87p-009)
   - Detect misalignment
   - React to misalignment
   - Attempt resolution
   - Track resolution success

### Phase 5: Integration & Testing (Ticket 10)
**Goal**: Full system integration

10. **Integration & Testing** (TKT-z87p-010)
    - Integrate all components
    - Create end-to-end test
    - Run simulation with multiple Beings
    - Verify information exchange
    - Measure Agreement evolution
    - Test stacked environments

---

## Dependencies

### Existing Systems
- **Being System** (`src/waft/being.py`) - Beings with skills, memories, lessons
- **TheCampfire** (`src/waft/core/campfire.py`) - Storytelling infrastructure
- **Scint System** - Multiple implementations to integrate with
- **Work Efforts = Quests** - Quest system for tracking

### New Dependencies
- None (using existing systems)

---

## Success Criteria

1. ✅ **Harm Class**: Tracks intentional/unintentional harm with Arrow of Intent
2. ✅ **Scint as Agreement**: Measures 0.0-1.0 Agreement between Beings
3. ✅ **Story Encoding**: Stories encode "How To Do" and "How To Understand"
4. ✅ **Information Exchange**: Beings exchange information when Agreement > threshold
5. ✅ **Misalignment Handling**: System reacts to misaligned Intent
6. ✅ **Encapsulated Environments**: Isolated environments with Being simulation
7. ✅ **Stacked Environments**: Multi-layer environment interaction
8. ✅ **Evolution**: Beings evolve communication strategies through simulation

---

## Risks & Mitigations

### Risk 1: Scint Repurposing Breaks Existing Systems
**Mitigation**: 
- Create new `Agreement` class that uses Scint concept
- Don't modify existing Scint implementations
- Use composition, not modification

### Risk 2: Story Encoding Too Lossy
**Mitigation**:
- Start with structured information payload
- Test encoding/decoding accuracy
- Iterate on encoding methods

### Risk 3: Agreement Calculation Computationally Expensive
**Mitigation**:
- Cache Agreement values
- Update incrementally
- Use approximate algorithms

### Risk 4: Stacked Environments Too Complex
**Mitigation**:
- Start with single environment
- Add stacking incrementally
- Test at each layer

---

## Next Steps

1. **Review Plan**: Get feedback on architecture
2. **Start Phase 1**: Create Harm class
3. **Iterate**: Build incrementally, test frequently
4. **Document**: Update as we learn

---

**Plan Created**: 2026-01-12 11:40:00 PST  
**Last Updated**: 2026-01-12 11:40:00 PST
