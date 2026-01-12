"""
Test minimal Storyteller implementation.

Verifies that Storyteller can generate basic narrative PDFs from text input.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution.storyteller import Storyteller


def test_text_input():
    """Test Storyteller with simple text input."""
    print("Testing Storyteller with text input...")
    
    text = """
    Alice started working on the project. She encountered a bug. 
    Bob helped her debug the issue. Alice and Bob worked together.
    Charlie reviewed the code. Alice fixed the bug. Bob was happy.
    The project was complete.
    """
    
    storyteller = Storyteller.from_text(
        text=text,
        narrative_style="simple",
        story_structure="linear"
    )
    
    output_path = Path("_temp/test_storyteller_text.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    pdf_path = storyteller.tell_story(
        output_path=output_path,
        title="Alice's Adventure",
        open_pdf=False
    )
    
    print(f"✅ Generated PDF: {pdf_path}")
    print(f"   File size: {pdf_path.stat().st_size / 1024:.2f} KB")
    return pdf_path


def test_structured_data():
    """Test Storyteller with structured data."""
    print("\nTesting Storyteller with structured data...")
    
    data = {
        "characters": {
            "Alice": {"name": "Alice", "role": "Developer"},
            "Bob": {"name": "Bob", "role": "Mentor"}
        },
        "settings": {
            "Office": {"name": "Office", "type": "workspace"}
        },
        "events": [
            {"character": "Alice", "action": "started work", "time": "morning", "description": "Alice began working on the project"},
            {"character": "Alice", "action": "encountered bug", "time": "afternoon", "description": "A subtle bug appeared"},
            {"character": "Bob", "action": "helped debug", "time": "afternoon", "description": "Bob provided guidance"},
            {"character": "Alice", "action": "fixed bug", "time": "evening", "description": "The bug was resolved"}
        ],
        "summary": "A developer's journey from problem to solution"
    }
    
    storyteller = Storyteller.from_data(
        data=data,
        narrative_style="simple",
        story_structure="linear"
    )
    
    output_path = Path("_temp/test_storyteller_structured.pdf")
    pdf_path = storyteller.tell_story(
        output_path=output_path,
        title="Developer's Journey",
        open_pdf=False
    )
    
    print(f"✅ Generated PDF: {pdf_path}")
    print(f"   File size: {pdf_path.stat().st_size / 1024:.2f} KB")
    return pdf_path


def test_events_input():
    """Test Storyteller with events list."""
    print("\nTesting Storyteller with events list...")
    
    events = [
        {"character": "Developer", "action": "started work", "time": "morning", "description": "The work began"},
        {"character": "Developer", "action": "encountered bug", "time": "afternoon", "description": "A challenge appeared"},
        {"character": "Developer", "action": "solved bug", "time": "evening", "description": "Success was achieved"}
    ]
    
    storyteller = Storyteller.from_events(
        events=events,
        narrative_style="simple",
        story_structure="linear"
    )
    
    output_path = Path("_temp/test_storyteller_events.pdf")
    pdf_path = storyteller.tell_story(
        output_path=output_path,
        title="Simple Story",
        open_pdf=False
    )
    
    print(f"✅ Generated PDF: {pdf_path}")
    print(f"   File size: {pdf_path.stat().st_size / 1024:.2f} KB")
    return pdf_path


def test_medium_complexity():
    """Test Storyteller with medium complexity style."""
    print("\nTesting Storyteller with medium complexity...")
    
    text = """
    Alice sat at her desk, staring at the blank screen. The project deadline loomed ahead.
    She began coding, methodically building the system. Bob noticed her struggle and offered help.
    Together they worked through the challenges. Alice learned new techniques from Bob.
    The project was completed successfully. Alice felt confident and capable.
    """
    
    storyteller = Storyteller.from_text(
        text=text,
        narrative_style="medium",
        story_structure="linear"
    )
    
    output_path = Path("_temp/test_storyteller_medium.pdf")
    pdf_path = storyteller.tell_story(
        output_path=output_path,
        title="Medium Complexity Story",
        open_pdf=False
    )
    
    print(f"✅ Generated PDF: {pdf_path}")
    print(f"   File size: {pdf_path.stat().st_size / 1024:.2f} KB")
    return pdf_path


if __name__ == "__main__":
    print("="*60)
    print("Storyteller Minimal Version Test")
    print("="*60)
    
    try:
        test_text_input()
        test_structured_data()
        test_events_input()
        test_medium_complexity()
        
        print("\n" + "="*60)
        print("✅ All tests completed successfully!")
        print("="*60)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
