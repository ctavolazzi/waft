#import "@preview/bananote:0.1.1": *

#show: note.with(
  title: [DnD Scenario Command Notes],
  authors: (
    ([ctavolazzi], [WAFT]),
  ),
  date: datetime.today(),
  version: "0.1",
)

#abstract[
Notes for implementing `/dnd-scenario`, the scenario realm, and experimental iterations.
]

= Goals
- Stand up a minimal scenario engine and realm structure
- Add `/dnd-scenario` Cursor command + CLI wiring
- Persist party state, scenario history, and lore
- Add crystallize/restore hooks for iteration

= Findings
- (TBD)

= Decisions
- Keep scaffolding minimal and inline; build on existing WAFT DnD systems

= TODO
- Map existing DnD campaign/encounter integration points
- Implement ScenarioRealm + ScenarioOrchestrator skeleton
- Wire CLI options for scenario modes + state controls
- Bootstrap `_realms/dnd_scenario_realm/` structure
