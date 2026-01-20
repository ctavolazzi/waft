#!/usr/bin/env python3
"""
Run Study Gym Session
====================

Executed by /study command to run a study session.
"""

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.study_gym import ChallengeGenerator, run_study_session


def parse_arguments(args: list) -> tuple[str, dict[str, Any]]:
    """Parse command line arguments."""
    if not args:
        return None, {}

    template_name = args[0]
    variables = {}

    # Parse variable assignments: key=value
    for arg in args[1:]:
        if "=" in arg:
            key, value = arg.split("=", 1)
            # Try to parse as number
            try:
                if "." in value:
                    variables[key] = float(value)
                else:
                    variables[key] = int(value)
            except ValueError:
                # Remove quotes if present
                variables[key] = value.strip("\"'")

    return template_name, variables


def main():
    """Main entry point for /study command."""
    args = sys.argv[1:] if len(sys.argv) > 1 else []

    if not args:
        # Show available templates
        print("=" * 60)
        print("📚 Study Gym - Available Challenge Templates")
        print("=" * 60)
        print()

        templates = ChallengeGenerator._get_templates()
        for name, template in templates.items():
            print(f"**{name}**")
            print(f"  {template['description']}")
            print(f"  Objective: {template['objective']}")
            print(f"  Variables: {', '.join(template['variables'])}")
            print()

        print("Usage: /study <template> [key=value ...]")
        print()
        print("Example:")
        print('  /study page_constraint target_pages=2 content="<h2>Test</h2><p>Content</p>"')
        print()
        return

    template_name, variables = parse_arguments(args)

    if not template_name:
        print("Error: No template specified")
        return

    # Generate challenge configuration
    try:
        challenge_config = ChallengeGenerator.generate_challenge(template_name, variables)
    except ValueError as e:
        print(f"❌ Error: {e}")
        print()
        print("Available templates:")
        for template in ChallengeGenerator.list_templates():
            print(f"  - {template}")
        return

    # Run study session
    try:
        session = run_study_session(challenge_config)

        print()
        print("=" * 60)
        print("📊 Session Summary")
        print("=" * 60)
        print(f"Session ID: {session.session_id}")
        print(f"Observations: {len(session.observations)}")
        print(f"Hypotheses: {len(session.hypotheses)}")
        print(f"Findings: {len(session.findings)}")
        print(f"Conclusions: {len(session.conclusions)}")
        print()

        # Show confirmed hypotheses
        confirmed = [h for h in session.hypotheses if h.status == "confirmed"]
        if confirmed:
            print("✅ Confirmed Hypotheses:")
            for hyp in confirmed:
                print(f"   - {hyp.statement} (confidence: {hyp.confidence:.2f})")
            print()

        # Show conclusions
        if session.conclusions:
            print("🎯 Conclusions:")
            for conclusion in session.conclusions:
                print(f"   - {conclusion}")
            print()

    except Exception as e:
        print(f"❌ Error during study session: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
