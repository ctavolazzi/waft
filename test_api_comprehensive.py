#!/usr/bin/env python3
"""
Comprehensive API stress test - "Prove it even harder"
Tests edge cases, error scenarios, validation, and performance.
"""

import shutil
import sys
import tempfile
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fastapi.testclient import TestClient

from waft.api.auth import get_or_create_token
from waft.api.main import create_app


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_test(name, passed=True):
    """Print test result."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"  {status}: {name}")


def test_comprehensive():
    """Comprehensive API stress test."""
    print_section("🔥 COMPREHENSIVE API STRESS TEST")
    print("Testing edge cases, validation, error handling, and performance\n")

    temp_dir = tempfile.mkdtemp()
    project_path = Path(temp_dir)
    (project_path / "_work_efforts").mkdir(exist_ok=True)

    passed = 0
    failed = 0

    try:
        app = create_app(project_path)
        client = TestClient(app)
        token = get_or_create_token(project_path)
        headers = {"Authorization": f"Bearer {token}"}

        # ===================================================================
        # SECTION 1: VALIDATION TESTS
        # ===================================================================
        print_section("1. VALIDATION TESTS")

        # Test 1.1: Title too long
        try:
            response = client.post(
                "/api/projects",
                json={"title": "x" * 201},  # Exceeds max length
                headers=headers,
            )
            if response.status_code == 422:
                print_test("Title max length validation (201 chars)", True)
                passed += 1
            else:
                print_test("Title max length validation", False)
                failed += 1
        except Exception as e:
            print_test(f"Title validation error: {e}", False)
            failed += 1

        # Test 1.2: Empty title
        try:
            response = client.post("/api/projects", json={"title": ""}, headers=headers)
            if response.status_code == 422:
                print_test("Empty title validation", True)
                passed += 1
            else:
                print_test("Empty title validation", False)
                failed += 1
        except Exception as e:
            print_test(f"Empty title error: {e}", False)
            failed += 1

        # Test 1.3: Too many tags
        try:
            response = client.post(
                "/api/projects",
                json={
                    "title": "Test",
                    "tags": [f"tag{i}" for i in range(21)],  # Exceeds max
                },
                headers=headers,
            )
            if response.status_code == 422:
                print_test("Max tags validation (21 tags)", True)
                passed += 1
            else:
                print_test("Max tags validation", False)
                failed += 1
        except Exception as e:
            print_test(f"Tags validation error: {e}", False)
            failed += 1

        # Test 1.4: Invalid status
        try:
            response = client.post(
                "/api/projects", json={"title": "Test", "status": "invalid_status"}, headers=headers
            )
            if response.status_code == 422:
                print_test("Invalid status validation", True)
                passed += 1
            else:
                print_test("Invalid status validation", False)
                failed += 1
        except Exception as e:
            print_test(f"Status validation error: {e}", False)
            failed += 1

        # Test 1.5: Invalid work effort ID format
        try:
            response = client.get("/api/work-efforts/INVALID-ID")
            if response.status_code == 404:
                print_test("Invalid work effort ID format", True)
                passed += 1
            else:
                print_test("Invalid work effort ID format", False)
                failed += 1
        except Exception as e:
            print_test(f"Invalid ID error: {e}", False)
            failed += 1

        # ===================================================================
        # SECTION 2: AUTHENTICATION TESTS
        # ===================================================================
        print_section("2. AUTHENTICATION TESTS")

        # Test 2.1: Missing token
        try:
            response = client.post("/api/projects", json={"title": "Test"})
            if response.status_code == 401:
                print_test("Missing token rejection", True)
                passed += 1
            else:
                print_test("Missing token rejection", False)
                failed += 1
        except Exception as e:
            print_test(f"Missing token error: {e}", False)
            failed += 1

        # Test 2.2: Invalid token
        try:
            response = client.post(
                "/api/projects",
                json={"title": "Test"},
                headers={"Authorization": "Bearer invalid_token_12345"},
            )
            if response.status_code == 401:
                print_test("Invalid token rejection", True)
                passed += 1
            else:
                print_test("Invalid token rejection", False)
                failed += 1
        except Exception as e:
            print_test(f"Invalid token error: {e}", False)
            failed += 1

        # Test 2.3: Malformed auth header
        try:
            response = client.post(
                "/api/projects",
                json={"title": "Test"},
                headers={"Authorization": "InvalidFormat token"},
            )
            if response.status_code == 401:
                print_test("Malformed auth header rejection", True)
                passed += 1
            else:
                print_test("Malformed auth header rejection", False)
                failed += 1
        except Exception as e:
            print_test(f"Malformed header error: {e}", False)
            failed += 1

        # Test 2.4: GET endpoints don't require auth
        try:
            response = client.get("/api/projects")
            if response.status_code == 200:
                print_test("GET endpoints public (no auth required)", True)
                passed += 1
            else:
                print_test("GET endpoints public", False)
                failed += 1
        except Exception as e:
            print_test(f"Public GET error: {e}", False)
            failed += 1

        # ===================================================================
        # SECTION 3: ERROR HANDLING TESTS
        # ===================================================================
        print_section("3. ERROR HANDLING TESTS")

        # Test 3.1: 404 Not Found
        try:
            response = client.get("/api/projects/nonexistent_project_id")
            if response.status_code == 404:
                error_data = response.json()
                if "error" in error_data and "message" in error_data:
                    print_test("404 error response format", True)
                    passed += 1
                else:
                    print_test("404 error response format", False)
                    failed += 1
            else:
                print_test("404 Not Found", False)
                failed += 1
        except Exception as e:
            print_test(f"404 error: {e}", False)
            failed += 1

        # Test 3.2: 422 Validation Error format
        try:
            response = client.post(
                "/api/projects",
                json={"title": ""},  # Invalid
                headers=headers,
            )
            if response.status_code == 422:
                error_data = response.json()
                if "error" in error_data and error_data["error"] == "VALIDATION_ERROR":
                    print_test("422 validation error format", True)
                    passed += 1
                else:
                    print_test("422 validation error format", False)
                    failed += 1
            else:
                print_test("422 Validation Error", False)
                failed += 1
        except Exception as e:
            print_test(f"422 error: {e}", False)
            failed += 1

        # Test 3.3: Error response has timestamp
        try:
            response = client.get("/api/projects/nonexistent")
            error_data = response.json()
            if "timestamp" in error_data:
                print_test("Error response includes timestamp", True)
                passed += 1
            else:
                print_test("Error response includes timestamp", False)
                failed += 1
        except Exception as e:
            print_test(f"Timestamp check error: {e}", False)
            failed += 1

        # ===================================================================
        # SECTION 4: CRUD OPERATIONS - EDGE CASES
        # ===================================================================
        print_section("4. CRUD OPERATIONS - EDGE CASES")

        # Test 4.1: Create project with minimal data
        try:
            response = client.post("/api/projects", json={"title": "Minimal"}, headers=headers)
            if response.status_code == 201:
                project_id = response.json()["project_id"]
                print_test("Create with minimal data", True)
                passed += 1
            else:
                print_test("Create with minimal data", False)
                failed += 1
                project_id = None
        except Exception as e:
            print_test(f"Minimal create error: {e}", False)
            failed += 1
            project_id = None

        # Test 4.2: Create project with maximum data
        if project_id:
            try:
                response = client.post(
                    "/api/projects",
                    json={
                        "title": "x" * 200,  # Max length
                        "description": "x" * 10000,  # Max length
                        "tags": [f"tag{i}" for i in range(20)],  # Max tags
                        "status": "planning",
                    },
                    headers=headers,
                )
                if response.status_code == 201:
                    print_test("Create with maximum data", True)
                    passed += 1
                else:
                    print_test("Create with maximum data", False)
                    failed += 1
            except Exception as e:
                print_test(f"Max data create error: {e}", False)
                failed += 1

        # Test 4.3: PATCH with no fields (should work)
        if project_id:
            try:
                response = client.patch(f"/api/projects/{project_id}", json={}, headers=headers)
                if response.status_code == 200:
                    print_test("PATCH with empty body", True)
                    passed += 1
                else:
                    print_test("PATCH with empty body", False)
                    failed += 1
            except Exception as e:
                print_test(f"Empty PATCH error: {e}", False)
                failed += 1

        # Test 4.4: Update non-existent project
        try:
            response = client.put(
                "/api/projects/nonexistent", json={"title": "Updated"}, headers=headers
            )
            if response.status_code == 404:
                print_test("Update non-existent project", True)
                passed += 1
            else:
                print_test("Update non-existent project", False)
                failed += 1
        except Exception as e:
            print_test(f"Update non-existent error: {e}", False)
            failed += 1

        # Test 4.5: Delete non-existent project
        try:
            response = client.delete("/api/projects/nonexistent", headers=headers)
            if response.status_code == 404:
                print_test("Delete non-existent project", True)
                passed += 1
            else:
                print_test("Delete non-existent project", False)
                failed += 1
        except Exception as e:
            print_test(f"Delete non-existent error: {e}", False)
            failed += 1

        # ===================================================================
        # SECTION 5: WORK EFFORTS - EDGE CASES
        # ===================================================================
        print_section("5. WORK EFFORTS - EDGE CASES")

        # Test 5.1: Create work effort with special characters in title
        try:
            response = client.post(
                "/api/work-efforts",
                json={
                    "title": "Test! @#$%^&*() Work Effort - Special Chars",
                    "description": "Testing slug generation",
                },
                headers=headers,
            )
            if response.status_code == 201:
                we_id = response.json()["id"]
                print_test("Create WE with special chars (slug generation)", True)
                passed += 1
            else:
                print_test("Create WE with special chars", False)
                failed += 1
                we_id = None
        except Exception as e:
            print_test(f"Special chars error: {e}", False)
            failed += 1
            we_id = None

        # Test 5.2: Verify work effort ID format
        if we_id:
            try:
                import re

                pattern = r"^WE-\d{6}-[a-z0-9]{4}$"
                if re.match(pattern, we_id):
                    print_test("Work effort ID format correct", True)
                    passed += 1
                else:
                    print_test(f"Work effort ID format: {we_id}", False)
                    failed += 1
            except Exception as e:
                print_test(f"ID format check error: {e}", False)
                failed += 1

        # Test 5.3: List with pagination
        try:
            # Create multiple work efforts
            for i in range(5):
                client.post("/api/work-efforts", json={"title": f"Test WE {i}"}, headers=headers)

            # Test pagination
            response = client.get("/api/work-efforts?limit=2&offset=0")
            if response.status_code == 200:
                data = response.json()
                if "items" in data and "total" in data and "has_more" in data:
                    if len(data["items"]) <= 2:
                        print_test("Pagination limit works", True)
                        passed += 1
                    else:
                        print_test("Pagination limit", False)
                        failed += 1
                else:
                    print_test("Pagination response format", False)
                    failed += 1
            else:
                print_test("Pagination endpoint", False)
                failed += 1
        except Exception as e:
            print_test(f"Pagination error: {e}", False)
            failed += 1

        # Test 5.4: Filter by status
        try:
            response = client.get("/api/work-efforts?status=active")
            if response.status_code == 200:
                data = response.json()
                if all(we.get("status") == "active" for we in data.get("items", [])):
                    print_test("Filter by status", True)
                    passed += 1
                else:
                    print_test("Filter by status", False)
                    failed += 1
            else:
                print_test("Filter by status endpoint", False)
                failed += 1
        except Exception as e:
            print_test(f"Status filter error: {e}", False)
            failed += 1

        # ===================================================================
        # SECTION 6: WORK EFFORT LINKING
        # ===================================================================
        print_section("6. WORK EFFORT LINKING")

        # Create project and work effort for linking tests
        try:
            proj_response = client.post(
                "/api/projects", json={"title": "Linking Test Project"}, headers=headers
            )
            link_project_id = proj_response.json()["project_id"]

            we_response = client.post(
                "/api/work-efforts", json={"title": "Linking Test WE"}, headers=headers
            )
            link_we_id = we_response.json()["id"]

            # Test 6.1: Link work effort
            try:
                response = client.post(
                    f"/api/projects/{link_project_id}/work-efforts/{link_we_id}", headers=headers
                )
                if response.status_code == 204:
                    print_test("Link work effort to project", True)
                    passed += 1
                else:
                    print_test("Link work effort", False)
                    failed += 1
            except Exception as e:
                print_test(f"Link error: {e}", False)
                failed += 1

            # Test 6.2: Verify link exists
            try:
                response = client.get(f"/api/projects/{link_project_id}")
                project = response.json()
                if link_we_id in project.get("related_work_efforts", []):
                    print_test("Verify work effort link", True)
                    passed += 1
                else:
                    print_test("Verify work effort link", False)
                    failed += 1
            except Exception as e:
                print_test(f"Verify link error: {e}", False)
                failed += 1

            # Test 6.3: Link same work effort twice (idempotent)
            try:
                response = client.post(
                    f"/api/projects/{link_project_id}/work-efforts/{link_we_id}", headers=headers
                )
                if response.status_code == 204:
                    # Should still only have one link
                    response = client.get(f"/api/projects/{link_project_id}")
                    project = response.json()
                    count = project.get("related_work_efforts", []).count(link_we_id)
                    if count == 1:
                        print_test("Idempotent linking (no duplicates)", True)
                        passed += 1
                    else:
                        print_test("Idempotent linking", False)
                        failed += 1
                else:
                    print_test("Idempotent linking", False)
                    failed += 1
            except Exception as e:
                print_test(f"Idempotent link error: {e}", False)
                failed += 1

            # Test 6.4: Unlink work effort
            try:
                response = client.delete(
                    f"/api/projects/{link_project_id}/work-efforts/{link_we_id}", headers=headers
                )
                if response.status_code == 204:
                    print_test("Unlink work effort", True)
                    passed += 1
                else:
                    print_test("Unlink work effort", False)
                    failed += 1
            except Exception as e:
                print_test(f"Unlink error: {e}", False)
                failed += 1

            # Test 6.5: Unlink non-existent link (should succeed)
            try:
                response = client.delete(
                    f"/api/projects/{link_project_id}/work-efforts/{link_we_id}", headers=headers
                )
                if response.status_code == 204:
                    print_test("Unlink non-existent (idempotent)", True)
                    passed += 1
                else:
                    print_test("Unlink non-existent", False)
                    failed += 1
            except Exception as e:
                print_test(f"Unlink non-existent error: {e}", False)
                failed += 1

            # Test 6.6: Invalid work effort ID format
            try:
                response = client.post(
                    f"/api/projects/{link_project_id}/work-efforts/INVALID-ID", headers=headers
                )
                if response.status_code == 422:
                    print_test("Invalid WE ID format validation", True)
                    passed += 1
                else:
                    print_test("Invalid WE ID format validation", False)
                    failed += 1
            except Exception as e:
                print_test(f"Invalid ID format error: {e}", False)
                failed += 1

        except Exception as e:
            print_test(f"Linking setup error: {e}", False)
            failed += 1

        # ===================================================================
        # SECTION 7: PERFORMANCE & CONCURRENCY
        # ===================================================================
        print_section("7. PERFORMANCE TESTS")

        # Test 7.1: Create multiple projects quickly
        try:
            start = time.time()
            project_ids = []
            for i in range(10):
                response = client.post(
                    "/api/projects", json={"title": f"Perf Test {i}"}, headers=headers
                )
                if response.status_code == 201:
                    project_ids.append(response.json()["project_id"])

            elapsed = time.time() - start
            if elapsed < 5.0:  # Should complete in under 5 seconds
                print_test(f"Create 10 projects quickly ({elapsed:.2f}s)", True)
                passed += 1
            else:
                print_test(f"Create 10 projects ({elapsed:.2f}s)", False)
                failed += 1
        except Exception as e:
            print_test(f"Performance test error: {e}", False)
            failed += 1

        # Test 7.2: List with many items
        try:
            start = time.time()
            response = client.get("/api/projects")
            elapsed = time.time() - start
            if response.status_code == 200 and elapsed < 1.0:
                print_test(f"List projects quickly ({elapsed:.2f}s)", True)
                passed += 1
            else:
                print_test(f"List projects ({elapsed:.2f}s)", False)
                failed += 1
        except Exception as e:
            print_test(f"List performance error: {e}", False)
            failed += 1

        # ===================================================================
        # SECTION 8: DATA INTEGRITY
        # ===================================================================
        print_section("8. DATA INTEGRITY TESTS")

        # Test 8.1: Update preserves unchanged fields
        if project_id:
            try:
                # Get original
                original = client.get(f"/api/projects/{project_id}").json()

                # Update only status
                client.patch(
                    f"/api/projects/{project_id}", json={"status": "active"}, headers=headers
                )

                # Get updated
                updated = client.get(f"/api/projects/{project_id}").json()

                # Check other fields preserved
                if (
                    updated["title"] == original["title"]
                    and updated["description"] == original["description"]
                ):
                    print_test("PATCH preserves unchanged fields", True)
                    passed += 1
                else:
                    print_test("PATCH preserves unchanged fields", False)
                    failed += 1
            except Exception as e:
                print_test(f"Field preservation error: {e}", False)
                failed += 1

        # Test 8.2: Work effort file structure
        if we_id:
            try:
                we_dir = project_path / "_work_efforts"
                found = False
                for item in we_dir.iterdir():
                    if item.is_dir() and item.name.startswith(we_id):
                        index_file = item / f"{we_id}_index.md"
                        if index_file.exists():
                            found = True
                            # Check tickets directory
                            tickets_dir = item / "tickets"
                            if tickets_dir.exists() and tickets_dir.is_dir():
                                print_test("Work effort file structure correct", True)
                                passed += 1
                            else:
                                print_test("Work effort file structure", False)
                                failed += 1
                        break

                if not found:
                    print_test("Work effort directory exists", False)
                    failed += 1
            except Exception as e:
                print_test(f"File structure error: {e}", False)
                failed += 1

        # ===================================================================
        # FINAL SUMMARY
        # ===================================================================
        print_section("TEST SUMMARY")

        total = passed + failed
        success_rate = (passed / total * 100) if total > 0 else 0

        print(f"\n  📊 Total Tests: {total}")
        print(f"  ✅ Passed: {passed}")
        print(f"  ❌ Failed: {failed}")
        print(f"  📈 Success Rate: {success_rate:.1f}%")

        if failed == 0:
            print("\n  🎉 ALL TESTS PASSED! API is ROCK SOLID! 🔥")
        elif success_rate >= 90:
            print("\n  ✅ Excellent! API is in great shape!")
        elif success_rate >= 75:
            print("\n  ⚠️  Good, but some issues need attention")
        else:
            print("\n  ❌ Multiple issues detected - review needed")

        return failed == 0

    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback

        traceback.print_exc()
        return False
    finally:
        shutil.rmtree(temp_dir)
        print("\n🧹 Cleaned up temporary directory")


if __name__ == "__main__":
    success = test_comprehensive()
    sys.exit(0 if success else 1)
