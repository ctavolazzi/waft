---
id: WE-261114-dirn
title: "WAFT direction and reuse map 2026-11-14"
status: active
created: 2026-11-14T16:24:51.042Z
last_updated: 2026-11-14T19:38:48.289Z
objective: "One recommended direction for WAFT, a phased plan with a check per phase, and a map of reusable code across the 12 repos"
labels: ['direction', 'waft']
---

# WAFT direction and reuse map 2026-11-14

## Objective

One recommended direction for WAFT, a phased plan with a check per phase, and a map of reusable code across the 12 repos

## Description

Full write-up in DIRECTION_AND_REUSE.md in this folder. Builds on the investigation backlog WE-261114-bklg.

## Tickets

| Ticket | Title | Status |
|--------|-------|--------|
| [[TKT-dirn-001_p0_1_stabilize_land_backlog_a1_to_a3_a6_and_a18_so|TKT-dirn-001]] | P0.1 Stabilize: land backlog A1 to A3, A6 and A18 so the suite and ruff F821 are clean | completed |
| [[TKT-dirn-002_p0_2_stabilize_fix_the_package_list_b1_to_b3_and_p|TKT-dirn-002]] | P0.2 Stabilize: fix the package list (B1 to B3) and prove a wheel install runs waft --help | completed |
| [[TKT-dirn-003_p0_3_stabilize_run_the_whole_suite_and_ruff_f821_i|TKT-dirn-003]] | P0.3 Stabilize: run the whole suite and ruff F821 in CI (C1, C10) | in_progress |
| [[TKT-dirn-004_p0_4_stabilize_stop_the_handshake_handing_out_the|TKT-dirn-004]] | P0.4 Stabilize: stop the handshake handing out the token and require auth on writes (E16, E2) | completed |
| [[TKT-dirn-005_p0_5_stabilize_upgrade_the_fixable_vulnerable_depe|TKT-dirn-005]] | P0.5 Stabilize: upgrade the fixable vulnerable dependencies (E7) | completed |
| [[TKT-dirn-006_p1_1_honest_loop_move_src_gym_rpg_into_the_package|TKT-dirn-006]] | P1.1 Honest loop: move src/gym/rpg into the package as waft.gym | completed |
| [[TKT-dirn-007_p1_2_honest_loop_port_the_fogsift_lab_loop_into_wa|TKT-dirn-007]] | P1.2 Honest loop: port the FogSift lab loop into waft.lab and make waft evolve use it | completed |
| [[TKT-dirn-008_p1_3_honest_loop_record_every_lab_run_in_a_logbook|TKT-dirn-008]] | P1.3 Honest loop: record every lab run in a Logbook (waft.record) | completed |
| [[TKT-dirn-009_p1_4_honest_loop_test_that_the_same_seed_gives_the|TKT-dirn-009]] | P1.4 Honest loop: test that the same seed gives the same head hash and ids are unique | completed |
| [[TKT-dirn-010_p2_1_real_agents_define_the_agent_protocol_and_kee|TKT-dirn-010]] | P2.1 Real agents: define the agent protocol and keep the deterministic mock | completed |
| [[TKT-dirn-011_p2_2_real_agents_add_a_local_model_provider_over_h|TKT-dirn-011]] | P2.2 Real agents: add a local model provider over HTTP behind Door Guy | in_progress |
| [[TKT-dirn-012_p2_3_real_agents_add_hosted_providers_behind_a_fla|TKT-dirn-012]] | P2.3 Real agents: add hosted providers behind a flag with a fallback chain and a budget | completed |
| [[TKT-dirn-013_p2_4_real_agents_add_a_recorded_fake_model_so_test|TKT-dirn-013]] | P2.4 Real agents: add a recorded fake model so tests never touch the network | completed |
| [[TKT-dirn-014_p3_1_real_tasks_add_held_out_and_harder_quests_bec|TKT-dirn-014]] | P3.1 Real tasks: add held-out and harder quests because the gym saturates at 1.00 by generation 9 | pending |
| [[TKT-dirn-015_p3_2_real_tasks_add_planted_defect_repositories_sc|TKT-dirn-015]] | P3.2 Real tasks: add planted-defect repositories scored by recall and precision | pending |
| [[TKT-dirn-016_p3_3_real_tasks_measure_whether_gym_fitness_predic|TKT-dirn-016]] | P3.3 Real tasks: measure whether gym fitness predicts repository-task results | pending |
| [[TKT-dirn-017_p4_1_one_surface_one_read_only_report_built_from_t|TKT-dirn-017]] | P4.1 One surface: one read-only report built from the Logbook, linked from the README | completed |
| [[TKT-dirn-018_p4_2_one_surface_fill_the_readme_claims_table_from|TKT-dirn-018]] | P4.2 One surface: fill the README claims table from real runs | pending |
| [[TKT-dirn-019_p5_1_trim_move_the_parked_products_out_of_the_core|TKT-dirn-019]] | P5.1 Trim: move the parked products out of the core package | pending |
| [[TKT-dirn-020_d1_decide_copy_fogsift_code_into_public_mit_waft_o|TKT-dirn-020]] | D1 Decide: copy FogSift code into public MIT WAFT, or depend on it | in_progress |
| [[TKT-dirn-021_d2_decide_what_the_waft_core_is_and_what_moves_out|TKT-dirn-021]] | D2 Decide: what the WAFT core is and what moves out | pending |
| [[TKT-dirn-022_d3_decide_model_and_api_budget_for_real_agents|TKT-dirn-022]] | D3 Decide: model and API budget for real agents | pending |

## Read first

[DIRECTION_AND_REUSE.md](DIRECTION_AND_REUSE.md) in this folder: the recommendation, what was measured for it, the target shape, the phases with a check for each, the reuse map across the 12 repos, and three decisions for CT. Each ticket's Notes say how to do it, which code to reuse, and when it is done.

## Progress

- 2026-11-14: direction proposed and reuse map written. Nothing built; every ticket is open.
- The recommendation: make WAFT's core the loop that already half exists: its own gym (`src/gym/rpg`), FogSift's seeded lab loop (`_workbench/fogsift-system/checks/waft_lab.py`) and FogSift's Logbook as the run record, then a real model client ported from `tavern-keeper-bot`.
- 2026-11-14, build pass: P0.1, P0.2, P0.4, P0.5, P1.1 to P1.4, P2.1, P2.3, P2.4 and P4.1 completed; P0.3, P2.2 and D1 in progress. See [BUILD_LOG_2026-11-14.md](BUILD_LOG_2026-11-14.md).
- The Tickets table above is the single record of per-ticket status.

## Next Steps

1. CT answers D1 (copy, depend or port), D2 (what the core is) and D3 (model budget).
2. P0 first; it overlaps the backlog's P1 items. Then P1, which is the phase that makes WAFT's main claim checkable.
3. Flip each ticket's `status` as it lands (`fogsift.py ticket status --we WE-261114-dirn --id TKT-dirn-NNN --status completed`), then `we sync`.

## Related

- Investigation backlog: `_work_efforts/WE-261114-bklg_waft_investigation_backlog_2026_11_14/`
- Sources: `_workbench/fogsift-system` (lab loop, Logbook, fixture), `tavern-keeper-bot` (model client, fake server, test harness), `_pyrite` (ledger tools), and the others in the reuse map
- PRs: none opened
