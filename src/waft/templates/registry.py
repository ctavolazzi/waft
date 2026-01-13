"""
PDF Template Registry
====================

Central registry for discovering and managing PDF templates.
Provides metadata, discovery, and validation capabilities.
"""

import importlib
import inspect
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
import re


@dataclass
class TemplateMetadata:
    """Metadata for a PDF template."""
    name: str
    module_name: str
    description: str
    category: str = "general"
    tags: List[str] = field(default_factory=list)
    generate_function: Optional[str] = None
    template_constant: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    example_usage: Optional[str] = None
    author: Optional[str] = None
    version: str = "1.0.0"
    status: str = "production"  # production, beta, deprecated


class TemplateRegistry:
    """Registry for PDF templates."""
    
    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize template registry.
        
        Args:
            templates_dir: Path to templates directory (defaults to this module's parent)
        """
        if templates_dir is None:
            templates_dir = Path(__file__).parent
        
        self.templates_dir = templates_dir
        self._templates: Dict[str, TemplateMetadata] = {}
        self._load_templates()
    
    def _load_templates(self) -> None:
        """Load all templates from the templates directory."""
        # Exclude utility modules
        excluded = {"__init__.py", "registry.py", "cli.py", "validator.py", "create.py"}
        
        for template_file in self.templates_dir.glob("*.py"):
            if template_file.name in excluded:
                continue
            
            try:
                metadata = self._extract_metadata(template_file)
                if metadata:
                    self._templates[metadata.name] = metadata
            except Exception as e:
                print(f"⚠️  Failed to load template {template_file.name}: {e}")
    
    def _extract_metadata(self, template_file: Path) -> Optional[TemplateMetadata]:
        """
        Extract metadata from a template file.
        
        Args:
            template_file: Path to template Python file
            
        Returns:
            TemplateMetadata or None if extraction fails
        """
        module_name = template_file.stem
        module_path = f"src.waft.templates.{module_name}"
        
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
                    "type": str(param.annotation) if param.annotation != inspect.Parameter.empty else "Any",
                    "required": param.default == inspect.Parameter.empty
                }
                parameters[param_name] = param_info
        
        # Find template constant (usually UPPER_SNAKE_CASE)
        template_constant = None
        for name, obj in inspect.getmembers(module):
            if isinstance(obj, str) and name.isupper() and "_TEMPLATE" in name:
                template_constant = name
                break
        
        # Extract category and tags from docstring
        category = self._extract_category(docstring, module_name)
        tags = self._extract_tags(docstring, module_name)
        
        # Generate display name
        display_name = self._generate_display_name(module_name)
        
        return TemplateMetadata(
            name=display_name,
            module_name=module_name,
            description=description,
            category=category,
            tags=tags,
            generate_function=generate_func_name,
            template_constant=template_constant,
            parameters=parameters,
            status="production"
        )
    
    def _extract_description(self, docstring: str) -> str:
        """Extract description from docstring."""
        if not docstring:
            return "No description available"
        
        lines = docstring.strip().split("\n")
        # Get first non-empty line after title
        for line in lines[1:]:
            line = line.strip()
            if line and not line.startswith("=") and not line.startswith("-"):
                return line
        
        return lines[0] if lines else "No description available"
    
    def _extract_category(self, docstring: str, module_name: str) -> str:
        """Extract category from docstring or infer from name."""
        # Look for category hints in docstring
        doc_lower = docstring.lower()
        if "field guide" in doc_lower or "manual" in doc_lower:
            return "field_guide"
        elif "lab" in doc_lower or "notebook" in doc_lower:
            return "lab_notes"
        elif "memo" in doc_lower or "personal" in doc_lower:
            return "memo"
        elif "technical" in doc_lower or "report" in doc_lower:
            return "technical"
        elif "one" in doc_lower and "page" in doc_lower:
            return "one_pager"
        
        # Infer from module name
        if "field" in module_name:
            return "field_guide"
        elif "lab" in module_name:
            return "lab_notes"
        elif "memo" in module_name:
            return "memo"
        elif "tm" in module_name or "report" in module_name:
            return "technical"
        elif "one" in module_name or "pager" in module_name:
            return "one_pager"
        
        return "general"
    
    def _extract_tags(self, docstring: str, module_name: str) -> List[str]:
        """Extract tags from docstring."""
        tags = []
        doc_lower = docstring.lower()
        
        # Common tags
        if "weasyprint" in doc_lower or "html" in doc_lower:
            tags.append("weasyprint")
        if "jinja2" in doc_lower:
            tags.append("jinja2")
        if "handwritten" in doc_lower:
            tags.append("handwritten")
        if "grid" in doc_lower:
            tags.append("grid")
        if "two-column" in doc_lower or "two column" in doc_lower:
            tags.append("two-column")
        
        # Add module name as tag
        tags.append(module_name)
        
        return tags
    
    def _generate_display_name(self, module_name: str) -> str:
        """Generate human-readable display name from module name."""
        # Convert snake_case to Title Case
        return module_name.replace("_", " ").title()
    
    def list_templates(self, category: Optional[str] = None, tag: Optional[str] = None) -> List[TemplateMetadata]:
        """
        List all templates, optionally filtered.
        
        Args:
            category: Filter by category
            tag: Filter by tag
            
        Returns:
            List of TemplateMetadata
        """
        templates = list(self._templates.values())
        
        if category:
            templates = [t for t in templates if t.category == category]
        
        if tag:
            templates = [t for t in templates if tag in t.tags]
        
        return sorted(templates, key=lambda t: t.name)
    
    def get_template(self, name: str) -> Optional[TemplateMetadata]:
        """
        Get template by name.
        
        Args:
            name: Template name (display name or module name)
            
        Returns:
            TemplateMetadata or None
        """
        # Try exact match first
        if name in self._templates:
            return self._templates[name]
        
        # Try module name match
        for template in self._templates.values():
            if template.module_name == name or template.name.lower() == name.lower():
                return template
        
        return None
    
    def get_generate_function(self, template_name: str) -> Optional[Callable]:
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
        
        module_path = f"src.waft.templates.{template.module_name}"
        try:
            module = importlib.import_module(module_path)
            return getattr(module, template.generate_function)
        except Exception:
            return None
    
    def search(self, query: str) -> List[TemplateMetadata]:
        """
        Search templates by name, description, or tags.
        
        Args:
            query: Search query
            
        Returns:
            List of matching TemplateMetadata
        """
        query_lower = query.lower()
        results = []
        
        for template in self._templates.values():
            if (query_lower in template.name.lower() or
                query_lower in template.description.lower() or
                any(query_lower in tag.lower() for tag in template.tags) or
                query_lower in template.category.lower()):
                results.append(template)
        
        return results
    
    def get_categories(self) -> List[str]:
        """Get all unique categories."""
        return sorted(set(t.category for t in self._templates.values()))
    
    def get_tags(self) -> List[str]:
        """Get all unique tags."""
        all_tags = set()
        for template in self._templates.values():
            all_tags.update(template.tags)
        return sorted(all_tags)
    
    def count(self) -> int:
        """Get total number of templates."""
        return len(self._templates)


# Global registry instance
_registry: Optional[TemplateRegistry] = None


def get_registry() -> TemplateRegistry:
    """Get the global template registry instance."""
    global _registry
    if _registry is None:
        _registry = TemplateRegistry()
    return _registry
