#!/usr/bin/env python3
"""
Complete Game Generation Script using OpenHands SDK

Generates the complete Electron Tavern Game Display:
- FastAPI server
- Electron app structure
- Tests
- Documentation

Uses the recommended tool set: TerminalTool, FileEditorTool, TaskTrackerTool

Usage:
    export LLM_API_KEY="your-api-key"
    export LLM_MODEL="anthropic/claude-sonnet-4-5-20250929"  # optional
    python scripts/generate_tavern_game_complete.py
"""

import os
import sys
from pathlib import Path

try:
    from openhands.sdk import LLM, Agent, Conversation, Tool
    from openhands.tools.file_editor import FileEditorTool
    from openhands.tools.task_tracker import TaskTrackerTool
    from openhands.tools.terminal import TerminalTool
except ImportError as e:
    print("❌ Error: OpenHands SDK not installed")
    print(f"   {e}")
    print("\n   Install with:")
    print("   pip install openhands-sdk openhands-tools")
    sys.exit(1)


def main():
    # Check for API key
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        print("❌ Error: LLM_API_KEY environment variable not set")
        print("\n   Set it with:")
        print('   export LLM_API_KEY="your-api-key"')
        sys.exit(1)

    # Get model
    model = os.getenv("LLM_MODEL", "anthropic/claude-sonnet-4-5-20250929")
    base_url = os.getenv("LLM_BASE_URL", None)

    print("🚀 Generating Complete Electron Tavern Game with OpenHands SDK")
    print(f"   Model: {model}")
    print()
    print("📋 Available Tools:")
    print("   - TerminalTool: Execute bash commands")
    print("   - FileEditorTool: Create/edit files")
    print("   - TaskTrackerTool: Track task progress")
    print()

    # Configure LLM
    llm = LLM(
        model=model,
        api_key=api_key,
        base_url=base_url,
    )

    # Create agent with recommended tool set
    agent = Agent(
        llm=llm,
        tools=[
            Tool(name=TerminalTool.name),  # Execute commands
            Tool(name=FileEditorTool.name),  # Create/edit files
            Tool(name=TaskTrackerTool.name),  # Track tasks
        ],
    )

    # Set workspace
    project_root = Path(__file__).parent.parent
    conversation = Conversation(agent=agent, workspace=str(project_root))

    print("📁 Workspace:", project_root)
    print()

    # Phase 1: FastAPI Server
    print("=" * 70)
    print("📡 Phase 1: Generating FastAPI Server")
    print("=" * 70)

    task1 = """
    Create examples/tavern_game_server.py - a FastAPI server for the Electron Tavern Game Display.
    
    Requirements (from implementation plan and security critique):
    
    1. FastAPI Application:
       - Bind to 127.0.0.1:8765 (local only, no external access)
       - Use asyncio.Lock() for game state management (prevents race conditions)
       - Add CORS middleware allowing only localhost origins
    
    2. Endpoints:
       - GET /api/state - Returns current game state JSON
       - POST /api/choice - Accepts player choice, validates with Pydantic, updates state atomically
       - GET /api/health - Health check endpoint
    
    3. Game State Structure:
       - character: Full DnD5eCharacter serialized (use to_dict() method + add computed properties)
       - current_scene: string
       - narrative: string  
       - choices: list of {id, text, type} objects
       - last_roll: dict with dice, result, modifier, total, dc, success
       - events: list of event history (limit to last 100 events)
    
    4. Security Requirements (CRITICAL):
       - Use asyncio.Lock() for all state updates (prevents race conditions)
       - Input validation with Pydantic models (reject invalid choice IDs)
       - CORS only allows localhost origins
       - Error handling with try/except blocks
       - Port availability checking before binding
    
    5. Code Patterns (follow existing codebase):
       - FastAPI patterns from src/waft/api/main.py
       - asyncio.Lock() pattern from src/waft/core/now_cycle.py
       - DnD5eCharacter serialization from src/waft/core/dnd5e/character.py
       - Add computed properties (modifiers, AC, proficiency_bonus) to serialization
    
    6. Dependencies:
       - Use FastAPI, uvicorn (already in pyproject.toml)
       - Use Pydantic for validation
       - Import from existing codebase: waft.core.dnd5e
    
    Create the file at examples/tavern_game_server.py with production-ready code.
    """

    conversation.send_message(task1)
    conversation.run()
    print("✅ Phase 1 complete: FastAPI server generated")
    print()

    # Phase 2: Electron App
    print("=" * 70)
    print("🖥️  Phase 2: Generating Electron App")
    print("=" * 70)

    task2 = """
    Create the Electron app structure in tavern_display/ directory:
    
    1. package.json:
       - electron dependency (~28.0.0)
       - scripts: start, dev (optional)
       - Proper project metadata
    
    2. main.js:
       - Create Electron BrowserWindow
       - Load src/index.html
       - Set up preload script (preload.js)
       - Configure window size (1200x800)
       - Security: webSecurity: true, nodeIntegration: false, contextIsolation: true
       - Handle window close events
    
    3. preload.js:
       - Use contextBridge to expose safe API
       - Expose window.electronAPI (no Node.js access from renderer)
       - Security best practices
    
    4. src/index.html:
       - Three-column layout:
         - Left: Character stats panel
         - Center: Narrative text area (scrollable)
         - Right: Event log sidebar (scrollable)
       - Bottom sections:
         - Dice roll display
         - Choice buttons (dynamically generated)
       - Semantic HTML with IDs for JavaScript targeting
    
    5. src/renderer.js:
       - API client functions:
         - fetchGameState() - Poll /api/state every 1-2 seconds
         - submitChoice(choiceId) - POST to /api/choice
       - UI update functions:
         - updateCharacterStats(character)
         - updateNarrative(text)
         - updateChoices(choices)
         - updateDiceRoll(roll)
         - addEventLog(event)
       - Event listeners for choice buttons
       - Polling loop for real-time updates
       - Error handling and connection management
    
    6. src/styles.css:
       - Dark theme matching existing visualizer
       - D&D color scheme: parchment (#F4E4BC), gold (#D4AF37), deep blue (#1a1a2e)
       - Responsive grid layout
       - Smooth animations for dice rolls
       - Clear typography for narrative text
       - Button styling with hover effects
    
    Follow Electron security best practices and the plan specifications.
    """

    conversation.send_message(task2)
    conversation.run()
    print("✅ Phase 2 complete: Electron app generated")
    print()

    # Phase 3: Tests
    print("=" * 70)
    print("🧪 Phase 3: Generating Tests")
    print("=" * 70)

    task3 = """
    Write comprehensive pytest tests for examples/tavern_game_server.py:
    
    1. Test GET /api/state:
       - Returns correct game state structure
       - Includes character with all computed properties
       - Includes choices, narrative, events
    
    2. Test POST /api/choice:
       - Validates choice ID exists in current choices
       - Rejects invalid choice IDs
       - Updates game state correctly
       - Returns updated state
    
    3. Test state management:
       - Test asyncio.Lock() prevents race conditions
       - Test concurrent requests don't corrupt state
       - Test state updates are atomic
    
    4. Test serialization:
       - Test DnD5eCharacter serialization includes computed properties
       - Test all fields are JSON-serializable
       - Test enum handling (ArmorType)
    
    5. Test error handling:
       - Test invalid input returns proper errors
       - Test server errors are handled gracefully
       - Test connection errors
    
    6. Test security:
       - Test CORS only allows localhost
       - Test input validation rejects malicious input
       - Test port binding to 127.0.0.1 only
    
    Use pytest, pytest-asyncio, and httpx for async testing.
    Follow existing test patterns from tests/ directory.
    Create tests/test_tavern_game_server.py
    """

    conversation.send_message(task3)
    conversation.run()
    print("✅ Phase 3 complete: Tests generated")
    print()

    # Phase 4: Documentation
    print("=" * 70)
    print("📚 Phase 4: Generating Documentation")
    print("=" * 70)

    task4 = """
    Generate comprehensive documentation:
    
    1. tavern_display/README.md:
       - Project overview
       - Installation instructions (npm install)
       - Development workflow
       - Running the app (npm start)
       - Architecture overview
       - Security considerations
    
    2. examples/TAVERN_GAME_API.md:
       - API endpoint documentation
       - Request/response formats
       - Game state structure
       - Error codes
       - Examples
    
    3. Update main README.md:
       - Add section about Electron Tavern Game Display
       - Link to documentation
       - Quick start guide
    
    Follow markdown best practices and include code examples.
    """

    conversation.send_message(task4)
    conversation.run()
    print("✅ Phase 4 complete: Documentation generated")
    print()

    print("=" * 70)
    print("🎉 All Phases Complete!")
    print("=" * 70)
    print()
    print("📝 Next Steps:")
    print("   1. Review generated code:")
    print("      - examples/tavern_game_server.py")
    print("      - tavern_display/")
    print("      - tests/test_tavern_game_server.py")
    print()
    print("   2. Run tests:")
    print("      pytest tests/test_tavern_game_server.py -v")
    print()
    print("   3. Start server:")
    print("      python examples/tavern_game_server.py")
    print()
    print("   4. Start Electron app:")
    print("      cd tavern_display && npm install && npm start")
    print()
    print("   5. Play the game!")


if __name__ == "__main__":
    main()
