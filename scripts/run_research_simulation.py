#!/usr/bin/env python3
"""
Quick launcher for Research Simulation Server

Starts the web server and opens browser automatically.
"""

import webbrowser
import time
import subprocess
import sys
from pathlib import Path

def main():
    """Start the research simulation server."""
    print("🔬 Starting Research Simulation Server...")
    print("📍 Server will be available at http://localhost:8001")
    print("🌐 Opening browser in 2 seconds...\n")
    
    # Wait a moment for server to start
    time.sleep(2)
    
    # Open browser
    webbrowser.open("http://localhost:8001")
    
    # Start server
    script_path = Path(__file__).parent / "research_simulation_server.py"
    subprocess.run([sys.executable, str(script_path)])

if __name__ == "__main__":
    main()
