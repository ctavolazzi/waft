# D&D Campaign PDF Evolution - Complete Work Effort

**Generated:** 2026-01-12 17:01:52

---

## Table of Contents

1. [Work Effort Overview](#work-effort-overview)
2. [Player's Guide](#player's-guide)
3. [Dungeon Master's Guide](#dungeon-master's-guide)
4. [Encounter Reference](#encounter-reference)
5. [World Map & Locations](#world-map--locations)
6. [NPC Reference Cards](#npc-reference-cards)
7. [PDF Evolution Findings](#pdf-evolution-findings)
8. [Quality Analysis Results](#quality-analysis-results)
9. [Generated PDFs](#generated-pdfs)
10. [Code Examples](#code-examples)

---

# Work Effort Overview

---
id: WE-260112-jqkn
title: "D&D Campaign PDF Evolution"
status: active
created: 2026-01-12T16:47:08.000Z
created_by: ctavolazzi
last_updated: 2026-01-12T16:47:08.000Z
branch: feature/WE-260112-jqkn-d_d_campaign_pdf_evolution
repository: waft
---

# WE-260112-jqkn: D&D Campaign PDF Evolution

## Metadata
- **Created**: Monday, January 12, 2026 at 4:47:08 PM PST
- **Author**: ctavolazzi
- **Repository**: waft
- **Branch**: feature/WE-260112-jqkn-d_d_campaign_pdf_evolution

## Objective
Create a comprehensive D&D 5e campaign plan that serves as a testbed for evolving the PDF maker. Generate multiple campaign documents using different PDF generator features, styles, and layouts to identify improvements, test capabilities, and document evolution.

## Campaign: "The Shattered Crown"
A 3-act campaign (levels 1-5) focused on political intrigue and ancient magic.

## Documents to Generate
1. **Player's Guide** - Campaign introduction with premium styling
2. **Dungeon Master's Guide** - Complete campaign reference with clinical standard styling
3. **Encounter Sheets** - Quick reference with compact layout
4. **World Map Document** - Location guide with image integration
5. **NPC Reference Cards** - Quick NPC lookup with card-based layout

## Progress
- 1/12/2026: Work effort created. Starting campaign content creation.
- 1/12/2026: All 5 campaign documents created and PDFs generated.
- 1/12/2026: Quality analysis completed and findings documented.
- 1/12/2026: Evolution report generated.
- 1/12/2026: Work effort PDF generator tool created - converts entire work effort to comprehensive PDF.

## Commits
- (populated as work progresses)

## Related
- PDF Generator: `src/waft/evolution/pdf_generator.py`
- Scientific PDF Generator: `src/waft/evolution/scientific_pdf_generator.py`
- PDF Generation Script: `examples/generate_dnd_campaign_pdfs.py`

## Tools

### Work Effort PDF Generator
**File:** `generate_work_effort_pdf.py`

Converts the entire work effort into a comprehensive PDF document including:
- All markdown files (campaign content, findings, analysis)
- Generated PDFs (as references with file sizes)
- Screenshots/PNG files (as references)
- Analysis results (formatted from JSON)
- Code examples (all scripts used)
- Complete documentation

**Usage:**
```bash
python3 _work_efforts/WE-260112-jqkn_d_d_campaign_pdf_evolution/generate_work_effort_pdf.py
```

**Output:**
- `WE-260112-jqkn_COMPLETE.pdf` - Complete work effort PDF
- `WE-260112-jqkn_COMPLETE.md` - Intermediate markdown (for debugging)

**Features:**
- Automatically collects all content from work effort
- Formats analysis results from JSON
- Includes code examples
- References all generated PDFs and screenshots
- Uses ScientificPDFGenerator for quality analysis
- Premium styling for professional presentation

---

### Character Sheet Generator
**File:** `generate_character_sheet.py`

Generates D&D 5e character sheet PDFs in both blank (template) and filled formats.

**Usage:**
```bash
# Generate both blank and example filled sheets
python3 _work_efforts/WE-260112-jqkn_d_d_campaign_pdf_evolution/generate_character_sheet.py
```

**Output:**
- `character_sheet_blank.pdf` - Blank template for manual filling
- `character_sheet_[name].pdf` - Filled character sheet (example: Aldric the Brave)

**Features:**
- **Blank Template**: Complete D&D 5e character sheet with all standard fields
- **Filled Sheets**: Automatically calculates modifiers, skill bonuses, saving throws
- **Standard Format**: All D&D 5e fields included (abilities, skills, combat, equipment, etc.)
- **Customizable**: Pass character data dictionary to generate custom sheets
- **Clinical Standard Styling**: Clean, professional appearance

**Character Data Format:**
```python
character_data = {
    "name": "Character Name",
    "class": "Fighter",
    "level": 3,
    "abilities": {"STR": 16, "DEX": 13, "CON": 15, "INT": 10, "WIS": 12, "CHA": 11},
    "skill_proficiencies": ["Athletics", "Perception"],
    "attacks": [{"name": "Longsword", "bonus": 5, "damage": "1d8+3", ...}],
    # ... more fields
}
```

**Functions:**
- `generate_blank_sheet()` - Creates blank template
- `generate_filled_sheet(character_data)` - Creates filled sheet from data

---

### Being Character Sheet Generator
**File:** `src/waft/evolution/being_character_sheet_generator.py`

Generates D&D 5e character sheets for Beings in multiple formats:
- **.txt** (default, generated automatically when Being is created)
- **.md** (on demand)
- **.pdf** (on demand)

**Integration:**
- Automatically generates `.txt` character sheet when a Being is spawned via `BeingSystem.spawn_being()`
- Uses template with placeholders for key details
- Converts Being skills and attributes to D&D character stats
- Integrates with D&D 5e character system

**Usage:**

**Automatic (.txt generation):**
```python
from src.waft.being import BeingSystem

being_system = BeingSystem(project_path=project_path)
being = being_system.spawn_being(reality_id="my_reality")
# .txt character sheet automatically generated in:
# _hidden/.truth/beings/{being_id}/character_sheet.txt
```

**On Demand (.md and .pdf):**
```python
from src.waft.evolution.being_character_sheet_generator import (
    generate_character_sheet_md,
    generate_character_sheet_pdf
)

# Generate .md
md_path = generate_character_sheet_md(being, project_path=project_path)

# Generate .pdf
pdf_path = generate_character_sheet_pdf(being, project_path=project_path)
```

**Features:**
- **Template System**: Uses placeholders for key details
- **Being Integration**: Converts Being skills to D&D ability scores
- **Automatic Generation**: .txt created automatically on Being spawn
- **On-Demand Formats**: .md and .pdf generated only when requested
- **D&D 5e Compatible**: Full D&D 5e character sheet format
- **Being Data Mapping**: Maps Being personality, memories, skills to character sheet

**Template Placeholders:**
- `{NAME}`, `{CLASS_LEVEL}`, `{BACKGROUND}`, etc.
- `{STR}`, `{STR_MOD}`, `{STR_SAVE}`, etc. (all abilities)
- `{ACROBATICS}`, `{ATHLETICS}`, etc. (all skills)
- `{AC}`, `{HP}`, `{INITIATIVE}`, etc. (combat stats)
- `{BEING_ID}`, `{REALITY_ID}`, `{GENERATED_DATE}` (metadata)

**Functions:**
- `generate_character_sheet_txt(being, ...)` - Auto-called on spawn, generates .txt
- `generate_character_sheet_md(being, ...)` - On-demand, generates .md
- `generate_character_sheet_pdf(being, ...)` - On-demand, generates .pdf
- `being_to_character_data(being, character)` - Converts Being to character data
- `create_character_from_being(being)` - Creates D&D character from Being


---

# Player's Guide

*Source: campaign_players_guide.md*

# The Shattered Crown
## Player's Guide

**Campaign Type**: Political Intrigue & Ancient Magic  
**Level Range**: 1-5  
**Setting**: Kingdom of Aetheria  
**Tone**: Mystery, Intrigue, Adventure

---

## Welcome to Aetheria

The Kingdom of Aetheria stands as a beacon of civilization, but beneath its golden spires, shadows stir. Ancient magic weaves through the land, and political machinations threaten to tear the realm apart. You are about to embark on a journey that will test your wits, your courage, and your loyalty.

---

## Campaign Overview

### The Story So Far

The kingdom has been peaceful for generations, but recent events have shaken the foundations of power. The young heir to the throne has vanished under mysterious circumstances, and whispers of conspiracy echo through the halls of power. Ancient artifacts have begun to resurface, and dark forces move in the shadows.

### Your Role

You are adventurers drawn into a web of intrigue that spans from the smallest village to the highest halls of power. Whether you seek justice, power, knowledge, or simply adventure, your actions will shape the fate of Aetheria.

---

## Character Creation Guidelines

### Starting Level
Characters begin at **Level 1**.

### Allowed Sources
- Player's Handbook
- Xanathar's Guide to Everything
- Tasha's Cauldron of Everything
- Other sources with DM approval

### Character Hooks

Choose one of the following backgrounds or create your own:

| Background | Connection |
|-----------|-----------|
| **Noble** | You have ties to the royal court or noble houses |
| **Criminal** | You have information about the conspiracy |
| **Sage** | You study ancient magic and artifacts |
| **Soldier** | You served in the royal guard or military |
| **Acolyte** | You serve a temple or religious order |
| **Folk Hero** | You're from Millbrook and know the missing heir |

### Starting Equipment
- Standard starting equipment from your class
- 50 gold pieces
- One trinket from your background

---

## The Kingdom of Aetheria

### Geography

Aetheria is a diverse kingdom with several distinct regions:

**The Capital City** - The heart of the kingdom, where politics and power converge  
**Millbrook** - A peaceful village where the campaign begins  
**Whispering Woods** - Ancient forest filled with mystery  
**The Northern Mountains** - Home to ancient temples and forgotten ruins  
**The Eastern Plains** - Fertile farmland and trade routes

### Major Factions

| Faction | Alignment | Goals |
|---------|----------|-------|
| **The Crown** | Lawful Good | Maintain order and protect the realm |
| **The Shadow Council** | Lawful Evil | Seize power through manipulation |
| **The Keepers** | Neutral Good | Preserve ancient knowledge |
| **The Free Blades** | Chaotic Good | Fight corruption and injustice |
| **The Cult of the Shattered Crown** | Chaotic Evil | Resurrect dark powers |

---

## Campaign Themes

### Political Intrigue
The campaign features complex political relationships. Your words and actions have consequences. Choose your allies carefully.

### Ancient Magic
Powerful artifacts and forgotten magic play a central role. Research and investigation will be rewarded.

### Mystery and Investigation
Not everything is as it seems. Clues are hidden throughout the world. Pay attention to details.

### Moral Complexity
There are no purely good or evil choices. Every decision has shades of gray.

---

## Starting the Campaign

### Session Zero
We'll begin in the **Village of Millbrook**, where you'll receive your first quest. The local lord's son has disappeared, and you've been called upon to investigate.

### What to Expect

- **Exploration**: Discover new locations and uncover secrets
- **Combat**: Face dangerous creatures and hostile forces
- **Social Interaction**: Negotiate, persuade, and deceive
- **Investigation**: Follow clues and solve mysteries
- **Roleplay**: Develop your character's story

---

## House Rules

### Inspiration
Inspiration can be awarded for excellent roleplay, creative problem-solving, or advancing the story in interesting ways.

### Critical Hits
On a critical hit, roll damage dice twice and add modifiers once.

### Flanking
When two allies flank an enemy, both gain advantage on attack rolls.

### Rest Variants
Short rests are 10 minutes. Long rests are 8 hours and restore all hit points and spell slots.

---

## Player Expectations

### What You Should Do
- **Engage with the story** - Ask questions, investigate, interact
- **Work as a team** - Support your fellow adventurers
- **Play your character** - Make decisions based on your character's personality
- **Have fun** - This is a game, enjoy it!

### What the DM Will Do
- **Create the world** - Build locations, NPCs, and encounters
- **Adjudicate rules** - Make rulings on unclear situations
- **Tell the story** - Narrate events and describe the world
- **Ensure fun** - Make sure everyone has a good time

---

## Questions?

If you have questions about character creation, the setting, or the campaign, don't hesitate to ask your DM. We're here to create an amazing story together!

---

**May your dice roll high and your adventures be legendary!**


---

# Dungeon Master's Guide

*Source: campaign_dm_guide.md*

# The Shattered Crown
## Dungeon Master's Guide

**Campaign Type**: Political Intrigue & Ancient Magic  
**Level Range**: 1-5  
**Estimated Sessions**: 8-12  
**Setting**: Kingdom of Aetheria

---

# Campaign Overview

## The Central Mystery

The campaign revolves around the disappearance of **Prince Aldric**, the young heir to the throne of Aetheria. As the party investigates, they uncover a conspiracy involving Duke Blackwood, who seeks to seize power by using an ancient artifact known as the **Shattered Crown**.

## Three-Act Structure

### Act 1: The Missing Heir (Levels 1-2)
**Sessions 1-4**

The party begins in Millbrook, investigating the disappearance of Lord Aldric's son. They discover clues pointing to ancient magic and political intrigue.

**Key Locations:**
- Millbrook Village
- Whispering Woods
- Abandoned Watchtower
- Ancient Burial Mound

**Major NPCs:**
- Lord Aldric (Noble, Lawful Good)
- Captain Thorne (Guard Captain, Lawful Neutral)
- The Mysterious Stranger (Unknown, Neutral)

**Climax:** Discovery of the first fragment of the Shattered Crown

---

### Act 2: The Conspiracy (Levels 2-4)
**Sessions 5-8**

The party travels to the capital city, uncovering Duke Blackwood's conspiracy. Political intrigue, social encounters, and urban exploration dominate.

**Key Locations:**
- Capital City (Aetheria)
- Noble Quarter
- Underground Tunnels
- Duke Blackwood's Estate
- Royal Archives

**Major NPCs:**
- Queen Valeria (Monarch, Lawful Good)
- Duke Blackwood (Noble, Lawful Evil) - **BBEG**
- Master Thief "Silk" (Rogue, Chaotic Neutral)
- Archmage Elara (Wizard, Neutral Good)

**Climax:** Uncovering the full extent of the conspiracy and Duke Blackwood's plans

---

### Act 3: The Final Confrontation (Levels 4-5)
**Sessions 9-12**

The party must stop Duke Blackwood from completing the ritual to restore the Shattered Crown. Final dungeon crawl and epic boss battle.

**Key Locations:**
- Temple of the Shattered Crown
- Shadow Realm (pocket dimension)
- The Crown Chamber

**Major NPCs:**
- Duke Blackwood (Final Boss)
- Ancient Guardian (Construct, Neutral)
- Prince Aldric (Rescued NPC)

**Climax:** Final battle with Duke Blackwood and resolution of the campaign

---

# Detailed Act Breakdown

## Act 1: The Missing Heir

### Session 1: The Call to Adventure

**Opening Scene:** The party arrives in Millbrook, a peaceful village that has been shaken by the disappearance of Lord Aldric's son, Prince Aldric.

**Key Encounters:**
1. **Meeting Lord Aldric** - Social encounter, information gathering
2. **Investigation in Millbrook** - Skill challenges (Investigation, Perception)
3. **The Mysterious Stranger** - First clue about ancient magic
4. **Combat: Bandits** - First combat encounter (Easy)

**Clues to Reveal:**
- Prince Aldric was last seen near Whispering Woods
- A strange symbol was found at the scene
- Ancient magic is involved

**Rewards:**
- 50 gold each
- Information about the conspiracy
- First quest hook

---

### Session 2: Into the Woods

**Location:** Whispering Woods

**Key Encounters:**
1. **Navigation Challenge** - Survival checks to navigate the woods
2. **Combat: Wolves** - Medium difficulty encounter
3. **The Abandoned Watchtower** - Exploration and investigation
4. **Combat: Goblins** - Medium difficulty encounter
5. **Discovery: First Fragment** - Find a piece of the Shattered Crown

**Clues to Reveal:**
- The fragment is part of an ancient artifact
- Someone else is searching for these fragments
- The conspiracy goes deeper than expected

**Rewards:**
- Fragment of the Shattered Crown (magic item)
- 100 gold
- Level up to 2

---

### Session 3: The Ancient Mound

**Location:** Ancient Burial Mound

**Key Encounters:**
1. **Puzzle: The Sealed Door** - Intelligence-based puzzle
2. **Combat: Skeletons** - Medium difficulty
3. **Trap: Pressure Plates** - Dexterity saves
4. **Combat: Wight** - Hard encounter
5. **Discovery: Ancient Texts** - Information about the Shattered Crown

**Clues to Reveal:**
- The Shattered Crown was broken into 5 fragments
- Each fragment grants power to its wielder
- Duke Blackwood seeks to reunite them

**Rewards:**
- Ancient texts (lore)
- Magic items
- 150 gold

---

### Session 4: The Capital Beckons

**Location:** Journey to Capital City

**Key Encounters:**
1. **Travel Encounter: Ambush** - Combat with Duke Blackwood's agents
2. **Social: Arrival in Capital** - Meeting with Queen Valeria
3. **Investigation: The Archives** - Research about the Shattered Crown
4. **Social: Meeting Duke Blackwood** - First encounter with BBEG (social)

**Clues to Reveal:**
- Duke Blackwood is behind the conspiracy
- He has 2 of the 5 fragments
- The party needs to find the remaining 3

**Rewards:**
- Royal favor
- Information about remaining fragments
- Level up to 3

---

## Act 2: The Conspiracy

### Session 5: The Noble Quarter

**Location:** Capital City - Noble Quarter

**Key Encounters:**
1. **Social: Noble Party** - Gather information through social interaction
2. **Stealth: Infiltrate Duke's Estate** - Stealth and investigation
3. **Combat: Guards** - Medium difficulty
4. **Discovery: Duke's Plans** - Find evidence of conspiracy

**Clues to Reveal:**
- Duke Blackwood plans to assassinate Queen Valeria
- He's working with a cult
- The ritual requires all 5 fragments

**Rewards:**
- Evidence of conspiracy
- 200 gold
- Magic items

---

### Session 6: The Underground

**Location:** Underground Tunnels

**Key Encounters:**
1. **Exploration: Tunnels** - Navigation and mapping
2. **Combat: Cultists** - Medium difficulty
3. **Puzzle: The Locked Vault** - Intelligence puzzle
4. **Combat: Cult Leader** - Hard encounter
5. **Discovery: Third Fragment** - Recover another fragment

**Clues to Reveal:**
- The cult serves an ancient evil
- Duke Blackwood is their leader
- The ritual is almost complete

**Rewards:**
- Third fragment
- 250 gold
- Level up to 4

---

### Session 7: The Archives

**Location:** Royal Archives

**Key Encounters:**
1. **Research Challenge** - Investigation and History checks
2. **Combat: Animated Armor** - Medium difficulty
3. **Puzzle: The Coded Manuscript** - Decipher ancient text
4. **Discovery: Location of Temple** - Find where the ritual will occur

**Clues to Reveal:**
- The Temple of the Shattered Crown location
- The ritual requires a blood sacrifice
- Prince Aldric is the intended sacrifice

**Rewards:**
- Complete information about the ritual
- 300 gold
- Magic items

---

### Session 8: The Race Against Time

**Location:** Capital City - Chase Sequence

**Key Encounters:**
1. **Chase: Through the City** - Skill challenge chase
2. **Combat: Duke's Agents** - Hard encounter
3. **Social: Confrontation with Duke** - Final social encounter before Act 3
4. **Discovery: Duke Escapes** - Sets up Act 3

**Clues to Reveal:**
- Duke has 4 of 5 fragments
- The party has 1 fragment
- The final fragment is in the Temple

**Rewards:**
- Information about the Temple
- 350 gold
- Level up to 5

---

## Act 3: The Final Confrontation

### Session 9: The Temple Entrance

**Location:** Temple of the Shattered Crown

**Key Encounters:**
1. **Exploration: Temple Exterior** - Investigation and exploration
2. **Combat: Temple Guardians** - Hard encounter
3. **Puzzle: The Three Trials** - Three-part puzzle challenge
4. **Combat: Shadow Creatures** - Hard encounter

**Clues to Reveal:**
- The Temple is a pocket dimension
- Time moves differently inside
- Duke is already inside

**Rewards:**
- Access to inner temple
- 400 gold

---

### Session 10: The Shadow Realm

**Location:** Shadow Realm (pocket dimension)

**Key Encounters:**
1. **Exploration: Shadow Realm** - Strange and dangerous environment
2. **Combat: Shadow Beasts** - Hard encounters
3. **Puzzle: The Mirror Maze** - Navigation puzzle
4. **Combat: Shadow Duke** - Hard encounter (Duke's shadow form)
5. **Discovery: Prince Aldric** - Find the captive prince

**Clues to Reveal:**
- The prince is alive but weakened
- Duke is performing the ritual
- The party must stop him before it completes

**Rewards:**
- Prince Aldric rescued
- 450 gold
- Magic items

---

### Session 11: The Crown Chamber

**Location:** The Crown Chamber (final dungeon)

**Key Encounters:**
1. **Combat: Final Guardians** - Very hard encounter
2. **Puzzle: The Crown Altar** - Final puzzle
3. **Combat: Ancient Guardian** - Very hard encounter (construct)
4. **Discovery: Final Fragment** - Recover the last fragment

**Clues to Reveal:**
- The ritual is almost complete
- Duke is in the final chamber
- The party must act now

**Rewards:**
- Final fragment
- 500 gold
- Legendary magic items

---

### Session 12: The Final Battle

**Location:** The Ritual Chamber

**Key Encounters:**
1. **Boss Battle: Duke Blackwood** - Epic final encounter
   - Phase 1: Duke with 4 fragments (Hard)
   - Phase 2: Duke with all 5 fragments (Very Hard)
   - Phase 3: Duke transformed (Extreme)

**Resolution Options:**
- **Good Ending:** Party defeats Duke, saves prince, returns fragments to safety
- **Neutral Ending:** Party defeats Duke but fragments are scattered
- **Bad Ending:** Duke completes ritual, party must deal with consequences

**Rewards:**
- Epic conclusion
- 1000 gold each
- Legendary rewards
- Campaign completion

---

# NPCs

## Major NPCs

### Lord Aldric
**Race:** Human  
**Class:** Noble (Fighter 5)  
**Alignment:** Lawful Good  
**Role:** Quest giver, father of missing prince

**Personality:** Worried, determined, honorable  
**Goals:** Find his son, protect the kingdom  
**Secrets:** Knows about the ancient artifacts

**Stats:**
```
AC: 16 (Chain Mail)
HP: 45
Attack: +6 (Longsword, 1d8+3)
```

---

### Captain Thorne
**Race:** Human  
**Class:** Fighter 4  
**Alignment:** Lawful Neutral  
**Role:** Guard captain, information source

**Personality:** Professional, suspicious, loyal  
**Goals:** Maintain order, investigate disappearance  
**Secrets:** Has evidence of conspiracy

---

### Queen Valeria
**Race:** Human  
**Class:** Noble (Bard 3)  
**Alignment:** Lawful Good  
**Role:** Monarch, ally

**Personality:** Wise, compassionate, strong  
**Goals:** Protect the kingdom, find the prince  
**Secrets:** Knows Duke Blackwood is dangerous

---

### Duke Blackwood (BBEG)
**Race:** Human  
**Class:** Warlock 5 (Fiend Patron)  
**Alignment:** Lawful Evil  
**Role:** Main antagonist

**Personality:** Cunning, ambitious, ruthless  
**Goals:** Seize the throne, complete the ritual  
**Secrets:** Made a pact with an ancient evil

**Stats (Final Form):**
```
AC: 18 (Mage Armor + Shield)
HP: 120
Spell Save DC: 16
Attacks: Eldritch Blast (+8, 2d10+4), Crown Powers
```

---

### Master Thief "Silk"
**Race:** Halfling  
**Class:** Rogue 4  
**Alignment:** Chaotic Neutral  
**Role:** Information broker, potential ally

**Personality:** Clever, opportunistic, mysterious  
**Goals:** Profit, survive  
**Secrets:** Has information about Duke's plans

---

### Archmage Elara
**Race:** Elf  
**Class:** Wizard 8  
**Alignment:** Neutral Good  
**Role:** Knowledge source, potential ally

**Personality:** Scholarly, helpful, cautious  
**Goals:** Preserve knowledge, stop dark magic  
**Secrets:** Knows how to destroy the fragments

---

# Locations

## Millbrook Village

**Size:** Small village (200 people)  
**Government:** Lord Aldric  
**Economy:** Farming, trade

**Key Locations:**
- Lord Aldric's Manor
- The Rusty Anchor (tavern)
- Village Square
- Millbrook Market

**Notable NPCs:**
- Lord Aldric
- Captain Thorne
- Tavern Keeper "Old Tom"

---

## Capital City (Aetheria)

**Size:** Large city (50,000 people)  
**Government:** Queen Valeria  
**Economy:** Trade, politics, magic

**Key Locations:**
- Royal Palace
- Noble Quarter
- The Archives
- Market District
- Underground Tunnels

**Notable NPCs:**
- Queen Valeria
- Duke Blackwood
- Archmage Elara
- Master Thief "Silk"

---

## Whispering Woods

**Type:** Ancient forest  
**Danger Level:** Medium  
**Features:** Magical, mysterious, dangerous

**Key Locations:**
- Abandoned Watchtower
- Ancient Burial Mound
- The Whispering Grove (magical location)

**Notable Encounters:**
- Wolves
- Goblins
- Magical creatures
- Ancient guardians

---

## Temple of the Shattered Crown

**Type:** Ancient temple/dungeon  
**Danger Level:** Very High  
**Features:** Pocket dimension, time distortion, powerful magic

**Key Locations:**
- Temple Entrance
- Shadow Realm
- The Crown Chamber
- The Ritual Chamber

**Notable Encounters:**
- Temple Guardians
- Shadow Creatures
- Ancient Guardian
- Duke Blackwood (final boss)

---

# Encounters

See `campaign_encounters.md` for detailed encounter statistics and tactics.

---

# Magic Items

## Fragments of the Shattered Crown

**Type:** Legendary (when complete), Rare (individual fragments)  
**Properties:** Each fragment grants different powers

**Fragment Powers:**
1. **Fragment of Power** - +1 to spell attack rolls and save DC
2. **Fragment of Protection** - +1 AC, resistance to necrotic damage
3. **Fragment of Knowledge** - Advantage on History and Arcana checks
4. **Fragment of Shadow** - Can cast Invisibility once per day
5. **Fragment of Crown** - +2 Charisma, advantage on Persuasion

**Complete Crown:** All powers combined, but corrupts the wielder

---

# Secrets and Revelations

## Act 1 Secrets
- The fragments are part of an ancient artifact
- Duke Blackwood is searching for them
- Ancient magic is involved in the conspiracy

## Act 2 Secrets
- Duke Blackwood plans to assassinate the queen
- He's working with a cult
- The ritual requires all 5 fragments and a blood sacrifice

## Act 3 Secrets
- Prince Aldric is the intended sacrifice
- The Temple is a pocket dimension
- Duke has made a pact with an ancient evil
- The complete crown corrupts its wielder

---

# Running the Campaign

## Pacing

- **Act 1:** Fast-paced investigation and discovery
- **Act 2:** Slower, more methodical political intrigue
- **Act 3:** High-stakes action and final confrontation

## Adjusting Difficulty

- Add or remove enemies from encounters
- Adjust HP of major enemies
- Modify DCs of skill challenges
- Provide more or fewer clues

## Player Agency

- Allow players to choose their approach
- Reward creative solutions
- Adapt to player choices
- Let players shape the story

---

# Conclusion

This campaign is designed to be flexible and adaptable. Use this guide as a framework, but don't be afraid to deviate based on player actions and interests. The most important thing is that everyone has fun!

**Good luck, and may your players' adventures be legendary!**


---

# Encounter Reference

*Source: campaign_encounters.md*

# The Shattered Crown
## Encounter Reference

Quick reference for all combat encounters in the campaign.

---

## Act 1 Encounters

### Encounter 1: Bandit Ambush
**Difficulty:** Easy  
**Level:** 1  
**Location:** Road to Millbrook

**Enemies:**
- 3x Bandits (CR 1/8 each)

**Tactics:**
- Ambush from roadside
- Target weakest party member
- Flee if half are defeated

**Terrain:**
- Road with trees on both sides
- Cover available

**Rewards:**
- 25 gold
- Basic weapons/armor

---

### Encounter 2: Wolves of the Woods
**Difficulty:** Medium  
**Level:** 1-2  
**Location:** Whispering Woods

**Enemies:**
- 1x Dire Wolf (CR 1)
- 3x Wolves (CR 1/4 each)

**Tactics:**
- Pack tactics (advantage when near allies)
- Target isolated party members
- Dire wolf focuses on strongest enemy

**Terrain:**
- Dense forest
- Difficult terrain (roots, undergrowth)
- Limited visibility

**Rewards:**
- 50 gold
- Wolf pelts (10 gold each)

---

### Encounter 3: Goblin Raiders
**Difficulty:** Medium  
**Level:** 2  
**Location:** Abandoned Watchtower

**Enemies:**
- 1x Goblin Boss (CR 1)
- 4x Goblins (CR 1/4 each)

**Tactics:**
- Use tower for cover
- Ranged attacks from above
- Goblin boss commands others
- Retreat if boss dies

**Terrain:**
- Abandoned watchtower (multi-level)
- Stairs provide advantage
- Windows for ranged attacks

**Rewards:**
- 75 gold
- First fragment of Shattered Crown
- Goblin weapons

---

### Encounter 4: Undead Guardians
**Difficulty:** Hard  
**Level:** 2-3  
**Location:** Ancient Burial Mound

**Enemies:**
- 1x Wight (CR 3)
- 4x Skeletons (CR 1/4 each)

**Tactics:**
- Skeletons engage in melee
- Wight uses ranged attacks
- Wight raises fallen skeletons
- Focus fire on spellcasters

**Terrain:**
- Burial chamber (confined space)
- Sarcophagi provide cover
- Magical darkness in corners

**Rewards:**
- 100 gold
- Ancient texts
- Magic items (roll on table)

---

## Act 2 Encounters

### Encounter 5: Duke's Agents
**Difficulty:** Medium  
**Level:** 3  
**Location:** Capital City Streets

**Enemies:**
- 2x Thugs (CR 1/2 each)
- 1x Spy (CR 1)

**Tactics:**
- Ambush in alley
- Spy uses sneak attack
- Thugs engage in melee
- Call for reinforcements if losing

**Terrain:**
- Urban alley
- Limited space
- Escape routes available

**Rewards:**
- 150 gold
- Evidence of conspiracy
- Information about Duke

---

### Encounter 6: Estate Guards
**Difficulty:** Medium  
**Level:** 3-4  
**Location:** Duke Blackwood's Estate

**Enemies:**
- 4x Guards (CR 1/8 each)
- 1x Veteran (CR 3)

**Tactics:**
- Guards form defensive line
- Veteran commands from rear
- Use estate features for cover
- Alert others if alarm raised

**Terrain:**
- Estate grounds
- Manicured gardens
- Building entrances
- High walls

**Rewards:**
- 200 gold
- Estate information
- Duke's plans

---

### Encounter 7: Cultists
**Difficulty:** Hard  
**Level:** 4  
**Location:** Underground Tunnels

**Enemies:**
- 1x Cult Fanatic (CR 2)
- 4x Cultists (CR 1/8 each)
- 2x Cult Fanatics (CR 2 each)

**Tactics:**
- Fanatics use spells
- Cultists engage in melee
- Focus on spellcasters
- Fight to the death

**Terrain:**
- Underground tunnels
- Narrow passages
- Limited visibility
- Magical darkness

**Rewards:**
- 250 gold
- Third fragment
- Cult information

---

### Encounter 8: Animated Armor
**Difficulty:** Medium  
**Level:** 4  
**Location:** Royal Archives

**Enemies:**
- 3x Animated Armor (CR 1 each)
- 1x Helmed Horror (CR 4)

**Tactics:**
- Animated armor engage in melee
- Helmed Horror uses magic resistance
- Protect archives
- Don't pursue if party flees

**Terrain:**
- Archive hall
- Bookshelves provide cover
- Narrow aisles
- Magical protections

**Rewards:**
- 300 gold
- Temple location information
- Ancient knowledge

---

### Encounter 9: Duke's Elite Agents
**Difficulty:** Hard  
**Level:** 4-5  
**Location:** Capital City Chase

**Enemies:**
- 2x Assassins (CR 8 each, reduced to CR 4)
- 1x Mage (CR 6, reduced to CR 4)

**Tactics:**
- Assassins use sneak attack
- Mage provides support
- Focus on party leader
- Escape if severely wounded

**Terrain:**
- City streets
- Rooftops
- Alleyways
- Crowded areas

**Rewards:**
- 350 gold
- Duke's escape route information
- Magic items

---

## Act 3 Encounters

### Encounter 10: Temple Guardians
**Difficulty:** Hard  
**Level:** 5  
**Location:** Temple Entrance

**Enemies:**
- 2x Stone Golems (CR 10 each, reduced to CR 5)
- 4x Animated Armor (CR 1 each)

**Tactics:**
- Golems engage strongest enemies
- Armor supports golems
- Protect temple entrance
- Fight until destroyed

**Terrain:**
- Temple entrance
- Large open area
- Pillars provide cover
- Magical barriers

**Rewards:**
- 400 gold
- Access to inner temple
- Temple map fragment

---

### Encounter 11: Shadow Beasts
**Difficulty:** Hard  
**Level:** 5  
**Location:** Shadow Realm

**Enemies:**
- 3x Shadow (CR 1/2 each)
- 2x Shadow Mastiff (CR 2 each)
- 1x Shadow Demon (CR 4)

**Tactics:**
- Use shadow to hide
- Target Strength-drained enemies
- Coordinate attacks
- Exploit shadow realm advantages

**Terrain:**
- Shadow realm (pocket dimension)
- Dim light everywhere
- Shifting terrain
- Magical darkness

**Rewards:**
- 450 gold
- Shadow-touched items
- Information about realm

---

### Encounter 12: Shadow Duke
**Difficulty:** Very Hard  
**Level:** 5  
**Location:** Shadow Realm

**Enemies:**
- 1x Shadow Duke (Duke Blackwood's shadow form)
  - Uses Duke's stats but with shadow abilities
  - CR 6

**Tactics:**
- Uses shadow magic
- Teleports between shadows
- Focuses on spellcasters
- Retreats if severely wounded

**Terrain:**
- Shadow realm
- Many shadow areas
- Unstable ground
- Magical effects

**Rewards:**
- 500 gold
- Prince Aldric location
- Shadow magic items

---

### Encounter 13: Ancient Guardian
**Difficulty:** Very Hard  
**Level:** 5  
**Location:** Crown Chamber

**Enemies:**
- 1x Ancient Guardian (Construct, CR 7, reduced to CR 5)

**Stats:**
```
AC: 18
HP: 120
Speed: 30 ft
STR: 20 (+5)
DEX: 10 (+0)
CON: 18 (+4)
INT: 6 (-2)
WIS: 10 (+0)
CHA: 1 (-5)

Attacks:
- Greatsword: +9, 2d6+5 slashing
- Fist: +9, 1d8+5 bludgeoning

Abilities:
- Magic Resistance
- Immutable Form
- Magic Weapons
```

**Tactics:**
- Protects the final fragment
- Focuses on strongest enemy
- Uses area attacks
- Fights until destroyed

**Terrain:**
- Crown Chamber
- Central altar
- Magical barriers
- Ancient runes

**Rewards:**
- 500 gold
- Final fragment
- Legendary magic items

---

### Encounter 14: Duke Blackwood (Final Boss)
**Difficulty:** Extreme  
**Level:** 5  
**Location:** Ritual Chamber

**Enemies:**
- 1x Duke Blackwood (Warlock 5, CR 6)

**Phase 1: Duke with 4 Fragments**
```
AC: 16
HP: 80
Spell Save DC: 15
Attacks: Eldritch Blast (+7, 2d10+3)

Abilities:
- Fragment Powers (4 fragments)
- Warlock Spells (3rd level)
- Legendary Actions (2 per turn)
```

**Phase 2: Duke with All 5 Fragments**
```
AC: 18
HP: 120
Spell Save DC: 16
Attacks: Eldritch Blast (+8, 2d10+4)

Abilities:
- All Fragment Powers
- Enhanced Warlock Spells
- Crown Corruption (begins)
- Legendary Actions (3 per turn)
```

**Phase 3: Duke Transformed**
```
AC: 20
HP: 150
Spell Save DC: 17
Attacks: Crown Blast (+9, 3d10+5), Crown Strike (melee)

Abilities:
- Full Crown Powers
- Dark Magic Mastery
- Regeneration (10 HP/round)
- Legendary Actions (4 per turn)
- Lair Actions (if in temple)
```

**Tactics:**
- Phase 1: Use fragments defensively, focus on spellcasters
- Phase 2: More aggressive, use all powers
- Phase 3: All-out attack, corrupted by crown

**Terrain:**
- Ritual Chamber
- Central ritual circle
- Magical barriers
- Unstable magic

**Rewards:**
- 1000 gold each
- Legendary magic items
- Campaign completion
- Kingdom's gratitude

---

## Encounter Tables

### Random Encounters (Travel)

**d20 Roll | Encounter**
1-5 | No encounter
6-8 | Bandits (1-3)
9-11 | Wolves (2-4)
12-13 | Traveling merchant
14-15 | Mysterious stranger
16-17 | Wild animals
18-19 | Weather event
20 | Special encounter (DM's choice)

---

## Tactics Guide

### General Combat Tips

**For Easy Encounters:**
- Enemies fight straightforward
- No complex tactics
- May flee if losing

**For Medium Encounters:**
- Basic coordination
- Focus fire on threats
- Use terrain advantage

**For Hard Encounters:**
- Advanced tactics
- Spell usage
- Environmental hazards
- May have reinforcements

**For Very Hard/Extreme:**
- Maximum tactics
- All abilities used
- Environmental effects
- Legendary actions
- Fight to the death

---

## Terrain Features

### Common Terrain Types

**Forest:**
- Difficult terrain (roots, undergrowth)
- Cover from trees
- Limited visibility
- Climbing opportunities

**Urban:**
- Narrow streets
- Buildings for cover
- Rooftops accessible
- Crowds may interfere

**Underground:**
- Confined spaces
- Limited visibility
- Echoes (sound travels)
- Collapse risks

**Temple/Dungeon:**
- Magical effects
- Traps possible
- Ancient protections
- Ritual circles

---

## Reward Guidelines

### Gold Rewards by Level

| Level | Easy | Medium | Hard | Very Hard |
|-------|------|--------|------|-----------|
| 1 | 25 | 50 | 75 | 100 |
| 2 | 50 | 100 | 150 | 200 |
| 3 | 75 | 150 | 225 | 300 |
| 4 | 100 | 200 | 300 | 400 |
| 5 | 125 | 250 | 375 | 500 |

### Magic Items

- **Easy Encounters:** Common items
- **Medium Encounters:** Uncommon items
- **Hard Encounters:** Rare items
- **Very Hard Encounters:** Very rare items
- **Extreme Encounters:** Legendary items

---

## Adjusting Encounters

### Making Encounters Easier
- Reduce enemy HP by 25%
- Remove 1-2 enemies
- Lower enemy AC by 1-2
- Reduce damage by 1 die

### Making Encounters Harder
- Increase enemy HP by 25%
- Add 1-2 enemies
- Increase enemy AC by 1-2
- Add environmental hazards
- Give enemies advantage

---

**Remember:** These are guidelines. Adjust based on your party's composition, tactics, and preferences!


---

# World Map & Locations

*Source: campaign_world_map.md*

# The Shattered Crown
## World Map & Locations

A comprehensive guide to the Kingdom of Aetheria and its key locations.

---

## Kingdom of Aetheria Overview

The Kingdom of Aetheria is a diverse realm spanning from the northern mountains to the eastern plains. The kingdom has been stable for generations, but recent events have revealed hidden dangers and ancient secrets.

**Capital:** Aetheria City  
**Ruler:** Queen Valeria  
**Population:** ~500,000  
**Government:** Feudal Monarchy  
**Major Exports:** Grain, textiles, magical components

---

## Major Regions

### The Capital Region
**Description:** The heart of the kingdom, centered around Aetheria City.  
**Terrain:** Rolling hills, fertile valleys  
**Climate:** Temperate, mild winters  
**Population:** Dense, urban

**Key Locations:**
- Aetheria City (Capital)
- Millbrook Village
- Trade Routes
- Royal Estates

---

### The Northern Mountains
**Description:** Rugged mountain range with ancient temples and forgotten ruins.  
**Terrain:** Mountains, valleys, caves  
**Climate:** Cold, snowy winters  
**Population:** Sparse, isolated

**Key Locations:**
- Temple of the Shattered Crown
- Ancient Ruins
- Mining Settlements
- Dragon's Peak (legendary)

---

### The Eastern Plains
**Description:** Vast grasslands perfect for farming and trade.  
**Terrain:** Flat plains, rolling hills  
**Climate:** Warm summers, mild winters  
**Population:** Moderate, agricultural

**Key Locations:**
- Farm Villages
- Trade Towns
- Caravan Routes
- Ancient Burial Mounds

---

### The Whispering Woods
**Description:** Ancient forest filled with mystery and magic.  
**Terrain:** Dense forest, clearings  
**Climate:** Cool, humid  
**Population:** Very sparse, mostly wildlife

**Key Locations:**
- Abandoned Watchtower
- The Whispering Grove
- Ancient Burial Mound
- Hidden Glades

---

## Detailed Locations

### Aetheria City (Capital)

**Size:** Large city (50,000 people)  
**Type:** Urban, political center  
**Government:** Direct royal rule  
**Economy:** Trade, politics, magic

**Districts:**

#### Royal Quarter
- **Royal Palace:** Queen Valeria's residence
- **Noble Estates:** Homes of major nobles
- **Royal Gardens:** Beautiful public gardens
- **Guard Barracks:** City guard headquarters

**Notable Features:**
- Grand architecture
- Magical protections
- High security
- Political importance

#### Market District
- **Grand Market:** Central trading hub
- **Merchant Quarter:** Shops and businesses
- **Guild Halls:** Trade guild headquarters
- **Inns and Taverns:** Accommodations

**Notable Features:**
- Bustling activity
- Diverse goods
- Information hub
- Social center

#### The Archives
- **Royal Library:** Vast collection of books
- **Magical Repository:** Stored magical items
- **Historical Records:** Kingdom's history
- **Research Facilities:** For scholars

**Notable Features:**
- Ancient knowledge
- Magical protections
- Restricted access
- Research opportunities

#### Underground Tunnels
- **Sewer System:** City's infrastructure
- **Secret Passages:** Hidden routes
- **Cult Hideouts:** Dangerous areas
- **Ancient Catacombs:** Historical significance

**Notable Features:**
- Dark and dangerous
- Hidden secrets
- Navigation challenges
- Potential discoveries

**Travel Times:**
- To Millbrook: 2 days by road
- To Northern Mountains: 5 days
- To Eastern Plains: 3 days
- To Whispering Woods: 1 day

---

### Millbrook Village

**Size:** Small village (200 people)  
**Type:** Rural, agricultural  
**Government:** Lord Aldric  
**Economy:** Farming, local trade

**Key Locations:**

#### Lord Aldric's Manor
- **Description:** Modest but well-maintained estate
- **Features:** Library, study, guest rooms
- **NPCs:** Lord Aldric, servants
- **Secrets:** Hidden documents about artifacts

#### The Rusty Anchor (Tavern)
- **Description:** Cozy village tavern
- **Features:** Common room, private rooms, stables
- **NPCs:** Old Tom (tavern keeper)
- **Information:** Local gossip, rumors

#### Village Square
- **Description:** Central gathering place
- **Features:** Well, market stalls, meeting hall
- **Events:** Weekly market, festivals
- **Information:** Village news, announcements

#### Millbrook Market
- **Description:** Small local market
- **Features:** Food stalls, crafts, supplies
- **Goods:** Basic equipment, food, local products
- **Prices:** Standard, sometimes cheaper than city

**Travel Times:**
- To Capital: 2 days by road
- To Whispering Woods: Half day
- To Nearest Town: 1 day

**Points of Interest:**
- Ancient stone circle (mysterious)
- Old mill (abandoned, haunted?)
- Village well (magical properties?)
- Lord's stables (horses available)

---

### Whispering Woods

**Size:** Large forest (50+ square miles)  
**Type:** Ancient, magical forest  
**Danger Level:** Medium to High  
**Features:** Magical, mysterious, dangerous

**Key Locations:**

#### Abandoned Watchtower
- **Description:** Old military watchtower, now abandoned
- **Features:** Three stories, rooftop, basement
- **Encounters:** Goblins, traps, first fragment
- **Secrets:** Hidden compartment with clues

**Location Details:**
- **Access:** Overgrown path from main road
- **Condition:** Structurally sound but neglected
- **Hazards:** Rotting floors, loose stones
- **Rewards:** First fragment, goblin loot

#### The Whispering Grove
- **Description:** Magical clearing in the forest
- **Features:** Ancient trees, magical aura, strange sounds
- **Encounters:** Fey creatures, magical effects
- **Secrets:** Portal to Feywild (hidden)

**Location Details:**
- **Access:** Follow the whispers (Perception DC 15)
- **Condition:** Pristine, untouched
- **Hazards:** Magical confusion, fey tricks
- **Rewards:** Fey blessings, magical items

#### Ancient Burial Mound
- **Description:** Prehistoric burial site
- **Features:** Underground chambers, ancient artifacts
- **Encounters:** Undead, traps, wight
- **Secrets:** Ancient texts about Shattered Crown

**Location Details:**
- **Access:** Hidden entrance (Investigation DC 18)
- **Condition:** Ancient but intact
- **Hazards:** Traps, undead, magical darkness
- **Rewards:** Ancient texts, magic items, second fragment

#### Hidden Glades
- **Description:** Secret clearings throughout the woods
- **Features:** Peaceful, beautiful, hidden
- **Encounters:** Wildlife, peaceful creatures
- **Secrets:** Rest spots, natural resources

**Travel Times:**
- Through woods: 1-2 days (depending on path)
- To Capital: 1 day from edge
- To Millbrook: Half day from edge

**Navigation:**
- **Easy Path:** Follow main road (safe, longer)
- **Direct Path:** Through woods (dangerous, shorter)
- **Hidden Path:** Ancient trail (secret, fastest)

**Hazards:**
- Getting lost (Survival DC 12)
- Dangerous creatures
- Magical effects
- Weather changes

---

### Temple of the Shattered Crown

**Size:** Large temple complex  
**Type:** Ancient temple/dungeon  
**Danger Level:** Very High  
**Features:** Pocket dimension, time distortion, powerful magic

**Key Locations:**

#### Temple Entrance
- **Description:** Grand entrance with massive doors
- **Features:** Guardian statues, magical barriers
- **Encounters:** Temple guardians, traps
- **Secrets:** Hidden passages, ancient runes

**Location Details:**
- **Access:** Northern Mountains, hidden valley
- **Condition:** Ancient but maintained by magic
- **Hazards:** Guardians, traps, magical barriers
- **Rewards:** Access to inner temple

#### Shadow Realm (Pocket Dimension)
- **Description:** Dark dimension connected to temple
- **Features:** Shifting terrain, shadow creatures, time distortion
- **Encounters:** Shadow beasts, shadow duke
- **Secrets:** Prince Aldric's location, shadow magic

**Location Details:**
- **Access:** Portal from temple
- **Condition:** Unstable, dangerous
- **Hazards:** Shadow creatures, environmental dangers
- **Rewards:** Prince Aldric, shadow items

#### The Crown Chamber
- **Description:** Central chamber where fragments are stored
- **Features:** Ancient altar, magical protections, final fragment
- **Encounters:** Ancient guardian, traps
- **Secrets:** Final fragment location, ritual knowledge

**Location Details:**
- **Access:** Deep in temple, past trials
- **Condition:** Pristine, magically protected
- **Hazards:** Guardian, traps, magical effects
- **Rewards:** Final fragment, legendary items

#### The Ritual Chamber
- **Description:** Where the final ritual takes place
- **Features:** Ritual circle, magical barriers, unstable magic
- **Encounters:** Duke Blackwood (final boss)
- **Secrets:** Ritual completion, crown restoration

**Location Details:**
- **Access:** Deepest part of temple
- **Condition:** Magically charged, unstable
- **Hazards:** Final boss, environmental dangers
- **Rewards:** Campaign completion, legendary rewards

**Travel Times:**
- From Capital: 5 days
- From Millbrook: 6 days
- From Whispering Woods: 5 days

**Special Properties:**
- Time moves differently inside
- Pocket dimension access
- Magical protections
- Ancient power source

---

## Travel Routes

### Main Roads

**The Royal Road:**
- Capital → Millbrook → Eastern Plains
- Well-maintained, safe
- Travel time: 2 days (Capital to Millbrook)
- Cost: Free (public road)

**The Northern Trail:**
- Capital → Northern Mountains → Temple
- Rough, dangerous
- Travel time: 5 days
- Cost: Free but risky

**The Eastern Trade Route:**
- Capital → Eastern Plains → Border
- Busy, commercial
- Travel time: 3 days
- Cost: Free, many travelers

### Secret Routes

**The Whisper Path:**
- Through Whispering Woods
- Hidden, magical
- Travel time: 1 day (if found)
- Cost: Free but requires discovery

**The Underground Network:**
- Through sewers and tunnels
- Dangerous, illegal
- Travel time: Varies
- Cost: Information or favors

---

## Points of Interest

### Natural Features

**Dragon's Peak:**
- Legendary mountain peak
- Said to be home to ancient dragon
- Never confirmed
- Location: Northern Mountains

**The Crystal Falls:**
- Beautiful waterfall with magical properties
- Water has minor healing properties
- Location: Whispering Woods
- Access: Hidden path

**The Standing Stones:**
- Ancient stone circle
- Magical significance
- Location: Near Millbrook
- Purpose: Unknown

### Historical Sites

**The Old Fort:**
- Abandoned military fort
- Historical significance
- Location: Eastern Plains
- Condition: Ruined

**The Ancient Library:**
- Ruins of old library
- May contain lost knowledge
- Location: Northern Mountains
- Access: Difficult

---

## Map Legend

**Symbols:**
- 🏰 Capital City
- 🏘️ Village/Town
- 🌲 Forest
- ⛰️ Mountains
- 🛣️ Road
- ⚠️ Dangerous Area
- ✨ Magical Location
- 🏛️ Temple/Ruins

**Distance Scale:**
- 1 inch = 50 miles
- Major cities: 2-5 days apart
- Villages: 1-2 days apart
- Dangerous areas: Variable

---

## Random Encounters by Region

### Capital Region
- Merchants
- Guards
- Nobles
- City events

### Northern Mountains
- Bandits
- Wild animals
- Weather
- Ancient guardians

### Eastern Plains
- Travelers
- Bandits
- Weather
- Farm events

### Whispering Woods
- Magical creatures
- Wildlife
- Fey
- Ancient guardians

---

**Use this guide to help players navigate the Kingdom of Aetheria and discover its secrets!**


---

# NPC Reference Cards

*Source: campaign_npcs.md*

# The Shattered Crown
## NPC Reference Cards

Quick reference for all major NPCs in the campaign.

---

## Major NPCs

### Lord Aldric
**Race:** Human  
**Class:** Noble (Fighter 5)  
**Alignment:** Lawful Good  
**Location:** Millbrook Village

**Appearance:**
- Middle-aged, distinguished
- Well-groomed beard
- Wears fine but practical clothes
- Carries himself with authority

**Personality:**
- Worried about his missing son
- Determined to find the truth
- Honorable and just
- Protective of his people

**Goals:**
- Find Prince Aldric
- Protect the kingdom
- Maintain order in his domain

**Secrets:**
- Knows about ancient artifacts
- Has hidden documents about the Shattered Crown
- Suspects Duke Blackwood

**Stats:**
```
AC: 16 (Chain Mail)
HP: 45
Speed: 30 ft
STR: 16 (+3)
DEX: 12 (+1)
CON: 14 (+2)
INT: 13 (+1)
WIS: 15 (+2)
CHA: 17 (+3)

Attacks:
- Longsword: +6, 1d8+3 slashing
- Dagger: +6, 1d4+3 piercing

Skills:
- Insight +5
- Persuasion +6
- History +4
```

**Role in Campaign:**
- Quest giver (Act 1)
- Information source
- Potential ally

---

### Captain Thorne
**Race:** Human  
**Class:** Fighter 4  
**Alignment:** Lawful Neutral  
**Location:** Millbrook Village

**Appearance:**
- Middle-aged, military bearing
- Short-cropped hair
- Wears guard uniform
- Carries sword and shield

**Personality:**
- Professional and disciplined
- Suspicious of strangers
- Loyal to Lord Aldric
- Methodical investigator

**Goals:**
- Maintain order
- Investigate disappearance
- Protect the village

**Secrets:**
- Has evidence of conspiracy
- Knows about Duke Blackwood's agents
- Has seen the mysterious symbol before

**Stats:**
```
AC: 18 (Chain Mail + Shield)
HP: 36
Speed: 30 ft
STR: 16 (+3)
DEX: 13 (+1)
CON: 14 (+2)
INT: 12 (+1)
WIS: 15 (+2)
CHA: 11 (+0)

Attacks:
- Longsword: +6, 1d8+3 slashing
- Shield Bash: +6, 1d4+3 bludgeoning

Skills:
- Investigation +4
- Perception +5
- Athletics +6
```

**Role in Campaign:**
- Information source
- Guard captain
- Potential combat ally

---

### Queen Valeria
**Race:** Human  
**Class:** Noble (Bard 3)  
**Alignment:** Lawful Good  
**Location:** Capital City

**Appearance:**
- Regal and elegant
- Middle-aged but youthful
- Wears royal regalia
- Carries herself with grace

**Personality:**
- Wise and compassionate
- Strong leader
- Cares deeply for her people
- Suspicious of Duke Blackwood

**Goals:**
- Protect the kingdom
- Find Prince Aldric
- Maintain peace
- Expose corruption

**Secrets:**
- Knows Duke Blackwood is dangerous
- Has evidence of his conspiracy
- Aware of ancient artifacts

**Stats:**
```
AC: 14 (Royal Robes + Dex)
HP: 24
Speed: 30 ft
STR: 10 (+0)
DEX: 14 (+2)
CON: 12 (+1)
INT: 16 (+3)
WIS: 15 (+2)
CHA: 18 (+4)

Spells:
- Cantrips: Vicious Mockery, Prestidigitation
- 1st Level: Charm Person, Cure Wounds
- 2nd Level: Suggestion

Skills:
- Insight +5
- Persuasion +7
- History +6
- Performance +7
```

**Role in Campaign:**
- Monarch and ally
- Information source
- Can provide resources

---

### Duke Blackwood (BBEG)
**Race:** Human  
**Class:** Warlock 5 (Fiend Patron)  
**Alignment:** Lawful Evil  
**Location:** Capital City / Temple

**Appearance:**
- Distinguished noble
- Dark, calculating eyes
- Wears expensive clothes
- Carries himself with confidence

**Personality:**
- Cunning and ambitious
- Ruthless when needed
- Charismatic in public
- Cold and calculating in private

**Goals:**
- Seize the throne
- Complete the ritual
- Restore the Shattered Crown
- Rule the kingdom

**Secrets:**
- Made a pact with an ancient evil
- Has 4 of 5 fragments
- Plans to sacrifice Prince Aldric
- Leader of the cult

**Stats (Final Form):**
```
AC: 18 (Mage Armor + Shield)
HP: 120 (Phase 3)
Speed: 30 ft
STR: 12 (+1)
DEX: 14 (+2)
CON: 16 (+3)
INT: 17 (+3)
WIS: 13 (+1)
CHA: 18 (+4)

Spell Save DC: 17
Spell Attack: +9

Spells:
- Eldritch Blast: +9, 3d10+5 force
- Crown Blast: +9, 3d10+5 necrotic
- Various Warlock spells

Abilities:
- Fragment Powers (all 5)
- Dark Magic Mastery
- Regeneration (10 HP/round)
- Legendary Actions (4 per turn)
```

**Role in Campaign:**
- Main antagonist
- Final boss
- Drives the conspiracy

---

### Master Thief "Silk"
**Race:** Halfling  
**Class:** Rogue 4  
**Alignment:** Chaotic Neutral  
**Location:** Capital City

**Appearance:**
- Small, nimble
- Wears dark, practical clothes
- Keeps face hidden
- Moves with grace

**Personality:**
- Clever and opportunistic
- Mysterious and secretive
- Self-interested but not evil
- Has a code of honor

**Goals:**
- Profit from information
- Survive
- Avoid trouble
- Help if paid well

**Secrets:**
- Has information about Duke's plans
- Knows about the fragments
- Has connections in the underworld
- Can be an ally if paid

**Stats:**
```
AC: 16 (Leather Armor + Dex)
HP: 28
Speed: 25 ft
STR: 10 (+0)
DEX: 18 (+4)
CON: 12 (+1)
INT: 14 (+2)
WIS: 13 (+1)
CHA: 15 (+2)

Attacks:
- Shortsword: +7, 1d6+4 piercing
- Dagger: +7, 1d4+4 piercing (thrown)

Skills:
- Stealth +10
- Sleight of Hand +10
- Investigation +8
- Deception +8
- Insight +5
```

**Role in Campaign:**
- Information broker
- Potential ally
- Can provide services

---

### Archmage Elara
**Race:** Elf  
**Class:** Wizard 8  
**Alignment:** Neutral Good  
**Location:** Capital City

**Appearance:**
- Elven, ageless
- Wears scholarly robes
- Carries a staff
- Has an air of wisdom

**Personality:**
- Scholarly and helpful
- Cautious but willing to help
- Knowledgeable about magic
- Protective of knowledge

**Goals:**
- Preserve ancient knowledge
- Stop dark magic
- Help the party
- Protect the kingdom

**Secrets:**
- Knows how to destroy fragments
- Has studied the Shattered Crown
- Knows about the ancient evil
- Can provide magical assistance

**Stats:**
```
AC: 15 (Mage Armor)
HP: 44
Speed: 30 ft
STR: 8 (-1)
DEX: 14 (+2)
CON: 12 (+1)
INT: 20 (+5)
WIS: 15 (+2)
CHA: 12 (+1)

Spell Save DC: 17
Spell Attack: +11

Spells:
- Various wizard spells (up to 4th level)
- Focus: Abjuration, Divination

Skills:
- Arcana +13
- History +13
- Investigation +11
- Insight +8
```

**Role in Campaign:**
- Knowledge source
- Magical ally
- Can provide spells/items

---

### The Mysterious Stranger
**Race:** Unknown  
**Class:** Unknown  
**Alignment:** Neutral  
**Location:** Various

**Appearance:**
- Hooded figure
- Face hidden
- Moves silently
- Leaves no trace

**Personality:**
- Mysterious and enigmatic
- Helpful but cryptic
- Knows more than they say
- Appears when needed

**Goals:**
- Unknown
- Seems to help the party
- Opposes Duke Blackwood
- Protects ancient knowledge

**Secrets:**
- True identity unknown
- Connection to ancient magic
- Knows about the fragments
- May be an ancient guardian

**Stats:**
```
Unknown - Appears powerful
Can disappear at will
Knows things they shouldn't
```

**Role in Campaign:**
- Mysterious helper
- Information source
- Plot device

---

### Prince Aldric
**Race:** Human  
**Class:** Noble (Fighter 1)  
**Alignment:** Lawful Good  
**Location:** Temple (captive)

**Appearance:**
- Young, noble bearing
- Resembles Lord Aldric
- Wears tattered clothes
- Looks determined despite captivity

**Personality:**
- Brave and determined
- Worried about the kingdom
- Grateful to rescuers
- Wants to help

**Goals:**
- Escape captivity
- Stop Duke Blackwood
- Return to his father
- Protect the kingdom

**Secrets:**
- Knows about Duke's plans
- Has information about the ritual
- Can identify the fragments
- Important for the ritual

**Stats:**
```
AC: 12 (No armor)
HP: 11
Speed: 30 ft
STR: 13 (+1)
DEX: 12 (+1)
CON: 12 (+1)
INT: 14 (+2)
WIS: 15 (+2)
CHA: 16 (+3)

Skills:
- History +4
- Insight +4
- Persuasion +5
```

**Role in Campaign:**
- Rescued NPC
- Information source
- Plot important

---

## Minor NPCs

### Old Tom (Tavern Keeper)
**Location:** Millbrook  
**Role:** Information source, services  
**Personality:** Friendly, talkative, knows local gossip

### Cult Leader
**Location:** Underground Tunnels  
**Role:** Antagonist  
**Personality:** Fanatical, dangerous, serves Duke

### Ancient Guardian
**Location:** Crown Chamber  
**Role:** Protector  
**Personality:** Mechanical, protective, follows ancient programming

---

## NPC Relationship Map

```
Lord Aldric
  ├── Prince Aldric (son, missing)
  ├── Captain Thorne (subordinate)
  └── Party (allies)

Queen Valeria
  ├── Duke Blackwood (enemy, suspect)
  ├── Archmage Elara (advisor)
  └── Party (potential allies)

Duke Blackwood
  ├── Cult (followers)
  ├── Ancient Evil (patron)
  └── Party (enemies)

Master Thief "Silk"
  ├── Underworld (connections)
  └── Party (potential ally, if paid)

Archmage Elara
  ├── Queen Valeria (advisor)
  └── Party (ally)

Mysterious Stranger
  └── Party (helper, mysterious)
```

---

## NPC Motivations

**Lord Aldric:** Find son, protect kingdom  
**Captain Thorne:** Maintain order, investigate  
**Queen Valeria:** Protect kingdom, find prince  
**Duke Blackwood:** Seize power, complete ritual  
**Master Thief "Silk":** Profit, survival  
**Archmage Elara:** Preserve knowledge, stop dark magic  
**Mysterious Stranger:** Unknown, seems helpful  
**Prince Aldric:** Escape, stop Duke, return home

---

## Using NPCs

### Social Encounters
- Use NPCs for information gathering
- Provide quest hooks
- Create roleplay opportunities
- Drive the story forward

### Combat Encounters
- Some NPCs can join combat
- Others provide support
- Some are enemies
- Adjust based on party needs

### Plot Devices
- NPCs drive the story
- Provide clues and information
- Create conflict and tension
- Resolve plot threads

---

**Use these NPCs to bring the campaign to life and create memorable interactions!**


---

# PDF Evolution Findings

# PDF Evolution Findings
## D&D Campaign PDF Generation Analysis

**Date:** January 12, 2026  
**Work Effort:** WE-260112-jqkn  
**Purpose:** Test PDF generator with diverse document types to identify improvements

---

## Executive Summary

Generated 5 D&D campaign documents using different PDF generator styles and configurations. Analysis identified several areas for improvement in handling diverse content types, layout requirements, and styling variations.

---

## Generated Documents

### 1. Player's Guide
- **Style:** Premium
- **Size:** 48.6 KB
- **Purpose:** Campaign introduction for players
- **Features Tested:** Premium styling, multi-section layout, table formatting

### 2. DM Guide
- **Style:** Clinical Standard
- **Size:** 26.3 KB
- **Purpose:** Complete campaign reference for DM
- **Features Tested:** Long-form content, nested sections, code blocks

### 3. Encounter Sheets
- **Style:** Clinical Standard (compact)
- **Size:** 15.0 KB
- **Purpose:** Quick reference for combat encounters
- **Features Tested:** Compact layout, table-heavy content, minimal margins

### 4. World Map
- **Style:** Premium
- **Size:** 47.8 KB
- **Purpose:** Location descriptions with map references
- **Features Tested:** Image integration, sidebar layouts, callout boxes

### 5. NPC Cards
- **Style:** Clinical Standard (compact)
- **Size:** 16.0 KB
- **Purpose:** Quick NPC lookup
- **Features Tested:** Card-based layout, grid formatting, compact styling

---

## Analysis Results

### Quality Analysis

All PDFs were successfully generated, but analysis revealed several gaps:

**Player's Guide:**
- Missing methodology/approach section (expected for campaign guide)
- Missing results/findings section (not applicable to player guide)
- Missing conclusion/summary section (could be useful)

**DM Guide:**
- Missing results/findings section (not applicable to reference guide)

**Encounter Sheets:**
- No concepts identified (tables and stats don't extract as concepts)
- No insights identified (reference material format)
- Missing introduction/overview section (could be helpful)

**World Map:**
- No actions identified (descriptive content)
- No insights identified (reference material)
- Missing methodology/approach section (not applicable)

**NPC Cards:**
- Missing introduction/overview section (could be helpful)
- Missing results/findings section (not applicable)

---

## Key Findings

### 1. Content Type Recognition

**Issue:** The analysis system expects academic/research document structure (methodology, results, findings) which doesn't apply to reference materials like D&D campaign guides.

**Impact:** Analysis flags "gaps" that aren't actually gaps for these document types.

**Recommendation:** 
- Add document type detection (reference, guide, academic, etc.)
- Customize analysis criteria based on document type
- Don't flag missing sections that aren't relevant to the document type

### 2. Table and Stat Block Handling

**Issue:** Encounter sheets contain many tables (monster stats, encounter details) but these aren't being recognized as structured content.

**Impact:** Analysis doesn't identify the rich structured data in tables.

**Recommendation:**
- Improve table extraction and recognition
- Recognize D&D stat blocks as structured content
- Count tables as "concepts" or structured data points

### 3. Compact Layout Support

**Issue:** Encounter sheets and NPC cards need very compact layouts with minimal margins, but current system has limited compact layout options.

**Impact:** Documents work but could be more space-efficient.

**Recommendation:**
- Add "compact" preset style
- Better support for card-based layouts
- Grid formatting options for reference cards

### 4. Image Integration

**Issue:** World map document is designed for image integration (maps, location images) but images weren't included in test.

**Impact:** Can't fully test image integration capabilities.

**Recommendation:**
- Test with actual images
- Verify image placement and sizing
- Test image + text layouts

### 5. Long-Form Content

**Issue:** DM Guide is a long document (20+ pages expected) but generated as 26.3 KB, suggesting it may be shorter than expected.

**Impact:** Need to verify long-form content handling.

**Recommendation:**
- Test with longer content
- Verify page breaks and section handling
- Test table of contents for long documents

---

## Pain Points Identified

### 1. Document Type Assumptions
- Analysis assumes academic/research structure
- Doesn't adapt to reference materials
- Flags irrelevant "missing" sections

### 2. Table Recognition
- Tables not recognized as structured content
- Stat blocks not identified
- Table formatting could be improved

### 3. Layout Flexibility
- Limited compact layout options
- Card-based layouts need better support
- Grid formatting not well supported

### 4. Image Support
- Image integration not fully tested
- Need examples with actual images
- Image + text layout needs verification

### 5. Styling Presets
- Only 2 main presets (premium, clinical_standard)
- Need more specialized presets (compact, card, reference)
- Custom styling requires code changes

---

## Improvement Opportunities

### High Priority

1. **Document Type Detection**
   - Detect document type (reference, guide, academic, etc.)
   - Customize analysis criteria per type
   - Don't flag irrelevant missing sections

2. **Table and Structured Data Recognition**
   - Better table extraction
   - Recognize D&D stat blocks
   - Count structured data as content

3. **Compact Layout Preset**
   - Add "compact" style preset
   - Minimal margins
   - Smaller fonts
   - Dense information layout

### Medium Priority

4. **Card-Based Layout Support**
   - Grid formatting
   - Card templates
   - Multi-column card layouts

5. **Image Integration Testing**
   - Test with actual images
   - Verify placement and sizing
   - Test various image + text layouts

6. **Long-Form Content Handling**
   - Table of contents generation
   - Better page break handling
   - Section navigation

### Low Priority

7. **Additional Style Presets**
   - Reference guide style
   - Quick reference style
   - Character sheet style

8. **Enhanced Analysis**
   - Document-type-specific analysis
   - Better content recognition
   - More nuanced gap detection

---

## Technical Observations

### What Worked Well

- ✅ PDF generation successful for all document types
- ✅ Different styles applied correctly (premium vs clinical_standard)
- ✅ Custom margins and font sizes work
- ✅ Basic table formatting works
- ✅ Multi-section documents handled properly

### What Needs Improvement

- ⚠️ Document type detection for analysis
- ⚠️ Table and structured data recognition
- ⚠️ Compact layout options
- ⚠️ Image integration (not fully tested)
- ⚠️ Long-form content handling (needs verification)

---

## Recommendations

### Immediate Actions

1. **Add Document Type Detection**
   - Implement document type classifier
   - Customize analysis per type
   - Update ScientificPDFGenerator

2. **Improve Table Recognition**
   - Better table extraction
   - Recognize structured data formats
   - Update analysis to count tables

3. **Create Compact Preset**
   - Add "compact" style preset
   - Test with encounter sheets and NPC cards
   - Verify space efficiency

### Future Enhancements

4. **Card Layout System**
   - Design card-based layout system
   - Support grid formatting
   - Test with NPC cards

5. **Image Integration**
   - Test with actual images
   - Verify placement and sizing
   - Document image best practices

6. **Long-Form Support**
   - Table of contents generation
   - Better section handling
   - Page break optimization

---

## Conclusion

The PDF generator successfully created all 5 campaign documents with appropriate styling. However, analysis revealed opportunities to improve:

1. **Document type awareness** - Don't apply academic analysis to reference materials
2. **Table recognition** - Better handling of structured data like stat blocks
3. **Layout flexibility** - More presets and options for different document types
4. **Image support** - Full testing and documentation needed

The campaign documents serve as excellent test cases for evolving the PDF generator to handle diverse content types and layouts more effectively.

---

**Next Steps:**
1. Implement document type detection
2. Improve table recognition
3. Add compact layout preset
4. Test image integration
5. Generate evolution report PDF


---

# Quality Analysis Results

## Quality Analysis Summary

### Player's Guide

**File Size:** 48.6 KB

**Scores:**
- Completeness: 0.42
- Structure: 0.25

**Gaps Identified:**
- Missing methodology/approach section
- Missing results/findings section
- Missing conclusion/summary section

**Suggestions:**
- Add more detailed content to improve completeness
- Improve document structure with clear sections

---

### DM Guide

**File Size:** 26.3 KB

**Scores:**
- Completeness: 0.30
- Structure: 0.75

**Gaps Identified:**
- Missing results/findings section

**Suggestions:**
- Add more detailed content to improve completeness

---

### Encounter Sheets

**File Size:** 15.0 KB

**Scores:**
- Completeness: 0.33
- Structure: 0.25

**Gaps Identified:**
- No concepts identified
- No insights identified
- Missing introduction/overview section
- Missing methodology/approach section
- Missing results/findings section

**Suggestions:**
- Add more detailed content to improve completeness
- Improve document structure with clear sections

---

### World Map

**File Size:** 47.8 KB

**Scores:**
- Completeness: 0.43
- Structure: 0.50

**Gaps Identified:**
- No actions identified
- No insights identified
- Missing methodology/approach section
- Missing results/findings section

**Suggestions:**
- Add more detailed content to improve completeness
- Improve document structure with clear sections

---

### NPC Cards

**File Size:** 16.0 KB

**Scores:**
- Completeness: 0.55
- Structure: 0.50

**Gaps Identified:**
- Missing introduction/overview section
- Missing results/findings section

**Suggestions:**
- Add more detailed content to improve completeness
- Improve document structure with clear sections

---



---

# Generated PDFs

## Generated PDF Documents

The following PDFs were generated as part of this work effort:

- **WE-260112-jqkn_COMPLETE**
  - File: `WE-260112-jqkn_COMPLETE.pdf`
  - Size: 47.5 KB

- **campaign_dm_guide**
  - File: `campaign_dm_guide.pdf`
  - Size: 26.3 KB

- **campaign_encounters**
  - File: `campaign_encounters.pdf`
  - Size: 15.0 KB

- **campaign_npcs**
  - File: `campaign_npcs.pdf`
  - Size: 16.0 KB

- **campaign_players_guide**
  - File: `campaign_players_guide.pdf`
  - Size: 48.6 KB

- **campaign_world_map**
  - File: `campaign_world_map.pdf`
  - Size: 47.8 KB

- **character_sheet_Aldric_the_Brave**
  - File: `character_sheet_Aldric_the_Brave.pdf`
  - Size: 12.7 KB

- **character_sheet_blank**
  - File: `character_sheet_blank.pdf`
  - Size: 11.9 KB

- **pdf_evolution_report**
  - File: `pdf_evolution_report.pdf`
  - Size: 51.9 KB



---

# Code Examples

## PDF Generation Script

**File:** `examples/generate_dnd_campaign_pdfs.py`

```python
"""
Generate D&D Campaign PDFs
==========================

Generates all 5 campaign documents as PDFs with different styles to test
and evolve the PDF generator capabilities.

Documents:
1. Player's Guide - Premium styling
2. DM Guide - Clinical standard styling
3. Encounter Sheets - Compact layout
4. World Map - Custom styling with images
5. NPC Reference Cards - Card-based layout
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.evolution.pdf_generator import PDFGenerator


def generate_players_guide():
    """Generate Player's Guide with premium styling."""
    print("\n📄 Generating Player's Guide (Premium Style)...")
    
    content_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "campaign_players_guide.md"
    output_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "campaign_players_guide.pdf"
    
    generator = PDFGenerator.from_file(
        file_path=content_path,
        title="The Shattered Crown - Player's Guide",
        style="premium",
        output_path=output_path
    )
    
    result = generator.save(
        output_path=output_path,
        convert_to_png=True,
        png_dpi=300
    )
    
    print(f"   ✅ Generated: {result}")
    return result


def generate_dm_guide():
    """Generate DM Guide with clinical standard styling."""
    print("\n📄 Generating DM Guide (Clinical Standard Style)...")
    
    content_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "campaign_dm_guide.md"
    output_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "campaign_dm_guide.pdf"
    
    generator = PDFGenerator.from_file(
        file_path=content_path,
        title="The Shattered Crown - Dungeon Master's Guide",
        style="clinical_standard",
        output_path=output_path
    )
    
    result = generator.save(
        output_path=output_path,
        convert_to_png=True,
        png_dpi=300
    )
    
    print(f"   ✅ Generated: {result}")
    return result


def generate_encounter_sheets():
    """Generate Encounter Sheets with compact layout."""
    print("\n📄 Generating Encounter Sheets (Compact Layout)...")
    
    content_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "campaign_encounters.md"
    output_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "campaign_encounters.pdf"
    
    # Use clinical standard with smaller margins for compact layout
    generator = PDFGenerator.from_file(
        file_path=content_path,
        title="The Shattered Crown - Encounter Reference",
        style="clinical_standard",
        output_path=output_path,
        margins=(15, 15, 15, 15),  # Smaller margins for compact
        font_size=10  # Smaller font
    )
    
    result = generator.save(
        output_path=output_path,
        convert_to_png=True,
        png_dpi=300
    )
    
    print(f"   ✅ Generated: {result}")
    return result


def generate_world_map():
    """Generate World Map document with custom styling."""
    print("\n📄 Generating World Map Document (Custom Styling)...")
    
    content_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "campaign_world_map.md"
    output_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "campaign_world_map.pdf"
    
    # Use premium style for world map
    generator = PDFGenerator.from_file(
        file_path=content_path,
        title="The Shattered Crown - World Map & Locations",
        style="premium",
        output_path=output_path
    )
    
    result = generator.save(
        output_path=output_path,
        convert_to_png=True,
        png_dpi=300
    )
    
    print(f"   ✅ Generated: {result}")
    return result


def generate_npc_cards():
    """Generate NPC Reference Cards with card-based layout."""
    print("\n📄 Generating NPC Reference Cards (Card Layout)...")
    
    content_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "campaign_npcs.md"
    output_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "campaign_npcs.pdf"
    
    # Use clinical standard with compact settings for cards
    generator = PDFGenerator.from_file(
        file_path=content_path,
        title="The Shattered Crown - NPC Reference Cards",
        style="clinical_standard",
        output_path=output_path,
        margins=(20, 20, 20, 20),
        font_size=10
    )
    
    result = generator.save(
        output_path=output_path,
        convert_to_png=True,
        png_dpi=300
    )
    
    print(f"   ✅ Generated: {result}")
    return result


def main():
    """Generate all campaign PDFs."""
    print("=" * 60)
    print("D&D Campaign PDF Generation")
    print("=" * 60)
    print("\nGenerating 5 campaign documents with different styles...")
    
    results = []
    
    try:
        # Generate all PDFs
        results.append(("Player's Guide", generate_players_guide()))
        results.append(("DM Guide", generate_dm_guide()))
        results.append(("Encounter Sheets", generate_encounter_sheets()))
        results.append(("World Map", generate_world_map()))
        results.append(("NPC Cards", generate_npc_cards()))
        
        # Summary
        print("\n" + "=" * 60)
        print("✅ PDF Generation Complete!")
        print("=" * 60)
        print("\nGenerated Documents:")
        for name, path in results:
            if path and path.exists():
                size_kb = path.stat().st_size / 1024
                print(f"   📄 {name}: {path.name} ({size_kb:.1f} KB)")
        
        # Check for PNG files
        work_effort_dir = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution"
        png_files = list(work_effort_dir.glob("*.png"))
        if png_files:
            print(f"\n📸 PNG Screenshots Generated: {len(png_files)}")
            for png in png_files:
                print(f"   🖼️  {png.name}")
        
        print("\n✅ All campaign PDFs generated successfully!")
        print(f"   Location: {work_effort_dir}")
        
    except Exception as e:
        print(f"\n❌ Error generating PDFs: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

```

## PDF Analysis Script

**File:** `examples/analyze_dnd_campaign_pdfs.py`

```python
"""
Analyze D&D Campaign PDFs
==========================

Uses ScientificPDFGenerator to analyze the quality of generated campaign PDFs
and document findings for PDF evolution.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.evolution.scientific_pdf_generator import ScientificPDFGenerator
from src.waft.evolution.pdf_generator import PDFGenerator


def analyze_pdf(pdf_path: Path, title: str):
    """Analyze a single PDF and return analysis results."""
    print(f"\n📊 Analyzing: {title}")
    print(f"   File: {pdf_path.name}")
    
    if not pdf_path.exists():
        print(f"   ❌ PDF not found: {pdf_path}")
        return None
    
    try:
        # Read the PDF content (we'll analyze the markdown source)
        # For now, we'll create a ScientificPDFGenerator from the markdown
        # and analyze it
        
        # Find corresponding markdown file
        md_name = pdf_path.stem.replace(".pdf", "") + ".md"
        md_path = pdf_path.parent / md_name
        
        if not md_path.exists():
            print(f"   ⚠️  Markdown source not found: {md_name}")
            return None
        
        # Create generator from markdown
        content = md_path.read_text()
        
        # Determine style based on document type
        if "players_guide" in pdf_path.stem:
            style = "premium"
        elif "dm_guide" in pdf_path.stem:
            style = "clinical_standard"
        elif "encounters" in pdf_path.stem:
            style = "clinical_standard"
        elif "world_map" in pdf_path.stem:
            style = "premium"
        elif "npcs" in pdf_path.stem:
            style = "clinical_standard"
        else:
            style = "clinical_standard"
        
        # Create scientific generator
        generator = ScientificPDFGenerator.from_content(
            content=content,
            title=title,
            style=style,
            scientific_mode=True
        )
        
        # Analyze quality
        analysis = generator.analyze_quality()
        
        print(f"   ✅ Analysis complete")
        print(f"   Quality Score: {analysis.get('quality_score', 'N/A')}")
        print(f"   Readability: {analysis.get('readability_score', 'N/A')}")
        print(f"   Completeness: {analysis.get('completeness_score', 'N/A')}")
        
        # Get gaps
        gaps = analysis.get('gaps', [])
        if gaps:
            print(f"   Gaps identified: {len(gaps)}")
            for gap in gaps[:3]:  # Show first 3
                print(f"      - {gap}")
        
        # Get suggestions
        suggestions = analysis.get('suggestions', [])
        if suggestions:
            print(f"   Suggestions: {len(suggestions)}")
            for suggestion in suggestions[:3]:  # Show first 3
                print(f"      - {suggestion}")
        
        return {
            'title': title,
            'pdf_path': pdf_path,
            'analysis': analysis,
            'file_size_kb': pdf_path.stat().st_size / 1024
        }
        
    except Exception as e:
        print(f"   ❌ Error analyzing PDF: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Analyze all campaign PDFs."""
    print("=" * 60)
    print("D&D Campaign PDF Quality Analysis")
    print("=" * 60)
    
    work_effort_dir = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution"
    
    pdfs_to_analyze = [
        ("Player's Guide", work_effort_dir / "campaign_players_guide.pdf"),
        ("DM Guide", work_effort_dir / "campaign_dm_guide.pdf"),
        ("Encounter Sheets", work_effort_dir / "campaign_encounters.pdf"),
        ("World Map", work_effort_dir / "campaign_world_map.pdf"),
        ("NPC Cards", work_effort_dir / "campaign_npcs.pdf"),
    ]
    
    results = []
    
    for title, pdf_path in pdfs_to_analyze:
        result = analyze_pdf(pdf_path, title)
        if result:
            results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Analysis Summary")
    print("=" * 60)
    
    if results:
        print(f"\nAnalyzed {len(results)} PDFs:")
        for result in results:
            print(f"\n   {result['title']}:")
            print(f"      Size: {result['file_size_kb']:.1f} KB")
            analysis = result['analysis']
            if 'quality_score' in analysis:
                print(f"      Quality: {analysis['quality_score']:.2f}/1.0")
            if 'readability_score' in analysis:
                print(f"      Readability: {analysis['readability_score']:.2f}/1.0")
            if 'completeness_score' in analysis:
                print(f"      Completeness: {analysis['completeness_score']:.2f}/1.0")
        
        # Save results to JSON
        results_file = work_effort_dir / "pdf_analysis_results.json"
        import json
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n✅ Analysis results saved to: {results_file}")
    else:
        print("\n❌ No PDFs were successfully analyzed")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

```

## Evolution Report Script

**File:** `examples/generate_dnd_evolution_report.py`

```python
"""
Generate D&D Campaign PDF Evolution Report
==========================================

Creates a comprehensive PDF report documenting the PDF evolution testing process
and findings from the D&D campaign document generation.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.evolution.pdf_generator import PDFGenerator


def main():
    """Generate evolution report PDF."""
    print("📄 Generating D&D Campaign PDF Evolution Report...")
    
    findings_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "pdf_evolution_findings.md"
    output_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "pdf_evolution_report.pdf"
    
    if not findings_path.exists():
        print(f"❌ Findings document not found: {findings_path}")
        return 1
    
    content = findings_path.read_text()
    
    generator = PDFGenerator.from_content(
        content=content,
        title="D&D Campaign PDF Evolution Report",
        style="premium",
        output_path=output_path
    )
    
    result = generator.save(
        output_path=output_path,
        convert_to_png=True,
        png_dpi=300
    )
    
    print(f"✅ Evolution report generated: {result}")
    print(f"   📄 {output_path.name}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

```



---

# Appendices

## Work Effort Information

- **Work Effort ID:** WE-260112-jqkn
- **Title:** D&D Campaign PDF Evolution
- **Purpose:** Test and evolve PDF generator with diverse document types
- **Status:** Active

## Files Included

This document consolidates all content from the work effort, including:

- Campaign planning documents
- Generated PDFs (referenced)
- Quality analysis results
- Evolution findings
- Code examples
- Screenshots and visual references

