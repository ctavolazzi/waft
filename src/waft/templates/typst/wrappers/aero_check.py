"""
Aero-Check Typst Template Wrapper
==================================

Python wrapper for aero-check Typst template to generate aviation-inspired checklists.

Uses:
- @preview/aero-check:0.1.1 - Checklist template
- @preview/umbra:0.1.1 - Gradient shadows (optional)

Category: checklist
Tags: [typst, checklist, aviation, umbra, shadows]
Source: typst-templates
"""

from pathlib import Path
from typing import Literal, Optional, List, Tuple
from dataclasses import dataclass, field

from ..compiler import TypstCompiler


# Type definitions
ChecklistStyle = Literal[0, 1]


@dataclass
class ChecklistStep:
    """A single step in a checklist."""
    text: str
    status: str = "Check"
    
    def __post_init__(self):
        """Validate step data."""
        if not self.text or not isinstance(self.text, str):
            raise ValueError("Step text must be a non-empty string")
        if not self.status or not isinstance(self.status, str):
            raise ValueError("Step status must be a non-empty string")


@dataclass
class ChecklistSection:
    """A section containing multiple steps."""
    name: str
    steps: List[ChecklistStep] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate section data."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Section name must be a non-empty string")
        if not isinstance(self.steps, list):
            raise ValueError("Steps must be a list")


@dataclass
class ChecklistTopic:
    """A topic containing multiple sections."""
    name: str
    sections: List[ChecklistSection] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate topic data."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Topic name must be a non-empty string")
        if not isinstance(self.sections, list):
            raise ValueError("Sections must be a list")


@dataclass
class ShadowConfig:
    """Configuration for umbra shadow effects."""
    enabled: bool = False
    radius: float = 0.5  # in cm
    shadow_stops: Tuple[str, str] = ("gray", "white")
    correction: float = 5.0  # in degrees
    
    def __post_init__(self):
        """Validate shadow configuration."""
        if not isinstance(self.radius, (int, float)) or self.radius < 0:
            raise ValueError("Shadow radius must be a non-negative number")
        if not isinstance(self.shadow_stops, tuple) or len(self.shadow_stops) != 2:
            raise ValueError("Shadow stops must be a tuple of two color strings")
        if not isinstance(self.correction, (int, float)):
            raise ValueError("Correction must be a number")


def _sanitize_typst_content(content: str) -> str:
    """
    Sanitize user-provided content to prevent Typst injection.
    
    Escapes special Typst characters that could be used for code injection.
    
    Args:
        content: User-provided content string
        
    Returns:
        Sanitized content string
    """
    if not content:
        return ""
    
    # Escape special Typst characters
    # Note: Typst uses # for commands, { } for blocks, [ ] for arguments, ( ) for functions
    # We escape these to prevent injection
    replacements = {
        "#": r"\#",
        "{": r"\{",
        "}": r"\}",
        "[": r"\[",
        "]": r"\]",
        "(": r"\(",
        ")": r"\)",
    }
    
    sanitized = content
    for char, escaped in replacements.items():
        sanitized = sanitized.replace(char, escaped)
    
    return sanitized


def _build_step_typst(step: ChecklistStep) -> str:
    """
    Build Typst code for a single step.
    
    Args:
        step: ChecklistStep object
        
    Returns:
        Typst code string for the step
    """
    sanitized_text = _sanitize_typst_content(step.text)
    sanitized_status = _sanitize_typst_content(step.status)
    return f'#step("{sanitized_text}", "{sanitized_status}")'


def _build_section_typst(section: ChecklistSection) -> str:
    """
    Build Typst code for a section with steps.
    
    Args:
        section: ChecklistSection object
        
    Returns:
        Typst code string for the section
    """
    sanitized_name = _sanitize_typst_content(section.name)
    
    typst_lines = [f'#section("{sanitized_name}")[']
    
    for step in section.steps:
        typst_lines.append(f"  {_build_step_typst(step)}")
    
    typst_lines.append("]")
    
    return "\n".join(typst_lines)


def _build_topic_typst(
    topic: ChecklistTopic,
    use_shadows: bool = False,
    shadow_config: Optional[ShadowConfig] = None
) -> str:
    """
    Build Typst code for a topic with sections and steps.
    
    Args:
        topic: ChecklistTopic object
        use_shadows: Whether to add shadow effects to topic header
        shadow_config: Shadow configuration (used if use_shadows is True)
        
    Returns:
        Typst code string for the topic
    """
    sanitized_name = _sanitize_typst_content(topic.name)
    
    typst_lines = []
    
    # Add shadowed header if shadows are enabled
    if use_shadows and shadow_config:
        # Build shadow-path call for topic header
        shadow_radius = shadow_config.radius
        color1, color2 = shadow_config.shadow_stops
        correction = shadow_config.correction
        
        typst_lines.append("#align(center)[")
        typst_lines.append(f"  #shadow-path(")
        typst_lines.append(f"    (2%, 2%), (2%, 98%), (98%, 98%), (98%, 2%),")
        typst_lines.append(f"    closed: true,")
        typst_lines.append(f"    shadow-radius: {shadow_radius}cm,")
        # Handle color strings - Typst colors need to be unquoted for method calls
        # If it's already an expression (has . or rgb(), use as-is
        # Otherwise, treat as color name (unquoted) and add lighten
        if '.' in color1 or color1.startswith('rgb('):
            # Already a Typst expression, use directly
            color1_str = color1
        else:
            # Simple color name, use unquoted and add lighten
            color1_str = f'{color1}.lighten(40%)'
        
        if '.' in color2 or color2.startswith('rgb('):
            color2_str = color2
        else:
            # Simple color name, use unquoted
            color2_str = color2
        
        typst_lines.append(f"    shadow-stops: ({color1_str}, {color2_str}),")
        typst_lines.append(f"    correction: {correction}deg")
        typst_lines.append(f"  )")
        typst_lines.append(f"  #pad(x: 2cm, y: 0.6cm)[")
        typst_lines.append(f'    #text(size: 16pt, weight: "bold", fill: gray.darken(30%))[')
        typst_lines.append(f"      {sanitized_name}")
        typst_lines.append(f"    ]")
        typst_lines.append(f"  ]")
        typst_lines.append("]")
        typst_lines.append("#v(0.5cm)")
    
    # Build topic with sections
    typst_lines.append(f'#topic("{sanitized_name}")[')
    
    for section in topic.sections:
        typst_lines.append(_build_section_typst(section))
        typst_lines.append("")
    
    typst_lines.append("]")
    
    return "\n".join(typst_lines)


def generate_aero_checklist(
    title: str,
    topics: List[ChecklistTopic],
    output_path: Path,
    disclaimer: Optional[str] = None,
    style: ChecklistStyle = 0,
    use_shadows: bool = False,
    shadow_config: Optional[ShadowConfig] = None,
    **kwargs
) -> Path:
    """
    Generate PDF using aero-check Typst template.
    
    Creates aviation-inspired checklists with optional umbra shadow enhancements.
    
    Args:
        title: Document title
        topics: List of ChecklistTopic objects containing sections and steps
        output_path: Where to save PDF
        disclaimer: Optional disclaimer text (shown below title)
        style: Checklist style (0 or 1)
        use_shadows: Whether to enable umbra shadow effects
        shadow_config: Shadow configuration (used if use_shadows is True)
        **kwargs: Additional template parameters (currently unused)
        
    Returns:
        Path to generated PDF
        
    Raises:
        ValueError: If invalid data provided
        RuntimeError: If Typst compilation fails
    """
    # Validate inputs
    if not title or not isinstance(title, str):
        raise ValueError("Title must be a non-empty string")
    if not topics or not isinstance(topics, list):
        raise ValueError("Topics must be a non-empty list")
    if not all(isinstance(t, ChecklistTopic) for t in topics):
        raise ValueError("All topics must be ChecklistTopic instances")
    if style not in (0, 1):
        raise ValueError("Style must be 0 or 1")
    
    # Use default shadow config if shadows enabled but no config provided
    if use_shadows and shadow_config is None:
        shadow_config = ShadowConfig(enabled=True)
    
    # Sanitize title and disclaimer
    sanitized_title = _sanitize_typst_content(title)
    sanitized_disclaimer = _sanitize_typst_content(disclaimer) if disclaimer else ""
    
    # Build Typst content
    typst_parts = []
    
    # Import aero-check package
    typst_parts.append('#import "@preview/aero-check:0.1.1": *')
    
    # Import umbra if shadows are enabled
    if use_shadows:
        typst_parts.append('#import "@preview/umbra:0.1.1": shadow-path')
    
    typst_parts.append("")
    
    # Set up checklist with title and disclaimer
    disclaimer_param = f'disclaimer: "{sanitized_disclaimer}",' if sanitized_disclaimer else ""
    typst_parts.append(f"#show: checklist.with(")
    typst_parts.append(f'  title: "{sanitized_title}",')
    if disclaimer_param:
        typst_parts.append(f"  {disclaimer_param}")
    typst_parts.append(f"  style: {style},")
    typst_parts.append(")")
    typst_parts.append("")
    
    # Add topics with column breaks between them
    for i, topic in enumerate(topics):
        if i > 0:
            typst_parts.append("#colbreak()")
            typst_parts.append("")
        
        typst_parts.append(_build_topic_typst(topic, use_shadows, shadow_config))
        typst_parts.append("")
    
    # Combine all parts
    typst_content = "\n".join(typst_parts)
    
    # Compile to PDF
    compiler = TypstCompiler()
    pdf_path = compiler.compile(typst_content, output_path)
    
    return pdf_path
