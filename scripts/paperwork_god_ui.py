#!/usr/bin/env python3
"""
Paperwork God Web UI
====================

Modern web interface for the Paperwork God system, including:
- Paperwork management
- Skurl (red tape obstacles)
- Realm creatures (Goblins & Ghouls)
- System statistics and visualization
"""

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.pantheon import PaperworkGod
from src.waft.pantheon.financial_documents import FinancialDocumentsManager


class PaperworkGodUIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Paperwork God UI."""

    def __init__(self, *args, **kwargs):
        self.paperwork_god = PaperworkGod()
        self.financial_manager = FinancialDocumentsManager()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        if path == "/" or path == "/index.html":
            self.serve_index()
        elif path == "/api/summary":
            self.serve_api_summary()
        elif path == "/api/paperwork":
            self.serve_api_paperwork(query)
        elif path == "/api/obstacles":
            self.serve_api_obstacles(query)
        elif path == "/api/creatures":
            self.serve_api_creatures()
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        """Handle POST requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/api/paperwork/register":
            self.handle_register_paperwork()
        elif path == "/api/obstacles/create":
            self.handle_create_obstacle()
        elif path == "/api/obstacles/resolve":
            self.handle_resolve_obstacle()
        else:
            self.send_error(404, "Not Found")

    def serve_index(self):
        """Serve main HTML page."""
        html = self.get_index_html()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def serve_api_summary(self):
        """Serve system summary API."""
        summary = self.paperwork_god.get_registry_summary()
        skurl_summary = self.paperwork_god.skurl.get_registry_summary()

        response = {
            "paperwork": {
                "total_documents": summary["total_documents"],
                "last_updated": summary["last_updated"],
            },
            "skurl": skurl_summary,
            "realm": summary["realm_creatures"],
        }

        self.send_json_response(response)

    def serve_api_paperwork(self, query):
        """Serve paperwork API."""
        if "id" in query:
            # Get specific paperwork
            doc_id = query["id"][0]
            record = self.paperwork_god.get_paperwork_record(doc_id)
            if record:
                self.send_json_response(record.to_dict())
            else:
                self.send_error(404, "Paperwork not found")
        else:
            # List all paperwork
            records = self.paperwork_god.list_all_paperwork()
            self.send_json_response([r.to_dict() for r in records])

    def serve_api_obstacles(self, query):
        """Serve obstacles API."""
        unresolved_only = query.get("unresolved", ["false"])[0].lower() == "true"
        obstacles = self.paperwork_god.skurl.list_all_obstacles(unresolved_only=unresolved_only)
        self.send_json_response([o.to_dict() for o in obstacles])

    def serve_api_creatures(self):
        """Serve creatures API."""
        realm = self.paperwork_god.realm
        goblins_path = realm.realm_path / "creatures" / "goblins"
        ghouls_path = realm.realm_path / "creatures" / "ghouls"

        goblins = []
        if goblins_path.exists():
            for goblin_file in goblins_path.glob("*.json"):
                goblins.append(json.loads(goblin_file.read_text(encoding="utf-8")))

        ghouls = []
        if ghouls_path.exists():
            for ghoul_file in ghouls_path.glob("*.json"):
                ghouls.append(json.loads(ghoul_file.read_text(encoding="utf-8")))

        self.send_json_response({"goblins": goblins, "ghouls": ghouls})

    def serve_api_budgets(self, query):
        """Serve budgets API."""
        if "id" in query:
            # Get specific budget
            budget_id = query["id"][0]
            budget = self.financial_manager.load_budget(budget_id)
            if budget:
                self.send_json_response(budget.to_dict())
            else:
                self.send_error(404, "Budget not found")
        else:
            # List all budgets
            budgets = self.financial_manager.list_budgets()
            self.send_json_response([b.to_dict() for b in budgets])

    def serve_api_balance_sheets(self, query):
        """Serve balance sheets API."""
        if "id" in query:
            # Get specific balance sheet
            bs_id = query["id"][0]
            bs = self.financial_manager.load_balance_sheet(bs_id)
            if bs:
                self.send_json_response(bs.to_dict())
            else:
                self.send_error(404, "Balance sheet not found")
        else:
            # List all balance sheets
            balance_sheets = self.financial_manager.list_balance_sheets()
            self.send_json_response([bs.to_dict() for bs in balance_sheets])

    def handle_register_paperwork(self):
        """Handle paperwork registration."""
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode("utf-8"))

        try:
            record = self.paperwork_god.register_paperwork(
                document_id=data["document_id"],
                document_path=Path(data["document_path"]),
                document_type=data.get("document_type", "form"),
                metadata=data.get("metadata", {}),
            )
            self.send_json_response(record.to_dict(), status=201)
        except Exception as e:
            self.send_error(400, str(e))

    def handle_create_obstacle(self):
        """Handle obstacle creation."""
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode("utf-8"))

        try:
            obstacle = self.paperwork_god.skurl.create_red_tape_obstacle(
                obstacle_id=data["obstacle_id"],
                description=data["description"],
                required_forms=data.get("required_forms", []),
                required_approvals=data.get("required_approvals", []),
                complexity_level=data.get("complexity_level", 1),
                metadata=data.get("metadata", {}),
            )
            self.send_json_response(obstacle.to_dict(), status=201)
        except Exception as e:
            self.send_error(400, str(e))

    def handle_resolve_obstacle(self):
        """Handle obstacle resolution."""
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode("utf-8"))

        obstacle = self.paperwork_god.skurl.resolve_obstacle(data["obstacle_id"])
        if obstacle:
            self.send_json_response(obstacle.to_dict())
        else:
            self.send_error(404, "Obstacle not found")

    def send_json_response(self, data, status=200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def get_index_html(self):
        """Generate main HTML page."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Paperwork God - Bureaucracy Management System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        header {
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .subtitle {
            color: #666;
            font-size: 1.1em;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }

        .stat-card:hover {
            transform: translateY(-5px);
        }

        .stat-card h3 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #333;
        }

        .content-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
        }

        .section {
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .section h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }

        .list-item {
            padding: 15px;
            margin-bottom: 10px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }

        .list-item h4 {
            color: #333;
            margin-bottom: 5px;
        }

        .list-item p {
            color: #666;
            font-size: 0.9em;
        }

        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
            margin-left: 10px;
        }

        .badge-pending {
            background: #ffc107;
            color: #333;
        }

        .badge-resolved {
            background: #28a745;
            color: white;
        }

        .badge-complexity {
            background: #dc3545;
            color: white;
        }

        .complexity-bar {
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            margin-top: 5px;
            overflow: hidden;
        }

        .complexity-fill {
            height: 100%;
            background: linear-gradient(90deg, #28a745, #ffc107, #dc3545);
            transition: width 0.3s;
        }

        .creature-item {
            display: flex;
            align-items: center;
            padding: 12px;
            margin-bottom: 8px;
            background: #f8f9fa;
            border-radius: 8px;
        }

        .creature-icon {
            font-size: 2em;
            margin-right: 15px;
        }

        .creature-info {
            flex: 1;
        }

        .creature-name {
            font-weight: bold;
            color: #333;
        }

        .creature-role {
            color: #666;
            font-size: 0.9em;
        }

        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: bold;
            transition: transform 0.2s;
        }

        button:hover {
            transform: scale(1.05);
        }

        button:active {
            transform: scale(0.95);
        }

        .loading {
            text-align: center;
            padding: 20px;
            color: #666;
        }

        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏛️ Paperwork God</h1>
            <p class="subtitle">Bureaucracy Management System • Realm of Bureaucracy</p>
        </header>

        <div class="stats-grid" id="stats-grid">
            <div class="stat-card">
                <h3>Documents</h3>
                <div class="stat-value" id="stat-documents">-</div>
            </div>
            <div class="stat-card">
                <h3>Red Tape Obstacles</h3>
                <div class="stat-value" id="stat-obstacles">-</div>
            </div>
            <div class="stat-card">
                <h3>Unresolved</h3>
                <div class="stat-value" id="stat-unresolved">-</div>
            </div>
            <div class="stat-card">
                <h3>Creatures</h3>
                <div class="stat-value" id="stat-creatures">-</div>
            </div>
        </div>

        <div class="content-grid">
            <div class="section">
                <h2>💰 Budgets</h2>
                <div id="budgets-list" class="loading">Loading...</div>
            </div>

            <div class="section">
                <h2>📊 Balance Sheets</h2>
                <div id="balance-sheets-list" class="loading">Loading...</div>
            </div>

            <div class="section">
                <h2>📄 Paperwork Registry</h2>
                <div id="paperwork-list" class="loading">Loading...</div>
            </div>

            <div class="section">
                <h2>👹 Skurl's Red Tape</h2>
                <div id="obstacles-list" class="loading">Loading...</div>
            </div>

            <div class="section">
                <h2>👹🧟 Realm Creatures</h2>
                <div id="creatures-list" class="loading">Loading...</div>
            </div>
        </div>
    </div>

    <script>
        async function fetchJSON(url) {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        }

        async function loadSummary() {
            try {
                const summary = await fetchJSON('/api/summary');

                document.getElementById('stat-documents').textContent = summary.paperwork.total_documents;
                document.getElementById('stat-obstacles').textContent = summary.skurl.total_obstacles;
                document.getElementById('stat-unresolved').textContent = summary.skurl.unresolved_obstacles;
                document.getElementById('stat-creatures').textContent = summary.realm.total_creatures;
            } catch (error) {
                console.error('Failed to load summary:', error);
            }
        }

        async function loadPaperwork() {
            try {
                const paperwork = await fetchJSON('/api/paperwork');
                const list = document.getElementById('paperwork-list');

                if (paperwork.length === 0) {
                    list.innerHTML = '<p style="color: #666; text-align: center;">No paperwork registered</p>';
                    return;
                }

                list.innerHTML = paperwork.map(doc => `
                    <div class="list-item">
                        <h4>${doc.document_id} <span class="badge badge-pending">${doc.status}</span></h4>
                        <p><strong>Type:</strong> ${doc.document_type}</p>
                        <p><strong>Path:</strong> ${doc.document_path}</p>
                        <p><strong>Created:</strong> ${new Date(doc.created_at).toLocaleString()}</p>
                    </div>
                `).join('');
            } catch (error) {
                document.getElementById('paperwork-list').innerHTML =
                    `<div class="error">Failed to load paperwork: ${error.message}</div>`;
            }
        }

        async function loadObstacles() {
            try {
                const obstacles = await fetchJSON('/api/obstacles?unresolved=false');
                const list = document.getElementById('obstacles-list');

                if (obstacles.length === 0) {
                    list.innerHTML = '<p style="color: #666; text-align: center;">No red tape obstacles</p>';
                    return;
                }

                list.innerHTML = obstacles.map(obs => {
                    const resolved = obs.resolved_at !== null;
                    const complexityPercent = (obs.complexity_level / 10) * 100;

                    return `
                        <div class="list-item">
                            <h4>${obs.obstacle_id}
                                <span class="badge ${resolved ? 'badge-resolved' : 'badge-pending'}">
                                    ${resolved ? 'Resolved' : 'Unresolved'}
                                </span>
                                <span class="badge badge-complexity">Complexity: ${obs.complexity_level}/10</span>
                            </h4>
                            <p>${obs.description}</p>
                            <div class="complexity-bar">
                                <div class="complexity-fill" style="width: ${complexityPercent}%"></div>
                            </div>
                            <p><strong>Required Forms:</strong> ${obs.required_forms.length}</p>
                            <p><strong>Required Approvals:</strong> ${obs.required_approvals.length}</p>
                            ${resolved ? `<p><strong>Resolved:</strong> ${new Date(obs.resolved_at).toLocaleString()}</p>` : ''}
                        </div>
                    `;
                }).join('');
            } catch (error) {
                document.getElementById('obstacles-list').innerHTML =
                    `<div class="error">Failed to load obstacles: ${error.message}</div>`;
            }
        }

        async function loadCreatures() {
            try {
                const creatures = await fetchJSON('/api/creatures');
                const list = document.getElementById('creatures-list');

                const allCreatures = [
                    ...creatures.goblins.map(c => ({...c, type: 'goblin', icon: '👹'})),
                    ...creatures.ghouls.map(c => ({...c, type: 'ghoul', icon: '🧟'}))
                ];

                if (allCreatures.length === 0) {
                    list.innerHTML = '<p style="color: #666; text-align: center;">No creatures in realm</p>';
                    return;
                }

                list.innerHTML = allCreatures.map(creature => `
                    <div class="creature-item">
                        <div class="creature-icon">${creature.icon}</div>
                        <div class="creature-info">
                            <div class="creature-name">${creature.name}</div>
                            <div class="creature-role">${creature.role} • ${creature.type}</div>
                        </div>
                    </div>
                `).join('');
            } catch (error) {
                document.getElementById('creatures-list').innerHTML =
                    `<div class="error">Failed to load creatures: ${error.message}</div>`;
            }
        }

        async function loadBudgets() {
            try {
                const budgets = await fetchJSON('/api/budgets');
                const list = document.getElementById('budgets-list');

                if (budgets.length === 0) {
                    list.innerHTML = '<p style="color: #666; text-align: center;">No budgets available</p>';
                    return;
                }

                list.innerHTML = budgets.map(budget => {
                    const variance = parseFloat(budget.totals.variance);
                    const variancePercent = budget.totals.variance_percent;
                    const varianceColor = variance < 0 ? '#28a745' : variance > 0 ? '#dc3545' : '#666';

                    return `
                        <div class="list-item">
                            <h4>${budget.name}</h4>
                            <p><strong>Period:</strong> ${new Date(budget.period_start).toLocaleDateString()} - ${new Date(budget.period_end).toLocaleDateString()}</p>
                            <p><strong>Budgeted:</strong> $${parseFloat(budget.totals.budgeted).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</p>
                            <p><strong>Actual:</strong> $${parseFloat(budget.totals.actual).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</p>
                            <p style="color: ${varianceColor};"><strong>Variance:</strong> $${Math.abs(variance).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})} (${Math.abs(variancePercent).toFixed(1)}%)</p>
                            <p><strong>Items:</strong> ${budget.items.length} line items</p>
                        </div>
                    `;
                }).join('');
            } catch (error) {
                document.getElementById('budgets-list').innerHTML =
                    `<div class="error">Failed to load budgets: ${error.message}</div>`;
            }
        }

        async function loadBalanceSheets() {
            try {
                const balanceSheets = await fetchJSON('/api/balance_sheets');
                const list = document.getElementById('balance-sheets-list');

                if (balanceSheets.length === 0) {
                    list.innerHTML = '<p style="color: #666; text-align: center;">No balance sheets available</p>';
                    return;
                }

                list.innerHTML = balanceSheets.map(bs => {
                    const isBalanced = bs.totals.is_balanced;
                    const balanceColor = isBalanced ? '#28a745' : '#dc3545';

                    return `
                        <div class="list-item">
                            <h4>${bs.name}</h4>
                            <p><strong>As of:</strong> ${new Date(bs.as_of_date).toLocaleDateString()}</p>
                            <p><strong>Total Assets:</strong> $${parseFloat(bs.totals.assets).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</p>
                            <p><strong>Total Liabilities:</strong> $${parseFloat(bs.totals.liabilities).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</p>
                            <p><strong>Total Equity:</strong> $${parseFloat(bs.totals.equity).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</p>
                            <p><strong>Liabilities + Equity:</strong> $${parseFloat(bs.totals.liabilities_plus_equity).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</p>
                            <p style="color: ${balanceColor}; font-weight: bold;">
                                ${isBalanced ? '✅ Balanced' : '❌ Not Balanced'}
                            </p>
                            <p><strong>Items:</strong> ${bs.items.length} accounts</p>
                        </div>
                    `;
                }).join('');
            } catch (error) {
                document.getElementById('balance-sheets-list').innerHTML =
                    `<div class="error">Failed to load balance sheets: ${error.message}</div>`;
            }
        }

        async function loadAll() {
            await Promise.all([
                loadSummary(),
                loadBudgets(),
                loadBalanceSheets(),
                loadPaperwork(),
                loadObstacles(),
                loadCreatures()
            ]);
        }

        // Load data on page load
        loadAll();

        // Refresh every 30 seconds
        setInterval(loadAll, 30000);
    </script>
</body>
</html>"""

    def log_message(self, format, *args):
        """Override to reduce log noise."""
        pass


def run_server(port=8080):
    """Run the web server."""
    server_address = ("", port)
    httpd = HTTPServer(server_address, PaperworkGodUIHandler)
    print(f"🏛️ Paperwork God UI running at http://localhost:{port}")
    print("Press Ctrl+C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Shutting down server...")
        httpd.shutdown()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Paperwork God Web UI")
    parser.add_argument("--port", type=int, default=8080, help="Port to run server on")
    args = parser.parse_args()

    run_server(args.port)
