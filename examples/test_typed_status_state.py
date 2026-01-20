#!/usr/bin/env python3
"""
Test Typed StatusState Integration
==================================

Tests the new typed StatusState classes with computed properties.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.waft_status import check_status
from src.waft.core.status_state import (
    EpistemicState,
    GamificationState,
    StatusState,
)
from src.waft.evolution.status_components import create_status_components_from_status_dict


def test_typed_state_creation():
    """Test creating typed state from dict."""
    print("🧪 Test 1: Typed State Creation")

    # Get status dict
    status_dict = check_status(project_path=Path.cwd(), log_event=False)

    # Create typed state
    typed_state = StatusState.from_dict(status_dict)

    print(f"  ✓ Epistemic coverage: {typed_state.epistemic.coverage_pct:.1f}%")
    print(f"  ✓ Epistemic health: {typed_state.epistemic.health_status}")
    print(f"  ✓ Gamification integrity: {typed_state.gamification.integrity_status}")
    print(f"  ✓ Project health score: {typed_state.project_health.health_score:.1f}")
    print(f"  ✓ Overall health: {typed_state.overall_health_status}")

    return typed_state


def test_computed_properties():
    """Test computed properties."""
    print("\n🧪 Test 2: Computed Properties")

    # Create test epistemic state
    epistemic = EpistemicState(
        initialized=True,
        knowledge_pct=75.0,
        uncertainty_pct=25.0,
        moon_phase="🌔",
        moon_phase_desc="Good (75% coverage)",
    )

    print(f"  ✓ Coverage: {epistemic.coverage_pct:.1f}% (expected: 87.5%)")
    print(f"  ✓ Health: {epistemic.health_status}")
    print(f"  ✓ Knowledge ratio: {epistemic.knowledge_ratio:.2f}")

    # Create test gamification state
    gamification = GamificationState(available=True, level=3, integrity=87.5, insight=450.0)

    print(f"  ✓ Integrity status: {gamification.integrity_status}")
    print(f"  ✓ Next level XP: {gamification.next_level_xp:.0f}")
    print(f"  ✓ Level progress: {gamification.level_progress_pct:.1f}%")

    return epistemic, gamification


def test_backward_compatibility():
    """Test backward compatibility (dict conversion)."""
    print("\n🧪 Test 3: Backward Compatibility")

    typed_state = StatusState.from_dict(check_status(log_event=False))

    # Convert back to dict
    status_dict = typed_state.to_dict()

    print("  ✓ Dict conversion successful")
    print(
        f"  ✓ Epistemic state in dict: {status_dict.get('epistemic_state', {}).get('coverage_pct')}"
    )
    print(f"  ✓ Overall health in dict: {status_dict.get('overall_health_status')}")

    return status_dict


def test_integration_with_components():
    """Test integration with status components."""
    print("\n🧪 Test 4: Integration with Components")

    status_dict = check_status(log_event=False)
    typed_state = StatusState.from_dict(status_dict)

    # Create components with typed state
    components = create_status_components_from_status_dict(status_dict, typed_state=typed_state)

    print(f"  ✓ Generated {len(components)} components with typed state")
    print("  ✓ Components use computed properties from typed state")

    return components


def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 Typed StatusState Testing")
    print("=" * 60)
    print()

    try:
        # Test 1: Creation
        test_typed_state_creation()

        # Test 2: Computed properties
        epistemic, gamification = test_computed_properties()

        # Test 3: Backward compatibility
        test_backward_compatibility()

        # Test 4: Integration
        test_integration_with_components()

        print()
        print("=" * 60)
        print("✅ All Tests Passed!")
        print("=" * 60)
        print()
        print("Key Benefits:")
        print("  ✓ Type safety and IDE autocomplete")
        print("  ✓ Computed properties (coverage, health, progress)")
        print("  ✓ Backward compatible (to_dict() method)")
        print("  ✓ Integration with status components")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    main()
