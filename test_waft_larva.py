"""
Test script for waft_larva.py
Tests database persistence, error handling, and artifact transitions.

Note: Requires dependencies to be installed:
    pip install streamlit pandas pyserial
"""

import os
import sqlite3
import sys

# Try to import, but provide helpful error if dependencies missing
try:
    from waft_larva import DB_NAME, Severity, WaftEntity
except ImportError as e:
    print("ERROR: Missing dependencies. Please install:")
    print("  pip install streamlit pandas pyserial")
    print(f"\nOriginal error: {e}")
    sys.exit(1)


def test_database_initialization():
    """Test that database initializes with correct schema and seed data."""
    print("Testing database initialization...")

    # Remove existing database if it exists
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

    # Create entity (should initialize database)
    entity = WaftEntity()

    # Verify tables exist
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Check chronicle table
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chronicle'")
    assert c.fetchone() is not None, "Chronicle table should exist"

    # Check artifacts table
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='artifacts'")
    assert c.fetchone() is not None, "Artifacts table should exist"

    # Check seed data
    c.execute("SELECT COUNT(*) FROM artifacts")
    count = c.fetchone()[0]
    assert count > 0, "Seed data should be created"

    # Check seed artifact name
    c.execute("SELECT name FROM artifacts WHERE name = 'Right_Index_Phalanx'")
    assert c.fetchone() is not None, "Seed artifact should exist"

    conn.close()
    print("✅ Database initialization: PASSED")


def test_chronicle_logging():
    """Test that chronicle logs entries correctly."""
    print("\nTesting chronicle logging...")

    entity = WaftEntity()

    # Log different severity levels
    entity.chronicle(Severity.THOUGHT, "Test thought message")
    entity.chronicle(Severity.STRAIN, "Test strain message")
    entity.chronicle(Severity.TRAUMA, "Test trauma message", "Test context")

    # Verify entries
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM chronicle WHERE severity = 'THOUGHT'")
    assert c.fetchone()[0] > 0, "THOUGHT entries should exist"

    c.execute("SELECT COUNT(*) FROM chronicle WHERE severity = 'STRAIN'")
    assert c.fetchone()[0] > 0, "STRAIN entries should exist"

    c.execute("SELECT COUNT(*) FROM chronicle WHERE severity = 'TRAUMA'")
    assert c.fetchone()[0] > 0, "TRAUMA entries should exist"

    conn.close()
    print("✅ Chronicle logging: PASSED")


def test_safe_breath_error_handling():
    """Test that safe_breath catches errors and logs TRAUMA."""
    print("\nTesting safe_breath error handling...")

    entity = WaftEntity()

    # Count initial TRAUMA entries
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM chronicle WHERE severity = 'TRAUMA'")
    initial_trauma_count = c.fetchone()[0]
    conn.close()

    # Trigger an error
    def failing_function():
        raise ValueError("Test error")

    result = entity.safe_breath(failing_function)

    # Verify error was caught
    assert result["success"] == False, "safe_breath should return success=False on error"
    assert "error" in result, "Result should contain error field"

    # Verify TRAUMA was logged
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM chronicle WHERE severity = 'TRAUMA'")
    new_trauma_count = c.fetchone()[0]
    conn.close()

    assert new_trauma_count > initial_trauma_count, "TRAUMA should be logged on error"
    print("✅ Error handling: PASSED")


def test_artifact_status_transitions():
    """Test artifact status transitions (VOID → PHYSICAL)."""
    print("\nTesting artifact status transitions...")

    entity = WaftEntity()

    # Get initial artifact
    artifact = entity.get_next_manifestation()
    assert artifact is not None, "Should have at least one artifact"

    artifact_id, name, gcode, status, birth_time = artifact
    assert status == "VOID", "Initial status should be VOID"

    # Confirm birth
    entity.confirm_birth(artifact_id)

    # Verify status changed
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT status, birth_time FROM artifacts WHERE id = ?", (artifact_id,))
    row = c.fetchone()
    assert row[0] == "PHYSICAL", "Status should be PHYSICAL after confirm_birth"
    assert row[1] is not None, "birth_time should be set"
    conn.close()

    # Verify it's no longer in get_next_manifestation
    next_artifact = entity.get_next_manifestation()
    if next_artifact is None:
        print("  (All artifacts are now PHYSICAL)")
    else:
        assert next_artifact[0] != artifact_id, "Confirmed artifact should not be returned"

    print("✅ Artifact transitions: PASSED")


def test_database_persistence():
    """Test that database persists across entity instances."""
    print("\nTesting database persistence...")

    # Create first entity and log something
    entity1 = WaftEntity()
    entity1.chronicle(Severity.THOUGHT, "Persistence test message")

    # Count entries
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM chronicle")
    count1 = c.fetchone()[0]
    conn.close()

    # Create new entity instance
    entity2 = WaftEntity()

    # Count entries again
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM chronicle")
    count2 = c.fetchone()[0]
    conn.close()

    assert count2 >= count1, "Database should persist across instances"

    # Verify the message exists
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM chronicle WHERE message = 'Persistence test message'")
    assert c.fetchone()[0] > 0, "Previous entries should persist"
    conn.close()

    print("✅ Database persistence: PASSED")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("WAFT LARVA TEST SUITE")
    print("=" * 60)

    try:
        test_database_initialization()
        test_chronicle_logging()
        test_safe_breath_error_handling()
        test_artifact_status_transitions()
        test_database_persistence()

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
