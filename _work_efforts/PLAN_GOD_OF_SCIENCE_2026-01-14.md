# Plan: God of Science - Autonomous Research Being

**Date**: 2026-01-14  
**Status**: 🎯 INITIAL DESIGN  
**Priority**: CRITICAL - Evolution of Scientist Aspect

---

## Vision

Create **The Scientist** - a Pantheon God that conducts autonomous, observational research using:
- GPT-Researcher architecture for deep web/local research
- Docker-based autonomous execution
- Visual/observational data capture (screenshots, exhibits)
- Comprehensive PDF reports with verifiable exhibits
- Electron web interface for real-time monitoring

**The Scientist** will be the God of Science, Observation, and Evidence - conducting research that builds up to "Science Bitch" report PDFs with full observational data.

---

## Architecture Overview

### Core Components

1. **The Scientist (God Class)**
   - Location: `src/waft/pantheon/scientist.py`
   - Inherits from Pantheon God pattern (like Magistrate/Judge)
   - Manages research lifecycle

2. **Research Engine**
   - Based on GPT-Researcher architecture
   - Location: `src/waft/pantheon/scientist/research_engine.py`
   - Handles web/local research, data collection

3. **Observational System**
   - Screenshot capture and visual data processing
   - Location: `src/waft/pantheon/scientist/observation.py`
   - SENSE, REACT, OBSERVE, RECORD, EXAMINE, ORGANIZE

4. **Docker Research Container**
   - Autonomous research execution
   - Location: `src/waft/pantheon/scientist/docker_research.py`
   - Isolated environment for research tasks

5. **Report Generator**
   - Comprehensive PDF with exhibits
   - Location: `src/waft/pantheon/scientist/report_generator.py`
   - Integrates with existing PDF generation

6. **Electron Interface**
   - Real-time research monitoring
   - Location: `src/waft/pantheon/scientist/electron_ui/`
   - Web-based dashboard

---

## Phase 1: Foundation - The Scientist God

### 1.1 Create God Class Structure

**File**: `src/waft/pantheon/scientist.py`

```python
class Scientist:
    """
    The Scientist: God of Science, Observation, and Evidence
    
    Conducts autonomous research using:
    - Web and local document research
    - Observational data capture (screenshots, visual evidence)
    - Docker-based autonomous execution
    - Comprehensive report generation with exhibits
    """
    
    def __init__(self, project_path: Path, magistrate: Optional[Magistrate] = None):
        self.pantheon_path = project_path / "_pantheon"
        self.scientist_path = self.pantheon_path / "scientist"
        self.research_path = self.scientist_path / "research"
        self.observations_path = self.scientist_path / "observations"
        self.reports_path = self.scientist_path / "reports"
        self.exhibits_path = self.scientist_path / "exhibits"
        
        # Initialize paths
        for path in [self.research_path, self.observations_path, 
                     self.reports_path, self.exhibits_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    def conduct_research(
        self,
        query: str,
        research_type: str = "web",  # "web", "local", "hybrid"
        use_docker: bool = True,
        capture_observations: bool = True
    ) -> ResearchResult:
        """Conduct autonomous research on a query."""
        pass
    
    def generate_report(
        self,
        research_id: str,
        include_exhibits: bool = True,
        format: str = "pdf"  # "pdf", "html", "both"
    ) -> Path:
        """Generate comprehensive research report with exhibits."""
        pass
```

### 1.2 Integrate with Pantheon

**File**: `src/waft/pantheon/__init__.py`

```python
from .scientist import Scientist

__all__ = ["Magistrate", "Judge", "Scientist"]
```

---

## Phase 2: Research Engine (OpenHands SDK Integration) ⭐ **UPDATED**

### 2.1 Use OpenHands SDK (Instead of Building from Scratch)

**Approach**: 
- **Use OpenHands SDK** - Production-ready agent framework
- Integrate with Scientist God
- Add custom observational tools on top

**Why OpenHands**:
- ✅ **Pre-defined tools**: Web browsing (Tavily MCP), file editing, bash execution
- ✅ **Docker execution**: REST-based Agent Server (exactly what we need!)
- ✅ **MCP integration**: Native support (we already use MCP!)
- ✅ **State-of-the-art**: Top performer on coding benchmarks
- ✅ **Model-agnostic**: Works with any LLM

**Key OpenHands Components**:
- `openhands.sdk.agent` - Agent execution framework
- `openhands.sdk.workspace` - Workspace management
- `openhands.sdk.tool` - Tool system (extensible)
- **Tavily MCP** - Web browsing (built-in!)

**Location**: `src/waft/pantheon/scientist/research_engine/` (wraps OpenHands)

### 2.2 Research Workflow (OpenHands-Powered)

```python
from openhands.sdk.agent import Agent
from openhands.sdk.workspace import Workspace

class ResearchEngine:
    """
    Research engine powered by OpenHands SDK.
    
    Uses OpenHands for:
    - Web browsing (Tavily MCP)
    - File editing (report generation)
    - Task execution (research workflow)
    - Docker execution (autonomous research)
    """
    
    def __init__(self, project_path: Path):
        self.workspace = Workspace(project_path)
        self.agent = Agent(
            workspace=self.workspace,
            tools=[
                "web_browse",  # Tavily MCP (built-in!)
                "file_edit",   # File editing
                "bash",        # Command execution
            ],
            custom_tools=[
                ScreenshotTool(),      # Our custom tool
                ExhibitGeneratorTool() # Our custom tool
            ]
        )
    
    async def conduct_research(
        self,
        query: str,
        report_source: str = "web",  # "web", "local", "hybrid"
        use_docker: bool = True
    ) -> ResearchResult:
        """Conduct deep research using OpenHands agent."""
        
        # Research task for OpenHands agent
        research_task = f"""
        Research the following query: {query}
        
        Steps:
        1. Search the web for relevant information
        2. Collect sources and citations
        3. Synthesize findings
        4. Generate comprehensive report in markdown
        """
        
        if use_docker:
            # Use OpenHands Agent Server (Docker)
            result = await self.agent.run_remote(
                task=research_task,
                server_url="http://localhost:8000"  # Agent Server
            )
        else:
            # Local execution
            result = await self.agent.run(task=research_task)
        
        return ResearchResult.from_openhands(result)
```

---

## Phase 3: Observational System

### 3.1 Observation Capture

**File**: `src/waft/pantheon/scientist/observation.py`

```python
class ObservationSystem:
    """
    Observational data capture system.
    
    Capabilities:
    - SENSE: Capture screenshots, visual data
    - REACT: Respond to visual stimuli
    - OBSERVE: Monitor research process
    - RECORD: Store observational data
    - EXAMINE: Analyze captured data
    - ORGANIZE: Structure observations
    - DOCUMENT: Create documentation
    - COLLECT: Gather evidence
    - BUILD: Construct knowledge
    - DISPLAY: Present findings
    """
    
    def capture_screenshot(
        self,
        context: str,
        research_stage: str
    ) -> Path:
        """Capture screenshot of current state."""
        pass
    
    def record_observation(
        self,
        observation_type: str,  # "screenshot", "data", "state", "event"
        data: Dict[str, Any],
        research_id: str
    ) -> Observation:
        """Record an observation."""
        pass
    
    def create_exhibit(
        self,
        observation: Observation,
        exhibit_label: str  # "Exhibit A", "Exhibit B", etc.
    ) -> Exhibit:
        """Create verifiable exhibit from observation."""
        pass
```

### 3.2 Visual Data Processing

- Screenshot capture during research
- State snapshots at key points
- Visual evidence of findings
- Exhibit generation with labels

---

## Phase 4: Docker-Based Autonomous Research ⭐ **SIMPLIFIED**

### 4.1 Use OpenHands Agent Server (Docker)

**OpenHands provides Docker execution out of the box!**

**File**: `src/waft/pantheon/scientist/docker_research.py`

```python
from openhands.sdk.agent import Agent

class DockerResearchRunner:
    """
    Docker-based autonomous research using OpenHands Agent Server.
    
    OpenHands Agent Server provides:
    - Docker/Kubernetes deployment
    - REST API for remote execution
    - Isolated execution environment
    - Production-ready infrastructure
    """
    
    def __init__(self, agent_server_url: str = "http://localhost:8000"):
        self.agent_server_url = agent_server_url
        self.agent = Agent()  # OpenHands agent
    
    async def run_research(
        self,
        query: str,
        research_config: Dict[str, Any]
    ) -> ResearchResult:
        """Run research in Docker via OpenHands Agent Server."""
        # OpenHands handles Docker execution automatically!
        result = await self.agent.run_remote(
            task=f"Research: {query}",
            server_url=self.agent_server_url
        )
        return ResearchResult.from_openhands(result)
```

### 4.2 OpenHands Docker Setup

**OpenHands provides Docker setup - no custom Dockerfile needed!**

```bash
# Use OpenHands Agent Server
docker run -p 8000:8000 openhands/agent-server

# Or use docker-compose (if provided by OpenHands)
docker-compose up agent-server
```

**Benefits**:
- ✅ No custom Dockerfile needed
- ✅ Production-ready infrastructure
- ✅ Automatic resource management
- ✅ Built-in security

---

## Phase 5: Report Generation with Exhibits

### 5.1 Comprehensive PDF Report

**File**: `src/waft/pantheon/scientist/report_generator.py`

```python
class ResearchReportGenerator:
    """
    Generate comprehensive research reports with exhibits.
    
    Report includes:
    - Executive summary
    - Research methodology
    - Findings with citations
    - Exhibits (screenshots, visual evidence)
    - Sources and references
    - Verifiable evidence chain
    """
    
    def generate_pdf_report(
        self,
        research_result: ResearchResult,
        observations: List[Observation],
        exhibits: List[Exhibit]
    ) -> Path:
        """Generate comprehensive PDF report."""
        # 1. Build report structure
        # 2. Add research content
        # 3. Embed exhibits (screenshots)
        # 4. Add citations and sources
        # 5. Generate PDF using academic template
        pass
```

### 5.2 Exhibit Integration

- Screenshots embedded as "Exhibit A", "Exhibit B", etc.
- Each exhibit labeled and referenced
- Visual evidence of research process
- Verifiable proof of findings

---

## Phase 6: Electron Web Interface

### 6.1 Electron App Structure

**Location**: `src/waft/pantheon/scientist/electron_ui/`

```
electron_ui/
├── main.js          # Electron main process
├── renderer/        # Web UI
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── package.json
└── preload.js
```

### 6.2 Real-Time Monitoring

- Live research progress
- Observation feed
- Exhibit gallery
- Report preview
- Research history

---

## Phase 7: Integration with Science-Bitch

### 7.1 Evolution Path

1. **Current**: `science-bitch` command (basic scientific method)
2. **Phase 1**: Add observational capabilities
3. **Phase 2**: Integrate GPT-Researcher engine
4. **Phase 3**: Add Docker execution
5. **Phase 4**: Create Scientist God
6. **Phase 5**: Full autonomous research with exhibits

### 7.2 Command Integration

```bash
# Use Scientist God for research
waft scientist research "What are the latest developments in AI research?"

# Generate report with exhibits
waft scientist report --research-id <id> --include-exhibits

# Monitor research in Electron
waft scientist monitor
```

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Create Scientist God class structure
- [ ] Integrate with Pantheon system
- [ ] Basic research workflow

### Phase 2: Research Engine (Week 2) ⭐ **UPDATED**
- [ ] Install OpenHands SDK
- [ ] Set up OpenHands Agent Server (Docker)
- [ ] Integrate OpenHands agent with Scientist God
- [ ] Configure Tavily MCP for web browsing
- [ ] Test web/local research capabilities

### Phase 3: Observations (Week 3)
- [ ] Screenshot capture system
- [ ] Observation recording
- [ ] Exhibit generation

### Phase 4: Docker (Week 4)
- [ ] Docker research container
- [ ] Autonomous execution
- [ ] Result extraction

### Phase 5: Reports (Week 5)
- [ ] PDF generation with exhibits
- [ ] Citation system
- [ ] Verifiable evidence chain

### Phase 6: Electron UI (Week 6)
- [ ] Electron app setup
- [ ] Real-time monitoring
- [ ] Research dashboard

### Phase 7: Integration (Week 7)
- [ ] Integrate with science-bitch
- [ ] Full workflow testing
- [ ] Documentation

---

## Key Design Principles

1. **Observational First**: All research must capture visual evidence
2. **Verifiable**: Every claim must have exhibit proof
3. **Autonomous**: Docker-based execution for reproducibility
4. **Comprehensive**: Full citations, sources, exhibits
5. **God Pattern**: Follows Pantheon architecture (Magistrate/Judge)

---

## Success Criteria

✅ **The Scientist** can:
- Conduct autonomous research using GPT-Researcher architecture
- Capture observational data (screenshots, visual evidence)
- Run research in Docker containers
- Generate comprehensive PDF reports with exhibits
- Display findings in Electron web interface
- Integrate with existing science-bitch workflow

✅ **Reports include**:
- Executive summary
- Research methodology
- Findings with citations
- Exhibits (Exhibit A, B, C...) with screenshots
- Sources and references
- Verifiable evidence chain

✅ **Observational capabilities**:
- SENSE: Screenshot capture
- REACT: Response to visual data
- OBSERVE: Monitor research process
- RECORD: Store observations
- EXAMINE: Analyze data
- ORGANIZE: Structure findings
- DOCUMENT: Create documentation
- COLLECT: Gather evidence
- BUILD: Construct knowledge
- DISPLAY: Present in Electron UI

---

## Next Steps

1. **Start with Phase 1**: Create Scientist God class
2. **Study GPT-Researcher**: Understand architecture
3. **Design observation system**: Screenshot capture workflow
4. **Plan Docker integration**: Container design
5. **Design report format**: PDF with exhibits structure

---

**This is the evolution of the Scientist Aspect into a full Pantheon God - The God of Science, Observation, and Evidence.**
