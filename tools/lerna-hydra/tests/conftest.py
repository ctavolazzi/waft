"""Shared fixtures for Lerna Hydra tests."""
import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def sandbox_dir(tmp_path):
    """Provide a temporary sandbox directory with a starter index.html."""
    sandbox = tmp_path / "sandbox"
    sandbox.mkdir()
    (sandbox / "index.html").write_text(
        "<html><body><h1>Sandbox</h1></body></html>"
    )
    (sandbox / "README.md").write_text("# Test Sandbox\n")
    (sandbox / "src").mkdir()
    (sandbox / "src" / "main.py").write_text("print('hello')\n")
    return sandbox


@pytest.fixture
def empty_sandbox(tmp_path):
    """Provide an empty temporary sandbox directory."""
    sandbox = tmp_path / "empty"
    sandbox.mkdir()
    return sandbox
