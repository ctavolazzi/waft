"""
PocketBaseInventory: HTTP REST client for storing Packrat's backpack items.

The Packrat no longer touches files directly - it makes network requests.
This teaches the concept of API Contracts.
"""
import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx

logger = logging.getLogger(__name__)

# Collection name for inventory
INVENTORY_COLLECTION = "inventory"


class PocketBaseInventory:
    """
    HTTP REST client for PocketBase Inventory collection.

    The Packrat stores items in its backpack via this client.
    """

    def __init__(self, base_url: str, admin_email: str, admin_password: str):
        """
        Initialize PocketBase client.

        Args:
            base_url: Base URL of PocketBase server (e.g., "http://localhost:8090")
            admin_email: Admin email for authentication
            admin_password: Admin password for authentication
        """
        self.base_url = base_url.rstrip("/")
        self.admin_email = admin_email
        self.admin_password = admin_password
        self.token: Optional[str] = None

        # HTTP client
        self.client = httpx.Client(timeout=30.0)

        # Authenticate
        self._authenticate()

        # Ensure collection exists
        self._ensure_collection()

    def _authenticate(self):
        """
        Authenticate with PocketBase admin API.

        CRITICAL: This will fail if admin user doesn't exist.
        Ensure RealmServer.bootstrap() runs BEFORE this.
        """
        try:
            response = self.client.post(
                f"{self.base_url}/api/admins/auth-with-password",
                json={
                    "identity": self.admin_email,
                    "password": self.admin_password,
                },
            )
            response.raise_for_status()
            data = response.json()
            self.token = data.get("token")
            if not self.token:
                raise RuntimeError("Failed to get auth token")

            # Set auth header for future requests
            self.client.headers.update({"Authorization": f"Bearer {self.token}"})
            logger.info(f"Authenticated with PocketBase at {self.base_url}")

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403 or e.response.status_code == 400:
                logger.error(
                    f"Authentication failed (403/400). Admin user may not exist.\n"
                    f"Fix: Open {self.base_url}/_/ and create admin manually, or check bootstrap logs."
                )
            raise
        except Exception as e:
            logger.error(f"Failed to authenticate with PocketBase: {e}")
            logger.error(f"Server may not be running or admin not created. Check: {self.base_url}/_/")
            raise

    def _ensure_collection(self):
        """Ensure the inventory collection exists with proper schema."""
        try:
            # Check if collection exists
            response = self.client.get(
                f"{self.base_url}/api/collections/{INVENTORY_COLLECTION}",
            )

            if response.status_code == 404:
                # Create collection
                logger.info(f"Creating '{INVENTORY_COLLECTION}' collection...")
                schema = {
                    "name": INVENTORY_COLLECTION,
                    "type": "base",
                    "schema": [
                        {
                            "name": "item_id",
                            "type": "text",
                            "required": True,
                            "unique": True,
                        },
                        {
                            "name": "source",
                            "type": "text",
                            "required": True,
                        },
                        {
                            "name": "payload",
                            "type": "json",
                            "required": True,
                        },
                        {
                            "name": "weight",
                            "type": "number",
                            "required": False,
                        },
                        {
                            "name": "pocket",
                            "type": "text",
                            "required": False,
                        },
                        {
                            "name": "collected_at",
                            "type": "date",
                            "required": True,
                        },
                    ],
                }

                response = self.client.post(
                    f"{self.base_url}/api/collections",
                    json=schema,
                )
                response.raise_for_status()
                logger.info(f"Created '{INVENTORY_COLLECTION}' collection")

            else:
                response.raise_for_status()
                logger.debug(f"Collection '{INVENTORY_COLLECTION}' already exists")

        except Exception as e:
            logger.error(f"Failed to ensure collection: {e}")
            raise

    def add_item(
        self,
        source: str,
        payload: Dict[str, Any],
        weight: float = 1.0,
        pocket: str = "main",
    ) -> str:
        """
        Add an item to the inventory.

        Args:
            source: Source name (empirica, chronicler, session)
            payload: Item data
            weight: Item weight (for sorting/filtering)
            pocket: Pocket name (for organization)

        Returns:
            Item ID
        """
        item_id = str(uuid.uuid4())

        record = {
            "item_id": item_id,
            "source": source,
            "payload": payload,
            "weight": weight,
            "pocket": pocket,
            "collected_at": datetime.now().isoformat(),
        }

        try:
            response = self.client.post(
                f"{self.base_url}/api/collections/{INVENTORY_COLLECTION}/records",
                json=record,
            )
            response.raise_for_status()
            logger.debug(f"Added item {item_id} from {source} to {pocket} pocket")
            return item_id

        except Exception as e:
            logger.error(f"Failed to add item: {e}")
            raise

    def get_items(
        self,
        source: Optional[str] = None,
        pocket: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Get items from inventory.

        Args:
            source: Filter by source
            pocket: Filter by pocket
            limit: Maximum number of items to return

        Returns:
            List of items
        """
        params = {"perPage": limit, "sort": "-collected_at"}

        if source:
            params["filter"] = f'source = "{source}"'
        if pocket:
            if "filter" in params:
                params["filter"] += f' && pocket = "{pocket}"'
            else:
                params["filter"] = f'pocket = "{pocket}"'

        try:
            response = self.client.get(
                f"{self.base_url}/api/collections/{INVENTORY_COLLECTION}/records",
                params=params,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("items", [])

        except Exception as e:
            logger.error(f"Failed to get items: {e}")
            raise

    def get_latest_items(self, source: Optional[str] = None, count: int = 1) -> List[Dict[str, Any]]:
        """
        Get latest items from a source.

        Args:
            source: Source name
            count: Number of latest items

        Returns:
            List of latest items
        """
        items = self.get_items(source=source, limit=count)
        return items[:count]

    def close(self):
        """Close HTTP client."""
        self.client.close()
