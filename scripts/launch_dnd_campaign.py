#!/usr/bin/env python3
"""
Launch D&D Campaign

Launches a D&D 5e campaign in the specified mode:
- interactive: CLI-based interactive campaign
- web: Web-based game UI (FastAPI + HTML)
- scenario: AI-driven scenario generation with quest PDFs
"""

import sys
import subprocess
import argparse
import webbrowser
import time
import threading
from pathlib import Path

def launch_interactive_campaign(project_root: Path):
    """Launch interactive CLI campaign."""
    script = project_root / "examples" / "interactive_dnd_game.py"
    if not script.exists():
        print(f"❌ Error: {script} not found")
        return False
    
    print("🎲 Launching Interactive D&D Campaign...")
    print("📖 Use commands: explore, shop, rest, combat, character, save, quit\n")
    
    try:
        subprocess.run([sys.executable, str(script)], cwd=project_root)
    except KeyboardInterrupt:
        print("\n🛑 Campaign ended")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True


def launch_web_campaign(project_root: Path):
    """Launch web-based D&D game."""
    script = project_root / "examples" / "dnd_game_server.py"
    if not script.exists():
        print(f"❌ Error: {script} not found")
        return False
    
    print("🌐 Launching Web-Based D&D Game...")
    print("📊 Game will be available at: http://localhost:8003")
    print("🔄 Opening browser in 3 seconds...\n")
    
    # Open browser after delay
    def open_browser():
        time.sleep(3)
        webbrowser.open("http://localhost:8003")
    
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    try:
        # Import and run the FastAPI server
        import uvicorn
        sys.path.insert(0, str(project_root / "examples"))
        from dnd_game_server import app
        
        uvicorn.run(app, host="0.0.0.0", port=8003, log_level="info")
    except KeyboardInterrupt:
        print("\n🛑 Web game server stopped")
    except ImportError:
        # Fallback: run as script
        print("⚠️  Running as script (uvicorn not available)")
        subprocess.run([sys.executable, str(script)], cwd=project_root)
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True


def launch_scenario_campaign(project_root: Path, new_party: bool = False):
    """Launch scenario generation mode."""
    sys.path.insert(0, str(project_root / "src"))
    
    try:
        from waft.core.dnd_scenario import (
            ScenarioRealm,
            ScenarioOrchestrator,
            QuestPDFGenerator
        )
    except ImportError as e:
        print(f"❌ Error importing D&D scenario modules: {e}")
        return False
    
    print("⚔️  Launching D&D Scenario Generation...\n")
    
    try:
        # Initialize scenario system
        scenario_realm = ScenarioRealm(project_path=project_root)
        orchestrator = ScenarioOrchestrator(scenario_realm)
        quest_generator = QuestPDFGenerator(project_path=project_root)
        
        print("✅ Scenario Realm initialized")
        print("✅ Scenario Orchestrator ready")
        if quest_generator.typst_available:
            print("✅ Quest PDF Generator ready (Typst available)\n")
        else:
            print("⚠️  Quest PDF Generator: Typst not available\n")
        
        # Spawn or load party
        party = orchestrator.party_manager.spawn_party(force_new=new_party)
        print(f"✅ Party ready: {len(party)} members\n")
        
        # Run a scenario
        import random
        scenario_modes = ["encounter", "explore", "lore"]
        scenario_mode = random.choice(scenario_modes)
        
        print(f"🎲 Running {scenario_mode} scenario...\n")
        scenario_result = orchestrator.run_scenario(mode=scenario_mode)
        
        # Generate quest markdown and PDF
        quest_title = f"Quest: {scenario_mode.title()} Scenario"
        quest_markdown = f"""# {quest_title}

## Scenario Type
{scenario_mode}

## Results
{scenario_result.get('status', 'complete')}

## Party Status
HP: {scenario_result.get('party_hp', 0)}/{scenario_result.get('party_max_hp', 0)}

## Details
```json
{scenario_result}
```
"""
        
        quest_pdf = quest_generator.generate_quest_pdf(
            quest_markdown=quest_markdown,
            quest_title=quest_title,
            template="wenyuan-campaign"
        )
        
        if quest_pdf:
            print(f"✅ Quest PDF generated: {quest_pdf}\n")
        else:
            print("⚠️  Quest PDF generation skipped (Typst not available)\n")
        
        print("✅ Scenario complete!")
        
    except Exception as e:
        print(f"❌ Error running scenario: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Launch D&D Campaign")
    parser.add_argument(
        "--mode",
        choices=["interactive", "web", "scenario"],
        default="interactive",
        help="Campaign mode (default: interactive)"
    )
    parser.add_argument(
        "--new-party",
        action="store_true",
        help="Create a new party (force new party creation)"
    )
    parser.add_argument(
        "--location",
        help="Start at specific location (web mode only)"
    )
    parser.add_argument(
        "--quest",
        help="Start with specific quest active (web mode only)"
    )
    
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent
    
    print(f"🎲 D&D Campaign Launcher")
    print(f"📁 Project: {project_root}")
    print(f"🎮 Mode: {args.mode}\n")
    
    success = False
    
    if args.mode == "interactive":
        success = launch_interactive_campaign(project_root)
    elif args.mode == "web":
        success = launch_web_campaign(project_root)
    elif args.mode == "scenario":
        success = launch_scenario_campaign(project_root, new_party=args.new_party)
    
    if success:
        print("\n✅ Campaign session complete!")
    else:
        print("\n❌ Campaign launch failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
