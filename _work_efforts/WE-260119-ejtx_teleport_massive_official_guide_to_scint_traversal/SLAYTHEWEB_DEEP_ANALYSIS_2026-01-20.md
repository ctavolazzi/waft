# Slay the Web Deep Analysis (2026-01-20)

## Executive Summary
Slay the Web is a Slay-the-Spire-style deckbuilding roguelike implemented as a UI-agnostic game engine with a Preact-based web UI. The core design is a single immutable-ish game state object updated by synchronous action functions, coordinated by an action manager queue (future/past/undo). Combat, dungeon traversal, and card rules live in `src/game/*`, while content definitions (cards, dungeons, monster rooms) live under `src/content/*`. A lightweight backend module can POST a minimized run state and action history.

## Core Architecture

### 1) Single State Object
- All game data lives in one `State` object (player, deck, piles, dungeon, timestamps).
- State is treated as immutable via `immer` (`produce`) in most actions.
- Essential fields: `turn`, `deck`, `drawPile`, `hand`, `discardPile`, `exhaustPile`, `player`, `dungeon`, `createdAt`, `endedAt`, `won`, `didCheat`.

Key files:
- `src/game/actions.js`
- `src/game/utils-state.js`

### 2) Action System
- Actions are synchronous functions that take `state` and optional props, and return a new state.
- An `ActionManager` queues future actions and stores past actions for undo/redo.
- Actions are invoked by name: `{type: 'playCard', ...}` routed via `actions[action.type]`.

Key files:
- `src/game/action-manager.js`
- `src/game/actions.js`

### 3) Game Loop
- `createNewGame()` sets up a new state, dungeon, starter deck, and initial draw.
- `endTurn()` sequence: discard hand -> apply regen -> monsters act -> decrease powers -> check game over -> start new turn if alive.
- `move()` handles dungeon progression and encounter reset.

Key files:
- `src/game/new-game.js`
- `src/game/actions.js`

## Combat & Cards

### Cards
- Cards are plain objects converted to `Card` class instances on creation.
- Core card properties: `name`, `type`, `energy`, `damage`, `block`, `target`, `powers`, `actions`, `conditions`, `exhaust`.
- Upgrade path via `cardUpgrades` with `createCard(name, true)`.

Key files:
- `src/game/cards.js`
- `src/content/cards/*`

### Playing a Card
- `playCard` validates energy + target, discards the card, spends energy, applies block.
- Attacks apply strength/weak modifiers, then `removeHealth`.
- Card powers (`card.powers`) and card actions (`card.actions`) are applied in order.

Key files:
- `src/game/actions.js` (`playCard`, `useCardActions`, `applyCardPowers`)

### Conditions
- `conditionsAreValid` gates card playability.
- Built-in conditions: `onlyType`, `healthPercentageAbove`, `healthPercentageBelow`.

Key files:
- `src/game/conditions.js`

### Powers
- Powers are modeled as lightweight classes with `use()` for stack effects.
- Includes `regen`, `vulnerable`, `weak`, `strength`.
- Player/monster powers decrement each turn.

Key files:
- `src/game/powers.js`
- `src/game/actions.js` (power application + decrement)

## Dungeon & Rooms

### Dungeon Graph
- Procedurally generated graph of floors with room nodes.
- Paths are precomputed; `pathTaken` tracks actual traversal.
- Node types: `start`, `M` (monster), `C` (campfire), `E` (elite), `boss`.

Key files:
- `src/game/dungeon.js`
- `src/game/rooms.js`

### Rooms
- `StartRoom`, `CampfireRoom`, `MonsterRoom` are basic room factories.
- Campfire stores choice + reward.

Key files:
- `src/game/rooms.js`

## Monster AI
- Monsters define a list of `intents` (damage, block, weak, vulnerable).
- `takeMonsterTurn` cycles through intents and applies effects.
- Monster damage respects weak; player death sets `endedAt`.

Key files:
- `src/game/monster.js`
- `src/game/actions.js` (`takeMonsterTurn`, `playMonsterActions`)

## Backend Run Logging
- `backend.js` posts a minimized run state (`MinifiedState`) and past actions.
- Large state parts (piles, paths) are removed for storage.
- API endpoint: `https://api.slaytheweb.cards/api/runs`.

Key file:
- `src/game/backend.js`

## Tests & Validation Signals
- Tests create a game, apply actions, and assert state transitions.
- Confirms deck shuffles, action queueing, dungeon movement, and power rules.

Key files:
- `tests/actions.js`
- `tests/game.js`
- `tests/dungeon.js`

## Autoplay & Simulation Signals (from tests)
- `tests/dungeon-complete-run.js` shows a headless loop: iterate floors, for each monster room play cards while energy remains, target the first alive monster, then `endTurn()` until the room completes or a max turn cap is hit.
- Baseline heuristic used: pick the first card with `energy <= currentEnergy`; target `player` if card target is player, otherwise `enemy{firstAliveIndex}`.
- The test uses `iddqd` (cheat) to set all monsters to 1 HP, indicating a simple “fast win” path for dungeon-completion validation.
- `tests/ai.js` validates monster intent cycling and multi-monster damage sequencing (player block reduced between each monster attack).

Key files:
- `tests/dungeon-complete-run.js`
- `tests/ai.js`

## Teleport Massive Mapping (Implications)

### Strong patterns to reuse
- **Single immutable state**: clean and easy to serialize for telemetry/autoplay.
- **Action queue**: future/past logs map directly to evidence logs.
- **Card action pipeline**: card actions + conditions align with Teleport Massive card taxonomy.
- **Dungeon graph**: graph + pathTaken works as a “reality traversal” substrate.

### Potential adaptations
- Replace `player.powers` with Teleport “scint energies” and “fracture conditions”.
- Use `backend.minimizeGameState` pattern for autoplay run snapshots.
- Map `intents` to “realm intent model” for monsters/encounters.

## Reference File Map
- Core engine: `src/game/*`
- Content definitions: `src/content/*`
- Tests: `tests/*`
- UI: `src/ui/*` (not needed for code-only autoplay)
