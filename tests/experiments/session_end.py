"""
Session End: Persist laboratory state to laboratory.jsonl

Creates a SESSION_END event with current organism state.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.waft.core.agent.state import EvolutionaryEvent, EvolutionaryEventType
from src.waft.core.science import TheObserver
from src.waft.core.science.taxonomy import LineagePoet


def create_session_end_event(project_path: Path):
    """Create SESSION_END event for laboratory persistence."""
    
    observer = TheObserver(project_path=project_path)
    
    # Get recent events to find living organisms
    events = observer.get_laboratory_log(limit=100)
    
    # Find most recent genesis events (living organisms)
    genesis_events = [
        e for e in events 
        if e.get("event_type") == "spawn" and 
        e.get("payload", {}).get("event") == "genesis"
    ]
    
    # Get unique organisms (by genome_id)
    living_organisms = {}
    for event in genesis_events:
        genome_id = event.get("genome_id")
        if genome_id and genome_id not in living_organisms:
            # Check if organism died (has death event)
            died = any(
                e.get("genome_id") == genome_id and 
                e.get("event_type") == "death"
                for e in events
            )
            if not died:
                living_organisms[genome_id] = event
    
    # Create session end event (use special hex genome_id for marker)
    # "SESSION_END" -> hex: 53455353494f4e5f454e44
    session_end_genome_id = "53455353494f4e5f454e44" + "0" * (64 - 16)  # Pad to 64 chars
    
    session_end_event = EvolutionaryEvent(
        timestamp=datetime.utcnow(),
        genome_id=session_end_genome_id,
        parent_id=None,
        generation=0,
        event_type=EvolutionaryEventType.SESSION_END,
        payload={
            "session_end": True,
            "tag": "SESSION_END",
            "living_organisms": [
                {
                    "genome_id": genome_id,
                    "scientific_name": LineagePoet.generate_name(genome_id),
                    "agent_id": event.get("agent_id"),
                    "generation": event.get("generation", 0),
                    "timestamp": event.get("timestamp")
                }
                for genome_id, event in living_organisms.items()
            ],
            "total_living": len(living_organisms)
        },
        agent_id="SESSION_END",
        lineage_path=[]
    )
    
    # Log to TheObserver
    observer.observe_event(session_end_event)
    
    return session_end_event, living_organisms


if __name__ == "__main__":
    event, organisms = create_session_end_event(project_root)
    
    print("=" * 80)
    print("SESSION END: Laboratory State Persisted")
    print("=" * 80)
    print()
    print(f"Living Organisms: {len(organisms)}")
    print()
    
    for i, (genome_id, org_event) in enumerate(organisms.items(), 1):
        scientific_name = LineagePoet.generate_name(genome_id)
        print(f"  {i}. {scientific_name}")
        print(f"     Genome: {genome_id[:16]}...")
        print(f"     Agent ID: {org_event.get('agent_id')}")
        print()
    
    print("✓ SESSION_END event logged to laboratory.jsonl")
