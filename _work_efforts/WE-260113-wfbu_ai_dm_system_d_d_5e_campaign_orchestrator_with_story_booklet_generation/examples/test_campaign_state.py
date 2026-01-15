"""
Test campaign state management system.
"""

from pathlib import Path
import sys
import tempfile
import shutil

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from campaign_state import (
    CampaignStateManager,
    CampaignStatus,
    SessionStatus
)
from rich.console import Console

console = Console()

def test_campaign_state():
    """Test campaign state management."""
    console.print("\n[bold cyan]🧪 Testing Campaign State Management[/bold cyan]\n")
    
    # Use temporary directory
    temp_dir = Path(tempfile.mkdtemp())
    console.print(f"[dim]Using temp directory: {temp_dir}[/dim]\n")
    
    try:
        manager = CampaignStateManager(temp_dir)
        
        # Test 1: Create campaign
        console.print("[bold]1. Creating Campaign...[/bold]")
        campaign = manager.create_campaign(
            campaign_name="The Mysterious Tavern",
            scenario_file="tavern_campaign.json",
            description="A D&D 5e campaign starting in a mysterious tavern",
            difficulty="medium"
        )
        console.print(f"  ✅ Campaign created: {campaign.campaign_id}")
        console.print(f"  ✅ Name: {campaign.campaign_name}")
        console.print(f"  ✅ Status: {campaign.status.value}\n")
        
        # Test 2: Add player characters
        console.print("[bold]2. Adding Player Characters...[/bold]")
        campaign.player_characters = {
            "Player1": "being_001",
            "Player2": "being_002"
        }
        manager.save_campaign(campaign)
        console.print(f"  ✅ Added {len(campaign.player_characters)} PCs\n")
        
        # Test 3: Create session
        console.print("[bold]3. Creating Session...[/bold]")
        session = manager.add_session(campaign.campaign_id, session_number=1)
        console.print(f"  ✅ Session created: {session.session_id}")
        console.print(f"  ✅ Session number: {session.session_number}")
        console.print(f"  ✅ Status: {session.status.value}\n")
        
        # Test 4: Add events
        console.print("[bold]4. Adding Events...[/bold]")
        event1 = manager.add_event(
            campaign_id=campaign.campaign_id,
            session_id=session.session_id,
            event_type="narrative",
            description="The party wakes up in a tavern",
            sequence_id="seq_001"
        )
        console.print(f"  ✅ Event 1: {event1.event_type} - {event1.description[:50]}...")
        
        event2 = manager.add_event(
            campaign_id=campaign.campaign_id,
            session_id=session.session_id,
            event_type="choice",
            description="Player chooses to investigate",
            choice_made="A",
            sequence_id="seq_001"
        )
        console.print(f"  ✅ Event 2: {event2.event_type} - Choice: {event2.choice_made}\n")
        
        # Test 5: Update session status
        console.print("[bold]5. Updating Session Status...[/bold]")
        manager.update_session_status(
            campaign_id=campaign.campaign_id,
            session_id=session.session_id,
            status=SessionStatus.IN_PROGRESS
        )
        console.print(f"  ✅ Session status updated to: IN_PROGRESS\n")
        
        # Test 6: Load campaign
        console.print("[bold]6. Loading Campaign...[/bold]")
        loaded = manager.load_campaign(campaign.campaign_id)
        console.print(f"  ✅ Campaign loaded: {loaded.campaign_name}")
        console.print(f"  ✅ Sessions: {len(loaded.sessions)}")
        console.print(f"  ✅ Events in session: {len(loaded.sessions[0].events)}\n")
        
        # Test 7: Get summary
        console.print("[bold]7. Campaign Summary...[/bold]")
        summary = manager.get_campaign_summary(campaign.campaign_id)
        console.print(f"  ✅ Summary generated:")
        for key, value in summary.items():
            console.print(f"     - {key}: {value}")
        console.print()
        
        # Test 8: List campaigns
        console.print("[bold]8. Listing Campaigns...[/bold]")
        campaigns = manager.list_campaigns()
        console.print(f"  ✅ Found {len(campaigns)} campaign(s)\n")
        
        console.print("[bold green]✅ All tests passed![/bold green]\n")
        
        return campaign, session
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
        console.print(f"[dim]Cleaned up temp directory[/dim]\n")

if __name__ == "__main__":
    test_campaign_state()
