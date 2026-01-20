#!/usr/bin/env python3
"""Initialize git and push to GitHub."""

import subprocess
import sys
from pathlib import Path

REPO_PATH = Path(__file__).parent
GITHUB_URL = "https://github.com/ctavolazzi/waft.git"


def run_cmd(cmd, cwd=None):
    """Run a command and return success status."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd or REPO_PATH,
            capture_output=True,
            text=True,
            check=True,
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def main():
    print("🌊 Initializing Waft repository for GitHub...\n")

    # Check if git is initialized
    if not (REPO_PATH / ".git").exists():
        print("→ Initializing git repository...")
        success, output = run_cmd(["git", "init"])
        if success:
            print("✅ Git repository initialized\n")
        else:
            print(f"❌ Failed to initialize git: {output}")
            sys.exit(1)
    else:
        print("✓ Git repository already initialized\n")

    # Check remote
    success, output = run_cmd(["git", "remote", "get-url", "origin"])
    if not success:
        print("→ Adding GitHub remote...")
        success, output = run_cmd(["git", "remote", "add", "origin", GITHUB_URL])
        if success:
            print("✅ Remote added\n")
        else:
            print(f"❌ Failed to add remote: {output}")
            sys.exit(1)
    else:
        print(f"✓ Remote 'origin' already configured: {output.strip()}\n")

    # Add all files
    print("→ Staging files...")
    success, output = run_cmd(["git", "add", "."])
    if not success:
        print(f"❌ Failed to stage files: {output}")
        sys.exit(1)
    print("✅ Files staged\n")

    # Check if there are changes
    success, output = run_cmd(["git", "diff", "--staged", "--quiet"])
    if success:
        print("✓ No changes to commit\n")
    else:
        print("→ Creating initial commit...")
        commit_msg = """Initial commit: Waft v0.1.0

- Ambient meta-framework for Python projects
- Orchestrates uv, _pyrite, and crewai
- CLI commands: waft new, waft verify
- Full project scaffolding with templates"""
        success, output = run_cmd(["git", "commit", "-m", commit_msg])
        if success:
            print("✅ Commit created\n")
        else:
            print(f"❌ Failed to create commit: {output}")
            sys.exit(1)

    # Set main branch
    print("→ Setting main branch...")
    run_cmd(["git", "branch", "-M", "main"])
    print("✅ Branch set to main\n")

    # Push to GitHub
    print("→ Pushing to GitHub...")
    print(f"  Repository: {GITHUB_URL}\n")
    success, output = run_cmd(["git", "push", "-u", "origin", "main"])
    if success:
        print("✅ Successfully pushed to GitHub!")
        print("   View at: https://github.com/ctavolazzi/waft\n")
    else:
        print(f"❌ Failed to push: {output}")
        print("\nYou may need to authenticate or push manually:")
        print("  git push -u origin main\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
