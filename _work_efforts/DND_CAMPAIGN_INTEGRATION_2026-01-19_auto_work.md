# D&D Campaign Integration - Auto Work Algorithms

**Date**: 2026-01-19
**Time**: 03:00:00 PST
**Status**: ✅ **COMPLETE** - D&D campaign and quest PDF generation integrated

---

## Summary

The auto-work algorithms now **run a full D&D campaign** as they execute work efforts, generating **Quest Files** (PDFs) from markdown scenarios using Typst templates.

---

## D&D Campaign Integration

### Purpose

The D&D campaign system:
- Runs scenarios (encounters, exploration, lore building) during work execution
- Generates quest markdown from scenario results
- Creates beautiful quest PDFs using Typst templates
- Maintains campaign state and world lore
- Creates narrative adventures parallel to technical work

### Integration Points

**After Successful Action Execution**:
1. Run a D&D scenario (encounter/explore/lore)
2. Generate quest markdown from scenario result
3. Compile quest PDF using Typst templates
4. Save quest PDF to `_realms/dnd_scenario_realm/quests/`

---

## Quest PDF Generation

### Typst Templates Supported

#### 1. **Wenyuan Campaign Template** (Priority)
- **Template**: `@preview/wenyuan-campaign:0.1.2`
- **Initialization**: `typst init @preview/wenyuan-campaign:0.1.2`
- **Usage**: Campaign-style quest documents
- **Style**: Professional D&D campaign layout

#### 2. **D&D 5e Character Sheet Style**
- **Template**: `@preview/owlbear:0.0.1`
- **Usage**: Character sheet inspired layout
- **Style**: D&D 5e official character sheet aesthetic

#### 3. **Simple Template** (Fallback)
- **Usage**: When Typst packages unavailable
- **Style**: Clean, simple layout with New Computer Modern font

---

## Scenario Types

### 1. Encounter Scenario
- **Type**: Combat encounters
- **Generates**: Combat encounter with enemies, rounds, rewards
- **Quest Content**: Encounter details, difficulty, XP gained, level ups

### 2. Exploration Scenario
- **Type**: Location discovery
- **Generates**: New locations, exploration results
- **Quest Content**: Location details, discovery information, lore entries

### 3. Lore Building Scenario
- **Type**: NPCs and events
- **Generates**: NPC encounters or world events
- **Quest Content**: NPC/event details, lore entries, world history

---

## Quest Markdown Structure

Each quest PDF includes:

```markdown
# Quest Title

**Quest ID**: WE-260119-xxxx
**Generated**: 2026-01-19 03:00:00
**Scenario Type**: Encounter/Explore/Lore

## Quest Overview

Work effort execution context and scenario details.

### Work Effort Details
- Work Effort ID
- Status
- Priority
- Action Taken

## Scenario Details

### Combat Encounter / Exploration / Lore Building
- Scenario-specific details
- Rewards (XP, level ups)
- Discoveries (locations, NPCs, events)

## Quest Context

How the quest was created through autonomous work execution.
```

---

## Integration Flow

```
1. Execute Work Effort Action
   ├─> Validate action
   ├─> Create reasoning trace (TheReasoner)
   ├─> Evaluate safety (Judge)
   ├─> Check safety gate (Empirica)
   └─> Prepare execution instruction

2. If Success:
   ├─> Tell Story Around Campfire
   │   └─> Generate narrative PDF
   │
   └─> Run D&D Scenario
       ├─> Select scenario mode (encounter/explore/lore)
       ├─> Execute scenario
       ├─> Generate quest markdown
       ├─> Compile quest PDF with Typst
       └─> Save quest PDF

3. Return Result
   └─> Includes story + quest PDF metadata
```

---

## Quest PDF Generation Process

### Step 1: Run Scenario
```python
scenario_result = orchestrator.run_scenario(mode="encounter")
# Returns: encounter details, party state, rewards
```

### Step 2: Generate Quest Markdown
```python
quest_markdown = _generate_quest_markdown_from_scenario(
    scenario_result, work_effort, action
)
# Returns: Formatted markdown with quest details
```

### Step 3: Create Typst File
```typst
#import "@preview/wenyuan-campaign:0.1.2": *

#show: campaign.with(
  title: "Quest: Work Effort Title",
  date: "2026-01-19",
)

#let content = [
  // Converted markdown content
]

#content
```

### Step 4: Compile to PDF
```bash
typst compile --root templates/typst/dnd quest.typ quest.pdf
```

---

## Example Quest PDF

**Title**: "Quest: Implement User Authentication"

**Content**:
- Quest Overview: Work effort execution context
- Work Effort Details: ID, status, priority, action
- Scenario Details: Encounter with goblins, 3 rounds, 50 XP gained
- Rewards: Experience points, level ups
- Quest Context: How quest was created

**PDF Location**: `_realms/dnd_scenario_realm/quests/quest_Implement_User_Authentication_20260119_030000.pdf`

---

## Campaign State Management

### Scenario Realm
- **Location**: `_realms/dnd_scenario_realm/`
- **Structure**:
  - `lore/locations/` - Discovered locations
  - `lore/npcs/` - Encountered NPCs
  - `lore/events/` - World events
  - `encounters/` - Combat encounters
  - `quests/` - Generated quest PDFs
  - `campaigns/` - Campaign tracking
  - `party_state.json` - Party state

### Persistent State
- Party state saved after each scenario
- Lore entries accumulate over time
- Encounter history tracked
- Quest PDFs archived

---

## Algorithm Integration

### Modified Function: `execute_work_effort_action`

**New Parameter**:
- `dnd_campaign: Optional[Dict]` - D&D campaign system

**New Behavior**:
- After successful action preparation
- If `dnd_campaign` available
- Run random scenario (encounter/explore/lore)
- Generate quest markdown
- Compile quest PDF with Typst
- Add quest PDF metadata to result

### Modified Function: `main`

**New Behavior**:
- Initialize ScenarioRealm
- Initialize ScenarioOrchestrator
- Initialize QuestPDFGenerator
- Pass `dnd_campaign` to execution
- Display quest PDF information in output

---

## Output Example

```
🤔 Thinking about work efforts...

🔬 Empirica: Active and monitoring

⚡ Pantheon: Summoning entities for guidance...
  ✅ Magistrate (Precedent & Proof)
  ✅ Judge (Judgment & Evaluation)
  ✅ TheReasoner (Reasoning Traces)
  ✅ GitHubGod (Repository State)

🔥 Campfire: Ready for storytelling

⚔️  D&D Campaign: Initializing realm and quest system...
  ✅ Scenario Realm initialized
  ✅ Scenario Orchestrator ready
  ✅ Quest PDF Generator ready (Typst available)

🎯 Selected: WE-260119-auth (score: 198.5)
🚀 Action: Update status to 'in_progress'

✅ Successfully prepared action for work effort: WE-260119-auth

📋 Work Effort: Implement User Authentication
🎯 Action: Update status to 'in_progress'
💬 Command: Update work effort WE-260119-auth status to 'in_progress'

🔥 Story told around the campfire:
   📖 Story ID: story_20260119_030000
   📄 PDF: _pyrite/campfire/story_20260119_030000.pdf

⚔️  D&D Quest PDF generated:
   📜 Quest: Encounter Scenario
   📄 PDF: _realms/dnd_scenario_realm/quests/quest_Implement_User_Authentication_20260119_030000.pdf
```

---

## Typst Template Details

### Wenyuan Campaign Template

**Initialization**:
```bash
typst init @preview/wenyuan-campaign:0.1.2
```

**Usage in Typst**:
```typst
#import "@preview/wenyuan-campaign:0.1.2": *

#show: campaign.with(
  title: "Quest Title",
  date: "2026-01-19",
)
```

**Features**:
- Professional campaign layout
- Date tracking
- Structured content sections

### D&D 5e Character Sheet Style

**Usage**:
```typst
#import "@preview/owlbear:0.0.1": *

#set page(margin: 2cm)
#set text(font: "New Computer Modern", size: 11pt)
```

**Features**:
- Character sheet aesthetic
- D&D 5e styling
- Official look and feel

---

## Status

✅ **D&D Campaign is ACTIVE and INTEGRATED**

**Integration Points**:
- ✅ Action execution: Scenarios run after successful actions
- ✅ Quest generation: Markdown generated from scenario results
- ✅ PDF compilation: Typst templates used for quest PDFs
- ✅ Campaign state: Realm state persists across executions
- ✅ Lore building: World lore accumulates over time
- ✅ Empirica logging: Quest generation logged as findings

**The system now runs a full D&D campaign parallel to technical work, generating beautiful quest PDFs using Typst templates.**

---

**D&D Campaign integration complete - algorithms now generate quest PDFs from D&D scenarios.**
