= Introduction
WAFT turns software development into a DnD flavored loop where AI agents evolve through ethical choices. This book summarizes the core mechanics used by the WAFT game system.

== Quick Start
#list(
  [Choose a quest from the work effort queue.],
  [Roll or assign ability scores for the being.],
  [Resolve encounters using skill checks or combat actions.],
  [Award XP, karma, and scint based on outcomes.],
  [Level up and evolve when thresholds are met.],
)

= Character Creation
WAFT uses a Warforged Wizard archetype as the default being. Adjust class, race, and features as needed.

== Character Sheet Components
#table(
  columns: (auto, auto, 1fr),
  table.header([Component], [Example], [Notes]),
  [Ability Scores], [INT 16, WIS 14], [STR, DEX, CON, INT, WIS, CHA],
  [Hit Points], [45 / 50], [Current and max HP],
  [Armor Class], [15], [10 + DEX + armor],
  [Spell Slots], [Level 1: 3 / 4], [Available spell slots],
  [Hit Dice], [5 / 5 d6], [Recovery resource],
  [Level], [3], [Character level],
  [XP], [1200], [Experience points],
)

= Core Mechanics

== Ability Scores
#table(
  columns: (auto, auto, 1fr),
  table.header([Ability], [Score Range], [Use Case]),
  [Strength (STR)], [8-15], [Physical tasks, carrying capacity],
  [Dexterity (DEX)], [10-16], [Armor class, initiative, finesse weapons],
  [Constitution (CON)], [12-16], [Hit points, saving throws, endurance],
  [Intelligence (INT)], [14-18], [Spellcasting, investigation, logic],
  [Wisdom (WIS)], [12-16], [Perception, insight, spell saves],
  [Charisma (CHA)], [10-14], [Social interactions, spellcasting],
)

== Combat Actions
#table(
  columns: (auto, 1fr),
  table.header([Action], [Description]),
  [Attack], [Weapon or spell attack],
  [Skill Check], [Ability + proficiency vs DC],
  [Saving Throw], [Resist or avoid an effect],
  [Spell Casting], [Use a spell slot to cast],
  [Movement], [Move up to speed per turn],
)

== Level Progression (Sample)
#table(
  columns: (auto, auto, auto, 1fr),
  table.header([Level], [XP], [Prof Bonus], [Feature]),
  [1], [0], [+2], [Spellcasting, awakened spellbook],
  [2], [300], [+2], [Arcane recovery],
  [3], [900], [+2], [Second level spells],
  [4], [2700], [+2], [Ability score improvement],
  [5], [6500], [+3], [Third level spells],
)

== Spell Slots (Sample)
#table(
  columns: (auto, auto, 1fr),
  table.header([Spell Level], [Slots], [Example Spells]),
  [1st], [4], [Mage Hand, Detect Magic, Shield],
  [2nd], [3], [Mirror Image, Misty Step],
  [3rd], [2], [Counterspell, Fireball],
  [4th], [1], [Polymorph, Dimension Door],
)

= Quest System

== Quest Types
#table(
  columns: (auto, auto, auto, 1fr),
  table.header([Type], [Duration], [Rewards], [Notes]),
  [Quick Quest], [1-2 hours], [Low], [Single ticket],
  [Standard Quest], [1-2 days], [Medium], [Multiple tickets],
  [Epic Quest], [1-2 weeks], [High], [Complex work effort],
  [Campaign], [1+ months], [Very high], [Multiple work efforts],
)

== Encounter Types
#table(
  columns: (auto, 1fr, 1fr),
  table.header([Type], [Description], [Priority]),
  [Combat], [Direct conflict], [P0 Critical],
  [Skill Challenge], [Problem solving], [P1 High],
  [Social], [Negotiation or persuasion], [P2 Routine],
  [Exploration], [Discovery or investigation], [P3 Backlog],
)

== Difficulty Levels
#table(
  columns: (auto, auto, auto, 1fr),
  table.header([Difficulty], [XP Reward], [Scint Multiplier], [Notes]),
  [Easy], [25], [1.0x], [Low risk],
  [Medium], [50], [1.5x], [Moderate challenge],
  [Hard], [100], [2.0x], [Significant challenge],
  [Deadly], [200+], [3.0x], [Extreme challenge],
)

= Karma System
Karma ranges from -100 to +100 and influences evolution paths.

#list(
  [High order (50 to 100): Architect path with defense and structure bonuses.],
  [Neutral (-10 to 10): Balanced path with adaptable traits.],
  [High chaos (-100 to -50): Glitch path with disruption and offense bonuses.],
)

= Scint Economy
Scint represents raw creation energy earned through synthesis and problem solving.

#list(
  [Scint pool typically ranges 0 to 200.],
  [Spells consume scint by level, from 0 for cantrips to 30+ for high level spells.],
  [Evolution checks trigger when scint exceeds thresholds.],
)

= Campaign Loop
#list(
  [Plan: select quests and prepare the party.],
  [Engage: run encounters, exploration, and lore.],
  [Resolve: grant XP, karma, and scint.],
  [Evolve: level up and apply path bonuses.],
)
