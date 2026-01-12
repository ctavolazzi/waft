#!/usr/bin/env python3
"""
Work Effort Status Tracker

Quick status check for WE-260111-dr0f work effort.

Usage:
    python tools/status.py
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

work_effort_path = Path(__file__).parent.parent
tickets_dir = work_effort_path / "tickets"


def get_ticket_status():
    """Get status of all tickets."""
    tickets = {}
    
    if not tickets_dir.exists():
        return tickets
    
    for ticket_file in tickets_dir.glob("*.md"):
        content = ticket_file.read_text()
        
        # Extract ticket ID and status
        ticket_id = ticket_file.stem
        status = "pending"
        
        if "status: completed" in content.lower():
            status = "completed"
        elif "status: in_progress" in content.lower():
            status = "in_progress"
        
        tickets[ticket_id] = {
            "file": ticket_file,
            "status": status
        }
    
    return tickets


def print_status():
    """Print work effort status."""
    tickets = get_ticket_status()
    
    print("=" * 60)
    print("WE-260111-dr0f: Evolutionary Iteration Process")
    print("=" * 60)
    print()
    
    print("Ticket Status:")
    print("-" * 60)
    
    completed = 0
    in_progress = 0
    pending = 0
    
    for ticket_id, info in sorted(tickets.items()):
        status = info["status"]
        status_icon = {
            "completed": "✅",
            "in_progress": "🔄",
            "pending": "⏳"
        }.get(status, "❓")
        
        print(f"{status_icon} {ticket_id}: {status}")
        
        if status == "completed":
            completed += 1
        elif status == "in_progress":
            in_progress += 1
        else:
            pending += 1
    
    print()
    print("Summary:")
    print(f"  ✅ Completed: {completed}/{len(tickets)}")
    print(f"  🔄 In Progress: {in_progress}/{len(tickets)}")
    print(f"  ⏳ Pending: {pending}/{len(tickets)}")
    print()
    
    # Next steps
    print("Next Steps:")
    print("-" * 60)
    
    if pending > 0:
        next_ticket = None
        for ticket_id, info in sorted(tickets.items()):
            if info["status"] == "pending":
                next_ticket = ticket_id
                break
        
        if next_ticket:
            print(f"  🎯 Next: {next_ticket}")
            print(f"     Recommended: TKT-dr0f-003 (Comparison Tools)")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    print_status()
