"""
O.D.D. Observatory Server - Real-time Service Mesh Monitor

Port: 2077 (Cyberpunk reference)
Pattern: Similar to TheCampfire (embedded HTML/CSS/JS, pure stdlib)

Features:
- GET /           - Serve embedded HTML dashboard
- GET /api/mesh   - Return JSON topology (nodes + links + status)
- POST /api/smite - Kill process on port via lsof + SIGTERM
"""

import json
import os
import signal
import socket
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse


class ObservatoryHandler(BaseHTTPRequestHandler):
    """HTTP handler for O.D.D. Observatory."""

    def __init__(self, observatory_instance, *args, **kwargs):
        self.observatory = observatory_instance
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self._serve_html()
        elif path == "/observatory.css":
            self._serve_css()
        elif path == "/observatory.js":
            self._serve_js()
        elif path == "/api/mesh":
            self._serve_mesh_api()
        elif path == "/api/events":
            self._serve_sse()
        else:
            self._send_404()

    def do_POST(self):
        """Handle POST requests."""
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/smite":
            self._handle_smite()
        elif path == "/api/demo/start-realm":
            self._handle_start_realm()
        elif path == "/api/demo/stop-realm":
            self._handle_stop_realm()
        else:
            self._send_404()

    def _serve_html(self):
        """Serve the observatory HTML page."""
        html = self.observatory._get_html()
        self._send_response(200, "text/html", html.encode())

    def _serve_css(self):
        """Serve CSS."""
        css = self.observatory._get_css()
        self._send_response(200, "text/css", css.encode())

    def _serve_js(self):
        """Serve JavaScript."""
        js = self.observatory._get_js()
        self._send_response(200, "application/javascript", js.encode())

    def _serve_mesh_api(self):
        """Serve mesh topology API."""
        mesh = self.observatory.get_mesh_topology()
        self._send_json(mesh)

    def _serve_sse(self):
        """Serve Server-Sent Events stream for real-time updates."""
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        # Track previous status to detect changes
        prev_status = {}

        try:
            while True:
                # Get current status
                mesh = self.observatory.get_mesh_topology()
                current_status = {n["id"]: n["status"] for n in mesh["nodes"]}

                # Check for changes
                changes = []
                for node_id, status in current_status.items():
                    if prev_status.get(node_id) != status:
                        changes.append({"id": node_id, "status": status})

                # Send event only if something changed
                if changes:
                    event_data = json.dumps({"type": "status_update", "changes": changes})
                    self.wfile.write(f"data: {event_data}\n\n".encode())
                    self.wfile.flush()
                    prev_status = current_status
                elif not prev_status:
                    # First connection - send initial state
                    prev_status = current_status
                    event_data = json.dumps({"type": "initial", "nodes": mesh["nodes"]})
                    self.wfile.write(f"data: {event_data}\n\n".encode())
                    self.wfile.flush()

                # Check every 2 seconds (but only emit on change)
                import time
                time.sleep(2)

        except (BrokenPipeError, ConnectionResetError):
            # Client disconnected
            pass

    def _handle_smite(self):
        """Handle smite (kill process) request."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode()) if body else {}

            port = data.get("port")
            if not port:
                self._send_json({"success": False, "error": "No port specified"}, status=400)
                return

            success, message = self.observatory.smite_port(int(port))
            self._send_json({"success": success, "message": message})
        except Exception as e:
            self._send_json({"success": False, "error": str(e)}, status=500)

    def _handle_start_realm(self):
        """Handle start demo realm request."""
        result = self.observatory.start_demo_realm()
        self._send_json(result)

    def _handle_stop_realm(self):
        """Handle stop demo realm request."""
        result = self.observatory.stop_demo_realm()
        self._send_json(result)

    def _send_json(self, data: dict[str, Any], status: int = 200):
        """Send JSON response."""
        json_str = json.dumps(data, indent=2)
        self._send_response(status, "application/json", json_str.encode())

    def _send_response(self, status: int, content_type: str, data: bytes):
        """Send HTTP response."""
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def _send_404(self):
        """Send 404 response."""
        self._send_response(404, "text/plain", b"Not Found")

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


class ObservatoryServer:
    """
    O.D.D. Observatory - Real-time Service Mesh Monitor

    Monitors all Realms registered in PortRegistry and displays
    a live force-directed graph visualization.

    Port: 2077
    """

    def __init__(self, project_path: Path, port: int = 2077, host: str = "localhost"):
        """
        Initialize Observatory.

        Args:
            project_path: Path to project root
            port: HTTP server port (default: 2077)
            host: HTTP server host
        """
        self.project_path = Path(project_path)
        self.port = port
        self.host = host

        # Load PortRegistry for realm discovery
        from ..realms.port_registry import PortRegistry

        self.registry = PortRegistry(project_path)

        # Demo realm for interactive walkthrough (lazy-loaded)
        self.demo_realm_server = None

    def check_port_status(self, port: int) -> bool:
        """
        Check if a port is listening (service is up).

        Args:
            port: Port number to check

        Returns:
            True if port is listening, False otherwise
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        try:
            result = sock.connect_ex(("localhost", port))
            return result == 0
        except Exception:
            return False
        finally:
            sock.close()

    def get_mesh_topology(self) -> dict[str, Any]:
        """
        Get current mesh topology with node status.

        Returns:
            Dict with nodes, links, and metadata
        """
        nodes = []
        links = []

        # Add Architect (central node, always up)
        nodes.append(
            {
                "id": "architect",
                "name": "Architect",
                "type": "core",
                "port": None,
                "status": "up",
            }
        )

        # Add realm nodes from registry
        realm_ports = self.registry.get_all_ports()
        for realm_name, port in realm_ports.items():
            status = "up" if self.check_port_status(port) else "down"
            nodes.append(
                {
                    "id": realm_name,
                    "name": realm_name.replace("_", " ").title(),
                    "type": "realm",
                    "port": port,
                    "status": status,
                }
            )
            # Link to architect (star topology)
            links.append({"source": "architect", "target": realm_name})

        # Add service nodes
        service_ports = self.registry.get_all_service_ports()
        for service_name, port in service_ports.items():
            # Skip observatory itself
            if service_name == "observatory":
                continue
            status = "up" if self.check_port_status(port) else "down"
            nodes.append(
                {
                    "id": service_name,
                    "name": service_name.replace("_", " ").title(),
                    "type": "service",
                    "port": port,
                    "status": status,
                }
            )
            links.append({"source": "architect", "target": service_name})

        return {
            "nodes": nodes,
            "links": links,
            "timestamp": __import__("datetime").datetime.now().isoformat(),
        }

    def smite_port(self, port: int) -> tuple[bool, str]:
        """
        Kill process listening on a port.

        Args:
            port: Port number

        Returns:
            Tuple of (success, message)
        """
        try:
            # Find PID using lsof
            cmd = ["lsof", "-t", "-i", f":{port}"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

            if result.returncode != 0 or not result.stdout.strip():
                return False, f"No process found on port {port}"

            pid = int(result.stdout.strip().split()[0])

            # Kill the process
            os.kill(pid, signal.SIGTERM)
            return True, f"Sent SIGTERM to PID {pid} on port {port}"
        except subprocess.TimeoutExpired:
            return False, "Timeout finding process"
        except ValueError as e:
            return False, f"Invalid PID: {e}"
        except ProcessLookupError:
            return False, "Process already terminated"
        except PermissionError:
            return False, "Permission denied - cannot kill process"
        except Exception as e:
            return False, f"Error: {e}"

    def start_demo_realm(self) -> dict:
        """
        Start a demo realm for the interactive walkthrough.

        Returns:
            Dict with success status and port/error
        """
        from ..realms.server import RealmServer

        if self.demo_realm_server and self.demo_realm_server.is_running():
            return {
                "success": True,
                "message": "Demo realm already running",
                "port": self.demo_realm_server.port,
            }

        try:
            self.demo_realm_server = RealmServer("demo_realm", self.project_path, lazy=True)
            if self.demo_realm_server.start():
                return {"success": True, "port": self.demo_realm_server.port}
            return {"success": False, "error": "Failed to start demo realm"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def stop_demo_realm(self) -> dict:
        """
        Stop the demo realm.

        Returns:
            Dict with success status
        """
        if self.demo_realm_server:
            self.demo_realm_server.stop()
            self.demo_realm_server = None
            return {"success": True}
        return {"success": True, "message": "No demo realm running"}

    def serve(self) -> None:
        """Start the observatory server."""
        observatory_instance = self

        class Handler(ObservatoryHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(observatory_instance, *args, **kwargs)

        server = HTTPServer((self.host, self.port), Handler)

        print("\n🔭 O.D.D. Observatory is online")
        print(f"📍 Dashboard: http://{self.host}:{self.port}")
        print("🌐 Monitoring service mesh...")
        print("\nPress Ctrl+C to shutdown\n")

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🔭 Observatory shutting down...\n")
            server.shutdown()

    def _get_html(self) -> str:
        """Generate the observatory HTML page."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔭 O.D.D. Observatory - Service Mesh Monitor</title>
    <link rel="stylesheet" href="/observatory.css">
    <script src="https://d3js.org/d3.v7.min.js"></script>
</head>
<body>
    <div class="observatory-container">
        <header class="observatory-header">
            <h1>🔭 O.D.D. Observatory</h1>
            <p class="subtitle">Real-time Service Mesh Monitor // Port 2077</p>
        </header>

        <main class="observatory-main">
            <div class="status-bar">
                <span id="liveIndicator" class="live-indicator">🔴 Connecting...</span>
                <button id="refreshBtn" class="refresh-btn">🔄 Refresh</button>
                <span id="nodeCount">Nodes: --</span>
                <span id="upCount">Up: --</span>
                <span id="downCount">Down: --</span>
                <span id="lastUpdate">Last update: --</span>
            </div>

            <div class="graph-container" id="meshGraph"></div>

            <div class="legend">
                <span class="legend-item"><span class="dot core"></span> Core</span>
                <span class="legend-item"><span class="dot realm-up"></span> Realm (Up)</span>
                <span class="legend-item"><span class="dot realm-down"></span> Realm (Down)</span>
                <span class="legend-item"><span class="dot service-up"></span> Service (Up)</span>
                <span class="legend-item"><span class="dot service-down"></span> Service (Down)</span>
            </div>

            <button id="demoBtn" class="demo-btn">🎬 Start Demo</button>
        </main>

        <!-- Demo overlay -->
        <div class="demo-overlay" id="demoOverlay">
            <div class="demo-modal">
                <div class="demo-step" id="demoStep">1</div>
                <h2 id="demoTitle">Welcome to O.D.D. Observatory</h2>
                <p id="demoText">Loading...</p>
                <div class="demo-actions">
                    <button id="demoPrev" class="demo-nav">← Back</button>
                    <button id="demoNext" class="demo-nav primary">Next →</button>
                </div>
                <button id="demoClose" class="demo-close">✕</button>
            </div>
        </div>

        <!-- Context menu for smite -->
        <div class="context-menu" id="contextMenu">
            <div class="menu-item smite" id="smiteBtn">⚡ SMITE</div>
            <div class="menu-item" id="openAdminBtn">📂 Open Admin</div>
        </div>
    </div>

    <script src="/observatory.js"></script>
</body>
</html>"""

    def _get_css(self) -> str:
        """Generate the observatory CSS."""
        return """
:root {
    --bg-dark: #050505;
    --bg-panel: #0a0a0a;
    --text-primary: #e0e0e0;
    --text-dim: #666;
    --neon-green: #2ea043;
    --neon-red: #f85149;
    --neon-blue: #58a6ff;
    --neon-purple: #a371f7;
    --glow-green: 0 0 10px #2ea043, 0 0 20px #2ea04366;
    --glow-red: 0 0 10px #f85149, 0 0 20px #f8514966;
    --glow-white: 0 0 15px #ffffff88;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background: var(--bg-dark);
    color: var(--text-primary);
    font-family: 'Courier New', monospace;
    min-height: 100vh;
}

.observatory-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    padding: 20px;
}

.observatory-header {
    text-align: center;
    padding: 20px 0;
    border-bottom: 1px solid #222;
}

.observatory-header h1 {
    font-size: 2rem;
    color: var(--neon-blue);
    text-shadow: var(--glow-white);
}

.subtitle {
    color: var(--text-dim);
    margin-top: 5px;
}

.observatory-main {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 20px 0;
}

.status-bar {
    display: flex;
    justify-content: center;
    gap: 30px;
    padding: 10px;
    background: var(--bg-panel);
    border-radius: 8px;
    margin-bottom: 20px;
}

.status-bar span {
    color: var(--text-dim);
}

.live-indicator {
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    background: #1a0a0a;
    border: 1px solid #333;
}

.live-indicator.connected {
    background: #0a1a0a;
    border-color: var(--neon-green);
    color: var(--neon-green);
}

.refresh-btn {
    background: var(--bg-dark);
    border: 1px solid #333;
    color: var(--neon-blue);
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-family: inherit;
    font-size: 0.9rem;
    transition: all 0.2s;
}

.refresh-btn:hover {
    background: #111;
    border-color: var(--neon-blue);
    box-shadow: 0 0 10px var(--neon-blue);
}

.refresh-btn:active {
    transform: scale(0.95);
}

.graph-container {
    flex: 1;
    background: var(--bg-panel);
    border-radius: 8px;
    position: relative;
    overflow: hidden;
}

.legend {
    display: flex;
    justify-content: center;
    gap: 20px;
    padding: 15px;
    margin-top: 20px;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-dim);
    font-size: 0.85rem;
}

.dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
}

.dot.core {
    background: white;
    box-shadow: var(--glow-white);
}

.dot.realm-up {
    background: var(--neon-green);
    box-shadow: var(--glow-green);
}

.dot.realm-down {
    background: #330000;
    border: 1px solid var(--neon-red);
}

.dot.service-up {
    background: var(--neon-purple);
}

.dot.service-down {
    background: #1a0a20;
    border: 1px solid var(--neon-purple);
}

/* Context menu */
.context-menu {
    display: none;
    position: fixed;
    background: var(--bg-panel);
    border: 1px solid #333;
    border-radius: 8px;
    padding: 5px 0;
    z-index: 1000;
    min-width: 150px;
}

.context-menu.visible {
    display: block;
}

.menu-item {
    padding: 10px 20px;
    cursor: pointer;
    transition: background 0.2s;
}

.menu-item:hover {
    background: #1a1a1a;
}

.menu-item.smite {
    color: var(--neon-red);
}

.menu-item.smite:hover {
    background: #200000;
}

/* Demo button */
.demo-btn {
    position: fixed;
    bottom: 30px;
    right: 30px;
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border: 2px solid var(--neon-purple);
    color: var(--neon-purple);
    padding: 15px 25px;
    border-radius: 30px;
    cursor: pointer;
    font-family: inherit;
    font-size: 1rem;
    font-weight: bold;
    transition: all 0.3s;
    z-index: 100;
}

.demo-btn:hover {
    background: linear-gradient(135deg, #16213e, #1a1a2e);
    box-shadow: 0 0 20px var(--neon-purple);
    transform: scale(1.05);
}

/* Demo overlay */
.demo-overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.85);
    z-index: 1000;
    justify-content: center;
    align-items: center;
}

.demo-overlay.active {
    display: flex;
}

.demo-modal {
    background: linear-gradient(135deg, #0a0a0f, #111118);
    border: 1px solid #333;
    border-radius: 20px;
    padding: 40px;
    max-width: 600px;
    width: 90%;
    position: relative;
    box-shadow: 0 0 50px rgba(0, 0, 0, 0.5);
}

.demo-step {
    position: absolute;
    top: -20px;
    left: 50%;
    transform: translateX(-50%);
    background: var(--neon-purple);
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 1.2rem;
}

.demo-modal h2 {
    color: var(--neon-blue);
    margin-bottom: 20px;
    text-align: center;
}

.demo-modal p {
    color: var(--text-primary);
    line-height: 1.8;
    margin-bottom: 30px;
    text-align: center;
}

.demo-actions {
    display: flex;
    justify-content: center;
    gap: 15px;
}

.demo-nav {
    background: var(--bg-dark);
    border: 1px solid #444;
    color: var(--text-primary);
    padding: 12px 30px;
    border-radius: 8px;
    cursor: pointer;
    font-family: inherit;
    font-size: 1rem;
    transition: all 0.2s;
}

.demo-nav:hover {
    border-color: var(--neon-blue);
}

.demo-nav.primary {
    background: var(--neon-purple);
    border-color: var(--neon-purple);
    color: white;
}

.demo-nav.primary:hover {
    box-shadow: 0 0 15px var(--neon-purple);
}

.demo-nav:disabled {
    opacity: 0.3;
    cursor: not-allowed;
}

.demo-close {
    position: absolute;
    top: 15px;
    right: 15px;
    background: none;
    border: none;
    color: #666;
    font-size: 1.5rem;
    cursor: pointer;
    transition: color 0.2s;
}

.demo-close:hover {
    color: var(--neon-red);
}

.demo-highlight {
    animation: pulse-highlight 2s infinite;
}

@keyframes pulse-highlight {
    0%, 100% { box-shadow: 0 0 0 0 rgba(163, 113, 247, 0.4); }
    50% { box-shadow: 0 0 0 20px rgba(163, 113, 247, 0); }
}

/* D3 node styles */
.node-label {
    font-size: 11px;
    fill: var(--text-primary);
    text-anchor: middle;
    pointer-events: none;
}

.link {
    stroke: #333;
    stroke-width: 1.5px;
}
"""

    def _get_js(self) -> str:
        """Generate the observatory JavaScript."""
        return """
const API_BASE = '';
let meshData = null;
let selectedNode = null;
let simulation = null;
let svg = null;
let nodeElements = null;
let linkElements = null;
let currentNodes = new Map(); // Track node positions

// Initialize
async function init() {
    setupGraph();
    await refreshMesh();
    connectEventStream();

    // Manual refresh button (for full topology reload)
    document.getElementById('refreshBtn').addEventListener('click', async () => {
        const btn = document.getElementById('refreshBtn');
        btn.textContent = '⏳ Loading...';
        btn.disabled = true;
        await refreshMesh();
        btn.textContent = '🔄 Refresh';
        btn.disabled = false;
    });
}

function connectEventStream() {
    const indicator = document.getElementById('liveIndicator');
    const eventSource = new EventSource('/api/events');

    eventSource.onopen = () => {
        indicator.textContent = '🟢 Live';
        indicator.classList.add('connected');
    };

    eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.type === 'status_update' && data.changes) {
            // Update only changed nodes (no rebuild, no bounce)
            updateNodeStatus(data.changes);
            updateStatusBar();
            document.getElementById('lastUpdate').textContent =
                `Last update: ${new Date().toLocaleTimeString()}`;
        }
    };

    eventSource.onerror = () => {
        indicator.textContent = '🔴 Reconnecting...';
        indicator.classList.remove('connected');
        eventSource.close();
        setTimeout(connectEventStream, 5000);
    };
}

function updateNodeStatus(changes) {
    if (!nodeElements) return;

    const changeMap = new Map(changes.map(c => [c.id, c.status]));

    nodeElements.each(function(d) {
        const newStatus = changeMap.get(d.id);
        if (newStatus !== undefined && newStatus !== d.status) {
            d.status = newStatus;
            // Smooth color transition
            d3.select(this).select('circle')
                .transition()
                .duration(500)
                .attr('fill', getNodeColor(d))
                .attr('stroke', getNodeStroke(d))
                .style('filter', getNodeGlow(d));
        }
    });

    // Update meshData for status bar
    if (meshData) {
        changes.forEach(c => {
            const node = meshData.nodes.find(n => n.id === c.id);
            if (node) node.status = c.status;
        });
    }
}

function setupGraph() {
    const container = document.getElementById('meshGraph');
    const width = container.clientWidth;
    const height = container.clientHeight;

    svg = d3.select('#meshGraph')
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    // Add zoom behavior
    const g = svg.append('g');
    svg.call(d3.zoom()
        .scaleExtent([0.3, 3])
        .on('zoom', (event) => g.attr('transform', event.transform)));

    // Store reference
    svg.mainGroup = g;

    // Create layer groups (links below nodes)
    g.append('g').attr('class', 'links-layer');
    g.append('g').attr('class', 'nodes-layer');
}

async function refreshMesh() {
    try {
        const response = await fetch(`${API_BASE}/api/mesh`);
        const newData = await response.json();

        // Check if topology changed (nodes added/removed)
        const topologyChanged = hasTopologyChanged(newData);

        meshData = newData;
        updateStatusBar();

        if (topologyChanged || !simulation) {
            // Full rebuild only if topology changed
            rebuildGraph();
        } else {
            // Just update node styles (no bounce)
            updateNodeStyles();
        }
    } catch (error) {
        console.error('Error fetching mesh:', error);
    }
}

function hasTopologyChanged(newData) {
    if (!meshData) return true;

    const oldIds = new Set(meshData.nodes.map(n => n.id));
    const newIds = new Set(newData.nodes.map(n => n.id));

    if (oldIds.size !== newIds.size) return true;
    for (const id of oldIds) {
        if (!newIds.has(id)) return true;
    }
    return false;
}

function updateStatusBar() {
    if (!meshData) return;

    const nodes = meshData.nodes;
    const upCount = nodes.filter(n => n.status === 'up').length;
    const downCount = nodes.filter(n => n.status === 'down').length;

    document.getElementById('nodeCount').textContent = `Nodes: ${nodes.length}`;
    document.getElementById('upCount').textContent = `Up: ${upCount}`;
    document.getElementById('downCount').textContent = `Down: ${downCount}`;
    document.getElementById('lastUpdate').textContent = `Last update: ${new Date().toLocaleTimeString()}`;
}

function updateNodeStyles() {
    // Update existing node colors/styles without touching positions
    if (!nodeElements) return;

    const statusMap = new Map(meshData.nodes.map(n => [n.id, n.status]));

    nodeElements.each(function(d) {
        const newStatus = statusMap.get(d.id);
        if (newStatus !== undefined) {
            d.status = newStatus;
            d3.select(this).select('circle')
                .transition()
                .duration(300)
                .attr('fill', getNodeColor(d))
                .attr('stroke', getNodeStroke(d))
                .style('filter', getNodeGlow(d));
        }
    });
}

function rebuildGraph() {
    if (!meshData || !svg) return;

    const g = svg.mainGroup;
    const container = document.getElementById('meshGraph');
    const width = container.clientWidth;
    const height = container.clientHeight;

    // Preserve existing positions
    const oldPositions = new Map();
    if (nodeElements) {
        nodeElements.each(d => {
            oldPositions.set(d.id, { x: d.x, y: d.y, vx: d.vx, vy: d.vy });
        });
    }

    // Apply old positions to new nodes
    meshData.nodes.forEach(node => {
        const old = oldPositions.get(node.id);
        if (old) {
            node.x = old.x;
            node.y = old.y;
            node.vx = old.vx || 0;
            node.vy = old.vy || 0;
        }
    });

    // Clear existing
    g.select('.links-layer').selectAll('*').remove();
    g.select('.nodes-layer').selectAll('*').remove();

    // Stop old simulation
    if (simulation) simulation.stop();

    // Create force simulation
    simulation = d3.forceSimulation(meshData.nodes)
        .force('link', d3.forceLink(meshData.links).id(d => d.id).distance(120))
        .force('charge', d3.forceManyBody().strength(-400))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide().radius(50))
        .alphaDecay(0.05); // Slower decay for smoother settling

    // If we had old positions, start with low alpha
    if (oldPositions.size > 0) {
        simulation.alpha(0.1);
    }

    // Draw links
    linkElements = g.select('.links-layer')
        .selectAll('line')
        .data(meshData.links)
        .enter()
        .append('line')
        .attr('class', 'link');

    // Draw nodes
    nodeElements = g.select('.nodes-layer')
        .selectAll('g')
        .data(meshData.nodes)
        .enter()
        .append('g')
        .attr('class', 'node')
        .call(d3.drag()
            .on('start', dragStarted)
            .on('drag', dragged)
            .on('end', dragEnded))
        .on('click', (event, d) => handleNodeClick(event, d))
        .on('contextmenu', (event, d) => handleContextMenu(event, d));

    // Node circles
    nodeElements.append('circle')
        .attr('r', d => d.type === 'core' ? 25 : 18)
        .attr('fill', d => getNodeColor(d))
        .attr('stroke', d => getNodeStroke(d))
        .attr('stroke-width', 2)
        .style('filter', d => getNodeGlow(d))
        .style('cursor', 'pointer');

    // Node labels
    nodeElements.append('text')
        .attr('class', 'node-label')
        .attr('dy', d => d.type === 'core' ? 40 : 32)
        .text(d => d.name);

    // Port labels
    nodeElements.filter(d => d.port)
        .append('text')
        .attr('class', 'node-label')
        .attr('dy', d => d.type === 'core' ? 52 : 44)
        .style('fill', '#666')
        .style('font-size', '9px')
        .text(d => `:${d.port}`);

    // Simulation tick
    simulation.on('tick', () => {
        linkElements
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);

        nodeElements.attr('transform', d => `translate(${d.x},${d.y})`);
    });
}

function getNodeColor(d) {
    if (d.type === 'core') return '#ffffff';
    if (d.status === 'up') {
        return d.type === 'realm' ? '#2ea043' : '#a371f7';
    }
    return d.type === 'realm' ? '#330000' : '#1a0a20';
}

function getNodeStroke(d) {
    if (d.type === 'core') return '#ffffff';
    if (d.status === 'down') {
        return d.type === 'realm' ? '#f85149' : '#a371f7';
    }
    return 'none';
}

function getNodeGlow(d) {
    if (d.type === 'core') return 'drop-shadow(0 0 8px #fff)';
    if (d.status === 'up') {
        return d.type === 'realm'
            ? 'drop-shadow(0 0 8px #2ea043)'
            : 'drop-shadow(0 0 8px #a371f7)';
    }
    return 'none';
}

function dragStarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
}

function dragEnded(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}

function handleNodeClick(event, d) {
    if (d.port && d.type === 'realm') {
        window.open(`http://localhost:${d.port}/_/`, '_blank');
    }
}

function handleContextMenu(event, d) {
    event.preventDefault();
    if (!d.port || d.type === 'core') return;

    selectedNode = d;
    const menu = document.getElementById('contextMenu');
    menu.style.left = `${event.clientX}px`;
    menu.style.top = `${event.clientY}px`;
    menu.classList.add('visible');
}

// Context menu actions
document.getElementById('smiteBtn').addEventListener('click', async () => {
    if (!selectedNode || !selectedNode.port) return;

    const confirmed = confirm(`SMITE ${selectedNode.name} on port ${selectedNode.port}?`);
    if (!confirmed) return;

    try {
        const response = await fetch(`${API_BASE}/api/smite`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ port: selectedNode.port })
        });
        const result = await response.json();
        alert(result.message);
        await refreshMesh();
    } catch (error) {
        alert('Error: ' + error.message);
    }

    hideContextMenu();
});

document.getElementById('openAdminBtn').addEventListener('click', () => {
    if (selectedNode && selectedNode.port) {
        window.open(`http://localhost:${selectedNode.port}/_/`, '_blank');
    }
    hideContextMenu();
});

function hideContextMenu() {
    document.getElementById('contextMenu').classList.remove('visible');
    selectedNode = null;
}

// Hide context menu on click elsewhere
document.addEventListener('click', (e) => {
    if (!e.target.closest('.context-menu')) {
        hideContextMenu();
    }
});

// Handle window resize
window.addEventListener('resize', () => {
    if (meshData) updateGraph();
});

// ===== DEMO CONTROLLER =====
const DEMO_STEPS = [
    {
        title: "Welcome to O.D.D. Observatory",
        text: "This is your real-time service mesh monitor. Watch your Realms come alive as glowing nodes in a force-directed graph.",
        action: null
    },
    {
        title: "The Architect",
        text: "The white node at the center is the Architect - it represents the WAFT core orchestrator. It's always up. All Realms connect to it in a star topology.",
        action: "highlightArchitect"
    },
    {
        title: "Realm Nodes",
        text: "Green nodes are running PocketBase servers (Realms). Red/dark nodes are offline. The status updates in real-time via Server-Sent Events.",
        action: null
    },
    {
        title: "Starting Demo Realm",
        text: "Watch the graph - a new node called 'demo_realm' is about to appear on port 8095!",
        action: "startDemoRealm"
    },
    {
        title: "Realm is Live!",
        text: "The demo_realm node appeared in green. It's a real PocketBase server! You can click it to open the admin panel.",
        action: "highlightDemoRealm"
    },
    {
        title: "Try SMITE",
        text: "Right-click the demo_realm node and select '⚡ SMITE' to terminate it. Watch it turn red as the process dies.",
        action: "waitForSmite"
    },
    {
        title: "Demo Complete!",
        text: "You've seen how the Observatory monitors your service mesh in real-time. Use 'waft observatory' to launch it anytime.",
        action: "cleanup"
    }
];

let demoStep = 0;
let demoActive = false;
let waitingForSmite = false;

function startDemo() {
    demoStep = 0;
    demoActive = true;
    waitingForSmite = false;
    document.getElementById('demoOverlay').classList.add('active');
    updateDemoUI();
}

function closeDemo() {
    demoActive = false;
    waitingForSmite = false;
    document.getElementById('demoOverlay').classList.remove('active');
    clearHighlights();
    // Cleanup demo realm if running
    fetch('/api/demo/stop-realm', { method: 'POST' }).catch(() => {});
}

function nextStep() {
    if (waitingForSmite) return; // Can't advance while waiting
    if (demoStep < DEMO_STEPS.length - 1) {
        demoStep++;
        updateDemoUI();
        executeStepAction(DEMO_STEPS[demoStep].action);
    } else {
        closeDemo();
    }
}

function prevStep() {
    if (waitingForSmite) return;
    if (demoStep > 0) {
        demoStep--;
        updateDemoUI();
        clearHighlights();
    }
}

function updateDemoUI() {
    const step = DEMO_STEPS[demoStep];
    document.getElementById('demoStep').textContent = demoStep + 1;
    document.getElementById('demoTitle').textContent = step.title;
    document.getElementById('demoText').textContent = step.text;

    // Update button states
    document.getElementById('demoPrev').disabled = demoStep === 0;
    const nextBtn = document.getElementById('demoNext');
    if (demoStep === DEMO_STEPS.length - 1) {
        nextBtn.textContent = 'Finish ✓';
    } else if (waitingForSmite) {
        nextBtn.textContent = 'Waiting...';
        nextBtn.disabled = true;
    } else {
        nextBtn.textContent = 'Next →';
        nextBtn.disabled = false;
    }
}

async function executeStepAction(action) {
    if (!action) return;

    switch (action) {
        case 'highlightArchitect':
            highlightNode('architect');
            break;

        case 'startDemoRealm':
            document.getElementById('demoNext').disabled = true;
            document.getElementById('demoNext').textContent = 'Starting...';
            try {
                const response = await fetch('/api/demo/start-realm', { method: 'POST' });
                const result = await response.json();
                if (result.success) {
                    // Wait for graph to update (SSE will push the change)
                    setTimeout(() => {
                        document.getElementById('demoNext').disabled = false;
                        document.getElementById('demoNext').textContent = 'Next →';
                    }, 3000);
                } else {
                    document.getElementById('demoText').textContent = 'Failed to start demo realm: ' + (result.error || 'Unknown error');
                    document.getElementById('demoNext').disabled = false;
                    document.getElementById('demoNext').textContent = 'Skip →';
                }
            } catch (e) {
                document.getElementById('demoText').textContent = 'Error starting realm: ' + e.message;
                document.getElementById('demoNext').disabled = false;
            }
            break;

        case 'highlightDemoRealm':
            highlightNode('demo_realm');
            break;

        case 'waitForSmite':
            waitingForSmite = true;
            updateDemoUI();
            // Watch for demo_realm status change
            const checkSmite = setInterval(() => {
                if (meshData) {
                    const demoNode = meshData.nodes.find(n => n.id === 'demo_realm');
                    if (!demoNode || demoNode.status === 'down') {
                        clearInterval(checkSmite);
                        waitingForSmite = false;
                        demoStep++;
                        updateDemoUI();
                    }
                }
            }, 500);
            break;

        case 'cleanup':
            fetch('/api/demo/stop-realm', { method: 'POST' }).catch(() => {});
            clearHighlights();
            break;
    }
}

function highlightNode(nodeId) {
    clearHighlights();
    if (!nodeElements) return;

    nodeElements.each(function(d) {
        if (d.id === nodeId) {
            d3.select(this).select('circle')
                .classed('demo-highlight', true)
                .style('animation', 'pulse-highlight 1.5s infinite');
        }
    });
}

function clearHighlights() {
    if (!nodeElements) return;
    nodeElements.selectAll('circle')
        .classed('demo-highlight', false)
        .style('animation', null);
}

// Demo button and modal event listeners
document.getElementById('demoBtn').addEventListener('click', startDemo);
document.getElementById('demoNext').addEventListener('click', nextStep);
document.getElementById('demoPrev').addEventListener('click', prevStep);
document.getElementById('demoClose').addEventListener('click', closeDemo);

// Allow ESC to close demo
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && demoActive) {
        closeDemo();
    }
});

// Initialize
init();
"""
