# Attention Mechanisms Research: Simplified Applications to WAFT

**Date:** 2026-01-11
**Purpose:** Research modern attention mechanisms and identify SUPER SIMPLIFIED versions applicable to WAFT's document generation

---

## What We Currently Have (V2)

**Current Selection Algorithm:**
```python
# Get top N ideas sorted by importance
all_ideas = distilled_chat.get_top_ideas(n=50, min_importance=0.1)

# Truncate to fit pages
ideas_to_show = min(8, len(all_ideas))
page_1_ideas = all_ideas[:split_point]
page_2_ideas = all_ideas[split_point:ideas_to_show]
```

**Problems:**
- Simple truncation (no diversity)
- No consideration of idea relationships
- Single importance dimension
- No query-specific selection

---

## Modern Attention Mechanisms (2024-2025 Research)

### 1. **Sparse Attention with Block Selection**

**Research:** [Native Sparse Attention (NSA)](https://aclanthology.org/2025.acl-long.1126.pdf) - ICLR 2025

**What it does:**
- Divides content into blocks
- Uses 3 parallel attention branches:
  - **Compressed attention**: Coarse-grained patterns (overview)
  - **Selected attention**: Important token blocks (details)
  - **Sliding attention**: Local context (coherence)

**SIMPLIFIED for WAFT:**
```python
class MultiModalIdeaSelector:
    """
    Select ideas using 3 parallel strategies:
    1. Overview mode: High-importance ideas from all categories
    2. Detail mode: Deep dive into top category
    3. Context mode: Ideas that connect to each other
    """

    def select_ideas(self, ideas, target_count):
        # Overview: Top 40% most important
        overview = sorted(ideas, key=lambda x: x.importance)[:int(target_count * 0.4)]

        # Detail: Top category deep dive (30%)
        top_category = self._get_top_category(ideas)
        detail = [i for i in ideas if i.category == top_category][:int(target_count * 0.3)]

        # Context: Ideas that reference each other (30%)
        context = self._get_connected_ideas(ideas, overview + detail)[:int(target_count * 0.3)]

        return self._deduplicate_and_merge(overview, detail, context)
```

**Why this helps:**
- Ensures diversity (not just top N by importance)
- Maintains coherence (context branch)
- Provides both breadth and depth

---

### 2. **Multi-Head Attention for Multiple Objectives**

**Research:** [MoH: Multi-Head Attention as Mixture-of-Head](https://arxiv.org/html/2410.11842v1)

**What it does:**
- Different "heads" optimize for different objectives
- Each head has specialized query-key-value projections
- Outputs are weighted and combined

**SIMPLIFIED for WAFT:**
```python
class MultiObjectiveSelector:
    """
    Select ideas using multiple specialized selectors (heads).
    Each head optimizes for a different objective.
    """

    def __init__(self):
        self.heads = {
            "importance": ImportanceHead(),      # Raw importance scores
            "diversity": DiversityHead(),        # Category diversity
            "coherence": CoherenceHead(),        # Semantic connections
            "novelty": NoveltyHead(),            # Unique concepts
        }

        # Learned or configured weights
        self.head_weights = {
            "importance": 0.4,
            "diversity": 0.25,
            "coherence": 0.25,
            "novelty": 0.1,
        }

    def select_ideas(self, ideas, target_count):
        # Each head selects ideas
        selections = {}
        for name, head in self.heads.items():
            selections[name] = head.select(ideas, target_count)

        # Score each idea across all heads
        idea_scores = {}
        for idea in ideas:
            score = sum(
                self.head_weights[name] * head.score(idea, selections[name])
                for name, head in self.heads.items()
            )
            idea_scores[idea] = score

        # Return top scored ideas
        return sorted(ideas, key=lambda i: idea_scores[i], reverse=True)[:target_count]
```

**Why this helps:**
- Addresses arbitrary fitness weight problem
- Each head is simple and testable
- Can adjust weights per use case (first-time viewer vs. expert)

---

### 3. **Query-Key-Value Architecture**

**Research:** [Attention in Neural Networks](https://towardsdatascience.com/attention-in-neural-networks-e66920838742/)

**Core concept:**
```
Score(Query, Key) = similarity(Query, Key)
Attention(Q, K, V) = softmax(Score) · V
```

**What it does:**
- **Query**: What you're looking for ("What does a first-time viewer need?")
- **Key**: Properties of each idea (category, keywords, position)
- **Value**: The actual idea content
- **Score**: How well the Key matches the Query

**SIMPLIFIED for WAFT:**
```python
class QueryBasedSelector:
    """
    Select ideas based on query-key matching.
    """

    def __init__(self, query_profile):
        # Query profile defines what we're looking for
        self.query = query_profile  # e.g., "first_time_viewer"

    def select_ideas(self, ideas, target_count):
        scores = []

        for idea in ideas:
            # Build key from idea properties
            key = {
                "category": idea.category,
                "keywords": self._extract_keywords(idea.content),
                "position": idea.source_location,
                "importance": idea.importance,
            }

            # Compute similarity to query
            score = self._query_key_similarity(self.query, key)
            scores.append((idea, score))

        # Softmax normalization
        scores = self._softmax_normalize(scores)

        # Return top ideas
        return [idea for idea, score in sorted(scores, key=lambda x: x[1], reverse=True)[:target_count]]

    def _query_key_similarity(self, query, key):
        """Compute how well key matches query."""
        score = 0.0

        # Category match
        if key["category"] in query.get("preferred_categories", []):
            score += 0.4

        # Keyword overlap
        query_keywords = set(query.get("keywords", []))
        key_keywords = set(key["keywords"])
        overlap = len(query_keywords & key_keywords)
        score += 0.3 * (overlap / max(len(query_keywords), 1))

        # Importance
        score += 0.3 * key["importance"]

        return score
```

**Example query profiles:**
```python
QUERY_PROFILES = {
    "first_time_viewer": {
        "preferred_categories": ["concept", "insight", "question"],
        "keywords": ["what is", "how to", "introduction", "overview"],
        "avoid_keywords": ["advanced", "implementation details"],
    },
    "implementer": {
        "preferred_categories": ["action", "decision"],
        "keywords": ["install", "setup", "integrate", "use"],
        "avoid_keywords": ["theory", "motivation"],
    },
}
```

**Why this helps:**
- Content selection adapts to audience
- Same chat can generate different one-pagers for different readers
- More principled than raw importance scores

---

### 4. **Cross-Attention Between Pages**

**Research:** [Cross-Attention for Content Fusion](https://link.springer.com/article/10.1007/s41019-025-00335-5)

**What it does:**
- Page 1 and Page 2 "attend" to each other
- Prevents redundancy
- Ensures complementarity

**SIMPLIFIED for WAFT:**
```python
class CrossPageSelector:
    """
    Select ideas for Page 1 and Page 2 such that they complement each other.
    """

    def select_two_pages(self, ideas, page_1_count, page_2_count):
        # Select Page 1 first (most important)
        page_1 = sorted(ideas, key=lambda x: x.importance, reverse=True)[:page_1_count]

        # Select Page 2 with cross-attention to Page 1
        remaining = [i for i in ideas if i not in page_1]

        # Score each remaining idea based on:
        # 1. Importance (intrinsic value)
        # 2. Novelty relative to Page 1 (avoids redundancy)
        # 3. Coherence with Page 1 (maintains flow)

        page_2_scores = []
        for idea in remaining:
            importance = idea.importance
            novelty = self._novelty_score(idea, page_1)
            coherence = self._coherence_score(idea, page_1)

            score = 0.4 * importance + 0.4 * novelty + 0.2 * coherence
            page_2_scores.append((idea, score))

        page_2 = [idea for idea, score in sorted(page_2_scores, key=lambda x: x[1], reverse=True)[:page_2_count]]

        return page_1, page_2

    def _novelty_score(self, idea, reference_ideas):
        """How different is this idea from reference ideas?"""
        # Simple: Check category diversity
        reference_categories = {i.category for i in reference_ideas}
        if idea.category not in reference_categories:
            return 1.0  # New category = high novelty

        # Check keyword overlap
        reference_keywords = set()
        for ref in reference_ideas:
            reference_keywords.update(self._extract_keywords(ref.content))

        idea_keywords = set(self._extract_keywords(idea.content))
        overlap = len(idea_keywords & reference_keywords)

        return 1.0 - (overlap / max(len(idea_keywords), 1))

    def _coherence_score(self, idea, reference_ideas):
        """How well does this idea connect to reference ideas?"""
        # Check if this idea references concepts from Page 1
        connections = 0
        for ref in reference_ideas:
            if self._ideas_are_related(idea, ref):
                connections += 1

        return min(connections / len(reference_ideas), 1.0)
```

**Why this helps:**
- Page 2 doesn't just repeat Page 1
- Maintains narrative flow across pages
- Reader gets both overview (P1) and complementary details (P2)

---

### 5. **Adaptive Retrieval**

**Research:** [Adaptive Retrieval in RAG](https://arxiv.org/html/2507.18910v1)

**What it does:**
- System decides HOW MANY items to retrieve, not just which ones
- Adjusts based on content density and query complexity

**SIMPLIFIED for WAFT:**
```python
class AdaptiveCountSelector:
    """
    Dynamically determine how many ideas to show based on content density.
    """

    def determine_idea_count(self, ideas, target_pages=2):
        # Analyze content density
        avg_idea_length = sum(len(i.content) for i in ideas) / len(ideas)

        # Short ideas = can fit more
        # Long ideas = fit fewer

        if avg_idea_length < 50:
            base_count = 20  # Short, concise ideas
        elif avg_idea_length < 100:
            base_count = 15  # Medium ideas
        else:
            base_count = 10  # Long, detailed ideas

        # Adjust for category distribution
        categories = {i.category for i in ideas}
        if len(categories) > 4:
            # Diverse content = need more ideas to show diversity
            base_count += 3

        # Adjust for importance distribution
        high_importance = [i for i in ideas if i.importance > 0.8]
        if len(high_importance) > base_count:
            # Many high-importance ideas = prioritize quality over quantity
            base_count = len(high_importance)

        return base_count
```

**Why this helps:**
- V2 currently uses fixed initial estimate (8 ideas)
- This adapts to actual content characteristics
- Reduces iteration count for convergence

---

### 6. **Cognitive-Aligned Selection**

**Research:** [Cognitive-Aligned Document Selection](https://arxiv.org/html/2502.11770v1)

**What it does:**
- Selection criteria inspired by cognitive processes
- A selected item must semantically align with query components

**SIMPLIFIED for WAFT:**
```python
class CognitiveSelector:
    """
    Select ideas based on cognitive alignment with reader intent.
    """

    # Cognitive dimensions for a first-time viewer
    COGNITIVE_NEEDS = {
        "orientation": ["what is", "overview", "introduction"],
        "motivation": ["why", "benefit", "value", "problem"],
        "action": ["how to", "get started", "setup", "install"],
        "understanding": ["concept", "architecture", "design"],
        "confidence": ["example", "demo", "proof", "validation"],
    }

    def select_ideas(self, ideas, target_count):
        # Ensure coverage of all cognitive needs
        selected = []
        remaining = list(ideas)

        # Phase 1: Ensure at least one idea per cognitive dimension
        for dimension, keywords in self.COGNITIVE_NEEDS.items():
            best_match = None
            best_score = 0

            for idea in remaining:
                score = self._cognitive_match_score(idea, keywords)
                if score > best_score:
                    best_match = idea
                    best_score = score

            if best_match:
                selected.append(best_match)
                remaining.remove(best_match)

        # Phase 2: Fill remaining slots with highest importance
        remaining_slots = target_count - len(selected)
        if remaining_slots > 0:
            top_remaining = sorted(remaining, key=lambda x: x.importance, reverse=True)[:remaining_slots]
            selected.extend(top_remaining)

        return selected

    def _cognitive_match_score(self, idea, keywords):
        """How well does this idea match cognitive keywords?"""
        idea_lower = idea.content.lower()
        matches = sum(1 for kw in keywords if kw in idea_lower)
        return matches / len(keywords)
```

**Why this helps:**
- Ensures one-pager addresses reader's cognitive needs
- Prevents over-representation of one dimension (e.g., all concepts, no actions)
- Based on actual cognitive science research

---

## SUPER SIMPLIFIED Integration Plan

### Phase 1: Multi-Head Selection (Immediate)

Replace simple truncation with 3 specialized heads:

```python
# In TwoPageGeneratorV2
def _select_ideas_with_attention(self, ideas, target_count):
    # Head 1: Importance (40%)
    importance_picks = sorted(ideas, key=lambda x: x.importance, reverse=True)[:int(target_count * 0.4)]

    # Head 2: Diversity (30%)
    diversity_picks = self._select_diverse_categories(ideas, int(target_count * 0.3))

    # Head 3: Coherence (30%)
    coherence_picks = self._select_coherent_ideas(ideas, importance_picks, int(target_count * 0.3))

    # Merge and deduplicate
    return self._deduplicate([*importance_picks, *diversity_picks, *coherence_picks])[:target_count]
```

**Implementation effort:** 2-3 hours
**Impact:** High - addresses content selection quality issues

---

### Phase 2: Cross-Page Attention (Near-term)

Ensure Page 1 and Page 2 complement each other:

```python
# In TwoPageGeneratorV2
def _split_pages_with_cross_attention(self, ideas, split_point):
    page_1 = ideas[:split_point]

    # Score remaining ideas for novelty + coherence
    page_2_candidates = ideas[split_point:]
    page_2_scores = [
        (idea, self._cross_attention_score(idea, page_1))
        for idea in page_2_candidates
    ]

    page_2 = [idea for idea, _ in sorted(page_2_scores, key=lambda x: x[1], reverse=True)]

    return page_1, page_2
```

**Implementation effort:** 3-4 hours
**Impact:** Medium-High - prevents redundancy between pages

---

### Phase 3: Query-Based Selection (Future)

Support different query profiles for different audiences:

```python
# Usage
generator = TwoPageGeneratorV2(query_profile="first_time_viewer")
result = generator.generate(distilled_chat, styling_genome, "output.pdf")

# vs.

generator = TwoPageGeneratorV2(query_profile="implementer")
result = generator.generate(distilled_chat, styling_genome, "output.pdf")
```

**Implementation effort:** 4-6 hours
**Impact:** High - enables audience-specific one-pagers

---

## Key Simplification Principles

1. **No Neural Networks**: We're using the *concepts* from attention mechanisms, not actual neural network implementations
2. **Deterministic**: All scores should be explainable and reproducible
3. **Lightweight**: No GPU required, runs on CPU in milliseconds
4. **Testable**: Each component can be unit tested independently
5. **Genomic**: Every selection strategy has a genome ID for evolution tracking

---

## Expected Improvements

### Current (V2):
```
Ideas selected: First 19 by importance
Categories: [concept: 8, action: 6, insight: 3, question: 2, decision: 0]
Page 1 vs Page 2: Simple 60/40 split, possible redundancy
```

### With Multi-Head Attention (Phase 1):
```
Ideas selected: Balanced by importance, diversity, coherence
Categories: [concept: 5, action: 4, insight: 4, question: 3, decision: 3]
Page 1 vs Page 2: Still 60/40 split, but better diversity within each page
```

### With Cross-Page Attention (Phase 2):
```
Ideas selected: Balanced across dimensions
Categories: [concept: 5, action: 4, insight: 4, question: 3, decision: 3]
Page 1: Overview + orientation (concepts, questions)
Page 2: Action + understanding (actions, insights, decisions)
Redundancy: < 10% keyword overlap between pages
```

### With Query Profiles (Phase 3):
```
First-time viewer profile:
  Page 1: [concept: 4, question: 3, insight: 2]
  Page 2: [action: 3, example: 2, motivation: 2]

Implementer profile:
  Page 1: [action: 5, decision: 3, setup: 1]
  Page 2: [integration: 3, configuration: 2, troubleshooting: 2]
```

---

## Sources

### Research Papers:
- [Efficient Attention Mechanisms for Large Language Models (2025)](https://arxiv.org/pdf/2507.19595)
- [Hardware-Aligned Sparse Attention (ICLR 2025)](https://aclanthology.org/2025.acl-long.1126.pdf)
- [Cognitive-Aligned Document Selection for RAG](https://arxiv.org/html/2502.11770v1)
- [RAG Advances 2024-2025](https://arxiv.org/html/2507.18910v1)
- [Multi-Head Attention as Mixture-of-Head](https://arxiv.org/html/2410.11842v1)
- [Interpreting Multi-Head Attention in Summarization](https://maartjeth.github.io/assets/documents/interpretability_mha_abstractive_summarization.pdf)
- [Human Guided Attention Patterns in Extractive Summarization](https://arxiv.org/abs/2112.05364)

### Educational Resources:
- [Attention in Neural Networks (Towards Data Science)](https://towardsdatascience.com/attention-in-neural-networks-e66920838742/)
- [Transformer Attention: Q, K, V Matrices Guide](https://www.billparker.ai/2024/10/transformer-attention-simple-guide-to-q.html)
- [Multi-Head Attention Tutorial](https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial6/Transformers_and_MHAttention.html)

---

## Next Steps

1. **Immediate**: Implement Phase 1 (Multi-Head Selection)
2. **Test**: Generate 10 diverse one-pagers and compare V2 vs V3
3. **Iterate**: Refine head weights based on actual results
4. **Evolve**: Track V2 → V3 as evolutionary mutation with fitness improvement

The attention mechanisms are sound. Let's engineer simplified versions into V3.
