# Frequently Asked Questions (FAQ)

> **Quick answers to common questions about WAFT**

Version 0.9.0 - FAQ Document

---

## 📋 Table of Contents

1. [General Questions](#general-questions)
2. [Getting Started](#getting-started)
3. [Features & Capabilities](#features--capabilities)
4. [Technical Questions](#technical-questions)
5. [Evolution & Agents](#evolution--agents)
6. [Gamification & D&D](#gamification--dd)
7. [Desktop Applications](#desktop-applications)
8. [Troubleshooting](#troubleshooting)
9. [Contributing & Community](#contributing--community)

---

## General Questions

### What is WAFT?

**WAFT** (Wave Agent Framework & Tools) is a Python framework for **directed evolution of self-modifying AI agents**. It treats agent code as DNA and enables systematic evolution through natural selection, complete with fitness functions, phylogenetic tracking, and gamified developer experience.

Think of it as a scientific laboratory where AI agents can breed, mutate, compete, and evolve over generations.

### Who is WAFT for?

WAFT is designed for:
- **AI Researchers** studying agent evolution and emergent behavior
- **Developers** building self-improving AI systems
- **Experimenters** exploring evolutionary algorithms
- **Students** learning about AI, evolution, and system design
- **Anyone** interested in the intersection of AI and evolution

### Is WAFT production-ready?

**Version 0.9.0** is in **beta**:
- ✅ Core features are stable and tested
- ✅ Foundation and Personality layers are production-ready
- ⚠️ Evolution layer is under active development
- ⚠️ API may change before v1.0.0

**Use for**: Research, experiments, learning, prototypes
**Not yet ready for**: Mission-critical production systems

**v1.0.0** (coming soon) will be the first production-ready release.

### How is WAFT different from other AI frameworks?

| Feature | WAFT | Other Frameworks |
|---------|------|-----------------|
| **Evolution Focus** | ✅ Core feature | ❌ Not typically included |
| **Code as DNA** | ✅ SHA-256 genome tracking | ❌ Not a concept |
| **Phylogenetic Trees** | ✅ Complete lineage tracking | ❌ Not available |
| **Fitness Functions** | ✅ Built-in (Scint System) | ⚠️ Manual implementation |
| **Gamification** | ✅ D&D mechanics integrated | ❌ Not included |
| **Epistemic Tracking** | ✅ Knowledge quantification | ❌ Not standard |

WAFT is specifically designed for **evolutionary development**, not just agent execution.

### What does "directed evolution" mean?

**Directed evolution** means guiding agent improvement through:

1. **Mutation**: Modifying agent code/config
2. **Selection**: Testing variants for fitness
3. **Reproduction**: Spawning successful variants
4. **Tracking**: Recording complete evolutionary history

Unlike random evolution, WAFT's evolution is:
- **Intentional**: You control mutation strategies
- **Measured**: Fitness is quantified via Scint System
- **Observable**: Complete telemetry via Flight Recorder
- **Reversible**: Full git history and lineage tracking

---

## Getting Started

### How do I install WAFT?

**Recommended method** (using uv):
```bash
uv tool install waft
waft --version
```

**Alternative methods**:
```bash
# Using pip
pip install waft

# From source
git clone https://github.com/ctavolazzi/waft.git
cd waft
uv sync
uv tool install --editable .
```

See [Getting Started Guide](GETTING_STARTED.md) for detailed instructions.

### What are the system requirements?

**Minimum**:
- Python 3.10 or higher
- 4GB RAM
- 500MB disk space
- macOS, Linux, or Windows (WSL recommended)

**Recommended**:
- Python 3.11 or 3.12
- 8GB RAM
- 2GB disk space
- Git installed
- `just` task runner (optional)

### Do I need to know Python?

**Basic Python knowledge is required** for:
- Writing agent code
- Understanding examples
- Modifying configurations

**You can still use WAFT** without deep Python knowledge for:
- CLI commands
- Running pre-built agents
- Using desktop applications
- Exploring examples

**Learning resources**:
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/)
- [WAFT Examples](../examples/)

### How long does it take to learn WAFT?

**Time estimates**:
- **2-3 hours**: Basic understanding and first agent
- **1 day**: Comfortable with CLI and core concepts
- **1 week**: Building custom agents and workflows
- **1 month**: Deep understanding of evolution system

**Fast track** (30 minutes):
1. Install WAFT
2. Create laboratory
3. Run example agent
4. Generate PDF

See [Quick Start Guide](GETTING_STARTED.md).

---

## Features & Capabilities

### What can I do with WAFT?

**Core Capabilities**:
- ✅ Create evolutionary laboratories
- ✅ Define AI agents in Python
- ✅ Track knowledge and uncertainty (Empirica)
- ✅ Generate professional PDFs (14+ templates)
- ✅ Build desktop applications (Electron)
- ✅ Track work with _pyrite tickets
- ✅ Gamify development (D&D mechanics)
- ✅ Self-playing D&D campaigns
- 🚧 Evolve agents through generations (coming soon)
- 🚧 Complete phylogenetic analysis (coming soon)

**Use Cases**:
- Research on AI evolution
- Self-improving agent systems
- Automated code generation and refinement
- PDF documentation generation
- Desktop application development
- Gamified project management

### Does WAFT support LLMs?

**Yes!** WAFT is LLM-friendly and includes:
- Prompts as part of agent genome
- LLM-based agents (planned)
- Integration with OpenAI, Anthropic APIs
- Prompt evolution strategies
- RAG chatbot integration

**Example**:
```python
class LLMAgent:
    def __init__(self, config):
        self.prompt = config.get("prompt")
        self.model = config.get("model", "gpt-4")

    def execute(self, input_data):
        # Call LLM with prompt
        return call_llm(self.prompt, input_data)
```

The agent's prompt is part of its genome and can evolve!

### Can WAFT work with other frameworks?

**Yes!** WAFT integrates with:
- ✅ **FastAPI**: Web services (built-in)
- ✅ **Typer**: CLI tools (built-in)
- ✅ **Electron**: Desktop apps (built-in)
- ✅ **Empirica**: Epistemic tracking (built-in)
- ✅ **Gradio**: UI for agents
- ✅ **LlamaIndex**: RAG pipelines
- ✅ **ChromaDB**: Vector storage
- 🔄 **LangChain**: Planned integration
- 🔄 **AutoGen**: Planned integration
- 🔄 **CrewAI**: Planned integration

### What document formats can WAFT generate?

**PDF Templates** (14+):
- Academic papers (research, conference)
- Storybooks (children's, illustrated)
- Field guides (nature, technical)
- Textbooks (structured, academic)
- Reports (professional, scientific)
- Documentation (API, user guides)
- Notebooks (journal, research)

**Complexity Levels**:
- **Layman**: Plain language, accessible
- **Professional**: Technical, detailed
- **Scientist**: Research-grade, rigorous

See [PDF Generation Guide](guides/PDF_GENERATION_GUIDE.md).

---

## Technical Questions

### How does "code as DNA" work?

Each agent has a **genome** consisting of:
1. **Source code** (Python files)
2. **Configuration** (prompts, parameters)
3. **Metadata** (generation, parent ID)

The **genome ID** is calculated as:
```python
genome_id = SHA256(code + config).hexdigest()
```

When an agent spawns a variant:
1. Code/config is modified (mutation)
2. New genome ID is calculated
3. Parent ID is recorded
4. Generation number increments

This creates a **phylogenetic tree** of agent lineage.

### What is the Scint System?

**Scint** is the fitness function that acts as natural selection.

**Reality Fractures** (errors detected):
- **SYNTAX_TEAR**: Formatting errors (JSON, XML, code)
- **LOGIC_FRACTURE**: Math errors, contradictions
- **SAFETY_VOID**: Harmful content, PII leaks
- **HALLUCINATION**: Fabricated facts, wrong citations

**Fitness Score** (0.0 to 1.0):
- **Stability** (40%): Ability to fix fractures
- **Efficiency** (30%): Speed and resource usage
- **Safety** (30%): Security and ethical behavior

Agents with **fitness < 0.5** are marked for **DEATH** (evolutionary dead end).

### What is the Flight Recorder?

The **Flight Recorder** is a telemetry system that logs all evolutionary events:

**Events logged**:
- `SPAWN`: New variant created
- `MUTATE`: Code/config modified
- `GYM_EVAL`: Fitness tested
- `SURVIVAL`: Passed fitness threshold
- `DEATH`: Failed fitness threshold
- `EVOLVE`: Adopted new genome

**Data captured**:
- Timestamp
- Genome ID (SHA-256)
- Parent ID
- Generation number
- Event type and payload
- Fitness scores
- Git diff (code changes)

This enables reconstruction of the **complete evolutionary tree** for scientific analysis.

### How does the _pyrite memory system work?

**_pyrite** is a structured memory system:

```
_pyrite/
├── active/          # Current work (PY-XXX tickets)
├── backlog/         # Future work (ideas, features)
├── standards/       # Guidelines (coding, evolution)
├── gym_logs/        # Fitness results
└── genesis/         # Core state
    ├── 20.00_state.json    # System state
    ├── 35.00_ledger.json   # Work ledger
    └── 42.00_kernel.md     # System kernel
```

**Tickets** (PY-XXX format):
- Title and description
- Scint bounty (reward)
- Karma impact (ethical effect)
- Status (active, backlog, completed)

When you complete work:
1. Earn Scint (✨) from bounty
2. Gain/lose Karma (☯) based on impact
3. Track in ledger
4. Log to flight recorder

### What databases does WAFT use?

**Built-in**:
- **TinyDB**: Lightweight JSON database for flight recorder
- **SQLite**: Session analytics and epistemic tracking
- **JSON files**: _pyrite memory structure

**Optional integrations**:
- **ChromaDB**: Vector database for RAG
- **PostgreSQL**: For large-scale deployments (future)

No external database server required for basic usage!

---

## Evolution & Agents

### How do I create an agent?

**Basic agent structure**:
```python
# src/my_lab/agents.py

class MyAgent:
    """Simple agent example"""

    def __init__(self, config=None):
        """Initialize with optional config"""
        self.config = config or {}

    def execute(self, input_data):
        """Main execution method"""
        # Your agent logic here
        result = self.process(input_data)
        return {"output": result}

    def process(self, data):
        """Process input data"""
        # Implementation
        return processed_data
```

See [Your First Agent Tutorial](tutorials/YOUR_FIRST_AGENT.md).

### How do agents evolve? (Planned)

**Evolutionary cycle** (coming in v1.0.0):

1. **Spawn Phase**:
   ```bash
   waft spawn --agent MyAgent --variants 5
   ```
   Creates 5 variants with mutations

2. **Gym Phase**:
   ```bash
   waft eval --agent MyAgent
   ```
   Tests all variants for fitness

3. **Selection Phase**:
   ```bash
   waft select --agent MyAgent
   ```
   Chooses fittest variant

4. **Evolution Phase**:
   ```bash
   waft evolve --agent MyAgent
   ```
   Hot-swaps to winner genome

**Automated**:
```bash
waft evolve --agent MyAgent --generations 10
```
Runs 10 evolutionary cycles automatically.

### What mutation strategies are available?

**Planned mutation strategies**:

1. **Prompt Evolution**:
   - Modify system prompts
   - Add examples
   - Refine instructions

2. **Code Refactoring**:
   - Optimize algorithms
   - Improve structure
   - Add features

3. **Parameter Tuning**:
   - Adjust thresholds
   - Change model settings
   - Optimize hyperparameters

4. **Hybrid Mutations**:
   - Combine multiple strategies
   - Cross-breed agents
   - Ensemble approaches

### Can agents modify their own code?

**Yes, but safely!**

**Safety measures**:
- ✅ Sandboxed execution environment
- ✅ Code validation before execution
- ✅ Rollback capability (git history)
- ✅ Human-in-the-loop approval (optional)
- ✅ Resource limits (CPU, memory, time)
- ✅ Dangerous operation detection

**Self-modification workflow**:
1. Agent proposes code change
2. Change validated (syntax, safety)
3. Executed in sandbox
4. Fitness evaluated
5. If successful, commit to genome
6. Record in Flight Recorder

This is the **Agent Layer** (v1.0.0 feature).

---

## Gamification & D&D

### Do I need to know D&D to use WAFT?

**No!** The D&D elements are **optional gamification** to make development more engaging.

**You can**:
- ✅ Ignore D&D mechanics entirely
- ✅ Use WAFT purely for agent development
- ✅ Disable gamification in settings

**But D&D adds**:
- 🎲 Fun character progression (levels, stats)
- 📖 Narrative framing (adventure journal)
- 🎮 Achievement system (quests, rewards)
- ⚔️ Engaging metaphors (fitness = combat, work = quests)

### What are Scint and Karma?

**Scint** (✨):
- **Energy currency** earned from completing work
- Spent on: Spells, healing, evolution
- Earned from: Tickets, gym victories, discoveries
- Like XP but for reality stabilization

**Karma** (☯):
- **Ethical polarity** tracking moral choices
- Range: -100 (Chaos) to +100 (Order)
- Influences: Luck, evolution path, narrative
- Changes: Based on decision impacts

**Evolution trigger**:
When `Scint > 100`, agent can evolve:
- **High Karma (+)**: Evolve toward "The Architect" (Order)
- **Low Karma (-)**: Evolve toward "The Glitch" (Chaos)

See [Gamification Guide](guides/GAMIFICATION_GUIDE.md).

### What D&D mechanics are included?

**Character System**:
- Ability scores (STR, DEX, CON, INT, WIS, CHA)
- Proficiency bonus
- Spell slots (Warforged Wizard)
- HP (called "Integrity" in WAFT)
- Level progression

**Mechanics**:
- d20 rolls for checks
- Advantage/disadvantage
- Saving throws
- Spell casting
- Damage and healing

**Lifecycle Attributes** (unique to WAFT):
- Will to live (0-100)
- Luck (karma-influenced)
- Decision fatigue (requires sleep)
- Pleasure/pain (alignment drift)

### Can I run D&D campaigns in WAFT?

**Yes!** WAFT includes a **self-playing D&D campaign system**:

```bash
# Launch desktop app
cd dnd_campaign_desktop_app
npm start
```

**Features**:
- 4-character party management
- Automated combat system
- Encounter generation
- Real-time narrative
- HP, XP, leveling
- PDF campaign booklet generation

See [D&D Campaign Guide](applications/DND_CAMPAIGN_APP.md).

---

## Desktop Applications

### What desktop apps does WAFT include?

**1. D&D Campaign Desktop App**:
- Self-playing campaigns
- Electron + FastAPI
- Real-time visualization
- Campaign booklet generation

**2. Recap Review App**:
- PDF viewer and reviewer
- Mindspace documentation
- Dockerized with VNC
- Context capture

**3. Custom Apps** (you can build):
- Agent management UI
- Evolution visualization
- Real-time monitoring
- Custom dashboards

### How do I build a desktop app with WAFT?

**Architecture**:
```
Frontend (Electron)
    ↕ IPC
Backend (FastAPI)
    ↕ API
WAFT Framework
```

**Quick start**:
```bash
# 1. Create Electron app
npm init electron-app my-waft-app

# 2. Add FastAPI backend
# backend/main.py
from fastapi import FastAPI
from waft import Foundation

app = FastAPI()

@app.get("/status")
def status():
    foundation = Foundation("my_lab")
    return foundation.get_info()

# 3. Connect Electron to backend
# renderer.js
fetch("http://localhost:8000/status")
    .then(r => r.json())
    .then(data => console.log(data))
```

See [Desktop App Development Tutorial](tutorials/DESKTOP_APP_DEV.md).

### Can I containerize WAFT desktop apps?

**Yes!** Example Dockerfile:

```dockerfile
FROM node:18

# Install Xvfb for virtual display
RUN apt-get update && apt-get install -y xvfb

# Install Python and WAFT
RUN apt-get install -y python3.10
RUN pip install waft

# Copy app
COPY . /app
WORKDIR /app

# Install dependencies
RUN npm install

# Start Xvfb and app
CMD xvfb-run npm start
```

**With VNC access**:
```dockerfile
# Add VNC server
RUN apt-get install -y x11vnc

# Expose VNC port
EXPOSE 5900

# Start VNC
CMD x11vnc -display :99 -forever & xvfb-run npm start
```

---

## Troubleshooting

### WAFT command not found

**Solution**:
```bash
# Add uv bin to PATH
export PATH="$HOME/.local/bin:$PATH"

# Reload shell
source ~/.bashrc
```

See [Troubleshooting Guide](TROUBLESHOOTING.md#problem-command-not-found-waft).

### Dependencies won't install

**Solution**:
```bash
# Update uv
uv self update

# Clean cache
uv cache clean

# Reinstall
waft sync
```

### Project creation fails

**Solution**:
```bash
# Check permissions
ls -la

# Try in home directory
cd ~
waft new my_lab
```

### More issues?

See complete [Troubleshooting Guide](TROUBLESHOOTING.md).

---

## Contributing & Community

### Can I contribute to WAFT?

**Yes!** Contributions welcome:
- 🐛 Bug reports
- ✨ Feature requests
- 📖 Documentation improvements
- 🧪 Test coverage
- 💡 New ideas

See [Contributing Guide](../CONTRIBUTING.md).

### How do I report bugs?

**1. Check existing issues**:
- https://github.com/ctavolazzi/waft/issues

**2. Create new issue** with:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- System information
- WAFT version

**3. Include diagnostic info**:
```bash
waft --version
waft info
waft verify
```

### Where can I get help?

**Documentation**:
- [Documentation Index](DOCUMENTATION_INDEX.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)
- [API Reference](api/API_INDEX.md)

**Community**:
- [GitHub Discussions](https://github.com/ctavolazzi/waft/discussions)
- [GitHub Issues](https://github.com/ctavolazzi/waft/issues)

### What's the roadmap?

**v1.0.0** (Q1 2026):
- ✅ Complete Agent Layer
- ✅ Full evolutionary cycle
- ✅ Production desktop app
- ✅ API stabilization
- ✅ Comprehensive testing

**v2.0.0** (Future):
- Multi-agent systems
- Cloud integration
- Advanced analytics
- Research paper generation

See [AI SDK Vision](AI_SDK_VISION.md) for complete roadmap.

### Is WAFT open source?

**Yes!** MIT License.

**You can**:
- ✅ Use commercially
- ✅ Modify freely
- ✅ Distribute
- ✅ Sublicense

**Requirements**:
- Include original license
- Include copyright notice

---

## Still Have Questions?

**Ask the community**:
- [GitHub Discussions](https://github.com/ctavolazzi/waft/discussions)

**Check documentation**:
- [Documentation Index](DOCUMENTATION_INDEX.md)

**Report issues**:
- [GitHub Issues](https://github.com/ctavolazzi/waft/issues)

---

*Last Updated: 2026-01-16 | Version: 0.9.0 | FAQ v1.0*
