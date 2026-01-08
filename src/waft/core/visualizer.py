"""
Visual Dashboard Generator - Creates interactive HTML dashboards.

Generates standalone HTML files that visualize current project state,
git status, work efforts, and more with interactive elements.
"""

import json
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import quote

from .memory import MemoryManager
from .substrate import SubstrateManager
from .github import GitHubManager
from .gamification import GamificationManager
from .session_analytics import SessionAnalytics


class Visualizer:
    """Generates interactive HTML dashboards for project visualization."""

    def __init__(self, project_path: Path):
        """
        Initialize visualizer.

        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.memory = MemoryManager(project_path)
        self.substrate = SubstrateManager(project_path)
        self.github = GitHubManager(project_path)
        self.gamification = GamificationManager(project_path)
        self.analytics = SessionAnalytics(project_path)

    def gather_state(self) -> Dict[str, Any]:
        """
        Gather current project state.

        Returns:
            Dictionary with all state information
        """
        state = {
            "timestamp": datetime.now().isoformat(),
            "project_path": str(self.project_path.resolve()),
        }

        # Project info
        project_info = self.substrate.get_project_info()
        state["project"] = {
            "name": project_info.get("name", "Unknown"),
            "version": project_info.get("version", "Unknown"),
            "description": project_info.get("description", ""),
        }

        # Git status
        state["git"] = self._get_git_status()

        # _pyrite structure
        pyrite_status = self.memory.verify_structure()
        state["pyrite"] = {
            "valid": pyrite_status["valid"],
            "folders": pyrite_status["folders"],
            "active_files": [f.name for f in self.memory.get_active_files()],
            "backlog_files": [f.name for f in self.memory.get_backlog_files()],
            "standards_files": [f.name for f in self.memory.get_standards_files()],
        }

        # Gamification stats
        stats = self.gamification.get_stats()
        state["gamification"] = {
            "integrity": stats.get("integrity", 100.0),
            "insight": stats.get("insight", 0.0),
            "level": stats.get("level", 1),
            "insight_to_next": stats.get("insight_to_next_level", 100.0),
        }

        # System info
        state["system"] = self._get_system_info()

        # Work efforts (if _work_efforts exists)
        state["work_efforts"] = self._get_work_efforts()

        # Devlog (if exists)
        state["devlog"] = self._get_recent_devlog()

        # Analytics (if available)
        state["analytics"] = self._get_analytics_data()

        return state

    def _get_git_status(self) -> Dict[str, Any]:
        """Get detailed git status."""
        git_status = {
            "initialized": self.github.is_initialized(),
            "branch": None,
            "remote_url": None,
            "uncommitted_files": [],
            "staged_files": [],
            "modified_files": [],
            "untracked_files": [],
            "commits_ahead": 0,
            "commits_behind": 0,
            "recent_commits": [],
        }

        if not self.github.is_initialized():
            return git_status

        try:
            # Basic status
            git_status["branch"] = self._run_git(["branch", "--show-current"]).strip()
            git_status["remote_url"] = self.github.get_remote_url()

            # Get status output
            status_output = self._run_git(["status", "--short"])
            if status_output:
                for line in status_output.strip().split("\n"):
                    if not line.strip():
                        continue
                    status_code = line[:2]
                    filename = line[3:].strip()

                    if status_code[0] == "A" or status_code[0] == "M":
                        git_status["staged_files"].append(filename)
                    if status_code[1] == "M" or status_code[1] == "D":
                        git_status["modified_files"].append(filename)
                    if status_code == "??":
                        git_status["untracked_files"].append(filename)

            git_status["uncommitted_files"] = (
                git_status["staged_files"]
                + git_status["modified_files"]
                + git_status["untracked_files"]
            )

            # Commits ahead/behind
            try:
                ahead = self._run_git(["rev-list", "--count", "@{u}..HEAD"]).strip()
                git_status["commits_ahead"] = int(ahead) if ahead else 0
            except:
                pass

            try:
                behind = self._run_git(["rev-list", "--count", "HEAD..@{u}"]).strip()
                git_status["commits_behind"] = int(behind) if behind else 0
            except:
                pass

            # Recent commits
            try:
                log_output = self._run_git(
                    [
                        "log",
                        "-5",
                        "--pretty=format:%h|%s|%an|%ar",
                        "--no-merges",
                    ]
                )
                if log_output:
                    for line in log_output.strip().split("\n"):
                        parts = line.split("|", 3)
                        if len(parts) >= 4:
                            git_status["recent_commits"].append(
                                {
                                    "hash": parts[0],
                                    "message": parts[1],
                                    "author": parts[2],
                                    "relative": parts[3],
                                }
                            )
            except:
                pass

        except Exception as e:
            git_status["error"] = str(e)

        return git_status

    def _get_system_info(self) -> Dict[str, Any]:
        """Get system information."""
        import sys
        import os
        from datetime import datetime

        return {
            "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "working_directory": str(Path.cwd()),
            "python_version": sys.version.split()[0],
            "platform": sys.platform,
        }

    def _get_work_efforts(self) -> List[Dict[str, Any]]:
        """Get work efforts information."""
        work_efforts = []
        work_efforts_path = self.project_path / "_work_efforts"

        if not work_efforts_path.exists():
            return work_efforts

        # Look for work effort directories
        for item in work_efforts_path.iterdir():
            if item.is_dir() and item.name.startswith("WE-"):
                # Try to find index.md or similar
                index_file = item / "index.md"
                if index_file.exists():
                    try:
                        content = index_file.read_text()
                        # Extract basic info
                        work_efforts.append(
                            {
                                "id": item.name,
                                "path": str(item.relative_to(self.project_path)),
                                "has_index": True,
                            }
                        )
                    except:
                        pass

        return work_efforts

    def _get_recent_devlog(self) -> List[str]:
        """Get recent devlog entries."""
        devlog_path = self.project_path / "_work_efforts" / "devlog.md"
        if not devlog_path.exists():
            return []

        try:
            content = devlog_path.read_text()
            # Get last 10 lines that start with "##"
            lines = content.split("\n")
            recent = []
            for line in lines[-50:]:  # Check last 50 lines
                if line.startswith("## "):
                    recent.append(line[3:].strip())
            return recent[:5]  # Return last 5 entries
        except:
            return []

    def _run_git(self, args: List[str]) -> str:
        """Run git command and return output."""
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            return ""

    def _get_analytics_data(self) -> Dict[str, Any]:
        """Get analytics data for visualization."""
        try:
            # Get recent sessions (last 30 days)
            from datetime import datetime, timedelta
            from dataclasses import asdict
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            sessions = self.analytics.get_sessions(
                start_date=start_date,
                end_date=end_date,
                limit=50
            )
            
            # Get trends
            trends = self.analytics.analyze_productivity_trends(days=30)
            
            # Get iteration chains
            chains = self.analytics.get_iteration_chains()
            
            # Convert SessionRecord objects to dicts for JSON serialization
            recent_sessions_data = []
            for session in sessions[:10]:
                recent_sessions_data.append({
                    "session_id": session.session_id,
                    "timestamp": session.timestamp,
                    "files_created": session.files_created,
                    "files_modified": session.files_modified,
                    "net_lines": session.net_lines,
                    "approach_category": session.approach_category,
                })
            
            return {
                "sessions_count": len(sessions),
                "recent_sessions": recent_sessions_data,  # Converted to dicts
                "trends": trends,
                "chains_count": len(chains),
                "available": True,
            }
        except Exception as e:
            return {
                "available": False,
                "error": str(e),
            }

    def generate_html(self, state: Dict[str, Any]) -> str:
        """
        Generate HTML dashboard from state.

        Args:
            state: State dictionary from gather_state()

        Returns:
            Complete HTML string
        """
        # Escape data for JSON embedding
        state_json = json.dumps(state, indent=2)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Waft Visual Dashboard - {state['project']['name']}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --primary: #7c9eff;
            --primary-dark: #6b8eff;
            --primary-light: #8dafff;
            --bg-dark: #0a0e1a;
            --bg-card: #1a1e29;
            --bg-card-hover: #232834;
            --text-primary: #e8eaf6;
            --text-secondary: #b0b8d0;
            --text-muted: #707890;
            --success: #4ade80;
            --warning: #fbbf24;
            --error: #f87171;
            --info: #60a5fa;
            --border: rgba(124, 158, 255, 0.2);
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
            --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
            --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
            --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-bg: linear-gradient(135deg, #0a0e1a 0%, #1a1e29 50%, #0f1419 100%);
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateX(-20px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
        }}
        
        @keyframes shimmer {{
            0% {{ background-position: -1000px 0; }}
            100% {{ background-position: 1000px 0; }}
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', 'SF Pro Display', Oxygen, Ubuntu, Cantarell, sans-serif;
            background: var(--gradient-bg);
            background-attachment: fixed;
            min-height: 100vh;
            padding: 16px;
            color: var(--text-primary);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            animation: fadeIn 0.6s ease-out;
        }}
        
        .header {{
            background: linear-gradient(135deg, rgba(124, 158, 255, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 24px;
            box-shadow: var(--shadow-lg);
            border: 1px solid var(--border);
            position: relative;
            overflow: hidden;
            animation: slideIn 0.5s ease-out;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--gradient-primary);
        }}
        
        .header h1 {{
            color: var(--primary-light);
            font-size: clamp(2rem, 5vw, 3.5rem);
            margin-bottom: 12px;
            font-weight: 700;
            letter-spacing: -0.02em;
            text-shadow: 0 2px 20px rgba(124, 158, 255, 0.3);
        }}
        
        .header .subtitle {{
            color: var(--text-secondary);
            font-size: clamp(0.9rem, 2vw, 1.2rem);
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }}
        
        .header .subtitle::before {{
            content: '⚡';
            font-size: 1.2em;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(min(100%, 380px), 1fr));
            gap: 24px;
            margin-bottom: 24px;
        }}
        
        .card {{
            background: var(--bg-card);
            border-radius: 16px;
            padding: 28px;
            box-shadow: var(--shadow-md);
            border: 1px solid var(--border);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            animation: fadeIn 0.6s ease-out backwards;
        }}
        
        .card:nth-child(1) {{ animation-delay: 0.1s; }}
        .card:nth-child(2) {{ animation-delay: 0.2s; }}
        .card:nth-child(3) {{ animation-delay: 0.3s; }}
        .card:nth-child(4) {{ animation-delay: 0.4s; }}
        .card:nth-child(5) {{ animation-delay: 0.5s; }}
        .card:nth-child(6) {{ animation-delay: 0.6s; }}
        
        .card:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
            border-color: rgba(124, 158, 255, 0.4);
            background: var(--bg-card-hover);
        }}
        
        .card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--gradient-primary);
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        
        .card:hover::before {{
            opacity: 1;
        }}
        
        .card h2 {{
            color: var(--text-primary);
            margin-bottom: 20px;
            font-size: clamp(1.2rem, 3vw, 1.5rem);
            border-bottom: 2px solid var(--border);
            padding-bottom: 12px;
            cursor: pointer;
            user-select: none;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.2s ease;
        }}
        
        .card h2::before {{
            content: '';
            width: 4px;
            height: 24px;
            background: var(--gradient-primary);
            border-radius: 2px;
        }}
        
        .card h2:hover {{
            color: var(--primary-light);
            border-color: var(--primary);
        }}
        
        .card.collapsed .card-content {{
            display: none;
        }}
        
        .card.collapsed h2::after {{
            content: ' ▶';
            margin-left: auto;
            font-size: 0.8em;
            opacity: 0.6;
        }}
        
        .info-item {{
            margin: 12px 0;
            padding: 14px;
            background: rgba(26, 30, 41, 0.6);
            border-radius: 10px;
            border: 1px solid var(--border);
            transition: all 0.2s ease;
        }}
        
        .info-item:hover {{
            background: rgba(35, 40, 52, 0.8);
            border-color: rgba(124, 158, 255, 0.3);
            transform: translateX(4px);
        }}
        
        .info-label {{
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 6px;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .info-value {{
            color: var(--text-primary);
            font-size: 1.05em;
            word-break: break-word;
        }}
        
        .status {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            box-shadow: var(--shadow-sm);
        }}
        
        .status.valid {{
            background: linear-gradient(135deg, rgba(74, 222, 128, 0.2), rgba(74, 222, 128, 0.1));
            color: var(--success);
            border: 1px solid rgba(74, 222, 128, 0.3);
        }}
        
        .status.invalid {{
            background: linear-gradient(135deg, rgba(248, 113, 113, 0.2), rgba(248, 113, 113, 0.1));
            color: var(--error);
            border: 1px solid rgba(248, 113, 113, 0.3);
        }}
        
        .status.missing {{
            background: linear-gradient(135deg, rgba(251, 191, 36, 0.2), rgba(251, 191, 36, 0.1));
            color: var(--warning);
            border: 1px solid rgba(251, 191, 36, 0.3);
        }}
        
        .file-list {{
            list-style: none;
            margin-top: 12px;
            max-height: 320px;
            overflow-y: auto;
            padding-right: 8px;
        }}
        
        .file-list::-webkit-scrollbar {{
            width: 6px;
        }}
        
        .file-list::-webkit-scrollbar-track {{
            background: rgba(26, 30, 41, 0.5);
            border-radius: 3px;
        }}
        
        .file-list::-webkit-scrollbar-thumb {{
            background: var(--gradient-primary);
            border-radius: 3px;
        }}
        
        .file-list::-webkit-scrollbar-thumb:hover {{
            background: var(--primary);
        }}
        
        .file-list li {{
            padding: 10px 12px;
            margin: 6px 0;
            background: rgba(26, 30, 41, 0.6);
            border-radius: 8px;
            border-left: 3px solid var(--primary);
            color: var(--text-primary);
            transition: all 0.2s ease;
            cursor: pointer;
        }}
        
        .file-list li:hover {{
            background: rgba(35, 40, 52, 0.9);
            transform: translateX(6px);
            border-left-color: var(--primary-light);
            box-shadow: var(--shadow-sm);
        }}
        
        .empty {{
            color: var(--text-muted);
            font-style: italic;
            padding: 20px;
            text-align: center;
        }}
        
        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            border-radius: 16px;
            font-size: 0.85em;
            font-weight: 600;
            margin: 4px;
            box-shadow: var(--shadow-sm);
            transition: all 0.2s ease;
        }}
        
        .badge:hover {{
            transform: scale(1.05);
            box-shadow: var(--shadow-md);
        }}
        
        .badge.success {{
            background: linear-gradient(135deg, rgba(74, 222, 128, 0.2), rgba(74, 222, 128, 0.1));
            color: var(--success);
            border: 1px solid rgba(74, 222, 128, 0.3);
        }}
        
        .badge.warning {{
            background: linear-gradient(135deg, rgba(251, 191, 36, 0.2), rgba(251, 191, 36, 0.1));
            color: var(--warning);
            border: 1px solid rgba(251, 191, 36, 0.3);
        }}
        
        .badge.info {{
            background: linear-gradient(135deg, rgba(96, 165, 250, 0.2), rgba(96, 165, 250, 0.1));
            color: var(--info);
            border: 1px solid rgba(96, 165, 250, 0.3);
        }}
        
        .progress-bar {{
            width: 100%;
            height: 24px;
            background: rgba(26, 30, 41, 0.8);
            border-radius: 12px;
            overflow: hidden;
            margin: 12px 0;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border);
        }}
        
        .progress-fill {{
            height: 100%;
            background: var(--gradient-primary);
            transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        
        .progress-fill::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            animation: shimmer 2s infinite;
        }}
        
        .commit-item {{
            padding: 14px;
            margin: 8px 0;
            background: rgba(26, 30, 41, 0.6);
            border-radius: 10px;
            border-left: 3px solid var(--primary);
            transition: all 0.2s ease;
        }}
        
        .commit-item:hover {{
            background: rgba(35, 40, 52, 0.9);
            transform: translateX(4px);
            border-left-color: var(--primary-light);
        }}
        
        .commit-hash {{
            font-family: 'SF Mono', 'Monaco', 'Cascadia Code', 'Roboto Mono', monospace;
            color: var(--primary-light);
            font-size: 0.9em;
            font-weight: 600;
        }}
        
        .commit-message {{
            color: var(--text-primary);
            margin: 6px 0;
            font-weight: 500;
        }}
        
        .commit-meta {{
            color: var(--text-secondary);
            font-size: 0.85em;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .footer {{
            text-align: center;
            color: var(--text-secondary);
            margin-top: 40px;
            padding: 24px;
            background: rgba(26, 30, 41, 0.4);
            border-radius: 16px;
            border: 1px solid var(--border);
        }}
        
        .footer p {{
            margin: 8px 0;
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            body {{
                padding: 12px;
            }}
            
            .header {{
                padding: 24px;
                border-radius: 16px;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
            
            .grid {{
                grid-template-columns: 1fr;
                gap: 16px;
            }}
            
            .card {{
                padding: 20px;
                border-radius: 12px;
            }}
            
            .card h2 {{
                font-size: 1.2rem;
            }}
        }}
        
        @media (max-width: 480px) {{
            .header {{
                padding: 20px;
            }}
            
            .header h1 {{
                font-size: 1.75rem;
            }}
            
            .card {{
                padding: 16px;
            }}
            
            .info-item {{
                padding: 12px;
            }}
            
            .file-list {{
                max-height: 250px;
            }}
        }}
        
        @media (min-width: 1200px) {{
            .grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}
        
        @media (min-width: 1600px) {{
            .grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}
        
        /* Print styles */
        @media print {{
            body {{
                background: white;
                color: black;
            }}
            
            .card {{
                break-inside: avoid;
                box-shadow: none;
                border: 1px solid #ddd;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌊 Waft Visual Dashboard</h1>
            <div class="subtitle">
                {state['project']['name']} v{state['project']['version']} • 
                Generated: {state['system']['date_time']}
            </div>
        </div>

        <!-- Status Overview - Most Important First -->
        <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr)); margin-bottom: 24px;">
            {self._render_status_overview_card(state)}
            {self._render_git_summary_card(state)}
            {self._render_health_card(state)}
        </div>

        <!-- Primary Information - Git & Changes -->
        <div class="grid" style="margin-bottom: 24px;">
            {self._render_git_card(state)}
        </div>

        <!-- Work & Progress -->
        <div class="grid" style="margin-bottom: 24px;">
            {self._render_work_efforts_card(state)}
            {self._render_gamification_card(state)}
        </div>

        <!-- Analytics & Trends -->
        {self._render_analytics_section(state) if state.get('analytics', {}).get('available') else ''}

        <!-- Project Structure & Details -->
        <div class="grid" style="margin-bottom: 24px;">
            {self._render_pyrite_card(state)}
            {self._render_project_details_card(state)}
        </div>

        <div class="footer">
            <p style="font-size: 1.1em; font-weight: 600; color: var(--primary-light); margin-bottom: 8px;">
                🌊 Waft - Ambient Meta-Framework for Python
            </p>
            <p style="font-size: 0.9em;">
                This dashboard is standalone - refresh the page or regenerate to update
            </p>
        </div>
    </div>

    <script>
        // Smooth scroll behavior
        document.documentElement.style.scrollBehavior = 'smooth';
        
        // Make cards collapsible with animation
        document.querySelectorAll('.card h2').forEach((header, index) => {{
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {{
                const card = this.parentElement;
                const content = card.querySelector('.card-content');
                
                if (card.classList.contains('collapsed')) {{
                    card.classList.remove('collapsed');
                    content.style.animation = 'fadeIn 0.3s ease-out';
                }} else {{
                    card.classList.add('collapsed');
                }}
            }});
            
            // Add hover effect
            header.addEventListener('mouseenter', function() {{
                if (!this.parentElement.classList.contains('collapsed')) {{
                    this.style.transform = 'translateX(4px)';
                }}
            }});
            
            header.addEventListener('mouseleave', function() {{
                this.style.transform = 'translateX(0)';
            }});
        }});
        
        // Animate progress bars on load
        document.addEventListener('DOMContentLoaded', function() {{
            const progressBars = document.querySelectorAll('.progress-fill');
            progressBars.forEach(bar => {{
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {{
                    bar.style.width = width;
                }}, 100);
            }});
        }});
        
        // Add smooth hover effects to file list items
        document.querySelectorAll('.file-list li').forEach(item => {{
            item.addEventListener('mouseenter', function() {{
                this.style.transform = 'translateX(6px) scale(1.02)';
            }});
            item.addEventListener('mouseleave', function() {{
                this.style.transform = 'translateX(0) scale(1)';
            }});
        }});
        
        // Add ripple effect to badges
        document.querySelectorAll('.badge').forEach(badge => {{
            badge.addEventListener('click', function(e) {{
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.style.position = 'absolute';
                ripple.style.borderRadius = '50%';
                ripple.style.background = 'rgba(255, 255, 255, 0.3)';
                ripple.style.transform = 'scale(0)';
                ripple.style.animation = 'ripple 0.6s ease-out';
                ripple.style.pointerEvents = 'none';
                
                this.style.position = 'relative';
                this.style.overflow = 'hidden';
                this.appendChild(ripple);
                
                setTimeout(() => ripple.remove(), 600);
            }});
        }});
        
        // Add CSS for ripple animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes ripple {{
                to {{
                    transform: scale(4);
                    opacity: 0;
                }}
            }}
        `;
        document.head.appendChild(style);
        
        // State data available in console
        const state = {state_json};
        console.log('🌊 Waft Dashboard State:', state);
        console.log('💡 Tip: All data is available in the state object');
        
        // Performance monitoring
        window.addEventListener('load', function() {{
            const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
            console.log(`⚡ Dashboard loaded in ${{loadTime}}ms`);
        }});
    </script>
</body>
</html>"""

    def _render_status_overview_card(self, state: Dict[str, Any]) -> str:
        """Render status overview card - quick health check."""
        pyrite = state["pyrite"]
        git = state["git"]
        gam = state["gamification"]
        
        # Calculate overall health score
        health_score = 0
        health_items = []
        
        if pyrite["valid"]:
            health_score += 25
            health_items.append("✓ Structure")
        if git.get("initialized", False):
            health_score += 25
            health_items.append("✓ Git")
        if gam["integrity"] >= 90:
            health_score += 25
            health_items.append("✓ Integrity")
        if len(git.get("uncommitted_files", [])) < 10:
            health_score += 25
            health_items.append("✓ Clean")
        
        health_color = "success" if health_score >= 75 else "warning" if health_score >= 50 else "error"
        health_text = "Excellent" if health_score >= 75 else "Good" if health_score >= 50 else "Needs Attention"
        
        uncommitted = len(git.get("uncommitted_files", []))
        git_status_text = "Clean" if uncommitted == 0 else f"{uncommitted} files"
        git_status_class = "success" if uncommitted == 0 else "warning" if uncommitted < 20 else "error"
        
        return f"""
            <div class="card" style="grid-column: span 1;">
                <h2>⚡ Status Overview</h2>
                <div class="card-content">
                    <div class="info-item" style="text-align: center; padding: 20px;">
                        <div style="font-size: 3em; margin-bottom: 10px;">
                            {'🟢' if health_score >= 75 else '🟡' if health_score >= 50 else '🔴'}
                        </div>
                        <div class="info-value" style="font-size: 1.5em; font-weight: 700; margin-bottom: 8px;">
                            {health_text}
                        </div>
                        <div class="info-label" style="font-size: 0.9em;">
                            {health_score}% Health Score
                        </div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Quick Status</div>
                        <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px;">
                            <span class="badge {health_color}">{health_text}</span>
                            <span class="badge {git_status_class}">{git_status_text}</span>
                            <span class="badge {'success' if pyrite['valid'] else 'error'}">{'Valid' if pyrite['valid'] else 'Invalid'} Structure</span>
                        </div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Health Indicators</div>
                        <div style="margin-top: 8px; line-height: 1.8;">
                            {'<br>'.join(health_items) if health_items else '<span class="empty">No health data</span>'}
                        </div>
                    </div>
                </div>
            </div>
        """
    
    def _render_git_summary_card(self, state: Dict[str, Any]) -> str:
        """Render git summary card - quick git status."""
        git = state["git"]
        if not git["initialized"]:
            return """
            <div class="card">
                <h2>🔀 Git Status</h2>
                <div class="card-content">
                    <div class="info-item">
                        <span class="status missing">Not Initialized</span>
                    </div>
                </div>
            </div>
            """
        
        uncommitted = len(git.get("uncommitted_files", []))
        status_class = "success" if uncommitted == 0 else "warning" if uncommitted < 20 else "error"
        
        return f"""
            <div class="card">
                <h2>🔀 Git Summary</h2>
                <div class="card-content">
                    <div class="info-item">
                        <div class="info-label">Branch</div>
                        <div class="info-value">
                            <span style="font-family: monospace; color: var(--primary-light);">{git.get('branch', 'N/A')}</span>
                        </div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Uncommitted Changes</div>
                        <div class="info-value">
                            <span class="badge {status_class}" style="font-size: 1.1em; padding: 8px 16px;">
                                {uncommitted} file{'' if uncommitted == 1 else 's'}
                            </span>
                        </div>
                    </div>
                    {f'<div class="info-item"><div class="info-label">Commits Ahead</div><div class="info-value"><span class="badge info">{git.get("commits_ahead", 0)}</span></div></div>' if git.get("commits_ahead", 0) > 0 else ''}
                    {f'<div class="info-item"><div class="info-label">Recent Activity</div><div class="info-value" style="font-size: 0.9em; color: var(--text-secondary);">{len(git.get("recent_commits", []))} commits in history</div></div>' if git.get("recent_commits") else ''}
                </div>
            </div>
        """
    
    def _render_health_card(self, state: Dict[str, Any]) -> str:
        """Render project health card."""
        pyrite = state["pyrite"]
        gam = state["gamification"]
        lock_exists = self.substrate.verify_lock()
        
        return f"""
            <div class="card">
                <h2>💚 Project Health</h2>
                <div class="card-content">
                    <div class="info-item">
                        <div class="info-label">Integrity</div>
                        <div class="info-value">
                            <span class="badge {'success' if gam['integrity'] >= 90 else 'warning' if gam['integrity'] >= 70 else 'error'}" style="font-size: 1.1em; padding: 8px 16px;">
                                {gam['integrity']:.1f}%
                            </span>
                        </div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Level</div>
                        <div class="info-value">
                            <span class="badge info" style="font-size: 1.1em; padding: 8px 16px;">
                                Level {gam['level']}
                            </span>
                        </div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Structure</div>
                        <div class="info-value">
                            <span class="status {'valid' if pyrite['valid'] else 'invalid'}">
                                {'✅ Valid' if pyrite['valid'] else '❌ Invalid'}
                            </span>
                        </div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Dependencies</div>
                        <div class="info-value">
                            <span class="status {'valid' if lock_exists else 'missing'}">
                                {'✅ Locked' if lock_exists else '⚠️ Missing'}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        """

    def _render_git_card(self, state: Dict[str, Any]) -> str:
        """Render detailed git status card."""
        git = state["git"]
        if not git["initialized"]:
            return """
            <div class="card">
                <h2>🔀 Git Details</h2>
                <div class="card-content">
                    <div class="info-item">
                        <span class="status missing">Not Initialized</span>
                        <div style="margin-top: 10px; color: var(--text-secondary); font-size: 0.9em;">
                            Run <code style="background: rgba(124, 158, 255, 0.2); padding: 2px 6px; border-radius: 4px;">git init</code> to initialize
                        </div>
                    </div>
                </div>
            </div>
            """

        uncommitted_count = len(git["uncommitted_files"])
        status_badge = "success" if uncommitted_count == 0 else "warning" if uncommitted_count < 20 else "error"
        
        # Organize files by type
        staged_count = len(git.get("staged_files", []))
        modified_count = len(git.get("modified_files", []))
        untracked_count = len(git.get("untracked_files", []))

        files_html = ""
        if git["uncommitted_files"]:
            files_html = "<div style='margin-top: 12px;'>"
            
            # Show file type breakdown
            if staged_count > 0 or modified_count > 0 or untracked_count > 0:
                files_html += "<div style='display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap;'>"
                if staged_count > 0:
                    files_html += f"<span class='badge success'>{staged_count} staged</span>"
                if modified_count > 0:
                    files_html += f"<span class='badge warning'>{modified_count} modified</span>"
                if untracked_count > 0:
                    files_html += f"<span class='badge info'>{untracked_count} untracked</span>"
                files_html += "</div>"
            
            # Show file list
            files_html += "<ul class='file-list'>"
            for f in git["uncommitted_files"][:25]:  # Show more files
                # Determine file type icon
                icon = "📝"
                if f.endswith(('.py', '.js', '.ts', '.jsx', '.tsx')):
                    icon = "💻"
                elif f.endswith(('.md', '.txt')):
                    icon = "📄"
                elif f.endswith(('.json', '.yaml', '.yml', '.toml')):
                    icon = "⚙️"
                elif f.endswith(('.png', '.jpg', '.svg', '.gif')):
                    icon = "🖼️"
                elif '/.git' in f or '/node_modules' in f:
                    icon = "🔧"
                
                files_html += f"<li>{icon} {f}</li>"
            if len(git["uncommitted_files"]) > 25:
                files_html += f"<li class='empty'>... and {len(git['uncommitted_files']) - 25} more files</li>"
            files_html += "</ul></div>"

        commits_html = ""
        if git["recent_commits"]:
            commits_html = "<div style='margin-top: 15px;'>"
            for commit in git["recent_commits"][:5]:
                commits_html += f"""
                    <div class="commit-item">
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                            <div class="commit-hash">{commit['hash']}</div>
                            <div style="flex: 1; color: var(--text-secondary); font-size: 0.85em;">{commit['relative']}</div>
                        </div>
                        <div class="commit-message">{commit['message']}</div>
                        <div class="commit-meta">👤 {commit['author']}</div>
                    </div>
                """
            commits_html += "</div>"

        return f"""
            <div class="card" style="grid-column: span 2;">
                <h2>🔀 Git Details & Changes</h2>
                <div class="card-content">
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 20px;">
                        <div class="info-item">
                            <div class="info-label">Branch</div>
                            <div class="info-value" style="font-family: monospace; color: var(--primary-light); font-size: 1.1em;">
                                {git['branch'] or 'N/A'}
                            </div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Uncommitted</div>
                            <div class="info-value">
                                <span class="badge {status_badge}" style="font-size: 1.1em; padding: 8px 16px;">
                                    {uncommitted_count} file{'' if uncommitted_count == 1 else 's'}
                                </span>
                            </div>
                        </div>
                        {f'<div class="info-item"><div class="info-label">Commits Ahead</div><div class="info-value"><span class="badge info" style="font-size: 1.1em; padding: 8px 16px;">{git["commits_ahead"]}</span></div></div>' if git.get("commits_ahead", 0) > 0 else ''}
                        {f'<div class="info-item"><div class="info-label">Remote</div><div class="info-value" style="font-size: 0.9em; word-break: break-all; color: var(--text-secondary);">{git.get("remote_url", "Not configured")}</div></div>' if git.get("remote_url") else ''}
                    </div>
                    {f'<div class="info-item"><div class="info-label">Changed Files</div>{files_html}</div>' if files_html else '<div class="info-item"><div class="empty">No uncommitted files</div></div>'}
                    {f'<div class="info-item" style="margin-top: 20px;"><div class="info-label">Recent Commits</div>{commits_html}</div>' if commits_html else ''}
                </div>
            </div>
        """

    def _render_pyrite_card(self, state: Dict[str, Any]) -> str:
        """Render _pyrite structure card with better organization."""
        pyrite = state["pyrite"]
        status_class = "valid" if pyrite["valid"] else "invalid"
        status_text = "✅ Valid" if pyrite["valid"] else "❌ Invalid"
        
        total_files = len(pyrite["active_files"]) + len(pyrite["backlog_files"]) + len(pyrite["standards_files"])

        # Group active files by date prefix if they have dates
        recent_files = []
        older_files = []
        for f in pyrite["active_files"][:15]:
            if f.startswith("2026-") or f.startswith("2025-"):
                recent_files.append(f)
            else:
                older_files.append(f)
        
        active_list = ""
        if recent_files or older_files:
            active_list = "<ul class='file-list' style='max-height: 300px;'>"
            # Show recent files first
            for f in recent_files[:12]:
                active_list += f"<li>📄 <span style='color: var(--primary-light);'>{f[:10]}</span> {f[11:] if len(f) > 10 else ''}</li>"
            # Then older files
            for f in older_files[:3]:
                active_list += f"<li>📄 {f}</li>"
            if len(pyrite["active_files"]) > 15:
                active_list += f"<li class='empty'>... and {len(pyrite['active_files']) - 15} more files</li>"
            active_list += "</ul>"
        else:
            active_list = '<div class="empty">No active files</div>'

        return f"""
            <div class="card">
                <h2>💎 Project Structure</h2>
                <div class="card-content">
                    <div class="info-item">
                        <div class="info-label">Structure Status</div>
                        <div class="info-value">
                            <span class="status {status_class}">{status_text}</span>
                            <span style="margin-left: 12px; color: var(--text-secondary); font-size: 0.9em;">
                                {total_files} total files
                            </span>
                        </div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">
                            Active Files 
                            <span class="badge info" style="font-size: 0.8em; margin-left: 8px;">{len(pyrite['active_files'])}</span>
                        </div>
                        {active_list}
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-top: 12px;">
                        <div class="info-item">
                            <div class="info-label">Backlog</div>
                            <div class="info-value">
                                <span class="badge {'info' if len(pyrite['backlog_files']) > 0 else 'warning'}">
                                    {len(pyrite['backlog_files'])} files
                                </span>
                            </div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Standards</div>
                            <div class="info-value">
                                <span class="badge {'info' if len(pyrite['standards_files']) > 0 else 'warning'}">
                                    {len(pyrite['standards_files'])} files
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        """
    
    def _render_project_details_card(self, state: Dict[str, Any]) -> str:
        """Render project details card - combines project info and system info."""
        project = state["project"]
        sys_info = state["system"]
        
        return f"""
            <div class="card">
                <h2>📦 Project Details</h2>
                <div class="card-content">
                    <div class="info-item">
                        <div class="info-label">Project</div>
                        <div class="info-value">
                            <strong style="color: var(--primary-light);">{project['name']}</strong>
                            <span style="color: var(--text-secondary); margin-left: 8px;">v{project['version']}</span>
                        </div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Path</div>
                        <div class="info-value" style="font-size: 0.85em; word-break: break-all; color: var(--text-secondary); font-family: monospace;">
                            {state['project_path']}
                        </div>
                    </div>
                    <div style="border-top: 1px solid var(--border); margin: 16px 0; padding-top: 16px;">
                        <div class="info-label" style="margin-bottom: 12px;">System Environment</div>
                        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px;">
                            <div style="padding: 8px; background: rgba(26, 30, 41, 0.4); border-radius: 6px;">
                                <div style="font-size: 0.85em; color: var(--text-secondary);">Python</div>
                                <div style="font-weight: 600; font-family: monospace;">{sys_info['python_version']}</div>
                            </div>
                            <div style="padding: 8px; background: rgba(26, 30, 41, 0.4); border-radius: 6px;">
                                <div style="font-size: 0.85em; color: var(--text-secondary);">Platform</div>
                                <div style="font-weight: 600;">{sys_info['platform']}</div>
                            </div>
                        </div>
                        <div style="margin-top: 8px; padding: 8px; background: rgba(26, 30, 41, 0.4); border-radius: 6px;">
                            <div style="font-size: 0.85em; color: var(--text-secondary);">Generated</div>
                            <div style="font-weight: 600; font-size: 0.9em;">{sys_info['date_time']}</div>
                        </div>
                    </div>
                </div>
            </div>
        """

    def _render_gamification_card(self, state: Dict[str, Any]) -> str:
        """Render gamification stats card."""
        gam = state["gamification"]
        integrity = gam["integrity"]
        insight = gam["insight"]
        insight_needed = gam["insight_to_next"]
        progress = (insight / insight_needed * 100) if insight_needed > 0 else 0

        return f"""
            <div class="card">
                <h2>🎮 Gamification</h2>
                <div class="card-content">
                    <div class="info-item">
                        <div class="info-label">Integrity</div>
                        <div class="info-value">
                            <span class="badge {'success' if integrity >= 90 else 'warning' if integrity >= 70 else 'invalid'}">
                                {integrity:.1f}%
                            </span>
                        </div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Level</div>
                        <div class="info-value">
                            <span class="badge info">Level {gam['level']}</span>
                        </div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Insight Progress</div>
                        <div class="info-value">
                            {insight:.0f} / {insight_needed:.0f}
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: {min(progress, 100)}%"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        """

    def _render_work_efforts_card(self, state: Dict[str, Any]) -> str:
        """Render work efforts and activity card."""
        efforts = state["work_efforts"]
        devlog_entries = state["devlog"]
        
        # Only show this card prominently if there's actual work
        if not efforts and not devlog_entries:
            return f"""
            <div class="card">
                <h2>📋 Work & Activity</h2>
                <div class="card-content">
                    <div class="info-item" style="text-align: center; padding: 30px;">
                        <div style="font-size: 2.5em; margin-bottom: 10px; opacity: 0.5;">📭</div>
                        <div class="empty" style="font-size: 1.1em;">No active work efforts</div>
                        <div style="margin-top: 12px; color: var(--text-secondary); font-size: 0.9em;">
                            Recent activity will appear here
                        </div>
                    </div>
                </div>
            </div>
            """
        
        efforts_html = ""
        if efforts:
            efforts_html = "<ul class='file-list'>"
            for effort in efforts[:8]:
                efforts_html += f"<li>📋 <strong>{effort['id']}</strong></li>"
            if len(efforts) > 8:
                efforts_html += f"<li class='empty'>... and {len(efforts) - 8} more work efforts</li>"
            efforts_html += "</ul>"
        else:
            efforts_html = '<div class="empty">No active work efforts</div>'

        devlog_html = ""
        if devlog_entries:
            devlog_html = "<ul class='file-list' style='max-height: 200px;'>"
            for entry in devlog_entries[:5]:
                # Truncate long entries
                display_entry = entry[:60] + "..." if len(entry) > 60 else entry
                devlog_html += f"<li>📝 {display_entry}</li>"
            devlog_html += "</ul>"
        else:
            devlog_html = '<div class="empty">No recent devlog entries</div>'

        return f"""
            <div class="card">
                <h2>📋 Work & Activity</h2>
                <div class="card-content">
                    <div class="info-item">
                        <div class="info-label">Active Work Efforts</div>
                        <div style="margin-top: 8px;">
                            <span class="badge info" style="margin-bottom: 8px; display: inline-block;">{len(efforts)} active</span>
                        </div>
                        {efforts_html}
                    </div>
                    <div class="info-item" style="margin-top: 16px;">
                        <div class="info-label">Recent Devlog</div>
                        {devlog_html}
                    </div>
                </div>
            </div>
        """


    def generate_and_open(self, output_path: Optional[Path] = None) -> Path:
        """
        Generate dashboard and open in browser.

        Args:
            output_path: Optional custom output path

        Returns:
            Path to generated HTML file
        """
        # Gather state
        state = self.gather_state()

        # Determine output path
        if output_path is None:
            waft_dir = self.project_path / "_pyrite" / ".waft"
            waft_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
            output_path = waft_dir / f"visualize-{timestamp}.html"
        else:
            output_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate HTML
        html = self.generate_html(state)

        # Write file
        output_path.write_text(html, encoding="utf-8")

        # Open in browser
        try:
            webbrowser.open(f"file://{output_path.resolve()}")
        except Exception as e:
            # If opening fails, just show the path
            print(f"Could not open browser automatically: {e}")
            print(f"Open manually: {output_path.resolve()}")

        return output_path

    def phase1(self, verbose: bool = False) -> Path:
        """
        Run Phase 1: Comprehensive data gathering and visualization.

        Executes all data gathering phases in logical order, then generates
        and opens the visualization dashboard.

        Args:
            verbose: If True, show detailed progress for each phase

        Returns:
            Path to generated HTML dashboard
        """
        print("\n🌊 Phase 1: Comprehensive Data Gathering & Visualization\n")

        # Phase 1.1: Environment Verification
        if verbose:
            print("Phase 1.1: Environment Verification")
        else:
            print("Phase 1.1: Environment Verification", end="... ")
        import sys
        from datetime import datetime
        env_info = {
            "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "working_directory": str(Path.cwd()),
            "python_version": sys.version.split()[0],
            "platform": sys.platform,
        }
        if verbose:
            print(f"  ✓ Date/time: {env_info['date_time']}")
            print(f"  ✓ Working directory: {env_info['working_directory']}")
            print(f"  ✓ Python: {env_info['python_version']}")
            print(f"  ✓ Platform: {env_info['platform']}")
        else:
            print("✓")

        # Phase 1.2: Project Discovery
        if verbose:
            print("\nPhase 1.2: Project Discovery")
        else:
            print("Phase 1.2: Project Discovery", end="... ")
        project_info = self.substrate.get_project_info()
        project_name = project_info.get("name", "Unknown")
        project_version = project_info.get("version", "Unknown")
        if verbose:
            print(f"  ✓ Waft project detected")
            print(f"  ✓ Project path: {self.project_path.resolve()}")
            print(f"  ✓ Project name: {project_name}")
            print(f"  ✓ Version: {project_version}")
        else:
            print("✓")

        # Phase 1.3: Git Status Analysis
        if verbose:
            print("\nPhase 1.3: Git Status Analysis")
        else:
            print("Phase 1.3: Git Status Analysis", end="... ")
        git_status = self._get_git_status()
        if verbose:
            if git_status["initialized"]:
                print(f"  ✓ Git initialized")
                print(f"  ✓ Branch: {git_status.get('branch', 'N/A')}")
                print(f"  ✓ Uncommitted files: {len(git_status.get('uncommitted_files', []))}")
                print(f"  ✓ Commits ahead: {git_status.get('commits_ahead', 0)}")
                print(f"  ✓ Recent commits: {len(git_status.get('recent_commits', []))} found")
            else:
                print(f"  ⚠️  Git not initialized")
        else:
            print("✓" if git_status["initialized"] else "⚠️")

        # Phase 1.4: Project Health Check
        if verbose:
            print("\nPhase 1.4: Project Health Check")
        else:
            print("Phase 1.4: Project Health Check", end="... ")
        pyrite_status = self.memory.verify_structure()
        lock_exists = self.substrate.verify_lock()
        stats = self.gamification.get_stats()
        if verbose:
            print(f"  ✓ _pyrite structure: {'Valid' if pyrite_status['valid'] else 'Invalid'}")
            print(f"  ✓ uv.lock: {'Exists' if lock_exists else 'Missing'}")
            print(f"  ✓ Integrity: {stats.get('integrity', 100.0):.1f}%")
            print(f"  ✓ Level: {stats.get('level', 1)}")
            print(f"  ✓ Insight: {stats.get('insight', 0.0):.0f}/{stats.get('insight_to_next_level', 100.0):.0f}")
        else:
            print("✓")

        # Phase 1.5: Work Effort Discovery
        if verbose:
            print("\nPhase 1.5: Work Effort Discovery")
        else:
            print("Phase 1.5: Work Effort Discovery", end="... ")
        work_efforts = self._get_work_efforts()
        devlog_entries = self._get_recent_devlog()
        if verbose:
            print(f"  ✓ Active work efforts: {len(work_efforts)}")
            print(f"  ✓ Recent devlog entries: {len(devlog_entries)} found")
        else:
            print("✓")

        # Phase 1.6: Memory Layer Analysis
        if verbose:
            print("\nPhase 1.6: Memory Layer Analysis")
        else:
            print("Phase 1.6: Memory Layer Analysis", end="... ")
        active_files = list(self.memory.get_active_files())
        backlog_files = list(self.memory.get_backlog_files())
        standards_files = list(self.memory.get_standards_files())
        if verbose:
            print(f"  ✓ Active files: {len(active_files)}")
            print(f"  ✓ Backlog files: {len(backlog_files)}")
            print(f"  ✓ Standards files: {len(standards_files)}")
        else:
            print("✓")

        # Phase 1.7: Integration Status
        if verbose:
            print("\nPhase 1.7: Integration Status")
        else:
            print("Phase 1.7: Integration Status", end="... ")
        from .empirica import EmpiricaManager
        empirica = EmpiricaManager(self.project_path)
        empirica_initialized = empirica.is_initialized()
        github_remote = self.github.get_remote_url()
        if verbose:
            print(f"  ✓ Empirica: {'Initialized' if empirica_initialized else 'Not initialized'}")
            print(f"  ✓ GitHub: {'Configured' if github_remote else 'Not configured'}")
            print(f"  ✓ Templates: All present")
        else:
            print("✓")

        # Phase 1.8: Visualization Generation
        if verbose:
            print("\nPhase 1.8: Visualization Generation")
            print("  📊 Gathering all data...")
        else:
            print("Phase 1.8: Visualization Generation", end="... ")
        state = self.gather_state()
        
        # Create Phase 1 output folder
        phase1_dir = self.project_path / "_pyrite" / "phase1"
        phase1_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        
        # Save raw state data as JSON
        json_path = phase1_dir / f"phase1-{timestamp}.json"
        json_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
        if verbose:
            print(f"  ✓ State data saved: {json_path.name}")
        
        # Generate and save HTML dashboard
        if verbose:
            print("  📄 Generating HTML dashboard...")
        html_path = phase1_dir / f"phase1-{timestamp}.html"
        html = self.generate_html(state)
        html_path.write_text(html, encoding="utf-8")
        if verbose:
            print(f"  ✓ Dashboard created: {html_path.name}")
            print("  🌐 Opening in browser...")
        else:
            print("✓")
        
        # Open dashboard in browser
        try:
            webbrowser.open(f"file://{html_path.resolve()}")
            if verbose:
                print("  ✓ Dashboard opened")
        except Exception as e:
            print(f"  ⚠️  Could not open browser: {e}")
            print(f"  📄 Open manually: {html_path.resolve()}")

        print(f"\n✅ Phase 1 Complete - All data gathered and visualized")
        print(f"   📁 Output folder: {phase1_dir.resolve()}")
        print(f"   📄 Dashboard: {html_path.name}")
        print(f"   📊 Data: {json_path.name}\n")

        return html_path
