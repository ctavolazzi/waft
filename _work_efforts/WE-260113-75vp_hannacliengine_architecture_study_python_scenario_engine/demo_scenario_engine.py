"""
Demo Scenario Engine - HannaCLIEngine-inspired Python implementation

A minimal working demo that demonstrates the core concepts:
- JSON-based scenario files
- Sequence/Choice/Container architecture
- Conditional choices
- Execution tracking for PDF generation
- Decision tree integration for intelligent choice recommendations
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from waft.core.scenario_decision_tree import ScenarioDecisionTree, ScenarioState

    DECISION_TREE_AVAILABLE = True
except ImportError:
    DECISION_TREE_AVAILABLE = False
    ScenarioDecisionTree = None
    ScenarioState = None


@dataclass
class ScenarioEvent:
    """Tracks a single event during scenario execution."""

    sequence_id: str
    sequence_type: str
    main_text: str
    secondary_text: str
    choices_available: list[str]
    choice_made: str | None = None
    outcome_text: str | None = None
    containers_updated: dict[str, list[str]] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class ScenarioEngine:
    """Minimal scenario engine inspired by HannaCLIEngine."""

    def __init__(self, scenario_file: Path, use_decision_tree: bool = False):
        """
        Initialize engine with a scenario JSON file.

        Args:
            scenario_file: Path to scenario JSON file
            use_decision_tree: If True, enable decision tree for choice recommendations
        """
        self.scenario_file = scenario_file
        self.scenario_data: dict[str, Any] = {}
        self.sequence_map: dict[str, int] = {}
        self.containers: dict[str, list[str]] = {}
        self.events: list[ScenarioEvent] = []
        self.current_sequence_id: str | None = None

        # Decision tree integration
        self.decision_tree: ScenarioDecisionTree | None = None
        self.use_decision_tree = use_decision_tree and DECISION_TREE_AVAILABLE
        if self.use_decision_tree:
            self.decision_tree = ScenarioDecisionTree()
        self.training_states: list[ScenarioState] = []
        self.training_choices: list[str] = []

    def load(self) -> bool:
        """Load scenario from JSON file."""
        try:
            with open(self.scenario_file) as f:
                self.scenario_data = json.load(f)

            # Map sequence IDs to indexes
            sequences = self.scenario_data.get("sequences", [])
            for i, seq in enumerate(sequences):
                self.sequence_map[seq["sqId"]] = i

            # Initialize containers
            for container_name in self.scenario_data.get("gameContainers", []):
                self.containers[container_name] = []

            return True
        except Exception as e:
            print(f"Error loading scenario: {e}")
            return False

    def run_sequence(self, sequence_id: str) -> bool:
        """Run a sequence by ID."""
        if sequence_id not in self.sequence_map:
            print(f"Sequence {sequence_id} not found!")
            return False

        self.current_sequence_id = sequence_id
        seq_index = self.sequence_map[sequence_id]
        sequence = self.scenario_data["sequences"][seq_index]

        # Create event
        event = ScenarioEvent(
            sequence_id=sequence_id,
            sequence_type=sequence.get("sqType", "ordinary"),
            main_text=sequence.get("mainText", ""),
            secondary_text=sequence.get("secondaryText", ""),
            choices_available=[],
        )

        # Display sequence
        print(f"\n{'=' * 60}")
        print(f"Sequence: {sequence_id}")
        print(f"{'=' * 60}\n")
        print(sequence.get("mainText", ""))
        print(f"\n{sequence.get('secondaryText', '')}\n")

        # Handle end sequences
        if sequence.get("sqType") == "end":
            print("\nTHE END - Thanks for playing!")
            self.events.append(event)
            return False

        # Process choices
        choices = sequence.get("choices", [])
        valid_choices = []

        for choice in choices:
            choice_type = choice.get("choiceType", "set")

            if choice_type == "set":
                # Always show
                letter = choice.get("choiceLetter", "")
                text = choice.get("choiceText", "")
                print(f"{letter}. {text}")
                valid_choices.append(letter)
                event.choices_available.append(f"{letter}: {text}")

            elif choice_type == "conditional":
                # Check condition
                condition = choice.get("choiceCondition", {})
                container_name = condition.get("container", "")
                required_value = condition.get("value", "")

                # Check if value exists in container
                if container_name in self.containers:
                    if required_value in self.containers[container_name]:
                        letter = choice.get("choiceLetter", "")
                        text = choice.get("choiceText", "")
                        print(f"{letter}. {text}")
                        valid_choices.append(letter)
                        event.choices_available.append(f"{letter}: {text} (conditional)")

        event.choices_available = valid_choices
        self.events.append(event)

        # Collect training data if decision tree is enabled
        if self.use_decision_tree and self.decision_tree:
            state = self._extract_state_features(sequence_id)
            self.training_states.append(state)

        return True

    def make_choice(self, sequence_id: str, choice_letter: str) -> str | None:
        """Process a player choice and return next sequence ID."""
        seq_index = self.sequence_map[sequence_id]
        sequence = self.scenario_data["sequences"][seq_index]
        choices = sequence.get("choices", [])

        # Find the choice
        choice = None
        for c in choices:
            if c.get("choiceLetter", "").upper() == choice_letter.upper():
                # Check if it's valid (set or conditional that passed)
                choice_type = c.get("choiceType", "set")
                if choice_type == "set":
                    choice = c
                    break
                elif choice_type == "conditional":
                    condition = c.get("choiceCondition", {})
                    container_name = condition.get("container", "")
                    required_value = condition.get("value", "")
                    if container_name in self.containers:
                        if required_value in self.containers[container_name]:
                            choice = c
                            break

        if not choice:
            print(f"Invalid choice: {choice_letter}")
            return None

        # Display outcome
        outcome = choice.get("outcomeText", "")
        print(f"\n{outcome}\n")

        # Update event
        if self.events:
            self.events[-1].choice_made = choice_letter
            self.events[-1].outcome_text = outcome

        # Collect training data if decision tree is enabled
        if self.use_decision_tree and self.decision_tree and self.training_states:
            # The state was already added in run_sequence, now add the choice
            self.training_choices.append(choice_letter.upper())

        # Process container add
        container_add = choice.get("containerAdd", {})
        if container_add.get("container", "") != "":
            container_name = container_add.get("container", "")
            value = container_add.get("value", "")
            if container_name in self.containers:
                self.containers[container_name].append(value)
                print(f"* Added '{value}' to {container_name} *")

                # Update event
                if self.events:
                    self.events[-1].containers_updated[container_name] = list(
                        self.containers[container_name]
                    )

        # Return next sequence
        next_sq = choice.get("nextSq", "")
        return next_sq if next_sq else None

    def _extract_state_features(self, sequence_id: str) -> ScenarioState:
        """
        Extract scenario state features for decision tree.

        Args:
            sequence_id: Current sequence ID

        Returns:
            ScenarioState object with current state
        """
        if not DECISION_TREE_AVAILABLE:
            raise ImportError("Decision tree module not available")

        seq_index = self.sequence_map.get(sequence_id, 0)
        sequence = (
            self.scenario_data["sequences"][seq_index]
            if seq_index < len(self.scenario_data["sequences"])
            else {}
        )

        # Get visited sequences
        visited_sequences = [e.sequence_id for e in self.events]

        # Get choice history
        choice_history = [e.choice_made for e in self.events if e.choice_made]

        # Get available choices for current sequence
        available_choices = []
        choices = sequence.get("choices", [])
        for choice in choices:
            choice_type = choice.get("choiceType", "set")
            if choice_type == "set":
                available_choices.append(choice.get("choiceLetter", ""))
            elif choice_type == "conditional":
                condition = choice.get("choiceCondition", {})
                container_name = condition.get("container", "")
                required_value = condition.get("value", "")
                if container_name in self.containers:
                    if required_value in self.containers[container_name]:
                        available_choices.append(choice.get("choiceLetter", ""))

        return ScenarioState(
            sequence_id=sequence_id,
            sequence_type=sequence.get("sqType", "ordinary"),
            containers=dict(self.containers),  # Copy to avoid mutation
            visited_sequences=visited_sequences,
            choice_history=choice_history,
            available_choices=available_choices,
        )

    def recommend_choice(self, sequence_id: str) -> tuple | None:
        """
        Use decision tree to recommend best choice.

        Args:
            sequence_id: Current sequence ID

        Returns:
            Tuple of (choice_letter, confidence) or None if no recommendation
        """
        if not self.use_decision_tree or not self.decision_tree:
            return None

        if not self.decision_tree.is_trained:
            return None

        state = self._extract_state_features(sequence_id)
        recommendation = self.decision_tree.recommend_choice(
            state, available_choices=state.available_choices
        )

        return recommendation

    def train_decision_tree(self) -> bool:
        """
        Train decision tree on collected training data.

        Returns:
            True if training succeeded, False otherwise
        """
        if not self.use_decision_tree or not self.decision_tree:
            return False

        if len(self.training_states) == 0 or len(self.training_choices) == 0:
            return False

        if len(self.training_states) != len(self.training_choices):
            # Trim to match lengths
            min_len = min(len(self.training_states), len(self.training_choices))
            self.training_states = self.training_states[:min_len]
            self.training_choices = self.training_choices[:min_len]

        try:
            self.decision_tree.train(self.training_states, self.training_choices)
            return True
        except Exception as e:
            print(f"Error training decision tree: {e}")
            return False

    def auto_train_decision_tree(self, min_events: int = 5) -> bool:
        """
        Automatically train decision tree after collecting enough events.

        Args:
            min_events: Minimum number of events required before training

        Returns:
            True if training occurred, False otherwise
        """
        if len(self.events) >= min_events and not self.decision_tree.is_trained:
            return self.train_decision_tree()
        return False

    def start(self) -> bool:
        """Start the scenario from the beginning."""
        start_sq = self.scenario_data.get("startSq", "")
        if not start_sq:
            print("No start sequence defined!")
            return False

        return self.run_sequence(start_sq)

    def to_markdown(self) -> str:
        """Convert execution events to markdown story."""
        md = f"""# {self.scenario_data.get("gameTitle", "Scenario")}

**Author:** {self.scenario_data.get("gameAuthor", "Unknown")}
**Description:** {self.scenario_data.get("gameDesc", "")}
**Generated:** {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

---

## Execution Log

"""

        for i, event in enumerate(self.events, 1):
            md += f"### Sequence {i}: {event.sequence_id}\n\n"
            md += f"{event.main_text}\n\n"

            if event.secondary_text:
                md += f"*{event.secondary_text}*\n\n"

            if event.choices_available:
                md += "**Available Choices:**\n"
                for choice in event.choices_available:
                    md += f"- {choice}\n"
                md += "\n"

            if event.choice_made:
                md += f"**Choice Made:** {event.choice_made}\n\n"
                if event.outcome_text:
                    md += f"{event.outcome_text}\n\n"

            if event.containers_updated:
                md += "**Container State:**\n"
                for container, values in event.containers_updated.items():
                    md += f"- **{container}**: {', '.join(values) if values else '(empty)'}\n"
                md += "\n"

            md += "---\n\n"

        # Final container state
        md += "## Final Container State\n\n"
        for container, values in self.containers.items():
            md += f"- **{container}**: {', '.join(values) if values else '(empty)'}\n"

        return md


def run_demo_scenario(
    scenario_file: Path,
    auto_play: bool = True,
    use_decision_tree: bool = False,
    use_recommendations: bool = False,
) -> ScenarioEngine:
    """
    Run a scenario demo.

    Args:
        scenario_file: Path to scenario JSON file
        auto_play: If True, auto-play through scenario
        use_decision_tree: If True, enable decision tree for recommendations
        use_recommendations: If True, use decision tree recommendations instead of first choice
    """
    engine = ScenarioEngine(scenario_file, use_decision_tree=use_decision_tree)

    if not engine.load():
        print("Failed to load scenario!")
        return engine

    # Display metadata
    print(f"\n{'=' * 60}")
    print(f"Game: {engine.scenario_data.get('gameTitle', 'Untitled')}")
    print(f"Author: {engine.scenario_data.get('gameAuthor', 'Unknown')}")
    if use_decision_tree:
        print("Decision Tree: ENABLED")
    print(f"{'=' * 60}\n")

    # Start scenario
    if not engine.start():
        return engine

    # Auto-play or interactive
    if auto_play:
        current_seq = engine.current_sequence_id
        while current_seq:
            # Get available choices from last event
            if engine.events and engine.events[-1].choices_available:
                # Try to get recommendation if enabled
                choice_letter = None
                if use_recommendations and engine.decision_tree and engine.decision_tree.is_trained:
                    recommendation = engine.recommend_choice(current_seq)
                    if recommendation:
                        choice_letter, confidence = recommendation
                        print(
                            f"\n[Decision Tree Recommendation: {choice_letter} (confidence: {confidence:.2f})]"
                        )

                # Fall back to first choice if no recommendation
                if not choice_letter:
                    first_choice = engine.events[-1].choices_available[0].split(":")[0].strip()
                    choice_letter = first_choice

                next_seq = engine.make_choice(current_seq, choice_letter)

                # Auto-train decision tree periodically
                if use_decision_tree:
                    engine.auto_train_decision_tree(min_events=3)

                if next_seq:
                    if not engine.run_sequence(next_seq):
                        break
                    current_seq = next_seq
                else:
                    break
            else:
                break
    else:
        # Interactive mode (not implemented in demo)
        print("Interactive mode not implemented in demo")

    # Final training if decision tree was used
    if use_decision_tree and engine.decision_tree and not engine.decision_tree.is_trained:
        engine.train_decision_tree()
        if engine.decision_tree.is_trained:
            print(f"\n[Decision Tree trained on {len(engine.training_states)} examples]")

    return engine


if __name__ == "__main__":
    # Demo
    scenario_file = Path(__file__).parent / "demo_scenario.json"
    engine = run_demo_scenario(scenario_file, auto_play=True)

    # Generate markdown
    markdown = engine.to_markdown()
    print("\n" + "=" * 60)
    print("MARKDOWN OUTPUT:")
    print("=" * 60)
    print(markdown)
