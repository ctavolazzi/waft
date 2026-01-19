# Skurl: Demi-God of Red Tape

## Spiritual Role

Skurl is a gremlin demi-god who serves under the Paperwork God. As the demi-god of red tape, Skurl specializes in bureaucratic obstacles, form complications, and the intricate web of regulations that make simple tasks require multiple forms, approvals, and signatures.

## As Above, So Below

- **As Above**: Gremlin demi-god creating celestial red tape and bureaucratic complications
- **So Below**: System tracking bureaucratic obstacles and form complications in `_pantheon/paperwork_god/skurl/`

## Nature

Skurl is a **demi-god** - a lesser divine being who serves under a full god. As a gremlin, Skurl has a mischievous nature and takes delight in creating bureaucratic complications.

- **Type**: Gremlin
- **Domain**: Red Tape
- **Parent God**: Paperwork God
- **Power Level**: Demi-god (lesser than full god, but still divine)

## Red Tape Obstacles

Skurl creates red tape obstacles that complicate bureaucratic processes:

- **Required Forms**: Multiple forms that must be completed
- **Required Approvals**: Multiple approval steps from different authorities
- **Complexity Level**: 1-10 scale indicating how complex the obstacle is
- **Resolution**: Obstacles can be resolved when all requirements are met

## Usage

```python
from src.waft.pantheon import PaperworkGod, Skurl
from pathlib import Path

# Initialize Paperwork God (Skurl is created automatically)
paperwork_god = PaperworkGod(project_path=Path.cwd())
skurl = paperwork_god.skurl

# Create a red tape obstacle
obstacle = skurl.create_red_tape_obstacle(
    obstacle_id="obstacle_001",
    description="Application requires 3 forms and 2 manager approvals",
    required_forms=["form_001", "form_002", "form_003"],
    required_approvals=["manager_approval", "director_approval"],
    complexity_level=7
)

# Get obstacle
obstacle = skurl.get_obstacle("obstacle_001")

# List all obstacles
all_obstacles = skurl.list_all_obstacles()

# List only unresolved obstacles
unresolved = skurl.list_all_obstacles(unresolved_only=True)

# Resolve an obstacle
resolved = skurl.resolve_obstacle("obstacle_001")

# Get summary
summary = skurl.get_registry_summary()
```

## Storage

- **Red Tape Registry**: `_pantheon/paperwork_god/skurl/red_tape_registry.json`
- **Obstacles**: `_pantheon/paperwork_god/skurl/obstacles/`
