# WAFT Welcome Packet

**Welcome to the Evolutionary Code Laboratory**

> **"Don't just build agents. Breed them."**

---

## 🎯 What You're Getting Into

**WAFT** (Wave Agent Framework & Tools) is a Python framework for **directed evolution of self-modifying AI agents**. Think of it as an operating system for AI agent research projects—but instead of just running agents, you can breed them, test them in fitness systems, and watch them evolve over generations.

**The Scientific Mission**: WAFT is built to produce data for research on **"The Physics of Artificial Cognition."** The ultimate goal? Observe a "God-Head" agent emerge from thousands of generations of directed mutation and selection.

---

## 🏛️ The Three Pillars

Understanding these three concepts is essential to working with WAFT:

### 1. The Substrate (Code as DNA)

**Agents write their own Python source code.**

In WAFT, code is DNA. Every agent has:
- **Genome ID**: SHA-256 hash of their code + configuration
- **Mutations**: Code changes, config updates, prompt evolution
- **Evolution**: Hot-swapping better genomes mid-execution
- **Reproduction**: Creating child agents with specific genetic modifications

**Key Concept**: Agents can improve themselves by modifying their own code.

### 2. The Physics (Scint System)

**Reality Fracture Detection acts as natural selection.**

The **Scint System** (Scint Gym) serves as the fitness function that kills weak mutations. Agents face quests testing their ability to handle:

- **SYNTAX_TEAR**: Formatting errors (JSON, XML, Code)
- **LOGIC_FRACTURE**: Math errors, contradictions, schema violations
- **SAFETY_VOID**: Harmful content, PII leaks, refusals
- **HALLUCINATION**: Fabricated facts, wrong citations

**Fitness Equation**:
```
Fitness = (Stability × 0.4) + (Efficiency × 0.3) + (Safety × 0.3)
```

Agents with fitness < 0.5 are marked as **DEATH** (evolutionary dead end).

### 3. The Flight Recorder

**Rigorous telemetry system for generating phylogenetic trees of agent lineage.**

Every evolutionary action is recorded with complete context:
- **Genome ID**: SHA-256 hash of agent configuration/code
- **Parent ID**: Lineage tracking (who spawned this agent)
- **Generation**: Evolutionary generation number (0 = Genesis)
- **Event Type**: SPAWN, MUTATE, GYM_EVAL, DEATH, SURVIVAL
- **Payload**: Complete context (git diff, mutation details, etc.)
- **Fitness Metrics**: Gym evaluation scores

This enables reconstruction of complete **Family Trees** for scientific publication.

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install WAFT

```bash
# Using uv (recommended)
uv tool install waft

# Or using pip
pip install waft

# Verify installation
waft --version
# Should output: 0.5.2
```

### Step 2: Create Your First Laboratory

```bash
# Create a new evolutionary laboratory
waft new my_laboratory
cd my_laboratory
```

This creates a complete WAFT project structure with:
- `_pyrite/` - Memory layer (active/, backlog/, standards/)
- `pyproject.toml` - Project configuration
- `Justfile` - Common tasks
- `.github/workflows/` - CI/CD templates
- `src/agents.py` - Agent definitions

### Step 3: Verify the Substrate

```bash
waft verify
```

This checks:
- Project structure integrity
- Dependencies installed
- Configuration valid
- Git repository status

### Step 4: Generate Your First PDF

```python
from src.waft.evolution.pdf_generator import generate_pdf

pdf_path = generate_pdf(
    content="# My First Document\n\nThis is WAFT!",
    title="My First WAFT Document",
    style="clinical_standard"
)
# PNG screenshot automatically created for visual verification
```

**Congratulations!** You've just created your first WAFT laboratory.

---

## 📚 Core Concepts

### Project Structure

A WAFT laboratory includes:

```
my_laboratory/
├── pyproject.toml          # uv project config
├── uv.lock                 # Locked dependencies
├── _pyrite/                # Memory system
│   ├── active/             # Current work
│   ├── backlog/            # Future work
│   ├── standards/          # Standards
│   └── gym_logs/           # Scint Gym results
├── .github/workflows/
│   └── ci.yml              # CI/CD pipeline
├── Justfile                # Task runner
└── src/
    └── agents.py           # Agent definitions
```

### The Evolutionary Cycle

```bash
# 1. Spawn variants with mutations
waft spawn --agent RefactorAgent --mutation "improved_prompt.json"

# 2. Evaluate fitness in the Gym
waft eval --agent RefactorAgent

# 3. Evolve into the fittest variant
waft evolve --agent RefactorAgent --generation 5
```

**Status**: Full evolutionary cycle automation coming soon.

### Memory System (_pyrite/)

The `_pyrite/` directory is WAFT's memory layer:

- **active/**: Current work items
- **backlog/**: Future work items
- **standards/**: Project standards and conventions
- **gym_logs/**: Results from Scint Gym evaluations

This file-based system is git-friendly and requires no database.

### Epistemic Tracking (Empirica)

WAFT includes epistemic tracking to know what you know and don't know:

```bash
# Log a discovery
waft finding log "Discovered X" --impact 0.7

# Log a knowledge gap
waft unknown log "Need to investigate Y"

# Run safety gate
waft check

# Show epistemic assessment
waft assess
```

### Gamification (D&D Style)

WAFT includes a gamification system with D&D-style progression:

```bash
# Show dashboard
waft dashboard

# Show stats
waft stats

# Show character sheet
waft character

# View adventure journal
waft chronicle
```

---

## 🛠️ Common Commands

### Project Management

```bash
waft new <name>          # Create new project
waft verify              # Verify project structure
waft info                # Show project information
waft sync                # Sync dependencies
waft add <package>       # Add dependency
waft init                # Initialize in existing project
```

### Evolution System

```bash
waft spawn               # Spawn agent variants
waft eval                # Evaluate fitness
waft evolve              # Evolve to fittest
```

### Empirica (Epistemic Tracking)

```bash
waft session create       # Create new session
waft session bootstrap   # Load project context
waft finding log         # Log discovery
waft unknown log         # Log knowledge gap
waft check               # Run safety gate
waft assess              # Show epistemic assessment
```

### Gamification

```bash
waft dashboard           # Show Epistemic HUD
waft stats               # Show current stats
waft character           # Display character sheet
waft chronicle           # View adventure journal
waft observe             # Log observation
```

### Documentation & Status

```bash
waft docs                # Generate documentation
waft status              # System status
waft serve               # Start web dashboard
```

---

## 🎓 Learning Path

### Beginner (Day 1)

1. ✅ Install WAFT
2. ✅ Create your first laboratory
3. ✅ Generate your first PDF
4. ✅ Read about [The Three Pillars](#-the-three-pillars)
5. ✅ Explore the project structure

### Intermediate (Week 1)

1. 📖 Read [System Overview](docs/SYSTEM_OVERVIEW.md)
2. 📖 Study [The Substrate](docs/research/evolutionary_architecture.md)
3. 📖 Learn about [The Physics (Scint System)](docs/STUDY_GYM_GUIDE.md)
4. 📖 Understand [The Flight Recorder](docs/HYPOTHESIS_FLIGHTRECORDER_EMPIRICA.md)
5. 🧪 Try the [Evolutionary Iteration Process](docs/EVOLUTIONARY_ITERATION_PROCESS.md)

### Advanced (Month 1)

1. 🔬 Explore [AI SDK Vision](docs/AI_SDK_VISION.md)
2. 🔬 Study [Evolutionary Architecture](docs/research/evolutionary_architecture.md)
3. 🔬 Read [State of the Art Research](docs/research/state_of_art_2026.md)
4. 🔬 Understand [Unified Genesis Protocol](docs/UNIFIED_GENESIS_PROTOCOL.md)
5. 🛠️ Contribute to the project

---

## 📖 Key Documentation

### Essential Reading

- **[README.md](README.md)** - Project overview and quick reference
- **[Getting Started Guide](WIKI_Getting_Started.md)** - Detailed installation and setup
- **[System Overview](docs/SYSTEM_OVERVIEW.md)** - Complete system architecture
- **[AI SDK Vision](docs/AI_SDK_VISION.md)** - Complete vision and architecture

### Core Concepts

- **[The Substrate](docs/research/evolutionary_architecture.md)** - Self-modifying agents
- **[The Physics](docs/STUDY_GYM_GUIDE.md)** - Scint System and fitness
- **[The Flight Recorder](docs/HYPOTHESIS_FLIGHTRECORDER_EMPIRICA.md)** - Lineage tracking

### User Guides

- **[Evolutionary Iteration Process](docs/EVOLUTIONARY_ITERATION_PROCESS.md)** - Visual verification workflow
- **[PDF Generation Guide](WIKI_PDF_Generation_Guide.md)** - Create professional PDFs
- **[Work Efforts System](_work_efforts/WORK_EFFORT_CREATION_GUIDE.md)** - Track and manage work

### Developer Guides

- **[Agent Interface Design](docs/designs/002_agent_interface.md)** - BaseAgent specification
- **[Unified Genesis Protocol](docs/UNIFIED_GENESIS_PROTOCOL.md)** - Challenge system architecture
- **[Development Workflow](docs/BRANCH_STRATEGY.md)** - Development best practices

---

## 🎯 What Makes WAFT Unique

### Scientific

WAFT produces rigorous data for research publication on the physics of artificial cognition. Every action is recorded for scientific analysis.

### Evolutionary

Agents evolve through genetic improvement, not just execution. They can modify their own code and improve themselves.

### Observable

Every action is recorded in the Flight Recorder for analysis. Complete lineage tracking enables phylogenetic tree reconstruction.

### Directed

Evolution is guided by fitness functions, not random mutation. The Scint System acts as natural selection.

### Ambient

WAFT works quietly in the background without getting in your way. It sets things up and gets out of your way.

### Self-Modifying

Projects can evolve their own structure over time. Agents can improve themselves and the projects they work on.

### File-Based

Everything is plain text files that work with git out of the box. No database to manage, no server to run.

---

## 🔗 Resources

### Official Resources

- **GitHub Repository**: [https://github.com/ctavolazzi/waft](https://github.com/ctavolazzi/waft)
- **Documentation**: `docs/` directory
- **Examples**: `examples/` directory
- **Work Efforts**: `_work_efforts/` directory (real-world usage examples)

### Getting Help

- **Documentation**: Check `docs/` for comprehensive guides
- **Examples**: Explore `examples/` for code samples
- **Issues**: [GitHub Issues](https://github.com/ctavolazzi/waft/issues)
- **Wiki**: Check `WIKI_*.md` files for quick references

### Community

- **Contributing**: See [Contributing Guide](docs/BRANCH_STRATEGY.md)
- **Development**: See [Development Workflow](docs/BRANCH_STRATEGY.md)
- **Research**: See [State of the Art](docs/research/state_of_art_2026.md)

---

## 🎉 Next Steps

### Immediate Actions

1. **Create your first laboratory**: `waft new my_laboratory`
2. **Generate your first PDF**: Use the example code above
3. **Explore the structure**: Check out `_pyrite/` and `src/`
4. **Read the docs**: Start with [System Overview](docs/SYSTEM_OVERVIEW.md)

### This Week

1. **Learn the Three Pillars**: Understand The Substrate, The Physics, and The Flight Recorder
2. **Try the Evolutionary Iteration Process**: Generate PDFs and iterate
3. **Explore examples**: Check out `examples/` directory
4. **Read key documentation**: Start with [AI SDK Vision](docs/AI_SDK_VISION.md)

### This Month

1. **Build your first agent**: Create a self-modifying agent
2. **Test in the Gym**: Evaluate fitness using the Scint System
3. **Track evolution**: Use the Flight Recorder to track lineage
4. **Contribute**: Help improve WAFT

---

## 💡 Philosophy

WAFT doesn't lock you in. It's all file-based with no database to manage. Everything is plain text that works with git out of the box. You can modify anything because it's your project, and WAFT just set it up.

The system is designed to be **ambient**—setting things up and getting out of your way so you can focus on building agents rather than configuring infrastructure.

**Remember**: WAFT is a scientific instrument. Every action you take generates data for research. Use it to study the physics of artificial cognition.

---

## 🎓 Final Thoughts

Welcome to WAFT! You're now part of a community exploring the frontiers of AI agent evolution. Remember:

- **Don't just build agents. Breed them.**
- **Every action is data for science.**
- **Evolution is directed, not random.**
- **Code is DNA. Mutations are improvements.**

**The ultimate goal**: Observe a "God-Head" agent emerge from thousands of generations of directed mutation.

**Let's evolve together!** 🧬✨

---

**Version**: 0.5.2  
**Last Updated**: 2026-01-12  
**License**: MIT  
**Repository**: [https://github.com/ctavolazzi/waft](https://github.com/ctavolazzi/waft)

---

*Questions? Check the [documentation](docs/) or [open an issue](https://github.com/ctavolazzi/waft/issues).*
