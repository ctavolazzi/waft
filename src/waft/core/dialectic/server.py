"""
DIALECTIC Server - The Dialectical Analysis Engine

Port: 2112 (Rush's sci-fi concept album reference)
Philosophy: Hegelian Dialectics - Thesis, Antithesis, Synthesis
"""

import http.server
import socketserver
import json
import logging
import subprocess
import shutil
from pathlib import Path
from typing import Any
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [DIALECTIC] - %(message)s')
logger = logging.getLogger("Dialectic")

DIALECTIC_PORT = 2112


class DialecticServer:
    """
    DIALECTIC - The Dialectical Analysis Engine
    
    A God that orchestrates three-phase analysis:
    - THESIS (Assembly): AI Town + Orchestration
    - ANTITHESIS (Sanity Check): Check Assumptions + Checkout
    - SYNTHESIS (Problem Description): Brief + Scientific Docs
    """
    
    def __init__(self, project_path: Path, port: int = DIALECTIC_PORT):
        self.project_path = Path(project_path)
        self.port = port
        self.realm_path = self.project_path / "_realms" / "dialectic_realm"
        self.outputs_path = self.realm_path / "outputs"
        self.sessions_path = self.realm_path / "sessions"
        self.current_session: dict[str, Any] | None = None
        self.server = None
        
        # Ensure realm directories exist
        self._ensure_realm_structure()
        
    def _ensure_realm_structure(self):
        """Ensure the realm directory structure exists."""
        (self.outputs_path / "assembly").mkdir(parents=True, exist_ok=True)
        (self.outputs_path / "sanity").mkdir(parents=True, exist_ok=True)
        (self.outputs_path / "synthesis").mkdir(parents=True, exist_ok=True)
        self.sessions_path.mkdir(parents=True, exist_ok=True)
        
    def _create_session(self) -> dict[str, Any]:
        """Create a new analysis session."""
        session_id = f"dialectic_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        session = {
            "id": session_id,
            "created_at": datetime.now().isoformat(),
            "phases": {
                "thesis": {"status": "pending", "output": None},
                "antithesis": {"status": "pending", "output": None},
                "synthesis": {"status": "pending", "output": None},
            },
            "sitrep": None,
        }
        self.current_session = session
        
        # Save session to disk
        session_file = self.sessions_path / f"{session_id}.json"
        with open(session_file, "w") as f:
            json.dump(session, f, indent=2)
            
        logger.info(f"Created session: {session_id}")
        return session

    def start(self):
        """Start the DIALECTIC server."""
        # Create initial session
        self._create_session()
        
        handler = lambda *args, **kwargs: DialecticRequestHandler(self, *args, **kwargs)
        socketserver.TCPServer.allow_reuse_address = True
        self.server = socketserver.TCPServer(("", self.port), handler)
        
        logger.info(f"")
        logger.info(f"╔══════════════════════════════════════════════════════════════╗")
        logger.info(f"║           DIALECTIC - The Dialectical Analysis Engine        ║")
        logger.info(f"║                                                              ║")
        logger.info(f"║   Port: {self.port}                                              ║")
        logger.info(f"║   URL:  http://localhost:{self.port}                            ║")
        logger.info(f"║                                                              ║")
        logger.info(f"║   Phases:                                                    ║")
        logger.info(f"║     1. THESIS     (Assembly)       - Gather & Orchestrate    ║")
        logger.info(f"║     2. ANTITHESIS (Sanity Check)   - Verify & Challenge      ║")
        logger.info(f"║     3. SYNTHESIS  (Problem Desc)   - Brief & Document        ║")
        logger.info(f"║                                                              ║")
        logger.info(f"║   Philosophy: Hegelian Dialectics                            ║")
        logger.info(f"╚══════════════════════════════════════════════════════════════╝")
        logger.info(f"")
        logger.info("Awaiting Thesis...")
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop the DIALECTIC server."""
        logger.info("DIALECTIC Engine shutting down...")
        if self.server:
            self.server.shutdown()
            self.server.server_close()

    def run_assembly_phase(self) -> dict[str, Any]:
        """
        Execute Phase 1: THESIS (Assembly)
        
        Runs AI Town Analysis + Comprehensive Orchestration.
        Gathers context, evidence, and initial state.
        """
        logger.info("═══════════════════════════════════════════════════════════════")
        logger.info("  Phase 1: THESIS (Assembly)")
        logger.info("═══════════════════════════════════════════════════════════════")
        
        from .phases.assembly import AssemblyPhase
        
        phase = AssemblyPhase(self.project_path, self.outputs_path / "assembly")
        result = phase.run()
        
        if self.current_session:
            self.current_session["phases"]["thesis"] = {
                "status": "complete",
                "output": result.get("output_path"),
                "completed_at": datetime.now().isoformat(),
            }
            self._save_session()
            
        logger.info(f"THESIS complete: {result.get('output_path', 'N/A')}")
        return result

    def run_antithesis_phase(self) -> dict[str, Any]:
        """
        Execute Phase 2: ANTITHESIS (Sanity Check)
        
        Runs Check Assumptions + Checkout.
        Challenges and validates gathered evidence.
        """
        logger.info("═══════════════════════════════════════════════════════════════")
        logger.info("  Phase 2: ANTITHESIS (Sanity Check)")
        logger.info("═══════════════════════════════════════════════════════════════")
        
        from .phases.antithesis import AntithesisPhase
        
        phase = AntithesisPhase(self.project_path, self.outputs_path / "sanity")
        result = phase.run()
        
        if self.current_session:
            self.current_session["phases"]["antithesis"] = {
                "status": "complete",
                "output": result.get("output_path"),
                "completed_at": datetime.now().isoformat(),
            }
            self._save_session()
            
        logger.info(f"ANTITHESIS complete: {result.get('output_path', 'N/A')}")
        return result

    def run_synthesis_phase(self) -> dict[str, Any]:
        """
        Execute Phase 3: SYNTHESIS (Problem Description)
        
        Runs Brief creation + MVP + Scientific Docs.
        Synthesizes findings into actionable documents.
        """
        logger.info("═══════════════════════════════════════════════════════════════")
        logger.info("  Phase 3: SYNTHESIS (Problem Description)")
        logger.info("═══════════════════════════════════════════════════════════════")
        
        from .phases.synthesis import SynthesisPhase
        
        phase = SynthesisPhase(self.project_path, self.outputs_path / "synthesis")
        result = phase.run()
        
        if self.current_session:
            self.current_session["phases"]["synthesis"] = {
                "status": "complete",
                "output": result.get("output_path"),
                "completed_at": datetime.now().isoformat(),
            }
            self._save_session()
            
        logger.info(f"SYNTHESIS complete: {result.get('output_path', 'N/A')}")
        return result
        
    def generate_sitrep(self) -> dict[str, Any]:
        """
        Generate Final SITREP Document
        
        Combines all three phases into a comprehensive status report
        that can seed a Work Effort.
        """
        logger.info("═══════════════════════════════════════════════════════════════")
        logger.info("  Generating SITREP - Status Report")
        logger.info("═══════════════════════════════════════════════════════════════")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"SITREP_{timestamp}.typ"
        output_path = self.outputs_path / output_filename
        
        # Generate SITREP content
        sitrep_content = self._generate_sitrep_content()
        
        # Write Typst file
        with open(output_path, "w") as f:
            f.write(sitrep_content)
            
        # Compile to PDF if typst is available
        pdf_path = None
        if shutil.which("typst"):
            pdf_output = output_path.with_suffix(".pdf")
            try:
                subprocess.run(
                    ["typst", "compile", str(output_path), str(pdf_output)],
                    check=True,
                    capture_output=True,
                )
                pdf_path = str(pdf_output)
                logger.info(f"SITREP PDF generated: {pdf_path}")
            except subprocess.CalledProcessError as e:
                logger.warning(f"Typst compilation failed: {e}")
        else:
            logger.warning("Typst not found - SITREP saved as .typ only")
            
        if self.current_session:
            self.current_session["sitrep"] = {
                "status": "complete",
                "output": pdf_path or str(output_path),
                "completed_at": datetime.now().isoformat(),
            }
            self._save_session()
            
        return {
            "status": "success",
            "output": pdf_path or str(output_path),
            "typ_path": str(output_path),
        }
        
    def _generate_sitrep_content(self) -> str:
        """Generate the SITREP Typst content."""
        timestamp = datetime.now()
        dtg = timestamp.strftime("%d%H%MZ %b %Y").upper()
        
        return f'''// SITREP - Status Report
// Generated by DIALECTIC Engine
// {timestamp.isoformat()}

#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center)[
  #text(16pt, weight: "bold")[SITUATION REPORT (SITREP)]
  #v(0.5em)
  #text(12pt)[DTG: {dtg}]
  #v(0.3em)
  #text(10pt, style: "italic")[Generated by DIALECTIC Engine // Port 2112]
]

#line(length: 100%, stroke: 0.5pt)

= 1. SITUATION

== a. Internal State Summary

#block(inset: 1em, stroke: (left: 3pt + blue))[
  *THESIS (Assembly Phase)* \\
  Status: {self.current_session["phases"]["thesis"]["status"] if self.current_session else "N/A"} \\
  Output: {self.current_session["phases"]["thesis"].get("output", "N/A") if self.current_session else "N/A"}
]

== b. External State Summary

Analysis of external dependencies and environment state would be captured here based on the Assembly phase output.

= 2. MISSION

Derived from the SYNTHESIS phase - the problem description and recommended course of action.

#block(inset: 1em, stroke: (left: 3pt + purple))[
  *SYNTHESIS (Problem Description Phase)* \\
  Status: {self.current_session["phases"]["synthesis"]["status"] if self.current_session else "N/A"} \\
  Output: {self.current_session["phases"]["synthesis"].get("output", "N/A") if self.current_session else "N/A"}
]

= 3. EXECUTION

== a. Thesis Phase Results
Evidence gathered and context established.

== b. Antithesis Phase Results
#block(inset: 1em, stroke: (left: 3pt + red))[
  *ANTITHESIS (Sanity Check Phase)* \\
  Status: {self.current_session["phases"]["antithesis"]["status"] if self.current_session else "N/A"} \\
  Output: {self.current_session["phases"]["antithesis"].get("output", "N/A") if self.current_session else "N/A"}
]

== c. Synthesis Phase Results
Problem description and recommendations synthesized.

= 4. SUSTAINMENT

Resources and dependencies identified during analysis.

= 5. COMMAND AND SIGNAL

== Next Steps
1. Review phase outputs
2. Consider seeding Work Effort from this SITREP
3. Execute recommended actions

#v(2em)
#line(length: 100%, stroke: 0.5pt)
#align(center)[
  #text(8pt, fill: gray)[
    DIALECTIC Engine // Realm: dialectic_realm // Port: 2112 \\
    Philosophy: Hegelian Dialectics - Thesis, Antithesis, Synthesis
  ]
]
'''

    def _save_session(self):
        """Save current session to disk."""
        if self.current_session:
            session_file = self.sessions_path / f"{self.current_session['id']}.json"
            with open(session_file, "w") as f:
                json.dump(self.current_session, f, indent=2)

    def _get_html(self) -> str:
        """Generate the dashboard HTML."""
        return self._get_dashboard_html()
        
    def _get_dashboard_html(self) -> str:
        """Generate the DIALECTIC dashboard HTML."""
        return '''<!DOCTYPE html>
<html>
<head>
    <title>DIALECTIC // PORT 2112</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
            color: #c9d1d9; 
            font-family: 'Courier New', monospace; 
            padding: 30px;
            min-height: 100vh;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 20px;
            border: 1px solid #30363d;
            border-radius: 8px;
            background: rgba(13, 17, 23, 0.8);
        }
        h1 { 
            color: #58a6ff; 
            font-size: 2.5em;
            text-shadow: 0 0 20px rgba(88, 166, 255, 0.5);
        }
        .subtitle { color: #8b949e; margin-top: 10px; }
        .container { 
            display: flex; 
            gap: 20px; 
            margin-top: 20px;
            flex-wrap: wrap;
            justify-content: center;
        }
        .panel { 
            border: 1px solid #30363d; 
            padding: 25px; 
            flex: 1;
            min-width: 280px;
            max-width: 350px;
            border-radius: 8px;
            background: rgba(22, 27, 34, 0.9);
            transition: all 0.3s ease;
        }
        .panel:hover {
            border-color: #58a6ff;
            box-shadow: 0 0 20px rgba(88, 166, 255, 0.2);
        }
        h2 { margin-top: 0; margin-bottom: 15px; }
        button { 
            background: #238636; 
            color: white; 
            border: none; 
            padding: 12px 24px; 
            cursor: pointer; 
            border-radius: 6px; 
            font-family: monospace;
            font-size: 14px;
            width: 100%;
            transition: all 0.2s ease;
        }
        button:hover { 
            background: #2ea043;
            transform: translateY(-2px);
        }
        button:active {
            transform: translateY(0);
        }
        .status { 
            margin-top: 15px; 
            color: #8b949e;
            padding: 10px;
            border-radius: 4px;
            background: rgba(0,0,0,0.3);
            min-height: 40px;
        }
        .thesis { border-top: 4px solid #1f6feb; }
        .thesis h2 { color: #1f6feb; }
        .antithesis { border-top: 4px solid #da3633; }
        .antithesis h2 { color: #da3633; }
        .synthesis { border-top: 4px solid #a371f7; }
        .synthesis h2 { color: #a371f7; }
        .sitrep-section {
            margin-top: 40px;
            text-align: center;
            padding: 30px;
            border: 2px dashed #30363d;
            border-radius: 8px;
        }
        .sitrep-section button {
            background: #1f6feb;
            font-size: 16px;
            padding: 15px 30px;
            width: auto;
        }
        .sitrep-section button:hover {
            background: #388bfd;
        }
        .phase-icon {
            font-size: 2em;
            margin-bottom: 10px;
        }
        .philosophy {
            margin-top: 40px;
            text-align: center;
            color: #6e7681;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>DIALECTIC</h1>
        <div class="subtitle">The Dialectical Analysis Engine // Port 2112</div>
    </div>
    
    <div class="container">
        <div class="panel thesis">
            <div class="phase-icon">📚</div>
            <h2>THESIS</h2>
            <p style="color: #8b949e; margin-bottom: 15px;">Assembly Phase</p>
            <p style="font-size: 12px; margin-bottom: 15px;">
                Gather context, run AI Town analysis, comprehensive orchestration.
            </p>
            <button onclick="trigger('/api/assembly/start', 'thesis-status')">Start Assembly</button>
            <div id="thesis-status" class="status">Awaiting initiation...</div>
        </div>
        
        <div class="panel antithesis">
            <div class="phase-icon">🔍</div>
            <h2>ANTITHESIS</h2>
            <p style="color: #8b949e; margin-bottom: 15px;">Sanity Check Phase</p>
            <p style="font-size: 12px; margin-bottom: 15px;">
                Check assumptions, validate evidence, create checkout.
            </p>
            <button onclick="trigger('/api/antithesis/start', 'antithesis-status')">Start Check</button>
            <div id="antithesis-status" class="status">Awaiting thesis...</div>
        </div>
        
        <div class="panel synthesis">
            <div class="phase-icon">✨</div>
            <h2>SYNTHESIS</h2>
            <p style="color: #8b949e; margin-bottom: 15px;">Problem Description</p>
            <p style="font-size: 12px; margin-bottom: 15px;">
                Create briefs, MVP docs, scientific reports.
            </p>
            <button onclick="trigger('/api/synthesis/start', 'synthesis-status')">Start Synthesis</button>
            <div id="synthesis-status" class="status">Awaiting antithesis...</div>
        </div>
    </div>

    <div class="sitrep-section">
        <h3 style="color: #58a6ff; margin-bottom: 20px;">FINAL OUTPUT</h3>
        <button onclick="trigger('/api/sitrep', 'sitrep-status')">GENERATE SITREP</button>
        <div id="sitrep-status" class="status" style="margin-top: 20px; display: inline-block; min-width: 300px;"></div>
    </div>
    
    <div class="philosophy">
        "The truth is the whole." - G.W.F. Hegel
    </div>

    <script>
        function trigger(endpoint, statusId) {
            const statusEl = document.getElementById(statusId);
            statusEl.innerText = "Running...";
            statusEl.style.color = "#f0883e";
            
            fetch(endpoint, { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    statusEl.innerText = "✓ Complete: " + (data.output || "Success");
                    statusEl.style.color = "#3fb950";
                })
                .catch(e => {
                    statusEl.innerText = "✗ Error: " + e.message;
                    statusEl.style.color = "#f85149";
                });
        }
        
        // Check status on load
        fetch('/api/status')
            .then(r => r.json())
            .then(data => {
                console.log("Session:", data);
            });
    </script>
</body>
</html>'''


class DialecticRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP Request Handler for DIALECTIC Engine."""
    
    def __init__(self, dialectic_server, *args, **kwargs):
        self.dialectic = dialectic_server
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.dialectic._get_dashboard_html().encode())
            return
            
        if self.path == '/api/status':
            self._send_json({
                "session": self.dialectic.current_session,
                "port": self.dialectic.port,
                "realm": str(self.dialectic.realm_path),
            })
            return

        super().do_GET()

    def do_POST(self):
        if self.path == '/api/assembly/start':
            result = self.dialectic.run_assembly_phase()
            self._send_json(result)
        elif self.path == '/api/antithesis/start':
            result = self.dialectic.run_antithesis_phase()
            self._send_json(result)
        elif self.path == '/api/synthesis/start':
            result = self.dialectic.run_synthesis_phase()
            self._send_json(result)
        elif self.path == '/api/sitrep':
            result = self.dialectic.generate_sitrep()
            self._send_json(result)
        else:
            self.send_error(404)

    def _send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
        
    def log_message(self, format, *args):
        """Custom log format."""
        logger.debug(f"{self.address_string()} - {format % args}")
