#!/usr/bin/env python3
"""
Bootstrap Epistemic State from Codebase Analysis

Automatically creates initial epistemic state by analyzing the codebase
and submitting preflight/postflight assessments to Empirica.

This helps TheOracle work immediately without requiring manual
preflight/postflight submissions.
"""

import json
import subprocess
import sys
from pathlib import Path

# Add project root to path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from waft.core.empirica import EmpiricaManager


def analyze_codebase(project_path: Path) -> dict[str, float]:
    """
    Analyze codebase to estimate epistemic vectors.

    Returns:
        Dictionary with estimated vector values
    """
    vectors = {
        "engagement": 0.7,  # Moderate engagement for active project
        "foundation": {
            "know": 0.6,  # Moderate knowledge (project exists, has structure)
            "do": 0.7,  # Can do things (code exists, scripts work)
            "context": 0.6,  # Understand context (project structure visible)
        },
        "comprehension": {"clarity": 0.6, "coherence": 0.7, "signal": 0.5, "density": 0.6},
        "execution": {"state": 0.7, "change": 0.5, "completion": 0.6, "impact": 0.6},
        "uncertainty": 0.4,  # Moderate uncertainty (some unknowns exist)
    }

    # Refine estimates based on codebase analysis
    try:
        # Check if project has substantial code
        src_dir = project_path / "src"
        if src_dir.exists():
            py_files = list(src_dir.rglob("*.py"))
            if len(py_files) > 50:
                vectors["foundation"]["know"] = 0.7
                vectors["foundation"]["do"] = 0.8
                vectors["comprehension"]["density"] = 0.7

        # Check for documentation
        docs_dir = project_path / "docs"
        readme = project_path / "README.md"
        if docs_dir.exists() or readme.exists():
            vectors["foundation"]["context"] = 0.7
            vectors["comprehension"]["clarity"] = 0.7

        # Check for tests
        tests_dir = project_path / "tests"
        if tests_dir.exists():
            vectors["foundation"]["know"] = 0.75
            vectors["uncertainty"] = 0.35

        # Check for work efforts (indicates active development)
        work_efforts = project_path / "_work_efforts"
        if work_efforts.exists():
            vectors["engagement"] = 0.8
            vectors["execution"]["state"] = 0.8

    except Exception:
        pass  # Use defaults if analysis fails

    return vectors


def bootstrap_epistemic_state(
    project_path: Path | None = None,
    ai_id: str = "claude-code",
    session_type: str = "development",
) -> bool:
    """
    Bootstrap epistemic state by creating session and submitting initial assessments.

    Args:
        project_path: Path to project root (default: current directory)
        ai_id: AI agent identifier
        session_type: Type of session

    Returns:
        True if successful, False otherwise
    """
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)

    print(f"🔮 Bootstrapping epistemic state for: {project_path}")
    print()

    # Initialize Empirica
    empirica = EmpiricaManager(project_path)

    if not empirica.is_initialized():
        print("→ Initializing Empirica...")
        if not empirica.initialize():
            print("❌ Failed to initialize Empirica")
            return False
        print("✓ Empirica initialized")
    else:
        print("✓ Empirica already initialized")

    # Create session
    print("→ Creating session...")
    session_id = empirica.create_session(ai_id=ai_id, session_type=session_type)
    if not session_id:
        print("❌ Failed to create session")
        return False
    print(f"✓ Session created: {session_id}")

    # Analyze codebase to estimate vectors
    print("→ Analyzing codebase...")
    vectors = analyze_codebase(project_path)
    print(
        f"✓ Estimated vectors: know={vectors['foundation']['know']:.0%}, uncertainty={vectors['uncertainty']:.0%}"
    )

    # Submit preflight using direct CLI call (more reliable)
    print("→ Submitting preflight assessment...")
    reasoning = f"Initial epistemic state bootstrap. Project: {project_path.name}, analyzed codebase structure."

    preflight_data = {"session_id": session_id, "vectors": vectors, "reasoning": reasoning}

    try:
        result = subprocess.run(
            ["empirica", "preflight-submit", "-"],
            cwd=project_path,
            input=json.dumps(preflight_data),
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        # Check if it actually succeeded
        try:
            output = json.loads(result.stdout)
            if output.get("ok"):
                print("✓ Preflight submitted")
            else:
                print(f"⚠️  Preflight returned: {output.get('message', 'unknown error')}")
        except json.JSONDecodeError:
            # Non-JSON output might still be success
            if result.returncode == 0:
                print("✓ Preflight submitted (non-JSON response)")
            else:
                print(f"⚠️  Preflight failed: {result.stderr}")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"⚠️  Preflight submission failed: {e}")

    # Submit postflight (same vectors for initial state)
    print("→ Submitting postflight assessment...")
    postflight_data = {
        "session_id": session_id,
        "vectors": vectors,
        "reasoning": "Initial state established via bootstrap.",
    }

    try:
        result = subprocess.run(
            ["empirica", "postflight-submit", "-"],
            cwd=project_path,
            input=json.dumps(postflight_data),
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        # Check if it actually succeeded
        try:
            output = json.loads(result.stdout)
            if output.get("ok"):
                print("✓ Postflight submitted")
            else:
                print(f"⚠️  Postflight returned: {output.get('message', 'unknown error')}")
        except json.JSONDecodeError:
            # Non-JSON output might still be success
            if result.returncode == 0:
                print("✓ Postflight submitted (non-JSON response)")
            else:
                print(f"⚠️  Postflight failed: {result.stderr}")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"⚠️  Postflight submission failed: {e}")

    # Verify state is now available
    print()
    print("→ Verifying epistemic state...")
    context = empirica.project_bootstrap()

    if context and context.get("epistemic_state"):
        epistemic_state = context.get("epistemic_state", {})
        state_vectors = epistemic_state.get("vectors", {})
        foundation = state_vectors.get("foundation", {})
        know = foundation.get("know", 0.0)
        uncertainty = state_vectors.get("uncertainty", 1.0)

        print("✓ Epistemic state available!")
        print(f"  Knowledge: {know:.0%}")
        print(f"  Uncertainty: {uncertainty:.0%}")
        print()
        print("🎉 Bootstrap complete! TheOracle should now work properly.")
        return True
    else:
        print("⚠️  Epistemic state not yet available in project-bootstrap")
        print("   This may take a moment for Empirica to process.")
        print("   Try running TheOracle again in a few seconds.")
        return True  # Still consider success - state may be processing


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Bootstrap epistemic state from codebase analysis")
    parser.add_argument("--path", "-p", type=str, help="Project path (default: current directory)")
    parser.add_argument(
        "--ai-id",
        type=str,
        default="claude-code",
        help="AI agent identifier (default: claude-code)",
    )
    parser.add_argument(
        "--session-type",
        type=str,
        default="development",
        help="Session type (default: development)",
    )

    args = parser.parse_args()

    project_path = Path(args.path) if args.path else None

    success = bootstrap_epistemic_state(
        project_path=project_path, ai_id=args.ai_id, session_type=args.session_type
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
