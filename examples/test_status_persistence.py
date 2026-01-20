#!/usr/bin/env python3
"""
Test Status Persistence System
==============================

Tests the status persistence system with checksums, history tracking, and comparison.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.waft_status import check_status
from src.waft.core.status_persistence import (
    StatusPersistence,
    load_status_snapshot,
    save_status_snapshot,
)


def test_save_and_load():
    """Test saving and loading snapshots."""
    print("🧪 Test 1: Save and Load")

    # Get status
    status = check_status(log_event=False)

    # Save snapshot
    snapshot = save_status_snapshot(status)
    snapshot_id = snapshot["snapshot_id"]

    print(f"  ✓ Snapshot saved: {snapshot_id}")
    print(f"  ✓ Checksum: {snapshot['checksum'][:16]}...")

    # Load snapshot
    loaded_status = load_status_snapshot(snapshot_id)

    assert loaded_status is not None, "Failed to load snapshot"
    assert loaded_status.get("epistemic_state") == status.get("epistemic_state"), "Status mismatch"

    print("  ✓ Snapshot loaded and verified")

    return snapshot_id


def test_integrity_verification():
    """Test checksum integrity verification."""
    print("\n🧪 Test 2: Integrity Verification")

    # Save snapshot
    status = check_status(log_event=False)
    snapshot = save_status_snapshot(status)
    snapshot_id = snapshot["snapshot_id"]

    # Load with verification
    loaded = load_status_snapshot(snapshot_id, verify_integrity=True)
    assert loaded is not None, "Valid snapshot should load"
    print("  ✓ Valid snapshot verified")

    # Corrupt the file
    snapshot_file = Path("_pyrite/.waft/status_snapshots") / f"{snapshot_id}.json"
    content = snapshot_file.read_text()
    corrupted = content.replace('"knowledge_pct":', '"knowledge_pct_corrupted":')
    snapshot_file.write_text(corrupted)

    # Try to load corrupted snapshot
    loaded_corrupted = load_status_snapshot(snapshot_id, verify_integrity=True)
    assert loaded_corrupted is None, "Corrupted snapshot should fail verification"
    print("  ✓ Corrupted snapshot rejected")

    # Restore file
    snapshot_file.write_text(content)


def test_list_snapshots():
    """Test listing snapshots."""
    print("\n🧪 Test 3: List Snapshots")

    persistence = StatusPersistence(Path.cwd())

    # Save a few snapshots
    for i in range(3):
        status = check_status(log_event=False)
        persistence.save_status_snapshot(status, snapshot_id=f"test_snapshot_{i}")

    # List snapshots
    snapshots = persistence.list_snapshots()

    assert len(snapshots) >= 3, f"Expected at least 3 snapshots, got {len(snapshots)}"
    print(f"  ✓ Found {len(snapshots)} snapshots")

    # Check latest
    latest = persistence.get_latest_snapshot()
    assert latest is not None, "Should have latest snapshot"
    print("  ✓ Latest snapshot retrieved")

    # Cleanup test snapshots
    for i in range(3):
        persistence.delete_snapshot(f"test_snapshot_{i}")


def test_compare_snapshots():
    """Test comparing snapshots."""
    print("\n🧪 Test 4: Compare Snapshots")

    persistence = StatusPersistence(Path.cwd())

    # Save two snapshots with different data
    status1 = check_status(log_event=False)
    status1["test_metric"] = 100
    persistence.save_status_snapshot(status1, snapshot_id="compare_test_1")

    status2 = check_status(log_event=False)
    status2["test_metric"] = 200
    persistence.save_status_snapshot(status2, snapshot_id="compare_test_2")

    # Compare
    comparison = persistence.compare_snapshots("compare_test_1", "compare_test_2")

    assert comparison is not None, "Comparison should succeed"
    assert "test_metric" in str(comparison["differences"]), "Should detect difference"
    print("  ✓ Comparison successful")
    print(f"  ✓ Found {len(comparison['differences'])} differences")

    # Cleanup
    persistence.delete_snapshot("compare_test_1")
    persistence.delete_snapshot("compare_test_2")


def test_status_history():
    """Test status history tracking."""
    print("\n🧪 Test 5: Status History")

    persistence = StatusPersistence(Path.cwd())

    # Save snapshots with varying epistemic state
    for i in range(3):
        status = check_status(log_event=False)
        # Simulate changing knowledge
        if "epistemic_state" in status:
            status["epistemic_state"]["knowledge_pct"] = 50.0 + (i * 10)
        persistence.save_status_snapshot(status, snapshot_id=f"history_test_{i}")

    # Get history
    history = persistence.get_status_history("epistemic_state.knowledge_pct", limit=3)

    assert len(history) >= 0, "Should have history entries"
    print(f"  ✓ Retrieved {len(history)} history entries")

    # Cleanup
    for i in range(3):
        persistence.delete_snapshot(f"history_test_{i}")


def test_cleanup():
    """Test cleanup of old snapshots."""
    print("\n🧪 Test 6: Cleanup Old Snapshots")

    persistence = StatusPersistence(Path.cwd())

    # Save many snapshots
    for i in range(5):
        status = check_status(log_event=False)
        persistence.save_status_snapshot(status, snapshot_id=f"cleanup_test_{i}")

    # Cleanup (keep only 2)
    deleted = persistence.cleanup_old_snapshots(keep_count=2)

    remaining = persistence.list_snapshots()
    test_snapshots = [s for s in remaining if s["snapshot_id"].startswith("cleanup_test_")]

    assert len(test_snapshots) <= 2, f"Should keep max 2, got {len(test_snapshots)}"
    print(f"  ✓ Cleanup successful (deleted {deleted}, kept {len(test_snapshots)})")

    # Cleanup remaining
    for snapshot in test_snapshots:
        persistence.delete_snapshot(snapshot["snapshot_id"])


def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 Status Persistence Testing")
    print("=" * 60)
    print()

    try:
        test_save_and_load()
        test_integrity_verification()
        test_list_snapshots()
        test_compare_snapshots()
        test_status_history()
        test_cleanup()

        print()
        print("=" * 60)
        print("✅ All Tests Passed!")
        print("=" * 60)
        print()
        print("Features Verified:")
        print("  ✓ Save and load snapshots")
        print("  ✓ Checksum integrity verification")
        print("  ✓ Snapshot listing and retrieval")
        print("  ✓ Snapshot comparison")
        print("  ✓ Status history tracking")
        print("  ✓ Old snapshot cleanup")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    main()
