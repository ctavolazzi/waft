---
name: Being Lifecycle Attributes and Now Cycle Event Loop
overview: Add will to live, luck, decision fatigue, and pleasure/pain attributes to WAFT beings, and implement a "Now" cycle event loop that calculates all system variables, records state, and unblocks beings for decisions.
todos:
  - id: extend_being_class
    content: Extend Being class in src/waft/being.py with will_to_live, luck, decision_fatigue, pleasure, pain attributes and related methods
    status: in_progress
  - id: create_now_cycle_manager
    content: Create NowCycleManager class in src/waft/core/now_cycle.py to handle the centralized event loop
    status: pending
  - id: create_personality_alignment
    content: Create PersonalityAlignment class in src/waft/core/personality_alignment.py to calculate pleasure/pain from alignment
    status: pending
  - id: add_being_personality_system
    content: Add personality and goal tracking to Being class (since Being doesn't have AgentState)
    status: pending
  - id: create_being_decision_system
    content: Create decision-making system for beings (since they don't have OODA cycles like BaseAgent)
    status: pending
  - id: integrate_karma_access
    content: Create mechanism for beings to access karma balance through KarmaMerchant
    status: pending
  - id: implement_storage
    content: Implement state recording to Akasha, flight recorder, and being state files after each cycle
    status: pending
  - id: implement_sleep_evolution
    content: Implement sleep duration evolution system that adapts based on being needs
    status: pending
  - id: add_tests
    content: Add unit and integration tests for new attributes and cycle system
    status: pending
  - id: migration_script
    content: Create migration script to add new attributes to existing beings with defaults
    status: pending

category: dreams
confidence: 0.64
constellation_date: 2026-01-14
---

