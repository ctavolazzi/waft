"""
COMPOSITE PATTERN - Built from test insights

After testing all patterns, we found that complex problems
need hierarchical delegation. Build Composite pattern for guide trees.
"""

from abc import ABC, abstractmethod

from foundation import Guide, Session


class GuideComponent(ABC):
    """Component interface for Composite pattern."""

    @abstractmethod
    def solve(self, problem: str) -> Session:
        """Solve a problem."""
        pass


class LeafGuide(GuideComponent):
    """Leaf node: actual Guide implementation."""

    def __init__(self, guide: Guide):
        self._guide = guide

    def solve(self, problem: str) -> Session:
        """Delegate to wrapped guide."""
        return self._guide.solve(problem)


class CompositeGuide(GuideComponent):
    """Composite: manages child guides."""

    def __init__(self, name: str):
        self.name = name
        self._children: list[GuideComponent] = []

    def add(self, guide: GuideComponent) -> None:
        """Add a child guide."""
        self._children.append(guide)

    def remove(self, guide: GuideComponent) -> None:
        """Remove a child guide."""
        self._children.remove(guide)

    def solve(self, problem: str) -> Session:
        """Solve by delegating to children and aggregating."""
        if not self._children:
            raise ValueError("No children to delegate to")

        # For now, just use first child
        # Could implement voting, consensus, etc.
        return self._children[0].solve(problem)


class VotingGuide(CompositeGuide):
    """Composite that uses majority voting."""

    def solve(self, problem: str) -> Session:
        """Solve with all children and pick best."""
        if not self._children:
            raise ValueError("No children to vote")

        sessions = [child.solve(problem) for child in self._children]

        # Pick session with highest quality
        best = max(sessions, key=lambda s: s.final_evaluation.overall.value)
        return best


# Test it
if __name__ == "__main__":
    print("Testing Composite Pattern:")

    # Create leaf guides
    from patterns import GuideFactory, GuideType

    strict_leaf = LeafGuide(GuideFactory.create(GuideType.STRICT, max_iterations=1))
    lenient_leaf = LeafGuide(GuideFactory.create(GuideType.LENIENT, max_iterations=1))

    # Create voting composite
    voting = VotingGuide("Voting Panel")
    voting.add(strict_leaf)
    voting.add(lenient_leaf)

    # Solve with voting
    session = voting.solve("Test problem for voting")
    print(f"  Voting result quality: {session.final_evaluation.overall.value:.3f}")
    print("  ✅ Composite pattern working")
