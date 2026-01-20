#!/usr/bin/env python3
"""
Interactive Proof System Demo Server

Creates a Colab-style interactive demo page where you can test claims
and see the proof system in action.

Usage:
    python3 scripts/proof_system_demo_server.py

Then open http://localhost:8000 in your browser.
"""

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from scripts.prove_it_comprehensive import ProofCaseBuilder

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WAFT Proof System - Interactive Demo</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #1e1e1e;
            color: #d4d4d4;
            line-height: 1.6;
        }}

        .header {{
            background: #252526;
            border-bottom: 1px solid #3e3e42;
            padding: 1rem 2rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .header h1 {{
            font-size: 1.5rem;
            font-weight: 600;
            color: #ffffff;
        }}

        .header .subtitle {{
            color: #858585;
            font-size: 0.9rem;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        .intro {{
            background: #252526;
            border: 1px solid #3e3e42;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 2rem;
        }}

        .intro h2 {{
            color: #4ec9b0;
            margin-bottom: 1rem;
            font-size: 1.3rem;
        }}

        .intro p {{
            margin-bottom: 0.5rem;
            color: #cccccc;
        }}

        .cell {{
            background: #252526;
            border: 1px solid #3e3e42;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            overflow: hidden;
        }}

        .cell-header {{
            background: #2d2d30;
            padding: 0.75rem 1rem;
            border-bottom: 1px solid #3e3e42;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .cell-type {{
            background: #0e639c;
            color: white;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .cell-type.code {{
            background: #0e639c;
        }}

        .cell-type.output {{
            background: #6a8759;
        }}

        .cell-content {{
            padding: 1rem;
        }}

        .claim-input {{
            width: 100%;
            min-height: 100px;
            background: #1e1e1e;
            color: #d4d4d4;
            border: 1px solid #3e3e42;
            padding: 1rem;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 0.95rem;
            resize: vertical;
            border-radius: 4px;
        }}

        .claim-input:focus {{
            outline: 2px solid #0e639c;
            outline-offset: -2px;
        }}

        .run-button {{
            background: #0e639c;
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
            margin-top: 1rem;
            transition: background 0.2s;
            font-size: 1rem;
        }}

        .run-button:hover {{
            background: #1177bb;
        }}

        .run-button:active {{
            background: #0a4d73;
        }}

        .run-button:disabled {{
            background: #3e3e42;
            cursor: not-allowed;
            opacity: 0.6;
        }}

        .output {{
            background: #1e1e1e;
            padding: 1.5rem;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9rem;
            white-space: pre-wrap;
            word-wrap: break-word;
            max-height: 800px;
            overflow-y: auto;
        }}

        .output.success {{
            color: #4ec9b0;
        }}

        .output.error {{
            color: #f48771;
        }}

        .example-claims {{
            background: #2d2d30;
            border: 1px solid #3e3e42;
            border-radius: 4px;
            padding: 1rem;
            margin-bottom: 2rem;
        }}

        .example-claims h3 {{
            color: #4ec9b0;
            margin-bottom: 0.75rem;
            font-size: 1rem;
        }}

        .example-claim {{
            background: #1e1e1e;
            padding: 0.75rem;
            margin: 0.5rem 0;
            border-radius: 4px;
            cursor: pointer;
            transition: background 0.2s;
            border-left: 3px solid #0e639c;
        }}

        .example-claim:hover {{
            background: #252526;
        }}

        .example-claim code {{
            color: #ce9178;
            font-size: 0.85rem;
        }}

        .analysis-section {{
            margin: 1rem 0;
            padding: 1rem;
            background: #2d2d30;
            border-radius: 4px;
            border-left: 4px solid #0e639c;
        }}

        .analysis-section h4 {{
            color: #4ec9b0;
            margin-bottom: 0.5rem;
        }}

        .assumption {{
            background: #1e1e1e;
            border: 1px solid #3e3e42;
            border-radius: 4px;
            padding: 1rem;
            margin: 0.75rem 0;
            border-left: 4px solid #3e3e42;
        }}

        .assumption.proven {{
            border-left-color: #4ec9b0;
        }}

        .assumption.disproven {{
            border-left-color: #f48771;
        }}

        .assumption.inconclusive {{
            border-left-color: #dcdcaa;
        }}

        .assumption-header {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 0.5rem;
        }}

        .status-badge {{
            padding: 0.3rem 0.8rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .status-badge.proven {{
            background: #1e3a1e;
            color: #4ec9b0;
        }}

        .status-badge.disproven {{
            background: #3a1e1e;
            color: #f48771;
        }}

        .status-badge.inconclusive {{
            background: #3a3a1e;
            color: #dcdcaa;
        }}

        .evidence {{
            margin-top: 0.75rem;
            padding: 0.75rem;
            background: #252526;
            border-radius: 4px;
            font-size: 0.85rem;
        }}

        .evidence-item {{
            margin: 0.5rem 0;
            color: #858585;
        }}

        .evidence-item strong {{
            color: #cccccc;
        }}

        .loading {{
            display: inline-block;
            width: 16px;
            height: 16px;
            border: 2px solid #3e3e42;
            border-top-color: #0e639c;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin-right: 0.5rem;
        }}

        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}

        .summary {{
            background: #2d2d30;
            border: 1px solid #3e3e42;
            border-radius: 4px;
            padding: 1rem;
            margin: 1rem 0;
        }}

        .summary h4 {{
            color: #4ec9b0;
            margin-bottom: 0.5rem;
        }}

        .summary-stats {{
            display: flex;
            gap: 2rem;
            margin-top: 0.5rem;
        }}

        .stat {{
            text-align: center;
        }}

        .stat-value {{
            font-size: 1.5rem;
            font-weight: 600;
            color: #4ec9b0;
        }}

        .stat-label {{
            font-size: 0.75rem;
            color: #858585;
            text-transform: uppercase;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔬 WAFT Proof System - Interactive Demo</h1>
        <span class="subtitle">Test claims and see the proof system in action</span>
    </div>

    <div class="container">
        <div class="intro">
            <h2>Welcome to the Interactive Proof System Demo</h2>
            <p>This page demonstrates the <strong>claim analysis system</strong> we just fixed. Enter a claim below and watch the system:</p>
            <ul style="margin-left: 1.5rem; margin-top: 0.5rem;">
                <li>✅ Analyze the claim to determine what to test</li>
                <li>✅ Identify target files and features</li>
                <li>✅ Run appropriate verification checks</li>
                <li>✅ Display proof results with evidence</li>
            </ul>
            <p style="margin-top: 1rem; color: #4ec9b0;"><strong>🎯 Key Fix:</strong> The system now analyzes claims instead of always checking templates!</p>
        </div>

        <div class="example-claims">
            <h3>📋 Example Claims (Click to Use)</h3>
            <div class="example-claim" onclick="setClaim('The show-me HTML report (show_me_bulletproof.py) implements a unified above-the-fold section with ID above-the-fold, responsive design with mobile breakpoints, and an abstract copy button that uses the clipboard API')">
                <strong>HTML Report Features:</strong><br>
                <code>The show-me HTML report (show_me_bulletproof.py) implements a unified above-the-fold section with ID above-the-fold, responsive design with mobile breakpoints, and an abstract copy button that uses the clipboard API</code>
            </div>
            <div class="example-claim" onclick="setClaim('All PDF templates have been fixed to remove black bars from headers')">
                <strong>Template Black Bars:</strong><br>
                <code>All PDF templates have been fixed to remove black bars from headers</code>
            </div>
            <div class="example-claim" onclick="setClaim('The proof system can analyze claims and determine what to test')">
                <strong>Proof System Analysis:</strong><br>
                <code>The proof system can analyze claims and determine what to test</code>
            </div>
        </div>

        <div class="cell">
            <div class="cell-header">
                <span class="cell-type code">Claim Input</span>
                <span style="color: #858585; font-size: 0.85rem;">Enter your claim and run the proof system</span>
            </div>
            <div class="cell-content">
                <textarea class="claim-input" id="claim-input" placeholder='Enter a claim to prove, e.g.:
"The show-me HTML report implements above-the-fold section with responsive design"

Or click an example above.'></textarea>
                <button class="run-button" id="run-button" onclick="runProof()">▶ Run Proof</button>
            </div>
        </div>

        <div class="cell" id="output-cell" style="display: none;">
            <div class="cell-header">
                <span class="cell-type output">Proof Results</span>
            </div>
            <div class="cell-content" id="output-content">
                <div class="output" id="output"></div>
            </div>
        </div>
    </div>

    <script>
        function setClaim(claimText) {{
            document.getElementById('claim-input').value = claimText;
            document.getElementById('claim-input').scrollIntoView({{ behavior: 'smooth', block: 'center' }});
        }}

        async function runProof() {{
            const claim = document.getElementById('claim-input').value.trim();
            if (!claim) {{
                alert('Please enter a claim first');
                return;
            }}

            const outputDiv = document.getElementById('output');
            const outputCell = document.getElementById('output-cell');
            const runButton = document.getElementById('run-button');

            // Show output cell
            outputCell.style.display = 'block';
            outputDiv.className = 'output';
            outputDiv.innerHTML = '<div class="loading"></div>Running proof system...';
            runButton.disabled = true;
            runButton.textContent = '⏳ Running...';

            try {{
                const response = await fetch('/prove', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{ claim: claim }})
                }});

                if (!response.ok) {{
                    throw new Error(`HTTP error! status: ${{response.status}}`);
                }}

                const data = await response.json();
                displayResults(data);

            }} catch (error) {{
                outputDiv.className = 'output error';
                outputDiv.textContent = `Error: ${{error.message}}`;
            }} finally {{
                runButton.disabled = false;
                runButton.textContent = '▶ Run Proof';
                outputCell.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
            }}
        }}

        function displayResults(data) {{
            const outputDiv = document.getElementById('output');
            const outputContent = document.getElementById('output-content');

            let html = '';

            // Summary
            html += `<div class="summary">
                <h4>📊 Proof Summary</h4>
                <div class="summary-stats">
                    <div class="stat">
                        <div class="stat-value">${{data.total}}</div>
                        <div class="stat-label">Total Assumptions</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value" style="color: #4ec9b0;">${{data.proven}}</div>
                        <div class="stat-label">Proven</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value" style="color: #f48771;">${{data.disproven}}</div>
                        <div class="stat-label">Disproven</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value" style="color: #dcdcaa;">${{data.inconclusive}}</div>
                        <div class="stat-label">Inconclusive</div>
                    </div>
                </div>
            </div>`;

            // Claim Analysis
            if (data.analysis) {{
                html += `<div class="analysis-section">
                    <h4>🔍 Claim Analysis</h4>
                    <p><strong>Verification Type:</strong> <code>${{data.analysis.verification_type}}</code></p>
                    <p><strong>Target Files:</strong> <code>${{data.analysis.target_files.join(', ') || 'None identified'}}</code></p>
                    <p><strong>Features to Check:</strong> <code>${{data.analysis.features_to_check.join(', ') || 'None identified'}}</code></p>
                </div>`;
            }}

            // Assumptions
            if (data.assumptions && data.assumptions.length > 0) {{
                html += `<h4 style="color: #4ec9b0; margin-top: 1.5rem; margin-bottom: 0.5rem;">📋 Assumption Validation</h4>`;

                data.assumptions.forEach((assumption, i) => {{
                    const status = assumption.status.toLowerCase();
                    const statusClass = status === 'proven' ? 'proven' : (status === 'disproven' ? 'disproven' : 'inconclusive');

                    html += `<div class="assumption ${{statusClass}}">
                        <div class="assumption-header">
                            <span class="status-badge ${{statusClass}}">${{assumption.status}}</span>
                            <strong>${{assumption.statement}}</strong>
                            <span style="color: #858585; margin-left: auto;">Confidence: ${{(assumption.confidence * 100).toFixed(0)}}%</span>
                        </div>`;

                    if (assumption.evidence && assumption.evidence.length > 0) {{
                        html += `<div class="evidence">`;
                        assumption.evidence.forEach(ev => {{
                            html += `<div class="evidence-item">`;
                            html += `<strong>${{ev.type}}:</strong> ${{ev.description}}`;
                            if (ev.result) {{
                                html += `<br><span style="color: #858585;">Result: ${{ev.result}}</span>`;
                            }}
                            if (ev.source_file) {{
                                html += `<br><span style="color: #858585;">Source: <code>${{ev.source_file}}</code></span>`;
                            }}
                            if (ev.source_lines && ev.source_lines.length > 0) {{
                                html += `<br><span style="color: #858585;">Lines: ${{ev.source_lines.join(', ')}}</span>`;
                            }}
                            html += `</div>`;
                        }});
                        html += `</div>`;
                    }}

                    html += `</div>`;
                }});
            }}

            outputDiv.className = 'output success';
            outputContent.innerHTML = html;
        }}
    </script>
</body>
</html>
"""


class ProofDemoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/prove":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))
            claim = data.get("claim", "")

            try:
                # Run proof system
                builder = ProofCaseBuilder(project_root, claim)

                # Analyze claim
                analysis = builder.analyze_claim()

                # Run assumption check
                assumptions_result = builder.run_assumption_check()

                # Prepare response
                response_data = {
                    "analysis": {
                        "verification_type": analysis["verification_type"],
                        "target_files": analysis["target_files"],
                        "features_to_check": analysis["features_to_check"],
                    },
                    "total": assumptions_result["total"],
                    "proven": assumptions_result["proven"],
                    "disproven": assumptions_result["disproven"],
                    "inconclusive": assumptions_result["total"]
                    - assumptions_result["proven"]
                    - assumptions_result["disproven"],
                    "assumptions": assumptions_result["assumptions"],
                }

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode())

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                error_response = {"error": str(e), "type": type(e).__name__}
                self.wfile.write(json.dumps(error_response).encode())

    def log_message(self, format, *args):
        # Suppress default logging
        pass


def main():
    port = 8000
    server_address = ("", port)
    httpd = HTTPServer(server_address, ProofDemoHandler)

    print("=" * 70)
    print("🔬 WAFT Proof System - Interactive Demo Server")
    print("=" * 70)
    print()
    print(f"✅ Server running at http://localhost:{port}")
    print()
    print("📋 Open your browser and navigate to:")
    print(f"   http://localhost:{port}")
    print()
    print("🎯 Try the example claims or enter your own!")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 70)
    print()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down server...")
        httpd.shutdown()
        print("✅ Server stopped")


if __name__ == "__main__":
    main()
