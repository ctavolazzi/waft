#!/usr/bin/env python3
"""
Generate FastAPI Game Server using OpenHands SDK

Based on the Hello World pattern, this script uses OpenHands to generate
the FastAPI server code following the implementation plan and security fixes.

Usage:
    export LLM_API_KEY="your-api-key"
    export LLM_MODEL="anthropic/claude-sonnet-4-5-20250929"  # optional
    python scripts/generate_tavern_server_openhands.py
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
    
    # Get model (default to Anthropic)
    model = os.getenv("LLM_MODEL", "anthropic/claude-sonnet-4-5-20250929")
    base_url = os.getenv("LLM_BASE_URL", None)
    
    print("🚀 Generating FastAPI Game Server with OpenHands SDK")
    print(f"   Model: {model}")
    print()
    
    # Configure LLM
    llm = LLM(
        model=model,
        api_key=api_key,
        base_url=base_url,
    )
    
    # Create agent with tools
    # Using built-in tools: TerminalTool, FileEditorTool, TaskTrackerTool
    # These are sufficient for code generation - custom tools not needed
    # 
    # Available OpenHands tools:
    # - TerminalTool: Execute bash/terminal commands
    # - FileEditorTool: Create, read, edit, delete files
    # - TaskTrackerTool: Track and manage task progress
    # - BashTool: Alternative to TerminalTool
    # - get_default_tools(): Get all default tools (may include more)
    #
    # For complete list, see: https://github.com/OpenHands/software-agent-sdk/tree/main/openhands-tools/openhands/tools
    agent = Agent(
        llm=llm,
        tools=[
            Tool(name=TerminalTool.name),      # Execute bash commands (npm, python, etc.)
            Tool(name=FileEditorTool.name),    # Edit/create files (Python, JS, HTML, CSS, etc.)
            Tool(name=TaskTrackerTool.name),   # Track task progress (multi-step tasks)
        ],
    )
    
    # Set workspace to project root
    project_root = Path(__file__).parent.parent
    conversation = Conversation(agent=agent, workspace=str(project_root))
    
    # Read plan and critique for context
    plan_path = project_root / ".cursor" / "plans" / "electron_tavern_game_display_2508cb95.plan.md"
    critique_path = project_root / "_work_efforts" / "CRITIQUE_2026-01-14_202222_electron_tavern_game_display.md"
    
    # Build task description
    task = f"""
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
       - choices: list of {{id, text, type}} objects
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
    
    The server should be production-ready with:
    - Proper error handling
    - Logging
    - Security best practices
    - Clean code structure
    - Type hints
    - Docstrings
    
    Create the file at examples/tavern_game_server.py
    """
    
    print("📝 Sending generation task to agent...")
    conversation.send_message(task)
    
    print("🚀 Running agent to generate code...")
    print("   (This may take a few minutes)")
    print()
    
    conversation.run()
    
    # Check if file was created
    server_file = project_root / "examples" / "tavern_game_server.py"
    if server_file.exists():
        print()
        print("✅ FastAPI server generated successfully!")
        print(f"   Location: {server_file}")
        print()
        print("📝 Next steps:")
        print("   1. Review the generated code")
        print("   2. Test with: python examples/tavern_game_server.py")
        print("   3. Run tests (after generating them)")
    else:
        print()
        print("⚠️  Warning: Server file not found at expected location")
        print("   Check agent output above for details")

if __name__ == "__main__":
    main()