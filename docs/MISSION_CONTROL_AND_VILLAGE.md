# Mission Control & The Village

**Inspired by Avatar and Fern Gully**

Two complementary Pantheon entities for coordinating work: Mission Control (structured, command-center style) and The Village (organic, community-based).

---

## Overview

### Mission Control 🎯
**Inspired by:** Avatar's human base operations, Fern Gully's fairy coordination

A centralized command center for coordinating missions, monitoring operations, and providing real-time oversight. Works seamlessly with Military Brass to track serious, structured work.

**Features:**
- Real-time mission monitoring
- Status tracking and alerts
- Command interface for mission operations
- Telemetry and operational data
- Automatic registration when missions are created

### The Village 🌳
**Inspired by:** Avatar's Na'vi village, Fern Gully's fairy community

A community space for organic coordination, sharing, and collective wisdom. Works seamlessly with Fae to coordinate whimsical, open-ended quests.

**Features:**
- Community gatherings for coordination
- Quest sharing and discovery
- Connection tracking between beings
- Collective wisdom and insights
- Organic collaboration patterns

---

## Architecture

### Mission Control Structure

```
_pantheon/mission_control/
├── control_registry.json      # Central registry
├── status/                     # Mission status files
│   └── {mission_id}_status.json
├── commands/                   # Issued commands
│   └── cmd_{timestamp}.json
└── telemetry/                  # Telemetry data
```

### The Village Structure

```
_pantheon/the_village/
├── village_registry.json       # Central registry
├── gatherings/                 # Community gatherings
│   └── gathering_{timestamp}.json
├── connections/                # Being connections
│   └── conn_{timestamp}.json
└── wisdom/                     # Collective wisdom
    └── wisdom_{timestamp}.json
```

---

## Integration

### Automatic Integration

**Missions → Mission Control:**
- When `MilitaryBrass.create_mission()` is called, the mission is automatically registered with Mission Control
- Mission Control begins monitoring the mission immediately
- Status updates can be sent to Mission Control at any time

**Quests → The Village:**
- When `Fae.create_quest()` is called, the quest is automatically shared with The Village
- The Village tracks the quest for community coordination
- Beings can discover and collaborate on shared quests

---

## Usage

### Mission Control

#### Python API

```python
from pathlib import Path
from waft.pantheon import MissionControl

# Initialize
mission_control = MissionControl(project_path=Path.cwd())

# Register a mission (usually automatic via Military Brass)
mission_control.register_mission("mission_20260115_081838_test")

# Update mission status
mission_control.update_status(
    mission_id="mission_20260115_081838_test",
    status="active",
    progress=0.5,
    alerts=["High priority task pending"],
    telemetry={"cpu_usage": 45.2, "memory_mb": 1024}
)

# Get mission status
status = mission_control.get_status("mission_20260115_081838_test")

# Get all mission statuses
all_status = mission_control.get_all_status()

# Issue a command
command = mission_control.issue_command(
    mission_id="mission_20260115_081838_test",
    command="prioritize",
    parameters={"priority": "high"}
)

# Get control summary
summary = mission_control.get_control_summary()
```

#### CLI Commands

```bash
# View all mission statuses
python scripts/mission_control_status.py status

# View specific mission
python scripts/mission_control_status.py status --mission mission_20260115_081838_test

# View control summary
python scripts/mission_control_status.py status --summary

# Issue a command
python scripts/mission_control_status.py command mission_20260115_081838_test halt
python scripts/mission_control_status.py command mission_20260115_081838_test prioritize --params '{"priority": "high"}'
```

### The Village

#### Python API

```python
from pathlib import Path
from waft.pantheon import TheVillage

# Initialize
village = TheVillage(project_path=Path.cwd())

# Create a gathering
gathering = village.create_gathering(
    topic="Quest Coordination",
    description="Discussing shared quest strategies",
    participants=["being_1", "being_2"]
)

# Add an insight to a gathering
village.add_insight(
    gathering_id="gathering_20260115_120000",
    insight="We should coordinate on discovery quests",
    contributor="being_1"
)

# Create a connection between beings
connection = village.create_connection(
    from_being="being_1",
    to_being="being_2",
    connection_type="collaboration",
    strength=0.8
)

# Share a quest (usually automatic via Fae)
village.share_quest(quest_id="quest_20260115_120000", shared_by="fae")

# Add to collective wisdom
wisdom = village.add_wisdom(
    wisdom="The best discoveries come from unexpected paths",
    source="fae"
)

# Get village summary
summary = village.get_village_summary()
```

#### CLI Commands

```bash
# View village summary
python scripts/village_status.py status --summary

# View all active gatherings
python scripts/village_status.py status

# View specific gathering
python scripts/village_status.py status --gathering gathering_20260115_120000

# Create a gathering
python scripts/village_status.py gathering "Quest Coordination" "Discussing shared quest strategies" --participants "being_1,being_2"

# Add an insight
python scripts/village_status.py insight gathering_20260115_120000 "We should coordinate on discovery quests" --contributor "being_1"

# Add wisdom
python scripts/village_status.py wisdom "The best discoveries come from unexpected paths" --source "fae"
```

---

## Mission Status

Mission status can be:
- `monitoring` - Mission Control is monitoring, waiting for activity
- `active` - Mission is actively in progress
- `critical` - Mission requires immediate attention
- `completed` - Mission completed successfully
- `aborted` - Mission was aborted

## Village Gatherings

Gatherings are community coordination events where beings can:
- Share insights and discoveries
- Coordinate on quests
- Build connections
- Contribute to collective wisdom

Gathering status:
- `active` - Gathering is ongoing
- `completed` - Gathering concluded
- `archived` - Gathering archived

---

## Commands

### Mission Control Commands

Available commands for missions:
- `halt` - Pause mission execution
- `resume` - Resume mission execution
- `prioritize` - Change mission priority
- `update_status` - Update mission status
- `request_telemetry` - Request telemetry data

### Village Operations

Village operations are more organic:
- **Gatherings** - Community coordination events
- **Connections** - Track relationships between beings
- **Wisdom** - Collective knowledge and insights
- **Quest Sharing** - Discover and collaborate on quests

---

## Philosophy

### Mission Control (Left Brain)
- **Structured**: Clear hierarchy, defined roles
- **Precise**: Exact status tracking, telemetry
- **Command-Driven**: Issue commands, get responses
- **Accountable**: Full audit trail, documented operations

### The Village (Right Brain)
- **Organic**: Natural flow, emergent patterns
- **Collaborative**: Shared wisdom, collective insights
- **Connection-Based**: Relationships matter
- **Discovery-Oriented**: Open-ended exploration

---

## Examples

### Example: Mission Monitoring

```python
# Mission is created (auto-registered with Mission Control)
from waft.pantheon import MilitaryBrass, MissionControl

brass = MilitaryBrass()
mission = brass.create_mission(
    name="Secure Authentication",
    objective="Implement secure authentication system",
    success_criteria=["OAuth2 working", "Tests pass", "Documentation complete"]
)

# Mission Control automatically begins monitoring
# Update status as mission progresses
mission_control = MissionControl()
mission_control.update_status(
    mission_id=mission.mission_id,
    status="active",
    progress=0.3,
    telemetry={"tickets_completed": 2, "tickets_total": 6}
)

# Issue command if needed
mission_control.issue_command(
    mission_id=mission.mission_id,
    command="prioritize",
    parameters={"priority": "high"}
)
```

### Example: Village Gathering

```python
# Quest is created (auto-shared with The Village)
from waft.pantheon import Fae, TheVillage

fae = Fae()
quest = fae.create_quest(
    name="Explore New Patterns",
    description="Discover interesting design patterns in the codebase"
)

# The Village automatically shares the quest
# Create a gathering to coordinate
village = TheVillage()
gathering = village.create_gathering(
    topic="Pattern Discovery",
    description="Coordinating on pattern exploration quest",
    participants=["being_1", "being_2"]
)

# Add insights as discoveries are made
village.add_insight(
    gathering_id=gathering["gathering_id"],
    insight="Found interesting observer pattern usage",
    contributor="being_1"
)

# Add to collective wisdom
village.add_wisdom(
    wisdom="Patterns emerge when you look for them",
    source="being_1"
)
```

---

## Integration with Quest/Mission System

Mission Control and The Village integrate seamlessly with the Quest/Mission system:

1. **Missions** → Automatically registered with **Mission Control**
2. **Quests** → Automatically shared with **The Village**
3. **Status Updates** → Flow to appropriate system
4. **Coordination** → Happens in the appropriate space

This creates a complete ecosystem:
- **Missions** (Military Brass) → **Mission Control** (Command Center)
- **Quests** (Fae) → **The Village** (Community)

---

## Storage

Both systems use file-based storage following "as above, so below" principles:
- **As Above**: Pantheon entities coordinating in the spiritual realm
- **So Below**: JSON files organizing data in the filesystem

All data is:
- Human-readable (JSON format)
- Git-friendly (text files)
- Portable (no database dependencies)
- Traceable (full history in files)

---

## Future Enhancements

Potential future features:
- **Mission Control**: Real-time WebSocket updates, dashboard UI
- **The Village**: Visual connection graphs, wisdom search
- **Integration**: Cross-system coordination, hybrid missions/quests
- **Analytics**: Mission success rates, village collaboration patterns

---

**Mission Control and The Village work together to provide both structured coordination (left brain) and organic collaboration (right brain), creating a complete ecosystem for managing work in WAFT.**
