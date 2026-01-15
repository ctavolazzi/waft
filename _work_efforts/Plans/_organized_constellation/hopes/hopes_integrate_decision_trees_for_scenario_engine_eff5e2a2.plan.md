---
name: Integrate Decision Trees for Scenario Engine
overview: Study the Ruby ID3 decision tree implementation and integrate decision tree capabilities into the Python ScenarioEngine to enable intelligent choice recommendations based on player behavior patterns, container state, and scenario history.
todos:
  - id: study-id3
    content: Clone and study Ruby ID3 decision tree implementation from GitHub, document algorithm details
    status: completed
  - id: implement-tree
    content: Create ScenarioDecisionTree class in src/waft/core/scenario_decision_tree.py with training and prediction methods
    status: completed
  - id: feature-engineering
    content: Implement feature extraction from scenario state (containers, sequences, history)
    status: completed
  - id: integrate-engine
    content: Modify ScenarioEngine to use decision tree for choice recommendations
    status: completed
  - id: test-validation
    content: Create tests and validation scenarios to verify decision tree recommendations
    status: completed
  - id: documentation
    content: Create analysis document and update work effort with new ticket
    status: completed

category: hopes
confidence: 1.00
constellation_date: 2026-01-14
---

# Integrate Decision Trees for Scenario Engine

## Context

The current `ScenarioEngine` (in `_work_efforts/WE-260113-75vp_hannacliengine_architecture_study_python_scenario_engine/demo_scenario_engine.py`) uses simple rule-based conditionals:

- **Set choices**: Always available
- **Conditional choices**: Based on container value presence

Decision trees can enhance this by:

- Learning from player choice patterns
- Predicting player preferences based on scenario state
- Adapting choice recommendations dynamically
- Making more sophisticated decisions beyond simple container checks

## Implementation Plan

### Phase 1: Study Ruby ID3 Implementation

**Files to examine:**

- Clone and study `https://github.com/igrigorik/decisiontree`
- Focus on `lib/decisiontree.rb` - ID3 algorithm implementation
- Understand continuous vs discrete attribute handling
- Review information gain calculation

**Deliverable:**

- Analysis document: `DECISION_TREE_ID3_ANALYSIS.md`
- Key concepts: information gain, entropy, tree construction, prediction

### Phase 2: Python Decision Tree Implementation

**Options:**

1. **Port Ruby ID3** - Direct port of the Ruby implementation
2. **Use scikit-learn** - Already mentioned in codebase (`TKT-sec1-004`)
3. **Hybrid** - Custom ID3 for interpretability, scikit-learn for advanced features

**Recommendation:** Start with scikit-learn `DecisionTreeClassifier` for rapid prototyping, then add custom ID3 if interpretability/rule extraction is needed.

**Implementation:**

- Create `src/waft/core/scenario_decision_tree.py`
- Class: `ScenarioDecisionTree`
- Methods:
  - `train(history: List[ScenarioEvent])` - Train on player choice history
  - `predict(sequence_state: Dict) -> Dict[str, float]` - Predict choice probabilities
  - `recommend_choice(sequence_id: str, available_choices: List[str]) -> str` - Recommend best choice

**Features:**

- Extract features from scenario state:
  - Container values (binary: present/absent)
  - Sequence history (which sequences visited)
  - Choice patterns (previous choice types)
  - Container counts (how many items in each container)
- Target: Which choice letter was selected
- Handle both discrete (container presence) and continuous (container counts) attributes

### Phase 3: Integrate with ScenarioEngine

**Modifications to `demo_scenario_engine.py`:**

1. **Add decision tree to ScenarioEngine:**
```python
from waft.core.scenario_decision_tree import ScenarioDecisionTree

class ScenarioEngine:
    def __init__(self, scenario_file: Path, use_decision_tree: bool = False):
        # ... existing init ...
        self.decision_tree: Optional[ScenarioDecisionTree] = None
        if use_decision_tree:
            self.decision_tree = ScenarioDecisionTree()
```

2. **Collect training data:**

- Store choice history with full state context
- Track: sequence_id, available_choices, container_state, choice_made

3. **Recommend choices:**
```python
def recommend_choice(self, sequence_id: str) -> Optional[str]:
    """Use decision tree to recommend best choice."""
    if not self.decision_tree or not self.decision_tree.is_trained:
        return None

    state = self._extract_state_features(sequence_id)
    probabilities = self.decision_tree.predict(state)

    # Return choice with highest probability
    return max(probabilities.items(), key=lambda x: x[1])[0]
```

4. **Optional: Auto-train mode:**

- Train on accumulated history after N events
- Update recommendations as player behavior patterns emerge

### Phase 4: Feature Engineering

**State Features:**

- **Container features**: Binary indicators for each possible container value
- **Sequence features**: Binary indicators for visited sequences
- **History features**: Count of choice types made (aggressive, cautious, exploratory)
- **Context features**: Current sequence type, number of available choices

**Example feature vector:**

```python
{
    "has_rusty_key": 1,
    "has_ornate_key": 0,
    "has_coin_purse": 1,
    "visited_seq_001": 1,
    "visited_seq_002": 0,
    "choice_count_aggressive": 2,
    "choice_count_cautious": 1,
    "current_sequence_type": "ordinary",
    "available_choices_count": 3
}
```

### Phase 5: Testing & Validation

**Test scenarios:**

1. **Simple scenario**: Train on demo_scenario.json, verify recommendations
2. **Player behavior patterns**: Simulate different player types (aggressive, cautious, exploratory)
3. **Adaptive learning**: Show how recommendations improve with more data

**Validation:**

- Compare decision tree recommendations vs random choice
- Measure recommendation accuracy on held-out test data
- Visualize decision tree structure (if using custom ID3)

## Files to Create/Modify

### New Files:

- `src/waft/core/scenario_decision_tree.py` - Decision tree implementation
- `_work_efforts/WE-260113-75vp_hannacliengine_architecture_study_python_scenario_engine/DECISION_TREE_ID3_ANALYSIS.md` - ID3 algorithm analysis
- `_work_efforts/WE-260113-75vp_hannacliengine_architecture_study_python_scenario_engine/tickets/TKT-75vp-008_integrate_decision_trees_for_intelligent_choice_recommendations.md` - New ticket

### Modified Files:

- `_work_efforts/WE-260113-75vp_hannacliengine_architecture_study_python_scenario_engine/demo_scenario_engine.py` - Add decision tree integration
- `_work_efforts/WE-260113-75vp_hannacliengine_architecture_study_python_scenario_engine/WE-260113-75vp_index.md` - Update with new ticket

## Dependencies

**Required:**

- `scikit-learn` - For DecisionTreeClassifier (or custom ID3 implementation)
- `numpy` - For feature vector operations

**Optional:**

- `graphviz` - For visualizing decision trees (if using custom ID3)

## Integration Points

**Link to existing systems:**

- **DecisionMatrixCalculator** (`src/waft/core/decision_matrix.py`) - Could use decision trees for criterion weighting
- **BeingDecisionSystem** (`src/waft/core/being_decisions.py`) - Could use decision trees for being choice patterns
- **Campaign Orchestrator** (`WE-260113-wfbu`) - Decision trees for DM choice recommendations

## Success Criteria

1. ✅ Decision tree can be trained on scenario execution history
2. ✅ Decision tree provides choice recommendations with confidence scores
3. ✅ Recommendations improve as more training data is collected
4. ✅ Integration doesn't break existing ScenarioEngine functionality
5. ✅ Decision tree can handle both discrete and continuous features

## Future Enhancements

- **Ensemble methods**: Combine multiple decision trees (bagging, like Ruby library)
- **Online learning**: Update tree incrementally as new choices are made
- **Rule extraction**: Convert tree to human-readable rules for scenario authors
- **Visualization**: Show decision tree structure in generated PDFs
- **Multi-player patterns**: Learn from multiple players' choice patterns

## Related Work Efforts

- **WE-260113-75vp** - Current scenario engine work (parent)
- **WE-260113-wfbu** - AI DM system with decision matrix integration
- **WE-260112-kgqt** - Being plays tavern game (scenario usage)