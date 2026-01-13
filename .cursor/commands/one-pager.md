# /one-pager - One-Pager Creator

**Purpose:** Create crystalized, printable 2-page (front/back) one-pagers from any content

**Usage:** `/one-pager [content] [options]`

**Script:** `scripts/create_one_pager.py`

---

## Overview

The One-Pager tool creates perfect 2-page printable documents from any content type:
- Markdown files/text
- Plain text
- Code files
- JSON/YAML data
- Python dictionaries
- HTML content

**Philosophy:** "Physical constellation of crystallized knowledge inside spacetime through the refraction of light" - Christopher Tavolazzi

Perfect for academic nerds who love physical binders full of paper.

---

## Quick Start

### From Markdown File
```
/one-pager file:README.md title:"README One-Pager"
```

### From Text Content
```
/one-pager text:"# My Document\n\nContent here" title:"My One-Pager"
```

### From Dictionary/JSON
```
/one-pager json:'{"title": "Config", "version": "0.5.0"}' title:"Config One-Pager"
```

### Briefing Document (NEW!)
```
/one-pager --briefing title:"Session Briefing"
```

Generates a field guide style 2-page briefing with:
- Current system status (git, work efforts, health)
- Chat context (what we're doing, recent topics)
- Larger context (project state, epistemic state)

Perfect for "at a glance" session documentation.

---

## Features

- **Automatic Format Detection**: Detects markdown, code, JSON, plain text
- **Smart Content Processing**: Converts any format to printable HTML
- **Exact 2-Page Constraint**: Always creates front/back of one sheet
- **Printer-Friendly**: Black and white, minimal ink usage
- **Intelligent Expansion**: Adds content if too short, condenses if too long
- **Multiple Input Types**: Files, strings, dictionaries, lists
- **Briefing Mode**: Field guide style briefing with system status and chat context

---

## Usage Examples

### Markdown
```
/one-pager markdown:"# Title\n\nContent" title:"My Doc"
```

### File Path
```
/one-pager file:docs/STUDY_GYM_GUIDE.md
```

### Dictionary
```
/one-pager dict:'{"key": "value", "list": [1,2,3]}'
```

### Code File
```
/one-pager file:src/waft/one_pager.py title:"One-Pager Source"
```

---

## Output

All one-pagers are saved to:
- `_work_efforts/one_pagers/[title]_[date].pdf`

Format:
- **2 pages exactly** (front and back of one sheet)
- **Printer-friendly** (black and white)
- **Professional formatting** (field guide style)
- **Ready for binder** (standard letter size)

---

## Integration

The One-Pager tool is part of WAFT's document generation system:

```python
from waft import OnePager

# From markdown
pager = OnePager.from_markdown("# Title\n\nContent", title="My Doc")
pager.generate()

# From file
pager = OnePager.from_file("README.md", title="README")
pager.generate()

# From dictionary
pager = OnePager.from_dict({"key": "value"}, title="Config")
pager.generate()

# Quick function
from waft import create_one_pager
create_one_pager("# Title\n\nContent", title="My Doc")
```

---

## Use Cases

- **Quick Reference**: Create one-pagers from documentation
- **Code Summaries**: Print code files as reference sheets
- **Configuration Docs**: Print config files for physical storage
- **Meeting Notes**: Convert notes to printable format
- **Research Gists**: Crystallize research findings
- **Binder Organization**: Build physical knowledge constellation
- **Session Briefings**: Generate "at a glance" status documents with system state and chat context

---

## Philosophy

> "I'm an academic nerd scientist I like binders full of paper it's cool to me the physical constellation of crystallized knowledge inside spacetime through the refraction of light"

This tool enables that. Create one-pagers from anything, print them, and build your physical knowledge constellation.

---

**Created with ❤️ for physical knowledge management.**
