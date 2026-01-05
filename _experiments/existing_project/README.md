# Existing Project

> Project created with [Waft](https://github.com/ctavolazzi/waft) - Ambient Meta-Framework for Python

## Quick Start

```bash
# Install dependencies
uv sync

# Or use just
just setup

# Run tests
just test

# Verify project structure
waft verify
```

## Project Structure

```
.
├── pyproject.toml          # uv project config
├── _pyrite/
│   ├── active/             # Current work
│   ├── backlog/            # Future work
│   └── standards/          # Standards
├── .github/workflows/
│   └── ci.yml              # CI/CD pipeline
├── Justfile                # Task runner
└── src/
    └── agents.py           # CrewAI template (optional)
```

## Development

```bash
# Run all checks
just check

# Format code
just format

# Lint code
just lint

# Clean generated files
just clean
```

## License

MIT
