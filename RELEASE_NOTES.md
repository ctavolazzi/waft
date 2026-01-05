# Waft v0.0.1 - Initial Release

🌊 **Waft** - Ambient, self-modifying Meta-Framework for Python

## What's New

This is the initial release of Waft, a meta-framework that orchestrates:
- **Environment** (`uv`) - Python package management
- **Memory** (`_pyrite`) - Persistent project structure
- **Agents** (`crewai`) - AI agent capabilities

## Features

- ✅ `waft new <name>` - Create new projects with full structure
- ✅ `waft verify` - Verify project structure
- ✅ Automatic `_pyrite` folder creation
- ✅ Template generation (Justfile, CI, CrewAI agents)
- ✅ Full `uv` integration

## Installation

```bash
uv tool install waft
```

## Quick Start

```bash
waft new my_project
cd my_project
waft verify
```

## Documentation

See [README.md](https://github.com/ctavolazzi/waft/blob/main/README.md) for full documentation.

---

**Full Changelog**: https://github.com/ctavolazzi/waft/compare/v0.0.1...main

