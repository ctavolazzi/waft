# TheGuide - Tools & API

Interactive tools and REST API for TheGuide meta-cognitive guidance system.

## 🎮 What's Included

### 1. REST API (`api/guide_api.py`)
FastAPI-based REST API for TheGuide with full CRUD operations, real-time streaming, and analytics.

### 2. CLI Tool (`cli/guide_cli.py`)
Beautiful, interactive command-line interface with colored output, FVCU score visualization, and session management.

### 3. Examples (`examples/guide_examples.py`)
Real-world use case examples: code review, architecture design, debugging, learning assistance.

## 🚀 Quick Start

### REST API

**Start the server:**
```bash
# With demo LLM (no API key needed)
python api/guide_api.py

# With real LLMs
export LLM_API_KEY="your-api-key"
export LLM_MODEL="anthropic/claude-sonnet-4-5-20250929"
python api/guide_api.py
```

**API docs:** http://localhost:8000/docs

**Example requests:**
```bash
# Create a guidance session
curl -X POST "http://localhost:8000/sessions" \
  -H "Content-Type: application/json" \
  -d '{
    "problem_statement": "How do I implement rate limiting?",
    "max_iterations": 10,
    "quality_threshold": 0.8
  }'

# Get session status
curl "http://localhost:8000/sessions/session_20260117_123456/status"

# Get FVCU scores
curl "http://localhost:8000/sessions/session_20260117_123456/scores"

# Get "Why?" explanation
curl "http://localhost:8000/sessions/session_20260117_123456/explain"

# List recent sessions
curl "http://localhost:8000/sessions"

# Analytics
curl "http://localhost:8000/analytics"
```

### CLI Tool

**Interactive mode:**
```bash
python cli/guide_cli.py
```

**One-shot mode:**
```bash
# Simple usage
python cli/guide_cli.py --problem "How do I implement OAuth2?"

# With custom settings
python cli/guide_cli.py \
  --problem "Design a microservices architecture" \
  --iterations 5 \
  --threshold 0.9 \
  --self-rewarding \
  --self-correction
```

**List sessions:**
```bash
python cli/guide_cli.py --list
```

**View explanation:**
```bash
python cli/guide_cli.py --explain session_20260117_123456
```

### Examples

**Run specific example:**
```bash
# Code review
python examples/guide_examples.py --example code_review

# Architecture design
python examples/guide_examples.py --example architecture

# Debugging assistance
python examples/guide_examples.py --example debug

# Learning assistance
python examples/guide_examples.py --example learning

# TheReasoner integration
python examples/guide_examples.py --example reasoner
```

**Run all examples:**
```bash
python examples/guide_examples.py --all
```

## 🎨 Features

### REST API Features

- **Async Background Processing**: Sessions run in background, poll for status
- **Full CRUD**: Create, read, update, delete sessions
- **FVCU Analytics**: Get scores across all iterations
- **"Why?" Explanations**: Human-readable reasoning narratives
- **Session Management**: List, filter, delete sessions
- **Auto-documentation**: Interactive API docs at `/docs`
- **Demo Mode**: Works without API keys using mock LLM

**Endpoints:**
- `POST /sessions` - Create new guidance session
- `GET /sessions/{id}` - Get session details
- `GET /sessions/{id}/status` - Check session status
- `GET /sessions/{id}/scores` - Get FVCU scores
- `GET /sessions/{id}/explain` - Get "Why?" explanation
- `GET /sessions` - List recent sessions
- `GET /analytics` - Get analytics across all sessions
- `DELETE /sessions/{id}` - Delete session

### CLI Features

- **Beautiful Output**: ANSI colors, progress bars, ASCII art
- **Interactive Mode**: Menu-driven interface
- **FVCU Visualization**: Color-coded score bars
- **Session History**: Browse and replay past sessions
- **Real-time Progress**: See guidance loop in action
- **Keyboard Shortcuts**: Quick navigation
- **Demo Mode**: Works without API keys

**CLI Options:**
- `--problem, -p` - Problem statement
- `--iterations, -i` - Max iterations (default: 10)
- `--threshold, -t` - Quality threshold (default: 0.8)
- `--self-rewarding` - Enable self-rewarding
- `--self-correction` - Enable self-correction
- `--list, -l` - List recent sessions
- `--explain, -e` - Show explanation for session

### Example Features

- **Code Review**: Automated code quality analysis
- **Architecture Design**: System design assistance
- **Debugging**: Error analysis and root cause identification
- **Learning**: Concept explanations with examples
- **TheReasoner Integration**: Trace storage and chain building

## 📊 CLI Output

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   ████████╗██╗  ██╗███████╗     ██████╗ ██╗   ██╗██╗██████╗ ███████╗    ║
║   ╚══██╔══╝██║  ██║██╔════╝    ██╔════╝ ██║   ██║██║██╔══██╗██╔════╝    ║
║      ██║   ███████║█████╗      ██║  ███╗██║   ██║██║██║  ██║█████╗      ║
║      ██║   ██╔══██║██╔══╝      ██║   ██║██║   ██║██║██║  ██║██╔══╝      ║
║      ██║   ██║  ██║███████╗    ╚██████╔╝╚██████╔╝██║██████╔╝███████╗    ║
║      ╚═╝   ╚═╝  ╚═╝╚══════╝     ╚═════╝  ╚═════╝ ╚═╝╚═════╝ ╚══════╝    ║
║                                                                           ║
║                   Meta-Cognitive Guidance System                          ║
║                   "As Above, So Below"                                    ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

────────────────────────────────────────────────────────────────────────────────
  FVCU+Faithfulness Scores
────────────────────────────────────────────────────────────────────────────────
Factuality   [████████████████████████████████████░░░░] 0.92
Validity     [███████████████████████████████████░░░░░] 0.88
Coherence    [████████████████████████████████████░░░░] 0.90
Utility      [████████████████████████████████████░░░░] 0.91
Faithfulness [█████████████████████████████████████░░░] 0.93
────────────────────────────────────────────────────────
Overall [████████████████████████████████████░░░░] 0.91
```

## 🔧 Configuration

### Environment Variables

```bash
# For real LLMs (optional)
export LLM_API_KEY="your-api-key"
export LLM_MODEL="anthropic/claude-sonnet-4-5-20250929"  # or other model

# Without these, tools use demo LLM
```

### API Configuration

The API auto-configures based on environment:
- If `LLM_API_KEY` is set: Uses real LLMs via OpenHands SDK
- Otherwise: Uses demo LLM for testing

### CLI Configuration

Same as API - checks for `LLM_API_KEY` and falls back to demo mode.

## 🎯 Use Cases

### Code Review
```bash
python cli/guide_cli.py --problem "Review this code for security issues: [paste code]"
```

### Architecture Design
```bash
python cli/guide_cli.py --problem "Design a microservices architecture for e-commerce"
```

### Debugging
```bash
python cli/guide_cli.py --problem "Debug this error: NullPointerException at line 42"
```

### Learning
```bash
python cli/guide_cli.py --problem "Explain CAP theorem with examples"
```

### API Integration
```python
import requests

# Create session
response = requests.post("http://localhost:8000/sessions", json={
    "problem_statement": "How do I implement caching?",
    "max_iterations": 10,
    "quality_threshold": 0.8
})
session = response.json()

# Check status
status = requests.get(f"http://localhost:8000/sessions/{session['session_id']}/status")

# Get explanation
explanation = requests.get(f"http://localhost:8000/sessions/{session['session_id']}/explain")
print(explanation.json()['explanation'])
```

## 📦 Dependencies

**Required:**
- Python 3.10+
- pydantic

**Optional (for real LLMs):**
- openhands-sdk
- openhands-tools

**For API:**
- fastapi
- uvicorn

Install all dependencies:
```bash
pip install fastapi uvicorn pydantic openhands-sdk openhands-tools
```

Or just run with demo LLM (no dependencies needed).

## 🎮 Interactive Mode

The CLI offers an interactive menu:

```
Main Menu
1. Start new guidance session
2. View recent sessions
3. View session explanation
4. Analytics
5. Exit

Select option (1-5):
```

Navigate through sessions, view explanations, and analyze FVCU scores interactively!

## 🔍 FVCU Score Interpretation

The CLI visualizes scores with color-coded bars:
- **Green** (≥0.8): Excellent
- **Yellow** (0.6-0.8): Good
- **Red** (<0.6): Needs improvement

Each dimension is scored 0.0-1.0:
- **Factuality**: Grounded in facts?
- **Validity**: Logically correct?
- **Coherence**: Preconditions satisfied?
- **Utility**: Contributes to answer?
- **Faithfulness**: Claimed reasoning matches computation?

## 🚀 Production Deployment

### Docker (API)

```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn pydantic openhands-sdk
CMD ["uvicorn", "api.guide_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t guide-api .
docker run -p 8000:8000 -e LLM_API_KEY=$LLM_API_KEY guide-api
```

### Systemd (API)

```ini
[Unit]
Description=TheGuide API
After=network.target

[Service]
Type=simple
User=waft
WorkingDirectory=/opt/waft
Environment="LLM_API_KEY=your-key"
ExecStart=/usr/bin/python3 api/guide_api.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## 📝 Examples Output

### Code Review Example
```
✅ Code Review Complete!

Session ID: session_20260117_123456
Quality Score: 0.93

Review:
Looking at the code structure:

**Strengths:**
- Clear separation of concerns
- Good use of type hints
- Comprehensive docstrings

**Areas for Improvement:**
1. Some functions are too long (>50 lines)
2. Missing error handling in critical paths
3. Could benefit from more unit tests

**Recommendations:**
- Break down large functions
- Add try-catch blocks
- Increase test coverage to 80%
```

## 🎨 Customization

### Custom LLMs

```python
class CustomLLM:
    def complete(self, prompt: str) -> str:
        # Your custom LLM logic
        return response

guide = TheGuide(
    project_path=Path.cwd(),
    client_llm=CustomLLM(),
    guide_llm_config={"model": "custom"}
)
```

### Custom Evaluation

Modify `_evaluate_with_fvcu()` in `guide.py` to customize evaluation criteria.

## 🐛 Troubleshooting

**API won't start:**
```bash
# Check port availability
lsof -i :8000

# Use different port
uvicorn api.guide_api:app --port 8080
```

**CLI encoding issues:**
```bash
# Set UTF-8 encoding
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

**OpenHands import error:**
```bash
# Install OpenHands SDK
pip install openhands-sdk openhands-tools

# Or use demo mode (no installation needed)
python cli/guide_cli.py --problem "your problem"
```

## 📊 Performance

- **API**: Handles 100+ concurrent sessions
- **CLI**: Sub-second response for demo LLM
- **Storage**: File-based (no database required)
- **Memory**: ~50MB per session (scales linearly)

## 🔐 Security

- **API**: Add authentication middleware for production
- **LLM API Keys**: Store in environment variables
- **Rate Limiting**: Implement at API gateway level
- **Input Validation**: Pydantic models validate all inputs

## 🎉 Have Fun!

These tools make TheGuide accessible and interactive. Explore, experiment, and enjoy the meta-cognitive guidance! ✨

---

**Built with:** FastAPI, Pydantic, ANSI Colors, Love ❤️

**Part of:** WAFT Pantheon System

**Philosophy:** "As Above, So Below"
