#!/usr/bin/env python3
"""
Pantheon Playground - Interactive Demo System

Explore how different Pantheon entities work together!

Demos:
1. TheGuide + TheReasoner: Meta-cognitive guidance with trace storage
2. TheGuide + Storyteller: Narrative generation with guidance
3. Multi-entity orchestration: Complex workflows

Usage:
    python playground/pantheon_playground.py --demo guide_reasoner
    python playground/pantheon_playground.py --demo all
    python playground/pantheon_playground.py --interactive
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import directly to avoid dependencies
import importlib.util


def load_module(name: str, path: Path):
    """Load a module dynamically."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Load TheGuide
pantheon_path = Path(__file__).parent.parent / "src" / "waft" / "pantheon"
guide_module = load_module("guide", pantheon_path / "guide.py")
TheGuide = guide_module.TheGuide
Protocol = guide_module.Protocol

# Try to load other entities
try:
    reasoner_module = load_module("reasoner", pantheon_path / "reasoner.py")
    TheReasoner = reasoner_module.TheReasoner
    HAS_REASONER = True
except Exception as e:
    print(f"⚠️  TheReasoner not available: {e}")
    HAS_REASONER = False

try:
    storyteller_module = load_module("storyteller", pantheon_path / "storyteller.py")
    Storyteller = storyteller_module.Storyteller
    HAS_STORYTELLER = True
except Exception as e:
    print(f"⚠️  Storyteller not available: {e}")
    HAS_STORYTELLER = False

# ============================================================================
# Demo LLM
# ============================================================================


class PlaygroundLLM:
    """Enhanced demo LLM for playground."""

    def __init__(self, personality="guide"):
        self.personality = personality
        self.call_count = 0

    def complete(self, prompt: str) -> str:
        """Generate contextual responses."""
        self.call_count += 1

        # Evaluation - check FIRST (most specific)
        if "fvcu" in prompt.lower() or (
            "evaluate" in prompt.lower() and "reasoning" in prompt.lower()
        ):
            base_score = 0.85 + (self.call_count % 3) * 0.05  # Vary between 0.85-0.95
            return f"""```json
{{
  "factuality": {base_score:.2f},
  "validity": {base_score - 0.02:.2f},
  "coherence": {base_score + 0.03:.2f},
  "utility": {base_score - 0.01:.2f},
  "faithfulness": {base_score + 0.02:.2f},
  "overall": {base_score:.2f},
  "rationale": "Strong systematic approach with clear logical progression.",
  "strengths": ["Well-structured", "Actionable steps", "Clear reasoning"],
  "weaknesses": ["Could add more specific examples"],
  "recommendations": ["Include code snippets", "Add visual diagrams"],
  "should_continue": false,
  "planning_detected": false,
  "unfaithful_reasoning_detected": false
}}
```"""

        # Story generation
        if "story" in prompt.lower() or "narrative" in prompt.lower():
            return """Once upon a time in the digital realm, there lived a curious developer who sought to understand the mysteries of code. With each line written, new patterns emerged - elegant solutions dancing across the screen like fireflies in the night.

The developer discovered that the true magic wasn't in the code itself, but in the reasoning behind it. Each decision, each trade-off, each elegant abstraction was a choice that told a story of its own."""

        # Architecture explanation
        if "architecture" in prompt.lower() or "system design" in prompt.lower():
            return """**Microservices Architecture Design:**

1. **API Gateway Layer**
   - Kong/AWS API Gateway
   - Rate limiting, auth, routing

2. **Service Mesh**
   - Istio/Linkerd for service-to-service communication
   - Traffic management, observability

3. **Core Services**
   - User Service (authentication, profiles)
   - Content Service (CRUD operations)
   - Analytics Service (metrics, tracking)

4. **Data Layer**
   - PostgreSQL for transactional data
   - Redis for caching and sessions
   - Elasticsearch for search

5. **Message Queue**
   - Kafka for event streaming
   - RabbitMQ for task queues

**Benefits:** Independent scaling, fault isolation, technology flexibility
**Trade-offs:** Increased complexity, network latency, data consistency challenges"""

        # Debugging guidance
        if "debug" in prompt.lower() or "error" in prompt.lower():
            return """**Debugging Strategy:**

1. **Reproduce the Issue**
   - Consistent steps to trigger the bug
   - Minimal test case

2. **Gather Evidence**
   - Stack traces
   - Log files
   - System state at failure time

3. **Form Hypothesis**
   - Most likely causes based on symptoms
   - Test assumptions systematically

4. **Test Solutions**
   - Fix the root cause, not symptoms
   - Add regression tests

5. **Document Findings**
   - Update documentation
   - Add preventive measures"""

        # Meta-cognitive guidance
        if "meta-cognitive" in prompt.lower():
            return """Let's approach this systematically by examining our thought process itself.

First, identify what we know and what we need to discover. Then, evaluate the quality of our reasoning at each step. Are we making logical leaps? Are our assumptions justified?

This meta-level awareness helps us catch errors early and build more robust solutions."""

        # Final answer
        if "final answer" in prompt.lower():
            return """Based on the systematic analysis and meta-cognitive guidance:

**Recommended Solution:**
1. Use a layered architecture approach
2. Implement clear separation of concerns
3. Add comprehensive error handling
4. Include monitoring and logging
5. Document design decisions

**Key Principles:**
- KISS (Keep It Simple, Stupid)
- DRY (Don't Repeat Yourself)
- SOLID principles
- Progressive enhancement

This approach balances simplicity with scalability while maintaining code quality."""

        # Default
        return f"🎮 Playground response #{self.call_count}: Exploring the problem space systematically..."


# ============================================================================
# Demo 1: TheGuide + TheReasoner Integration
# ============================================================================


def demo_guide_reasoner():
    """Demonstrate TheGuide + TheReasoner working together."""
    print("\n" + "=" * 80)
    print("  🎮 Demo 1: TheGuide + TheReasoner Integration")
    print("=" * 80 + "\n")

    print("This demo shows how TheGuide creates reasoning traces in TheReasoner")
    print("for transparent, traceable meta-cognitive guidance.\n")

    # Create TheGuide
    client_llm = PlaygroundLLM(personality="client")
    guide = TheGuide(
        project_path=Path.cwd(), client_llm=client_llm, guide_llm_config={"model": "demo"}
    )
    guide.guide_llm = PlaygroundLLM(personality="guide")

    print("📝 Running guidance session: 'Design a caching strategy'\n")

    # Run session
    answer, protocol = guide.solve(
        problem_statement="Design a caching strategy for a high-traffic API",
        max_iterations=2,
        quality_threshold=0.85,
    )

    print("✅ Session Complete!")
    print(f"   Session ID: {protocol.session_id}")
    print(f"   Iterations: {protocol.iteration_count}")
    print(f"   Quality Score: {protocol.quality_score:.2f}\n")

    print(f"📊 Final Answer:\n{answer}\n")

    # Show TheReasoner integration
    if HAS_REASONER:
        print("🔗 TheReasoner Integration:")
        try:
            reasoner = guide.reasoner
            recent = reasoner.get_recent_traces(limit=5)
            print(f"   ✅ {len(recent)} traces created during session")

            if recent:
                for i, trace in enumerate(recent[:3], 1):
                    print(f"\n   Trace {i}:")
                    print(f"   - ID: {trace.get('trace_id', 'N/A')}")
                    print(f"   - Decision: {trace.get('decision', 'N/A')[:60]}...")
                    print(f"   - Parent: {trace.get('parent_trace_id', 'N/A')}")
        except Exception as e:
            print(f"   ⚠️  Could not access traces: {e}")
    else:
        print("⚠️  TheReasoner not available (using mock)")

    print("\n💡 Key Feature: Each iteration creates a linked trace in TheReasoner,")
    print("   building a complete reasoning chain you can explore!")

    return protocol


# ============================================================================
# Demo 2: Multi-Stage Problem Solving
# ============================================================================


def demo_multi_stage():
    """Demonstrate multi-stage problem solving."""
    print("\n" + "=" * 80)
    print("  🎮 Demo 2: Multi-Stage Problem Solving")
    print("=" * 80 + "\n")

    print("This demo shows TheGuide tackling complex problems in stages.\n")

    client_llm = PlaygroundLLM()
    guide = TheGuide(
        project_path=Path.cwd(), client_llm=client_llm, guide_llm_config={"model": "demo"}
    )
    guide.guide_llm = PlaygroundLLM()

    stages = [
        ("Analysis", "Analyze the requirements for a real-time chat system"),
        ("Design", "Design the architecture based on the analysis"),
        ("Implementation", "Outline implementation steps"),
    ]

    results = []

    for stage_name, problem in stages:
        print(f"📍 Stage: {stage_name}")
        print(f"   Problem: {problem}\n")

        answer, protocol = guide.solve(
            problem_statement=problem, max_iterations=1, quality_threshold=0.85
        )

        results.append({"stage": stage_name, "answer": answer, "protocol": protocol})

        print(f"   ✅ Quality: {protocol.quality_score:.2f}")
        print(f"   📝 Answer: {answer[:100]}...\n")

    print("=" * 80)
    print("🎉 All stages complete!")
    print(f"   Total sessions: {len(results)}")
    print(
        f"   Average quality: {sum(r['protocol'].quality_score for r in results) / len(results):.2f}"
    )

    return results


# ============================================================================
# Demo 3: FVCU Score Evolution
# ============================================================================


def demo_score_evolution():
    """Show how FVCU scores evolve over iterations."""
    print("\n" + "=" * 80)
    print("  🎮 Demo 3: FVCU Score Evolution")
    print("=" * 80 + "\n")

    print("This demo tracks how reasoning quality improves with iterations.\n")

    client_llm = PlaygroundLLM()
    guide = TheGuide(
        project_path=Path.cwd(), client_llm=client_llm, guide_llm_config={"model": "demo"}
    )
    guide.guide_llm = PlaygroundLLM()

    answer, protocol = guide.solve(
        problem_statement="Explain the CAP theorem and its implications",
        max_iterations=3,
        quality_threshold=0.95,
    )

    print("📊 Score Evolution Across Iterations:\n")
    print(
        f"{'Iter':<6} {'Fact':<6} {'Valid':<6} {'Coher':<6} {'Util':<6} {'Faith':<6} {'Overall':<8}"
    )
    print("-" * 60)

    for eval_data in protocol.evaluations:
        scores = eval_data["scores"]
        print(
            f"{eval_data['iteration']:<6} "
            f"{scores['factuality']:<6.2f} "
            f"{scores['validity']:<6.2f} "
            f"{scores['coherence']:<6.2f} "
            f"{scores['utility']:<6.2f} "
            f"{scores['faithfulness']:<6.2f} "
            f"{scores['overall']:<8.2f}"
        )

    print("\n💡 Notice how scores can guide the iterative refinement process!")

    return protocol


# ============================================================================
# Demo 4: Comparative Analysis
# ============================================================================


def demo_comparative():
    """Compare different solution approaches."""
    print("\n" + "=" * 80)
    print("  🎮 Demo 4: Comparative Solution Analysis")
    print("=" * 80 + "\n")

    print("This demo uses TheGuide to compare different approaches.\n")

    client_llm = PlaygroundLLM()

    approaches = [
        "Monolithic architecture",
        "Microservices architecture",
        "Serverless architecture",
    ]

    results = []

    for approach in approaches:
        print(f"🔍 Analyzing: {approach}")

        guide = TheGuide(
            project_path=Path.cwd(), client_llm=client_llm, guide_llm_config={"model": "demo"}
        )
        guide.guide_llm = PlaygroundLLM()

        answer, protocol = guide.solve(
            problem_statement=f"Evaluate the {approach} approach for an e-commerce platform. Consider scalability, complexity, and cost.",
            max_iterations=1,
            quality_threshold=0.8,
        )

        results.append({"approach": approach, "score": protocol.quality_score, "answer": answer})

        print(f"   Quality Score: {protocol.quality_score:.2f}\n")

    print("=" * 80)
    print("📊 Comparative Results:\n")

    for result in sorted(results, key=lambda x: x["score"], reverse=True):
        print(f"🏆 {result['approach']}: {result['score']:.2f}")
        print(f"   {result['answer'][:80]}...\n")

    return results


# ============================================================================
# Interactive Playground
# ============================================================================


def interactive_playground():
    """Run interactive playground mode."""
    print("\n" + "=" * 80)
    print("  🎮 Pantheon Playground - Interactive Mode")
    print("=" * 80 + "\n")

    print("Available demos:")
    print("  1. TheGuide + TheReasoner Integration")
    print("  2. Multi-Stage Problem Solving")
    print("  3. FVCU Score Evolution")
    print("  4. Comparative Solution Analysis")
    print("  5. Custom Problem (your choice!)")
    print("  0. Exit")

    while True:
        try:
            choice = input("\n🎮 Select demo (0-5): ").strip()

            if choice == "0":
                print("\n👋 Thanks for playing!\n")
                break
            elif choice == "1":
                demo_guide_reasoner()
            elif choice == "2":
                demo_multi_stage()
            elif choice == "3":
                demo_score_evolution()
            elif choice == "4":
                demo_comparative()
            elif choice == "5":
                problem = input("\n📝 Enter your problem: ").strip()
                if problem:
                    client_llm = PlaygroundLLM()
                    guide = TheGuide(
                        project_path=Path.cwd(),
                        client_llm=client_llm,
                        guide_llm_config={"model": "demo"},
                    )
                    guide.guide_llm = PlaygroundLLM()

                    answer, protocol = guide.solve(
                        problem_statement=problem, max_iterations=3, quality_threshold=0.85
                    )

                    print("\n✅ Session Complete!")
                    print(f"   Quality: {protocol.quality_score:.2f}")
                    print(f"\n📊 Answer:\n{answer}\n")
            else:
                print("❌ Invalid choice")

        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 Thanks for playing!\n")
            break


# ============================================================================
# Main
# ============================================================================


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Pantheon Playground - Interactive Demo System")

    parser.add_argument(
        "--demo",
        "-d",
        choices=["guide_reasoner", "multi_stage", "score_evolution", "comparative", "all"],
        help="Run specific demo",
    )
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")

    args = parser.parse_args()

    print("\n🎮 Welcome to the Pantheon Playground! 🎮\n")
    print("Explore how different Pantheon entities work together.")
    print("All demos use mock LLMs - no API keys needed!\n")

    if args.interactive:
        interactive_playground()
    elif args.demo == "guide_reasoner":
        demo_guide_reasoner()
    elif args.demo == "multi_stage":
        demo_multi_stage()
    elif args.demo == "score_evolution":
        demo_score_evolution()
    elif args.demo == "comparative":
        demo_comparative()
    elif args.demo == "all":
        demo_guide_reasoner()
        demo_multi_stage()
        demo_score_evolution()
        demo_comparative()
    else:
        # Show menu
        print("Run with --interactive for interactive mode, or choose a demo:")
        print("  --demo guide_reasoner    TheGuide + TheReasoner integration")
        print("  --demo multi_stage       Multi-stage problem solving")
        print("  --demo score_evolution   FVCU score tracking")
        print("  --demo comparative       Comparative analysis")
        print("  --demo all              Run all demos")
        print("\nExample:")
        print("  python playground/pantheon_playground.py --demo all")
        print("  python playground/pantheon_playground.py --interactive")


if __name__ == "__main__":
    main()
