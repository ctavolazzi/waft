"""
AI DM System Demo

Demonstrates the AI DM system orchestrating tools to run a campaign
and generate a story booklet.
"""

import sys
import tempfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from campaign_orchestrator import CampaignOrchestrator
from campaign_state import SessionStatus
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def demo_ai_dm_system():
    """Run a complete AI DM system demo."""
    console.print("\n" + "=" * 70)
    console.print(Panel.fit("[bold cyan]🎲 AI DM System Demo[/bold cyan]", border_style="cyan"))
    console.print("=" * 70 + "\n")

    # Use temporary directory
    temp_dir = Path(tempfile.mkdtemp())
    console.print(f"[dim]Working directory: {temp_dir}[/dim]\n")

    try:
        # Initialize orchestrator
        console.print("[bold]1. Initializing Campaign Orchestrator...[/bold]")
        orchestrator = CampaignOrchestrator(temp_dir)
        console.print("  ✅ Orchestrator initialized\n")

        # Start campaign
        console.print("[bold]2. Starting Campaign...[/bold]")
        campaign = orchestrator.start_campaign(
            campaign_name="The Mysterious Tavern",
            scenario_file="tavern_campaign.json",
            description="A D&D 5e campaign where the party wakes up in a mysterious tavern",
            difficulty="medium",
        )
        console.print(f"  ✅ Campaign created: [cyan]{campaign.campaign_name}[/cyan]")
        console.print(f"  ✅ Campaign ID: [dim]{campaign.campaign_id}[/dim]\n")

        # Add player characters
        console.print("[bold]3. Adding Player Characters...[/bold]")
        campaign.player_characters = {
            "Aragorn": "being_aragorn_001",
            "Gandalf": "being_gandalf_001",
        }
        orchestrator.state_manager.save_campaign(campaign)
        console.print(f"  ✅ Added {len(campaign.player_characters)} player characters\n")

        # Run session
        console.print("[bold]4. Running Campaign Session...[/bold]")
        session = orchestrator.run_session(campaign.campaign_id, session_number=1)
        console.print(f"  ✅ Session started: [cyan]Session {session.session_number}[/cyan]")
        console.print(f"  ✅ Session ID: [dim]{session.session_id}[/dim]\n")

        # Add narrative events
        console.print("[bold]5. Campaign Events...[/bold]")

        event1 = orchestrator.state_manager.add_event(
            campaign_id=campaign.campaign_id,
            session_id=session.session_id,
            event_type="narrative",
            description="The party wakes up in a dimly lit tavern with no memory of how they got there",
            sequence_id="seq_001",
        )
        console.print(f"  📖 [dim]{event1.description[:60]}...[/dim]")

        event2 = orchestrator.state_manager.add_event(
            campaign_id=campaign.campaign_id,
            session_id=session.session_id,
            event_type="choice",
            description="Aragorn chooses to investigate the mysterious note",
            participants=["being_aragorn_001"],
            choice_made="A",
            sequence_id="seq_001",
        )
        console.print(
            f"  🎯 Choice made: [cyan]{event2.choice_made}[/cyan] - {event2.description[:50]}..."
        )

        event3 = orchestrator.state_manager.add_event(
            campaign_id=campaign.campaign_id,
            session_id=session.session_id,
            event_type="narrative",
            description="The party finds an ornate key with strange symbols",
            sequence_id="seq_002",
        )
        console.print(f"  📖 [dim]{event3.description[:60]}...[/dim]\n")

        # DM decision (simulated)
        console.print("[bold]6. DM Decision (Simulated)...[/bold]")
        decision = orchestrator.make_dm_decision(
            campaign_id=campaign.campaign_id,
            problem="What encounter should happen next?",
            alternatives=["Combat", "Social", "Exploration"],
            criteria={"pacing": 0.5, "story": 0.5},
            scores={
                "Combat": {"pacing": 7, "story": 6},
                "Social": {"pacing": 6, "story": 9},
                "Exploration": {"pacing": 8, "story": 7},
            },
        )
        console.print("  ✅ DM decision made (simulated)")
        console.print("  📊 Recommendation: [cyan]Social encounter[/cyan]\n")

        # Complete session
        console.print("[bold]7. Completing Session...[/bold]")
        orchestrator.state_manager.update_session_status(
            campaign_id=campaign.campaign_id,
            session_id=session.session_id,
            status=SessionStatus.COMPLETED,
        )
        console.print("  ✅ Session completed\n")

        # Generate campaign summary
        console.print("[bold]8. Campaign Summary...[/bold]")
        summary = orchestrator.state_manager.get_campaign_summary(campaign.campaign_id)

        table = Table(title="Campaign Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        for key, value in summary.items():
            table.add_row(key.replace("_", " ").title(), str(value))

        console.print(table)
        console.print()

        # Generate story booklet
        console.print("[bold]9. Generating Story Booklet...[/bold]")
        booklet_path = orchestrator.generate_story_booklet(
            campaign_id=campaign.campaign_id, output_path=temp_dir / "campaign_booklet.pdf"
        )

        size_kb = booklet_path.stat().st_size / 1024
        console.print(f"  ✅ Booklet generated: [green]{booklet_path.name}[/green]")
        console.print(f"  📄 Size: [dim]{size_kb:.1f} KB[/dim]\n")

        # Final summary
        console.print(
            Panel.fit(
                "[bold green]✅ Demo Complete![/bold green]\n\n"
                f"Campaign: {campaign.campaign_name}\n"
                f"Sessions: {summary['session_count']}\n"
                f"Events: {summary['total_events']}\n"
                f"Booklet: {booklet_path.name}",
                border_style="green",
            )
        )

        return campaign, booklet_path

    finally:
        # Don't cleanup - keep files for inspection
        console.print(f"\n[dim]Files saved in: {temp_dir}[/dim]")
        console.print("[dim]Remove manually when done inspecting[/dim]\n")


if __name__ == "__main__":
    demo_ai_dm_system()
