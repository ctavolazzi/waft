# The GitHub God: God of Repository Management

**Pantheon Entity (Timeless Force that Binds Reality Together)**

The GitHub God maintains the fundamental principle of repository management and version control - the Aspect of Creation related to code distribution and collaboration.

## Philosophy

**As above, so below:**
- **As above**: Pantheon god maintaining the celestial code repositories
- **So below**: File-based system tracking GitHub operations and repository state

The GitHub God is timeless - it maintains stable repository principles and only evolves when sufficient evidence collected by Beings proves that change is needed.

## Purpose

The GitHub God provides:
- **Repository State Tracking**: Current branch, commits, remote status
- **Branch Management**: Summary of all branches and their status
- **Rollup Generation**: Comprehensive activity summaries
- **Operation Logging**: Track all GitHub operations

## Usage

### Generate a Full Rollup

```python
from waft.pantheon import GitHubGod
from pathlib import Path

github_god = GitHubGod(project_path=Path.cwd())

# Generate comprehensive rollup
rollup = github_god.generate_rollup(
    since="2026-01-01",
    include_all_branches=True
)

print(f"Total commits: {rollup['total_commits']}")
print(f"Current branch: {rollup['repository_state']['current_branch']}")
```

### Get Repository State

```python
# Get current repository state
state = github_god.get_repository_state()
print(f"Branch: {state['current_branch']}")
print(f"Commits: {state['commit_count']}")
print(f"Remote: {state['remote_url']}")
```

### Get Branch Summary

```python
# Get all branches and their status
summary = github_god.get_branch_summary()
for branch in summary['branches']:
    print(f"{branch['name']}: {'ahead' if branch['ahead'] else ''} {'behind' if branch['behind'] else ''}")
```

### Log Operations

```python
# Log a GitHub operation
op_id = github_god.log_operation(
    operation="push",
    details={"branch": "main", "commits": 5},
    result="success"
)
```

## Storage

- **Operations**: `_pantheon/github_god/operations/op_*.json`
- **Rollups**: `_pantheon/github_god/rollups/rollup_*.json`
- **Index**: `_pantheon/github_god/rollup_index.json`

## Integration

The GitHub God integrates with:
- **Git operations**: Direct git command execution
- **Repository tracking**: State monitoring
- **Rollup generation**: Activity summaries
- **MCP Servers**: Tracks Model Context Protocol server configuration

## Example Rollup Structure

```json
{
  "generated_at": "2026-01-16T22:00:00",
  "since": "2026-01-01",
  "repository_state": {
    "current_branch": "main",
    "commit_count": 1234,
    "remote_url": "https://github.com/user/repo.git",
    "unstaged_changes": 4
  },
  "branch_summary": {
    "total_branches": 15,
    "branches": [...]
  },
  "recent_commits": [...],
  "total_commits": 50,
  "summary": {
    "current_branch": "main",
    "total_branches": 15,
    "recent_commits_count": 50,
    "unstaged_files": 4
  }
}
```
