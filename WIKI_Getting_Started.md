# Getting Started with WAFT

**Quick start guide to get WAFT up and running in 5 minutes.**

---

## Installation

### Prerequisites

- **Python**: 3.10 or higher
- **uv**: Python package manager (recommended) or pip

### Install WAFT

```bash
# Using uv (recommended)
uv tool install waft

# Or using pip
pip install waft
```

### Verify Installation

```bash
waft --version
# Should output: 0.9.3
```

---

## Quick Start

### 1. Create a New Project

```bash
waft new my_laboratory
cd my_laboratory
```

This creates a complete WAFT project structure with:
- `_pyrite/` - Memory layer (active/, backlog/, standards/)
- `pyproject.toml` - Project configuration
- `Justfile` - Common tasks
- `.github/workflows/` - CI/CD templates

### 2. Verify the Substrate

```bash
waft verify
```

This checks:
- Project structure integrity
- Dependencies installed
- Configuration valid
- Git repository status

### 3. Generate Your First PDF

```python
from src.waft.evolution.pdf_generator import generate_pdf

pdf_path = generate_pdf(
    content="# My First Document\n\nThis is WAFT!",
    title="My First WAFT Document",
    style="clinical_standard"
)
# PNG screenshot automatically created for visual verification
```

---

## Next Steps

### Learn the Core Concepts

1. **[The Substrate](The-Substrate)** - Self-modifying agents
2. **[The Physics](The-Physics)** - Scint System and fitness
3. **[The Flight Recorder](The-Flight-Recorder)** - Lineage tracking

### Try the Evolutionary Iteration Process

1. Generate a PDF
2. Check the PNG screenshot (created automatically)
3. Identify visual issues
4. Fix and regenerate
5. Compare before/after

**Learn more**: [Evolutionary Iteration Process](Evolutionary-Iteration-Process)

### Explore Examples

- `examples/` - Example scripts and demos
- `docs/` - Complete documentation
- `_work_efforts/` - Real-world usage examples

---

## Common Commands

```bash
# Project management
waft new <name>          # Create new project
waft verify              # Verify project structure
waft info                # Show project information
waft sync                # Sync dependencies

# Document generation
waft docs                # Generate documentation
waft status              # System status

# Evolution system
waft spawn               # Spawn agent variants
waft eval                # Evaluate fitness
waft evolve              # Evolve to fittest
```

---

## Getting Help

- **Documentation**: [docs/](https://github.com/ctavolazzi/waft/tree/main/docs)
- **Issues**: [GitHub Issues](https://github.com/ctavolazzi/waft/issues)
- **Examples**: `examples/` directory

---

**Welcome to WAFT! Start evolving your agents today.**
