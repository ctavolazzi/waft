#!/usr/bin/env python3
"""
Generate Electron Tavern Game with OpenHands SDK + MCP + Skills + Persistence

This ULTIMATE version uses:
- Built-in OpenHands tools
- Our MCP servers (work-efforts, docs-maintainer, simple-tools, filesystem)
- Skills system (loads AGENTS.md automatically + game-specific skills)
- Persistence (save/restore conversation state for multi-session workflows)

Usage:
    export LLM_API_KEY="your-api-key"
    export LLM_MODEL="anthropic/claude-sonnet-4-5-20250929"  # optional
    python scripts/generate_tavern_game_with_skills.py
    
    # Resume from saved state:
    python scripts/generate_tavern_game_with_skills.py --resume <conversation-id>
    
    # List saved conversations:
    python scripts/generate_tavern_game_with_skills.py --list
"""

import os
import sys
import uuid
import argparse
from pathlib import Path

try:
    from openhands.sdk import (
        LLM, Agent, AgentContext, Conversation, Tool, LLMRegistry,
        Event, LLMConvertibleEvent, ThinkingBlock, RedactedThinkingBlock
    )
    from openhands.sdk.context import Skill, KeywordTrigger
    from openhands.sdk.context.skills import load_project_skills
    from openhands.sdk.context.condenser import LLMSummarizingCondenser
    from openhands.sdk.llm.router import MultimodalRouter
    from openhands.sdk.secret import SecretSource
    from openhands.sdk.tool import register_tool
    from openhands.tools.file_editor import FileEditorTool
    from openhands.tools.task_tracker import TaskTrackerTool
    from openhands.tools.terminal import TerminalTool
    from openhands.tools.delegate import DelegateTool, DelegationVisualizer, register_agent
except ImportError as e:
    print("❌ Error: OpenHands SDK not installed")
    print(f"   {e}")
    print("\n   Install with:")
    print("   pip install openhands-sdk openhands-tools")
    sys.exit(1)

def list_conversations(persistence_dir: Path):
    """List all saved conversations."""
    if not persistence_dir.exists():
        print("No saved conversations found.")
        return
    
    conversations = [d for d in persistence_dir.iterdir() if d.is_dir()]
    if not conversations:
        print("No saved conversations found.")
        return
    
    print(f"Found {len(conversations)} saved conversation(s):\n")
    for conv_dir in sorted(conversations):
        base_state = conv_dir / "base_state.json"
        if base_state.exists():
            import json
            try:
                with open(base_state) as f:
                    state = json.load(f)
                    created = state.get("metadata", {}).get("created_at", "unknown")
                    print(f"  {conv_dir.name}")
                    print(f"    Created: {created}")
                    print(f"    Status: {state.get('execution_state', {}).get('status', 'unknown')}")
                    print()
            except Exception as e:
                print(f"  {conv_dir.name} (error reading state: {e})")
        else:
            print(f"  {conv_dir.name} (incomplete)")

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Generate Electron Tavern Game with OpenHands")
    parser.add_argument("--resume", type=str, help="Resume from conversation ID")
    parser.add_argument("--list", action="store_true", help="List saved conversations")
    parser.add_argument("--persistence-dir", type=str, default=None, help="Persistence directory (default: .conversations)")
    parser.add_argument("--condenser-max-size", type=int, default=50, help="Max events before condensing (default: 50)")
    parser.add_argument("--condenser-keep-first", type=int, default=3, help="Events to keep at start (default: 3)")
    parser.add_argument("--no-condenser", action="store_true", help="Disable context condenser")
    parser.add_argument("--use-delegation", action="store_true", help="Use sub-agent delegation for parallel execution")
    parser.add_argument("--max-sub-agents", type=int, default=3, help="Maximum concurrent sub-agents (default: 3)")
    parser.add_argument("--secrets-file", type=str, default=None, help="Path to secrets file (JSON format: {\"KEY\": \"value\"})")
    parser.add_argument("--use-routing", action="store_true", help="Use model routing (text-only → cheaper model, multimodal → expensive model)")
    parser.add_argument("--secondary-model", type=str, default=None, help="Secondary model for routing (default: auto-detect cheaper model)")
    parser.add_argument("--show-reasoning", action="store_true", help="Display model reasoning traces (thinking blocks for Anthropic, reasoning for OpenAI)")
    parser.add_argument("--reasoning-effort", type=str, default="high", choices=["none", "low", "medium", "high"], help="Reasoning effort level for OpenAI models (default: high)")
    args = parser.parse_args()
    
    # Set workspace
    project_root = Path(__file__).parent.parent
    workspace_path = str(project_root)
    
    # Set persistence directory
    if args.persistence_dir:
        persistence_dir = Path(args.persistence_dir)
    else:
        persistence_dir = project_root / ".conversations"
    
    # Handle --list
    if args.list:
        list_conversations(persistence_dir)
        return
    
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
    
    # Determine conversation ID
    if args.resume:
        conversation_id = uuid.UUID(args.resume)
        print("🔄 Resuming conversation:", conversation_id)
        print(f"   Persistence dir: {persistence_dir}")
        print()
    else:
        conversation_id = uuid.uuid4()
    print("🚀 Generating Electron Tavern Game with OpenHands SDK + MCP + Skills + Persistence")
    print(f"   Model: {model}")
    print(f"   Conversation ID: {conversation_id}")
    print(f"   Persistence dir: {persistence_dir}")
    
    # Check for observability configuration
    observability_enabled = False
    observability_backend = None
    
    if os.getenv("LMNR_PROJECT_API_KEY"):
        observability_enabled = True
        observability_backend = "Laminar"
    elif os.getenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT") or os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT") or os.getenv("OTEL_ENDPOINT"):
        observability_enabled = True
        endpoint = os.getenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT") or os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT") or os.getenv("OTEL_ENDPOINT")
        if "honeycomb" in endpoint.lower():
            observability_backend = "Honeycomb"
        elif "jaeger" in endpoint.lower() or "localhost" in endpoint.lower():
            observability_backend = "Jaeger"
        else:
            observability_backend = "OTLP"
    
    if observability_enabled:
        print(f"   📊 Observability: Enabled ({observability_backend})")
        print(f"   Session ID: {conversation_id} (use this to find traces in your dashboard)")
    else:
        print("   📊 Observability: Disabled (set LMNR_PROJECT_API_KEY or OTEL_* vars to enable)")
    print()
    
    # Create LLM Registry for centralized management
    llm_registry = LLMRegistry()
    
    # Configure LLM with optional routing and reasoning
    llm_kwargs = {
        "api_key": api_key,
        "base_url": base_url,
    }
    
    # Add reasoning effort for OpenAI models
    if "gpt" in model.lower() or "openai" in model.lower():
        llm_kwargs["reasoning_effort"] = args.reasoning_effort
        if args.show_reasoning:
            print(f"🧠 Reasoning enabled (effort: {args.reasoning_effort})")
            print("   (OpenAI reasoning traces will be displayed)")
            print()
    
    if args.use_routing:
        # Primary LLM (multimodal-capable, expensive)
        primary_llm = LLM(
            usage_id="agent-primary",
            model=model,
            **llm_kwargs,
        )
        llm_registry.add(primary_llm)
        
        # Secondary LLM (text-only, cheaper)
        # Default to a cheaper model if not specified
        secondary_model = args.secondary_model or "anthropic/claude-haiku-3-5-20241022"
        secondary_llm = LLM(
            usage_id="agent-secondary",
            model=secondary_model,
            **llm_kwargs,
        )
        llm_registry.add(secondary_llm)
        
        # Create multimodal router
        multimodal_router = MultimodalRouter(
            usage_id="multimodal-router",
            llms_for_routing={"primary": primary_llm, "secondary": secondary_llm},
        )
        llm_registry.add(multimodal_router)
        llm = multimodal_router  # Use router as LLM
        
        print("🔄 Model routing enabled:")
        print(f"   Primary (multimodal): {model}")
        print(f"   Secondary (text-only): {secondary_model}")
        print("   (Text-only requests → cheaper model, multimodal → expensive model)")
        print()
    else:
        # Single LLM (no routing)
        main_llm = LLM(
            usage_id="agent",
            model=model,
            **llm_kwargs,
        )
        llm_registry.add(main_llm)
        llm = llm_registry.get("agent")  # Get from registry
    
    # Configure context condenser (optional, but recommended for long conversations)
    condenser = None
    if not args.no_condenser:
        # Create separate LLM for condenser with its own usage_id
        condenser_llm = LLM(
            usage_id="condenser",
            model=model,
            api_key=api_key,
            base_url=base_url,
        )
        llm_registry.add(condenser_llm)
        
        condenser = LLMSummarizingCondenser(
            llm=condenser_llm,
            max_size=args.condenser_max_size,
            keep_first=args.condenser_keep_first,
        )
        print("💾 Context condenser enabled:")
        print(f"   Max size: {args.condenser_max_size} events")
        print(f"   Keep first: {args.condenser_keep_first} events")
        print("   (Older conversation history will be summarized to save tokens)")
        print()
    
    # Load project skills (automatically finds AGENTS.md, CLAUDE.md, GEMINI.md)
    print("📚 Loading project skills...")
    try:
        project_skills = load_project_skills(workspace_dir=workspace_path)
        print(f"✅ Loaded {len(project_skills)} project skills (AGENTS.md, etc.)")
    except Exception as e:
        print(f"⚠️  Could not load project skills: {e}")
        print("   Continuing without project skills...")
        project_skills = []
    
    # Create game-specific skills
    game_skills = [
        # Always-loaded skill: Game development context
        Skill(
            name="game-development-context",
            content="""
            You are developing an Electron desktop game application for a D&D 5e tavern scenario.
            
            Key Context:
            - This is a local-only game (no external services)
            - Uses FastAPI server on 127.0.0.1:8765
            - Electron app displays game state in real-time
            - Follows security best practices from critique
            - Uses existing codebase patterns (FastAPI, asyncio.Lock, DnD5eCharacter)
            
            Coding Standards (from AGENTS.md):
            - Direct & Minimal Python style
            - No unnecessary abstractions
            - Use existing patterns from codebase
            - Follow security fixes from critique
            """,
            trigger=None,  # Always loaded
        ),
        # Keyword-triggered skill: D&D 5e rules
        Skill(
            name="dnd5e-rules",
            content="""
            D&D 5e Rules Reference:
            - Ability scores: 3-18 range
            - Modifiers: (score - 10) / 2, rounded down
            - AC: 10 + DEX modifier + armor bonus
            - Proficiency bonus: +2 at level 1, +3 at level 5, etc.
            - Skill checks: d20 + ability modifier + proficiency (if proficient)
            - Use DnD5eCharacter class from waft.core.dnd5e
            - Use DnDRoller for dice rolling
            """,
            trigger=KeywordTrigger(keywords=["dnd", "d&d", "5e", "ability", "modifier", "roll", "dice"]),
        ),
        # Keyword-triggered skill: Electron security
        Skill(
            name="electron-security",
            content="""
            Electron Security Best Practices:
            - webSecurity: true (keep enabled)
            - nodeIntegration: false (no Node.js in renderer)
            - contextIsolation: true (use contextBridge)
            - Use preload.js to expose safe API via contextBridge
            - Never expose Node.js APIs to renderer
            - Validate all inputs from renderer
            """,
            trigger=KeywordTrigger(keywords=["electron", "security", "preload", "renderer", "contextBridge"]),
        ),
        # Keyword-triggered skill: FastAPI patterns
        Skill(
            name="fastapi-patterns",
            content="""
            FastAPI Patterns from this codebase:
            - Use async endpoints with asyncio.Lock() for state management
            - Follow patterns from src/waft/api/main.py
            - Use Pydantic models for validation
            - Add CORS middleware for localhost only
            - Use app.state for shared state
            - Follow error handling patterns from existing endpoints
            """,
            trigger=KeywordTrigger(keywords=["fastapi", "endpoint", "api", "server", "async"]),
        ),
    ]
    
    # Combine project skills + game skills
    all_skills = list(project_skills) + game_skills
    
    # Create agent context with skills
    agent_context = AgentContext(
        skills=all_skills,
        # Optional: Load public skills from OpenHands registry
        load_public_skills=False,  # Set to True to load community skills
        # Optional: Add system message suffix
        system_message_suffix="""
<PROJECT_CONTEXT>
Project: WAFT (Waft - Ambient, self-modifying Meta-Framework)
Repository: waft
Current Task: Electron Tavern Game Display Development
</PROJECT_CONTEXT>
        """.strip(),
    )
    
    # Configure MCP servers
    mcp_config = {
        "mcpServers": {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", workspace_path]
            },
            "work-efforts": {
                "command": "node",
                "args": ["/Users/ctavolazzi/Code/.mcp-servers/work-efforts/server.js"]
            },
            "simple-tools": {
                "command": "node",
                "args": ["/Users/ctavolazzi/Code/.mcp-servers/simple-tools/server.js"]
            },
            "docs-maintainer": {
                "command": "python",
                "args": ["/Users/ctavolazzi/Code/.mcp-servers/docs-maintainer/server.py"]
            },
        }
    }
    
    print("📋 Available Capabilities:")
    print("   Built-in Tools:")
    print("     - TerminalTool, FileEditorTool, TaskTrackerTool")
    print("   MCP Servers:")
    print("     - filesystem, work-efforts, simple-tools, docs-maintainer")
    print("   Skills:")
    print(f"     - {len(project_skills)} project skills (AGENTS.md, etc.)")
    print(f"     - {len(game_skills)} game-specific skills")
    print("     - game-development-context (always active)")
    print("     - dnd5e-rules (triggered by: dnd, d&d, 5e, ability, modifier, roll, dice)")
    print("     - electron-security (triggered by: electron, security, preload, renderer)")
    print("     - fastapi-patterns (triggered by: fastapi, endpoint, api, server, async)")
    print()
    
    # Create agent with tools + MCP + skills + condenser
    agent = Agent(
        llm=llm,
        tools=[
            Tool(name=TerminalTool.name),
            Tool(name=FileEditorTool.name),
            Tool(name=TaskTrackerTool.name),
        ],
        mcp_config=mcp_config,
        agent_context=agent_context,  # Add skills!
        condenser=condenser,  # Add condenser for token efficiency!
    )
    
    # Create conversation with persistence and optional delegation visualizer
    visualizer = None
    if args.use_delegation:
        visualizer = DelegationVisualizer(name="Game Developer")
    
    # Setup reasoning callback if enabled
    reasoning_callbacks = []
    if args.show_reasoning:
        def show_reasoning(event: Event):
            """Display model reasoning traces (thinking blocks or reasoning)."""
            if isinstance(event, LLMConvertibleEvent):
                message = event.to_llm_message()
                
                # Check for Anthropic thinking blocks
                if hasattr(message, "thinking_blocks") and message.thinking_blocks:
                    print(f"\n🧠 Thinking Blocks ({len(message.thinking_blocks)}):")
                    for i, block in enumerate(message.thinking_blocks):
                        if isinstance(block, RedactedThinkingBlock):
                            print(f"  Block {i + 1}: [REDACTED] {block.data[:100]}...")
                        elif isinstance(block, ThinkingBlock):
                            thinking_text = block.thinking[:500] if len(block.thinking) > 500 else block.thinking
                            print(f"  Block {i + 1}: {thinking_text}")
                            if len(block.thinking) > 500:
                                print(f"    ... ({len(block.thinking) - 500} more characters)")
                
                # Check for OpenAI reasoning (in message content or attributes)
                if hasattr(message, "reasoning") and message.reasoning:
                    print(f"\n🧠 Reasoning Trace:")
                    reasoning_text = str(message.reasoning)[:500] if len(str(message.reasoning)) > 500 else str(message.reasoning)
                    print(f"  {reasoning_text}")
                    if len(str(message.reasoning)) > 500:
                        print(f"  ... ({len(str(message.reasoning)) - 500} more characters)")
        
        reasoning_callbacks.append(show_reasoning)
    
    conversation = Conversation(
        agent=agent,
        workspace=workspace_path,
        persistence_dir=str(persistence_dir),
        conversation_id=conversation_id,
        visualizer=visualizer,  # Add delegation visualizer if enabled
        callbacks=reasoning_callbacks if reasoning_callbacks else None,  # Add reasoning callback if enabled
    )
    
    # Add LLM registry to conversation for centralized tracking
    conversation.llm_registry = llm_registry
    
    # Setup secrets if provided
    if args.secrets_file:
        import json
        try:
            with open(args.secrets_file) as f:
                secrets = json.load(f)
            conversation.update_secrets(secrets)
            print(f"🔐 Loaded {len(secrets)} secret(s) from {args.secrets_file}")
            print("   (Secret values will be masked in command outputs)")
            print()
        except Exception as e:
            print(f"⚠️  Warning: Could not load secrets from {args.secrets_file}: {e}")
            print("   Continuing without secrets...")
            print()
    
    # Also check for common environment variables that might be secrets
    # (User can manually add these via update_secrets if needed)
    common_secret_vars = ["GITHUB_TOKEN", "NPM_TOKEN", "API_KEY", "SECRET_KEY"]
    env_secrets = {}
    for var in common_secret_vars:
        value = os.getenv(var)
        if value:
            env_secrets[var] = value
    
    if env_secrets:
        conversation.update_secrets(env_secrets)
        print(f"🔐 Loaded {len(env_secrets)} secret(s) from environment variables")
        print("   (Secret values will be masked in command outputs)")
        print()
    
    print("📁 Workspace:", project_root)
    print()
    
    # Check if resuming
    if args.resume:
        print("✅ Conversation state restored from disk")
        print("   Continuing from saved state...")
        print()
        # Don't re-run phases if resuming - let user continue manually
        print("💡 To continue, send a message to the conversation:")
        print(f"   conversation.send_message('Continue with next phase')")
        print(f"   conversation.run()")
        print()
        print("Or use the conversation interactively in your code.")
        return
    
    # Phase 0: Create Work Effort (using MCP!)
    print("=" * 70)
    print("📋 Phase 0: Creating Work Effort (via MCP)")
    print("=" * 70)
    
    task0 = f"""
    Use the work-efforts MCP server to create a work effort for this game development project.
    
    Use work-efforts:create_work_effort with:
    - repo_path: "{workspace_path}"
    - title: "Electron Tavern Game Display Development"
    - description: "Develop Electron desktop app for D&D tavern scenario game with FastAPI server. Includes real-time game state display, character stats, dice rolls, and choice-based gameplay."
    - status: "active"
    
    This will create a work effort in _work_efforts/ following the Johnny Decimal system.
    """
    
    conversation.send_message(task0)
    conversation.run()
    print("✅ Phase 0 complete: Work effort created")
    print()
    
    # Phase 1: Generate FastAPI Server
    print("=" * 70)
    print("📡 Phase 1: Generating FastAPI Server")
    print("=" * 70)
    
    task1 = """
    Create examples/tavern_game_server.py - a FastAPI server for the Electron Tavern Game Display.
    
    The agent context includes:
    - AGENTS.md with project coding standards (direct & minimal Python style)
    - FastAPI patterns from the codebase
    - Security best practices from the critique
    - D&D 5e rules reference (available when needed)
    
    Requirements:
    
    1. FastAPI Application:
       - Bind to 127.0.0.1:8765 (local only, no external access)
       - Use asyncio.Lock() for game state management (prevents race conditions)
       - Add CORS middleware allowing only localhost origins
       - Follow FastAPI patterns from src/waft/api/main.py
    
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
    
    4. Security Requirements (CRITICAL - from critique):
       - Use asyncio.Lock() for all state updates (prevents race conditions)
       - Input validation with Pydantic models (reject invalid choice IDs)
       - CORS only allows localhost origins
       - Error handling with try/except blocks
       - Port availability checking before binding
    
    5. Code Patterns:
       - Follow direct & minimal Python style from AGENTS.md
       - Use existing patterns from src/waft/api/main.py
       - Use asyncio.Lock() pattern from src/waft/core/now_cycle.py
       - DnD5eCharacter serialization from src/waft/core/dnd5e/character.py
       - Add computed properties (modifiers, AC, proficiency_bonus) to serialization
    
    6. Dependencies:
       - Use FastAPI, uvicorn (already in pyproject.toml)
       - Use Pydantic for validation
       - Import from existing codebase: waft.core.dnd5e
    
        Create the file at examples/tavern_game_server.py with production-ready code.
        Follow the coding standards from AGENTS.md (direct & minimal style).
        """
    else:
        task1 = """
        Create examples/tavern_game_server.py - a FastAPI server for the Electron Tavern Game Display.
    
    The agent context includes Electron security best practices that will be triggered
    when you work on Electron-specific code.
    
    Requirements:
    
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
       - Follow Electron security best practices from skills
    
    3. preload.js:
       - Use contextBridge to expose safe API
       - Expose window.electronAPI (no Node.js access from renderer)
       - Security best practices (no Node.js in renderer)
    
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
    
        Follow Electron security best practices (from skills) and the plan specifications.
        """
    else:
        task2 = """
        Create the Electron app structure in tavern_display/ directory.
    
    Test Requirements:
    
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
    else:
        task3 = """
        Write comprehensive pytest tests for examples/tavern_game_server.py.
    
    # Phase 4: Generate Documentation (using docs-maintainer MCP!)
    print("=" * 70)
    print("📚 Phase 4: Generating Documentation (via MCP)")
    print("=" * 70)
    
    task4 = f"""
    Generate comprehensive documentation using the docs-maintainer MCP server:
    
    1. Use docs-maintainer:create_doc to create structured documentation:
       - repo_path: "{workspace_path}"
       - area: "20-29" (development area)
       - category: "20" (architecture)
       - title: "Electron Tavern Game Display Architecture"
       - content: Document the architecture, API endpoints, game state structure, security considerations
    
    2. Also create tavern_display/README.md manually:
       - Project overview
       - Installation instructions (npm install)
       - Development workflow
       - Running the app (npm start)
       - Architecture overview
       - Security considerations
    
    3. Create examples/TAVERN_GAME_API.md:
       - API endpoint documentation
       - Request/response formats
       - Game state structure
       - Error codes
       - Examples
    
    Use the docs-maintainer MCP tools for structured documentation, and FileEditorTool for README files.
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
    print("      - _docs/ (if created via MCP)")
    print()
    print("   2. Check work effort:")
    print("      - _work_efforts/ (created via MCP)")
    print()
    print("   3. Run tests:")
    print("      pytest tests/test_tavern_game_server.py -v")
    print()
    print("   4. Start server:")
    print("      python examples/tavern_game_server.py")
    print()
    print("   5. Start Electron app:")
    print("      cd tavern_display && npm install && npm start")
    print()
    print("   6. Play the game!")
    print()
    print("💡 The agent had access to:")
    print("   - AGENTS.md (project coding standards)")
    print("   - Game-specific skills (D&D rules, Electron security, FastAPI patterns)")
    print("   - MCP servers (work-efforts, docs-maintainer, simple-tools)")
    print("   - Built-in tools (TerminalTool, FileEditorTool, TaskTrackerTool)")
    if condenser:
        print("   - Context condenser (automatic token optimization)")
    if args.use_delegation:
        print("   - Sub-agent delegation (parallel execution with specialized agents)")
    print()
    
    # Display metrics
    print("=" * 70)
    print("📊 Metrics & Cost Tracking")
    print("=" * 70)
    print()
    
    # Get combined metrics for entire conversation
    combined_metrics = conversation.conversation_stats.get_combined_metrics()
    print(f"💰 Total Cost: ${combined_metrics.accumulated_cost:.6f}")
    
    if combined_metrics.accumulated_token_usage:
        token_usage = combined_metrics.accumulated_token_usage
        print(f"📝 Total Tokens:")
        print(f"   - Prompt tokens: {token_usage.prompt_tokens:,}")
        print(f"   - Completion tokens: {token_usage.completion_tokens:,}")
        print(f"   - Total tokens: {token_usage.prompt_tokens + token_usage.completion_tokens:,}")
        if token_usage.cache_read_tokens:
            print(f"   - Cache read tokens: {token_usage.cache_read_tokens:,}")
        if token_usage.cache_write_tokens:
            print(f"   - Cache write tokens: {token_usage.cache_write_tokens:,}")
        if token_usage.reasoning_tokens:
            print(f"   - Reasoning tokens: {token_usage.reasoning_tokens:,}")
    
    # Show breakdown by usage_id
    usage_to_metrics = conversation.conversation_stats.usage_to_metrics
    if len(usage_to_metrics) > 1:
        print()
        print("📊 Cost Breakdown by Usage ID:")
        for usage_id, metrics in sorted(usage_to_metrics.items()):
            cost = metrics.accumulated_cost
            if metrics.accumulated_token_usage:
                tokens = metrics.accumulated_token_usage
                total_tokens = tokens.prompt_tokens + tokens.completion_tokens
                print(f"   - {usage_id}: ${cost:.6f} ({total_tokens:,} tokens)")
            else:
                print(f"   - {usage_id}: ${cost:.6f}")
    
    # Show LLM Registry status
    if hasattr(conversation, 'llm_registry') and conversation.llm_registry:
        registered_llms = conversation.llm_registry.list_usage_ids()
        if registered_llms:
            print()
            print("🤖 LLM Registry:")
            print(f"   Registered LLMs: {', '.join(registered_llms)}")
            print("   (Use registry.get('usage_id') to retrieve specific LLMs)")
    
    # Show latency metrics if available
    if combined_metrics.response_latencies:
        latencies = combined_metrics.response_latencies
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            print()
            print(f"⏱️  Performance:")
            print(f"   - Average latency: {avg_latency:.2f}s")
            print(f"   - Total API calls: {len(latencies)}")
    
    print()
    print("💾 Conversation state saved to:")
    print(f"   {persistence_dir / str(conversation_id)}")
    print()
    print("🔄 To resume this conversation later:")
    print(f"   python scripts/generate_tavern_game_with_skills.py --resume {conversation_id}")
    
    if condenser:
        print()
        print("💰 Context condenser benefits:")
        print("   - Up to 2x reduction in API costs")
        print("   - Consistent response times in long sessions")
        print("   - Important information preserved via summaries")
    
    if args.use_delegation:
        print()
        print("🤝 Sub-agent delegation benefits:")
        print("   - 3x speedup with parallel execution")
        print("   - Specialized agents for better quality")
        print("   - Improved throughput")
    
    if args.show_reasoning:
        print()
        print("🧠 Reasoning traces enabled:")
        if "anthropic" in model.lower() or "claude" in model.lower():
            print("   - Anthropic Extended Thinking (thinking blocks)")
            print("   - See model's internal reasoning process")
        elif "gpt" in model.lower() or "openai" in model.lower():
            print(f"   - OpenAI Reasoning (effort: {args.reasoning_effort})")
            print("   - See model's reasoning traces")
        print("   - Useful for debugging and transparency")

if __name__ == "__main__":
    main()