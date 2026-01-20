# Troubleshooting Guide

> **Solutions to common WAFT problems and issues**

Version 0.9.0 - Troubleshooting Reference

---

## 📋 Table of Contents

1. [Quick Diagnostics](#quick-diagnostics)
2. [Installation Issues](#installation-issues)
3. [Project Creation Problems](#project-creation-problems)
4. [CLI Command Errors](#cli-command-errors)
5. [Dependency Issues](#dependency-issues)
6. [Runtime Errors](#runtime-errors)
7. [Performance Problems](#performance-problems)
8. [Desktop App Issues](#desktop-app-issues)
9. [Getting More Help](#getting-more-help)

---

## Quick Diagnostics

Before diving into specific issues, run these quick diagnostic commands:

```bash
# Check WAFT installation
waft --version

# Verify project structure
waft verify

# Get project info
waft info

# Check Python version
python --version

# Check uv installation
uv --version

# Check system resources
df -h  # Disk space
free -h  # Memory (Linux)
```

---

## Installation Issues

### Problem: `command not found: waft`

**Symptoms**:
```bash
$ waft --version
bash: waft: command not found
```

**Causes**:
- uv tool bin directory not in PATH
- WAFT not installed properly
- Shell configuration not updated

**Solutions**:

1. **Check if WAFT is installed**:
   ```bash
   uv tool list
   ```
   If WAFT is not listed, install it:
   ```bash
   uv tool install waft
   ```

2. **Add uv bin to PATH**:
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   export PATH="$HOME/.local/bin:$PATH"

   # Reload shell
   source ~/.bashrc  # or ~/.zshrc
   ```

3. **Use full path temporarily**:
   ```bash
   ~/.local/bin/waft --version
   ```

### Problem: `ModuleNotFoundError: No module named 'waft'`

**Symptoms**:
```python
from waft import Foundation
ModuleNotFoundError: No module named 'waft'
```

**Causes**:
- WAFT not installed in current environment
- Wrong Python environment activated
- Import error in code

**Solutions**:

1. **Install WAFT in current environment**:
   ```bash
   pip install waft
   # or
   uv pip install waft
   ```

2. **Check which Python is running**:
   ```bash
   which python
   python --version
   ```

3. **Activate correct environment**:
   ```bash
   # If using venv
   source venv/bin/activate

   # If using conda
   conda activate myenv
   ```

### Problem: Python version incompatibility

**Symptoms**:
```
ERROR: Python 3.9.x is not supported. Requires Python 3.10+
```

**Solutions**:

1. **Install Python 3.10+ using uv**:
   ```bash
   uv python install 3.10
   uv python pin 3.10
   ```

2. **Or use system package manager**:
   ```bash
   # macOS
   brew install python@3.10

   # Ubuntu/Debian
   sudo apt-get install python3.10

   # Arch
   sudo pacman -S python310
   ```

3. **Verify installation**:
   ```bash
   python3.10 --version
   ```

---

## Project Creation Problems

### Problem: `Project already exists`

**Symptoms**:
```bash
$ waft new my_lab
ERROR: Directory 'my_lab' already exists
```

**Solutions**:

1. **Use a different name**:
   ```bash
   waft new my_lab_v2
   ```

2. **Remove existing directory** (if safe):
   ```bash
   rm -rf my_lab
   waft new my_lab
   ```

3. **Use `waft init` on existing project**:
   ```bash
   cd my_lab
   waft init
   ```

### Problem: Permission denied during creation

**Symptoms**:
```bash
$ waft new my_lab
ERROR: Permission denied: /home/user/my_lab
```

**Solutions**:

1. **Check directory permissions**:
   ```bash
   ls -la
   ```

2. **Create in user home directory**:
   ```bash
   cd ~
   waft new my_lab
   ```

3. **Fix permissions** (if you own the directory):
   ```bash
   chmod 755 /path/to/parent
   ```

### Problem: `_pyrite` structure not created

**Symptoms**:
- Project created but `_pyrite/` directory missing
- `waft verify` fails

**Solutions**:

1. **Manually create structure**:
   ```bash
   cd my_lab
   mkdir -p _pyrite/{active,backlog,standards,gym_logs,genesis}
   waft verify
   ```

2. **Reinitialize**:
   ```bash
   cd my_lab
   waft init
   ```

3. **Check for errors in creation log**:
   ```bash
   # Run with debug output
   WAFT_DEBUG=1 waft new my_lab
   ```

---

## CLI Command Errors

### Problem: `Invalid command`

**Symptoms**:
```bash
$ waft evolv
ERROR: No such command 'evolv'
```

**Solutions**:

1. **Check spelling**:
   ```bash
   waft evolve  # Correct
   ```

2. **List available commands**:
   ```bash
   waft --help
   ```

3. **Check command exists in your version**:
   ```bash
   waft --version
   # Some commands only available in later versions
   ```

### Problem: `Missing required option`

**Symptoms**:
```bash
$ waft spawn
ERROR: Missing option '--agent'
```

**Solutions**:

1. **Provide required options**:
   ```bash
   waft spawn --agent MyAgent
   ```

2. **Check command help**:
   ```bash
   waft spawn --help
   ```

3. **Use environment variables** (if supported):
   ```bash
   export WAFT_AGENT=MyAgent
   waft spawn
   ```

### Problem: Command hangs or freezes

**Symptoms**:
- Command doesn't complete
- No output for extended time
- CPU at 100%

**Solutions**:

1. **Cancel and try again**:
   ```bash
   Ctrl+C  # Cancel
   waft verify  # Try again
   ```

2. **Check for infinite loops in agents**:
   ```python
   # Look for while True without exit conditions
   ```

3. **Increase timeout** (if supported):
   ```bash
   waft eval --timeout 300
   ```

4. **Run with debug output**:
   ```bash
   WAFT_DEBUG=1 waft command
   ```

---

## Dependency Issues

### Problem: `uv.lock` out of sync

**Symptoms**:
```bash
$ waft sync
ERROR: uv.lock is out of sync with pyproject.toml
```

**Solutions**:

1. **Update lock file**:
   ```bash
   uv lock --update
   ```

2. **Sync dependencies**:
   ```bash
   waft sync
   ```

3. **Regenerate if corrupted**:
   ```bash
   rm uv.lock
   waft sync
   ```

### Problem: Dependency conflicts

**Symptoms**:
```
ERROR: Cannot install package X because of conflict with package Y
```

**Solutions**:

1. **Check versions in `pyproject.toml`**:
   ```toml
   dependencies = [
       "package-x>=1.0.0,<2.0.0",  # Be specific
   ]
   ```

2. **Update conflicting packages**:
   ```bash
   waft add "package-x>=2.0.0"
   ```

3. **Create fresh environment**:
   ```bash
   rm -rf .venv
   waft sync
   ```

### Problem: Package not found

**Symptoms**:
```
ERROR: Could not find a version that satisfies the requirement package-x
```

**Solutions**:

1. **Check package name spelling**:
   ```bash
   # Search on PyPI
   pip search package-x
   ```

2. **Check package exists**:
   - Visit https://pypi.org/
   - Search for package

3. **Specify correct index**:
   ```bash
   uv add package-x --index-url https://pypi.org/simple
   ```

---

## Runtime Errors

### Problem: `ImportError` in agents

**Symptoms**:
```python
ImportError: cannot import name 'Something' from 'module'
```

**Solutions**:

1. **Check imports in agent code**:
   ```python
   # Verify module names and import paths
   from waft.being import Being  # Correct
   # not
   from waft import Being  # Wrong
   ```

2. **Verify dependencies installed**:
   ```bash
   waft sync
   ```

3. **Check Python path**:
   ```python
   import sys
   print(sys.path)
   ```

### Problem: `AttributeError` on objects

**Symptoms**:
```python
AttributeError: 'Being' object has no attribute 'genome_id'
```

**Solutions**:

1. **Check WAFT version**:
   ```bash
   waft --version
   # Some attributes added in later versions
   ```

2. **Initialize object correctly**:
   ```python
   being = Being(
       name="Test",
       being_type="Warforged Wizard"
   )
   # Don't access attributes before initialization
   ```

3. **Check API documentation**:
   - See [API Reference](api/API_INDEX.md)

### Problem: JSON decoding errors

**Symptoms**:
```
JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Solutions**:

1. **Validate JSON files**:
   ```bash
   # Check file
   cat _pyrite/genesis/20.00_state.json | python -m json.tool
   ```

2. **Fix malformed JSON**:
   - Remove trailing commas
   - Ensure proper quotes
   - Validate structure

3. **Regenerate if corrupted**:
   ```bash
   # Backup first
   cp _pyrite/genesis/20.00_state.json backup.json
   # Regenerate
   waft init
   ```

---

## Performance Problems

### Problem: Slow command execution

**Symptoms**:
- Commands take unusually long
- High CPU usage
- System becomes unresponsive

**Solutions**:

1. **Check system resources**:
   ```bash
   top  # or htop
   ```

2. **Limit parallel operations**:
   ```bash
   # If spawning variants
   waft spawn --variants 5  # Reduce from 10
   ```

3. **Clear caches**:
   ```bash
   # Clear Python cache
   find . -type d -name __pycache__ -exec rm -rf {} +

   # Clear uv cache
   uv cache clean
   ```

4. **Optimize database**:
   ```bash
   # If using TinyDB
   sqlite3 waft_memory.db "VACUUM;"
   ```

### Problem: Large memory usage

**Symptoms**:
- System running out of memory
- Slow performance
- Swap usage high

**Solutions**:

1. **Monitor memory**:
   ```bash
   # Linux
   free -h

   # macOS
   vm_stat
   ```

2. **Process files in streams**:
   ```python
   # Don't load entire file
   with open("large_file.txt") as f:
       for line in f:  # Stream line by line
           process(line)
   ```

3. **Limit batch sizes**:
   ```python
   # Process in chunks
   for chunk in chunks(large_list, size=100):
       process_chunk(chunk)
   ```

### Problem: Disk space issues

**Symptoms**:
```
OSError: [Errno 28] No space left on device
```

**Solutions**:

1. **Check disk usage**:
   ```bash
   df -h
   du -sh _pyrite/*
   ```

2. **Clean up old logs**:
   ```bash
   # Remove old gym logs
   find _pyrite/gym_logs -type f -mtime +30 -delete
   ```

3. **Clean uv cache**:
   ```bash
   uv cache clean
   ```

---

## Desktop App Issues

### Problem: Electron app won't start

**Symptoms**:
- App window doesn't open
- No error message
- Process starts then exits

**Solutions**:

1. **Check logs**:
   ```bash
   # macOS
   ~/Library/Logs/waft/main.log

   # Linux
   ~/.config/waft/logs/main.log
   ```

2. **Run from terminal**:
   ```bash
   cd dnd_campaign_desktop_app
   npm start
   ```

3. **Rebuild dependencies**:
   ```bash
   cd dnd_campaign_desktop_app
   rm -rf node_modules
   npm install
   ```

### Problem: Docker container issues

**Symptoms**:
- Container won't start
- VNC connection fails
- Display errors

**Solutions**:

1. **Check container status**:
   ```bash
   docker ps -a
   docker logs container_name
   ```

2. **Restart container**:
   ```bash
   docker restart container_name
   ```

3. **Rebuild image**:
   ```bash
   docker build -t waft-app .
   docker run -d -p 5900:5900 waft-app
   ```

4. **Check port conflicts**:
   ```bash
   lsof -i :5900  # VNC port
   lsof -i :8000  # FastAPI port
   ```

---

## Getting More Help

### Debug Mode

Enable debug output for more information:

```bash
# Set environment variable
export WAFT_DEBUG=1
export WAFT_LOG_LEVEL=DEBUG

# Run command
waft command
```

### Log Files

Check log files for detailed error information:

```bash
# Project logs
cat _pyrite/logs/waft.log

# System logs
# macOS
tail -f ~/Library/Logs/waft/debug.log

# Linux
tail -f ~/.local/share/waft/logs/debug.log
```

### Verbose Output

Most commands support `--verbose` flag:

```bash
waft verify --verbose
waft sync --verbose
```

### Community Support

1. **GitHub Issues**: Report bugs
   - https://github.com/ctavolazzi/waft/issues

2. **GitHub Discussions**: Ask questions
   - https://github.com/ctavolazzi/waft/discussions

3. **Documentation**: Check docs
   - [Documentation Index](DOCUMENTATION_INDEX.md)
   - [FAQ](FAQ.md)

### Diagnostic Information

When reporting issues, include:

```bash
# System info
uname -a
python --version
waft --version

# Project info
waft info
waft verify

# Environment
pip list | grep waft
env | grep WAFT
```

### Clean Reinstall

If all else fails, try a clean reinstall:

```bash
# 1. Uninstall
uv tool uninstall waft

# 2. Clear cache
uv cache clean
rm -rf ~/.cache/uv

# 3. Reinstall
uv tool install waft

# 4. Verify
waft --version
```

---

## Common Error Messages

### Error: "Project not found"

**Fix**: Run command from project directory
```bash
cd my_lab
waft verify
```

### Error: "Invalid configuration"

**Fix**: Check `pyproject.toml` syntax
```bash
# Validate TOML
python -c "import tomli; tomli.load(open('pyproject.toml', 'rb'))"
```

### Error: "Database locked"

**Fix**: Close other WAFT processes
```bash
# Find processes
ps aux | grep waft

# Kill if needed
kill <pid>
```

### Error: "Git repository not found"

**Fix**: Initialize git repository
```bash
git init
git add .
git commit -m "Initial commit"
```

---

## Prevention Tips

### 1. Keep WAFT Updated

```bash
uv tool upgrade waft
```

### 2. Regular Verification

```bash
# Run periodically
waft verify
```

### 3. Backup Important Data

```bash
# Backup _pyrite
tar -czf pyrite_backup.tar.gz _pyrite/
```

### 4. Use Version Control

```bash
# Commit regularly
git add .
git commit -m "Save progress"
```

### 5. Monitor Resources

```bash
# Check disk space
df -h

# Check memory
free -h
```

---

**Still having issues?** Open an issue on [GitHub](https://github.com/ctavolazzi/waft/issues) with:
- Error message
- Steps to reproduce
- System information
- WAFT version

---

*Last Updated: 2026-01-16 | Version: 0.9.0 | Troubleshooting Guide v1.0*
