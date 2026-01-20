#!/usr/bin/env python3
"""
TheGuide Examples - Real-World Use Cases

Collection of example scripts demonstrating TheGuide capabilities:
- Code review guidance
- Architecture design assistance
- Debugging help
- Learning assistance
- Integration with other Pantheon entities

Run examples:
    python examples/guide_examples.py --example code_review
    python examples/guide_examples.py --example architecture
    python examples/guide_examples.py --example debug
    python examples/guide_examples.py --all
"""

import sys
from pathlib import Path
import argparse
from typing import Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Mock LLM for examples
class ExampleLLM:
    """Example LLM with realistic technical responses."""

    def __init__(self):
        self.call_count = 0

    def complete(self, prompt: str) -> str:
        self.call_count += 1

        # Code review guidance
        if "code review" in prompt.lower():
            if "first instruction" in prompt.lower():
                return "Let's start by examining the overall code structure and identifying potential issues in organization, naming, and high-level design."
            elif "follow the instruction" in prompt.lower():
                return """Looking at the code structure:

**Strengths:**
- Clear separation of concerns
- Good use of type hints
- Comprehensive docstrings

**Areas for Improvement:**
1. Some functions are too long (>50 lines)
2. Missing error handling in critical paths
3. Could benefit from more unit tests
4. Some variable names could be more descriptive

**Recommendations:**
- Break down large functions into smaller, focused ones
- Add try-catch blocks for file I/O and external API calls
- Increase test coverage to at least 80%
- Follow naming conventions more consistently"""

            elif "meta-cognitive evaluator" in prompt.lower():
                return """{
  "factuality": 0.95,
  "validity": 0.92,
  "coherence": 0.90,
  "utility": 0.93,
  "faithfulness": 0.94,
  "overall": 0.93,
  "rationale": "Thorough code review with actionable feedback.",
  "strengths": ["Specific recommendations", "Balanced feedback"],
  "weaknesses": ["Could prioritize issues by severity"],
  "recommendations": ["Add severity levels to recommendations"],
  "should_continue": true,
  "planning_detected": false,
  "unfaithful_reasoning_detected": false
}"""

        # Architecture guidance
        elif "architecture" in prompt.lower() or "design" in prompt.lower():
            if "first instruction" in prompt.lower():
                return "Let's begin by understanding the system requirements, scale expectations, and key constraints."
            elif "follow the instruction" in prompt.lower():
                return """System Architecture Analysis:

**Requirements:**
- Handle 10K requests/second
- 99.9% uptime SLA
- Multi-region deployment
- Real-time data processing

**Proposed Architecture:**
1. **Load Balancer Layer**: AWS ELB with auto-scaling
2. **API Gateway**: Kong for rate limiting and auth
3. **Application Layer**: Microservices in Kubernetes
4. **Data Layer**: PostgreSQL (primary), Redis (cache)
5. **Message Queue**: Kafka for async processing
6. **Monitoring**: Prometheus + Grafana

**Trade-offs:**
- Microservices add complexity but enable independent scaling
- Kafka ensures reliability but adds latency
- Multi-region increases cost but improves availability"""

            elif "meta-cognitive evaluator" in prompt.lower():
                return """{
  "factuality": 0.94,
  "validity": 0.91,
  "coherence": 0.93,
  "utility": 0.95,
  "faithfulness": 0.92,
  "overall": 0.93,
  "rationale": "Solid architecture with clear rationale for tech choices.",
  "strengths": ["Comprehensive coverage", "Trade-off analysis"],
  "weaknesses": ["Missing disaster recovery plan"],
  "recommendations": ["Add DR and backup strategies"],
  "should_continue": true,
  "planning_detected": false,
  "unfaithful_reasoning_detected": false
}"""

        # Debugging assistance
        elif "debug" in prompt.lower() or "error" in prompt.lower():
            if "first instruction" in prompt.lower():
                return "Let's systematically analyze the error message, stack trace, and identify the root cause."
            elif "follow the instruction" in prompt.lower():
                return """Debugging Analysis:

**Error:** NullPointerException at line 42

**Root Cause Analysis:**
1. The `user` object is null when `user.getName()` is called
2. This happens when database query returns no results
3. Query fails because user ID format changed in recent migration

**Fix:**
```python
# Before (buggy)
user = db.get_user(user_id)
name = user.getName()  # NPE if user is null

# After (fixed)
user = db.get_user(user_id)
if user is None:
    raise UserNotFoundException(f"User {user_id} not found")
name = user.getName()
```

**Prevention:**
- Add null checks before accessing object properties
- Use Optional<T> types where applicable
- Add integration tests for edge cases"""

            elif "meta-cognitive evaluator" in prompt.lower():
                return """{
  "factuality": 0.96,
  "validity": 0.94,
  "coherence": 0.95,
  "utility": 0.97,
  "faithfulness": 0.95,
  "overall": 0.95,
  "rationale": "Excellent debugging analysis with clear fix and prevention.",
  "strengths": ["Root cause identified", "Concrete solution provided"],
  "weaknesses": [],
  "recommendations": ["Consider adding monitoring to detect this issue earlier"],
  "should_continue": false,
  "planning_detected": false,
  "unfaithful_reasoning_detected": false
}"""

        # Learning assistance
        elif "learn" in prompt.lower() or "explain" in prompt.lower():
            if "first instruction" in prompt.lower():
                return "Let's break down the concept into fundamental components and build understanding step-by-step."
            elif "follow the instruction" in prompt.lower():
                return """Understanding OAuth 2.0:

**Core Concept:**
OAuth 2.0 is an authorization framework that allows applications to access resources on behalf of a user without sharing passwords.

**Key Components:**
1. **Resource Owner** - The user who owns the data
2. **Client** - The application requesting access
3. **Authorization Server** - Issues access tokens
4. **Resource Server** - Hosts the protected resources

**Flow (Authorization Code Grant):**
1. Client redirects user to authorization server
2. User authenticates and grants permission
3. Server redirects back with authorization code
4. Client exchanges code for access token
5. Client uses token to access protected resources

**Why It Matters:**
- Eliminates password sharing
- Allows granular permissions
- Enables single sign-on
- Industry standard for API access"""

            elif "meta-cognitive evaluator" in prompt.lower():
                return """{
  "factuality": 0.97,
  "validity": 0.95,
  "coherence": 0.96,
  "utility": 0.94,
  "faithfulness": 0.96,
  "overall": 0.96,
  "rationale": "Clear, accurate explanation with good structure.",
  "strengths": ["Builds from fundamentals", "Real-world context"],
  "weaknesses": ["Could include a diagram"],
  "recommendations": ["Add visual representation of the flow"],
  "should_continue": false,
  "planning_detected": false,
  "unfaithful_reasoning_detected": false
}"""

        # Final answer fallback
        elif "final answer" in prompt.lower():
            return "Based on the systematic analysis, the recommended approach provides a solid solution that addresses the key requirements while considering trade-offs and best practices."

        return f"Example response #{self.call_count}"

# ============================================================================
# Example 1: Code Review Assistance
# ============================================================================

def example_code_review():
    """Demonstrate code review guidance."""
    print("\n" + "="*80)
    print("  Example 1: Code Review Assistance")
    print("="*80 + "\n")

    try:
        from waft.pantheon import TheGuide
    except:
        import importlib.util
        guide_path = Path(__file__).parent.parent / "src" / "waft" / "pantheon" / "guide.py"
        spec = importlib.util.spec_from_file_location("guide", guide_path)
        guide_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(guide_module)
        TheGuide = guide_module.TheGuide

    # Create guide with example LLM
    client_llm = ExampleLLM()
    guide = TheGuide(
        project_path=Path.cwd(),
        client_llm=client_llm,
        guide_llm_config={"model": "example"}
    )
    guide.guide_llm = ExampleLLM()

    # Run code review
    answer, protocol = guide.solve(
        problem_statement="""Review this Python code for best practices and potential issues:

```python
def process_data(file_path):
    data = open(file_path).read()
    result = []
    for line in data.split('\\n'):
        if line:
            parts = line.split(',')
            result.append({'name': parts[0], 'value': int(parts[1])})
    return result
```
""",
        max_iterations=3,
        quality_threshold=0.85
    )

    print("✅ Code Review Complete!\n")
    print(f"Session ID: {protocol.session_id}")
    print(f"Quality Score: {protocol.quality_score:.2f}\n")
    print(f"Review:\n{answer}\n")

    return protocol

# ============================================================================
# Example 2: Architecture Design
# ============================================================================

def example_architecture_design():
    """Demonstrate architecture design assistance."""
    print("\n" + "="*80)
    print("  Example 2: Architecture Design Assistance")
    print("="*80 + "\n")

    try:
        from waft.pantheon import TheGuide
    except:
        import importlib.util
        guide_path = Path(__file__).parent.parent / "src" / "waft" / "pantheon" / "guide.py"
        spec = importlib.util.spec_from_file_location("guide", guide_path)
        guide_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(guide_module)
        TheGuide = guide_module.TheGuide

    client_llm = ExampleLLM()
    guide = TheGuide(
        project_path=Path.cwd(),
        client_llm=client_llm,
        guide_llm_config={"model": "example"}
    )
    guide.guide_llm = ExampleLLM()

    answer, protocol = guide.solve(
        problem_statement="""Design a scalable architecture for a real-time chat application that needs to support:
- 100K concurrent users
- Message persistence
- File sharing
- Push notifications
- Multi-device sync
""",
        max_iterations=3,
        quality_threshold=0.85
    )

    print("✅ Architecture Design Complete!\n")
    print(f"Session ID: {protocol.session_id}")
    print(f"Quality Score: {protocol.quality_score:.2f}\n")
    print(f"Design:\n{answer}\n")

    return protocol

# ============================================================================
# Example 3: Debugging Assistance
# ============================================================================

def example_debugging():
    """Demonstrate debugging assistance."""
    print("\n" + "="*80)
    print("  Example 3: Debugging Assistance")
    print("="*80 + "\n")

    try:
        from waft.pantheon import TheGuide
    except:
        import importlib.util
        guide_path = Path(__file__).parent.parent / "src" / "waft" / "pantheon" / "guide.py"
        spec = importlib.util.spec_from_file_location("guide", guide_path)
        guide_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(guide_module)
        TheGuide = guide_module.TheGuide

    client_llm = ExampleLLM()
    guide = TheGuide(
        project_path=Path.cwd(),
        client_llm=client_llm,
        guide_llm_config={"model": "example"}
    )
    guide.guide_llm = ExampleLLM()

    answer, protocol = guide.solve(
        problem_statement="""Help debug this error:

Error: NullPointerException at UserService.java:42
Stack trace:
  at com.app.UserService.processUser(UserService.java:42)
  at com.app.Controller.handleRequest(Controller.java:15)

Code at line 42:
  String name = user.getName();  // NPE occurs here

Context: This started happening after recent database migration.
""",
        max_iterations=2,
        quality_threshold=0.90
    )

    print("✅ Debugging Complete!\n")
    print(f"Session ID: {protocol.session_id}")
    print(f"Quality Score: {protocol.quality_score:.2f}\n")
    print(f"Solution:\n{answer}\n")

    return protocol

# ============================================================================
# Example 4: Learning Assistance
# ============================================================================

def example_learning():
    """Demonstrate learning assistance."""
    print("\n" + "="*80)
    print("  Example 4: Learning Assistance")
    print("="*80 + "\n")

    try:
        from waft.pantheon import TheGuide
    except:
        import importlib.util
        guide_path = Path(__file__).parent.parent / "src" / "waft" / "pantheon" / "guide.py"
        spec = importlib.util.spec_from_file_location("guide", guide_path)
        guide_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(guide_module)
        TheGuide = guide_module.TheGuide

    client_llm = ExampleLLM()
    guide = TheGuide(
        project_path=Path.cwd(),
        client_llm=client_llm,
        guide_llm_config={"model": "example"}
    )
    guide.guide_llm = ExampleLLM()

    answer, protocol = guide.solve(
        problem_statement="Explain OAuth 2.0 in simple terms with a practical example.",
        max_iterations=2,
        quality_threshold=0.90
    )

    print("✅ Learning Session Complete!\n")
    print(f"Session ID: {protocol.session_id}")
    print(f"Quality Score: {protocol.quality_score:.2f}\n")
    print(f"Explanation:\n{answer}\n")

    return protocol

# ============================================================================
# Example 5: Integration with TheReasoner
# ============================================================================

def example_reasoner_integration():
    """Demonstrate integration with TheReasoner."""
    print("\n" + "="*80)
    print("  Example 5: TheReasoner Integration")
    print("="*80 + "\n")

    try:
        from waft.pantheon import TheGuide, TheReasoner
    except:
        import importlib.util
        pantheon_path = Path(__file__).parent.parent / "src" / "waft" / "pantheon"

        # Import TheGuide
        guide_path = pantheon_path / "guide.py"
        spec = importlib.util.spec_from_file_location("guide", guide_path)
        guide_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(guide_module)
        TheGuide = guide_module.TheGuide

    client_llm = ExampleLLM()
    guide = TheGuide(
        project_path=Path.cwd(),
        client_llm=client_llm,
        guide_llm_config={"model": "example"}
    )
    guide.guide_llm = ExampleLLM()

    # Run a session
    answer, protocol = guide.solve(
        problem_statement="How do I implement a caching strategy?",
        max_iterations=2
    )

    print("✅ Session Complete!\n")
    print(f"Session ID: {protocol.session_id}\n")

    # Show TheReasoner integration
    print("🔗 TheReasoner Integration:")
    try:
        reasoner = guide.reasoner
        recent_traces = reasoner.get_recent_traces(limit=5)
        print(f"  Recent traces: {len(recent_traces)}")

        if recent_traces:
            latest = recent_traces[0]
            print(f"  Latest trace: {latest.get('trace_id', 'N/A')}")
            print(f"  Decision: {latest.get('decision', 'N/A')[:60]}...")
    except Exception as e:
        print(f"  (TheReasoner not available: {e})")

    return protocol

# ============================================================================
# Main
# ============================================================================

def main():
    """Run examples."""
    parser = argparse.ArgumentParser(description="TheGuide Examples")
    parser.add_argument("--example", "-e", choices=[
        "code_review", "architecture", "debug", "learning", "reasoner"
    ], help="Run specific example")
    parser.add_argument("--all", "-a", action="store_true", help="Run all examples")

    args = parser.parse_args()

    examples = {
        "code_review": example_code_review,
        "architecture": example_architecture_design,
        "debug": example_debugging,
        "learning": example_learning,
        "reasoner": example_reasoner_integration
    }

    if args.all:
        for name, func in examples.items():
            try:
                func()
            except Exception as e:
                print(f"❌ Example '{name}' failed: {e}")
                import traceback
                traceback.print_exc()
    elif args.example:
        examples[args.example]()
    else:
        print("TheGuide Examples\n")
        print("Available examples:")
        for name in examples.keys():
            print(f"  - {name}")
        print("\nUsage:")
        print("  python examples/guide_examples.py --example code_review")
        print("  python examples/guide_examples.py --all")

if __name__ == "__main__":
    main()
