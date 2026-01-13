# Decision Tree ID3 Algorithm Analysis

**Source**: https://github.com/igrigorik/decisiontree  
**Date**: January 13, 2026  
**Purpose**: Analysis of Ruby ID3 implementation for integration into Python ScenarioEngine

---

## Overview

The ID3 (Iterative Dichotomiser 3) algorithm is a decision tree learning algorithm that uses information gain to recursively build a tree structure. This Ruby implementation supports both discrete (categorical) and continuous (numerical) attributes.

---

## Core Concepts

### 1. Entropy

**Definition**: Measures the impurity or uncertainty in a dataset.

**Formula**:
```
Entropy(S) = -Σ (p_i × log₂(p_i))
```
Where:
- `S` is the dataset
- `p_i` is the proportion of examples belonging to class `i`

**Ruby Implementation**:
```ruby
def entropy
  each_with_object(Hash.new(0)) do |i, result|
    result[i] += 1
  end.values.inject(0, :+) do |count|
    percentage = count.to_f / length
    -percentage * Math.log2(percentage)
  end
end
```

**Example**:
- Pure dataset (all same class): Entropy = 0
- Maximum uncertainty (50/50 split): Entropy = 1.0
- Higher entropy = more uncertainty = more information needed

### 2. Information Gain

**Definition**: The reduction in entropy achieved by splitting on an attribute.

**Formula**:
```
Gain(S, A) = Entropy(S) - Σ (|S_v| / |S|) × Entropy(S_v)
```
Where:
- `S` is the dataset
- `A` is the attribute
- `S_v` is the subset of `S` where attribute `A` has value `v`

**Intuition**: 
- Higher information gain = better attribute for splitting
- We want to maximize information gain at each step

### 3. ID3 Algorithm

**Pseudocode**:
```
ID3(data, attributes, default):
  1. If data is empty → return default
  2. If all examples have same classification → return that classification
  3. If no attributes left → return most common classification
  4. Choose attribute A with highest information gain
  5. For each value v of attribute A:
     - Create subset S_v where A = v
     - Recursively call ID3(S_v, attributes - A, default)
  6. Return tree with A as root, subtrees as children
```

---

## Implementation Details

### Discrete Attributes

**Handling**: Each unique value becomes a branch.

**Information Gain Calculation**:
```ruby
def id3_discrete(data, attributes, attribute)
  index = attributes.index(attribute)
  values = data.map { |row| row[index] }.uniq
  
  remainder = values.sort.inject(0, :+) do |val|
    classification = data.each_with_object([]) do |row, result|
      result << row.last if row[index] == val
    end
    ((classification.size.to_f / data.size) * classification.entropy)
  end
  
  [data.classification.entropy - remainder, index]
end
```

**Example**:
- Attribute: `color` with values `["red", "blue", "green"]`
- Creates 3 branches: one for each color value
- Each branch gets subset of data with that color

### Continuous Attributes

**Handling**: Finds optimal threshold to create binary split (>= threshold vs < threshold).

**Threshold Selection**:
```ruby
def id3_continuous(data, attributes, attribute)
  values = data.collect { |d| d[attributes.index(attribute)] }.uniq.sort
  thresholds = []
  values.each_index do |i|
    thresholds.push((values[i] + (values[i + 1].nil? ? values[i] : values[i + 1])).to_f / 2)
  end
  thresholds.pop
  
  # Test each threshold, find one with max information gain
  gain = thresholds.collect do |threshold|
    sp = data.partition { |d| d[attributes.index(attribute)] >= threshold }
    pos = (sp[0].size).to_f / data.size
    neg = (sp[1].size).to_f / data.size
    [data.classification.entropy - pos * sp[0].classification.entropy - neg * sp[1].classification.entropy, threshold]
  end
  gain.max { |a, b| a[0] <=> b[0] }
end
```

**Example**:
- Attribute: `temperature` with values `[36.6, 37, 38, 40, 50]`
- Calculates thresholds: `[36.8, 37.5, 39, 45]`
- Tests each: `temperature >= 37.5` vs `temperature < 37.5`
- Chooses threshold with highest information gain

### Tree Construction

**Recursive Process**:
1. **Base Cases**:
   - Empty data → return default value
   - All same class → return that class
   - No attributes → return most common class

2. **Recursive Case**:
   - Choose best attribute (highest information gain)
   - Partition data by attribute values
   - Recursively build subtrees for each partition
   - Return tree with attribute as root

**Ruby Structure**:
```ruby
tree = {
  Node(attribute, threshold, gain) => {
    value1 => subtree1,
    value2 => subtree2,
    ...
  }
}
```

### Prediction

**Process**:
1. Start at root node
2. Check attribute value in test example
3. Follow branch matching that value
4. If leaf node → return classification
5. If internal node → recurse into subtree

**Ruby Implementation**:
```ruby
def descend(tree, test)
  attr = tree.to_a.first
  return @default unless attr
  
  if type(attr.first.attribute) == :continuous
    if test[attribute_index] >= threshold
      return descend(attr[1]['>='], test)
    else
      return descend(attr[1]['<'], test)
    end
  else
    value = test[attribute_index]
    return descend(attr[1][value], test)
  end
end
```

---

## Key Features

### 1. Mixed Attribute Types

Supports both discrete and continuous in same dataset:
```ruby
dec_tree = DecisionTree::ID3Tree.new(
  labels, 
  training, 
  "not angry", 
  color: :discrete, 
  hunger: :continuous
)
```

### 2. Default Value Handling

Returns default value when:
- No matching branch found
- Empty dataset
- Tree traversal reaches undefined path

### 3. Inconsistent Dataset Handling

Preprocessing step removes duplicate attribute combinations, keeping most common classification:
```ruby
data2 = data.inject({}) do |hash, d|
  hash[d.slice(0..-2)] ||= Hash.new(0)
  hash[d.slice(0..-2)][d.last] += 1
  hash
end
```

### 4. Ruleset & Pruning

**Ruleset**: Converts tree to set of if-then rules
**Pruning**: Removes rules that don't improve accuracy on validation set (C4.5-style)

### 5. Bagging (Ensemble)

Trains 10 Ruleset classifiers and uses voting for prediction:
```ruby
class Bagging
  def train
    @classifiers = 10.times.map do |i|
      Ruleset.new(attributes, data, default, @type)
    end
    # Train each classifier
  end
  
  def predict(test)
    predictions = Hash.new(0)
    @classifiers.each do |c|
      p, accuracy = c.predict(test)
      predictions[p] += accuracy
    end
    # Return prediction with highest weighted vote
  end
end
```

---

## Application to Scenario Engine

### Feature Extraction

**Container Features** (Discrete):
- Binary indicators: `has_rusty_key`, `has_ornate_key`, `has_coin_purse`
- Values: `0` (absent) or `1` (present)

**Sequence Features** (Discrete):
- Binary indicators: `visited_seq_001`, `visited_seq_002`
- Values: `0` (not visited) or `1` (visited)

**History Features** (Continuous):
- Counts: `choice_count_aggressive`, `choice_count_cautious`
- Values: Integer counts

**Context Features** (Mixed):
- `current_sequence_type`: Discrete (ordinary, end)
- `available_choices_count`: Continuous (integer)

### Training Data Format

**Example**:
```python
training = [
    # [has_rusty_key, has_ornate_key, visited_seq_001, choice_count_aggressive, ...] → choice_letter
    [1, 0, 1, 2, ...],  # → 'A'
    [0, 1, 1, 1, ...],  # → 'B'
    [1, 1, 0, 0, ...],  # → 'C'
]
```

### Prediction

Given current scenario state:
1. Extract feature vector
2. Traverse decision tree
3. Return predicted choice letter
4. Optionally return confidence/probability

---

## Advantages for Scenario Engine

1. **Interpretability**: Tree structure is human-readable
2. **Handles Mixed Types**: Both discrete (containers) and continuous (counts)
3. **No Assumptions**: Non-parametric, no distribution assumptions
4. **Feature Importance**: Information gain shows which features matter most
5. **Rule Extraction**: Can convert to rules for scenario authors

---

## Limitations & Considerations

1. **Overfitting**: Deep trees can memorize training data
   - **Solution**: Pruning, max depth limits, minimum samples per leaf

2. **Greedy Algorithm**: Chooses locally optimal splits, not globally optimal
   - **Solution**: Usually good enough in practice

3. **Categorical Bias**: Favors attributes with many values
   - **Solution**: Use information gain ratio (C4.5) instead of information gain

4. **Missing Values**: Original ID3 doesn't handle missing data
   - **Solution**: Use most common value, or skip examples with missing data

5. **Continuous Attributes**: Only binary splits (>= vs <)
   - **Solution**: Can create multiple thresholds, but increases complexity

---

## Python Implementation Options

### Option 1: scikit-learn DecisionTreeClassifier

**Pros**:
- Battle-tested, optimized
- Handles missing values, pruning
- Supports various criteria (gini, entropy, log_loss)
- Easy to use

**Cons**:
- Less interpretable (black box)
- Harder to extract rules
- More dependencies

### Option 2: Custom ID3 Implementation

**Pros**:
- Full control over algorithm
- Easy to extract rules
- Can visualize tree structure
- Educational value

**Cons**:
- More code to maintain
- May have bugs
- Less optimized

### Option 3: Hybrid Approach

**Recommendation**: Start with scikit-learn for rapid prototyping, add custom ID3 if interpretability/rule extraction is needed.

---

## References

- **ID3 Algorithm**: Quinlan, J. R. (1986). "Induction of Decision Trees". Machine Learning.
- **C4.5 Algorithm**: Quinlan, J. R. (1993). "C4.5: Programs for Machine Learning".
- **Ruby Implementation**: https://github.com/igrigorik/decisiontree
- **Blog Post**: http://www.igvita.com/2007/04/16/decision-tree-learning-in-ruby/

---

## Next Steps

1. Implement Python decision tree (scikit-learn or custom)
2. Design feature extraction from scenario state
3. Integrate with ScenarioEngine
4. Test with demo scenario data
5. Evaluate recommendation accuracy
