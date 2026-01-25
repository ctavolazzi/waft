#!/usr/bin/env python3.12
"""Quick test that Eleventy CYOA works."""

import sys
sys.path.insert(0, '/home/user/waft/src')

try:
    import yaml
    from rich.console import Console
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Installing with --break-system-packages...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "--quiet", "pyyaml", "rich"])
    import yaml
    from rich.console import Console

from waft.core.scenario_formats import ElevntyCYOAParser

console = Console()

# Test loading
console.print("[cyan]Testing Eleventy CYOA scenario loading...[/cyan]")
scenario = ElevntyCYOAParser.load_scenario('examples/eleventy_cyoa_demo')

console.print(f"✅ Loaded scenario with {len(scenario.nodes)} nodes")
console.print(f"   Start node: {scenario.start_node_id}")
console.print(f"   Nodes: {', '.join(scenario.nodes.keys())}")

# Test validation
console.print("\n[cyan]Testing validation...[/cyan]")
is_valid, errors = ElevntyCYOAParser.validate_scenario('examples/eleventy_cyoa_demo')
if is_valid:
    console.print("✅ Validation passed")
else:
    console.print("[red]❌ Validation failed:[/red]")
    for error in errors:
        console.print(f"   {error}")

# Test node access
console.print("\n[cyan]Testing node access...[/cyan]")
start = scenario.get_start_node()
console.print(f"✅ Start node: '{start.title}'")
console.print(f"   Content preview: {start.content[:50]}...")
console.print(f"   Choices: {len(start.choices)}")

console.print("\n[bold green]🎉 Everything works![/bold green]")
console.print("\nTo run interactively:")
console.print("  python3.12 test_scenario_quick.py --interactive")

if "--interactive" in sys.argv:
    console.print("\n" + "="*60)
    scenario.run_interactive()
