# Getting Started with WAFT

> **Get up and running with the Wave Agent Framework & Tools in under 15 minutes**

Welcome! This guide will take you from zero to creating your first evolutionary AI agent laboratory.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Creating Your First Laboratory](#creating-your-first-laboratory)
4. [Understanding the Structure](#understanding-the-structure)
5. [Basic Commands](#basic-commands)
6. [Your First Agent](#your-first-agent)
7. [Next Steps](#next-steps)
8. [Getting Help](#getting-help)

---

## Prerequisites

Before installing WAFT, ensure you have:

### Required
- **Python 3.10 or higher**
  ```bash
  python --version  # Should show 3.10 or higher
  ```

- **uv package manager** - Fast Python package installer and manager
  ```bash
  # Install uv (macOS/Linux)
  curl -LsSf https://astral.sh/uv/install.sh | sh

  # Or using pip
  pip install uv

  # Verify installation
  uv --version
  ```

### Optional but Recommended
- **Git** - For version control (required for evolutionary tracking)
  ```bash
  git --version
  ```

- **just** - Task runner for convenience
  ```bash
  # macOS
  brew install just

  # Linux
  cargo install just
  ```

### System Requirements
- **OS**: macOS, Linux, or Windows (WSL recommended)
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 500MB for WAFT + dependencies

---

## Installation

### Method 1: Install via uv (Recommended)

This is the fastest and cleanest way to install WAFT:

```bash
# Install WAFT as a tool
uv tool install waft

# Verify installation
waft --version
```

**Expected output:**
```
waft version 0.9.0
```

### Method 2: Install from Source (Development)

Use this if you want to contribute to WAFT or modify it:

```bash
# Clone the repository
git clone https://github.com/ctavolazzi/waft.git
cd waft

# Sync dependencies
uv sync

# Install in editable mode
uv tool install --editable .

# Verify installation
waft --version
```

### Method 3: Install via pip (Traditional)

```bash
pip install waft
waft --version
```

### Troubleshooting Installation

**Problem: `command not found: waft`**
- Ensure uv's tool bin directory is in your PATH
- Check with: `uv tool list`
- Add to PATH: `export PATH="$HOME/.local/bin:$PATH"`

**Problem: Python version too old**
- Install Python 3.10+: `uv python install 3.10`
- Set as default: `uv python pin 3.10`

**Problem: Permission denied**
- Don't use sudo with uv
- Check file permissions: `ls -la ~/.local/share/uv`

---

## Creating Your First Laboratory

Now that WAFT is installed, let's create your first evolutionary laboratory!

### Step 1: Create a New Project

```bash
# Create a laboratory named 'my_lab'
waft new my_lab

# Or specify a custom path
waft new my_lab --path ~/Projects/waft_experiments
```

**What happens:**
- Creates a new directory with uv project structure
- Initializes Python environment
- Sets up _pyrite memory system
- Creates initial configuration files
- Initializes git repository (if git is available)

**Expected output:**
```
✨ Creating new WAFT laboratory: my_lab
📁 Initializing project structure...
🔧 Setting up uv environment...
🧠 Initializing _pyrite memory system...
📊 Setting up Empirica for epistemic tracking...
🎲 Initializing TavernKeeper gamification...
✅ Laboratory created successfully!

Next steps:
  cd my_lab
  waft verify
  waft info
```

### Step 2: Enter Your Laboratory

```bash
cd my_lab
```

### Step 3: Verify Everything Works

```bash
waft verify
```

**Expected output:**
```
🔍 Verifying WAFT laboratory structure...

✅ Project Structure: Valid
✅ pyproject.toml: Found
✅ uv.lock: Present
✅ _pyrite/ memory: Initialized
✅ Python environment: Ready (3.10.12)

🎉 Laboratory is ready for evolution!
```

---

## Understanding the Structure

Your new laboratory has a specific structure designed for evolutionary AI development:

```
my_lab/
├── pyproject.toml              # Project configuration and dependencies
├── uv.lock                     # Dependency lock file
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
├── .python-version             # Python version specification
│
├── _pyrite/                    # Memory and work management system
│   ├── active/                 # Current work items
│   ├── backlog/               # Future work items
│   ├── standards/             # Project standards and guidelines
│   └── gym_logs/              # Fitness evaluation results
│
├── .github/                    # GitHub configuration (optional)
│   └── workflows/
│       └── ci.yml             # Continuous integration
│
├── src/                        # Source code directory
│   └── my_lab/
│       ├── __init__.py
│       └── agents.py          # Your agent definitions
│
├── tests/                      # Test directory
│   └── __init__.py
│
└── Justfile                    # Task runner configuration (optional)
```

### Key Directories Explained

#### `_pyrite/` - The Memory System
The **_pyrite** directory is WAFT's structured memory system:

- **`active/`** - Work you're currently doing
  - Contains tickets (PY-XXX) with tasks and bounties
  - Tracked evolution experiments

- **`backlog/`** - Future work items
  - Ideas for agents to build
  - Features to implement
  - Experiments to run

- **`standards/`** - Project standards
  - Coding conventions
  - Agent design patterns
  - Evolution strategies

- **`gym_logs/`** - Fitness evaluation results
  - Scint detection reports
  - Fitness scores
  - Evolution metrics

#### `src/my_lab/` - Your Code
All your agent code lives here:

- **`agents.py`** - Define your agents
- Additional modules as needed
- Keep it organized and modular

---

## Basic Commands

Here are the essential commands you'll use daily:

### Project Management

```bash
# Get project info
waft info

# Verify project structure
waft verify

# Add a dependency
waft add requests
waft add "pandas>=2.0.0"

# Sync dependencies
waft sync
```

### Agent Development

```bash
# Create a new agent (coming soon)
waft agent create RefactorAgent

# List agents
waft agent list

# Run an agent
waft agent run RefactorAgent
```

### Evolution

```bash
# Spawn agent variants
waft spawn --agent RefactorAgent --mutation prompt_v2.json

# Evaluate fitness
waft eval --agent RefactorAgent

# Run full evolutionary cycle (coming soon)
waft evolve --agent RefactorAgent --generations 10
```

### Empirica (Knowledge Tracking)

```bash
# Start a session
waft session create --ai-id Claude

# Log a discovery
waft finding log "Discovered that X causes Y" --impact 0.8

# Log an unknown
waft unknown log "Need to investigate why Z happens"

# Check safety gate
waft check

# View assessment
waft assess
```

### Gamification

```bash
# View your dashboard
waft dashboard

# See character sheet
waft character

# View adventure journal
waft chronicle

# Log an observation
waft observe "This refactor is clean!" --mood delighted
```

### Web Dashboard

```bash
# Start web interface
waft serve

# Custom port and dev mode
waft serve --port 8080 --dev
```

---

## Your First Agent

Let's create a simple agent to understand the basics.

### Step 1: Open `src/my_lab/agents.py`

```bash
# Use your preferred editor
code src/my_lab/agents.py
# or
vim src/my_lab/agents.py
```

### Step 2: Define Your Agent

```python
"""
My first WAFT agent - A simple greeting agent
"""

from typing import Dict, Any


class GreetingAgent:
    """
    A simple agent that generates personalized greetings.

    This demonstrates:
    - Basic agent structure
    - Configuration handling
    - Simple behavior
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the agent with optional configuration."""
        self.config = config or {}
        self.greeting_style = self.config.get("style", "formal")
        self.language = self.config.get("language", "english")

    def generate_greeting(self, name: str) -> str:
        """Generate a greeting for the given name."""
        greetings = {
            "formal": {
                "english": f"Good day, {name}. How may I assist you?",
                "spanish": f"Buenos días, {name}. ¿En qué puedo ayudarle?",
            },
            "casual": {
                "english": f"Hey {name}! What's up?",
                "spanish": f"¡Hola {name}! ¿Qué tal?",
            },
            "friendly": {
                "english": f"Hi {name}, great to see you!",
                "spanish": f"¡Hola {name}, qué gusto verte!",
            }
        }

        return greetings.get(self.greeting_style, {}).get(
            self.language,
            f"Hello, {name}!"
        )

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main execution method."""
        name = input_data.get("name", "friend")
        greeting = self.generate_greeting(name)

        return {
            "greeting": greeting,
            "style": self.greeting_style,
            "language": self.language,
            "success": True
        }


# Agent factory function
def create_agent(agent_type: str, config: Dict[str, Any] = None):
    """Create an agent of the specified type."""
    agents = {
        "greeting": GreetingAgent,
    }

    agent_class = agents.get(agent_type)
    if not agent_class:
        raise ValueError(f"Unknown agent type: {agent_type}")

    return agent_class(config)


# Example usage
if __name__ == "__main__":
    # Create a formal greeting agent
    agent = create_agent("greeting", {"style": "formal"})
    result = agent.run({"name": "Alice"})
    print(result["greeting"])

    # Create a casual greeting agent
    casual_agent = create_agent("greeting", {"style": "casual"})
    result = casual_agent.run({"name": "Bob"})
    print(result["greeting"])
```

### Step 3: Test Your Agent

```bash
# Run the agent
uv run python src/my_lab/agents.py
```

**Expected output:**
```
Good day, Alice. How may I assist you?
Hey Bob! What's up?
```

### Step 4: Log Your Progress

```bash
# Log this as a finding
waft finding log "Created first GreetingAgent with multi-language support" --impact 0.6

# Log what you learned
waft observe "Agent structure is straightforward and modular" --mood satisfied
```

---

## Next Steps

Congratulations! You've created your first WAFT laboratory and agent. Here's what to explore next:

### Beginner Path

1. **[Core Concepts](guides/CORE_CONCEPTS.md)** - Understand WAFT fundamentals
   - Genome IDs and evolution
   - Scint system and fitness
   - Flight recorder and lineage

2. **[CLI Commands Guide](guides/CLI_COMMANDS.md)** - Master the command line
   - All available commands
   - Options and flags
   - Advanced usage

3. **[Evolution Basics Tutorial](tutorials/EVOLUTION_BASICS.md)** - Run your first evolution
   - Spawn variants
   - Evaluate fitness
   - Select winners

### Intermediate Path

4. **[PDF Generation Tutorial](tutorials/PDF_GENERATION.md)** - Create documents
   - Use templates
   - Customize styles
   - Generate reports

5. **[D&D Campaign Setup](tutorials/DND_CAMPAIGN_SETUP.md)** - Self-playing campaigns
   - Configure parties
   - Run combat
   - Generate narratives

6. **[Desktop App Development](tutorials/DESKTOP_APP_DEV.md)** - Build Electron apps
   - Set up Electron
   - FastAPI backend
   - Integration

### Advanced Path

7. **[Architecture Overview](ARCHITECTURE.md)** - Deep dive into system design
8. **[API Reference](api/API_INDEX.md)** - Complete API documentation
9. **[Contributing Guide](../CONTRIBUTING.md)** - Contribute to WAFT

---

## Getting Help

### Documentation

- **[Documentation Index](DOCUMENTATION_INDEX.md)** - All documentation
- **[FAQ](FAQ.md)** - Frequently asked questions
- **[Troubleshooting](TROUBLESHOOTING.md)** - Common issues

### Community

- **GitHub Issues** - Bug reports and feature requests
  - https://github.com/ctavolazzi/waft/issues

- **GitHub Discussions** - Questions and community help
  - https://github.com/ctavolazzi/waft/discussions

### Commands for Help

```bash
# Get help on any command
waft --help
waft new --help
waft evolve --help

# Get project info
waft info

# Check system status
waft verify
```

---

## Common First Questions

### Q: What's the difference between WAFT and other AI frameworks?

WAFT focuses on **evolutionary development** - agents improve through genetic mutation and selection, not just execution. Think of it as breeding agents rather than building them.

### Q: Do I need to know D&D to use WAFT?

No! The D&D elements are optional gamification. You can use WAFT purely for AI agent development without engaging with the RPG mechanics.

### Q: Can I use WAFT with existing projects?

Yes! Use `waft init` in an existing project to add WAFT structure:

```bash
cd existing_project
waft init
```

### Q: How do I share my agents?

Agents are just Python code. Share them via:
- Git repositories
- PyPI packages
- Direct file sharing
- WAFT agent registry (coming soon)

### Q: Is WAFT production-ready?

WAFT v0.9.0 is in **beta**. Core features are stable, but the API may change before v1.0.0. Use for experiments and research; test thoroughly before production use.

---

## Quick Reference Card

```bash
# Installation
uv tool install waft

# Create laboratory
waft new my_lab
cd my_lab

# Verify setup
waft verify

# Add dependencies
waft add package_name

# Create agent
# Edit src/my_lab/agents.py

# Track knowledge
waft finding log "Your discovery"
waft unknown log "What you don't know"

# View dashboard
waft dashboard

# Get help
waft --help
```

---

## What You've Learned

After completing this guide, you now know:

✅ How to install WAFT and its dependencies
✅ How to create a new evolutionary laboratory
✅ The structure and purpose of key directories
✅ Essential WAFT commands for daily use
✅ How to create a basic agent
✅ How to track your progress with Empirica
✅ Where to go for help and next steps

---

## Celebrate Your Progress! 🎉

You've taken the first step into evolutionary AI development. You now have:

- A working WAFT laboratory
- Your first agent
- Understanding of the basic workflow
- Tools to track your learning

**Next milestone**: Complete the [Evolution Basics Tutorial](tutorials/EVOLUTION_BASICS.md) to run your first evolutionary cycle!

---

**Need help?** Check [Troubleshooting](TROUBLESHOOTING.md) or open an issue on GitHub.

**Ready to learn more?** See the [Documentation Index](DOCUMENTATION_INDEX.md) for all guides.

---

*Last Updated: 2026-01-16 | Version: 0.9.0 | [Report Issues](https://github.com/ctavolazzi/waft/issues)*
