#import "@preview/bananote:0.1.1": *

#show: note.with(
  title: [Teleport Massive Card Game MVP Guide],
  authors: (
    ([ctavolazzi], [WAFT]),
  ),
  date: datetime(year: 2026, month: 1, day: 20),
  version: "0.1"
)

#abstract[
This guide adapts Slay the Web mechanics into a Teleport Massive-themed MVP. It outlines the core loop, card taxonomy, energy economy, dungeon/room/intent model, content pipeline, and testing approach.
]

= Goals
- Define the minimal playable loop for the Teleport Massive card game.
- Map Slay the Web mechanics to Teleport Massive narrative framing.
- Produce a structure that can feed autoplay + telemetry.

= Core Loop
1. Initialize run state (deck, energy, player health, dungeon graph).
2. Enter room and draw hand.
3. Play cards until out of energy or end turn.
4. Resolve monster intents.
5. Apply end-of-turn effects and advance room.
6. Repeat until boss room cleared or player defeated.

= Card Taxonomy
- Attack: direct damage or multi-target damage.
- Skill: block, draw, or utility manipulation.
- Power: persistent effects (regen, focus, vulnerability).
- Status: negative transient cards (fracture, entropy).
- Curse: persistent negative cards that clog the deck.

= Energy Economy
- Baseline energy: 3 per turn.
- Energy gain/restore tied to "Scint alignment" cards.
- Energy loss tied to "Fracture" debuffs.
- Energy scaling for elites and boss encounters.

= Dungeon / Room / Intent Model
- Dungeon is a graph of nodes (floors x rooms).
- Room types: Start, Monster, Campfire, Elite, Boss.
- Each Monster has a list of intents (damage, block, apply debuff).
- Intents cycle per turn (telegraphed in UI and logged in telemetry).

= Content Pipeline
1. Define card in content registry (name, cost, target, actions).
2. Register upgrades and power interactions.
3. Define monsters and intents per room.
4. Define dungeon layouts and path rules.
5. Validate content with tests and simulation runs.

= Testing Approach
- Unit tests for actions (draw, play, damage, powers).
- Dungeon navigation tests for pathTaken + room completion.
- Autoplay runs with fixed seeds to validate balance.
- Telemetry log validation (schema and run completeness).

= Teleport Massive Narrative Framing
- Player is a Scint operator navigating fracture nodes.
- Cards represent traversal protocols, containment seals, and energy refactors.
- Powers mirror long-running field effects (stabilize, weaken, expose).
- Gates/Dealer challenges act as meta-encounters for lore and rewards.
