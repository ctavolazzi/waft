#!/usr/bin/env python3
"""
Work Dashboard Generator - Polymorphic Work Dashboard with Neumorphism

Generates an interactive HTML dashboard with WAFT-generated polymorphic action buttons.
The system intelligently analyzes work efforts and projects to determine available actions,
then generates context-aware buttons with beautiful neumorphism styling.

Security: All file operations validated, errors handled gracefully.
Uses proven patterns from existing codebase.
"""

import argparse
import json
import logging
import platform
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

# Import work effort collection from show_me.py
from scripts.show_me import get_projects, get_work_efforts
from src.waft.core.html_realm_network_security import _is_sensitive_file

# Import security functions (proven patterns from codebase)
from src.waft.utils import _validate_path_in_storage

logger = logging.getLogger(__name__)

# Security constants (from existing codebase)
MAX_INDEX_FILE_SIZE = 1 * 1024 * 1024  # 1MB
MAX_FRONTMATTER_SIZE = 10 * 1024  # 10KB (from work_effort_service.py)
MAX_WORK_EFFORTS = 100  # Performance limit


def _validate_work_effort_path(we_dir: Path, project_root: Path) -> bool:
    """Validate work effort directory path is safe (uses existing patterns)."""
    try:
        # Use existing validation pattern from utils.py
        relative_path = we_dir.relative_to(project_root)
        if not _validate_path_in_storage(relative_path, project_root):
            return False

        # Check for sensitive files (from html_realm_network_security.py)
        if _is_sensitive_file(we_dir):
            return False

        # Reject path traversal in directory name
        if ".." in we_dir.parts:
            return False

        # Check for symlinks (security: reject symlinks)
        if we_dir.exists() and we_dir.is_symlink():
            return False

        return True
    except (OSError, ValueError, AttributeError):
        return False


def find_index_file(we_dir: Path, we_id: str) -> Path | None:
    """Find work effort index file with fallback patterns (from show_me.py lines 59-68)."""
    patterns = [f"{we_id}_index.md", f"{we_dir.name}_index.md", "index.md"]

    for pattern in patterns:
        candidate = we_dir / pattern
        if candidate.exists() and _validate_work_effort_path(
            candidate.parent, we_dir.parent.parent
        ):
            return candidate

    return None


def read_work_effort_index(index_file: Path) -> dict[str, Any]:
    """Read and validate work effort index file securely (from work_effort_service.py pattern)."""
    try:
        # Check file size
        if index_file.stat().st_size > MAX_INDEX_FILE_SIZE:
            logger.warning(f"Index file too large: {index_file}")
            return {}

        content = index_file.read_text(encoding="utf-8")

        # Parse YAML frontmatter with size limit (from work_effort_service.py lines 106-132)
        frontmatter = {}
        if "---" in content:
            frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
            if frontmatter_match:
                frontmatter_text = frontmatter_match.group(1)
                if len(frontmatter_text) > MAX_FRONTMATTER_SIZE:
                    logger.warning(f"Frontmatter too large: {index_file}")
                    return {}
                try:
                    frontmatter = yaml.safe_load(frontmatter_text) or {}
                except yaml.YAMLError as e:
                    logger.warning(f"YAML parse error in {index_file}: {e}")
                    return {}

        return frontmatter
    except (OSError, FileNotFoundError, PermissionError) as e:
        logger.warning(f"Error reading index file {index_file}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error reading {index_file}: {e}")
        return {}


def get_recent_git_activity(work_effort_path: Path, days: int = 7) -> list[dict]:
    """Get recent git activity for work effort with validation and timeouts."""
    # Check if git is available
    try:
        subprocess.run(
            ["git", "--version"], shell=False, capture_output=True, check=True, timeout=2
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.CalledProcessError):
        logger.debug("Git not available, skipping git history")
        return []

    # Check if path is in git repository
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=work_effort_path,
            shell=False,
            capture_output=True,
            check=False,
            timeout=2,
        )
        if result.returncode != 0:
            return []  # Not a git repository
    except Exception:
        return []

    # Get recent commits (limit output size)
    try:
        result = subprocess.run(
            [
                "git",
                "log",
                f"--since={days} days ago",
                "--format=%H|%s|%an|%ad",
                "--date=iso",
                "--max-count=10",  # Limit results
                str(work_effort_path),
            ],
            shell=False,
            capture_output=True,
            text=True,
            timeout=5,  # Timeout after 5 seconds
            check=False,
        )
        if result.returncode == 0:
            commits = []
            for line in result.stdout.strip().split("\n"):
                if line:
                    parts = line.split("|", 3)
                    if len(parts) == 4:
                        commits.append(
                            {
                                "hash": parts[0],
                                "message": parts[1],
                                "author": parts[2],
                                "date": parts[3],
                            }
                        )
            return commits
    except subprocess.TimeoutExpired:
        logger.warning("Git log timed out")
    except Exception as e:
        logger.warning(f"Error getting git history: {e}")

    return []


def analyze_work_effort_actions(work_effort: dict, project_path: Path) -> list[dict]:
    """
    Analyze work effort state and generate available actions.

    Security: All file operations validated, errors handled gracefully.
    Uses proven patterns from existing codebase.
    """
    actions = []
    we_id = work_effort.get("id", "")
    we_path = work_effort.get("path", "")
    status = work_effort.get("status", "open")
    we_dir = project_path / we_path

    # SECURITY: Validate work effort ID format before use
    import re

    if not we_id or not re.match(r"^WE-\d{6}-[a-z0-9]{4}$", we_id):
        logger.warning(f"Invalid work effort ID format: {we_id}")
        return actions  # Return empty actions for invalid ID

    # Validate path before any operations
    if not _validate_work_effort_path(we_dir, project_path):
        logger.warning(f"Invalid work effort path: {we_dir}")
        return actions

    # Find and read index file (with fallback patterns)
    index_file = find_index_file(we_dir, we_id)
    if not index_file:
        # No index file - return basic actions
        if status == "open":
            # we_id already validated at function start
            actions.append(
                {
                    "id": "action_start",
                    "label": "Start Work",
                    "icon": "▶️",
                    "action": "status_transition",
                    "command": f"Update work effort {we_id} status to 'active'",  # we_id validated at function start
                    "priority": "high",
                    "available": True,
                    "reason": "Work effort is open and ready to start",
                }
            )
        return actions

    # Read index file securely
    metadata = read_work_effort_index(index_file)
    if not metadata:
        return actions  # Failed to read, return basic actions

    # Read content for keyword analysis
    try:
        content = index_file.read_text(encoding="utf-8")
        content_lower = content.lower()
    except Exception as e:
        logger.warning(f"Error reading content: {e}")
        content_lower = ""

    # Status-based actions
    if status == "open":
        actions.append(
            {
                "id": "action_start",
                "label": "Start Work",
                "icon": "▶️",
                "action": "status_transition",
                "command": f"Update work effort {we_id} status to 'active'",
                "priority": "high",
                "available": True,
                "reason": "Work effort is open and ready to start",
            }
        )
    elif status == "active":
        actions.append(
            {
                "id": "action_progress",
                "label": "Add Progress Note",
                "icon": "📝",
                "action": "add_progress",
                "command": f"Add a progress note to work effort {we_id}",
                "priority": "medium",
                "available": True,
                "reason": "Work effort is active",
            }
        )
        actions.append(
            {
                "id": "action_complete",
                "label": "Mark Complete",
                "icon": "✅",
                "action": "status_transition",
                "command": f"Update work effort {we_id} status to 'completed'",
                "priority": "medium",
                "available": True,
                "reason": "Work effort is active and can be completed",
            }
        )
        actions.append(
            {
                "id": "action_pause",
                "label": "Pause Work",
                "icon": "⏸️",
                "action": "status_transition",
                "command": f"Update work effort {we_id} status to 'paused'",
                "priority": "low",
                "available": True,
                "reason": "Work effort can be paused",
            }
        )
    elif status == "paused":
        actions.append(
            {
                "id": "action_resume",
                "label": "Resume Work",
                "icon": "▶️",
                "action": "status_transition",
                "command": f"Update work effort {we_id} status to 'active'",
                "priority": "high",
                "available": True,
                "reason": "Work effort is paused and can be resumed",
            }
        )

    # Content-based actions
    if "todo" in content_lower:
        actions.append(
            {
                "id": "action_todos",
                "label": "Address TODOs",
                "icon": "✅",
                "action": "review_todos",
                "command": f"Review and address TODOs in work effort {we_id}",
                "priority": "high",
                "available": True,
                "reason": "Work effort contains TODO items",
            }
        )

    if "fixme" in content_lower:
        actions.append(
            {
                "id": "action_fixme",
                "label": "Fix Issues",
                "icon": "🔧",
                "action": "fix_issues",
                "command": f"Fix FIXME items in work effort {we_id}",
                "priority": "high",
                "available": True,
                "reason": "Work effort contains FIXME items",
            }
        )

    # Activity-based actions (with git validation)
    git_activity = get_recent_git_activity(we_dir, days=7)
    if git_activity:
        actions.append(
            {
                "id": "action_review_changes",
                "label": "Review Recent Changes",
                "icon": "🔍",
                "action": "review_changes",
                "command": f"Review recent git changes for work effort {we_id}",
                "priority": "high",
                "available": True,
                "reason": f"Work effort has {len(git_activity)} recent commit(s)",
            }
        )

    # Always available: Review action
    actions.append(
        {
            "id": "action_review",
            "label": "Review & Status Update",
            "icon": "📊",
            "action": "review",
            "command": f"Review work effort {we_id} and provide status update",
            "priority": "medium",
            "available": True,
            "reason": "Review is always available",
        }
    )

    return actions


def generate_neumorphic_css() -> str:
    """Generate complete neumorphism CSS framework with accessibility."""
    return """
:root {
  --neu-bg: #e0e5ec;
  --neu-shadow-light: #ffffff;
  --neu-shadow-dark: #a3b1c6;
  --neu-text: #2d3436;
  --neu-accent: #6c5ce7;
  --neu-success: #00b894;
  --neu-warning: #fdcb6e;
  --neu-danger: #d63031;

  /* Accessibility: Ensure WCAG AA contrast (4.5:1 minimum) */
  --neu-text-contrast: #1a1a1a;
  --neu-focus-ring: 0 0 0 3px rgba(108, 92, 231, 0.3);
  --neu-transition: all 0.2s ease;
}

@media (prefers-color-scheme: dark) {
  :root {
    --neu-bg: #2d3436;
    --neu-shadow-light: #3d4446;
    --neu-shadow-dark: #1d2426;
    --neu-text: #dfe6e9;
    --neu-text-contrast: #ffffff;
  }
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: var(--neu-bg);
  color: var(--neu-text-contrast);
  line-height: 1.6;
  padding: 20px;
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: var(--neu-text-contrast);
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.neumorphic-card {
  background: var(--neu-bg);
  border-radius: 20px;
  box-shadow:
    9px 9px 16px var(--neu-shadow-dark),
    -9px -9px 16px var(--neu-shadow-light);
  padding: 24px;
  position: relative;
}

.neumorphic-button {
  background: var(--neu-bg);
  border: none;
  border-radius: 12px;
  box-shadow:
    6px 6px 12px var(--neu-shadow-dark),
    -6px -6px 12px var(--neu-shadow-light);
  padding: 12px 24px;
  min-height: 44px;
  min-width: 44px;
  transition: var(--neu-transition);
  cursor: pointer;
  font-size: 1rem;
  color: var(--neu-text-contrast);
  font-weight: 500;
  outline: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin: 4px;
}

.neumorphic-button:focus {
  box-shadow: var(--neu-focus-ring),
              6px 6px 12px var(--neu-shadow-dark),
              -6px -6px 12px var(--neu-shadow-light);
}

.neumorphic-button:active {
  box-shadow:
    inset 4px 4px 8px var(--neu-shadow-dark),
    inset -4px -4px 8px var(--neu-shadow-light);
  transform: scale(0.98);
}

.neumorphic-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}

.neumorphic-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow:
    8px 8px 16px var(--neu-shadow-dark),
    -8px -8px 16px var(--neu-shadow-light);
}

.neumorphic-button-primary {
  color: var(--neu-accent);
}

.neumorphic-button-success {
  color: var(--neu-success);
}

.neumorphic-button-warning {
  color: var(--neu-warning);
}

.neumorphic-button-danger {
  color: var(--neu-danger);
}

.neumorphic-badge {
  background: var(--neu-bg);
  border-radius: 8px;
  box-shadow:
    3px 3px 6px var(--neu-shadow-dark),
    -3px -3px 6px var(--neu-shadow-light);
  padding: 4px 12px;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--neu-text-contrast);
  display: inline-block;
  margin: 4px;
}

.work-effort-card {
  margin-bottom: 30px;
}

.work-effort-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.work-effort-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--neu-text-contrast);
}

.work-effort-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
}

.feedback {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 12px 24px;
  border-radius: 12px;
  box-shadow:
    6px 6px 12px var(--neu-shadow-dark),
    -6px -6px 12px var(--neu-shadow-light);
  z-index: 1000;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.feedback.success {
  background: var(--neu-success);
  color: white;
}

.feedback.error {
  background: var(--neu-danger);
  color: white;
}

.feedback.info {
  background: var(--neu-accent);
  color: white;
}

.command-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-content {
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-content textarea {
  width: 100%;
  min-height: 200px;
  margin: 16px 0;
  font-family: monospace;
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .neumorphic-button {
    padding: 10px 16px;
    font-size: 0.9rem;
  }

  .neumorphic-card {
    padding: 16px;
    border-radius: 16px;
  }

  .header h1 {
    font-size: 2rem;
  }
}
"""


def generate_command_queue_js() -> str:
    """Generate JavaScript for clipboard-first command queuing."""
    return """
// Feature detection
const hasClipboardAPI = navigator.clipboard && navigator.clipboard.writeText;

async function queueCommand(action, workEffortId, context) {
  const command = {
    id: `cmd_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    timestamp: new Date().toISOString(),
    work_effort_id: workEffortId,
    ...action,
    context
  };

  const commandText = JSON.stringify(command, null, 2);

  // PRIMARY: Copy to clipboard (works everywhere)
  try {
    if (hasClipboardAPI) {
      await navigator.clipboard.writeText(commandText);
    } else {
      // Fallback: Textarea method (works in all browsers)
      const textarea = document.createElement('textarea');
      textarea.value = commandText;
      textarea.style.position = 'fixed';
      textarea.style.left = '-9999px';
      textarea.setAttribute('aria-hidden', 'true');
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
    }

    showFeedback('✅ Command copied to clipboard. Paste into Cursor.', 'success');
    showCommandModal(commandText);
  } catch (err) {
    showFeedback('❌ Could not copy to clipboard. Showing command for manual copy.', 'error');
    showCommandModal(commandText);
  }

  // OPTIONAL: Try API endpoint if FastAPI server is running
  try {
    const response = await fetch('/api/work-dashboard/queue-command', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: commandText
    });
    if (response.ok) {
      showFeedback('✅ Command also queued via API.', 'info');
    }
  } catch (err) {
    // API not available - clipboard is sufficient
  }
}

function showCommandModal(commandText) {
  const modal = document.createElement('div');
  modal.className = 'command-modal';
  modal.innerHTML = `
    <div class="modal-content neumorphic-card">
      <h3>Command Ready</h3>
      <p>Command has been copied to clipboard. You can also copy it manually:</p>
      <textarea class="neumorphic-input" readonly>${commandText}</textarea>
      <button class="neumorphic-button" onclick="copyFromModal()">Copy Again</button>
      <button class="neumorphic-button" onclick="closeModal()">Close</button>
    </div>
  `;
  modal.id = 'commandModal';
  document.body.appendChild(modal);
}

function copyFromModal() {
  const modal = document.getElementById('commandModal');
  const textarea = modal.querySelector('textarea');
  textarea.select();
  document.execCommand('copy');
  showFeedback('✅ Copied again!', 'success');
}

function closeModal() {
  const modal = document.getElementById('commandModal');
  if (modal) {
    document.body.removeChild(modal);
  }
}

function showFeedback(message, type) {
  const feedback = document.createElement('div');
  feedback.className = `feedback ${type}`;
  feedback.textContent = message;
  document.body.appendChild(feedback);

  setTimeout(() => {
    feedback.style.animation = 'slideIn 0.3s ease reverse';
    setTimeout(() => {
      if (feedback.parentNode) {
        document.body.removeChild(feedback);
      }
    }, 300);
  }, 3000);
}

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeModal();
  }
});
"""


def generate_polymorphic_html(
    work_efforts: list[dict], projects: list[dict], project_path: Path
) -> str:
    """Generate complete HTML with polymorphic buttons and neumorphic styling."""
    # Limit work efforts for performance
    work_efforts = work_efforts[:MAX_WORK_EFFORTS]

    # Analyze actions for each work effort
    work_efforts_with_actions = []
    for we in work_efforts:
        actions = analyze_work_effort_actions(we, project_path)
        we["actions"] = actions
        work_efforts_with_actions.append(we)

    # Generate stats
    stats = {
        "total": len(work_efforts),
        "active": sum(1 for we in work_efforts if we.get("status") == "active"),
        "open": sum(1 for we in work_efforts if we.get("status") == "open"),
        "completed": sum(1 for we in work_efforts if we.get("status") == "completed"),
        "paused": sum(1 for we in work_efforts if we.get("status") == "paused"),
    }

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WAFT Work Dashboard</title>
    <style>
{generate_neumorphic_css()}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>WAFT Work Dashboard</h1>
            <p>Polymorphic Action Buttons - Generated {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>

        <div class="stats">
            <div class="neumorphic-card">
                <h3>Total Work Efforts</h3>
                <p style="font-size: 2rem; font-weight: bold;">{stats["total"]}</p>
            </div>
            <div class="neumorphic-card">
                <h3>Active</h3>
                <p style="font-size: 2rem; font-weight: bold; color: var(--neu-success);">{stats["active"]}</p>
            </div>
            <div class="neumorphic-card">
                <h3>Open</h3>
                <p style="font-size: 2rem; font-weight: bold; color: var(--neu-accent);">{stats["open"]}</p>
            </div>
            <div class="neumorphic-card">
                <h3>Completed</h3>
                <p style="font-size: 2rem; font-weight: bold; color: var(--neu-success);">{stats["completed"]}</p>
            </div>
        </div>

        <div class="work-efforts">
"""

    # Generate work effort cards
    for we in work_efforts_with_actions:
        status = we.get("status", "open")
        status_class = f"status-{status}"

        html += f"""
            <div class="neumorphic-card work-effort-card">
                <div class="work-effort-header">
                    <div>
                        <h2 class="work-effort-title">{we.get("title", we.get("id", "Unknown"))}</h2>
                        <p style="color: var(--neu-text); margin-top: 4px;">{we.get("id", "")}</p>
                    </div>
                    <span class="neumorphic-badge {status_class}">{status.upper()}</span>
                </div>

                <div class="work-effort-actions">
"""

        # Generate action buttons
        for action in we.get("actions", []):
            priority_class = f"neumorphic-button-{action.get('priority', 'medium')}"
            html += f"""
                    <button
                        class="neumorphic-button {priority_class}"
                        onclick="queueCommand({json.dumps(action)}, {json.dumps(we.get("id"))}, {json.dumps(we)})"
                        title="{action.get("reason", "")}"
                        aria-label="{action.get("label", "")}"
                    >
                        <span>{action.get("icon", "")}</span>
                        <span>{action.get("label", "")}</span>
                    </button>
"""

        html += """
                </div>
            </div>
"""

    html += """
        </div>
    </div>

    <script>
"""
    html += generate_command_queue_js()
    html += """
    </script>
</body>
</html>
"""

    return html


def open_in_browser(html_path: Path) -> None:
    """Open HTML file in default browser securely (no shell=True)."""
    # Validate path before use
    if not html_path.exists():
        logger.error(f"HTML file does not exist: {html_path}")
        return

    system = platform.system()
    try:
        if system == "Darwin":  # macOS
            subprocess.run(["open", str(html_path)], shell=False, check=False)
        elif system == "Windows":
            # Use cmd /c start instead of shell=True (SECURITY FIX)
            subprocess.run(["cmd", "/c", "start", "", str(html_path)], shell=False, check=False)
        elif system == "Linux":
            subprocess.run(["xdg-open", str(html_path)], shell=False, check=False)
        else:
            logger.warning(f"Unknown system: {system}, cannot open browser")
    except Exception as e:
        logger.warning(f"Could not open browser: {e}")
        logger.info(f"Open manually: {html_path}")


def main():
    """Main entry point for work dashboard generation."""
    parser = argparse.ArgumentParser(description="Generate WAFT Work Dashboard")
    parser.add_argument(
        "--output",
        type=str,
        default="_work_efforts/work_dashboard.html",
        help="Output HTML file path",
    )
    parser.add_argument(
        "--queue-dir", type=str, default=".cursor/command_queue", help="Command queue directory"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=MAX_WORK_EFFORTS,
        help=f"Maximum work efforts to process (default: {MAX_WORK_EFFORTS})",
    )
    parser.add_argument("--no-open", action="store_true", help="Don't open browser automatically")

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Get project path
    project_path = Path.cwd()

    # Collect work efforts and projects
    logger.info("Collecting work efforts and projects...")
    work_efforts = get_work_efforts(project_path, days_back=0)  # Get all
    projects = get_projects(project_path)

    # Limit work efforts
    work_efforts = work_efforts[: args.limit]

    logger.info(f"Found {len(work_efforts)} work efforts and {len(projects)} projects")

    # Generate HTML
    logger.info("Generating HTML dashboard...")
    html = generate_polymorphic_html(work_efforts, projects, project_path)

    # Write HTML file
    output_path = project_path / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")

    logger.info(f"Dashboard generated: {output_path}")

    # Open in browser
    if not args.no_open:
        logger.info("Opening in browser...")
        open_in_browser(output_path)

    return 0


if __name__ == "__main__":
    exit(main())
