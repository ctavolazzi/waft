# WAFT Installation Guide

This guide will help you install and set up WAFT in your project.

## Quick Start

### Option 1: Use Demo Output as Template

The easiest way to get started is to use the demo output as a template:

```bash
# Run the demo
python3 examples/interactive_demo.py

# Copy demo structure to your project
cp -r demo_output my_project

# Navigate to your project
cd my_project

# Initialize WAFT
waft init
```

### Option 2: Manual Installation

1. **Install WAFT**:
   ```bash
   pip install waft
   ```

2. **Create project structure**:
   ```bash
   mkdir my_project
   cd my_project
   waft init
   ```

3. **Set up _pyrite**:
   ```bash
   waft memory init
   ```

## Project Structure

A typical WAFT project has this structure:

```
my_project/
├── tools/
│   └── _pyrite/          # Work effort management
│       ├── active/       # Current work
│       ├── backlog/      # Future work
│       └── standards/    # Project standards
├── _work_efforts/        # Work effort tracking
└── README.md
```

## Initial Setup

After installation:

1. **Review the structure** - Understand how WAFT organizes work
2. **Create your first work effort** - Start tracking your projects
3. **Set up standards** - Define your project standards
4. **Start journaling** - Begin tracking your thoughts and learnings

## Next Steps

- Read the [Meta-Cognitive Demonstration](Meta-Cognitive-Demonstration.md)
- Review [Work Effort System](work-effort-system.md) documentation
- Check out [Examples](../examples/) for more usage patterns

## Troubleshooting

### Demo doesn't run

Make sure you have all dependencies:
```bash
pip install weasyprint rich typer
```

### PDF generation fails

WeasyPrint requires system dependencies. See [WeasyPrint installation guide](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation).

### Import errors

Make sure you're in the WAFT project root when running examples:
```bash
cd /path/to/waft
python3 examples/interactive_demo.py
```

## Support

For issues or questions:
- Check the [GitHub Issues](https://github.com/ctavolazzi/waft/issues)
- Review the [Documentation](../docs/)
- Read the [Wiki](../.github/wiki/)
