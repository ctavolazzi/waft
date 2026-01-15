# AI DM System Architecture

**Work Effort**: WE-260113-wfbu  
**Date**: 2026-01-13  
**Status**: Design Phase

---

## Vision

Create an AI Dungeon Master system that orchestrates WAFT tools to run D&D 5e campaigns, generate branching narratives, make data-driven decisions, analyze campaign outcomes, and automatically create story booklets from campaign data.

---

## Core Concept

The AI DM is an orchestrator that uses:
1. **HannaCLI Scenario Engine** - Branching narratives and choices
2. **Decision Matrix System** - Data-driven campaign decisions
3. **Scientific Method Tool** - Campaign analysis and hypothesis testing
4. **Being System** - Player characters and NPCs
5. **D&D 5e Engine** - Game mechanics and rules
6. **PDF Generator** - Story booklet creation from any data

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      AI DM System                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Campaign Orchestrator                        │  │
│  │  - Session management                                     │  │
│  │  - State tracking                                        │  │
│  │  - Tool coordination                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                          │                                       │
│        ┌─────────────────┼─────────────────┐                   │
│        │                 │                 │                   │
│        ▼                 ▼                 ▼                   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                │
│  │ Scenario │    │ Decision │    │Scientific│                │
│  │  Engine  │    │  Matrix  │    │  Method  │                │
│  │(HannaCLI)│    │  System  │    │   Tool   │                │
│  └──────────┘    └──────────┘    └──────────┘                │
│        │                 │                 │                   │
│        └─────────────────┼─────────────────┘                   │
│                          │                                       │
│                          ▼                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Story Booklet Generator                     │  │
│  │  - Campaign data → Markdown                              │  │
│  │  - API documentation generation                         │  │
│  │  - PDF creation                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Supporting Systems                           │
├─────────────────────────────────────────────────────────────────┤
│  - Being System (PCs & NPCs)                                    │
│  - D&D 5e Engine (mechanics)                                    │
│  - PDF Generator (output)                                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Campaign Orchestrator

**Purpose**: Central coordinator for all campaign activities

**Responsibilities**:
- Manage campaign sessions
- Track campaign state
- Coordinate tool usage
- Generate story booklets
- Handle player interactions

**Key Methods**:
```python
class CampaignOrchestrator:
    def start_campaign(self, config: CampaignConfig) -> Campaign
    def run_session(self, campaign_id: str) -> Session
    def make_dm_decision(self, context: DecisionContext) -> Decision
    def generate_story_booklet(self, campaign_id: str) -> Path
    def analyze_campaign(self, campaign_id: str) -> Analysis
```

### 2. Scenario Engine Integration (HannaCLI)

**Purpose**: Provide branching narratives and player choices

**Integration**:
- Load scenario JSON files
- Execute sequences
- Process player choices
- Track container state
- Generate narrative events

**Usage in Campaign**:
```python
# Load campaign scenario
scenario = ScenarioEngine.load("campaign_scenario.json")

# Run sequence
sequence = scenario.run_sequence("tavern_encounter")

# Process player choice
next_sequence = scenario.make_choice("seq_001", "A")

# Track state
containers = scenario.containers  # inventory, clues, etc.
```

**Campaign Integration**:
- Scenarios define campaign structure
- Choices create branching paths
- Containers track campaign state
- Outcomes feed into story generation

### 3. Decision Matrix System Integration

**Purpose**: Make data-driven DM decisions

**Integration**:
- Use for NPC decisions
- Use for campaign direction choices
- Use for encounter balancing
- Use for story branching decisions

**Usage in Campaign**:
```python
from waft.core.decision_cli import DecisionCLI

# DM needs to decide: Which encounter next?
decision = DecisionCLI()
result = decision.run_decision_matrix(
    problem="Which encounter should happen next?",
    alternatives=["Combat", "Social", "Exploration", "Mystery"],
    criteria={
        "player_energy": 0.3,
        "story_progression": 0.4,
        "character_development": 0.3
    },
    scores={
        "Combat": {"player_energy": 8, "story_progression": 6, "character_development": 5},
        "Social": {"player_energy": 6, "story_progression": 9, "character_development": 8},
        # ...
    }
)

# Use recommendation
next_encounter = result["recommendation"]  # e.g., "Social"
```

**Campaign Integration**:
- NPCs use decision matrices for choices
- DM uses for campaign pacing
- Story branching decisions
- Encounter selection

### 4. Scientific Method Tool Integration

**Purpose**: Analyze campaign outcomes and test hypotheses

**Integration**:
- Test campaign hypotheses
- Analyze player behavior
- Measure campaign success
- Track campaign metrics

**Usage in Campaign**:
```python
from scientific_method_tool import Hypothesis, ExperimentManager

# Hypothesis: "Players prefer social encounters over combat"
hypothesis = Hypothesis(
    statement="Players prefer social encounters over combat",
    prediction="Social encounters will have higher engagement scores"
)

# Create experiment
manager = ExperimentManager()
experiment = manager.create_experiment(hypothesis)

# Capture initial state (A)
initial_state = manager.capture_state(experiment.id, "initial")

# Run campaign session
session_results = run_campaign_session()

# Collect data (C)
manager.collect_data(experiment.id, "engagement", session_results["engagement"])
manager.collect_data(experiment.id, "encounter_type", session_results["encounter_type"])

# Capture final state (B)
final_state = manager.capture_state(experiment.id, "final")

# Analyze
analysis = manager.analyze(experiment.id)
# Use results to improve campaign
```

**Campaign Integration**:
- Test campaign design hypotheses
- Analyze player preferences
- Measure campaign effectiveness
- Optimize campaign pacing

### 5. Story Booklet Generator

**Purpose**: Generate comprehensive booklets from campaign data

**Features**:
- Campaign story narrative
- Character profiles
- Session summaries
- Decision logs
- API documentation (for campaign APIs)
- Public API usage guides
- Statistics and analysis

**Input Data Sources**:
- Campaign state
- Session logs
- Character data
- Decision matrices
- Scientific method results
- Scenario execution logs
- Being evolution data

**Output Structure**:
```markdown
# Campaign Booklet: [Campaign Name]

## Part I: Campaign Overview
- Campaign summary
- Setting and world
- Main characters

## Part II: Session Logs
- Session 1: [Summary]
- Session 2: [Summary]
- ...

## Part III: Character Development
- PC profiles
- NPC profiles
- Character arcs

## Part IV: Decisions Made
- Decision matrices used
- Choices made
- Outcomes

## Part V: Campaign Analysis
- Scientific method results
- Hypotheses tested
- Insights gained

## Part VI: API Documentation
- Campaign APIs
- Public API usage
- Integration guides

## Part VII: Statistics
- Campaign metrics
- Player engagement
- Story progression
```

### 6. Being System Integration

**Purpose**: Manage player characters and NPCs

**Integration**:
- PCs are Beings
- NPCs are Beings
- Character evolution tracked
- Skills and memories managed

**Usage**:
```python
from waft.core.being_system import BeingSystem

being_system = BeingSystem()

# Create PC
pc = being_system.spawn_being(
    reality_id="campaign_reality",
    skills={"investigation": 15.0, "persuasion": 12.0}
)

# Character makes decision
decision = pc.make_decision("investigation")

# Track evolution
pc.learn_skill("investigation", 2.0)
pc.add_memory("found_clue", {"clue": "mysterious_note"})
```

### 7. D&D 5e Engine Integration

**Purpose**: Handle game mechanics

**Integration**:
- Character creation
- Skill checks
- Combat resolution
- Dice rolling
- Ability modifiers

**Usage**:
```python
from waft.core.dnd5e import DnD5eCharacter, DnDRoller

# Create character from Being
character = DnD5eCharacter.from_being(pc)

# Skill check
roller = DnDRoller()
result = roller.ability_check(
    ability="intelligence",
    skill="investigation",
    character=character,
    dc=15
)
```

---

## Campaign Flow

### 1. Campaign Initialization

```python
# Create campaign
campaign = CampaignOrchestrator.start_campaign(
    CampaignConfig(
        name="The Mysterious Tavern",
        scenario_file="tavern_campaign.json",
        players=["Player1", "Player2"],
        difficulty="medium"
    )
)

# Create PCs
for player_name in campaign.players:
    pc = being_system.spawn_being(
        reality_id=campaign.id,
        skills=generate_character_skills()
    )
    campaign.add_pc(player_name, pc)
```

### 2. Session Execution

```python
# Start session
session = campaign.run_session()

# Load scenario sequence
scenario = ScenarioEngine.load(campaign.scenario_file)
sequence = scenario.run_sequence(session.current_sequence_id)

# Present choices to players
choices = sequence.get_choices()

# Players make choices
player_choice = get_player_input(choices)

# Process choice
outcome = scenario.make_choice(sequence.id, player_choice)

# DM decision: What happens next?
dm_decision = campaign.make_dm_decision(
    DecisionContext(
        current_state=scenario.containers,
        player_choices=[player_choice],
        campaign_pacing=session.pacing
    )
)

# Use decision matrix for DM choice
next_encounter = decision_matrix.run(
    problem="What encounter next?",
    alternatives=["combat", "social", "exploration"],
    criteria=dm_decision.criteria,
    scores=dm_decision.scores
)

# Update campaign state
session.add_event("encounter", next_encounter)
scenario.containers["campaign_state"].append(next_encounter)
```

### 3. Story Generation

```python
# After session
session.complete()

# Generate story booklet
booklet = campaign.generate_story_booklet(
    campaign_id=campaign.id,
    include_apis=True,  # Include API documentation
    include_analysis=True  # Include scientific method results
)

# Booklet includes:
# - Session narrative
# - Character development
# - Decisions made
# - API documentation
# - Campaign statistics
```

---

## Booklet Generator Design

### Universal Booklet Generator

**Purpose**: Generate booklets from ANY input data

**Features**:
- Auto-detect data structure
- Generate API documentation
- Create usage guides
- Include examples
- Generate PDF output

**API**:
```python
class BookletGenerator:
    def generate_from_data(
        self,
        data: Any,  # Any data structure
        title: str,
        output_path: Path,
        include_apis: bool = True,
        include_examples: bool = True
    ) -> Path:
        """
        Generate booklet from any input data.
        
        - Auto-detects data structure
        - Generates API documentation
        - Creates usage examples
        - Outputs PDF
        """
```

**Data Sources Supported**:
- JSON files
- Python objects
- API endpoints
- Database schemas
- Configuration files
- Campaign data
- Experiment results
- Decision matrices

**Output Sections**:
1. **Overview** - What is this data?
2. **Structure** - Data schema/structure
3. **API Documentation** - If applicable
4. **Usage Examples** - How to use
5. **Reference** - Complete reference
6. **Statistics** - If applicable

---

## Implementation Plan

### Phase 1: Core Orchestrator
1. Create `CampaignOrchestrator` class
2. Implement session management
3. Basic tool integration stubs

### Phase 2: Tool Integration
1. Integrate Scenario Engine (HannaCLI)
2. Integrate Decision Matrix System
3. Integrate Scientific Method Tool
4. Integrate Being System
5. Integrate D&D 5e Engine

### Phase 3: Booklet Generator
1. Create universal booklet generator
2. Implement API documentation generation
3. Implement data structure analysis
4. Implement PDF output

### Phase 4: Campaign Features
1. Campaign state management
2. Session tracking
3. Story generation
4. Decision logging

### Phase 5: AI DM Intelligence
1. DM decision-making logic
2. Campaign pacing algorithms
3. Encounter balancing
4. Story coherence

---

## File Structure

```
src/waft/campaign/
├── __init__.py
├── orchestrator.py          # CampaignOrchestrator
├── session.py               # Session management
├── dm_decision.py           # DM decision logic
├── booklet_generator.py     # Universal booklet generator
├── api_doc_generator.py     # API documentation generator
└── campaign_state.py        # Campaign state management

examples/campaigns/
├── tavern_campaign.json     # Sample campaign scenario
└── sample_campaign.py       # Example campaign

docs/
└── AI_DM_SYSTEM_GUIDE.md    # User guide
```

---

## Success Criteria

- [ ] Campaign orchestrator runs D&D 5e campaigns
- [ ] Scenario engine provides branching narratives
- [ ] Decision matrices guide DM choices
- [ ] Scientific method analyzes campaigns
- [ ] Booklet generator creates PDFs from any data
- [ ] API documentation auto-generated
- [ ] Campaign sessions tracked and logged
- [ ] Story booklets generated automatically
- [ ] All tools integrated and working together

---

**Next Steps**: Begin Phase 1 implementation
