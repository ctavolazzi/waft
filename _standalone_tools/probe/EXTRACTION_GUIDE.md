# Extraction Guide - Moving Probe to Standalone Repo

This guide explains how to extract the Probe system from WAFT into its own standalone GitHub repository.

## Current Structure

The probe system exists in two places:

1. **WAFT Integration**: `src/waft/core/probe.py` (for use within WAFT)
2. **Standalone Ready**: `_standalone_tools/probe/` (prepared for extraction)

## Extraction Steps

### Step 1: Create New GitHub Repository

```bash
# Create new repo on GitHub (via web UI or gh CLI)
gh repo create probe-pokey-stick --public --description "Pokey Stick for Testing - Probe services, endpoints, and files"

# Or use your preferred name
gh repo create your-probe-repo-name --public
```

### Step 2: Copy Standalone Directory

```bash
# From WAFT project root
cp -r _standalone_tools/probe /path/to/new/repo
cd /path/to/new/repo
```

### Step 3: Initialize Git

```bash
cd /path/to/new/repo
git init
git add .
git commit -m "Initial commit: Probe system extracted from WAFT"
git branch -M main
git remote add origin https://github.com/ctavolazzi/probe-pokey-stick.git
git push -u origin main
```

### Step 4: Update Package Name (if needed)

Edit `pyproject.toml` to match your repository name:

```toml
[project]
name = "probe-pokey-stick"  # Change to match your repo name
```

### Step 5: Add Tests (Recommended)

Create `tests/` directory and add test files:

```bash
mkdir tests
# Add test_probe.py, etc.
```

### Step 6: Update Documentation

- Update `README.md` with correct repository URLs
- Add `LICENSE` file (MIT recommended)
- Add `.gitignore` if needed
- Add `CONTRIBUTING.md` if accepting contributions

### Step 7: Publish to PyPI (Optional)

```bash
# Build package
python -m build

# Upload to PyPI (requires account setup)
python -m twine upload dist/*
```

## Maintaining Connection to WAFT

### Option 1: Keep as Submodule

If you want WAFT to reference the standalone repo:

```bash
# In WAFT project
git submodule add https://github.com/ctavolazzi/probe-pokey-stick.git _standalone_tools/probe
```

### Option 2: Sync Changes

Create a sync script to keep both versions in sync:

```bash
# scripts/sync_probe_to_standalone.sh
#!/bin/bash
cp src/waft/core/probe.py _standalone_tools/probe/src/probe/probe.py
# Update other files as needed
```

### Option 3: Use as Dependency

Once published to PyPI, WAFT can use it as a dependency:

```toml
# In WAFT's pyproject.toml
dependencies = [
    "probe-pokey-stick>=0.1.0",
]
```

Then update WAFT code to import from the package:

```python
# Instead of: from waft.core.probe import ProbeCollector
from probe import ProbeCollector
```

## File Mapping

| WAFT Location | Standalone Location | Notes |
|--------------|---------------------|-------|
| `src/waft/core/probe.py` | `src/probe/probe.py` | Main code |
| `src/waft/core/PROBE_README.md` | `docs/README.md` | Documentation |
| `examples/probe_example.py` | `examples/example.py` | Example usage |
| N/A | `pyproject.toml` | Package config |
| N/A | `README.md` | Main README |
| N/A | `LICENSE` | License file |

## Checklist Before Extraction

- [ ] All code is self-contained (no WAFT-specific imports)
- [ ] Dependencies are minimal (only `requests`)
- [ ] Documentation is complete
- [ ] Examples work independently
- [ ] Tests are written (recommended)
- [ ] License is added
- [ ] `.gitignore` is configured
- [ ] Package name is appropriate
- [ ] Version is set (0.1.0 for initial release)

## Post-Extraction

After extraction:

1. **Update WAFT**: Decide whether to keep local copy or use as dependency
2. **Version Management**: Use semantic versioning (0.1.0, 0.2.0, etc.)
3. **CI/CD**: Set up GitHub Actions for testing and publishing
4. **Documentation**: Keep docs updated as features are added
5. **Releases**: Tag releases in git for version tracking

## Future Development

Once extracted, the probe system can evolve independently:

- Add new probe types (DatabaseProbe, KubernetesProbe, etc.)
- Add CLI interface
- Add web dashboard
- Add integrations with monitoring tools
- Add plugins/extensions system

## Questions?

If you need help with extraction, check:
- [GitHub Docs](https://docs.github.com/en/repositories/creating-and-managing-repositories)
- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Publishing Guide](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/)
