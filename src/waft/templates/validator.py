"""
Template Validator
==================

Validates PDF templates for correctness and completeness.
"""

import importlib
import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from .registry import TemplateMetadata


@dataclass
class ValidationResult:
    """Result of template validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]


class TemplateValidator:
    """Validates PDF templates."""
    
    def validate(self, template: TemplateMetadata) -> ValidationResult:
        """
        Validate a template.
        
        Args:
            template: TemplateMetadata to validate
            
        Returns:
            ValidationResult
        """
        errors = []
        warnings = []
        
        # Check module can be imported
        try:
            module_path = f"src.waft.templates.{template.module_name}"
            module = importlib.import_module(module_path)
        except Exception as e:
            errors.append(f"Cannot import module: {e}")
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)
        
        # Check generate function exists
        if template.generate_function:
            if not hasattr(module, template.generate_function):
                errors.append(f"Generate function '{template.generate_function}' not found")
            else:
                func = getattr(module, template.generate_function)
                if not callable(func):
                    errors.append(f"'{template.generate_function}' is not callable")
                else:
                    # Check function signature
                    sig = inspect.signature(func)
                    required_params = ["title", "content", "output_path"]
                    missing_params = [p for p in required_params if p not in sig.parameters]
                    if missing_params:
                        warnings.append(f"Missing recommended parameters: {missing_params}")
        else:
            warnings.append("No generate function found")
        
        # Check template constant exists
        if template.template_constant:
            if not hasattr(module, template.template_constant):
                errors.append(f"Template constant '{template.template_constant}' not found")
            else:
                template_str = getattr(module, template.template_constant)
                if not isinstance(template_str, str):
                    errors.append(f"'{template.template_constant}' is not a string")
                else:
                    # Basic template validation
                    if "{{" not in template_str and "{%" not in template_str:
                        warnings.append("Template string doesn't contain Jinja2 syntax")
        
        # Check docstring
        if not module.__doc__:
            warnings.append("Module missing docstring")
        
        # Check for WeasyPrint import
        if "weasyprint" not in str(module.__dict__):
            warnings.append("Module may not import WeasyPrint")
        
        # Check for Jinja2 import
        if "Template" not in str(module.__dict__) and "jinja2" not in str(module.__dict__):
            warnings.append("Module may not import Jinja2 Template")
        
        is_valid = len(errors) == 0
        return ValidationResult(is_valid=is_valid, errors=errors, warnings=warnings)
    
    def validate_all(self, templates_dir: Optional[Path] = None) -> dict:
        """
        Validate all templates.
        
        Args:
            templates_dir: Path to templates directory
            
        Returns:
            Dict mapping template names to ValidationResult
        """
        from .registry import TemplateRegistry
        
        registry = TemplateRegistry(templates_dir)
        results = {}
        
        for template in registry.list_templates():
            results[template.name] = self.validate(template)
        
        return results
