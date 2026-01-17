# Meta-Cognitive Demonstration

The WAFT Meta-Cognitive Demonstration is a comprehensive walkthrough of WAFT's unique capabilities, showing how the system tracks its own work and enables continuity across AI sessions.

## Overview

The demonstration showcases:
- Basic file organization (2022 ChatGPT level)
- Work effort management system (_pyrite)
- Epistemic memory through text-based tracking
- Meta-cognitive perspective-taking
- Recursive self-improvement foundation

## Running the Demo

```bash
python3 examples/interactive_demo.py
```

The demo will:
1. Create a demo folder structure
2. Organize files into logical categories
3. Install and demonstrate the _pyrite system
4. Create work efforts and journal entries
5. Explain meta-cognitive concepts
6. Generate a PDF booklet
7. Open the booklet automatically

## What You'll See

### Step 1: Creating a Demo Folder
The demo starts by creating a messy folder with files scattered everywhere, demonstrating the need for organization.

### Step 2: Cleaning Up
Files are organized into logical categories:
- `documents/` - Text files, markdown, PDFs
- `scripts/` - Python scripts
- `data/` - JSON, CSV, YAML files
- `temp/` - Temporary files

### Step 3: Creating Tools Folder
A `tools/` folder is created to house WAFT-specific tooling.

### Step 4: Installing _pyrite
The _pyrite work effort management system is installed, creating:
- `_pyrite/active/` - Current work efforts
- `_pyrite/backlog/` - Future work
- `_pyrite/standards/` - Project standards

### Step 5: Work Effort Management
A basic work effort and journal entry are created to demonstrate tracking.

### Step 6: Meta-Cognition Explanation
The core concept is explained: how WAFT tracks what it knows and doesn't know through text-based epistemic memory.

## The Core Concept

**Why _pyrite?**

So that WAFT can track on its own what it knows and what it doesn't.

The work efforts ticketing system acts as a sort of **rudimentary epistemic memory** - a journal that any LLM can pick up and wear like a pair of glasses to see how the previous AI saw its world.

**This is perspective taking.**

This is a very, very, very basic, very very very simple form of LLM meta-cognition across architectures using a work efforts and journaling system to track "thoughts" or **intellectual labor quanta** in the form of text in the WAFT system, which can self-modify and recursively self-improve based on external and internal feedback.

## Intellectual Labor Quanta

Each work effort, journal entry, or documentation piece represents a **quantum of intellectual labor** - a discrete unit of thought and work that can be tracked, measured, and built upon.

## Cross-Architecture Meta-Cognition

This system works across different AI architectures because it's based on **text** - the universal interface. Any LLM can read and understand:
- Work effort descriptions
- Journal entries
- Documentation
- Status updates

This creates a form of **perspective-taking** where one AI can understand how another AI (or a previous version of itself) saw the world.

## Output

The demo generates:
- **Organized folder structure** - Ready to use as a template
- **PDF booklet** - Complete documentation of the demo
- **Meta-cognition explanation** - Detailed explanation of concepts
- **Work effort examples** - Sample work efforts and journals

## Using Demo as Template

The `demo_output/` folder can serve as a jumping off point for full WAFT installations:

1. Review the structure
2. Copy to your project
3. Initialize WAFT: `waft init`
4. Start tracking work in `tools/_pyrite/active/`

## Related Documentation

- [Meta-Cognition Explanation](meta-cognition-explanation.md)
- [Work Effort System](work-effort-system.md)
- [Installation Guide](installation-guide.md)
