# WAFT Installation Template

This folder structure serves as a template for new WAFT installations.

## Structure

```
.waft_template/
├── tools/
│   └── _pyrite/          # Work effort management system
│       ├── active/       # Current work efforts
│       ├── backlog/      # Future work
│       └── standards/    # Project standards
└── README.md             # This file
```

## Usage

To use this as a starting point for a new WAFT project:

1. Copy this folder structure to your project root
2. Rename `.waft_template` to match your project structure
3. Initialize WAFT: `waft init`
4. Start tracking work in `tools/_pyrite/active/`

## About _pyrite

The `_pyrite` system provides:
- **Work effort tracking** - Discrete units of intellectual labor
- **Epistemic memory** - What the system knows and doesn't know
- **Perspective-taking** - AI systems can "wear" previous perspectives
- **Recursive improvement** - System can improve based on its own observations

See `meta_cognition_explanation.md` for the full explanation.
