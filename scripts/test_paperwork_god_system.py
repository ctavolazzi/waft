#!/usr/bin/env python3
"""
Test Paperwork God System
==========================

Comprehensive test of the Paperwork God, Skurl (demi-god of red tape),
and the Realm of Bureaucracy with Goblins and Ghouls.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.pantheon import PaperworkGod


def test_paperwork_god():
    """Test Paperwork God functionality."""
    print("📄 Testing Paperwork God...")
    print("-" * 60)

    # Initialize
    paperwork_god = PaperworkGod()
    assert paperwork_god is not None, "PaperworkGod should initialize"
    print("  ✅ PaperworkGod initialized")

    # Test registry
    registry = paperwork_god._load_registry()
    assert "records" in registry, "Registry should have records"
    assert "demi_gods" in registry, "Registry should list demi-gods"
    assert "Skurl" in registry["demi_gods"], "Skurl should be listed as demi-god"
    print("  ✅ Registry structure correct")

    # Test registering paperwork
    test_doc = paperwork_god.register_paperwork(
        document_id="test_doc_001",
        document_path=Path("test_forms/test_form.pdf"),
        document_type="form",
        metadata={"test": True},
    )
    assert test_doc.document_id == "test_doc_001", "Document ID should match"
    assert test_doc.document_type == "form", "Document type should match"
    print(f"  ✅ Registered paperwork: {test_doc.document_id}")

    # Test retrieving paperwork
    retrieved = paperwork_god.get_paperwork_record("test_doc_001")
    assert retrieved is not None, "Should retrieve paperwork"
    assert retrieved.document_id == "test_doc_001", "Retrieved ID should match"
    print("  ✅ Retrieved paperwork record")

    # Test listing all paperwork
    all_paperwork = paperwork_god.list_all_paperwork()
    assert len(all_paperwork) > 0, "Should have at least one record"
    print(f"  ✅ Listed all paperwork: {len(all_paperwork)} records")

    # Test summary
    summary = paperwork_god.get_registry_summary()
    assert "total_documents" in summary, "Summary should have total_documents"
    assert "demi_gods" in summary, "Summary should list demi-gods"
    assert "realm_creatures" in summary, "Summary should include realm creatures"
    print(f"  ✅ Registry summary: {summary['total_documents']} documents")

    print("  ✅ Paperwork God tests passed!\n")
    return paperwork_god


def test_skurl(paperwork_god):
    """Test Skurl (demi-god of red tape) functionality."""
    print("👹 Testing Skurl (Demi-God of Red Tape)...")
    print("-" * 60)

    # Get Skurl
    skurl = paperwork_god.skurl
    assert skurl is not None, "Skurl should be accessible"
    assert skurl.parent_god is not None, "Skurl should have parent god"
    print("  ✅ Skurl accessible from PaperworkGod")

    # Test registry
    registry = skurl._load_registry()
    assert "obstacles" in registry, "Registry should have obstacles"
    assert registry["demi_god"] == "Skurl", "Registry should identify as Skurl"
    assert registry["type"] == "gremlin", "Skurl should be a gremlin"
    assert registry["domain"] == "red_tape", "Skurl's domain should be red_tape"
    assert registry["parent_god"] == "PaperworkGod", "Parent god should be PaperworkGod"
    print("  ✅ Skurl registry structure correct")

    # Test creating red tape obstacle
    obstacle = skurl.create_red_tape_obstacle(
        obstacle_id="test_obstacle_001",
        description="Test obstacle requiring multiple forms",
        required_forms=["form_A", "form_B", "form_C"],
        required_approvals=["manager", "director"],
        complexity_level=7,
        metadata={"test": True},
    )
    assert obstacle.obstacle_id == "test_obstacle_001", "Obstacle ID should match"
    assert obstacle.complexity_level == 7, "Complexity should match"
    assert len(obstacle.required_forms) == 3, "Should have 3 required forms"
    assert len(obstacle.required_approvals) == 2, "Should have 2 required approvals"
    assert not obstacle.is_resolved, "New obstacle should be unresolved"
    print(f"  ✅ Created red tape obstacle: {obstacle.obstacle_id}")
    print(f"     Complexity: {obstacle.complexity_level}/10")
    print(f"     Required Forms: {len(obstacle.required_forms)}")
    print(f"     Required Approvals: {len(obstacle.required_approvals)}")

    # Test retrieving obstacle
    retrieved = skurl.get_obstacle("test_obstacle_001")
    assert retrieved is not None, "Should retrieve obstacle"
    assert retrieved.obstacle_id == "test_obstacle_001", "Retrieved ID should match"
    print("  ✅ Retrieved obstacle")

    # Test listing all obstacles
    all_obstacles = skurl.list_all_obstacles()
    assert len(all_obstacles) > 0, "Should have at least one obstacle"
    print(f"  ✅ Listed all obstacles: {len(all_obstacles)} total")

    # Test listing unresolved obstacles
    unresolved = skurl.list_all_obstacles(unresolved_only=True)
    assert len(unresolved) > 0, "Should have unresolved obstacles"
    assert all(not o.is_resolved for o in unresolved), "All should be unresolved"
    print(f"  ✅ Listed unresolved obstacles: {len(unresolved)}")

    # Test resolving obstacle
    resolved = skurl.resolve_obstacle("test_obstacle_001")
    assert resolved is not None, "Should resolve obstacle"
    assert resolved.is_resolved, "Obstacle should be resolved"
    assert resolved.resolved_at is not None, "Should have resolution timestamp"
    print("  ✅ Resolved obstacle")

    # Verify unresolved count decreased
    unresolved_after = skurl.list_all_obstacles(unresolved_only=True)
    assert len(unresolved_after) < len(unresolved), "Unresolved count should decrease"
    print(f"  ✅ Unresolved count decreased: {len(unresolved_after)} remaining")

    # Test summary
    summary = skurl.get_registry_summary()
    assert "total_obstacles" in summary, "Summary should have total_obstacles"
    assert "unresolved_obstacles" in summary, "Summary should have unresolved count"
    assert "resolved_obstacles" in summary, "Summary should have resolved count"
    assert summary["demi_god_type"] == "gremlin", "Should be gremlin type"
    assert summary["domain"] == "red_tape", "Domain should be red_tape"
    assert summary["parent_god"] == "PaperworkGod", "Parent should be PaperworkGod"
    print(f"  ✅ Skurl summary: {summary['total_obstacles']} obstacles")
    print(f"     Unresolved: {summary['unresolved_obstacles']}")
    print(f"     Resolved: {summary['resolved_obstacles']}")

    print("  ✅ Skurl tests passed!\n")
    return skurl


def test_realm_creatures(paperwork_god):
    """Test Realm of Bureaucracy creatures (Goblins and Ghouls)."""
    print("👹🧟 Testing Realm of Bureaucracy Creatures...")
    print("-" * 60)

    realm = paperwork_god.realm
    assert realm is not None, "Realm should be accessible"
    print("  ✅ Realm accessible from PaperworkGod")

    # Test creature summary
    summary = realm.get_creatures_summary()
    assert "goblins" in summary, "Summary should have goblins count"
    assert "ghouls" in summary, "Summary should have ghouls count"
    assert "total_creatures" in summary, "Summary should have total count"
    print(f"  ✅ Creature summary: {summary['goblins']} Goblins, {summary['ghouls']} Ghouls")
    print(f"     Total: {summary['total_creatures']} creatures")

    # Test creating new goblin
    new_goblin = realm.create_goblin(
        goblin_id="test_goblin_001",
        name="TestGoblin",
        role="test_assistant",
        metadata={"test": True},
    )
    assert new_goblin["goblin_id"] == "test_goblin_001", "Goblin ID should match"
    assert new_goblin["name"] == "TestGoblin", "Goblin name should match"
    assert new_goblin["type"] == "goblin", "Type should be goblin"
    print(f"  ✅ Created Goblin: {new_goblin['name']} ({new_goblin['role']})")

    # Verify goblin file exists
    goblin_file = realm.realm_path / "creatures" / "goblins" / "test_goblin_001.json"
    assert goblin_file.exists(), "Goblin file should exist"
    print("  ✅ Goblin file created")

    # Test creating new ghoul
    new_ghoul = realm.create_ghoul(
        ghoul_id="test_ghoul_001", name="TestGhoul", role="test_guardian", metadata={"test": True}
    )
    assert new_ghoul["ghoul_id"] == "test_ghoul_001", "Ghoul ID should match"
    assert new_ghoul["name"] == "TestGhoul", "Ghoul name should match"
    assert new_ghoul["type"] == "ghoul", "Type should be ghoul"
    print(f"  ✅ Created Ghoul: {new_ghoul['name']} ({new_ghoul['role']})")

    # Verify ghoul file exists
    ghoul_file = realm.realm_path / "creatures" / "ghouls" / "test_ghoul_001.json"
    assert ghoul_file.exists(), "Ghoul file should exist"
    print("  ✅ Ghoul file created")

    # Test updated summary
    updated_summary = realm.get_creatures_summary()
    assert updated_summary["goblins"] > summary["goblins"], "Goblin count should increase"
    assert updated_summary["ghouls"] > summary["ghouls"], "Ghoul count should increase"
    print(
        f"  ✅ Updated summary: {updated_summary['goblins']} Goblins, {updated_summary['ghouls']} Ghouls"
    )

    print("  ✅ Realm creatures tests passed!\n")
    return realm


def test_integration():
    """Test integration between all components."""
    print("🔗 Testing System Integration...")
    print("-" * 60)

    # Initialize Paperwork God
    paperwork_god = PaperworkGod()

    # Test that Skurl is automatically created
    assert paperwork_god.skurl is not None, "Skurl should be auto-created"
    print("  ✅ Skurl auto-created with PaperworkGod")

    # Test that realm is accessible
    assert paperwork_god.realm is not None, "Realm should be accessible"
    print("  ✅ Realm accessible from PaperworkGod")

    # Test that realm has creatures
    creatures = paperwork_god.realm.get_creatures_summary()
    assert creatures["total_creatures"] > 0, "Realm should have creatures"
    print(f"  ✅ Realm has {creatures['total_creatures']} creatures")

    # Test full workflow: paperwork -> red tape -> resolution
    doc = paperwork_god.register_paperwork(
        document_id="integration_test_001",
        document_path=Path("test/integration_form.pdf"),
        document_type="form",
    )
    print(f"  ✅ Created paperwork: {doc.document_id}")

    obstacle = paperwork_god.skurl.create_red_tape_obstacle(
        obstacle_id="integration_obstacle_001",
        description="Integration test obstacle",
        required_forms=[doc.document_id],
        required_approvals=["manager"],
        complexity_level=3,
    )
    print(f"  ✅ Created obstacle for paperwork: {obstacle.obstacle_id}")

    # Resolve obstacle
    resolved = paperwork_god.skurl.resolve_obstacle(obstacle.obstacle_id)
    assert resolved.is_resolved, "Obstacle should be resolved"
    print("  ✅ Resolved obstacle in workflow")

    # Test summary includes all components
    summary = paperwork_god.get_registry_summary()
    assert summary["total_documents"] > 0, "Should have documents"
    assert "Skurl" in summary["demi_gods"], "Should list Skurl"
    assert summary["realm_creatures"]["total_creatures"] > 0, "Should have creatures"
    print("  ✅ Full system integration working")

    print("  ✅ Integration tests passed!\n")


def main():
    """Run all tests."""
    print("🏛️ PAPERWORK GOD SYSTEM TEST SUITE")
    print("=" * 60)
    print()

    try:
        # Test Paperwork God
        paperwork_god = test_paperwork_god()

        # Test Skurl
        skurl = test_skurl(paperwork_god)

        # Test Realm Creatures
        realm = test_realm_creatures(paperwork_god)

        # Test Integration
        test_integration()

        print("=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print()
        print("System Status:")
        print("  ✅ Paperwork God: Operational")
        print("  ✅ Skurl (Demi-God): Operational")
        print("  ✅ Realm of Bureaucracy: Operational")
        print(f"  ✅ Goblins: {realm.get_creatures_summary()['goblins']}")
        print(f"  ✅ Ghouls: {realm.get_creatures_summary()['ghouls']}")
        print()

        return 0

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback

        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
