"""
Utility functions for Streamlit UI.
"""

import streamlit as st
from pathlib import Path
from typing import Optional, Dict, Any
import subprocess
import json
import shlex
import re


# Whitelist of allowed WAFT CLI commands
ALLOWED_COMMANDS = {
    "waft verify",
    "waft info",
    "waft sync",
    "waft status",
    "waft session status",
    "waft assess",
    "waft check",
    "waft dashboard",
    "waft stats",
    "waft character",
    "waft chronicle",
}


def run_cli_command(command: str, project_path: Path) -> Dict[str, Any]:
    """
    Run a WAFT CLI command and return results.
    
    Security: Validates command format and whitelists allowed commands
    to prevent command injection attacks.
    
    Args:
        command: CLI command to run (e.g., "waft verify")
        project_path: Project path
        
    Returns:
        Dict with 'success', 'output', 'error' keys
    """
    # Validate command format
    if not command or not isinstance(command, str):
        return {
            "success": False,
            "output": "",
            "error": "Invalid command: must be a non-empty string",
            "returncode": -1
        }
    
    # Strip whitespace
    command = command.strip()
    
    # Must start with "waft "
    if not command.startswith("waft "):
        return {
            "success": False,
            "output": "",
            "error": "Invalid command: must start with 'waft '",
            "returncode": -1
        }
    
    # Check against whitelist
    if command not in ALLOWED_COMMANDS:
        return {
            "success": False,
            "output": "",
            "error": f"Command not allowed. Allowed commands: {', '.join(sorted(ALLOWED_COMMANDS))}",
            "returncode": -1
        }
    
    # Additional validation: ensure no shell metacharacters
    if re.search(r'[;&|`$(){}[\]<>]', command):
        return {
            "success": False,
            "output": "",
            "error": "Invalid command: contains illegal characters",
            "returncode": -1
        }
    
    try:
        # Use shlex.split for safe command parsing
        safe_command = shlex.split(command)
        
        result = subprocess.run(
            safe_command,
            cwd=str(project_path),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "Command timed out after 30 seconds",
            "returncode": -1
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e),
            "returncode": -1
        }


def display_error(error: str, title: str = "Error"):
    """Display an error message in Streamlit."""
    st.error(f"**{title}**: {error}")


def display_success(message: str, title: str = "Success"):
    """Display a success message in Streamlit."""
    st.success(f"**{title}**: {message}")


def display_info(message: str, title: str = "Info"):
    """Display an info message in Streamlit."""
    st.info(f"**{title}**: {message}")


def format_json(data: Any) -> str:
    """Format data as JSON string."""
    return json.dumps(data, indent=2, default=str)


def load_json_file(file_path: Path) -> Optional[Dict]:
    """Load JSON file safely."""
    try:
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return None


def save_json_file(file_path: Path, data: Dict) -> bool:
    """Save data to JSON file safely."""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception:
        return False
