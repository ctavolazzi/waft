# WAFT CLI Improvements Plan

**Date**: 2026-01-11
**Status**: In Progress

## Recommendation: Use `rich` (Already in Project)

**Why `rich`?**
- ✅ **Already in dependencies** (`rich>=13.0.0` in `pyproject.toml`)
- ✅ **Already used throughout WAFT** (main.py, core modules, CLI)
- ✅ **Lightweight API** - Simple `console.print()` with markup
- ✅ **Stable & well-maintained** - Active development, widely used
- ✅ **Minimal dependencies** - Just `typing-extensions` and `pygments` (optional)
- ✅ **Perfect for CLI** - Colors, status, progress, tables, panels

**Alternatives considered:**
- `colorama` - Too basic, only colors
- `click` - More for argument parsing, not output formatting
- `blessed` - Too heavy, terminal manipulation library

## Current State

**Demo script (`examples/interactive_demo.py`):**
- Uses plain `print()` statements
- Custom animation functions (`typing_print`, `loading_animation`)
- No color/styling
- Inconsistent with rest of WAFT

**Rest of WAFT:**
- Uses `rich.Console()` extensively
- Pattern: `console = Console()` then `console.print("[green]text[/green]")`
- Uses `console.status()` for loading operations
- Uses `Panel`, `Table`, `Progress` for structured output

## Improvement Plan

### Phase 1: Demo Script Enhancement (Low Impact)

**Replace:**
```python
print("  ✅ Created: file.txt")
```

**With:**
```python
console.print("  [green]✅[/green] Created: file.txt")
```

**Replace custom animations:**
```python
loading_animation("Installing...", duration=1.5)
```

**With:**
```python
with console.status("[bold cyan]Installing...[/bold cyan]"):
    # do work
    time.sleep(1.5)
```

**Benefits:**
- Consistent with WAFT codebase
- Better visual feedback
- Cleaner code (no custom animation functions)
- Automatic terminal detection
- Better color support

### Phase 2: Create Reusable CLI Utilities (Optional)

Create `src/waft/cli/output.py`:
```python
"""Reusable CLI output utilities using rich."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def success(message: str):
    console.print(f"[green]✅[/green] {message}")

def error(message: str):
    console.print(f"[red]❌[/red] {message}")

def info(message: str):
    console.print(f"[cyan]ℹ️[/cyan] {message}")

def step(step_num: int, total: int, description: str):
    console.print(f"[bold cyan][{step_num}/{total}][/bold cyan] {description}")
```

### Phase 3: Standardize Across All Scripts (Future)

- Update other demo/example scripts
- Create CLI style guide
- Document patterns

## Implementation

1. Update `examples/interactive_demo.py` to use `rich`
2. Remove custom animation functions
3. Add color/styling to output
4. Use `console.status()` for operations
5. Test demo still works correctly

## Low Impact Improvements

1. **Color coding**:
   - Success: `[green]`
   - Info: `[cyan]`
   - Warnings: `[yellow]`
   - Errors: `[red]`
   - Steps: `[bold cyan]`

2. **Status indicators**:
   - Use `console.status()` instead of custom loading animations
   - Automatic spinner, cleaner code

3. **Structured output**:
   - Use `Panel` for sections
   - Use `Table` for file listings (optional)

4. **Consistency**:
   - Match patterns used in `main.py`
   - Same visual style across WAFT

## Example Transformation

**Before:**
```python
print("  📁 Creating directory: tools/")
tools_dir.mkdir(exist_ok=True)
print("     ✅ Directory created")
```

**After:**
```python
console.print("  [cyan]📁[/cyan] Creating directory: [bold]tools/[/bold]")
tools_dir.mkdir(exist_ok=True)
console.print("     [green]✅[/green] Directory created")
```

**Or with status:**
```python
console.print("  [cyan]📁[/cyan] Creating directory: [bold]tools/[/bold]")
with console.status("[dim]Creating...[/dim]"):
    tools_dir.mkdir(exist_ok=True)
console.print("     [green]✅[/green] Directory created")
```
