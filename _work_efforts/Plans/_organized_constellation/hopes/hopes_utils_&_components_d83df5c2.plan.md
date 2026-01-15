---
name: Utils & Components
overview: Create a component library in _includes/components/, a utils/ directory with utility scripts, and generate a filetree document.
todos:
  - id: create-gitignore
    content: Create .gitignore for Jekyll
    status: pending
  - id: create-components
    content: Create component library in _includes/components/
    status: pending
    dependencies:
      - create-gitignore
  - id: create-utils
    content: Create utils/ directory with utility scripts
    status: pending
    dependencies:
      - create-components
  - id: generate-filetree
    content: Generate and save FILETREE.txt
    status: pending
    dependencies:
      - create-utils
  - id: commit-all
    content: Commit and push all changes
    status: pending
    dependencies:
      - generate-filetree

category: hopes
confidence: 1.00
constellation_date: 2026-01-14
---

# Utils & Component Library

## 1. Component Library

Create `_includes/components/` with reusable Jekyll components and an index:

| File | Description |
|------|-------------|
| `_includes/components/index.md` | Documentation of all components |
| `_includes/components/button.html` | Button component |
| `_includes/components/alert.html` | Alert/notice box |
| `_includes/components/badge.html` | Status badge |
| `_includes/components/callout.html` | Callout/highlight box |

## 2. Utils Directory

Create `utils/` with standalone utility scripts:

| File | Description |
|------|-------------|
| `utils/filetree.sh` | Generate filetree of project |
| `utils/uuid.sh` | Generate UUID filenames |
| `utils/timestamp.sh` | Output formatted timestamps |
| `utils/random-name.sh` | Generate random project names |
| `utils/logger.sh` | Simple logging utility |
| `utils/README.md` | Documentation for all utils |

## 3. Filetree Document

Generate and save `FILETREE.txt` in project root showing current structure.

## 4. Gitignore

Create `.gitignore` to ignore `_site/`, caches, etc.