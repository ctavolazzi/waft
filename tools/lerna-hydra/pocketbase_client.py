"""PocketBase client — session and transmission persistence.

Talks to PocketBase REST API for storing session info and
agent transmissions (prompt, thoughts, response).
"""
import json
import logging
import time
from typing import Any, Optional

import httpx

logger = logging.getLogger("lerna-hydra.pocketbase")

DEFAULT_PB_URL = "http://127.0.0.1:8090"


class PocketBaseClient:
    """Async client for PocketBase REST API."""

    def __init__(self, base_url: str = DEFAULT_PB_URL):
        self.base_url = base_url.rstrip("/")
        self.api = f"{self.base_url}/api/collections"

    async def health_check(self) -> bool:
        """Check if PocketBase is reachable."""
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(f"{self.base_url}/api/health")
                return resp.status_code == 200
        except Exception:
            return False

    async def create_session(self, session_data: dict[str, Any]) -> Optional[dict]:
        """Store a new session record.

        session_data should include:
            - sandbox_path: str
            - llama_url: str
            - model_name: str
            - started_at: str (ISO timestamp)
            - status: str ("running", "stopped")
        """
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(
                    f"{self.api}/sessions/records",
                    json=session_data,
                )
                if resp.status_code in (200, 201):
                    record = resp.json()
                    logger.info(f"Session stored: {record.get('id')}")
                    return record
                else:
                    logger.warning(f"PB session create failed: {resp.status_code} {resp.text}")
                    return None
        except Exception as e:
            logger.warning(f"PB session create error: {e}")
            return None

    async def update_session(self, record_id: str, data: dict[str, Any]) -> Optional[dict]:
        """Update an existing session record."""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.patch(
                    f"{self.api}/sessions/records/{record_id}",
                    json=data,
                )
                if resp.status_code == 200:
                    return resp.json()
                return None
        except Exception:
            return None

    async def create_transmission(self, data: dict[str, Any]) -> Optional[dict]:
        """Store a transmission (one agent loop iteration).

        data should include:
            - session_id: str (PB record ID)
            - step: int
            - prompt: str (observation sent to model)
            - thoughts: str (reasoning_content)
            - response: str (content)
            - actions: str (JSON of parsed actions)
            - results: str (JSON of action results)
        """
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(
                    f"{self.api}/transmissions/records",
                    json=data,
                )
                if resp.status_code in (200, 201):
                    return resp.json()
                return None
        except Exception as e:
            logger.warning(f"PB transmission create error: {e}")
            return None

    async def update_transmission(self, record_id: str, data: dict[str, Any]) -> Optional[dict]:
        """Update a transmission record (streaming updates)."""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.patch(
                    f"{self.api}/transmissions/records/{record_id}",
                    json=data,
                )
                if resp.status_code == 200:
                    return resp.json()
                return None
        except Exception:
            return None
