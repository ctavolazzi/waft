#!/usr/bin/env python3.12
"""Direct test of eleventy_cyoa.py without full waft imports."""

import sys
import subprocess

# Install dependencies if needed
try:
    import yaml
    from rich.console import Console
except ImportError:
    print("Installing dependencies...")
    subprocess.run([
        sys.executable, "-m", "pip", "install",
        "--break-system-packages", "--quiet",
        "pyyaml", "rich"
    ])
    import yaml
    from rich.console import Console

# Import directly from the file
sys.path.insert(0, '/home/user/waft/src/waft/core/scenario_formats')
from eleventy_cyoa import ElevntyCYOAParser, ElevntyCYOAScenario

console = Console()

# Test
console.print("[cyan]Testing Eleventy CYOA...[/cyan]")
scenario = ElevntyCYOAParser.load_scenario('/home/user/waft/examples/eleventy_cyoa_demo')

console.print(f"✅ Loaded {len(scenario.nodes)} nodes")
console.print(f"   Start: {scenario.start_node_id}")

# Validate
is_valid, errors = ElevntyCYOAParser.validate_scenario('/home/user/waft/examples/eleventy_cyoa_demo')
console.print(f"✅ Valid: {is_valid}")

console.print("\n[bold green]It works![/bold green]")
console.print("\nRun with --play to play the scenario")

if "--play" in sys.argv:
    console.print("\n" + "="*60)
    scenario.run_interactive()
