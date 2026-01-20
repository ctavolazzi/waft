# Quick Start Guide - Using the WAFT Architecture

## Installation

```bash
cd /home/user/waft
pip install -e .
```

## Basic Usage

### 1. Simple Guide (Foundation)

```python
from waft.foundation import Guide

# Create a basic guide
guide = Guide(max_iterations=10, quality_threshold=0.8)

# Solve a problem
session = guide.solve("What is the capital of France?")

# Check results
print(f"Quality: {session.final_evaluation.overall.value}")
print(f"Iterations: {len(session.steps)}")
```

### 2. Using Strategies (Patterns)

```python
from waft.patterns import StrategyGuide, StrictStrategy, LenientStrategy

# Create guides with different strategies
strict = StrategyGuide(StrictStrategy(), max_iterations=5)
lenient = StrategyGuide(LenientStrategy(), max_iterations=5)

# Solve the same problem with both
problem = "Explain quantum physics"
strict_session = strict.solve(problem)
lenient_session = lenient.solve(problem)

print(f"Strict quality: {strict_session.final_evaluation.overall.value}")
print(f"Lenient quality: {lenient_session.final_evaluation.overall.value}")
```

### 3. Using Decorators (Patterns)

```python
from waft.foundation import Guide
from waft.patterns import CachingDecorator, TimingDecorator, ValidationDecorator

# Stack decorators
base = Guide(max_iterations=5)
validated = ValidationDecorator(base)
cached = CachingDecorator(validated)
timed = TimingDecorator(cached)

# Use the decorated guide
session = timed.solve("What is 2 + 2?")  # First call - miss
session = timed.solve("What is 2 + 2?")  # Second call - cache hit
```

### 4. Using Factory (Patterns)

```python
from waft.patterns import GuideFactory, GuideType

# Create different guide types easily
strict_guide = GuideFactory.create(GuideType.STRICT, max_iterations=5)
lenient_guide = GuideFactory.create(GuideType.LENIENT, max_iterations=5)
observable_guide = GuideFactory.create(GuideType.OBSERVABLE, max_iterations=5)
cached_guide = GuideFactory.create(GuideType.CACHED, max_iterations=5)

# Use them
session = strict_guide.solve("What is the meaning of life?")
```

### 5. Using Observer (Patterns)

```python
from waft.patterns import ObservableGuide, QualityLogger, ThresholdAlerter

# Create observable guide with monitoring
guide = ObservableGuide(max_iterations=10)
guide.attach(QualityLogger())
guide.attach(ThresholdAlerter(threshold=0.9))

# Run - observers will be notified at each step
session = guide.solve("Complex problem that requires iterations")
```

### 6. Using Composite (Voting)

```python
from waft.patterns import GuideFactory, GuideType
from waft.composite import LeafGuide, VotingGuide

# Create multiple guides
strict = LeafGuide(GuideFactory.create(GuideType.STRICT, max_iterations=5))
lenient = LeafGuide(GuideFactory.create(GuideType.LENIENT, max_iterations=5))
basic = LeafGuide(GuideFactory.create(GuideType.BASIC, max_iterations=5))

# Create voting panel
voting = VotingGuide("My Voting Panel")
voting.add(strict)
voting.add(lenient)
voting.add(basic)

# Solve - all guides vote, best result wins
session = voting.solve("What is the best programming language?")
print(f"Consensus quality: {session.final_evaluation.overall.value}")
```

### 7. Using Adaptive Guide (Advanced)

```python
from waft.advanced import AdaptiveGuide

# Create adaptive guide that learns
guide = AdaptiveGuide(max_iterations=5)

# Solve multiple problems - it learns which strategies work best
for i in range(10):
    session = guide.solve(f"Problem {i}")
    print(f"Problem {i}: quality={session.final_evaluation.overall.value:.3f}")

# Check what it learned
stats = guide.get_stats()
for name, stat in stats.items():
    if stat.total_uses > 0:
        print(f"{name}: uses={stat.total_uses}, "
              f"success_rate={stat.success_rate:.2f}, "
              f"avg_quality={stat.avg_quality:.3f}")
```

### 8. Using Quality Analyzer (Advanced)

```python
from waft.foundation import Guide
from waft.advanced import QualityAnalyzer

# Solve a problem
guide = Guide(max_iterations=10)
session = guide.solve("Explain machine learning")

# Analyze the quality in depth
metrics = QualityAnalyzer.analyze(session)

print(f"Overall Score: {metrics.overall_score:.3f}")
print(f"Grade: {metrics.grade}")
print(f"Improvement Rate: {metrics.improvement_rate:.3f}")
print(f"Convergence Speed: {metrics.convergence_speed:.3f}")
print(f"Consistency: {metrics.consistency:.3f}")
print(f"Efficiency: {metrics.efficiency:.3f}")
```

### 9. Using Smart Guide (Advanced)

```python
from waft.advanced import SmartGuide

# Create guide that picks strategy based on problem type
guide = SmartGuide(max_iterations=5)

# It automatically classifies problems and picks best strategy
math_session = guide.solve("Calculate 15 + 27")  # Uses strict strategy
creative_session = guide.solve("Write a story about a robot")  # Uses lenient
factual_session = guide.solve("Is Python a programming language?")  # Uses strict

print(f"Math quality: {math_session.final_evaluation.overall.value:.3f}")
print(f"Creative quality: {creative_session.final_evaluation.overall.value:.3f}")
print(f"Factual quality: {factual_session.final_evaluation.overall.value:.3f}")
```

### 10. Using Session Recorder (Advanced)

```python
from waft.foundation import Guide
from waft.advanced import SessionRecorder

# Create recorder
recorder = SessionRecorder()
guide = Guide(max_iterations=5)

# Record multiple sessions
for i in range(10):
    session = guide.solve(f"Problem {i}")
    recorder.record(session)

# Analyze all recordings
analysis = recorder.analyze_all()
print(f"Total sessions: {analysis['total']}")
print(f"Average quality: {analysis['avg_quality']:.3f}")
print(f"Average efficiency: {analysis['avg_efficiency']:.3f}")
print(f"Grade distribution: {analysis['grade_distribution']}")

# Replay a specific session
session = recorder.replay(5)
print(f"Replayed session quality: {session.final_evaluation.overall.value:.3f}")
```

### 11. Using Ensemble Guide (Advanced)

```python
from waft.advanced import EnsembleGuide

# Create ensemble that runs all strategies
ensemble = EnsembleGuide(max_iterations=5)

# It runs strict, lenient, and length strategies, picks best
session = ensemble.solve("What is the best approach to software architecture?")
print(f"Ensemble quality: {session.final_evaluation.overall.value:.3f}")
```

## Complete Integration Example

Here's how to use multiple layers together:

```python
from waft.foundation import Guide
from waft.patterns import (
    GuideFactory, GuideType,
    CachingDecorator, TimingDecorator,
    ObservableGuide, QualityLogger, ThresholdAlerter
)
from waft.composite import LeafGuide, VotingGuide
from waft.advanced import (
    AdaptiveGuide, QualityAnalyzer,
    SessionRecorder, EnsembleGuide
)

# Create a sophisticated system
recorder = SessionRecorder()

# Create decorated guides
strict = TimingDecorator(CachingDecorator(
    GuideFactory.create(GuideType.STRICT, max_iterations=5)
))
lenient = TimingDecorator(CachingDecorator(
    GuideFactory.create(GuideType.LENIENT, max_iterations=5)
))

# Create voting panel
voting = VotingGuide("Expert Panel")
voting.add(LeafGuide(strict))
voting.add(LeafGuide(lenient))

# Create adaptive guide
adaptive = AdaptiveGuide(max_iterations=5)

# Create ensemble
ensemble = EnsembleGuide(max_iterations=5)

# Test different approaches
problems = [
    "Calculate the area of a circle with radius 5",
    "Write a creative story about time travel",
    "Explain how blockchain works",
    "What is the capital of Japan?"
]

for problem in problems:
    print(f"\nProblem: {problem}")

    # Try voting approach
    voting_session = voting.solve(problem)
    recorder.record(voting_session)
    print(f"  Voting: {voting_session.final_evaluation.overall.value:.3f}")

    # Try adaptive approach
    adaptive_session = adaptive.solve(problem)
    recorder.record(adaptive_session)
    print(f"  Adaptive: {adaptive_session.final_evaluation.overall.value:.3f}")

    # Try ensemble approach
    ensemble_session = ensemble.solve(problem)
    recorder.record(ensemble_session)
    print(f"  Ensemble: {ensemble_session.final_evaluation.overall.value:.3f}")

    # Analyze best result
    best = max([voting_session, adaptive_session, ensemble_session],
               key=lambda s: s.final_evaluation.overall.value)
    metrics = QualityAnalyzer.analyze(best)
    print(f"  Best: {metrics.overall_score:.3f} (Grade: {metrics.grade})")

# Final analysis
print("\n" + "="*80)
print("FINAL ANALYSIS")
print("="*80)

analysis = recorder.analyze_all()
print(f"Total sessions: {analysis['total']}")
print(f"Average quality: {analysis['avg_quality']:.3f}")
print(f"Average efficiency: {analysis['avg_efficiency']:.3f}")
print(f"Grade distribution: {analysis['grade_distribution']}")

# Check adaptive learning
print("\nAdaptive learning statistics:")
for name, stat in adaptive.get_stats().items():
    if stat.total_uses > 0:
        print(f"  {name}: uses={stat.total_uses}, "
              f"success={stat.success_rate:.2f}, "
              f"quality={stat.avg_quality:.3f}")
```

## Testing Your Code

Run the comprehensive tests:

```bash
# Test foundation and patterns
python tests/test_comprehensive.py

# Test full system integration
python tests/test_full_system.py

# Test production code fixes
python tests/verify_fix.py
python tests/test_premise_validation.py
```

## Architecture Overview

```
Layer 0: Score (atomic data type)
    ↓
Layer 1: evaluate_text() (pure function)
    ↓
Layer 2: Evaluation (multi-dimensional)
    ↓
Layer 3: Step (iteration cycle)
    ↓
Layer 4: Session (complete loop)
    ↓
Layer 5: Guide (OOP wrapper)
    ↓
Layer 6: Patterns (7 design patterns)
    ↓
Layer 7: Composite (hierarchical guides)
    ↓
Layer 8: Advanced (learning, analysis, ensembles)
```

Each layer builds on the one below without modifying it.

## Key Principles

1. **Immutability** - Core data structures are frozen
2. **Pure Functions** - No side effects in core transformations
3. **Composition** - Build new capabilities without changing existing code
4. **Single Responsibility** - Each component does one thing well
5. **Open/Closed** - Open for extension, closed for modification

## Performance Tips

1. **Use caching** for repeated queries:
   ```python
   cached = CachingDecorator(guide)
   ```

2. **Limit iterations** for faster results:
   ```python
   guide = Guide(max_iterations=3)  # Instead of 10
   ```

3. **Use appropriate strategies**:
   - Strict for math/factual
   - Lenient for creative
   - Smart for automatic selection

4. **Monitor with observers** to track performance:
   ```python
   observable = ObservableGuide()
   observable.attach(QualityLogger())
   ```

5. **Use ensemble sparingly** - runs multiple strategies (slower but better quality)

## Next Steps

1. Read `ARCHITECTURE.md` for deep understanding
2. Run the test suite to see everything in action
3. Try the examples above
4. Build your own patterns on top of the foundation
5. Contribute improvements!

## Support

For questions or issues, check:
- `ARCHITECTURE.md` - Full architecture documentation
- `tests/` - Comprehensive test suite with examples
- Source code in `src/waft/` - Well-commented implementation
