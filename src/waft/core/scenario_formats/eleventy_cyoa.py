"""
Eleventy CYOA - Level 1 Scenario Format for WAFT.

Minimal CYOA format based on Raymond Camden's Eleventy pattern.
Uses Markdown with YAML front matter for dead-simple branching narratives.

Format Example:
```yaml
---
title: Start of the Story
choices:
  - text: This is choice one
    path: one
  - text: This is choice two
    path: two
---

This is the start of the story. You've got some choices to make now!
```

No choices = "The End"
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()


@dataclass
class Choice:
    """Represents a single choice in a scenario."""

    text: str
    path: str


@dataclass
class ScenarioNode:
    """Represents a single node (page) in the scenario."""

    id: str
    title: str
    content: str
    choices: list[Choice] = field(default_factory=list)
    source_file: Path | None = None

    @property
    def is_ending(self) -> bool:
        """Check if this node is an ending (no choices)."""
        return len(self.choices) == 0


class ElevntyCYOAScenario:
    """
    A Choose-Your-Own-Adventure scenario.

    Loads and manages a collection of interconnected scenario nodes.
    """

    def __init__(self, scenario_dir: Path):
        """
        Initialize scenario from directory of Markdown files.

        Args:
            scenario_dir: Directory containing .md scenario files
        """
        self.scenario_dir = Path(scenario_dir)
        self.nodes: dict[str, ScenarioNode] = {}
        self.start_node_id: str | None = None

        self._load_scenario()
        self._validate_graph()

    def _load_scenario(self) -> None:
        """Load all scenario nodes from Markdown files."""
        if not self.scenario_dir.exists():
            raise FileNotFoundError(f"Scenario directory not found: {self.scenario_dir}")

        md_files = list(self.scenario_dir.glob("*.md"))
        if not md_files:
            raise ValueError(f"No .md files found in {self.scenario_dir}")

        for md_file in md_files:
            node = self._parse_markdown_file(md_file)
            self.nodes[node.id] = node

            # First node alphabetically becomes start node (or use "start.md")
            if md_file.stem == "start" or self.start_node_id is None:
                self.start_node_id = node.id

    def _parse_markdown_file(self, file_path: Path) -> ScenarioNode:
        """
        Parse a Markdown file with YAML front matter.

        Args:
            file_path: Path to .md file

        Returns:
            ScenarioNode instance
        """
        content = file_path.read_text()

        # Split front matter and content
        # Pattern: --- at start, YAML block, ---, content
        pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
        match = re.match(pattern, content, re.DOTALL)

        if not match:
            raise ValueError(
                f"Invalid format in {file_path.name}. Expected YAML front matter:\n"
                "---\ntitle: Node Title\nchoices:\n  - text: Choice text\n    path: node_id\n---\n"
                "Content here..."
            )

        front_matter_str = match.group(1)
        markdown_content = match.group(2).strip()

        # Parse YAML front matter
        try:
            front_matter = yaml.safe_load(front_matter_str)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {file_path.name}: {e}")

        # Extract title
        title = front_matter.get("title", file_path.stem)

        # Extract choices
        choices_data = front_matter.get("choices", [])
        choices = []
        for choice_data in choices_data:
            if not isinstance(choice_data, dict):
                raise ValueError(
                    f"Invalid choice format in {file_path.name}. Expected dict with 'text' and 'path'."
                )

            text = choice_data.get("text")
            path = choice_data.get("path")

            if not text or not path:
                raise ValueError(
                    f"Choice missing 'text' or 'path' in {file_path.name}:\n{choice_data}"
                )

            choices.append(Choice(text=text, path=path))

        # Create node (use filename without extension as ID)
        node_id = file_path.stem

        return ScenarioNode(
            id=node_id,
            title=title,
            content=markdown_content,
            choices=choices,
            source_file=file_path,
        )

    def _validate_graph(self) -> None:
        """
        Validate scenario graph for broken links.

        Raises:
            ValueError: If any choice paths to non-existent nodes
        """
        broken_links = []

        for node in self.nodes.values():
            for choice in node.choices:
                if choice.path not in self.nodes:
                    broken_links.append(
                        f"Node '{node.id}' has broken link: '{choice.path}' (from choice: '{choice.text}')"
                    )

        if broken_links:
            error_msg = "Scenario graph validation failed:\n" + "\n".join(broken_links)
            raise ValueError(error_msg)

    def get_node(self, node_id: str) -> ScenarioNode | None:
        """Get a node by ID."""
        return self.nodes.get(node_id)

    def get_start_node(self) -> ScenarioNode:
        """Get the starting node."""
        if self.start_node_id is None:
            raise ValueError("No start node found")
        node = self.get_node(self.start_node_id)
        if node is None:
            raise ValueError(f"Start node '{self.start_node_id}' not found")
        return node

    def run_interactive(self) -> None:
        """Run scenario interactively in the terminal."""
        current_node = self.get_start_node()
        visited_nodes = []

        console.print(
            Panel.fit(
                "[bold cyan]📖 Eleventy CYOA Scenario[/bold cyan]",
                subtitle=f"Loaded from {self.scenario_dir.name}",
            )
        )

        while True:
            visited_nodes.append(current_node.id)

            # Display current node
            console.print("\n")
            console.print(Panel(f"[bold]{current_node.title}[/bold]", style="cyan"))
            console.print(Markdown(current_node.content))

            # Check if ending
            if current_node.is_ending:
                console.print("\n[bold green]═══ THE END ═══[/bold green]\n")
                break

            # Display choices
            console.print("\n[yellow]What do you do?[/yellow]")
            for i, choice in enumerate(current_node.choices, 1):
                console.print(f"  {i}. {choice.text}")

            # Get user choice
            while True:
                choice_input = Prompt.ask(
                    "\n[bold]Enter choice number[/bold]",
                    choices=[str(i) for i in range(1, len(current_node.choices) + 1)],
                )

                try:
                    choice_idx = int(choice_input) - 1
                    selected_choice = current_node.choices[choice_idx]
                    break
                except (ValueError, IndexError):
                    console.print("[red]Invalid choice. Try again.[/red]")

            # Navigate to next node
            next_node = self.get_node(selected_choice.path)
            if next_node is None:
                console.print(
                    f"[red]Error: Node '{selected_choice.path}' not found![/red]"
                )
                break

            current_node = next_node

        # Show stats
        console.print(f"\n[dim]Nodes visited: {len(visited_nodes)}[/dim]")
        console.print(f"[dim]Path: {' → '.join(visited_nodes)}[/dim]")


class ElevntyCYOAParser:
    """Parser for Eleventy CYOA scenarios."""

    @staticmethod
    def load_scenario(scenario_dir: Path | str) -> ElevntyCYOAScenario:
        """
        Load a scenario from a directory.

        Args:
            scenario_dir: Path to directory containing .md files

        Returns:
            ElevntyCYOAScenario instance
        """
        return ElevntyCYOAScenario(Path(scenario_dir))

    @staticmethod
    def validate_scenario(scenario_dir: Path | str) -> tuple[bool, list[str]]:
        """
        Validate a scenario without running it.

        Args:
            scenario_dir: Path to directory containing .md files

        Returns:
            Tuple of (is_valid, error_messages)
        """
        try:
            ElevntyCYOAScenario(Path(scenario_dir))
            return True, []
        except Exception as e:
            return False, [str(e)]
