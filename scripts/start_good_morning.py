#!/usr/bin/env python3
"""
Start Good Morning Dashboard

Launches the Streamlit morning briefing dashboard on port 8507
and opens it in the browser.
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path


def main():
    """Start the Good Morning dashboard."""
    project_root = Path(__file__).parent.parent
    dashboard_file = project_root / "good_morning.py"

    if not dashboard_file.exists():
        print(f"❌ Error: {dashboard_file} not found")
        sys.exit(1)

    print("🌅 Starting Good Morning dashboard...")
    print("📊 Dashboard will be available at: http://localhost:8507")
    print("🔄 Opening browser in 3 seconds...")

    # Open browser after a short delay
    def open_browser():
        time.sleep(3)
        webbrowser.open("http://localhost:8507")

    import threading

    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    # Start Streamlit
    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(dashboard_file),
                "--server.port",
                "8507",
                "--server.headless",
                "false",
                "--browser.gatherUsageStats",
                "false",
            ],
            cwd=project_root,
        )
    except KeyboardInterrupt:
        print("\n🛑 Good Morning dashboard stopped")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
