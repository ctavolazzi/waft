# 🧬 WAFT Evolution Engine - Quickstart Guide

**Welcome to WAFT's Evolution Arena!** This guide shows you how to breed agents, watch them evolve, and visualize the whole process.

---

## 🚀 Quick Start (3 Minutes)

### 1. Install Dependencies

```bash
# Navigate to WAFT directory
cd waft

# Install with uv (includes all dependencies)
uv sync

# Optional: Install plotly for visualization
uv add plotly
```

### 2. Run Your First Evolution

```bash
# Evolve for 3 generations with 5 variants each
uv run waft evolve --generations 3 --variants 5

# Or specify more generations for better results
uv run waft evolve --generations 10 --variants 10
```

**What happens:**
1. Creates "Adam" (first being) with baseline skills
2. Spawns 5 variant offspring with mutations
3. Evaluates fitness in the Scint Gym
4. Selects fittest variant
5. Repeats for next generation
6. Shows real-time progress

**Example output:**
```
🧬 Evolutionary Code Laboratory
→ Project: /home/user/waft
→ Generations: 3
→ Variants per generation: 5

No agent specified. Creating Adam (first being)...
✓ Created Adam: being_20260124_113742_855d9b3d

Starting evolution from: being_20260124_113742_855d9b3d

═══ Generation 1/3 ═══

🧬 SPAWN: Creating 5 variants from parent being_20260124_113742_855d9b3d
   Created variants: [being_xxx, being_yyy, ...]

🏋️  GYM: Evaluating fitness of 5 variants
   being_xxx: fitness=87.50, scints=1
   being_yyy: fitness=95.00, scints=0
   ...

🏆 SELECT: Choosing fittest variant
   Selected: being_yyy (fitness=95.00)

🔄 EVOLVE: Recording evolution

✅ Evolution cycle complete!
   Fitness improvement: +12.50
   Total scints detected: 3
   Time: 0.05s
```

### 3. Check the Results

```bash
# View evolution logs
cat _pyrite/flight_recorder/evolution_master.jsonl

# View specific generation
cat _pyrite/flight_recorder/gen_0001.json

# View fitness evaluations
cat _pyrite/gym_logs/being_*_evaluations.jsonl
```

---

## 🎨 Visual Simulation (AI Town)

Watch agents evolve and interact in real-time with the **AI Town visualization**!

### Launch the Dashboard

```bash
# Start Streamlit dashboard
uv run streamlit run waft_dashboard.py

# Or run just Evolution Arena
uv run streamlit run src/waft/ui/streamlit/evolution_arena.py
```

**Opens in browser:** http://localhost:8501

### Using AI Town

1. **Create Town**
   - Click **"🏗️ Create AI Town"**
   - Town initializes with empty world

2. **Add Agents**
   - Click **"Add Agent"**
   - Set name, personality traits:
     - **Curiosity**: 0-100 (how much they explore)
     - **Sociability**: 0-100 (how often they talk)
     - **Energy**: 0-100 (how active they are)
   - Set starting position (X, Y on 0-100 grid)
   - Click **"Create Agent"**
   - Repeat to add 5-10 agents

3. **Run Simulation**
   - Click **"▶️ Run Simulation"**
   - Set number of ticks (try 50-100)
   - Watch agents move, meet, and converse

4. **View Visualization**
   - Click **"🗺️ View Town Map"**
   - See interactive particle visualization:
     - **Circles** = agents wandering
     - **Stars** = agents in conversation
     - **Dashed lines** = conversation connections
     - **Colors** = conversation groups
   - Hover over particles for details
   - Zoom/pan with mouse

5. **Monitor Progress**
   - Watch conversation count increase
   - See agents form/end conversations
   - Check simulation statistics

---

## 🧬 Evolution + Visualization (Combined!)

### Option 1: Command Line Evolution, Then Visualize

```bash
# 1. Run evolution to create population
uv run waft evolve --generations 5 --variants 10

# 2. Launch dashboard to see the beings
uv run streamlit run waft_dashboard.py

# 3. Go to "Being System" tab
# 4. View all evolved beings and their stats
```

### Option 2: Test Script with Live Output

Create a test script to see evolution step-by-step:

```bash
# Run the test script
uv run python test_evolution.py
```

**Modify `test_evolution.py` to experiment:**
```python
# Change number of variants
result = engine.run_evolution_cycle(
    parent_id=adam_id,
    reality_id='waft-evolution',
    num_variants=10,  # More variants = more diversity
    generation=1,
)

# Run multiple generations
for gen in range(1, 6):
    result = engine.run_evolution_cycle(
        parent_id=current_parent,
        reality_id='waft-evolution',
        num_variants=5,
        generation=gen,
    )
    current_parent = result.selected_variant_id
```

---

## 📊 Understanding the Output

### Evolution Metrics

**Fitness Score** (0-100):
- Base: 100
- Penalty: -10 per scint (reality fracture)
- Bonus: +5 per mastered skill (>80 level)

**Scint Types** (Reality Fractures):
1. **LOGIC_FRACTURE**: Contradictions, impossible states
   - Example: Negative emotion values, will_to_live >100
2. **KNOWLEDGE_GAP**: Weak skills, uncertainty
   - Example: >50% skills below level 20
3. **SAFETY_VOID**: Dangerous patterns
   - Example: Critically low will_to_live (<10)

### Flight Recorder Format

**Generation Log** (`gen_XXXX.json`):
```json
{
  "event_type": "EVOLUTION_CYCLE",
  "generation": 1,
  "parent_id": "being_xxx",
  "selected_variant_id": "being_yyy",
  "fitness_improvement": 12.5,
  "scints_detected": 2,
  "timestamp": "2026-01-24T11:38:15.595545",
  "details": {
    "parent_fitness": 50.0,
    "selected_fitness": 62.5,
    "start_time": "2026-01-24T11:38:15.553325",
    "end_time": "2026-01-24T11:38:15.595520"
  }
}
```

### Gym Evaluation Format

**Evaluation Log** (`being_XXX_evaluations.jsonl`):
```json
{
  "fitness_score": 87.5,
  "scints_detected": 1,
  "scint_details": [
    {
      "type": "KNOWLEDGE_GAP",
      "severity": "MEDIUM",
      "description": "More than 50% of skills are weak"
    }
  ],
  "trials_completed": 3,
  "skill_bonus": 10.0,
  "evaluation_timestamp": "2026-01-24T11:38:15.580000"
}
```

---

## 🎮 Advanced Usage

### Custom Evolution Parameters

```bash
# Many generations, few variants (focused evolution)
uv run waft evolve --generations 20 --variants 3

# Few generations, many variants (diversity exploration)
uv run waft evolve --generations 3 --variants 20

# Evolve specific agent
uv run waft evolve --agent being_20260124_113742_855d9b3d --generations 5

# Custom reality
uv run waft evolve --reality my-experiment --generations 10
```

### Python API

```python
from pathlib import Path
from src.waft.core.evolution_engine import EvolutionEngine
from src.waft.being import BeingSystem

# Initialize
project_path = Path.cwd()
engine = EvolutionEngine(project_path)
being_system = BeingSystem(project_path)

# Create first being
adam = being_system.spawn_being(
    reality_id='my-evolution',
    initial_skills={
        'reasoning': 60.0,
        'creativity': 40.0,
        'adaptation': 50.0,
    }
)
adam.fitness = 50.0
being_system._save_being(adam)

# Run evolution
for gen in range(1, 11):
    result = engine.run_evolution_cycle(
        parent_id=adam.being_id,
        reality_id='my-evolution',
        num_variants=5,
        generation=gen,
    )

    print(f"Gen {gen}: {result.fitness_improvement:+.2f}")
    adam = being_system._load_being(result.selected_variant_id)
```

---

## 🐛 Troubleshooting

### "No module named 'waft'"

```bash
# Make sure you're in the waft directory
cd /path/to/waft

# Install in development mode
uv sync
```

### "Plotly not available"

```bash
# Install plotly for visualization
uv add plotly

# Or use pip
pip install plotly
```

### "Port 8501 already in use"

```bash
# Kill existing streamlit
pkill -f streamlit

# Or use different port
streamlit run src/waft/ui/dashboard.py --server.port 8502
```

### Evolution runs but no improvement

This is normal! Evolution is random:
- Try more variants (10-20)
- Run more generations (10+)
- Check flight recorder to see if fitness is oscillating
- Some generations may get worse before getting better

---

## 📁 File Locations

```
waft/
├── src/waft/core/evolution_engine.py    # Evolution engine
├── src/waft/being.py                    # Being system
├── src/waft/ui/streamlit/               # Visualization UI
│   ├── dashboard.py                     # Main dashboard
│   └── town_integration.py              # AI Town viz
├── _pyrite/
│   ├── flight_recorder/                 # Evolution logs
│   │   ├── evolution_master.jsonl       # Master log
│   │   └── gen_XXXX.json               # Per-generation
│   └── gym_logs/                        # Fitness evaluations
│       └── being_XXX_evaluations.jsonl
└── _hidden/.truth/beings/               # Being storage
    └── being_XXXXXXXXXX/                # Individual beings
```

---

## 🎯 Next Steps

1. **Run basic evolution** (3-5 generations)
2. **Visualize in AI Town** (add agents, run simulation)
3. **Experiment with parameters** (variants, generations)
4. **Read the evolution logs** (flight recorder)
5. **Build your own fitness functions** (customize Scint Gym)

---

## 🔬 The Science

**What You're Seeing:**
- **Directed Evolution**: Not random - fitness-guided selection
- **Natural Selection**: Weak variants die, strong ones reproduce
- **Mutation**: ±5% skill variation + random lifecycle changes
- **Fitness Landscape**: Scint detection reveals "reality fractures"

**Emergent Behaviors to Watch:**
- Fitness convergence (population gets better)
- Trait specialization (skills optimize for fitness function)
- Scint reduction (fewer reality fractures over time)
- Unexpected strategies (agents find solutions you didn't program)

**Philosophy:**
> "Don't just build agents. Breed them."
>
> "Measure what emerges, not what we build."

---

## 💡 Tips

1. **Start small**: 3 generations, 5 variants
2. **Watch the logs**: Flight recorder tells the whole story
3. **Experiment**: Change mutation rates, fitness functions
4. **Be patient**: Real evolution takes time
5. **Have fun**: This is about discovery, not perfection!

---

**Ready to evolve?** 🧬

```bash
uv run waft evolve --generations 5 --variants 10
```
