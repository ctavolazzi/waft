"""
Tendril Network: Elastic Node Graph System

Creates a traversible node network where:
- Nodes = Entities in the realm (files, directories, data points)
- Tendrils = Connections between nodes (edges in the graph)
- Strings = The actual connection data/messages flowing through tendrils
- Messages flow back to Mission Control via Tether

This creates a truly elastic, traversible node system for realm exploration.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List, Set, Tuple
from datetime import datetime
import json
import hashlib
from dataclasses import dataclass, asdict
from collections import deque


@dataclass
class Node:
    """A node in the realm network."""
    node_id: str
    node_type: str  # 'file', 'directory', 'data', 'entity'
    path: str
    metadata: Dict[str, Any]
    discovered_at: str
    last_accessed: str
    connections: Set[str]  # Set of node_ids this node connects to
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            **asdict(self),
            "connections": list(self.connections)
        }


@dataclass
class Tendril:
    """A tendril (edge) connecting two nodes."""
    tendril_id: str
    from_node_id: str
    to_node_id: str
    connection_type: str  # 'contains', 'references', 'depends_on', 'related_to'
    strength: float  # 0.0 to 1.0 - connection strength
    created_at: str
    messages_sent: int
    last_message_at: Optional[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class String:
    """A message/string flowing through a tendril."""
    string_id: str
    tendril_id: str
    from_node_id: str
    to_node_id: str
    message_type: str  # 'discovery', 'update', 'query', 'response'
    payload: Dict[str, Any]
    timestamp: str
    status: str  # 'pending', 'in_transit', 'delivered', 'failed'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class TendrilNetwork:
    """
    Elastic node graph system with tendrils and strings.
    
    This creates a traversible network where nodes are connected by tendrils,
    and messages (strings) flow through the network back to Mission Control.
    """
    
    def __init__(self, realm_path: Path, network_name: str = "realm_network"):
        """
        Initialize Tendril Network.
        
        Args:
            realm_path: Path to the realm
            network_name: Name for this network instance
        """
        self.realm_path = Path(realm_path)
        self.network_name = network_name
        
        # Network storage
        self.network_dir = self.realm_path / "_scout_base" / "tendril_network"
        self.network_dir.mkdir(parents=True, exist_ok=True)
        
        # Network state files
        self.nodes_file = self.network_dir / "nodes.json"
        self.tendrils_file = self.network_dir / "tendrils.json"
        self.strings_file = self.network_dir / "strings.json"
        
        # In-memory network
        self.nodes: Dict[str, Node] = {}
        self.tendrils: Dict[str, Tendril] = {}
        self.strings: List[String] = []
        
        # Load existing network
        self._load_network()
    
    def _load_network(self) -> None:
        """Load network from disk."""
        try:
            if self.nodes_file.exists():
                nodes_data = json.loads(self.nodes_file.read_text(encoding="utf-8"))
                for node_data in nodes_data.get("nodes", []):
                    node = Node(
                        node_id=node_data["node_id"],
                        node_type=node_data["node_type"],
                        path=node_data["path"],
                        metadata=node_data["metadata"],
                        discovered_at=node_data["discovered_at"],
                        last_accessed=node_data["last_accessed"],
                        connections=set(node_data.get("connections", []))
                    )
                    self.nodes[node.node_id] = node
            
            if self.tendrils_file.exists():
                tendrils_data = json.loads(self.tendrils_file.read_text(encoding="utf-8"))
                for tendril_data in tendrils_data.get("tendrils", []):
                    tendril = Tendril(**tendril_data)
                    self.tendrils[tendril.tendril_id] = tendril
            
            if self.strings_file.exists():
                strings_data = json.loads(self.strings_file.read_text(encoding="utf-8"))
                for string_data in strings_data.get("strings", []):
                    string = String(**string_data)
                    self.strings.append(string)
        except Exception as e:
            print(f"   ⚠️  Could not load network: {e}")
    
    def _save_network(self) -> None:
        """Save network to disk."""
        try:
            # Save nodes
            nodes_data = {
                "network_name": self.network_name,
                "last_update": datetime.now().isoformat(),
                "nodes": [node.to_dict() for node in self.nodes.values()]
            }
            self.nodes_file.write_text(
                json.dumps(nodes_data, indent=2),
                encoding="utf-8"
            )
            
            # Save tendrils
            tendrils_data = {
                "network_name": self.network_name,
                "last_update": datetime.now().isoformat(),
                "tendrils": [tendril.to_dict() for tendril in self.tendrils.values()]
            }
            self.tendrils_file.write_text(
                json.dumps(tendrils_data, indent=2),
                encoding="utf-8"
            )
            
            # Save strings (keep last 1000)
            strings_data = {
                "network_name": self.network_name,
                "last_update": datetime.now().isoformat(),
                "strings": [string.to_dict() for string in self.strings[-1000:]]
            }
            self.strings_file.write_text(
                json.dumps(strings_data, indent=2),
                encoding="utf-8"
            )
        except Exception as e:
            print(f"   ⚠️  Could not save network: {e}")
    
    def create_node(
        self,
        path: Path,
        node_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Node:
        """
        Create a new node in the network.
        
        Args:
            path: Path to the entity
            node_type: Type of node ('file', 'directory', 'data', 'entity')
            metadata: Additional metadata
            
        Returns:
            Created node
        """
        # Generate node ID from path
        path_str = str(path.relative_to(self.realm_path) if path.is_relative_to(self.realm_path) else path)
        node_id = hashlib.sha256(f"{self.network_name}:{path_str}".encode()).hexdigest()[:16]
        
        # Check if node exists
        if node_id in self.nodes:
            # Update existing node
            node = self.nodes[node_id]
            node.last_accessed = datetime.now().isoformat()
            if metadata:
                node.metadata.update(metadata)
            return node
        
        # Create new node
        node = Node(
            node_id=node_id,
            node_type=node_type,
            path=path_str,
            metadata=metadata or {},
            discovered_at=datetime.now().isoformat(),
            last_accessed=datetime.now().isoformat(),
            connections=set()
        )
        
        self.nodes[node_id] = node
        self._save_network()
        
        return node
    
    def create_tendril(
        self,
        from_node_id: str,
        to_node_id: str,
        connection_type: str = "related_to",
        strength: float = 0.5
    ) -> Tendril:
        """
        Create a tendril (connection) between two nodes.
        
        Args:
            from_node_id: Source node ID
            to_node_id: Target node ID
            connection_type: Type of connection
            strength: Connection strength (0.0 to 1.0)
            
        Returns:
            Created tendril
        """
        # Generate tendril ID
        tendril_id = hashlib.sha256(
            f"{from_node_id}:{to_node_id}:{connection_type}".encode()
        ).hexdigest()[:16]
        
        # Check if tendril exists
        if tendril_id in self.tendrils:
            return self.tendrils[tendril_id]
        
        # Create new tendril
        tendril = Tendril(
            tendril_id=tendril_id,
            from_node_id=from_node_id,
            to_node_id=to_node_id,
            connection_type=connection_type,
            strength=strength,
            created_at=datetime.now().isoformat(),
            messages_sent=0,
            last_message_at=None
        )
        
        self.tendrils[tendril_id] = tendril
        
        # Update node connections
        if from_node_id in self.nodes:
            self.nodes[from_node_id].connections.add(to_node_id)
        if to_node_id in self.nodes:
            self.nodes[to_node_id].connections.add(from_node_id)
        
        self._save_network()
        
        return tendril
    
    def send_string(
        self,
        from_node_id: str,
        to_node_id: str,
        message_type: str,
        payload: Dict[str, Any],
        connection_type: Optional[str] = None
    ) -> String:
        """
        Send a string (message) through a tendril.
        
        Args:
            from_node_id: Source node
            to_node_id: Target node
            message_type: Type of message
            payload: Message data
            connection_type: Connection type (auto-detected if None)
            
        Returns:
            Created string
        """
        # Find or create tendril
        tendril = None
        for t in self.tendrils.values():
            if (t.from_node_id == from_node_id and t.to_node_id == to_node_id) or \
               (t.from_node_id == to_node_id and t.to_node_id == from_node_id):
                tendril = t
                break
        
        if not tendril:
            # Create new tendril
            tendril = self.create_tendril(
                from_node_id=from_node_id,
                to_node_id=to_node_id,
                connection_type=connection_type or "message",
                strength=0.5
            )
        
        # Create string
        string_id = hashlib.sha256(
            f"{from_node_id}:{to_node_id}:{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        string = String(
            string_id=string_id,
            tendril_id=tendril.tendril_id,
            from_node_id=from_node_id,
            to_node_id=to_node_id,
            message_type=message_type,
            payload=payload,
            timestamp=datetime.now().isoformat(),
            status="in_transit"
        )
        
        self.strings.append(string)
        
        # Update tendril
        tendril.messages_sent += 1
        tendril.last_message_at = datetime.now().isoformat()
        
        self._save_network()
        
        return string
    
    def traverse_network(
        self,
        start_node_id: str,
        max_depth: int = 5,
        traversal_type: str = "bfs"  # 'bfs' or 'dfs'
    ) -> List[Node]:
        """
        Traverse the network from a starting node.
        
        Uses BFS (Breadth-First Search) or DFS (Depth-First Search).
        
        Args:
            start_node_id: Starting node ID
            max_depth: Maximum traversal depth
            traversal_type: 'bfs' or 'dfs'
            
        Returns:
            List of nodes in traversal order
        """
        if start_node_id not in self.nodes:
            return []
        
        visited: Set[str] = set()
        result: List[Node] = []
        
        if traversal_type == "bfs":
            # Breadth-First Search
            queue = deque([(start_node_id, 0)])
            
            while queue:
                node_id, depth = queue.popleft()
                
                if node_id in visited or depth > max_depth:
                    continue
                
                visited.add(node_id)
                result.append(self.nodes[node_id])
                
                # Add connected nodes
                for connected_id in self.nodes[node_id].connections:
                    if connected_id not in visited:
                        queue.append((connected_id, depth + 1))
        
        else:
            # Depth-First Search
            stack = [(start_node_id, 0)]
            
            while stack:
                node_id, depth = stack.pop()
                
                if node_id in visited or depth > max_depth:
                    continue
                
                visited.add(node_id)
                result.append(self.nodes[node_id])
                
                # Add connected nodes
                for connected_id in self.nodes[node_id].connections:
                    if connected_id not in visited:
                        stack.append((connected_id, depth + 1))
        
        return result
    
    def find_path(
        self,
        from_node_id: str,
        to_node_id: str,
        algorithm: str = "dijkstra"  # 'dijkstra', 'bfs', 'dfs'
    ) -> Optional[List[str]]:
        """
        Find shortest path between two nodes.
        
        Args:
            from_node_id: Start node
            to_node_id: End node
            algorithm: Pathfinding algorithm
            
        Returns:
            List of node IDs forming the path, or None if no path exists
        """
        if from_node_id == to_node_id:
            return [from_node_id]
        
        if from_node_id not in self.nodes or to_node_id not in self.nodes:
            return None
        
        if algorithm == "bfs":
            # Simple BFS pathfinding
            queue = deque([(from_node_id, [from_node_id])])
            visited = {from_node_id}
            
            while queue:
                current_id, path = queue.popleft()
                
                if current_id == to_node_id:
                    return path
                
                for connected_id in self.nodes[current_id].connections:
                    if connected_id not in visited:
                        visited.add(connected_id)
                        queue.append((connected_id, path + [connected_id]))
        
        elif algorithm == "dijkstra":
            # Dijkstra's algorithm (using tendril strength as weights)
            import heapq
            
            distances = {from_node_id: 0}
            previous = {}
            pq = [(0, from_node_id)]
            visited = set()
            
            while pq:
                dist, current_id = heapq.heappop(pq)
                
                if current_id in visited:
                    continue
                
                visited.add(current_id)
                
                if current_id == to_node_id:
                    # Reconstruct path
                    path = []
                    node = to_node_id
                    while node is not None:
                        path.append(node)
                        node = previous.get(node)
                    return list(reversed(path))
                
                for connected_id in self.nodes[current_id].connections:
                    # Find tendril strength (inverse for weight)
                    tendril_strength = 1.0
                    for tendril in self.tendrils.values():
                        if (tendril.from_node_id == current_id and tendril.to_node_id == connected_id) or \
                           (tendril.from_node_id == connected_id and tendril.to_node_id == current_id):
                            tendril_strength = 1.0 - tendril.strength  # Inverse for weight
                            break
                    
                    new_dist = dist + tendril_strength
                    
                    if connected_id not in distances or new_dist < distances[connected_id]:
                        distances[connected_id] = new_dist
                        previous[connected_id] = current_id
                        heapq.heappush(pq, (new_dist, connected_id))
        
        return None
    
    def get_network_stats(self) -> Dict[str, Any]:
        """Get network statistics."""
        return {
            "total_nodes": len(self.nodes),
            "total_tendrils": len(self.tendrils),
            "total_strings": len(self.strings),
            "nodes_by_type": {
                node_type: sum(1 for n in self.nodes.values() if n.node_type == node_type)
                for node_type in set(n.node_type for n in self.nodes.values())
            },
            "connection_types": {
                conn_type: sum(1 for t in self.tendrils.values() if t.connection_type == conn_type)
                for conn_type in set(t.connection_type for t in self.tendrils.values())
            },
            "average_connections_per_node": (
                sum(len(n.connections) for n in self.nodes.values()) / len(self.nodes)
                if self.nodes else 0
            )
        }
    
    def build_realm_network(self, max_depth: int = 3) -> Dict[str, Any]:
        """
        Build network by discovering nodes and creating tendrils.
        
        Args:
            max_depth: Maximum directory depth to explore
            
        Returns:
            Build results
        """
        print(f"   🌐 Building Tendril Network...")
        
        nodes_created = 0
        tendrils_created = 0
        
        def explore_directory(dir_path: Path, depth: int = 0, parent_node_id: Optional[str] = None):
            nonlocal nodes_created, tendrils_created
            
            if depth > max_depth:
                return
            
            # Create node for directory
            dir_node = self.create_node(
                path=dir_path,
                node_type="directory",
                metadata={
                    "depth": depth,
                    "item_count": len(list(dir_path.iterdir())) if dir_path.exists() else 0
                }
            )
            nodes_created += 1
            
            # Connect to parent
            if parent_node_id:
                self.create_tendril(
                    from_node_id=parent_node_id,
                    to_node_id=dir_node.node_id,
                    connection_type="contains",
                    strength=0.8
                )
                tendrils_created += 1
            
            try:
                for item in dir_path.iterdir():
                    if item.is_dir():
                        explore_directory(item, depth + 1, dir_node.node_id)
                    elif item.is_file():
                        # Create node for file
                        file_node = self.create_node(
                            path=item,
                            node_type="file",
                            metadata={
                                "size": item.stat().st_size,
                                "extension": item.suffix,
                                "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                            }
                        )
                        nodes_created += 1
                        
                        # Connect file to directory
                        self.create_tendril(
                            from_node_id=dir_node.node_id,
                            to_node_id=file_node.node_id,
                            connection_type="contains",
                            strength=0.9
                        )
                        tendrils_created += 1
            except (PermissionError, OSError):
                pass
        
        # Start exploration from realm root
        if self.realm_path.exists():
            explore_directory(self.realm_path, depth=0)
        
        self._save_network()
        
        stats = self.get_network_stats()
        
        print(f"      ✅ Network built: {nodes_created} nodes, {tendrils_created} tendrils")
        
        return {
            "success": True,
            "nodes_created": nodes_created,
            "tendrils_created": tendrils_created,
            "network_stats": stats
        }
