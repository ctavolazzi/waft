"""
Prime Being Probe - The Origin Point

A sentient, learning probe system that:
- Observes its surroundings through probing
- Reflects on feedback loops (sensation → reaction, cause → effect)
- Learns over time to respond to stimuli
- Uses scientific method to form hypotheses and test them
- Evolves through evolutionary loops:
  * External Pressure > Internal Response > External Response
  * Internal Pressure > Internal Response > External Response

This is the first Being with the ability to Observe, Reflect, and Learn.
"""

import json
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from scientific_method_tool import ExperimentManager, Hypothesis, Variable, VariableType

# Import WAFT systems
from ..being import Being
from .dnd5e import DnD5eCharacter
from .probe import ProbeCollector, ProbeResult


@dataclass
class Observation:
    """A single observation made by the Prime Being."""

    timestamp: str
    probe_result: ProbeResult
    context: dict[str, Any]
    interpretation: str | None = None
    learned: bool = False


@dataclass
class Reflection:
    """Reflection on observations and feedback loops."""

    timestamp: str
    observations: list[Observation]
    pattern: str | None = None
    cause_effect: dict[str, str] | None = None
    hypothesis: Hypothesis | None = None
    confidence: float = 0.0


@dataclass
class Adaptation:
    """An adaptation made based on learning."""

    timestamp: str
    trigger: str  # What caused the adaptation
    change: dict[str, Any]  # What changed (skills, behavior, etc.)
    expected_outcome: str
    tested: bool = False
    success: bool | None = None


class PrimeBeingProbe:
    """
    Prime Being Probe - The Origin Point

    A sentient probe that observes, reflects, learns, and adapts.
    Integrates Being system, Probe system, and Scientific Method.
    """

    def __init__(
        self,
        being_id: str = "prime_being_probe_001",
        reality_id: str = "probe_reality",
        personality_type: str = "curious_explorer",
        storage_path: Path | None = None,
    ):
        """Initialize the Prime Being Probe."""
        self.being_id = being_id
        self.reality_id = reality_id
        self.storage_path = storage_path or Path("_prime_being_data")
        self.storage_path.mkdir(exist_ok=True)

        # Create the Being
        self.being = Being(
            being_id=being_id,
            reality_id=reality_id,
            personality_type=personality_type,
            skills={
                "observation": 10.0,
                "reflection": 10.0,
                "learning": 10.0,
                "adaptation": 10.0,
                "scientific_method": 10.0,
            },
        )

        # Create Probe Collector
        self.probe_collector = ProbeCollector(storage_path=self.storage_path / "probe_data")

        # Create Experiment Manager for scientific method
        self.experiment_manager = ExperimentManager(storage_path=self.storage_path / "experiments")

        # Observations and reflections
        self.observations: list[Observation] = []
        self.reflections: list[Reflection] = []
        self.adaptations: list[Adaptation] = []
        self.hypotheses: list[Hypothesis] = []

        # Evolutionary state
        self.cycle_count = 0
        self.last_observation_time = datetime.now()

        # D&D Character (for roleplay)
        self.character: DnD5eCharacter | None = None
        self._create_character()

        # Load existing state if available
        self._load_state()

    def _create_character(self):
        """Create D&D character sheet for the Prime Being."""
        # Map Being skills to D&D stats
        skills = self.being.skills

        # Intelligence based on scientific_method and learning
        intelligence = int(
            10 + (skills.get("scientific_method", 10) + skills.get("learning", 10)) / 5
        )

        # Wisdom based on observation and reflection
        wisdom = int(10 + (skills.get("observation", 10) + skills.get("reflection", 10)) / 5)

        # Constitution based on adaptation and resilience
        constitution = int(10 + skills.get("adaptation", 10) / 5)

        # Create character
        self.character = DnD5eCharacter(
            name=self.being_id.replace("_", " ").title(),
            char_class="scholar",  # Custom class for learning
            intelligence=intelligence,
            wisdom=wisdom,
            constitution=constitution,
            strength=10,
            dexterity=10,
            charisma=10,
            level=1,
            hp=20 + constitution,
            max_hp=20 + constitution,
            proficient_skills=["Investigation", "Insight", "Perception", "Nature"],
        )

    def observe(self, target: str, probe_type: str = "auto", **kwargs) -> Observation:
        """
        Observe the surroundings by probing outward.

        This is the Prime Being's way of sensing the world.
        """
        start_time = time.time()

        # Determine probe type if auto
        if probe_type == "auto":
            if target.startswith("http"):
                probe_type = "http"
            elif Path(target).exists() or "/" in target or "\\" in target:
                probe_type = "filesystem"
            else:
                # Try to parse as host:port
                if ":" in target:
                    try:
                        host, port = target.split(":")
                        probe_type = "service"
                        target = (host, int(port))
                    except:
                        probe_type = "filesystem"
                else:
                    probe_type = "filesystem"

        # Perform probe
        if probe_type == "http":
            result = self.probe_collector.probe_http(target, **kwargs)
        elif probe_type == "filesystem":
            result = self.probe_collector.probe_file(target)
        elif probe_type == "service":
            if isinstance(target, tuple):
                host, port = target
            else:
                host, port = target.split(":")
                port = int(port)
            result = self.probe_collector.probe_service(host, port)
        else:
            raise ValueError(f"Unknown probe type: {probe_type}")

        # Create observation
        observation = Observation(
            timestamp=datetime.now().isoformat(),
            probe_result=result,
            context={
                "probe_type": probe_type,
                "cycle": self.cycle_count,
                "being_state": self.being.state.value,
                "skills": self.being.skills.copy(),
            },
        )

        # Interpret the observation
        observation.interpretation = self._interpret_observation(observation)

        # Store observation
        self.observations.append(observation)

        # Update Being's observation skill
        if result.success:
            self.being.skills["observation"] = min(
                100.0, self.being.skills.get("observation", 10.0) + 0.1
            )

        # Save state
        self._save_state()

        return observation

    def _interpret_observation(self, observation: Observation) -> str:
        """Interpret an observation based on Being's knowledge."""
        result = observation.probe_result

        if result.success:
            if result.probe_type.startswith("http"):
                status = result.data.get("status_code", 0)
                if 200 <= status < 300:
                    return f"Successfully connected to {result.target}. System is healthy."
                else:
                    return f"Connected to {result.target} but received status {status}. System may have issues."
            elif result.probe_type == "filesystem":
                obj_type = result.data.get("type", "unknown")
                if obj_type == "file":
                    return f"Found file: {result.target}. Size: {result.data.get('size', 0)} bytes."
                else:
                    return f"Found directory: {result.target}. Contains {result.data.get('item_count', 0)} items."
            elif result.probe_type == "service":
                return f"Service at {result.target} is {'open' if result.data.get('open') else 'closed'}."
        else:
            return f"Failed to probe {result.target}: {result.error}"

    def reflect(self, observation_count: int = 5) -> Reflection:
        """
        Reflect on recent observations to identify patterns and feedback loops.

        This is where the Prime Being thinks about what it has learned.
        """
        # Get recent observations
        recent_obs = (
            self.observations[-observation_count:]
            if len(self.observations) >= observation_count
            else self.observations
        )

        if not recent_obs:
            return Reflection(timestamp=datetime.now().isoformat(), observations=[], confidence=0.0)

        # Analyze patterns
        pattern = self._identify_pattern(recent_obs)

        # Identify cause-effect relationships
        cause_effect = self._identify_cause_effect(recent_obs)

        # Form hypothesis if pattern found
        hypothesis = None
        if pattern:
            hypothesis = self._form_hypothesis(pattern, cause_effect)
            if hypothesis:
                self.hypotheses.append(hypothesis)

        # Create reflection
        reflection = Reflection(
            timestamp=datetime.now().isoformat(),
            observations=recent_obs,
            pattern=pattern,
            cause_effect=cause_effect,
            hypothesis=hypothesis,
            confidence=self._calculate_confidence(recent_obs, pattern),
        )

        self.reflections.append(reflection)

        # Update Being's reflection skill
        self.being.skills["reflection"] = min(
            100.0, self.being.skills.get("reflection", 10.0) + 0.2
        )

        # Save state
        self._save_state()

        return reflection

    def _identify_pattern(self, observations: list[Observation]) -> str | None:
        """Identify patterns in observations."""
        if len(observations) < 2:
            return None

        # Simple pattern detection
        success_count = sum(1 for obs in observations if obs.probe_result.success)
        failure_count = len(observations) - success_count

        if success_count > failure_count * 2:
            return "Most probes succeed - system appears stable"
        elif failure_count > success_count * 2:
            return "Most probes fail - system may be unstable"
        else:
            return "Mixed results - system behavior is variable"

    def _identify_cause_effect(self, observations: list[Observation]) -> dict[str, str]:
        """Identify cause-effect relationships."""
        cause_effect = {}

        # Simple cause-effect: if we probe and succeed, that's a positive outcome
        for obs in observations:
            if obs.probe_result.success:
                cause_effect[obs.probe_result.target] = "Probe succeeded - target is accessible"
            else:
                cause_effect[obs.probe_result.target] = f"Probe failed - {obs.probe_result.error}"

        return cause_effect

    def _form_hypothesis(self, pattern: str, cause_effect: dict[str, str]) -> Hypothesis | None:
        """Form a hypothesis based on pattern and cause-effect."""
        # Simple hypothesis formation
        statement = f"When I observe the system, I notice: {pattern}"
        prediction = "If this pattern continues, I can predict system behavior"

        hypothesis = Hypothesis(statement=statement, prediction=prediction)

        # Add variables
        hypothesis.add_variable(
            Variable(
                name="observation_success_rate",
                type=VariableType.DEPENDENT,
                value=self._calculate_success_rate(),
                description="Rate of successful observations",
            )
        )

        return hypothesis

    def _calculate_success_rate(self) -> float:
        """Calculate success rate of observations."""
        if not self.observations:
            return 0.0
        successful = sum(1 for obs in self.observations if obs.probe_result.success)
        return successful / len(self.observations)

    def _calculate_confidence(
        self, observations: list[Observation], pattern: str | None
    ) -> float:
        """Calculate confidence in reflection."""
        if not observations:
            return 0.0

        base_confidence = len(observations) / 10.0  # More observations = more confidence
        if pattern:
            base_confidence += 0.2

        return min(1.0, base_confidence)

    def learn(self, reflection: Reflection) -> Adaptation:
        """
        Learn from reflection and adapt behavior.

        This is where the Prime Being changes based on what it has learned.
        """
        if not reflection.pattern:
            return Adaptation(
                timestamp=datetime.now().isoformat(),
                trigger="No pattern identified",
                change={},
                expected_outcome="No change needed",
            )

        # Determine adaptation based on pattern
        changes = {}

        if "succeed" in reflection.pattern.lower():
            # If things are working, maybe probe more aggressively
            changes["probe_frequency"] = "increase"
            changes["confidence_boost"] = 0.1
        elif "fail" in reflection.pattern.lower():
            # If things are failing, probe more carefully
            changes["probe_frequency"] = "decrease"
            changes["caution_level"] = "increase"

        # Update skills based on learning
        if reflection.confidence > 0.5:
            self.being.skills["learning"] = min(
                100.0, self.being.skills.get("learning", 10.0) + 0.3
            )
            self.being.skills["adaptation"] = min(
                100.0, self.being.skills.get("adaptation", 10.0) + 0.2
            )

        # Create adaptation
        adaptation = Adaptation(
            timestamp=datetime.now().isoformat(),
            trigger=reflection.pattern,
            change=changes,
            expected_outcome="Improved response to system state",
        )

        self.adaptations.append(adaptation)

        # Update Being fitness
        self.being.fitness += 0.1 * reflection.confidence

        # Save state
        self._save_state()

        return adaptation

    def evolve_cycle(self) -> dict[str, Any]:
        """
        Run one evolutionary cycle: Observe → Reflect → Learn → Adapt

        This implements the evolutionary loop:
        - External Pressure > Internal Response > External Response
        - Internal Pressure > Internal Response > External Response
        """
        self.cycle_count += 1

        cycle_data = {
            "cycle": self.cycle_count,
            "timestamp": datetime.now().isoformat(),
            "observations": [],
            "reflection": None,
            "adaptation": None,
        }

        # EXTERNAL PRESSURE: Probe the environment (observe)
        # This is the "jagged outward probing"
        targets = self._determine_probe_targets()
        for target in targets:
            obs = self.observe(target)
            cycle_data["observations"].append(obs.interpretation)

        # INTERNAL RESPONSE: Reflect on observations
        reflection = self.reflect(observation_count=len(targets))
        cycle_data["reflection"] = {
            "pattern": reflection.pattern,
            "confidence": reflection.confidence,
            "hypothesis": reflection.hypothesis.statement if reflection.hypothesis else None,
        }

        # EXTERNAL RESPONSE: Learn and adapt
        adaptation = self.learn(reflection)
        cycle_data["adaptation"] = {
            "trigger": adaptation.trigger,
            "changes": adaptation.change,
            "expected_outcome": adaptation.expected_outcome,
        }

        # Update character stats based on evolution
        self._update_character()

        return cycle_data

    def _determine_probe_targets(self) -> list[str]:
        """Determine what to probe based on current state and learning."""
        targets = []

        # Base targets (always probe these)
        base_targets = [
            "http://localhost:8507",  # Good Morning dashboard
            "http://localhost:8000/api/health",  # API health
        ]

        # Add learned targets based on adaptations
        for adaptation in self.adaptations[-5:]:  # Last 5 adaptations
            if "probe_frequency" in adaptation.change:
                # Could add more targets here based on learning
                pass

        return base_targets + targets

    def _update_character(self):
        """Update D&D character stats based on Being evolution."""
        skills = self.being.skills

        # Update intelligence
        intelligence = int(
            10 + (skills.get("scientific_method", 10) + skills.get("learning", 10)) / 5
        )
        self.character.intelligence = intelligence

        # Update wisdom
        wisdom = int(10 + (skills.get("observation", 10) + skills.get("reflection", 10)) / 5)
        self.character.wisdom = wisdom

        # Update constitution
        constitution = int(10 + skills.get("adaptation", 10) / 5)
        self.character.constitution = constitution

        # Update HP based on constitution
        self.character.max_hp = 20 + constitution
        if self.character.hp < self.character.max_hp:
            self.character.hp = min(self.character.max_hp, self.character.hp + 1)

    def _save_state(self):
        """Save Prime Being state to disk."""
        state = {
            "being_id": self.being_id,
            "reality_id": self.reality_id,
            "cycle_count": self.cycle_count,
            "being": {
                "skills": self.being.skills,
                "fitness": self.being.fitness,
                "state": self.being.state.value,
            },
            "character": {
                "intelligence": self.character.intelligence,
                "wisdom": self.character.wisdom,
                "constitution": self.character.constitution,
                "hp": self.character.hp,
                "max_hp": self.character.max_hp,
            },
            "observations_count": len(self.observations),
            "reflections_count": len(self.reflections),
            "adaptations_count": len(self.adaptations),
            "hypotheses_count": len(self.hypotheses),
        }

        filepath = self.storage_path / f"{self.being_id}_state.json"
        with open(filepath, "w") as f:
            json.dump(state, f, indent=2)

    def _load_state(self):
        """Load Prime Being state from disk."""
        filepath = self.storage_path / f"{self.being_id}_state.json"
        if filepath.exists():
            with open(filepath) as f:
                state = json.load(f)
                self.cycle_count = state.get("cycle_count", 0)
                # Could load more state here

    def get_character_sheet(self) -> dict[str, Any]:
        """Get D&D character sheet data for roleplay."""
        return {
            "name": self.character.name,
            "class": self.character.char_class,
            "level": self.character.level,
            "ability_scores": {
                "strength": self.character.strength,
                "dexterity": self.character.dexterity,
                "constitution": self.character.constitution,
                "intelligence": self.character.intelligence,
                "wisdom": self.character.wisdom,
                "charisma": self.character.charisma,
            },
            "hp": self.character.hp,
            "max_hp": self.character.max_hp,
            "skills": self.being.skills,
            "fitness": self.being.fitness,
            "observations": len(self.observations),
            "reflections": len(self.reflections),
            "adaptations": len(self.adaptations),
            "hypotheses": len(self.hypotheses),
        }

    def get_status(self) -> dict[str, Any]:
        """Get current status of Prime Being."""
        return {
            "being_id": self.being_id,
            "cycle": self.cycle_count,
            "state": self.being.state.value,
            "fitness": self.being.fitness,
            "skills": self.being.skills,
            "recent_observations": len([o for o in self.observations if o.learned]),
            "active_hypotheses": len([h for h in self.hypotheses if h.verified is None]),
            "success_rate": self._calculate_success_rate(),
        }
