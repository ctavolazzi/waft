"""
Typst Template Registry
=======================

Central registry for discovering and managing Typst templates.
Auto-discovers wrapper modules by scanning for generate_* functions.
"""

import importlib
import inspect
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class TypstTemplateMetadata:
    """Metadata for a Typst template."""

    name: str
    module_name: str
    description: str
    category: str = "general"
    tags: list[str] = field(default_factory=list)
    generate_function: str | None = None
    parameters: dict[str, Any] = field(default_factory=dict)
    example_usage: str | None = None
    author: str | None = None
    version: str = "1.0.0"
    status: str = "production"  # production, beta, deprecated
    source_repo: str | None = None  # e.g., "lapreprint", "dnd5e", "wenyuan"


class TypstTemplateRegistry:
    """Registry for Typst templates with auto-discovery."""

    def __init__(self, wrappers_dir: Path | None = None):
        """
        Initialize Typst template registry.

        Args:
            wrappers_dir: Path to wrappers directory (defaults to this module's parent/wrappers)
        """
        if wrappers_dir is None:
            wrappers_dir = Path(__file__).parent / "wrappers"

        self.wrappers_dir = wrappers_dir
        self._templates: dict[str, TypstTemplateMetadata] = {}
        self._load_templates()

    def _load_templates(self) -> None:
        """Load all templates from the wrappers directory."""
        if not self.wrappers_dir.exists():
            return

        excluded = {"__init__.py", "__pycache__"}

        for wrapper_file in self.wrappers_dir.glob("*.py"):
            if wrapper_file.name in excluded:
                continue

            try:
                metadata = self._extract_metadata(wrapper_file)
                if metadata:
                    self._templates[metadata.name] = metadata
            except Exception as e:
                print(f"⚠️  Failed to load Typst template {wrapper_file.name}: {e}")

    def _extract_metadata(self, wrapper_file: Path) -> TypstTemplateMetadata | None:
        """
        Extract metadata from a wrapper file.

        Args:
            wrapper_file: Path to wrapper Python file

        Returns:
            TypstTemplateMetadata or None if extraction fails
        """
        module_name = wrapper_file.stem
        module_path = f"src.waft.templates.typst.wrappers.{module_name}"

        try:
            module = importlib.import_module(module_path)
        except Exception as e:
            print(f"⚠️  Could not import {module_path}: {e}")
            return None

        # Extract docstring
        docstring = module.__doc__ or ""
        description = self._extract_description(docstring)

        # Find generate function
        generate_func = None
        generate_func_name = None
        for name, obj in inspect.getmembers(module, inspect.isfunction):
            if name.startswith("generate_"):
                generate_func = obj
                generate_func_name = name
                break

        if not generate_func:
            return None  # No generate function found

        # Extract parameters from generate function
        parameters = {}
        if generate_func:
            sig = inspect.signature(generate_func)
            for param_name, param in sig.parameters.items():
                if param_name in ["output_path", "title", "content"]:
                    continue  # Skip common required params
                param_info = {
                    "name": param_name,
                    "default": param.default if param.default != inspect.Parameter.empty else None,
                    "type": str(param.annotation)
                    if param.annotation != inspect.Parameter.empty
                    else "Any",
                    "required": param.default == inspect.Parameter.empty,
                }
                parameters[param_name] = param_info

        # Extract category and tags from docstring
        category = self._extract_category(docstring, module_name)
        tags = self._extract_tags(docstring, module_name)

        # Extract source repo from module name or docstring
        source_repo = self._extract_source_repo(module_name, docstring)

        # Generate display name
        display_name = self._generate_display_name(module_name)

        return TypstTemplateMetadata(
            name=display_name,
            module_name=module_name,
            description=description,
            category=category,
            tags=tags,
            generate_function=generate_func_name,
            parameters=parameters,
            source_repo=source_repo,
        )

    def _extract_description(self, docstring: str) -> str:
        """Extract description from docstring."""
        if not docstring:
            return ""

        # Get first paragraph
        lines = docstring.strip().split("\n")
        description_lines = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("Args:") or line.startswith("Returns:"):
                break
            description_lines.append(line)

        return " ".join(description_lines).strip()

    def _extract_category(self, docstring: str, module_name: str) -> str:
        """Extract category from docstring or infer from module name."""
        # Look for category in docstring
        category_match = re.search(r"category:\s*(\w+)", docstring, re.IGNORECASE)
        if category_match:
            return category_match.group(1).lower()

        # Infer from module name
        module_lower = module_name.lower()
        if "preprint" in module_lower or "academic" in module_lower:
            return "preprint"
        elif "dnd" in module_lower or "rpg" in module_lower or "campaign" in module_lower:
            return "rpg"
        elif "cv" in module_lower or "resume" in module_lower:
            return "cv"
        elif "thesis" in module_lower:
            return "thesis"
        elif "report" in module_lower:
            return "report"
        elif "presentation" in module_lower:
            return "presentation"
        elif "essay" in module_lower:
            return "essay"
        elif "assignment" in module_lower:
            return "assignment"
        elif "paper" in module_lower:
            return "paper"
        else:
            return "general"

    def _extract_tags(self, docstring: str, module_name: str) -> list[str]:
        """Extract tags from docstring."""
        tags = []

        # Look for tags in docstring
        tags_match = re.search(r"tags?:\s*\[(.*?)\]", docstring, re.IGNORECASE)
        if tags_match:
            tags_str = tags_match.group(1)
            tags.extend([t.strip().strip("\"'") for t in tags_str.split(",")])

        # Add inferred tags from module name
        module_lower = module_name.lower()
        if "typst" not in tags:
            tags.append("typst")
        if "pdf" not in tags:
            tags.append("pdf")

        return tags

    def _extract_source_repo(self, module_name: str, docstring: str) -> str | None:
        """Extract source repository from module name or docstring."""
        # Check docstring for source repo
        repo_match = re.search(r"source[:\s]+(\w+)", docstring, re.IGNORECASE)
        if repo_match:
            return repo_match.group(1).lower()

        # Infer from module name patterns
        module_lower = module_name.lower()
        if "lapreprint" in module_lower or "preprint" in module_lower:
            return "lapreprint"
        elif "dnd5e" in module_lower or "dnd" in module_lower:
            return "dnd5e"
        elif "wenyuan" in module_lower or "campaign" in module_lower:
            return "wenyuan"

        return None

    def _generate_display_name(self, module_name: str) -> str:
        """Generate display name from module name."""
        # Convert snake_case to Title Case
        parts = module_name.split("_")
        return " ".join(word.capitalize() for word in parts)

    def list_templates(self) -> list[TypstTemplateMetadata]:
        """List all registered templates."""
        return list(self._templates.values())

    def get_template(self, name: str) -> TypstTemplateMetadata | None:
        """
        Get template by name.

        Args:
            name: Template name (case-insensitive)

        Returns:
            TypstTemplateMetadata or None
        """
        name_lower = name.lower()
        for template in self._templates.values():
            if template.name.lower() == name_lower or template.module_name.lower() == name_lower:
                return template
        return None

    def get_generate_function(self, template_name: str) -> Callable | None:
        """
        Get the generate function for a template.

        Args:
            template_name: Template name

        Returns:
            Generate function or None
        """
        template = self.get_template(template_name)
        if not template or not template.generate_function:
            return None

        module_path = f"src.waft.templates.typst.wrappers.{template.module_name}"
        try:
            module = importlib.import_module(module_path)
            return getattr(module, template.generate_function)
        except Exception:
            return None

    def search(self, query: str) -> list[TypstTemplateMetadata]:
        """
        Search templates by name, description, or tags.

        Args:
            query: Search query

        Returns:
            List of matching TypstTemplateMetadata
        """
        query_lower = query.lower()
        results = []

        for template in self._templates.values():
            if (
                query_lower in template.name.lower()
                or query_lower in template.description.lower()
                or any(query_lower in tag.lower() for tag in template.tags)
                or query_lower in template.category.lower()
            ):
                results.append(template)

        return results

    def get_categories(self) -> list[str]:
        """Get all unique categories."""
        return sorted(set(t.category for t in self._templates.values()))

    def get_tags(self) -> list[str]:
        """Get all unique tags."""
        all_tags = set()
        for template in self._templates.values():
            all_tags.update(template.tags)
        return sorted(all_tags)

    def count(self) -> int:
        """Get total number of templates."""
        return len(self._templates)


# Global registry instance
_registry: TypstTemplateRegistry | None = None


def get_typst_registry() -> TypstTemplateRegistry:
    """Get the global Typst template registry instance."""
    global _registry
    if _registry is None:
        _registry = TypstTemplateRegistry()
    return _registry
