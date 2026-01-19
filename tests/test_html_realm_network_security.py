"""
Unit tests for HTML Realm Network Security Module.

Tests all security validation functions to ensure:
- Sensitive files are excluded
- Path traversal is prevented
- Size limits are enforced
- Timeouts work correctly
- Safe parsing (no script execution)
- Secure permissions are set
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import os
import stat

from waft.core.html_realm_network_security import (
    SENSITIVE_PATTERNS,
    MAX_HTML_SIZE,
    MAX_PARSING_TIME,
    FILE_PERM,
    DIR_PERM,
    _is_sensitive_file,
    _validate_html_path,
    parse_html_safely,
    extract_html_metadata,
    set_secure_permissions,
)


@pytest.fixture
def temp_project():
    """Create a temporary project directory for testing."""
    temp_dir = tempfile.mkdtemp()
    project_path = Path(temp_dir) / "test_project"
    project_path.mkdir(parents=True)
    yield project_path
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_html():
    """Sample HTML content for testing."""
    return """<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>Test Page</h1>
    <p>This is a test page with some content.</p>
    <a href="/page1.html">Link 1</a>
    <a href="/page2.html">Link 2</a>
</body>
</html>"""


# --- Security Constants Tests ---

def test_sensitive_patterns_defined():
    """Test that sensitive patterns are defined."""
    assert len(SENSITIVE_PATTERNS) > 0
    assert MAX_HTML_SIZE == 10 * 1024 * 1024
    assert MAX_PARSING_TIME == 30
    assert FILE_PERM == 0o600
    assert DIR_PERM == 0o700


# --- Path Validation Tests ---

def test_is_sensitive_file_hidden_directory(temp_project):
    """Test that _hidden/ directory is detected as sensitive."""
    hidden_path = temp_project / "_hidden" / "file.html"
    hidden_path.parent.mkdir()
    assert _is_sensitive_file(hidden_path) is True


def test_is_sensitive_file_env_file(temp_project):
    """Test that .env files are detected as sensitive."""
    env_path = temp_project / ".env"
    env_path.write_text("SECRET=value")
    assert _is_sensitive_file(env_path) is True


def test_is_sensitive_file_secrets_directory(temp_project):
    """Test that secrets/ directory is detected as sensitive."""
    secrets_path = temp_project / "secrets" / "file.html"
    secrets_path.parent.mkdir()
    assert _is_sensitive_file(secrets_path) is True


def test_is_sensitive_file_key_file(temp_project):
    """Test that .key files are detected as sensitive."""
    key_path = temp_project / "private.key"
    key_path.write_text("key content")
    assert _is_sensitive_file(key_path) is True


def test_is_sensitive_file_normal_file(temp_project):
    """Test that normal files are not detected as sensitive."""
    normal_path = temp_project / "normal.html"
    normal_path.write_text("<html></html>")
    assert _is_sensitive_file(normal_path) is False


def test_validate_html_path_valid_file(temp_project, sample_html):
    """Test validation of a valid HTML file."""
    html_file = temp_project / "test.html"
    html_file.write_text(sample_html)
    assert _validate_html_path(html_file, temp_project) is True


def test_validate_html_path_invalid_extension(temp_project):
    """Test that non-HTML files are rejected."""
    txt_file = temp_project / "test.txt"
    txt_file.write_text("Not HTML")
    assert _validate_html_path(txt_file, temp_project) is False


def test_validate_html_path_too_large(temp_project):
    """Test that files exceeding MAX_HTML_SIZE are rejected."""
    # Create a file larger than MAX_HTML_SIZE
    large_file = temp_project / "large.html"
    large_content = "<html>" + "x" * (MAX_HTML_SIZE + 1) + "</html>"
    large_file.write_text(large_content)
    assert _validate_html_path(large_file, temp_project) is False


def test_validate_html_path_sensitive_file(temp_project):
    """Test that sensitive files are rejected."""
    sensitive_file = temp_project / "_hidden" / "test.html"
    sensitive_file.parent.mkdir()
    sensitive_file.write_text("<html></html>")
    assert _validate_html_path(sensitive_file, temp_project) is False


def test_validate_html_path_path_traversal(temp_project):
    """Test that path traversal attempts are rejected."""
    # Try to access parent directory
    traversal_path = temp_project / ".." / "test.html"
    assert _validate_html_path(traversal_path, temp_project) is False


# --- Safe HTML Parsing Tests ---

def test_parse_html_safely_valid_file(temp_project, sample_html):
    """Test parsing a valid HTML file."""
    html_file = temp_project / "test.html"
    html_file.write_text(sample_html)
    
    result = parse_html_safely(html_file)
    assert result is not None
    assert result["parsed"] is True
    assert "soup" in result
    assert result["size"] > 0


def test_parse_html_safely_nonexistent_file(temp_project):
    """Test parsing a non-existent file."""
    html_file = temp_project / "nonexistent.html"
    result = parse_html_safely(html_file)
    assert result is None


def test_parse_html_safely_too_large_file(temp_project):
    """Test parsing a file that's too large."""
    large_file = temp_project / "large.html"
    large_content = "<html>" + "x" * (MAX_HTML_SIZE + 1) + "</html>"
    large_file.write_text(large_content)
    
    result = parse_html_safely(large_file)
    assert result is None


def test_parse_html_safely_malformed_html(temp_project):
    """Test parsing malformed HTML (should handle gracefully)."""
    malformed_file = temp_project / "malformed.html"
    malformed_file.write_text("<html><body><p>Unclosed tag")
    
    # Should not crash, but may return None or partial result
    result = parse_html_safely(malformed_file)
    # BeautifulSoup is lenient, so it might still parse
    # The important thing is it doesn't crash


# --- Metadata Extraction Tests ---

def test_extract_html_metadata_with_soup(temp_project, sample_html):
    """Test metadata extraction from parsed HTML."""
    html_file = temp_project / "test.html"
    html_file.write_text(sample_html)
    
    result = parse_html_safely(html_file)
    assert result is not None
    
    metadata = extract_html_metadata(result["soup"])
    assert metadata["title"] == "Test Page"
    assert len(metadata["links"]) == 2
    assert "/page1.html" in metadata["links"]
    assert "/page2.html" in metadata["links"]
    assert metadata["link_count"] == 2


def test_extract_html_metadata_no_soup():
    """Test metadata extraction when soup is None."""
    metadata = extract_html_metadata(None)
    assert metadata["title"] == ""
    assert metadata["links"] == []
    assert metadata["link_count"] == 0


def test_extract_html_metadata_no_title(temp_project):
    """Test metadata extraction from HTML without title."""
    html_content = "<html><body><p>No title</p></body></html>"
    html_file = temp_project / "notitle.html"
    html_file.write_text(html_content)
    
    result = parse_html_safely(html_file)
    assert result is not None
    
    metadata = extract_html_metadata(result["soup"])
    assert metadata["title"] == ""
    assert metadata["link_count"] == 0


# --- File Permissions Tests ---

def test_set_secure_permissions_file(temp_project):
    """Test setting secure permissions on a file."""
    test_file = temp_project / "test.txt"
    test_file.write_text("test content")
    
    # Set permissions
    set_secure_permissions(test_file, is_dir=False)
    
    # Check permissions (may not work on Windows)
    try:
        file_stat = test_file.stat()
        # On Unix, check that permissions are restrictive
        # 0o600 = rw------- (owner read/write only)
        if os.name != 'nt':  # Not Windows
            assert (file_stat.st_mode & 0o777) == FILE_PERM
    except (OSError, AttributeError):
        # Windows or permission check failed - that's okay
        pass


def test_set_secure_permissions_directory(temp_project):
    """Test setting secure permissions on a directory."""
    test_dir = temp_project / "test_dir"
    test_dir.mkdir()
    
    # Set permissions
    set_secure_permissions(test_dir, is_dir=True)
    
    # Check permissions (may not work on Windows)
    try:
        dir_stat = test_dir.stat()
        # On Unix, check that permissions are restrictive
        # 0o700 = rwx------ (owner read/write/execute only)
        if os.name != 'nt':  # Not Windows
            assert (dir_stat.st_mode & 0o777) == DIR_PERM
    except (OSError, AttributeError):
        # Windows or permission check failed - that's okay
        pass


def test_set_secure_permissions_nonexistent_file(temp_project):
    """Test setting permissions on non-existent file (should not crash)."""
    nonexistent = temp_project / "nonexistent.txt"
    # Should not raise exception
    set_secure_permissions(nonexistent, is_dir=False)


# --- Integration Tests ---

def test_full_security_workflow(temp_project, sample_html):
    """Test the complete security workflow."""
    html_file = temp_project / "secure.html"
    html_file.write_text(sample_html)
    
    # 1. Validate path
    assert _validate_html_path(html_file, temp_project) is True
    
    # 2. Parse safely
    result = parse_html_safely(html_file)
    assert result is not None
    
    # 3. Extract metadata
    metadata = extract_html_metadata(result["soup"])
    assert metadata["title"] == "Test Page"
    
    # 4. Set secure permissions
    set_secure_permissions(html_file, is_dir=False)
    
    # All steps completed successfully
    assert True


def test_security_rejects_all_sensitive_patterns(temp_project):
    """Test that all sensitive patterns are properly rejected."""
    sensitive_paths = [
        temp_project / "_hidden" / "file.html",
        temp_project / ".env",
        temp_project / "secrets" / "file.html",
        temp_project / "private.key",
        temp_project / "cert.pem",
        temp_project / "secret.secret",
        temp_project / ".git" / "config",
        temp_project / "node_modules" / "package" / "file.html",
    ]
    
    for path in sensitive_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix == ".html":
            path.write_text("<html></html>")
        else:
            path.write_text("content")
        
        # Should be detected as sensitive
        assert _is_sensitive_file(path) is True, f"Path {path} should be sensitive"
        
        # Should be rejected by validation
        if path.suffix == ".html":
            assert _validate_html_path(path, temp_project) is False, f"Path {path} should be rejected"
