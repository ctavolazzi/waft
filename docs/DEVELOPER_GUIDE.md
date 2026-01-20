# Developer Guide

> **Complete guide for developers working with and on WAFT**

Version 0.9.0 - Developer Documentation

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Development Setup](#development-setup)
3. [Project Structure](#project-structure)
4. [Development Workflow](#development-workflow)
5. [Creating Agents](#creating-agents)
6. [Extending WAFT](#extending-waft)
7. [Testing](#testing)
8. [Best Practices](#best-practices)
9. [Debugging](#debugging)
10. [Contributing](#contributing)

---

## Overview

This guide is for developers who want to:
- Build custom agents with WAFT
- Extend WAFT's functionality
- Contribute to WAFT development
- Integrate WAFT with other systems
- Understand WAFT internals

### Prerequisites

**Knowledge**:
- Python 3.10+ (intermediate level)
- Git version control
- Command-line interface
- Object-oriented programming
- Async/await patterns (helpful)

**Tools**:
- Python 3.10 or higher
- uv package manager
- Git
- Code editor (VS Code, PyCharm, vim, etc.)
- just task runner (optional but recommended)

---

## Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ctavolazzi/waft.git
cd waft
```

### 2. Set Up Development Environment

```bash
# Install dependencies
uv sync

# Install WAFT in editable mode
uv tool install --editable .

# Verify installation
waft --version
```

### 3. Configure Development Tools

**Install development dependencies**:
```bash
uv sync --extra dev
```

**Install optional tools**:
```bash
# just task runner (macOS)
brew install just

# just task runner (Linux)
cargo install just

# Or download from: https://github.com/casey/just
```

### 4. Set Up Pre-commit Hooks (Optional)

```bash
# Install pre-commit
uv pip install pre-commit

# Install hooks
pre-commit install
```

### 5. Verify Setup

```bash
# Run verification
waft verify

# Run tests
pytest

# Check code style
ruff check src/

# Format code
ruff format src/
```

---

## Project Structure

### High-Level Structure

```
waft/
├── src/waft/              # Main source code
│   ├── __init__.py
│   ├── main.py           # CLI entry point
│   ├── foundation.py     # Foundation layer
│   ├── being.py          # Entity system
│   ├── tavernkeeper.py   # D&D mechanics
│   └── evolution/        # Evolution modules
│
├── tests/                # Test suite
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── e2e/             # End-to-end tests
│
├── docs/                # Documentation
│   ├── guides/          # User guides
│   ├── api/             # API reference
│   └── tutorials/       # Tutorials
│
├── examples/            # Example projects
│   ├── basic_agent/     # Simple agent
│   └── advanced/        # Advanced examples
│
├── _experiments/        # Experimental features
├── _work_efforts/       # Development tracking
├── scripts/             # Utility scripts
├── pyproject.toml       # Project config
└── README.md            # Main readme
```

### Source Code Organization

```
src/waft/
├── core/                   # Foundation layer
│   ├── foundation.py
│   ├── substrate_manager.py
│   ├── memory_manager.py
│   └── config.py
│
├── cli/                    # CLI interface
│   ├── commands.py
│   ├── validators.py
│   └── formatters.py
│
├── intelligence/           # Intelligence layer
│   ├── empirica_integration.py
│   ├── session_analytics.py
│   └── decision_matrix.py
│
├── personality/            # Personality layer
│   ├── tavernkeeper.py
│   ├── being.py
│   ├── narrator.py
│   └── karma.py
│
└── evolution/              # Evolution layer
    ├── scint_detector.py
    ├── genome_manager.py   # Planned
    └── flight_recorder.py  # Planned
```

---

## Development Workflow

### Daily Development Cycle

```bash
# 1. Create feature branch
git checkout -b feature/my-feature

# 2. Make changes
# ... edit code ...

# 3. Run tests
pytest tests/

# 4. Check code quality
ruff check src/
ruff format src/

# 5. Commit changes
git add .
git commit -m "feat: add my feature"

# 6. Push and create PR
git push origin feature/my-feature
```

### Quick Reinstall During Development

```bash
# When you make changes to WAFT itself
uv tool uninstall waft
uv tool install --editable .

# Or use the convenience script
./scripts/dev-reinstall.sh
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/unit/test_foundation.py

# Specific test
pytest tests/unit/test_foundation.py::test_initialize

# With coverage
pytest --cov=waft --cov-report=html

# Watch mode (requires pytest-watch)
ptw
```

### Code Quality Checks

```bash
# Lint with ruff
ruff check src/

# Format with ruff
ruff format src/

# Type checking (if using mypy)
mypy src/waft/

# All checks via just
just check
```

---

## Creating Agents

### Basic Agent Structure

```python
"""
My custom agent.

This agent does X, Y, and Z.
"""

from typing import Dict, Any, Optional
from pathlib import Path


class MyAgent:
    """
    Description of what this agent does.

    Attributes:
        config: Agent configuration
        state: Internal state
    """

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        project_path: Optional[Path] = None
    ):
        """
        Initialize the agent.

        Args:
            config: Configuration dictionary
            project_path: Path to WAFT project
        """
        self.config = config or {}
        self.project_path = project_path or Path.cwd()
        self.state = {}

    def execute(
        self,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Main execution method.

        Args:
            input_data: Input for the agent

        Returns:
            Output dictionary with results

        Raises:
            ValueError: If input is invalid
        """
        # Validate input
        self._validate_input(input_data)

        # Process
        result = self._process(input_data)

        # Return
        return {
            "success": True,
            "output": result,
            "metadata": self._get_metadata()
        }

    def _validate_input(
        self,
        input_data: Dict[str, Any]
    ) -> None:
        """Validate input data."""
        required_keys = ["key1", "key2"]
        for key in required_keys:
            if key not in input_data:
                raise ValueError(f"Missing required key: {key}")

    def _process(
        self,
        input_data: Dict[str, Any]
    ) -> Any:
        """Process input and return result."""
        # Your logic here
        return processed_result

    def _get_metadata(self) -> Dict[str, Any]:
        """Get execution metadata."""
        return {
            "agent": self.__class__.__name__,
            "config": self.config,
            "state": self.state
        }
```

### Advanced Agent with Evolution

```python
"""
Evolvable agent with genome tracking.
"""

from typing import Dict, Any, Optional
from hashlib import sha256
import json


class EvolvableAgent:
    """Agent that can track and evolve its genome."""

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        code: Optional[str] = None
    ):
        """Initialize with config and code."""
        self.config = config or {}
        self.code = code or self._get_source_code()
        self.genome_id = self._calculate_genome_id()
        self.generation = self.config.get("generation", 0)
        self.parent_id = self.config.get("parent_id")

    def _calculate_genome_id(self) -> str:
        """Calculate SHA-256 genome ID."""
        genome_data = f"{self.code}{json.dumps(self.config, sort_keys=True)}"
        return sha256(genome_data.encode()).hexdigest()

    def _get_source_code(self) -> str:
        """Get agent source code."""
        import inspect
        return inspect.getsource(self.__class__)

    def spawn_variant(
        self,
        mutation: Dict[str, Any],
        variant_name: str
    ) -> "EvolvableAgent":
        """
        Spawn a variant with mutation.

        Args:
            mutation: Changes to apply
            variant_name: Name for variant

        Returns:
            New agent instance with mutation
        """
        # Create new config
        new_config = self.config.copy()
        new_config.update(mutation)
        new_config["generation"] = self.generation + 1
        new_config["parent_id"] = self.genome_id

        # Create variant
        variant = self.__class__(config=new_config, code=self.code)

        return variant

    def get_lineage(self) -> List[str]:
        """Get ancestry (list of parent genome IDs)."""
        lineage = []
        current = self

        while current.parent_id:
            lineage.append(current.parent_id)
            # Load parent (implementation depends on storage)
            current = self._load_parent(current.parent_id)

        return lineage

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent logic."""
        # Your agent logic
        result = self._process(input_data)

        return {
            "success": True,
            "output": result,
            "genome_id": self.genome_id,
            "generation": self.generation
        }
```

### Agent with WAFT Integration

```python
"""
Agent fully integrated with WAFT systems.
"""

from waft.being import Being
from waft.tavernkeeper import TavernKeeper
from waft.karma import KarmaTracker
from waft.empirica_integration import EmpericaClient


class WaftIntegratedAgent:
    """Agent using all WAFT features."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize with WAFT systems."""
        # Create Being
        self.being = Being(
            name=config.get("name", "Agent"),
            being_type="Warforged Wizard"
        )

        # Initialize systems
        self.tavern = TavernKeeper(self.being)
        self.karma = KarmaTracker(self.being)
        self.empirica = EmpericaClient()

        # Start session
        self.session_id = self.empirica.create_session()

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute with full WAFT integration."""
        # Check safety gate
        gate = self.empirica.safety_gate_check(
            operation={"type": "execute", "input": input_data}
        )

        if gate != "PROCEED":
            return {"success": False, "reason": f"Safety gate: {gate}"}

        # Roll intelligence check
        check = self.tavern.roll_check(
            ability="Intelligence",
            difficulty=15
        )

        if not check["success"]:
            # Failed check
            return {
                "success": False,
                "reason": "Failed intelligence check",
                "roll": check
            }

        # Execute
        result = self._process(input_data)

        # Record success
        self.being.earn_scint(50, "Successful execution")
        self.karma.record_action(
            action="Executed task",
            impact=5,
            category="order"
        )
        self.empirica.log_finding(
            content=f"Successfully executed: {input_data}",
            impact=0.7
        )

        return {
            "success": True,
            "output": result,
            "scint": self.being.scint_balance,
            "karma": self.being.karma,
            "check": check
        }

    def _process(self, input_data: Dict[str, Any]) -> Any:
        """Process input data."""
        # Your logic
        return result
```

---

## Extending WAFT

### Adding a New CLI Command

```python
# In src/waft/cli/commands.py or new file

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def my_command(
    arg: str,
    option: str = typer.Option("default", "--option", "-o"),
    verbose: bool = typer.Option(False, "--verbose", "-v")
):
    """
    Description of what this command does.

    Args:
        arg: Required argument
        option: Optional flag
        verbose: Verbose output
    """
    if verbose:
        console.print("[blue]Running my_command...[/blue]")

    # Your logic
    result = do_something(arg, option)

    console.print(f"[green]✓[/green] Success: {result}")


# Register in main.py
from waft.cli.commands import my_command
app.add_typer(my_command.app, name="my-command")
```

### Creating a Custom Template

```python
# In src/waft/evolution/templates/my_template.py

from waft.evolution.document_builder import DocumentTemplate


class MyCustomTemplate(DocumentTemplate):
    """Custom PDF template."""

    template_name = "my_custom"

    def render(
        self,
        content: str,
        metadata: Dict[str, Any]
    ) -> str:
        """
        Render template with content.

        Args:
            content: Markdown content
            metadata: Document metadata

        Returns:
            Rendered HTML
        """
        # Use Jinja2 template
        template = self.jinja_env.get_template("my_custom.html")

        # Render
        html = template.render(
            content=content,
            metadata=metadata,
            styles=self._get_styles()
        )

        return html

    def _get_styles(self) -> str:
        """Get CSS styles for template."""
        return """
        /* Your CSS here */
        body {
            font-family: 'Georgia', serif;
            line-height: 1.6;
        }
        """


# Register template
from waft.evolution.document_builder import DocumentBuilder

DocumentBuilder.register_template(MyCustomTemplate)
```

### Adding Custom Scint Types

```python
# In your project or as WAFT extension

from waft.evolution.scint_detector import ScintDetector, Scint, ScintType
from enum import Enum


# Extend ScintType
class CustomScintType(str, Enum):
    """Custom scint types."""
    PERFORMANCE_ISSUE = "performance_issue"
    SECURITY_VULNERABILITY = "security_vulnerability"


class CustomScintDetector(ScintDetector):
    """Detector with custom scint types."""

    def detect_performance_issues(
        self,
        output: str,
        execution_time: float
    ) -> List[Scint]:
        """Detect performance problems."""
        scints = []

        if execution_time > 5.0:
            scints.append(Scint(
                type=CustomScintType.PERFORMANCE_ISSUE,
                severity="high",
                location="execution",
                description=f"Slow execution: {execution_time}s"
            ))

        return scints

    def detect_security_issues(
        self,
        code: str
    ) -> List[Scint]:
        """Detect security vulnerabilities."""
        scints = []

        dangerous_patterns = [
            r'eval\(',
            r'exec\(',
            r'__import__',
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, code):
                scints.append(Scint(
                    type=CustomScintType.SECURITY_VULNERABILITY,
                    severity="critical",
                    location=pattern,
                    description=f"Dangerous operation: {pattern}"
                ))

        return scints
```

---

## Testing

### Writing Unit Tests

```python
# tests/unit/test_my_agent.py

import pytest
from pathlib import Path
from my_lab.agents import MyAgent


class TestMyAgent:
    """Tests for MyAgent."""

    @pytest.fixture
    def agent(self):
        """Create agent instance for testing."""
        config = {"param1": "value1"}
        return MyAgent(config=config)

    def test_initialization(self, agent):
        """Test agent initializes correctly."""
        assert agent.config == {"param1": "value1"}
        assert agent.state == {}

    def test_execute_success(self, agent):
        """Test successful execution."""
        input_data = {
            "key1": "value1",
            "key2": "value2"
        }

        result = agent.execute(input_data)

        assert result["success"] is True
        assert "output" in result

    def test_execute_invalid_input(self, agent):
        """Test execution with invalid input."""
        input_data = {"key1": "value1"}  # Missing key2

        with pytest.raises(ValueError, match="Missing required key"):
            agent.execute(input_data)

    def test_process(self, agent):
        """Test internal processing."""
        input_data = {"key1": "test"}
        result = agent._process(input_data)

        assert result is not None

    def test_metadata(self, agent):
        """Test metadata generation."""
        metadata = agent._get_metadata()

        assert metadata["agent"] == "MyAgent"
        assert "config" in metadata
        assert "state" in metadata
```

### Integration Tests

```python
# tests/integration/test_agent_integration.py

import pytest
from pathlib import Path
from waft.foundation import Foundation
from my_lab.agents import MyAgent


class TestAgentIntegration:
    """Integration tests for agent with WAFT."""

    @pytest.fixture
    def project_path(self, tmp_path):
        """Create temporary project."""
        foundation = Foundation(
            project_name="test_lab",
            project_path=tmp_path
        )
        foundation.initialize()
        return tmp_path / "test_lab"

    def test_agent_in_project(self, project_path):
        """Test agent works in WAFT project."""
        agent = MyAgent(project_path=project_path)
        result = agent.execute({"key1": "val1", "key2": "val2"})

        assert result["success"] is True

    def test_agent_with_empirica(self, project_path):
        """Test agent with Empirica tracking."""
        from waft.empirica_integration import EmpericaClient

        client = EmpericaClient(project_path=project_path)
        session_id = client.create_session()

        agent = MyAgent(project_path=project_path)
        result = agent.execute({"key1": "val1", "key2": "val2"})

        # Verify tracking
        assessment = client.get_assessment(session_id)
        assert assessment is not None
```

### Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific test
pytest tests/unit/test_my_agent.py::TestMyAgent::test_execute_success

# With coverage
pytest --cov=waft --cov-report=html
open htmlcov/index.html

# Parallel execution
pytest -n auto

# Watch mode
ptw
```

---

## Best Practices

### 1. Code Style

Follow PEP 8 and project conventions:

```python
# Good: Clear, documented, typed
def process_data(
    input_data: Dict[str, Any],
    options: Optional[Dict[str, Any]] = None
) -> ProcessedResult:
    """
    Process input data with optional configuration.

    Args:
        input_data: Data to process
        options: Processing options

    Returns:
        Processed result object

    Raises:
        ValueError: If input is invalid
    """
    # Implementation
    pass


# Avoid: Unclear, undocumented, untyped
def process(data, opts=None):
    # What does this do?
    pass
```

### 2. Error Handling

Handle errors gracefully:

```python
# Good: Specific exceptions, helpful messages
def load_config(path: Path) -> Dict[str, Any]:
    """Load configuration file."""
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        raise ConfigError(f"Config file not found: {path}")
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in {path}: {e}")


# Avoid: Bare except, silent failures
def load_config(path):
    try:
        return json.load(open(path))
    except:
        return {}  # Silent failure!
```

### 3. Type Hints

Use type hints for clarity:

```python
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

# Good: Clear types
def create_agent(
    name: str,
    config: Dict[str, Any],
    project_path: Optional[Path] = None
) -> Agent:
    """Create and return agent."""
    pass


# Avoid: No types
def create_agent(name, config, project_path=None):
    """Create and return agent."""
    pass
```

### 4. Documentation

Document thoroughly:

```python
class Agent:
    """
    Base agent class for WAFT.

    This class provides the foundation for all WAFT agents.
    Subclass this to create custom agents.

    Attributes:
        config: Agent configuration dictionary
        state: Internal agent state
        genome_id: Unique genome identifier

    Example:
        >>> agent = Agent(config={"param": "value"})
        >>> result = agent.execute(input_data)
        >>> print(result["output"])
    """

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent with given input.

        This is the main entry point for agent execution.
        Override this method in subclasses to implement
        custom behavior.

        Args:
            input_data: Input dictionary with keys:
                - key1 (str): Description
                - key2 (int): Description

        Returns:
            Dictionary with keys:
                - success (bool): Whether execution succeeded
                - output (Any): Execution result
                - metadata (dict): Execution metadata

        Raises:
            ValueError: If input is invalid
            RuntimeError: If execution fails

        Example:
            >>> agent.execute({"key1": "value", "key2": 42})
            {"success": True, "output": ..., "metadata": ...}
        """
        pass
```

### 5. Testing

Write comprehensive tests:

```python
# Test happy path
def test_execute_success():
    """Test successful execution."""
    pass

# Test edge cases
def test_execute_empty_input():
    """Test with empty input."""
    pass

# Test error conditions
def test_execute_invalid_input():
    """Test with invalid input."""
    pass

# Test integration
def test_agent_with_waft_systems():
    """Test agent with WAFT integration."""
    pass
```

---

## Debugging

### Enable Debug Mode

```bash
# Set environment variables
export WAFT_DEBUG=1
export WAFT_LOG_LEVEL=DEBUG

# Run command
waft verify
```

### Use Python Debugger

```python
# In code
import pdb; pdb.set_trace()

# Or using breakpoint() (Python 3.7+)
breakpoint()
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

def my_function():
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
```

### Profiling

```bash
# Profile execution
python -m cProfile -o profile.stats src/waft/main.py

# View results
python -m pstats profile.stats
```

---

## Contributing

See [Contributing Guide](../CONTRIBUTING.md) for:
- Code of conduct
- Pull request process
- Coding standards
- Review process

---

*Last Updated: 2026-01-16 | Version: 0.9.0 | Developer Guide v1.0*
