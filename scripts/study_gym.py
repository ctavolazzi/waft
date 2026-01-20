#!/usr/bin/env python3
"""
Study Gym CLI
=============

Command-line interface for the DocumentBuilder Study Gym.
"""

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.study_gym import ChallengeGenerator, run_study_session


def parse_variables(var_string: str) -> dict[str, Any]:
    """Parse variable string into dictionary."""
    variables = {}

    # Format: key1=value1 key2=value2
    parts = var_string.split()
    for part in parts:
        if "=" in part:
            key, value = part.split("=", 1)
            # Try to parse as number
            try:
                if "." in value:
                    variables[key] = float(value)
                else:
                    variables[key] = int(value)
            except ValueError:
                variables[key] = value

    return variables


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: study_gym.py <template> [variables]")
        print()
        print("Available templates:")
        for template in ChallengeGenerator.list_templates():
            print(f"  - {template}")
        print()
        print("Example:")
        print("  study_gym.py page_constraint target_pages=2 content='<h2>Test</h2>'")
        sys.exit(1)

    template_name = sys.argv[1]
    variables = {}

    if len(sys.argv) > 2:
        var_string = " ".join(sys.argv[2:])
        variables = parse_variables(var_string)

    # Generate challenge
    try:
        challenge_config = ChallengeGenerator.generate_challenge(template_name, variables)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Run study session
    session = run_study_session(challenge_config)

    print()
    print("✅ Study session complete!")
    print(f"   Session ID: {session.session_id}")
    print(f"   Observations: {len(session.observations)}")
    print(f"   Hypotheses: {len(session.hypotheses)}")
    print(f"   Findings: {len(session.findings)}")
    print(f"   Conclusions: {len(session.conclusions)}")


if __name__ == "__main__":
    main()
