"""
WAFT Reflection System Demonstration
=====================================

This demonstrates WAFT's ability to observe and document itself.

What happens here:
1. WAFT scans its own codebase
2. Identifies documentation gaps
3. Generates a reflection report
4. Creates architecture documentation
5. Assembles everything into a binder

WAFT DOCUMENTING ITSELF.

This is the recursive self-improvement loop:
- System observes itself
- Documents what it sees
- Uses that documentation to improve
- Documents the improvements
- Cycle continues

Run this to see WAFT reflect on its own existence.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.reflection import (
    generate_architecture_doc_example,
    run_reflection_example,
)


def main():
    """Run full reflection demonstration."""

    print("=" * 80)
    print("WAFT REFLECTION SYSTEM DEMONSTRATION")
    print("=" * 80)
    print()
    print("WAFT is about to observe itself, document what it sees,")
    print("and create comprehensive self-documentation.")
    print()
    print("This is a system achieving self-awareness through documentation.")
    print()
    print("=" * 80)
    print()

    # Step 1: Run reflection
    print("STEP 1: OBSERVATION")
    print("-" * 80)
    run_reflection_example()

    print()
    input("Press Enter to continue to Step 2...")
    print()

    # Step 2: Generate architecture docs
    print("STEP 2: ARCHITECTURE DOCUMENTATION")
    print("-" * 80)
    generate_architecture_doc_example()

    print()
    print("=" * 80)
    print("REFLECTION COMPLETE")
    print("=" * 80)
    print()
    print("Generated:")
    print("  1. Reflection Report: _work_efforts/WAFT_Reflection_Report.pdf")
    print("  2. Architecture Doc: _work_efforts/WAFT_Architecture.pdf")
    print()
    print("WAFT has successfully documented itself.")
    print()
    print("These documents were created BY WAFT, ABOUT WAFT, USING WAFT.")
    print("The system is now self-documenting.")
    print()
    print("=" * 80)
    print()
    print("🎉 THE RECURSIVE LOOP IS COMPLETE 🎉")
    print()
    print("WAFT can now:")
    print("  - Observe its own structure")
    print("  - Identify documentation gaps")
    print("  - Generate documentation to fill those gaps")
    print("  - Use that documentation to inform future development")
    print("  - Document those changes")
    print("  - Repeat indefinitely")
    print()
    print("A self-improving system through documentation.")
    print()


if __name__ == "__main__":
    main()
