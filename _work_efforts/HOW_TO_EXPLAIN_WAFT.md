# How to Explain Waft to Someone

**Created**: 2026-01-04
**Purpose**: Clear explanations for different audiences

---

## The 30-Second Elevator Pitch

**"Waft is like an operating system for Python projects. Instead of manually setting up project structure, dependencies, CI/CD, and documentation every time, you run one command and get a fully configured project with best practices built in."**

---

## The 2-Minute Explanation

### What It Is

**Waft** is a **meta-framework** for Python projects. Think of it as a project generator that sets up everything you need for modern Python development:

- ✅ **Project structure** - Organized folders and files
- ✅ **Dependency management** - Uses `uv` (fast Python package manager)
- ✅ **CI/CD pipeline** - GitHub Actions workflow ready to go
- ✅ **Task runner** - Justfile with common commands
- ✅ **Memory system** - `_pyrite/` folders for organizing project knowledge
- ✅ **AI agent template** - Optional CrewAI starter code

### What Problem It Solves

**Before Waft:**
```
You: "I want to start a new Python project"
You: *spends 30 minutes setting up*
- Creating pyproject.toml
- Setting up virtual environment
- Writing .gitignore
- Creating CI/CD workflow
- Setting up testing
- Writing README
- Organizing folder structure
```

**With Waft:**
```bash
waft new my_project
cd my_project
# Done! Everything is set up.
```

### How It Works

Waft orchestrates three layers:

1. **Environment (Substrate)** - Uses `uv` for package management
2. **Memory (_pyrite)** - File-based knowledge organization (active/, backlog/, standards/)
3. **Agents (CrewAI)** - Optional AI agent capabilities

Everything is **file-based** - no database, no server, just plain text files that work with git.

### What Makes It Unique

1. **Ambient** - Works quietly in the background, doesn't get in your way
2. **Self-modifying** - Projects can evolve their own structure
3. **Meta-framework** - Doesn't replace tools, orchestrates them
4. **File-based** - Everything is plain text, git-friendly, portable

---

## The 5-Minute Demo Script

### Step 1: Show the Problem
"Every time I start a new Python project, I have to:
- Set up pyproject.toml
- Configure dependencies
- Write CI/CD workflows
- Create folder structure
- Set up testing
- Write documentation templates

This takes 30+ minutes and I always forget something."

### Step 2: Show the Solution
```bash
# Install (one time)
uv tool install waft

# Create project (10 seconds)
waft new my_awesome_project

# That's it! Let me show you what it created...
cd my_awesome_project
waft info
```

### Step 3: Show What It Created
```bash
# Show the structure
tree -L 2

# Show it's a real Python project
cat pyproject.toml

# Show the memory system
ls -la _pyrite/

# Show CI/CD is ready
cat .github/workflows/ci.yml

# Show task runner
just --list
```

### Step 4: Show It Works
```bash
# Verify everything is set up correctly
waft verify

# Sync dependencies
waft sync

# Add a dependency
waft add pytest

# Start web dashboard
waft serve
# Opens http://localhost:8000
```

### Step 5: Explain the Philosophy
"Waft doesn't lock you in. It's all file-based:
- No database to manage
- Everything is plain text
- Works with git out of the box
- You can modify anything
- It's your project, Waft just set it up"

---

## For Different Audiences

### For Developers

**"Waft is a project scaffolding tool that sets up modern Python projects with best practices. It uses `uv` for dependencies, creates a `_pyrite/` memory system for organizing project knowledge, and includes CI/CD, task runners, and optional AI agent templates. Everything is file-based and git-friendly."**

**Key Points:**
- Uses `uv` (fast, modern Python package manager)
- File-based storage (no database)
- 7 CLI commands for project management
- Extensible architecture
- MIT licensed

### For Project Managers

**"Waft standardizes how we create Python projects. Instead of each developer setting up projects differently, everyone uses the same structure, same CI/CD, same best practices. This reduces onboarding time and ensures consistency across projects."**

**Key Points:**
- Standardizes project structure
- Reduces setup time from 30+ minutes to 10 seconds
- Ensures best practices are followed
- Makes projects easier to understand and maintain

### For Technical Leads

**"Waft is a meta-framework that orchestrates the Python development stack. It provides a consistent project structure, integrates with modern tools (`uv`, `just`, GitHub Actions), and includes a file-based memory system (`_pyrite/`) for organizing project knowledge. It's designed to be ambient - it sets things up and gets out of your way."**

**Key Points:**
- Architecture: Substrate (uv) → Memory (_pyrite) → Agents (CrewAI)
- File-based, no external dependencies
- Extensible with helper functions and utilities
- Well-documented with comprehensive guides
- Tested and validated

### For Non-Technical Stakeholders

**"Waft is a tool that helps developers start new projects faster. Instead of spending time setting up the project structure, it does it automatically. This means developers can start building features sooner, and all projects follow the same standards."**

**Key Points:**
- Saves time (30+ minutes → 10 seconds)
- Ensures consistency
- Reduces errors
- Free and open source

---

## Common Questions & Answers

### "Why not just use cookiecutter?"

**Answer:** "Cookiecutter is great for templates, but Waft goes further. It:
- Integrates with `uv` for dependency management
- Provides ongoing project management commands (`waft sync`, `waft add`, `waft verify`)
- Includes a memory system (`_pyrite/`) for organizing project knowledge
- Offers a web dashboard for project visualization
- Is designed as a meta-framework, not just a template generator"

### "Is this another framework I have to learn?"

**Answer:** "No! Waft is a meta-framework - it orchestrates tools you already know (`uv`, `just`, GitHub Actions). It sets things up and gets out of your way. You can use any Python framework (FastAPI, Django, Flask) inside a Waft project."

### "What if I don't like the structure it creates?"

**Answer:** "Everything is file-based and editable. Waft creates the structure, but you own it. You can modify anything, add folders, change templates. Waft just gives you a good starting point."

### "Do I need to use all the features?"

**Answer:** "No! The `_pyrite/` memory system is optional - use it if you want. CrewAI agents are optional. CI/CD is optional (though recommended). Waft sets things up, but you decide what to use."

### "How is this different from Poetry/pipenv/conda?"

**Answer:** "Those are package managers. Waft uses `uv` (which is faster) and adds project structure, CI/CD, memory organization, and project management commands. It's a layer above package management."

---

## Visual Explanation

### The Three Layers

```
┌─────────────────────────────────────┐
│         Agents (CrewAI)              │  ← Optional AI capabilities
│         ───────────────              │
├─────────────────────────────────────┤
│      Memory (_pyrite/)               │  ← Project knowledge organization
│      active/ backlog/ standards/     │
├─────────────────────────────────────┤
│      Substrate (uv)                  │  ← Package management
│      pyproject.toml uv.lock          │
└─────────────────────────────────────┘
```

### What Gets Created

```
my_project/
├── pyproject.toml          ← Python project config
├── uv.lock                  ← Locked dependencies
├── _pyrite/                 ← Memory system
│   ├── active/             ← Current work
│   ├── backlog/            ← Future work
│   └── standards/           ← Standards
├── .github/workflows/
│   └── ci.yml              ← CI/CD pipeline
├── Justfile                ← Task runner
├── .gitignore              ← Git ignore rules
├── README.md               ← Project documentation
└── src/
    └── agents.py           ← CrewAI template (optional)
```

---

## Quick Reference Card

**Install:**
```bash
uv tool install waft
```

**Create Project:**
```bash
waft new my_project
```

**Commands:**
- `waft new <name>` - Create new project
- `waft verify` - Verify structure
- `waft sync` - Sync dependencies
- `waft add <package>` - Add dependency
- `waft init` - Add to existing project
- `waft info` - Show project info
- `waft serve` - Web dashboard

**Key Features:**
- ✅ File-based (no database)
- ✅ Git-friendly
- ✅ Fast setup (10 seconds)
- ✅ Best practices included
- ✅ Extensible

---

## The One-Liner

**"Waft is a one-command project generator that sets up modern Python projects with best practices, dependency management, CI/CD, and a file-based memory system - all in 10 seconds."**

---

## Demo Checklist

When showing Waft to someone, demonstrate:

- [ ] Install: `uv tool install waft`
- [ ] Create project: `waft new demo_project`
- [ ] Show structure: `tree` or `ls -la`
- [ ] Show it's real: `cat pyproject.toml`
- [ ] Verify: `waft verify`
- [ ] Show commands: `waft --help`
- [ ] Show web dashboard: `waft serve`
- [ ] Explain philosophy: file-based, ambient, meta-framework

---

## Summary

**Waft is:**
- A project scaffolding tool
- A meta-framework that orchestrates tools
- File-based and git-friendly
- Fast (10-second setup)
- Extensible and customizable

**Waft is NOT:**
- A Python framework (use FastAPI, Django, etc. inside it)
- A package manager (uses `uv` for that)
- A database system (everything is files)
- Lock-in (you own your project)

**Best for:**
- Starting new Python projects quickly
- Standardizing project structure
- Teams wanting consistency
- Developers who value file-based workflows

