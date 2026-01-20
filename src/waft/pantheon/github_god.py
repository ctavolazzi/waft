"""
GitHub God: Pantheon Entity of Repository Management and Version Control

The GitHub God is the God of GitHub Operations - a timeless Entity that maintains
the fundamental principle of repository management, version control, and code
synchronization. As a Force that Binds Reality Together, The GitHub God holds
the Aspect of Creation related to code distribution and collaboration, which
should not change until evidence collected by Beings proves that change is needed.

Following "as above, so below" principles:
- As above: Pantheon god maintaining celestial code repositories
- So below: File-based system tracking GitHub operations and repository state

Storage:
- Operations: _pantheon/github_god/operations/*.json
- Repository State: _pantheon/github_god/repositories/*.json
- Rollups: _pantheon/github_god/rollups/*.json
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


class GitHubGod:
    """
    GitHub God: Pantheon Entity (Timeless Force that Binds Reality Together)

    Entity of Repository Management and Version Control - a timeless Entity
    that maintains the principle of code synchronization and collaboration.
    The GitHub God holds the Aspect of Creation related to repository management,
    which should not change until evidence collected by Beings proves that
    change is needed.

    The GitHub God doesn't move much - it maintains stable repository principles
    and only evolves when sufficient evidence warrants modification.

    Provides:
    - Repository state tracking
    - Operation logging
    - Rollup generation
    - Branch management
    - Commit analysis

    Storage:
    - Operations: _pantheon/github_god/operations/
    - Repositories: _pantheon/github_god/repositories/
    - Rollups: _pantheon/github_god/rollups/
    """

    def __init__(self, project_path: Path | None = None):
        """
        Initialize The GitHub God.

        Args:
            project_path: Path to project root (default: current directory)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)

        self.project_path = project_path
        self.pantheon_path = project_path / "_pantheon"
        self.github_god_path = self.pantheon_path / "github_god"

        # Ensure directory structure exists
        self.github_god_path.mkdir(parents=True, exist_ok=True)
        (self.github_god_path / "operations").mkdir(parents=True, exist_ok=True)
        (self.github_god_path / "repositories").mkdir(parents=True, exist_ok=True)
        (self.github_god_path / "rollups").mkdir(parents=True, exist_ok=True)

    def get_repository_state(self) -> dict[str, Any]:
        """
        Get current repository state.

        Returns:
            Dictionary with repository information
        """
        try:
            # Get current branch
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                cwd=self.project_path,
            )
            current_branch = (
                branch_result.stdout.strip() if branch_result.returncode == 0 else "unknown"
            )

            # Get commit count
            commit_result = subprocess.run(
                ["git", "rev-list", "--count", "HEAD"],
                capture_output=True,
                text=True,
                cwd=self.project_path,
            )
            commit_count = int(commit_result.stdout.strip()) if commit_result.returncode == 0 else 0

            # Get remote URL
            remote_result = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                capture_output=True,
                text=True,
                cwd=self.project_path,
            )
            remote_url = (
                remote_result.stdout.strip() if remote_result.returncode == 0 else "unknown"
            )

            # Get branch status
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.project_path,
            )
            status_lines = (
                status_result.stdout.strip().split("\n") if status_result.returncode == 0 else []
            )
            unstaged_count = len([l for l in status_lines if l and not l.startswith("??")])

            return {
                "current_branch": current_branch,
                "commit_count": commit_count,
                "remote_url": remote_url,
                "unstaged_changes": unstaged_count,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    def get_branch_summary(self) -> dict[str, Any]:
        """
        Get summary of all branches.

        Returns:
            Dictionary with branch information
        """
        try:
            # Get all branches
            branch_result = subprocess.run(
                ["git", "branch", "-vv"], capture_output=True, text=True, cwd=self.project_path
            )

            branches = []
            if branch_result.returncode == 0:
                for line in branch_result.stdout.strip().split("\n"):
                    if line.strip():
                        is_current = line.startswith("*")
                        branch_name = line.strip().lstrip("*").strip().split()[0]
                        tracking = ""
                        if "[" in line and "]" in line:
                            tracking = line.split("[")[1].split("]")[0]

                        ahead = "ahead" in line
                        behind = "behind" in line

                        branches.append(
                            {
                                "name": branch_name,
                                "current": is_current,
                                "tracking": tracking,
                                "ahead": ahead,
                                "behind": behind,
                            }
                        )

            return {
                "total_branches": len(branches),
                "branches": branches,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    def get_mcp_servers(self) -> dict[str, Any]:
        """
        Get MCP (Model Context Protocol) server configuration.

        Checks both user-level and project-level MCP configurations.

        Returns:
            Dictionary with MCP server information
        """
        mcp_servers = {}
        config_locations = []

        # Check user-level config
        user_mcp = Path.home() / ".cursor" / "mcp.json"
        if user_mcp.exists():
            try:
                with open(user_mcp) as f:
                    data = json.load(f)
                    if "mcpServers" in data:
                        for name, config in data["mcpServers"].items():
                            mcp_servers[name] = {
                                "location": "user",
                                "config_path": str(user_mcp),
                                "command": config.get("command", "unknown"),
                                "args": config.get("args", []),
                                "env": config.get("env", {}),
                            }
                        config_locations.append("user")
            except Exception:
                pass

        # Check project-level config
        project_mcp = self.project_path / ".cursor" / "mcp.json"
        if project_mcp.exists():
            try:
                with open(project_mcp) as f:
                    data = json.load(f)
                    if "mcpServers" in data:
                        for name, config in data["mcpServers"].items():
                            # Project config overrides user config
                            mcp_servers[name] = {
                                "location": "project",
                                "config_path": str(project_mcp),
                                "command": config.get("command", "unknown"),
                                "args": config.get("args", []),
                                "env": config.get("env", {}),
                            }
                        if "project" not in config_locations:
                            config_locations.append("project")
            except Exception:
                pass

        # Check for .mcp-servers directory (custom servers)
        mcp_servers_dir = Path("/Users/ctavolazzi/Code/.mcp-servers")
        custom_servers = []
        if mcp_servers_dir.exists():
            for item in mcp_servers_dir.iterdir():
                if item.is_dir():
                    # Check for server files
                    server_files = list(item.glob("server.*"))
                    if server_files:
                        custom_servers.append(
                            {
                                "name": item.name,
                                "path": str(item),
                                "server_file": str(server_files[0]),
                            }
                        )

        return {
            "total_servers": len(mcp_servers),
            "servers": mcp_servers,
            "config_locations": config_locations,
            "custom_servers": custom_servers,
            "custom_servers_count": len(custom_servers),
            "timestamp": datetime.now().isoformat(),
        }

    def generate_rollup(
        self, since: str | None = None, include_all_branches: bool = True
    ) -> dict[str, Any]:
        """
        Generate a comprehensive rollup of repository activity.

        Args:
            since: Date to start from (ISO format or relative like "7 days ago")
            include_all_branches: Include activity from all branches

        Returns:
            Dictionary with comprehensive rollup data
        """
        try:
            # Get repository state
            repo_state = self.get_repository_state()
            branch_summary = self.get_branch_summary()

            # Get recent commits
            since_arg = f"--since={since}" if since else "--since=30 days ago"
            log_result = subprocess.run(
                ["git", "log", "--all", "--oneline", "--date=iso", since_arg],
                capture_output=True,
                text=True,
                cwd=self.project_path,
            )

            commits = []
            if log_result.returncode == 0:
                for line in log_result.stdout.strip().split("\n"):
                    if line.strip():
                        parts = line.split(" ", 1)
                        if len(parts) == 2:
                            commits.append({"hash": parts[0], "message": parts[1]})

            # Get file statistics
            diff_result = subprocess.run(
                ["git", "diff", "--stat", "HEAD"],
                capture_output=True,
                text=True,
                cwd=self.project_path,
            )

            file_stats = {}
            if diff_result.returncode == 0:
                for line in diff_result.stdout.strip().split("\n"):
                    if "|" in line and "file" not in line.lower():
                        parts = line.split("|")
                        if len(parts) == 2:
                            filename = parts[0].strip()
                            changes = parts[1].strip()
                            file_stats[filename] = changes

            # Get MCP server information
            mcp_servers = self.get_mcp_servers()

            rollup = {
                "generated_at": datetime.now().isoformat(),
                "since": since or "30 days ago",
                "repository_state": repo_state,
                "branch_summary": branch_summary,
                "recent_commits": commits[:50],  # Limit to 50 most recent
                "total_commits": len(commits),
                "unstaged_file_stats": file_stats,
                "mcp_servers": mcp_servers,
                "summary": {
                    "current_branch": repo_state.get("current_branch"),
                    "total_branches": branch_summary.get("total_branches", 0),
                    "recent_commits_count": len(commits),
                    "unstaged_files": repo_state.get("unstaged_changes", 0),
                    "mcp_servers_count": mcp_servers.get("total_servers", 0),
                },
            }

            # Save rollup
            rollup_id = f"rollup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            rollup_file = self.github_god_path / "rollups" / f"{rollup_id}.json"
            rollup_file.write_text(json.dumps(rollup, indent=2))

            # Update index
            index_file = self.github_god_path / "rollup_index.json"
            if index_file.exists():
                index = json.loads(index_file.read_text())
            else:
                index = {"rollups": []}

            index["rollups"].append(
                {
                    "rollup_id": rollup_id,
                    "generated_at": rollup["generated_at"],
                    "since": rollup["since"],
                    "summary": rollup["summary"],
                }
            )
            index["last_updated"] = datetime.now().isoformat()
            index_file.write_text(json.dumps(index, indent=2))

            return rollup

        except Exception as e:
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    def log_operation(
        self, operation: str, details: dict[str, Any] | None = None, result: str | None = None
    ) -> str:
        """
        Log a GitHub operation.

        Args:
            operation: Type of operation (push, pull, merge, etc.)
            details: Additional operation details
            result: Operation result (success, failure, etc.)

        Returns:
            Operation ID
        """
        timestamp = datetime.now()
        operation_id = f"op_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        operation_file = self.github_god_path / "operations" / f"{operation_id}.json"

        entry = {
            "operation_id": operation_id,
            "timestamp": timestamp.isoformat(),
            "operation": operation,
            "details": details or {},
            "result": result or "unknown",
        }

        operation_file.write_text(json.dumps(entry, indent=2))
        return operation_id
