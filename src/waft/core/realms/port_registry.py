"""
Port Registry: Maps Realm names to ports to prevent collisions.

Every Realm gets its own port for its PocketBase server.
"""
import json
import logging
from pathlib import Path
from typing import Dict

logger = logging.getLogger(__name__)

# Default port assignments for PocketBase Realms
DEFAULT_PORTS: Dict[str, int] = {
    "daily_learning_realm": 8090,
    "library_realm": 8091,
    "security_realm": 8080,  # The Gatekeeper
    "core_realm": 8092,  # Main Core Database (The One's realm)
    "demo_realm": 8095,  # Demo realm for Observatory walkthrough
}

# Service ports for non-PocketBase services (Gods, Engines, etc.)
SERVICE_PORTS: Dict[str, int] = {
    "campfire": 5000,       # TheCampfire storytelling
    "observatory": 2077,    # O.D.D. Observatory mesh monitor
    "dialectic_realm": 2112,  # DIALECTIC Analysis Engine
}

# Port range: 8080-8999 (reserved for WAFT PocketBase Realms)
MIN_PORT = 8080
MAX_PORT = 8999


class PortRegistry:
    """Manages port assignments for Realms."""

    def __init__(self, project_path: Path):
        """
        Initialize port registry.

        Args:
            project_path: Path to project root
        """
        self.project_path = Path(project_path).resolve()
        self.registry_path = self.project_path / "src" / "waft" / "core" / "realms" / "port_registry.json"
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)

        # Load or initialize registry
        if self.registry_path.exists():
            with open(self.registry_path, "r", encoding="utf-8") as f:
                self.ports: Dict[str, int] = json.load(f)
        else:
            self.ports = DEFAULT_PORTS.copy()
            self._save()

    def _save(self):
        """Save registry to disk."""
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(self.ports, f, indent=2)

    def get_port(self, realm_name: str) -> int:
        """
        Get port for a Realm, assigning one if it doesn't exist.

        Args:
            realm_name: Name of the Realm

        Returns:
            Port number
        """
        if realm_name in self.ports:
            return self.ports[realm_name]

        # Find next available port
        used_ports = set(self.ports.values())
        for port in range(MIN_PORT, MAX_PORT + 1):
            if port not in used_ports:
                self.ports[realm_name] = port
                self._save()
                logger.info(f"Assigned port {port} to Realm '{realm_name}'")
                return port

        raise RuntimeError(f"No available ports in range {MIN_PORT}-{MAX_PORT}")

    def register(self, realm_name: str, port: int):
        """
        Manually register a Realm with a specific port.

        Args:
            realm_name: Name of the Realm
            port: Port number (must be in valid range)
        """
        if port < MIN_PORT or port > MAX_PORT:
            raise ValueError(f"Port {port} must be in range {MIN_PORT}-{MAX_PORT}")

        if realm_name in self.ports and self.ports[realm_name] != port:
            logger.warning(f"Realm '{realm_name}' already has port {self.ports[realm_name]}, changing to {port}")

        self.ports[realm_name] = port
        self._save()

    def get_all_ports(self) -> Dict[str, int]:
        """Get all registered realm ports."""
        return self.ports.copy()

    def get_service_port(self, service_name: str) -> int | None:
        """
        Get port for a service (non-PocketBase).

        Args:
            service_name: Name of the service

        Returns:
            Port number or None if not found
        """
        return SERVICE_PORTS.get(service_name)

    def get_all_service_ports(self) -> Dict[str, int]:
        """Get all registered service ports."""
        return SERVICE_PORTS.copy()

    def get_all_known_ports(self) -> Dict[str, int]:
        """Get all ports (realms + services)."""
        all_ports = self.ports.copy()
        all_ports.update(SERVICE_PORTS)
        return all_ports
