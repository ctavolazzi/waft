#!/usr/bin/env python3
"""
TheGuide CLI - Interactive Meta-Cognitive Guidance

A beautiful, interactive CLI for TheGuide system.

Features:
- Interactive guidance sessions
- Real-time FVCU score display
- Session history browsing
- "Why?" explanations
- ASCII art visualizations

Usage:
    # Interactive mode
    python cli/guide_cli.py

    # One-shot mode
    python cli/guide_cli.py --problem "How do I build a REST API?"

    # With options
    python cli/guide_cli.py --iterations 5 --threshold 0.9
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from waft.pantheon import EvaluationScores, Protocol, TheGuide
except ImportError:
    # Fallback to direct import
    import importlib.util

    guide_path = Path(__file__).parent.parent / "src" / "waft" / "pantheon" / "guide.py"
    spec = importlib.util.spec_from_file_location("guide", guide_path)
    guide_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guide_module)
    TheGuide = guide_module.TheGuide
    Protocol = guide_module.Protocol
    EvaluationScores = guide_module.EvaluationScores

# ============================================================================
# Colors and Styling
# ============================================================================


class Colors:
    """ANSI color codes."""

    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def colorize(text: str, color: str) -> str:
    """Add color to text."""
    return f"{color}{text}{Colors.END}"


def print_header(text: str):
    """Print a styled header."""
    print("\n" + colorize("=" * 80, Colors.CYAN))
    print(colorize(f"  {text}", Colors.BOLD + Colors.CYAN))
    print(colorize("=" * 80, Colors.CYAN))


def print_section(text: str):
    """Print a styled section."""
    print(f"\n{colorize('─' * 80, Colors.BLUE)}")
    print(colorize(f"  {text}", Colors.BOLD))
    print(colorize("─" * 80, Colors.BLUE))


def print_success(text: str):
    """Print success message."""
    print(colorize(f"✅ {text}", Colors.GREEN))


def print_error(text: str):
    """Print error message."""
    print(colorize(f"❌ {text}", Colors.RED))


def print_info(text: str):
    """Print info message."""
    print(colorize(f"ℹ️  {text}", Colors.CYAN))


def print_warning(text: str):
    """Print warning message."""
    print(colorize(f"⚠️  {text}", Colors.YELLOW))


# ============================================================================
# ASCII Art
# ============================================================================

LOGO = """
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   ████████╗██╗  ██╗███████╗     ██████╗ ██╗   ██╗██╗██████╗ ███████╗    ║
║   ╚══██╔══╝██║  ██║██╔════╝    ██╔════╝ ██║   ██║██║██╔══██╗██╔════╝    ║
║      ██║   ███████║█████╗      ██║  ███╗██║   ██║██║██║  ██║█████╗      ║
║      ██║   ██╔══██║██╔══╝      ██║   ██║██║   ██║██║██║  ██║██╔══╝      ║
║      ██║   ██║  ██║███████╗    ╚██████╔╝╚██████╔╝██║██████╔╝███████╗    ║
║      ╚═╝   ╚═╝  ╚═╝╚══════╝     ╚═════╝  ╚═════╝ ╚═╝╚═════╝ ╚══════╝    ║
║                                                                           ║
║                   Meta-Cognitive Guidance System                          ║
║                   "As Above, So Below"                                    ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

# ============================================================================
# FVCU Score Visualization
# ============================================================================


def visualize_score(name: str, score: float, width: int = 40) -> str:
    """Create a visual bar for a score."""
    filled = int(score * width)
    empty = width - filled

    # Color based on score
    if score >= 0.8:
        color = Colors.GREEN
    elif score >= 0.6:
        color = Colors.YELLOW
    else:
        color = Colors.RED

    bar = colorize("█" * filled, color) + colorize("░" * empty, Colors.END)
    return f"{name:12} [{bar}] {score:.2f}"


def display_fvcu_scores(scores: dict):
    """Display FVCU+Faithfulness scores with visualization."""
    print_section("FVCU+Faithfulness Scores")

    print(visualize_score("Factuality", scores["factuality"]))
    print(visualize_score("Validity", scores["validity"]))
    print(visualize_score("Coherence", scores["coherence"]))
    print(visualize_score("Utility", scores["utility"]))
    print(visualize_score("Faithfulness", scores["faithfulness"]))
    print(colorize("─" * 60, Colors.BLUE))
    print(visualize_score(colorize("Overall", Colors.BOLD), scores["overall"]))


# ============================================================================
# Mock LLM for Demo
# ============================================================================


class DemoLLM:
    """Demo LLM for CLI demonstration."""

    def __init__(self, model="demo-cli"):
        self.model = model
        self.call_count = 0

    def complete(self, prompt: str) -> str:
        """Generate demo responses."""
        self.call_count += 1

        if "meta-cognitive guide" in prompt.lower():
            if "first instruction" in prompt.lower():
                return "Let's begin by clearly defining the problem scope and identifying the key requirements."
            else:
                return "Now let's explore potential solutions and evaluate their trade-offs systematically."

        elif "follow the instruction" in prompt.lower():
            return """I'll approach this methodically:

1. Define the core requirements
2. Research best practices and existing solutions
3. Design a solution architecture
4. Consider implementation details
5. Identify potential challenges

Let me work through each step..."""

        elif "meta-cognitive evaluator" in prompt.lower():
            return """{
  "factuality": 0.92,
  "validity": 0.88,
  "coherence": 0.90,
  "utility": 0.91,
  "faithfulness": 0.93,
  "overall": 0.91,
  "rationale": "Excellent systematic approach with clear logical flow.",
  "strengths": ["Methodical breakdown", "Clear structure"],
  "weaknesses": ["Could add more specific examples"],
  "recommendations": ["Include concrete code examples"],
  "should_continue": false,
  "planning_detected": false,
  "unfaithful_reasoning_detected": false
}"""

        elif "final answer" in prompt.lower():
            return """Based on the systematic analysis:

**Recommended Approach:**
1. Start with a clear architecture design
2. Implement core components incrementally
3. Test thoroughly at each stage
4. Document as you build
5. Iterate based on feedback

**Key Considerations:**
- Keep it simple and maintainable
- Follow established patterns
- Plan for scalability
- Consider security from the start

This provides a solid foundation for success!"""

        return f"Demo response #{self.call_count}"


# ============================================================================
# Interactive CLI
# ============================================================================


class GuideCLI:
    """Interactive CLI for TheGuide."""

    def __init__(self):
        """Initialize the CLI."""
        self.guide: TheGuide | None = None
        self.project_path = Path.cwd()

    def setup(self):
        """Set up TheGuide instance."""
        # Check for API key
        api_key = os.getenv("LLM_API_KEY")
        model = os.getenv("LLM_MODEL", "anthropic/claude-sonnet-4-5-20250929")

        if api_key:
            try:
                from openhands.sdk import LLM

                client_llm = LLM(model=model, api_key=api_key)
                guide_llm_config = {"model": model, "api_key": api_key}
                print_success(f"Using real LLMs: {model}")
            except ImportError:
                client_llm = DemoLLM()
                guide_llm_config = {"model": "demo"}
                print_warning("OpenHands SDK not available, using demo LLM")
        else:
            client_llm = DemoLLM()
            guide_llm_config = {"model": "demo"}
            print_info("Using demo LLM (set LLM_API_KEY for real LLMs)")

        self.guide = TheGuide(
            project_path=self.project_path, client_llm=client_llm, guide_llm_config=guide_llm_config
        )

        print_info(f"Project: {self.project_path}")
        print_info(f"Storage: {self.guide.guide_path}")

    def run_session(
        self,
        problem: str,
        max_iterations: int = 10,
        quality_threshold: float = 0.8,
        enable_self_rewarding: bool = False,
        enable_self_correction: bool = False,
    ):
        """Run a guidance session."""
        print_header(f"Guidance Session - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        print_section("Problem Statement")
        print(f"  {problem}\n")

        print_section("Configuration")
        print(f"  Max Iterations: {max_iterations}")
        print(f"  Quality Threshold: {quality_threshold}")
        print(f"  Self-Rewarding: {enable_self_rewarding}")
        print(f"  Self-Correction: {enable_self_correction}")

        # Update guide settings
        self.guide.enable_self_rewarding = enable_self_rewarding
        self.guide.enable_self_correction = enable_self_correction

        print_section("Running Guidance Loop...")
        print()

        # Run guidance
        try:
            answer, protocol = self.guide.solve(
                problem_statement=problem,
                max_iterations=max_iterations,
                quality_threshold=quality_threshold,
            )

            # Display results
            print_header("Results")

            print_section("Final Answer")
            print(f"{answer}\n")

            print_section("Session Summary")
            print(f"  Session ID: {protocol.session_id}")
            print(f"  Iterations: {protocol.iteration_count}")
            print(
                f"  Quality Score: {colorize(f'{protocol.quality_score:.2f}', Colors.BOLD + Colors.GREEN)}"
            )
            print(f"  Created: {protocol.created}")
            print(f"  Completed: {protocol.completed}")

            # Display scores for each iteration
            for i, eval_data in enumerate(protocol.evaluations, 1):
                print(f"\n{colorize(f'Iteration {i}', Colors.BOLD)}")
                display_fvcu_scores(eval_data["scores"])

                if eval_data.get("planning_detected"):
                    print_warning("Forward-looking planning detected")

                if eval_data.get("unfaithful_reasoning_detected"):
                    print_warning("Unfaithful reasoning detected")

            # Ask if user wants explanation (only in interactive mode)
            try:
                print("\n")
                response = input(colorize("View 'Why?' explanation? (y/N): ", Colors.CYAN))
                if response.lower() == "y":
                    self.show_explanation(protocol.session_id)
            except (EOFError, KeyboardInterrupt):
                # Non-interactive mode or user cancelled
                print("\n")

            return protocol

        except Exception as e:
            print_error(f"Session failed: {e}")
            import traceback

            traceback.print_exc()
            return None

    def show_explanation(self, session_id: str):
        """Show 'Why?' explanation for a session."""
        print_header("'Why?' Explanation")

        explanation = self.guide.explain(session_id)
        print(explanation)

    def list_sessions(self, limit: int = 10):
        """List recent sessions."""
        print_header("Recent Sessions")

        recent = self.guide.get_recent_sessions(limit=limit)

        if not recent:
            print_info("No sessions found")
            return

        for i, session in enumerate(recent, 1):
            session_id = session.get("session_id", "N/A")
            print(f"\n{colorize(f'{i}. {session_id}', Colors.BOLD)}")
            print(f"   Problem: {session.get('problem_summary', 'N/A')[:60]}...")
            print(f"   Quality: {visualize_score('', session.get('quality_score', 0.0), width=20)}")
            print(f"   Iterations: {session.get('iterations', 0)}")
            print(f"   Created: {session.get('created', 'N/A')}")

    def interactive_mode(self):
        """Run in interactive mode."""
        print(colorize(LOGO, Colors.CYAN))

        while True:
            print_section("Main Menu")
            print("1. Start new guidance session")
            print("2. View recent sessions")
            print("3. View session explanation")
            print("4. Analytics")
            print("5. Exit")

            choice = input(colorize("\nSelect option (1-5): ", Colors.CYAN))

            if choice == "1":
                problem = input(colorize("\nEnter your problem: ", Colors.YELLOW))
                if problem:
                    self.run_session(problem)

            elif choice == "2":
                self.list_sessions()

            elif choice == "3":
                session_id = input(colorize("\nEnter session ID: ", Colors.YELLOW))
                if session_id:
                    self.show_explanation(session_id)

            elif choice == "4":
                self.show_analytics()

            elif choice == "5":
                print_success("Goodbye! ✨")
                break

            else:
                print_error("Invalid choice")

    def show_analytics(self):
        """Show analytics across sessions."""
        print_header("Analytics")

        summary = self.guide.get_session_summary()
        recent = self.guide.get_recent_sessions(limit=100)

        print(f"  Total Sessions: {summary['total_sessions']}")
        print(f"  Total Protocols: {summary['total_protocols']}")

        if recent:
            avg_quality = sum(s.get("quality_score", 0.0) for s in recent) / len(recent)
            avg_iterations = sum(s.get("iterations", 0) for s in recent) / len(recent)

            print(f"  Average Quality: {avg_quality:.2f}")
            print(f"  Average Iterations: {avg_iterations:.1f}")

        print(f"  Last Updated: {summary.get('last_updated', 'N/A')}")


# ============================================================================
# Main
# ============================================================================


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="TheGuide CLI - Meta-Cognitive Guidance System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python cli/guide_cli.py

  # One-shot mode
  python cli/guide_cli.py --problem "How do I build a REST API?"

  # With custom settings
  python cli/guide_cli.py --problem "Explain OAuth2" --iterations 5 --threshold 0.9
        """,
    )

    parser.add_argument("--problem", "-p", help="Problem statement")
    parser.add_argument("--iterations", "-i", type=int, default=10, help="Max iterations")
    parser.add_argument("--threshold", "-t", type=float, default=0.8, help="Quality threshold")
    parser.add_argument("--self-rewarding", action="store_true", help="Enable self-rewarding")
    parser.add_argument("--self-correction", action="store_true", help="Enable self-correction")
    parser.add_argument("--list", "-l", action="store_true", help="List recent sessions")
    parser.add_argument("--explain", "-e", help="Show explanation for session ID")

    args = parser.parse_args()

    # Create CLI instance
    cli = GuideCLI()
    cli.setup()

    # Handle different modes
    if args.list:
        cli.list_sessions()
    elif args.explain:
        cli.show_explanation(args.explain)
    elif args.problem:
        cli.run_session(
            problem=args.problem,
            max_iterations=args.iterations,
            quality_threshold=args.threshold,
            enable_self_rewarding=args.self_rewarding,
            enable_self_correction=args.self_correction,
        )
    else:
        # Interactive mode
        cli.interactive_mode()


if __name__ == "__main__":
    main()
