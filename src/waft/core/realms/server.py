"""
RealmServer: Manages PocketBase server lifecycle for a Realm.

Each Realm is an active PocketBase server running on its own port.
"""
import atexit
import json
import logging
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, Optional

from .pocketbase_downloader import download_pocketbase, verify_pocketbase
from .port_registry import PortRegistry

logger = logging.getLogger(__name__)


class RealmServer:
    """
    Manages a PocketBase server instance for a Realm.

    Responsibilities:
    - Spawn PocketBase subprocess
    - Monitor process health
    - Bootstrap admin user
    - Manage data directory isolation
    """

    def __init__(self, realm_name: str, project_path: Path, lazy: bool = False):
        """
        Initialize RealmServer.

        Args:
            realm_name: Name of the Realm
            project_path: Path to project root
            lazy: If True, don't start server until explicitly requested
        """
        self.realm_name = realm_name
        self.project_path = Path(project_path).resolve()
        self.lazy = lazy

        # Get port from registry
        port_registry = PortRegistry(self.project_path)
        self.port = port_registry.get_port(realm_name)

        # Setup directories
        self.realm_path = self.project_path / "_realms" / realm_name
        self.data_dir = self.realm_path / "pb_data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Get PocketBase binary
        self.binary_path = download_pocketbase(self.project_path)
        if not verify_pocketbase(self.binary_path):
            raise RuntimeError("PocketBase binary verification failed")

        # Process management
        self.process: Optional[subprocess.Popen] = None
        self.base_url = f"http://localhost:{self.port}"

        # Admin credentials (stored in realm config)
        self.config_path = self.realm_path / "realm_config.json"
        self._load_config()

        # Register cleanup handler to prevent zombie processes
        atexit.register(self._cleanup_on_exit)

    def _load_config(self):
        """Load or initialize realm configuration."""
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.config = {
                "admin_email": f"admin@{self.realm_name}.local",
                "admin_password": None,  # Will be set during bootstrap
                "bootstrapped": False,
            }
            self._save_config()

    def _save_config(self):
        """Save realm configuration."""
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2)

    def start(self) -> bool:
        """
        Start the PocketBase server.

        CRITICAL: Bootstrap admin BEFORE starting server to avoid auth failures.

        Returns:
            True if server started successfully
        """
        if self.process and self.process.poll() is None:
            logger.info(f"Realm '{self.realm_name}' server already running on port {self.port}")
            return True

        logger.info(f"Starting Realm '{self.realm_name}' server on port {self.port}...")

        # CRITICAL: Bootstrap admin BEFORE starting server
        # This ensures the admin exists before any API calls are made
        if not self.config.get("bootstrapped", False):
            logger.info("Bootstrapping admin user before server start...")
            if not self.bootstrap():
                logger.error("Bootstrap failed - server may not accept API calls")
                logger.warning(f"Manual fix: Open {self.base_url}/_/ after server starts")

        # Build command
        cmd = [
            str(self.binary_path),
            "serve",
            "--dir",
            str(self.data_dir),
            "--http",
            f"127.0.0.1:{self.port}",
        ]

        try:
            # Start process (detached, redirect output to log file)
            log_file = self.realm_path / "pocketbase.log"
            with open(log_file, "a", encoding="utf-8") as log:
                self.process = subprocess.Popen(
                    cmd,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    cwd=str(self.data_dir),
                )

            # Wait a moment for server to start
            time.sleep(2)

            # Check if process is still running
            if self.process.poll() is not None:
                logger.error(f"Realm '{self.realm_name}' server failed to start (exit code: {self.process.returncode})")
                # Check log file for errors
                if log_file.exists():
                    with open(log_file, "r", encoding="utf-8") as f:
                        log_content = f.read()
                        if "address already in use" in log_content.lower():
                            logger.error(f"Port {self.port} is already in use!")
                            logger.info("Run 'pkill pocketbase' to kill zombie processes")
                return False

            logger.info(f"Realm '{self.realm_name}' server running at {self.base_url}")
            logger.info(f"Admin UI: {self.base_url}/_/")
            return True

        except Exception as e:
            logger.error(f"Failed to start Realm '{self.realm_name}' server: {e}")
            return False

    def bootstrap(self) -> bool:
        """
        Bootstrap admin user (first-time setup).

        CRITICAL: Uses PocketBase `superuser upsert` command to create admin.
        This MUST run before any API calls, or authentication will fail.

        Returns:
            True if bootstrap successful
        """
        if self.config.get("bootstrapped", False):
            logger.info(f"Realm '{self.realm_name}' already bootstrapped")
            return True

        logger.info(f"Bootstrapping Realm '{self.realm_name}'...")

        # Generate admin password if not set
        if not self.config.get("admin_password"):
            import secrets

            self.config["admin_password"] = secrets.token_urlsafe(16)
            self._save_config()

        # CRITICAL: Use PocketBase `superuser upsert` command (v0.22+)
        # This creates the admin account BEFORE the server starts accepting API calls
        try:
            cmd = [
                str(self.binary_path),
                "superuser",
                "upsert",
                self.config["admin_email"],
                self.config["admin_password"],
                "--dir",
                str(self.data_dir),
            ]

            logger.info(f"Creating admin user: {self.config['admin_email']}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:
                logger.error(f"Failed to create admin user: {result.stderr}")
                logger.warning(f"Manual setup required: Open {self.base_url}/_/ and create admin")
                return False

            logger.info("Admin user created successfully")
            self.config["bootstrapped"] = True
            self._save_config()

            logger.info(f"Realm '{self.realm_name}' bootstrap complete")
            logger.info(f"Admin email: {self.config['admin_email']}")
            logger.info(f"Admin UI: {self.base_url}/_/")

            return True

        except subprocess.TimeoutExpired:
            logger.error("Bootstrap command timed out")
            return False
        except Exception as e:
            logger.error(f"Bootstrap failed: {e}")
            logger.warning(f"Manual setup required: Open {self.base_url}/_/ and create admin")
            return False

    def stop(self):
        """Stop the PocketBase server."""
        if self.process:
            logger.info(f"Stopping Realm '{self.realm_name}' server...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.warning(f"Realm '{self.realm_name}' server didn't stop gracefully, killing...")
                self.process.kill()
                self.process.wait()
            self.process = None
            logger.info(f"Realm '{self.realm_name}' server stopped")

    def _cleanup_on_exit(self):
        """
        Cleanup handler registered with atexit.

        Prevents zombie processes if Python script crashes or is force-quit.
        """
        if self.process and self.process.poll() is None:
            logger.warning(f"Cleaning up zombie process for Realm '{self.realm_name}'...")
            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except (subprocess.TimeoutExpired, Exception):
                try:
                    self.process.kill()
                    self.process.wait()
                except Exception:
                    pass
            self.process = None

    def is_running(self) -> bool:
        """Check if server is running."""
        if not self.process:
            return False
        return self.process.poll() is None

    def get_status(self) -> Dict[str, Any]:
        """Get server status."""
        return {
            "realm_name": self.realm_name,
            "port": self.port,
            "base_url": self.base_url,
            "running": self.is_running(),
            "data_dir": str(self.data_dir),
            "bootstrapped": self.config.get("bootstrapped", False),
        }
