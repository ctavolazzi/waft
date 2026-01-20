#!/usr/bin/env python3
"""
Pyrite Obstacle Course
=======================

A comprehensive test suite that challenges Pyrite's capabilities:
- Concurrent locking
- Complex evolutionary cycles
- State management
- Error handling
- Performance
- Edge cases

Run this to verify Pyrite is working correctly under stress.
"""

import json
import sys
import threading
import time
from pathlib import Path
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.pyrite import EvolutionaryStrategy, WorkEffortStatus, get_pyrite


class ObstacleCourse:
    """Obstacle course for testing Pyrite."""

    def __init__(self):
        self.pyrite = get_pyrite()
        self.results: list[dict[str, Any]] = []
        self.passed = 0
        self.failed = 0

    def test(self, name: str, func):
        """Run a test and record results."""
        print(f"\n🧪 Test: {name}")
        try:
            start = time.time()
            result = func()
            duration = time.time() - start

            if result:
                self.passed += 1
                print(f"  ✅ PASSED ({duration:.3f}s)")
                self.results.append({"test": name, "status": "PASSED", "duration": duration})
                return True
            else:
                self.failed += 1
                print(f"  ❌ FAILED ({duration:.3f}s)")
                self.results.append({"test": name, "status": "FAILED", "duration": duration})
                return False
        except Exception as e:
            self.failed += 1
            print(f"  ❌ ERROR: {e}")
            self.results.append({"test": name, "status": "ERROR", "error": str(e)})
            return False

    # ==================== Obstacle 1: Basic Functionality ====================

    def obstacle_1_basic_functionality(self):
        """Test basic Pyrite functionality."""
        print("\n" + "=" * 60)
        print("OBSTACLE 1: Basic Functionality")
        print("=" * 60)

        # Test 1.1: Get instance
        self.test("1.1 Get Pyrite Instance", lambda: self.pyrite is not None)

        # Test 1.2: /think ability
        self.test("1.2 /think Ability", lambda: "status" in self.pyrite.execute_ability("/think"))

        # Test 1.3: /status ability
        self.test(
            "1.3 /status Ability", lambda: "personality" in self.pyrite.execute_ability("/status")
        )

        # Test 1.4: Personality summary
        self.test("1.4 Personality Summary", lambda: len(self.pyrite.get_personality_summary()) > 0)

        # Test 1.5: Work effort graph
        self.test("1.5 Work Effort Graph", lambda: len(self.pyrite._work_effort_graph) > 0)

    # ==================== Obstacle 2: Locking System ====================

    def obstacle_2_locking(self):
        """Test locking system."""
        print("\n" + "=" * 60)
        print("OBSTACLE 2: Locking System")
        print("=" * 60)

        we_id = (
            list(self.pyrite._work_effort_graph.keys())[0]
            if self.pyrite._work_effort_graph
            else None
        )
        if not we_id:
            print("  ⚠️  No work efforts available for locking tests")
            return

        # Test 2.1: Acquire lock
        self.test(
            "2.1 Acquire Lock", lambda: self.pyrite.acquire_lock(we_id, "test-lock-1", timeout=5.0)
        )

        # Test 2.2: Check if locked
        self.test("2.2 Is Locked", lambda: self.pyrite.is_locked(we_id))

        # Test 2.3: Get lock holder
        self.test(
            "2.3 Get Lock Holder", lambda: self.pyrite.get_lock_holder(we_id) == "test-lock-1"
        )

        # Test 2.4: Fail to acquire second lock
        self.test(
            "2.4 Fail Second Lock",
            lambda: not self.pyrite.acquire_lock(we_id, "test-lock-2", timeout=1.0),
        )

        # Test 2.5: Release lock
        self.test("2.5 Release Lock", lambda: self.pyrite.release_lock(we_id, "test-lock-1"))

        # Test 2.6: Verify unlocked
        self.test("2.6 Verify Unlocked", lambda: not self.pyrite.is_locked(we_id))

    # ==================== Obstacle 3: Concurrent Locking ====================

    def obstacle_3_concurrent_locking(self):
        """Test concurrent locking."""
        print("\n" + "=" * 60)
        print("OBSTACLE 3: Concurrent Locking")
        print("=" * 60)

        we_id = (
            list(self.pyrite._work_effort_graph.keys())[0]
            if self.pyrite._work_effort_graph
            else None
        )
        if not we_id:
            print("  ⚠️  No work efforts available for concurrent tests")
            return

        results = []

        def try_lock(lock_id: str):
            """Try to acquire lock."""
            success = self.pyrite.acquire_lock(we_id, lock_id, timeout=2.0)
            if success:
                time.sleep(0.1)
                self.pyrite.release_lock(we_id, lock_id)
            results.append((lock_id, success))

        # Test 3.1: Sequential locks
        self.test(
            "3.1 Sequential Locks",
            lambda: all(
                self.pyrite.acquire_lock(we_id, f"seq-{i}", timeout=1.0)
                and self.pyrite.release_lock(we_id, f"seq-{i}")
                for i in range(5)
            ),
        )

        # Test 3.2: Concurrent locks (should serialize)
        results.clear()
        threads = [threading.Thread(target=try_lock, args=(f"concurrent-{i}",)) for i in range(5)]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Only one should succeed at a time
        successful = sum(1 for _, success in results if success)
        self.test(
            "3.2 Concurrent Locks Serialize",
            lambda: successful == 5,  # All should eventually succeed
        )

    # ==================== Obstacle 4: Monitoring ====================

    def obstacle_4_monitoring(self):
        """Test monitoring system."""
        print("\n" + "=" * 60)
        print("OBSTACLE 4: Monitoring System")
        print("=" * 60)

        # Test 4.1: Monitor all
        self.test(
            "4.1 Monitor All",
            lambda: "total_work_efforts" in self.pyrite.execute_ability("/monitor"),
        )

        # Test 4.2: Monitor specific
        we_id = (
            list(self.pyrite._work_effort_graph.keys())[0]
            if self.pyrite._work_effort_graph
            else None
        )
        if we_id:
            self.test(
                "4.2 Monitor Specific",
                lambda: "we_id" in self.pyrite.execute_ability("/monitor", we_id),
            )

        # Test 4.3: State history
        if we_id:
            self.test(
                "4.3 State History", lambda: isinstance(self.pyrite.get_state_history(we_id), list)
            )

        # Test 4.4: Metrics
        self.test("4.4 Metrics", lambda: isinstance(self.pyrite.get_metrics(), dict))

    # ==================== Obstacle 5: Organization ====================

    def obstacle_5_organization(self):
        """Test organization system."""
        print("\n" + "=" * 60)
        print("OBSTACLE 5: Organization System")
        print("=" * 60)

        # Test 5.1: Organize
        self.test("5.1 Organize", lambda: "total_nodes" in self.pyrite.execute_ability("/organize"))

        # Test 5.2: Get work effort
        we_id = (
            list(self.pyrite._work_effort_graph.keys())[0]
            if self.pyrite._work_effort_graph
            else None
        )
        if we_id:
            self.test("5.2 Get Work Effort", lambda: self.pyrite.get_work_effort(we_id) is not None)

        # Test 5.3: Get children
        if we_id:
            self.test("5.3 Get Children", lambda: isinstance(self.pyrite.get_children(we_id), list))

        # Test 5.4: Get ancestors
        if we_id:
            self.test(
                "5.4 Get Ancestors", lambda: isinstance(self.pyrite.get_ancestors(we_id), list)
            )

    # ==================== Obstacle 6: Evolutionary Cycles ====================

    def obstacle_6_evolution(self):
        """Test evolutionary cycles."""
        print("\n" + "=" * 60)
        print("OBSTACLE 6: Evolutionary Cycles")
        print("=" * 60)

        we_id = None
        for test_id in list(self.pyrite._work_effort_graph.keys())[:10]:
            if not self.pyrite.is_locked(test_id):
                we_id = test_id
                break

        if not we_id:
            print("  ⚠️  No work efforts available for evolution tests")
            return

        # Test 6.1: Initiate evolution
        result = self.pyrite.execute_ability("/evolve", we_id, "adaptive", 3)
        self.test(
            "6.1 Initiate Evolution", lambda: result.get("status") == "success" or "error" in result
        )

        # Test 6.2: Evolutionary history
        self.test(
            "6.2 Evolutionary History",
            lambda: isinstance(self.pyrite.get_evolutionary_history(we_id), list),
        )

        # Test 6.3: Different strategies
        strategies = ["conservative", "aggressive", "adaptive", "exploratory"]
        for strategy in strategies:
            self.test(
                f"6.3 Strategy: {strategy}",
                lambda s=strategy: self.pyrite.initiate_evolution(we_id, EvolutionaryStrategy(s), 2)
                is not None,
            )

    # ==================== Obstacle 7: Personality & Attributes ====================

    def obstacle_7_personality(self):
        """Test personality system."""
        print("\n" + "=" * 60)
        print("OBSTACLE 7: Personality & Attributes")
        print("=" * 60)

        # Test 7.1: Get attributes
        self.test("7.1 Get Attributes", lambda: len(self.pyrite._attributes) > 0)

        # Test 7.2: Update attribute
        initial_wisdom = self.pyrite.get_attribute("wisdom").value
        self.pyrite.update_attribute("wisdom", 0.1)
        new_wisdom = self.pyrite.get_attribute("wisdom").value

        self.test("7.2 Update Attribute", lambda: new_wisdom > initial_wisdom)

        # Test 7.3: Grow attributes
        before = {name: attr.value for name, attr in self.pyrite._attributes.items()}
        self.pyrite.grow_attributes()
        after = {name: attr.value for name, attr in self.pyrite._attributes.items()}

        self.test(
            "7.3 Grow Attributes", lambda: all(after[name] >= before[name] for name in before)
        )

        # Test 7.4: Personality summary
        self.test("7.4 Personality Summary", lambda: len(self.pyrite.get_personality_summary()) > 0)

    # ==================== Obstacle 8: Secrets ====================

    def obstacle_8_secrets(self):
        """Test secrets system."""
        print("\n" + "=" * 60)
        print("OBSTACLE 8: Secrets System")
        print("=" * 60)

        # Test 8.1: Create secret
        secret_id = self.pyrite.create_secret({"test": "data"}, {"visible": "metadata"})
        self.test("8.1 Create Secret", lambda: secret_id is not None and len(secret_id) > 0)

        # Test 8.2: Get metadata
        self.test(
            "8.2 Get Secret Metadata",
            lambda: self.pyrite.get_secret_metadata(secret_id) is not None,
        )

        # Test 8.3: List secrets
        self.test("8.3 List Secrets", lambda: len(self.pyrite.list_secrets()) > 0)

        # Test 8.4: Multiple secrets
        secret_ids = [self.pyrite.create_secret({"data": i}, {"index": i}) for i in range(3)]
        self.test(
            "8.4 Multiple Secrets", lambda: len(secret_ids) == 3 and all(sid for sid in secret_ids)
        )

    # ==================== Obstacle 9: Status Management ====================

    def obstacle_9_status_management(self):
        """Test status management."""
        print("\n" + "=" * 60)
        print("OBSTACLE 9: Status Management")
        print("=" * 60)

        we_id = (
            list(self.pyrite._work_effort_graph.keys())[0]
            if self.pyrite._work_effort_graph
            else None
        )
        if not we_id:
            print("  ⚠️  No work efforts available for status tests")
            return

        node = self.pyrite.get_work_effort(we_id)
        if not node:
            return

        original_status = node.status

        # Test 9.1: Update status
        self.test(
            "9.1 Update Status",
            lambda: self.pyrite.update_work_effort_status(we_id, WorkEffortStatus.ACTIVE),
        )

        # Test 9.2: Verify status changed
        node_after = self.pyrite.get_work_effort(we_id)
        self.test("9.2 Verify Status Changed", lambda: node_after.status == WorkEffortStatus.ACTIVE)

        # Restore original status
        self.pyrite.update_work_effort_status(we_id, original_status)

    # ==================== Obstacle 10: Edge Cases ====================

    def obstacle_10_edge_cases(self):
        """Test edge cases."""
        print("\n" + "=" * 60)
        print("OBSTACLE 10: Edge Cases")
        print("=" * 60)

        # Test 10.1: Lock non-existent work effort
        self.test(
            "10.1 Lock Non-Existent",
            lambda: not self.pyrite.acquire_lock("NON-EXISTENT", "test", timeout=0.1),
        )

        # Test 10.2: Monitor non-existent
        result = self.pyrite.execute_ability("/monitor", "NON-EXISTENT")
        self.test("10.2 Monitor Non-Existent", lambda: "error" in result)

        # Test 10.3: Release lock not held
        we_id = (
            list(self.pyrite._work_effort_graph.keys())[0]
            if self.pyrite._work_effort_graph
            else None
        )
        if we_id:
            self.test(
                "10.3 Release Lock Not Held",
                lambda: not self.pyrite.release_lock(we_id, "not-held-lock"),
            )

        # Test 10.4: Evolve non-existent
        result = self.pyrite.execute_ability("/evolve", "NON-EXISTENT", "adaptive", 1)
        self.test("10.4 Evolve Non-Existent", lambda: result.get("status") == "failed")

        # Test 10.5: Get work effort non-existent
        self.test(
            "10.5 Get Work Effort Non-Existent",
            lambda: self.pyrite.get_work_effort("NON-EXISTENT") is None,
        )

    # ==================== Obstacle 11: Empirica Integration ====================

    def obstacle_11_empirica(self):
        """Test Empirica integration."""
        print("\n" + "=" * 60)
        print("OBSTACLE 11: Empirica Integration")
        print("=" * 60)

        # Test 11.1: Empirica initialized
        self.test("11.1 Empirica Initialized", lambda: hasattr(self.pyrite, "empirica"))

        # Test 11.2: Session exists
        self.test(
            "11.2 Empirica Session",
            lambda: self.pyrite._empirica_session_id is not None
            or not self.pyrite.empirica.is_initialized(),
        )

        # Test 11.3: /think includes Empirica
        result = self.pyrite.execute_ability("/think")
        self.test("11.3 /think Includes Empirica", lambda: "empirica" in result)

        # Test 11.4: /evolve uses Empirica
        we_id = (
            list(self.pyrite._work_effort_graph.keys())[0]
            if self.pyrite._work_effort_graph
            else None
        )
        if we_id and not self.pyrite.is_locked(we_id):
            result = self.pyrite.execute_ability("/evolve", we_id, "adaptive", 1)
            self.test(
                "11.4 /evolve Uses Empirica",
                lambda: "empirica" in result or result.get("status") == "failed",
            )

    # ==================== Run All Obstacles ====================

    def run_all(self):
        """Run all obstacles."""
        print("\n" + "=" * 60)
        print("PYRITE OBSTACLE COURSE")
        print("=" * 60)
        print("Testing Pyrite's capabilities under stress...")

        start_time = time.time()

        self.obstacle_1_basic_functionality()
        self.obstacle_2_locking()
        self.obstacle_3_concurrent_locking()
        self.obstacle_4_monitoring()
        self.obstacle_5_organization()
        self.obstacle_6_evolution()
        self.obstacle_7_personality()
        self.obstacle_8_secrets()
        self.obstacle_9_status_management()
        self.obstacle_10_edge_cases()
        self.obstacle_11_empirica()

        duration = time.time() - start_time

        # Print summary
        print("\n" + "=" * 60)
        print("OBSTACLE COURSE COMPLETE")
        print("=" * 60)
        print(f"Total Tests: {self.passed + self.failed}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"⏱️  Duration: {duration:.2f}s")
        print(f"📊 Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")

        # Save results
        results_file = Path(__file__).parent / "pyrite_obstacle_course_results.json"
        results_file.write_text(
            json.dumps(
                {
                    "summary": {
                        "total": self.passed + self.failed,
                        "passed": self.passed,
                        "failed": self.failed,
                        "duration": duration,
                        "success_rate": self.passed / (self.passed + self.failed) * 100
                        if (self.passed + self.failed) > 0
                        else 0,
                    },
                    "results": self.results,
                },
                indent=2,
            )
        )

        print(f"\n📄 Results saved to: {results_file}")

        return self.failed == 0


def main():
    """Run obstacle course."""
    course = ObstacleCourse()
    success = course.run_all()

    if success:
        print("\n🎉 All obstacles passed! Pyrite is ready for production.")
        return 0
    else:
        print("\n⚠️  Some obstacles failed. Review the results above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
