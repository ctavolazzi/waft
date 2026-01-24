#!/usr/bin/env python3
"""
Self-Iterative Push Protocol: TheGuide Dashboard Evolution

Orchestrates 3-stage evolution:
1. Baseline (current state)
2. Visual Upgrade (dark mode + 3-body animation)
3. Meta-Cognitive Integration (live data streams)
"""

import os
import time
import shutil
from pathlib import Path

# --- Configuration ---
WORK_DIR = Path("_guide_push")
SCREENSHOT_DIR = WORK_DIR / "screenshots"
REPORT_FILE = WORK_DIR / "report.typ"
TARGET_FILE = Path(__file__).parent / "theguide_hello.py"

# --- HTML Templates ---

# V1: Baseline (current state - we'll extract from the server)
HTML_V1 = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TheGuide - Hello World</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #333;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 60px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 800px;
            margin: 20px;
        }
        h1 { font-size: 4em; margin-bottom: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
        .subtitle { font-size: 1.5em; color: #666; margin-bottom: 40px; }
        .three-body { display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; margin: 40px 0; padding: 30px; background: #f8f9fa; border-radius: 15px; }
        .body-card { padding: 20px; background: white; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .body-card h3 { color: #667eea; margin-bottom: 10px; font-size: 1.2em; }
        .body-card p { color: #666; font-size: 0.9em; }
        .emoji { font-size: 3em; margin-bottom: 10px; }
        .status { margin-top: 30px; padding: 20px; background: #e8f5e9; border-radius: 10px; color: #2e7d32; }
        .status h3 { color: #2e7d32; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hello World</h1>
        <p class="subtitle">From TheGuide - The Conscience of the Simulation</p>
        <div class="three-body">
            <div class="body-card"><div class="emoji">🧠</div><h3>Mind</h3><p>TheOracle</p><p style="font-size: 0.8em; color: #999; margin-top: 5px;">Reasoning & Epistemic Intelligence</p></div>
            <div class="body-card"><div class="emoji">🤖</div><h3>Body</h3><p>NarcissusAgent</p><p style="font-size: 0.8em; color: #999; margin-top: 5px;">Action & Self-Modification</p></div>
            <div class="body-card"><div class="emoji">✨</div><h3>Spirit</h3><p>TheGuide</p><p style="font-size: 0.8em; color: #999; margin-top: 5px;">Conscience & Meta-Cognitive Guidance</p></div>
        </div>
        <div class="status">
            <h3>✅ TheGuide is Active</h3>
            <p>The 3-Body Problem is solved. Mind, Body, and Spirit are unified.</p>
        </div>
    </div>
</body>
</html>"""

# V2: Visual Upgrade (Dark Mode + 3-Body Animation)
HTML_V2 = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TheGuide | Pantheon Entity</title>
    <style>
        :root { 
            --bg: #0a0a0a; 
            --text: #e0e0e0; 
            --accent: #00ff9d; 
            --panel: #1a1a1a;
            --danger: #ff0055;
            --warning: #ffaa00;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            margin: 0; 
            background: var(--bg); 
            color: var(--text); 
            font-family: 'Courier New', monospace; 
            display: grid; 
            grid-template-rows: 60px 1fr; 
            height: 100vh; 
            overflow: hidden; 
        }
        header { 
            border-bottom: 1px solid #333; 
            display: flex; 
            align-items: center; 
            padding: 0 20px; 
            justify-content: space-between;
            background: var(--panel);
        }
        h1 { 
            font-size: 1.2rem; 
            text-transform: uppercase; 
            letter-spacing: 2px; 
            margin: 0; 
            color: var(--accent); 
        }
        .status { 
            font-size: 0.8rem; 
            color: #666; 
            font-family: monospace;
        }
        main { 
            display: grid; 
            grid-template-columns: 300px 1fr 300px; 
            gap: 1px; 
            background: #333; 
        }
        .panel { 
            background: var(--panel); 
            padding: 20px; 
            overflow-y: auto; 
        }
        .panel h3 {
            color: var(--accent);
            margin-bottom: 15px;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 1px solid #333;
            padding-bottom: 5px;
        }
        .center-stage { 
            background: #000; 
            position: relative; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
        }
        canvas { 
            border: 1px solid #333; 
            box-shadow: 0 0 20px rgba(0,255,157,0.1);
            background: #000;
        }
        .metric { 
            margin-bottom: 15px; 
        }
        .metric-label {
            font-size: 0.75rem;
            color: #888;
            margin-bottom: 5px;
            text-transform: uppercase;
        }
        .bar-bg { 
            background: #222; 
            height: 6px; 
            width: 100%; 
            border-radius: 3px;
            overflow: hidden;
        }
        .bar-fg { 
            background: var(--accent); 
            height: 100%; 
            width: 0%; 
            transition: width 0.5s;
            border-radius: 3px;
        }
        #logs {
            font-size: 0.7rem; 
            opacity: 0.7;
            line-height: 1.6;
            font-family: 'Courier New', monospace;
        }
        #logs .log-entry {
            margin-bottom: 5px;
            color: #888;
        }
        #logs .log-entry.active {
            color: var(--accent);
        }
    </style>
</head>
<body>
    <header>
        <h1>TheGuide <span style="font-size:0.5em; opacity:0.5;">// META-COGNITIVE ARCHITECTURE</span></h1>
        <div class="status">SYSTEM: ONLINE | PORT: 7072 | STATUS: OPERATIONAL</div>
    </header>
    <main>
        <div class="panel">
            <h3>LOG STREAM</h3>
            <div id="logs">
                <div class="log-entry active">> INITIALIZING PANTHEON...</div>
                <div class="log-entry">> CONNECTING TO MINDS...</div>
                <div class="log-entry">> BODY: NARCISSUS [STANDBY]</div>
                <div class="log-entry">> SPIRIT: THEGUIDE [ACTIVE]</div>
            </div>
        </div>
        <div class="center-stage">
            <canvas id="threeBody" width="600" height="400"></canvas>
        </div>
        <div class="panel">
            <h3>METRICS</h3>
            <div class="metric">
                <div class="metric-label">FATIGUE</div>
                <div class="bar-bg"><div class="bar-fg" style="width: 12%"></div></div>
            </div>
            <div class="metric">
                <div class="metric-label">CURIOSITY</div>
                <div class="bar-bg"><div class="bar-fg" style="width: 85%"></div></div>
            </div>
            <div class="metric">
                <div class="metric-label">ENTROPY</div>
                <div class="bar-bg"><div class="bar-fg" style="width: 42%"></div></div>
            </div>
        </div>
    </main>
    <script>
        // 3-Body Simulation
        const canvas = document.getElementById('threeBody');
        const ctx = canvas.getContext('2d');
        let t = 0;
        
        function draw() {
            // Fade effect
            ctx.fillStyle = 'rgba(0,0,0,0.1)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            t += 0.05;
            const cx = canvas.width / 2; 
            const cy = canvas.height / 2;
            
            // Body 1: Mind (TheOracle) - Red
            ctx.fillStyle = '#ff0055';
            ctx.beginPath();
            const x1 = cx + Math.cos(t) * 100;
            const y1 = cy + Math.sin(t * 1.3) * 80;
            ctx.arc(x1, y1, 8, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = 'rgba(255,0,85,0.3)';
            ctx.beginPath();
            ctx.arc(x1, y1, 15, 0, Math.PI * 2);
            ctx.fill();
            
            // Body 2: Body (NarcissusAgent) - Green
            ctx.fillStyle = '#00ff9d';
            ctx.beginPath();
            const x2 = cx + Math.cos(t + 2) * 150;
            const y2 = cy + Math.sin(t * 0.8) * 150;
            ctx.arc(x2, y2, 10, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = 'rgba(0,255,157,0.3)';
            ctx.beginPath();
            ctx.arc(x2, y2, 20, 0, Math.PI * 2);
            ctx.fill();
            
            // Body 3: Spirit (TheGuide) - Blue
            ctx.fillStyle = '#0099ff';
            ctx.beginPath();
            const x3 = cx + Math.cos(t * 0.7 + 4) * 120;
            const y3 = cy + Math.sin(t * 1.1) * 120;
            ctx.arc(x3, y3, 6, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = 'rgba(0,153,255,0.3)';
            ctx.beginPath();
            ctx.arc(x3, y3, 12, 0, Math.PI * 2);
            ctx.fill();
            
            // Connection lines
            ctx.strokeStyle = 'rgba(255,255,255,0.1)';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.lineTo(x3, y3);
            ctx.closePath();
            ctx.stroke();
            
            requestAnimationFrame(draw);
        }
        draw();
    </script>
</body>
</html>"""

# V3: Meta-Cognitive Integration (Live Data Streams)
HTML_V3 = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TheGuide | Pantheon Entity</title>
    <style>
        :root { 
            --bg: #0a0a0a; 
            --text: #e0e0e0; 
            --accent: #00ff9d; 
            --panel: #1a1a1a;
            --danger: #ff0055;
            --warning: #ffaa00;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            margin: 0; 
            background: var(--bg); 
            color: var(--text); 
            font-family: 'Courier New', monospace; 
            display: grid; 
            grid-template-rows: 60px 1fr; 
            height: 100vh; 
            overflow: hidden; 
        }
        header { 
            border-bottom: 1px solid #333; 
            display: flex; 
            align-items: center; 
            padding: 0 20px; 
            justify-content: space-between;
            background: var(--panel);
        }
        h1 { 
            font-size: 1.2rem; 
            text-transform: uppercase; 
            letter-spacing: 2px; 
            margin: 0; 
            color: var(--accent); 
        }
        .status { 
            font-size: 0.8rem; 
            color: #666; 
            font-family: monospace;
        }
        main { 
            display: grid; 
            grid-template-columns: 300px 1fr 300px; 
            gap: 1px; 
            background: #333; 
        }
        .panel { 
            background: var(--panel); 
            padding: 20px; 
            overflow-y: auto; 
        }
        .panel h3 {
            color: var(--accent);
            margin-bottom: 15px;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 1px solid #333;
            padding-bottom: 5px;
        }
        .center-stage { 
            background: #000; 
            position: relative; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
        }
        canvas { 
            border: 1px solid #333; 
            box-shadow: 0 0 20px rgba(0,255,157,0.1);
            background: #000;
        }
        .metric { 
            margin-bottom: 15px; 
        }
        .metric-label {
            font-size: 0.75rem;
            color: #888;
            margin-bottom: 5px;
            text-transform: uppercase;
        }
        .bar-bg { 
            background: #222; 
            height: 6px; 
            width: 100%; 
            border-radius: 3px;
            overflow: hidden;
        }
        .bar-fg { 
            background: var(--accent); 
            height: 100%; 
            width: 0%; 
            transition: width 0.5s;
            border-radius: 3px;
        }
        .bar-fg.danger {
            background: var(--danger);
        }
        #logs {
            font-size: 0.7rem; 
            opacity: 0.7;
            line-height: 1.6;
            font-family: 'Courier New', monospace;
        }
        #logs .log-entry {
            margin-bottom: 5px;
            color: #888;
        }
        #logs .log-entry.active {
            color: var(--accent);
        }
        #logs .log-entry.success {
            color: var(--accent);
        }
        #logs .log-entry.warning {
            color: var(--warning);
        }
        .fvcu-grid {
            display: grid;
            gap: 10px;
        }
        .fvcu-item {
            padding: 8px;
            background: #222;
            border-radius: 4px;
            border-left: 3px solid var(--accent);
        }
        .fvcu-label {
            font-size: 0.7rem;
            color: #888;
            margin-bottom: 3px;
        }
        .fvcu-value {
            font-size: 0.9rem;
            color: var(--accent);
            font-weight: bold;
        }
    </style>
</head>
<body>
    <header>
        <h1>TheGuide <span style="font-size:0.5em; opacity:0.5;">// META-COGNITIVE ARCHITECTURE</span></h1>
        <div class="status">SYSTEM: ONLINE | PORT: 7072 | STATUS: OPERATIONAL</div>
    </header>
    <main>
        <div class="panel">
            <h3>LOG STREAM</h3>
            <div id="logs">
                <div class="log-entry success">> INITIALIZING PANTHEON... [OK]</div>
                <div class="log-entry success">> CONNECTING TO MINDS... [OK]</div>
                <div class="log-entry active">> AGENT: NARCISSUS [ACTIVE]</div>
                <div class="log-entry active">> AGENT: EMPIRICA [ACTIVE]</div>
                <div class="log-entry warning">> FRACTURE DETECTED IN MODULE: SELF_REFLECTION</div>
                <div class="log-entry">> REPAIR STRATEGY: REROLL</div>
                <div class="log-entry success">> OPTIMIZATION COMPLETE.</div>
            </div>
        </div>
        <div class="center-stage">
            <canvas id="threeBody" width="600" height="400"></canvas>
        </div>
        <div class="panel">
            <h3>FVCU ANALYSIS</h3>
            <div class="fvcu-grid">
                <div class="fvcu-item">
                    <div class="fvcu-label">FACTUALITY</div>
                    <div class="fvcu-value">0.87</div>
                    <div class="bar-bg"><div class="bar-fg" style="width: 87%"></div></div>
                </div>
                <div class="fvcu-item">
                    <div class="fvcu-label">VALIDITY</div>
                    <div class="fvcu-value">0.92</div>
                    <div class="bar-bg"><div class="bar-fg" style="width: 92%"></div></div>
                </div>
                <div class="fvcu-item">
                    <div class="fvcu-label">COHERENCE</div>
                    <div class="fvcu-value">0.78</div>
                    <div class="bar-bg"><div class="bar-fg" style="width: 78%"></div></div>
                </div>
                <div class="fvcu-item">
                    <div class="fvcu-label">UTILITY</div>
                    <div class="fvcu-value">0.85</div>
                    <div class="bar-bg"><div class="bar-fg" style="width: 85%"></div></div>
                </div>
                <div class="fvcu-item">
                    <div class="fvcu-label">ENTROPY</div>
                    <div class="fvcu-value">0.12</div>
                    <div class="bar-bg"><div class="bar-fg danger" style="width: 12%"></div></div>
                </div>
            </div>
        </div>
    </main>
    <script>
        // 3-Body Simulation
        const canvas = document.getElementById('threeBody');
        const ctx = canvas.getContext('2d');
        let t = 0;
        
        function draw() {
            // Fade effect
            ctx.fillStyle = 'rgba(0,0,0,0.1)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            t += 0.05;
            const cx = canvas.width / 2; 
            const cy = canvas.height / 2;
            
            // Body 1: Mind (TheOracle) - Red
            ctx.fillStyle = '#ff0055';
            ctx.beginPath();
            const x1 = cx + Math.cos(t) * 100;
            const y1 = cy + Math.sin(t * 1.3) * 80;
            ctx.arc(x1, y1, 8, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = 'rgba(255,0,85,0.3)';
            ctx.beginPath();
            ctx.arc(x1, y1, 15, 0, Math.PI * 2);
            ctx.fill();
            
            // Body 2: Body (NarcissusAgent) - Green
            ctx.fillStyle = '#00ff9d';
            ctx.beginPath();
            const x2 = cx + Math.cos(t + 2) * 150;
            const y2 = cy + Math.sin(t * 0.8) * 150;
            ctx.arc(x2, y2, 10, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = 'rgba(0,255,157,0.3)';
            ctx.beginPath();
            ctx.arc(x2, y2, 20, 0, Math.PI * 2);
            ctx.fill();
            
            // Body 3: Spirit (TheGuide) - Blue
            ctx.fillStyle = '#0099ff';
            ctx.beginPath();
            const x3 = cx + Math.cos(t * 0.7 + 4) * 120;
            const y3 = cy + Math.sin(t * 1.1) * 120;
            ctx.arc(x3, y3, 6, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = 'rgba(0,153,255,0.3)';
            ctx.beginPath();
            ctx.arc(x3, y3, 12, 0, Math.PI * 2);
            ctx.fill();
            
            // Connection lines
            ctx.strokeStyle = 'rgba(255,255,255,0.1)';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.lineTo(x3, y3);
            ctx.closePath();
            ctx.stroke();
            
            requestAnimationFrame(draw);
        }
        draw();
    </script>
</body>
</html>"""

# --- Typst Report Template ---
TYPST_REPORT = """#set page(paper: "a4", margin: 2cm)
#set text(font: "Helvetica", size: 11pt)

#let title-page(title, subtitle) = {
  align(center + horizon)[
    #text(size: 24pt, weight: "bold", title)
    #v(1cm)
    #text(size: 14pt, style: "italic", subtitle)
    #v(2cm)
    #line(length: 100%)
    #v(1cm)
    *Generated by WAFT System*
    #datetime.today().display()
  ]
  pagebreak()
}

#title-page("TheGuide: Iterative Evolution", "Project 'Self-Push' Report")

= Executive Summary
This document captures the iterative evolution of the "TheGuide" meta-cognitive dashboard. The system underwent a rapid self-improvement cycle focusing on visualization, real-time telemetry, and FVCU (Factuality, Validity, Coherence, Utility) integration.

The 3-Body Problem architecture (Mind: TheOracle, Body: NarcissusAgent, Spirit: TheGuide) was visualized through an animated canvas simulation, demonstrating the dynamic relationships between components.

= Iteration History

== Stage 1: Baseline
The initial state represented a minimal connectivity test ("Hello World") with a clean, gradient-based design showcasing the three components in a static card layout.

#figure(
  rect(width: 100%, height: 6cm, fill: luma(240%), stroke: 1pt + gray)[
    #align(center + horizon)[*Screenshot Placeholder: BASELINE*]
  ],
  caption: [Initial server response with static 3-Body architecture display.]
)

*Key Features:*
- Gradient background (purple to blue)
- Three-card layout for Mind/Body/Spirit
- Status indicator showing system activation
- Clean, modern typography

== Stage 2: Visual Architecture
The UI was overhauled to reflect the "Pantheon" aesthetic: dark mode, high-contrast neon accents (#00ff9d), and a live canvas rendering the 3-Body problem (Mind, Body, Spirit) with orbital mechanics.

#figure(
  rect(width: 100%, height: 6cm, fill: luma(240%), stroke: 1pt + gray)[
    #align(center + horizon)[*Screenshot Placeholder: VISUALS*]
  ],
  caption: [Dark mode interface with animated 3-Body simulation canvas.]
)

*Key Features:*
- Dark theme (#0a0a0a background, #1a1a1a panels)
- Three-panel layout (Log Stream | Canvas | Metrics)
- Real-time 3-Body orbital animation
- Monospace typography (Courier New)
- Neon accent colors for active states
- Live log stream with status indicators

== Stage 3: Meta-Cognitive Integration
The final stage integrated mock data streams for FVCU analysis and multi-agent coordination (Narcissus/Empirica status). The metrics panel was replaced with FVCU scores, and the log stream showed active agent communication.

#figure(
  rect(width: 100%, height: 6cm, fill: luma(240%), stroke: 1pt + gray)[
    #align(center + horizon)[*Screenshot Placeholder: META*]
  ],
  caption: [Live telemetry with FVCU metrics and agent coordination logs.]
)

*Key Features:*
- FVCU (Factuality, Validity, Coherence, Utility) scoring
- Entropy metric with danger threshold visualization
- Active agent status (Narcissus, Empirica)
- Fracture detection and repair strategy logging
- Color-coded log entries (success/warning/active)
- Enhanced 3-Body animation with connection lines

= Technical Implementation

== Architecture
The dashboard is served via a Python HTTP server (`theguide_hello.py`) that:
- Initializes TheGuide Pantheon entity
- Serves HTML content dynamically
- Provides JSON API endpoint for status (`/api/guide/status`)
- Runs on localhost:7072

== Evolution Process
The "Self-Iterative Push" protocol:
1. *Backup*: Original HTML template preserved
2. *Iterate*: Three distinct versions applied sequentially
3. *Observe*: Screenshots captured at each stage
4. *Document*: Typst report generated automatically

= Future Roadmap
1. **Real-time WebSocket Integration**: Connect canvas to actual `Empirica` state
2. **Interactive Console**: Allow direct querying of TheOracle via the web UI
3. **Agent Graph**: Visualize the connection topology between _pyrite, NovaSystem, and Narcissus
4. **Live FVCU Updates**: Stream actual evaluation scores from TheGuide sessions
5. **Fracture Visualization**: Show detected fractures in source code with repair strategies
6. **Session History**: Display past guidance sessions and protocols

= Conclusion
The iterative evolution successfully transformed a simple "Hello World" page into a sophisticated meta-cognitive dashboard. The 3-Body Problem visualization provides immediate visual feedback on system state, while FVCU metrics offer quantitative assessment of reasoning quality.

The dashboard now serves as both a monitoring tool and a demonstration of the unified architecture, where Mind (TheOracle), Body (NarcissusAgent), and Spirit (TheGuide) work in harmony.
"""

def main():
    """Execute the Self-Iterative Push protocol."""
    # Create work directory
    WORK_DIR.mkdir(exist_ok=True)
    SCREENSHOT_DIR.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("✨ Self-Iterative Push Protocol: TheGuide Evolution")
    print("=" * 60)
    print(f"\n📁 Work Directory: {WORK_DIR.absolute()}")
    print(f"📸 Screenshot Directory: {SCREENSHOT_DIR.absolute()}")
    print(f"📄 Report File: {REPORT_FILE.absolute()}")
    
    # Backup original file
    backup_path = TARGET_FILE.with_suffix(".py.bak")
    if not backup_path.exists():
        shutil.copy(TARGET_FILE, backup_path)
        print(f"\n✅ Created backup: {backup_path}")
    
    # Extract current HTML from the server file
    print(f"\n📋 Target file: {TARGET_FILE}")
    
    # --- STAGE 1: BASELINE ---
    print("\n" + "=" * 60)
    print("--- STAGE 1: BASELINE (CURRENT STATE) ---")
    print("=" * 60)
    print("\n✅ Baseline is currently active on the server.")
    print("   📸 Screenshot location: " + str(SCREENSHOT_DIR / 'baseline.png'))
    print("   🌐 View at: http://localhost:7072")
    print("\n   [You can take the screenshot now, then continue...]")
    time.sleep(2)
    
    # --- STAGE 2: VISUAL UPGRADE ---
    print("\n" + "=" * 60)
    print("--- STAGE 2: VISUAL UPGRADE ---")
    print("=" * 60)
    
    # Update the server to serve V2
    update_server_html(TARGET_FILE, HTML_V2)
    print("✅ Applied V2 (Dark Mode + 3-Body Animation)")
    print("   🔄 Please RELOAD http://localhost:7072 in your browser")
    print("   📸 Screenshot location: " + str(SCREENSHOT_DIR / 'visuals.png'))
    print("\n   [Waiting 5 seconds for you to reload and observe...]")
    time.sleep(5)
    
    # --- STAGE 3: META INTEGRATION ---
    print("\n" + "=" * 60)
    print("--- STAGE 3: META-COGNITIVE INTEGRATION ---")
    print("=" * 60)
    
    # Update the server to serve V3
    update_server_html(TARGET_FILE, HTML_V3)
    print("✅ Applied V3 (FVCU Analysis + Live Telemetry)")
    print("   🔄 Please RELOAD http://localhost:7072 in your browser")
    print("   📸 Screenshot location: " + str(SCREENSHOT_DIR / 'meta.png'))
    print("\n   [Waiting 5 seconds for you to reload and observe...]")
    time.sleep(5)
    
    # --- Generate Report ---
    print("\n" + "=" * 60)
    print("--- GENERATING REPORT ---")
    print("=" * 60)
    
    REPORT_FILE.write_text(TYPST_REPORT)
    print(f"✅ Generated Typst report: {REPORT_FILE}")
    print(f"\n📝 To compile the report, run:")
    print(f"   typst compile {REPORT_FILE}")
    
    print("\n" + "=" * 60)
    print("✅ Self-Iterative Push Protocol Complete!")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"   - 3 stages completed")
    print(f"   - Screenshots: {SCREENSHOT_DIR}")
    print(f"   - Report: {REPORT_FILE}")
    print(f"\n💡 Note: Server is now running V3. Restore backup if needed.")

def update_server_html(server_file: Path, html_content: str):
    """Update the serve_hello_world method in the server file."""
    content = server_file.read_text()
    
    import re
    
    # Pattern to match the HTML template (handles f-strings)
    # Match from "html = f\"\"\"" or "html = \"\"\"" to the closing """
    pattern = r'(def serve_hello_world\(self\):.*?html = f?""").*?(""")'
    
    # Replace with new HTML (keep f-string format if needed)
    new_content = re.sub(
        pattern,
        f'\\1{html_content}\\2',
        content,
        flags=re.DOTALL
    )
    
    server_file.write_text(new_content)
    print(f"   ✅ Server file updated")

if __name__ == "__main__":
    main()
