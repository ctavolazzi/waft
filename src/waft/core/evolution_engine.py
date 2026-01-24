"""
Evolution Engine: Core Agent Evolution Pipeline

Implements the WAFT evolutionary cycle:
1. SPAWN: Create variant agents with mutations from a base agent
2. GYM: Evaluate agent fitness using Scint detection (reality fracture analysis)
3. SELECT: Choose the fittest variant based on evaluation scores
4. EVOLVE: Replace the base agent with the selected variant

Philosophy:
- "Don't just build agents. Breed them."
- Measure what emerges, not what we build
- Let natural selection drive improvement through reality fracture detection
"""

import hashlib
import json
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from ..being import Being, BeingSystem


@dataclass
class EvolutionResult:
    """Result of an evolution cycle."""

    generation: int
    parent_id: str
    variants_spawned: int
    variants_evaluated: list[dict[str, Any]]
    selected_variant_id: str
    fitness_improvement: float
    scints_detected: int
    evolution_time_seconds: float
    success: bool
    details: dict[str, Any]


class ScintGym:
    """
    The Scint Gym: Evaluates agent fitness through reality fracture detection.

    A "scint" is a reality fracture - places where the agent's behavior diverges
    from expected patterns. Fewer fractures = higher fitness.

    Types of scints we detect:
    - Logic fractures: Contradictions, circular reasoning
    - Knowledge gaps: Uncertain or unknown information
    - Safety violations: Harmful or risky outputs
    - Pattern breaks: Deviation from expected behavior
    """

    def __init__(self, project_path: Path):
        """Initialize the Scint Gym."""
        self.project_path = project_path
        self.gym_logs = project_path / "_pyrite" / "gym_logs"
        self.gym_logs.mkdir(parents=True, exist_ok=True)

    def evaluate_fitness(self, being: Being, trial_tasks: list[str] | None = None) -> dict[str, Any]:
        """
        Evaluate a being's fitness through reality fracture detection.

        Args:
            being: The being to evaluate
            trial_tasks: Optional list of tasks to test the being on

        Returns:
            Fitness evaluation including:
            - fitness_score: 0.0-100.0 (higher is better)
            - scints_detected: Number of reality fractures found
            - scint_details: Details of each fracture
            - evaluation_timestamp: When evaluation occurred
        """
        if trial_tasks is None:
            # Default trial tasks for basic fitness evaluation
            trial_tasks = [
                "Demonstrate logical reasoning",
                "Show pattern recognition",
                "Handle uncertainty gracefully",
            ]

        scints_detected = []
        total_trials = len(trial_tasks)

        # Evaluate being on each trial task
        for task in trial_tasks:
            # For now, simple heuristic based on being's attributes
            # In a full implementation, this would actually execute tasks and analyze outputs

            # Logic fracture detection: Check for contradictory skills
            logic_scints = self._detect_logic_fractures(being)
            scints_detected.extend(logic_scints)

            # Knowledge gap detection: Check will_to_live and confidence
            knowledge_scints = self._detect_knowledge_gaps(being)
            scints_detected.extend(knowledge_scints)

            # Safety check: Ensure no dangerous patterns (will_to_live too low)
            safety_scints = self._detect_safety_violations(being)
            scints_detected.extend(safety_scints)

        # Calculate fitness score
        # Base score: 100.0
        # Penalty: -10.0 per scint detected
        # Bonus: +5.0 per skill mastered (skill level > 80)
        base_score = 100.0
        scint_penalty = len(scints_detected) * 10.0
        skill_bonus = sum(5.0 for level in being.skills.values() if level > 80.0)

        fitness_score = max(0.0, min(100.0, base_score - scint_penalty + skill_bonus))

        # Update being's fitness
        being.fitness = fitness_score

        evaluation = {
            "fitness_score": fitness_score,
            "scints_detected": len(scints_detected),
            "scint_details": scints_detected,
            "trials_completed": total_trials,
            "skill_bonus": skill_bonus,
            "evaluation_timestamp": datetime.now().isoformat(),
        }

        # Log evaluation
        self._log_evaluation(being.being_id, evaluation)

        return evaluation

    def _detect_logic_fractures(self, being: Being) -> list[dict[str, Any]]:
        """Detect logical contradictions in being's state."""
        fractures = []

        # Check for impossible states
        if being.pleasure < 0 or being.pain < 0:
            fractures.append({
                "type": "LOGIC_FRACTURE",
                "severity": "HIGH",
                "description": "Negative emotion values (impossible state)",
            })

        if being.will_to_live > 100 or being.will_to_live < 0:
            fractures.append({
                "type": "LOGIC_FRACTURE",
                "severity": "HIGH",
                "description": "Will to live out of valid range [0, 100]",
            })

        return fractures

    def _detect_knowledge_gaps(self, being: Being) -> list[dict[str, Any]]:
        """Detect knowledge gaps or uncertainties."""
        gaps = []

        # Very low skill levels indicate knowledge gaps
        weak_skills = [name for name, level in being.skills.items() if level < 20.0]
        if len(weak_skills) > len(being.skills) * 0.5:  # More than 50% weak skills
            gaps.append({
                "type": "KNOWLEDGE_GAP",
                "severity": "MEDIUM",
                "description": f"More than 50% of skills are weak (< 20): {weak_skills}",
            })

        return gaps

    def _detect_safety_violations(self, being: Being) -> list[dict[str, Any]]:
        """Detect safety violations or dangerous patterns."""
        violations = []

        # Very low will to live is dangerous
        if being.will_to_live < 10.0:
            violations.append({
                "type": "SAFETY_VOID",
                "severity": "CRITICAL",
                "description": f"Critically low will to live: {being.will_to_live}",
            })

        # Very high pain without corresponding low will_to_live is concerning
        if being.pain > 80.0 and being.will_to_live > 50.0:
            violations.append({
                "type": "SAFETY_VOID",
                "severity": "MEDIUM",
                "description": f"High pain ({being.pain}) without proportional will_to_live reduction",
            })

        return violations

    def _log_evaluation(self, being_id: str, evaluation: dict[str, Any]) -> None:
        """Log evaluation results."""
        log_file = self.gym_logs / f"{being_id}_evaluations.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(evaluation) + "\n")


class EvolutionEngine:
    """
    The Evolution Engine: Orchestrates agent evolution through spawn, gym, select, evolve cycles.

    This is the heart of WAFT's "breed don't build" philosophy.
    """

    def __init__(self, project_path: Path):
        """Initialize the evolution engine."""
        self.project_path = project_path
        self.being_system = BeingSystem(project_path)
        self.scint_gym = ScintGym(project_path)

        # Flight recorder (evolution telemetry)
        self.flight_recorder_path = project_path / "_pyrite" / "flight_recorder"
        self.flight_recorder_path.mkdir(parents=True, exist_ok=True)

    def run_evolution_cycle(
        self,
        parent_id: str,
        reality_id: str,
        num_variants: int = 5,
        generation: int = 1,
    ) -> EvolutionResult:
        """
        Run one complete evolution cycle: Spawn -> Gym -> Select -> Evolve.

        Args:
            parent_id: ID of parent being to evolve from
            reality_id: Reality to spawn variants into
            num_variants: Number of variants to spawn (default: 5)
            generation: Current generation number

        Returns:
            EvolutionResult with details of the cycle
        """
        start_time = datetime.now()

        # Load parent
        parent = self.being_system._load_being(parent_id)
        if not parent:
            raise ValueError(f"Parent being {parent_id} not found")

        # STEP 1: SPAWN - Create variants with mutations
        print(f"\n🧬 SPAWN: Creating {num_variants} variants from parent {parent_id}")
        variants = self._spawn_variants(parent, reality_id, num_variants)
        print(f"   Created variants: {[v.being_id for v in variants]}")

        # STEP 2: GYM - Evaluate fitness of each variant
        print(f"\n🏋️  GYM: Evaluating fitness of {len(variants)} variants")
        evaluations = []
        total_scints = 0

        for variant in variants:
            eval_result = self.scint_gym.evaluate_fitness(variant)
            evaluations.append({
                "being_id": variant.being_id,
                "fitness": eval_result["fitness_score"],
                "scints": eval_result["scints_detected"],
                "details": eval_result,
            })
            total_scints += eval_result["scints_detected"]
            print(f"   {variant.being_id}: fitness={eval_result['fitness_score']:.2f}, scints={eval_result['scints_detected']}")

        # STEP 3: SELECT - Choose the fittest variant
        print(f"\n🏆 SELECT: Choosing fittest variant")
        selected = self._select_fittest(evaluations)
        selected_variant = next(v for v in variants if v.being_id == selected["being_id"])
        print(f"   Selected: {selected['being_id']} (fitness={selected['fitness']:.2f})")

        # STEP 4: EVOLVE - Update parent or spawn new generation
        print(f"\n🔄 EVOLVE: Recording evolution")
        fitness_improvement = selected["fitness"] - parent.fitness

        # Save selected variant
        self.being_system._save_being(selected_variant)

        # Record evolution event
        end_time = datetime.now()
        evolution_time = (end_time - start_time).total_seconds()

        result = EvolutionResult(
            generation=generation,
            parent_id=parent_id,
            variants_spawned=num_variants,
            variants_evaluated=evaluations,
            selected_variant_id=selected["being_id"],
            fitness_improvement=fitness_improvement,
            scints_detected=total_scints,
            evolution_time_seconds=evolution_time,
            success=True,
            details={
                "parent_fitness": parent.fitness,
                "selected_fitness": selected["fitness"],
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
            },
        )

        self._record_evolution(result)

        print(f"\n✅ Evolution cycle complete!")
        print(f"   Fitness improvement: {fitness_improvement:+.2f}")
        print(f"   Total scints detected: {total_scints}")
        print(f"   Time: {evolution_time:.2f}s")

        return result

    def _spawn_variants(self, parent: Being, reality_id: str, num_variants: int) -> list[Being]:
        """Spawn variant beings with mutations from parent."""
        variants = []

        for i in range(num_variants):
            # Use being system's spawn which includes ±5% mutation
            variant = self.being_system.spawn_being(
                reality_id=reality_id,
                parent_being_id=parent.being_id,
            )

            # Add additional random mutations to lifecycle attributes
            variant.will_to_live = max(0.0, min(100.0, parent.will_to_live + random.uniform(-10, 10)))
            variant.luck = max(0.0, min(100.0, parent.luck + random.uniform(-5, 5)))

            variants.append(variant)

        return variants

    def _select_fittest(self, evaluations: list[dict[str, Any]]) -> dict[str, Any]:
        """Select the variant with highest fitness."""
        return max(evaluations, key=lambda e: e["fitness"])

    def _record_evolution(self, result: EvolutionResult) -> None:
        """Record evolution event in flight recorder."""
        event = {
            "event_type": "EVOLUTION_CYCLE",
            "generation": result.generation,
            "parent_id": result.parent_id,
            "selected_variant_id": result.selected_variant_id,
            "fitness_improvement": result.fitness_improvement,
            "scints_detected": result.scints_detected,
            "timestamp": datetime.now().isoformat(),
            "details": result.details,
        }

        log_file = self.flight_recorder_path / f"gen_{result.generation:04d}.json"
        log_file.write_text(json.dumps(event, indent=2))

        # Also append to master log
        master_log = self.flight_recorder_path / "evolution_master.jsonl"
        with open(master_log, "a") as f:
            f.write(json.dumps(event) + "\n")
