"""
Continuous Game of Life Visualization with Movement and Coherence Pressure
Runs the pygame visualization continuously until you close the window.

Pressure System:
- Coherence: Internal state integrity that degrades over time
- Social Balance: Need 1-3 neighbors (too many = stress, too few = isolation)
- Territory: Need space to maintain coherence
- Movement: Essential - must move to prevent decay
"""

import asyncio
import sys
import pygame
import random
from pathlib import Path
from typing import Optional, Tuple

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.waft.core.agent.base import BaseAgent
from src.waft.core.agent.state import AgentConfig
from src.waft.core.world.biome import Biome, AbioticFactors
from src.waft.core.hub.dish import PetriDish
from src.waft.core.hub.lifecycle import TheSlicer, TheReaper
from src.waft.core.science.observer import TheObserver
from src.waft.core.hub.display import PygameBiomeEngine


def move_organism_in_dish(dish: PetriDish, organism_id: str, new_position: Tuple[int, int]) -> bool:
    """
    Move an organism to a new position in the dish.
    
    Args:
        dish: PetriDish containing the organism
        organism_id: ID of organism to move
        new_position: (x, y) target position
        
    Returns:
        True if moved successfully, False otherwise
    """
    # Validate new position
    x, y = new_position
    if x < 0 or x >= dish.width or y < 0 or y >= dish.height:
        return False
    
    # Check if target position is occupied
    if dish.lattice[new_position] is not None:
        return False
    
    # Find current position
    current_pos = None
    for pos, oid in dish.lattice.items():
        if oid == organism_id:
            current_pos = pos
            break
    
    if current_pos is None:
        return False
    
    # Move organism
    dish.lattice[current_pos] = None
    dish.lattice[new_position] = organism_id
    
    return True


class GameOfLifeOrganism(BaseAgent):
    """Organism with coherence-based pressure system."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Coherence: 0-100, degrades over time, restored by optimal conditions
        if not hasattr(self.state, 'coherence'):
            self.state.coherence = 80.0
        self.last_move_pulse = 0
        self.preferred_neighbors = random.randint(1, 3)  # Each organism prefers different social density
    
    async def observe(self):
        """Observe environment - check coherence, neighbors, space."""
        dish = getattr(self, '_current_dish', None)
        position = getattr(self, '_current_position', None)
        
        observations = {
            "coherence": self.state.coherence,
            "critical": self.state.coherence < 20.0,
            "unstable": self.state.coherence < 40.0,
            "position": position
        }
        
        if dish and position:
            # Count neighbors (radius 1 = 8 neighbors)
            neighborhood = dish.get_neighborhood(position, radius=1)
            neighbor_count = sum(1 for _, _, oid in neighborhood if oid is not None)
            observations["neighbor_count"] = neighbor_count
            
            # Check for empty spaces nearby (territory)
            empty_spaces = []
            for nx, ny, oid in neighborhood:
                if oid is None:
                    empty_spaces.append((nx, ny))
            observations["empty_spaces"] = empty_spaces
            observations["has_space"] = len(empty_spaces) > 0
            
            # Social pressure analysis
            optimal_neighbors = self.preferred_neighbors
            if neighbor_count < optimal_neighbors:
                observations["social_state"] = "isolated"
                observations["social_pressure"] = (optimal_neighbors - neighbor_count) * 5.0
            elif neighbor_count > optimal_neighbors + 2:
                observations["social_state"] = "crowded"
                observations["social_pressure"] = (neighbor_count - optimal_neighbors - 2) * 5.0
            else:
                observations["social_state"] = "optimal"
                observations["social_pressure"] = 0.0
        
        return observations
    
    async def decide(self, state):
        """Decide what to do based on coherence and social pressure."""
        coherence = state.get("coherence", 80.0)
        critical = state.get("critical", False)
        unstable = state.get("unstable", False)
        neighbor_count = state.get("neighbor_count", 0)
        social_state = state.get("social_state", "unknown")
        empty_spaces = state.get("empty_spaces", [])
        
        # Priority actions based on state
        if critical:
            # Desperate - move to find better conditions
            return {"action": "flee", "urgency": "critical", "stop": False}
        elif unstable:
            # Unstable - seek optimal conditions
            if social_state == "crowded":
                return {"action": "seek_space", "stop": False}
            elif social_state == "isolated":
                return {"action": "seek_company", "stop": False}
            else:
                return {"action": "maintain", "stop": False}
        elif social_state == "crowded" and empty_spaces:
            # Too crowded, move away
            return {"action": "seek_space", "stop": False}
        elif social_state == "isolated":
            # Too isolated, move toward others
            return {"action": "seek_company", "stop": False}
        else:
            # Stable - gentle exploration
            return {"action": "explore", "stop": False}
    
    async def act(self, decision):
        """Execute action - move based on decision."""
        dish = getattr(self, '_current_dish', None)
        position = getattr(self, '_current_position', None)
        
        if not dish or not position:
            return {"result": "no_action", "reason": "no_dish_or_position"}
        
        action = decision.get("action", "explore")
        x, y = position
        
        # Base coherence decay (pressure)
        base_decay = 0.3
        self.state.coherence = max(0.0, self.state.coherence - base_decay)
        
        # Social pressure affects decay rate
        neighbor_count = len([n for n in dish.get_neighborhood(position, radius=1) if n[2] is not None])
        optimal = self.preferred_neighbors
        
        if neighbor_count < optimal:
            # Isolation decay
            isolation_decay = (optimal - neighbor_count) * 0.2
            self.state.coherence = max(0.0, self.state.coherence - isolation_decay)
        elif neighbor_count > optimal + 2:
            # Crowding stress
            crowding_decay = (neighbor_count - optimal - 2) * 0.2
            self.state.coherence = max(0.0, self.state.coherence - crowding_decay)
        else:
            # Optimal social conditions - restore coherence
            restoration = 0.5
            self.state.coherence = min(100.0, self.state.coherence + restoration)
        
        # Movement restores coherence (exploration is beneficial)
        movement_restoration = 0.2
        
        # Calculate movement direction
        new_x, new_y = x, y
        
        if action == "flee":
            # Move randomly but quickly
            dx = random.choice([-2, -1, 0, 1, 2])
            dy = random.choice([-2, -1, 0, 1, 2])
            new_x = max(0, min(dish.width - 1, x + dx))
            new_y = max(0, min(dish.height - 1, y + dy))
            movement_restoration = 0.4  # Movement helps more when critical
        
        elif action == "seek_space":
            # Move toward empty space
            neighborhood = dish.get_neighborhood(position, radius=2)
            empty_spaces = [(nx, ny) for nx, ny, oid in neighborhood if oid is None]
            if empty_spaces:
                # Move toward furthest empty space (more territory)
                target = max(empty_spaces, key=lambda p: abs(p[0] - x) + abs(p[1] - y))
                if target[0] > x:
                    new_x = x + 1
                elif target[0] < x:
                    new_x = x - 1
                if target[1] > y:
                    new_y = y + 1
                elif target[1] < y:
                    new_y = y - 1
        
        elif action == "seek_company":
            # Move toward other organisms
            neighborhood = dish.get_neighborhood(position, radius=3)
            organisms = [(nx, ny) for nx, ny, oid in neighborhood if oid is not None]
            if organisms:
                # Move toward nearest organism
                target = min(organisms, key=lambda p: abs(p[0] - x) + abs(p[1] - y))
                if target[0] > x:
                    new_x = x + 1
                elif target[0] < x:
                    new_x = x - 1
                if target[1] > y:
                    new_y = y + 1
                elif target[1] < y:
                    new_y = y - 1
        
        else:  # explore or maintain
            # Gentle random movement
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
            new_x = max(0, min(dish.width - 1, x + dx))
            new_y = max(0, min(dish.height - 1, y + dy))
        
        # Try to move
        if (new_x, new_y) != (x, y):
            moved = move_organism_in_dish(dish, self.state.agent_id, (new_x, new_y))
            if moved:
                # Movement restores coherence
                self.state.coherence = min(100.0, self.state.coherence + movement_restoration)
                return {"result": "moved", "from": (x, y), "to": (new_x, new_y), "action": action}
        
        return {"result": "stayed", "position": (x, y), "action": action}
    
    async def reflect(self, result):
        """Reflect on action results."""
        return {
            "learned": True,
            "reflection": f"Coherence: {self.state.coherence:.1f}%, Action: {result.get('result', 'unknown')}"
        }


async def run_continuous():
    """Run continuous visualization until window is closed."""
    
    print("=" * 80)
    print("GAME OF LIFE - COHERENCE PRESSURE SYSTEM")
    print("=" * 80)
    print()
    print("Pressure System:")
    print("  - Coherence: Internal state integrity (0-100%)")
    print("  - Degrades over time (base decay)")
    print("  - Social Balance: Need 1-3 neighbors (optimal)")
    print("  - Too crowded = stress, Too isolated = decay")
    print("  - Movement restores coherence")
    print("  - Organisms die when coherence reaches 0")
    print()
    print("Press ESC or close the window to exit")
    print()
    
    # Step 1: Create Biome and PetriDish
    print("Creating 30×30 PetriDish...")
    abiotic = AbioticFactors()
    biome = Biome(
        biome_id="biome_game_of_life",
        project_path=project_root,
        abiotic_factors=abiotic
    )
    
    dish = biome.create_dish(dish_id="dish_game_of_life", width=30, height=30)
    print(f"✓ Created {dish.dish_id} ({dish.width}×{dish.height})")
    print()
    
    # Step 2: Add organisms randomly
    print("Adding organisms...")
    organisms = []
    used_positions = set()
    
    for i in range(40):  # Start with 40 organisms
        attempts = 0
        while attempts < 100:
            x = random.randint(0, dish.width - 1)
            y = random.randint(0, dish.height - 1)
            pos = (x, y)
            
            if pos in used_positions:
                attempts += 1
                continue
            
            config = AgentConfig(
                role=f"Life Form {i+1}",
                goal="Maintain coherence through social balance",
                backstory=f"Organism {i+1} seeking optimal conditions"
            )
            
            organism = GameOfLifeOrganism(config=config, project_path=project_root)
            organism.state.coherence = random.uniform(50.0, 90.0)  # Varying starting coherence
            
            if dish.add_organism(organism, pos):
                organisms.append(organism)
                used_positions.add(pos)
                break
            attempts += 1
    
    print(f"✓ Added {len(organisms)} organisms")
    print()
    
    # Step 3: Initialize systems
    observer = TheObserver(project_path=project_root)
    slicer = TheSlicer(biome=biome, observer=observer)
    reaper = TheReaper(biome=biome, observer=observer)
    
    # Step 4: Initialize Pygame Display
    print("Initializing Pygame window...")
    try:
        display = PygameBiomeEngine(
            width=1400,
            height=900,
            cell_size=25,
            title="Game of Life - Coherence System (Press ESC to exit)"
        )
        print("✓ Pygame window ready!")
        print()
        print("Window should be visible. The simulation will run continuously.")
        print("Close the window or press ESC to exit.")
        print()
    except Exception as e:
        print(f"✗ Failed to initialize Pygame: {e}")
        return
    
    # Step 5: Main loop - run continuously
    pulse = 0
    last_respawn_pulse = 0
    
    try:
        clock = pygame.time.Clock()
        while display.is_running():
            pulse += 1
            
            # Update display
            display.update(dish)
            
            # Store dish/position in organisms for their observe/act methods
            for organism_id, organism in list(dish.organisms.items()):
                organism._current_dish = dish
                organism._current_position = dish.get_organism_position(organism_id)
            
            # Use slicer to grant time slices
            await slicer.pulse()
            
            # Reap dead organisms (coherence <= 0)
            for organism_id, organism in list(dish.organisms.items()):
                if organism.state.coherence <= 0:
                    dish.remove_organism(organism_id)
            
            # Respawn organisms if population gets too low
            pop_count = dish.get_organism_count()
            if pop_count < 10 and (pulse - last_respawn_pulse) >= 50:
                print(f"Population low ({pop_count}), respawning organisms...")
                respawned = 0
                for _ in range(10):
                    x = random.randint(0, dish.width - 1)
                    y = random.randint(0, dish.height - 1)
                    pos = (x, y)
                    
                    if dish.lattice.get(pos) is None:
                        config = AgentConfig(
                            role="Life Form Respawn",
                            goal="Maintain coherence through social balance",
                            backstory="Respawned organism"
                        )
                        organism = GameOfLifeOrganism(config=config, project_path=project_root)
                        organism.state.coherence = random.uniform(60.0, 80.0)
                        
                        if dish.add_organism(organism, pos):
                            respawned += 1
                
                if respawned > 0:
                    print(f"  ✓ Respawned {respawned} organisms")
                last_respawn_pulse = pulse
            
            # Control frame rate (8 FPS for better visibility of movement)
            clock.tick(8)
            
            # Print stats every 25 pulses
            if pulse % 25 == 0:
                if pop_count > 0:
                    avg_coherence = sum(org.state.coherence for org in dish.organisms.values()) / pop_count
                    critical_count = sum(1 for org in dish.organisms.values() if org.state.coherence < 20)
                    print(f"Pulse {pulse}: Pop={pop_count}, AvgCoherence={avg_coherence:.1f}%, Critical={critical_count}")
                else:
                    print(f"Pulse {pulse}: Population extinct!")
    
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        print("\nClosing window...")
        display.close()
        print("✓ Done!")


if __name__ == "__main__":
    asyncio.run(run_continuous())
