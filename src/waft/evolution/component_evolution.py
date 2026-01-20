"""
Component Evolution System

Components evolve over time with traits that develop based on:
- User feedback
- Success/failure rates
- Performance metrics
- Section preferences
- Random mutations for exploration

Each component learns:
- Minimum pages required
- Height estimates
- Preferred sections
- Success patterns
- User preferences
"""

import json
import random
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class SectionPreference(Enum):
    """Where components prefer to appear."""

    TITLE_AREA = "title_area"
    ABSTRACT_AREA = "abstract_area"
    BODY_START = "body_start"
    BODY_MIDDLE = "body_middle"
    BODY_END = "body_end"
    CONCLUSION = "conclusion"
    ANYWHERE = "anywhere"  # No preference


@dataclass
class ComponentTrait:
    """
    Evolving traits of a component.

    These traits develop over time based on experience and feedback.
    """

    # Page requirements
    min_pages_required: float = 1.0  # Minimum pages needed to use this component
    max_pages_allowed: float | None = None  # Maximum pages where component works

    # Size estimates
    height_estimate: float = 0.1  # Estimated height (0.0-1.0 of a page)
    height_variance: float = 0.05  # How much height can vary

    # Section preferences (weights: 0.0-1.0)
    section_preferences: dict[SectionPreference, float] = field(
        default_factory=lambda: {SectionPreference.ANYWHERE: 1.0}
    )

    # Success metrics
    success_count: int = 0
    failure_count: int = 0
    avg_fitness_when_used: float = 0.0

    # User feedback
    user_likes: int = 0
    user_dislikes: int = 0
    user_feedback_score: float = 0.5  # 0.0 = disliked, 1.0 = loved

    # Evolution metadata
    generation: int = 0
    mutations_applied: list[str] = field(default_factory=list)
    last_evolved: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "min_pages_required": self.min_pages_required,
            "max_pages_allowed": self.max_pages_allowed,
            "height_estimate": self.height_estimate,
            "height_variance": self.height_variance,
            "section_preferences": {k.value: v for k, v in self.section_preferences.items()},
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "avg_fitness_when_used": self.avg_fitness_when_used,
            "user_likes": self.user_likes,
            "user_dislikes": self.user_dislikes,
            "user_feedback_score": self.user_feedback_score,
            "generation": self.generation,
            "mutations_applied": self.mutations_applied,
            "last_evolved": self.last_evolved.isoformat() if self.last_evolved else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ComponentTrait":
        """Deserialize from dictionary."""
        section_prefs = {
            SectionPreference(k): v for k, v in data.get("section_preferences", {}).items()
        }
        if not section_prefs:
            section_prefs = {SectionPreference.ANYWHERE: 1.0}

        return cls(
            min_pages_required=data.get("min_pages_required", 1.0),
            max_pages_allowed=data.get("max_pages_allowed"),
            height_estimate=data.get("height_estimate", 0.1),
            height_variance=data.get("height_variance", 0.05),
            section_preferences=section_prefs,
            success_count=data.get("success_count", 0),
            failure_count=data.get("failure_count", 0),
            avg_fitness_when_used=data.get("avg_fitness_when_used", 0.0),
            user_likes=data.get("user_likes", 0),
            user_dislikes=data.get("user_dislikes", 0),
            user_feedback_score=data.get("user_feedback_score", 0.5),
            generation=data.get("generation", 0),
            mutations_applied=data.get("mutations_applied", []),
            last_evolved=datetime.fromisoformat(data["last_evolved"])
            if data.get("last_evolved")
            else None,
        )

    def get_fitness(self) -> float:
        """Calculate overall fitness score (0.0-1.0)."""
        # Base fitness from success rate
        total_uses = self.success_count + self.failure_count
        if total_uses == 0:
            success_rate = 0.5  # Neutral if never used
        else:
            success_rate = self.success_count / total_uses

        # Weighted combination
        fitness = (
            success_rate * 0.4  # 40% success rate
            + self.avg_fitness_when_used * 0.3  # 30% performance
            + self.user_feedback_score * 0.3  # 30% user feedback
        )

        return min(1.0, max(0.0, fitness))

    def mutate(self, mutation_rate: float = 0.1) -> "ComponentTrait":
        """
        Create a mutated version of this trait.

        Applies random mutations for exploration.
        """
        new_trait = ComponentTrait(
            min_pages_required=self.min_pages_required,
            max_pages_allowed=self.max_pages_allowed,
            height_estimate=self.height_estimate,
            height_variance=self.height_variance,
            section_preferences=self.section_preferences.copy(),
            success_count=self.success_count,
            failure_count=self.failure_count,
            avg_fitness_when_used=self.avg_fitness_when_used,
            user_likes=self.user_likes,
            user_dislikes=self.user_dislikes,
            user_feedback_score=self.user_feedback_score,
            generation=self.generation + 1,
            mutations_applied=self.mutations_applied.copy(),
        )

        # Random mutations
        if random.random() < mutation_rate:
            # Mutate height estimate
            new_trait.height_estimate = max(
                0.05, min(0.5, self.height_estimate + random.gauss(0, 0.02))
            )
            new_trait.mutations_applied.append("height_estimate")

        if random.random() < mutation_rate:
            # Mutate min pages
            new_trait.min_pages_required = max(1.0, self.min_pages_required + random.gauss(0, 0.1))
            new_trait.mutations_applied.append("min_pages_required")

        if random.random() < mutation_rate:
            # Mutate section preferences
            section = random.choice(list(SectionPreference))
            new_trait.section_preferences[section] = random.uniform(0.5, 1.0)
            new_trait.mutations_applied.append(f"section_preference_{section.value}")

        new_trait.last_evolved = datetime.utcnow()
        return new_trait

    def learn_from_result(
        self,
        success: bool,
        fitness: float,
        pages_used: int,
        section_used: SectionPreference | None = None,
    ):
        """Learn from a generation attempt."""
        if success:
            self.success_count += 1
            # Update average fitness
            total = self.success_count + self.failure_count
            self.avg_fitness_when_used = (
                self.avg_fitness_when_used * (total - 1) + fitness
            ) / total
        else:
            self.failure_count += 1

        # Learn about page requirements
        if success and pages_used < self.min_pages_required:
            # Can work with fewer pages than we thought
            self.min_pages_required = pages_used * 0.9  # Slight margin

        # Learn about section preferences
        if section_used and success:
            # Increase preference for successful sections
            current = self.section_preferences.get(section_used, 0.5)
            self.section_preferences[section_used] = min(1.0, current + 0.1)

    def learn_from_user_feedback(self, liked: bool, feedback_strength: float = 1.0):
        """Learn from explicit user feedback."""
        if liked:
            self.user_likes += 1
            self.user_feedback_score = min(
                1.0, self.user_feedback_score + (0.1 * feedback_strength)
            )
        else:
            self.user_dislikes += 1
            self.user_feedback_score = max(
                0.0, self.user_feedback_score - (0.1 * feedback_strength)
            )


@dataclass
class EvolvedComponent:
    """
    A component with evolving traits.

    Components learn and adapt over time.
    """

    component_type: str  # e.g., "title", "image", "section"
    component_id: str  # Unique identifier
    trait: ComponentTrait
    content_template: str | None = None  # Template for generating content

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "component_type": self.component_type,
            "component_id": self.component_id,
            "trait": self.trait.to_dict(),
            "content_template": self.content_template,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EvolvedComponent":
        """Deserialize from dictionary."""
        return cls(
            component_type=data["component_type"],
            component_id=data["component_id"],
            trait=ComponentTrait.from_dict(data["trait"]),
            content_template=data.get("content_template"),
        )


class ComponentEvolutionEngine:
    """
    Engine that evolves components over time.

    Manages:
    - Component trait evolution
    - Learning from feedback
    - Mutation and exploration
    - Persistent storage
    """

    def __init__(self, evolution_dir: Path | None = None):
        """
        Initialize evolution engine.

        Args:
            evolution_dir: Directory for storing evolution data
        """
        if evolution_dir is None:
            evolution_dir = Path("_genetics/component_evolution")
        self.evolution_dir = Path(evolution_dir)
        self.evolution_dir.mkdir(parents=True, exist_ok=True)

        self.components: dict[str, EvolvedComponent] = {}
        self.evolution_history: list[dict[str, Any]] = []

        # Load existing components
        self._load_components()

    def _load_components(self):
        """Load evolved components from disk."""
        components_file = self.evolution_dir / "components.json"
        if components_file.exists():
            try:
                with open(components_file) as f:
                    data = json.load(f)
                    for comp_data in data.get("components", []):
                        comp = EvolvedComponent.from_dict(comp_data)
                        self.components[comp.component_id] = comp
                print(f"Loaded {len(self.components)} evolved components")
            except Exception as e:
                print(f"Warning: Failed to load components: {e}")

    def _save_components(self):
        """Save evolved components to disk."""
        components_file = self.evolution_dir / "components.json"
        data = {
            "components": [comp.to_dict() for comp in self.components.values()],
            "last_updated": datetime.utcnow().isoformat(),
        }
        with open(components_file, "w") as f:
            json.dump(data, f, indent=2)

    def get_or_create_component(
        self,
        component_type: str,
        component_id: str | None = None,
    ) -> EvolvedComponent:
        """Get existing component or create new one."""
        if component_id is None:
            component_id = f"{component_type}_{len(self.components)}"

        if component_id in self.components:
            return self.components[component_id]

        # Create new component
        component = EvolvedComponent(
            component_type=component_type,
            component_id=component_id,
            trait=ComponentTrait(),
        )
        self.components[component_id] = component
        self._save_components()

        return component

    def evolve_component(
        self,
        component_id: str,
        mutation_rate: float = 0.1,
    ) -> EvolvedComponent:
        """Evolve a component by creating a mutated version."""
        if component_id not in self.components:
            raise ValueError(f"Component {component_id} not found")

        parent = self.components[component_id]
        new_trait = parent.trait.mutate(mutation_rate=mutation_rate)

        # Create evolved component
        evolved = EvolvedComponent(
            component_type=parent.component_type,
            component_id=f"{component_id}_gen{new_trait.generation}",
            trait=new_trait,
            content_template=parent.content_template,
        )

        self.components[evolved.component_id] = evolved
        self._save_components()

        # Record evolution
        self.evolution_history.append(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "parent_id": component_id,
                "evolved_id": evolved.component_id,
                "mutations": new_trait.mutations_applied,
            }
        )

        return evolved

    def learn_from_generation(
        self,
        component_id: str,
        success: bool,
        fitness: float,
        pages_used: int,
        section_used: SectionPreference | None = None,
    ):
        """Record learning from a generation attempt."""
        if component_id not in self.components:
            return

        component = self.components[component_id]
        component.trait.learn_from_result(
            success=success,
            fitness=fitness,
            pages_used=pages_used,
            section_used=section_used,
        )
        self._save_components()

    def learn_from_user_feedback(
        self,
        component_id: str,
        liked: bool,
        feedback_strength: float = 1.0,
    ):
        """Record user feedback."""
        if component_id not in self.components:
            return

        component = self.components[component_id]
        component.trait.learn_from_user_feedback(liked, feedback_strength)
        self._save_components()

    def get_best_components(
        self,
        component_type: str | None = None,
        min_fitness: float = 0.0,
        limit: int = 10,
    ) -> list[EvolvedComponent]:
        """Get best components by fitness."""
        candidates = list(self.components.values())

        if component_type:
            candidates = [c for c in candidates if c.component_type == component_type]

        # Filter by fitness
        candidates = [c for c in candidates if c.trait.get_fitness() >= min_fitness]

        # Sort by fitness
        candidates.sort(key=lambda c: c.trait.get_fitness(), reverse=True)

        return candidates[:limit]

    def get_evolution_report(self) -> str:
        """Generate evolution report."""
        if not self.components:
            return "# Component Evolution Report\n\nNo components evolved yet."

        report = f"""# Component Evolution Report

Generated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}

## Overview
- **Total Components**: {len(self.components)}
- **Total Evolutions**: {len(self.evolution_history)}

## Component Fitness Rankings

"""
        # Group by type
        by_type: dict[str, list[EvolvedComponent]] = {}
        for comp in self.components.values():
            if comp.component_type not in by_type:
                by_type[comp.component_type] = []
            by_type[comp.component_type].append(comp)

        for comp_type, components in by_type.items():
            components.sort(key=lambda c: c.trait.get_fitness(), reverse=True)
            report += f"### {comp_type.title()} Components\n\n"

            for comp in components[:5]:  # Top 5
                trait = comp.trait
                report += f"- **{comp.component_id}** (Gen {trait.generation})\n"
                report += f"  - Fitness: {trait.get_fitness():.3f}\n"
                report += f"  - Success Rate: {trait.success_count}/{trait.success_count + trait.failure_count}\n"
                report += f"  - User Feedback: {trait.user_feedback_score:.3f}\n"
                report += f"  - Min Pages: {trait.min_pages_required:.1f}\n"
                report += f"  - Height: {trait.height_estimate:.3f} ± {trait.height_variance:.3f}\n"
                report += "\n"

        return report
