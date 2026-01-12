#!/usr/bin/env python3
"""
Analyze GitHub Repositories for D&D 5e AI Exploration

Fetches repository information and documents findings in work effort folders.
"""

import json
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
WORK_EFFORTS_DIR = PROJECT_ROOT / "_work_efforts"

# Repository list from parent work effort
REPOSITORIES = [
    {
        "owner": "foundryvtt",
        "repo": "dnd5e",
        "work_effort_id": "l9sc",
        "priority": "HIGH",
        "category": "Core D&D 5e"
    },
    {
        "owner": "5e-bits",
        "repo": "5e-database",
        "work_effort_id": "2759",
        "priority": "HIGH",
        "category": "Core D&D 5e"
    },
    {
        "owner": "ctavolazzi",
        "repo": "AI-DnD",
        "work_effort_id": "6ca4",
        "priority": "HIGH",
        "category": "AI D&D Tools"
    },
    {
        "owner": "QuitoTactico",
        "repo": "DnD-AI",
        "work_effort_id": "jtkv",
        "priority": "MEDIUM",
        "category": "AI D&D Tools"
    },
    {
        "owner": "fedefreak92",
        "repo": "dungeon-master-ai-project",
        "work_effort_id": "v90k",
        "priority": "MEDIUM",
        "category": "AI D&D Tools"
    },
    {
        "owner": "chungs10",
        "repo": "dnd-ai",
        "work_effort_id": "o7f0",
        "priority": "MEDIUM",
        "category": "AI D&D Tools"
    },
    {
        "owner": "deckofdmthings",
        "repo": "GameMasterAI",
        "work_effort_id": "jxot",
        "priority": "MEDIUM",
        "category": "AI D&D Tools"
    },
    {
        "owner": "raeleus",
        "repo": "Hashtag-DnD",
        "work_effort_id": "ys1t",
        "priority": "MEDIUM",
        "category": "AI D&D Tools"
    },
    {
        "owner": "Tsinx",
        "repo": "aidnd",
        "work_effort_id": "qm3i",
        "priority": "MEDIUM",
        "category": "AI D&D Tools"
    },
    {
        "owner": "mfreeman451",
        "repo": "dd-chatgpt-dm",
        "work_effort_id": "8o35",
        "priority": "MEDIUM",
        "category": "AI D&D Tools"
    },
]


def get_repo_info_via_gh(owner: str, repo: str) -> Optional[Dict]:
    """Get repository information using gh CLI."""
    try:
        result = subprocess.run(
            ["gh", "repo", "view", f"{owner}/{repo}", "--json", "name,description,url,stargazerCount,updatedAt,isArchived,primaryLanguage,topics"],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
        return None


def get_readme_via_gh(owner: str, repo: str) -> Optional[str]:
    """Get README content using gh CLI."""
    try:
        result = subprocess.run(
            ["gh", "repo", "view", f"{owner}/{repo}", "--json", "readme"],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
        if "readme" in data and data["readme"]:
            return data["readme"].get("text", "")
        return None
    except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
        return None


def analyze_repository(repo_info: Dict) -> Dict:
    """Analyze a single repository."""
    owner = repo_info["owner"]
    repo = repo_info["repo"]
    
    print(f"\n📦 Analyzing: {owner}/{repo}")
    
    analysis = {
        "owner": owner,
        "repo": repo,
        "work_effort_id": repo_info["work_effort_id"],
        "priority": repo_info["priority"],
        "category": repo_info["category"],
        "analyzed_at": datetime.now().isoformat(),
        "repo_data": None,
        "readme_content": None,
        "findings": {}
    }
    
    # Get repository info
    repo_data = get_repo_info_via_gh(owner, repo)
    if repo_data:
        analysis["repo_data"] = repo_data
        print(f"  ✅ Repository info retrieved")
        print(f"     Stars: {repo_data.get('stargazerCount', 'N/A')}")
        print(f"     Language: {repo_data.get('primaryLanguage', {}).get('name', 'N/A')}")
        print(f"     Archived: {repo_data.get('isArchived', False)}")
    else:
        print(f"  ⚠️  Could not retrieve repository info")
    
    # Get README
    readme = get_readme_via_gh(owner, repo)
    if readme:
        analysis["readme_content"] = readme
        print(f"  ✅ README retrieved ({len(readme)} chars)")
        
        # Extract key information from README
        findings = extract_readme_info(readme)
        analysis["findings"].update(findings)
    else:
        print(f"  ⚠️  Could not retrieve README")
    
    return analysis


def extract_readme_info(readme: str) -> Dict:
    """Extract key information from README."""
    findings = {
        "has_installation": False,
        "installation_methods": [],
        "language_detected": None,
        "framework_detected": None,
        "has_docker": False,
        "has_npm": False,
        "has_pip": False,
        "key_features": []
    }
    
    readme_lower = readme.lower()
    
    # Check for installation instructions
    if any(keyword in readme_lower for keyword in ["install", "setup", "getting started", "quick start"]):
        findings["has_installation"] = True
    
    # Detect installation methods
    if "npm install" in readme_lower or "yarn" in readme_lower or "pnpm" in readme_lower:
        findings["has_npm"] = True
        findings["installation_methods"].append("npm/yarn/pnpm")
    
    if "pip install" in readme_lower or "pipenv" in readme_lower or "poetry" in readme_lower:
        findings["has_pip"] = True
        findings["installation_methods"].append("pip/poetry")
    
    if "docker" in readme_lower:
        findings["has_docker"] = True
        findings["installation_methods"].append("docker")
    
    # Detect languages/frameworks
    if "react" in readme_lower or "next.js" in readme_lower:
        findings["framework_detected"] = "React/Next.js"
    elif "vue" in readme_lower:
        findings["framework_detected"] = "Vue"
    elif "fastapi" in readme_lower or "flask" in readme_lower or "django" in readme_lower:
        findings["framework_detected"] = "Python Web Framework"
    elif "express" in readme_lower:
        findings["framework_detected"] = "Express.js"
    
    # Extract key features (look for common patterns)
    feature_patterns = [
        r"## Features?",
        r"## Key Features?",
        r"## What.*does",
        r"## Features?.*\n(.*?)(?=\n##|\n#|$)",
    ]
    
    for pattern in feature_patterns:
        match = re.search(pattern, readme, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        if match:
            # Extract bullet points or list items
            content = match.group(0) if match.groups() else match.group(0)
            lines = content.split('\n')
            for line in lines[:10]:  # First 10 lines
                if line.strip().startswith('-') or line.strip().startswith('*'):
                    feature = line.strip().lstrip('-*').strip()
                    if feature and len(feature) < 200:
                        findings["key_features"].append(feature)
            break
    
    return findings


def save_analysis(analysis: Dict):
    """Save analysis to work effort folder."""
    work_effort_id = analysis["work_effort_id"]
    work_effort_name = f"WE-260111-{work_effort_id}_{analysis['repo'].replace('_', '-')}_installation_exploration"
    work_effort_dir = WORK_EFFORTS_DIR / work_effort_name
    
    if not work_effort_dir.exists():
        print(f"  ⚠️  Work effort directory not found: {work_effort_dir}")
        return
    
    # Save analysis JSON
    analysis_file = work_effort_dir / "REPOSITORY_ANALYSIS.json"
    with open(analysis_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    print(f"  ✅ Analysis saved to: {analysis_file.name}")
    
    # Update INSTALLATION_EXPLORATION.md with findings
    exploration_file = work_effort_dir / "INSTALLATION_EXPLORATION.md"
    if exploration_file.exists():
        update_exploration_file(exploration_file, analysis)
        print(f"  ✅ Updated: {exploration_file.name}")


def update_exploration_file(file_path: Path, analysis: Dict):
    """Update installation exploration file with analysis findings."""
    content = file_path.read_text()
    
    # Update project information section
    repo_data = analysis.get("repo_data", {})
    findings = analysis.get("findings", {})
    
    # Replace placeholders with actual data
    if repo_data:
        if "[PROJECT_NAME]" in content:
            content = content.replace("[PROJECT_NAME]", repo_data.get("name", analysis["repo"]))
        if "[OWNER]" in content:
            content = content.replace("[OWNER]", analysis["owner"])
        if "[REPO_NAME]" in content:
            content = content.replace("[REPO_NAME]", analysis["repo"])
        if "[TO_BE_DETERMINED]" in content:
            lang = repo_data.get("primaryLanguage", {}).get("name", "Unknown")
            content = content.replace("[TO_BE_DETERMINED]", lang)
    
    # Add analysis findings section
    findings_section = f"""
## Initial Analysis Results

**Analysis Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

### Repository Information
- **Stars**: {repo_data.get('stargazerCount', 'N/A') if repo_data else 'N/A'}
- **Language**: {repo_data.get('primaryLanguage', {}).get('name', 'Unknown') if repo_data else 'Unknown'}
- **Archived**: {repo_data.get('isArchived', False) if repo_data else 'Unknown'}
- **Last Updated**: {repo_data.get('updatedAt', 'Unknown') if repo_data else 'Unknown'}
- **Description**: {repo_data.get('description', 'N/A') if repo_data else 'N/A'}

### Installation Analysis
- **Has Installation Instructions**: {findings.get('has_installation', False)}
- **Installation Methods Detected**: {', '.join(findings.get('installation_methods', ['None']))}
- **Framework Detected**: {findings.get('framework_detected', 'None')}

### Key Features Detected
{chr(10).join(f"- {feature}" for feature in findings.get('key_features', [])[:5]) if findings.get('key_features') else "- None detected"}

---
"""
    
    # Insert findings after "## Initial Analysis" section
    if "## Initial Analysis" in content:
        # Find the end of Initial Analysis section
        pattern = r"(## Initial Analysis.*?\n)(?=##|$)"
        replacement = r"\1" + findings_section
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    else:
        # Add at the beginning if section doesn't exist
        content = findings_section + "\n" + content
    
    file_path.write_text(content)


def main():
    """Main function to analyze all repositories."""
    print("🔍 Starting GitHub Repository Analysis\n")
    print(f"Analyzing {len(REPOSITORIES)} repositories...\n")
    
    all_analyses = []
    
    for repo_info in REPOSITORIES:
        try:
            analysis = analyze_repository(repo_info)
            save_analysis(analysis)
            all_analyses.append(analysis)
        except Exception as e:
            print(f"  ❌ Error analyzing {repo_info['owner']}/{repo_info['repo']}: {e}")
            continue
    
    # Create summary
    summary_file = WORK_EFFORTS_DIR / "WE-260111-jpw1_dnd5e_ai_exploration_initiative" / "REPOSITORY_ANALYSIS_SUMMARY.md"
    create_summary(summary_file, all_analyses)
    
    print(f"\n✅ Analysis complete!")
    print(f"   Analyzed: {len(all_analyses)}/{len(REPOSITORIES)} repositories")
    print(f"   Summary: {summary_file.name}")


def create_summary(file_path: Path, analyses: List[Dict]):
    """Create summary document of all analyses."""
    content = f"""# Repository Analysis Summary

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Overview

Analysis of {len(analyses)} repositories for D&D 5e AI exploration initiative.

---

## Repository Analysis Results

"""
    
    for analysis in analyses:
        repo_data = analysis.get("repo_data", {})
        findings = analysis.get("findings", {})
        
        content += f"""
### {analysis['owner']}/{analysis['repo']}

**Work Effort**: WE-260111-{analysis['work_effort_id']}  
**Priority**: {analysis['priority']}  
**Category**: {analysis['category']}

**Repository Info**:
- Stars: {repo_data.get('stargazerCount', 'N/A') if repo_data else 'N/A'}
- Language: {repo_data.get('primaryLanguage', {}).get('name', 'Unknown') if repo_data else 'Unknown'}
- Archived: {repo_data.get('isArchived', False) if repo_data else 'Unknown'}
- Description: {repo_data.get('description', 'N/A') if repo_data else 'N/A'}

**Installation**:
- Has Installation Instructions: {findings.get('has_installation', False)}
- Methods: {', '.join(findings.get('installation_methods', ['None']))}
- Framework: {findings.get('framework_detected', 'None')}

**Status**: {'✅ Analyzed' if repo_data or findings.get('has_installation') else '⚠️ Partial'}

---
"""
    
    file_path.write_text(content)


if __name__ == "__main__":
    main()
