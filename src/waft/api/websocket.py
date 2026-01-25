"""
WebSocket Support for Real-Time Evolution Monitoring.

Provides live updates for:
- Agent spawning/death events
- Fitness evaluations
- Mutation events
- Population statistics
- Battle royale matches
"""

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable
from uuid import uuid4

from fastapi import WebSocket, WebSocketDisconnect


class EventType(str, Enum):
    """Types of real-time events."""

    # Evolution events
    AGENT_SPAWN = "agent_spawn"
    AGENT_DEATH = "agent_death"
    AGENT_MUTATE = "agent_mutate"
    AGENT_CROSSOVER = "agent_crossover"
    FITNESS_UPDATE = "fitness_update"
    GENERATION_COMPLETE = "generation_complete"

    # Battle events
    BATTLE_START = "battle_start"
    BATTLE_ROUND = "battle_round"
    BATTLE_END = "battle_end"
    BATTLE_DAMAGE = "battle_damage"

    # System events
    POPULATION_UPDATE = "population_update"
    SYSTEM_STATUS = "system_status"
    ERROR = "error"

    # User interaction
    PING = "ping"
    PONG = "pong"


@dataclass
class EvolutionEvent:
    """An event in the evolution system."""

    event_type: EventType
    payload: dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    event_id: str = field(default_factory=lambda: str(uuid4())[:8])

    def to_json(self) -> str:
        return json.dumps(
            {
                "event_type": self.event_type.value,
                "event_id": self.event_id,
                "timestamp": self.timestamp.isoformat(),
                "payload": self.payload,
            }
        )


class ConnectionManager:
    """
    Manages WebSocket connections for real-time evolution monitoring.

    Supports:
    - Multiple concurrent connections
    - Channel-based subscriptions
    - Broadcast and targeted messaging
    - Connection health monitoring
    """

    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.subscriptions: dict[str, set[str]] = {}  # channel -> connection_ids
        self.connection_metadata: dict[str, dict] = {}
        self._event_handlers: dict[EventType, list[Callable]] = {}

    async def connect(self, websocket: WebSocket, client_id: str | None = None) -> str:
        """
        Accept a new WebSocket connection.

        Args:
            websocket: The WebSocket connection
            client_id: Optional client identifier

        Returns:
            Connection ID
        """
        await websocket.accept()

        connection_id = client_id or str(uuid4())[:12]
        self.active_connections[connection_id] = websocket
        self.connection_metadata[connection_id] = {
            "connected_at": datetime.utcnow().isoformat(),
            "subscriptions": [],
            "message_count": 0,
        }

        # Send welcome message
        await self.send_personal_message(
            connection_id,
            EvolutionEvent(
                event_type=EventType.SYSTEM_STATUS,
                payload={
                    "status": "connected",
                    "connection_id": connection_id,
                    "message": "Welcome to WAFT Evolution Stream",
                    "available_channels": [
                        "evolution",
                        "battles",
                        "population",
                        "fitness",
                        "all",
                    ],
                },
            ),
        )

        return connection_id

    def disconnect(self, connection_id: str):
        """Disconnect a client and clean up subscriptions."""
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]

        if connection_id in self.connection_metadata:
            del self.connection_metadata[connection_id]

        # Remove from all subscriptions
        for channel in self.subscriptions:
            self.subscriptions[channel].discard(connection_id)

    async def subscribe(self, connection_id: str, channel: str):
        """Subscribe a connection to a channel."""
        if channel not in self.subscriptions:
            self.subscriptions[channel] = set()

        self.subscriptions[channel].add(connection_id)

        if connection_id in self.connection_metadata:
            self.connection_metadata[connection_id]["subscriptions"].append(channel)

        await self.send_personal_message(
            connection_id,
            EvolutionEvent(
                event_type=EventType.SYSTEM_STATUS,
                payload={
                    "status": "subscribed",
                    "channel": channel,
                },
            ),
        )

    async def unsubscribe(self, connection_id: str, channel: str):
        """Unsubscribe a connection from a channel."""
        if channel in self.subscriptions:
            self.subscriptions[channel].discard(connection_id)

    async def send_personal_message(self, connection_id: str, event: EvolutionEvent):
        """Send a message to a specific connection."""
        if connection_id in self.active_connections:
            websocket = self.active_connections[connection_id]
            try:
                await websocket.send_text(event.to_json())
                if connection_id in self.connection_metadata:
                    self.connection_metadata[connection_id]["message_count"] += 1
            except Exception:
                self.disconnect(connection_id)

    async def broadcast(self, event: EvolutionEvent, channel: str = "all"):
        """Broadcast an event to all subscribers of a channel."""
        target_connections = set()

        if channel == "all":
            target_connections = set(self.active_connections.keys())
        elif channel in self.subscriptions:
            target_connections = self.subscriptions[channel]

        disconnected = []
        for connection_id in target_connections:
            if connection_id in self.active_connections:
                try:
                    await self.active_connections[connection_id].send_text(event.to_json())
                except Exception:
                    disconnected.append(connection_id)

        # Clean up disconnected clients
        for conn_id in disconnected:
            self.disconnect(conn_id)

    async def broadcast_to_all(self, event: EvolutionEvent):
        """Broadcast to all connected clients."""
        await self.broadcast(event, "all")

    def register_handler(self, event_type: EventType, handler: Callable):
        """Register a handler for an event type."""
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        self._event_handlers[event_type].append(handler)

    async def handle_message(self, connection_id: str, message: str):
        """Process an incoming message from a client."""
        try:
            data = json.loads(message)
            event_type = data.get("event_type", "")

            if event_type == "ping":
                await self.send_personal_message(
                    connection_id,
                    EvolutionEvent(
                        event_type=EventType.PONG,
                        payload={"timestamp": datetime.utcnow().isoformat()},
                    ),
                )

            elif event_type == "subscribe":
                channel = data.get("channel", "all")
                await self.subscribe(connection_id, channel)

            elif event_type == "unsubscribe":
                channel = data.get("channel", "all")
                await self.unsubscribe(connection_id, channel)

            # Trigger registered handlers
            if event_type in self._event_handlers:
                for handler in self._event_handlers[event_type]:
                    await handler(connection_id, data)

        except json.JSONDecodeError:
            await self.send_personal_message(
                connection_id,
                EvolutionEvent(
                    event_type=EventType.ERROR,
                    payload={"error": "Invalid JSON message"},
                ),
            )

    def get_stats(self) -> dict:
        """Get connection statistics."""
        return {
            "active_connections": len(self.active_connections),
            "channels": {
                channel: len(subs) for channel, subs in self.subscriptions.items()
            },
            "total_messages": sum(
                meta.get("message_count", 0)
                for meta in self.connection_metadata.values()
            ),
        }


# Global connection manager instance
manager = ConnectionManager()


# Evolution event emitters
async def emit_agent_spawn(agent_data: dict):
    """Emit agent spawn event."""
    event = EvolutionEvent(
        event_type=EventType.AGENT_SPAWN,
        payload=agent_data,
    )
    await manager.broadcast(event, "evolution")
    await manager.broadcast(event, "all")


async def emit_agent_death(agent_id: str, cause: str = "fitness"):
    """Emit agent death event."""
    event = EvolutionEvent(
        event_type=EventType.AGENT_DEATH,
        payload={"agent_id": agent_id, "cause": cause},
    )
    await manager.broadcast(event, "evolution")
    await manager.broadcast(event, "all")


async def emit_mutation(agent_id: str, mutations: dict):
    """Emit mutation event."""
    event = EvolutionEvent(
        event_type=EventType.AGENT_MUTATE,
        payload={"agent_id": agent_id, "mutations": mutations},
    )
    await manager.broadcast(event, "evolution")


async def emit_crossover(parent_a: str, parent_b: str, offspring: str):
    """Emit crossover event."""
    event = EvolutionEvent(
        event_type=EventType.AGENT_CROSSOVER,
        payload={
            "parent_a": parent_a,
            "parent_b": parent_b,
            "offspring": offspring,
        },
    )
    await manager.broadcast(event, "evolution")


async def emit_fitness_update(agent_id: str, fitness: float, metrics: dict):
    """Emit fitness update event."""
    event = EvolutionEvent(
        event_type=EventType.FITNESS_UPDATE,
        payload={
            "agent_id": agent_id,
            "fitness": fitness,
            "metrics": metrics,
        },
    )
    await manager.broadcast(event, "fitness")
    await manager.broadcast(event, "evolution")


async def emit_generation_complete(generation: int, stats: dict):
    """Emit generation complete event."""
    event = EvolutionEvent(
        event_type=EventType.GENERATION_COMPLETE,
        payload={
            "generation": generation,
            "stats": stats,
        },
    )
    await manager.broadcast(event, "evolution")
    await manager.broadcast(event, "all")


async def emit_population_update(population_data: dict):
    """Emit population statistics update."""
    event = EvolutionEvent(
        event_type=EventType.POPULATION_UPDATE,
        payload=population_data,
    )
    await manager.broadcast(event, "population")


# Battle event emitters
async def emit_battle_start(battle_id: str, participants: list[dict]):
    """Emit battle start event."""
    event = EvolutionEvent(
        event_type=EventType.BATTLE_START,
        payload={
            "battle_id": battle_id,
            "participants": participants,
        },
    )
    await manager.broadcast(event, "battles")
    await manager.broadcast(event, "all")


async def emit_battle_round(battle_id: str, round_num: int, actions: list[dict]):
    """Emit battle round event."""
    event = EvolutionEvent(
        event_type=EventType.BATTLE_ROUND,
        payload={
            "battle_id": battle_id,
            "round": round_num,
            "actions": actions,
        },
    )
    await manager.broadcast(event, "battles")


async def emit_battle_damage(battle_id: str, attacker: str, target: str, damage: float):
    """Emit damage event in battle."""
    event = EvolutionEvent(
        event_type=EventType.BATTLE_DAMAGE,
        payload={
            "battle_id": battle_id,
            "attacker": attacker,
            "target": target,
            "damage": damage,
        },
    )
    await manager.broadcast(event, "battles")


async def emit_battle_end(battle_id: str, winner: str, results: dict):
    """Emit battle end event."""
    event = EvolutionEvent(
        event_type=EventType.BATTLE_END,
        payload={
            "battle_id": battle_id,
            "winner": winner,
            "results": results,
        },
    )
    await manager.broadcast(event, "battles")
    await manager.broadcast(event, "all")


# WebSocket endpoint handler
async def websocket_endpoint(websocket: WebSocket, client_id: str | None = None):
    """
    WebSocket endpoint for real-time evolution monitoring.

    Usage:
        ws://localhost:8000/ws/evolution
        ws://localhost:8000/ws/evolution?client_id=my-client

    Subscribe to channels by sending:
        {"event_type": "subscribe", "channel": "evolution"}

    Available channels:
        - evolution: All evolution events
        - battles: Battle royale events
        - population: Population statistics
        - fitness: Fitness updates
        - all: All events
    """
    connection_id = await manager.connect(websocket, client_id)

    try:
        while True:
            message = await websocket.receive_text()
            await manager.handle_message(connection_id, message)
    except WebSocketDisconnect:
        manager.disconnect(connection_id)
