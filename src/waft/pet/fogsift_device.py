#!/usr/bin/env python3
"""
FogSift Device Simulator

Simulates a physical FogSift device that can link with others.
Run multiple instances to test the linking protocol.

Usage:
    # Terminal 1: Device on port 5001
    python fogsift_device.py --port 5001 --name Luna

    # Terminal 2: Device on port 5002, link to 5001
    python fogsift_device.py --port 5002 --name Orion --link 5001

When devices link:
- Creatures detect each other
- They can visit the neighboring screen
- Social stats boost for both
"""

import argparse
import json
import os
import socket
import sys
import threading
import time
from dataclasses import dataclass
from typing import Optional

try:
    from .fogsift_creature import FogSiftCreature, create_starter, STARTER_SPECIES
except ImportError:
    from fogsift_creature import FogSiftCreature, create_starter, STARTER_SPECIES


@dataclass
class DeviceState:
    """State shared between linked devices."""
    creature_id: str
    creature_name: str
    creature_species: str
    creature_emotion: str
    creature_position: float  # 0.0 = left edge, 1.0 = right edge
    is_visiting: bool  # True if creature is on the other device's screen


class FogSiftDevice:
    """
    Simulates a FogSift hardware device.

    Features:
    - Runs a creature simulation
    - Listens for incoming links (like magnetic connection)
    - Can connect to other devices
    - Exchanges creature state for cross-screen interaction
    """

    def __init__(self, port: int, creature_name: str = None, creature_species: str = "PixelFox"):
        self.port = port
        self.creature = create_starter(creature_species, creature_name or f"Pet_{port}")
        self.creature.age_hours = 2  # Skip egg for demo
        self.creature.tick(0)

        # Networking
        self.server_socket: Optional[socket.socket] = None
        self.connected_device: Optional[socket.socket] = None
        self.connected_port: Optional[int] = None

        # State
        self.running = True
        self.neighbor_state: Optional[DeviceState] = None
        self.creature_position = 0.5  # Center of screen
        self.creature_visiting_neighbor = False

        # Threading
        self.lock = threading.Lock()

    def start_server(self):
        """Start listening for incoming connections."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('127.0.0.1', self.port))
        self.server_socket.listen(1)
        self.server_socket.settimeout(0.5)  # Non-blocking accept

        thread = threading.Thread(target=self._accept_connections, daemon=True)
        thread.start()

    def _accept_connections(self):
        """Accept incoming connections (runs in thread)."""
        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                with self.lock:
                    if self.connected_device is None:
                        self.connected_device = conn
                        self.connected_port = addr[1]
                        self._on_link_established()
                        # Start receiving from this connection
                        thread = threading.Thread(target=self._receive_loop, args=(conn,), daemon=True)
                        thread.start()
                    else:
                        conn.close()  # Already connected
            except socket.timeout:
                continue
            except OSError:
                break

    def connect_to(self, target_port: int) -> bool:
        """Connect to another device (initiates the link)."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('127.0.0.1', target_port))
            with self.lock:
                self.connected_device = sock
                self.connected_port = target_port
            self._on_link_established()

            # Start receiving
            thread = threading.Thread(target=self._receive_loop, args=(sock,), daemon=True)
            thread.start()
            return True
        except (ConnectionRefusedError, OSError):
            return False

    def _on_link_established(self):
        """Called when a link is established."""
        self.creature.is_linked = True
        self.creature.social = min(100, self.creature.social + 20)
        self.creature.mood = min(100, self.creature.mood + 10)

    def _on_link_broken(self):
        """Called when a link is broken."""
        self.creature.is_linked = False
        self.neighbor_state = None
        self.creature_visiting_neighbor = False
        self.creature_position = 0.5

    def _receive_loop(self, sock: socket.socket):
        """Receive state updates from connected device."""
        buffer = ""
        while self.running:
            try:
                data = sock.recv(4096).decode('utf-8')
                if not data:
                    break
                buffer += data

                # Process complete JSON messages
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line.strip():
                        try:
                            state_data = json.loads(line)
                            with self.lock:
                                self.neighbor_state = DeviceState(**state_data)
                        except json.JSONDecodeError:
                            pass
            except (OSError, ConnectionResetError):
                break

        # Connection lost
        with self.lock:
            self.connected_device = None
            self._on_link_broken()

    def send_state(self):
        """Send current state to connected device."""
        if self.connected_device is None:
            return

        state = DeviceState(
            creature_id=self.creature.creature_id,
            creature_name=self.creature.name,
            creature_species=self.creature.species,
            creature_emotion=self.creature.get_emotion(),
            creature_position=self.creature_position,
            is_visiting=self.creature_visiting_neighbor,
        )

        try:
            msg = json.dumps(state.__dict__) + '\n'
            self.connected_device.sendall(msg.encode('utf-8'))
        except (OSError, BrokenPipeError):
            with self.lock:
                self.connected_device = None
                self._on_link_broken()

    def update_creature_position(self):
        """
        Update creature position based on mood and neighbor presence.
        Creatures naturally wander, and may visit neighbors.
        """
        import random

        # Base wandering
        self.creature_position += random.uniform(-0.05, 0.05)

        # If neighbor exists and creature is social, drift toward edge
        if self.neighbor_state and self.creature.mood > 50:
            if self.creature_position > 0.5:
                self.creature_position += 0.02  # Drift toward right (neighbor)
            else:
                self.creature_position -= 0.02  # Or left

        # Check if creature crosses to neighbor
        if self.creature_position > 1.0:
            self.creature_visiting_neighbor = True
            self.creature_position = 0.0  # Appear on left of neighbor's screen
        elif self.creature_position < 0.0:
            self.creature_visiting_neighbor = True
            self.creature_position = 1.0  # Appear on right of neighbor's screen
        else:
            self.creature_visiting_neighbor = False

        # Clamp position
        self.creature_position = max(0.0, min(1.0, self.creature_position))

    def render(self) -> str:
        """Render the device display."""
        lines = []

        width = 40
        lines.append("╔" + "═" * width + "╗")
        lines.append(f"║ Device :{self.port:<5} {self.creature.name:>25} ║")
        lines.append("╠" + "═" * width + "╣")

        # Connection status
        if self.connected_device:
            lines.append(f"║ 🔗 LINKED to :{self.connected_port:<24} ║")
        else:
            lines.append(f"║ ○ Not linked{' ' * 26}║")

        lines.append("╠" + "═" * width + "╣")

        # Screen area (where creatures appear)
        screen_width = width - 2

        # Draw creature at its position
        creature_pos = int(self.creature_position * (screen_width - 4))
        visitor_pos = None

        # Check if neighbor's creature is visiting us
        if self.neighbor_state and self.neighbor_state.is_visiting:
            visitor_pos = int(self.neighbor_state.creature_position * (screen_width - 4))

        # Build screen rows
        for row in range(4):
            line = [' '] * screen_width

            # Draw our creature (if not visiting neighbor)
            if not self.creature_visiting_neighbor:
                sprites = self._get_creature_sprite(self.creature.get_emotion())
                if row < len(sprites):
                    sprite = sprites[row]
                    for i, c in enumerate(sprite):
                        if 0 <= creature_pos + i < screen_width:
                            line[creature_pos + i] = c

            # Draw visiting creature
            if visitor_pos is not None and self.neighbor_state:
                visitor_sprites = self._get_creature_sprite(self.neighbor_state.creature_emotion)
                if row < len(visitor_sprites):
                    sprite = visitor_sprites[row]
                    for i, c in enumerate(sprite):
                        if 0 <= visitor_pos + i < screen_width:
                            line[visitor_pos + i] = c

            lines.append("║ " + ''.join(line) + " ║")

        lines.append("╠" + "═" * width + "╣")

        # Stats
        def bar(v): return "█" * int(v / 10) + "░" * (10 - int(v / 10))
        lines.append(f"║ HGR [{bar(self.creature.hunger)}] {self.creature.hunger:5.0f} ║")
        lines.append(f"║ NRG [{bar(self.creature.energy)}] {self.creature.energy:5.0f} ║")
        lines.append(f"║ MOD [{bar(self.creature.mood)}] {self.creature.mood:5.0f} ║")
        lines.append(f"║ SOC [{bar(self.creature.social)}] {self.creature.social:5.0f} ║")

        lines.append("╠" + "═" * width + "╣")

        # Status
        status = self.creature.get_emotion()
        visiting = "→ VISITING" if self.creature_visiting_neighbor else ""
        guest = f"← GUEST: {self.neighbor_state.creature_name}" if (self.neighbor_state and self.neighbor_state.is_visiting) else ""
        lines.append(f"║ {status:<12} {visiting:<12} {guest:<12}║")

        lines.append("╚" + "═" * width + "╝")

        return '\n'.join(lines)

    def _get_creature_sprite(self, emotion: str) -> list[str]:
        """Get simple sprite for emotion."""
        sprites = {
            "happy": ["/\\_/\\", "(^.^)", " > < "],
            "content": ["/\\_/\\", "(o.o)", " > < "],
            "sad": ["/\\_/\\", "(;.;)", " > < "],
            "sleeping": ["/\\_/\\", "(-.-)", " zzZ "],
            "hungry": ["/\\_/\\", "(o.o)", " >o< "],
            "tired": ["/\\_/\\", "(-.-)", " > < "],
        }
        return sprites.get(emotion, sprites["content"])

    def tick(self, hours: float = None):
        """Update simulation."""
        self.creature.tick(hours)
        self.update_creature_position()
        self.send_state()

    def stop(self):
        """Stop the device."""
        self.running = False
        if self.connected_device:
            self.connected_device.close()
        if self.server_socket:
            self.server_socket.close()


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    parser = argparse.ArgumentParser(description='FogSift Device Simulator')
    parser.add_argument('--port', type=int, default=5001, help='Port to listen on')
    parser.add_argument('--name', type=str, default=None, help='Creature name')
    parser.add_argument('--species', type=str, default='PixelFox', choices=list(STARTER_SPECIES.keys()))
    parser.add_argument('--link', type=int, default=None, help='Port to link to')
    args = parser.parse_args()

    device = FogSiftDevice(args.port, args.name, args.species)
    device.start_server()

    print(f"🔌 Device started on port {args.port}")

    if args.link:
        print(f"🔗 Connecting to port {args.link}...")
        if device.connect_to(args.link):
            print("✅ Linked!")
        else:
            print("❌ Failed to link")

    print("\nPress Ctrl+C to stop\n")
    time.sleep(1)

    try:
        while device.running:
            clear_screen()
            device.tick(0.01)  # Simulate time passing
            print(device.render())
            print("\n[F]eed  [P]lay  [Q]uit")
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass
    finally:
        device.stop()
        print("\n👋 Device stopped")


if __name__ == "__main__":
    main()
