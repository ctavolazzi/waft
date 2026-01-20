"""
Template Metadata Extractor
============================

Helper module for extracting metadata from Typst template README files.
"""

import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class TemplateMetadata:
    """Extracted metadata from a template README."""
    name: str
    description: str = ""
    usage_instructions: str = ""
    configuration: Dict[str, Any] = field(default_factory=dict)
    parameters: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    category: str = "general"
    tags: List[str] = field(default_factory=list)


def extract_metadata(readme_content: str, template_name: str) -> TemplateMetadata:
    """
    Extract metadata from a template README file.
    
    Args:
        readme_content: Content of the README.md file
        template_name: Name of the template
        
    Returns:
        TemplateMetadata object with extracted information
    """
    metadata = TemplateMetadata(name=template_name)
    
    # Extract description (first paragraph after title)
    description_match = re.search(
        r'^#\s+\S+\s*\n\n([^\n]+(?:\n[^\n]+)*?)(?:\n\n|##)',
        readme_content,
        re.MULTILINE | re.DOTALL
    )
    if description_match:
        metadata.description = description_match.group(1).strip()
    
    # Extract usage section
    usage_match = re.search(
        r'##\s+Usage\s*\n\n(.*?)(?=\n##|\Z)',
        readme_content,
        re.MULTILINE | re.DOTALL
    )
    if usage_match:
        metadata.usage_instructions = usage_match.group(1).strip()
    
    # Extract configuration section
    config_match = re.search(
        r'##\s+Configuration\s*\n\n(.*?)(?=\n##|\Z)',
        readme_content,
        re.MULTILINE | re.DOTALL
    )
    if config_match:
        config_text = config_match.group(1)
        metadata.configuration["raw"] = config_text
        
        # Extract parameter list (look for bullet points or numbered lists)
        param_pattern = r'[-*]\s*`([^`]+)`:\s*(.+?)(?=\n[-*]|\n\n|$)'
        params = re.findall(param_pattern, config_text, re.MULTILINE)
        for param_name, param_desc in params:
            metadata.parameters.append({
                "name": param_name,
                "description": param_desc.strip()
            })
    
    # Extract code examples
    code_blocks = re.findall(
        r'```(?:typ|typst)?\n(.*?)```',
        readme_content,
        re.MULTILINE | re.DOTALL
    )
    metadata.examples = code_blocks
    
    # Infer category from template name
    name_lower = template_name.lower()
    if "letter" in name_lower:
        metadata.category = "letter"
    elif "book" in name_lower:
        metadata.category = "book"
    elif "paper" in name_lower or "ieee" in name_lower or "ams" in name_lower:
        metadata.category = "academic"
    elif "news" in name_lower or "newsletter" in name_lower:
        metadata.category = "newsletter"
    elif "form" in name_lower:
        metadata.category = "form"
    elif "game" in name_lower:
        metadata.category = "game"
    elif "word" in name_lower:
        metadata.category = "word"
    
    # Add default tags
    metadata.tags = ["typst", "official", metadata.category]
    
    return metadata


def format_metadata_markdown(metadata: TemplateMetadata) -> str:
    """
    Format template metadata as markdown.
    
    Args:
        metadata: TemplateMetadata object
        
    Returns:
        Formatted markdown string
    """
    lines = [
        f"### {metadata.name}",
        "",
        f"**Category:** {metadata.category}",
        f"**Tags:** {', '.join(metadata.tags)}",
        "",
    ]
    
    if metadata.description:
        lines.extend([
            "**Description:**",
            metadata.description,
            "",
        ])
    
    if metadata.usage_instructions:
        lines.extend([
            "**Usage:**",
            metadata.usage_instructions,
            "",
        ])
    
    if metadata.parameters:
        lines.extend([
            "**Parameters:**",
            "",
        ])
        for param in metadata.parameters:
            if isinstance(param, dict):
                lines.append(f"- `{param['name']}`: {param['description']}")
            else:
                lines.append(f"- `{param}`")
        lines.append("")
    
    if metadata.examples:
        lines.extend([
            "**Example:**",
            "```typst",
            metadata.examples[0] if metadata.examples else "",
            "```",
            "",
        ])
    
    return "\n".join(lines)
