"""
Test the universal booklet generator with various data types.
"""

from pathlib import Path
import sys
import json

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from booklet_generator import generate_booklet, BookletGenerator, BookletConfig
from rich.console import Console

console = Console()

def test_json_file():
    """Test with JSON file."""
    console.print("\n[bold cyan]Test 1: JSON File[/bold cyan]")
    
    # Create sample JSON
    sample_data = {
        "name": "Test API",
        "version": "1.0.0",
        "endpoints": [
            {"path": "/users", "method": "GET"},
            {"path": "/users/{id}", "method": "GET"},
            {"path": "/users", "method": "POST"}
        ],
        "authentication": {
            "type": "Bearer Token",
            "header": "Authorization"
        }
    }
    
    json_file = Path(__file__).parent / "sample_api.json"
    with open(json_file, 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    output = generate_booklet(
        data=str(json_file),
        title="Sample API Documentation",
        output_path=Path(__file__).parent / "test_json_file_booklet.pdf"
    )
    
    console.print(f"[green]✅ Generated:[/green] {output}")
    return output

def test_python_object():
    """Test with Python object."""
    console.print("\n[bold cyan]Test 2: Python Object[/bold cyan]")
    
    class SampleConfig:
        def __init__(self):
            self.database_url = "postgresql://localhost/db"
            self.api_key = "secret_key"
            self.features = ["feature1", "feature2", "feature3"]
            self.settings = {
                "timeout": 30,
                "retries": 3,
                "cache": True
            }
    
    config = SampleConfig()
    
    output = generate_booklet(
        data=config,
        title="Configuration Documentation",
        output_path=Path(__file__).parent / "test_python_object_booklet.pdf"
    )
    
    console.print(f"[green]✅ Generated:[/green] {output}")
    return output

def test_dict_data():
    """Test with dictionary."""
    console.print("\n[bold cyan]Test 3: Dictionary Data[/bold cyan]")
    
    campaign_data = {
        "campaign_name": "The Mysterious Tavern",
        "sessions": [
            {"session": 1, "date": "2026-01-13", "events": 5},
            {"session": 2, "date": "2026-01-14", "events": 8}
        ],
        "characters": {
            "pc1": {"name": "Aragorn", "level": 5, "class": "Ranger"},
            "pc2": {"name": "Gandalf", "level": 10, "class": "Wizard"}
        },
        "statistics": {
            "total_sessions": 2,
            "total_events": 13,
            "average_events_per_session": 6.5
        }
    }
    
    output = generate_booklet(
        data=campaign_data,
        title="Campaign Data Documentation",
        output_path=Path(__file__).parent / "test_dict_booklet.pdf"
    )
    
    console.print(f"[green]✅ Generated:[/green] {output}")
    return output

def main():
    """Run all tests."""
    console.print("\n[bold]🧪 Testing Universal Booklet Generator[/bold]\n")
    
    outputs = []
    
    try:
        outputs.append(test_json_file())
    except Exception as e:
        console.print(f"[red]❌ JSON file test failed:[/red] {e}")
    
    try:
        outputs.append(test_python_object())
    except Exception as e:
        console.print(f"[red]❌ Python object test failed:[/red] {e}")
    
    try:
        outputs.append(test_dict_data())
    except Exception as e:
        console.print(f"[red]❌ Dictionary test failed:[/red] {e}")
    
    console.print(f"\n[bold green]✅ Generated {len(outputs)} booklets![/bold green]\n")
    
    for output in outputs:
        if output and output.exists():
            size_kb = output.stat().st_size / 1024
            console.print(f"  - {output.name}: {size_kb:.1f} KB")

if __name__ == "__main__":
    main()
