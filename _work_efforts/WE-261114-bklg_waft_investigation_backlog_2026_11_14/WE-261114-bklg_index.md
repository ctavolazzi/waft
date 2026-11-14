---
id: WE-261114-bklg
title: "WAFT investigation backlog 2026-11-14"
status: active
created: 2026-11-14T15:43:40.231Z
last_updated: 2026-11-14T15:43:48.986Z
objective: "A numbered list of things to investigate, decide or expand on, found while setting up and running WAFT"
labels: ['investigation', 'waft']
---

# WAFT investigation backlog 2026-11-14

## Objective

A numbered list of things to investigate, decide or expand on, found while setting up and running WAFT

## Description

Full write-up in INVESTIGATION_BACKLOG.md in this folder. Ticket titles carry the same ids (A1 to R8) plus S1 to S3 for the setup done in this session.

## Tickets

| Ticket | Title | Status |
|--------|-------|--------|
| [[TKT-bklg-001_a1_add_the_missing_get_tracer_imports_in_two_core|TKT-bklg-001]] | A1 Add the missing get_tracer imports in two core modules | pending |
| [[TKT-bklg-002_a2_fix_span_end_on_a_span_that_has_no_end_method|TKT-bklg-002]] | A2 Fix span.end() on a Span that has no end method | pending |
| [[TKT-bklg-003_a3_import_spanstatus_where_input_transformer_uses|TKT-bklg-003]] | A3 Import SpanStatus where input_transformer uses it | pending |
| [[TKT-bklg-004_a4_rerun_the_suite_after_a1_to_a3_and_list_what_is|TKT-bklg-004]] | A4 Rerun the suite after A1 to A3 and list what is still red | pending |
| [[TKT-bklg-005_a5_find_how_the_half_wired_tracing_change_reached|TKT-bklg-005]] | A5 Find how the half-wired tracing change reached main | pending |
| [[TKT-bklg-006_a6_add_the_clirunner_import_to_tests_test_commands|TKT-bklg-006]] | A6 Add the CliRunner import to tests/test_commands.py | pending |
| [[TKT-bklg-007_a7_decide_the_fate_of_the_three_test_files_that_fa|TKT-bklg-007]] | A7 Decide the fate of the three test files that fail at collection | pending |
| [[TKT-bklg-008_a8_explain_the_setup_error_in_tests_real_proof_tes|TKT-bklg-008]] | A8 Explain the setup error in tests/real_proof_test.py | pending |
| [[TKT-bklg-009_a9_make_the_six_pdf_to_png_tests_pass_or_skip|TKT-bklg-009]] | A9 Make the six PDF-to-PNG tests pass or skip | pending |
| [[TKT-bklg-010_a10_stop_tests_from_writing_trace_files_into_the_t|TKT-bklg-010]] | A10 Stop tests from writing trace files into the tracked tree | pending |
| [[TKT-bklg-011_a11_find_why_uv_rewrites_uv_lock_on_every_run|TKT-bklg-011]] | A11 Find why uv rewrites uv.lock on every run | pending |
| [[TKT-bklg-012_a12_clear_the_deprecation_warnings|TKT-bklg-012]] | A12 Clear the deprecation warnings | pending |
| [[TKT-bklg-013_a13_find_out_whether_the_root_level_suites_in_test|TKT-bklg-013]] | A13 Find out whether the root-level suites in tests/ are run anywhere | pending |
| [[TKT-bklg-014_a14_add_pytest_configuration_to_pyproject_toml|TKT-bklg-014]] | A14 Add pytest configuration to pyproject.toml | pending |
| [[TKT-bklg-015_a15_measure_coverage_over_all_of_src|TKT-bklg-015]] | A15 Measure coverage over all of src | pending |
| [[TKT-bklg-016_a16_review_the_23_skips_8_xfails_and_the_1_xpass|TKT-bklg-016]] | A16 Review the 23 skips, 8 xfails and the 1 xpass | pending |
| [[TKT-bklg-017_a17_run_the_suite_on_python_3_12_and_3_13|TKT-bklg-017]] | A17 Run the suite on Python 3.12 and 3.13 | pending |
| [[TKT-bklg-018_a18_fix_the_31_undefined_names_that_ruff_finds|TKT-bklg-018]] | A18 Fix the 31 undefined names that ruff finds | pending |
| [[TKT-bklg-019_b1_fix_the_package_list_the_wheel_holds_202_of_516|TKT-bklg-019]] | B1 Fix the package list: the wheel holds 202 of 516 Python files | pending |
| [[TKT-bklg-020_b2_make_a_wheel_install_start_waft_help_fails_toda|TKT-bklg-020]] | B2 Make a wheel install start: waft --help fails today | pending |
| [[TKT-bklg-021_b3_ship_template_data_files_in_the_wheel|TKT-bklg-021]] | B3 Ship template data files in the wheel | pending |
| [[TKT-bklg-022_b4_make_the_empirica_dependency_installable_with_o|TKT-bklg-022]] | B4 Make the empirica dependency installable with one command | pending |
| [[TKT-bklg-023_b5_test_waft_against_current_empirica|TKT-bklg-023]] | B5 Test WAFT against current Empirica | pending |
| [[TKT-bklg-024_b6_split_heavy_dependencies_into_extras|TKT-bklg-024]] | B6 Split heavy dependencies into extras | pending |
| [[TKT-bklg-025_b7_align_the_python_version_settings|TKT-bklg-025]] | B7 Align the Python version settings | pending |
| [[TKT-bklg-026_b8_decide_the_package_name|TKT-bklg-026]] | B8 Decide the package name | pending |
| [[TKT-bklg-027_b9_define_a_release_procedure_and_tag_it|TKT-bklg-027]] | B9 Define a release procedure and tag it | pending |
| [[TKT-bklg-028_b10_build_and_run_the_dockerfile|TKT-bklg-028]] | B10 Build and run the Dockerfile | pending |
| [[TKT-bklg-029_b11_test_on_macos_and_windows|TKT-bklg-029]] | B11 Test on macOS and Windows | pending |
| [[TKT-bklg-030_c1_run_the_whole_test_suite_in_ci|TKT-bklg-030]] | C1 Run the whole test suite in CI | pending |
| [[TKT-bklg-031_c2_find_out_whether_the_staging_gate_can_ever_run|TKT-bklg-031]] | C2 Find out whether the staging gate can ever run | pending |
| [[TKT-bklg-032_c3_remove_the_debug_blocks_the_staging_gate_greps|TKT-bklg-032]] | C3 Remove the debug blocks the staging gate greps for | pending |
| [[TKT-bklg-033_c4_triage_the_remote_branches_the_open_pr_and_the|TKT-bklg-033]] | C4 Triage the remote branches, the open PR and the open issue | pending |
| [[TKT-bklg-034_c5_add_dependency_update_automation|TKT-bklg-034]] | C5 Add dependency update automation | pending |
| [[TKT-bklg-035_c6_add_secret_and_vulnerability_scanning_to_ci|TKT-bklg-035]] | C6 Add secret and vulnerability scanning to CI | pending |
| [[TKT-bklg-036_c7_build_and_smoke_test_the_artifacts_in_ci|TKT-bklg-036]] | C7 Build and smoke-test the artifacts in CI | pending |
| [[TKT-bklg-037_c8_pin_tool_and_runner_versions_in_workflows|TKT-bklg-037]] | C8 Pin tool and runner versions in workflows | pending |
| [[TKT-bklg-038_c9_measure_ci_health_over_the_last_100_runs|TKT-bklg-038]] | C9 Measure CI health over the last 100 runs | pending |
| [[TKT-bklg-039_c10_turn_on_ruff_f821_for_all_of_src_in_ci|TKT-bklg-039]] | C10 Turn on ruff F821 for all of src in CI | pending |
| [[TKT-bklg-040_d1_untrack_the_9_015_node_modules_files|TKT-bklg-040]] | D1 Untrack the 9,015 node_modules files | pending |
| [[TKT-bklg-041_d2_decide_where_generated_pdfs_live|TKT-bklg-041]] | D2 Decide where generated PDFs live | pending |
| [[TKT-bklg-042_d3_decide_what_to_do_about_the_largest_tracked_fil|TKT-bklg-042]] | D3 Decide what to do about the largest tracked files | pending |
| [[TKT-bklg-043_d4_check_the_rights_to_third_party_files_in_a_publ|TKT-bklg-043]] | D4 Check the rights to third-party files in a public MIT repo | pending |
| [[TKT-bklg-044_d5_resolve_the_eight_uninitialized_submodules|TKT-bklg-044]] | D5 Resolve the eight uninitialized submodules | pending |
| [[TKT-bklg-045_d6_design_the_target_layout_for_the_repo_root|TKT-bklg-045]] | D6 Design the target layout for the repo root | pending |
| [[TKT-bklg-046_d7_untrack_tool_state|TKT-bklg-046]] | D7 Untrack tool state | pending |
| [[TKT-bklg-047_d8_move_runtime_data_out_of_git|TKT-bklg-047]] | D8 Move runtime data out of git | pending |
| [[TKT-bklg-048_d9_remove_hardcoded_users_ctavolazzi_paths|TKT-bklg-048]] | D9 Remove hardcoded /Users/ctavolazzi paths | pending |
| [[TKT-bklg-049_d10_spin_parked_projects_out_of_the_lab_repo|TKT-bklg-049]] | D10 Spin parked projects out of the lab repo | pending |
| [[TKT-bklg-050_d11_set_a_size_budget|TKT-bklg-050]] | D11 Set a size budget | pending |
| [[TKT-bklg-051_d12_decide_whether_to_rewrite_history|TKT-bklg-051]] | D12 Decide whether to rewrite history | pending |
| [[TKT-bklg-052_e1_rotate_or_retire_the_two_crypto_keys_that_are_s|TKT-bklg-052]] | E1 Rotate or retire the two crypto keys that are still public in history | pending |
| [[TKT-bklg-053_e2_review_api_authentication|TKT-bklg-053]] | E2 Review API authentication | pending |
| [[TKT-bklg-054_e3_review_cors_settings|TKT-bklg-054]] | E3 Review CORS settings | pending |
| [[TKT-bklg-055_e4_audit_shell_and_subprocess_calls|TKT-bklg-055]] | E4 Audit shell and subprocess calls | pending |
| [[TKT-bklg-056_e5_remove_leftover_agent_logging_blocks|TKT-bklg-056]] | E5 Remove leftover agent logging blocks | pending |
| [[TKT-bklg-057_e6_scan_the_full_history_for_secrets|TKT-bklg-057]] | E6 Scan the full history for secrets | pending |
| [[TKT-bklg-058_e7_audit_dependencies_for_known_vulnerabilities|TKT-bklg-058]] | E7 Audit dependencies for known vulnerabilities | pending |
| [[TKT-bklg-059_e8_review_the_electron_app_s_security_settings|TKT-bklg-059]] | E8 Review the Electron app's security settings | pending |
| [[TKT-bklg-060_e9_test_that_pdf_redaction_removes_the_text|TKT-bklg-060]] | E9 Test that PDF redaction removes the text | pending |
| [[TKT-bklg-061_e10_test_the_api_and_cli_for_path_traversal|TKT-bklg-061]] | E10 Test the API and CLI for path traversal | pending |
| [[TKT-bklg-062_e11_define_the_sandbox_for_self_modifying_code|TKT-bklg-062]] | E11 Define the sandbox for self-modifying code | pending |
| [[TKT-bklg-063_e12_decide_what_the_realm_hmac_protects|TKT-bklg-063]] | E12 Decide what the realm HMAC protects | pending |
| [[TKT-bklg-064_f1_split_main_py_into_command_modules|TKT-bklg-064]] | F1 Split main.py into command modules | pending |
| [[TKT-bklg-065_f2_fix_variant_identity_in_waft_evolve|TKT-bklg-065]] | F2 Fix variant identity in waft evolve | pending |
| [[TKT-bklg-066_f3_find_out_what_evolution_operates_on|TKT-bklg-066]] | F3 Find out what \"evolution\" operates on | pending |
| [[TKT-bklg-067_f4_resolve_the_overlapping_names_pyrite_empirica_a|TKT-bklg-067]] | F4 Resolve the overlapping names pyrite, empirica and fogsift | pending |
| [[TKT-bklg-068_f5_move_demos_and_generators_out_of_the_package_ro|TKT-bklg-068]] | F5 Move demos and generators out of the package root | pending |
| [[TKT-bklg-069_f6_remove_versioned_duplicates|TKT-bklg-069]] | F6 Remove versioned duplicates | pending |
| [[TKT-bklg-070_f7_run_dead_code_detection|TKT-bklg-070]] | F7 Run dead-code detection | pending |
| [[TKT-bklg-071_f8_check_layering_and_import_cycles|TKT-bklg-071]] | F8 Check layering and import cycles | pending |
| [[TKT-bklg-072_f9_shrink_the_ruff_exclusion_list|TKT-bklg-072]] | F9 Shrink the ruff exclusion list | pending |
| [[TKT-bklg-073_f10_measure_type_check_errors|TKT-bklg-073]] | F10 Measure type-check errors | pending |
| [[TKT-bklg-074_f11_review_global_singletons|TKT-bklg-074]] | F11 Review global singletons | pending |
| [[TKT-bklg-075_f12_inventory_the_data_stores|TKT-bklg-075]] | F12 Inventory the data stores | pending |
| [[TKT-bklg-076_f13_choose_which_front_ends_to_keep|TKT-bklg-076]] | F13 Choose which front ends to keep | pending |
| [[TKT-bklg-077_f14_find_why_a_first_quickstart_run_changed_tracke|TKT-bklg-077]] | F14 Find why a first quickstart run changed tracked files in the checkout | pending |
| [[TKT-bklg-078_f15_centralize_configuration|TKT-bklg-078]] | F15 Centralize configuration | pending |
| [[TKT-bklg-079_f16_pin_down_the_api_error_contract|TKT-bklg-079]] | F16 Pin down the API error contract | pending |
| [[TKT-bklg-080_f17_pick_one_observability_story|TKT-bklg-080]] | F17 Pick one observability story | pending |
| [[TKT-bklg-081_g1_make_one_index_for_the_3_680_markdown_files|TKT-bklg-081]] | G1 Make one index for the 3,680 Markdown files | pending |
| [[TKT-bklg-082_g2_fix_docs_that_name_commands_the_cli_does_not_ha|TKT-bklg-082]] | G2 Fix docs that name commands the CLI does not have | pending |
| [[TKT-bklg-083_g3_build_a_claims_table|TKT-bklg-083]] | G3 Build a claims table | pending |
| [[TKT-bklg-084_g4_add_a_claude_md_for_this_repo|TKT-bklg-084]] | G4 Add a CLAUDE.md for this repo | pending |
| [[TKT-bklg-085_g5_date_and_triage_the_root_status_documents|TKT-bklg-085]] | G5 Date and triage the root status documents | pending |
| [[TKT-bklg-086_g6_write_a_one_page_state_md_for_waft|TKT-bklg-086]] | G6 Write a one-page STATE.md for WAFT | pending |
| [[TKT-bklg-087_g7_place_waft_in_the_business_priorities|TKT-bklg-087]] | G7 Place WAFT in the business priorities | pending |
| [[TKT-bklg-088_g8_check_whether_the_verify_score_on_a_fresh_proje|TKT-bklg-088]] | G8 Check whether the verify score on a fresh project is a false alarm | pending |
| [[TKT-bklg-089_g9_turn_the_readme_quickstart_into_a_test|TKT-bklg-089]] | G9 Turn the README quickstart into a test | pending |
| [[TKT-bklg-090_g10_check_links_and_file_references_in_docs|TKT-bklg-090]] | G10 Check links and file references in docs | pending |
| [[TKT-bklg-091_g11_decide_the_fate_of_the_field_manual_landing_pa|TKT-bklg-091]] | G11 Decide the fate of the field-manual landing page | pending |
| [[TKT-bklg-092_h1_write_the_one_sentence_purpose|TKT-bklg-092]] | H1 Write the one-sentence purpose | pending |
| [[TKT-bklg-093_h2_decide_what_moves_to_fogsift_waft|TKT-bklg-093]] | H2 Decide what moves to FogSift/waft | pending |
| [[TKT-bklg-094_h3_name_the_audience|TKT-bklg-094]] | H3 Name the audience | pending |
| [[TKT-bklg-095_h4_keep_the_repo_public_or_private_while_d4_and_e1|TKT-bklg-095]] | H4 Keep the repo public or private while D4 and E1 are open | pending |
| [[TKT-bklg-096_h5_choose_a_licence_deliberately|TKT-bklg-096]] | H5 Choose a licence deliberately | pending |
| [[TKT-bklg-097_h6_decide_whether_waft_becomes_video_content|TKT-bklg-097]] | H6 Decide whether WAFT becomes video content | pending |
| [[TKT-bklg-098_h7_decide_how_waft_could_earn_or_save_money|TKT-bklg-098]] | H7 Decide how WAFT could earn or save money | pending |
| [[TKT-bklg-099_h8_decide_how_much_time_waft_gets|TKT-bklg-099]] | H8 Decide how much time WAFT gets | pending |
| [[TKT-bklg-100_h9_check_the_name_waft_for_collisions|TKT-bklg-100]] | H9 Check the name WAFT for collisions | pending |
| [[TKT-bklg-101_i1_triage_the_132_work_efforts|TKT-bklg-101]] | I1 Triage the 132 work efforts | pending |
| [[TKT-bklg-102_i2_bridge_the_status_vocabulary_for_simpleagentos|TKT-bklg-102]] | I2 Bridge the status vocabulary for SimpleAgentOS | pending |
| [[TKT-bklg-103_i3_decide_whether_to_adopt_waft_into_the_fogsift_s|TKT-bklg-103]] | I3 Decide whether to adopt WAFT into the FogSift system | pending |
| [[TKT-bklg-104_i4_decide_where_waft_s_findings_and_unknowns_survi|TKT-bklg-104]] | I4 Decide where WAFT's findings and unknowns survive | pending |
| [[TKT-bklg-105_i5_check_commands_that_depend_on_empirica_s_thresh|TKT-bklg-105]] | I5 Check commands that depend on Empirica's threshold message | pending |
| [[TKT-bklg-106_i6_run_repowise_doc_drift_on_this_repo|TKT-bklg-106]] | I6 Run repowise doc-drift on this repo | pending |
| [[TKT-bklg-107_i7_test_that_waft_work_efforts_and_pyrite_we_write|TKT-bklg-107]] | I7 Test that waft work-efforts and pyrite we write the same format | pending |
| [[TKT-bklg-108_i8_create_the_daily_hub_for_this_work|TKT-bklg-108]] | I8 Create the daily hub for this work | pending |
| [[TKT-bklg-109_i9_close_the_three_recorded_fogsift_gaps_about_waf|TKT-bklg-109]] | I9 Close the three recorded FogSift gaps about WAFT and rerun the proof | pending |
| [[TKT-bklg-110_i10_connect_waft_s_gym_score_to_real_repository_wo|TKT-bklg-110]] | I10 Connect WAFT's gym score to real repository work | pending |
| [[TKT-bklg-111_j1_choose_the_default_pdf_engine|TKT-bklg-111]] | J1 Choose the default PDF engine | pending |
| [[TKT-bklg-112_j2_list_the_system_programs_each_command_needs|TKT-bklg-112]] | J2 List the system programs each command needs | pending |
| [[TKT-bklg-113_j3_decide_whether_waft_pdf_library_is_input_or_out|TKT-bklg-113]] | J3 Decide whether waft_pdf_library is input or output | pending |
| [[TKT-bklg-114_j4_declare_the_pdf_to_image_dependency|TKT-bklg-114]] | J4 Declare the PDF-to-image dependency | pending |
| [[TKT-bklg-115_j5_map_the_rag_module|TKT-bklg-115]] | J5 Map the RAG module | pending |
| [[TKT-bklg-116_j6_audit_the_typst_and_latex_template_licences|TKT-bklg-116]] | J6 Audit the Typst and LaTeX template licences | pending |
| [[TKT-bklg-117_k1_decide_the_home_of_the_tavern_keeper|TKT-bklg-117]] | K1 Decide the home of the Tavern Keeper | pending |
| [[TKT-bklg-118_k2_move_the_teleport_massive_material|TKT-bklg-118]] | K2 Move the Teleport Massive material | pending |
| [[TKT-bklg-119_k3_check_the_d_d_content_licensing|TKT-bklg-119]] | K3 Check the D&D content licensing | pending |
| [[TKT-bklg-120_k4_review_the_wager_and_karma_mechanics_before_any|TKT-bklg-120]] | K4 Review the wager and karma mechanics before any public release | pending |
| [[TKT-bklg-121_k5_decide_about_the_pet_device|TKT-bklg-121]] | K5 Decide about the pet device | pending |
| [[TKT-bklg-122_l1_choose_the_branch_policy|TKT-bklg-122]] | L1 Choose the branch policy | pending |
| [[TKT-bklg-123_l2_fix_the_stop_hook_conflict|TKT-bklg-123]] | L2 Fix the stop-hook conflict | pending |
| [[TKT-bklg-124_l3_add_pre_commit_checks|TKT-bklg-124]] | L3 Add pre-commit checks | pending |
| [[TKT-bklg-125_l4_add_a_justfile_or_makefile|TKT-bklg-125]] | L4 Add a Justfile or Makefile | pending |
| [[TKT-bklg-126_l5_write_the_start_and_end_of_session_routine|TKT-bklg-126]] | L5 Write the start and end of session routine | pending |
| [[TKT-bklg-127_l6_set_a_rule_for_closing_work_efforts|TKT-bklg-127]] | L6 Set a rule for closing work efforts | pending |
| [[TKT-bklg-128_l7_schedule_a_weekly_health_run|TKT-bklg-128]] | L7 Schedule a weekly health run | pending |
| [[TKT-bklg-129_l8_decide_whether_agents_may_merge_to_main|TKT-bklg-129]] | L8 Decide whether agents may merge to main | pending |
| [[TKT-bklg-130_r1_map_the_prior_art_for_evolving_and_self_improvi|TKT-bklg-130]] | R1 Map the prior art for evolving and self-improving agents | pending |
| [[TKT-bklg-131_r2_define_fitness_for_repository_work|TKT-bklg-131]] | R2 Define fitness for repository work | pending |
| [[TKT-bklg-132_r3_specify_safety_for_self_modifying_agents|TKT-bklg-132]] | R3 Specify safety for self-modifying agents | pending |
| [[TKT-bklg-133_r4_measure_whether_empirica_s_gate_changes_outcome|TKT-bklg-133]] | R4 Measure whether Empirica's gate changes outcomes | pending |
| [[TKT-bklg-134_r5_test_determinism_of_waft_evolve|TKT-bklg-134]] | R5 Test determinism of waft evolve | pending |
| [[TKT-bklg-135_r6_write_a_formal_genome_spec_with_property_tests|TKT-bklg-135]] | R6 Write a formal genome spec with property tests | pending |
| [[TKT-bklg-136_r7_plan_a_public_benchmark|TKT-bklg-136]] | R7 Plan a public benchmark | pending |
| [[TKT-bklg-137_r8_study_how_the_front_ends_could_become_one|TKT-bklg-137]] | R8 Study how the front ends could become one | pending |
| [[TKT-bklg-138_s1_fetch_empirica_1_2_3_into_unified_empirica_so_u|TKT-bklg-138]] | S1 Fetch empirica 1.2.3 into _unified/empirica so uv sync can resolve it | completed |
| [[TKT-bklg-139_s2_run_uv_sync_extra_dev_and_confirm_the_waft_cli|TKT-bklg-139]] | S2 Run uv sync --extra dev and confirm the waft CLI starts from the checkout | completed |
| [[TKT-bklg-140_s3_measure_the_baseline_tests_ruff_wheel_ci_branch|TKT-bklg-140]] | S3 Measure the baseline: tests, ruff, wheel, CI, branches, sizes, work efforts | completed |

## Read first

[INVESTIGATION_BACKLOG.md](INVESTIGATION_BACKLOG.md) in this folder holds the evidence and the first step for every ticket, the baseline numbers, and a record of what this session did and did not change. Ticket ids in the table below (A1 to R8, S1 to S3) match its headings.

## Progress

- 2026-11-14: environment set up (S1, S2), baseline measured (S3). Those three tickets are completed; the other 137 are open.
- Ticket counts: 137 backlog items, tagged measured 51, read 50, question 36; owner agent 87, CT 30, research 20; priority P1 26, P2 53, P3 58.
- The Tickets table above is the single record of per-ticket status.
- Nothing in `src/` was changed. A1 to A3 were tested as a temporary edit (25 failed tests became 15) and reverted.

## Next Steps

1. Review the first ten in INVESTIGATION_BACKLOG.md. B1 and B2 come first: a wheel built from this repo cannot start the CLI.
2. CT decides the tickets owned by `CT`, starting with G7 (where WAFT sits in the priorities) and H1 (what WAFT is for).
3. Hand `agent` tickets to a coding agent one group at a time (A, then B and C), and `research` tickets to a more capable model.
4. Flip each ticket's `status` as it lands (`fogsift.py ticket status --we WE-261114-bklg --id TKT-bklg-NNN --status completed`), then `we sync`.
5. Set this work effort's `status` to completed when every ticket is done, or close the ones CT drops.

## Related

- Docs: [INVESTIGATION_BACKLOG.md](INVESTIGATION_BACKLOG.md)
- Cross-repo context: `_workbench/fogsift-system/FINDINGS.md` (WAFT gaps #43, #44, #236) and `_workbench/_work_efforts/WE-261109-r1h3_plan_of_action_across_the_12_repos`
- PRs: none opened
