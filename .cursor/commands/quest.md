# /quest - Create Whimsical Quest (Fae-Guided)

**Purpose:** Create an open-ended, whimsical Quest guided by the Fae. Perfect for exploratory, creative, or open-ended work where the outcome is uncertain.

**Usage:** `/quest [description]` or automatic hook when plans are created

---

## Overview

This command creates a Quest object for open-ended, whimsical work. The Fae guide these quests, bringing creativity, wonder, and unexpected paths. Quests are perfect when you're exploring, experimenting, or letting the work unfold naturally.

**Perfect for:**
- Exploratory work with uncertain outcomes
- Creative projects that need room to breathe
- Experimental features
- Open-ended research
- Whimsical side projects
- "Let's see what happens" work

**Philosophy:**
- **Left Brain**: Missions (structured, serious, documented)
- **Right Brain**: Quests (whimsical, open-ended, creative)

---

## How It Works

### Fae-Guided Creation

When a quest is created, the Fae weave their magic:

1. **Fae Blessing**: The Fae bless the quest with creativity and wonder
2. **Open-Ended Structure**: Quest allows for exploration and discovery
3. **Whimsical Rewards**: Rewards include magical items, inspiration, and serendipity
4. **Flexible Completion**: Quest can evolve and change as you explore
5. **Fae Registry**: Quest registered in Fae realm (TavernKeeper with Fae metadata)

### Quest Structure

The Quest object created includes:

```python
{
    "id": "quest_[unique_id]",
    "name": "[Quest Name]",
    "type": "whimsical",  # Quest type
    "status": "active",
    "description": "[Open-ended description]",
    "fae_guidance": "[Fae blessing/guidance]",
    "difficulty": [1-10],  # Flexible, can change
    "win_condition": "exploration_complete",  # Open-ended
    "loot_table": {
        "xp": [calculated],
        "inspiration": [calculated],
        "serendipity": [calculated],
        "magical_items": [random]
    },
    "plan_path": "[path/to/plan.md]",  # If from plan
    "fae_realm": "active",  # Fae tracking
    "created_at": "[timestamp]",
    "progress": "exploring"
}
```

---

## Manual Usage

### Create Quest from Description

```bash
/quest "Explore new UI patterns for the dashboard"
```

Creates a whimsical quest for open-ended exploration.

### Create Quest from Plan

```bash
/quest --from-plan _work_efforts/Plans/feature_x.plan.md
```

Creates a quest from an existing plan (if outcome is open-ended).

### Create Quest with Fae Guidance

```bash
/quest "Build something beautiful" --fae-guidance "Let creativity flow"
```

Creates a quest with explicit Fae blessing.

---

## Quest Characteristics

### Whimsical Nature

- **Open-Ended**: No strict completion criteria
- **Evolving**: Quest can change as you explore
- **Creative**: Encourages experimentation
- **Flexible**: Adapts to discoveries
- **Wonder-Filled**: Brings joy and curiosity

### Fae Guidance

The Fae provide:
- **Inspiration**: Creative sparks and ideas
- **Serendipity**: Unexpected discoveries
- **Wonder**: Sense of magic and possibility
- **Flexibility**: Ability to pivot and explore
- **Joy**: Fun and enjoyment in the work

### Rewards

Quest rewards are whimsical:
- **XP**: Experience points for exploration
- **Inspiration**: Creative energy and ideas
- **Serendipity**: Chance for unexpected discoveries
- **Magical Items**: Random creative tools or insights
- **Wonder**: Sense of accomplishment and joy

---

## Quest Lifecycle

1. **Created**: Quest created with Fae blessing
2. **Active**: Quest is active and ready for exploration
3. **Exploring**: Work is happening, discoveries being made
4. **Evolving**: Quest adapts to new discoveries
5. **Complete**: Quest naturally concludes (or evolves into new quest)
6. **Rewarded**: Fae distribute whimsical rewards

---

## Integration with Fae

### Fae Pantheon

The Fae are mythical beings in the Pantheon who guide whimsical work:
- **Domain**: Fae Realm (Creativity, Wonder, Exploration)
- **Aspect**: Whimsy, Creativity, Open-Ended Discovery
- **Connection**: Right brain, creative consciousness
- **Evolution**: Fae grow stronger with each quest completed

### Fae Registry

Quests are registered in the Fae realm:
- **Storage**: `_pantheon/fae/quests/`
- **Tracking**: Quest status, discoveries, evolution
- **Blessings**: Fae blessings and guidance recorded

---

## Example

### Creating a Quest

```
/quest "Explore new ways to visualize data"
```

### Generated Quest

```json
{
  "id": "quest_explore_data_viz_abc123",
  "name": "Explore New Ways to Visualize Data",
  "type": "whimsical",
  "status": "active",
  "description": "Explore new ways to visualize data - let creativity guide the path",
  "fae_guidance": "The Fae whisper: 'Follow the colors, let patterns emerge, discover beauty in the data'",
  "difficulty": 5,
  "win_condition": "exploration_complete",
  "loot_table": {
    "xp": 50,
    "inspiration": 30,
    "serendipity": 20,
    "magical_items": ["Color Palette Insight", "Pattern Recognition"]
  },
  "fae_realm": "active",
  "created_at": "2026-01-15T08:00:00",
  "progress": "exploring"
}
```

---

## Quest vs Mission

### Use Quest When:
- ✅ Outcome is uncertain or open-ended
- ✅ You want to explore and discover
- ✅ Creative/experimental work
- ✅ "Let's see what happens" attitude
- ✅ Right brain, whimsical approach

### Use Mission When:
- ✅ Outcome is well-defined and serious
- ✅ Structured, documented approach needed
- ✅ Military-style precision required
- ✅ Left brain, analytical approach
- ✅ Serious documentation needed

---

## Integration Points

### Automatic Creation

When a plan is created with open-ended outcome:
1. Plan metadata indicates "whimsical" or "exploratory"
2. Quest is automatically created
3. Fae bless the quest
4. Quest registered in Fae realm

### Manual Creation

Use `/quest` command to create quests directly:
- For exploratory work
- For creative projects
- For experimental features
- For "let's see" work

---

## Fae Blessings

The Fae can provide:
- **Inspiration**: Creative ideas and sparks
- **Serendipity**: Unexpected discoveries
- **Guidance**: Gentle nudges in creative directions
- **Wonder**: Sense of magic and possibility
- **Joy**: Fun and enjoyment in the work

---

## Related Commands

- **`/mission`**: Create serious, structured missions (Military Brass)
- **`/plan-evolve`**: Creates plans (can become quests or missions)
- **`/quests`**: Lists and manages quests

---

**Quests are for whimsical, open-ended work guided by the Fae. Missions are for serious, structured work guided by Military Brass.**
