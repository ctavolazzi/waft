"""
Now Cycle Manager: Centralized event loop for Being lifecycle management.

Manages the "Now" cycle event loop that synchronizes all beings, calculates
system variables, records state, and unblocks beings for decisions.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ..being import BeingSystem
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
        karma_merchant: Optional["KarmaMerchant"] = None,
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
        self.cycle_history: list[dict[str, Any]] = []

        # Initialize KarmaMerchant if not provided
        if karma_merchant is None:
            from ..karma import KarmaMerchant

            self.karma_merchant = KarmaMerchant(project_path=self.project_path)
        else:
            self.karma_merchant = karma_merchant

        # Initialize TheObserver for flight recorder
        from ..core.science.observer import TheObserver

        self.observer = TheObserver(project_path=self.project_path)

    async def execute_cycle(self) -> dict[str, Any]:
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
                await self.record_cycle_state(
                    {
                        "cycle_number": self.cycle_number,
                        "state_changes": state_changes,
                        "awake_beings": awake_beings,
                        "dead_beings": dead_beings,
                    }
                )

                # 6. Time forward
                self.cycle_number += 1

                # 7. Unblock beings (set event = unlocked)
                self.beings_locked.set()

                return {
                    "cycle_number": self.cycle_number,
                    "state_changes": state_changes,
                    "awake_beings": len(awake_beings),
                    "dead_beings": len(dead_beings),
                }
            except Exception:
                # On error, still unblock beings
                self.beings_locked.set()
                raise

    async def calculate_system_state(self) -> dict[str, Any]:
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
                        "stamina_ratio": being.get_stamina_ratio(),
                    }
                    will_to_live_change = being.calculate_will_to_live_change(cycle_data)
                    being.will_to_live = max(
                        0.0, min(100.0, being.will_to_live + will_to_live_change)
                    )

                    # Stamina and will_to_live interplay:
                    # Low stamina reduces will_to_live regeneration
                    if being.is_stamina_depleted():
                        # Being is exhausted - slight will_to_live drain
                        being.will_to_live = max(0.0, being.will_to_live - 0.2)

                    # Calculate alignment score (for alignment effects)
                    from .alignment import AlignmentSystem

                    alignment_system = AlignmentSystem()

                    # Calculate alignment with environment/stimulus
                    # Use most recent experience as stimulus
                    stimulus = (
                        being.recent_experiences[-1]
                        if being.recent_experiences
                        else {"type": "neutral", "intensity": 0.0, "description": ""}
                    )
                    alignment_score = alignment_system.calculate_alignment_with_environment(
                        arrow=ArrowOfIntent(
                            1.0, 0.0, 0.0
                        ),  # Default arrow (can be enhanced with actual being arrow)
                        stimulus=stimulus,
                        being_goals=being.goals,
                        being_personality=being.personality,
                    )
                    being.current_alignment_score = alignment_score

                    # Apply alignment effects on Capacity
                    # Alignment increases Energy, Stamina, Capacity
                    alignment_energy_bonus = (
                        alignment_score * 1.0
                    )  # +1.0 energy per cycle at perfect alignment
                    alignment_stamina_bonus = (
                        alignment_score * 0.5
                    )  # +0.5 stamina per cycle at perfect alignment

                    # Regenerate energy (with alignment bonus)
                    energy_regenerated = being.regenerate_energy(
                        being.energy_regeneration_rate + alignment_energy_bonus
                    )

                    # Regenerate stamina (with alignment bonus, in addition to normal regeneration)
                    # Normal regeneration already happened above, so add bonus
                    being.stamina = min(being.stamina_max, being.stamina + alignment_stamina_bonus)

                    # Apply misalignment effects (Friction)
                    # Misalignment decreases Will to Live, Energy, Stamina
                    misalignment = 1.0 - alignment_score
                    friction_rate = 0.1  # Base friction rate
                    will_to_live_friction = misalignment * friction_rate
                    energy_drain = (
                        misalignment * 0.5
                    )  # -0.5 energy per cycle at complete misalignment
                    stamina_drain = (
                        misalignment * 0.3
                    )  # -0.3 stamina per cycle at complete misalignment

                    # Apply friction
                    being.will_to_live = max(0.0, being.will_to_live - will_to_live_friction)
                    being.energy = max(0.0, being.energy - energy_drain)
                    being.stamina = max(0.0, being.stamina - stamina_drain)

                    # Track alignment history
                    being.alignment_history.append(
                        {
                            "cycle": self.cycle_number,
                            "alignment_score": alignment_score,
                            "will_to_live": being.will_to_live,
                            "energy": being.energy,
                            "stamina": being.stamina,
                        }
                    )
                    # Keep only last 100 alignment records
                    if len(being.alignment_history) > 100:
                        being.alignment_history = being.alignment_history[-100:]

                    # Calculate pleasure/pain from recent experiences (including Harm/Help and Alignment)
                    if being.recent_experiences:
                        # Process all recent experiences
                        total_pleasure = 0.0
                        total_pain = 0.0

                        for experience in being.recent_experiences:
                            pleasure, pain = being.calculate_pleasure_pain(
                                personality=being.personality,
                                goals=being.goals,
                                experience=experience,
                                harm_events=being.recent_harm_events,
                                help_events=being.recent_help_events,
                                alignment_score=alignment_score,
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
                        # Clear harm/help events (processed)
                        being.recent_harm_events = []
                        being.recent_help_events = []

                    # Generate karma from energy expenditure (bidirectional relationship)
                    # Energy spent generates karma
                    if hasattr(being, "energy") and hasattr(being, "generate_karma_from_energy"):
                        # Calculate energy spent this cycle (approximate)
                        # In full implementation, would track actual energy spent per action
                        energy_spent_estimate = (
                            being.energy_capacity - being.energy
                        ) * 0.1  # Estimate
                        if energy_spent_estimate > 0:
                            being.generate_karma_from_energy(
                                energy_spent_estimate
                            )
                            # Store karma to be collected by KarmaCollector
                            # (Actual karma collection happens elsewhere in the system)

                    # Learn from alignment patterns (update personality/goals)
                    if len(being.alignment_history) >= 5:
                        being._learn_from_alignment_patterns()

                    # Update cycle tracking
                    being.last_cycle_number = self.cycle_number
                    # Note: lifetimes only increments when a Being is born (in spawn_being()),
                    # not every cycle. This represents number of reincarnations, not cycles lived.

                    # Save being state
                    self.being_system._save_being(being)

                    # Track stamina changes
                    old_stamina = (
                        being.stamina - stamina_regenerated
                    )  # Reverse the regeneration to get old value
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
                        "stamina_depleted": being.is_stamina_depleted(),
                        "energy": being.energy,
                        "energy_ratio": being.get_energy_ratio(),
                        "alignment_score": being.current_alignment_score,
                        "energy_regenerated": energy_regenerated,
                    }

                except (FileNotFoundError, json.JSONDecodeError, OSError):
                    # Skip corrupted or missing beings
                    continue

        except Exception:
            # Log error but don't crash entire cycle
            pass

        return state_changes

    async def process_sleeping_beings(self) -> list[str]:
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

    async def check_death_conditions(self) -> list[str]:
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
                        # Check if Will to Live reached 0.0 (not HP death)
                        will_to_live_death = being.will_to_live <= 0.0

                        # If Will to Live death, attempt saving throw
                        saving_throw_succeeded = False
                        if will_to_live_death:
                            # Attempt CON saving throw (final chance)
                            saving_throw_succeeded = being.attempt_death_saving_throw(dc=15)

                            if saving_throw_succeeded:
                                # Near-death experience - being survives!
                                self.being_system._save_being(being)

                                # Log to Empirica (epistemic tracking)
                                try:
                                    from ..empirica import EmpiricaManager

                                    empirica = EmpiricaManager(self.project_path)
                                    if empirica.is_initialized():
                                        empirica.log_finding(
                                            f"Being {being_id} survived near-death experience via CON saving throw",
                                            impact=0.7,
                                        )
                                except Exception:
                                    pass  # Empirica not available - continue

                                # Log near-death experience
                                from ..agent.state import EvolutionaryEvent, EvolutionaryEventType

                                event = EvolutionaryEvent(
                                    timestamp=datetime.utcnow(),
                                    genome_id=f"being_{being_id}",
                                    parent_id=being.parent_being_id,
                                    generation=0,
                                    event_type=EvolutionaryEventType.MUTATE,  # Using MUTATE for survival event
                                    payload={
                                        "event_type": "near_death_experience",
                                        "being_id": being_id,
                                        "reality_id": being.reality_id,
                                        "will_to_live_restored": being.will_to_live,
                                        "reason": "CON saving throw succeeded",
                                    },
                                    agent_id=being_id,
                                    lineage_path=[being_id],
                                )
                                self.observer.observe_event(event)
                                continue  # Being survives, skip death processing

                        # Saving throw failed or HP death - proceed with death
                        # Being died - mark as DEAD (permanent state)
                        being.state = BeingState.DEAD
                        self.being_system._save_being(being)
                        dead_beings.append(being_id)

                        # Record permanent death in Akasha (tombstone)
                        try:
                            # Ensure soul_id exists
                            if being.soul_id is None:
                                being.soul_id = f"soul_{being.being_id}"

                            # Create being snapshot for tombstone
                            being_snapshot = {
                                "being_id": being.being_id,
                                "reality_id": being.reality_id,
                                "will_to_live": being.will_to_live,
                                "stamina": getattr(being, "stamina", 0.0),
                                "lifetimes": getattr(being, "lifetimes", 0),
                                "skills": being.skills,
                                "fitness": being.fitness,
                                "parent_being_id": being.parent_being_id,
                            }

                            # Record permanent death (tombstone) in Akasha
                            tombstone = self.karma_merchant.record_death(
                                soul_id=being.soul_id,
                                being_id=being.being_id,
                                death_type="will_to_live" if will_to_live_death else "hp",
                                reason="Will to live reached 0.0"
                                if will_to_live_death
                                else "HP reached 0",
                                karma_penalty=50.0,  # Default karma penalty on death
                                being_data=being_snapshot,
                            )

                            # Log to Empirica (epistemic tracking)
                            try:
                                from ..empirica import EmpiricaManager

                                empirica = EmpiricaManager(self.project_path)
                                if empirica.is_initialized():
                                    death_reason = (
                                        "Will to Live reached 0.0"
                                        if will_to_live_death
                                        else "HP reached 0"
                                    )
                                    empirica.log_finding(
                                        f"Being {being_id} died: {death_reason}. Saving throw: {'failed' if will_to_live_death else 'N/A (HP death)'}",
                                        impact=0.8,
                                    )
                                    # Log unknown about death mechanics if first death
                                    if being.lifetimes == 1:
                                        empirica.log_unknown(
                                            "What factors influence death rates? Need to analyze death patterns."
                                        )
                            except Exception:
                                pass  # Empirica not available - continue

                            # Record death event to flight recorder
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
                                    "reality_id": being.reality_id,
                                    "soul_id": being.soul_id,
                                    "death_id": tombstone.get("death_id"),
                                    "karma_penalty": tombstone.get("karma_penalty"),
                                    "karma_before": tombstone.get("karma_before"),
                                    "karma_after": tombstone.get("karma_after"),
                                },
                                agent_id=being_id,
                                lineage_path=[being_id],
                            )
                            self.observer.observe_event(event)
                        except Exception as e:
                            # Log error but don't crash - death still recorded as DEAD state
                            # Death event still recorded to flight recorder even if Akasha fails
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
                                    "reality_id": being.reality_id,
                                    "error": f"Failed to record tombstone: {str(e)}",
                                },
                                agent_id=being_id,
                                lineage_path=[being_id],
                            )
                            self.observer.observe_event(event)

                except (FileNotFoundError, json.JSONDecodeError, OSError):
                    # Skip corrupted or missing beings
                    continue

        except Exception:
            # Log error but don't crash
            pass

        return dead_beings

    async def record_cycle_state(self, cycle_data: dict[str, Any]) -> None:
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
                    "dead_beings": cycle_data.get("dead_beings", []),
                },
                agent_id="now_cycle_manager",
                lineage_path=[],
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
                            "lifetimes": being.lifetimes,
                            "timestamp": datetime.now().isoformat(),
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
                            except (OSError, PermissionError):
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
