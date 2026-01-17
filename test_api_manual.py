#!/usr/bin/env python3
"""
Manual test script for WAFT API endpoints.
Tests the new CRUD operations without requiring pytest.
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fastapi.testclient import TestClient
from waft.api.main import create_app
from waft.api.auth import get_or_create_token

def test_api():
    """Test the API endpoints."""
    print("🧪 Testing WAFT API Endpoints\n")
    
    # Create temporary project directory
    temp_dir = tempfile.mkdtemp()
    project_path = Path(temp_dir)
    (project_path / "_work_efforts").mkdir(exist_ok=True)
    
    try:
        # Create app and client
        app = create_app(project_path)
        client = TestClient(app)
        
        # Get auth token
        token = get_or_create_token(project_path)
        headers = {"Authorization": f"Bearer {token}"}
        
        print("✅ App created successfully")
        print(f"✅ Auth token generated: {token[:20]}...\n")
        
        # Test 1: Create Project
        print("📝 Test 1: Create Project (POST /api/projects)")
        response = client.post(
            "/api/projects",
            json={
                "title": "Test Project",
                "description": "A test project for API testing",
                "tags": ["test", "api"],
                "status": "planning"
            },
            headers=headers
        )
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        project_data = response.json()
        project_id = project_data["project_id"]
        print(f"   ✅ Project created: {project_id}")
        print(f"   ✅ Title: {project_data['title']}")
        print(f"   ✅ Status: {project_data['status']}\n")
        
        # Test 2: Get Project
        print("📖 Test 2: Get Project (GET /api/projects/{project_id})")
        response = client.get(f"/api/projects/{project_id}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print(f"   ✅ Project retrieved: {response.json()['title']}\n")
        
        # Test 3: List Projects
        print("📋 Test 3: List Projects (GET /api/projects)")
        response = client.get("/api/projects")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        projects = response.json()
        assert len(projects) > 0, "Should have at least one project"
        print(f"   ✅ Found {len(projects)} project(s)\n")
        
        # Test 4: Update Project (PATCH)
        print("✏️  Test 4: Update Project (PATCH /api/projects/{project_id})")
        response = client.patch(
            f"/api/projects/{project_id}",
            json={"status": "active"},
            headers=headers
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.json()["status"] == "active", "Status should be updated"
        print(f"   ✅ Project status updated to: {response.json()['status']}\n")
        
        # Test 5: Create Work Effort
        print("📝 Test 5: Create Work Effort (POST /api/work-efforts)")
        response = client.post(
            "/api/work-efforts",
            json={
                "title": "Test Work Effort",
                "description": "A test work effort",
                "status": "active",
                "tags": ["test"]
            },
            headers=headers
        )
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        we_data = response.json()
        we_id = we_data["id"]
        assert we_id.startswith("WE-"), "Work effort ID should start with WE-"
        print(f"   ✅ Work effort created: {we_id}")
        print(f"   ✅ Title: {we_data['title']}\n")
        
        # Test 6: Get Work Effort
        print("📖 Test 6: Get Work Effort (GET /api/work-efforts/{we_id})")
        response = client.get(f"/api/work-efforts/{we_id}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print(f"   ✅ Work effort retrieved: {response.json()['title']}\n")
        
        # Test 7: List Work Efforts
        print("📋 Test 7: List Work Efforts (GET /api/work-efforts)")
        response = client.get("/api/work-efforts")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        we_list = response.json()
        assert "items" in we_list, "Response should have 'items' key"
        assert "total" in we_list, "Response should have 'total' key"
        print(f"   ✅ Found {we_list['total']} work effort(s)\n")
        
        # Test 8: Link Work Effort to Project
        print("🔗 Test 8: Link Work Effort to Project (POST /api/projects/{project_id}/work-efforts/{we_id})")
        response = client.post(
            f"/api/projects/{project_id}/work-efforts/{we_id}",
            headers=headers
        )
        assert response.status_code == 204, f"Expected 204, got {response.status_code}"
        print(f"   ✅ Work effort linked to project\n")
        
        # Test 9: Verify link
        print("🔍 Test 9: Verify Work Effort Link")
        response = client.get(f"/api/projects/{project_id}")
        project = response.json()
        assert we_id in project["related_work_efforts"], "Work effort should be in related_work_efforts"
        print(f"   ✅ Work effort {we_id} is linked to project\n")
        
        # Test 10: Unlink Work Effort
        print("🔓 Test 10: Unlink Work Effort (DELETE /api/projects/{project_id}/work-efforts/{we_id})")
        response = client.delete(
            f"/api/projects/{project_id}/work-efforts/{we_id}",
            headers=headers
        )
        assert response.status_code == 204, f"Expected 204, got {response.status_code}"
        print(f"   ✅ Work effort unlinked from project\n")
        
        # Test 11: Delete Work Effort
        print("🗑️  Test 11: Delete Work Effort (DELETE /api/work-efforts/{we_id})")
        response = client.delete(
            f"/api/work-efforts/{we_id}",
            headers=headers
        )
        assert response.status_code == 204, f"Expected 204, got {response.status_code}"
        print(f"   ✅ Work effort deleted\n")
        
        # Test 12: Delete Project
        print("🗑️  Test 12: Delete Project (DELETE /api/projects/{project_id})")
        response = client.delete(
            f"/api/projects/{project_id}",
            headers=headers
        )
        assert response.status_code == 204, f"Expected 204, got {response.status_code}"
        print(f"   ✅ Project deleted\n")
        
        # Test 13: Auth Required
        print("🔒 Test 13: Authentication Required (POST /api/projects without token)")
        response = client.post(
            "/api/projects",
            json={"title": "Should Fail"}
        )
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        print(f"   ✅ Unauthorized request correctly rejected\n")
        
        # Test 14: Error Handling
        print("❌ Test 14: Error Handling (GET /api/projects/nonexistent)")
        response = client.get("/api/projects/nonexistent")
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        error_data = response.json()
        assert "error" in error_data, "Error response should have 'error' field"
        assert "message" in error_data, "Error response should have 'message' field"
        print(f"   ✅ Error response format correct: {error_data['error']}\n")
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print(f"\n📊 Test Summary:")
        print(f"   - Projects CRUD: ✅")
        print(f"   - Work Efforts CRUD: ✅")
        print(f"   - Authentication: ✅")
        print(f"   - Error Handling: ✅")
        print(f"   - Work Effort Linking: ✅")
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)
        print(f"\n🧹 Cleaned up temporary directory")

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
