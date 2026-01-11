# WAFT Framework Documentation Generator

This tool generates comprehensive documentation about how WAFT functions by inspecting itself.

## Purpose

Creates a beautiful, full-featured PDF documentation booklet that describes:
- WAFT's architecture and structure
- Core components and their functions
- Template system
- Binder system
- Reflection system
- How everything works together

## Key Feature

**The documentation is NOT hardcoded** - it's generated dynamically by WAFT inspecting itself:
- Scans the codebase using AST analysis
- Extracts information about modules, classes, functions
- Analyzes architecture and relationships
- Generates documentation based on actual findings
- Updates automatically as WAFT evolves

## Usage

```bash
python3 tools/framework_documentation/generate_framework_docs.py
```

The script will:
1. Scan WAFT's codebase
2. Analyze structure and components
3. Extract information about how things work
4. Generate a beautiful PDF booklet
5. Open it automatically

## Output

- `WAFT_Framework_Documentation.pdf` - Complete framework documentation
