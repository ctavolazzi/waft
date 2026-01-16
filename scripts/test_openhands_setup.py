#!/usr/bin/env python3
"""
Test OpenHands SDK Setup

Simple verification script to ensure OpenHands is properly configured
before running full code generation.

Usage:
    export LLM_API_KEY="your-api-key"
    export LLM_MODEL="anthropic/claude-sonnet-4-5-20250929"  # optional
    python scripts/test_openhands_setup.py
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
        print("\n   Or for OpenHands Cloud:")
        print('   export LLM_API_KEY="your-openhands-api-key"')
        print('   export LLM_MODEL="openhands/claude-sonnet-4-5-20250929"')
        sys.exit(1)
    
    # Get model (default to Anthropic)
    model = os.getenv("LLM_MODEL", "anthropic/claude-sonnet-4-5-20250929")
    base_url = os.getenv("LLM_BASE_URL", None)
    
    print("🔧 Testing OpenHands SDK Setup")
    print(f"   Model: {model}")
    print(f"   API Key: {'*' * 10}{api_key[-4:] if len(api_key) > 4 else '****'}")
    print()
    
    try:
        # Configure LLM
        print("📡 Configuring LLM...")
        llm = LLM(
            model=model,
            api_key=api_key,
            base_url=base_url,
        )
        print("✅ LLM configured")
        
        # Create agent with built-in tools
        # Available OpenHands tools:
        # - TerminalTool: Execute bash/terminal commands
        # - FileEditorTool: Create, read, edit, delete files
        # - TaskTrackerTool: Track and manage task progress
        # - BashTool: Alternative to TerminalTool
        # - get_default_tools(): Get all default tools
        #
        # For complete list: https://github.com/OpenHands/software-agent-sdk/tree/main/openhands-tools/openhands/tools
        print("🤖 Creating agent...")
        agent = Agent(
            llm=llm,
            tools=[
                Tool(name=TerminalTool.name),      # Execute bash commands
                Tool(name=FileEditorTool.name),    # Edit/create files
                Tool(name=TaskTrackerTool.name),   # Track task progress
            ],
        )
        print("✅ Agent created with built-in tools")
        
        # Set workspace to project root
        project_root = Path(__file__).parent.parent
        print(f"📁 Workspace: {project_root}")
        
        # Create conversation
        print("💬 Starting conversation...")
        conversation = Conversation(agent=agent, workspace=str(project_root))
        
        # Simple test task
        test_task = """
        Write a brief test file called OPENHANDS_TEST.txt with:
        1. Confirmation that OpenHands SDK is working
        2. Current project name (waft)
        3. A note that the setup is ready for game generation
        
        Keep it brief - just 3-4 lines.
        """
        
        print("📝 Sending test task to agent...")
        conversation.send_message(test_task)
        
        print("🚀 Running agent...")
        conversation.run()
        
        # Check if file was created
        test_file = project_root / "OPENHANDS_TEST.txt"
        if test_file.exists():
            print("✅ Test file created successfully!")
            print(f"\n📄 Content of {test_file.name}:")
            print("-" * 50)
            print(test_file.read_text())
            print("-" * 50)
            print("\n🎉 OpenHands SDK is working correctly!")
            print("\n✅ Setup verified - ready to generate game code")
            print("\n   Next steps:")
            print("   1. Review the test file above")
            print("   2. Run: python scripts/generate_tavern_game.py")
            print("   3. Or run individual phase scripts")
            
            # Clean up test file (optional)
            cleanup = input("\n🗑️  Delete test file? (y/n): ").strip().lower()
            if cleanup == 'y':
                test_file.unlink()
                print("✅ Test file deleted")
        else:
            print("⚠️  Warning: Test file not created")
            print("   Agent may have completed task differently")
            print("   Check agent output above")
            
    except Exception as e:
        print(f"\n❌ Error during setup test: {e}")
        print("\n   Troubleshooting:")
        print("   1. Check API key is correct")
        print("   2. Check model name matches your provider")
        print("   3. Check network connection")
        print("   4. Verify OpenHands SDK is installed: pip install openhands-sdk openhands-tools")
        sys.exit(1)

if __name__ == "__main__":
    main()