# FogSift Creature Mechanics

## Overview

Each device hosts a creature that lives, grows, and interacts. The system draws from tamagotchi simplicity while adding depth through the magnetic linking mechanic.

---

## Creature States

### Core Stats
| Stat | Range | Decay Rate | Effect |
|------|-------|------------|--------|
| **Hunger** | 0-100 | -5/hour | Below 20: mood drops, energy halved |
| **Energy** | 0-100 | -3/hour (awake) | Below 20: forced sleep |
| **Mood** | 0-100 | varies | Affects animations, interaction willingness |
| **Bond** | 0-100 | +1/interaction | Unlocks behaviors, evolutions |

### Derived States
- **Health**: f(hunger, energy, mood) - general wellbeing
- **Social**: increases when linked to other devices
- **Age**: time since hatching (affects evolution paths)

---

## Lifecycle

```
[Egg] → [Hatchling] → [Juvenile] → [Adult] → [Elder]
  │         │            │           │          │
  └─────────┴────────────┴───────────┴──────────┘
            Evolution triggers based on care quality
```

### Evolution Paths
Care quality during each stage influences evolution:
- **High care** → Healthy, social variants
- **Neglect** → Scraggly, independent variants
- **Specialized** → Feed certain foods, specific evolutions

---

## Interactions

### Solo Device
| Input | Action |
|-------|--------|
| Button A | Feed |
| Button B | Play mini-game |
| A + B | Status screen |
| Long press A | Light toggle |
| Long press B | Settings |

### Linked Devices
When two devices magnetically connect:

1. **Detection** (instant)
   - Pogo pins establish communication
   - Devices exchange creature data

2. **Meeting Animation** (2-3 seconds)
   - Creatures walk toward shared edge
   - Display edge pixels align

3. **Interaction Options**
   - **Play**: Joint mini-game, both creatures benefit
   - **Trade items**: Exchange food, toys
   - **Breed**: If compatible, create egg (requires third device or app)
   - **Battle**: Friendly competition, winner gains mood

4. **Passive Benefits**
   - Social stat increases while linked
   - Mood boost for both creatures
   - Landscape extends across screens

---

## Multi-Device Configurations

### 2 Devices (Linear)
```
┌─────┐┌─────┐
│  A  ││  B  │
└─────┘└─────┘
```
- Creatures can visit each other's screen
- Shared landscape (forest extends)

### 4 Devices (Grid)
```
┌─────┐┌─────┐
│  A  ││  B  │
├─────┤├─────┤
│  C  ││  D  │
└─────┘└─────┘
```
- Creates ecosystem
- Creatures roam freely across all screens
- Emergent group behaviors

### N Devices (Line)
```
┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐
│     ││     ││     ││     ││     │
└─────┘└─────┘└─────┘└─────┘└─────┘
```
- Panoramic landscape
- Creatures can "travel" long distances
- Migration patterns

---

## Creature Types

### Starter Creatures
| Name | Element | Personality |
|------|---------|-------------|
| **Pixel Fox** | Forest | Curious, playful |
| **Hoot** | Forest | Wise, nocturnal |
| **Splash** | Water | Energetic, social |
| **Ember** | Fire | Independent, fierce |

### Environment Affinity
Creatures prefer certain landscapes:
- **Forest creatures**: Thrive in wooded tiles
- **Water creatures**: Need pond/river tiles
- **Fire creatures**: Like warm/volcanic tiles

When placed in wrong environment: mood penalty, different animations

---

## Breeding & Genetics

### Compatibility
- Same element: 100% success, predictable offspring
- Adjacent elements: 75% success, hybrid possible
- Opposite elements: 25% success, rare hybrid

### Inheritance
```python
offspring_traits = {
    "color": weighted_random([parent_a.color, parent_b.color]),
    "pattern": mutate(random_choice([parent_a.pattern, parent_b.pattern])),
    "personality": blend(parent_a.personality, parent_b.personality),
    "element": inherit_or_mutate(parent_a.element, parent_b.element),
}
```

### Mutations
- 5% chance of random trait mutation
- Rare colors, patterns unlock through breeding
- Some mutations only appear in specific conditions

---

## Mini-Games

### Solo Games
1. **Feed Frenzy**: Catch falling food (reaction game)
2. **Pixel Jump**: Platformer obstacle course
3. **Memory Match**: Pattern memorization

### Linked Games
1. **Tug of War**: Button mashing competition
2. **Relay Race**: Creature runs across both screens
3. **Co-op Catch**: Pass object back and forth

---

## Items & Economy

### Food Types
| Item | Effect | Rarity |
|------|--------|--------|
| Berry | +10 hunger | Common |
| Fish | +20 hunger, +5 mood | Uncommon |
| Cake | +30 hunger, +15 mood, -5 energy | Rare |
| Golden Apple | Full restore | Legendary |

### Toys
- Increase mood when used
- Different creatures prefer different toys
- Can be traded between linked devices

### Currency
- **Pixels**: Earned through play, spent on items
- **Stardust**: Earned through linking, used for rare items

---

## WAFT Integration Points

### Pet System Module
```python
from waft.pet import PetBeing, EmotionAdapter

class FogSiftCreature(PetBeing):
    def __init__(self, species, traits):
        super().__init__()
        self.species = species
        self.traits = traits
        self.emotion = EmotionAdapter(self)

    def on_neighbor_detected(self, neighbor_creature):
        # Handle magnetic link event
        self.social += 10
        self.trigger_meeting_animation(neighbor_creature)
```

### Evolution System
- Leverage Scint Gym fitness concepts
- Creature "fitness" determines evolution path
- Can simulate generations before implementing in firmware

### Procedural Generation
- Use WAFT to generate new creature variants
- Test behavior patterns in simulation
- Export verified creatures to firmware

---

## Technical Notes

### State Persistence
- Save to flash every 5 minutes
- Save on power-off detection
- Creature survives battery death (up to X days)

### Clock
- RTC for accurate time tracking
- Day/night cycle affects creature behavior
- Events tied to real time (holidays, seasons)

### Display Rendering
- 8-bit color palette (256 colors)
- Sprite-based animation system
- 60fps target for smooth movement
- Dithering for gradients
