"""
PocketBase Scout: Enhanced RealmScout with PocketBase integration

This scout sets up PocketBase on the realm, uses the probe system to collect data,
and stores findings in PocketBase for UI generation.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import subprocess
import shutil
import os

from .realm_colonization import RealmScout
from .probe import ProbeCollector, FileSystemProbe
from .tendril_network import TendrilNetwork


class PocketBaseScout(RealmScout):
    """
    Enhanced RealmScout with PocketBase integration.
    
    This scout:
    1. Sets up PocketBase instance on the realm
    2. Uses probe system to collect data
    3. Stores findings in PocketBase
    4. Generates UI from collected data
    """
    
    def __init__(
        self,
        being_id: str,
        reality_id: str,
        realm_name: str,
        realm_path: Path,
        parent_being_id: Optional[str] = None,
        **kwargs
    ):
        """Initialize PocketBase Scout."""
        # Initialize as RealmScout
        super().__init__(
            being_id=being_id,
            reality_id=reality_id,
            realm_name=realm_name,
            realm_path=realm_path,
            parent_being_id=parent_being_id,
            **kwargs
        )
        
        # Add PocketBase skills
        self.skills.update({
            "pocketbase_setup": 8.0,
            "data_collection": 10.0,
            "ui_generation": 7.0,
            "vision": 9.0,  # Ability to see (screenshots and interpretation)
            "screenshot_capture": 10.0,
            "image_interpretation": 8.0
        })
        
        # Scout base directory
        self.scout_base = self.realm_path / "_scout_base"
        self.pocketbase_dir = self.scout_base / "pocketbase"
        self.pocketbase_data_dir = self.pocketbase_dir / "pb_data"
        self.probe_data_dir = self.scout_base / "probe_data"
        self.screenshots_dir = self.scout_base / "screenshots"
        self.vision_data_dir = self.scout_base / "vision_data"
        
        # Create directories first
        self.scout_base.mkdir(parents=True, exist_ok=True)
        self.probe_data_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.vision_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Probe collector
        self.probe_collector = ProbeCollector(storage_path=self.probe_data_dir)
        
        # PocketBase status
        self.pocketbase_status: Dict[str, Any] = {
            "installed": False,
            "running": False,
            "port": 8090,
            "admin_email": "admin@realm.local",
            "admin_password": None
        }
        
        # Vision capabilities
        self.vision_enabled = True
        self.screenshots_taken: List[Dict[str, Any]] = []
        self.interpretations: List[Dict[str, Any]] = []
        
        # Tendril Network
        self.tendril_network = TendrilNetwork(
            realm_path=self.realm_path,
            network_name=f"{realm_name}_network"
        )
        
        # Mission Control connection (via tether)
        self.mission_control = None  # Will be set when tether is available
    
    def setup_pocketbase(self) -> Dict[str, Any]:
        """
        Set up PocketBase instance on the realm.
        
        Returns:
            Setup result
        """
        print(f"   📦 Setting up PocketBase scout base...")
        
        try:
            # Create scout base directory
            self.scout_base.mkdir(parents=True, exist_ok=True)
            self.pocketbase_dir.mkdir(parents=True, exist_ok=True)
            self.probe_data_dir.mkdir(parents=True, exist_ok=True)
            
            # Check if PocketBase binary exists
            pb_binary = self._find_pocketbase_binary()
            
            if not pb_binary:
                print(f"   ⚠️  PocketBase binary not found - using simulation mode")
                self.pocketbase_status["installed"] = False
                self.pocketbase_status["simulation_mode"] = True
                return {
                    "success": True,
                    "mode": "simulation",
                    "message": "PocketBase simulation mode enabled"
                }
            
            # Copy PocketBase to scout base
            pb_dest = self.pocketbase_dir / "pocketbase"
            if not pb_dest.exists():
                shutil.copy2(pb_binary, pb_dest)
                os.chmod(pb_dest, 0o755)
            
            self.pocketbase_status["installed"] = True
            self.pocketbase_status["binary_path"] = str(pb_dest)
            
            print(f"   ✅ PocketBase binary ready at: {pb_dest}")
            
            return {
                "success": True,
                "mode": "real",
                "binary_path": str(pb_dest),
                "data_dir": str(self.pocketbase_data_dir)
            }
            
        except Exception as e:
            print(f"   ❌ PocketBase setup failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "mode": "simulation"
            }
    
    def _find_pocketbase_binary(self) -> Optional[Path]:
        """Find PocketBase binary on system."""
        # Common locations
        locations = [
            Path.home() / "pocketbase" / "pocketbase",
            Path("/usr/local/bin/pocketbase"),
            Path("/opt/pocketbase/pocketbase"),
            Path.cwd() / "pocketbase" / "pocketbase",
        ]
        
        for loc in locations:
            if loc.exists() and loc.is_file():
                return loc
        
        # Check if in PATH
        try:
            result = subprocess.run(
                ["which", "pocketbase"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return Path(result.stdout.strip())
        except Exception:
            pass
        
        return None
    
    def probe_realm(self) -> Dict[str, Any]:
        """
        Probe the realm using the probe system.
        
        Returns:
            Probe results
        """
        print(f"   🔍 Probing realm with probe system...")
        
        probe_results = []
        
        try:
            # Probe directory structure
            print(f"      → Probing directory structure...")
            for item in self.realm_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    result = self.probe_collector.probe_file(str(item))
                    probe_results.append(result.to_dict())
                    print(f"         ✓ Probed: {item.name}")
            
            # Probe files in root
            print(f"      → Probing root files...")
            for item in self.realm_path.iterdir():
                if item.is_file():
                    result = self.probe_collector.probe_file(str(item))
                    probe_results.append(result.to_dict())
                    print(f"         ✓ Probed: {item.name}")
            
            # Save probe results
            probe_file = self.probe_data_dir / f"probe_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            probe_file.write_text(
                json.dumps(probe_results, indent=2),
                encoding="utf-8"
            )
            
            print(f"   ✅ Probe complete: {len(probe_results)} items probed")
            print(f"      Results saved to: {probe_file}")
            
            return {
                "success": True,
                "items_probed": len(probe_results),
                "results_file": str(probe_file),
                "results": probe_results
            }
            
        except Exception as e:
            print(f"   ❌ Probe failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def store_in_pocketbase(self, probe_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Store probe data in PocketBase (or simulation).
        
        Args:
            probe_data: Probe results to store
            
        Returns:
            Storage result
        """
        print(f"   💾 Storing data in PocketBase...")
        
        if not self.pocketbase_status.get("installed"):
            # Simulation mode - store as JSON
            print(f"      → Simulation mode: storing as JSON")
            
            storage_file = self.scout_base / "pocketbase_data.json"
            data = {
                "realm_name": self.realm_name,
                "scout_id": self.being_id,
                "collected_at": datetime.now().isoformat(),
                "probe_data": probe_data,
                "realm_path": str(self.realm_path),
                "items_count": len(probe_data.get("results", []))
            }
            
            storage_file.write_text(
                json.dumps(data, indent=2),
                encoding="utf-8"
            )
            
            print(f"      ✅ Data stored to: {storage_file}")
            
            return {
                "success": True,
                "mode": "simulation",
                "storage_file": str(storage_file),
                "items_stored": len(probe_data.get("results", []))
            }
        else:
            # Real PocketBase mode (would use API here)
            print(f"      → Real PocketBase mode (not implemented yet)")
            return {
                "success": False,
                "error": "Real PocketBase integration not yet implemented",
                "mode": "real"
            }
    
    def generate_ui(self, stored_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Interactive UI from collected data with Tendril Network.
        
        Args:
            stored_data: Data stored in PocketBase (includes probe_data, vision_data, tendril_network)
            
        Returns:
            UI generation result
        """
        print(f"   🎨 Generating Interactive UI with Tendril Network...")
        
        try:
            # Create UI directory
            ui_dir = self.scout_base / "ui"
            ui_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate HTML visualization
            html_file = ui_dir / "realm_visualization.html"
            
            probe_results = stored_data.get("probe_data", {}).get("results", [])
            network_data = stored_data.get("tendril_network", {})
            
            html_content = self._generate_html_ui(probe_results, network_data)
            
            html_file.write_text(html_content, encoding="utf-8")
            
            # Automatically open in browser
            try:
                import webbrowser
                file_url = f"file://{html_file.absolute()}"
                webbrowser.open(file_url)
                print(f"      ✅ Interactive UI generated: {html_file}")
            except Exception as e:
                print(f"      ⚠️  Could not auto-open browser: {e}")
                print(f"      💡 Manually open: file://{html_file.absolute()}")
            
            return {
                "success": True,
                "ui_file": str(html_file),
                "items_visualized": len(probe_results),
                "network_visualized": network_data.get("success", False)
            }
            
        except Exception as e:
            print(f"   ❌ UI generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_html_ui(self, probe_results: List[Dict[str, Any]], network_data: Optional[Dict[str, Any]] = None) -> str:
        """Generate Interactive HTML UI from probe results and tendril network."""
        
        items_html = ""
        for i, result in enumerate(probe_results[:50]):  # Limit to 50 items
            target = result.get("target", "Unknown")
            probe_type = result.get("probe_type", "unknown")
            success = result.get("success", False)
            data = result.get("data", {})
            
            status_icon = "✅" if success else "❌"
            
            items_html += f"""
            <div class="item" data-node-id="node_{i}">
                <div class="item-header">
                    <span class="status">{status_icon}</span>
                    <span class="type">{probe_type}</span>
                    <span class="target">{target}</span>
                </div>
                <div class="item-data">
                    <pre>{json.dumps(data, indent=2)}</pre>
                </div>
            </div>
            """
        
        # Network visualization
        network_html = ""
        if network_data:
            network_stats = network_data.get("network_stats", {})
            network_html = f"""
            <div class="network-section">
                <h2>🌐 Tendril Network</h2>
                <div class="network-stats">
                    <div class="stat-card">
                        <div class="stat-label">Nodes</div>
                        <div class="stat-value">{network_stats.get('total_nodes', 0)}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Tendrils</div>
                        <div class="stat-value">{network_stats.get('total_tendrils', 0)}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Strings</div>
                        <div class="stat-value">{network_stats.get('total_strings', 0)}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Avg Connections</div>
                        <div class="stat-value">{network_stats.get('average_connections_per_node', 0):.1f}</div>
                    </div>
                </div>
                <div id="network-graph" class="network-graph">
                    <p>🌐 Interactive network graph (click nodes to traverse)</p>
                    <div id="node-list" class="node-list"></div>
                </div>
            </div>
            """
        
        # Get network data for visualization
        network_stats = {}
        nodes_data = []
        tendrils_data = []
        
        if network_data and network_data.get("success"):
            network_stats = network_data.get("network_stats", {})
            # Get actual network data
            nodes_list = list(self.tendril_network.nodes.values())
            tendrils_list = list(self.tendril_network.tendrils.values())
            
            nodes_data = [
                {
                    "id": node.node_id,
                    "type": node.node_type,
                    "path": node.path,
                    "connections": len(node.connections)
                }
                for node in nodes_list[:100]  # Limit for performance
            ]
            tendrils_data = [
                {
                    "id": t.tendril_id,
                    "from": t.from_node_id,
                    "to": t.to_node_id,
                    "type": t.connection_type,
                    "strength": t.strength
                }
                for t in tendrils_list[:200]  # Limit for performance
            ]
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Realm Visualization: {self.realm_name}</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
            background: #0a0a0a;
            color: #00ff00;
            padding: 20px;
            line-height: 1.6;
        }}
        
        .header {{
            border-bottom: 2px solid #00ff00;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        
        h1 {{
            color: #00ff00;
            font-size: 2em;
            margin-bottom: 10px;
        }}
        
        .info {{
            color: #888;
            font-size: 0.9em;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: #1a1a1a;
            border: 1px solid #00ff00;
            padding: 15px;
            border-radius: 5px;
        }}
        
        .stat-label {{
            color: #888;
            font-size: 0.8em;
            margin-bottom: 5px;
        }}
        
        .stat-value {{
            color: #00ff00;
            font-size: 1.5em;
            font-weight: bold;
        }}
        
        .items {{
            display: grid;
            gap: 15px;
        }}
        
        .item {{
            background: #1a1a1a;
            border: 1px solid #333;
            padding: 15px;
            border-radius: 5px;
        }}
        
        .item-header {{
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
            align-items: center;
        }}
        
        .status {{
            font-size: 1.2em;
        }}
        
        .type {{
            background: #333;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.8em;
        }}
        
        .target {{
            color: #00ff00;
            flex: 1;
        }}
        
        .item-data {{
            background: #0a0a0a;
            padding: 10px;
            border-radius: 3px;
            max-height: 200px;
            overflow-y: auto;
        }}
        
        .item-data pre {{
            color: #888;
            font-size: 0.85em;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        
        .network-section {{
            margin-top: 40px;
            padding-top: 30px;
            border-top: 2px solid #00ff00;
        }}
        
        .network-graph {{
            margin-top: 20px;
            background: #1a1a1a;
            border: 1px solid #00ff00;
            padding: 20px;
            border-radius: 5px;
            min-height: 400px;
        }}
        
        .node-list {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 10px;
            margin-top: 20px;
        }}
        
        .network-node {{
            background: #0a0a0a;
            border: 1px solid #333;
            padding: 10px;
            border-radius: 3px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .network-node:hover {{
            border-color: #00ff00;
            background: #1a1a1a;
        }}
        
        .network-node.selected {{
            border-color: #00ff00;
            background: #0f3f0f;
        }}
        
        .node-type {{
            color: #888;
            font-size: 0.8em;
        }}
        
        .node-connections {{
            color: #00ff00;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        
        svg {{
            width: 100%;
            height: 400px;
            background: #0a0a0a;
        }}
        
        .link {{
            stroke: #333;
            stroke-width: 2px;
        }}
        
        .link.active {{
            stroke: #00ff00;
            stroke-width: 3px;
        }}
        
        .node-circle {{
            fill: #00ff00;
            stroke: #0a0a0a;
            stroke-width: 2px;
            cursor: pointer;
        }}
        
        .node-circle:hover {{
            fill: #00ff88;
        }}
        
        .node-label {{
            fill: #00ff00;
            font-size: 10px;
            pointer-events: none;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌍 Realm Visualization: {self.realm_name}</h1>
        <div class="info">
            Scout: {self.being_id}<br>
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
            Realm Path: {self.realm_path}
        </div>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-label">Items Probed</div>
            <div class="stat-value">{len(probe_results)}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Successful</div>
            <div class="stat-value">{sum(1 for r in probe_results if r.get('success'))}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Failed</div>
            <div class="stat-value">{sum(1 for r in probe_results if not r.get('success'))}</div>
        </div>
    </div>
    
    <div class="items">
        {items_html}
    </div>
    
    {network_html}
    
    <script>
        // Tendril Network Visualization
        const networkData = {{
            nodes: {json.dumps(nodes_data)},
            tendrils: {json.dumps(tendrils_data)}
        }};
        
        // Simple network visualization
        if (networkData.nodes.length > 0) {{
            const nodeList = document.getElementById('node-list');
            
            networkData.nodes.forEach(node => {{
                const nodeEl = document.createElement('div');
                nodeEl.className = 'network-node';
                nodeEl.dataset.nodeId = node.id;
                nodeEl.innerHTML = `
                    <div class="node-type">${{node.type}}</div>
                    <div>${{node.path.split('/').pop()}}</div>
                    <div class="node-connections">${{node.connections}} connections</div>
                `;
                
                nodeEl.addEventListener('click', () => {{
                    // Highlight node
                    document.querySelectorAll('.network-node').forEach(n => n.classList.remove('selected'));
                    nodeEl.classList.add('selected');
                    
                    // Show connections
                    const connectedTendrils = networkData.tendrils.filter(t => 
                        t.from === node.id || t.to === node.id
                    );
                    console.log(`Node ${{node.id}} has ${{connectedTendrils.length}} tendrils`);
                }});
                
                nodeList.appendChild(nodeEl);
            }});
        }}
        
        // Network traversal function
        function traverseNetwork(startNodeId, maxDepth = 3) {{
            const visited = new Set();
            const queue = [[startNodeId, 0]];
            const path = [];
            
            while (queue.length > 0) {{
                const [nodeId, depth] = queue.shift();
                
                if (visited.has(nodeId) || depth > maxDepth) continue;
                
                visited.add(nodeId);
                path.push(nodeId);
                
                // Find connected nodes
                networkData.tendrils.forEach(tendril => {{
                    if (tendril.from === nodeId && !visited.has(tendril.to)) {{
                        queue.push([tendril.to, depth + 1]);
                    }}
                    if (tendril.to === nodeId && !visited.has(tendril.from)) {{
                        queue.push([tendril.from, depth + 1]);
                    }}
                }});
            }}
            
            return path;
        }}
        
        // Make traversal available globally
        window.traverseNetwork = traverseNetwork;
        window.networkData = networkData;
        
        console.log('🌐 Tendril Network loaded:', networkData.nodes.length, 'nodes,', networkData.tendrils.length, 'tendrils');
        console.log('💡 Try: traverseNetwork(networkData.nodes[0].id) to traverse from first node');
    </script>
</body>
</html>
"""
        return html
    
    def take_screenshot(self, target_path: Optional[Path] = None, description: str = "") -> Dict[str, Any]:
        """
        Take a screenshot of the realm or a specific target.
        
        The Scout's ability to SEE - captures visual representation.
        
        Args:
            target_path: Path to screenshot (if None, screenshots realm root)
            description: Description of what's being captured
            
        Returns:
            Screenshot result
        """
        print(f"   📸 Taking screenshot...")
        
        try:
            # Determine target
            if target_path is None:
                target_path = self.realm_path
            
            # Generate screenshot filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_name = f"screenshot_{timestamp}.png"
            screenshot_path = self.screenshots_dir / screenshot_name
            
            # Try different screenshot methods
            screenshot_taken = False
            
            # Method 1: If it's a file, try to capture it
            if target_path.is_file():
                # For images, just copy them
                if target_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                    import shutil
                    shutil.copy2(target_path, screenshot_path)
                    screenshot_taken = True
                    print(f"      ✓ Captured image file: {target_path.name}")
            
            # Method 2: If it's a directory, try to capture directory listing
            elif target_path.is_dir():
                # Create a visual representation of directory structure
                self._create_directory_screenshot(target_path, screenshot_path)
                screenshot_taken = True
                print(f"      ✓ Captured directory structure: {target_path.name}")
            
            # Method 3: Try using PIL to capture screen (if on macOS/Linux)
            if not screenshot_taken:
                try:
                    screenshot_taken = self._capture_screen_screenshot(screenshot_path)
                    if screenshot_taken:
                        print(f"      ✓ Captured screen screenshot")
                except Exception as e:
                    print(f"      ⚠️  Screen capture not available: {e}")
            
            if screenshot_taken and screenshot_path.exists():
                screenshot_info = {
                    "screenshot_path": str(screenshot_path),
                    "target": str(target_path),
                    "description": description,
                    "timestamp": datetime.now().isoformat(),
                    "size_bytes": screenshot_path.stat().st_size
                }
                self.screenshots_taken.append(screenshot_info)
                
                # Automatically interpret the screenshot
                interpretation = self.interpret_screenshot(screenshot_path, description)
                
                return {
                    "success": True,
                    "screenshot_path": str(screenshot_path),
                    "screenshot_info": screenshot_info,
                    "interpretation": interpretation
                }
            else:
                return {
                    "success": False,
                    "error": "Could not capture screenshot"
                }
                
        except Exception as e:
            print(f"   ❌ Screenshot failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_directory_screenshot(self, dir_path: Path, output_path: Path) -> None:
        """Create a visual representation of directory structure."""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Get directory listing
            items = []
            for item in sorted(dir_path.iterdir()):
                if item.is_dir():
                    items.append(f"📁 {item.name}/")
                else:
                    size = item.stat().st_size
                    size_str = f"{size:,} bytes" if size < 1024*1024 else f"{size/(1024*1024):.1f} MB"
                    items.append(f"📄 {item.name} ({size_str})")
            
            # Create image
            width, height = 800, min(600, 50 + len(items) * 25)
            img = Image.new('RGB', (width, height), color='#0a0a0a')
            draw = ImageDraw.Draw(img)
            
            # Try to use monospace font
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
            except:
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14)
                except:
                    font = ImageFont.load_default()
            
            # Draw header
            draw.text((10, 10), f"Directory: {dir_path.name}", fill='#00ff00', font=font)
            draw.text((10, 35), f"Path: {dir_path}", fill='#888', font=font)
            
            # Draw items
            y = 70
            for item in items[:20]:  # Limit to 20 items
                draw.text((20, y), item, fill='#00ff00', font=font)
                y += 25
            
            if len(items) > 20:
                draw.text((20, y), f"... and {len(items) - 20} more items", fill='#888', font=font)
            
            # Save
            img.save(output_path, 'PNG')
            
        except ImportError:
            # Fallback: create text file representation
            output_path.with_suffix('.txt').write_text(
                f"Directory: {dir_path.name}\nPath: {dir_path}\n\nItems:\n" + 
                "\n".join([f"  {item}" for item in items[:50]]),
                encoding="utf-8"
            )
            # Create a simple placeholder image using basic methods
            import struct
            # Create minimal 1x1 PNG
            png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82'
            output_path.write_bytes(png_data)
        except Exception as e:
            raise Exception(f"Failed to create directory screenshot: {e}")
    
    def _capture_screen_screenshot(self, output_path: Path) -> bool:
        """Try to capture screen screenshot (platform-dependent)."""
        import platform
        
        system = platform.system()
        
        if system == "Darwin":  # macOS
            try:
                subprocess.run(
                    ["screencapture", "-x", str(output_path)],
                    check=True,
                    capture_output=True
                )
                return True
            except:
                return False
        elif system == "Linux":
            try:
                subprocess.run(
                    ["import", "-window", "root", str(output_path)],
                    check=True,
                    capture_output=True
                )
                return True
            except:
                return False
        else:
            return False
    
    def interpret_screenshot(self, screenshot_path: Path, context: str = "") -> Dict[str, Any]:
        """
        Interpret a screenshot using vision capabilities.
        
        The Scout's ability to UNDERSTAND what it sees.
        
        Args:
            screenshot_path: Path to screenshot image
            context: Context about what the screenshot shows
            
        Returns:
            Interpretation result
        """
        print(f"      🔍 Interpreting screenshot...")
        
        try:
            interpretation = {
                "screenshot_path": str(screenshot_path),
                "context": context,
                "timestamp": datetime.now().isoformat(),
                "analysis": {}
            }
            
            # Basic image analysis
            if screenshot_path.exists():
                try:
                    from PIL import Image
                    
                    img = Image.open(screenshot_path)
                    width, height = img.size
                    mode = img.mode
                    
                    interpretation["analysis"] = {
                        "dimensions": f"{width}x{height}",
                        "mode": mode,
                        "format": img.format,
                        "size_bytes": screenshot_path.stat().st_size
                    }
                    
                    # Try to extract text if it's a text-heavy image
                    # (This is basic - could be enhanced with OCR)
                    interpretation["analysis"]["has_text"] = mode in ['RGB', 'RGBA', 'L']
                    interpretation["analysis"]["is_visual"] = True
                    
                    print(f"         ✓ Image analyzed: {width}x{height}, {mode}")
                    
                except ImportError:
                    interpretation["analysis"] = {
                        "note": "PIL/Pillow not available for detailed analysis",
                        "file_exists": True,
                        "size_bytes": screenshot_path.stat().st_size
                    }
                except Exception as e:
                    interpretation["analysis"]["error"] = str(e)
            
            # Store interpretation
            self.interpretations.append(interpretation)
            
            # Save interpretation
            interpretation_file = self.vision_data_dir / f"interpretation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            interpretation_file.write_text(
                json.dumps(interpretation, indent=2),
                encoding="utf-8"
            )
            
            return interpretation
            
        except Exception as e:
            print(f"         ❌ Interpretation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def see_realm(self) -> Dict[str, Any]:
        """
        The Scout's primary vision method - SEE the realm.
        
        Takes screenshots of key areas and interprets them.
        
        Returns:
            Vision results
        """
        print(f"\n   👁️  SCOUT VISION: Seeing the Realm...")
        print(f"   {'='*60}")
        
        vision_results = {
            "screenshots": [],
            "interpretations": [],
            "vision_summary": {}
        }
        
        # Screenshot 1: Realm root
        print(f"\n   📸 Screenshot 1: Realm root directory")
        root_screenshot = self.take_screenshot(
            target_path=self.realm_path,
            description="Realm root directory structure"
        )
        if root_screenshot.get("success"):
            vision_results["screenshots"].append(root_screenshot["screenshot_info"])
            vision_results["interpretations"].append(root_screenshot.get("interpretation", {}))
        
        # Screenshot 2: Scout base
        scout_base_path = self.scout_base
        if scout_base_path.exists():
            print(f"\n   📸 Screenshot 2: Scout base")
            base_screenshot = self.take_screenshot(
                target_path=scout_base_path,
                description="Scout base directory"
            )
            if base_screenshot.get("success"):
                vision_results["screenshots"].append(base_screenshot["screenshot_info"])
                vision_results["interpretations"].append(base_screenshot.get("interpretation", {}))
        
        # Screenshot 3: Key directories
        key_dirs = ["exploration", "case_files", "_scout_base"]
        for dir_name in key_dirs:
            dir_path = self.realm_path / dir_name
            if dir_path.exists() and dir_path.is_dir():
                print(f"\n   📸 Screenshot: {dir_name}/")
                dir_screenshot = self.take_screenshot(
                    target_path=dir_path,
                    description=f"{dir_name} directory contents"
                )
                if dir_screenshot.get("success"):
                    vision_results["screenshots"].append(dir_screenshot["screenshot_info"])
                    vision_results["interpretations"].append(dir_screenshot.get("interpretation", {}))
        
        # Summary
        vision_results["vision_summary"] = {
            "total_screenshots": len(vision_results["screenshots"]),
            "total_interpretations": len(vision_results["interpretations"]),
            "screenshots_dir": str(self.screenshots_dir),
            "vision_data_dir": str(self.vision_data_dir)
        }
        
        print(f"\n   ✅ Vision complete: {len(vision_results['screenshots'])} screenshots taken")
        print(f"   {'='*60}\n")
        
        return vision_results
    
    def _relay_to_mission_control(self, mission_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Relay messages back to Mission Control via Tether.
        
        Creates strings that flow through the tendril network
        and sends them back to Mission Control.
        
        Args:
            mission_data: Complete mission data to relay
            
        Returns:
            Relay result
        """
        print(f"      → Creating relay strings...")
        
        try:
            from ..pantheon.mission_control import MissionControl
            from pathlib import Path
            
            # Initialize Mission Control
            mission_control = MissionControl(project_path=Path.cwd())
            
            # Find or create mission for this realm
            mission_id = f"realm_scout_{self.realm_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            mission_control.register_mission(mission_id)
            
            # Create root node for Mission Control connection
            root_node = self.tendril_network.create_node(
                path=Path("mission_control"),
                node_type="entity",
                metadata={"entity_type": "mission_control", "mission_id": mission_id}
            )
            
            # Create relay strings for key data
            strings_sent = 0
            
            # Relay 1: Network stats
            if "tendril_network" in mission_data:
                network_stats = mission_data["tendril_network"].get("network_stats", {})
                # Find a representative node to send from
                if self.tendril_network.nodes:
                    first_node_id = list(self.tendril_network.nodes.keys())[0]
                    string = self.tendril_network.send_string(
                        from_node_id=first_node_id,
                        to_node_id=root_node.node_id,
                        message_type="network_stats",
                        payload=network_stats,
                        connection_type="telemetry"
                    )
                    strings_sent += 1
                    print(f"         ✓ Relayed network stats: {network_stats.get('total_nodes', 0)} nodes")
            
            # Relay 2: Vision data
            if "vision" in mission_data:
                vision_summary = mission_data["vision"].get("vision_summary", {})
                if self.tendril_network.nodes:
                    first_node_id = list(self.tendril_network.nodes.keys())[0]
                    string = self.tendril_network.send_string(
                        from_node_id=first_node_id,
                        to_node_id=root_node.node_id,
                        message_type="vision_report",
                        payload=vision_summary,
                        connection_type="observation"
                    )
                    strings_sent += 1
                    print(f"         ✓ Relayed vision data: {vision_summary.get('total_screenshots', 0)} screenshots")
            
            # Relay 3: Probe results
            if "probe_results" in mission_data:
                probe_summary = {
                    "items_probed": mission_data["probe_results"].get("items_probed", 0),
                    "success": mission_data["probe_results"].get("success", False)
                }
                if self.tendril_network.nodes:
                    first_node_id = list(self.tendril_network.nodes.keys())[0]
                    string = self.tendril_network.send_string(
                        from_node_id=first_node_id,
                        to_node_id=root_node.node_id,
                        message_type="probe_report",
                        payload=probe_summary,
                        connection_type="discovery"
                    )
                    strings_sent += 1
                    print(f"         ✓ Relayed probe results: {probe_summary.get('items_probed', 0)} items")
            
            # Update Mission Control with telemetry
            network_stats = mission_data.get("tendril_network", {}).get("network_stats", {})
            vision_summary = mission_data.get("vision", {}).get("vision_summary", {})
            
            mission_control.update_status(
                mission_id=mission_id,
                status="active",
                progress=1.0,
                telemetry={
                    "realm_name": self.realm_name,
                    "scout_id": self.being_id,
                    "network_nodes": network_stats.get("total_nodes", 0),
                    "tendrils": network_stats.get("total_tendrils", 0),
                    "strings_sent": strings_sent,
                    "vision_screenshots": vision_summary.get("total_screenshots", 0)
                }
            )
            
            print(f"      ✅ Relayed {strings_sent} strings to Mission Control")
            
            return {
                "success": True,
                "mission_id": mission_id,
                "strings_sent": strings_sent,
                "root_node_id": root_node.node_id
            }
            
        except Exception as e:
            print(f"      ❌ Relay failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def run_full_mission(self) -> Dict[str, Any]:
        """
        Run complete scout mission with PocketBase integration.
        
        Returns:
            Complete mission results
        """
        print(f"\n{'='*70}")
        print(f"🚀 POCKETBASE SCOUT MISSION: {self.realm_name}")
        print(f"{'='*70}\n")
        
        results = {
            "scout_id": self.being_id,
            "realm_name": self.realm_name,
            "realm_path": str(self.realm_path),
            "mission_start": datetime.now().isoformat()
        }
        
        # Step 1: Setup PocketBase
        print("📦 Step 1: Setting up PocketBase scout base...")
        pb_setup = self.setup_pocketbase()
        results["pocketbase_setup"] = pb_setup
        print()
        
        # Step 2: Probe realm
        print("🔍 Step 2: Probing realm with probe system...")
        probe_results = self.probe_realm()
        results["probe_results"] = probe_results
        print()
        
        # Step 3: Store in PocketBase
        if probe_results.get("success"):
            print("💾 Step 3: Storing data in PocketBase...")
            storage_result = self.store_in_pocketbase(probe_results)
            results["storage"] = storage_result
            print()
            
        # Step 4: Vision - SEE the realm
        print("👁️  Step 4: Scout Vision - Seeing the Realm...")
        vision_results = self.see_realm()
        results["vision"] = vision_results
        print()
        
        # Step 5: Build Tendril Network
        print("🌐 Step 5: Building Tendril Network...")
        network_result = self.tendril_network.build_realm_network(max_depth=3)
        results["tendril_network"] = network_result
        print()
        
        # Step 6: Relay messages to Mission Control via Tether
        print("📡 Step 6: Relaying messages to Mission Control via Tether...")
        relay_result = self._relay_to_mission_control(results)
        results["mission_control_relay"] = relay_result
        print()
        
        # Step 7: Generate Interactive UI
        if storage_result.get("success"):
            print("🎨 Step 7: Generating Interactive UI with Tendril Network...")
            ui_result = self.generate_ui({
                "probe_data": probe_results,
                "vision_data": vision_results,
                "tendril_network": network_result
            })
            results["ui_generation"] = ui_result
            print()
            
            # Automatically open UI in browser
            if ui_result.get("success") and ui_result.get("ui_file"):
                try:
                    import webbrowser
                    ui_path = Path(ui_result["ui_file"])
                    if ui_path.exists():
                        file_url = f"file://{ui_path.absolute()}"
                        webbrowser.open(file_url)
                        print(f"   🌐 UI automatically opened in browser!")
                except Exception as e:
                    print(f"   ⚠️  Could not auto-open browser: {e}")
                    print(f"   💡 Manually open: file://{ui_path.absolute()}")
        
        results["mission_end"] = datetime.now().isoformat()
        results["success"] = all([
            pb_setup.get("success"),
            probe_results.get("success"),
            results.get("storage", {}).get("success", False),
            results.get("ui_generation", {}).get("success", False)
        ])
        
        print(f"{'='*70}")
        if results["success"]:
            print(f"✅ MISSION COMPLETE")
        else:
            print(f"⚠️  MISSION COMPLETE (with warnings)")
        print(f"{'='*70}\n")
        
        return results
