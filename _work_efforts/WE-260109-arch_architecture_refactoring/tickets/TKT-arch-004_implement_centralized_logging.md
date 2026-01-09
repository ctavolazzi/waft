---
id: TKT-arch-004
parent: WE-260109-arch
title: "Implement centralized logging system"
status: open
priority: HIGH
created: 2026-01-09T00:00:00.000Z
created_by: claude_audit
assigned_to: null
---

# TKT-arch-004: Implement centralized logging system

## Metadata
- **Created**: Thursday, January 9, 2026
- **Parent Work Effort**: WE-260109-arch
- **Author**: Claude Audit System
- **Priority**: HIGH
- **Estimated Effort**: 2 tickets

## Description

Replace scattered `print()` statements throughout library code with a proper centralized logging system. This improves debuggability, allows log level control, and follows Python best practices.

## Current State

**Problems**:
- `print()` used throughout library code
- No log levels (can't separate INFO from DEBUG)
- No log rotation or management
- No structured logging
- Hard to debug in production
- Clutters stdout in library usage

**Examples from audit**:
```python
# substrate.py:63, 66
print(f"Error: {e.stderr}")
print("Error: uv not found...")

# utils.py: Multiple print statements
print(f"Info: ...")

# Many more across 49 files
```

## Problem Impact

**Severity**: HIGH ⚠️
- **Debugging**: Can't trace issues without print debugging
- **Production**: No production logging
- **Library Usage**: print() clutters stdout when used as library
- **Best Practices**: Python logging is standard, print() is amateur
- **Control**: Can't disable debug logs in production

## Acceptance Criteria

- [ ] Centralized logging configuration module created
- [ ] All library code uses logging instead of print()
- [ ] CLI output uses print() (user-facing is OK)
- [ ] Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- [ ] Environment variable for log level (WAFT_LOG_LEVEL)
- [ ] Optional file logging (WAFT_LOG_FILE)
- [ ] No print() in `src/waft/core/` (except CLI feedback)
- [ ] All tests pass
- [ ] Documentation updated

## Implementation Plan

### Step 1: Create Logging Configuration

Create `src/waft/logging_config.py`:

```python
"""
Centralized logging configuration for Waft.

Provides consistent logging across all modules with:
- Configurable log levels via environment variable
- Optional file logging
- Structured logging format
- Performance considerations
"""

import logging
import os
import sys
from pathlib import Path
from typing import Optional


# Default log level
DEFAULT_LOG_LEVEL = "INFO"

# Environment variables
ENV_LOG_LEVEL = "WAFT_LOG_LEVEL"
ENV_LOG_FILE = "WAFT_LOG_FILE"

# Log format
LOG_FORMAT = "%(asctime)s [%(levelname)8s] %(name)s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_log_level() -> int:
    """
    Get log level from environment or default.

    Returns:
        Log level (logging.DEBUG, logging.INFO, etc.)
    """
    level_name = os.getenv(ENV_LOG_LEVEL, DEFAULT_LOG_LEVEL).upper()
    return getattr(logging, level_name, logging.INFO)


def get_log_file() -> Optional[Path]:
    """
    Get log file path from environment if set.

    Returns:
        Path to log file or None
    """
    log_file = os.getenv(ENV_LOG_FILE)
    if log_file:
        return Path(log_file)
    return None


def setup_logging(
    level: Optional[int] = None,
    log_file: Optional[Path] = None,
    force: bool = False,
) -> None:
    """
    Setup logging configuration.

    Args:
        level: Log level (if None, reads from env)
        log_file: Optional file to log to (if None, reads from env)
        force: If True, reconfigure even if already configured
    """
    # Avoid reconfiguring if already setup
    if logging.getLogger("waft").handlers and not force:
        return

    # Get configuration
    if level is None:
        level = get_log_level()
    if log_file is None:
        log_file = get_log_file()

    # Create formatters
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # Setup root logger for waft
    logger = logging.getLogger("waft")
    logger.setLevel(level)
    logger.handlers.clear()  # Remove existing handlers

    # Console handler (stdout for INFO+, stderr for WARNING+)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (if log file specified)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)  # Log everything to file
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Log initial message
    logger.debug(f"Logging initialized at level {logging.getLevelName(level)}")
    if log_file:
        logger.debug(f"Logging to file: {log_file}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger
    """
    # Ensure logging is setup
    setup_logging()

    # Return logger under waft namespace
    return logging.getLogger(f"waft.{name}")


# Setup logging on import
setup_logging()
```

### Step 2: Replace print() with logging

**Pattern for library code**:

```python
# Old (BAD - library code):
print(f"Error: {message}")
print(f"Info: {info}")

# New (GOOD - library code):
from ..logging_config import get_logger

logger = get_logger(__name__)

logger.error(f"Error: {message}")
logger.info(f"Info: {info}")
```

**Pattern for CLI code**:

```python
# CLI user feedback (KEEP print() - this is OK):
from rich.console import Console

console = Console()
console.print("[green]✅ Success![/green]")
typer.echo("Project created!")

# Internal errors/info (USE logging):
from ..logging_config import get_logger

logger = get_logger(__name__)
logger.debug(f"Internal state: {state}")
logger.error(f"Unexpected error: {e}")
```

### Step 3: Update All Library Code

**High Priority** (Core library):
- [ ] src/waft/core/substrate.py
- [ ] src/waft/core/empirica.py
- [ ] src/waft/core/memory.py
- [ ] src/waft/core/gamification.py
- [ ] src/waft/utils.py

**Medium Priority** (Other modules):
- [ ] src/waft/core/*.py (all remaining)
- [ ] src/waft/api/*.py

**Low Priority / Keep print()** (CLI/User-facing):
- [ ] src/waft/main.py (review - CLI output OK)
- [ ] src/waft/commands/*.py (CLI output OK)
- [ ] demo.py (demo script - print() OK)

### Step 4: Add Logging Controls

**Environment Variables**:
```bash
# Set log level
export WAFT_LOG_LEVEL=DEBUG

# Enable file logging
export WAFT_LOG_FILE=~/.waft/debug.log

# Normal operation
export WAFT_LOG_LEVEL=WARNING
```

**In Code**:
```python
# main.py - add CLI flag
@app.command()
def serve(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable debug logging"),
):
    if verbose:
        setup_logging(level=logging.DEBUG, force=True)
    # ...
```

### Step 5: Update Documentation

Create `docs/LOGGING.md`:

```markdown
# Logging in Waft

## For Users

### Enable Debug Logging

```bash
# Temporary (current session)
export WAFT_LOG_LEVEL=DEBUG
waft verify

# Or use CLI flag
waft serve --verbose
```

### Log to File

```bash
export WAFT_LOG_FILE=~/.waft/debug.log
waft verify
```

### Log Levels

- `DEBUG`: Detailed information for diagnosing issues
- `INFO`: General informational messages (default)
- `WARNING`: Warning messages (something unexpected)
- `ERROR`: Error messages (something failed)
- `CRITICAL`: Critical errors (system cannot continue)

## For Developers

### Using Logging

```python
from waft.logging_config import get_logger

logger = get_logger(__name__)

logger.debug("Detailed debug info")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred", exc_info=True)
logger.critical("Critical failure")
```

### When to Use print() vs logging

**Use logging** (library code):
- Internal state changes
- Errors and warnings
- Debug information
- Anything users shouldn't always see

**Use print() or Rich console** (CLI code):
- User feedback (success messages)
- Progress indicators
- Interactive prompts
- CLI output

### Performance

Logging has minimal overhead. Use liberally for debugging, but:
- Avoid logging in tight loops
- Use appropriate log levels
- Let users control verbosity
```

## Testing Strategy

**Unit Tests**:
```python
def test_logging_configuration():
    """Test logging can be configured."""
    from waft.logging_config import setup_logging, get_logger

    setup_logging(level=logging.DEBUG, force=True)
    logger = get_logger("test")

    # Should not raise
    logger.debug("debug")
    logger.info("info")
    logger.error("error")
```

**Integration Tests**:
- Verify log levels control output
- Verify file logging works
- Verify no print() in library code (grep test)

**Manual Tests**:
```bash
# Test debug logging
WAFT_LOG_LEVEL=DEBUG waft verify

# Test file logging
WAFT_LOG_FILE=/tmp/waft.log waft verify
cat /tmp/waft.log

# Test production (minimal output)
WAFT_LOG_LEVEL=ERROR waft verify
```

## Files to Change

**New Files**:
- `src/waft/logging_config.py` (centralized config)
- `docs/LOGGING.md` (documentation)
- `tests/test_logging.py` (logging tests)

**Modified Files** (replace print() with logging):
- `src/waft/core/substrate.py`
- `src/waft/core/empirica.py`
- `src/waft/core/memory.py`
- `src/waft/core/gamification.py`
- `src/waft/utils.py`
- (All other library files with print())

**Review** (keep print() if CLI output):
- `src/waft/main.py`
- `src/waft/commands/*.py`

## Migration Checklist

For each file with print():
- [ ] Import get_logger
- [ ] Create module logger
- [ ] Replace print() with logger.info/debug/error
- [ ] Test the module
- [ ] Verify no print() remains (except CLI output)

## Benefits

**Debugging**:
- ✅ Can enable debug logs when needed
- ✅ Can log to file for analysis
- ✅ Structured, timestamped logs
- ✅ Log levels separate concerns

**Production**:
- ✅ Control verbosity per environment
- ✅ Production errors logged properly
- ✅ No stdout pollution

**Best Practices**:
- ✅ Follows Python logging conventions
- ✅ Professional codebase
- ✅ Easy to integrate with monitoring

## Related Issues

- Audit Finding: "No Logging System (MEDIUM)"
- Audit Finding: "print() Statements in Library Code"
- TKT-arch-006: Replace print() (depends on this)

## Commits

- (populated as work progresses)
