# cognitive_prosthetics_cli

Standalone CLI package for deterministic environment and repository readiness checks.

## Install

```bash
cd cognitive_prosthetics_cli
pip install -e .
```

## Usage

```bash
cprost check
cprost check --json
```

## Manifest

By default, `cprost check` looks for `repositories.json` in the current working directory.
If that file is not present, it falls back to a small in-code default manifest.

You can pass a custom manifest file with:

```bash
cprost check --manifest /absolute/path/to/repositories.json
```

Example shape:

```json
{
  "repositories": [
    {
      "id": "waft",
      "name": "waft",
      "path": "~/Code/active/waft",
      "required_paths": [
        "README.md",
        "src/waft/main.py"
      ]
    }
  ]
}
```

## Exit Code Contract

- `0`: all required checks pass
- `1`: at least one required check fails
