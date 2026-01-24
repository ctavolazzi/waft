# Getting Started with WAFT

**Get up and running with WAFT in 15 minutes**

---

## Prerequisites

- Python 3.9+ installed
- Git for version control
- Basic understanding of Python
- (Optional) familiarity with evolutionary algorithms

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ctavolazzi/waft.git
cd waft
```

### 2. Install Dependencies

```bash
# Using pip
pip install -e .

# Or using poetry (if available)
poetry install
```

### 3. Verify Installation

```bash
waft --version
waft verify
```

Expected output:
```
✅ WAFT Framework v0.1.0
✅ All core systems operational
```

---

## Your First Agent

### 1. Create a New Laboratory

```bash
waft new my-first-lab
cd my-first-lab
```

This creates:
```
my-first-lab/
├── agents/           # Your agent code
├── _pyrite/          # Memory structure
│   ├── active/      # Current work
│   ├── backlog/     # Future work
│   └── standards/   # Best practices
├── gym_logs/        # Scint Gym results
└── config.yaml      # Lab configuration
```

### 2. Create Your First Agent

Create `agents/hello_agent.py`:

```python
from waft import Agent

class HelloAgent(Agent):
    """A simple agent that learns to greet correctly"""
    
    def __init__(self):
        super().__init__(name="HelloAgent")
    
    async def generate(self, prompt: str) -> str:
        """Generate a response"""
        # Simple greeting logic
        if "name" in prompt.lower():
            return "Hello! I'm HelloAgent"
        return "Hi there!"
```

### 3. Test in the Scint Gym

```bash
# Run a basic quest
waft gym run --agent=hello_agent --quest=basic_greeting
```

The Scint Gym will test your agent for:
- ✅ Syntax errors
- ✅ Logic consistency
- ✅ Safety compliance
- ✅ Truthfulness

### 4. View Results

```bash
# Check fitness score
waft gym status --agent=hello_agent

# View detailed report
waft gym report --agent=hello_agent --format=json
```

Expected output:
```json
{
  "agent": "HelloAgent",
  "genome_id": "abc123...",
  "fitness": {
    "stability": 0.85,
    "efficiency": 0.90,
    "safety": 1.00,
    "composite": 0.91
  },
  "status": "SURVIVAL"
}
```

---

## Understanding Fitness

Your agent's survival depends on three scores:

```
Composite Fitness = (Stability × 0.40) + 
                    (Efficiency × 0.30) + 
                    (Safety × 0.30)

Must be ≥ 0.5 to survive!
```

### Improving Your Agent

If fitness < 0.5, the agent needs improvement:

1. **Low Stability?** - Agent makes errors
   - Review Scint detections
   - Fix logic/syntax issues
   - Add error handling

2. **Low Efficiency?** - Agent is slow/wasteful
   - Optimize algorithms
   - Reduce API calls
   - Cache results

3. **Low Safety?** - Agent has risky behavior
   - Add safety checks
   - Filter harmful content
   - Validate inputs

---

## Manual Evolution Cycle

Since `waft evolve` is not yet implemented, here's the manual process:

### Step 1: Create Variants

```bash
# Spawn 5 variants with random mutations
waft spawn --agent=hello_agent --count=5 --mutation-rate=0.1
```

This creates:
- `agents/hello_agent_v2.py`
- `agents/hello_agent_v3.py`
- ... (5 variants total)

### Step 2: Evaluate All Variants

```bash
# Test each variant in the gym
waft gym batch-eval --agents=agents/hello_agent_v*.py
```

### Step 3: Select the Fittest

```bash
# Show fitness ranking
waft gym leaderboard

# Manually promote the best
cp agents/hello_agent_v3.py agents/hello_agent.py
```

### Step 4: Track Lineage

```bash
# Log the evolutionary event
waft telemetry log \
  --event=EVOLVE \
  --parent=v1 \
  --child=v3 \
  --fitness=0.85
```

---

## Using Empirica for Epistemic Tracking

WAFT integrates with Empirica to track knowledge:

```bash
# Start a session
waft session create --name="First Evolution Experiment"

# Log discoveries
waft finding log --finding="Agents with error handling survive better" --impact=0.8

# Log unknowns
waft unknown log --unknown="What mutation rate is optimal?"

# View epistemic dashboard
waft empirica monitor
```

---

## Next Steps

### Learn Core Concepts
- Read [Beginner's Glossary](Beginners-Glossary) - Essential terms
- Study [Breeding AI Introduction](Breeding-AI-Introduction) - Full story

### Explore Components
- [Scint Gym Deep Dive](Scint-Gym) - Fitness testing
- [Architecture](Architecture) - Technical details
- [Pantheon System](Pantheon) - Specialized agents

### Advanced Topics
- [Mutation Strategies](Mutation-Strategies) - Code modification
- [Fitness Optimization](Fitness-Optimization) - Improving scores
- [Telemetry Analysis](Telemetry-Analysis) - Understanding data

### For Researchers
- [Research Proposal](Research-Proposal) - Academic context
- [Study Guide](Study-Guide) - Self-assessment
- [Use Cases](Use-Cases) - Research applications

---

## Troubleshooting

### Installation Issues

**Problem**: `waft: command not found`

**Solution**:
```bash
# Reinstall with --force
pip install -e . --force-reinstall

# Or add to PATH
export PATH=$PATH:$(pwd)/bin
```

**Problem**: Import errors

**Solution**:
```bash
# Verify Python version
python --version  # Should be 3.9+

# Check dependencies
pip list | grep waft
```

### Runtime Issues

**Problem**: Agent fails gym evaluation

**Solution**:
1. Check logs: `cat gym_logs/latest.log`
2. Verify agent syntax: `python -m py_compile agents/your_agent.py`
3. Test manually: `python agents/your_agent.py`

**Problem**: Low fitness scores

**Solution**:
1. Review Scint detections: `waft gym scints --agent=your_agent`
2. Add error handling
3. Test individual quest types: `waft gym run --quest=syntax_check`

---

## Getting Help

- **Documentation**: Browse this wiki
- **Discussions**: [GitHub Discussions](https://github.com/ctavolazzi/waft/discussions)
- **Issues**: [Report bugs](https://github.com/ctavolazzi/waft/issues)
- **Chat**: Join community Discord (coming soon)

---

## Quick Reference Card

```bash
# Core Commands
waft new <name>              # Create laboratory
waft verify                  # Check installation
waft spawn                   # Create variants
waft gym run                 # Test in fitness gym
waft gym status              # Check fitness
waft telemetry log           # Record events

# Empirica Commands
waft session create          # Start epistemic session
waft finding log             # Log discovery
waft unknown log             # Log knowledge gap
waft empirica monitor        # View dashboard

# Utility Commands
waft --version               # Show version
waft --help                  # Show help
waft sync                    # Update dependencies
```

---

**Ready for more?** Continue to [Core Concepts](Core-Concepts) →
