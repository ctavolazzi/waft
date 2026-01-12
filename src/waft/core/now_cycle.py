"""
Now Cycle Manager: Centralized event loop for Being lifecycle management.

Manages the "Now" cycle event loop that synchronizes all beings, calculates
system variables, records state, and unblocks beings for decisions.
"""

import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional, TYPE_CHECKING
from datetime import datetime
import json

if TYPE_CHECKING:
    from ..being import BeingSystem, Being, BeingState
    from ..karma import KarmaMerchant


class NowCycleManager:
    """
    Manages the "Now" cycle event loop.
    
    Coordinates all beings, calculates system state,
    records to storage, and unblocks beings for decisions.
    
    The cycle flow:
    1. Lock all beings (async-safe)
    2. Calculate system state (will_to_live, luck, pleasure/pain, sleep)
    3. Process sleeping beings
    4. Check death conditions
    5. Record state to storage
    6. Time marches forward (+1 cycle)
    7. Unblock beings (allow decisions)
    """
    
    def __init__(
        self,
        project_path: Path,
        being_system: "BeingSystem",
        karma_merchant: Optional["KarmaMerchant"] = None
    ):
        """
        Initialize NowCycleManager.
        
        Args:
            project_path: Path to project root
            being_system: BeingSystem instance for being management
            karma_merchant: Optional KarmaMerchant instance (will create if None)
        """
        self.project_path = Path(project_path)
        self.being_system = being_system
        self.cycle_number = 0
        self.cycle_lock = asyncio.Lock()  # Prevent concurrent cycles
        self.beings_locked = asyncio.Event()  # Async-safe locking for beings
        self.beings_locked.set()  # Start unlocked (beings can make decisions)
        self.cycle_history: List[Dict[str, Any]] = []
        
        # Initialize KarmaMerchant if not provided
        if karma_merchant is None:
            from ..karma import KarmaMerchant
            self.karma_merchant = KarmaMerchant(project_path=self.project_path)
        else:
            self.karma_merchant = karma_merchant
        
        # Initialize TheObserver for flight recorder
        from ..core.science.observer import TheObserver
        self.observer = TheObserver(project_path=self.project_path)
    
    async def execute_cycle(self) -> Dict[str, Any]:
        """
        Execute one complete "Now" cycle.
        
        CRITICAL: Uses asyncio.Lock to prevent concurrent cycle execution.
        
        Returns:
            Cycle result dictionary with state changes
        """
        # CRITICAL: Prevent concurrent cycles
        async with self.cycle_lock:
            # 1. Lock all beings (clear event = locked)
            self.beings_locked.clear()
            
            try:
                # 2. Calculate system state
                state_changes = await self.calculate_system_state()
                
                # 3. Process sleeping beings
                awake_beings = await self.process_sleeping_beings()
                
                # 4. Check death conditions
                dead_beings = await self.check_death_conditions()
                
                # 5. Record state
                await self.record_cycle_state({
                    "cycle_number": self.cycle_number,
                    "state_changes": state_changes,
                    "awake_beings": awake_beings,
                    "dead_beings": dead_beings
                })
                
                # 6. Time forward
                self.cycle_number += 1
                
                # 7. Unblock beings (set event = unlocked)
                self.beings_locked.set()
                
                return {
                    "cycle_number": self.cycle_number,
                    "state_changes": state_changes,
                    "awake_beings": len(awake_beings),
                    "dead_beings": len(dead_beings)
                }
            except Exception as e:
                # On error, still unblock beings
                self.beings_locked.set()
                raise
    
    async def calculate_system_state(self) -> Dict[str, Any]:
        """
        Calculate all system variables for all beings.
        
        For each being:
        - Get karma balance (via soul_id)
        - Calculate will_to_live change
        - Calculate luck
        - Calculate pleasure/pain from recent experiences
        - Update attributes
        
        Returns:
            Dictionary with state changes for all beings
        """
        state_changes = {}
        
        # Get all active beings
        try:
            beings_path = self.being_system.beings_path
            if not beings_path.exists():
                return state_changes
            
            being_files = list(beings_path.glob("*.json"))
            
            for being_file in being_files:
                try:
                    being_id = being_file.stem
                    
                    # Load being
                    being = self.being_system._load_being(being_id)
                    
                    # Skip if being is archived or dead
                    from ..being import BeingState
                    if being.state == BeingState.ARCHIVED:
                        continue
                    
                    # Get karma balance
                    karma_balance = self.being_system.get_karma_balance(being)
                    
                    # Calculate luck
                    new_luck = being.calculate_luck(karma_balance)
                    luck_change = new_luck - being.luck
                    being.luck = new_luck
                    
                    # Recalculate stamina (from all stats, especially willpower)
                    # This happens each cycle as stats change
                    being.stamina = being._calculate_stamina()
                    
                    # Regenerate stamina (interplays with will_to_live)
                    stamina_regenerated = being.regenerate_stamina()
                    
                    # Calculate will_to_live change
                    cycle_data = {
                        "decisions_made": being.decision_quota_max - being.decision_fatigue,
                        "pain": being.pain,
                        "pleasure": being.pleasure,
                        "stamina_ratio": being.get_stamina_ratio()
                    }
                    will_to_live_change = being.calculate_will_to_live_change(cycle_data)
                    being.will_to_live = max(0.0, min(100.0, being.will_to_live + will_to_live_change))
                    
                    # Stamina and will_to_live interplay:
                    # Low stamina reduces will_to_live regeneration
                    if being.is_stamina_depleted():
                        # Being is exhausted - slight will_to_live drain
                        being.will_to_live = max(0.0, being.will_to_live - 0.2)
                    
                    # Calculate pleasure/pain from recent experiences
                    if being.recent_experiences:
                        # Process all recent experiences
                        total_pleasure = 0.0
                        total_pain = 0.0
                        
                        for experience in being.recent_experiences:
                            pleasure, pain = being.calculate_pleasure_pain(
                                personality=being.personality,
                                goals=being.goals,
                                experience=experience
                            )
                            total_pleasure += pleasure
                            total_pain += pain
                        
                        # Average over experiences
                        num_experiences = len(being.recent_experiences)
                        if num_experiences > 0:
                            being.pleasure = total_pleasure / num_experiences
                            being.pain = total_pain / num_experiences
                        
                        # Clear recent experiences (processed)
                        being.recent_experiences = []
                    
                    # Update cycle tracking
                    being.last_cycle_number = self.cycle_number
                    being.cycles_alive += 1
                    
                    # Save being state
                    self.being_system._save_being(being)
                    
                    # Track stamina changes
                    old_stamina = being.stamina - stamina_regenerated  # Reverse the regeneration to get old value
                    stamina_change = being.stamina - old_stamina
                    
                    state_changes[being_id] = {
                        "luck_change": luck_change,
                        "will_to_live_change": will_to_live_change,
                        "stamina_change": stamina_change,
                        "stamina": being.stamina,
                        "stamina_ratio": being.get_stamina_ratio(),
                        "willpower": being.willpower,
                        "pleasure": being.pleasure,
                        "pain": being.pain,
                        "stamina_depleted": being.is_stamina_depleted()
                    }
                
                except (FileNotFoundError, json.JSONDecodeError, OSError) as e:
                    # Skip corrupted or missing beings
                    continue
        
        except Exception as e:
            # Log error but don't crash entire cycle
            pass
        
        return state_changes
    
    async def process_sleeping_beings(self) -> List[str]:
        """
        Process sleeping beings, return list of newly awake being IDs.
        
        Returns:
            List of being IDs that just woke up
        """
        awake_beings = []
        
        try:
            beings_path = self.being_system.beings_path
            if not beings_path.exists():
                return awake_beings
            
            being_files = list(beings_path.glob("*.json"))
            
            for being_file in being_files:
                try:
                    being_id = being_file.stem
                    being = self.being_system._load_being(being_id)
                    
                    if being.is_sleeping:
                        # Process sleep
                        if being.process_sleep():
                            # Being is now awake
                            awake_beings.append(being_id)
                            self.being_system._save_being(being)
                
                except (FileNotFoundError, json.JSONDecodeError, OSError):
                    # Skip corrupted or missing beings
                    continue
        
        except Exception:
            # Log error but don't crash
            pass
        
        return awake_beings
    
    async def check_death_conditions(self) -> List[str]:
        """
        Check for dead beings (will_to_live = 0), return list of dead being IDs.
        
        Returns:
            List of being IDs that died this cycle
        """
        from ..being import BeingState
        
        dead_beings = []
        
        try:
            beings_path = self.being_system.beings_path
            if not beings_path.exists():
                return dead_beings
            
            being_files = list(beings_path.glob("*.json"))
            
            for being_file in being_files:
                try:
                    being_id = being_file.stem
                    being = self.being_system._load_being(being_id)
                    
                    # Skip already archived beings
                    if being.state == BeingState.ARCHIVED:
                        continue
                    
                    # Check death condition
                    if being.check_death():
                        # Being died - archive it
                        being.state = BeingState.ARCHIVED
                        self.being_system._save_being(being)
                        dead_beings.append(being_id)
                        
                        # Record death event
                        from ..agent.state import EvolutionaryEvent, EvolutionaryEventType
                        event = EvolutionaryEvent(
                            timestamp=datetime.utcnow(),
                            genome_id=f"being_{being_id}",
                            parent_id=being.parent_being_id,
                            generation=0,
                            event_type=EvolutionaryEventType.DEATH,
                            payload={
                                "death_type": "will_to_live",
                                "reason": "Will to live reached 0.0",
                                "being_id": being_id,
                                "reality_id": being.reality_id
                            },
                            agent_id=being_id,
                            lineage_path=[being_id]
                        )
                        self.observer.observe_event(event)
                
                except (FileNotFoundError, json.JSONDecodeError, OSError):
                    # Skip corrupted or missing beings
                    continue
        
        except Exception:
            # Log error but don't crash
            pass
        
        return dead_beings
    
    async def record_cycle_state(self, cycle_data: Dict[str, Any]) -> None:
        """
        Record cycle state to Akasha, flight recorder, and being files.
        
        CRITICAL: Includes error handling for all storage operations.
        
        Records:
        - Cycle events to flight recorder (via TheObserver)
        - Being state to Akasha (via soul_id)
        - Being state to being files (JSON)
        
        Args:
            cycle_data: Cycle data dictionary
        """
        from ..agent.state import EvolutionaryEvent, EvolutionaryEventType
        
        # Record cycle event to flight recorder
        try:
            event = EvolutionaryEvent(
                timestamp=datetime.utcnow(),
                genome_id="now_cycle",
                parent_id=None,
                generation=0,
                event_type=EvolutionaryEventType.MUTATE,  # Using MUTATE for cycle events
                payload={
                    "cycle_event": True,
                    "cycle_number": cycle_data.get("cycle_number", self.cycle_number),
                    "state_changes": cycle_data.get("state_changes", {}),
                    "awake_beings": cycle_data.get("awake_beings", []),
                    "dead_beings": cycle_data.get("dead_beings", [])
                },
                agent_id="now_cycle_manager",
                lineage_path=[]
            )
            self.observer.observe_event(event)
        except Exception:
            # Log error but don't crash
            pass
        
        # Record being state to Akasha (via soul_id)
        try:
            beings_path = self.being_system.beings_path
            if beings_path.exists():
                being_files = list(beings_path.glob("*.json"))
                
                for being_file in being_files:
                    try:
                        being_id = being_file.stem
                        being = self.being_system._load_being(being_id)
                        
                        # Skip archived beings
                        from ..being import BeingState
                        if being.state == BeingState.ARCHIVED:
                            continue
                        
                        # Ensure soul_id exists
                        if being.soul_id is None:
                            being.soul_id = f"soul_{being.being_id}"
                        
                        # Update soul record in Akasha with current being state
                        akasha_data = self.karma_merchant.access_akasha(being.soul_id)
                        
                        # Add being state to soul record
                        if "being_states" not in akasha_data:
                            akasha_data["being_states"] = []
                        
                        # Record current state
                        being_state_record = {
                            "cycle_number": self.cycle_number,
                            "being_id": being_id,
                            "will_to_live": being.will_to_live,
                            "willpower": being.willpower,
                            "stamina": being.stamina,
                            "stamina_max": being.stamina_max,
                            "stamina_ratio": being.get_stamina_ratio(),
                            "stamina_depleted": being.is_stamina_depleted(),
                            "luck": being.luck,
                            "pleasure": being.pleasure,
                            "pain": being.pain,
                            "decision_fatigue": being.decision_fatigue,
                            "is_sleeping": being.is_sleeping,
                            "cycles_alive": being.cycles_alive,
                            "timestamp": datetime.now().isoformat()
                        }
                        
                        akasha_data["being_states"].append(being_state_record)
                        
                        # Keep being_states bounded (last 50 cycles)
                        if len(akasha_data["being_states"]) > 50:
                            akasha_data["being_states"].pop(0)
                        
                        # Save updated soul record
                        soul_file = self.karma_merchant.akasha_path / f"{being.soul_id}.json"
                        if self.karma_merchant._validate_path_in_project(soul_file):
                            try:
                                with open(soul_file, "w", encoding="utf-8") as f:
                                    json.dump(akasha_data, f, indent=2, ensure_ascii=False)
                                
                                # CRITICAL: Set file permissions
                                try:
                                    soul_file.chmod(0o600)
                                except (OSError, PermissionError):
                                    pass
                            except (IOError, OSError, PermissionError):
                                # Skip if can't write
                                pass
                    
                    except (FileNotFoundError, json.JSONDecodeError, OSError, ValueError):
                        # Skip corrupted or invalid beings
                        continue
        
        except Exception:
            # Log error but don't crash
            pass
        
        # Record to cycle history
        self.cycle_history.append(cycle_data)
        
        # Keep history bounded (last 100 cycles)
        if len(self.cycle_history) > 100:
            self.cycle_history.pop(0)
