"""
Templates module - Text assets for project scaffolding.
"""

from pathlib import Path


class TemplateWriter:
    """Writes template files to a project."""

    def __init__(self, project_path: Path):
        """
        Initialize template writer.

        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.templates_dir = Path(__file__).parent

    def write_all(self) -> None:
        """Write all templates to the project."""
        self.write_justfile()
        self.write_ci_yml()
        self.write_agents_py()

    def write_justfile(self) -> None:
        """Write Justfile template."""
        justfile_path = self.project_path / "Justfile"

        if justfile_path.exists():
            return

        content = """# Justfile - Modern task runner
# Install: cargo install just
# Usage: just <recipe>

# Setup project dependencies
setup:
    uv sync

# Run tests
test:
    uv run pytest

# Run adversarial validation suite
verify:
    uv run tools/validation_test.py

# Fix linting and formatting issues
fix:
    uv run ruff check --fix .
    uv run ruff format .

# Format code only
format:
    uv run ruff format .

# Lint code only
lint:
    uv run ruff check .

# Run all checks (lint, format, test, verify)
check: lint format test verify
    @echo "✅ All checks passed!"

# Clean generated files
clean:
    rm -rf .venv
    rm -f uv.lock
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete
    find . -type f -name ".coverage" -delete
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
    @echo "✅ Cleaned generated files"

# Show available recipes
default:
    @just --list
"""
        justfile_path.write_text(content)

    def write_ci_yml(self) -> None:
        """Write GitHub Actions CI workflow."""
        workflows_dir = self.project_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)

        ci_yml = workflows_dir / "ci.yml"

        if ci_yml.exists():
            return

        content = """name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  validate:
    name: Adversarial Verification
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          version: "latest"
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      
      - name: Install dependencies
        run: uv sync
      
      - name: Run Adversarial Verification
        run: uv run tools/validation_test.py
      
      - name: Upload validation report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: validation-report
          path: validation_report.json
          retention-days: 30

  test:
    name: Run Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          version: "latest"
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      
      - name: Install dependencies
        run: uv sync
      
      - name: Run tests
        run: uv run pytest

  lint:
    name: Lint and Format Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          version: "latest"
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      
      - name: Install dependencies
        run: uv sync
      
      - name: Check formatting
        run: uv run ruff format --check .
      
      - name: Check linting
        run: uv run ruff check .
"""
        ci_yml.write_text(content)

    def write_agents_py(self) -> None:
        """Write agents.py template for CrewAI."""
        src_dir = self.project_path / "src"
        src_dir.mkdir(exist_ok=True)

        agents_py = src_dir / "agents.py"

        if agents_py.exists():
            return

        content = """"""
CrewAI Agents - Starter Template

This file provides a starter template for setting up CrewAI agents.
Customize this to fit your project's needs.
"""

from crewai import Agent, Task, Crew
from typing import List, Optional


def create_agent(
    role: str,
    goal: str,
    backstory: str,
    verbose: bool = True,
) -> Agent:
    """
    Create a CrewAI agent.
    
    Args:
        role: The agent's role
        goal: The agent's goal
        backstory: The agent's backstory
        verbose: Whether to enable verbose output
        
    Returns:
        Configured Agent instance
    """
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        verbose=verbose,
        allow_delegation=False,
    )


def create_crew(agents: List[Agent], tasks: List[Task]) -> Crew:
    """
    Create a CrewAI crew.
    
    Args:
        agents: List of agents
        tasks: List of tasks
        
    Returns:
        Configured Crew instance
    """
    return Crew(
        agents=agents,
        tasks=tasks,
        verbose=True,
    )


# Example usage:
if __name__ == "__main__":
    # Create agents
    researcher = create_agent(
        role="Researcher",
        goal="Research and gather information",
        backstory="You are a research specialist...",
    )
    
    writer = create_agent(
        role="Writer",
        goal="Write clear and engaging content",
        backstory="You are a content writer...",
    )
    
    # Create tasks
    research_task = Task(
        description="Research the topic",
        agent=researcher,
    )
    
    writing_task = Task(
        description="Write about the research findings",
        agent=writer,
    )
    
    # Create crew and execute
    crew = create_crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
    )
    
    result = crew.kickoff()
    print(result)
"""
        agents_py.write_text(content)
