# Research Simulation Server

**Interactive web-based research platform for demo batching system**

---

## Quick Start

```bash
# Start the server
python3 scripts/research_simulation_server.py

# Or use the launcher (opens browser automatically)
python3 scripts/run_research_simulation.py
```

**Server URL**: http://localhost:8001

---

## How It Works

### 1. Web Interface
- Beautiful form with input fields
- Start button to launch simulation
- Real-time status updates

### 2. Simulation Execution
- Runs batching system with your parameters
- Generates multiple permutations
- Collects metrics and data

### 3. Data Collection
- Metrics: permutations, souls, karma stats, PDF size, generation time
- Analysis: karma distribution, efficiency metrics
- Constraints: max iterations calculation

### 4. Scientific Method Workflow
- **Observe**: Collect data from simulation
- **Findings**: Analyze patterns and results
- **Hypothesis**: Generate testable hypothesis
- **Test**: Validate hypothesis with evidence
- **Conclusions**: Draw conclusions from results

### 5. Research Report
- Comprehensive PDF report
- All observations, findings, hypothesis, test results
- Conclusions and recommendations
- Downloadable from web interface

---

## Features

✅ **Interactive Web Interface** - Beautiful form-based UI  
✅ **Real-time Status** - Live updates during simulation  
✅ **Data Collection** - Comprehensive metrics gathering  
✅ **Analysis Algorithms** - Karma distribution, efficiency analysis  
✅ **Scientific Method** - Observe → Hypothesis → Test → Conclude  
✅ **Research Report** - PDF report with all findings  
✅ **Ready Status** - Clear completion message with report link  

---

## Usage

1. **Start Server**: Run `python3 scripts/research_simulation_server.py`
2. **Open Browser**: Navigate to http://localhost:8001
3. **Fill Form**: Enter permutations, max pages, max file size
4. **Start Simulation**: Click "Start Simulation" button
5. **Wait for Results**: Status updates in real-time
6. **View Report**: Click "View Research Report" when ready

---

## API Endpoints

- `GET /` - Web interface
- `POST /api/run-simulation` - Run simulation with config
- `GET /api/status` - Get current simulation status
- `GET /api/report` - Download research report PDF

---

**Research Simulation Complete!** 🔬📊
