"""
Scenario Decision Tree - Intelligent choice recommendations for scenario engine.

Uses decision tree learning to predict player choices based on:
- Container state (inventory, clues, karma, etc.)
- Sequence history (which sequences have been visited)
- Choice patterns (previous choice types)
- Context features (current sequence type, available choices count)
"""

from dataclasses import dataclass

import numpy as np

try:
    from sklearn.preprocessing import LabelEncoder
    from sklearn.tree import DecisionTreeClassifier

    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    DecisionTreeClassifier = None
    LabelEncoder = None


@dataclass
class ScenarioState:
    """Represents the state of a scenario at a decision point."""

    sequence_id: str
    sequence_type: str
    containers: dict[str, list[str]]
    visited_sequences: list[str]
    choice_history: list[str]
    available_choices: list[str]
    choice_made: str | None = None


class ScenarioDecisionTree:
    """
    Decision tree for predicting player choices in scenario engine.

    Uses scikit-learn DecisionTreeClassifier with entropy criterion
    (matching ID3 algorithm) to learn from player choice patterns.
    """

    def __init__(self, max_depth: int | None = 10, min_samples_split: int = 2):
        """
        Initialize decision tree.

        Args:
            max_depth: Maximum depth of tree (None = unlimited)
            min_samples_split: Minimum samples required to split a node
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError(
                "scikit-learn is required for ScenarioDecisionTree. "
                "Install with: pip install scikit-learn"
            )

        self.tree = DecisionTreeClassifier(
            criterion="entropy",  # ID3 uses entropy (information gain)
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            random_state=42,
        )
        self.label_encoder = LabelEncoder()
        self.feature_names: list[str] = []
        self.is_trained: bool = False
        self.all_container_values: set = set()
        self.all_sequence_ids: set = set()

    def _extract_features(self, state: ScenarioState) -> np.ndarray:
        """
        Extract feature vector from scenario state.

        Features:
        - Container features: Binary indicators for each possible container value
        - Sequence features: Binary indicators for visited sequences
        - History features: Count of choice types made
        - Context features: Current sequence type (encoded), available choices count

        Returns:
            Feature vector as numpy array
        """
        features = []

        # Container features: Binary indicators for each possible container value
        for container_value in sorted(self.all_container_values):
            # Check if value exists in any container
            found = False
            for _container_name, values in state.containers.items():
                if container_value in values:
                    found = True
                    break
            features.append(1 if found else 0)

        # Sequence features: Binary indicators for visited sequences
        for seq_id in sorted(self.all_sequence_ids):
            features.append(1 if seq_id in state.visited_sequences else 0)

        # History features: Count of choice types
        # Count aggressive choices (A, B typically)
        aggressive_count = sum(1 for c in state.choice_history if c in ["A", "B"])
        features.append(aggressive_count)

        # Count cautious choices (C, D typically)
        cautious_count = sum(1 for c in state.choice_history if c in ["C", "D"])
        features.append(cautious_count)

        # Count exploratory choices (E, F typically)
        exploratory_count = sum(1 for c in state.choice_history if c in ["E", "F"])
        features.append(exploratory_count)

        # Context features
        # Sequence type: encoded as integer (ordinary=0, end=1, etc.)
        seq_type_map = {"ordinary": 0, "end": 1}
        features.append(seq_type_map.get(state.sequence_type, 0))

        # Available choices count
        features.append(len(state.available_choices))

        return np.array(features)

    def _build_feature_names(self, states: list[ScenarioState]) -> list[str]:
        """Build list of feature names for interpretability."""
        names = []

        # Container features
        for container_value in sorted(self.all_container_values):
            names.append(f"has_{container_value}")

        # Sequence features
        for seq_id in sorted(self.all_sequence_ids):
            names.append(f"visited_{seq_id}")

        # History features
        names.extend(
            ["choice_count_aggressive", "choice_count_cautious", "choice_count_exploratory"]
        )

        # Context features
        names.extend(["sequence_type", "available_choices_count"])

        return names

    def train(self, states: list[ScenarioState], choices: list[str]) -> None:
        """
        Train decision tree on scenario states and choices.

        Args:
            states: List of scenario states at decision points
            choices: List of choices made (corresponding to states)

        Raises:
            ValueError: If states and choices have different lengths
        """
        if len(states) != len(choices):
            raise ValueError(
                f"States ({len(states)}) and choices ({len(choices)}) must have same length"
            )

        if len(states) == 0:
            raise ValueError("Cannot train on empty dataset")

        # Collect all possible container values and sequence IDs
        self.all_container_values = set()
        self.all_sequence_ids = set()

        for state in states:
            for _container_name, values in state.containers.items():
                self.all_container_values.update(values)
            self.all_sequence_ids.add(state.sequence_id)
            self.all_sequence_ids.update(state.visited_sequences)

        # Extract features
        X = np.array([self._extract_features(state) for state in states])

        # Encode choice labels
        y = self.label_encoder.fit_transform(choices)

        # Build feature names
        self.feature_names = self._build_feature_names(states)

        # Train tree
        self.tree.fit(X, y)
        self.is_trained = True

    def predict(self, state: ScenarioState) -> dict[str, float]:
        """
        Predict choice probabilities for given state.

        Args:
            state: Current scenario state

        Returns:
            Dictionary mapping choice letters to probabilities

        Raises:
            ValueError: If tree is not trained
        """
        if not self.is_trained:
            raise ValueError("Decision tree must be trained before prediction")

        # Extract features
        features = self._extract_features(state).reshape(1, -1)

        # Get probabilities for each class
        probabilities = self.tree.predict_proba(features)[0]

        # Map back to choice letters
        choice_probs = {}
        for i, choice_letter in enumerate(self.label_encoder.classes_):
            choice_probs[choice_letter] = float(probabilities[i])

        return choice_probs

    def recommend_choice(
        self, state: ScenarioState, available_choices: list[str] | None = None
    ) -> tuple[str, float] | None:
        """
        Recommend best choice for given state.

        Args:
            state: Current scenario state
            available_choices: Optional list of available choices to filter by

        Returns:
            Tuple of (choice_letter, confidence) or None if no recommendation

        Raises:
            ValueError: If tree is not trained
        """
        if not self.is_trained:
            return None

        # Get all predictions
        predictions = self.predict(state)

        # Filter by available choices if provided
        if available_choices:
            predictions = {k: v for k, v in predictions.items() if k in available_choices}

        if not predictions:
            return None

        # Return choice with highest probability
        best_choice = max(predictions.items(), key=lambda x: x[1])
        return best_choice

    def get_feature_importance(self) -> dict[str, float]:
        """
        Get feature importance scores.

        Returns:
            Dictionary mapping feature names to importance scores

        Raises:
            ValueError: If tree is not trained
        """
        if not self.is_trained:
            raise ValueError("Decision tree must be trained before getting feature importance")

        importances = self.tree.feature_importances_
        return dict(zip(self.feature_names, importances, strict=False))

    def get_tree_depth(self) -> int:
        """Get the depth of the trained tree."""
        if not self.is_trained:
            return 0
        return int(self.tree.tree_.max_depth)
