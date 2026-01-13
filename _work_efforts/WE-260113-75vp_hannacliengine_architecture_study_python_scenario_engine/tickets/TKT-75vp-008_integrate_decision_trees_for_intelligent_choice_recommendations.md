---
id: TKT-75vp-008
parent: WE-260113-75vp
title: "Integrate decision trees for intelligent choice recommendations"
status: completed
created: 2026-01-13T10:06:00.000Z
created_by: ctavolazzi
assigned_to: null
---

# TKT-75vp-008: Integrate decision trees for intelligent choice recommendations

## Metadata
- **Created**: Tuesday, January 13, 2026 at 2:06:00 AM PST
- **Completed**: Tuesday, January 13, 2026 at 2:06:00 AM PST
- **Parent Work Effort**: WE-260113-75vp
- **Author**: ctavolazzi

## Description
Integrate decision tree learning (ID3 algorithm) into the Python ScenarioEngine to enable intelligent choice recommendations based on player behavior patterns, container state, and scenario history.

## Acceptance Criteria
- [x] Ruby ID3 implementation studied and analyzed
- [x] Python decision tree class created (`ScenarioDecisionTree`)
- [x] Feature extraction from scenario state implemented
- [x] Decision tree integrated with ScenarioEngine
- [x] Training and prediction methods working
- [x] Test suite created for validation
- [x] Documentation created (ID3 analysis document)

## Files Changed

### New Files:
- `src/waft/core/scenario_decision_tree.py` - Decision tree implementation using scikit-learn
- `_work_efforts/WE-260113-75vp_hannacliengine_architecture_study_python_scenario_engine/DECISION_TREE_ID3_ANALYSIS.md` - Comprehensive ID3 algorithm analysis
- `_work_efforts/WE-260113-75vp_hannacliengine_architecture_study_python_scenario_engine/test_decision_tree.py` - Test suite for decision tree functionality
- `_work_efforts/WE-260113-75vp_hannacliengine_architecture_study_python_scenario_engine/decisiontree_repo/` - Cloned Ruby ID3 repository for reference

### Modified Files:
- `_work_efforts/WE-260113-75vp_hannacliengine_architecture_study_python_scenario_engine/demo_scenario_engine.py` - Added decision tree integration
- `_work_efforts/WE-260113-75vp_hannacliengine_architecture_study_python_scenario_engine/WE-260113-75vp_index.md` - Updated with new ticket

## Implementation Notes

### Phase 1: Study Ruby ID3 Implementation
- Cloned and analyzed `https://github.com/igrigorik/decisiontree`
- Documented key concepts: entropy, information gain, tree construction
- Analyzed discrete vs continuous attribute handling
- Created comprehensive analysis document

### Phase 2: Python Decision Tree Implementation
- Created `ScenarioDecisionTree` class using scikit-learn
- Uses `DecisionTreeClassifier` with entropy criterion (matching ID3)
- Supports both discrete and continuous features
- Implements training, prediction, and recommendation methods

### Phase 3: Feature Engineering
Features extracted from scenario state:
- **Container features**: Binary indicators for each possible container value
- **Sequence features**: Binary indicators for visited sequences
- **History features**: Counts of choice types (aggressive, cautious, exploratory)
- **Context features**: Current sequence type, available choices count

### Phase 4: Integration with ScenarioEngine
- Added optional `use_decision_tree` parameter to `ScenarioEngine.__init__`
- Implemented `_extract_state_features()` method
- Added `recommend_choice()` method for getting recommendations
- Added `train_decision_tree()` and `auto_train_decision_tree()` methods
- Updated `run_demo_scenario()` to support decision tree recommendations

### Phase 5: Testing & Validation
- Created comprehensive test suite (`test_decision_tree.py`)
- Tests cover: feature extraction, training, integration, accuracy
- Validates recommendation functionality

## Key Features

### Decision Tree Capabilities
1. **Training**: Learns from scenario execution history
2. **Prediction**: Predicts choice probabilities for given state
3. **Recommendation**: Recommends best choice with confidence scores
4. **Feature Importance**: Shows which features matter most
5. **Auto-training**: Automatically trains after collecting enough data

### Integration Points
- **ScenarioEngine**: Optional decision tree support
- **Training Data Collection**: Automatically collects state/choice pairs
- **Recommendation Display**: Shows recommendations during scenario execution

## Dependencies

**Required:**
- `scikit-learn` - For DecisionTreeClassifier
- `numpy` - For feature vector operations

**Installation:**
```bash
pip install scikit-learn numpy
```

## Usage Example

```python
from demo_scenario_engine import run_demo_scenario
from pathlib import Path

# Run scenario with decision tree enabled
scenario_file = Path("demo_scenario.json")
engine = run_demo_scenario(
    scenario_file,
    auto_play=True,
    use_decision_tree=True,
    use_recommendations=True  # Use recommendations instead of first choice
)

# Get recommendation for a sequence
recommendation = engine.recommend_choice("seq_001")
if recommendation:
    choice, confidence = recommendation
    print(f"Recommended: {choice} (confidence: {confidence:.2f})")
```

## Algorithm Details

### ID3 Algorithm
- Uses **entropy** (information gain) to select best attributes
- Supports **discrete** (categorical) and **continuous** (numerical) attributes
- Recursively builds tree by choosing attribute with highest information gain
- Returns default value when no matching branch found

### Feature Extraction
- Container values: Binary presence indicators
- Sequence history: Binary visited indicators
- Choice patterns: Counts of choice types
- Context: Sequence type and available choices count

## Future Enhancements

1. **Ensemble Methods**: Combine multiple trees (bagging, like Ruby library)
2. **Online Learning**: Update tree incrementally as new choices are made
3. **Rule Extraction**: Convert tree to human-readable rules for scenario authors
4. **Visualization**: Show decision tree structure in generated PDFs
5. **Multi-player Patterns**: Learn from multiple players' choice patterns

## Related Work

- **WE-260113-75vp** - Parent work effort (scenario engine)
- **WE-260113-wfbu** - AI DM system (could use decision trees for DM choices)
- **WE-260112-kgqt** - Being plays tavern game (scenario usage)

## Commits
- (work in progress, not yet committed)
