# Waft

> **Ambient, self-modifying Meta-Framework for Python**

Waft is the "Operating System" for your projects, gently orchestrating:
- **Environment** (`uv`) - Python package management
- **Memory** (`_pyrite`) - Persistent project structure
- **Agents** (`crewai`) - AI agent capabilities (optional)
- **Epistemic Tracking** (`Empirica`) - Knowledge and learning measurement

## Quick Start

```bash
# Install Waft
uv tool install waft

# Create a new project
waft new my_awesome_project

# Verify project structure
cd my_awesome_project
waft verify
```

## What Waft Creates

When you run `waft new <name>`, it creates:

- ✅ **uv project** - Fully configured Python project
- ✅ **_pyrite structure** - Memory folders (active/, backlog/, standards/)
- ✅ **Justfile** - Modern task runner with standard recipes
- ✅ **CI/CD** - GitHub Actions workflow for validation
- ✅ **CrewAI template** - Starter template for AI agents

## Commands

### `waft new <name>`

Creates a new project with full Waft structure:

```bash
waft new my_project
```

### `waft verify`

Verifies the project structure:

```bash
waft verify
```

Checks:
- `_pyrite` directory structure
- `uv.lock` existence
- Project configuration

## Philosophy

Waft is **ambient** - it works quietly in the background, setting up the infrastructure so you can focus on building.

Waft is **self-modifying** - projects created with Waft can evolve and adapt.

Waft is a **meta-framework** - it doesn't replace your tools, it orchestrates them.

## Installation

```bash
# Using uv (recommended)
uv tool install waft

# Or from source
git clone https://github.com/ctavolazzi/waft.git
cd waft
uv sync
uv tool install --editable .
```

### Development Mode

When developing waft itself, **always use `--editable` mode**:

```bash
uv tool install --editable .
```

This ensures code changes are immediately reflected when running `waft` commands.
Without `--editable`, you must reinstall after each code change.

**Quick reinstall script:**
```bash
./scripts/dev-reinstall.sh
```

## Requirements

- Python 3.10+
- `uv` package manager ([install](https://github.com/astral-sh/uv))
- `just` task runner (optional, [install](https://github.com/casey/just))

### Optional Dependencies

- **CrewAI**: For AI agent capabilities. Install with `uv sync --extra crewai` in projects that need it.
  - Note: Requires macOS 13.0+ due to onnxruntime dependency

## Project Structure

A Waft project includes:

```
my_project/
├── pyproject.toml          # uv project config
├── _pyrite/
│   ├── active/             # Current work
│   ├── backlog/            # Future work
│   └── standards/          # Standards
├── .github/workflows/
│   └── ci.yml              # CI/CD pipeline
├── Justfile                # Task runner
└── src/
    └── agents.py           # CrewAI template
```

## License

MIT

## Repository

https://github.com/ctavolazzi/waft

