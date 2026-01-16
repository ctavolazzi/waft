# Quest/Mission System

## Overview

The Quest/Mission system provides two distinct approaches to work:

- **Quests** (Fae-Guided): Open-ended, whimsical, creative work (Right brain)
- **Missions** (Military Brass): Serious, structured, documented work (Left brain)

## Philosophy

### Left Brain vs Right Brain

- **Left Brain (Missions)**: Structured, analytical, documented, serious
- **Right Brain (Quests)**: Creative, exploratory, open-ended, whimsical

### Pantheon Integration

- **Fae**: Mythical beings guiding whimsical quests
- **Military Brass**: Serious beings overseeing structured missions

---

## Quests (Fae-Guided)

### Characteristics

- **Open-Ended**: No strict completion criteria
- **Whimsical**: Creative and playful
- **Exploratory**: Encourages discovery
- **Flexible**: Can evolve and change
- **Wonder-Filled**: Brings joy and curiosity

### When to Use

- ✅ Outcome is uncertain or open-ended
- ✅ You want to explore and discover
- ✅ Creative/experimental work
- ✅ "Let's see what happens" attitude
- ✅ Right brain, whimsical approach

### Fae Guidance

The Fae provide:
- **Inspiration**: Creative sparks and ideas
- **Serendipity**: Unexpected discoveries
- **Wonder**: Sense of magic and possibility
- **Flexibility**: Ability to pivot and explore
- **Joy**: Fun and enjoyment in the work

### Usage

```bash
# Create quest from description
/quest "Explore new UI patterns"

# Create quest from plan
/quest --from-plan _work_efforts/Plans/feature_x.plan.md

# CLI
python scripts/create_quest.py "Explore new UI patterns"
```

---

## Missions (Military Brass)

### Characteristics

- **Structured**: Clear objectives and success criteria
- **Documented**: Comprehensive mission documentation
- **Accountable**: Full tracking and reporting
- **Precise**: Measurable outcomes and metrics
- **Professional**: Military-style organization

### When to Use

- ✅ Outcome is well-defined and serious
- ✅ Structured, documented approach needed
- ✅ Military-style precision required
- ✅ Left brain, analytical approach
- ✅ Serious documentation needed
- ✅ Accountability and tracking critical

### Military Brass Oversight

The Military Brass provide:
- **Structure**: Clear organization and planning
- **Accountability**: Tracking and reporting
- **Documentation**: Comprehensive mission records
- **Precision**: Measurable objectives and criteria
- **Professionalism**: Serious, structured approach

### Mission PDF

Every mission generates a professional PDF:
- **Mission Briefing**: Comprehensive briefing document
- **Objective**: Clear mission objective
- **Plan**: Detailed mission plan
- **Success Criteria**: Measurable success metrics
- **Timeline**: Mission timeline and milestones
- **Resources**: Required resources and dependencies
- **Classification**: Security classification if applicable

### Usage

```bash
# Create mission from objective
/mission "Implement secure authentication system"

# Create mission with success criteria
/mission "Deploy production system" --success-criteria "System deployed" "Tests passing"

# Create mission from plan
/mission --from-plan _work_efforts/Plans/security_feature.plan.md

# CLI
python scripts/create_mission.py "Implement secure authentication" --success-criteria "OAuth2 working" "Tests passing"
```

---

## Language Style

### Quests (Fae)

- Whimsical and playful language
- "The Fae whisper..."
- "May your path be filled with wonder"
- Creative and inspiring
- Open-ended and flexible

### Missions (Military Brass)

- Soft military language (NCIS TV style)
- "Mission briefing prepared"
- "Objective defined and approved"
- "Mission status: In progress"
- "Mission complete - debriefing scheduled"
- Professional but approachable
- Clear and direct
- Respectful and structured

---

## Automatic Plan Detection

When a plan is created, the system automatically determines if it should be a quest or mission:

### Mission Indicators (Serious)

- Keywords: secure, security, production, deploy, critical, compliance
- Has success criteria
- Many structured todos (>5)
- Explicit "mission" or "serious" type

### Quest Indicators (Whimsical)

- Keywords: explore, experiment, discover, creative, whimsical
- Open-ended description
- Few todos or vague objectives
- Explicit "quest" or "whimsical" type

---

## Integration

### Pantheon Gods

- **Fae** (`src/waft/pantheon/fae.py`): Guides whimsical quests
- **Military Brass** (`src/waft/pantheon/military_brass.py`): Oversees serious missions

### Storage

- **Quests**: `_pantheon/fae/quests/`
- **Missions**: `_pantheon/military_brass/missions/`
- **Mission PDFs**: `_pantheon/military_brass/missions/*.pdf`
- **Briefings**: `_pantheon/military_brass/briefings/`

### Automatic Hooks

When plans are created:
1. Plan type is determined (quest vs mission)
2. Appropriate entity (Fae or Military Brass) creates quest/mission
3. Quest registered in Fae realm or Mission PDF generated
4. System tracks progress and completion

---

## Commands

### Quest Commands

- `/quest [description]` - Create whimsical quest
- `/quest --from-plan [path]` - Create quest from plan
- `python scripts/create_quest.py [description]` - CLI quest creation

### Mission Commands

- `/mission [objective]` - Create serious mission
- `/mission --from-plan [path]` - Create mission from plan
- `python scripts/create_mission.py [objective]` - CLI mission creation

---

## Examples

### Quest Example

```
/quest "Explore new ways to visualize data"
```

**Result**: Whimsical quest with Fae guidance, open-ended exploration, creative rewards.

### Mission Example

```
/mission "Implement secure authentication system" --success-criteria "OAuth2 working" "Tests passing" "Documentation complete"
```

**Result**: Serious mission with Military Brass oversight, mission PDF, structured tracking, professional documentation.

---

## Summary

- **Quests** = Right brain, Fae-guided, whimsical, open-ended
- **Missions** = Left brain, Military Brass, serious, structured
- **Automatic Detection** = System determines quest vs mission from plan characteristics
- **Pantheon Integration** = Fae and Military Brass are part of the Pantheon
- **Documentation** = Missions get PDFs, Quests get Fae blessings

**Choose Quest for exploration, Mission for precision.**
