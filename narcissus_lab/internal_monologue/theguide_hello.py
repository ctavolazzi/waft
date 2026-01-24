#!/usr/bin/env python3
"""
TheGuide Web Interface with Console Goblin

The 3-Body Problem Solution:
- Mind: TheOracle (reasoning)
- Body: NarcissusAgent (action)
- Spirit: TheGuide (conscience)

Features:
- WebSocket for reactive updates (NO POLLING)
- Console Goblin for real-time logging
- File watching with debounced reload
"""

import sys
import json
import asyncio
import hashlib
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread, Lock
from queue import Queue
import webbrowser

# Add waft root to path
waft_root = Path(__file__).resolve().parents[2]
if str(waft_root) not in sys.path:
    sys.path.insert(0, str(waft_root))
if str(waft_root / "src") not in sys.path:
    sys.path.insert(0, str(waft_root / "src"))

from waft.pantheon.guide import TheGuide


# =============================================================================
# Console Goblin - Reactive Log System
# =============================================================================

class ConsoleGoblin:
    """
    The Console Goblin collects and broadcasts logs reactively.
    No polling - events are pushed when they happen.
    """
    
    def __init__(self, max_logs: int = 100):
        self.logs = []
        self.max_logs = max_logs
        self.subscribers = []
        self.lock = Lock()
        self._log_id = 0
    
    def log(self, message: str, level: str = "info", source: str = "system"):
        """Add a log entry and notify all subscribers."""
        with self.lock:
            self._log_id += 1
            entry = {
                "id": self._log_id,
                "timestamp": datetime.now().isoformat(),
                "message": message,
                "level": level,  # info, success, warning, error, active
                "source": source,
            }
            self.logs.append(entry)
            
            # Trim old logs
            if len(self.logs) > self.max_logs:
                self.logs = self.logs[-self.max_logs:]
            
            # Notify subscribers (reactive push)
            self._notify({"type": "log", "entry": entry})
    
    def subscribe(self, callback):
        """Subscribe to log events."""
        with self.lock:
            self.subscribers.append(callback)
    
    def unsubscribe(self, callback):
        """Unsubscribe from log events."""
        with self.lock:
            if callback in self.subscribers:
                self.subscribers.remove(callback)
    
    def _notify(self, event):
        """Notify all subscribers of an event."""
        for callback in self.subscribers[:]:
            try:
                callback(event)
            except Exception:
                pass
    
    def get_recent(self, count: int = 20):
        """Get recent logs."""
        with self.lock:
            return self.logs[-count:]
    
    def broadcast(self, event_type: str, data: dict):
        """Broadcast a custom event to all subscribers."""
        self._notify({"type": event_type, **data})


# Global console goblin instance
goblin = ConsoleGoblin()


# =============================================================================
# File Watcher - Reactive (No Polling)
# =============================================================================

class FileWatcher:
    """
    Watches files for changes using mtime comparison.
    Debounces rapid changes (e.g., during save).
    """
    
    def __init__(self, goblin: ConsoleGoblin, debounce_seconds: float = 0.5):
        self.goblin = goblin
        self.debounce_seconds = debounce_seconds
        self.watched_files = {}  # path -> (mtime, hash)
        self.lock = Lock()
        self._running = False
        self._thread = None
        self._pending_reload = False
        self._last_change_time = 0
    
    def watch(self, filepath: Path):
        """Add a file to watch."""
        with self.lock:
            if filepath.exists():
                stat = filepath.stat()
                self.watched_files[str(filepath)] = {
                    "mtime": stat.st_mtime,
                    "hash": self._hash_file(filepath),
                    "path": filepath,
                }
                self.goblin.log(f"Watching: {filepath.name}", "info", "watcher")
    
    def _hash_file(self, filepath: Path) -> str:
        """Get file hash."""
        try:
            return hashlib.md5(filepath.read_bytes()).hexdigest()
        except Exception:
            return ""
    
    def check_changes(self) -> bool:
        """Check for file changes. Returns True if any file changed."""
        changed = False
        with self.lock:
            for path_str, info in self.watched_files.items():
                filepath = info["path"]
                if not filepath.exists():
                    continue
                
                stat = filepath.stat()
                current_mtime = stat.st_mtime
                
                # Only check hash if mtime changed (efficient)
                if current_mtime != info["mtime"]:
                    current_hash = self._hash_file(filepath)
                    if current_hash != info["hash"]:
                        changed = True
                        info["mtime"] = current_mtime
                        info["hash"] = current_hash
                        self.goblin.log(f"File changed: {filepath.name}", "warning", "watcher")
        
        return changed
    
    def start(self, check_interval: float = 0.3):
        """Start watching in background thread."""
        if self._running:
            return
        
        self._running = True
        
        def watch_loop():
            while self._running:
                if self.check_changes():
                    # Debounce: wait for writes to settle
                    self._last_change_time = time.time()
                    self._pending_reload = True
                
                # Check if debounce period passed
                if self._pending_reload:
                    if time.time() - self._last_change_time >= self.debounce_seconds:
                        self._pending_reload = False
                        self.goblin.broadcast("reload", {"reason": "file_changed"})
                        self.goblin.log("Triggering reload...", "active", "watcher")
                
                time.sleep(check_interval)
        
        self._thread = Thread(target=watch_loop, daemon=True)
        self._thread.start()
    
    def stop(self):
        """Stop watching."""
        self._running = False


# =============================================================================
# SSE (Server-Sent Events) for Reactive Updates
# =============================================================================

class SSEManager:
    """
    Manages Server-Sent Events connections for reactive updates.
    This is simpler than WebSocket and doesn't require external deps.
    """
    
    def __init__(self, goblin: ConsoleGoblin):
        self.goblin = goblin
        self.event_queue = Queue()
        
        # Subscribe to goblin events
        self.goblin.subscribe(self._on_event)
    
    def _on_event(self, event):
        """Handle events from goblin."""
        self.event_queue.put(event)
    
    def format_sse(self, event_type: str, data: dict) -> str:
        """Format as SSE message."""
        json_data = json.dumps(data)
        return f"event: {event_type}\ndata: {json_data}\n\n"


# =============================================================================
# HTTP Handler
# =============================================================================

class TheGuideHandler(BaseHTTPRequestHandler):
    """HTTP handler for TheGuide web interface with SSE support."""
    
    guide = None
    goblin = None
    watcher = None
    sse_manager = None

    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/" or self.path == "/index.html":
            self.serve_dashboard()
        elif self.path == "/api/guide/status":
            self.serve_status()
        elif self.path == "/api/logs":
            self.serve_logs()
        elif self.path == "/events":
            self.serve_sse()
        else:
            self.send_error(404, "Not Found")
    
    def serve_sse(self):
        """Serve Server-Sent Events stream for reactive updates."""
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        
        # Send initial connection event
        self.wfile.write(b"event: connected\ndata: {\"status\": \"ok\"}\n\n")
        self.wfile.flush()
        
        # Send recent logs
        for log in self.goblin.get_recent(20):
            msg = f"event: log\ndata: {json.dumps(log)}\n\n"
            self.wfile.write(msg.encode())
        self.wfile.flush()
        
        self.goblin.log("Client connected to event stream", "success", "sse")
        
        # Stream events reactively
        try:
            while True:
                try:
                    # Block until event available (no polling!)
                    event = self.sse_manager.event_queue.get(timeout=30)
                    event_type = event.get("type", "message")
                    msg = f"event: {event_type}\ndata: {json.dumps(event)}\n\n"
                    self.wfile.write(msg.encode())
                    self.wfile.flush()
                except Exception:
                    # Send keepalive
                    self.wfile.write(b": keepalive\n\n")
                    self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            self.goblin.log("Client disconnected", "info", "sse")
    
    def serve_logs(self):
        """Serve recent logs as JSON."""
        logs = self.goblin.get_recent(50)
        response = json.dumps({"logs": logs})
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response.encode())))
        self.end_headers()
        self.wfile.write(response.encode())
    
    def serve_status(self):
        """Serve TheGuide status as JSON."""
        status = {
            "active": True,
            "project_path": str(self.guide.project_path),
            "pantheon_path": str(self.guide.pantheon_path),
            "guide_path": str(self.guide.guide_path),
            "sessions_count": len(self.guide.index.get("sessions", [])),
        }
        
        response = json.dumps(status, indent=2)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response.encode())))
        self.end_headers()
        self.wfile.write(response.encode())
    
    def serve_dashboard(self):
        """Serve the dashboard with reactive SSE (no polling)."""
        static_html_path = Path(__file__).parent / "guide_dashboard.html"
        
        if static_html_path.exists():
            html = static_html_path.read_text(encoding="utf-8")
            # Inject reactive script before </body>
            if "</body>" in html:
                html = html.replace("</body>", self._get_reactive_script() + "</body>")
        else:
            html = self._get_fallback_html()
        
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html.encode())))
        self.end_headers()
        self.wfile.write(html.encode())
    
    def _get_reactive_script(self):
        """Get the reactive SSE script (NO POLLING)."""
        return """
    <script>
        // ========================================
        // CONSOLE GOBLIN - Reactive Event System
        // ========================================
        const ConsoleGoblin = {
            logs: [],
            maxLogs: 100,
            listeners: [],
            
            init() {
                this.connectSSE();
                console.log('%c🧙 Console Goblin Awakened', 'color: #00ff9d; font-weight: bold');
            },
            
            connectSSE() {
                const eventSource = new EventSource('/events');
                
                eventSource.onopen = () => {
                    this.log('🔗 Connected to server', 'success');
                };
                
                eventSource.addEventListener('log', (e) => {
                    const entry = JSON.parse(e.data);
                    if (entry.entry) {
                        this.addLog(entry.entry);
                    } else {
                        this.addLog(entry);
                    }
                });
                
                eventSource.addEventListener('reload', (e) => {
                    this.log('🔄 Reloading...', 'warning');
                    setTimeout(() => location.reload(), 100);
                });
                
                eventSource.addEventListener('fvcu', (e) => {
                    const data = JSON.parse(e.data);
                    this.updateFVCU(data);
                });
                
                eventSource.onerror = () => {
                    this.log('⚠️ Connection lost, reconnecting...', 'warning');
                };
            },
            
            addLog(entry) {
                this.logs.push(entry);
                if (this.logs.length > this.maxLogs) {
                    this.logs = this.logs.slice(-this.maxLogs);
                }
                this.render();
            },
            
            log(message, level = 'info') {
                this.addLog({
                    id: Date.now(),
                    timestamp: new Date().toISOString(),
                    message,
                    level,
                    source: 'client'
                });
            },
            
            render() {
                const logsEl = document.getElementById('logs');
                if (!logsEl) return;
                
                logsEl.innerHTML = this.logs.slice(-20).map(entry => {
                    const levelClass = entry.level || 'info';
                    const time = new Date(entry.timestamp).toLocaleTimeString();
                    const source = entry.source ? `[${entry.source}]` : '';
                    return `<div class="log-entry ${levelClass}"><span class="log-time">${time}</span> ${source} ${entry.message}</div>`;
                }).join('');
                
                // Auto-scroll to bottom
                logsEl.scrollTop = logsEl.scrollHeight;
            },
            
            updateFVCU(data) {
                // Update FVCU display when data arrives
                const metrics = ['factuality', 'validity', 'coherence', 'utility', 'faithfulness'];
                metrics.forEach(m => {
                    const el = document.querySelector(`[data-metric="${m}"]`);
                    if (el && data[m] !== undefined) {
                        const value = data[m];
                        el.querySelector('.fvcu-value').textContent = value.toFixed(2);
                        el.querySelector('.bar-fg').style.width = `${value * 100}%`;
                    }
                });
            }
        };
        
        // Initialize on load
        document.addEventListener('DOMContentLoaded', () => ConsoleGoblin.init());
        
        // Also init if already loaded
        if (document.readyState !== 'loading') ConsoleGoblin.init();
    </script>
    <style>
        #logs { max-height: calc(100vh - 200px); overflow-y: auto; }
        .log-entry { padding: 4px 0; border-bottom: 1px solid #222; font-size: 0.75rem; }
        .log-time { color: #555; margin-right: 8px; }
        .log-entry.success { color: #00ff9d; }
        .log-entry.warning { color: #ffaa00; }
        .log-entry.error { color: #ff0055; }
        .log-entry.active { color: #0099ff; }
        .log-entry.info { color: #888; }
    </style>
"""
    
    def _get_fallback_html(self):
        """Fallback HTML with Console Goblin."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TheGuide | Console Goblin</title>
    <style>
        :root { --bg: #0a0a0a; --text: #e0e0e0; --accent: #00ff9d; --panel: #1a1a1a; --danger: #ff0055; --warning: #ffaa00; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: var(--bg); color: var(--text); font-family: 'Courier New', monospace; display: grid; grid-template-rows: 60px 1fr; height: 100vh; overflow: hidden; }
        header { border-bottom: 1px solid #333; display: flex; align-items: center; padding: 0 20px; justify-content: space-between; background: var(--panel); }
        h1 { font-size: 1.2rem; text-transform: uppercase; letter-spacing: 2px; color: var(--accent); }
        .status { font-size: 0.8rem; color: #666; }
        main { display: grid; grid-template-columns: 350px 1fr 300px; gap: 1px; background: #333; }
        .panel { background: var(--panel); padding: 20px; overflow-y: auto; }
        .panel h3 { color: var(--accent); margin-bottom: 15px; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #333; padding-bottom: 5px; }
        .center-stage { background: #000; display: flex; justify-content: center; align-items: center; }
        canvas { border: 1px solid #333; box-shadow: 0 0 20px rgba(0,255,157,0.1); }
        #logs { font-size: 0.7rem; line-height: 1.6; max-height: calc(100vh - 150px); overflow-y: auto; }
        .log-entry { padding: 4px 0; border-bottom: 1px solid #222; }
        .log-time { color: #555; margin-right: 8px; }
        .log-entry.success { color: #00ff9d; }
        .log-entry.warning { color: #ffaa00; }
        .log-entry.error { color: #ff0055; }
        .log-entry.active { color: #0099ff; }
        .fvcu-grid { display: grid; gap: 10px; }
        .fvcu-item { padding: 8px; background: #222; border-radius: 4px; border-left: 3px solid var(--accent); }
        .fvcu-label { font-size: 0.7rem; color: #888; margin-bottom: 3px; }
        .fvcu-value { font-size: 0.9rem; color: var(--accent); font-weight: bold; }
        .bar-bg { background: #222; height: 6px; width: 100%; border-radius: 3px; overflow: hidden; margin-top: 5px; }
        .bar-fg { background: var(--accent); height: 100%; transition: width 0.3s; border-radius: 3px; }
        .bar-fg.danger { background: var(--danger); }
    </style>
</head>
<body>
    <header>
        <h1>🧙 Console Goblin <span style="font-size:0.5em; opacity:0.5;">// REACTIVE EVENT STREAM</span></h1>
        <div class="status">SYSTEM: ONLINE | PORT: 7072 | MODE: SSE (NO POLLING)</div>
    </header>
    <main>
        <div class="panel">
            <h3>🧙 GOBLIN LOG STREAM</h3>
            <div id="logs"></div>
        </div>
        <div class="center-stage">
            <canvas id="threeBody" width="600" height="400"></canvas>
        </div>
        <div class="panel">
            <h3>FVCU ANALYSIS</h3>
            <div class="fvcu-grid">
                <div class="fvcu-item" data-metric="factuality"><div class="fvcu-label">FACTUALITY</div><div class="fvcu-value">--</div><div class="bar-bg"><div class="bar-fg" style="width: 0%"></div></div></div>
                <div class="fvcu-item" data-metric="validity"><div class="fvcu-label">VALIDITY</div><div class="fvcu-value">--</div><div class="bar-bg"><div class="bar-fg" style="width: 0%"></div></div></div>
                <div class="fvcu-item" data-metric="coherence"><div class="fvcu-label">COHERENCE</div><div class="fvcu-value">--</div><div class="bar-bg"><div class="bar-fg" style="width: 0%"></div></div></div>
                <div class="fvcu-item" data-metric="utility"><div class="fvcu-label">UTILITY</div><div class="fvcu-value">--</div><div class="bar-bg"><div class="bar-fg" style="width: 0%"></div></div></div>
                <div class="fvcu-item" data-metric="faithfulness"><div class="fvcu-label">FAITHFULNESS</div><div class="fvcu-value">--</div><div class="bar-bg"><div class="bar-fg" style="width: 0%"></div></div></div>
            </div>
        </div>
    </main>
    <script>
        // 3-Body Animation
        const canvas = document.getElementById('threeBody');
        const ctx = canvas.getContext('2d');
        let t = 0;
        function draw() {
            ctx.fillStyle = 'rgba(0,0,0,0.1)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            t += 0.05;
            const cx = canvas.width / 2, cy = canvas.height / 2;
            
            // Mind (Red)
            ctx.fillStyle = '#ff0055';
            ctx.beginPath();
            ctx.arc(cx + Math.cos(t) * 100, cy + Math.sin(t * 1.3) * 80, 8, 0, Math.PI * 2);
            ctx.fill();
            
            // Body (Green)
            ctx.fillStyle = '#00ff9d';
            ctx.beginPath();
            ctx.arc(cx + Math.cos(t + 2) * 150, cy + Math.sin(t * 0.8) * 150, 10, 0, Math.PI * 2);
            ctx.fill();
            
            // Spirit (Blue)
            ctx.fillStyle = '#0099ff';
            ctx.beginPath();
            ctx.arc(cx + Math.cos(t * 0.7 + 4) * 120, cy + Math.sin(t * 1.1) * 120, 6, 0, Math.PI * 2);
            ctx.fill();
            
            requestAnimationFrame(draw);
        }
        draw();
    </script>
""" + self._get_reactive_script() + """
</body>
</html>"""
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


# =============================================================================
# Main Server
# =============================================================================

def main():
    """Start TheGuide web server with Console Goblin."""
    port = 8008  # Homebase port
    
    # Initialize components
    project_path = waft_root
    guide = TheGuide(project_path=project_path)
    watcher = FileWatcher(goblin, debounce_seconds=0.5)
    sse_manager = SSEManager(goblin)
    
    # Inject into handler
    TheGuideHandler.guide = guide
    TheGuideHandler.goblin = goblin
    TheGuideHandler.watcher = watcher
    TheGuideHandler.sse_manager = sse_manager
    
    # Start watching files
    html_path = Path(__file__).parent / "guide_dashboard.html"
    watcher.watch(html_path)
    watcher.watch(Path(__file__))  # Watch server file too
    watcher.start()
    
    # Startup logs
    print("\n" + "=" * 55)
    print("🧙 TheGuide + Console Goblin")
    print("=" * 55)
    print(f"🧠 Mind: TheOracle (Reasoning)")
    print(f"🤖 Body: NarcissusAgent (Action)")
    print(f"✨ Spirit: TheGuide (Conscience)")
    print("-" * 55)
    print(f"🚀 Server: http://localhost:{port}")
    print(f"📡 Mode: SSE (Server-Sent Events) - NO POLLING")
    print(f"🔄 Reload: Reactive on file save (debounced)")
    print("=" * 55 + "\n")
    
    goblin.log("🧙 Console Goblin awakened", "success", "goblin")
    goblin.log(f"🏛️ Pantheon: {guide.pantheon_path}", "info", "system")
    goblin.log("🔌 SSE stream ready - reactive mode", "active", "sse")
    
    # Create server
    server = HTTPServer(("localhost", port), TheGuideHandler)
    
    # Open browser
    def open_browser():
        time.sleep(1)
        webbrowser.open(f"http://localhost:{port}")
    Thread(target=open_browser, daemon=True).start()
    
    goblin.log("🌐 Browser opening...", "info", "system")
    
    try:
        print("💡 Press Ctrl+C to stop\n")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
        watcher.stop()
        server.shutdown()
        print("✅ Server stopped")


if __name__ == "__main__":
    main()
