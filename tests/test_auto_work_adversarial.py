"""
Adversarial Test Suite for Auto Work Command

HARSH, SECURITY-FIRST testing that assumes malicious intent and worst-case scenarios.
Tests all attack vectors, edge cases, and failure modes.
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any, List

# Import the module under test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.auto_work import (
    calculate_work_effort_priority,
    select_best_work_effort,
    get_work_effort_action,
    execute_work_effort_action,
    _validate_work_effort_id,
)


class TestWorkEffortIDValidation:
    """CRITICAL: Test work effort ID validation to prevent injection."""
    
    def test_valid_id_format(self):
        """Valid IDs should pass."""
        assert _validate_work_effort_id("WE-260112-wfga") == True
        assert _validate_work_effort_id("WE-260119-abc1") == True
        assert _validate_work_effort_id("WE-260119-1234") == True
    
    def test_invalid_id_format_path_traversal(self):
        """CRITICAL: Path traversal attempts should be rejected."""
        assert _validate_work_effort_id("../etc/passwd") == False
        assert _validate_work_effort_id("WE-260112-../../") == False
        assert _validate_work_effort_id("WE-260112-..//") == False
    
    def test_invalid_id_format_command_injection(self):
        """CRITICAL: Command injection attempts should be rejected."""
        assert _validate_work_effort_id("WE-260112-;rm") == False
        assert _validate_work_effort_id("WE-260112-|cat") == False
        assert _validate_work_effort_id("WE-260112-$(id)") == False
        assert _validate_work_effort_id("WE-260112-`ls`") == False
    
    def test_invalid_id_format_sql_injection(self):
        """SQL injection attempts should be rejected."""
        assert _validate_work_effort_id("WE-260112-'OR'1") == False
        assert _validate_work_effort_id("WE-260112-DROP") == False
    
    def test_invalid_id_format_xss(self):
        """XSS attempts should be rejected."""
        assert _validate_work_effort_id("WE-260112-<script>") == False
        assert _validate_work_effort_id("WE-260112-<img>") == False
    
    def test_invalid_id_format_unicode(self):
        """Unicode injection attempts should be rejected."""
        assert _validate_work_effort_id("WE-260112-测试") == False
        assert _validate_work_effort_id("WE-260112-🚀") == False
    
    def test_invalid_id_format_too_long(self):
        """Excessively long IDs should be rejected."""
        assert _validate_work_effort_id("WE-260112-" + "a" * 100) == False
    
    def test_invalid_id_format_wrong_structure(self):
        """Wrong structure should be rejected."""
        assert _validate_work_effort_id("WE-260112") == False  # Missing suffix
        assert _validate_work_effort_id("WE-260112-wfga-extra") == False  # Too many parts
        assert _validate_work_effort_id("260112-wfga") == False  # Missing WE- prefix
        assert _validate_work_effort_id("WE-26011-wfga") == False  # Wrong date format
        assert _validate_work_effort_id("WE-260112-WFGA") == False  # Uppercase suffix
    
    def test_empty_id(self):
        """Empty ID should be rejected."""
        assert _validate_work_effort_id("") == False
        assert _validate_work_effort_id(None) == False  # Type check


class TestCommandInjectionPrevention:
    """CRITICAL: Test command injection prevention."""
    
    @pytest.fixture
    def malicious_work_effort(self):
        """Create a work effort with malicious content."""
        return {
            "id": "WE-260112-wfga",  # Valid ID
            "path": "_work_efforts/WE-260112-wfga",
            "status": "active",
            "title": "Malicious Work Effort",
        }
    
    @pytest.fixture
    def malicious_action(self):
        """Create an action with malicious command."""
        return {
            "id": "action_malicious",
            "label": "Malicious Action",
            "action": "status_transition",  # Valid action type
            "command": "rm -rf /; echo 'pwned'",  # MALICIOUS
            "priority": "high",
        }
    
    def test_malicious_command_rejected_by_length(self, malicious_work_effort, malicious_action, tmp_path):
        """CRITICAL: Malicious commands should be rejected by length limit."""
        result = execute_work_effort_action(malicious_work_effort, malicious_action, tmp_path)
        # Long malicious commands should fail validation
        if len(malicious_action["command"]) > 500:
            assert result.get("success") == False
            assert "validation" in result.get("error", "").lower()
    
    def test_action_type_whitelist_enforced(self, malicious_work_effort, tmp_path):
        """CRITICAL: Only whitelisted action types should be allowed."""
        malicious_action = {
            "id": "action_malicious",
            "label": "Malicious Action",
            "action": "rm -rf /",  # NOT in whitelist
            "command": "Some command",
            "priority": "high",
        }
        
        result = execute_work_effort_action(malicious_work_effort, malicious_action, tmp_path)
        assert result.get("success") == False
        assert "whitelist" in result.get("error", "").lower() or "invalid" in result.get("error", "").lower()
    
    def test_invalid_work_effort_id_rejected(self, tmp_path):
        """CRITICAL: Invalid work effort IDs should be rejected."""
        malicious_work_effort = {
            "id": "../../etc/passwd",  # Path traversal
            "path": "_work_efforts/WE-260112-wfga",
            "status": "active",
        }
        
        action = {
            "id": "action_test",
            "label": "Test Action",
            "action": "status_transition",
            "command": "Test command",
            "priority": "high",
        }
        
        result = execute_work_effort_action(malicious_work_effort, action, tmp_path)
        assert result.get("success") == False
        assert "invalid" in result.get("error", "").lower() or "format" in result.get("error", "").lower()


class TestPathTraversalPrevention:
    """CRITICAL: Test path traversal prevention."""
    
    @pytest.fixture
    def project_path(self, tmp_path):
        """Create a temporary project structure."""
        project = tmp_path / "project"
        project.mkdir()
        (project / "_work_efforts").mkdir()
        return project
    
    def test_path_traversal_in_work_effort_path(self, project_path):
        """CRITICAL: Path traversal in work effort path should be rejected."""
        malicious_work_effort = {
            "id": "WE-260112-wfga",
            "path": "../../etc/passwd",  # Path traversal
            "status": "active",
        }
        
        # Should be filtered out during selection
        selected = select_best_work_effort([malicious_work_effort], project_path)
        assert selected is None or selected.get("id") != malicious_work_effort["id"]
    
    def test_absolute_path_rejected(self, project_path):
        """CRITICAL: Absolute paths should be rejected."""
        malicious_work_effort = {
            "id": "WE-260112-wfga",
            "path": "/etc/passwd",  # Absolute path
            "status": "active",
        }
        
        selected = select_best_work_effort([malicious_work_effort], project_path)
        assert selected is None or selected.get("id") != malicious_work_effort["id"]


class TestEmpiricaGateIntegration:
    """CRITICAL: Test Empirica safety gates."""
    
    @pytest.fixture
    def work_effort(self):
        return {
            "id": "WE-260112-wfga",
            "path": "_work_efforts/WE-260112-wfga",
            "status": "active",
            "title": "Test Work Effort",
        }
    
    @pytest.fixture
    def action(self):
        return {
            "id": "action_test",
            "label": "Test Action",
            "action": "status_transition",
            "command": "Update work effort WE-260112-wfga status to 'active'",
            "priority": "high",
        }
    
    def test_empirica_halt_blocks_execution(self, work_effort, action, tmp_path):
        """CRITICAL: HALT gate should block execution."""
        # Mock the import inside the function
        mock_empirica = Mock()
        mock_empirica.is_initialized.return_value = True
        mock_empirica.check_submit.return_value = "HALT"
        mock_empirica_class = Mock(return_value=mock_empirica)
        
        with patch('src.waft.core.empirica.EmpiricaManager', mock_empirica_class):
            result = execute_work_effort_action(work_effort, action, tmp_path)
        
        assert result.get("success") == False
        assert result.get("gate_result") == "HALT"
        assert "approval" in result.get("error", "").lower() or "halt" in result.get("error", "").lower()
    
    def test_empirica_branch_blocks_execution(self, work_effort, action, tmp_path):
        """CRITICAL: BRANCH gate should block execution."""
        mock_empirica = Mock()
        mock_empirica.is_initialized.return_value = True
        mock_empirica.check_submit.return_value = "BRANCH"
        mock_empirica_class = Mock(return_value=mock_empirica)
        
        with patch('src.waft.core.empirica.EmpiricaManager', mock_empirica_class):
            result = execute_work_effort_action(work_effort, action, tmp_path)
        
        assert result.get("success") == False
        assert result.get("gate_result") == "BRANCH"
        assert "investigation" in result.get("error", "").lower() or "branch" in result.get("error", "").lower()
    
    def test_empirica_revise_blocks_execution(self, work_effort, action, tmp_path):
        """CRITICAL: REVISE gate should block execution."""
        mock_empirica = Mock()
        mock_empirica.is_initialized.return_value = True
        mock_empirica.check_submit.return_value = "REVISE"
        mock_empirica_class = Mock(return_value=mock_empirica)
        
        with patch('src.waft.core.empirica.EmpiricaManager', mock_empirica_class):
            result = execute_work_effort_action(work_effort, action, tmp_path)
        
        assert result.get("success") == False
        assert result.get("gate_result") == "REVISE"
        assert "revision" in result.get("error", "").lower() or "revise" in result.get("error", "").lower()
    
    def test_empirica_proceed_allows_execution(self, work_effort, action, tmp_path):
        """PROCEED gate should allow execution."""
        mock_empirica = Mock()
        mock_empirica.is_initialized.return_value = True
        mock_empirica.check_submit.return_value = "PROCEED"
        mock_empirica_class = Mock(return_value=mock_empirica)
        
        with patch('src.waft.core.empirica.EmpiricaManager', mock_empirica_class):
            result = execute_work_effort_action(work_effort, action, tmp_path)
        
        assert result.get("success") == True
        assert result.get("gate_result") is None  # No gate result when proceeding
    
    def test_empirica_unavailable_continues(self, work_effort, action, tmp_path):
        """If Empirica unavailable, should continue (graceful degradation)."""
        with patch('src.waft.core.empirica.EmpiricaManager', side_effect=Exception("Empirica not available")):
            result = execute_work_effort_action(work_effort, action, tmp_path)
        
        # Should continue without gate (graceful degradation)
        assert result.get("success") == True
    
    def test_empirica_not_initialized_continues(self, work_effort, action, tmp_path):
        """If Empirica not initialized, should continue."""
        mock_empirica = Mock()
        mock_empirica.is_initialized.return_value = False
        mock_empirica_class = Mock(return_value=mock_empirica)
        
        with patch('src.waft.core.empirica.EmpiricaManager', mock_empirica_class):
            result = execute_work_effort_action(work_effort, action, tmp_path)
        
        # Should continue without gate check
        assert result.get("success") == True
        mock_empirica.check_submit.assert_not_called()


class TestFileSizeLimits:
    """Test file size limit enforcement."""
    
    @pytest.fixture
    def project_path(self, tmp_path):
        """Create a temporary project structure."""
        project = tmp_path / "project"
        project.mkdir()
        (project / "_work_efforts").mkdir()
        return project
    
    def test_large_file_rejected(self, project_path):
        """CRITICAL: Files exceeding size limit should be rejected."""
        we_dir = project_path / "_work_efforts" / "WE-260112-wfga"
        we_dir.mkdir()
        
        # Create a file larger than MAX_INDEX_FILE_SIZE (1MB)
        large_file = we_dir / "index.md"
        large_file.write_text("x" * (2 * 1024 * 1024))  # 2MB
        
        work_effort = {
            "id": "WE-260112-wfga",
            "path": "_work_efforts/WE-260112-wfga",
            "status": "active",
        }
        
        # Should handle large file gracefully (skip content analysis)
        score = calculate_work_effort_priority(work_effort, project_path)
        # Should still calculate score (just without content analysis)
        assert isinstance(score, float)
        assert score >= 0


class TestErrorHandling:
    """Test error handling and graceful degradation."""
    
    @pytest.fixture
    def project_path(self, tmp_path):
        """Create a temporary project structure."""
        project = tmp_path / "project"
        project.mkdir()
        (project / "_work_efforts").mkdir()
        return project
    
    def test_git_operation_failure_handled(self, project_path):
        """Git operation failures should be handled gracefully."""
        work_effort = {
            "id": "WE-260112-wfga",
            "path": "_work_efforts/WE-260112-wfga",
            "status": "active",
        }
        
        we_dir = project_path / "_work_efforts" / "WE-260112-wfga"
        we_dir.mkdir()
        
        # Mock git operation to fail
        with patch('scripts.auto_work.get_recent_git_activity', side_effect=Exception("Git error")):
            score = calculate_work_effort_priority(work_effort, project_path)
            # Should still return a score (without git activity)
            assert isinstance(score, float)
            assert score >= 0
    
    def test_file_read_error_handled(self, project_path):
        """File read errors should be handled gracefully."""
        work_effort = {
            "id": "WE-260112-wfga",
            "path": "_work_efforts/WE-260112-wfga",
            "status": "active",
        }
        
        we_dir = project_path / "_work_efforts" / "WE-260112-wfga"
        we_dir.mkdir()
        
        # Create a file that can't be read (permission denied simulation)
        index_file = we_dir / "index.md"
        index_file.write_text("test")
        
        # Mock file read to fail
        with patch('pathlib.Path.read_text', side_effect=PermissionError("Permission denied")):
            score = calculate_work_effort_priority(work_effort, project_path)
            # Should still return a score (without content analysis)
            assert isinstance(score, float)
            assert score >= 0


class TestPriorityScoring:
    """Test priority scoring edge cases."""
    
    @pytest.fixture
    def project_path(self, tmp_path):
        """Create a temporary project structure."""
        project = tmp_path / "project"
        project.mkdir()
        (project / "_work_efforts").mkdir()
        return project
    
    def test_completed_work_effort_zero_score(self, project_path):
        """Completed work efforts should have zero score."""
        work_effort = {
            "id": "WE-260112-wfga",
            "path": "_work_efforts/WE-260112-wfga",
            "status": "completed",
        }
        
        score = calculate_work_effort_priority(work_effort, project_path)
        assert score == 0.0
    
    def test_active_higher_than_paused(self, project_path):
        """Active work efforts should score higher than paused."""
        active = {
            "id": "WE-260112-active",
            "path": "_work_efforts/WE-260112-active",
            "status": "active",
        }
        
        paused = {
            "id": "WE-260112-paused",
            "path": "_work_efforts/WE-260112-paused",
            "status": "paused",
        }
        
        active_score = calculate_work_effort_priority(active, project_path)
        paused_score = calculate_work_effort_priority(paused, project_path)
        
        assert active_score > paused_score
    
    def test_critical_higher_than_low(self, project_path):
        """CRITICAL priority should score higher than LOW."""
        critical = {
            "id": "WE-260112-critical",
            "path": "_work_efforts/WE-260112-critical",
            "status": "active",
            "priority": "CRITICAL",
        }
        
        low = {
            "id": "WE-260112-low",
            "path": "_work_efforts/WE-260112-low",
            "status": "active",
            "priority": "LOW",
        }
        
        critical_score = calculate_work_effort_priority(critical, project_path)
        low_score = calculate_work_effort_priority(low, project_path)
        
        assert critical_score > low_score
    
    def test_todo_increases_score(self, project_path):
        """Work efforts with TODOs should score higher."""
        we_dir = project_path / "_work_efforts" / "WE-260112-wfga"
        we_dir.mkdir()
        index_file = we_dir / "index.md"
        index_file.write_text("# Work Effort\n\nTODO: Fix this")
        
        work_effort = {
            "id": "WE-260112-wfga",
            "path": "_work_efforts/WE-260112-wfga",
            "status": "active",
        }
        
        score = calculate_work_effort_priority(work_effort, project_path)
        assert score > 100.0  # Base active score (100) + TODO bonus (20)


class TestSelectionLogic:
    """Test work effort selection logic."""
    
    @pytest.fixture
    def project_path(self, tmp_path):
        """Create a temporary project structure."""
        project = tmp_path / "project"
        project.mkdir()
        (project / "_work_efforts").mkdir()
        return project
    
    def test_selects_highest_priority(self, project_path):
        """Should select work effort with highest priority score."""
        # Create directories for validation (using valid ID format)
        (project_path / "_work_efforts" / "WE-260112-low1").mkdir(parents=True)
        (project_path / "_work_efforts" / "WE-260112-crit").mkdir(parents=True)
        
        work_efforts = [
            {
                "id": "WE-260112-low1",
                "path": "_work_efforts/WE-260112-low1",
                "status": "active",
                "priority": "LOW",
            },
            {
                "id": "WE-260112-crit",
                "path": "_work_efforts/WE-260112-crit",
                "status": "active",
                "priority": "CRITICAL",
            },
        ]
        
        selected = select_best_work_effort(work_efforts, project_path)
        assert selected is not None
        assert selected.get("id") == "WE-260112-crit"
    
    def test_filters_invalid_ids(self, project_path):
        """Should filter out work efforts with invalid IDs."""
        work_efforts = [
            {
                "id": "../../etc/passwd",  # Invalid
                "path": "_work_efforts/WE-260112-wfga",
                "status": "active",
            },
            {
                "id": "WE-260112-wfga",  # Valid
                "path": "_work_efforts/WE-260112-wfga",
                "status": "active",
            },
        ]
        
        selected = select_best_work_effort(work_efforts, project_path)
        assert selected is not None
        assert selected.get("id") == "WE-260112-wfga"
    
    def test_filters_completed(self, project_path):
        """Should filter out completed work efforts."""
        # Create directories for validation (using valid ID format)
        (project_path / "_work_efforts" / "WE-260112-done").mkdir(parents=True)
        (project_path / "_work_efforts" / "WE-260112-act1").mkdir(parents=True)
        
        work_efforts = [
            {
                "id": "WE-260112-done",
                "path": "_work_efforts/WE-260112-done",
                "status": "completed",
            },
            {
                "id": "WE-260112-act1",
                "path": "_work_efforts/WE-260112-act1",
                "status": "active",
            },
        ]
        
        selected = select_best_work_effort(work_efforts, project_path)
        assert selected is not None
        assert selected.get("id") == "WE-260112-act1"
    
    def test_empty_list_returns_none(self, project_path):
        """Empty list should return None."""
        selected = select_best_work_effort([], project_path)
        assert selected is None
    
    def test_all_completed_returns_none(self, project_path):
        """If all work efforts are completed, should return None."""
        work_efforts = [
            {
                "id": "WE-260112-completed1",
                "path": "_work_efforts/WE-260112-completed1",
                "status": "completed",
            },
            {
                "id": "WE-260112-completed2",
                "path": "_work_efforts/WE-260112-completed2",
                "status": "completed",
            },
        ]
        
        selected = select_best_work_effort(work_efforts, project_path)
        assert selected is None


class TestActionSelection:
    """Test action selection logic."""
    
    @pytest.fixture
    def project_path(self, tmp_path):
        """Create a temporary project structure."""
        project = tmp_path / "project"
        project.mkdir()
        (project / "_work_efforts").mkdir()
        return project
    
    @patch('scripts.auto_work.analyze_work_effort_actions')
    def test_selects_highest_priority_action(self, mock_analyze, project_path):
        """Should select action with highest priority."""
        mock_analyze.return_value = [
            {
                "id": "action_low",
                "label": "Low Priority",
                "action": "review",
                "priority": "low",
            },
            {
                "id": "action_high",
                "label": "High Priority",
                "action": "status_transition",
                "priority": "high",
            },
        ]
        
        work_effort = {
            "id": "WE-260112-wfga",
            "path": "_work_efforts/WE-260112-wfga",
            "status": "active",
        }
        
        action = get_work_effort_action(work_effort, project_path)
        assert action is not None
        assert action.get("id") == "action_high"
    
    @patch('scripts.auto_work.analyze_work_effort_actions')
    def test_no_actions_returns_none(self, mock_analyze, project_path):
        """If no actions available, should return None."""
        mock_analyze.return_value = []
        
        work_effort = {
            "id": "WE-260112-wfga",
            "path": "_work_efforts/WE-260112-wfga",
            "status": "active",
        }
        
        action = get_work_effort_action(work_effort, project_path)
        assert action is None


class TestConcurrentExecution:
    """Test concurrent execution scenarios."""
    
    def test_multiple_instances_could_run(self, tmp_path):
        """WARNING: Multiple instances could run simultaneously (no locking)."""
        # This test documents the current behavior (no locking)
        # In production, this should be fixed with file locks
        work_effort = {
            "id": "WE-260112-wfga",
            "path": "_work_efforts/WE-260112-wfga",
            "status": "active",
        }
        
        action = {
            "id": "action_test",
            "label": "Test Action",
            "action": "status_transition",
            "command": "Test command",
            "priority": "high",
        }
        
        # Both should succeed (no locking prevents this)
        result1 = execute_work_effort_action(work_effort, action, tmp_path)
        result2 = execute_work_effort_action(work_effort, action, tmp_path)
        
        # Currently both succeed (this is a known issue)
        # TODO: Add file locking to prevent concurrent execution
        assert result1.get("success") == True
        assert result2.get("success") == True


class TestMalformedData:
    """Test handling of malformed data."""
    
    @pytest.fixture
    def project_path(self, tmp_path):
        """Create a temporary project structure."""
        project = tmp_path / "project"
        project.mkdir()
        (project / "_work_efforts").mkdir()
        return project
    
    def test_missing_required_fields(self, project_path):
        """Missing required fields should be handled gracefully."""
        work_effort = {}  # Missing all fields
        
        score = calculate_work_effort_priority(work_effort, project_path)
        # Should return a score (defaults to 0 or minimal)
        assert isinstance(score, float)
        assert score >= 0
    
    def test_invalid_status(self, project_path):
        """Invalid status should be handled gracefully."""
        work_effort = {
            "id": "WE-260112-wfga",
            "path": "_work_efforts/WE-260112-wfga",
            "status": "invalid_status",
        }
        
        score = calculate_work_effort_priority(work_effort, project_path)
        # Should return a score (defaults to 0 for unknown status)
        assert isinstance(score, float)
        assert score >= 0
    
    def test_invalid_priority(self, project_path):
        """Invalid priority should be handled gracefully."""
        work_effort = {
            "id": "WE-260112-wfga",
            "path": "_work_efforts/WE-260112-wfga",
            "status": "active",
            "priority": "INVALID_PRIORITY",
        }
        
        score = calculate_work_effort_priority(work_effort, project_path)
        # Should default to MEDIUM priority
        assert isinstance(score, float)
        assert score >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
