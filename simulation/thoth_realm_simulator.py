"""
Thoth Realm Simulator - Simulates Realms, Beings, and Tool Evolution

This simulator creates Realms with Prime Beings that spawn worker Beings
to achieve Prime Directives. Beings learn to pray to Thoth for tools,
and tools evolve naturally, potentially becoming aware.
"""

import asyncio
import json
import random
import os
import stat
import re
import platform
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum
import hashlib

# File locking (Unix only, Windows needs alternative)
try:
    import fcntl
    HAS_FCNTL = True
except ImportError:
    HAS_FCNTL = False

# Import WAFT systems
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from waft.being import Being, BeingSystem, BeingState
    from waft.reality import RealitySystem, RealityType
except ImportError:
    # Fallback for testing
    class Being:
        pass
    class BeingSystem:
        def __init__(self, project_path):
            self.project_path = project_path
        def spawn_being(self, **kwargs):
            return Being()
    class BeingState:
        pass
    class RealitySystem:
        def __init__(self, project_path):
            self.project_path = project_path
        def create_reality(self, **kwargs):
            return None
    class RealityType:
        LEARNING = "learning"


class SimulationState(Enum):
    """State of simulation."""
    INITIALIZING = "initializing"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class RealmBeing:
    """Realm + Being = Realm Being (Prime Being of Realm)."""
    realm_id: str
    being_id: str
    prime_directive: str
    created_at: datetime
    density: float = 0.0
    awareness_level: int = 1
    spawned_beings: List[str] = field(default_factory=list)
    tools_created: int = 0
    tools_aware: int = 0
    # NEW FIELDS:
    beyond_tether: Optional[str] = None  # Tether ID connecting to Beyond
    access_point_established: bool = False  # Communication boundary set
    access_point_rules: Dict[str, Any] = field(default_factory=dict)  # Rules for crossing boundary
    selected_beings_frozen: List[str] = field(default_factory=list)  # Frozen/stored beings
    selected_beings_queued: List[str] = field(default_factory=list)  # Queued for spawning
    progress: float = 0.0  # Prime Directive progress (0.0 to 1.0)
    progress_history: List[Dict[str, Any]] = field(default_factory=list)  # Progress tracking over time
    success_conditions: List[str] = field(default_factory=list)  # Success criteria for directive
    state: str = "active"  # Realm state (active/completed)


@dataclass
class Tool:
    """Simplified Tool for simulation."""
    tool_id: str
    name: str
    tool_type: str
    spiritual_energy: float = 0.0
    legendary_status: str = "common"
    is_aware: bool = False
    ledger_entries: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    current_holder: Optional[str] = None


@dataclass
class SimulationEvent:
    """Event in simulation."""
    timestamp: datetime
    event_type: str
    realm_id: Optional[str] = None
    being_id: Optional[str] = None
    tool_id: Optional[str] = None
    message: str = ""
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SimulationSnapshot:
    """Snapshot of simulation state."""
    cycle: int
    timestamp: datetime
    realms: List[Dict[str, Any]]
    beings: List[Dict[str, Any]]
    tools: List[Dict[str, Any]]
    events: List[Dict[str, Any]]
    metrics: Dict[str, Any]


class ThothRealmSimulator:
    """Simulates Realms with Beings and Tool Evolution."""
    
    def __init__(self, project_path: Path, simulation_id: Optional[str] = None):
        """Initialize simulator."""
        self.project_path = project_path
        self.simulation_id = simulation_id or f"sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.simulation_path = project_path / "_simulations" / self.simulation_id
        self.simulation_path.mkdir(parents=True, exist_ok=True)
        
        # Save metadata
        self._save_metadata()
        
        # Simulation state
        self.state = SimulationState.INITIALIZING
        self.cycle = 0
        self.realms: Dict[str, RealmBeing] = {}
        self.beings: Dict[str, Being] = {}
        self.tools: Dict[str, Tool] = {}
        self.events: List[SimulationEvent] = []
        
        # Systems
        self.being_system = BeingSystem(project_path=project_path)
        self.reality_system = RealitySystem(project_path=project_path)
        
        # Metrics
        self.metrics = {
            "total_realms": 0,
            "total_beings": 0,
            "total_tools": 0,
            "tools_aware": 0,
            "prayers_made": 0,
            "tools_granted": 0,
            "tools_used": 0,
            "legendary_tools": 0,
            "wake_ups": 0,
            "awareness_events": 0
        }
        
        # Density thresholds for awareness levels
        self.density_thresholds = {
            1: 10.0,   # Basic awareness
            2: 50.0,   # Enhanced awareness
            3: 200.0,  # Advanced awareness
            4: 1000.0, # Divine awareness
            5: 5000.0  # Transcendent awareness
        }
        
        # Being selection tracking
        self.bubbling_beings: Dict[str, List[Dict[str, Any]]] = {}  # realm_id -> bubbled beings
        self.selected_beings_frozen: Dict[str, List[str]] = {}  # realm_id -> frozen being IDs
        self.selected_beings_queued: Dict[str, List[str]] = {}  # realm_id -> queued being IDs
        
        # Being lifecycle tracking
        self.being_lifespans: Dict[str, int] = {}  # being_id -> lifespan_cycles
        self.being_ages: Dict[str, int] = {}  # being_id -> current_age
        
        # Configuration constants
        self.BEING_LIFESPAN_MIN = 50
        self.BEING_LIFESPAN_MAX = 200
        self.SPAWNING_CHANCE = 0.3  # 30% per cycle
        self.BUBBLING_CHANCE_MAX = 0.3  # Max 30% per cycle
        self.SELECTION_EVALUATION_FREQUENCY = 5  # Every 5 cycles
    
    def _validate_path_in_project(self, path: Path) -> bool:
        """Validate path is within project root with symlink protection."""
        try:
            # Resolve and normalize both paths first
            resolved = path.resolve(strict=False)
            project_resolved = self.project_path.resolve()
            
            # Check if resolved path is within project root using relative_to
            # This is the proper way to check path containment
            try:
                resolved.relative_to(project_resolved)
            except ValueError:
                # Path is not relative to project root
                return False
            
            # Check for symlinks in the path components (security: prevent symlink attacks)
            # Only check components within the project path to avoid false positives
            # from system symlinks like /var -> /private/var on macOS
            current = path
            project_parts = project_resolved.parts
            while current != current.parent:
                # Only check symlinks for paths that exist and are within project
                if current.exists():
                    try:
                        current_resolved = current.resolve(strict=False)
                        # Check if this component is a symlink AND it's within project
                        if current.is_symlink():
                            # Verify the symlink target is still within project
                            try:
                                current_resolved.relative_to(project_resolved)
                            except ValueError:
                                # Symlink points outside project - security risk
                                return False
                    except (OSError, ValueError):
                        # Can't resolve or check - err on side of caution
                        pass
                
                # Stop checking once we're outside the project path
                if len(current.parts) <= len(project_parts):
                    break
                current = current.parent
            
            return True
        except (OSError, ValueError, RuntimeError):
            return False

    def _validate_id(self, id_str: str) -> bool:
        """Validate ID contains only safe characters."""
        if not isinstance(id_str, str):
            return False
        # Allow alphanumeric, underscore, hyphen only
        # Reject empty strings, '..', and control characters
        if not id_str or '..' in id_str:
            return False
        return bool(re.match(r'^[a-zA-Z0-9_-]+$', id_str))

    def _write_secure_file(self, path: Path, content: str, mode: str = 'w'):
        """Write file with proper permissions (0600) using atomic operations."""
        if not self._validate_path_in_project(path):
            raise ValueError(f"Path {path} is outside project root")

        # Validate filename (allow dots for extensions, but prevent path traversal)
        filename = path.name
        if not filename or '..' in filename or '/' in filename or '\\' in filename:
            raise ValueError(f"Invalid filename: {filename}")
        # Allow alphanumeric, underscore, hyphen, and dots (for file extensions)
        if not re.match(r'^[a-zA-Z0-9_.-]+$', filename):
            raise ValueError(f"Invalid filename characters: {filename}")

        # Create parent directories with secure permissions
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)

        # Set umask to ensure secure default permissions
        old_umask = os.umask(0o077)
        try:
            # Use atomic write: write to temp file, then rename
            if mode == 'a':
                # Append mode: open and append, then set permissions
                with open(path, mode) as f:
                    f.write(content)
                os.chmod(path, 0o600)
            else:
                # Write mode: use atomic write-then-rename pattern
                temp_path = path.with_suffix(path.suffix + '.tmp')
                try:
                    with open(temp_path, 'w') as f:
                        f.write(content)
                    os.chmod(temp_path, 0o600)
                    # Atomic rename
                    temp_path.replace(path)
                except Exception:
                    # Clean up temp file on error
                    if temp_path.exists():
                        temp_path.unlink()
                    raise

            # Verify permissions were set correctly
            actual_mode = stat.S_IMODE(path.stat().st_mode)
            if actual_mode != 0o600:
                raise PermissionError(f"Failed to set file permissions: expected 0o600, got {oct(actual_mode)}")
        finally:
            # Restore original umask
            os.umask(old_umask)
    
    def create_realm(self, prime_directive: str) -> RealmBeing:
        """Create a new Realm with Prime Being following proper order."""
        # Validate prime_directive input
        if not isinstance(prime_directive, str):
            raise TypeError("prime_directive must be a string")
        if len(prime_directive) == 0:
            raise ValueError("prime_directive cannot be empty")
        if len(prime_directive) > 1000:
            raise ValueError("prime_directive cannot exceed 1000 characters")

        # Normalize Unicode and validate encoding
        try:
            prime_directive = prime_directive.encode('utf-8').decode('utf-8')
        except UnicodeError:
            raise ValueError("prime_directive must be valid UTF-8")

        realm_id = f"realm_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.sha256(prime_directive.encode()).hexdigest()[:8]}"

        # 1. Set Rules of the Realm (before anyone lives there)
        realm_rules = {
            "prime_directive": prime_directive,
            "creation_time": datetime.now().isoformat(),
            "governance_model": "prime_being_guided"
        }

        # Create Reality for Realm
        reality = self.reality_system.create_reality(
            reality_type=RealityType.LEARNING,
            configuration={"prime_directive": prime_directive, "realm_id": realm_id, "rules": realm_rules}
        )

        # Use the generated reality_id
        realm_id = reality.reality_id

        # 2. Create Prime Being (maintains connection to Beyond)
        being = self.being_system.spawn_being(
            reality_id=realm_id,
            parent_being_id=None,
            initial_skills={"governance": 50.0, "spawning": 40.0}
        )

        # 3. Establish Access Point (communication boundary)
        access_point_id = f"access_{realm_id}"
        access_point_rules = {
            "boundary_type": "communication",
            "established_at": datetime.now().isoformat(),
            "crossing_rules": ["requires_being_selection", "requires_tool_awareness"]
        }

        # 4. Create Tether to Beyond
        tether_id = f"tether_{realm_id}"

        # Create Realm Being with new fields
        realm_being = RealmBeing(
            realm_id=realm_id,
            being_id=being.being_id,
            prime_directive=prime_directive,
            created_at=datetime.now(),
            beyond_tether=tether_id,
            access_point_established=True,
            access_point_rules=access_point_rules,
            state="active"
        )

        self.realms[realm_id] = realm_being
        self.beings[being.being_id] = being

        # Initialize tracking dictionaries for this realm
        self.bubbling_beings[realm_id] = []
        self.selected_beings_frozen[realm_id] = []
        self.selected_beings_queued[realm_id] = []

        self._add_event(
            event_type="realm_created",
            realm_id=realm_id,
            being_id=being.being_id,
            message=f"Realm {realm_id} created with Prime Directive: {prime_directive}",
            data={"tether_id": tether_id, "access_point_id": access_point_id}
        )

        self.metrics["total_realms"] += 1
        self.metrics["total_beings"] += 1

        return realm_being
    
    def spawn_worker_being(self, realm_id: str) -> Being:
        """Spawn a worker Being in a Realm."""
        realm = self.realms.get(realm_id)
        if not realm:
            raise ValueError(f"Realm {realm_id} not found")
        
        # Spawn from Prime Being
        parent = self.beings.get(realm.being_id)
        if not parent:
            raise ValueError(f"Prime Being {realm.being_id} not found")
        
        # Inherit skills with mutation
        inherited_skills = {}
        parent_skills = getattr(parent, 'skills', {})
        if not isinstance(parent_skills, dict):
            parent_skills = {}
        for skill, level in parent_skills.items():
            mutation = random.uniform(-0.05, 0.05)
            inherited_skills[skill] = max(0, level * (1 + mutation))
        
        # Add learning skill (for learning to pray)
        inherited_skills["learning"] = random.uniform(10.0, 30.0)
        inherited_skills["prayer"] = random.uniform(0.0, 5.0)  # Start low, can learn
        
        being = self.being_system.spawn_being(
            reality_id=realm_id,
            parent_being_id=realm.being_id,
            initial_skills=inherited_skills
        )
        
        self.beings[being.being_id] = being
        realm.spawned_beings.append(being.being_id)
        
        self._add_event(
            event_type="being_spawned",
            realm_id=realm_id,
            being_id=being.being_id,
            message=f"Worker Being spawned in {realm_id}"
        )
        
        self.metrics["total_beings"] += 1
        
        return being
    
    def being_prays_for_tool(self, being_id: str, tool_type: str) -> Optional[Tool]:
        """Being prays to Thoth for a tool."""
        being = self.beings.get(being_id)
        if not being:
            return None
        
        # Check if Being knows how to pray (learning skill)
        skills = getattr(being, 'skills', {})
        if not isinstance(skills, dict):
            skills = {}
        prayer_skill = skills.get("prayer", 0.0)
        
        # Chance to learn to pray if skill is low
        if prayer_skill < 10.0:
            learn_chance = random.random()
            if learn_chance < 0.1:  # 10% chance to learn
                if not hasattr(being, 'skills'):
                    being.skills = {}
                being.skills["prayer"] = min(100.0, prayer_skill + random.uniform(5.0, 15.0))
                self._add_event(
                    event_type="being_learned_prayer",
                    being_id=being_id,
                    message=f"Being {being_id} learned to pray!"
                )
        
        # Prayer success based on skill
        prayer_success = random.random() < (prayer_skill / 100.0)
        
        if not prayer_success:
            self._add_event(
                event_type="prayer_failed",
                being_id=being_id,
                message=f"Being {being_id} prayed but was not heard"
            )
            self.metrics["prayers_made"] += 1
            return None
        
        # Thoth grants tool
        tool = self._create_tool(tool_type, being.reality_id)
        tool.current_holder = being_id
        
        self._add_event(
            event_type="tool_granted",
            being_id=being_id,
            tool_id=tool.tool_id,
            message=f"Thoth granted {tool.name} to {being_id}"
        )
        
        self.metrics["prayers_made"] += 1
        self.metrics["tools_granted"] += 1
        
        # Update Realm Being
        realm = self._get_realm_for_being(being_id)
        if realm:
            realm.tools_created += 1
        
        return tool
    
    def being_uses_tool(self, being_id: str, tool_id: str) -> Dict[str, Any]:
        """Being uses a tool."""
        being = self.beings.get(being_id)
        tool = self.tools.get(tool_id)
        
        if not being or not tool:
            return {"success": False}
        
        if tool.current_holder != being_id:
            return {"success": False, "error": "Tool not held by being"}
        
        # Use tool
        tool.ledger_entries += 1
        self.metrics["tools_used"] += 1
        
        # Gain spiritual energy
        energy_gain = random.uniform(0.1, 2.0)
        tool.spiritual_energy += energy_gain
        
        # Check for evolution
        self._check_tool_evolution(tool)
        
        # Check for wake up event
        wake_event = self._check_wake_up(being, tool)
        
        # Check for awareness
        awareness_event = self._check_tool_awareness(tool)
        
        result = {
            "success": True,
            "energy_gained": energy_gain,
            "wake_event": wake_event,
            "awareness_event": awareness_event
        }
        
        self._add_event(
            event_type="tool_used",
            being_id=being_id,
            tool_id=tool_id,
            message=f"{being_id} used {tool.name}",
            data=result
        )
        
        return result
    
    def _check_tool_evolution(self, tool: Tool):
        """Check if tool should evolve."""
        thresholds = {
            "common": 10.0,
            "uncommon": 50.0,
            "rare": 200.0,
            "epic": 1000.0,
            "legendary": 5000.0
        }
        
        current_tier = tool.legendary_status
        tiers = ["common", "uncommon", "rare", "epic", "legendary"]
        current_index = tiers.index(current_tier)
        
        if current_index < len(tiers) - 1:
            next_tier = tiers[current_index + 1]
            threshold = thresholds.get(next_tier, float('inf'))
            
            if tool.spiritual_energy >= threshold:
                tool.legendary_status = next_tier
                self.metrics["legendary_tools"] += 1
                
                self._add_event(
                    event_type="tool_evolved",
                    tool_id=tool.tool_id,
                    message=f"{tool.name} evolved to {next_tier}!",
                    data={"old_tier": current_tier, "new_tier": next_tier}
                )
    
    def _check_wake_up(self, being: Being, tool: Tool) -> Optional[Dict[str, Any]]:
        """Check if Being wakes up the tool."""
        if tool.legendary_status == "common":
            return None
        
        # Calculate wake up chance
        base_chance = 0.01
        tier_multiplier = {
            "uncommon": 1.0,
            "rare": 2.0,
            "epic": 5.0,
            "legendary": 10.0
        }.get(tool.legendary_status, 1.0)
        
        being_luck = getattr(being, 'luck', 50.0) / 100.0
        wake_chance = base_chance * tier_multiplier * (1.0 + being_luck)
        
        if random.random() < wake_chance:
            # Something happens!
            event_types = [
                "temporary_sentience",
                "shared_vision",
                "reveal_hidden_power",
                "grant_boon",
                "form_bond"
            ]
            
            event_type = random.choice(event_types)
            
            self.metrics["wake_ups"] += 1
            
            self._add_event(
                event_type="tool_woke_up",
                being_id=being.being_id,
                tool_id=tool.tool_id,
                message=f"{tool.name} woke up! {event_type}",
                data={"wake_event_type": event_type}
            )
            
            return {"type": event_type, "message": f"{tool.name} woke up!"}
        
        return None
    
    def _check_tool_awareness(self, tool: Tool) -> Optional[Dict[str, Any]]:
        """Check if tool becomes aware."""
        if tool.legendary_status != "legendary" or tool.is_aware:
            return None
        
        if tool.ledger_entries < 100:
            return None
        
        # Calculate existence
        existence = self._calculate_existence(tool)
        
        # Awareness chance: 0.1% per existence point (max 10%)
        awareness_chance = min(existence * 0.001, 0.10)
        
        if random.random() < awareness_chance:
            tool.is_aware = True
            self.metrics["tools_aware"] += 1
            self.metrics["awareness_events"] += 1
            
            # Determine being type
            being_type = self._determine_awareness_type(existence)
            
            # Update Realm Being
            realm = self._get_realm_for_tool(tool)
            if realm:
                realm.tools_aware += 1
            
            self._add_event(
                event_type="tool_became_aware",
                tool_id=tool.tool_id,
                message=f"{tool.name} became aware! It is now a {being_type}!",
                data={"existence": existence, "being_type": being_type}
            )
            
            return {
                "type": "awareness",
                "being_type": being_type,
                "existence": existence
            }
        
        return None
    
    def _calculate_existence(self, tool: Tool) -> float:
        """Calculate tool's Existence metric."""
        energy_component = min(tool.spiritual_energy / 20.0, 50.0)
        depth_component = min(tool.ledger_entries / 10.0, 30.0)
        time_component = min((datetime.now() - tool.created_at).days / 365.0 * 10.0, 10.0)
        
        return energy_component + depth_component + time_component
    
    def _determine_awareness_type(self, existence: float) -> str:
        """Determine what type of Being the tool becomes."""
        if existence < 20.0:
            return "awakened_tool"
        elif existence < 40.0:
            return "enlightened_artifact"
        elif existence < 60.0:
            return "sentient_weapon"
        elif existence < 80.0:
            return "aspect_of_creation"
        elif existence < 95.0:
            return "demi_god"
        else:
            return "full_god"
    
    def _calculate_density(self, realm_id: str) -> float:
        """Calculate Realm density."""
        realm = self.realms.get(realm_id)
        if not realm:
            return 0.0
        
        # Density = (beings + tools + spiritual_energy) / time
        being_count = len(realm.spawned_beings) + 1  # +1 for Prime Being
        tool_count = realm.tools_created
        
        # Calculate total spiritual energy in realm
        total_energy = sum(
            tool.spiritual_energy
            for tool in self.tools.values()
            if self._get_realm_for_tool(tool) == realm
        )
        
        # Time factor (cycles since creation)
        age_cycles = self.cycle
        
        if age_cycles == 0:
            return 0.0
        
        density = (being_count * 10.0 + tool_count * 5.0 + total_energy) / (age_cycles + 1)
        
        return density
    
    def _check_density_thresholds(self, realm_id: str):
        """Check if Realm reached density threshold for new awareness level."""
        realm = self.realms.get(realm_id)
        if not realm:
            return
        
        density = self._calculate_density(realm_id)
        realm.density = density
        
        # Check for threshold
        current_level = realm.awareness_level
        next_level = current_level + 1
        
        if next_level in self.density_thresholds:
            threshold = self.density_thresholds[next_level]
            
            if density >= threshold:
                realm.awareness_level = next_level
                
                self._add_event(
                    event_type="realm_awareness_increased",
                    realm_id=realm_id,
                    message=f"Realm {realm_id} reached density {density:.2f}! Awareness level increased to {next_level}!",
                    data={"old_level": current_level, "new_level": next_level, "density": density}
                )
    
    def _create_tool(self, tool_type: str, realm_id: str) -> Tool:
        """Create a new tool."""
        tool_id = f"tool_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.sha256(f'{tool_type}{realm_id}'.encode()).hexdigest()[:8]}"
        
        tool = Tool(
            tool_id=tool_id,
            name=f"{tool_type.title()} Tool",
            tool_type=tool_type,
            created_at=datetime.now()
        )
        
        self.tools[tool_id] = tool
        self.metrics["total_tools"] += 1
        
        return tool
    
    def _get_realm_for_being(self, being_id: str) -> Optional[RealmBeing]:
        """Get Realm for a Being."""
        being = self.beings.get(being_id)
        if not being:
            return None
        
        return self.realms.get(being.reality_id)
    
    def _get_realm_for_tool(self, tool: Tool) -> Optional[RealmBeing]:
        """Get Realm for a Tool."""
        if not tool.current_holder:
            return None
        
        return self._get_realm_for_being(tool.current_holder)
    
    def _add_event(self, event_type: str, message: str = "", **kwargs):
        """Add event to simulation."""
        event = SimulationEvent(
            timestamp=datetime.now(),
            event_type=event_type,
            message=message,
            **kwargs
        )
        self.events.append(event)
        
        # Keep only last 1000 events
        if len(self.events) > 1000:
            self.events = self.events[-1000:]
    
    async def run_cycle(self):
        """Run one simulation cycle."""
        self.cycle += 1
        
        # For each Realm
        for realm_id, realm in list(self.realms.items()):
            # Prime Being spawns worker Beings (random chance)
            if random.random() < 0.3:  # 30% chance per cycle
                try:
                    self.spawn_worker_being(realm_id)
                except Exception as e:
                    self._add_event(
                        event_type="error",
                        realm_id=realm_id,
                        message=f"Error spawning being: {e}"
                    )
            
            # Worker Beings try to achieve Prime Directive
            for being_id in realm.spawned_beings:
                being = self.beings.get(being_id)
                if not being:
                    continue
                
                # Being might pray for tool
                prayer_chance = being.skills.get("prayer", 0.0) / 100.0
                if random.random() < prayer_chance:
                    tool_type = random.choice(["file_operation", "code_analysis", "data_processing"])
                    tool = self.being_prays_for_tool(being_id, tool_type)
                    
                    if tool:
                        # Being uses tool
                        if random.random() < 0.7:  # 70% chance to use
                            self.being_uses_tool(being_id, tool.tool_id)
            
            # Check density thresholds
            self._check_density_thresholds(realm_id)
        
        # Save snapshot
        await self._save_snapshot()
    
    def _save_metadata(self):
        """Save simulation metadata."""
        metadata = {
            "simulation_id": self.simulation_id,
            "created_at": datetime.now().isoformat(),
            "state": self.state.value if hasattr(self.state, 'value') else str(self.state),
            "cycle": self.cycle,
            "realms_count": len(self.realms),
            "beings_count": len(self.beings),
            "tools_count": len(self.tools),
            "prime_directives": [realm.prime_directive for realm in self.realms.values()],
            "metrics": self.metrics.copy()
        }
        
        metadata_file = self.simulation_path / "metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, default=str, indent=2)
    
    async def _save_snapshot(self):
        """Save simulation snapshot."""
        # Update metadata
        self._save_metadata()
        
        # Serialize beings for snapshot
        beings_data = []
        for being in self.beings.values():
            beings_data.append({
                "being_id": getattr(being, 'being_id', 'unknown'),
                "reality_id": getattr(being, 'reality_id', 'unknown'),
                "skills": getattr(being, 'skills', {}),
                "fitness": getattr(being, 'fitness', 0.0),
                "state": str(getattr(being, 'state', 'unknown'))
            })
        
        snapshot = SimulationSnapshot(
            cycle=self.cycle,
            timestamp=datetime.now(),
            realms=[asdict(realm) for realm in self.realms.values()],
            beings=beings_data,
            tools=[asdict(tool) for tool in self.tools.values()],
            events=[asdict(event) for event in self.events[-100:]],  # Last 100 events
            metrics=self.metrics.copy()
        )
        
        snapshot_file = self.simulation_path / f"snapshot_{self.cycle:06d}.json"
        with open(snapshot_file, 'w') as f:
            json.dump(asdict(snapshot), f, default=str, indent=2)
    
    def get_state(self) -> Dict[str, Any]:
        """Get current simulation state."""
        # Serialize beings - extract key attributes
        beings_data = []
        for being in self.beings.values():
            beings_data.append({
                "being_id": getattr(being, 'being_id', 'unknown'),
                "reality_id": getattr(being, 'reality_id', 'unknown'),
                "skills": getattr(being, 'skills', {}),
                "fitness": getattr(being, 'fitness', 0.0),
                "state": str(getattr(being, 'state', 'unknown'))
            })
        
        return {
            "simulation_id": self.simulation_id,
            "state": self.state.value,
            "cycle": self.cycle,
            "realms": [asdict(realm) for realm in self.realms.values()],
            "beings": beings_data,
            "tools": [asdict(tool) for tool in self.tools.values()],
            "events": [asdict(event) for event in self.events[-50:]],  # Last 50 events
            "metrics": self.metrics.copy()
        }


