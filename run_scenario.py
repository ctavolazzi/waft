#!/usr/bin/env python3.12
"""Simple runner for Eleventy CYOA scenarios."""

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
    ], check=True)
    import yaml
    from rich.console import Console

# Import directly
sys.path.insert(0, '/home/user/waft/src/waft/core/scenario_formats')
from eleventy_cyoa import ElevntyCYOAParser

if __name__ == "__main__":
    scenario_path = sys.argv[1] if len(sys.argv) > 1 else '/home/user/waft/examples/eleventy_cyoa_demo'

    scenario = ElevntyCYOAParser.load_scenario(scenario_path)
    scenario.run_interactive()
