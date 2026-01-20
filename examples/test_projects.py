"""
Test suite for Projects Feature.

Tests core functionality of ProjectManager and data models.
"""

import tempfile
from pathlib import Path

from src.waft.core.projects import ProgressEntry, ProjectManager, ProjectStatus


def test_create_project():
    """Test project creation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = ProjectManager(Path(tmpdir))

        project = manager.create_project(
            title="Test Project",
            description="A test project",
            tags=["test", "example"],
            status=ProjectStatus.ACTIVE,
        )

        assert project.project_id.startswith("proj_")
        assert project.title == "Test Project"
        assert project.description == "A test project"
        assert project.status == ProjectStatus.ACTIVE
        assert "test" in project.tags
        assert project.progress_percent == 0.0

        print("✅ Project creation test passed")


def test_get_project():
    """Test getting a project."""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = ProjectManager(Path(tmpdir))

        # Create project
        created = manager.create_project(title="Test Project", description="A test project")

        # Get project
        retrieved = manager.get_project(created.project_id)

        assert retrieved is not None
        assert retrieved.project_id == created.project_id
        assert retrieved.title == created.title

        print("✅ Get project test passed")


def test_list_projects():
    """Test listing projects."""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = ProjectManager(Path(tmpdir))

        # Create multiple projects
        project1 = manager.create_project("Project 1", status=ProjectStatus.ACTIVE)
        manager.create_project("Project 2", status=ProjectStatus.PAUSED)
        project3 = manager.create_project("Project 3", tags=["test"])

        # List all
        all_projects = manager.list_projects()
        assert len(all_projects) == 3

        # Filter by status
        active = manager.list_projects(status=ProjectStatus.ACTIVE)
        assert len(active) == 1
        assert active[0].project_id == project1.project_id

        # Filter by tags
        tagged = manager.list_projects(tags=["test"])
        assert len(tagged) == 1
        assert tagged[0].project_id == project3.project_id

        print("✅ List projects test passed")


def test_update_project():
    """Test updating a project."""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = ProjectManager(Path(tmpdir))

        # Create project
        project = manager.create_project("Test Project")

        # Update
        project.title = "Updated Title"
        project.description = "Updated description"
        project.status = ProjectStatus.ACTIVE
        manager.update_project(project)

        # Verify
        updated = manager.get_project(project.project_id)
        assert updated.title == "Updated Title"
        assert updated.description == "Updated description"
        assert updated.status == ProjectStatus.ACTIVE

        print("✅ Update project test passed")


def test_progress_tracking():
    """Test progress tracking."""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = ProjectManager(Path(tmpdir))

        # Create project
        project = manager.create_project("Test Project")

        # Add progress entry
        from datetime import datetime

        entry = ProgressEntry(
            entry_id="entry_1",
            timestamp=datetime.now().isoformat(),
            progress_delta=25.0,
            notes="Phase 1 complete",
        )
        project.progress_entries.append(entry)
        project.progress_percent = 25.0
        manager.update_project(project)

        # Verify
        updated = manager.get_project(project.project_id)
        assert updated.progress_percent == 25.0
        assert len(updated.progress_entries) == 1
        assert updated.progress_entries[0].progress_delta == 25.0

        print("✅ Progress tracking test passed")


def test_input_validation():
    """Test input validation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = ProjectManager(Path(tmpdir))

        # Test invalid title (too long)
        try:
            manager.create_project("x" * 300)  # Exceeds MAX_TITLE_LENGTH
            raise AssertionError("Should have raised ValueError")
        except ValueError:
            pass

        # Test invalid progress (negative)
        project = manager.create_project("Test")
        try:
            project.progress_percent = -10.0
            manager.update_project(project)
            raise AssertionError("Should have raised ValueError")
        except ValueError:
            pass

        # Test invalid progress (>100)
        try:
            project.progress_percent = 150.0
            manager.update_project(project)
            raise AssertionError("Should have raised ValueError")
        except ValueError:
            pass

        print("✅ Input validation test passed")


def test_security_validation():
    """Test security validation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = ProjectManager(Path(tmpdir))

        # Test path traversal in project_id
        try:
            manager.get_project("../../../etc/passwd")
            raise AssertionError("Should have raised ValueError")
        except ValueError:
            pass

        # Test invalid project_id characters
        try:
            manager.get_project("proj/with/slashes")
            raise AssertionError("Should have raised ValueError")
        except ValueError:
            pass

        print("✅ Security validation test passed")


def run_all_tests():
    """Run all tests."""
    print("\n🧪 Running Projects Feature Tests\n")

    try:
        test_create_project()
        test_get_project()
        test_list_projects()
        test_update_project()
        test_progress_tracking()
        test_input_validation()
        test_security_validation()

        print("\n✅ All tests passed!\n")
        return True
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ Test error: {e}\n")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
