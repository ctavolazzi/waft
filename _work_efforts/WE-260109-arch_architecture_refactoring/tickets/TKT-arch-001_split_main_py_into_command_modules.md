---
id: TKT-arch-001
parent: WE-260109-arch
title: "Split main.py into command modules"
status: open
priority: HIGH
created: 2026-01-09T00:00:00.000Z
created_by: claude_audit
assigned_to: null
---

# TKT-arch-001: Split main.py into command modules

## Metadata
- **Created**: Thursday, January 9, 2026
- **Parent Work Effort**: WE-260109-arch
- **Author**: Claude Audit System
- **Priority**: HIGH
- **Estimated Effort**: 3 tickets

## Description

Break up the 1,957-line main.py monolith into domain-organized command modules. This is the single most impactful architecture improvement for the codebase.

## Current State

**main.py**: 1,957 lines containing:
- 29+ @app.command() definitions
- Repeated patterns and logic
- Mixed concerns (project, empirica, gamification, RPG, analytics)
- Hard to navigate and test

## Proposed Organization

### Commands by Domain

**Project Management** → `commands/project.py`:
- `waft new <name>`
- `waft init`
- `waft verify`
- `waft info`

**Empirica/Epistemic** → `commands/empirica.py`:
- `waft session create/resume`
- `waft session bootstrap`
- `waft finding log`
- `waft unknown log`
- `waft check`
- `waft assess`
- `waft checkpoint`
- `waft checkout`
- `waft resume`

**Gamification** → `commands/gamification.py`:
- `waft stats`
- `waft level`
- `waft achievements`
- `waft dashboard`

**RPG/TavernKeeper** → `commands/tavern.py`:
- `waft character`
- `waft chronicle`
- `waft roll`
- `waft quests`
- `waft note`
- `waft observe`

**Analytics** → `commands/analytics.py`:
- `waft analytics sessions`
- `waft analytics trends`

**Decision Engine** → `commands/decision.py`:
- `waft decide`

**Dependencies** → `commands/deps.py`:
- `waft add`
- `waft sync`

**Web Server** → `commands/server.py`:
- `waft serve`

## Acceptance Criteria

- [ ] main.py reduced to < 200 lines (just CLI setup)
- [ ] Each command module < 500 lines
- [ ] Commands organized by logical domain
- [ ] All imports updated correctly
- [ ] All 29+ commands still work
- [ ] All existing tests pass
- [ ] No functionality changes (pure refactor)
- [ ] Code review approved

## Implementation Plan

### Step 1: Create Command Module Structure

```bash
mkdir -p src/waft/commands
touch src/waft/commands/__init__.py
touch src/waft/commands/project.py
touch src/waft/commands/empirica.py
touch src/waft/commands/gamification.py
touch src/waft/commands/tavern.py
touch src/waft/commands/analytics.py
touch src/waft/commands/decision.py
touch src/waft/commands/deps.py
touch src/waft/commands/server.py
```

### Step 2: Create Base Command Module

Create `src/waft/commands/__init__.py`:

```python
"""
Command modules for Waft CLI.

Each module contains related commands organized by domain:
- project: Project creation and management
- empirica: Epistemic tracking (Empirica integration)
- gamification: Integrity, insight, achievements
- tavern: RPG mechanics (TavernKeeper)
- analytics: Session analytics and trends
- decision: Decision matrix analysis
- deps: Dependency management
- server: Web server commands
"""

from pathlib import Path
import typer

# Export for convenience
__all__ = [
    "get_project_path",
    "ensure_waft_project",
]


def get_project_path() -> Path:
    """Get current project path."""
    return Path.cwd()


def ensure_waft_project(path: Path) -> bool:
    """Verify current directory is a Waft project."""
    pyrite = path / "_pyrite"
    if not pyrite.exists():
        typer.echo("❌ Error: Not a Waft project (no _pyrite/ directory)")
        typer.echo(f"   Current directory: {path}")
        typer.echo("   Run 'waft init' to initialize Waft in this project")
        raise typer.Exit(1)
    return True
```

### Step 3: Extract Commands (Example: project.py)

Create `src/waft/commands/project.py`:

```python
"""Project management commands."""

from pathlib import Path
import typer
from rich.console import Console

from ..core.substrate import SubstrateManager
from ..core.memory import MemoryManager
from ..core.gamification import GamificationManager
from ..templates import TemplateWriter
from . import get_project_path, ensure_waft_project

app = typer.Typer()
console = Console()


@app.command()
def new(
    name: str = typer.Argument(..., help="Project name"),
    path: str = typer.Option(".", help="Directory to create project in"),
):
    """Create a new Waft project."""
    # Move implementation from main.py
    # ... existing code ...
    pass


@app.command()
def init():
    """Initialize Waft in an existing project."""
    # Move implementation from main.py
    # ... existing code ...
    pass


@app.command()
def verify():
    """Verify project structure and health."""
    # Move implementation from main.py
    # ... existing code ...
    pass


@app.command()
def info():
    """Show project information."""
    # Move implementation from main.py
    # ... existing code ...
    pass
```

### Step 4: Update main.py

Simplify main.py to just CLI orchestration:

```python
"""
Waft - Ambient Meta-Framework for Python.

Main CLI entry point.
"""

import typer
from pathlib import Path

from .commands import project, empirica, gamification, tavern, analytics, decision, deps, server

app = typer.Typer(
    name="waft",
    help="Waft - Ambient Meta-Framework for Python",
    add_completion=False,
)

# Register command groups
app.add_typer(project.app, name="project", help="Project management")
app.add_typer(empirica.app, name="empirica", help="Epistemic tracking")
app.add_typer(gamification.app, name="gamification", help="Gamification")
app.add_typer(tavern.app, name="tavern", help="RPG mechanics")
app.add_typer(analytics.app, name="analytics", help="Session analytics")
app.add_typer(decision.app, name="decision", help="Decision analysis")
app.add_typer(deps.app, name="deps", help="Dependency management")
app.add_typer(server.app, name="server", help="Web server")

# Keep top-level commands for convenience
@app.command()
def new(name: str, path: str = "."):
    """Create a new Waft project."""
    project.new(name, path)


@app.command()
def verify():
    """Verify project structure."""
    project.verify()


# ... etc for other common commands ...


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
```

### Step 5: Move Commands Systematically

For each command in old main.py:

1. **Identify domain** (project, empirica, etc.)
2. **Copy command** to appropriate module
3. **Update imports** in command
4. **Test command** works in new location
5. **Delete from main.py** once verified
6. **Update any references** elsewhere

### Step 6: Test Everything

```bash
# Run all tests
pytest tests/ -v

# Manual smoke test each command
waft new test-project
waft init
waft verify
waft stats
# ... etc for all commands ...

# Verify CLI help
waft --help
waft project --help
waft empirica --help
```

## Migration Strategy

**Incremental Migration** (low risk):
1. Create new module structure
2. Copy commands (don't delete yet)
3. Test new commands work
4. Update main.py to use new modules
5. Delete old code
6. Verify tests pass

**Do NOT** attempt big-bang rewrite. Move commands incrementally.

## Testing Strategy

**Before Migration**:
- [ ] Document all 29 commands and their behavior
- [ ] Run full test suite, record results
- [ ] Create command inventory checklist

**During Migration**:
- [ ] Test each command after moving
- [ ] Verify imports work
- [ ] Check for any circular dependencies

**After Migration**:
- [ ] All tests pass (same results as before)
- [ ] All commands work (manual verification)
- [ ] Code coverage maintained or improved
- [ ] No broken imports

## Files to Create

**New Structure**:
- `src/waft/commands/__init__.py`
- `src/waft/commands/project.py`
- `src/waft/commands/empirica.py`
- `src/waft/commands/gamification.py`
- `src/waft/commands/tavern.py`
- `src/waft/commands/analytics.py`
- `src/waft/commands/decision.py`
- `src/waft/commands/deps.py`
- `src/waft/commands/server.py`

**Modified**:
- `src/waft/main.py` (reduce to < 200 lines)
- `tests/test_commands.py` (may need import updates)

**Total New Files**: 9
**Total LOC**: ~1,900 (same total, just organized)

## Benefits

**Immediate**:
- ✅ Easier to find code
- ✅ Smaller files to understand
- ✅ Clear domain boundaries
- ✅ Independent testing per domain

**Long-term**:
- ✅ Easier to add new commands
- ✅ Easier to deprecate commands
- ✅ Possible plugin architecture
- ✅ Better IDE navigation

## Risks

**Low Risk** (pure refactor):
- Same code, just reorganized
- All tests should pass unchanged

**Medium Risk** (import issues):
- Circular import dependencies
- Missing imports
- Relative import paths

**Mitigation**:
- Incremental migration
- Test after each module move
- Keep commits small and focused

## Success Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| main.py lines | 1,957 | < 200 | -90% |
| Largest file | 1,957 | < 500 | -75% |
| Files with commands | 1 | 9 | +800% |
| Commands per file | 29 | ~3-7 | Better |
| Test coverage | X% | X%+ | +5-10% |

## Related Issues

- Audit Finding: "main.py: 1,957 Line Monolith"
- Principle: Single Responsibility Principle (SRP)
- Pattern: Command pattern, domain-driven design

## Commits

- (populated as work progresses)

## Notes

This is the #1 architecture improvement for Waft. The current main.py is unmaintainable at 1,957 lines. This refactor will make all future work significantly easier.

The key is to do this incrementally and test thoroughly at each step. Don't try to move everything at once - move one domain at a time, verify it works, then move the next.
