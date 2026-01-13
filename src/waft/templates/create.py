"""
Template Creation Utility
=========================

Utilities for creating new PDF templates.
"""

from pathlib import Path
from typing import Optional, Dict, Any


TEMPLATE_SKELETON = '''"""
{description}
{equals_line}

{features_text}
"""

from pathlib import Path
from jinja2 import Template
from weasyprint import HTML


{constant_name} = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{{{ title }}}}</title>

    <style>
        @page {{
            size: letter;
            margin: 1in;
        }}

        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #1a1a1a;
        }}

        .content {{
            margin: 0 auto;
            max-width: 6.5in;
        }}

        h1 {{
            font-size: 24pt;
            margin-bottom: 0.3in;
            border-bottom: 2px solid #333;
            padding-bottom: 0.1in;
        }}

        h2 {{
            font-size: 18pt;
            margin-top: 0.3in;
            margin-bottom: 0.15in;
        }}

        p {{
            margin-bottom: 0.15in;
        }}
    </style>
</head>
<body>
    <div class="content">
        <h1>{{{{ title }}}}</h1>
        {{{{ content }}}}
    </div>
</body>
</html>
"""


def generate_{function_name}(
    title: str,
    content: str,
    output_path: Path,
    **kwargs
) -> Path:
    """
    Generate a {display_name} PDF.

    Args:
        title: Document title
        content: Main content (HTML)
        output_path: Where to save PDF
        **kwargs: Additional template-specific parameters

    Returns:
        Path to generated PDF
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template({constant_name})
    html_output = template.render(
        title=title,
        content=content,
        **kwargs
    )

    HTML(string=html_output).write_pdf(output_path)
    return output_path
'''


def create_template(
    name: str,
    description: str,
    features: Optional[list] = None,
    output_dir: Optional[Path] = None
) -> Path:
    """
    Create a new PDF template file.
    
    Args:
        name: Template name (snake_case, e.g., "my_template")
        description: Template description
        features: List of feature descriptions
        output_dir: Directory to create template in (defaults to templates dir)
        
    Returns:
        Path to created template file
    """
    if output_dir is None:
        output_dir = Path(__file__).parent
    
    # Generate module name
    module_name = name.lower().replace(" ", "_").replace("-", "_")
    if not module_name.isidentifier():
        raise ValueError(f"Invalid template name: {name}")
    
    # Generate constant name
    constant_name = module_name.upper().replace("-", "_") + "_TEMPLATE"
    
    # Generate function name
    function_name = module_name
    
    # Generate display name
    display_name = name.replace("_", " ").replace("-", " ").title()
    
    # Format features
    if features:
        features_text = "Features:\n" + "\n".join(f"- {f}" for f in features)
    else:
        features_text = ""
    
    # Generate equals line
    equals_line = "=" * len(description)
    
    # Generate template content
    template_content = TEMPLATE_SKELETON.format(
        description=description,
        equals_line=equals_line,
        features_text=features_text,
        constant_name=constant_name,
        function_name=function_name,
        display_name=display_name
    )
    
    # Write template file
    template_file = output_dir / f"{module_name}.py"
    template_file.write_text(template_content)
    
    return template_file


def create_template_interactive() -> Path:
    """Interactively create a new template."""
    print("📄 Create New PDF Template\n")
    
    # Get name
    name = input("Template name (snake_case, e.g., 'my_template'): ").strip()
    if not name:
        raise ValueError("Template name is required")
    
    # Get description
    description = input("Description: ").strip()
    if not description:
        description = f"{name.replace('_', ' ').title()} Template"
    
    # Get features
    print("\nEnter features (one per line, empty line to finish):")
    features = []
    while True:
        feature = input("  Feature: ").strip()
        if not feature:
            break
        features.append(feature)
    
    # Create template
    template_file = create_template(
        name=name,
        description=description,
        features=features if features else None
    )
    
    print(f"\n✅ Created template: {template_file}")
    print(f"\nNext steps:")
    print(f"  1. Edit {template_file} to customize the template")
    print(f"  2. Test with: python -m src.waft.templates.cli show {name}")
    print(f"  3. Validate with: python -m src.waft.templates.cli validate --name {name}")
    
    return template_file
